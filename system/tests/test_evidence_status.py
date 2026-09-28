import json

import pytest

from system import evidence_status, spend_guard
from system import verify_claims as verifier
from system.evidence_status import PackEvidence, SourceText

QUOTE = "The maximum supported weight is 30 lb."


def make_pack(tmp_path, quote=QUOTE, source_name="source.md", approved=True,
              verdicts=None):
    packs = tmp_path / "evidence-packs"
    vault = tmp_path / "source-vault"
    pack = packs / "test-product"
    pack.mkdir(parents=True)
    (vault / "test-product").mkdir(parents=True)
    source_path = vault / "test-product" / source_name
    source_path.write_text(QUOTE + " Keep the product dry.\n", encoding="utf-8")
    manifest = {"sources": [{"source_id": "src_text", "type": "SPEC_PAGE",
                             "local_path": source_name,
                             "sha256": evidence_status.file_sha256(source_path)}]}
    (vault / "test-product" / "manifest.json").write_text(json.dumps(manifest))
    claim = {"claim_id": "claim_weight", "version": 1, "type": "LIMIT",
             "predicate": "maximum_weight", "subject": "prod_test",
             "applicability": {}, "consequence_ceiling": "C3",
             "object": {"value": 30, "unit": "lb"},
             "source_bindings": [{"source_id": "src_text", "page": None, "quote": quote}]}
    (pack / "claims.json").write_text(json.dumps([claim]))
    reviews = [{"claim_id": "claim_weight",
                "disposition": "APPROVED_FOR_PUBLISH" if approved else "NEEDS_RECHECK"}]
    (pack / "reviews.json").write_text(json.dumps({"reviews": reviews}))
    if verdicts is not None:
        (pack / "verdicts.json").write_text(json.dumps(verdicts))
    return packs, vault, pack, claim


def evidence(tmp_path, packs, vault, **kwargs):
    return PackEvidence("test-product", packs_root=packs, vault_root=vault,
                        source_text=SourceText(tmp_path / "text-cache", **kwargs))


def entailed_receipt(pack, claim, receipt_id="rcpt_1"):
    evidence_status.append_receipt(pack, {
        "kind": "semantic_check", "claim_id": claim["claim_id"],
        "claim_digest": evidence_status.claim_digest(claim),
        "result": "ENTAILED", "receipt_id": receipt_id})


def test_fully_supported_claim_is_eligible(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path)
    entailed_receipt(pack, claim)
    decision = evidence(tmp_path, packs, vault).decision("claim_weight")
    assert decision["eligible"], decision["reasons"]


def test_ev01_fabricated_quote_suffix_is_rejected(tmp_path):
    # The first 60 characters match the source; the suffix was invented.
    packs, vault, pack, claim = make_pack(
        tmp_path, quote=QUOTE + " It is also safe for adults up to 300 lb.")
    entailed_receipt(pack, claim)
    decision = evidence(tmp_path, packs, vault).decision("claim_weight")
    assert not decision["eligible"]
    assert "binding_0:quote_not_found" in decision["reasons"]


def test_ev02_parser_unavailable_is_visible_not_a_pass(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path, source_name="manual.pdf")

    def missing_parser(_path):
        raise evidence_status.ParserUnavailable("pypdfium2 is not installed")

    entailed_receipt(pack, claim)
    decision = evidence(tmp_path, packs, vault, pdf_parser=missing_parser).decision(
        "claim_weight")
    assert not decision["eligible"]
    assert "binding_0:parser_unavailable" in decision["reasons"]


