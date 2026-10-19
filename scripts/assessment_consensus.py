"""Consensus / debated status of method assessments.

Every submitted assessment issue is stored as a *vote* in
``_data/assessment_votes/<method-slug>.json``. This module turns the votes of a
method into:

- a per-criterion agreement score,
- a method-level status (``single`` / ``consensus`` / ``debated``),
- a "published" value per criterion (confidence-weighted majority).

Running this file as a script rebuilds ``_data/assessment_status.json`` (a
generated, gitignored build artifact read by ``_layouts/method.html``).

Only the newest assessment from each named assessor contributes to consensus.
This also cleans up duplicate votes from older data; anonymous assessments
remain independent because their authors cannot be matched.

Agreement of one criterion
--------------------------
Each vote i has a softened weight w_i = sqrt(confidence / 5) (sqrt(3 / 5)
when no confidence is known, e.g. a baseline vote seeded from a pre-existing
assessment) and an answer. A similarity s(a, b) in [0, 1] compares two answers:

- ordinal criteria: the square of 1 - |level(a) - level(b)| / (n_levels - 1)
  (distance-based); non-level options such as "Inapplicable" only match
  themselves,
- multiple-choice criteria: the square of Jaccard similarity of selected
  options.

The agreement is the softened-confidence-weighted similarity share supported by the best-supported
answer: max_i  sum_j w_j * s(a_i, a_j) / sum_j w_j. With exact-match answers
it is the weighted share of assessors giving the modal answer, so ">= 80% of
the assessors agree" reads literally.

Method status
-------------
One vote: ``single`` (the confidence score is displayed). Two or more votes:
``consensus`` when at least 80% of the criteria answered by >= 2 assessors reach
an agreement of >= 80%; ``debated`` otherwise. There are 25 criteria, so when
all are compared, 20 agreed criteria meet the threshold.
"""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VOTES_DIR = PROJECT_ROOT / "_data/assessment_votes"
STATUS_FILE = PROJECT_ROOT / "_data/assessment_status.json"

# A criterion is agreed from this agreement; a method is Consensus from this
# share of agreed criteria.
CRITERION_THRESHOLD = 0.80
METHOD_THRESHOLD = 0.80
EPSILON = 1e-9
DEFAULT_CONFIDENCE = 3
MAX_CONFIDENCE = 5

REQUIRED_PERMISSIVE = ["Required", "Recommended", "Relaxes assumption"]

# TSV column -> (label shown on method pages, kind, ordered levels).
# Levels run in the order of the issue form options; "Inapplicable" and other
# non-level answers are handled as categorical values. Keep ordinal levels in
# sync with .github/ISSUE_TEMPLATE/method-assessment.yml (checked by a test).
CRITERIA = {
    "Objective": ("Objective", "multiple", None),
    "Estimand": ("Estimand", "multiple", None),
    "Type": ("Type", "multiple", None),
    "Minimal TS length": (
        "Minimal TS length", "ordinal", ["≥ 100", "≥ 10", "Handles ≤ 10"]),
    "Handles few samples": (
        "Handles few samples", "ordinal", ["No", "10 to 100", "Yes ≤ 10", "Yes CT design"]),
    "Handles huge datasets (n)": (
        "Handles huge datasets (n)", "ordinal", ["No", "Most dont", "Most do", "Yes"]),
    "Handles missing data": (
        "Handles missing data", "ordinal", ["No: requires prelim. correction", "Partially", "Yes"]),
    "RS-data proven": (
        "RS-data proven", "ordinal", ["No", "Few applications", "Yes"]),
    "Requires explicit processes": ("Requires explicit processes", "multiple", None),
    "Exposure type": ("Exposure type", "multiple", None),
    "Number of variables": ("Number of variables", "multiple", None),
    "Propaguates uncertainty": (
        "Propagates uncertainty", "ordinal",
        ["Needs model-agnostic propagation", "Model-specific tools", "Inherent capacity"]),
    "Handles lag effects": ("Handles lag effects", "ordinal", ["No", "Possible", "Yes"]),
    "Parametric nature": ("Parametric nature", "multiple", None),
    "Language": ("Language", "multiple", None),
    "Usage": ("Usage", "multiple", None),
    "Fonctional form": ("Functional form", "multiple", None),
    "No unobserved confounders": ("No unobserved confounders", "ordinal", REQUIRED_PERMISSIVE),
    "No interference": ("No interference", "ordinal", REQUIRED_PERMISSIVE),
    "Well-defined treatments": ("Well-defined treatments", "ordinal", REQUIRED_PERMISSIVE),
    "Common support (positivity)": ("Common support (positivity)", "ordinal", REQUIRED_PERMISSIVE),
    "Causal Markov Condition": ("Causal Markov Condition", "ordinal", REQUIRED_PERMISSIVE),
    "Faithfulness": ("Faithfulness", "ordinal", REQUIRED_PERMISSIVE),
    "IID": ("IID", "ordinal", REQUIRED_PERMISSIVE),
    "Model specific": ("Model specific assumption", "multiple", None),
}
CONFIDENCE_COLUMN = "Confidence in assessment"

