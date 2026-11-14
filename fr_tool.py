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
  grep     Regex search inside one document's full text, with context.

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
"""

import argparse
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
TIMEOUT = 90

DOC_TYPES = {
    "RULE": "Rule",
    "PRORULE": "Proposed Rule",
    "NOTICE": "Notice",
    "PRESDOCU": "Presidential Document",
}
PRES_TYPES = ["determination", "executive_order", "memorandum", "notice",
              "proclamation", "presidential_order", "other"]


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
            last = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("request failed after %d tries: %s (%s)" % (retries, url, last))


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


def cmd_search(a):
    p = [("per_page", a.per_page), ("page", a.page), ("order", a.order)]
    p += [("fields[]", f) for f in SEARCH_FIELDS]
    if a.query:
        p.append(("conditions[term]", a.query))
    for t in a.type or []:
        p.append(("conditions[type][]", t.upper()))
    for ag in a.agency or []:
        p.append(("conditions[agencies][]", ag))
    for pt in a.pres_type or []:
        p.append(("conditions[presidential_document_type][]", pt))
    if a.since:
        p.append(("conditions[publication_date][gte]", a.since))
    if a.until:
        p.append(("conditions[publication_date][lte]", a.until))
    if a.docket:
        p.append(("conditions[docket_id]", a.docket))
    if a.rin:
        p.append(("conditions[regulation_id_number]", a.rin))
    if a.cfr:
        m = re.match(r"^(\d+):(\d+)$", a.cfr)
        if not m:
            sys.exit("--cfr must look like TITLE:PART, e.g. 8:214")
        p += [("conditions[cfr][title]", m.group(1)),
              ("conditions[cfr][part]", m.group(2))]
    if a.significant:
        p.append(("conditions[significant]", 1))

    data = _api("/documents.json", p)
    total = data.get("count", 0)
    results = data.get("results") or []
    pages = data.get("total_pages", 1)
    print("Found %d document(s); page %d of %s (%d shown)\n"
          % (total, a.page, pages, len(results)))
    for i, r in enumerate(results, 1 + (a.page - 1) * a.per_page):
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
        print("%d. [%s] %s" % (i, r.get("document_number"), r.get("title")))
        print("   " + " | ".join(line2))
        if r.get("action"):
            print("   action: " + r["action"])
        if agencies:
            print("   agencies: " + agencies)
        extra = []
        if r.get("docket_ids"):
            extra.append("docket: " + "; ".join(r["docket_ids"]))
        if r.get("regulation_id_numbers"):
            extra.append("RIN: " + "; ".join(r["regulation_id_numbers"]))
        if r.get("presidential_document_number"):
            extra.append("pres. doc no.: " + str(r["presidential_document_number"]))
        if extra:
            print("   " + " | ".join(extra))
        if r.get("abstract") and not a.brief:
            ab = re.sub(r"\s+", " ", r["abstract"]).strip()
            if len(ab) > 400:
                ab = ab[:400].rsplit(" ", 1)[0] + " ..."
            print("   abstract: " + ab)
        print()
    if pages and a.page < pages:
        print("(more results: rerun with --page %d)" % (a.page + 1))


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


def _get_meta(num):
    p = [("fields[]", f) for f in DOC_FIELDS + ["raw_text_url", "body_html_url"]]
    try:
        return _api("/documents/%s.json" % urllib.parse.quote(num), p)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit("No Federal Register document with number %r." % num)
        raise


def cmd_doc(a):
    m = _get_meta(a.document_number)
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
    corr = m.get("corrections") or []
    if corr:
        add("Corrections", ", ".join(
            c.rstrip("/").split("/")[-1] if isinstance(c, str) else str(c)
            for c in corr))
    add("Disposition", m.get("disposition_notes"))
    add("URL", m.get("html_url"))
    add("PDF", m.get("pdf_url"))
    print("\n".join(out))
    if m.get("abstract"):
        print("\nAbstract:\n" + re.sub(r"\s+", " ", m["abstract"]).strip())
    print("\nUse `toc`, `grep` or `text` with this document number to read the full text.")


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


def get_full_text(num):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, re.sub(r"[^\w.-]", "_", num) + ".txt")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, encoding="utf-8") as f:
            return f.read()
    m = _get_meta(num)
    text, errors = None, []
    for key in ("raw_text_url", "body_html_url"):
        url = m.get(key)
        if not url:
            continue
        try:
            final, body = _http_get(url)
            if _looks_blocked(final, body):
                errors.append("%s blocked" % key)
                continue
            text = _clean_text(body.decode("utf-8", "replace"))
            break
        except Exception as e:  # noqa: BLE001
            errors.append("%s: %s" % (key, e))
    if text is None and m.get("publication_date"):
        url = GOVINFO_HTML.format(date=m["publication_date"], num=num)
        try:
            _, body = _http_get(url)
            text = _clean_text(body.decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            errors.append("govinfo: %s" % e)
    if text is None:
        sys.exit("Could not download full text for %s (%s)" % (num, "; ".join(errors)))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def _page_at(lines, idx):
    """Return the printed FR page number in effect at line idx, if any."""
    for j in range(idx, -1, -1):
        mm = re.match(r"\s*\[\[Page (\d+)\]\]", lines[j])
        if mm:
            return mm.group(1)
    return None


def cmd_text(a):
    lines = get_full_text(a.document_number).split("\n")
    n = len(lines)
    start = max(1, a.start)
    end = min(n, start + a.lines - 1)
    if start > n:
        sys.exit("Document has only %d lines." % n)
    pg = _page_at(lines, start - 1)
    print("[%s: lines %d-%d of %d%s]" % (a.document_number, start, end, n,
                                        ", FR page %s" % pg if pg else ""))
    for i in range(start - 1, end):
        print("%6d  %s" % (i + 1, lines[i]))
    if end < n:
        print("[... continue with --start %d]" % (end + 1))


HEADING_RES = [
    re.compile(r"^(PART \d+\w*\s*--.*)$"),
    re.compile(r"^(Sec\.\s+\d+[\w.]*\s+.*)$"),
    re.compile(r"^((?:[IVXL]+)\.\s+[A-Z].{2,})$"),
    re.compile(r"^([A-Z]\.\s+[A-Z].{2,})$"),
    re.compile(r"^((?:SUMMARY|DATES|ADDRESSES|FOR FURTHER INFORMATION CONTACT|"
               r"SUPPLEMENTARY INFORMATION|AGENCY|ACTION|List of Subjects).*)$"),
    re.compile(r"^((?:Section|Sec\.)\s+\d+\.\s+.*)$"),
]


def cmd_toc(a):
    lines = get_full_text(a.document_number).split("\n")
    count = 0
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if not s or s.startswith(" ") or len(s) > 160 or re.match(r"^[A-Z]\. Ct\.", s):
            continue
        for rx in HEADING_RES:
            if rx.match(s):
                print("%6d  %s" % (i + 1, s))
                count += 1
                break
        if count >= a.max:
            print("[outline truncated at %d entries; use --max]" % a.max)
            break
    if count == 0:
        print("(no headings detected; use `text` or `grep`)")
    print("\n[%d lines total. Read a section with: text %s --start LINE]"
          % (len(lines), a.document_number))


def cmd_grep(a):
    lines = get_full_text(a.document_number).split("\n")
    flags = re.IGNORECASE if a.ignore_case else 0
    try:
        rx = re.compile(a.pattern, flags)
    except re.error as e:
        sys.exit("Bad regex: %s" % e)
    hits = [i for i, ln in enumerate(lines) if rx.search(ln)]
    print("[%d matching line(s) for /%s/ in %s (%d lines)]"
          % (len(hits), a.pattern, a.document_number, len(lines)))
    shown, last_end = 0, -1
    for i in hits:
        if shown >= a.max:
            print("[... %d more matches; raise --max or narrow the pattern]"
                  % (len(hits) - shown))
            break
        lo, hi = max(0, i - a.context), min(len(lines), i + a.context + 1)
        if lo <= last_end:
            lo = last_end + 1
        else:
            pg = _page_at(lines, i)
            print("--" + (" (FR page %s)" % pg if pg else ""))
        for j in range(lo, hi):
            mark = ">" if j == i or rx.search(lines[j]) else " "
            print("%6d%s %s" % (j + 1, mark, lines[j]))
        last_end = hi - 1
        shown += 1


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
                   choices=["relevance", "newest", "oldest", "executive_order_number"])
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
    g.add_argument("pattern", help="Python regular expression")
    g.add_argument("-i", "--ignore-case", action="store_true")
    g.add_argument("--context", type=int, default=2, help="lines of context (default 2)")
    g.add_argument("--max", type=int, default=25, help="max matches shown (default 25)")
    g.set_defaults(func=cmd_grep)

    a = ap.parse_args(argv)
    if getattr(a, "per_page", None) is not None:
        a.per_page = max(1, min(50, a.per_page))
    try:
        a.func(a)
    except RuntimeError as e:
        sys.exit("Error: %s" % e)
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
