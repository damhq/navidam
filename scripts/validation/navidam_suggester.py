from __future__ import annotations

import csv
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
METHOD_ASSESSMENTS_PATH = ROOT_DIR / "_data" / "method_assessments_clean.tsv"
OBJECTIVE_CRITERIA_MAP_PATH = ROOT_DIR / "_data" / "objective_criteria_map.json"

FILTER_CRITERIA = [
    "Objective",
    "Estimand",
    "Type",
    "Minimal TS length",
    "Handles few samples",
    "Handles huge datasets (n)",
    "Handles missing data",
    "RS-data proven",
    "Fonctional form",
    "No unobserved confounders",
    "No interference",
    "Well-defined treatments",
    "Common support (positivity)",
    "Causal Markov Condition",
    "Faithfulness",
    "IID",
    "Model specific",
    "Requires explicit processes",
    "Exposure type",
    "Number of variables",
    "Propaguates uncertainty",
    "Handles lag effects",
    "Parametric nature",
    "Language",
    "Usage",
]

MULTI_VALUE_CRITERIA = {
    "Estimand",
    "Type",
    "Fonctional form",
    "Model specific",
    "Requires explicit processes",
    "Exposure type",
    "Number of variables",
    "Parametric nature",
    "Language",
    "Usage",
}

OPTION_ALIASES = {
    "Minimal TS length": {
        "Handles <= 10": "Handles ≤ 10",
        "<= 10": "Handles ≤ 10",
        ">= 10": "≥ 10",
        ">= 100": "≥ 100",
        "Handles ≥ 10": "≥ 10",
    },
    "Exposure type": {
        "Continuous or Time-varying": "Continuous / Time-varying",
        "Continuous or Time varying": "Continuous / Time-varying",
        "Time-varying": "Continuous / Time-varying",
    },
    "No unobserved confounders": {
        "Assumption-free": "Relaxes assumption",
    },
    "No interference": {
        "Assumption-free": "Relaxes assumption",
    },
    "Well-defined treatments": {
        "Assumption-free": "Relaxes assumption",
    },
    "Common support (positivity)": {
        "Assumption-free": "Relaxes assumption",
    },
    "Causal Markov Condition": {
        "Assumption-free": "Relaxes assumption",
    },
    "Faithfulness": {
        "Assumption-free": "Relaxes assumption",
    },
    "IID": {
        "Assumption-free": "Relaxes assumption",
    },
}

ORDINAL_CRITERIA_ORDER = {
    "Minimal TS length": ["≥ 100", "≥ 10", "Handles ≤ 10"],
    "Handles few samples": ["No", "10 to 100", "Yes ≤ 10", "Yes CT design"],
    "Handles huge datasets (n)": ["No", "Most dont", "Most do", "Yes", "Necessary"],
    "Handles missing data": ["No: requires prelim. correction", "Partially", "Yes"],
    "RS-data proven": ["No", "Few applications", "Yes"],
    "Propaguates uncertainty": ["Needs model-agnostic propagation", "Model-specific tools", "Inherent capacity"],
    "Handles lag effects": ["No", "Possible", "Yes"],
    "No unobserved confounders": ["Required", "Recommended", "Relaxes assumption"],
    "No interference": ["Required", "Recommended", "Relaxes assumption"],
    "Well-defined treatments": ["Required", "Recommended", "Relaxes assumption"],
    "Common support (positivity)": ["Required", "Recommended", "Relaxes assumption"],
    "Causal Markov Condition": ["Required", "Recommended", "Relaxes assumption"],
    "Faithfulness": ["Required", "Recommended", "Relaxes assumption"],
    "IID": ["Required", "Recommended", "Relaxes assumption"],
}

COMPOSITE_OPTIONS = {
    "Estimand": {
        "Any treatment effect": ["ATE", "ATT", "LATE", "CATE"],
    },
    "Handles huge datasets (n)": {
        "Necessary": ["Yes", "Most do"],
    },
}

# Method values standing for the union of other options (mirrors impliedOptions in criteria.js).
IMPLIED_OPTIONS = {
    "Exposure type": {
        "All": ["Binary", "Categorical", "Continuous / Time-varying", "Compositional", "Multivariate"],
    },
}