CATEGORIES = {
    **dict.fromkeys(["Objective"], "Outcome"),
    **dict.fromkeys(["Estimand"], "Outcome"),
    **dict.fromkeys(["Type", "Minimal TS length", "Handles few samples",
                     "Handles huge datasets (n)", "Handles missing data", "RS-data proven"], "Data compatibility"),
    **dict.fromkeys(["Requires explicit processes", "Exposure type", "Number of variables",
                     "Propaguates uncertainty", "Handles lag effects", "Parametric nature"], "Model properties"),
    **dict.fromkeys(["Language", "Usage"], "Implementation"),
    **dict.fromkeys(["Fonctional form", "No unobserved confounders", "No interference",
                     "Well-defined treatments", "Common support (positivity)", "Causal Markov Condition",
                     "Faithfulness", "IID", "Model specific"], "Assumptions"),
}

# Criteria where ticking nothing is a valid answer ("no specific assumption").
# It is stored in votes as the explicit value NONE and published as an empty cell.
NONE_ALLOWED = {"Model specific"}
NONE = "None"



def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-") or "method"


def split_values(text):
    """Cell text ('a, b') -> list of stripped, non-empty values."""
    return [v.strip() for v in (text or "").split(",") if v.strip()]


def parse_confidence(value):
    try:
        confidence = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return confidence if 1 <= confidence <= MAX_CONFIDENCE else None


def author_key(name):
    """Stable key for a named assessor; anonymous votes cannot be matched."""
    normalized = " ".join((name or "").casefold().split())
    if normalized in {"", "anonymous", "unknown"}:
        return None
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def vote_author_key(vote):
    return vote.get("author_key") or author_key(vote.get("assessor"))


def deduplicate_votes(votes):
    """Keep only the newest named assessor vote, preserving anonymous votes."""
    newest = {}
    for index, vote in enumerate(votes):
        key = vote_author_key(vote)
        if key is None:
            continue
        date = str(vote.get("date") or "")
        try:
            issue = int(vote.get("issue") or 0)
        except (TypeError, ValueError):
            issue = 0
        # Dates/issues determine which historical assessment is newer; list
        # order breaks ties and keeps the most recently appended record.
        rank = (bool(date or issue or not vote.get("baseline")), date, issue, index)
        if key not in newest or rank > newest[key][0]:
            newest[key] = (rank, index)

    keep = {entry[1] for entry in newest.values()}
    return [
        vote for index, vote in enumerate(votes)
        if vote_author_key(vote) is None or index in keep
    ]


def weight(vote):
    confidence = (vote.get("confidence") or DEFAULT_CONFIDENCE) / MAX_CONFIDENCE
    return confidence ** 0.5


# "All" stands for the union of the listed options of that criterion.
ALL_EXPANSION = {
    "Exposure type": ["Binary", "Categorical", "Continuous / Time-varying",
                      "Compositional", "Multivariate"],
}


def expand_all(column, answer):
    if "All" in answer and column in ALL_EXPANSION:
        return list(dict.fromkeys([v for v in answer if v != "All"] + ALL_EXPANSION[column]))
    return answer


def similarity(column, a, b):
    """Similarity in [0, 1] between two answers (lists of strings)."""
    _label, kind, levels = CRITERIA[column]
    if kind == "multiple":
        a, b = expand_all(column, a), expand_all(column, b)
    if set(a) == set(b):
        return 1.0
    if kind == "ordinal":
        # Legacy multi-select answers: several levels count as the most
        # permissive one (the last level); non-level values (e.g.
        # "Inapplicable") next to a level are ignored.
        positions = []
        for answer in (a, b):
            idx = [levels.index(v) for v in dict.fromkeys(answer) if v in levels]
            if not idx:  # only "Inapplicable", "Don't know", ...
                return 0.0
            positions.append(max(idx))
        raw_similarity = max(0.0, 1 - abs(positions[0] - positions[1]) / (len(levels) - 1))
    else:
        union = set(a) | set(b)
        raw_similarity = len(set(a) & set(b)) / len(union)
    return raw_similarity ** 2


def vote_answer(vote, column):
    """Answer of a vote for a criterion. An unticked "none allowed" criterion
    counts as the explicit answer None, also in votes stored before that rule."""
    answer = vote.get("answers", {}).get(column)
    if not answer and column in NONE_ALLOWED:
        return [NONE]
    return answer or []


def criterion_answers(votes, column):
    return [(v, vote_answer(v, column)) for v in votes if vote_answer(v, column)]


