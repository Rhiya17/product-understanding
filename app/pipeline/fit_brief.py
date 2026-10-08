"""Turn a verified fit calculation into an authoring brief for the video pipeline.

Nothing here is written for one question. The fit engine discovers the
evidence for whichever object/space pair the job names, decides orientation
and clearances, and this module turns that result into:

- ``steps``: the same shape the worker gives procedure videos, with stable
  ids (fit_step_*) that the critic reviews and the answer's chapters use;
- ``scene``: the brief Astra builds to (dimensions, orientation, placement,
  evidence references, what is unverified and how to disclose it);
- ``checks``: the trusted geometry spec the sandboxed runner enforces.

A video is only made for FITS_CONFIRMED or LIKELY_FITS_UNCONFIRMED. Unknown
dimensions get a clearly labelled illustrative size equal to the minimum
the fit needs plus clearance; they are never presented as measured.
"""
import json
import re

from app.pipeline.store import REPO_ROOT
from system import evidence_status, fit_answer, fit_engine

OBJECT_PREFIX = "STROLLER_"
COLLIDERS = {"floor": "FIT_FLOOR", "seatback": "FIT_SEATBACK", "liftgate": "FIT_LIFTGATE",
             "side_left": "FIT_SIDE_L", "side_right": "FIT_SIDE_R", "ceiling": "FIT_CEILING"}
# Ordered: earlier patterns are better references for the fit scene.
PHOTO_HINTS = {"object": [r"folded.*standing|self-standing", r"folded", r"fold"],
               "space": [r"trunk-open|open.*trunk", r"liftgate|cargo", r"trunk", r"rear"]}
MAX_PHOTOS = 4


class FitBriefError(RuntimeError):
    """The fit cannot be shown honestly; the customer keeps the written answer."""


def space_for_procedure(procedure_id):
    catalog = json.loads((REPO_ROOT / "source-vault" / "catalog.json").read_text())
    for product in catalog["products"]:
        if fit_answer.procedure_id(product["dir"]) == procedure_id:
            return product["dir"]
    raise FitBriefError("This fit question no longer matches a catalog product.")


def _name(product_dir):
    catalog = json.loads((REPO_ROOT / "source-vault" / "catalog.json").read_text())
    for product in catalog["products"]:
        if product["dir"] == product_dir:
            return f"{product.get('brand', '')} {product.get('model', '')}".strip()
    return product_dir


def _photos(product_dir, role):
    manifest = json.loads((REPO_ROOT / "source-vault" / product_dir / "manifest.json").read_text())
    scored = []
    exterior = []
    for index, source in enumerate(manifest.get("sources", [])):
        path = str(source.get("local_path") or "")
        if source.get("type") != "IMAGE" or not path:
            continue
        flags = f"{source.get('rights_note', '')} {source.get('notes', '')}".lower()
        if re.search(r"contains (a person|people)", flags):
            continue  # provider likeness filters; also not product geometry
        if str(source.get("authority", "")).upper().startswith("MANUFACTURER") is False:
            continue
        rank = next((i for i, pattern in enumerate(PHOTO_HINTS[role])
                     if re.search(pattern, path, re.I)), len(PHOTO_HINTS[role]))
        scored.append((rank, index, source["source_id"]))
        if re.search(r"studio-front|liftgate-open-front", path, re.I):
            exterior.append(source["source_id"])
    ranked = [sid for _, _, sid in sorted(scored)]
    if role == "space" and exterior:
        # Interior close-ups alone cannot establish a recognisable vehicle body.
        selected = ranked[:2] + exterior[:2]
        if product_dir == "tesla-model-y":
            user_ref = "src_user_red_trunk_reference_20261007"
            if any(item["source_id"] == user_ref for item in manifest.get("sources", [])):
                selected = [user_ref, *ranked[:1], *exterior[:2]]
        return list(dict.fromkeys(selected + ranked))[:MAX_PHOTOS]
    return ranked[:MAX_PHOTOS]


