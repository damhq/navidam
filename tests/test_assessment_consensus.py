import json
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "scripts"))

import assessment_consensus as ac  # noqa: E402


def vote(confidence, **answers):
    return {"assessor": "A", "confidence": confidence, "answers": {k: v.split("|") for k, v in answers.items()}}


def status_of(votes):
    return ac.method_status(votes)


def test_single_vote_is_single_status_with_confidence():
    result = status_of([vote(4, IID="Required")])
    assert result["status"] == "single"
    assert result["confidence"] == 4


def test_two_identical_assessments_are_consensus():
    votes = [vote(4, IID="Required", Objective="Detection"), vote(2, IID="Required", Objective="Detection")]
    result = status_of(votes)
    assert result["status"] == "consensus"
    assert result["agreement_share"] == 1


def test_two_opposite_ordinal_answers_are_debated():
    votes = [vote(3, IID="Required"), vote(3, IID="Relaxes assumption")]
    result = status_of(votes)
    assert result["status"] == "debated"
    assert result["criteria"][0]["debated"] is True


def test_adjacent_ordinal_answers_are_below_the_bar():
    # Squared similarity makes adjacent levels score 0.25, giving agreement 62.5%.
    votes = [vote(3, IID="Required"), vote(3, IID="Recommended")]
    assert ac.similarity("IID", ["Required"], ["Recommended"]) == 0.25
    assert status_of(votes)["criteria"][0]["agreement"] == pytest.approx(0.625)
    assert status_of(votes)["status"] == "debated"


def test_criterion_agreement_bar_is_80_percent():
    votes = [vote(3, IID="Required"), vote(3, IID="Required"), vote(3, IID="Relaxes assumption")]
    crit = status_of(votes)["criteria"][0]
    assert crit["agreement"] == pytest.approx(2 / 3, abs=1e-3)
    assert crit["debated"] is True
    votes = [vote(5, IID="Required"), vote(5, IID="Required"), vote(1, IID="Relaxes assumption")]
    assert status_of(votes)["criteria"][0]["debated"] is False


def test_confidence_weights_the_agreement():
    # Softened weights: 5/5 -> 1; 1/5 -> sqrt(0.2), so support remains below 80%.
    votes = [vote(5, Language="R"), vote(1, Language="Python")]
    assert ac.weight(votes[0]) == 1
    assert ac.weight(votes[1]) == pytest.approx(0.2 ** 0.5)
    assert status_of(votes)["status"] == "debated"
    assert ac.consensus_value(votes, "Language") == ["R"]


def test_multiple_choice_uses_jaccard():
    assert ac.similarity("Language", ["R", "Python"], ["R"]) == 0.25
    assert ac.similarity("Language", ["R"], ["Python"]) == 0.0


def test_non_level_ordinal_answers_only_match_themselves():
    assert ac.similarity("IID", ["Inapplicable"], ["Required"]) == 0.0
    assert ac.similarity("IID", ["Inapplicable"], ["Inapplicable"]) == 1.0


def test_legacy_multiple_values_on_ordinal_criteria():
    # Several levels count as the most permissive one; duplicates and non-level values are ignored.
    assert ac.similarity("IID", ["Required", "Recommended"], ["Recommended"]) == 1.0
    assert ac.similarity("IID", ["Required", "Recommended"], ["Required"]) == 0.25
    assert ac.similarity("IID", ["Required", "Recommended"], ["Required", "Recommended"]) == 1.0
    assert ac.similarity("IID", ["Recommended", "Recommended"], ["Recommended"]) == 1.0
    assert ac.similarity("IID", ["Recommended", "Inapplicable"], ["Recommended"]) == 1.0
    assert ac.similarity("IID", ["Required", "Recommended"], ["Relaxes assumption"]) == 0.25


