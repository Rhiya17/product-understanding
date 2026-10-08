"""Cargo-fit answers ("Will the Ready2Jet fit in my Tesla Model Y trunk?").

The verdict comes only from system/fit_engine.py, which reads verified claims.
Every number shown is a served (eligible) claim with its source quote; the
placement instructions are computed from those claims and labelled as such.
A fit is called confirmed only when the engine found no unknown constraint.
"""

import re

from system import fit_engine

FIT_WORDS = re.compile(r"\b(fit|fits|fitting|room|space|go in|goes in|load)\b", re.I)
CARGO_WORDS = re.compile(r"\b(trunk|boot|cargo|hatch|back of (my|the) car)\b", re.I)
PROCEDURE_PREFIX = "fit_"
STEP_IDS = ("fit_step_fold", "fit_step_open", "fit_step_place", "fit_step_close")
VIDEO_VERDICTS = {"FITS_CONFIRMED", "LIKELY_FITS_UNCONFIRMED"}
_cache = {}


def procedure_id(space_dir):
    return f"{PROCEDURE_PREFIX}{space_dir.replace('-', '_')}_trunk"


def is_fit_procedure(procedure):
    return str(procedure or "").startswith(PROCEDURE_PREFIX)


def fit_pair(question, product_dirs, packs_root=None):
    """(object_dir, space_dir) when the question asks whether one named product
    fits in another's cargo space, decided from each pack's claims."""
    if not (FIT_WORDS.search(question or "") and CARGO_WORDS.search(question or "")):
        return None
    kwargs = {"packs_root": packs_root} if packs_root else {}
    dirs = [d for d in dict.fromkeys(product_dirs) if d]
    objects = [d for d in dirs if "object" in fit_engine.roles(d, **kwargs)]
    spaces = [d for d in dirs if "space" in fit_engine.roles(d, **kwargs)]
    if len(objects) == 1 and len(spaces) == 1 and objects[0] != spaces[0]:
        return objects[0], spaces[0]
    return None


def is_fit_question(question, detected, packs_root=None):
    pair = fit_pair(question, detected, packs_root)
    return (*pair, f"{pair[0]}:{pair[1]}") if pair else None


def result_for(object_dir, space_dir, packs_root, vault_root, fingerprint=None):
    key = (object_dir, space_dir, str(packs_root), fingerprint)
    if fingerprint is None or key not in _cache:
        if fingerprint is not None:
            _cache.clear()
        result = fit_engine.run_case(f"{object_dir}:{space_dir}", packs_root=packs_root,
                                     vault_root=vault_root)
        if fingerprint is None:
            return result
        _cache[key] = result
    return _cache[key]


def _result(case, engine):
    object_dir, space_dir = case.split(":", 1)
    return result_for(object_dir, space_dir, engine.packs_root, engine.vault_root,
                      engine._fingerprint())


def _cm(mm):
    return f"{mm / 10:.0f} cm ({mm / 25.4:.1f} in)"


MEASUREMENT_LABELS = {
    "claim_tmy_tp12365_depth": "Trunk depth",
    "claim_tmy_tpd1ev_depth": "Trunk depth",
    "claim_tmy_tp12365_floor_to_top_repair_20261007": "Trunk floor to top, straight up",
    "claim_tmy_tp12365_floor_to_top": "Trunk floor to top, straight up",
    "claim_tmy_tp12365_opening_length": "Liftgate opening, first span (axis not stated by the source)",
    "claim_tmy_tp12365_opening_width": "Liftgate opening, second span (axis not stated by the source)",
}
MEASURERS = {"12365auto": "tape-measured by 12365auto (车质网) on a 2025 Model Y Long Range AWD",
             "d1ev": "measured by a 第一电动网 (d1ev) reviewer on a 2025 refreshed Model Y"}


def _measurement_text(claim):
    label = MEASUREMENT_LABELS.get(claim["claim_id"])
    obj = claim.get("object") or {}
    if not label or "value" not in obj:
        return None
    who = next((v for k, v in MEASURERS.items() if k in claim["claim_id"].replace("tp", "")
                or k in str((claim.get("applicability") or {}).get("revision", ""))), "")
    return f"{label}: {obj['value']:g} {obj['unit']}" + (f", {who}." if who else ".")


def _served_inputs(result, names):
    seen, out = set(), []
    for name in names:
        for item in result["parameters"].get(name, {}).get("inputs", []):
            key = (item["product_dir"], item["claim_id"])
            if item.get("eligible_to_serve") and key not in seen:
                seen.add(key)
                out.append(key)
    return out


