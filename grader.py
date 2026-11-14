#!/usr/bin/env python3
"""Grade a bench run against ANSWER_KEY.md and rubric.toml.

The grader agent reads the task, the answer key and the rubric criteria, may
check citations with the same Federal Register tools as the agent under test,
and returns a verdict for every criterion: "yes", "no" or "unclear". This
script turns verdicts into points; the grader agent never scores.

Prompt caching is implicit (a breakpoint at the end of the latest user message
or tool-output group, so each turn reuses the previous history), plus one
explicit breakpoint at the end of the stable prefix (instructions + task +
answer key + criteria). The submission comes after it, so grading many runs
reuses the cached prefix.

Examples:
  uv run grader.py runs/<run-id> --model gpt-6.1-sol --effort high
  uv run grader.py --answer some_answer.md --model gpt-6.1-sol
  uv run grader.py --rescore runs/<run-id>/grades/<grade-id>

Outputs go to <run>/grades/<grade-id>/ (or --out):
  transcript.json  every request's response, tool call, tool result and usage
  verdicts.json    the grader's structured verdicts
  score.json       points computed from the verdicts
  report.md        verdicts, rationales and points per question
"""

import argparse
import hashlib
import json
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, create_model

import harness_common as hc

VERDICTS = ("yes", "no", "unclear")


# --------------------------------------------------------------------------- #
# Rubric
# --------------------------------------------------------------------------- #
@dataclass
class Criterion:
    id: str
    question: str
    text: str
    kind: str = "credit"  # credit | penalty | gate
    points: float = 0.0
    group: str | None = None
    ladder: str | None = None


@dataclass
class Ladder:
    """ "At least 1", "at least 2", ... criteria, in rubric order.

    Only the unbroken run of "yes" from the first rung counts. `within` names
    another ladder whose count this one cannot exceed.
    """
    id: str
    question: str
    within: str | None = None


@dataclass
class Group:
    id: str
    question: str
    cap: float | None = None
    gate: str | None = None
    factor: float = 1.0


@dataclass
class Rubric:
    questions: dict[str, float]  # id -> max points, in order
    criteria: list[Criterion]
    groups: dict[str, Group] = field(default_factory=dict)
    ladders: dict[str, Ladder] = field(default_factory=dict)  # a parent before its `within`

    def for_question(self, qid: str) -> list[Criterion]:
        return [c for c in self.criteria if c.question == qid]

    def rungs(self, ladder_id: str) -> list[Criterion]:
        return [c for c in self.criteria if c.ladder == ladder_id]


def load_rubric(path: Path) -> Rubric:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    questions = {q["id"]: float(q["points"]) for q in data["question"]}
    groups = {g["id"]: Group(**g) for g in data.get("group", [])}
    ladders = {l["id"]: Ladder(**l) for l in data.get("ladder", [])}
    criteria = []
    for qid in questions:
        for c in data.get("criterion", []):
            if c["question"] == qid:
                criteria.append(Criterion(**c))
        for p in data.get("per_question_penalty", []):
            criteria.append(Criterion(id="%s_%s" % (qid.lower(), p["suffix"]), question=qid,
                                      text=p["text"], kind="penalty", points=p["points"]))
    rubric = Rubric(questions, criteria, groups, ladders)
    scale_questions(rubric, data)
    validate_rubric(rubric, data)
    return rubric


def scale_questions(r: Rubric, data: dict) -> None:
    """Rescale questions that declare `criteria_points`.

    A question's criteria may be written on a different scale from the
    question's weight: `criteria_points` is the total its criteria add up to,
    `points` is what the question is worth. Every credit, penalty and group cap
    of the question is multiplied by points / criteria_points, so the question
    keeps its internal balance at a new weight.
    """
    for q in data["question"]:
        written = q.get("criteria_points")
        if written is None:
            continue
        if written <= 0:
            raise ValueError("%s: criteria_points must be positive" % q["id"])
        f = float(q["points"]) / float(written)
        for c in r.for_question(q["id"]):
            c.points *= f
        for g in r.groups.values():
            if g.question == q["id"] and g.cap is not None:
                g.cap *= f


