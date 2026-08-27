"""Validate the POC 6 Stage C evidence map, action, and folded pose."""

from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
RIG_BLEND = HERE / "ready2jet-rigged.blend"
JOINT_MAP = HERE / "joint-evidence.json"
ACTION_SPEC = HERE / "action-spec.json"
INPUT_MANIFEST = HERE.parent / "inputs" / "source-manifest.json"
OUT = HERE / "validation-stage-c.json"


def bbox(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return low, high


def pct_error(actual, target):
    return [100.0 * (actual[i] - target[i]) / target[i] for i in range(3)]


def main():
    errors = []
    evidence = json.loads(JOINT_MAP.read_text())
    spec = json.loads(ACTION_SPEC.read_text())
    manifest = json.loads(INPUT_MANIFEST.read_text())

    required_joint_fields = {"joint", "object", "type", "axis", "range", "evidence", "confidence"}
    for index, joint in enumerate(evidence.get("joints", [])):
        missing = sorted(required_joint_fields - joint.keys())
        if missing:
            errors.append(f"joint {index} missing {missing}")
        if joint.get("confidence") not in {"DOCUMENTED", "INFERRED"}:
            errors.append(f"joint {joint.get('joint')} has invalid confidence")
        if not joint.get("evidence"):
            errors.append(f"joint {joint.get('joint')} has no evidence")
    if len(evidence.get("joints", [])) < 13:
        errors.append("joint evidence map has fewer than 13 mapped motions/states")
    if not evidence.get("inferred_inventory"):
        errors.append("INFERRED inventory is empty")

    bpy.ops.wm.open_mainfile(filepath=str(RIG_BLEND))
    scene = bpy.context.scene
    rig = bpy.data.objects.get("RigRoot")
    if not rig:
        errors.append("RigRoot missing")
        raise SystemExit(errors)
    if scene.get("internal_only") is not True:
        errors.append("scene is not marked internal_only")
    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        errors.append("license status changed")

    expected_props = {
        "stage_prepare", "stage_thumb_switch", "stage_handle_lever", "stage_auto_fold", "stage_secure",
        "defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch", "effective_latch_state",
    }
    missing_props = sorted(prop for prop in expected_props if prop not in rig)
    if missing_props:
        errors.append(f"missing rig properties: {missing_props}")

    action = bpy.data.actions.get(spec.get("action"))
    curve_paths = set()
    if not action:
        errors.append("named fold action missing")
    else:
        for layer in action.layers:
            for strip in layer.strips:
                for channelbag in strip.channelbags:
                    curve_paths.update(fcurve.data_path for fcurve in channelbag.fcurves)
    for prop in ("stage_prepare", "stage_thumb_switch", "stage_handle_lever", "stage_auto_fold", "stage_secure"):
        if f'["{prop}"]' not in curve_paths:
            errors.append(f"action curve missing {prop}")

    expected_stage_order = ["stage_prepare", "stage_thumb_switch", "stage_handle_lever", "stage_auto_fold", "stage_secure"]
    actual_stage_order = sorted(spec.get("stage_parameters", {}), key=lambda key: spec["stage_parameters"][key]["frames"][0])
    if actual_stage_order != expected_stage_order:
        errors.append(f"stage order is {actual_stage_order}")

    geometry = [
        obj for obj in bpy.data.collections["TWIN_GEOMETRY"].objects
        if obj.type == "MESH" and not obj.hide_render
    ]
    frame_checks = {}
    for frame in (1, 48, 66, 84, 96):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        low, high = bbox(geometry)
        frame_checks[str(frame)] = {
            "stage_auto_fold": float(rig["stage_auto_fold"]),
            "bbox_m_DWH": list(high - low),
            "minimum_z_m": low.z,
        }
        if low.z < -0.005:
            errors.append(f"frame {frame} penetrates the ground plane: z={low.z:.4f}")

    if not math.isclose(frame_checks["66"]["stage_auto_fold"], 0.5, abs_tol=1e-6):
        errors.append("fold parameter does not scrub continuously at frame 66")

    scene.frame_set(96)
    bpy.context.view_layer.update()
    wheel_gap = (bpy.data.objects["Wheel_FL"].matrix_world.translation - bpy.data.objects["Wheel_RL"].matrix_world.translation).length
    if wheel_gap > 0.05:
        errors.append(f"front/rear wheel centers do not cluster: {wheel_gap:.4f} m")
    open_dims = frame_checks["1"]["bbox_m_DWH"]
    folded_dims = frame_checks["96"]["bbox_m_DWH"]
    if folded_dims[0] >= open_dims[0] or folded_dims[2] >= 0.9 * open_dims[2]:
        errors.append("folded envelope did not contract in depth and height")

    rig["defect_skip_latch"] = 1.0
    rig.update_tag()
    scene.frame_set(95)
    scene.frame_set(96)
    bpy.context.view_layer.update()
    skipped_latch_state = float(rig["effective_latch_state"])
    if skipped_latch_state != 0.0:
        errors.append("skipped-latch defect parameter did not suppress latch state")
    rig["defect_skip_latch"] = 0.0

    rig["defect_reverse_direction"] = 1.0
    rig.update_tag()
    scene.frame_set(83)
    scene.frame_set(84)
    bpy.context.view_layer.update()
    reverse_front_angle_deg = math.degrees(bpy.data.objects["FrontFrame_ROOT"].rotation_euler.y)
    if reverse_front_angle_deg < 60.0:
        errors.append("reverse-direction defect parameter did not reverse the front-frame hinge")
    rig["defect_reverse_direction"] = 0.0

    dims = manifest["verified_dimensions"]
    target_open = [dims["open_cm"]["D"] / 100, dims["open_cm"]["W"] / 100, dims["open_cm"]["H"] / 100]
    target_folded = [dims["folded_cm"]["D"] / 100, dims["folded_cm"]["W"] / 100, dims["folded_cm"]["H"] / 100]
    result = {
        "status": "PASS" if not errors else "FAIL",
        "blender_version": bpy.app.version_string,
        "joint_count": len(evidence.get("joints", [])),
        "inferred_joint_count": sum(joint.get("confidence") == "INFERRED" for joint in evidence.get("joints", [])),
        "action": spec.get("action"),
        "stage_order": actual_stage_order,
        "frame_checks": frame_checks,
        "wheel_center_cluster_gap_m": wheel_gap,
        "target_open_dimensions_m_DWH": target_open,
        "open_dimension_error_percent_DWH": pct_error(open_dims, target_open),
        "target_folded_dimensions_m_DWH": target_folded,
        "folded_dimension_confidence": dims["folded_cm"]["confidence"],
        "folded_dimension_error_percent_DWH": pct_error(folded_dims, target_folded),
        "defect_parameter_checks": {
            "skip_latch_effective_state": skipped_latch_state,
            "reverse_direction_front_angle_deg": reverse_front_angle_deg,
        },
        "external_spend_usd": 0,
        "internal_only": True,
        "errors": errors,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