def answer(doc, engine, obj_dir, space_dir, case):
    products = engine.products()
    obj, space = products[obj_dir], products[space_dir]
    result = _result(case, engine)
    verdict = result["verdict"]
    rec = result.get("recommended") or {}
    doc.set_product(obj)
    doc.headline = f"{obj.name} in a {space.name} trunk"
    if verdict == "UNKNOWN" or not rec:
        doc.add_gap(obj, doc.intent, detail=(
            "We can't answer this yet: the measurements it depends on haven't passed "
            "verification."))
        return doc
    checks = {c["constraint"]: c for c in rec["checks"]}
    axes = rec["axes_mm"]
    long_side, short_side, thickness = axes["lateral"], axes["along_x"], axes["vertical"]
    standing = next((o for o in result["orientations"]
                     if o["axes_named"]["vertical"] == "stroller_folded_height"), None)
    unknown = rec["unknown_constraints"]
    need_width = rec["requirements"]["floor_width_between_arches_min_mm"]
    if verdict == "FITS_CONFIRMED":
        doc.direct = (f"Yes. Folded and laid flat, the {obj.name} fits in the {space.name} "
                      "trunk with the liftgate closed, with room to spare on every measured "
                      "dimension.")
        status_text = "Confirmed by every measurement it depends on."
    elif verdict == "LIKELY_FITS_UNCONFIRMED":
        doc.direct = (
            f"Very likely, but not confirmed. Folded and laid flat with its long side across "
            f"the car, the {obj.name} clears every measured {space.name} trunk dimension "
            f"with room to spare, including with the liftgate closed. One measurement it "
            f"depends on, the floor width between the wheel arches (it needs at least "
            f"{_cm(need_width)}), has not been verified for the current Model Y.")
        status_text = "Not confirmed: one deciding measurement is unverified."
    else:
        doc.direct = (f"No. Folded, the {obj.name} does not fit in the {space.name} trunk "
                      "in any orientation with the liftgate closed.")
        status_text = "Does not fit."
    verdict_items = [{"text": status_text, "claim_id": None, "derived": True,
                      "verdict": verdict, "source_refs": []}]
    for constraint, label in (("closed_hatch_height", "Height with the liftgate closed"),
                              ("floor_depth", "Floor depth, seatback to load lip"),
                              ("aperture_lateral", "Through the open liftgate"),
                              ("floor_width", "Floor width between the wheel arches")):
        check = checks.get(constraint)
        if not check:
            continue
        if check["status"] == "UNKNOWN":
            text = (f"{label}: needs {_cm(check['required_mm'])}; no verified measurement "
                    "for the current Model Y.")
        else:
            text = (f"{label}: needs {_cm(check['required_mm'])}, has "
                    f"{_cm(check['available_mm'])} ({check['status'].lower()}, "
                    f"{_cm(check['margin_mm'])} to spare).")
        verdict_items.append({"text": text, "claim_id": None, "derived": True,
                              "check": check, "source_refs": []})
    doc.blocks.append({"kind": "fit_check", "primary": True, "title": "Fit check",
                       "items": verdict_items})
    place = [
        f"Fold the stroller completely. Folded it is up to about {_cm(long_side)} by "
        f"{_cm(short_side)} by {_cm(thickness)} (sources differ slightly; the fit check "
        "uses the largest figure for each side).",
        "Open the liftgate fully.",
        "Lay the folded stroller flat, with its long side running across the car.",
        "Slide it in over the flush load lip and push it forward against the rear seatbacks.",
        "Close the liftgate.",
    ]
    if standing and standing["verdict"] == "DOES_NOT_FIT":
        ceiling = next(c for c in standing["checks"] if c["constraint"] == "closed_hatch_height")
        place.append(f"Don't stand it upright: it is about {_cm(ceiling['required_mm'] - result['clearance_mm'])} "
                     f"tall, more than the {_cm(ceiling['available_mm'])} floor-to-top height "
                     "with the liftgate closed.")
    # Placement items carry the same step ids as the video brief, so a fit
    # video's chapters line up with these rows.
    step_ids = [STEP_IDS[0], STEP_IDS[1], STEP_IDS[2], STEP_IDS[2], STEP_IDS[3], None]
    doc.blocks.append({"kind": "subprocedure", "primary": False, "title": "How to place it",
                       "derived": True,
                       "items": [{"text": t, "claim_id": step_ids[i] if i < len(step_ids) else None,
                                  "derived": True, "source_refs": []}
                                 for i, t in enumerate(place)]})
    measured = {}
    for product_dir, claim_id in _served_inputs(result, list(result["parameters"])):
        product = products[product_dir]
        claim = product.claims[claim_id]
        measured.setdefault(product_dir, []).append(
            doc._item(product, claim, _measurement_text(claim)))
        doc.context.setdefault("claim_ids", []).append(claim_id)
    for product_dir, items in measured.items():
        doc.blocks.append({"kind": "fact", "primary": False,
                           "title": f"Measurements used · {products[product_dir].name}",
                           "items": items})
    warnings = []
    for claim in space.claims.values():
        text = " ".join(str(v) for v in (claim.get("object") or {}).values()).lower()
        if claim.get("type") == "WARNING" and space.eligible(claim["claim_id"]) and re.search(
                r"liftgate|trunk|cargo|load", text):
            warnings.append(doc._item(space, claim))
    if warnings:
        doc.blocks.append({"kind": "warnings", "title": "Safety", "primary": False,
                           "items": warnings[:6]})
    if unknown:
        notes = {"floor_width": (
            "No verifiable measurement of the 2025+ Model Y's floor width between the wheel "
            "arches exists in our sources. A 2020–24 Model Y measured 94 cm there (image "
            "only), and a 2025 review says the cargo space is essentially unchanged, but "
            "neither counts as a verified measurement of the current car.")}
        doc.gap = {"reason": "unverified_dimension",
                   "message": " ".join(notes.get(u, f"{u} is not verified.") for u in unknown),
                   "unknown_constraints": unknown}
        doc.blocks.insert(1, {"kind": "notes", "primary": False, "title": "Not yet verified",
                              "items": [{"text": doc.gap["message"], "claim_id": None,
                                         "derived": True, "source_refs": []}]})
    sens = rec.get("sensitivity") or {}
    doc.coverage = {"procedure_id": procedure_id(space.dir), "required_steps": [],
                    "missing_steps": [],
                    "complete": verdict == "FITS_CONFIRMED",
                    "fit": {"engine": result["engine"], "verdict": verdict,
                            "evidence_fingerprint": result["evidence_fingerprint"],
                            "sensitivity": sens,
                            "scope": result["question_scope"]}}
    doc.context.update({"product_dir": obj.dir, "procedure_id": procedure_id(space.dir),
                        "secondary_product": space.dir})
    doc.partial = verdict != "FITS_CONFIRMED"
    return doc
