"""Render the POC 7 defect_reverse_direction negative-control sequence in Blender."""

from __future__ import annotations

import hashlib
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE_BLEND = REPO / "poc-3d-static-twin" / "twin" / "ready2jet-rigged.blend"
EXPECTED_BLEND_SHA256 = "83d80dc107d46edecbe89d4d97dabf726887012dd4c0917f8da8e2961a9dc79d"
FRAME_DIR = Path("/tmp/poc7-defect-reverse-direction-frames")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aim(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def main() -> None:
    if sha256_of(SOURCE_BLEND) != EXPECTED_BLEND_SHA256:
        raise SystemExit("source blend hash changed; refusing to render the defect control")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    scene = bpy.context.scene
    rig = bpy.data.objects["RigRoot"]
    required = {"defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch"}
    missing = sorted(required - set(rig.keys()))
    if missing:
        raise SystemExit(f"rig is missing declared defect parameters: {missing}")
    rig["defect_reverse_direction"] = 1.0
    rig["defect_skip_handle_release"] = 0.0
    rig["defect_skip_latch"] = 0.0
    rig.update_tag()

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
    scene.frame_start = 1
    scene.frame_end = 96
    scene["internal_only"] = True
    scene["external_publication_forbidden"] = True
    scene["motion_authority"] = "ready2jet-rigged.blend / defect_reverse_direction=1.0"
    scene["render_script"] = "poc-wanvace-control-video/render_defect_control.py"

    data = bpy.data.cameras.new("POC7_Defect_OfficialAngle_Camera")
    camera = bpy.data.objects.new("POC7_Defect_OfficialAngle_Camera", data)
    (bpy.data.collections.get("QA_ONLY") or scene.collection).objects.link(camera)
    data.lens = 58
    aim(camera, (-1.45, -1.42, 1.08), (0.03, 0.0, 0.48))
    scene.camera = camera
    scene["camera_evidence"] = "same fixed official-angle camera as render_twin.py"

    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(FRAME_DIR.glob("frame-*.png"))
    if existing:
        raise SystemExit(f"fresh frame directory required; found {len(existing)} existing PNGs")
    scene.render.filepath = str(FRAME_DIR / "frame-")
    bpy.ops.render.render(animation=True)
    frames = sorted(FRAME_DIR.glob("frame-*.png"))
    if len(frames) != 96:
        raise SystemExit(f"rendered {len(frames)} of 96 defect frames")
    print(f"rendered {len(frames)} defect_reverse_direction frames to {FRAME_DIR}")


if __name__ == "__main__":
    main()
