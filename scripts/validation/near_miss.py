"""
Near-miss analysis: does showing methods that fail exactly one specified criterion
recover the recall lost to assessment errors?

Run from the repository root:
    python3 scripts/validation/near_miss.py [--reps 5]

Same design as the error-propagation analysis in engine_sensitivity.py (studies from the TRUE
table, run on a PERTURBED table). The near-miss set is the union of the strict result and the
methods returned by NaviDAMSuggestionEngine.suggest_near_misses (the near-miss feature of the website),
i.e. all methods failing at most one criterion. Results are saved as near_miss.json / near_miss_runs.csv in the results folder.
"""
import argparse, json, random
from pathlib import Path
import pandas as pd
from scripts.validation import engine_sensitivity as es
from scripts.validation.engine_sensitivity import ns, K_LEVELS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="scripts/validation/engine_sensitivity/engine_eval_model_specific_20261029")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    out = Path(a.out)
    rng = random.Random(a.seed)
    rows = es.load_rows()
    pool = es.option_pool(rows)
    pairs = [(r, o) for r in rows for o in es.values(r, "Objective")]
    recs = []
    for e in [0.05, 0.15, 0.3]:
        for _ in range(a.reps):
            eng = ns.NaviDAMSuggestionEngine(es.perturb(rows, pool, e, rng))
            for r, o in pairs:
                for kk in K_LEVELS[1:]:
                    s = es.make_study(r, o, rng, kk)
                    strict = set(eng.suggest_methods(s))
                    near = strict | {n["Method"] for n in eng.suggest_near_misses(s)}
                    m = r["Method"]
                    recs.append(dict(e=e, k_spec=kk, strict_hit=m in strict, near_hit=m in near,
                                     strict_size=len(strict), near_size=len(near)))
    df = pd.DataFrame(recs)
    df.to_csv(out / "near_miss_runs.csv", index=False)
    g = df.groupby(["e", "k_spec"]).agg(strict_recall=("strict_hit", "mean"), near_recall=("near_hit", "mean"),
                                         strict_size_median=("strict_size", "median"),
                                         near_size_median=("near_size", "median"),
                                         strict_size_mean=("strict_size", "mean"),
                                         near_size_mean=("near_size", "mean")).reset_index()
    json.dump(g.to_dict("records"), open(out / "near_miss.json", "w"), indent=1)
    print(g.round(2).to_string())


if __name__ == "__main__":
    main()
