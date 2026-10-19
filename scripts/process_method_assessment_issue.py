"""Create or fill a row in the raw method-assessment TSV from a 'Method
assessment' GitHub issue (.github/ISSUE_TEMPLATE/method-assessment.yml), then
call generate_method_pages.py to (re)build the cleaned data file and any
missing method documentation pages.

Input: the parsed issue form answers as JSON (field id -> string, or list of
strings for checkboxes/multi-selects), provided via the ISSUE_JSON env var
(see .github/workflows/method-assessment.yml). Can also be supplied by hand
for local testing, same convention as process_method_issue.py.

Behavior:
- If no row in the raw TSV has a matching "Method" name, a new row is
  appended with Category/Sub-category/Assessor and all assessment columns
  filled from the issue.
- If a matching row exists but every column after "Sub-category" is empty
  (i.e. it's just a placeholder entry), the empty cells are filled in from
  the issue. Any already non-empty cell (e.g. an existing Category) is left
  untouched rather than overwritten.
- If a matching row exists and already has assessment content, the issue is
  treated as a *review* of that existing assessment: the criteria of the row
  become the confidence-weighted majority over all recorded votes
  (Category/Sub-category are never touched), and the PR body lists each
  suggested change (old -> new) for a maintainer to accept or reject via
  normal review. If neither the row nor the votes change, no PR is opened.
- The Assessor cell of the row is never replaced: the method page lists every
  assessor found in the votes.
- Every issue is also stored as a vote in _data/assessment_votes/ (see
  assessment_consensus.py), from which the Consensus / Debated / confidence
  status badge of the method page is computed. A named assessor has one vote
  per method: a later assessment replaces their earlier vote, including a
  baseline vote seeded from a pre-existing assessment.
- generate_method_pages.py is only ever called to fill in *missing* pages
  (it already skips a method's file if it exists), so an existing
  documentation page is never overwritten by this script.
"""
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_method_issue import contributor_name, find_existing_file  # noqa: E402
import assessment_consensus as consensus  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_TSV = PROJECT_ROOT / "_data/DetectionAttribution methods - Method Assessment.tsv"
HEADER_SKIP_LINES = 3

COLUMNS = [
    "Author", "Doc status", "Reviewer", "Assessor", "Method", "Assessment status",
    "AI-assisted", "AI flag", "Category", "Sub-category",
    "Objective", "Estimand", "Type", "Minimal TS length", "Handles few samples",
    "Handles huge datasets (n)", "Handles missing data", "RS-data proven",
    "Fonctional form", "No unobserved confounders", "No interference",
    "Well-defined treatments", "Common support (positivity)", "Causal Markov Condition",
    "Faithfulness", "IID", "Model specific", "Requires explicit processes",
    "Exposure type", "Number of variables", "Propaguates uncertainty",
    "Handles lag effects", "Parametric nature", "Language", "Usage",
    "Confidence in assessment",
]
# Columns an issue can never overwrite; only "Assessor" may be filled if empty.
# ("Assessment status", "AI-assisted" and "AI flag" are managed by maintainers /
# bulk scripts, never by an issue.)
IDENTITY_COLUMNS = ["Author", "Doc status", "Reviewer", "Assessor", "Method", "Category", "Sub-category",
                    "Assessment status", "AI-assisted", "AI flag"]
ASSESSMENT_COLUMNS = [c for c in COLUMNS if c not in IDENTITY_COLUMNS]

# Maps TSV column -> issue field id. List-valued fields are joined with ", ".
FIELD_MAP = {
    "Objective": "objective",
    "Estimand": "estimand",
    "Type": "data_type",
    "Minimal TS length": "minimal_ts_length",
    "Handles few samples": "handles_few_samples",
    "Handles huge datasets (n)": "handles_huge_datasets",
    "Handles missing data": "handles_missing_data",
    "RS-data proven": "rs_data_proven",
    "Fonctional form": "functional_form",
    "No unobserved confounders": "no_unobserved_confounders",
    "No interference": "no_interference",
    "Well-defined treatments": "well_defined_treatments",
    "Common support (positivity)": "common_support_positivity",
    "Causal Markov Condition": "causal_markov_condition",
    "Faithfulness": "faithfulness",
    "IID": "iid",
    "Model specific": "model_specific_assumptions",
    "Requires explicit processes": "requires_explicit_processes",
    "Exposure type": "exposure_type",
    "Number of variables": "number_of_variables",
    "Propaguates uncertainty": "propagates_uncertainty",
    "Handles lag effects": "handles_lag_effects",
    "Parametric nature": "parametric_nature",
    "Language": "language",
    "Usage": "usage",
    "Confidence in assessment": "confidence",
}
LIST_FIELDS = {
    "category", "sub_category", "objective", "estimand", "data_type",
    "requires_explicit_processes", "exposure_type", "number_of_variables",
    "parametric_nature", "language", "usage", "functional_form",
    "model_specific_assumptions",
}


