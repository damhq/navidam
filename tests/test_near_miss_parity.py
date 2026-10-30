import csv
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validation.navidam_suggester import (
    FILTER_CRITERIA,
    NaviDAMSuggestionEngine,
    get_used_criteria_keys,
    load_method_rows,
    split_criterion_values,
)

FIXED_STUDIES = [
    {"Objective": "Effect estimation", "Estimand": ["Any treatment effect"], "Handles lag effects": ["Yes"]},
    {"Objective": "Effect estimation", "Type": ["Panel data (many samples)"], "Handles few samples": ["Yes ≤ 10"],
     "Exposure type": ["Binary"], "Model specific": ["No specific assumption"]},
    {"Objective": "Detection", "Minimal TS length": ["≥ 100"], "Handles missing data": ["Yes"], "Language": ["Python"]},
    {"Objective": "Causal relationship(s)", "Exposure type": ["All"], "Handles huge datasets (n)": ["Necessary"]},
    {"Objective": "Effect estimation", "No unobserved confounders": ["Relaxes assumption"], "Estimand": ["ATE", "CATE"],
     "Parametric nature": ["Non-parametric"]},
    # Contradictory criteria: strict result is empty, near misses are the fallback
    {"Objective": "Effect estimation", "Estimand": ["Mediation effects"], "Type": ["Spatial only (cross-sectional)"],
     "Handles lag effects": ["Yes"], "Language": ["GIS"]},
]


def seeded_studies(rows, count=40, seed=7):
    rng = random.Random(seed)
    studies = []
    for _ in range(count):
        row = rng.choice(rows)
        objective = rng.choice(split_criterion_values(row["Objective"]))
        usable = [c for c in get_used_criteria_keys(objective) if c != "Objective" and c in FILTER_CRITERIA]
        study = {"Objective": objective}
        for criterion in rng.sample(sorted(usable), 5):
            options = sorted({v for r in rows for v in split_criterion_values(r.get(criterion, ""))
                              if v not in {"Don't know", "Inapplicable"}})
            if options:
                study[criterion] = [rng.choice(options)]
        studies.append(study)
    return studies


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_js_and_python_near_misses_agree():
    rows = load_method_rows()
    studies = FIXED_STUDIES + seeded_studies(rows)
    objective_map = json.loads((ROOT_DIR / "_data" / "objective_criteria_map.json").read_text(encoding="utf-8"))
    payload = json.dumps({"rows": rows, "objectiveMap": objective_map, "studies": studies})
    result = subprocess.run(
        ["node", str(ROOT_DIR / "tests" / "near_miss_parity.mjs")],
        input=payload, capture_output=True, text=True, check=True,
    )
    js_results = json.loads(result.stdout)

    engine = NaviDAMSuggestionEngine(rows)
    with_near_misses = 0
    for study, js in zip(studies, js_results):
        strict = engine.suggest_methods(study)
        near = engine.suggest_near_misses(study)
        assert sorted(js["strict"]) == sorted(strict), study
        assert sorted(map(tuple, js["near"])) == sorted((n["Method"], n["failed_criterion"]) for n in near), study
        assert not {n["Method"] for n in near} & set(strict)
        with_near_misses += bool(near)
    assert with_near_misses >= 5