def test_share_of_criteria_decides_method_status():
    # Model specific is unticked in both votes: an agreed "None" answer.
    agree = dict(Objective="Detection", Language="R", Usage="a", **{"Model specific": "None"})
    votes = [vote(3, IID="Required", **agree), vote(3, IID="Relaxes assumption", **agree)]
    result = status_of(votes)
    assert (result["agreeing"], result["evaluated"]) == (4, 5)
    assert result["status"] == "consensus"  # 4/5 == 80%
    agree.update(Language="R")
    votes = [vote(3, IID="Required", **agree), vote(3, IID="Relaxes assumption", Objective="Detection", Language="Python", Usage="b")]
    assert status_of(votes)["status"] == "debated"
    exactly_at_threshold = dict(agree, Type="Spatial only")
    votes = [
        vote(3, IID="Required", **exactly_at_threshold),
        vote(3, IID="Relaxes assumption", **exactly_at_threshold),
    ]
    assert status_of(votes)["status"] == "consensus"  # 4/5 == 80%
    more = dict(agree, Faithfulness="Required", Type="x", Estimand="y", Usage="a", **{"Number of variables": "z"}, **{"Exposure type": "w"})
    votes = [vote(3, IID="Required", **more), vote(3, IID="Relaxes assumption", **more)]
    assert status_of(votes)["status"] == "consensus"  # 8/9 >= 80%


def test_published_value_prefers_current_value_on_tie():
    votes = [vote(3, Language="R"), vote(3, Language="Python")]
    assert ac.compute_published(votes, {"Language": "Python"})["Language"] == "Python"
    assert ac.compute_published(votes, {"Language": "R"})["Language"] == "R"


def test_published_confidence_is_rounded_mean():
    votes = [vote(5, IID="Required"), vote(2, IID="Required")]
    assert ac.compute_published(votes)[ac.CONFIDENCE_COLUMN] == "4"


def test_status_file_hides_issue_numbers(tmp_path):
    votes_dir = tmp_path / "votes"
    votes_dir.mkdir()
    data = {"method": "M", "votes": [
        dict(vote(3, IID="Required"), assessor="A", issue=12),
        dict(vote(3, IID="Required"), assessor="B", issue=13),
    ]}
    (votes_dir / "m.json").write_text(json.dumps(data), encoding="utf-8")
    out = tmp_path / "status.json"
    ac.build_status_file(votes_dir, out)
    text = out.read_text(encoding="utf-8")
    assert json.loads(text)["M"]["status"] == "consensus"
    assert "issue" not in text


def test_status_uses_only_newest_vote_per_named_assessor(tmp_path):
    votes_dir = tmp_path / "votes"
    votes_dir.mkdir()
    old = dict(vote(2, IID="Required"), assessor="A", baseline=True)
    new = dict(vote(4, IID="Recommended"), assessor="A", issue=84, date="2026-10-13")
    (votes_dir / "m.json").write_text(
        json.dumps({"method": "M", "votes": [old, new]}), encoding="utf-8"
    )
    out = tmp_path / "status.json"
    ac.build_status_file(votes_dir, out)
    status = json.loads(out.read_text(encoding="utf-8"))["M"]
    assert status["status"] == "single"
    assert status["assessors"] == 1
    assert status["voters"] == [{"name": "A", "confidence": 4}]


def test_ordinal_levels_match_issue_template():
    src = (ROOT_DIR / ".github/ISSUE_TEMPLATE/method-assessment.yml").read_text(encoding="utf-8")
    for block in yaml.safe_load(src)["body"]:
        field_id = block.get("id")
        if not field_id or not re.search(r"# Ordinal criteria\n\s+id: " + field_id + "\n", src) or field_id == "confidence":
            continue
        label = block["attributes"]["label"]
        entry = next((v for k, v in ac.CRITERIA.items() if v[0] == label or k == label), None)
        assert entry is not None, f"{label} missing from CRITERIA"
        assert entry[1] == "ordinal"
        assert entry[2] == [o for o in block["attributes"]["options"] if o != "Inapplicable"]


def test_minimal_ts_length_legacy_multiple_values_use_most_permissive_level():
    legacy = ["Handles ≤ 10", "≥ 10", "≥ 100"]
    assert ac.similarity("Minimal TS length", legacy, ["Handles ≤ 10"]) == 1.0
    assert ac.similarity("Minimal TS length", legacy, ["≥ 100"]) == 0.0
    assert ac.similarity("Minimal TS length", ["≥ 10", "≥ 100"], ["≥ 10"]) == 1.0


