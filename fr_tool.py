#!/usr/bin/env python3
"""fr_tool.py - search and read the U.S. Federal Register.

This is the ONLY research tool available in this task. It talks to the public
Federal Register API (federalregister.gov) and, for full text, falls back to
GovInfo (govinfo.gov) when federalregister.gov blocks automated text downloads.
Python 3.8+ standard library only.

Commands
--------
  search   Search Federal Register documents (rules, proposed rules, notices,
           presidential documents) by keyword and filters.
  doc      Show metadata for one document (title, dates, citation, abstract,
           CFR parts affected, docket, RIN, corrections, page range...).
  toc      Show an outline (headings with line numbers) of a document's text.
  text     Print a document's full text, by line range, with line numbers.
  grep     Regex search inside one document's full text, with context. The
           regex runs over the whole text, so a match may span lines.

Examples
--------
  python fr_tool.py search "duration of status" --type RULE --since 2025-01-01
  python fr_tool.py search "H-1B" --type PRESDOCU --since 2026-01-01 --order newest
  python fr_tool.py search "" --agency homeland-security-department --cfr 8:214
  python fr_tool.py doc 2026-14439
  python fr_tool.py toc 2026-14439
  python fr_tool.py grep 2026-14439 "within 5 months" --context 3
  python fr_tool.py text 2026-14439 --start 18300 --lines 200

Documents are identified by their FR document number (e.g. 2026-14439), which
`search` prints. Full texts are cached locally after the first download.
Run `python fr_tool.py <command> -h` for all options of a command.

Reproducibility
---------------
  FR_TOOL_AS_OF=YYYY-MM-DD  Hide every document published after this date:
      `search` never returns one and the other commands report it as not found.
  FR_TOOL_SNAPSHOT=DIR      Read-only store of full texts (default: corpus/ next
      to this script), consulted before the cache (FR_TOOL_CACHE). Both hold
      <number>.txt plus <number>.json (publication date, source, sha256), so a
      cached document becomes part of the snapshot by copying its two files.

Library use
-----------
  import fr_tool
  print(fr_tool.search("duration of status", doc_type="RULE", since="2025-01-01"))
  print(fr_tool.grep("2026-14439", "within 5 months", context=3))

search(), doc(), toc(), text() and grep() return the same text the CLI prints.
They raise FRToolError (instead of exiting) on bad input or failed downloads.
"""

import argparse
import bisect
import datetime
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.federalregister.gov/api/v1"
GOVINFO_HTML = "https://www.govinfo.gov/content/pkg/FR-{date}/html/{num}.htm"
USER_AGENT = "fr_tool/1.0 (policy-research benchmark; stdlib urllib)"
CACHE_DIR = os.environ.get(
    "FR_TOOL_CACHE", os.path.join(os.path.expanduser("~"), ".cache", "fr_tool")
)
SNAPSHOT_DIR = os.environ.get(
    "FR_TOOL_SNAPSHOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")
)
# Documents published after this date (YYYY-MM-DD) are treated as nonexistent.
AS_OF = os.environ.get("FR_TOOL_AS_OF") or None
TIMEOUT = 90
ORDERS = ["relevance", "newest", "oldest", "executive_order_number"]

DOC_TYPES = {
    "RULE": "Rule",
    "PRORULE": "Proposed Rule",
    "NOTICE": "Notice",
    "PRESDOCU": "Presidential Document",
}
PRES_TYPES = ["determination", "executive_order", "memorandum", "notice",
              "proclamation", "presidential_order", "other"]


class FRToolError(Exception):
    """Bad input or a document that cannot be found or downloaded."""


class FRNotFound(FRToolError):
    """No such document (or it was published after AS_OF)."""


class FRNetworkError(FRToolError):
    """An HTTP request or download failed; the caller's input is not at fault."""


# Full texts read in this process: document number -> where the text came from.
LOADED = {}


def _as_list(v):
    if v is None:
        return []
    return [v] if isinstance(v, str) else list(v)


def _iso_date(label, v):
    if not v:
        return None
    try:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError(v)
        return datetime.date.fromisoformat(v).isoformat()
    except ValueError:
        raise FRToolError("%s must be YYYY-MM-DD, got %r" % (label, v)) from None


