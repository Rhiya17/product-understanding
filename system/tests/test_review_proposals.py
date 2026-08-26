import json

from system import review_proposals


def claim(claim_id, tier="C0", claim_type="SPEC"):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": tier,
        "type": claim_type,
        "predicate": claim_id,
        "object": {"value": claim_id},
        "applicability": {"market": "US"},
        "authority": "MANUFACTURER_MANUAL",
        "source_bindings": [{
            "source_id": "src", "page": 1, "quote": f"Quote for {claim_id}",
        }],
        "extraction_notes": "notes",
    }


def verdict(claim_id, result="ENTAILED"):
    return {
        "claim_id": claim_id,
        "binding_index": 0,
        "verdict": result,
        "note": "faithful" if result == "ENTAILED" else "unsupported detail",
    }


def test_proposals_cover_every_undecided_claim_without_writing_reviews(tmp_path):
    pack = tmp_path / "test-product"
    pack.mkdir()
    claims = [
        claim("claim_alarm", "C0"),
        claim("claim_c3", "C3", "STEP"),
        claim("claim_batch", "C1"),
        claim("claim_reviewed", "C2"),
        claim("claim_reviewed_alarm", "C2"),
    ]
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    (pack / "verdicts.json").write_text(json.dumps({
        "status": "COMPLETE",
        "verdicts": [
            verdict("claim_alarm", "MEANING_CHANGED"),
            verdict("claim_c3"), verdict("claim_batch"),
            verdict("claim_reviewed"),
            verdict("claim_reviewed_alarm", "MEANING_CHANGED"),
        ],
        "conflict_triage": [],
    }), encoding="utf-8")
    reviews = {"reviews": [
        {"claim_id": "claim_reviewed", "reviewer": "owner@example.com",
         "disposition": "APPROVED_FOR_PUBLISH"},
        {"claim_id": "claim_reviewed_alarm", "reviewer": "owner@example.com",
         "disposition": "APPROVED_FOR_PUBLISH"},
    ]}
    reviews_path = pack / "reviews.json"
    reviews_path.write_text(json.dumps(reviews), encoding="utf-8")
    before = reviews_path.read_bytes()

    result = review_proposals.render_pack(pack, date="2026-08-26")
    text = (pack / "review-proposals.md").read_text()

    assert result["undecided"] == 3
    assert result["reopened_alarms"] == 1
    assert result["needs_recheck"] == 2
    assert result["proposed_reject"] == 0
    assert result["proposed_approve"] == 2
    assert "claim_alarm" in text
    assert "claim_c3" in text
    assert "claim_batch" in text
    assert "### `claim_reviewed`" not in text
    assert "claim_reviewed_alarm" in text
    assert "REOPENED AFTER V2 ALARM" in text
    assert "Rewrite the procedure step" not in text
    assert "OWNER CONFIRMS" in text
    assert reviews_path.read_bytes() == before
