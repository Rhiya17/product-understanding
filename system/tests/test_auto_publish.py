import json

from system import auto_publish, evidence_status, fit_engine
from system.evidence_status import PackEvidence

TEXT = ("Folded it measures 30 H x 20.5 W x 11.5 D in. Retail table: 31 x 19.5 x 11 in. "
        "Size less than 43.5*12.0*8.0. Trunk depth 1060 mm. Floor to top 680 mm. "
        "Opening 1140 mm. Floor width 940 mm.")


def claim(cid, quote, obj, subject="prod_obj", notes=None, app=None, ctype="SPEC"):
    return {"claim_id": cid, "version": 1, "type": ctype, "predicate": cid,
            "subject": subject, "applicability": app or {}, "consequence_ceiling": "C2",
            "object": obj, "authority": "MANUFACTURER_SPEC_PAGE",
            "source_bindings": [{"source_id": "src", "page": None, "quote": quote}],
            **({"extraction_notes": notes} if notes else {})}


def make(tmp_path, product, product_id, claims, receipts=True, identity=None, reviews=None):
    packs, vault = tmp_path / "evidence-packs", tmp_path / "source-vault"
    (packs / product).mkdir(parents=True, exist_ok=True)
    (vault / product).mkdir(parents=True, exist_ok=True)
    src = vault / product / "s.md"
    src.write_text(TEXT)
    (vault / product / "manifest.json").write_text(json.dumps({
        "product_id": product_id, "identity": identity or {"market": "US"},
        "sources": [{"source_id": "src", "type": "SPEC_PAGE", "local_path": "s.md",
                     "authority": "MANUFACTURER", "sha256": evidence_status.file_sha256(src)}]}))
    (packs / product / "claims.json").write_text(json.dumps(claims))
    if reviews:
        (packs / product / "reviews.json").write_text(json.dumps({"reviews": reviews}))
    if receipts:
        for c in claims:
            evidence_status.append_receipt(packs / product, {
                "kind": "semantic_check", "claim_id": c["claim_id"],
                "claim_digest": evidence_status.claim_digest(c), "result": "ENTAILED",
                "model": "qwen/qwen3-vl-235b-a22b-instruct", "receipt_id": "r_" + c["claim_id"]})
    return packs, vault


def folded_claims():
    return [
        claim("claim_gcc", "Folded it measures 30 H x 20.5 W x 11.5 D in.",
              {"height": 30, "width": 20.5, "depth": 11.5, "unit": "in",
               "authority_note": "Graco Consumer Care (brand account) answer"},
              notes="CONFLICT: contradicts claim_target and claim_amazon."),
        claim("claim_target", "Retail table: 31 x 19.5 x 11 in.",
              {"height": 31, "width": 19.5, "depth": 11, "unit": "in",
               "authority_note": "Target.com table (retailer data, not brand-authored)"},
              notes="CONFLICT: contradicts claim_gcc and claim_amazon."),
        claim("claim_amazon", "Size less than 43.5*12.0*8.0.",
              {"values": [43.5, 12, 8], "axes": None, "qualifier": "upper bound ('Less than')",
               "unit": "in", "authority_note": "Amazon (retailer data, not brand-authored)"},
              notes="CONFLICT: contradicts claim_gcc and claim_target."),
    ]


def test_conflict_rules_rank_brand_over_retailer_and_exclude_unlabeled(tmp_path):
    packs, vault = make(tmp_path, "obj", "prod_obj", folded_claims())
    resolutions, decisions = auto_publish.run("obj", packs, vault)
    assert len(resolutions) == 1
    outcomes = resolutions[0]["outcomes"]
    assert outcomes == {"claim_gcc": "SERVE", "claim_target": "SUPERSEDED", "claim_amazon": "EXCLUDED"}
    by = {d["claim_id"]: d["decision"] for d in decisions}
    assert by == {"claim_gcc": "AUTO_APPROVED", "claim_target": "AUTO_HELD", "claim_amazon": "AUTO_HELD"}
    pack = PackEvidence("obj", packs_root=packs, vault_root=vault)
    assert pack.eligible("claim_gcc") and not pack.eligible("claim_target")
    assert pack.decision("claim_gcc")["approval_basis"] == "auto:auto-publish-v1"


def test_no_independent_receipt_means_held(tmp_path):
    packs, vault = make(tmp_path, "obj", "prod_obj", folded_claims()[:1], receipts=False)
    _, decisions = auto_publish.run("obj", packs, vault)
    assert decisions[0]["decision"] == "AUTO_HELD"
    assert "independent_verification" in decisions[0]["failed_checks"]


def test_claude_receipt_is_not_independent(tmp_path):
    c = folded_claims()[0]
    c.pop("extraction_notes")
    packs, vault = make(tmp_path, "obj", "prod_obj", [c], receipts=False)
    evidence_status.append_receipt(packs / "obj", {
        "kind": "semantic_check", "claim_id": c["claim_id"],
        "claim_digest": evidence_status.claim_digest(c), "result": "ENTAILED",
        "model": "claude-opus", "receipt_id": "r1"})
    _, decisions = auto_publish.run("obj", packs, vault)
    assert decisions[0]["decision"] == "AUTO_HELD"


def test_human_rejection_overrides_auto_approval(tmp_path):
    c = folded_claims()[0]
    c.pop("extraction_notes")
    packs, vault = make(tmp_path, "obj", "prod_obj", [c],
                        reviews=[{"claim_id": "claim_gcc", "disposition": "REJECTED_FOR_SERVING"}])
    _, decisions = auto_publish.run("obj", packs, vault)
    assert decisions[0]["decision"] == "AUTO_APPROVED"
    assert not PackEvidence("obj", packs_root=packs, vault_root=vault).eligible("claim_gcc")