def _hidden(publication_date):
    return bool(AS_OF and publication_date and publication_date > AS_OF)


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
def _http_get(url, retries=3):
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.geturl(), resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if e.code in (400, 422):
                raise FRToolError("The Federal Register API rejected the request (HTTP %d): %s"
                                  % (e.code, _rejection_detail(e))) from None
            last = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise FRNetworkError("request failed after %d tries: %s (%s)" % (retries, url, last))


def _rejection_detail(e):
    """What the API said was wrong, e.g. 'agencies: invalid value'."""
    try:
        body = e.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return str(e.reason)
    try:
        errors = json.loads(body).get("errors")
        if isinstance(errors, dict):
            return "; ".join("%s: %s" % kv for kv in errors.items())
    except (ValueError, AttributeError):
        pass
    return re.sub(r"\s+", " ", body).strip()[:300] or str(e.reason)


def _api(path, params=None):
    query = ""
    if params:
        query = "?" + urllib.parse.urlencode(params, doseq=True)
    _, body = _http_get(API + path + query)
    return json.loads(body.decode("utf-8"))


# --------------------------------------------------------------------------- #
# search
# --------------------------------------------------------------------------- #
SEARCH_FIELDS = ["document_number", "title", "type", "publication_date",
                 "citation", "agencies", "abstract", "effective_on",
                 "docket_ids", "regulation_id_numbers", "subtype", "action",
                 "presidential_document_number", "signing_date",
                 "executive_order_number"]


def search(query="", doc_type=None, agency=None, pres_type=None, since=None,
           until=None, docket=None, rin=None, cfr=None, significant=False,
           order="relevance", per_page=10, page=1, brief=False):
    """Search Federal Register documents. Returns the formatted result list.

    doc_type, agency and pres_type accept a string or a list of strings.
    """
    types = [t.upper() for t in _as_list(doc_type)]
    for t in types:
        if t not in DOC_TYPES:
            raise FRToolError("type must be one of %s, got %r" % (", ".join(DOC_TYPES), t))
    pres_types = _as_list(pres_type)
    for pt in pres_types:
        if pt not in PRES_TYPES:
            raise FRToolError("pres_type must be one of %s, got %r" % (", ".join(PRES_TYPES), pt))
    if order not in ORDERS:
        raise FRToolError("order must be one of %s, got %r" % (", ".join(ORDERS), order))
    per_page = max(1, min(50, int(per_page)))
    page = max(1, int(page))
    since, until = _iso_date("since", since), _iso_date("until", until)
    if AS_OF and (not until or until > AS_OF):
        until = AS_OF

    p = [("per_page", per_page), ("page", page), ("order", order)]
    p += [("fields[]", f) for f in SEARCH_FIELDS]
    if query:
        p.append(("conditions[term]", query))
    for t in types:
        p.append(("conditions[type][]", t))
    for ag in _as_list(agency):
        p.append(("conditions[agencies][]", ag))
    for pt in pres_types:
        p.append(("conditions[presidential_document_type][]", pt))
    if since:
        p.append(("conditions[publication_date][gte]", since))
    if until:
        p.append(("conditions[publication_date][lte]", until))
    if docket:
        p.append(("conditions[docket_id]", docket))
    if rin:
        p.append(("conditions[regulation_id_number]", rin))
    if cfr:
        m = re.match(r"^(\d+):(\d+)$", cfr)
        if not m:
            raise FRToolError("--cfr must look like TITLE:PART with a numeric part, e.g. 8:214. "
                              "Lettered parts are not supported by this filter; search by "
                              "keyword instead.")
        p += [("conditions[cfr][title]", m.group(1)),
              ("conditions[cfr][part]", m.group(2))]
    if significant:
        p.append(("conditions[significant]", 1))

    data = _api("/documents.json", p)
    total = data.get("count", 0)
    results = data.get("results") or []
    pages = data.get("total_pages", 1)
    out = ["Found %d document(s); page %d of %s (%d shown)\n"
           % (total, page, pages, len(results))]
    for i, r in enumerate(results, 1 + (page - 1) * per_page):
        agencies = ", ".join(x.get("name") or x.get("raw_name", "")
                             for x in r.get("agencies") or [])
        line2 = ["type: " + (r.get("subtype") or r.get("type") or "?"),
                 "published: " + str(r.get("publication_date"))]
        if r.get("citation"):
            line2.append(r["citation"])
        if r.get("effective_on"):
            line2.append("effective: " + r["effective_on"])
        if r.get("signing_date"):
            line2.append("signed: " + r["signing_date"])
        out.append("%d. [%s] %s" % (i, r.get("document_number"), r.get("title")))
        out.append("   " + " | ".join(line2))
        if r.get("action"):
            out.append("   action: " + r["action"])
        if agencies:
            out.append("   agencies: " + agencies)
        extra = []
        if r.get("docket_ids"):
            extra.append("docket: " + "; ".join(r["docket_ids"]))
        if r.get("regulation_id_numbers"):
            extra.append("RIN: " + "; ".join(r["regulation_id_numbers"]))
        if r.get("presidential_document_number"):
            extra.append("pres. doc no.: " + str(r["presidential_document_number"]))
        if extra:
            out.append("   " + " | ".join(extra))
        if r.get("abstract") and not brief:
            ab = re.sub(r"\s+", " ", r["abstract"]).strip()
            if len(ab) > 400:
                ab = ab[:400].rsplit(" ", 1)[0] + " ..."
            out.append("   abstract: " + ab)
        out.append("")
    if pages and page < pages:
        out.append("(more results: rerun with --page %d)" % (page + 1))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# doc
