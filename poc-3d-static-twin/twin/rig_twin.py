"""Stage C: evidence-map and parameterize the Ready2Jet fold rig."""

from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
SOURCE_BLEND = HERE / "ready2jet-stage-b.blend"
OUT_BLEND = HERE / "ready2jet-rigged.blend"
ACTION_SPEC = HERE / "action-spec.json"
QA_DIR = HERE / "stage-c-qa"


def parent_keep_world(obj, parent):
    bpy.context.view_layer.update()
    matrix = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = matrix
    bpy.context.view_layer.update()


def add_prop(obj, name, value=0.0, description=""):
    obj[name] = value
    obj.id_properties_ui(name).update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, description=description)


def driver(obj, data_path, index, expression, variables):
    fcurve = obj.driver_add(data_path, index) if index is not None else obj.driver_add(data_path)
    drv = fcurve.driver
    drv.type = "SCRIPTED"
    drv.expression = expression
    for name, source, source_path in variables:
        var = drv.variables.new()
        var.name = name
        var.type = "SINGLE_PROP"
        target = var.targets[0]
        target.id = source
        target.data_path = source_path
    return fcurve


def key_property(rig, prop, keys):
    for frame, value in keys:
        # Keep the ID property floating-point. Assigning a bare 0/1 changes an
        # ID property to integer and makes Blender evaluate the F-curve as a
        # midpoint step even when its keyframes say LINEAR.
        rig[prop] = float(value)
        rig.keyframe_insert(data_path=f'["{prop}"]', frame=frame, group="Fold stages")


def set_linear(action):
    # Blender 5.2 stores keyframes in layered Action channel bags.
    for layer in action.layers:
        for strip in layer.strips:
            for channelbag in strip.channelbags:
                for fcurve in channelbag.fcurves:
                    for point in fcurve.keyframe_points:
                        point.interpolation = "LINEAR"


