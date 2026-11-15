#!/usr/bin/env python3
"""Run the agent under test on TASK.md and record its structured answers.

The agent gets TASK.md as its only instructions and the Federal Register
function tools from harness_common. TASK.md is auto-split (harness_common.
split_task) at its '## Questions' heading: the instructions before it go in
a developer message (higher priority, stable prompt prefix) and the
questions go in a user message. It works in a stateless Responses API loop
and ends with one structured answer per question.

Prompt caching is implicit: OpenAI places a breakpoint at the end of the latest
user message or tool-output group, so each turn reuses the history cached by
the previous one.

Example:
  uv run bench.py --model gpt-6.1-sol --effort high

Outputs go to runs/<run-id>/:
  transcript.json  every request's response, tool call, tool result and usage
  answer.json      the structured final answer
  answer.md        the same answer as a Markdown memo (what the grader reads)
"""

import argparse
import sys

from pydantic import BaseModel, Field, create_model

import harness_common as hc


class QuestionAnswer(BaseModel):
    answer: str = Field(description="Direct answer to each lettered part, in order, "
                        "labelled (a), (b), ...")
    basis: str = Field(description="Provisions and documents relied on, with citations.")
    uncertainty: str = Field(description='What the documents leave open, or "None".')


def answer_model(qids: list[str]) -> type[BaseModel]:
    """A schema with one required QuestionAnswer per question in TASK.md."""
    return create_model("BenchAnswer", **{q: (QuestionAnswer, ...) for q in qids})


def answer_markdown(answer: dict) -> str:
    parts = []
    for qid, qa in answer.items():
        parts.append("## %s\n\n**Answer:**\n%s\n\n**Basis:**\n%s\n\n**Uncertainty:**\n%s\n"
                     % (qid, qa["answer"].strip(), qa["basis"].strip(),
                        qa["uncertainty"].strip()))
    return "\n".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    hc.add_agent_args(ap, default_max_turns=200)
    ap.add_argument("--run-id", help="output folder name under runs/ "
                    "(default: <timestamp>_<model>_<effort>)")
    a = ap.parse_args(argv)

    task_md = hc.read_text(hc.TASK_PATH)
    qids = hc.question_ids(task_md)
    Answer = answer_model(qids)

    run_id = a.run_id or hc.slug("%s_%s_%s" % (
        hc.datetime.now().strftime("%Y%m%d-%H%M%S"), a.model, a.effort or "default"))
    out_dir = hc.RUNS_DIR / run_id
    out_dir.mkdir(parents=True, exist_ok=False)

    client = hc.make_client(a.timeout)
    developer_md, questions_md = hc.split_task(task_md)
    initial_input = [hc.developer_message(developer_md),
                     hc.user_message(questions_md)]
    config = hc.agent_config(a, client) | {"run_id": run_id, "questions": qids,
                                           "task_file": str(hc.TASK_PATH),
                                           "prompt_split": "developer/user at '## Questions'"}
    transcript = hc.Transcript(
        out_dir / "transcript.json", "bench", config,
        hc.static_request(hc.FR_TOOLS, Answer, a), initial_input)
    hc.log("bench run %s -> %s" % (run_id, out_dir))

    try:
        result = hc.run_agent(
            client, model=a.model, effort=a.effort, reasoning_summary=a.reasoning_summary,
            input_items=initial_input, tools=hc.FR_TOOLS, text_format=Answer,
            transcript=transcript, max_turns=a.max_turns, context_budget=a.context_budget,
            provider=a.provider)
    except BaseException as e:
        transcript.finish("error", error="%s: %s" % (type(e).__name__, e))
        raise

    final = result.output.model_dump() if result.output else None
    transcript.finish(result.status, final_output=final, error=result.error)
    transcript.warn_tool_errors()
    usage = transcript.data["usage_total"]
    hc.log("status=%s turns=%d tool_calls=%d input=%s (cached %s) output=%s (reasoning %s)" % (
        result.status, len(transcript.data["turns"]), transcript.data["tool_calls_total"],
        usage.get("input_tokens"), usage.get("input_tokens_details", {}).get("cached_tokens"),
        usage.get("output_tokens"),
        usage.get("output_tokens_details", {}).get("reasoning_tokens")))
    if final is None:
        hc.log("no final answer: %s" % result.error)
        return 1
    hc.write_json(out_dir / "answer.json", final)
    (out_dir / "answer.md").write_text(answer_markdown(final), encoding="utf-8")
    print(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