def load_issue_fields():
    raw = os.environ.get("ISSUE_JSON")
    if not raw:
        print("ISSUE_JSON env var is empty or missing", file=sys.stderr)
        sys.exit(1)
    data = json.loads(raw)
    fields = {}
    for key, value in data.items():
        if key in LIST_FIELDS:
            if isinstance(value, str):
                value = [v.strip() for v in value.split("\n") if v.strip()]
            fields[key] = [str(v).strip() for v in value or []]
        else:
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            fields[key] = (value or "").strip()
    return fields


def field_value_for_column(column, fields):
    field_id = FIELD_MAP[column]
    value = fields.get(field_id)
    if isinstance(value, list):
        return ", ".join(value)
    return value or ""


def read_raw_tsv():
    with open(RAW_TSV, newline="", encoding="utf-8") as f:
        lines = f.readlines()
    header_lines = lines[:HEADER_SKIP_LINES]
    reader = csv.DictReader(lines[HEADER_SKIP_LINES:], delimiter="\t")
    rows = [dict(row) for row in reader]
    return header_lines, rows


def write_raw_tsv(header_lines, rows):
    with open(RAW_TSV, "w", newline="", encoding="utf-8") as f:
        f.writelines(header_lines)
        writer = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t", restval="", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def find_row(rows, method_name):
    target = method_name.strip().casefold()
    for row in rows:
        if (row.get("Method") or "").strip().casefold() == target:
            return row
    return None


def is_assessment_empty(row):
    return all(not (row.get(col) or "").strip() for col in ASSESSMENT_COLUMNS)


def build_new_row(method_name, fields):
    row = {col: "" for col in COLUMNS}
    row["Method"] = method_name
    row["Assessor"] = fields.get("author", "")
    row["Category"] = ", ".join(fields.get("category") or [])
    row["Sub-category"] = ", ".join(fields.get("sub_category") or [])
    for column in ASSESSMENT_COLUMNS:
        row[column] = field_value_for_column(column, fields)
    return row


def fill_empty_row(row, fields):
    if not (row.get("Category") or "").strip():
        row["Category"] = ", ".join(fields.get("category") or [])
    if not (row.get("Sub-category") or "").strip():
        row["Sub-category"] = ", ".join(fields.get("sub_category") or [])
    if not (row.get("Assessor") or "").strip():
        row["Assessor"] = contributor_name(fields)
    for column in ASSESSMENT_COLUMNS:
        if not (row.get(column) or "").strip():
            row[column] = field_value_for_column(column, fields)


def issue_answers(fields):
    """Criterion column -> list of selected values, as submitted in the issue."""
    answers = {}
    for column in consensus.CRITERIA:
        value = fields.get(FIELD_MAP[column])
        values = value if isinstance(value, list) else ([value] if value else [])
        values = [v for v in values if v]
        if values:
            answers[column] = values
        elif column in consensus.NONE_ALLOWED:
            answers[column] = [consensus.NONE]
    return answers


def author_key(name):
    return consensus.author_key(name)


def build_vote(fields):
    return {
        "author_key": author_key(fields.get("author")),
        "issue": int(os.environ.get("ISSUE_NUMBER") or 0) or None,
        "assessor": contributor_name(fields),
        "date": (os.environ.get("ISSUE_DATE") or "")[:10],
        "confidence": consensus.parse_confidence(fields.get("confidence")),
        "answers": issue_answers(fields),
    }


def baseline_vote(row):
    """Vote standing for an assessment that predates the vote store."""
    answers = {c: consensus.split_values(row.get(c)) for c in consensus.CRITERIA}
    for column in consensus.NONE_ALLOWED:
        answers[column] = answers[column] or [consensus.NONE]
    return {
        "issue": None,
        "baseline": True,
        "assessor": (row.get("Assessor") or "").strip() or "Unknown",
        "date": "",
        "confidence": consensus.parse_confidence(row.get(consensus.CONFIDENCE_COLUMN)),
        "answers": {c: v for c, v in answers.items() if v},
    }


