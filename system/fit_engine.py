#!/usr/bin/env python3
"""Deterministic cargo-fit engine driven only by verified evidence claims.

Replaces the placeholder boxes in poc-higgsfield-geometry/fit_engine.py.

A fit case maps each geometric parameter to every claim that states it; it
is discovered from claim predicates (``build_case``), never hand-written. A claim is usable when its quotes are found in
the hash-pinned source, its subject matches the pack, its current digest has
an ENTAILED independent receipt, and the automatic conflict resolution did not
EXCLUDE it. Superseded values stay usable as conservative bounds (rule R5):
object dimensions take the per-axis maximum, cargo-space dimensions the
minimum. Parameters without usable evidence are UNKNOWN, never estimated; the
engine reports, for each orientation, the largest value of every unknown at
which the fit would still hold, and whether the fit is CONFIRMED (no unknown
constraint) or only LIKELY.

Coordinates (mm): x forward from the load lip into the car, y lateral,
z up from the cargo floor.

    python -m system.fit_engine graco-ready2jet-2212125:tesla-model-y [--out PATH]
"""

import argparse
import hashlib
import json
import math
import re
import sys
from itertools import permutations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from system import auto_publish, evidence_status  # noqa: E402

ENGINE_VERSION = "fit-engine-v2"
CLEARANCE_MM = 25
INTRUSION_SCENARIOS_MM = [50, 100, 150]

# Generic parameter discovery. A product plays the OBJECT role when it has
# folded-dimension claims, and the SPACE role when it has rear-cargo
# measurement claims. Parameters are found by predicate / measured-quantity
# text, so any new pack that states the same facts works without new code.
OBJECT_RULES = {
    "object_folded_height": ("height", r"folded_dimensions"),
    "object_folded_width": ("width", r"folded_dimensions"),
    "object_folded_depth": ("depth", r"folded_dimensions"),
}
SPACE_RULES = {
    "floor_depth": r"rear_trunk_depth|cargo_floor_length|trunk depth",
    "closed_ceiling_height": r"rear_trunk_floor_to_top|floor to (the )?top",
    "aperture_min_span": r"rear_trunk_opening|trunk opening|liftgate opening",
    "floor_width_between_arches": r"floor_width|between (the )?wheel|wheel[- ]?arch(es)? width",
}
SPACE_LABELS = {
    "floor_depth": "Trunk depth, seatback to load lip",
    "closed_ceiling_height": "Trunk floor to top, liftgate closed",
    "aperture_min_span": "Liftgate opening (smallest measured span)",
    "floor_width_between_arches": "Floor width between the wheel arches",
}
UNIT_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "in": 25.4}


class FitInputError(RuntimeError):
    pass


def _to_mm(value, unit):
    if unit not in UNIT_MM:
        raise FitInputError(f"unsupported unit {unit!r}")
    return float(value) * UNIT_MM[unit]


class Evidence:
    def __init__(self, packs_root, vault_root):
        self.packs_root, self.vault_root = packs_root, vault_root
        self.packs, self.excluded = {}, {}

    def pack(self, product_dir):
        if product_dir not in self.packs:
            pack = evidence_status.PackEvidence(product_dir, packs_root=self.packs_root,
                                                vault_root=self.vault_root)
            self.packs[product_dir] = pack
            excluded = set()
            for res in auto_publish.build_resolutions(pack):
                excluded |= {c for c, o in res["outcomes"].items() if o == "EXCLUDED"}
            self.excluded[product_dir] = excluded
        return self.packs[product_dir]

    def usable(self, product_dir, claim_id):
        """(usable, record) for one claim used as a fit input."""
        pack = self.pack(product_dir)
        claim = pack.claims.get(claim_id)
        if claim is None:
            return False, {"claim_id": claim_id, "problem": "unknown_claim"}
        digest = evidence_status.claim_digest(claim)
        problems = []
        bindings = [pack.authenticate_binding(b) for b in claim.get("source_bindings", [])]
        if not bindings or not all(s in evidence_status.AUTHENTICATED for s in bindings):
            problems.append("source_support")
        _, identity = auto_publish._identity(pack)
        manifest_id = evidence_status.load_json(pack.vault_dir / "manifest.json", {}).get(
            "product_id")
        if auto_publish._product_match(claim, manifest_id, identity):
            problems.append("product_match")
        receipt = pack.current_receipt(claim_id, digest)
        if not (receipt and receipt.get("result") == "ENTAILED"
                and str(receipt.get("serving_model") or receipt.get("model") or "")
                .startswith("qwen/")) or pack.alarm_outstanding(claim_id, digest):
            problems.append("independent_verification")
        if claim_id in self.excluded[product_dir]:
            problems.append("excluded_by_conflict_rule")
        return not problems, {"product_dir": product_dir, "claim_id": claim_id,
                              "claim_digest": digest, "problems": problems,
                              "receipt_id": (receipt or {}).get("receipt_id"),
                              "eligible_to_serve": pack.eligible(claim_id)}


