"""Validate Stage S motion equivalence and binding invariants.

The validator compares every armature bone with its source object across all
96 frames for the official action and each of the three defect scenarios.
It records full relative joint-angle traces and enforces the work-order
tolerance of 1e-4 rad.  Translation and scale are checked as additional
guards for the seat, canopy, basket, and whole-rig channels.

Usage:
  Blender --background --python validate_skin_motion.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import bpy


HERE = Path(__file__).resolve().parent
BLEND = HERE / "ready2jet-skinned.blend"
SOURCE_RIG = HERE / "ready2jet-rigged.blend"
SKIN_REPORT = HERE / "skinning-report.json"
OUT = HERE / "validation-stage-s.json"
TRACES = HERE / "motion-traces-stage-s.json"
ARMATURE = "Ready2Jet_SkinArmature_INTERNAL_ONLY"
SKIN = "Ready2Jet_PhotoSkin_INTERNAL_ONLY"
ANGLE_TOLERANCE_RAD = 1e-4
TRANSLATION_TOLERANCE_M = 1e-5
SCALE_TOLERANCE = 1e-5
RIGHTS_NOTE = "Tripo3D license check OPEN — do not ship"


SCENARIOS = {
    "correct": {},
    "defect_reverse_direction": {"defect_reverse_direction": 1.0},
    "defect_skip_handle_release": {"defect_skip_handle_release": 1.0},
    "defect_skip_latch": {"defect_skip_latch": 1.0},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scale_error(a, b) -> float:
    return max(abs(float(a[index]) - float(b[index])) for index in range(3))


def main() -> None:
    errors: list[str] = []
    if not BLEND.exists() or not SKIN_REPORT.exists():
        raise SystemExit("Stage S build artifacts are missing")
    build = json.loads(SKIN_REPORT.read_text())
    if sha256(SOURCE_RIG) != build.get("source_rig_sha256"):
        errors.append("source rig changed after binding")

    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    scene = bpy.context.scene
    rig = bpy.data.objects.get("RigRoot")
    armature = bpy.data.objects.get(ARMATURE)
    skin = bpy.data.objects.get(SKIN)
    if rig is None or armature is None or skin is None:
        raise SystemExit("RigRoot, Stage S armature, or Stage S skin is missing")

    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        errors.append("scene license guard changed")
    if scene.get("rights_note") != RIGHTS_NOTE:
        errors.append("scene rights note missing or changed")
    if scene.get("internal_only") is not True or scene.get("external_publication_forbidden") is not True:
        errors.append("scene internal-only publication guards missing")
    if scene.get("motion_authority") != "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged":
        errors.append("motion authority marker missing or changed")
    if build.get("approved_by") is not None:
        errors.append("agent approval is forbidden")

    action = bpy.data.actions.get("Ready2Jet_Fold_Correct")
    if action is None or not rig.animation_data or rig.animation_data.action != action:
        errors.append("Ready2Jet_Fold_Correct is not active on RigRoot")

    bone_targets = build["bone_targets"]
    missing_bones = sorted(set(bone_targets) - set(armature.pose.bones.keys()))
    missing_targets = sorted(target for target in bone_targets.values() if target not in bpy.data.objects)
    if missing_bones:
        errors.append(f"armature bones missing: {missing_bones}")
    if missing_targets:
        errors.append(f"motion-source objects missing: {missing_targets}")

    proxy_visible = sorted(
        obj.name for obj in bpy.data.collections["TWIN_GEOMETRY"].objects
        if obj.type == "MESH" and not obj.hide_render
    )
    if proxy_visible:
        errors.append(f"proxy geometry visible in Stage S renders: {proxy_visible}")
    if skin.hide_render:
        errors.append("photo-derived skin is hidden from renders")
    armature_modifiers = [modifier for modifier in skin.modifiers if modifier.type == "ARMATURE"]
    if len(armature_modifiers) != 1 or armature_modifiers[0].object != armature:
        errors.append("skin must have exactly one modifier targeting the Stage S armature")

    weight_sum_error = 0.0
    unweighted_vertices = []
    for vertex in skin.data.vertices:
        total = sum(group.weight for group in vertex.groups)
        weight_sum_error = max(weight_sum_error, abs(total - 1.0))
        if total == 0.0:
            unweighted_vertices.append(vertex.index)
    if unweighted_vertices:
        errors.append(f"{len(unweighted_vertices)} scan vertices are unweighted")
    if weight_sum_error > 1e-5:
        errors.append(f"vertex weights do not normalize to 1 (max error {weight_sum_error})")

    frame_start = int(scene.frame_start)
    frame_end = int(scene.frame_end)
    traces = {
        "schema_version": 1,
        "angle_units": "radians",
        "tolerance_rad": ANGLE_TOLERANCE_RAD,
        "frame_start": frame_start,
        "frame_end": frame_end,
        "scenarios": {},
    }
    global_max_angle = 0.0
    global_max_translation = 0.0
    global_max_scale = 0.0
    global_worst = None
    latch_max_error = 0.0
    latch_worst = None

    defect_names = ("defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch")
    for scenario_name, active_defects in SCENARIOS.items():
        for prop in defect_names:
            rig[prop] = float(active_defects.get(prop, 0.0))
        rig.update_tag()
        # Force a dependency-graph transition before sampling.  Re-setting an
        # ID property while parked on the same frame can otherwise leave a
        # downstream custom-property driver cached until the next frame.
        scene.frame_set(frame_start + 1)
        scene.frame_set(frame_start)
        bpy.context.view_layer.update()
        scenario_traces = {bone: [] for bone in bone_targets}

        for frame in range(frame_start, frame_end + 1):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            for bone_name, target_name in bone_targets.items():
                pose_bone = armature.pose.bones[bone_name]
                target = bpy.data.objects[target_name]
                bone_world = armature.matrix_world @ pose_bone.matrix
                target_world = target.matrix_world

                if pose_bone.parent:
                    bone_parent_world = armature.matrix_world @ pose_bone.parent.matrix
                    bone_relative = bone_parent_world.inverted_safe() @ bone_world
                else:
                    bone_relative = armature.matrix_world.inverted_safe() @ bone_world
                if target.parent:
                    target_relative = target.parent.matrix_world.inverted_safe() @ target_world
                else:
                    target_relative = target_world

                bone_rotation = bone_relative.to_quaternion()
                target_rotation = target_relative.to_quaternion()
                angle_error = target_rotation.rotation_difference(bone_rotation).angle
                translation_error = (target_relative.translation - bone_relative.translation).length
                current_scale_error = scale_error(target_relative.to_scale(), bone_relative.to_scale())
                global_max_angle = max(global_max_angle, angle_error)
                global_max_translation = max(global_max_translation, translation_error)
                global_max_scale = max(global_max_scale, current_scale_error)
                if global_worst is None or angle_error > global_worst["angle_error_rad"]:
                    global_worst = {
                        "scenario": scenario_name,
                        "frame": frame,
                        "bone": bone_name,
                        "target": target_name,
                        "angle_error_rad": angle_error,
                    }
                scenario_traces[bone_name].append({
                    "frame": frame,
                    "object_relative_angle_rad": target_rotation.angle,
                    "armature_relative_angle_rad": bone_rotation.angle,
                    "angle_error_rad": angle_error,
                })

            # effective_latch_state is itself a driver over an action-driven
            # custom property.  Blender's headless dependency graph can expose
            # the previous frame for that two-driver chain during monotonic
            # scrubbing, so evaluate the sampled frame from its predecessor as
            # Stage C's endpoint validator does.
            if frame > frame_start:
                scene.frame_set(frame - 1)
                scene.frame_set(frame)
                bpy.context.view_layer.update()
            current_latch_error = abs(float(rig["effective_latch_state"]) - float(armature["effective_latch_state"]))
            if current_latch_error > latch_max_error:
                latch_max_error = current_latch_error
                latch_worst = {
                    "scenario": scenario_name,
                    "frame": frame,
                    "rig_state": float(rig["effective_latch_state"]),
                    "armature_state": float(armature["effective_latch_state"]),
                    "error": current_latch_error,
                }
        traces["scenarios"][scenario_name] = scenario_traces

    for prop in defect_names:
        rig[prop] = 0.0
    scene.frame_set(1)
    bpy.context.view_layer.update()

    if global_max_angle > ANGLE_TOLERANCE_RAD:
        errors.append(f"armature/object joint-angle trace error {global_max_angle:.9g} rad exceeds {ANGLE_TOLERANCE_RAD}")
    if global_max_translation > TRANSLATION_TOLERANCE_M:
        errors.append(f"armature/object relative translation error {global_max_translation:.9g} m exceeds {TRANSLATION_TOLERANCE_M}")
    if global_max_scale > SCALE_TOLERANCE:
        errors.append(f"armature/object relative scale error {global_max_scale:.9g} exceeds {SCALE_TOLERANCE}")
    if latch_max_error > 1e-6:
        errors.append(f"latch-state driver mismatch {latch_max_error:.9g}")

    status = "PASS" if not errors else "FAIL"
    traces["status"] = status
    traces["max_angle_error_rad"] = global_max_angle
    TRACES.write_text(json.dumps(traces, indent=2) + "\n")
    result = {
        "status": status,
        "blender_version": bpy.app.version_string,
        "action": "Ready2Jet_Fold_Correct",
        "scenarios": list(SCENARIOS),
        "frames_checked_per_scenario": frame_end - frame_start + 1,
        "bone_count": len(bone_targets),
        "joint_angle_tolerance_rad": ANGLE_TOLERANCE_RAD,
        "max_joint_angle_error_rad": global_max_angle,
        "max_relative_translation_error_m": global_max_translation,
        "max_relative_scale_error": global_max_scale,
        "max_latch_state_error": latch_max_error,
        "worst_latch_sample": latch_worst,
        "worst_angle_sample": global_worst,
        "weight_sum_max_error": weight_sum_error,
        "unweighted_vertex_count": len(unweighted_vertices),
        "full_trace_file": TRACES.name,
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
        "external_spend_usd": 0,
        "errors": errors,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
