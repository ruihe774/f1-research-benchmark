"""Plot benchmark score against log-scale theoretical cost, one point per run."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis"

# Okabe-Ito, colorblind-safe; one hue per provider
COLORS = {
    "anthropic": "#D55E00", "openai": "#0072B2", "google": "#009E73",
    "deepseek": "#CC79A7", "meta": "#E69F00", "z-ai": "#56B4E9",
    "moonshotai": "#7A7A7A",
}


# label offsets (points) to keep the crowded top-right cluster legible
OFFSETS = {
    "gpt-6.1-sol": (-6, 12, "right"),
    "gemini-4-hydrogen": (0, -17, "center"),
    "claude-sonnet-5-5": (0, 12, "center"),
    "gemini-4-carbon": (0, -17, "center"),
    "claude-opus-5-5": (0, 12, "center"),
}


def score(run):
    totals = [json.loads(p.read_text())["total"]["score"]
              for p in sorted((ROOT / "runs" / run / "grades").glob("*/score.json"))]
    return totals[-1] if totals else None


df = pd.read_csv(OUT / "runs_theoretical_cost.csv")
df["score"] = df["run"].map(score)
df["provider"] = df["model"].str.split("/").str[0]
df["name"] = df["model"].str.split("/").str[1]
df = df.dropna(subset=["score"])

summary = (df.groupby(["name", "provider"])
             .agg(cost=("theoretical_cost_usd", "mean"), score=("score", "mean"),
                  smin=("score", "min"), smax=("score", "max"), n=("run", "count"))
             .reset_index().sort_values("cost"))
summary.round(3).to_csv(OUT / "model_summary.csv", index=False)
print(summary.round(2).to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
for _, r in df.iterrows():
    ax.scatter(r.theoretical_cost_usd, r.score, s=40, color=COLORS[r.provider],
               alpha=0.45, edgecolor="white", linewidth=0.8, zorder=3)
for _, r in summary.iterrows():
    c = COLORS[r.provider]
    ax.scatter(r.cost, r.score, s=110, color=c, edgecolor="white", linewidth=1.5, zorder=4)
    dx, dy, ha = OFFSETS.get(r["name"], (7, 6, "left"))
    ax.annotate(r["name"], (r.cost, r.score), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color="#222", ha=ha, zorder=5)

# Pareto frontier of model means (cheapest-first, strictly improving score)
front, best = [], -1
for _, r in summary.iterrows():
    if r.score > best:
        front.append((r.cost, r.score)); best = r.score
ax.step(*zip(*front), where="post", color="#999", lw=1.2, ls="--", zorder=2)

ax.set_xscale("log")
ax.set_xlim(0.03, 3.6)
ax.set_xlabel("Theoretical cost per run (USD, log scale)")
ax.set_ylabel("Score (out of 100)")
ax.set_title("F-1 Research Benchmark: score vs. cost", loc="left", fontsize=13, weight="bold")
ax.grid(True, which="major", color="#e5e5e5", lw=0.8, zorder=0)
ax.grid(True, which="minor", axis="x", color="#f1f1f1", lw=0.5, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.xaxis.set_major_formatter(lambda v, _: f"${v:g}")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=p) for p, c in COLORS.items()]
ax.legend(handles=handles, title="Provider", frameon=False, loc="lower right", fontsize=9)
ax.text(0.01, 0.01, "Small points: individual runs. Large: model mean. Dashed: Pareto frontier of means.",
        transform=ax.transAxes, fontsize=8, color="#666")
fig.tight_layout()
fig.savefig(OUT / "cost_vs_score.png")
