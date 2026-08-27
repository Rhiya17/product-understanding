"""Render deterministic internal-only POC 6 turntable and fold videos."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
SOURCE_BLEND = HERE / "ready2jet-rigged.blend"
RENDERS = HERE / "renders"
VERIFICATION_FRAMES = HERE / "verification" / "rendered-official-frames"
FRAME_ROOT = Path("/tmp/poc6-articulated-twin-frames")


def aim(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def linearize(action):
    if not action:
        return
    for layer in action.layers:
        for strip in layer.strips:
            for channelbag in strip.channelbags:
                for fcurve in channelbag.fcurves:
                    for point in fcurve.keyframe_points:
                        point.interpolation = "LINEAR"


def new_camera(name):
    data = bpy.data.cameras.new(name)
    camera = bpy.data.objects.new(name, data)
    bpy.data.collections["QA_ONLY"].objects.link(camera)
    data.lens = 58
    bpy.context.scene.camera = camera
    return camera


def setup_scene():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_file_extension = True
    scene["internal_only"] = True
    scene["external_publication_forbidden"] = True
    scene["render_script"] = "render_twin.py"
    scene["deterministic_render_seed"] = 0
    RENDERS.mkdir(parents=True, exist_ok=True)
    VERIFICATION_FRAMES.mkdir(parents=True, exist_ok=True)
    return scene, bpy.data.objects["RigRoot"]


def render_sequence(scene, stem):
    scene.render.image_settings.file_format = "PNG"
    frame_dir = FRAME_ROOT / stem
    frame_dir.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(frame_dir / "frame-")
    bpy.ops.render.render(animation=True)
    frames = sorted(frame_dir.glob("frame-*.png"))
    expected = scene.frame_end - scene.frame_start + 1
    if len(frames) != expected:
        raise SystemExit(f"render sequence incomplete: {len(frames)} of {expected} frames in {frame_dir}")
    print(f"rendered {len(frames)} frames to {frame_dir}")


def render_turntable(scene, rig):
    saved_action = rig.animation_data.action if rig.animation_data else None
    rig.animation_data.action = None
    for prop in ("stage_prepare", "stage_thumb_switch", "stage_handle_lever", "stage_auto_fold", "stage_secure"):
        rig[prop] = 0.0
    rig.update_tag()

    target = bpy.data.objects.new("Turntable_Target", None)
    orbit = bpy.data.objects.new("Turntable_Orbit", None)
    bpy.data.collections["QA_ONLY"].objects.link(target)
    bpy.data.collections["QA_ONLY"].objects.link(orbit)
    target.location = (0.0, 0.0, 0.52)
    orbit.location = target.location
    camera = new_camera("Turntable_Camera")
    camera.parent = orbit
    camera.location = (0.0, -2.35, 0.18)
    track = camera.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    for frame in range(1, 73):
        orbit.rotation_euler.z = 2 * math.pi * (frame - 1) / 72
        orbit.keyframe_insert("rotation_euler", index=2, frame=frame)
    linearize(orbit.animation_data.action)
    scene.frame_start = 1
    scene.frame_end = 72
    render_sequence(scene, "open-turntable")
    rig.animation_data.action = saved_action


def setup_fold_camera(scene, name, location, target):
    camera = new_camera(name)
    aim(camera, location, target)
    scene.frame_start = 1
    scene.frame_end = 96
    return camera


def render_official(scene, rig):
    setup_fold_camera(scene, "OfficialAngle_Camera", (-1.45, -1.42, 1.08), (0.03, 0.0, 0.48))
    scene["camera_evidence"] = "Approximate fixed front-left three-quarter angle of official fold video frames 1166-1206"
    render_sequence(scene, "fold-official-angle")

    scene.render.image_settings.file_format = "PNG"
    for frame in (48, 57, 66, 75, 84):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        scene.render.filepath = str(VERIFICATION_FRAMES / f"render-{frame:04d}.png")
        bpy.ops.render.render(write_still=True)


def render_novel(scene, rig):
    setup_fold_camera(scene, "NovelRearRight_Camera", (1.72, 1.65, 1.25), (0.08, 0.0, 0.46))
    scene["camera_evidence"] = "Fixed rear-right three-quarter diagnostic angle absent from the official fixed-camera video"
    render_sequence(scene, "fold-novel-rear-right")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=("turntable", "official", "novel", "all"), default="all")
    script_args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(script_args)
    targets = ("turntable", "official", "novel") if args.target == "all" else (args.target,)
    for target in targets:
        scene, rig = setup_scene()
        if target == "turntable":
            render_turntable(scene, rig)
        elif target == "official":
            render_official(scene, rig)
        else:
            render_novel(scene, rig)


if __name__ == "__main__":
    main()