# --------------------------------------------------------------------------- #
DOC_FIELDS = SEARCH_FIELDS + [
    "dates", "start_page", "end_page", "page_length", "cfr_references",
    "html_url", "pdf_url", "comments_close_on", "corrections", "correction_of",
    "significant", "topics", "signing_date", "disposition_notes",
    "regulations_dot_gov_info", "comment_url", "volume", "toc_subject",
    "toc_doc",
]


def _get_meta(num, fields=None):
    p = [("fields[]", f) for f in fields or DOC_FIELDS + ["raw_text_url"]]
    not_found = FRNotFound("No Federal Register document with number %r." % num)
    try:
        m = _api("/documents/%s.json" % urllib.parse.quote(num), p)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise not_found from None
        raise
    if _hidden(m.get("publication_date")):
        raise not_found
    return m


def _visible_corrections(m):
    """Document numbers of corrections to `m`, minus any published after AS_OF."""
    nums = [c.rstrip("/").split("/")[-1] if isinstance(c, str) else str(c)
            for c in m.get("corrections") or []]
    if not AS_OF:
        return nums
    out = []
    for n in nums:
        try:
            _get_meta(n, fields=["publication_date"])
        except FRNotFound:
            continue
        out.append(n)
    return out


def doc(document_number):
    """Metadata for one document (dates, citation, docket, RIN, CFR parts...)."""
    m = _get_meta(document_number)
    out = []

    def add(label, val):
        if val not in (None, "", [], {}):
            out.append("%-18s %s" % (label + ":", val))

    add("Document number", m.get("document_number"))
    add("Title", m.get("title"))
    add("Type", m.get("subtype") or m.get("type"))
    add("Action", m.get("action"))
    add("Agencies", ", ".join(x.get("name") or x.get("raw_name", "")
                               for x in m.get("agencies") or []))
    add("Citation", m.get("citation"))
    if m.get("start_page"):
        add("Pages", "%s-%s (%s pages)" % (m.get("start_page"), m.get("end_page"),
                                           m.get("page_length")))
    add("Published", m.get("publication_date"))
    add("Signed", m.get("signing_date"))
    add("Effective", m.get("effective_on"))
    add("Comments close", m.get("comments_close_on"))
    add("Dates", re.sub(r"\s+", " ", m.get("dates") or "").strip())
    add("Docket", "; ".join(m.get("docket_ids") or []))
    add("RIN", "; ".join(m.get("regulation_id_numbers") or []))
    add("Pres. doc no.", m.get("presidential_document_number"))
    add("EO number", m.get("executive_order_number"))
    add("Significant", m.get("significant"))
    cfr = ["%s CFR %s" % (c.get("title"), c.get("part"))
           for c in m.get("cfr_references") or []]
    add("CFR affected", ", ".join(cfr))
    add("Topics", ", ".join(m.get("topics") or []))
    add("Correction of", m.get("correction_of"))
    add("Corrections", ", ".join(_visible_corrections(m)))
    add("Disposition", m.get("disposition_notes"))
    add("URL", m.get("html_url"))
    add("PDF", m.get("pdf_url"))
    if m.get("abstract"):
        out.append("\nAbstract:\n" + re.sub(r"\s+", " ", m["abstract"]).strip())
    out.append("\nUse `toc`, `grep` or `text` with this document number to read the full text.")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# full text (with cache)