def test_ev03_failed_recheck_never_clears_an_alarm(tmp_path):
    alarm = {"model": verifier.MODEL_ID, "prompt_version": "v2", "date": "2026-08-01",
             "status": "PARTIAL", "reason": "earlier run",
             "verdicts": [{"claim_id": "claim_weight", "binding_index": 0,
                           "verdict": "MEANING_CHANGED", "note": "changed", "basis": "CLAIM_QUOTE_UNION"}]}
    packs, vault, pack, claim = make_pack(tmp_path, verdicts=alarm)

    def failed(_arguments):
        raise verifier.ProviderFailure("unavailable")

    verifier.verify_pack(pack, vault_root=vault, cache_path=tmp_path / "cache.json",
                         provider=failed, date="2026-09-23")
    document = json.loads((pack / "verdicts.json").read_text())
    assert document["status"] == "FAILED"
    assert [v["verdict"] for v in document["verdicts"]] == ["MEANING_CHANGED"]
    decision = evidence(tmp_path, packs, vault).decision("claim_weight")
    assert "unresolved_alarm" in decision["reasons"]


def test_alarm_needs_entailed_recheck_and_resolution_record(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path)
    digest = evidence_status.claim_digest(claim)
    evidence_status.append_receipt(pack, {"kind": "semantic_check", "claim_id": "claim_weight",
                                          "claim_digest": digest, "result": "MEANING_CHANGED",
                                          "receipt_id": "r_alarm"})
    entailed_receipt(pack, claim, receipt_id="r_recheck")
    assert "unresolved_alarm" in evidence(tmp_path, packs, vault).decision("claim_weight")["reasons"]
    evidence_status.append_receipt(pack, {"kind": "alarm_resolution", "claim_id": "claim_weight",
                                          "claim_digest": digest, "recheck_receipt_id": "r_recheck",
                                          "rationale": "source-level recheck"})
    assert evidence(tmp_path, packs, vault).decision("claim_weight")["eligible"]


def test_ev04_receipt_binds_to_the_exact_claim_version(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path)
    entailed_receipt(pack, claim)
    changed = dict(claim, object={"value": 35, "unit": "lb"})
    (pack / "claims.json").write_text(json.dumps([changed]))
    decision = evidence(tmp_path, packs, vault).decision("claim_weight")
    assert "no_receipt_for_current_version" in decision["reasons"]


def test_unapproved_and_source_hash_changes_block_serving(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path, approved=False)
    entailed_receipt(pack, claim)
    (vault / "test-product" / "source.md").write_text("edited source\n")
    reasons = evidence(tmp_path, packs, vault).decision("claim_weight")["reasons"]
    assert "not_approved" in reasons
    assert "binding_0:source_hash_mismatch" in reasons


def test_receipt_run_is_metered_and_stops_on_provider_failure(tmp_path):
    packs, vault, pack, claim = make_pack(tmp_path)
    guard = spend_guard.SpendGuard(tmp_path / "approvals.jsonl", tmp_path / "ledger.jsonl")
    manifest = {"run_id": "run_t", "category": "answer_verifier", "purpose": "test",
                "provider": "fake", "model": verifier.MODEL_ID, "inputs": {"claims": ["claim_weight"]},
                "max_calls": 5, "cap_usd": 0.5, "retry_policy": "none"}
    receipt = spend_guard.record_owner_approval(manifest, "owner@example.com",
                                                approvals_path=guard.approvals_path)
    run = guard.authorize(manifest, receipt["approval_id"])

    def entailed(_arguments):
        return {"output": json.dumps({"verdict": "ENTAILED", "note": "Faithful."}),
                "model": verifier.MODEL_ID, "usage": {"cost": 0.0002}}

    summary = verifier.verify_claims_to_receipts(pack, ["claim_weight"], run, "run_t",
                                                 provider=entailed)
    assert summary["results"] == {"claim_weight": "ENTAILED"}
    assert evidence(tmp_path, packs, vault).decision("claim_weight")["eligible"]

    def failed(_arguments):
        raise verifier.ProviderFailure("down")

    summary = verifier.verify_claims_to_receipts(pack, ["claim_weight"], run, "run_t",
                                                 provider=failed)
    assert summary["stopped"].startswith("ProviderFailure")
    with pytest.raises(spend_guard.SpendRefused):
        run.reserve(0.01, "after unknown billing")
    # The failure is its own receipt kind; the ENTAILED verdict still stands.
    assert evidence(tmp_path, packs, vault).decision("claim_weight")["eligible"]
