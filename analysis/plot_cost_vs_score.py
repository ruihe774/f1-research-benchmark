"""Plot benchmark score against log-scale theoretical cost, one point per run."""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text

ROOT = Path(__file__).resolve().parent.parent
TASK = sys.argv[1] if len(sys.argv) > 1 else "f1"
OUT = ROOT / "analysis" / TASK
RUNS = ROOT / "tasks" / TASK / "runs"
TITLES = {"f1": "F-1", "tariffs": "Tariffs", "rif": "RIF"}

# Okabe-Ito, colorblind-safe; one hue per provider
COLORS = {
    "anthropic": "#D55E00", "openai": "#0072B2", "google": "#009E73",
    "deepseek": "#CC79A7", "meta": "#E69F00", "z-ai": "#56B4E9",
    "moonshotai": "#7A7A7A",
}


def score(run):
    totals = [json.loads(p.read_text())["total"]["score"]
              for p in sorted((RUNS / run / "grades").glob("*/score.json"))]
    return totals[-1] if totals else None


def effort(run):
    return json.loads((RUNS / run / "transcript.json").read_text())["config"]["reasoning_effort"]


df = pd.read_csv(OUT / "runs_theoretical_cost.csv")
df["effort"] = df["run"].map(effort)
df["score"] = df["run"].map(score)
df["provider"] = df["model"].str.split("/").str[0]
df["name"] = df["model"].str.split("/").str[1]
df = df.dropna(subset=["score"])

summary = (df.groupby(["name", "provider", "effort"])
             .agg(cost=("theoretical_cost_usd", "mean"), score=("score", "mean"),
                  smin=("score", "min"), smax=("score", "max"), n=("run", "count"))
             .reset_index().sort_values("cost"))
# efforts are never averaged together; label a model's points with its effort only if it has several
multi = summary.groupby("name")["effort"].transform("nunique") > 1
summary["label"] = summary["name"].where(~multi, summary["name"] + " (" + summary["effort"] + ")")
summary.round(3).to_csv(OUT / "model_summary.csv", index=False)
print(summary.round(2).to_string(index=False))

# Models far below the rest (e.g. runs that gave up early) would compress the axes; leave them
# out of the plot and list them in a footnote instead. model_summary.csv still has them.
cut = df.score.median() - 25
off = summary[summary.score < cut]
summary = summary[summary.score >= cut]
df = df[df.set_index(["name", "effort"]).index.isin(summary.set_index(["name", "effort"]).index)]
offnote = "; ".join(f"{r.label} (mean {r.score:.1f}, ${r.cost:.3f})" for _, r in off.iterrows())

fig, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
for _, r in df.iterrows():
    ax.scatter(r.theoretical_cost_usd, r.score, s=40, color=COLORS[r.provider],
               alpha=0.45, edgecolor="white", linewidth=0.8, zorder=3)
texts = []
for _, r in summary.iterrows():
    c = COLORS[r.provider]
    ax.scatter(r.cost, r.score, s=110, color=c, edgecolor="white", linewidth=1.5, zorder=4)
    texts.append(ax.text(r.cost, r.score, r["label"], fontsize=8.5, color="#222", zorder=5))

# Pareto frontier of model means (cheapest-first, strictly improving score)
front, best = [], -1
for _, r in summary.iterrows():
    if r.score > best:
        front.append((r.cost, r.score)); best = r.score
ax.step(*zip(*front), where="post", color="#999", lw=1.2, ls="--", zorder=2)

ax.set_xscale("log")
if TASK == "f1":
    ax.set_ylim(77.5, 100.5)
    ax.set_xlim(0.03, 3.6)
else:
    ax.set_ylim(max(0, df.score.min() - 4), min(100.5, df.score.max() + 4))
    ax.set_xlim(df.theoretical_cost_usd.min() * 0.7, df.theoretical_cost_usd.max() * 1.6)
ax.set_xlabel("Theoretical cost per run (USD, log scale)")
ax.set_ylabel("Score (out of 100)")
ax.set_title(f"FR Research Benchmark, {TITLES.get(TASK, TASK)} task: score vs. cost", loc="left", fontsize=13, weight="bold")
ax.grid(True, which="major", color="#e5e5e5", lw=0.8, zorder=0)
ax.grid(True, which="minor", axis="x", color="#f1f1f1", lw=0.5, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.xaxis.set_major_formatter(lambda v, _: f"${v:g}")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=p) for p, c in COLORS.items() if p in set(df.provider)]
ax.legend(handles=handles, title="Provider", frameon=False, loc="lower right", bbox_to_anchor=(1, 0.04), fontsize=9)
ax.text(0.01, 0.01, "Small points: individual runs. Large: mean per model and effort. Dashed: Pareto frontier of means.\n"
        "Labels without parentheses are high effort; models run at several efforts show the effort in parentheses.",
        transform=ax.transAxes, fontsize=8, color="#666")
if offnote:
    ax.text(0.01, 0.075, "Not shown (far below axis): " + offnote, transform=ax.transAxes,
            fontsize=8, color="#666", ha="left", va="bottom")
# place labels last: adjust_text needs the final scale and limits, and avoids every point
fig.canvas.draw()
adjust_text(texts, x=np.r_[df.theoretical_cost_usd, summary.cost], y=np.r_[df.score, summary.score], ax=ax,
            arrowprops=dict(arrowstyle="-", color="#999", lw=0.6),
            expand=(1.05, 1.2), force_pull=(0.05, 0.05), pull_threshold=3, explode_radius=30,
            max_move=(8, 8), min_arrow_len=6)
fig.tight_layout()
fig.savefig(OUT / "cost_vs_score.png")
