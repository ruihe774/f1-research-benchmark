# FR Research Benchmark

A benchmark for LLM agents doing policy research on the U.S. Federal Register. Each task casts the agent as a researcher at an organization that needs answers about a set of 2026 federal actions. The agent gets only Federal Register search and reading tools, and its answers are graded against a confidential answer key by a second LLM agent.

All tasks share one harness, one frozen corpus of Federal Register documents, and one reference date, **November 14, 2026**. Each task is worth 100 points:

| Task | Folder | Role and subject | Questions |
|---|---|---|---|
| F-1 | `tasks/f1/` (default) | International student office; the DHS final rule ending "duration of status" for F-1 students, with the proposed rules, notices and presidential documents around it | 16 |
| Tariffs | `tasks/tariffs/` | Customs broker's researcher; the 2026 section 338 duties and import exclusions on Canadian products, the July 2026 section 301 forced-labor tariffs, and how both interact with section 232 and earlier duties | 15 |
| RIF | `tasks/rif/` | Federal HR office researcher; OPM's 2026 rewrite of the reduction in force rules (5 CFR part 351), its corrections, the RIF appeals rule and related rules | 14 |

The tasks rest on policy changes made in 2026, so they cannot be answered from memory. The Tariffs and RIF tasks lean on what separated models on the F-1 task: computations that chain several provisions across documents, places where a preamble or recital says something different from the operative text, reviews of a worked file with planted errors and sound steps, exhaustive comparisons with a count ladder, and passages with no keyword handle.

## What it tests

- Finding the governing documents in a large corpus, and reading long regulatory text closely.
- Applying rule provisions to concrete scenarios, with date and rate arithmetic shown.
- Telling the kinds of authority apart: final rule text, preamble, commenters, proposed rules and presidential documents.
- Flagging gaps honestly where the text is silent. TASK.md says a confident unsupported answer is worse than a flagged gap.
- Avoiding stale or wrong sources. Some pending proposals look relevant but are not in force.

## Results

Score against theoretical cost per run (log scale), one plot per task. Small points are individual runs, large points are the mean per model and effort, and the dashed line is the Pareto frontier of the means. Models far below the rest are left off the plot and named in its footnote. The per-model numbers are in `analysis/<task>/model_summary.csv`.

### F-1

![F-1: cost vs score](analysis/f1/cost_vs_score.png)

### Tariffs

![Tariffs: cost vs score](analysis/tariffs/cost_vs_score.png)

### RIF

![RIF: cost vs score](analysis/rif/cost_vs_score.png)

## Layout