ANONYMOUS_NAMES = {"", "anonymous", "unknown"}


def vote_key(vote):
    return consensus.vote_author_key(vote)


def upsert_vote(votes, vote):
    """One vote per assessor and method: a new submission replaces the vote from
    the same issue (issue edits) or from the same author (matched on the author
    key, which also works for named legacy votes). Older duplicate votes are
    reduced to the newest assessment before applying the submission."""
    votes = consensus.deduplicate_votes(votes)
    key = vote_key(vote)
    for i, existing in enumerate(votes):
        same_issue = vote["issue"] is not None and existing.get("issue") == vote["issue"]
        if same_issue or (key is not None and vote_key(existing) == key):
            votes[i] = vote
            return votes
    votes.append(vote)
    return consensus.deduplicate_votes(votes)


def compute_changes(row, published):
    """List of (column, old_value, new_value) for criteria whose published
    (confidence-weighted majority) value differs from the existing row.
    Category/Sub-category are excluded: they're never revised by an assessment
    issue. Same options in another order are not a change."""
    changes = []
    for column in ASSESSMENT_COLUMNS:
        if column not in published:
            continue
        new_value = published[column].strip()
        old_value = (row.get(column) or "").strip()
        if (not new_value and column not in consensus.NONE_ALLOWED) or new_value == old_value:
            continue
        if column != consensus.CONFIDENCE_COLUMN and set(consensus.split_values(old_value)) == set(consensus.split_values(new_value)):
            continue
        changes.append((column, old_value, new_value))
    return changes


def apply_changes(row, changes):
    for column, _old_value, new_value in changes:
        row[column] = new_value


def write_github_output(status, page_status, method_name, changes=None):
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"status={status}\n")
        f.write(f"page_status={page_status}\n")
        f.write(f"method_name={method_name}\n")
        changes_md = "\n".join(
            f"- **{column}**: `{old or '(empty)'}` \u2192 `{new}`"
            for column, old, new in (changes or [])
        )
        f.write(f"changes<<GH_OUTPUT_EOF\n{changes_md}\nGH_OUTPUT_EOF\n")


def run_generate_method_pages():
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/generate_method_pages.py")],
        cwd=PROJECT_ROOT, check=True,
    )


def main():
    fields = load_issue_fields()
    method_name = fields.get("method_name", "").strip()
    if not method_name:
        print("No method_name field found in issue, aborting", file=sys.stderr)
        sys.exit(1)

    header_lines, rows = read_raw_tsv()
    row = find_row(rows, method_name)

    old_votes_text = consensus.votes_path(method_name).read_text(encoding="utf-8") \
        if consensus.votes_path(method_name).exists() else ""
    votes = consensus.load_votes(method_name)
    if not votes and row is not None and not is_assessment_empty(row):
        votes.append(baseline_vote(row))
    votes = upsert_vote(votes, build_vote(fields))
    votes_changed = consensus.votes_text(method_name, votes) != old_votes_text

    changes = []
    if row is None:
        rows.append(build_new_row(method_name, fields))
        status = "row-created"
    elif is_assessment_empty(row):
        fill_empty_row(row, fields)
        status = "row-filled"
    else:
        changes = compute_changes(row, consensus.compute_published(votes, row))
        if changes:
            print(f"'{method_name}' already assessed; applying {len(changes)} suggested change(s) for review.")
            apply_changes(row, changes)
            status = "assessment-revised"
        elif votes_changed:
            print(f"'{method_name}' already assessed; vote recorded, published assessment unchanged.")
            status = "vote-recorded"
        else:
            print(f"'{method_name}' already assessed and issue suggests no changes; nothing to do.")
            write_github_output("already-assessed-no-changes", "unchanged", method_name)
            return

    consensus.save_votes(method_name, votes)
    write_raw_tsv(header_lines, rows)
    # The cleaned data file is a build artifact regenerated from the raw TSV
    # by clean_method_assessments.py during the site build, so it is never
    # written here and never appears in auto-generated PRs.

    # Never overwrite (or duplicate) an existing documentation page, wherever it lives.
    existing_page = find_existing_file(method_name)
    if existing_page:
        page_status = "existing-elsewhere"
        print(f"Row updated; documentation page already exists at {existing_page.relative_to(PROJECT_ROOT)}, not touching it.")
    else:
        run_generate_method_pages()
        page_status = "generated"

    write_github_output(status, page_status, method_name, changes if status == "assessment-revised" else None)


if __name__ == "__main__":
    main()