def _evidence(result, products):
    """Every served input claim with its quote, grouped by parameter."""
    out = {}
    for name, param in result["parameters"].items():
        items = []
        for item in param["inputs"]:
            if not item.get("eligible_to_serve"):
                continue
            pack = products[item["product_dir"]]
            claim = pack.claims[item["claim_id"]]
            items.append({"claim_id": item["claim_id"], "product_dir": item["product_dir"],
                          "value_mm": item.get("value_mm"),
                          "quotes": [b.get("quote") for b in claim.get("source_bindings", [])],
                          "measured_vehicle": (claim.get("object") or {}).get("measured_vehicle")})
        out[name] = {"status": param["status"], "value_mm": param["value_mm"], "claims": items,
                     "note": param.get("note")}
    return out


def build(object_dir, space_dir, packs_root=None, vault_root=None):
    packs_root = packs_root or REPO_ROOT / "evidence-packs"
    vault_root = vault_root or REPO_ROOT / "source-vault"
    result = fit_engine.run_case(f"{object_dir}:{space_dir}", packs_root=packs_root,
                                 vault_root=vault_root)
    verdict = result["verdict"]
    if verdict not in fit_answer.VIDEO_VERDICTS:
        raise FitBriefError({
            "DOES_NOT_FIT": "The verified measurements show it does not fit, so there is no "
                            "placement to demonstrate.",
            "UNKNOWN": "The measurements this depends on are not verified, so a video "
                       "would have to invent them."}.get(verdict, "The fit is undecided."))
    rec = result["recommended"]
    axes = rec["axes_mm"]
    margin = result["clearance_mm"]
    products = {d: evidence_status.PackEvidence(d, packs_root=packs_root, vault_root=vault_root)
                for d in (object_dir, space_dir)}
    evidence = _evidence(result, products)
    space = {}
    for name in fit_engine.SPACE_RULES:
        param = result["parameters"][name]
        if param["status"] == "EVIDENCED":
            space[name] = {"value_mm": param["value_mm"], "status": "EVIDENCED"}
    unknown = {}
    needs = rec["requirements"]
    if "floor_width" in rec["unknown_constraints"]:
        unknown["floor_width_between_arches"] = {
            "status": "UNVERIFIED",
            "illustrative_mm": round(needs["floor_width_between_arches_min_mm"] + 2 * margin),
            "disclose": "The floor width between the wheel arches is not verified for this "
                        "vehicle; it is drawn at an illustrative width, not a measurement."}
    object_name, space_name = _name(object_dir), _name(space_dir)
    open_steps = [c for c in products[space_dir].claims.values()
                  if c.get("type") == "STEP" and products[space_dir].eligible(c["claim_id"])
                  and re.search(r"open", str((c.get("object") or {}).get("procedure", "")))
                  and re.search(r"liftgate|trunk", json.dumps(c.get("object")), re.I)]
    used = {k: [c["claim_id"] for c in v["claims"]] for k, v in evidence.items()}
    object_ids = sorted({c for k in fit_engine.OBJECT_RULES for c in used[k]})
    steps = [
        {"claim_id": fit_answer.STEP_IDS[0], "parts": [],
         "text": f"Show the {object_name} fully folded, standing behind the {space_name}'s "
                 f"open trunk. Folded size used: {axes['lateral']:.0f} x {axes['along_x']:.0f} x "
                 f"{axes['vertical']:.0f} mm.",
         "quote": " | ".join(q for c in evidence["object_folded_height"]["claims"]
                             for q in c["quotes"]),
         "evidence_claim_ids": object_ids, "manual_pages": []},
        {"claim_id": fit_answer.STEP_IDS[1], "parts": [],
         "text": f"The {space_name} liftgate is fully open.",
         "quote": " | ".join(b.get("quote", "") for c in open_steps[:1]
                             for b in c.get("source_bindings", [])),
         "evidence_claim_ids": [c["claim_id"] for c in open_steps[:1]], "manual_pages": []},
        {"claim_id": fit_answer.STEP_IDS[2], "parts": [],
         "text": (f"Lift the folded {object_name}, lay it flat and slide it in over the load lip: "
                  f"its {axes['lateral']:.0f} mm side runs across the car, "
                  f"{axes['along_x']:.0f} mm front-to-back, {axes['vertical']:.0f} mm tall. "
                  f"It comes to rest on the floor against the rear seatbacks, centred, with at "
                  f"least {margin} mm clear of every surface."),
         "quote": "", "evidence_claim_ids": sorted({c for v in used.values() for c in v}),
         "manual_pages": []},
        {"claim_id": fit_answer.STEP_IDS[3], "parts": [],
         "text": (f"Close the liftgate fully. The stroller stays clear: its top is "
                  f"{axes['vertical']:.0f} mm against a {space.get('closed_ceiling_height', {}).get('value_mm', 0):.0f} mm "
                  f"floor-to-top height."),
         "quote": "", "evidence_claim_ids": used.get("closed_ceiling_height", []),
         "manual_pages": []},
    ]
    scene = {
        "kind": "cargo_fit", "verdict": verdict, "engine": result["engine"],
        "evidence_fingerprint": result["evidence_fingerprint"],
        "units": "mm in this brief; build the scene in meters",
        "frame": "+Z up. +X points from the load lip into the car toward the rear seats. "
                 "The load lip's inner edge is at x=0; the cargo floor top is the reference "
                 "height (it is flush with the lip).",
        "object": {"product_dir": object_dir, "name": object_name, "state": "folded",
                   "envelope_mm": {"along_x": axes["along_x"], "lateral": axes["lateral"],
                                   "vertical": axes["vertical"]},
                   "orientation": rec["axes_named"],
                   "required_object_prefix": OBJECT_PREFIX},
        "space": {"product_dir": space_dir, "name": space_name,
                  "measured": space, "unverified": unknown,
                  "scope": result["question_scope"]},
        "placement": {"rest_on": "floor", "against": "rear seatbacks", "lateral": "centred",
                      "clearance_mm": margin,
                      "sensitivity": rec["sensitivity"]},
        "required_colliders": COLLIDERS,
        "collider_rules": ("Model each collider as a closed mesh with the given name: FIT_FLOOR "
                           "spans exactly from the load lip (x=0) to the seatback base at the "
                           "measured floor depth; FIT_CEILING is the closed floor-to-top limit "
                           "(parcel shelf/headliner underside) at exactly the measured height "
                           "above the floor top; FIT_SEATBACK is the rear seatbacks; FIT_SIDE_L "
                           "and FIT_SIDE_R are the side trims/wheel arches; FIT_LIFTGATE is the "
                           "liftgate, animated from open to fully closed by the last frame. "
                           f"Every visible mesh of the {object_name} is named with the "
                           f"prefix {OBJECT_PREFIX}."),
        "disclosure": [u["disclose"] for u in unknown.values()]
                      + ([] if verdict == "FITS_CONFIRMED" else
                         ["The fit is not confirmed by every measurement; show it as an "
                          "illustration of the calculated placement, not as proof."]),
        "evidence": evidence,
        "reference_photo_ids": {object_dir: _photos(object_dir, "object"),
                                space_dir: _photos(space_dir, "space")},
    }
    if space_dir == "tesla-model-y":
        scene["appearance_requirements"] = {
            "exterior_paint": "red, not blue",
            "interior": "Match the user trunk photo: dark charcoal carpet, flat continuous cargo floor, dark side trim and wheel arches, upright seatbacks at the far forward end; no seat cushion in the cargo bay.",
            "reference_scope": "User photo is an appearance reference only; its model year and trim are unverified. Preserve verified dimensions and their existing uncertainty. Do not derive measurements from this photo.",
            "visibility": "Light the dark cargo bay so the folded stroller stays distinct. Use opaque high-contrast dimension labels. Avoid tinted transparent bodywork washing out the stroller.",
        }
    checks = {
        "object_prefix": OBJECT_PREFIX, "colliders": COLLIDERS,
        "object_envelope_m": [axes["along_x"] / 1000, axes["lateral"] / 1000,
                              axes["vertical"] / 1000],
        "object_tolerance": 0.06, "space_tolerance": 0.02,
        "space_targets_m": {k: v["value_mm"] / 1000 for k, v in space.items()
                            if k in ("floor_depth", "closed_ceiling_height")},
        "clearance_m": margin / 1000,
    }
    label = (f"{object_name} in a {space_name} trunk · 3D fit demonstration (Astra + Blender)")
    caveat = ("3D illustration of a placement calculated from verified measurements; geometry "
              "and clearances were checked automatically.")
    if verdict != "FITS_CONFIRMED":
        caveat += " Not confirmed: " + " ".join(u["disclose"] for u in unknown.values())
    return {"steps": steps, "scene": scene, "checks": checks, "product_name": object_name,
            "label": label, "caveat": caveat, "result": result}