| Path | Purpose |
|---|---|
| `tasks/<name>/` | One folder per task. The F-1 task is `tasks/f1/`, the default. |
| `tasks/<name>/TASK.md` | The agent's only instructions: role, tools, ground rules and the questions. |
| `tasks/<name>/ANSWER_KEY.md` | Confidential reference answers. **Never show it to the agent under test.** |
| `tasks/<name>/rubric.toml` | Machine-readable criteria derived from the answer key, with points, caps, gates and penalties. |
| `tasks/<name>/runs/` | Output of runs and grades (committed). |
| `bench.py` | Runs the agent on a task's `TASK.md` and records structured answers. |
| `grader.py` | Grades a run against its task's `ANSWER_KEY.md` and `rubric.toml`. |
| `harness_common.py` | Shared code: the agent loop (OpenAI Responses API), the FR function tools, transcript recording. |
| `fr_tool.py` | The Federal Register search/read tool (`search`, `doc`, `toc`, `text`, `grep`). Standard library only. |
| `corpus/` | Frozen snapshot of the documents (`<doc-number>.txt` plus `.json` metadata), shared by all tasks. |
| `analysis/pricing.csv` | Per-model token prices (USD per 1M tokens), by context tier. Shared by all tasks. |
| `analysis/theoretical_cost.py` | Computes each run's theoretical cost from its transcript and `pricing.csv`; writes `analysis/<task>/runs_theoretical_cost.csv`. |
| `analysis/plot_cost_vs_score.py` | Plots score against cost; writes `analysis/<task>/cost_vs_score.png` and `model_summary.csv`. |
| `analysis/<task>/` | Cost and plot outputs for `f1`, `tariffs` and `rif`. |

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` in the repo root (gitignored):

```
OPENAI_API_KEY=...
# optional
OPENAI_BASE_URL=...
FR_TOOL_CACHE=/path/to/cache
```

## Running

Run the agent under test:

```bash
uv run bench.py --model <model-id> --effort high                 # the F-1 task
uv run bench.py --task <name> --model <model-id> --effort high   # another task under tasks/
```

Options (shared with the grader's agent):

| Flag | Meaning |
|---|---|
| `--task` | Task folder name under `tasks/` (default `f1`). The grader takes it from the run. |
| `--model` | Model ID (required). |
| `--effort` | Reasoning effort. |
| `--reasoning-summary` | Reasoning summary mode (default `auto`). |
| `--max-turns` | Turn limit (default 200 for `bench.py`). |
| `--context-budget` | Context budget. Every tool result ends with a line giving the tokens left. The loop asks for the final answer when the turn limit or budget is reached. |
| `--timeout` | Request timeout in seconds (default 3600). |
| `--run-id` | Output folder name (default `<timestamp>_<model>_<effort>`). |

Each run writes to `tasks/<name>/runs/<run-id>/`:

- `transcript.json`: every response, tool call, tool result and token usage.
- `answer.json`: the structured final answer.
- `answer.md`: the same answer as a Markdown memo. This is what the grader reads.

Each question gets three fields: `answer` (each lettered part, in order), `basis` (citations) and `uncertainty` (or "None").

Grade a run:

```bash
uv run grader.py tasks/f1/runs/<run-id> --model <grader-model> --effort high
uv run grader.py --answer some_answer.md --model <grader-model> --task f1   # grade a Markdown file
uv run grader.py --rescore tasks/f1/runs/<run-id>/grades/<grade-id>         # recompute points from saved verdicts
```

Grader outputs go to `<run>/grades/<grade-id>/` (or `--out`): `transcript.json`, `verdicts.json`, `score.json` and `report.md`. `--cache-ttl {30m,12h}` sets the prompt-cache lifetime for the grading prefix.

## Cost and analysis

```bash
uv run analysis/theoretical_cost.py [task]     # writes analysis/<task>/runs_theoretical_cost.csv
uv run analysis/plot_cost_vs_score.py [task]   # writes analysis/<task>/cost_vs_score.png and model_summary.csv
```

`task` is a folder under `tasks/` (default `f1`); each script reads that task's runs in `tasks/<task>/runs/`. Run the cost script first. For a run with several grades the plot uses the latest. Theoretical cost assumes every cacheable token is a cache hit and every new token (user prompt, tool results) is a miss. Prices come from `pricing.csv`, with context-size tiers where a provider has them.

## The Federal Register tools

The agent has five function tools: `fr_search`, `fr_doc`, `fr_toc`, `fr_grep` and `fr_text`. It has no web access and no other databases (no eCFR, USCIS or SEVP sites). Documents are identified by FR document number, such as `2026-14439`.

The same tools work from the command line:

```bash
uv run fr_tool.py search "duration of status" --type RULE --since 2025-01-01
uv run fr_tool.py toc 2026-14439
uv run fr_tool.py grep 2026-14439 "within 5 months" --context 3
```

### Reproducibility

- The tool reads full texts from the frozen `corpus/` snapshot (`FR_TOOL_SNAPSHOT`) before it checks the cache or the network.
- `FR_TOOL_AS_OF=YYYY-MM-DD` hides every document published after that date. The harness records this value in each run's config.
- A downloaded document joins the snapshot if you copy its `.txt` and `.json` files into `corpus/`.

## Scoring

A task's `rubric.toml` lists criteria for each question, plus criteria applied to every question (such as citations). The grader agent gives each criterion a verdict of `yes`, `no` or `unclear`. It never sees point values. `grader.py` turns verdicts into points:

- **credit** criteria add points on `yes`. **penalty** criteria deduct points on `yes`.
- **gate** criteria carry no points. A group whose gate is not `yes` has its credit multiplied by the group's `factor`.
- **ladders** ("at least 1", "at least 2", ...) count items. Only the unbroken run of `yes` from the first rung counts. A `yes` that breaks the rule is scored as `unclear` and flagged for human review.
- A question's score is credits minus penalties, clamped to `[0, question points]`.
- The headline score counts `unclear` as `no`. `score_min` and `score_max` resolve every `unclear` against or in favour of the submission.

Where `rubric.toml` and the point split in `ANSWER_KEY.md` differ, `rubric.toml` decides.

| Question | Topic | Points |
|---|---|---|
| Q1 | The D/S final rule: citation, dates, docket, RIN, NPRM | 3 |
| Q2 | Authorized stay after program end, transfer timing, OPT filing | 6 |
| Q3 | Admission period, program extension, filing deadlines, work authorization | 8 |
| Q4 | Travel while an I-539 is pending | 5 |
| Q5 | SEVIS transfer from a master's to a PhD program | 7 |
| Q6 | Whether a second master's-level program is allowed | 5 |
| Q7 | The H-1B $100,000 payment, fee proposals, change of status | 8 |
| Q8 | The proposed rule on the 60-day grace period | 4 |
| Q9 | Changes between the proposed and final rule | 3 |
| Q10 | Other documents relevant to post-graduation work | 4 |
| Q11 | Extension-of-stay cost and processing time | 4 |
| Q12 | Timeliness of filing in the 60-day period, employment | 5 |
| Q13 | Travel during the transition period and its effect on stay and OPT filings | 10 |
| Q14 | The OPT fee proposal applied to a STEM OPT extension | 10 |
| Q15 | Checking seven draft statements against the rule text and preamble | 9 |
| Q16 | A six-year program: four-year cap, extension, re-entry, F-2 spouse | 9 |
| | **Total** | **100** |

Tariffs task (`tasks/tariffs/`):

| Question | Topic | Points |
|---|---|---|
| Q1 | Inventory of the section 338 proclamations against Canada | 2 |
| Q2 | The three-day delay of the duties' start date | 3 |
| Q3 | Import exclusion versus duty: arrival, warehouse and zone cases | 3 |
| Q4 | Section 338 duties on goods that also bear section 232 duties | 4 |
| Q5 | Scope changes: the Part A and Part B lists | 3 |
| Q6 | Section 301 rates by economy, flat and net of the MFN rate | 3 |
| Q7 | Specific and compound MFN rates | 1 |
| Q8 | Section 301 start date and goods in transit | 2 |
| Q9 | Chapter 98, USMCA and section 232 goods under the section 301 action | 3 |
| Q10 | Canadian goods under both actions | 3 |
| Q11 | Where the documents of each action disagree (count ladder) | 25 |
| Q12 | Exemptions for particular articles, economy by economy | 4 |
| Q13 | Section 232 duty on a USMCA machine: non-U.S. content, the minimum, the Commerce guidance | 19 |
| Q14 | Ten statements checked against the memorandum, the notice and the proposal | 10 |
| Q15 | Duties owed on Canadian aluminum extrusions at fourteen dates in 2025 and 2026 | 15 |
| | **Total** | **100** |

RIF task (`tasks/rif/`):

| Question | Topic | Points |
|---|---|---|
| Q1 | The final rule, its corrections and other rules amending part 351 | 3 |
| Q2 | A six-employee retention register | 3 |
| Q3 | Retired members of the uniformed services | 2 |
| Q4 | The four-year period, cutoff dates and missing ratings | 3 |
| Q5 | Which rules apply, and when standing is fixed | 3 |
| Q6 | Assignment rights | 1 |
| Q7 | RIF appeals: forum, deadline, burden | 4 |
| Q8 | Administrative leave during the notice period | 3 |
| Q9 | Review of a twelve-step RIF file with planted errors | 7 |
| Q10 | The career transition definition of "displaced" and its correction | 1 |
| Q11 | Proposed versus final regulatory text of part 351 (count ladder) | 10 |
| Q12 | A RIF with a restoration-protected employee and assignment rights | 7 |
| Q13 | Where the main rule's preamble and its regulatory text part ways (count ladder) | 28 |
| Q14 | The appeals rule against its text, its proposal and the MSPB's rule (count ladder) | 25 |
| | **Total** | **100** |

In both newer tasks the early questions come from drafts that two inexpensive models answered almost perfectly. They keep their criteria at a reduced weight through `criteria_points`; most of the points sit in questions with no fixed number of answers, where the agent must find discrepancies on its own and is scored on a count ladder against a verified list.

In the F-1 task, Q13–Q16 were added after the first round of runs showed Q1–Q12 close to saturated for the strongest models. Q1–Q12 keep their original criteria and internal point split. Each carries `criteria_points` in `rubric.toml`, and `grader.py` scales its credits, caps and penalties to the weight above.

## Notes for maintainers

- Keep every `ANSWER_KEY.md` and `rubric.toml` out of anything the agent can read. `bench.py` gives the agent only the task's `TASK.md` and the FR tools.
- To add a task, create `tasks/<name>/` with `TASK.md` (questions under `### Qn` headings), `ANSWER_KEY.md` and `rubric.toml`, and copy its documents into `corpus/`. A `[grader]` table in the rubric can replace the F-1 wording in the grader's instructions (`finding`, `outside_sources`).
- `TASK.md` should not contain answer-bearing examples. A past commit removed them from the tool examples.
- Not all of the corpus is relevant. It includes proposed rules, a correction and presidential documents that bear on the questions, some only as distractors.
