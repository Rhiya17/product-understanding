"""Fail-closed validator for the five-lane photo-projection work order."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: str | Path):
    return json.loads((ROOT / path).read_text())


def visible_watermark(path: Path) -> bool:
    with Image.open(path) as image:
        image.seek(0)
        rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)[:48, :700]
    red = (rgb[:, :, 0] > 180) & (rgb[:, :, 1] < 130) & (rgb[:, :, 2] < 110)
    return int(red.sum()) >= 500


def validate_registry(slug: str, expected_ids: set[str], errors: list[str]) -> None:
    registry = load(f"evidence-packs/{slug}/derived-assets.json")
    by_id = {asset["asset_id"]: asset for asset in registry["assets"]}
    for asset_id in expected_ids:
        if asset_id not in by_id:
            errors.append(f"missing registered asset {asset_id}")
            continue
        asset = by_id[asset_id]
        path = ROOT / asset["local_path"]
        if not path.exists() or sha256(path) != asset["sha256"]:
            errors.append(f"{asset_id}: file/hash mismatch")
        if asset.get("approved_by") is not None or asset.get("internal_only") is not True:
            errors.append(f"{asset_id}: approval/internal-only guard failed")
        if asset.get("external_spend_usd") != 0:
            errors.append(f"{asset_id}: external spend is not zero")
        if asset.get("tripo_texture_ancestry") is not False:
            errors.append(f"{asset_id}: unexpected Tripo texture ancestry")
        if asset.get("camera_gate", {}).get("minimum_iou", 0) < 0.75:
            errors.append(f"{asset_id}: camera gate below threshold")
        if not visible_watermark(path):
            errors.append(f"{asset_id}: visible watermark check failed")


def main() -> None:
    errors = []
    baseline = load("poc-3d-static-twin/photo-projection/protected-baseline.json")
    for relative, expected in baseline["sha256"].items():
        path = ROOT / relative
        if not path.exists() or sha256(path) != expected:
            errors.append(f"protected file changed: {relative}")

    ready = load("poc-3d-static-twin/photo-projection/ready2jet/verdict.json")
    if ready["verdict"] != "SKIPPED_CAMERA_MATCH_GATE" or any(
        score >= 0.75 for score in ready["final_camera_matches"].values()
    ):
        errors.append("Lane 1 verdict/gate mismatch")
    if (ROOT / "evidence-packs/graco-ready2jet-2212125/derived-assets.json").exists():
        errors.append("Lane 1 unexpectedly registered an asset")

    validate_registry("levoit-core-300s", {"derived_levoit_levoit_turntable_20260827"}, errors)
    validate_registry("apple-macbook-air-13-m3", {
        "derived_macbook_closed_macbook_closed_turntable_20260827",
        "derived_macbook_open_macbook_open_turntable_20260827",
    }, errors)

    bose = load("poc-3d-static-twin/photo-projection/bose/verdict.json")
    bose_registry = load("evidence-packs/bose-qc-ultra-headphones/derived-assets.json")
    interim = next((asset for asset in bose_registry["assets"]
                    if asset["asset_id"] == "derived_bose_tripo_h31_turntable_20260827"), None)
    if bose["verdict"] != "SKIPPED_PROJECTED_TWIN_RETAIN_TRIPO_INTERIM" or not interim:
        errors.append("Lane 4 interim verdict/asset missing")
    elif interim.get("tripo_ancestry") is not True or interim.get("worst_axis_scale_error_percent") != 147.0:
        errors.append("Lane 4 interim ancestry/scale label missing")

    snugride = load("poc-3d-static-twin/photo-projection/snugride/audit.json")
    if snugride["verdict"] != "AUDIT_SKIP_NO_TWIN_SERVE_OFFICIAL_MEDIA":
        errors.append("Lane 5 audit verdict missing")
    if snugride["inventory_summary"] != {
        "official_images": 12, "person_free_images": 3,
        "clean_distinct_semantic_views": 1, "person_free_side_or_rear_views": 0,
    }:
        errors.append("Lane 5 inventory summary changed")

    for lane in ("ready2jet", "levoit", "macbook", "bose", "snugride"):
        hours = load(f"poc-3d-static-twin/photo-projection/{lane}/hours.json")
        if hours.get("external_spend_usd") != 0 or "hours" not in hours:
            errors.append(f"{lane}: hours/spend log invalid")

    blend_validation = load("poc-3d-static-twin/photo-projection/validation-blends.json")
    if blend_validation.get("status") != "PASS":
        errors.append("Blender scene validation failed")

    result = {"status": "PASS" if not errors else "FAIL", "lanes_with_terminal_outcomes": 5,
              "registered_new_assets": 3, "external_spend_usd": 0, "errors": errors}
    (HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
