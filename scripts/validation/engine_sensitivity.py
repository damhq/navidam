"""
NaviDAM decision-engine evaluation: synthetic-study benchmark, ablation,
and assessment-error propagation.

Run from the NaviDAM repository root (after scripts/clean_method_assessments.py):
    python3 engine_sensitivity.py --out results_dir

Uses the same filtering engine as the website (scripts/validation/navidam_suggester.py).

Design
------
Synthetic studies. Each synthetic study is generated from one "generating"
method m and one of its objectives o: for every criterion applicable to o, the
study keeps a criterion with probability p_spec and, if kept, picks ONE option
at random among the options recorded for m (fallback values Don't know /
Inapplicable are never picked). By construction m is a correct answer to the
study, so:
  * recall  = P(m is in the candidate set)            (must be 1 with exact assessments)
  * size    = number of candidate methods             (informativeness of the output)
Ablation. For fully specified studies (p_spec = 1), each criterion in turn is
reset to "Any" and the increase in candidate-set size is recorded.
Error propagation. Assessments are perturbed: each (method, criterion) cell with
a regular value is, with probability e, replaced by a different random option
set of the same size. Studies are generated from the TRUE table and run on the
PERTURBED table; recall of the generating method is compared with the
independent-error expectation (1 - e)^k, k = number of criteria specified.
"""
import argparse, json, random, sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from scripts.validation import navidam_suggester as ns  # noqa: E402

FALLBACK = {"Don't know", "Inapplicable", ""}


def load_rows():
    d = pd.read_csv(ROOT / "_data" / "method_assessments_clean.tsv", sep="\t", dtype=str).fillna("")
    return d.to_dict("records")


def values(row, c):
    return [v for v in ns._method_values(row, c) if v not in FALLBACK]


def option_pool(rows):
    pool = {}
    for c in ns.FILTER_CRITERIA:
        s = set()
        for r in rows:
            s.update(values(r, c))
        pool[c] = sorted(s)
    for c, order in ns.ORDINAL_CRITERIA_ORDER.items():
        pool[c] = list(order)
    return pool


def applicable(obj):
    return [c for c in ns.FILTER_CRITERIA if c != "Objective" and c in ns.get_used_criteria_keys(obj)]


def make_study(row, obj, rng, p_spec=1.0):
    study = {"Objective": obj}
    for c in applicable(obj):
        vals = values(row, c)
        if not vals or rng.random() > p_spec:
            continue
        study[c] = rng.choice(vals)
    return study


def perturb(rows, pool, e, rng):
    out = []
    for r in rows:
        r2 = dict(r)
        for c in ns.FILTER_CRITERIA:
            if c == "Objective":
                continue
            vals = values(r, c)
            if not vals or rng.random() >= e:
                continue
            opts = [o for o in pool[c] if o not in FALLBACK]
            k = min(len(vals), len(opts))
            for _ in range(20):
                new = rng.sample(opts, k)
                if set(new) != set(vals):
                    break
            r2[c] = "; ".join(new)
        out.append(r2)
    return out


def omit(rows, e, rng):
    """Omission errors: drop one valid option (multi-option cells) or downgrade ordinal capability by one level."""
    out = []
    for r in rows:
        r2 = dict(r)
        for c in ns.FILTER_CRITERIA:
            if c == "Objective":
                continue
            vals = values(r, c)
            if not vals or rng.random() >= e:
                continue
            if c in ns.ORDINAL_CRITERIA_ORDER:
                order = ns.ORDINAL_CRITERIA_ORDER[c]
                pos = [order.index(v) for v in vals if v in order]
                if not pos or max(pos) == 0:
                    continue
                r2[c] = order[max(pos) - 1]
            else:
                if len(vals) < 2:
                    continue
                drop = rng.choice(vals)
                r2[c] = "; ".join(v for v in vals if v != drop)
        out.append(r2)
    return out