def test_changed_claim_needs_a_new_decision(tmp_path):
    c = folded_claims()[0]
    c.pop("extraction_notes")
    packs, vault = make(tmp_path, "obj", "prod_obj", [c])
    auto_publish.run("obj", packs, vault)
    c["object"]["height"] = 29
    (packs / "obj" / "claims.json").write_text(json.dumps([c]))
    assert not PackEvidence("obj", packs_root=packs, vault_root=vault).eligible("claim_gcc")


def test_market_mismatch_requires_body_equivalence(tmp_path):
    c = claim("c_depth", "Trunk depth 1060 mm.", {"value": 1060, "unit": "mm",
              "measured_quantity": "trunk depth"}, subject="prod_car", app={"market": "CN"})
    packs, vault = make(tmp_path, "car", "prod_car", [c])
    _, decisions = auto_publish.run("car", packs, vault, dry_run=True)
    assert "product_match" in decisions[0]["failed_checks"]
    packs, vault = make(tmp_path / "eq", "car", "prod_car", [c],
                        identity={"market": "US", "body_equivalence": {"markets": ["CN"]}})
    _, decisions = auto_publish.run("car", packs, vault, dry_run=True)
    assert decisions[0]["decision"] == "AUTO_APPROVED"


def _fit_case(tmp_path, width_claim):
    car = [claim("t_depth", "Trunk depth 1060 mm.", {"value": 1060, "unit": "mm"}, "prod_car"),
           claim("t_top", "Floor to top 680 mm.", {"value": 680, "unit": "mm"}, "prod_car"),
           claim("t_open", "Opening 1140 mm.", {"value": 1140, "unit": "mm"}, "prod_car")]
    if width_claim:
        car.append(claim("t_width", "Floor width 940 mm.", {"value": 940, "unit": "mm"},
                         "prod_car"))
    packs, vault = make(tmp_path, "obj", "prod_obj", folded_claims())
    make(tmp_path, "car", "prod_car", car)
    src = lambda p, c, f=None: {"product_dir": p, "claim_id": c, **({"field": f} if f else {})}
    case = {"case": "t", "scope": {}, "clearance_mm": 25, "intrusion_scenarios_mm": [100],
            "object_axes": ["h", "w", "d"], "parameters": {
                "h": {"role": "object_max", "sources": [src("obj", "claim_gcc", "height"),
                                                       src("obj", "claim_target", "height"),
                                                       src("obj", "claim_amazon", "height")]},
                "w": {"role": "object_max", "sources": [src("obj", "claim_gcc", "width")]},
                "d": {"role": "object_max", "sources": [src("obj", "claim_gcc", "depth")]},
                "floor_depth": {"role": "space_min", "sources": [src("car", "t_depth")]},
                "closed_ceiling_height": {"role": "space_min", "sources": [src("car", "t_top")]},
                "aperture_min_span": {"role": "space_min", "sources": [src("car", "t_open")]},
                "floor_width_between_arches": {"role": "space_min", "sources": (
                    [src("car", "t_width")] if width_claim else [])}}}
    return packs, vault, case


def test_fit_is_only_likely_when_a_deciding_width_is_unknown(tmp_path, monkeypatch):
    packs, vault, case = _fit_case(tmp_path, width_claim=False)
    result = fit_engine.run_case(case, packs, vault)
    assert result["verdict"] == "LIKELY_FITS_UNCONFIRMED"
    rec = result["recommended"]
    assert rec["unknown_constraints"] == ["floor_width"]
    # Conservative envelope: the superseded retailer height (31 in) is used,
    # the unlabeled Amazon value is excluded.
    assert result["parameters"]["h"]["value_mm"] == round(31 * 25.4, 1)
    assert rec["axes_named"]["vertical"] == "d"
    upright = [o for o in result["orientations"] if o["axes_named"]["vertical"] == "h"]
    assert all(o["verdict"] == "DOES_NOT_FIT" for o in upright)


def test_fit_is_confirmed_when_every_constraint_is_evidenced(tmp_path, monkeypatch):
    packs, vault, case = _fit_case(tmp_path, width_claim=True)
    result = fit_engine.run_case(case, packs, vault)
    assert result["verdict"] == "FITS_CONFIRMED"
    assert result["recommended"]["sensitivity"][
        "seatback_recline_max_deg_at_zero_trim_intrusion"] > 45


def test_fit_parameters_are_discovered_from_claims_not_hand_written(tmp_path):
    packs, vault, _ = _fit_case(tmp_path, width_claim=False)
    car = json.loads((packs / "car" / "claims.json").read_text())
    for c in car:
        c["predicate"] = {"t_depth": "rear_trunk_depth", "t_top": "rear_trunk_floor_to_top",
                          "t_open": "rear_trunk_opening"}[c["claim_id"]]
    (packs / "car" / "claims.json").write_text(json.dumps(car))
    obj = json.loads((packs / "obj" / "claims.json").read_text())
    for c in obj:
        c["predicate"] = "folded_dimensions"
    (packs / "obj" / "claims.json").write_text(json.dumps(obj))
    assert fit_engine.roles("car", packs) == {"space"}
    assert fit_engine.roles("obj", packs) == {"object"}
    case = fit_engine.build_case("obj", "car", packs)
    found = {k: [s["claim_id"] for s in v["sources"]] for k, v in case["parameters"].items()}
    assert found["floor_depth"] == ["t_depth"]
    assert found["floor_width_between_arches"] == []
    assert set(found["object_folded_height"]) == {"claim_gcc", "claim_target"}
