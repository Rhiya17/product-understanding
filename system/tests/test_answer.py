import json

from system import answer


def make_claim(claim_id, predicate, obj, quote, tier="C0", ctype="SPEC"):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": tier,
        "type": ctype,
        "predicate": predicate,
        "object": obj,
        "source_bindings": [{
            "source_id": "src_spec", "page": None, "quote": quote,
        }],
    }


def build_vault_and_pack(tmp_path):
    vault = tmp_path / "vault"
    packs = tmp_path / "packs"
    product_dir = "acme-widget-9000"
    (vault / product_dir).mkdir(parents=True)
    (packs / product_dir).mkdir(parents=True)
    (vault / "catalog.json").write_text(json.dumps({
        "products": [{
            "product_id": "prod_acme_widget",
            "dir": product_dir,
            "brand": "Acme",
            "model": "Widget 9000",
            "category": "widget",
        }],
    }), encoding="utf-8")
    (vault / product_dir / "manifest.json").write_text(json.dumps({
        "sources": [{
            "source_id": "src_spec",
            "origin_url": "https://example.com/spec",
        }],
    }), encoding="utf-8")
    claims = [
        make_claim("claim_w_weight", "product_weight",
                   {"value": 7.5, "unit": "lb"}, "Weight 7.5 lb"),
        make_claim("claim_w_weight_old", "product_weight",
                   {"value": 8.1, "unit": "lb"}, "Weight 8.1 lb"),
        make_claim("claim_w_noise", "noise_level",
                   {"value": 24, "unit": "dB"}, "Noise level 24dB"),
        make_claim("claim_w_range", "bluetooth_range",
                   {"value": 30, "unit": "ft"}, "Range 30 ft"),
    ]
    (packs / product_dir / "claims.json").write_text(
        json.dumps(claims), encoding="utf-8")
    (packs / product_dir / "reviews.json").write_text(json.dumps({
        "reviews": [
            {"claim_id": "claim_w_weight", "reviewer": "owner@example.com",
             "disposition": "APPROVED_FOR_PUBLISH"},
            {"claim_id": "claim_w_weight_old", "reviewer": "owner@example.com",
             "disposition": "REJECTED_FOR_SERVING"},
            {"claim_id": "claim_w_range", "reviewer": "owner@example.com",
             "disposition": "APPROVED_FOR_PUBLISH"},
        ],
    }), encoding="utf-8")
    (packs / product_dir / "verdicts.json").write_text(json.dumps({
        "verdicts": [
            {"claim_id": "claim_w_weight", "binding_index": 0,
             "verdict": "ENTAILED", "note": "faithful"},
            {"claim_id": "claim_w_range", "binding_index": 0,
             "verdict": "MEANING_CHANGED", "note": "condition dropped"},
        ],
    }), encoding="utf-8")
    return packs, vault


def run(question, tmp_path, **kwargs):
    packs, vault = build_vault_and_pack(tmp_path)
    return answer.search(question, packs_root=packs, vault_root=vault,
                         **kwargs)


def test_published_claim_answers_with_citation(tmp_path):
    results, hidden = run("how much does the acme widget weigh?", tmp_path)
    assert results and results[0]["claim_id"] == "claim_w_weight"
    assert results[0]["status"] == "PUBLISHED"
    citation = results[0]["citations"][0]
    assert citation["quote"] == "Weight 7.5 lb"
    assert citation["origin_url"] == "https://example.com/spec"
    # Rejected sibling and any other non-published match are counted, not shown.
    assert hidden["REJECTED"] == 1


def test_candidate_and_suspended_hidden_by_default(tmp_path):
    results, hidden = run("how quiet is the widget? bluetooth range?",
                          tmp_path)
    returned = {row["claim_id"] for row in results}
    assert "claim_w_noise" not in returned  # CANDIDATE: no review yet
    assert "claim_w_range" not in returned  # SUSPENDED: approved + alarm
    assert hidden["CANDIDATE"] >= 1
    assert hidden["SUSPENDED"] == 1


def test_preview_labels_unpublished_matches(tmp_path):
    results, _ = run("bluetooth range and noise of the widget", tmp_path,
                     preview=True, top=10)
    statuses = {row["claim_id"]: row["status"] for row in results}
    assert statuses["claim_w_range"] == "SUSPENDED"
    assert statuses["claim_w_noise"] == "CANDIDATE"
    # Rejected claims stay out even in preview.
    assert "claim_w_weight_old" not in statuses


def test_synonyms_reach_predicate_vocabulary(tmp_path):
    results, _ = run("is the widget loud?", tmp_path, preview=True)
    assert results and results[0]["claim_id"] == "claim_w_noise"


def test_no_match_returns_empty(tmp_path):
    results, hidden = run("does it support warp drive?", tmp_path)
    assert results == []
    assert sum(hidden.values()) == 0


def test_procedure_question_composes_ordered_steps(tmp_path):
    packs, vault = build_vault_and_pack(tmp_path)
    steps = [
        {"claim_id": f"claim_w_fold_{n}", "consequence_ceiling": "C1",
         "type": "STEP", "predicate": "procedure_step",
         "object": {"procedure": "fold_widget", "step_number": n,
                    "action": f"Fold action {n}"},
         "source_bindings": [{"source_id": "src_spec", "page": None,
                              "quote": f"{n}. Fold action {n}"}]}
        for n in (3, 1, 2)
    ]
    pack = packs / "acme-widget-9000"
    existing = json.loads((pack / "claims.json").read_text())
    (pack / "claims.json").write_text(json.dumps(existing + steps),
                                     encoding="utf-8")
    results, _ = answer.search("how do I fold the widget? fold action",
                               packs_root=packs, vault_root=vault,
                               preview=True, top=5)
    composed = [row for row in results if row.get("steps")]
    assert len(composed) == 1
    row = composed[0]
    assert row["claim_id"] == "procedure:fold_widget"
    assert [step["step_number"] for step in row["steps"]] == [1, 2, 3]
    assert results[0] is row  # the assembled procedure outranks fragments
    fragment_ids = {r["claim_id"] for r in results if not r.get("steps")}
    assert not fragment_ids & {"claim_w_fold_1", "claim_w_fold_2",
                               "claim_w_fold_3"}