def best_supported(column, answered, prefer=None):
    """Return (agreement, index of the best-supported answer).

    Ties are broken in favour of the answer equal to `prefer` (the currently
    published one), then the most confident vote, then the earliest vote."""
    total = sum(weight(v) for v, _ in answered)
    best = None
    for i, (vote_i, answer_i) in enumerate(answered):
        support = sum(weight(v) * similarity(column, answer_i, a) for v, a in answered) / total
        preferred = prefer is not None and set(answer_i) == set(prefer)
        key = (round(support, 9), preferred, weight(vote_i), -i)
        if best is None or key > best[0]:
            best = (key, support, i)
    return best[1], best[2]


def consensus_value(votes, column, prefer=None):
    answered = criterion_answers(votes, column)
    if not answered:
        return None
    _agreement, idx = best_supported(column, answered, prefer)
    return answered[idx][1]


def published_confidence(votes):
    scores = [v["confidence"] for v in votes if v.get("confidence")]
    return round(sum(scores) / len(scores)) if scores else None


def compute_published(votes, current_row=None):
    """Column -> published cell text (', '-joined) for every answered criterion,
    plus the confidence column."""
    published = {}
    for column in CRITERIA:
        prefer = split_values((current_row or {}).get(column))
        if not prefer and current_row is not None and column in NONE_ALLOWED:
            prefer = [NONE]
        value = consensus_value(votes, column, prefer or None)
        if value:
            published[column] = "" if value == [NONE] else ", ".join(value)
    confidence = published_confidence(votes)
    if confidence:
        published[CONFIDENCE_COLUMN] = str(confidence)
    return published


def method_status(votes):
    """Status dict for one method (see module docstring)."""
    n = len(votes)
    confidences = [v["confidence"] for v in votes if v.get("confidence")]
    result = {
        "status": "single",
        "assessors": n,
        "confidence": published_confidence(votes),
        "agreeing": 0,
        "evaluated": 0,
        "agreement_share": None,
        "assessor_names": list(dict.fromkeys(v.get("assessor") or "Anonymous" for v in votes)),
        "voters": [{"name": v.get("assessor") or "Anonymous", "confidence": v.get("confidence")} for v in votes],
        "required_criteria": 0,
        "method_threshold": round(METHOD_THRESHOLD * 100),
        "criterion_threshold": round(CRITERION_THRESHOLD * 100),
        "criteria": [],
    }
    if confidences:
        result["confidence_mean"] = round(sum(confidences) / len(confidences), 1)
    if n < 2:
        return result

    for column, (label, _kind, _levels) in CRITERIA.items():
        answered = criterion_answers(votes, column)
        if len(answered) < 2:
            continue
        agreement, _idx = best_supported(column, answered)
        agrees = agreement >= CRITERION_THRESHOLD - EPSILON
        result["evaluated"] += 1
        result["agreeing"] += int(agrees)
        result["criteria"].append({
            "column": column,
            "label": label,
            "agreement": round(agreement, 3),
            "debated": not agrees,
            "category": CATEGORIES.get(column, ""),
            "values": [", ".join(vote_answer(v, column)) for v in votes],
            "answers": [
                {"assessor": v.get("assessor") or "Anonymous",
                 "confidence": v.get("confidence"),
                 "value": ", ".join(answer)}
                for v, answer in answered
            ],
        })

    if result["evaluated"]:
        result["required_criteria"] = math.ceil(METHOD_THRESHOLD * result["evaluated"] - EPSILON)
        share = result["agreeing"] / result["evaluated"]
        result["agreement_share"] = round(share, 3)
        result["status"] = "consensus" if share >= METHOD_THRESHOLD - EPSILON else "debated"
    return result


def votes_path(method_name):
    return VOTES_DIR / f"{slugify(method_name)}.json"


def load_votes(method_name):
    path = votes_path(method_name)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return deduplicate_votes(json.load(f).get("votes", []))


def votes_text(method_name, votes):
    return json.dumps({"method": method_name, "votes": votes}, ensure_ascii=False, indent=2) + "\n"


def save_votes(method_name, votes):
    VOTES_DIR.mkdir(parents=True, exist_ok=True)
    votes_path(method_name).write_text(
        votes_text(method_name, deduplicate_votes(votes)), encoding="utf-8"
    )


def build_status_file(votes_dir=VOTES_DIR, output=STATUS_FILE):
    """Recompute the status of every method that has votes. Issue numbers and
    assessor identities of anonymous votes never reach the output."""
    statuses = {}
    for path in sorted(Path(votes_dir).glob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        method = data.get("method")
        if method and data.get("votes"):
            statuses[method] = method_status(deduplicate_votes(data["votes"]))
    with open(output, "w", encoding="utf-8") as f:
        json.dump(statuses, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return statuses


if __name__ == "__main__":
    result = build_status_file()
    print(f"Assessment status written to {STATUS_FILE} ({len(result)} method(s) with votes)")
    sys.exit(0)