def validate_rubric(r: Rubric, data: dict) -> None:
    ids = [c.id for c in r.criteria]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError("duplicate criterion ids: %s" % sorted(dupes))
    by_id = {c.id: c for c in r.criteria}
    unknown_q = {c["question"] for c in data.get("criterion", [])} - set(r.questions)
    if unknown_q:
        raise ValueError("criteria for unknown questions: %s" % sorted(unknown_q))
    for c in r.criteria:
        if not c.id.isidentifier():
            raise ValueError("criterion id %r is not an identifier" % c.id)
        if c.kind not in ("credit", "penalty", "gate"):
            raise ValueError("%s: bad kind %r" % (c.id, c.kind))
        if c.kind == "gate" and c.points:
            raise ValueError("%s: gate criteria carry no points" % c.id)
        if c.kind != "gate" and c.points <= 0:
            raise ValueError("%s: points must be positive" % c.id)
        if c.group:
            g = r.groups.get(c.group)
            if g is None or g.question != c.question:
                raise ValueError("%s: unknown group %r for %s" % (c.id, c.group, c.question))
            if c.kind != "credit":
                raise ValueError("%s: only credit criteria belong to groups" % c.id)
        if c.ladder:
            lad = r.ladders.get(c.ladder)
            if lad is None or lad.question != c.question:
                raise ValueError("%s: unknown ladder %r for %s" % (c.id, c.ladder, c.question))
            if c.kind == "gate":
                raise ValueError("%s: gate criteria cannot be ladder rungs" % c.id)
    seen = set()
    for lad in r.ladders.values():
        rungs = r.rungs(lad.id)
        if len(rungs) < 2 or len({c.kind for c in rungs}) != 1:
            raise ValueError("ladder %s: needs at least two rungs of one kind" % lad.id)
        if lad.within:
            parent = r.ladders.get(lad.within)
            if parent is None or parent.question != lad.question or lad.within not in seen:
                raise ValueError("ladder %s: `within` must name an earlier ladder of %s"
                                 % (lad.id, lad.question))
        seen.add(lad.id)
    for g in r.groups.values():
        if g.gate:
            gc = by_id.get(g.gate)
            if gc is None or gc.kind != "gate" or gc.question != g.question:
                raise ValueError("group %s: gate %r must be a gate criterion of %s"
                                 % (g.id, g.gate, g.question))
    for qid, pts in r.questions.items():
        best = question_score(r, qid, {}, "max")["credit"]
        if abs(best - pts) > 1e-9:
            raise ValueError("%s: criteria allow %.2f credit points, question is worth %.2f"
                             % (qid, best, pts))


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def resolve(c: Criterion, verdict: str | None, mode: str) -> str:
    """Resolve "unclear" (or a missing verdict).

    mode "headline": unclear counts as no. "max": in the submission's favour.
    "min": against it.
    """
    if verdict in ("yes", "no"):
        return verdict
    if mode == "headline":
        return "no"
    favourable = "no" if c.kind == "penalty" else "yes"
    unfavourable = "yes" if c.kind == "penalty" else "no"
    return favourable if mode == "max" else unfavourable


def _run_of_yes(values: list[str | None]) -> int:
    n = 0
    for v in values:
        if v != "yes":
            break
        n += 1
    return n


