import json

from system import review_queue


def make_claim(claim_id, tier, notes="notes", quote="A | B\nsecond line"):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": tier,
        "type": "SPEC",
        "predicate": claim_id,
        "object": {"value": claim_id},
        "source_bindings": [{
            "source_id": "src_text", "page": None, "quote": quote,
        }],
        "extraction_notes": notes,
    }


def verdict(claim_id, result="ENTAILED", note="faithful"):
    return {
        "claim_id": claim_id, "binding_index": 0,
        "verdict": result, "note": note,
    }


def test_queue_ordering_unresolved_bucket_fences_and_human_skip(tmp_path):
    pack = tmp_path / "test-product"
    pack.mkdir()
    alarm = make_claim("claim_alarm", "C0")
    conflict_a = make_claim(
        "claim_conflict_a", "C3",
        notes="CONFLICT: contradicts claim_conflict_b — mismatch.")
    conflict_b = make_claim(
        "claim_conflict_b", "C2",
        notes="CONFLICT: contradicts claim_conflict_a — mismatch.")
    c3 = make_claim("claim_c3", "C3")
    c2 = make_claim("claim_c2", "C2")
    unresolved_c0 = make_claim("claim_unresolved_c0", "C0")
    missing_c1 = make_claim("claim_missing_c1", "C1")
    eligible = make_claim("claim_eligible", "C0")
    human = make_claim("claim_human", "C3")
    claims = [alarm, conflict_a, conflict_b, c3, c2, unresolved_c0,
              missing_c1, eligible, human]
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    (pack / "gaps.json").write_text(json.dumps({
        "gaps": [{
            "gap_id": "gap_one", "kind": "SOURCE_MISSING", "waives": [],
            "reason": "Source absent.", "closes_when": "Capture it.",
        }]
    }), encoding="utf-8")
    entries = [
        verdict("claim_alarm", "MEANING_CHANGED", "number changed"),
        verdict("claim_conflict_a"), verdict("claim_conflict_b"),
        verdict("claim_c3"), verdict("claim_c2"),
        verdict("claim_unresolved_c0", "CANNOT_JUDGE", "unclear"),
        verdict("claim_eligible"), verdict("claim_human"),
    ]
    (pack / "verdicts.json").write_text(json.dumps({
        "model": "qwen/qwen3-vl-235b-a22b-instruct",
        "prompt_version": "v1", "date": "2026-08-24", "status": "COMPLETE",
        "verdicts": entries,
        "conflict_triage": [{
            "pair": ["claim_conflict_a", "claim_conflict_b"],
            "result": "GENUINE_CONFLICT", "note": "The numbers differ.",
            "context_sha256": "a" * 64,
        }],
    }), encoding="utf-8")
    (pack / "reviews.json").write_text(json.dumps({
        "reviews": [
            {"claim_id": "claim_human", "reviewer": "human@example.com",
             "scope": "manual", "disposition": "NEEDS_RECHECK"},
        ]
    }), encoding="utf-8")

    result = review_queue.render_pack(pack)
    text = (pack / "review-queue.md").read_text()

    assert result == {
        "product": "test-product", "alarms": 1, "conflicts": 1,
        "c3": 1, "c2": 1, "unresolved_verifier": 2,
        "gaps": 1, "batch_eligible": 1, "spot_audit_sample": 1,
        "path": str(pack / "review-queue.md"),
    }
    headings = [
        "## 1. MEANING_CHANGED alarms", "## 2. Unresolved conflict pairs",
        "## 3. C3 claims", "## 4. C2 claims",
        "## 5. Unresolved verifier — C0/C1", "## 6. Open gaps",
        "## 7. Batch-eligible C0/C1 spot-audit",
    ]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "Triage (advisory): `GENUINE_CONFLICT`" in text
    assert "claim_missing_c1" in text
    assert "one or more binding verdicts are missing" in text
    assert "claim_human" not in text
    assert "claim_eligible" in text
    assert "Spot-audit sample: `1` of `1` eligible claims." in text
    assert "```text\nA | B\nsecond line\n```" in text
    assert "```json" in text


def test_partial_status_routes_all_unreviewed_c0_c1_to_unresolved(tmp_path):
    pack = tmp_path / "partial-product"
    pack.mkdir()
    claims = [make_claim("claim_c0", "C0"), make_claim("claim_c1", "C1")]
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    (pack / "gaps.json").write_text(json.dumps({"gaps": []}), encoding="utf-8")
    (pack / "verdicts.json").write_text(json.dumps({
        "status": "PARTIAL", "verdicts": [verdict("claim_c0")],
        "conflict_triage": [],
    }), encoding="utf-8")

    result = review_queue.render_pack(pack)
    text = (pack / "review-queue.md").read_text()
    assert result["unresolved_verifier"] == 2
    assert text.count("document status is PARTIAL") == 2


def test_spot_audit_sample_is_stable_and_limited_to_five():
    claims = [make_claim(f"claim_{index}", "C0") for index in range(12)]
    first = review_queue.spot_audit_sample("test-product", claims)
    second = review_queue.spot_audit_sample("test-product", list(reversed(claims)))

    assert len(first) == 5
    assert [claim["claim_id"] for claim in first] == [
        claim["claim_id"] for claim in second
    ]
