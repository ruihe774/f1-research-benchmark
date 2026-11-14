"""Shared code for bench.py and grader.py.

- The Federal Register tools (fr_tool.py) exposed as OpenAI function tools,
  frozen at the task's reference date.
- A stateless Responses API agent loop (store=False, full history replayed on
  every request) that ends in a Pydantic structured output. The loop asks for
  the final answer when the turn limit or the context budget is reached.
- Transcript recording: every request's response, tool call, tool result and
  token usage, written to JSON after each turn.
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Literal

import openai
import pydantic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
# OPENAI_API_KEY and, optionally, OPENAI_BASE_URL and FR_TOOL_CACHE come from
# .env. Neither the SDK nor fr_tool reads .env files, and fr_tool reads its
# settings when imported, so load it first.
load_dotenv(ROOT / ".env")

import fr_tool  # noqa: E402

TASK_PATH = ROOT / "TASK.md"
ANSWER_KEY_PATH = ROOT / "ANSWER_KEY.md"
RUBRIC_PATH = ROOT / "rubric.toml"
RUNS_DIR = ROOT / "runs"

# "Today" in TASK.md. The tools hide every document published after it, so a
# run gives the same Federal Register whenever it is made.
AS_OF = "2026-11-14"
fr_tool.AS_OF = AS_OF

MAX_OUTPUT_TOKENS = 128_000
EFFORTS = ["none", "minimal", "low", "medium", "high", "xhigh", "max"]
REASONING_SUMMARIES = ["auto", "concise", "detailed", "none"]

# Tool outputs are capped before they first enter the context: trimming them
# later would change the prompt prefix.
TOOL_OUTPUT_CHAR_LIMIT = 40_000
# Tool output is counted against the context budget before the API reports its
# size; 3 characters per token overestimates it.
CHARS_PER_TOKEN = 3
DEFAULT_CONTEXT_BUDGET = 250_000
MAX_TEXT_LINES = 400
MAX_GREP_CONTEXT = 10
MAX_GREP_MATCHES = 100
MAX_TOC_ENTRIES = 1000


# --------------------------------------------------------------------------- #
# Federal Register tools
# --------------------------------------------------------------------------- #
DocType = Literal["RULE", "PRORULE", "NOTICE", "PRESDOCU"]
PresType = Literal["determination", "executive_order", "memorandum", "notice",
                   "proclamation", "presidential_order", "other"]
Order = Literal["relevance", "newest", "oldest", "executive_order_number"]


class FrSearchArgs(BaseModel):
    query: str = Field(description='Full-text search terms; "" for none. Supports quoted '
                       'phrases, e.g. "\\"extension of stay\\" F-1".')
    doc_type: list[DocType] | None = Field(
        description="Document types: RULE, PRORULE (proposed rule), NOTICE, PRESDOCU "
        "(presidential document). null for all.")
    agency: list[str] | None = Field(
        description="Agency slugs, e.g. homeland-security-department, "
        "u-s-citizenship-and-immigration-services, u-s-immigration-and-customs-enforcement, "
        "state-department, labor-department, executive-office-of-the-president.")
    pres_type: list[PresType] | None = Field(
        description="Presidential document subtypes (use with doc_type PRESDOCU).")
    since: str | None = Field(description="Published on/after YYYY-MM-DD.")
    until: str | None = Field(description="Published on/before YYYY-MM-DD.")
    docket: str | None = Field(description="Docket ID, e.g. EPA-HQ-OAR-2021-0317.")
    rin: str | None = Field(description="Regulation Identifier Number, e.g. 2060-AV16.")
    cfr: str | None = Field(description="CFR title:part affected, numeric part only, e.g. 8:214 (lettered parts such as 274a are not supported).")
    significant: bool | None = Field(description="true: only significant regulatory actions.")
    order: Order | None = Field(description="Sort order (default relevance).")
    per_page: int | None = Field(description="Results per page, 1-50 (default 10).")
    page: int | None = Field(description="Results page (default 1).")
    brief: bool | None = Field(description="true: omit abstracts.")


class FrDocArgs(BaseModel):
    document_number: str = Field(description="FR document number, e.g. 2024-00366.")


class FrTocArgs(BaseModel):
    document_number: str = Field(description="FR document number.")
    max_entries: int | None = Field(
        description="Maximum outline entries (default 400, at most %d)." % MAX_TOC_ENTRIES)


class FrGrepArgs(BaseModel):
    document_number: str = Field(description="FR document number.")
    pattern: str = Field(
        description="Python regular expression, searched over the whole text (a match may "
        "span lines). ^ and $ match at line boundaries; . does not match a newline.")
    ignore_case: bool | None = Field(description="Case-insensitive match (default false).")
    context: int | None = Field(
        description="Lines of context around each match (default 2, at most %d)."
        % MAX_GREP_CONTEXT)
    max_matches: int | None = Field(
        description="Maximum matches shown (default 25, at most %d)." % MAX_GREP_MATCHES)


class FrTextArgs(BaseModel):
    document_number: str = Field(description="FR document number.")
    start: int | None = Field(description="First line, 1-based (default 1).")
    lines: int | None = Field(
        description="Number of lines (default 150, at most %d)." % MAX_TEXT_LINES)


def _given(v, default):
    return default if v is None else v


def _run_search(a: FrSearchArgs) -> str:
    return fr_tool.search(
        a.query, doc_type=a.doc_type, agency=a.agency, pres_type=a.pres_type,
        since=a.since, until=a.until, docket=a.docket, rin=a.rin, cfr=a.cfr,
        significant=bool(a.significant), order=_given(a.order, "relevance"),
        per_page=_given(a.per_page, 10), page=_given(a.page, 1), brief=bool(a.brief))


def _run_doc(a: FrDocArgs) -> str:
    return fr_tool.doc(a.document_number)


def _run_toc(a: FrTocArgs) -> str:
    n = min(max(1, _given(a.max_entries, 400)), MAX_TOC_ENTRIES)
    return fr_tool.toc(a.document_number, max_entries=n)


def _run_grep(a: FrGrepArgs) -> str:
    return fr_tool.grep(
        a.document_number, a.pattern, ignore_case=bool(a.ignore_case),
        context=min(max(0, _given(a.context, 2)), MAX_GREP_CONTEXT),
        max_matches=min(max(1, _given(a.max_matches, 25)), MAX_GREP_MATCHES))


def _run_text(a: FrTextArgs) -> str:
    return fr_tool.text(a.document_number, start=_given(a.start, 1),
                        lines=min(max(1, _given(a.lines, 150)), MAX_TEXT_LINES))


@dataclass
class Tool:
    name: str
    description: str
    args_model: type[BaseModel]
    run: Callable[[Any], str]

    def param(self) -> dict:
        return openai.pydantic_responses_function_tool(
            self.args_model, name=self.name, description=self.description)


_HINTS = ("Output may contain CLI-style hints such as '--start N' or '--max'; "
          "they refer to this tool's parameters.")

FR_TOOLS = [
    Tool("fr_search",
         "Search U.S. Federal Register documents (rules, proposed rules, notices, "
         "presidential documents) by keywords and filters. Prints document numbers, "
         "titles, types, dates, citations, dockets, RINs and abstracts.",
         FrSearchArgs, _run_search),
    Tool("fr_doc",
         "Metadata for one Federal Register document: title, type, action, citation, "
         "page range, publication/signing/effective dates, comment deadline, docket, RIN, "
         "CFR parts affected, corrections, abstract.",
         FrDocArgs, _run_doc),
    Tool("fr_toc",
         "Outline of a document's full text: headings with line numbers. " + _HINTS,
         FrTocArgs, _run_toc),
    Tool("fr_grep",
         "Regex search inside one document's full text. Shows the lines of each match "
         "with line numbers, context lines and the FR page of each match. " + _HINTS,
         FrGrepArgs, _run_grep),
    Tool("fr_text",
         "Read a document's full text by line range, with line numbers. "
         "[[Page N]] markers give FR page numbers. " + _HINTS,
         FrTextArgs, _run_text),
]


def run_tool(tools: dict[str, Tool], call) -> tuple[str, str | None, str | None]:
    """Execute one function call.

    Returns (output text, error message or None, error kind or None). Errors are
    returned to the model as the tool output so it can recover. Kind "input"
    means the call itself was wrong; "infra" means the tool or the network
    failed, which is not the model's doing.
    """
    tool = tools.get(call.name)
    if tool is None:
        err = "unknown tool %r" % call.name
        return "Error: " + err, err, "input"
    try:
        args = call.parsed_arguments if isinstance(
            getattr(call, "parsed_arguments", None), tool.args_model) \
            else tool.args_model.model_validate_json(call.arguments)
    except pydantic.ValidationError as e:
        err = "invalid arguments: %s" % e
        return "Error: " + err, err, "input"
    try:
        out = tool.run(args)
    except fr_tool.FRNetworkError as e:
        return "Error: %s" % e, str(e), "infra"
    except fr_tool.FRToolError as e:
        return "Error: %s" % e, str(e), "input"
    except Exception as e:  # noqa: BLE001 - surface anything else to the model
        err = "%s: %s" % (type(e).__name__, e)
        return "Error: " + err, err, "infra"
    if len(out) > TOOL_OUTPUT_CHAR_LIMIT:
        out = (out[:TOOL_OUTPUT_CHAR_LIMIT]
               + "\n[... output truncated at %d characters; request a smaller range]"
               % TOOL_OUTPUT_CHAR_LIMIT)
    return out, None, None


# --------------------------------------------------------------------------- #
# Task files
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def question_ids(task_md: str) -> list[str]:
    ids = re.findall(r"^### (Q\d+)\s*$", task_md, flags=re.M)
    if not ids:
        raise ValueError("no '### Qn' headings found in TASK.md")
    return ids


# --------------------------------------------------------------------------- #
# Transcript
# --------------------------------------------------------------------------- #
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def add_usage(total: dict, usage: dict | None) -> None:
    """Add every integer in a (nested) usage dict into `total`."""
    for k, v in (usage or {}).items():
        if isinstance(v, bool):
            continue
        if isinstance(v, int):
            total[k] = total.get(k, 0) + v
        elif isinstance(v, dict):
            add_usage(total.setdefault(k, {}), v)


def write_json(path: Path, data) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


class Transcript:
    """Everything sent to and received from the API, saved after each turn."""

    def __init__(self, path: Path, kind: str, config: dict, request: dict,
                 initial_input: list):
        self.path = path
        self.data = {
            "kind": kind,
            "started_at": now_iso(),
            "finished_at": None,
            "status": "running",
            "error": None,
            "config": config,
            # Request fields that stay the same on every turn.
            "request": request,
            "initial_input": initial_input,
            "turns": [],
            "usage_total": {},
            "tool_calls_total": 0,
            # Failed tool calls by kind: input | infra | budget (see run_tool).
            "tool_errors_total": {},
            # Full texts the tools read: number -> source, origin, sha256.
            "fr_documents": {},
            "final_output": None,
        }
        self.save()

    def add_turn(self, turn: dict) -> None:
        self.data["turns"].append(turn)
        add_usage(self.data["usage_total"], turn.get("usage"))
        self.data["tool_calls_total"] += len(turn.get("tool_results", []))
        errors = self.data["tool_errors_total"]
        for r in turn.get("tool_results", []):
            if r["error_kind"]:
                errors[r["error_kind"]] = errors.get(r["error_kind"], 0) + 1
        self.data["fr_documents"] = dict(fr_tool.LOADED)
        self.save()

    def finish(self, status: str, final_output=None, error: str | None = None) -> None:
        self.data.update(status=status, final_output=final_output, error=error,
                         finished_at=now_iso())
        self.save()

    def save(self) -> None:
        write_json(self.path, self.data)

    def warn_tool_errors(self) -> None:
        n = self.data["tool_errors_total"].get("infra", 0)
        if n:
            log("WARNING: %d tool call(s) failed for infrastructure reasons (network, "
                "Federal Register outage); the run may understate the model. See "
                "error_kind in %s" % (n, self.path))


# --------------------------------------------------------------------------- #
# Agent loop
# --------------------------------------------------------------------------- #
def make_client(timeout: float) -> openai.OpenAI:
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set (put it in %s)" % (ROOT / ".env"))
    return openai.OpenAI(timeout=timeout, max_retries=5)


def to_input_item(item) -> dict:
    """Turn a response output item into a replayable input item.

    Keeps every field the API returned (encrypted reasoning, assistant phase,
    ids) and drops only the SDK's client-side parse results.
    """
    data = item.to_dict()
    data.pop("created_by", None)
    if data.get("type") == "function_call":
        data.pop("parsed_arguments", None)
        if data.get("id") is None:
            data.pop("id", None)
    if data.get("type") == "message":
        for part in data.get("content", []):
            if part.get("type") == "output_text":
                part.pop("parsed", None)
    return data


def developer_message(text: str) -> dict:
    return {"role": "developer", "content": [{"type": "input_text", "text": text}]}


def user_message(text: str) -> dict:
    return {"role": "user", "content": [{"type": "input_text", "text": text}]}


@dataclass
class AgentResult:
    # completed | incomplete | refused | max_turns | context_budget | no_final_answer | error
    status: str
    output: BaseModel | None = None
    error: str | None = None
    input_items: list = field(default_factory=list)


FINAL_TURN_NOTE = ("%s reached. Tool calls are now disabled. Give your final "
                   "answer now in the required format, based on what you have found.")
LIMITS = {"max_turns": "Turn limit", "context_budget": "Context budget"}
BUDGET_SKIP = "Not run: the context budget for this task is used up."
NO_ANSWER_NOTE = ("Continue working. When you are done, give your final answer in the "
                  "required format.")
# Appended to every tool result so the model can see the budget it is spending.
# Only new outputs carry it, so the cached prompt prefix is unchanged.
BUDGET_FOOTER = "\n[context budget: about %d tokens left]"
BAD_FORMAT_NOTE = ("Your final answer could not be parsed against the required format "
                   "(%s). Give the complete final answer again in the required format.")
MAX_NUDGES = 3


def log(msg: str) -> None:
    print("[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg), file=sys.stderr, flush=True)


def _brief_args(arguments: str, limit: int = 160) -> str:
    try:
        a = {k: v for k, v in json.loads(arguments).items() if v not in (None, False)}
        s = json.dumps(a, ensure_ascii=False)
    except ValueError:
        s = arguments
    return s if len(s) <= limit else s[:limit] + "..."


def run_agent(client: openai.OpenAI, *, model: str, effort: str | None,
              reasoning_summary: str, input_items: list, tools: list[Tool],
              text_format: type[BaseModel], transcript: Transcript, max_turns: int,
              context_budget: int) -> AgentResult:
    """Drive a stateless tool-calling loop until the model returns a parsed answer.

    Every request carries the full history: the initial input plus every output
    item (including encrypted reasoning) and tool result, appended in order and
    never edited, so the prompt prefix stays stable from turn to turn.

    The history is never trimmed, so it must not outgrow the model's context
    window. Every tool result ends with the estimated number of tokens left in
    `context_budget`, so the model can pace its reading. Once the next request
    is estimated at `context_budget` input tokens or more (0: no budget),
    remaining tool calls are not run and the model gets one last request,
    without tools, for its final answer, as at the turn limit.
    """
    items = list(input_items)
    tool_map = {t.name: t for t in tools}
    reasoning = {}
    if effort:
        reasoning["effort"] = effort
    if reasoning_summary != "none":
        reasoning["summary"] = reasoning_summary
    request = dict(
        model=model,
        tools=[t.param() for t in tools],
        text_format=text_format,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        store=False,
    )
    if reasoning:
        request["reasoning"] = reasoning
    nudges = 0
    limit = None  # the limit reached, once the final answer has been asked for
    context = 0  # estimated input tokens of the next request

    def over_budget() -> bool:
        return bool(context_budget) and context >= context_budget

    for turn_no in range(1, max_turns + 1):
        injected = []
        if limit is None and (over_budget() or turn_no == max_turns):
            limit = "context_budget" if over_budget() else "max_turns"
            injected.append(developer_message(FINAL_TURN_NOTE % LIMITS[limit]))
            items.extend(injected)
            if limit == "context_budget":
                log("turn %d: context budget reached (about %d of %d tokens); asking for "
                    "the final answer" % (turn_no, context, context_budget))
        final_turn = limit is not None
        turn = {"turn": turn_no, "started_at": now_iso(), "injected_input": injected,
                "tool_choice": "none" if final_turn else "auto", "limit": limit,
                "context_estimate": context}
        t0 = time.monotonic()
        try:
            raw = client.responses.with_raw_response.parse(
                input=items, tool_choice=turn["tool_choice"], **request)
        except openai.APIError as e:
            turn.update(elapsed_s=round(time.monotonic() - t0, 2),
                        api_error={"type": type(e).__name__, "message": str(e),
                                   "body": getattr(e, "body", None)})
            transcript.add_turn(turn)
            return AgentResult("error", error="%s: %s" % (type(e).__name__, e),
                               input_items=items)
        turn["elapsed_s"] = round(time.monotonic() - t0, 2)
        turn["request_id"] = raw.headers.get("x-request-id")
        try:
            resp = raw.parse()
        except (pydantic.ValidationError, ValueError) as e:
            # The final message did not match the schema (e.g. cut off). Keep the
            # raw response, replay it and ask again.
            body = raw.http_response.json()
            turn.update(response=body, usage=body.get("usage"), parse_error=str(e))
            context = sum((body.get("usage") or {}).get(k, 0)
                          for k in ("input_tokens", "output_tokens"))
            transcript.add_turn(turn)
            log("turn %d: answer failed to parse: %s" % (turn_no, str(e).splitlines()[0]))
            if body.get("status") == "incomplete":
                return AgentResult("incomplete", error=json.dumps(
                    body.get("incomplete_details")), input_items=items)
            nudges += 1
            if nudges > MAX_NUDGES:
                return AgentResult("no_final_answer", error=str(e), input_items=items)
            items.extend(_strip_ids(o) for o in body.get("output", []))
            note = developer_message(BAD_FORMAT_NOTE % str(e).splitlines()[0])
            items.append(note)
            turn["injected_after"] = [note]
            transcript.save()
            continue

        turn["response"] = resp.to_dict()
        turn["usage"] = resp.usage.to_dict() if resp.usage else None
        items.extend(to_input_item(o) for o in resp.output)
        calls = [o for o in resp.output if o.type == "function_call"]
        u = resp.usage
        # This request's input and output are the next request's input.
        context = (u.input_tokens + u.output_tokens) if u else context
        log("turn %d: %s, %d tool call(s), in=%s (cached %s) out=%s, %.1fs" % (
            turn_no, resp.status, len(calls), u and u.input_tokens,
            u and u.input_tokens_details.cached_tokens, u and u.output_tokens,
            turn["elapsed_s"]))

        if resp.status == "incomplete":
            transcript.add_turn(turn)
            reason = resp.incomplete_details and resp.incomplete_details.reason
            return AgentResult("incomplete", error="incomplete: %s" % reason,
                               input_items=items)

        if calls and not final_turn:
            results = []
            for call in calls:
                c0 = time.monotonic()
                if over_budget():
                    out, err, kind = BUDGET_SKIP, "context budget reached", "budget"
                else:
                    out, err, kind = run_tool(tool_map, call)
                context += len(out) // CHARS_PER_TOKEN + 1
                footer = ""
                if context_budget:
                    footer = BUDGET_FOOTER % max(0, context_budget - context)
                    context += len(footer) // CHARS_PER_TOKEN + 1
                results.append({"call_id": call.call_id, "name": call.name,
                                "arguments": call.arguments, "output": out,
                                "footer": footer, "error": err, "error_kind": kind,
                                "elapsed_s": round(time.monotonic() - c0, 2)})
                items.append({"type": "function_call_output", "call_id": call.call_id,
                              "output": out + footer})
                log("  %s %s -> %d chars%s" % (call.name, _brief_args(call.arguments),
                                                 len(out), " (%s error)" % kind if err else ""))
            turn["tool_results"] = results
            transcript.add_turn(turn)
            continue

        transcript.add_turn(turn)
        refusals = [c.refusal for o in resp.output if o.type == "message"
                    for c in o.content if c.type == "refusal"]
        if refusals:
            return AgentResult("refused", error=" ".join(refusals), input_items=items)
        if resp.output_parsed is not None:
            return AgentResult("completed", output=resp.output_parsed, input_items=items)
        if final_turn:
            return AgentResult(limit, error="no final answer at the %s"
                               % LIMITS[limit].lower(), input_items=items)
        nudges += 1
        if nudges > MAX_NUDGES:
            return AgentResult("no_final_answer", error="model stopped without a final answer",
                               input_items=items)
        note = developer_message(NO_ANSWER_NOTE)
        items.append(note)
        turn["injected_after"] = [note]
        transcript.save()

    limit = limit or "max_turns"
    return AgentResult(limit, error="no final answer at the %s" % LIMITS[limit].lower(),
                       input_items=items)


def _strip_ids(item: dict) -> dict:
    """Raw output item from an unparsed response, made replayable."""
    item = dict(item)
    item.pop("created_by", None)
    if item.get("type") == "function_call" and item.get("id") is None:
        item.pop("id", None)
    return item


# --------------------------------------------------------------------------- #
# CLI helpers
# --------------------------------------------------------------------------- #
def add_agent_args(ap: argparse.ArgumentParser, *, default_max_turns: int,
                   model_required: bool = True) -> None:
    ap.add_argument("--model", required=model_required, help="model id, e.g. gpt-6.1-sol")
    ap.add_argument("--effort", choices=EFFORTS, default=None,
                    help="reasoning effort (default: the model's default)")
    ap.add_argument("--reasoning-summary", choices=REASONING_SUMMARIES, default="auto",
                    help="reasoning summaries to record in the transcript (default auto)")
    ap.add_argument("--max-turns", type=int, default=default_max_turns,
                    help="maximum model requests; the last one may not call tools "
                    "(default %d)" % default_max_turns)
    ap.add_argument("--context-budget", type=int, default=DEFAULT_CONTEXT_BUDGET,
                    help="input tokens after which the model is asked for its final answer "
                    "instead of overflowing the context window; keep it below the model's "
                    "input limit; 0 disables (default %d)" % DEFAULT_CONTEXT_BUDGET)
    ap.add_argument("--timeout", type=float, default=3600,
                    help="per-request timeout in seconds (default 3600)")


def agent_config(a: argparse.Namespace, client: openai.OpenAI) -> dict:
    return {
        "model": a.model,
        "reasoning_effort": a.effort,
        "reasoning_summary": a.reasoning_summary,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "max_turns": a.max_turns,
        "context_budget": a.context_budget,
        "timeout_s": a.timeout,
        "store": False,
        "base_url": str(client.base_url),
        "openai_sdk": openai.__version__,
        "fr_tool_as_of": fr_tool.AS_OF,
        "fr_tool_snapshot": fr_tool.SNAPSHOT_DIR,
        "fr_tool_cache": fr_tool.CACHE_DIR,
        "tool_output_char_limit": TOOL_OUTPUT_CHAR_LIMIT,
        # Each tool result ends with this line (tokens left in the budget).
        "budget_footer": BUDGET_FOOTER.strip() if a.context_budget else None,
    }


def static_request(tools: list[Tool], text_format: type[BaseModel],
                   a: argparse.Namespace) -> dict:
    """The request fields that are identical on every turn, for the transcript."""
    from openai.lib._parsing._responses import type_to_text_format_param
    return {
        "model": a.model,
        "reasoning": {"effort": a.effort, "summary": a.reasoning_summary},
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "store": False,
        "tools": [t.param() for t in tools],
        "text": {"format": type_to_text_format_param(text_format)},
    }


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "-", s).strip("-")