SKIP_SELECTED_VALUES = {"", "Don't know", "Inapplicable", "__unsure__"}
NO_SPECIFIC_CRITERION = "Model specific"
NO_SPECIFIC_VALUE = "No specific assumption"
METHOD_FALLBACK_VALUES = {"Don't know", "Inapplicable"}

METHOD_CONCEPT_PATTERNS = [
    ("Instrumental variables", [r"\binstrumental variables?\b", r"\biv\b"]),
    ("Gradient / Stratified analyses", [r"\bgradient\b", r"\bstratified analys(?:is|es)\b"]),
    ("SEMs", [r"\bstructural equation models?\b", r"\bsems?\b"]),
    ("GLMs, GEEs", [r"\bglms?\b", r"\bgees?\b", r"\bgeneralized linear models?\b", r"\bgeneralized estimating equations?\b"]),
    ("GAMs", [r"\bgams?\b", r"\bgeneralized additive models?\b"]),
    ("GLMMs, GAMMs", [r"\bglmms?\b", r"\bgamms?\b", r"\bgeneralized linear mixed models?\b", r"\bgeneralized additive mixed models?\b"]),
    ("Tree-based ML algorithms", [r"\btree[- ]based\b", r"\brandom forest\b", r"\bboost(?:ed|ing)?\b"]),
    ("SHAP", [r"\bshap\b", r"\bshapley\b"]),
    ("Mediation analysis", [r"\bmediation analys(?:is|es)\b"]),
    ("Linear path method", [r"\blinear path method\b"]),
    ("Frontdoor criterion", [r"\bfrontdoor\b", r"\bfront-door\b"]),
    ("Doubly robust estimation", [r"\bdoubly robust\b"]),
    ("RDD (LATE)", [r"\brdd\b", r"\bregression discontinuity\b"]),
    ("DiD & BACI", [r"\bdid\b", r"\bbaci\b", r"\bdiff(?:erence)?[- ]in[- ]diff(?:erence)?s?\b", r"\bdifference[- ]in[- ]differences\b", r"\bbefore[- ]after control[- ]impact\b"]),
    ("Panel designs, TWFE", [r"\btwfe\b", r"\btwo[- ]way fixed effects?\b", r"\bfixed[- ]effects panel regression\b", r"\bfixed effects estimator\b"]),
    ("Matching methods", [r"\bmatching\b"]),
    ("Weighting & Propensity scores", [r"\bpropensity scores?\b", r"\bipw\b", r"\bweighting\b"]),
    ("Synthetic controls", [r"\bsynthetic controls?\b"]),
    ("Interrupted time series", [r"\binterrupted time series\b", r"\bitsa?\b"]),
    ("Matrix completion", [r"\bmatrix completion\b", r"\binteractive fixed effects\b"]),
    ("Target transformation (F-learner)", [r"\bf[- ]learner\b", r"\btarget transformation\b"]),
    ("S,T, X learners", [r"\bs[-/, ]*t[-/, ]*x learners?\b", r"\bx[- ]learner\b", r"\bt[- ]learner\b", r"\bs[- ]learner\b"]),
    ("NNs", [r"\bneural networks?\b", r"\bnns?\b", r"\bdragonnet\b"]),
    ("BART", [r"\bbart\b", r"\bbayesian additive regression trees?\b"]),
    ("Causal forests", [r"\bcausal forests?\b"]),
    ("Double Machine learning", [r"\bdouble machine learning\b", r"\bdml\b"]),
    ("R-learner", [r"\br[- ]learner\b"]),
    ("Targeted Maximum Likelihood Estimation (TMLE)", [r"\btmle\b", r"\btargeted maximum likelihood estimation\b"]),
    ("Modified Treatment Policies", [r"\bmodified treatment policies\b", r"\bmtp\b"]),
    ("Reinforcement learning", [r"\breinforcement learning\b", r"\bq-learning\b", r"\bdynamic treatment regime\b"]),
    ("PC", [r"\bpc algorithm\b", r"\bpcalg\b", r"\bpc\b"]),
    ("PCMCI", [r"\bpcmci\b"]),
    ("FCI, TsFCI", [r"\bfci\b", r"\btsfci\b"]),
    ("GES, TsGFCI", [r"\bges\b", r"\bgfci\b", r"\btsgfci\b"]),
    ("DYNOTEARS", [r"\bdynotears\b"]),
    ("LiNGAM", [r"\blingam\b"]),
    ("Kernel methods", [r"\bkernel methods?\b"]),
    ("Additive noise models", [r"\badditive noise models?\b", r"\banm\b"]),
    ("Granger causality", [r"\bgranger causality\b"]),
    ("RCTs", [r"\bexperimental manipulation\b", r"\bexperimentally manipulating\b", r"\bmanipulating forest stands\b", r"\bcanopy cover treatments?\b"]),
    ("RCTs", [r"\brcts\b", r"\brandomi[sz]ed controlled trials?\b", r"\bcontrolled experiment\b"]),
    ("Randomised saturation designs", [r"\brandomi[sz]ed saturation designs?\b"]),
    ("dc-CA", [r"\bdc[- ]ca\b"]),
    ("CCM", [r"\bconvergent cross mapping\b", r"\bccm\b"]),
    ("Bayesian network learning", [r"\bbayesian network learning\b", r"\bbayesian networks?\b", r"\bdirected acyclic graph\b", r"\bdag\b", r"\bcausal diagram\b", r"\bstructural causal modelling\b"]),
]

