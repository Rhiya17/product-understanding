"""Blender-side validation of registered photo-projected geometry scenes."""

from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CASES = [
    {
        "name": "levoit",
        "blend": HERE / "levoit/levoit-photo-projected.blend",
        "claim_ids": ["claim_c300s_spec_dimensions"],
        "dimensions": (0.22098, 0.22098, 0.36068),
    },
    {
        "name": "macbook-closed",
        "blend": HERE / "macbook/closed/macbook-closed-photo-projected.blend",
        "claim_ids": ["claim_mba_spec_height", "claim_mba_spec_depth", "claim_mba_spec_width"],
        "dimensions": (0.3041, 0.215, 0.0113),
    },
    {
        "name": "macbook-open",
        "blend": HERE / "macbook/open/macbook-open-photo-projected.blend",
        "claim_ids": ["claim_mba_spec_height", "claim_mba_spec_depth", "claim_mba_spec_width"],
        "base_dimensions": (0.3041, 0.215, 0.0113 * 0.52),
    },
]


def bbox(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return high - low


def close(actual, expected, tolerance=2e-5):
    return all(math.isclose(a, e, abs_tol=tolerance) for a, e in zip(actual, expected))


def main() -> None:
    errors = []
    results = {}
    for case in CASES:
        bpy.ops.wm.open_mainfile(filepath=str(case["blend"]))
        scene = bpy.context.scene
        collection = bpy.data.collections.get("PRODUCT_GEOMETRY")
        geometry = [obj for obj in collection.all_objects if obj.type == "MESH" and not obj.hide_render]
        if scene.get("internal_only") is not True:
            errors.append(f"{case['name']}: internal_only missing")
        if scene.get("external_spend_usd") != 0.0:
            errors.append(f"{case['name']}: external spend changed")
        if scene.get("tripo_texture_ancestry") is not False:
            errors.append(f"{case['name']}: Tripo texture ancestry flag changed")
        if json.loads(scene.get("geometry_claim_ids", "[]")) != case["claim_ids"]:
            errors.append(f"{case['name']}: claim metadata mismatch")
        if case.get("dimensions"):
            actual = tuple(bbox(geometry))
            if not close(actual, case["dimensions"]):
                errors.append(f"{case['name']}: dimensions {actual} != {case['dimensions']}")
        else:
            base = bpy.data.objects.get("BaseSlab")
            actual = tuple(base.dimensions)
            if not close(actual, case["base_dimensions"]):
                errors.append(f"{case['name']}: base dimensions {actual} != {case['base_dimensions']}")
        cameras = [obj for obj in scene.objects if obj.type == "CAMERA" and obj.name.startswith("Projection_")]
        if not cameras or any(float(camera.get("camera_match_iou", 0)) < 0.75 for camera in cameras):
            errors.append(f"{case['name']}: projection camera without passing IoU")
        photo_materials = [material for material in bpy.data.materials if material.name.startswith("PHOTO_")]
        if not photo_materials:
            errors.append(f"{case['name']}: no photo material")
        if any(material.get("appearance_pixels") != "official source image RGB only" for material in photo_materials):
            errors.append(f"{case['name']}: material appearance policy mismatch")
        results[case["name"]] = {
            "geometry_objects": len(geometry),
            "projection_cameras": len(cameras),
            "photo_materials": len(photo_materials),
        }
    output = {"status": "PASS" if not errors else "FAIL", "blender_version": bpy.app.version_string,
              "results": results, "errors": errors}
    (HERE / "validation-blends.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