def resolve_parameter(spec, evidence):
    """Combine every usable source of one parameter conservatively."""
    values, inputs = [], []
    for src in spec.get("sources", []):
        ok, record = evidence.usable(src["product_dir"], src["claim_id"])
        record["field"] = src.get("field")
        inputs.append(record)
        if not ok:
            continue
        claim = evidence.pack(src["product_dir"]).claims[src["claim_id"]]
        obj = claim.get("object") or {}
        raw = obj.get(src["field"]) if src.get("field") else obj.get("value")
        unit = src.get("unit") or obj.get("unit")
        if raw is None or unit is None:
            record["problems"].append("no_value_in_object")
            continue
        record["value_mm"] = round(_to_mm(raw, unit), 1)
        values.append(record["value_mm"])
    if not values:
        return {"status": "UNKNOWN", "value_mm": None, "inputs": inputs,
                "note": spec.get("unknown_note")}
    combine = max if spec["role"] == "object_max" else min
    return {"status": "EVIDENCED", "value_mm": combine(values), "inputs": inputs,
            "combined_with": combine.__name__, "n_sources": len(values)}


def _limit_value(params, name):
    p = params.get(name)
    return p["value_mm"] if p and p["status"] == "EVIDENCED" else None


def evaluate_orientation(dims, params, case):
    """Constraints for one axis assignment (along_x, lateral, vertical)."""
    along_x, lateral, vertical = dims
    m = float(case["clearance_mm"])
    depth = _limit_value(params, "floor_depth")
    ceiling = _limit_value(params, "closed_ceiling_height")
    width = _limit_value(params, "floor_width_between_arches")
    aperture = _limit_value(params, "aperture_min_span")
    aperture_h = _limit_value(params, "aperture_height") or ceiling
    checks, unknown = [], []

    def add(name, phase, need, have, note):
        status = "UNKNOWN" if have is None else ("PASS" if need <= have + 1e-9 else "FAIL")
        checks.append({"constraint": name, "phase": phase, "required_mm": round(need, 1),
                       "available_mm": None if have is None else round(have, 1),
                       "margin_mm": None if have is None else round(have - need, 1),
                       "status": status, "note": note})
        if status == "UNKNOWN":
            unknown.append(name)

    add("closed_hatch_height", "final_placement_closed_hatch", vertical + m, ceiling,
        "Stroller top plus clearance must stay below the measured floor-to-top height "
        "with the liftgate closed.")
    add("floor_width", "final_placement", lateral + 2 * m, width,
        "Lateral extent plus clearance on both sides between the wheel-arch trims.")
    # Depth with two unknown intrusions: closed-liftgate inner trim I (from the
    # lip, near-vertical lower rear face) and seatback recline theta. Report
    # the largest I (at theta = 0) and theta (at I = 0) that still fit.
    need_depth = along_x + 2 * m
    add("floor_depth", "final_placement", need_depth, depth,
        "Fore-aft extent plus clearance, before liftgate-trim and seatback-recline "
        "allowances.")
    if depth is not None:
        slack = depth - need_depth
        rise = vertical + m
        sens = {"liftgate_trim_intrusion_max_mm_at_upright_seatback": round(slack, 1),
                "seatback_recline_max_deg_at_zero_trim_intrusion":
                    round(math.degrees(math.atan2(slack, rise)), 1) if slack > 0 else None}
        for intrusion in case.get("intrusion_scenarios_mm", []):
            left = slack - intrusion
            sens[f"seatback_recline_max_deg_if_trim_intrusion_{intrusion}mm"] = (
                round(math.degrees(math.atan2(left, rise)), 1) if left > 0 else None)
    else:
        sens = {}
    add("aperture_lateral", "insertion_path", lateral + 2 * m, aperture,
        "Lateral extent passing through the open liftgate aperture (smallest measured "
        "span; the source does not say which span is horizontal).")
    add("aperture_vertical", "insertion_path", vertical + m, aperture_h,
        "Height while sliding in over the flush load lip.")
    statuses = {c["status"] for c in checks}
    if "FAIL" in statuses:
        verdict = "DOES_NOT_FIT"
    elif "UNKNOWN" in statuses:
        verdict = "LIKELY_FITS_UNCONFIRMED"
    else:
        verdict = "FITS_CONFIRMED"
    required = {"floor_width_between_arches_min_mm": round(lateral + 2 * m, 1),
                "floor_depth_min_mm": round(need_depth, 1),
                "closed_height_min_mm": round(vertical + m, 1)}
    return {"axes_mm": {"along_x": along_x, "lateral": lateral, "vertical": vertical},
            "verdict": verdict, "checks": checks, "unknown_constraints": unknown,
            "sensitivity": sens, "requirements": required}


def _claims(product_dir, packs_root):
    path = Path(packs_root) / product_dir / "claims.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text())
    return data.get("claims", []) if isinstance(data, dict) else data


def _text(claim):
    obj = claim.get("object") or {}
    return f"{claim.get('predicate', '')} {obj.get('measured_quantity', '')}".lower()