# --------------------------------------------------------------------------- #
def _clean_text(raw):
    t = re.sub(r"<[^>]+>", "", raw)
    t = html.unescape(t)
    t = "".join(ch if (ch in "\n\t" or ord(ch) >= 32) else " " for ch in t)
    t = t.replace("\r\n", "\n")
    return t.strip("\n") + "\n"


def _looks_blocked(final_url, body):
    if "unblock.federalregister.gov" in (final_url or ""):
        return True
    head = body[:4000].decode("utf-8", "replace").lower()
    return "captcha" in head or "request access" in head and len(body) < 20000


def _stored_text(num):
    """(text, record) from the snapshot or the cache, or None if in neither."""
    name = re.sub(r"[^\w.-]", "_", num)
    for origin, d in (("snapshot", SNAPSHOT_DIR), ("cache", CACHE_DIR)):
        tpath, rpath = os.path.join(d, name + ".txt"), os.path.join(d, name + ".json")
        # The record is written last, so a text without one is incomplete.
        if os.path.exists(tpath) and os.path.exists(rpath):
            with open(tpath, encoding="utf-8") as f:
                text = f.read()
            with open(rpath, encoding="utf-8") as f:
                record = json.load(f)
            return text, dict(record, origin=origin)
    return None


def _download_text(num):
    """(text, record) from federalregister.gov or, failing that, govinfo.gov.

    Both serve the same GPO text, so line numbers and [[Page N]] markers do not
    depend on which one answered.
    """
    m = _get_meta(num)
    date = m.get("publication_date")
    sources = [("federalregister.gov", m.get("raw_text_url")),
               ("govinfo.gov", date and GOVINFO_HTML.format(date=date, num=num))]
    errors = []
    for source, url in sources:
        if not url:
            continue
        try:
            final, body = _http_get(url)
            if _looks_blocked(final, body):
                errors.append("%s blocked" % source)
                continue
            text = _clean_text(body.decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            errors.append("%s: %s" % (source, e))
            continue
        return text, {"document_number": num, "publication_date": date, "source": source,
                      "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                      "retrieved_at": datetime.datetime.now(datetime.timezone.utc)
                      .isoformat(timespec="seconds")}
    raise FRNetworkError("Could not download full text for %s (%s)" % (num, "; ".join(errors)))


def get_full_text(num):
    stored = _stored_text(num)
    if stored:
        text, record = stored
        if _hidden(record.get("publication_date")):
            raise FRNotFound("No Federal Register document with number %r." % num)
    else:
        text, record = _download_text(num)
        os.makedirs(CACHE_DIR, exist_ok=True)
        base = os.path.join(CACHE_DIR, re.sub(r"[^\w.-]", "_", num))
        with open(base + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
        with open(base + ".json.tmp", "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        os.replace(base + ".json.tmp", base + ".json")
        record = dict(record, origin="download")
    if num not in LOADED:
        LOADED[num] = {"publication_date": record.get("publication_date"),
                       "source": record.get("source"), "origin": record["origin"],
                       "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    return text


def _page_at(lines, idx):
    """Return the printed FR page number in effect at line idx, if any."""
    for j in range(idx, -1, -1):
        mm = re.match(r"\s*\[\[Page (\d+)\]\]", lines[j])
        if mm:
            return mm.group(1)
    return None


def text(document_number, start=1, lines=150):
    """Full text from line `start` (1-based), `lines` lines, with line numbers."""
    all_lines = get_full_text(document_number).split("\n")
    n = len(all_lines)
    start = max(1, start)
    end = min(n, start + lines - 1)
    if start > n:
        raise FRToolError("Document has only %d lines." % n)
    pg = _page_at(all_lines, start - 1)
    out = ["[%s: lines %d-%d of %d%s]" % (document_number, start, end, n,
                                         ", FR page %s" % pg if pg else "")]
    for i in range(start - 1, end):
        out.append("%6d  %s" % (i + 1, all_lines[i]))
    if end < n:
        out.append("[... continue with --start %d]" % (end + 1))
    return "\n".join(out)


HEADING_RES = [
    re.compile(r"^(PART \d+\w*\s*--.*)$"),
    re.compile(r"^(Sec\.\s+\d+[\w.]*\s+.*)$"),
    re.compile(r"^((?:[IVXL]+)\.\s+[A-Z].{2,})$"),
    re.compile(r"^([A-Z]\.\s+[A-Z].{2,})$"),
    re.compile(r"^((?:SUMMARY|DATES|ADDRESSES|FOR FURTHER INFORMATION CONTACT|"
               r"SUPPLEMENTARY INFORMATION|AGENCY|ACTION|List of Subjects).*)$"),
    re.compile(r"^((?:Section|Sec\.)\s+\d+\.\s+.*)$"),
]


def toc(document_number, max_entries=400):
    """Outline of headings with line numbers."""
    lines = get_full_text(document_number).split("\n")
    out = []
    count = 0
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if not s or s.startswith(" ") or len(s) > 160 or re.match(r"^[A-Z]\. Ct\.", s):
            continue
        for rx in HEADING_RES:
            if rx.match(s):
                out.append("%6d  %s" % (i + 1, s))
                count += 1
                break
        if count >= max_entries:
            out.append("[outline truncated at %d entries; use --max]" % max_entries)
            break
    if count == 0:
        out.append("(no headings detected; use `text` or `grep`)")
    out.append("\n[%d lines total. Read a section with: text %s --start LINE]"
               % (len(lines), document_number))
    return "\n".join(out)


def grep(document_number, pattern, ignore_case=False, context=2, max_matches=25):
    """Regex search within a document's full text, with context lines.

    The pattern is run, as written, against the whole document rather than
    line by line, so it can match across line breaks (the text is hard-wrapped)
    if it allows for them, e.g. with `\\s+`. `^` and `$` anchor at line
    boundaries (re.MULTILINE) and `.` does not match a newline. Empty matches
    are ignored.
    """
    try:
        rx = re.compile(pattern, re.MULTILINE | (re.IGNORECASE if ignore_case else 0))
    except re.error as e:
        raise FRToolError("Bad regex: %s" % e) from None
    text = get_full_text(document_number)
    lines = text.split("\n")
    starts = [0]
    for ln in lines[:-1]:
        starts.append(starts[-1] + len(ln) + 1)
    context = max(0, context)
    # (first line, last line) of each match, not counting whitespace at its edges.
    hits = []
    for m in rx.finditer(text):
        a, b = m.start(), m.end()
        if a == b:
            continue
        found = m.group()
        if found.strip():
            a, b = a + len(found) - len(found.lstrip()), a + len(found.rstrip())
        hits.append((bisect.bisect_right(starts, a) - 1, bisect.bisect_right(starts, b - 1) - 1))
    out = ["[%d match(es) for /%s/ in %s (%d lines)]"
           % (len(hits), pattern, document_number, len(lines))]
    matched = set()
    for first, last in hits[:max_matches]:
        matched.update(range(first, last + 1))
    last_end = -1
    for first, last in hits[:max_matches]:
        lo, hi = max(0, first - context), min(len(lines), last + context + 1)
        if lo <= last_end:
            lo = last_end + 1
        else:
            pg = _page_at(lines, first)
            out.append("--" + (" (FR page %s)" % pg if pg else ""))
        for j in range(lo, hi):
            out.append("%6d%s %s" % (j + 1, ">" if j in matched else " ", lines[j]))
        last_end = max(last_end, hi - 1)
    if len(hits) > max_matches:
        out.append("[... %d more matches; raise --max or narrow the pattern]"
                   % (len(hits) - max_matches))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def cmd_search(a):
    print(search(a.query, doc_type=a.type, agency=a.agency, pres_type=a.pres_type,
                 since=a.since, until=a.until, docket=a.docket, rin=a.rin,
                 cfr=a.cfr, significant=a.significant, order=a.order,
                 per_page=a.per_page, page=a.page, brief=a.brief))


def cmd_doc(a):
    print(doc(a.document_number))


def cmd_text(a):
    print(text(a.document_number, start=a.start, lines=a.lines))


def cmd_toc(a):
    print(toc(a.document_number, max_entries=a.max))


def cmd_grep(a):
    print(grep(a.document_number, a.pattern, ignore_case=a.ignore_case,
               context=a.context, max_matches=a.max))


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="fr_tool.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="search Federal Register documents")
    s.add_argument("query", help="full-text search terms ('' for none). Supports "
                   "quoted phrases, e.g. '\"extension of stay\" F-1'")
    s.add_argument("--type", action="append", choices=list(DOC_TYPES) +
                   [k.lower() for k in DOC_TYPES],
                   help="document type; repeatable (RULE, PRORULE, NOTICE, PRESDOCU)")
    s.add_argument("--agency", action="append",
                   help="agency slug, repeatable (e.g. homeland-security-department, "
                   "u-s-citizenship-and-immigration-services, "
                   "u-s-immigration-and-customs-enforcement, state-department, "
                   "labor-department, executive-office-of-the-president)")
    s.add_argument("--pres-type", action="append", choices=PRES_TYPES,
                   help="presidential document subtype (use with --type PRESDOCU)")
    s.add_argument("--since", help="published on/after YYYY-MM-DD")
    s.add_argument("--until", help="published on/before YYYY-MM-DD")
    s.add_argument("--docket", help="docket ID, e.g. 'ICEB-2025-0001'")
    s.add_argument("--rin", help="Regulation Identifier Number, e.g. 1653-AA95")
    s.add_argument("--cfr", help="CFR title:part affected, e.g. 8:214")
    s.add_argument("--significant", action="store_true",
                   help="only significant regulatory actions")
    s.add_argument("--order", default="relevance",
                   choices=ORDERS)
    s.add_argument("--per-page", type=int, default=10, help="1-50 (default 10)")
    s.add_argument("--page", type=int, default=1)
    s.add_argument("--brief", action="store_true", help="omit abstracts")
    s.set_defaults(func=cmd_search)

    d = sub.add_parser("doc", help="metadata for one document")
    d.add_argument("document_number")
    d.set_defaults(func=cmd_doc)

    t = sub.add_parser("text", help="print full text by line range")
    t.add_argument("document_number")
    t.add_argument("--start", type=int, default=1, help="first line (1-based)")
    t.add_argument("--lines", type=int, default=150, help="number of lines (default 150)")
    t.set_defaults(func=cmd_text)

    o = sub.add_parser("toc", help="outline of headings with line numbers")
    o.add_argument("document_number")
    o.add_argument("--max", type=int, default=400)
    o.set_defaults(func=cmd_toc)

    g = sub.add_parser("grep", help="regex search within a document's full text")
    g.add_argument("document_number")
    g.add_argument("pattern", help="Python regular expression, searched over the whole "
                   "text: ^ and $ match at line boundaries, . does not match a newline")
    g.add_argument("-i", "--ignore-case", action="store_true")
    g.add_argument("--context", type=int, default=2, help="lines of context (default 2)")
    g.add_argument("--max", type=int, default=25, help="max matches shown (default 25)")
    g.set_defaults(func=cmd_grep)

    a = ap.parse_args(argv)
    try:
        a.func(a)
    except FRNetworkError as e:
        sys.exit("Error: %s" % e)
    except FRToolError as e:
        sys.exit(str(e))
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
