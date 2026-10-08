import json
import re
import shutil
from pathlib import Path

import pytest

from system import evidence_status
from system.answer_engine import AnswerEngine

REPO_ROOT = Path(__file__).resolve().parents[2]
LAUNCH = REPO_ROOT / "docs" / "workorders" / "showme-launch-regression-cases.json"


def add_test_receipts(packs, result="ENTAILED", only=None):
    """Explicitly test-only receipts in an isolated copy of the packs."""
    for pack_dir in sorted(p.parent for p in packs.glob("*/claims.json")):
        pack = evidence_status.PackEvidence(pack_dir.name, packs_root=packs)
        for claim_id, claim in pack.claims.items():
            if only is not None and claim_id not in only:
                continue
            if pack.dispositions.get(claim_id) == "APPROVED_FOR_PUBLISH":
                evidence_status.append_receipt(pack_dir, {
                    "kind": "semantic_check", "claim_id": claim_id,
                    "claim_digest": evidence_status.claim_digest(claim),
                    "result": result, "receipt_id": f"TEST_ONLY_{claim_id}_{result}"})


@pytest.fixture(scope="module")
def packs(tmp_path_factory):
    root = tmp_path_factory.mktemp("packs") / "evidence-packs"
    shutil.copytree(REPO_ROOT / "evidence-packs", root,
                    ignore=shutil.ignore_patterns("__pycache__", "*.py", "workorders",
                                                  "verification-receipts.jsonl"))
    add_test_receipts(root)
    return root


@pytest.fixture(scope="module")
def engine(packs, tmp_path_factory):
    return AnswerEngine(packs_root=packs, source_text=evidence_status.SourceText(
        tmp_path_factory.mktemp("text-cache")))


def claim_ids(document):
    return [item["claim_id"] for block in document["blocks"]
            for item in block["items"] if item.get("claim_id")]


def outcome(document):
    return {"needs_input": "clarify", "unsupported": "missing_evidence"}.get(
        document["status"], "answer")


@pytest.mark.parametrize("case", json.loads(LAUNCH.read_text())["cases"],
                         ids=lambda case: case["id"])
def test_launch_questions_meet_their_rubric(engine, case):
    document = engine.answer(case["question"], case["selected_product"] or None).to_dict()
    ids = set(claim_ids(document))
    assert outcome(document) in case["acceptable_outcomes"]
    assert set(case["required_claim_ids"]) <= ids
    assert not set(case["forbidden_claim_ids"]) & ids


def test_weight_question_never_substitutes_a_component_limit(engine):
    # Since 2026-10-07 the pack has its own product-weight claim
    # (claim_r2j_spec_product_weight, 13.2 lb). In this fixture it has no
    # receipt, so it is not served; a component limit must never stand in.
    document = engine.answer("How much does the Ready2Jet stroller weigh?").to_dict()
    assert document["status"] == "unsupported"
    assert not {"claim_r2j_dimension_basket_capacity",
                "claim_r2j_limit_cup_holder_weight"} & set(claim_ids(document))
    assert not re.search(r"\b(10|1)\s*(lb|kg|pound)", document["direct_answer"], re.I)


def test_positive_control_answers_when_evidence_exists(engine):
    document = engine.answer("How much does the MacBook Air weigh?").to_dict()
    assert document["status"] == "ready"
    assert "claim_mba_spec_weight" in claim_ids(document)
    assert "2.7" in document["direct_answer"]


@pytest.mark.parametrize("question", [
    "How do I operate the Ready2Jet stroller brakes?",
    "How do I use the Ready2Jet brakes?",
    "Show me how to lock the Ready2Jet brakes",
    "Show me the Ready2Jet brakes",
])
def test_control_operation_routes_to_complete_owned_procedure(engine, question):
    document = engine.answer(question).to_dict()
    assert document["coverage"]["procedure_id"] == "brake"
    assert document["status"] == "ready"
    assert {"claim_r2j_step_brake_1", "claim_r2j_step_brake_2"} <= set(claim_ids(document))
    assert "claim_r2j_step_fold_2" not in claim_ids(document)


def test_negation_and_permission_polarity(engine):
    wash = engine.answer("Can I machine wash the stroller seat?",
                         "graco-ready2jet-2212125").to_dict()
    assert wash["direct_answer"].startswith("No.")
    cup = engine.answer("Is the cup holder dishwasher safe?",
                        "graco-ready2jet-2212125").to_dict()
    assert cup["direct_answer"].startswith("Yes.")
    assert "top rack" in cup["direct_answer"].lower()


def test_ev06_revision_scope_is_applied(engine):
    original = engine.answer("How loud is the original Core 300S (HEAPAPLVSUS0073)?",
                             "levoit-core-300s").to_dict()
    assert original["status"] == "unsupported"
    assert "claim_c300s_spec_noise_300sp" not in claim_ids(original)
    current = engine.answer("How loud is the Core 300S-P?", "levoit-core-300s").to_dict()
    assert "300S-P" in current["direct_answer"]


def test_follow_up_view_inherits_the_parent_procedure(engine):
    parent = engine.answer("How do I fold the Ready2Jet stroller?").to_dict()
    follow = engine.answer("Show it from behind", None, parent["context"]).to_dict()
    assert follow["status"] == "ready"
    assert claim_ids(follow)[:7] == parent["coverage"]["required_steps"]
    assert "isn't available yet" in follow["visual"]["message"]
    alone = engine.answer("Show it from behind", "graco-ready2jet-2212125").to_dict()
    assert alone["status"] == "needs_input"


def test_ev05_missing_middle_step_blocks_a_complete_procedure(packs, tmp_path):
    copy = tmp_path / "evidence-packs"
    shutil.copytree(packs, copy)
    add_test_receipts(copy, result="MEANING_CHANGED", only={"claim_r2j_step_fold_4"})
    engine = AnswerEngine(packs_root=copy, source_text=evidence_status.SourceText(tmp_path / "t"))
    document = engine.answer("How do I fold the Ready2Jet stroller?").to_dict()
    assert document["status"] == "partial"
    assert document["coverage"]["complete"] is False
    assert document["coverage"]["missing_steps"] == ["claim_r2j_step_fold_4"]
    steps = next(b for b in document["blocks"] if b["kind"] == "steps")
    assert len(steps["items"]) == 7
    assert steps["items"][3].get("unverified") is True
    assert "Follow these 7 steps" not in document["direct_answer"]


def test_without_receipts_nothing_is_served(tmp_path):
    copy = tmp_path / "evidence-packs"
    shutil.copytree(REPO_ROOT / "evidence-packs", copy,
                    ignore=shutil.ignore_patterns("__pycache__", "*.py", "workorders",
                                                  "verification-receipts.jsonl"))
    engine = AnswerEngine(packs_root=copy, source_text=evidence_status.SourceText(tmp_path / "t"))
    document = engine.answer("Can I machine wash the stroller seat?",
                             "graco-ready2jet-2212125").to_dict()
    assert document["status"] == "unsupported"
    assert document["gap"]["reason"] == "not_verified"
    assert claim_ids(document) == []