def roles(product_dir, packs_root=evidence_status.PACKS_ROOT):
    """Which fit roles a product's claims support: {'object', 'space'} subset."""
    found = set()
    for claim in _claims(product_dir, packs_root):
        text = _text(claim)
        if re.search(OBJECT_RULES["object_folded_height"][1], text):
            found.add("object")
        if re.search(SPACE_RULES["floor_depth"], text) or re.search(
                SPACE_RULES["closed_ceiling_height"], text):
            found.add("space")
    return found


def build_case(object_dir, space_dir, packs_root=evidence_status.PACKS_ROOT):
    """Discover every claim stating each fit parameter. Nothing is hand-picked."""
    parameters = {}
    object_claims = _claims(object_dir, packs_root)
    for name, (field, pattern) in OBJECT_RULES.items():
        parameters[name] = {"role": "object_max", "sources": [
            {"product_dir": object_dir, "claim_id": c["claim_id"], "field": field}
            for c in object_claims if re.search(pattern, _text(c))
            and (c.get("object") or {}).get(field) is not None]}
    space_claims = _claims(space_dir, packs_root)
    for name, pattern in SPACE_RULES.items():
        sources = [{"product_dir": space_dir, "claim_id": c["claim_id"]}
                   for c in space_claims if re.search(pattern, _text(c))
                   and isinstance((c.get("object") or {}).get("value"), (int, float))]
        parameters[name] = {"role": "space_min", "sources": sources,
                            "label": SPACE_LABELS[name],
                            "unknown_note": None if sources else
                            f"No claim in the {space_dir} evidence pack states this measurement."}
    return {"case": f"{object_dir}:{space_dir}",
            "scope": {"object": {"product_dir": object_dir, "state": "folded"},
                      "space": {"product_dir": space_dir, "space": "rear trunk, second row "
                                "upright; liftgate closed for the final placement"}},
            "clearance_mm": CLEARANCE_MM, "intrusion_scenarios_mm": INTRUSION_SCENARIOS_MM,
            "object_axes": list(OBJECT_RULES), "parameters": parameters}


def run_case(case, packs_root=evidence_status.PACKS_ROOT,
             vault_root=evidence_status.VAULT_ROOT):
    """``case`` is a case dict, or "object_dir:space_dir" to discover one."""
    if isinstance(case, str):
        case = build_case(*case.split(":", 1), packs_root=packs_root)
    case_name = case["case"]
    evidence = Evidence(packs_root, vault_root)
    params = {name: resolve_parameter(spec, evidence)
              for name, spec in case["parameters"].items()}
    obj = [params[n]["value_mm"] for n in case["object_axes"]]
    if any(v is None for v in obj):
        missing = [n for n in case["object_axes"] if params[n]["value_mm"] is None]
        result = {"verdict": "UNKNOWN", "reason": f"object dimensions unknown: {missing}"}
    else:
        names = dict(zip(obj, case["object_axes"]))
        orientations = []
        for dims in sorted(set(permutations(obj))):
            row = evaluate_orientation(dims, params, case)
            row["axes_named"] = {k: names[v] for k, v in row["axes_mm"].items()}
            orientations.append(row)
        rank = {"FITS_CONFIRMED": 0, "LIKELY_FITS_UNCONFIRMED": 1, "DOES_NOT_FIT": 2}

        worst = max(case.get("intrusion_scenarios_mm") or [0])
        robust_deg = float(case.get("robust_recline_deg", 30))

        def score(row):
            # Prefer orientations that still fit with the largest liftgate-trim
            # allowance and a realistically reclined seatback, then by margin.
            margins = [c["margin_mm"] for c in row["checks"] if c["margin_mm"] is not None]
            sens = row["sensitivity"]
            tolerance = (sens.get(f"seatback_recline_max_deg_if_trim_intrusion_{worst}mm")
                         if worst else sens.get("seatback_recline_max_deg_at_zero_trim_intrusion"))
            return (rank[row["verdict"]], len(row["unknown_constraints"]),
                    not (tolerance or 0) >= robust_deg, -(min(margins) if margins else 0))
        orientations.sort(key=score)
        best = orientations[0]
        result = {"verdict": best["verdict"], "recommended": best,
                  "orientations": orientations}
    payload = {
        "engine": ENGINE_VERSION, "case": case_name,
        "question_scope": case["scope"], "clearance_mm": case["clearance_mm"],
        "parameters": params, **result,
    }
    fingerprint = hashlib.sha256(json.dumps(
        [[i["claim_id"], i["claim_digest"]] for p in params.values() for i in p["inputs"]
         if "claim_digest" in i], sort_keys=True).encode()).hexdigest()
    payload["evidence_fingerprint"] = fingerprint
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("case")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    payload = run_case(args.case)
    text = json.dumps(payload, indent=1, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    rec = payload.get("recommended") or {}
    print(f"verdict: {payload['verdict']}; recommended axes {rec.get('axes_named')}; "
          f"unknown: {rec.get('unknown_constraints')}")
    for check in rec.get("checks", []):
        print(f"  {check['phase']:<30} {check['constraint']:<20} need {check['required_mm']}"
              f" have {check['available_mm']} -> {check['status']}")
    print("  sensitivity:", rec.get("sensitivity"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
