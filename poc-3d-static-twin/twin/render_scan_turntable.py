"""Render a turntable of a textured Tripo scan (static look-alike twin).

INTERNAL ONLY: the Tripo3D license check is open (Decision 1); these renders
must not ship. The scan is the photo-derived statue — product-accurate look,
no articulation. Output: renders/scan-turntable frames.

Usage:
  Blender --background --python render_scan_turntable.py -- \
    --glb /abs/model.glb --output-dir /abs/frames --frames 24 --resolution 1024
"""

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
GLB = (HERE.parent / "runs" / "tripo-probe-01"
       / "model_mesh-k11lDWbp1BeH5sJR6lO6C_model.glb")
FRAME_DIR = HERE / "renders" / "frames-scan-turntable"
FRAMES = 72


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--glb", type=Path, default=GLB)
    parser.add_argument("--output-dir", type=Path, default=FRAME_DIR)
    parser.add_argument("--frames", type=int, default=FRAMES)
    parser.add_argument("--resolution", type=int, default=1024)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return parser.parse_args(argv)


def main():
    args = parse_args()
    if not args.glb.is_file():
        raise SystemExit(f"GLB does not exist: {args.glb}")
    if args.frames < 2 or args.resolution < 256:
        raise SystemExit("frames must be >=2 and resolution must be >=256")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output_dir}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    bpy.ops.import_scene.gltf(filepath=str(args.glb))
    meshes = [o for o in scene.objects if o.type == "MESH"]
    if not meshes:
        raise SystemExit("GLB contains no mesh objects")
    # Center the complete imported hierarchy (some GLBs contain many meshes).
    bounds = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector(min(v[i] for v in bounds) for i in range(3))
    hi = Vector(max(v[i] for v in bounds) for i in range(3))
    center = (lo + hi) / 2
    for root in [o for o in scene.objects if o.parent is None]:
        root.location += Vector((-center.x, -center.y, -lo.z))
    model_size = hi - lo
    radius = max(model_size.length / 2, 0.01)

    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.93, 0.945, 0.965, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.45

    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
    floor = bpy.context.object
    floor_mat = bpy.data.materials.new("Floor")
    floor_mat.use_nodes = True
    bsdf = floor_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.80, 0.80, 0.78, 1)
    bsdf.inputs["Roughness"].default_value = 0.85
    floor.data.materials.append(floor_mat)

    for name, energy, light_size, loc, color in (
        ("Key", 420, 5.0, (-2.2, -2.9, 3.3), (1.0, 0.972, 0.93)),
        ("Fill", 150, 4.0, (2.6, -1.2, 2.0), (0.90, 0.94, 1.0)),
        ("Rim", 300, 3.0, (2.6, 2.8, 2.6), (0.95, 0.97, 1.0)),
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.size = light_size
        data.color = color
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = loc
        direction = Vector((0, 0, 0.45)) - Vector(loc)
        light.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    orbit = bpy.data.objects.new("Orbit", None)
    scene.collection.objects.link(orbit)
    orbit.location = (0, 0, model_size.z * 0.48)
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 58
    cam = bpy.data.objects.new("Cam", cam_data)
    scene.collection.objects.link(cam)
    cam.parent = orbit
    fov = 2 * math.atan(36 / (2 * cam_data.lens))
    distance = radius / math.sin(fov / 2) * 1.25
    cam.location = (0.0, -distance, model_size.z * 0.08)
    track = cam.constraints.new("TRACK_TO")
    track.target = orbit
    scene.camera = cam

    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    for attr in ("use_raytracing", "use_gtao"):
        if hasattr(scene.eevee, attr):
            setattr(scene.eevee, attr, True)
    scene.view_settings.look = "AgX - Punchy"
    scene.render.resolution_x = scene.render.resolution_y = args.resolution
    scene.render.image_settings.file_format = "PNG"

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for frame in range(args.frames):
        orbit.rotation_euler = (0, 0, 2 * math.pi * frame / args.frames)
        scene.render.filepath = str(args.output_dir / f"frame-{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
    print("rendered", args.frames, "frames to", args.output_dir)


if __name__ == "__main__":
    main()