def test_diverging_assessors_published_value():
    # Higher confidence wins.
    votes = [vote(2, Language="R"), vote(4, Language="Python")]
    assert ac.compute_published(votes, {"Language": "R"})["Language"] == "Python"
    # Same confidence: the currently published value is kept, else the earliest vote.
    votes = [vote(3, Language="R"), vote(3, Language="Python")]
    assert ac.compute_published(votes, {"Language": "Python"})["Language"] == "Python"
    assert ac.compute_published(votes)["Language"] == "R"


def test_exposure_all_is_union_of_types():
    from assessment_consensus import similarity
    five = ["Binary", "Categorical", "Continuous / Time-varying", "Compositional", "Multivariate"]
    assert similarity("Exposure type", ["All"], five) == 1.0
    assert similarity("Exposure type", ["All"], ["Binary"]) == (1 / 5) ** 2
    assert similarity("Exposure type", ["All"], ["Inapplicable"]) == 0.0


def test_same_author_replaces_previous_vote_even_if_anonymous():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from process_method_assessment_issue import upsert_vote, author_key
    def v(shown, real, issue, conf):
        return {"issue": issue, "assessor": shown, "author_key": author_key(real), "confidence": conf, "answers": {}}
    legacy = {"issue": None, "baseline": True, "assessor": "Jean Dupont", "confidence": 2, "answers": {}}
    votes = [legacy, v("Anonymous", "Marie Curie", 2, 3)]
    votes = upsert_vote(votes, v("Jean Dupont", " jean  dupont ", 5, 4))
    assert [(x["issue"], x["confidence"]) for x in votes] == [(5, 4), (2, 3)]
    votes = upsert_vote(votes, v("Anonymous", "marie curie", 6, 5))
    assert [(x["issue"], x["confidence"]) for x in votes] == [(5, 4), (6, 5)]
    assert "Marie" not in str(votes)
    votes = upsert_vote(votes, v("Anonymous", "", 7, 3))
    assert len(votes) == 3


def test_new_submission_cleans_existing_same_author_duplicates():
    from process_method_assessment_issue import upsert_vote, author_key
    old = {"issue": None, "baseline": True, "assessor": "Joaquim Estopinan",
           "confidence": 3, "answers": {}}
    prior = {"issue": 84, "date": "2026-10-13", "assessor": "Joaquim Estopinan",
             "author_key": author_key("Joaquim Estopinan"), "confidence": 4, "answers": {}}
    replacement = {"issue": 91, "date": "2026-10-19", "assessor": "Joaquim Estopinan",
                   "author_key": author_key("Joaquim Estopinan"), "confidence": 5, "answers": {}}
    assert upsert_vote([old, prior], replacement) == [replacement]


def test_status_exposes_per_assessor_values():
    votes = [vote(3, IID="Required"), vote(5, IID="Recommended")]
    status = ac.method_status(votes)
    assert len(status["voters"]) == 2
    crit = next(c for c in status["criteria"] if c["column"] == "IID")
    assert crit["values"] == ["Required", "Recommended"]


def test_no_model_specific_assumption_is_a_valid_agreeing_answer():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import process_method_assessment_issue as pm
    fields = {"model_specific_assumptions": []}
    assert pm.issue_answers(fields)["Model specific"] == ["None"]
    votes = [vote(3, **{"Model specific": "None"}), vote(4, **{"Model specific": "None"})]
    crit = next(c for c in ac.method_status(votes)["criteria"] if c["column"] == "Model specific")
    assert not crit["debated"]
    assert ac.compute_published(votes, {"Model specific": ""})["Model specific"] == ""
    row = {"Model specific": "", "Confidence in assessment": "4"}
    assert pm.compute_changes(row, ac.compute_published(votes, row)) == []


def test_none_versus_one_assumption_is_debated_and_can_publish_empty():
    import process_method_assessment_issue as pm
    votes = [vote(2, **{"Model specific": "Stationarity"}), vote(5, **{"Model specific": "None"})]
    crit = next(c for c in ac.method_status(votes)["criteria"] if c["column"] == "Model specific")
    assert crit["debated"]
    row = {"Model specific": "Stationarity", "Confidence in assessment": "4"}
    changes = pm.compute_changes(row, ac.compute_published(votes, row))
    assert ("Model specific", "Stationarity", "") in changes
