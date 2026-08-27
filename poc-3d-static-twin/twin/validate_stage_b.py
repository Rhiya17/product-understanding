"""Headless validator for the saved Stage B Blender artifact.

Usage:
  Blender --background ready2jet-stage-b.blend --python validate_stage_b.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
OUT = HERE / "validation-stage-b.json"
TARGET = Vector((0.6858, 0.5207, 1.0922))


def bbox(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH" or obj.hide_render:
            continue
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return lo, hi


def main():
    required = {
        "FrontLeg108_L", "FrontLeg108_R", "RearLeg110_L", "RearLeg110_R",
        "HandleGrip", "ThumbSwitch", "SqueezeLever", "SeatBack",
        "CanopyFabric", "Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR",
        "Basket_INFERRED", "BellyBarGrip", "CupHolder_INFERRED",
    }
    names = set(bpy.data.objects.keys())
    missing = sorted(required - names)
    geometry = bpy.data.collections.get("TWIN_GEOMETRY")
    reference = bpy.data.objects.get("REFERENCE_TripoProbe01_DO_NOT_RENDER")
    checks = {
        "required_parts_present": not missing,
        "geometry_collection_present": geometry is not None,
        "reference_present_and_hidden": bool(reference and reference.hide_render and reference.hide_viewport),
        "internal_only_scene_flag": bpy.context.scene.get("internal_only") is True,
        "open_license_scene_flag": bpy.context.scene.get("license_status") == "Tripo3D OPEN - DO NOT SHIP",
        "scaffold_run_id": bpy.context.scene.get("scaffold_run_id") == "tripo-probe-01",
        "scaffold_pack_hash": bpy.context.scene.get("scaffold_pack_hash") == "da454173c3733e0227d90f869925145897669e96df8f7c593f0f45be94d8a83f",
        "four_wheel_roots": all(bpy.data.objects.get(name) for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR")),
        "three_spokes_per_wheel": all(
            sum(1 for suffix in (1, 2, 3) if bpy.data.objects.get(f"{name}_Spoke{suffix}")) == 3
            for name in ("Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR")
        ),
    }
    dimensions = None
    error = None
    if geometry:
        lo, hi = bbox(list(geometry.objects))
        dimensions = hi - lo
        error = Vector(100 * (dimensions[i] - TARGET[i]) / TARGET[i] for i in range(3))
        checks["open_dimensions_within_5_percent"] = all(abs(value) <= 5 for value in error)
        checks["inferred_objects_labeled"] = all(
            obj.get("confidence") == "INFERRED"
            for obj in geometry.objects
            if "INFERRED" in obj.name or obj.name in {"SeatBack", "SeatBase", "CalfSupport", "CanopyFabric"}
        )
    result = {
        "blend": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "checks": checks,
        "missing_required_objects": missing,
        "dimensions_m_DWH": list(dimensions) if dimensions else None,
        "dimension_error_percent_DWH": list(error) if error else None,
        "passed": all(checks.values()),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
