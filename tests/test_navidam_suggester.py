import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
METHOD_ASSESSMENTS_PATH = ROOT_DIR / "_data" / "method_assessments_clean.tsv"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validation.navidam_suggester import NaviDAMSuggestionEngine, methods_match


EXPECTED_METHOD_SETS = {
    "PC": {
        "PC",
        "PCMCI",
        "Bayesian network learning",
        "Invariant causal prediction",
        "Dynamical footprint analysis (Cano et al. 2025)",
    },
    "DiD & BACI": {"DiD & BACI"},
    "Structural equation modelling (SEM)": {"Structural equation modelling (SEM)"},
    "Synthetic controls": {"Synthetic controls"},
    "CCM": {"CCM"},
    "RCTs": {"RCTs", "Randomised saturation designs"},
}


def load_method_rows():
    with METHOD_ASSESSMENTS_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def method_row(method_rows, method_name):
    return next(row for row in method_rows if row["Method"] == method_name)


def test_exact_method_row_includes_own_method():
    method_rows = load_method_rows()
    engine = NaviDAMSuggestionEngine(method_rows)

    for method_name in EXPECTED_METHOD_SETS:
        suggestions = set(engine.suggest_methods(method_row(method_rows, method_name)))
        assert method_name in suggestions


def test_ui_verified_method_sets_match_python_engine():
    method_rows = load_method_rows()
    engine = NaviDAMSuggestionEngine(method_rows)

    for method_name, expected_set in EXPECTED_METHOD_SETS.items():
        suggestions = set(engine.suggest_methods(method_row(method_rows, method_name)))
        assert suggestions == expected_set


def test_method_concept_alignment_examples():
    positive_pairs = [
        ("two-way fixed effects estimator", "Panel designs, TWFE"),
        ("fixed-effects panel regression", "Panel designs, TWFE"),
        ("PC algorithm", "PC"),
        ("Convergent Cross Mapping", "CCM"),
        ("Directed acyclic graph (DAG) scheme", "Bayesian network learning"),
        ("Causal diagram", "Bayesian network learning"),
        ("Experimental manipulation", "RCTs"),
        ("Experimen[tally manipulating forest stands", "RCTs"),
        ("Structural Causal Modelling", "Bayesian network learning"),
    ]

    negative_pairs = [
        ("Process tracing", "Synthetic controls"),
        ("Multiple-case study", "PC"),
    ]

    for reported, suggested in positive_pairs:
        assert methods_match(reported, suggested)

    for reported, suggested in negative_pairs:
        assert not methods_match(reported, suggested)

def test_exposure_all_is_union_of_types():
    from scripts.validation import navidam_suggester as ns
    row_all = {"Method": "A", "Exposure type": "All"}
    assert "Binary" in ns._method_values(row_all, "Exposure type")
    assert "Multivariate" in ns._method_values(row_all, "Exposure type")
