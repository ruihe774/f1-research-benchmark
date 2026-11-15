"""Theoretical cost per run: every token that can be cached is a cache hit, every
token that cannot (new user prompt / tool results) is a cache miss. Prices in
pricing.csv are USD per 1M tokens. Usage: theoretical_cost.py [task] (default f1).
Writes <task>/runs_theoretical_cost.csv."""
import csv, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
TASK = sys.argv[1] if len(sys.argv) > 1 else "f1"
RUNS = HERE.parent / "tasks" / TASK / "runs"
OUT = HERE / TASK
OUT.mkdir(exist_ok=True)
# Context-size tier thresholds (input tokens per request). The OpenAI threshold is
# not given in pricing.csv; 272K is assumed (no request in the runs exceeds 234K).
LONG = {"anthropic/claude-haiku-5-5": 100_000, "meta/muse-ember": 200_000,
        "openai/gpt-6.1-sol": 272_000, "openai/gpt-6.1-terra": 272_000,
        "openai/gpt-6-luna": 272_000}

prices = {}
for r in csv.DictReader(open(HERE / "pricing.csv")):
    prices.setdefault(r["model"], {})[r["tier"]] = r

def pick(model, tier_key):
    t = prices[model]
    return t[tier_key] if tier_key in t else t[""]

def tiers(model):
    """Return (small-tier key, large-tier key) in pricing.csv for a model."""
    return {
        "anthropic/claude-haiku-5-5": ("prompts <=100K", "prompts >100K"),
        "meta/muse-ember": ("<=200K input", ">200K input"),
    }.get(model, ("short context", "long context") if model.startswith("openai/") else ("", ""))

def cost(model, turns, variant=None):
    total = 0.0
    prev = None  # input + output of the previous request = cacheable prefix
    for t in turns:
        u = t.get("usage")
        if not u:
            continue
        inp, out = u["input_tokens"], u["output_tokens"]
        hit = min(prev, inp) if prev is not None else 0  # turn 1: nothing cached yet
        miss = inp - hit
        small, large = tiers(model)
        if model in LONG:
            key = large if inp > LONG[model] else small
        elif model == "deepseek/deepseek-v4.1-flash-1017":
            key = variant
        elif model == "google/gemini-4-carbon":
            key = "through Nov 30 2026"
        else:
            key = ""
        p = pick(model, key)
        total += (miss * float(p["uncached_input"]) + hit * float(p["cached_input_read"])
                  + out * float(p["output"])) / 1e6
        prev = inp + out
    return total

rows = []
for f in sorted((RUNS).glob("*/transcript.json")):
    d = json.load(open(f))
    model = d["config"]["model"]
    variants = ["off-peak", "peak"] if model.startswith("deepseek/") else [None]
    c = {v: cost(model, d["turns"], v) for v in variants}
    u = d["usage_total"]
    rows.append({"run": f.parent.name, "model": model,
                 "input_tokens": u["input_tokens"], "output_tokens": u["output_tokens"],
                 "theoretical_cost_usd": round(c.get(None, c.get("off-peak", 0)), 4),
                 "theoretical_cost_peak_usd": round(c["peak"], 4) if "peak" in c else ""})
with open(OUT / "runs_theoretical_cost.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["run"][:50].ljust(50), r["theoretical_cost_usd"], r["theoretical_cost_peak_usd"])