GENERIC_METHOD_WORDS = {
    "a",
    "an",
    "and",
    "analysis",
    "analyses",
    "approach",
    "approaches",
    "based",
    "design",
    "designs",
    "estimation",
    "estimator",
    "estimators",
    "framework",
    "general",
    "implementation",
    "method",
    "methods",
    "model",
    "models",
    "reported",
    "scheme",
    "the",
    "using",
}


def split_criterion_values(raw_value):
    if raw_value is None:
        return []
    if isinstance(raw_value, float) and raw_value != raw_value:
        return []
    if isinstance(raw_value, list):
        parts = raw_value
    else:
        parts = [raw_value]

    values = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, float) and part != part:
            continue
        text = str(part).strip()
        if not text or text.casefold() in {"nan", "none", "null"}:
            continue
        values.extend(piece.strip() for piece in re.split(r"\s*[;,]\s*", text) if piece.strip())
    return values


def normalize_option_value(criterion, option):
    normalized = str(option).strip()
    normalized = normalized.replace(">=", "≥").replace("<=", "≤")
    return OPTION_ALIASES.get(criterion, {}).get(normalized, normalized)


@lru_cache(maxsize=1)
def load_objective_criteria_map():
    with OBJECTIVE_CRITERIA_MAP_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def load_method_rows():
    with METHOD_ASSESSMENTS_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def get_used_criteria_keys(objective):
    objective_map = load_objective_criteria_map()
    if objective and objective in objective_map:
        return set(objective_map[objective] + ["Objective"])
    return set(FILTER_CRITERIA)


def _normalize_selected_values(criterion, raw_value):
    seen = set()
    normalized_values = []
    for value in split_criterion_values(raw_value):
        normalized = normalize_option_value(criterion, value)
        if normalized in SKIP_SELECTED_VALUES or normalized in seen:
            continue
        seen.add(normalized)
        normalized_values.append(normalized)
    return normalized_values


def _method_values(row, criterion):
    values = [normalize_option_value(criterion, value) for value in split_criterion_values(row.get(criterion, ""))]
    implied = IMPLIED_OPTIONS.get(criterion, {})
    expanded = list(values)
    for value in values:
        expanded.extend(c for c in implied.get(value, []) if c not in expanded)
    return expanded


