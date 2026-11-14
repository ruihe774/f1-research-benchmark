# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A benchmark for LLM agents doing policy research over a frozen snapshot of Federal Register documents about the DHS final rule ending "duration of status" for F-1 students. The agent under test answers 16 questions (Q1–Q16, 100 points) in `TASK.md` using only Federal Register tools; a second LLM agent (the grader) scores the answer against a confidential key. The task is set as of 2026-11-14. See `README.md` for the full flag tables and the per-question point table.

There is no test suite or linter. Python 3.13+, managed with `uv`.

## Commands

```bash
uv sync                                                    # install deps
uv run bench.py --model <model-id> --effort high           # run agent -> runs/<run-id>/
uv run grader.py runs/<run-id> --model <grader-model> --effort high
uv run grader.py --answer file.md --model <grader-model>   # grade an arbitrary Markdown answer
uv run grader.py --rescore runs/<run-id>/grades/<grade-id> # recompute points from saved verdicts (no LLM call)
uv run fr_tool.py grep 2026-14439 "within 5 months" --context 3   # tools also work as a CLI (search/doc/toc/text/grep)
uv run theoretical_cost.py                                 # writes runs_theoretical_cost.csv from pricing.csv + run transcripts
uv run analysis/plot_cost_vs_score.py                      # cost vs. score plot in analysis/
```

`.env` needs `OPENAI_API_KEY`; `OPENAI_BASE_URL` (the code uses the OpenAI Responses API, pointed at other providers via a base URL, with model IDs like `anthropic/claude-sonnet-5-5`) and `FR_TOOL_CACHE` are optional.

## Architecture

- `harness_common.py` — shared by `bench.py` and `grader.py`: the agent loop `run_agent` (Responses API, turn limit and `--context-budget` handling, forced final answer when either runs out), pydantic arg models and `Tool` wrappers for the five FR tools, `Transcript` recording, and `add_agent_args`/`agent_config` for the shared CLI flags. Provider quirks go in `request_extra_body`.
- `bench.py` — gives the agent `TASK.md` plus the FR tools, with a structured-output schema (per question: `answer`, `basis`, `uncertainty`). Writes `transcript.json`, `answer.json`, `answer.md`.
- `grader.py` — loads `rubric.toml`, builds a stable (cacheable) prefix of TASK + `ANSWER_KEY.md` + rubric, and has the grader agent return yes/no/unclear verdicts per criterion without seeing point values. Points are computed deterministically in code (`score_verdicts`): credits, penalties, gates with factors, caps, and ladders, with `unclear` counted as `no` in the headline score (`score_min`/`score_max` bound it). `validate_rubric` checks the rubric's consistency.
- `fr_tool.py` — stdlib-only Federal Register search/read tool. Reads full text from `corpus/` first, then the cache, then the network. `FR_TOOL_AS_OF=YYYY-MM-DD` hides later documents (recorded in each run's config).
- `corpus/` — frozen snapshot, `<doc-number>.txt` + `.json` metadata per document. To add a document, copy its pair from `.fr_cache/` (gitignored download cache) into `corpus/`. Some documents are deliberate distractors.
- `rubric.toml` — Q1–Q12 keep their original criteria on an older scale and carry `criteria_points`; `grader.py` rescales them to the question's `points`. Q13+ are written directly in final points. Where it differs from `ANSWER_KEY.md`, `rubric.toml` decides points.

## Rules to preserve

- `ANSWER_KEY.md` and `rubric.toml` must never be reachable by the agent under test; `bench.py` exposes only `TASK.md` and the FR tools.
- `TASK.md` must not contain answer-bearing examples (including in tool-usage examples).
- If you change a question's criteria or points in `rubric.toml`, re-run `grader.py` with `--rescore` on saved grades rather than regrading when only point values changed.
- `runs/` is committed (not gitignored); run outputs and grades are part of the repo history.
