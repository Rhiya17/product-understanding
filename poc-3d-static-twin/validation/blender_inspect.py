"""Headless Blender inspection for a POC 5 mesh (runbook Stage 4).

Renders, per run:
  canonical orthographic views  front / rear / left / right / top
  region close-ups              handle, belly-bar, front wheels, canopy
  36-frame 360-degree turntable (mp4, Blender's built-in FFmpeg)
plus a stats.json with Blender version, object/mesh counts, and world bbox.

Usage:
  <blender> --background --python validation/blender_inspect.py -- \
      --glb runs/meshy-run-01/model/model.glb --out validation/renders/meshy-run-01

Note on axes: the glTF importer converts Y-up (glTF) to Z-up (Blender), so
Blender Z = glTF Y. The canonical renders are named by BLENDER world axes;
axis-mapping conclusions must reference stats.json's bbox.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

RES = 1024
TURN_FRAMES = 36


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True)
    ap.add_argument("--out", required=True)
    return ap.parse_args(argv)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def world_bbox(objs):
    pts = []
    for o in objs:
        for corner in o.bound_box:
            pts.append(o.matrix_world @ Vector(corner))
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def setup_lighting():
    world = bpy.data.worlds["World"] if bpy.data.worlds else bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
        bg.inputs[1].default_value = 1.0
    for name, loc, energy in (
        ("key", (5, -5, 8), 3.0),
        ("fill", (-6, -3, 5), 1.5),
        ("back", (0, 7, 6), 1.5),
    ):
        light_data = bpy.data.lights.new(name, type="SUN")
        light_data.energy = energy
        light = bpy.data.objects.new(name, light_data)
        bpy.context.collection.objects.link(light)
        light.location = loc
        direction = -Vector(loc)
        light.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera():
    cam_data = bpy.data.cameras.new("inspect_cam")
    cam = bpy.data.objects.new("inspect_cam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def aim(cam, location, target):
    cam.location = location
    direction = Vector(target) - Vector(location)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_to(path):
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    args = parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    clear_scene()
    bpy.ops.import_scene.gltf(filepath=args.glb)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    lo, hi = world_bbox(meshes)
    center = (lo + hi) / 2
    size = hi - lo
    radius = max(size) * 1.25

    stats = {
        "blender_version": bpy.app.version_string,
        "glb": args.glb,
        "mesh_objects": len(meshes),
        "total_vertices": sum(len(o.data.vertices) for o in meshes),
        "total_polygons": sum(len(o.data.polygons) for o in meshes),
        "world_bbox_min": list(lo), "world_bbox_max": list(hi),
        "world_bbox_size_xyz": list(size),
        "note": "Blender is Z-up; glTF importer maps glTF +Y (up) to Blender +Z.",
    }
    (out / "stats.json").write_text(json.dumps(stats, indent=2))

    setup_lighting()
    scene = bpy.context.scene
    scene.render.resolution_x = RES
    scene.render.resolution_y = RES
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"

    cam = make_camera()

    # Canonical orthographic views, semantic names. Mapping verified on the
    # meshy-v1-pilot mesh: stroller front = -X, rear = +X, left side = -Y
    # (parent-behind-handle convention). Meshy appears to orient consistently,
    # but VERIFY FACING PER RUN before trusting these names on a new mesh.
    cam.data.type = "ORTHO"
    dist = max(size) * 3
    views = {
        "ortho-front": (center + Vector((-dist, 0, 0)), max(size.y, size.z)),
        "ortho-rear": (center + Vector((dist, 0, 0)), max(size.y, size.z)),
        "ortho-side-left": (center + Vector((0, -dist, 0)), max(size.x, size.z)),
        "ortho-side-right": (center + Vector((0, dist, 0)), max(size.x, size.z)),
        "ortho-top": (center + Vector((0, 0, dist)), max(size.x, size.y)),
    }
    for name, (loc, span) in views.items():
        cam.data.ortho_scale = span * 1.15
        aim(cam, loc, center)
        render_to(out / f"{name}.png")

    # Region close-ups (perspective), targeted by bbox fractions.
    cam.data.type = "PERSP"
    cam.data.lens = 50
    regions = {
        "closeup-handle": (center + Vector((0, 0, size.z * 0.35)), radius * 0.9),
        "closeup-bellybar": (center + Vector((0, -size.y * 0.15, size.z * 0.15)), radius * 0.8),
        "closeup-frontwheels": (center + Vector((0, -size.y * 0.25, -size.z * 0.35)), radius * 0.8),
        "closeup-canopy": (center + Vector((0, size.y * 0.2, size.z * 0.30)), radius * 0.9),
    }
    for name, (target, d) in regions.items():
        aim(cam, target + Vector((d * 0.7, -d * 0.7, d * 0.35)), target)
        render_to(out / f"{name}.png")

    # 360-degree turntable, three-quarter elevation. This Blender build has no
    # FFMPEG image format, so render PNG frames (GIF assembly happens outside).
    turn_dir = out / "turntable"
    turn_dir.mkdir(exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = scene.render.resolution_y = 512
    elev = size.z * 0.35
    for f in range(TURN_FRAMES):
        ang = 2 * math.pi * f / TURN_FRAMES
        loc = center + Vector((radius * 1.6 * math.cos(ang), radius * 1.6 * math.sin(ang), elev))
        aim(cam, loc, center)
        render_to(turn_dir / f"frame-{f:02d}.png")

    print("INSPECTION COMPLETE ->", out)


if __name__ == "__main__":
    main()
