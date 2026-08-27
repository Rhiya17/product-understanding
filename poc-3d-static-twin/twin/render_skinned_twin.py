"""Render the internal-only Stage S skinned fold from two fixed cameras.

The scene is opened read-only for each target.  The existing RigRoot action
and defect controls are the sole animation source.  Source PNG sequences are
written to /tmp and encoded separately; the five official-angle comparison
poses are persisted for the evidence contact sheet.

Usage:
  Blender --background --python render_skinned_twin.py -- --preview
  Blender --background --python render_skinned_twin.py -- --target official
  Blender --background --python render_skinned_twin.py -- --target all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
SOURCE_BLEND = HERE / "ready2jet-skinned.blend"
FRAME_ROOT = Path("/tmp/product-understanding-stage-s-frames")
VERIFICATION_FRAMES = HERE / "verification" / "skinned-rendered-official-frames"
PREVIEW_DIR = HERE / "stage-s-qa" / "previews"
RIGHTS_NOTE = "INTERNAL ONLY — TRIPO3D LICENSE CHECK OPEN — DO NOT SHIP"


def aim(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def new_camera(name, location, target):
    data = bpy.data.cameras.new(name)
    data.lens = 58
    camera = bpy.data.objects.new(name, data)
    (bpy.data.collections.get("QA_ONLY") or bpy.context.scene.collection).objects.link(camera)
    aim(camera, location, target)
    bpy.context.scene.camera = camera
    return camera


def setup_scene():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    scene = bpy.context.scene
    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        raise SystemExit("license guard changed; refusing to render")
    if scene.get("motion_authority") != "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged":
        raise SystemExit("motion authority changed; refusing to render")
    rig = bpy.data.objects["RigRoot"]
    for prop in ("defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch"):
        rig[prop] = 0.0
    rig.update_tag()
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_file_extension = True
    scene.render.film_transparent = False
    scene.render.use_stamp = True
    scene.render.use_stamp_note = True
    scene.render.stamp_note_text = RIGHTS_NOTE
    scene.render.stamp_font_size = 18
    scene.render.stamp_foreground = (1.0, 0.3, 0.18, 1.0)
    scene.render.stamp_background = (0.02, 0.02, 0.02, 0.78)
    for prop in (
        "use_stamp_time", "use_stamp_date", "use_stamp_frame", "use_stamp_frame_range",
        "use_stamp_camera", "use_stamp_lens", "use_stamp_scene", "use_stamp_filename",
        "use_stamp_marker", "use_stamp_memory", "use_stamp_hostname", "use_stamp_render_time",
    ):
        if hasattr(scene.render, prop):
            setattr(scene.render, prop, False)
    scene.frame_start = 1
    scene.frame_end = 96
    scene["render_script"] = "render_skinned_twin.py"
    scene["render_rights_note"] = RIGHTS_NOTE
    return scene


def render_sequence(scene, stem):
    frame_dir = FRAME_ROOT / stem
    frame_dir.mkdir(parents=True, exist_ok=True)
    # Refuse to silently mix old and new frame sets.
    for old_frame in frame_dir.glob("frame-*.png"):
        old_frame.unlink()
    scene.render.filepath = str(frame_dir / "frame-")
    bpy.ops.render.render(animation=True)
    frames = sorted(frame_dir.glob("frame-*.png"))
    if len(frames) != 96:
        raise SystemExit(f"{stem}: rendered {len(frames)} of 96 frames")
    print(f"rendered {len(frames)} frames to {frame_dir}")


def setup_official(scene):
    new_camera("Skinned_OfficialAngle_Camera", (-1.45, -1.42, 1.08), (0.03, 0.0, 0.48))
    scene["camera_evidence"] = "Approximate fixed front-left three-quarter angle of official fold video frames 1166-1206"


def setup_novel(scene):
    new_camera("Skinned_NovelRearRight_Camera", (1.72, 1.65, 1.25), (0.08, 0.0, 0.46))
    scene["camera_evidence"] = "Fixed rear-right three-quarter diagnostic angle absent from the official fixed-camera video"


def render_official(scene):
    setup_official(scene)
    render_sequence(scene, "skinned-fold-official-angle")
    VERIFICATION_FRAMES.mkdir(parents=True, exist_ok=True)
    for frame in (48, 57, 66, 75, 84):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        scene.render.filepath = str(VERIFICATION_FRAMES / f"render-{frame:04d}.png")
        bpy.ops.render.render(write_still=True)


def render_novel(scene):
    setup_novel(scene)
    render_sequence(scene, "skinned-fold-novel-rear-right")


def render_preview():
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for camera_name, setup in (("official", setup_official), ("novel", setup_novel)):
        scene = setup_scene()
        setup(scene)
        for frame in (1, 66, 96):
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            scene.render.filepath = str(PREVIEW_DIR / f"{camera_name}-{frame:04d}.png")
            bpy.ops.render.render(write_still=True)
    print(f"rendered Stage S previews to {PREVIEW_DIR}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=("official", "novel", "all"), default="all")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if args.preview:
        render_preview()
        return
    targets = ("official", "novel") if args.target == "all" else (args.target,)
    for target in targets:
        scene = setup_scene()
        if target == "official":
            render_official(scene)
        else:
            render_novel(scene)


if __name__ == "__main__":
    main()