class NaviDAMSuggestionEngine:
    def __init__(self, method_rows=None):
        self.method_rows = method_rows if method_rows is not None else load_method_rows()

    def suggest_methods(self, criteria_row):
        objective = normalize_option_value("Objective", criteria_row.get("Objective", ""))
        used_criteria_keys = get_used_criteria_keys(objective)
        filtered = self.method_rows

        for criterion in FILTER_CRITERIA:
            if criterion not in used_criteria_keys:
                continue

            selected_values = _normalize_selected_values(criterion, criteria_row.get(criterion, ""))
            if not selected_values:
                continue
            # No restriction requested: keep all methods, including empty cells
            if criterion == NO_SPECIFIC_CRITERION and NO_SPECIFIC_VALUE in selected_values:
                continue

            composite_for_criterion = COMPOSITE_OPTIONS.get(criterion, {})
            if any(selected in composite_for_criterion for selected in selected_values):
                included = set()
                for selected in selected_values:
                    if selected in composite_for_criterion:
                        included.update(composite_for_criterion[selected])
                    else:
                        included.add(selected)
                filtered = [
                    row
                    for row in filtered
                    if any(
                        method_value in included or method_value in METHOD_FALLBACK_VALUES
                        for method_value in _method_values(row, criterion)
                    )
                ]
                continue

            if criterion in ORDINAL_CRITERIA_ORDER:
                order = ORDINAL_CRITERIA_ORDER[criterion]
                selected_positions = [order.index(value) for value in selected_values if value in order]
                if not selected_positions:
                    continue
                filtered = [
                    row
                    for row in filtered
                    if any(
                        method_value in METHOD_FALLBACK_VALUES
                        or (
                            method_value in order
                            and any(order.index(method_value) >= selected_position for selected_position in selected_positions)
                        )
                        for method_value in _method_values(row, criterion)
                    )
                ]
                continue

            implied = IMPLIED_OPTIONS.get(criterion, {})

            def matches(method_values):
                if any(value in METHOD_FALLBACK_VALUES for value in method_values):
                    return True
                return any(
                    all(c in method_values for c in implied[sel]) if sel in implied else sel in method_values
                    for sel in selected_values
                )

            filtered = [row for row in filtered if matches(_method_values(row, criterion))]

        suggestions = []
        seen_methods = set()
        for row in filtered:
            method_name = str(row.get("Method", "")).strip()
            if not method_name or method_name in seen_methods:
                continue
            seen_methods.add(method_name)
            suggestions.append(method_name)
        return suggestions


def _basic_method_string(text):
    if text is None:
        return ""
    if isinstance(text, float) and text != text:
        return ""
    ascii_text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower().replace("&", " and ")
    ascii_text = re.sub(r"[^a-z0-9]+", " ", ascii_text)
    normalized = re.sub(r"\s+", " ", ascii_text).strip()
    if normalized in {"nan", "none", "null"}:
        return ""
    return normalized


def canonicalize_method_name(method_name):
    normalized = _basic_method_string(method_name)
    if not normalized:
        return ""

    for canonical, patterns in METHOD_CONCEPT_PATTERNS:
        if any(re.search(pattern, normalized) for pattern in patterns):
            return canonical

    tokens = [token for token in normalized.split() if token not in GENERIC_METHOD_WORDS]
    return " ".join(tokens) if tokens else normalized


@lru_cache(maxsize=1)
def method_concept_index():
    concept_map = {}
    for row in load_method_rows():
        method_name = str(row.get("Method", "") or "").strip()
        if not method_name:
            continue
        concept_map[method_name] = canonicalize_method_name(method_name)
    return concept_map


def method_name_variants(method_name):
    variants = set()
    if not str(method_name or "").strip():
        return variants

    candidates = {str(method_name).strip()}
    candidates.update(part.strip() for part in re.split(r"\s*(?:/|&| and )\s*", str(method_name)) if part.strip())
    candidates.update(part.strip() for part in re.split(r"\s*,\s*", str(method_name)) if part.strip())
    candidates.update(match.strip() for match in re.findall(r"\(([^)]+)\)", str(method_name)) if match.strip())

    for candidate in candidates:
        canonical = canonicalize_method_name(candidate)
        if canonical:
            variants.add(canonical)

    for known_method, concept in method_concept_index().items():
        normalized_known = _basic_method_string(known_method)
        normalized_input = _basic_method_string(method_name)
        if not normalized_input or not normalized_known:
            continue
        if normalized_input in normalized_known or normalized_known in normalized_input:
            variants.add(concept)
    return variants


def method_concept_label(method_name):
    return canonicalize_method_name(method_name)


def methods_match(reported_method, suggested_method):
    reported_variants = method_name_variants(reported_method)
    suggested_variants = method_name_variants(suggested_method)
    if not reported_variants or not suggested_variants:
        return False

    if reported_variants & suggested_variants:
        return True

    for reported_variant in reported_variants:
        for suggested_variant in suggested_variants:
            if len(reported_variant) >= 5 and (reported_variant in suggested_variant or suggested_variant in reported_variant):
                return True

            reported_tokens = set(reported_variant.split())
            suggested_tokens = set(suggested_variant.split())
            if not reported_tokens or not suggested_tokens:
                continue

            common_tokens = reported_tokens & suggested_tokens
            if len(common_tokens) >= 2 and len(common_tokens) / min(len(reported_tokens), len(suggested_tokens)) >= 0.75:
                return True

    return False