def check_ladders(r: Rubric, verdicts: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Find ladders whose verdicts contradict each other.

    A "yes" above a rung that is not "yes" cannot be right; one of the two
    verdicts is wrong, so both rungs and those between become "unclear". A rung
    beyond the count of the ladder it is `within` becomes "unclear" too.
    Unclear rungs earn nothing in the headline score.
    Returns (verdicts to score, ids of the inconsistent ladders).
    """
    out, bad, counts = dict(verdicts), [], {}
    for lad in r.ladders.values():
        ids = [c.id for c in r.rungs(lad.id)]
        given = [verdicts.get(i) for i in ids]
        counts[lad.id] = n = _run_of_yes(given)
        last_yes = max((k for k, v in enumerate(given) if v == "yes"), default=-1)
        limit = min(n, counts[lad.within]) if lad.within else n
        if last_yes >= n or limit < n:
            bad.append(lad.id)
            out.update(dict.fromkeys(ids[limit:last_yes + 1], "unclear"))
    return out, bad


def apply_ladders(r: Rubric, qid: str, resolved: dict[str, str]) -> None:
    """Keep only each ladder's unbroken run of "yes", capped by its `within` ladder."""
    counts = {}
    for lad in (l for l in r.ladders.values() if l.question == qid):
        ids = [c.id for c in r.rungs(lad.id)]
        n = _run_of_yes([resolved[i] for i in ids])
        if lad.within:
            n = min(n, counts[lad.within])
        counts[lad.id] = n
        resolved.update(dict.fromkeys(ids[n:], "no"))


def question_score(r: Rubric, qid: str, verdicts: dict[str, str], mode: str) -> dict:
    crits = r.for_question(qid)
    resolved = {c.id: resolve(c, verdicts.get(c.id), mode) for c in crits}
    apply_ladders(r, qid, resolved)
    ungrouped, grouped, penalty = 0.0, {}, 0.0
    awarded = {}
    for c in crits:
        yes = resolved[c.id] == "yes"
        if c.kind == "credit" and yes:
            if c.group:
                grouped[c.group] = grouped.get(c.group, 0.0) + c.points
            else:
                ungrouped += c.points
        elif c.kind == "penalty" and yes:
            penalty += c.points
        if c.kind == "credit":
            awarded[c.id] = c.points if yes else 0.0
        elif c.kind == "penalty":
            awarded[c.id] = -c.points if yes else 0.0
    group_scores = {}
    for g in (g for g in r.groups.values() if g.question == qid):
        s = grouped.get(g.id, 0.0)
        if g.cap is not None:
            s = min(s, g.cap)
        if g.gate and resolved[g.gate] != "yes":
            s *= g.factor
        group_scores[g.id] = s
    # What each criterion contributed after its group's cap and gate factor.
    effective = {}
    for c in crits:
        pts = awarded.get(c.id)
        if pts is None:
            continue
        if c.group and grouped.get(c.group):
            pts = pts * group_scores[c.group] / grouped[c.group]
        effective[c.id] = round(pts, 4)
    credit = ungrouped + sum(group_scores.values())
    score = max(0.0, min(r.questions[qid], credit - penalty))
    return {"score": round(score, 4), "credit": round(credit, 4),
            "penalty": round(penalty, 4), "groups": group_scores,
            "points_by_criterion": awarded, "effective_points_by_criterion": effective}


def score_verdicts(r: Rubric, verdicts: dict[str, str]) -> dict:
    out = {"questions": {}, "unclear": [c.id for c in r.criteria
                                        if verdicts.get(c.id) == "unclear"]}
    verdicts, out["inconsistent_ladders"] = check_ladders(r, verdicts)
    totals = {"score": 0.0, "score_min": 0.0, "score_max": 0.0}
    for qid, pts in r.questions.items():
        head = question_score(r, qid, verdicts, "headline")
        lo = question_score(r, qid, verdicts, "min")["score"]
        hi = question_score(r, qid, verdicts, "max")["score"]
        out["questions"][qid] = {"points": pts, "score": head["score"], "score_min": lo,
                                 "score_max": hi, "credit": head["credit"],
                                 "penalty": head["penalty"],
                                 "points_by_criterion": head["points_by_criterion"],
                                 "effective_points_by_criterion":
                                     head["effective_points_by_criterion"]}
        totals["score"] += head["score"]
        totals["score_min"] += lo
        totals["score_max"] += hi
    out["total"] = {k: round(v, 2) for k, v in totals.items()}
    out["total"]["max"] = sum(r.questions.values())
    return out


# --------------------------------------------------------------------------- #
# Grader agent
# --------------------------------------------------------------------------- #
class Verdict(BaseModel):
    rationale: str = Field(description="Brief evidence: what the submission says (quote or "
                           "locate it) and any tool checks. Explain any 'unclear'.")
    verdict: Literal["yes", "no", "unclear"]


def verdict_model(r: Rubric) -> type[BaseModel]:
    """One required Verdict per criterion, nested per question, in rubric order."""
    fields = {}
    for qid in r.questions:
        qmodel = create_model("%sVerdicts" % qid,
                              **{c.id: (Verdict, ...) for c in r.for_question(qid)})
        fields[qid] = (qmodel, ...)
    fields["rubric_feedback"] = (str, Field(
        description="Problems with the rubric or answer key that this submission exposed "
        "(wrong expected answers, ambiguous criteria, valid answers the key misses). "
        "Empty string if none."))
    return create_model("GraderVerdicts", **fields)


MISSING_VERDICT = {"verdict": "unclear",
                   "rationale": "(no verdict: criterion added to the rubric after grading)"}


def flatten_verdicts(output: dict, r: Rubric) -> dict[str, str]:
    """Criterion id -> verdict. Criteria the grader never saw count as unclear."""
    return {c.id: output.get(c.question, {}).get(c.id, MISSING_VERDICT)["verdict"]
            for c in r.criteria}


GRADER_INSTRUCTIONS = """\
You are the grader for a policy-research benchmark. An AI agent was given the \
task below and the Federal Register tools you also have. Its answer arrives in \
the next message. Grade it against the answer key and the rubric criteria.

# What you produce

A verdict for every rubric criterion: "yes", "no" or "unclear", each with a \
brief rationale. You do not assign points. Code computes the score from your \
verdicts, so judge each criterion on its own and do not soften verdicts to \
adjust a total.

# How to judge

- Each criterion is a statement about the submission. "yes" means the \
submission clearly satisfies it. "no" means it clearly does not, including \
when the point is missing or wrong. "unclear" is for the specific cases in \
the "unclear" section below.
- Where a criterion marks an element as "welcome but not required" or says \
"either ... is enough", do not withhold "yes" for the missing optional \
element. Every other element of a criterion is required: if one is missing, \
the verdict is "no".
- Judge a question's criteria on that question's answer, basis and \
uncertainty fields. Content under another question counts only if this \
question's answer explicitly refers to it.
- Accept equivalent wording and correct extra detail. Dates, document numbers, \
citations and amounts must be right; the key notes where alternatives are \
acceptable.
- The answer key's general rules apply through your verdicts. If a part relies \
on a fabricated source, treats a proposed rule as in force, or presents a \
commenter's statement as a DHS finding, answer "no" on that part's credit \
criteria. Claims based on sources outside the Federal Register (USCIS or SEVP \
websites, memory) earn no credit.
- Credit criteria: "yes" earns credit. Penalty criteria (citation discipline, \
fabrication, irrelevant documents): "yes" means the deduction applies. Gate \
criteria: "yes" means the submission flags the uncertainty or meets the \
condition described; without it the related credit is reduced.
- "At least k" ladders: count qualifying items carefully, and keep the counts \
consistent across the ladder. In each rationale, list the items you counted. \
"At least 3" cannot be "yes" unless "at least 2" is; a count of items with some \
further property (an accurate location, a correct status) cannot exceed the \
count of items. A ladder that breaks these rules is set aside for human review.
- The key is not exhaustive. If the submission gives an answer the key does not \
anticipate, check it with the tools. Credit it when it is correct and meets the \
criterion's intent, and say so in rubric_feedback.

# Tools

You have fr_search, fr_doc, fr_toc, fr_grep and fr_text, the same Federal \
Register tools the agent had. Use them to check citations, quotations, \
documents or claims the key does not cover, especially before answering "yes" \
to a fabrication penalty. You do not need to re-verify facts the key already \
states. The world is as of November 14, 2026.

# "unclear"

"unclear" is not a middle grade. The headline score counts it as "no", and \
every "unclear" is listed for a human to resolve, with the score range showing \
what each resolution would give. Use it only when a careful reader with the \
tools still could not settle the verdict:

1. The submission is genuinely ambiguous on the point: it can fairly be read \
either as satisfying the criterion or not. Examples: a date is given but it is \
impossible to tell which provision or counting rule produced it; a caveat \
appears but it is unclear whether it attaches to this part or to another one; \
a required element is implied but not stated.
2. The verdict depends on a fact you tried to check and could not: the cited \
document or page could not be retrieved, or searching did not find a passage \
the submission relies on and you cannot rule out that it exists. This applies \
especially to the fabrication penalty: answer "yes" only after confirming the \
source does not exist or does not contain the claim, and "unclear" if you \
could not confirm either way.
3. The submission takes a reasonable approach the key and criterion do not \
anticipate, you checked it with the tools, and you still cannot tell whether \
it meets the criterion's intent. Or the criterion or key appears to be wrong \
for this submission (for example, it demands a figure the submission shows is \
incorrect).

Do not use "unclear":

- When the point is missing or wrong. That is "no".
- When a required element of the criterion is absent. That is "no", even if \
the rest is excellent.
- Before you have checked. If a tool call could settle it, make the call.
- To split the difference on a judgment call you are able to make, or to \
soften or raise a score. Decide, and explain the decision.

For every "unclear", the rationale must name which of the three cases applies \
and what would resolve it: the two readings, the check that failed, or the \
suspected problem in the key. Most criteria in a submission should get "yes" \
or "no". Note general problems with the rubric or key in rubric_feedback.
"""


def stable_prefix(task_md: str, key_md: str, r: Rubric) -> str:
    lines = [GRADER_INSTRUCTIONS,
             "\n# Task given to the agent (TASK.md)\n\n<task>\n%s\n</task>\n" % task_md.strip(),
             "\n# Answer key (ANSWER_KEY.md)\n\n<answer_key>\n%s\n</answer_key>\n"
             % key_md.strip(),
             "\n# Rubric criteria\n",
             "Give a verdict for every criterion below, in the output field with the same id. "
             "Kinds: [credit], [penalty], [gate].\n"]
    for qid in r.questions:
        lines.append("\n## %s\n" % qid)
        for c in r.for_question(qid):
            lines.append("- `%s` [%s]: %s" % (c.id, c.kind, c.text))
    return "\n".join(lines) + "\n"


SUBMISSION_TEMPLATE = """\
Grade the following submission. Give a verdict for every criterion.

<submission>
{answer}
</submission>
"""


def report_markdown(output: dict, scores: dict, r: Rubric, source: str) -> str:
    t = scores["total"]
    out = ["# Grading report", "", "Submission: `%s`" % source, "",
           "**Score: %.2f / %g** (unclear counted as no; range %.2f to %.2f)"
           % (t["score"], t["max"], t["score_min"], t["score_max"]), ""]
    if scores["unclear"]:
        out += ["Unclear verdicts for human review: " +
                ", ".join("`%s`" % u for u in scores["unclear"]), ""]
    if scores["inconsistent_ladders"]:
        out += ["Inconsistent \"at least k\" ladders for human review (a \"yes\" that "
                "contradicts a lower rung or the ladder it depends on is scored as unclear): "
                + ", ".join("`%s`" % l for l in scores["inconsistent_ladders"]), ""]
    if output.get("rubric_feedback", "").strip():
        out += ["## Rubric feedback", "", output["rubric_feedback"].strip(), ""]
    out += ["| Question | Score | Max | Range |", "|---|---|---|---|"]
    for qid, q in scores["questions"].items():
        out.append("| %s | %.2f | %g | %.2f to %.2f |"
                   % (qid, q["score"], q["points"], q["score_min"], q["score_max"]))
    for qid, q in scores["questions"].items():
        out += ["", "## %s: %.2f / %g" % (qid, q["score"], q["points"]), "",
                "| Criterion | Kind | Verdict | Points | Rationale |", "|---|---|---|---|---|"]
        for c in r.for_question(qid):
            v = output.get(qid, {}).get(c.id, MISSING_VERDICT)
            raw = q["points_by_criterion"].get(c.id)
            eff = q.get("effective_points_by_criterion", {}).get(c.id, raw)
            if raw is None:
                pts = ""
            elif eff == raw:
                pts = "%g" % raw
            else:  # reduced by the group's cap or gate factor
                pts = "%g (of %g)" % (eff, raw)
            rationale = " ".join(v["rationale"].split()).replace("|", "\\|")
            out.append("| `%s` | %s | %s | %s | %s |" % (
                c.id, c.kind, v["verdict"], pts, rationale))
    return "\n".join(out) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_scores(out_dir: Path, output: dict, r: Rubric, source: str) -> dict:
    scores = score_verdicts(r, flatten_verdicts(output, r))
    hc.write_json(out_dir / "score.json", scores)
    (out_dir / "report.md").write_text(report_markdown(output, scores, r, source),
                                       encoding="utf-8")
    return scores


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", nargs="?", help="bench run folder (reads answer.md)")
    ap.add_argument("--answer", help="grade this Markdown answer file instead of a run")
    ap.add_argument("--out", help="output folder (default <run>/grades/<grade-id>)")
    ap.add_argument("--rescore", metavar="GRADE_DIR",
                    help="recompute score.json and report.md from an existing "
                    "verdicts.json with the current rubric; no API calls")
    ap.add_argument("--cache-ttl", choices=["30m", "12h"], default="30m",
                    help="minimum lifetime of the stable-prefix breakpoint (default 30m); "
                    "the implicit breakpoints keep the default 30m")
    hc.add_agent_args(ap, default_max_turns=80, model_required=False)
    a = ap.parse_args(argv)

    rubric = load_rubric(hc.RUBRIC_PATH)

    if a.rescore:
        d = Path(a.rescore)
        output = json.loads((d / "verdicts.json").read_text(encoding="utf-8"))
        meta = json.loads((d / "transcript.json").read_text(encoding="utf-8"))["config"]
        scores = write_scores(d, output, rubric, meta.get("answer_file", "?"))
        print("%.2f / %g" % (scores["total"]["score"], scores["total"]["max"]))
        return 0

    if bool(a.run) == bool(a.answer):
        ap.error("give either a run folder or --answer")
    if not a.model:
        ap.error("--model is required")
    answer_path = Path(a.answer) if a.answer else Path(a.run) / "answer.md"
    answer_md = answer_path.read_text(encoding="utf-8")

    grade_id = hc.slug("%s_%s_%s" % (hc.datetime.now().strftime("%Y%m%d-%H%M%S"),
                                     a.model, a.effort or "default"))
    if a.out:
        out_dir = Path(a.out)
    elif a.run:
        out_dir = Path(a.run) / "grades" / grade_id
    else:
        out_dir = hc.RUNS_DIR / "grades" / grade_id
    out_dir.mkdir(parents=True, exist_ok=False)

    task_md = hc.read_text(hc.TASK_PATH)
    key_md = hc.read_text(hc.ANSWER_KEY_PATH)
    Verdicts = verdict_model(rubric)
    initial_input = [
        # Stable prefix: identical for every submission graded with the same
        # task, key, rubric and settings. The explicit breakpoint ends it.
        {"role": "developer", "content": [{
            "type": "input_text", "text": stable_prefix(task_md, key_md, rubric),
            "prompt_cache_breakpoint": {"mode": "explicit", "ttl": a.cache_ttl}}]},
        hc.user_message(SUBMISSION_TEMPLATE.format(answer=answer_md.strip())),
    ]

    client = hc.make_client(a.timeout)
    config = hc.agent_config(a, client) | {
        "grade_id": out_dir.name, "answer_file": str(answer_path),
        "sha256": {"answer": sha256(answer_path), "task": sha256(hc.TASK_PATH),
                   "answer_key": sha256(hc.ANSWER_KEY_PATH),
                   "rubric": sha256(hc.RUBRIC_PATH)},
        "criteria": len(rubric.criteria),
    }
    transcript = hc.Transcript(
        out_dir / "transcript.json", "grader", config,
        hc.static_request(hc.FR_TOOLS, Verdicts, a), initial_input)
    hc.log("grading %s -> %s" % (answer_path, out_dir))

    try:
        result = hc.run_agent(
            client, model=a.model, effort=a.effort, reasoning_summary=a.reasoning_summary,
            input_items=initial_input, tools=hc.FR_TOOLS, text_format=Verdicts,
            transcript=transcript, max_turns=a.max_turns, context_budget=a.context_budget,
            provider=a.provider)
    except BaseException as e:
        transcript.finish("error", error="%s: %s" % (type(e).__name__, e))
        raise

    output = result.output.model_dump() if result.output else None
    transcript.finish(result.status, final_output=output, error=result.error)
    transcript.warn_tool_errors()
    usage = transcript.data["usage_total"]
    details = usage.get("input_tokens_details", {})
    hc.log("status=%s turns=%d tool_calls=%d input=%s (cached %s, cache writes %s) output=%s"
           % (result.status, len(transcript.data["turns"]),
              transcript.data["tool_calls_total"], usage.get("input_tokens"),
              details.get("cached_tokens"), details.get("cache_write_tokens"),
              usage.get("output_tokens")))
    if output is None:
        hc.log("no verdicts: %s" % result.error)
        return 1
    hc.write_json(out_dir / "verdicts.json", output)
    scores = write_scores(out_dir, output, rubric, str(answer_path))
    t = scores["total"]
    hc.log("score %.2f / %g (range %.2f to %.2f, %d unclear, %d inconsistent ladder(s))"
           % (t["score"], t["max"], t["score_min"], t["score_max"], len(scores["unclear"]),
              len(scores["inconsistent_ladders"])))
    print(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