def aim(cam, location, target):
    cam.location = location
    cam.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def render(path):
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    if not SOURCE_BLEND.exists():
        raise SystemExit(f"missing Stage B blend: {SOURCE_BLEND}")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    QA_DIR.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    rig = bpy.data.objects["RigRoot"]
    front = bpy.data.objects["FrontFrame_ROOT"]
    lower = bpy.data.objects["LowerHandle_ROOT"]
    upper = bpy.data.objects["UpperHandle_ROOT"]
    seat = bpy.data.objects["SeatUnit_ROOT"]
    canopy = bpy.data.objects["Canopy_ROOT"]
    belly = bpy.data.objects["BellyBar_ROOT"]
    cup = bpy.data.objects["CupHolder_ROOT"]
    basket = bpy.data.objects["Basket_INFERRED"]
    caster_l = bpy.data.objects["Wheel_FL"]
    caster_r = bpy.data.objects["Wheel_FR"]
    thumb = bpy.data.objects["ThumbSwitch"]
    lever = bpy.data.objects["SqueezeLever"]

    # Kinematic hierarchy: upper handle follows lower handle; canopy and belly
    # bar follow the inferred seat unit; cup holder follows the handle frame.
    parent_keep_world(upper, lower)
    parent_keep_world(canopy, seat)
    parent_keep_world(belly, seat)
    parent_keep_world(cup, lower)

    for name, description in (
        ("stage_prepare", "Fold canopy, rotate cup holder, align front casters"),
        ("stage_thumb_switch", "Slide thumb switch per claim_r2j_step_fold_4"),
        ("stage_handle_lever", "Squeeze handle lever per claim_r2j_step_fold_5"),
        ("stage_auto_fold", "Patent/video-backed automatic fold motion"),
        ("stage_secure", "Final folded latch/check state"),
        ("defect_reverse_direction", "Render-time defect: reverse fold rotations"),
        ("defect_skip_handle_release", "Render-time defect: suppress visible lever release while fold proceeds"),
        ("defect_skip_latch", "Render-time defect: folded motion completes without secure latch state"),
        ("effective_latch_state", "Computed postcondition after optional skipped-latch defect"),
    ):
        add_prop(rig, name, 0.0, description)

    common_fold_vars = [
        ("fold", rig, '["stage_auto_fold"]'),
        ("reverse", rig, '["defect_reverse_direction"]'),
    ]
    driver(front, "rotation_euler", 1, f"{math.radians(-65)}*fold*(1-2*reverse)", common_fold_vars)
    driver(rig, "location", 2, "0.075*sin(pi*fold)", [("fold", rig, '["stage_auto_fold"]')])
    driver(lower, "rotation_euler", 1, f"{math.radians(60)}*fold*(1-2*reverse)", common_fold_vars)
    driver(upper, "rotation_euler", 1, f"{math.radians(-78)}*fold*(1-2*reverse)", common_fold_vars)
    driver(seat, "rotation_euler", 1, f"{math.radians(-22)}*fold*(1-2*reverse)", common_fold_vars)
    driver(seat, "location", 0, "-0.01+0.15*fold", [("fold", rig, '["stage_auto_fold"]')])
    driver(seat, "location", 2, "0.53-0.15*fold", [("fold", rig, '["stage_auto_fold"]')])
    driver(canopy, "rotation_euler", 1, f"{math.radians(35)}*prep", [("prep", rig, '["stage_prepare"]')])
    # The evidence shows the soft canopy collapsing but does not expose its
    # internal bows. A root-scale envelope makes that approximation explicit
    # and parameterized instead of inventing hidden linkage geometry.
    driver(canopy, "scale", 0, "1-0.75*prep", [("prep", rig, '["stage_prepare"]')])
    driver(canopy, "scale", 2, "1-0.65*prep", [("prep", rig, '["stage_prepare"]')])
    driver(cup, "rotation_euler", 0, f"{math.radians(-90)}*prep", [("prep", rig, '["stage_prepare"]')])
    driver(basket, "scale", 0, "1-0.55*fold", [("fold", rig, '["stage_auto_fold"]')])
    driver(caster_l, "rotation_euler", 2, f"{math.radians(90)}*prep", [("prep", rig, '["stage_prepare"]')])
    driver(caster_r, "rotation_euler", 2, f"{math.radians(-90)}*prep", [("prep", rig, '["stage_prepare"]')])

    thumb_base_y = thumb.location.y
    lever_base_z = lever.location.z
    driver(thumb, "location", 1, f"{thumb_base_y}+0.025*slide", [("slide", rig, '["stage_thumb_switch"]')])
    driver(
        lever,
        "location",
        2,
        f"{lever_base_z}-0.018*squeeze*(1-skip)",
        [
            ("squeeze", rig, '["stage_handle_lever"]'),
            ("skip", rig, '["defect_skip_handle_release"]'),
        ],
    )
    driver(
        rig,
        '["effective_latch_state"]',
        None,
        "secure*(1-skip)",
        [
            ("secure", rig, '["stage_secure"]'),
            ("skip", rig, '["defect_skip_latch"]'),
        ],
    )

    rig.animation_data_create()
    action = bpy.data.actions.new("Ready2Jet_Fold_Correct")
    action.use_fake_user = True
    rig.animation_data.action = action
    key_property(rig, "stage_prepare", [(1, 0), (24, 1), (96, 1)])
    key_property(rig, "stage_thumb_switch", [(1, 0), (24, 0), (36, 1), (96, 1)])
    key_property(rig, "stage_handle_lever", [(1, 0), (36, 0), (48, 1), (96, 1)])
    key_property(rig, "stage_auto_fold", [(1, 0), (48, 0), (84, 1), (96, 1)])
    key_property(rig, "stage_secure", [(1, 0), (84, 0), (96, 1)])
    set_linear(action)

    markers = {
        1: "claim_fold_1_2_preconditions",
        2: "claim_fold_3_canopy",
        24: "claim_fold_4_thumb_switch",
        36: "claim_fold_5_handle_lever",
        48: "automatic_fold_begins",
        84: "claim_fold_6_check_secure",
        96: "fold_complete",
    }
    for frame, name in markers.items():
        scene.timeline_markers.new(name, frame=frame)
    scene.frame_start = 1
    scene.frame_end = 96
    scene.render.fps = 24
    scene["stage"] = "C rigged"
    scene["joint_evidence"] = "joint-evidence.json"
    scene["correct_action"] = action.name
    scene["defect_parameters"] = "defect_reverse_direction, defect_skip_handle_release, defect_skip_latch"

    action_spec = {
        "action": action.name,
        "frame_start": 1,
        "frame_end": 96,
        "fps": 24,
        "stage_parameters": {
            "stage_prepare": {"frames": [1, 24], "claims": ["claim_r2j_step_fold_3", "claim_r2j_step_fold_tips_1", "claim_r2j_step_fold_tips_2"]},
            "stage_thumb_switch": {"frames": [24, 36], "claims": ["claim_r2j_step_fold_4"]},
            "stage_handle_lever": {"frames": [36, 48], "claims": ["claim_r2j_step_fold_5"]},
            "stage_auto_fold": {"frames": [48, 84], "evidence": ["US20220169297A1 figs 11A-11F", "video frames 1166-1193"]},
            "stage_secure": {"frames": [84, 96], "claims": ["claim_r2j_step_fold_6"]}
        },
        "preconditions": ["claim_r2j_step_fold_1", "claim_r2j_step_fold_2"],
        "postcondition": "claim_r2j_step_fold_7 belly bar remains available as carry handle",
        "defect_parameters": {
            "defect_reverse_direction": "0 correct; 1 reverses all principal fold rotations",
            "defect_skip_handle_release": "0 correct; 1 suppresses visible squeeze-lever travel while automatic motion continues",
            "defect_skip_latch": "0 correct; 1 forces effective_latch_state to 0 after the fold"
        }
    }
    ACTION_SPEC.write_text(json.dumps(action_spec, indent=2) + "\n")

    # Deterministic Stage C pose QA using the saved Stage B camera/lights.
    cam = bpy.data.objects["QA_Camera"]
    cam.data.type = "PERSP"
    cam.data.lens = 58
    aim(cam, (-1.35, -1.25, 1.15), (0, 0, 0.48))
    scene.render.resolution_x = scene.render.resolution_y = 768
    for frame, name in ((1, "open"), (66, "mid-fold"), (96, "folded")):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        render(QA_DIR / f"{name}.png")

    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    print(f"saved {OUT_BLEND} with action {action.name}")


if __name__ == "__main__":
    main()
