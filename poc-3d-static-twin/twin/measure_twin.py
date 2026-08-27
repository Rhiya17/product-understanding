"""Measure open and folded POC 6 envelopes in the rigged Blender scene."""

from __future__ import annotations

import json
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
BLEND = HERE / "ready2jet-rigged.blend"
MANIFEST = HERE.parent / "inputs" / "source-manifest.json"
OUT = HERE / "verification" / "dimension-check.json"


def world_bbox(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return low, high


def error(actual, target):
    return [100 * (actual[index] - target[index]) / target[index] for index in range(3)]


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    scene = bpy.context.scene
    objects = [
        obj for obj in bpy.data.collections["TWIN_GEOMETRY"].objects
        if obj.type == "MESH" and not obj.hide_render
    ]
    measured = {}
    for state, frame in (("open", 1), ("folded", 96)):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        low, high = world_bbox(objects)
        measured[state] = {"frame": frame, "bbox_min_xyz_m": list(low), "bbox_max_xyz_m": list(high), "dimensions_m_DWH": list(high - low)}

    manifest = json.loads(MANIFEST.read_text())
    dims = manifest["verified_dimensions"]
    open_target = [dims["open_cm"]["D"] / 100, dims["open_cm"]["W"] / 100, dims["open_cm"]["H"] / 100]
    folded_target = [dims["folded_cm"]["D"] / 100, dims["folded_cm"]["W"] / 100, dims["folded_cm"]["H"] / 100]
    result = {
        "axis_order": "DWH = Blender XYZ",
        "open": {**measured["open"], "target_m_DWH": open_target, "error_percent_DWH": error(measured["open"]["dimensions_m_DWH"], open_target), "target_confidence": "OFFICIAL"},
        "folded": {**measured["folded"], "target_m_DWH": folded_target, "error_percent_DWH": error(measured["folded"]["dimensions_m_DWH"], folded_target), "target_confidence": dims["folded_cm"]["confidence"], "target_method": dims["folded_cm"]["method"]},
        "external_spend_usd": 0,
        "internal_only": True,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