def n_specified(study):
    return sum(1 for k in study if k != "Objective")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="engine_eval")
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    rows = load_rows()
    pool = option_pool(rows)
    eng = ns.NaviDAMSuggestionEngine(rows)
    pairs = [(r, o) for r in rows for o in values(r, "Objective")]
    res = {"n_methods": len(rows), "n_method_objective_pairs": len(pairs)}

    # 1. Synthetic-study benchmark across specification levels
    recs = []
    for p in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
        for _ in range(a.reps):
            for r, o in pairs:
                s = make_study(r, o, rng, p)
                cand = eng.suggest_methods(s)
                recs.append(dict(p_spec=p, objective=o, method=r["Method"], k=n_specified(s),
                                 size=len(cand), hit=r["Method"] in cand))
    bench = pd.DataFrame(recs)
    bench.to_csv(out / "benchmark_runs.csv", index=False)
    res["recall_exact_assessments"] = float(bench.hit.mean())
    g = bench.groupby("p_spec").agg(k_mean=("k", "mean"), size_median=("size", "median"),
                                     size_q25=("size", lambda x: x.quantile(.25)),
                                     size_q75=("size", lambda x: x.quantile(.75)),
                                     size_one=("size", lambda x: (x == 1).mean()))
    res["by_specification"] = g.reset_index().to_dict("records")
    full = bench[bench.p_spec == 1.0]
    res["full_spec_by_objective"] = full.groupby("objective").agg(
        n=("size", "size"), k_mean=("k", "mean"), size_median=("size", "median"),
        size_mean=("size", "mean"), unique=("size", lambda x: (x == 1).mean())).reset_index().to_dict("records")
    totals = {o: sum(1 for r in rows if o in values(r, "Objective")) for o in set(full.objective)}
    res["methods_per_objective"] = totals

    # Indistinguishable methods: identical candidate sets under full specification
    # (pairs of methods never separated by any synthetic study)
    # 2. Ablation (fully specified studies)
    abl = defaultdict(list)
    base_sizes = []
    for _ in range(max(5, a.reps // 2)):
        for r, o in pairs:
            s = make_study(r, o, rng, 1.0)
            base = len(eng.suggest_methods(s))
            base_sizes.append(base)
            for c in list(s):
                if c == "Objective":
                    continue
                s2 = {k: v for k, v in s.items() if k != c}
                abl[c].append(len(eng.suggest_methods(s2)) - base)
    abl_df = pd.DataFrame([dict(criterion=c, mean_increase=np.mean(v), share_informative=np.mean(np.array(v) > 0), n=len(v))
                           for c, v in abl.items()]).sort_values("mean_increase", ascending=False)
    abl_df.to_csv(out / "ablation.csv", index=False)
    res["ablation"] = abl_df.to_dict("records")
    res["ablation_base_size_mean"] = float(np.mean(base_sizes))

    # 3. Error propagation
    err = []
    for e in [0.0, 0.05, 0.1, 0.2, 0.3]:
        for rep in range(a.reps):
            prow = perturb(rows, pool, e, rng)
            peng = ns.NaviDAMSuggestionEngine(prow)
            for r, o in pairs:
                for p in (0.25, 1.0):
                    s = make_study(r, o, rng, p)
                    cand = peng.suggest_methods(s)
                    err.append(dict(e=e, p_spec=p, k=n_specified(s), hit=r["Method"] in cand, size=len(cand)))
    err = pd.DataFrame(err)
    err.to_csv(out / "error_propagation_runs.csv", index=False)
    eg = err.groupby(["e", "p_spec"]).agg(recall=("hit", "mean"), k_mean=("k", "mean"),
                                           size_median=("size", "median")).reset_index()
    eg["expected_indep"] = [float(np.mean((1 - e) ** err[(err.e == e) & (err.p_spec == p)].k)) for e, p in zip(eg.e, eg.p_spec)]
    res["error_propagation"] = eg.to_dict("records")

    # 3b. Omission-error model
    om = []
    for e in [0.0, 0.05, 0.1, 0.2, 0.3]:
        for rep in range(a.reps):
            peng = ns.NaviDAMSuggestionEngine(omit(rows, e, rng))
            for r, o in pairs:
                for p in (0.25, 1.0):
                    s = make_study(r, o, rng, p)
                    om.append(dict(e=e, p_spec=p, hit=r["Method"] in peng.suggest_methods(s)))
    res["omission_errors"] = pd.DataFrame(om).groupby(["e", "p_spec"]).hit.mean().reset_index().rename(columns={"hit": "recall"}).to_dict("records")

    # 3c. Single-criterion filtering power
    sp = []
    for r, o in pairs:
        base = len(eng.suggest_methods({"Objective": o}))
        for c in applicable(o):
            vals = values(r, c)
            if vals:
                sp.append(dict(criterion=c, removed=1 - len(eng.suggest_methods({"Objective": o, c: rng.choice(vals)})) / base))
    res["single_criterion_power"] = pd.DataFrame(sp).groupby("criterion").removed.mean().sort_values(ascending=False).to_dict()

    # 4. LLM-initiated vs expert assessments: breadth of recorded options
    br = []
    for r in rows:
        ai = str(r.get("AI-assisted", "")).strip().lower() == "yes"
        for c in ns.FILTER_CRITERIA:
            if c in ns.MULTI_VALUE_CRITERIA:
                vals = values(r, c)
                if vals:
                    br.append(dict(ai=ai, criterion=c, n_opts=len(vals) / max(1, len(pool[c]))))
        dk = sum(1 for c in ns.FILTER_CRITERIA if any(v in ("Don't know", "Inapplicable") for v in ns._method_values(r, c)))
        br.append(dict(ai=ai, criterion="__fallback__", n_opts=dk))
    br = pd.DataFrame(br)
    from scipy.stats import mannwhitneyu
    m = br[br.criterion != "__fallback__"]
    f = br[br.criterion == "__fallback__"]
    res["breadth_ai_vs_expert"] = dict(
        share_options_ai=float(m[m.ai].n_opts.mean()), share_options_expert=float(m[~m.ai].n_opts.mean()),
        p_mw=float(mannwhitneyu(m[m.ai].n_opts, m[~m.ai].n_opts).pvalue),
        fallback_cells_ai=float(f[f.ai].n_opts.mean()), fallback_cells_expert=float(f[~f.ai].n_opts.mean()),
        n_ai=int(sum(str(r.get("AI-assisted", "")).lower() == "yes" for r in rows)))
    # retrieval frequency by AI status (are AI-drafted methods suggested more often?)
    ai_names = {r["Method"] for r in rows if str(r.get("AI-assisted", "")).lower() == "yes"}
    runs = bench[bench.p_spec == 0.5]
    # frequency at which each method appears in candidate sets of OTHER methods' studies
    freq = defaultdict(int); tot = 0
    for _ in range(3):
        for r, o in pairs:
            s = make_study(r, o, rng, 0.5)
            for mname in eng.suggest_methods(s):
                if mname != r["Method"]:
                    freq[mname] += 1
            tot += 1
    fr = pd.Series({r["Method"]: freq.get(r["Method"], 0) / tot for r in rows})
    res["false_positive_rate_ai"] = float(fr[fr.index.isin(ai_names)].mean())
    res["false_positive_rate_expert"] = float(fr[~fr.index.isin(ai_names)].mean())
    res["p_fp_mw"] = float(mannwhitneyu(fr[fr.index.isin(ai_names)], fr[~fr.index.isin(ai_names)]).pvalue)

    (out / "summary.json").write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res, indent=1, default=float)[:6000])


if __name__ == "__main__":
    main()
