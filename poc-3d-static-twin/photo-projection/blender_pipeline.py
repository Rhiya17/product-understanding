"""Deterministic geometry, camera gates, projective UVs, and local rendering.

This script runs only in Blender 5.2 LTS.  It never overwrites the Ready2Jet
mechanism twin or source-vault.  Camera gating and projection are separate
phases so no image can reach a material before its measured IoU is final.

Examples:
  Blender --background --python blender_pipeline.py -- --lane ready2jet --phase gate-raw
  Blender --background --python blender_pipeline.py -- --lane levoit --phase build
  Blender --background --python blender_pipeline.py -- --lane macbook --state open --phase render
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text())
GATE_RESOLUTION = 256
RENDER_RESOLUTION = 1024
WATERMARK = CONFIG["watermark"]
FRAME_ROOT = Path("/tmp/product-understanding-photo-projection")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stem(source_id: str) -> str:
    return source_id.replace("#", "-").replace("/", "-")


def lane_key(lane: str, state: str | None) -> str:
    return f"{lane}-{state}" if state else lane


def lane_dir(lane: str) -> Path:
    return HERE / lane


def state_dir(lane: str, state: str | None) -> Path:
    return lane_dir(lane) / state if state else lane_dir(lane)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for blocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras,
                   bpy.data.lights, bpy.data.images):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)


def ensure_collection(name: str) -> bpy.types.Collection:
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def move_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def principled_material(name: str, color: tuple[float, float, float], roughness: float = 0.6,
                        metallic: float = 0.0) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    material.diffuse_color = (*color, 1.0)
    return material


def bevel(obj: bpy.types.Object, width: float, segments: int = 4) -> None:
    modifier = obj.modifiers.new("deterministic_edge_radius", "BEVEL")
    modifier.width = width
    modifier.segments = segments


def cube_part(name: str, dimensions: tuple[float, float, float], location: tuple[float, float, float],
              material: bpy.types.Material, edge: float, collection: bpy.types.Collection) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel(obj, edge)
    obj.data.materials.append(material)
    move_to_collection(obj, collection)
    return obj


def cylinder_part(name: str, radius: float, depth: float, z: float, material: bpy.types.Material,
                  collection: bpy.types.Collection, vertices: int = 96) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = name
    bevel(obj, min(radius * 0.08, depth * 0.2), 3)
    obj.data.materials.append(material)
    move_to_collection(obj, collection)
    return obj


def set_scene_metadata(lane: str, state: str | None) -> None:
    spec = CONFIG["lanes"][lane]
    scene = bpy.context.scene
    scene["photo_projection_workorder"] = "docs/workorders/workorder-photo-projection-catalog.md"
    scene["lane"] = int(spec["lane"])
    scene["product_id"] = spec["product_id"]
    scene["geometry_claim_ids"] = json.dumps(spec.get("claim_ids", []))
    scene["geometry_dimensions_m"] = json.dumps(spec.get("dimensions_m", {}), sort_keys=True)
    scene["geometry_method"] = "deterministic parametric geometry; observed proportions are INFERRED" if lane != "ready2jet" else "existing Ready2Jet mechanism twin; rig/action/evidence map untouched"
    scene["appearance_policy"] = "hash-verified official vault imagery only; neutral fallback elsewhere"
    scene["internal_only"] = True
    scene["approved_by"] = ""
    scene["external_spend_usd"] = 0.0
    scene["manufacturer_imagery_rights_review_open"] = True
    scene["tripo_texture_ancestry"] = False
    if state:
        scene["product_state"] = state


def build_levoit() -> None:
    spec = CONFIG["lanes"]["levoit"]
    w, h = spec["dimensions_m"]["width"], spec["dimensions_m"]["height"]
    radius = w / 2
    collection = ensure_collection("PRODUCT_GEOMETRY")
    white = principled_material("Neutral_White_Fallback", (0.78, 0.79, 0.80), 0.5)
    dark = principled_material("Neutral_Dark_Fallback", (0.025, 0.027, 0.03), 0.42)
    cylinder_part("LowerVentShell", radius * 0.98, h * 0.45, h * 0.225, white, collection)
    cylinder_part("UpperHousing", radius, h * 0.48, h * 0.69, white, collection)
    cylinder_part("BaseRing_INFERRED", radius * 0.94, h * 0.035, h * 0.0175, dark, collection)
    cylinder_part("TopRim", radius * 0.98, h * 0.055, h * 0.9525, white, collection)
    cylinder_part("ControlPanel", radius * 0.73, h * 0.010, h * 0.995, dark, collection)
    set_scene_metadata("levoit", None)
    bpy.context.scene["observed_proportion_note"] = "upper/lower split and panel/rim ratios traced from src_img_three_quarter_elevated_3000; unseen interior omitted as INFERRED"
    bpy.context.scene["wrap_policy"] = spec["wrap_policy"]
    save = lane_dir("levoit") / "levoit-parametric.blend"
    save.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(save))


def build_macbook(state: str) -> None:
    spec = CONFIG["lanes"]["macbook"]
    width = spec["dimensions_m"]["width"]
    depth = spec["dimensions_m"]["depth"]
    closed_h = spec["dimensions_m"]["height_closed"]
    collection = ensure_collection("PRODUCT_GEOMETRY")
    midnight = principled_material("Midnight_Neutral_Fallback", (0.055, 0.065, 0.082), 0.38, 0.55)
    black = principled_material("Display_Neutral_Fallback", (0.008, 0.010, 0.014), 0.3)
    if state == "closed":
        cube_part("BaseSlab", (width, depth, closed_h * 0.52), (0, 0, closed_h * 0.26), midnight,
                  closed_h * 0.12, collection)
        cube_part("Lid", (width, depth, closed_h * 0.48), (0, 0, closed_h * 0.76), midnight,
                  closed_h * 0.12, collection)
    else:
        base_h = closed_h * 0.52
        cube_part("BaseSlab", (width, depth, base_h), (0, 0, base_h / 2), midnight,
                  closed_h * 0.12, collection)
        cube_part("KeyboardDeck", (width * 0.965, depth * 0.93, closed_h * 0.08),
                  (0, -depth * 0.015, base_h + closed_h * 0.04), midnight, closed_h * 0.05, collection)
        lid_length = depth * 0.66
        angle = math.radians(75)
        hinge_y = depth / 2 - closed_h * 1.2
        center = (0, hinge_y + 0.5 * lid_length * math.cos(angle),
                  base_h + 0.5 * lid_length * math.sin(angle))
        lid = cube_part("Lid", (width, lid_length, closed_h * 0.38), center, midnight,
                        closed_h * 0.10, collection)
        lid.rotation_euler.x = angle
        # A neutral inset is deterministic geometry; keyboard and deck details
        # remain exclusively photo-projected.
        display = cube_part("DisplayInset_INFERRED", (width * 0.92, lid_length * 0.90, closed_h * 0.035),
                            center, black, closed_h * 0.03, collection)
        display.rotation_euler.x = angle
        local_normal = Vector((0, 0, 1))
        display.location += display.rotation_euler.to_matrix() @ local_normal * (closed_h * 0.22)
    set_scene_metadata("macbook", state)
    bpy.context.scene["open_lid_angle_deg_INFERRED"] = 75.0 if state == "open" else 0.0
    save = state_dir("macbook", state) / f"macbook-{state}-parametric.blend"
    save.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(save))


def curve_arc(name: str, points: list[tuple[float, float, float]], bevel_depth: float,
              material: bpy.types.Material, collection: bpy.types.Collection) -> bpy.types.Object:
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 4
    curve.bevel_resolution = 4
    curve.bevel_depth = bevel_depth
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def build_bose() -> None:
    spec = CONFIG["lanes"]["bose"]
    width = spec["dimensions_m"]["width"]
    height = spec["dimensions_m"]["height"]
    depth = spec["dimensions_m"]["depth"]
    collection = ensure_collection("PRODUCT_GEOMETRY")
    black = principled_material("Black_Neutral_Fallback", (0.012, 0.014, 0.017), 0.36, 0.15)
    cushion = principled_material("Cushion_Neutral_Fallback", (0.006, 0.007, 0.009), 0.82)
    half = width * 0.43
    bottom = height * 0.34
    points = [
        (-half, 0, bottom),
        (-half * 0.92, 0, height * 0.70),
        (-half * 0.58, 0, height * 0.94),
        (0, 0, height),
        (half * 0.58, 0, height * 0.94),
        (half * 0.92, 0, height * 0.70),
        (half, 0, bottom),
    ]
    curve_arc("HeadbandArc", points, depth * 0.22, black, collection)
    for side, x in (("L", -width * 0.32), ("R", width * 0.32)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(x, 0, height * 0.255))
        cup = bpy.context.object
        cup.name = f"Earcup_{side}"
        cup.scale = (width * 0.17, depth * 0.50, height * 0.24)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        cup.data.materials.append(black)
        move_to_collection(cup, collection)
        bpy.ops.mesh.primitive_torus_add(major_radius=height * 0.115, minor_radius=depth * 0.09,
                                         major_segments=64, minor_segments=16,
                                         location=(x, -depth * 0.42, height * 0.255),
                                         rotation=(math.pi / 2, 0, 0))
        pad = bpy.context.object
        pad.name = f"EarCushion_{side}"
        pad.scale.x = 0.78
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        pad.data.materials.append(cushion)
        move_to_collection(pad, collection)
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=depth * 0.10, depth=height * 0.17,
                                             location=(x, 0, height * 0.48))
        slider = bpy.context.object
        slider.name = f"Slider_{side}_INFERRED"
        slider.data.materials.append(black)
        move_to_collection(slider, collection)
    set_scene_metadata("bose", None)
    bpy.context.scene["dimension_source_note"] = "claim_bqcu2_spec_headphone_weight_1 source quote includes 1.772 H x 6.299 W x 8.071 D in; mapped to depth/width/height by observed wearing orientation"
    save = lane_dir("bose") / "bose-parametric.blend"
    save.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(save))


def build(lane: str, state: str | None) -> None:
    if lane == "ready2jet":
        raise SystemExit("Ready2Jet uses the existing mechanism twin and has no build phase")
    clear_scene()
    if lane == "levoit":
        build_levoit()
    elif lane == "macbook":
        if state not in {"open", "closed"}:
            raise SystemExit("MacBook build requires --state open|closed")
        build_macbook(state)
    elif lane == "bose":
        build_bose()
    else:
        raise SystemExit(f"unsupported build lane {lane}")


def source_blend(lane: str, state: str | None, projected: bool = False) -> Path:
    if projected:
        return state_dir(lane, state) / f"{lane}{'-' + state if state else ''}-photo-projected.blend"
    if lane == "ready2jet":
        return ROOT / CONFIG["lanes"][lane]["geometry"]
    if lane == "levoit":
        return lane_dir(lane) / "levoit-parametric.blend"
    if lane == "macbook":
        return state_dir(lane, state) / f"macbook-{state}-parametric.blend"
    if lane == "bose":
        return lane_dir(lane) / "bose-parametric.blend"
    raise ValueError(lane)


def open_geometry(lane: str, state: str | None, projected: bool = False) -> list[bpy.types.Object]:
    path = source_blend(lane, state, projected)
    if not path.exists():
        raise SystemExit(f"missing scene: {path}")
    bpy.ops.wm.open_mainfile(filepath=str(path))
    if bpy.app.version_string != "5.2.0 LTS":
        raise SystemExit(f"binding Blender version changed: {bpy.app.version_string}")
    scene = bpy.context.scene
    if lane == "ready2jet":
        scene.frame_set(1)
        collection = bpy.data.collections.get("TWIN_GEOMETRY")
        if collection is None:
            raise SystemExit("Ready2Jet TWIN_GEOMETRY collection missing")
        geometry = [obj for obj in collection.all_objects if obj.type == "MESH" and not obj.hide_render]
        for obj in scene.objects:
            if obj not in geometry and obj.type not in {"CAMERA", "LIGHT"}:
                obj.hide_render = True
    else:
        collection = bpy.data.collections.get("PRODUCT_GEOMETRY")
        if collection is None:
            raise SystemExit("PRODUCT_GEOMETRY collection missing")
        # Curves are deterministically converted in the derived working scene.
        for obj in list(collection.all_objects):
            if obj.type == "CURVE":
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                bpy.ops.object.convert(target="MESH")
                obj.select_set(False)
        geometry = [obj for obj in collection.all_objects if obj.type == "MESH" and not obj.hide_render]
    if not geometry:
        raise SystemExit("no renderable geometry")
    return geometry


def world_bbox(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return low, high


def new_camera(name: str, target: Vector, azimuth_deg: float, elevation_deg: float,
               distance: float, lens: float = 70.0, shift_x: float = 0.0,
               shift_y: float = 0.0) -> bpy.types.Object:
    azimuth = math.radians(azimuth_deg)
    elevation = math.radians(elevation_deg)
    direction = Vector((math.cos(elevation) * math.cos(azimuth),
                        math.cos(elevation) * math.sin(azimuth),
                        math.sin(elevation)))
    data = bpy.data.cameras.new(name)
    data.type = "PERSP"
    data.lens = lens
    data.shift_x = shift_x
    data.shift_y = shift_y
    camera = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = target + direction * distance
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera
    return camera


def setup_mask_render() -> None:
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = scene.render.resolution_y = GATE_RESOLUTION
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.view_settings.look = "AgX - Medium High Contrast"
    override = bpy.data.materials.get("CAMERA_GATE_WHITE") or bpy.data.materials.new("CAMERA_GATE_WHITE")
    override.use_nodes = True
    nodes = override.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (1, 1, 1, 1)
    emission.inputs["Strength"].default_value = 1.0
    override.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    bpy.context.view_layer.material_override = override
    world = scene.world or bpy.data.worlds.new("GateWorld")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0


def eligible_sources(lane: str, state: str | None) -> list[dict]:
    sources = CONFIG["lanes"][lane].get("sources", [])
    if lane == "macbook":
        sources = [source for source in sources if source.get("state") == state]
    return sources


def gate_raw(lane: str, state: str | None) -> None:
    geometry = open_geometry(lane, state)
    setup_mask_render()
    low, high = world_bbox(geometry)
    target = (low + high) / 2
    max_dim = max(high - low)
    base_distance = max_dim * 4.5
    out = state_dir(lane, state) / "camera-gates" / "raw"
    out.mkdir(parents=True, exist_ok=True)
    attempts: dict[str, list[dict]] = {}
    for source in eligible_sources(lane, state):
        source_attempts = []
        for azimuth in source["camera_grid"]["azimuth_deg"]:
            for elevation in source["camera_grid"]["elevation_deg"]:
                name = f"Gate_{stem(source['source_id'])}_{azimuth}_{elevation}"
                camera = new_camera(name, target, azimuth, elevation, base_distance)
                file_name = f"{stem(source['source_id'])}__az{azimuth:+04d}__el{elevation:+03d}.png"
                path = out / file_name
                bpy.context.scene.render.filepath = str(path)
                bpy.ops.render.render(write_still=True)
                source_attempts.append({
                    "mask_local_path": str(path.relative_to(ROOT)),
                    "azimuth_deg": azimuth,
                    "elevation_deg": elevation,
                    "lens_mm": camera.data.lens,
                    "base_distance_m": base_distance,
                    "target_xyz_m": list(target),
                    "base_position_xyz_m": list(camera.location),
                    "base_rotation_euler_rad": list(camera.rotation_euler),
                })
                bpy.data.objects.remove(camera, do_unlink=True)
        attempts[source["source_id"]] = source_attempts
    record = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "resolution_px": [GATE_RESOLUTION, GATE_RESOLUTION],
        "camera_type": "PERSP",
        "attempts": attempts,
    }
    (state_dir(lane, state) / "camera-gates" / "raw-attempts.json").write_text(json.dumps(record, indent=2) + "\n")


def gate_final(lane: str, state: str | None) -> None:
    geometry = open_geometry(lane, state)
    del geometry
    setup_mask_render()
    directory = state_dir(lane, state) / "camera-gates"
    preliminary = json.loads((directory / "camera-fits-preliminary.json").read_text())
    out = directory / "final"
    out.mkdir(parents=True, exist_ok=True)
    rendered = {}
    for source_id, fit in preliminary["selected"].items():
        target = Vector(fit["target_xyz_m"])
        camera = new_camera(
            f"FinalGate_{stem(source_id)}", target, fit["azimuth_deg"], fit["elevation_deg"],
            fit["fitted_distance_m"], fit["lens_mm"], fit["shift_x"], fit["shift_y"],
        )
        path = out / f"{stem(source_id)}.png"
        bpy.context.scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        rendered[source_id] = {
            "mask_local_path": str(path.relative_to(ROOT)),
            "position_xyz_m": list(camera.location),
            "rotation_euler_rad": list(camera.rotation_euler),
            "focal_length_mm": camera.data.lens,
            "shift_x": camera.data.shift_x,
            "shift_y": camera.data.shift_y,
        }
        bpy.data.objects.remove(camera, do_unlink=True)
    (directory / "final-renders.json").write_text(json.dumps({"schema_version": 1, "renders": rendered}, indent=2) + "\n")


def load_mask(path: Path) -> tuple[np.ndarray, int, int]:
    image = bpy.data.images.load(str(path), check_existing=True)
    width, height = image.size
    pixels = np.asarray(image.pixels[:], dtype=np.float32).reshape(height, width, image.channels)
    channel = pixels[:, :, 0]
    return channel, width, height


def projection_matrix(camera: bpy.types.Object, scene: bpy.types.Scene):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    camera_matrix = camera.calc_matrix_camera(
        depsgraph, x=scene.render.resolution_x, y=scene.render.resolution_y,
        scale_x=scene.render.pixel_aspect_x, scale_y=scene.render.pixel_aspect_y,
    )
    return camera_matrix @ camera.matrix_world.inverted()


def project_world(matrix, world: Vector) -> tuple[float, float, float]:
    clip = matrix @ world.to_4d()
    if clip.w == 0:
        return math.inf, math.inf, 0.0
    return (clip.x / clip.w + 1.0) * 0.5, (clip.y / clip.w + 1.0) * 0.5, clip.w


def fallback_color(obj: bpy.types.Object) -> tuple[float, float, float]:
    if obj.data.materials:
        material = obj.data.materials[0]
        if material:
            return tuple(float(x) for x in material.diffuse_color[:3])
    return (0.12, 0.12, 0.13)


def projection_material(obj: bpy.types.Object, source_id: str, uv_name: str,
                        texture_path: Path) -> bpy.types.Material:
    name = f"PHOTO_{stem(source_id)}_{obj.name}"[:63]
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    fallback = nodes.new("ShaderNodeBsdfPrincipled")
    fallback.inputs["Base Color"].default_value = (*fallback_color(obj), 1.0)
    fallback.inputs["Roughness"].default_value = 0.72
    photo = nodes.new("ShaderNodeBsdfPrincipled")
    photo.inputs["Roughness"].default_value = 0.58
    uv = nodes.new("ShaderNodeUVMap")
    uv.uv_map = uv_name
    image_node = nodes.new("ShaderNodeTexImage")
    image_node.image = bpy.data.images.load(str(texture_path), check_existing=True)
    image_node.extension = "CLIP"
    material.node_tree.links.new(uv.outputs["UV"], image_node.inputs["Vector"])
    material.node_tree.links.new(image_node.outputs["Color"], photo.inputs["Base Color"])
    material.node_tree.links.new(image_node.outputs["Alpha"], mix.inputs[0])
    material.node_tree.links.new(fallback.outputs["BSDF"], mix.inputs[1])
    material.node_tree.links.new(photo.outputs["BSDF"], mix.inputs[2])
    material.node_tree.links.new(mix.outputs["Shader"], output.inputs["Surface"])
    material["source_id"] = source_id
    material["source_texture_sha256"] = sha256(texture_path)
    material["appearance_pixels"] = "official source image RGB only"
    return material


def object_area(poly: bpy.types.MeshPolygon) -> float:
    return float(poly.area)


def project(lane: str, state: str | None) -> None:
    geometry = open_geometry(lane, state)
    directory = state_dir(lane, state)
    matches = json.loads((directory / "camera-gates" / "camera-matches.json").read_text())
    prepared = json.loads((lane_dir(lane) / "source-preparation.json").read_text())
    prepared_by_id = {source["source_id"]: source for source in prepared["sources"]}
    configured = {source["source_id"]: source for source in eligible_sources(lane, state)}
    passed_ids = [source_id for source_id, record in matches["matches"].items() if record["status"] == "PASS"]
    passed_ids.sort(key=lambda source_id: configured[source_id]["projection_order"])
    if not passed_ids:
        raise SystemExit("no camera-qualified source; §0.7 forbids projection")

    scene = bpy.context.scene
    # Camera matches were solved on a square sensor canvas; UV projection must
    # use that identical aspect ratio regardless of the build scene defaults.
    scene.render.resolution_x = scene.render.resolution_y = GATE_RESOLUTION
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
    cameras = {}
    camera_matrices = {}
    for source_id in passed_ids:
        record = matches["matches"][source_id]
        camera = new_camera(
            f"Projection_{stem(source_id)}", Vector(record["target_xyz_m"]), record["azimuth_deg"],
            record["elevation_deg"], record["distance_m"], record["focal_length_mm"],
            record["shift_x"], record["shift_y"],
        )
        camera.hide_render = True
        camera["camera_match_iou"] = record["silhouette_iou"]
        camera["source_id"] = source_id
        cameras[source_id] = camera
        camera_matrices[source_id] = projection_matrix(camera, scene)

    assigned: dict[str, set[int]] = {obj.name: set() for obj in geometry}
    coverage_by_source = {source_id: 0.0 for source_id in passed_ids}
    total_area = sum(object_area(poly) for obj in geometry for poly in obj.data.polygons)
    object_records = {}
    threshold = math.cos(math.radians(float(CONFIG["front_facing_degrees"])))

    for obj in geometry:
        original_slots = len(obj.data.materials)
        source_slot = {}
        source_masks = {}
        for source_id in passed_ids:
            allowed = configured[source_id].get("part_allow")
            if allowed is not None and obj.name not in allowed:
                continue
            uv_name = f"UV_{stem(source_id)}"[:63]
            uv_layer = obj.data.uv_layers.get(uv_name) or obj.data.uv_layers.new(name=uv_name)
            camera = cameras[source_id]
            scene.camera = camera
            matrix = camera_matrices[source_id]
            for loop in obj.data.loops:
                world = obj.matrix_world @ obj.data.vertices[loop.vertex_index].co
                u, v, _ = project_world(matrix, world)
                uv_layer.data[loop.index].uv = (u, v)
            texture_path = ROOT / prepared_by_id[source_id]["masked_texture_local_path"]
            material = projection_material(obj, source_id, uv_name, texture_path)
            obj.data.materials.append(material)
            source_slot[source_id] = len(obj.data.materials) - 1
            source_masks[source_id] = load_mask(ROOT / prepared_by_id[source_id]["mask_local_path"])

        world_normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
        area_total = sum(object_area(poly) for poly in obj.data.polygons)
        source_area = {source_id: 0.0 for source_id in passed_ids}
        diagnostic = {source_id: {"faces": 0, "camera_facing": 0, "positive_depth": 0,
                                  "xy_in_frame": 0, "in_frame": 0, "inside_mask": 0,
                                  "x_min": None, "x_max": None, "y_min": None, "y_max": None}
                      for source_id in passed_ids}
        for source_id in passed_ids:
            if source_id not in source_slot:
                continue
            camera = cameras[source_id]
            scene.camera = camera
            matrix = camera_matrices[source_id]
            mask, width, height = source_masks[source_id]
            for poly in obj.data.polygons:
                diagnostic[source_id]["faces"] += 1
                if poly.index in assigned[obj.name]:
                    continue
                center_world = obj.matrix_world @ poly.center
                normal_world = (world_normal_matrix @ poly.normal).normalized()
                view = (camera.location - center_world).normalized()
                if normal_world.dot(view) < threshold:
                    continue
                diagnostic[source_id]["camera_facing"] += 1
                u, v, depth = project_world(matrix, center_world)
                for key, value in (("x_min", u), ("x_max", u), ("y_min", v), ("y_max", v)):
                    current = diagnostic[source_id][key]
                    if current is None or (key.endswith("min") and value < current) or (key.endswith("max") and value > current):
                        diagnostic[source_id][key] = float(value)
                if depth > 0:
                    diagnostic[source_id]["positive_depth"] += 1
                if 0 <= u <= 1 and 0 <= v <= 1:
                    diagnostic[source_id]["xy_in_frame"] += 1
                if depth <= 0 or not (0 <= u <= 1 and 0 <= v <= 1):
                    continue
                diagnostic[source_id]["in_frame"] += 1
                x = min(width - 1, max(0, int(u * width)))
                y = min(height - 1, max(0, int((1.0 - v) * height)))
                if mask[y, x] < 0.5:
                    continue
                diagnostic[source_id]["inside_mask"] += 1
                poly.material_index = source_slot[source_id]
                assigned[obj.name].add(poly.index)
                area = object_area(poly)
                source_area[source_id] += area
                coverage_by_source[source_id] += area
        covered = sum(source_area.values())
        object_records[obj.name] = {
            "part_area_mesh_units2": area_total,
            "covered_area_mesh_units2": covered,
            "coverage_fraction": round(covered / area_total, 6) if area_total else 0.0,
            "fallback_fraction": round(1.0 - covered / area_total, 6) if area_total else 1.0,
            "source_area_fraction": {
                source_id: round(area / area_total, 6) if area_total else 0.0
                for source_id, area in source_area.items()
            },
            "original_material_slot_count": original_slots,
            "projection_diagnostic_face_counts": diagnostic,
        }

    scene["qualified_projection_sources"] = json.dumps(passed_ids)
    scene["camera_match_gate"] = 0.75
    scene["front_facing_threshold_deg"] = CONFIG["front_facing_degrees"]
    scene["projection_policy"] = "best-view-first; later sources fill only previously uncovered faces; alpha feathers to neutral fallback"
    scene["coverage_measurement"] = "mesh polygon area; centroid must be camera-facing and inside source product mask"
    output_blend = source_blend(lane, state, projected=True)
    output_blend.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
    coverage = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "geometry_blend": str(output_blend.relative_to(ROOT)),
        "geometry_sha256": sha256(output_blend),
        "qualified_sources_best_view_first": passed_ids,
        "front_facing_threshold_deg": CONFIG["front_facing_degrees"],
        "overall_coverage_fraction": round(sum(coverage_by_source.values()) / total_area, 6) if total_area else 0.0,
        "overall_fallback_fraction": round(1.0 - sum(coverage_by_source.values()) / total_area, 6) if total_area else 1.0,
        "source_area_fraction": {
            source_id: round(area / total_area, 6) if total_area else 0.0
            for source_id, area in coverage_by_source.items()
        },
        "parts": object_records,
        "uncovered_policy": "neutral pre-existing/dimension-build material; never invented",
    }
    (directory / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")


def setup_render_scene(scene: bpy.types.Scene) -> None:
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = scene.render.resolution_y = RENDER_RESOLUTION
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.fps = 24
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.use_stamp = True
    scene.render.use_stamp_note = True
    scene.render.stamp_note_text = WATERMARK
    scene.render.stamp_font_size = 20
    scene.render.stamp_foreground = (1.0, 0.30, 0.18, 1.0)
    scene.render.stamp_background = (0.02, 0.02, 0.02, 0.82)
    for prop in (
        "use_stamp_time", "use_stamp_date", "use_stamp_frame", "use_stamp_frame_range", "use_stamp_camera",
        "use_stamp_lens", "use_stamp_scene", "use_stamp_filename", "use_stamp_marker", "use_stamp_memory",
        "use_stamp_hostname", "use_stamp_render_time",
    ):
        if hasattr(scene.render, prop):
            setattr(scene.render, prop, False)
    world = scene.world or bpy.data.worlds.new("PhotoProjectionWorld")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.72, 0.76, 0.82, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    # Projection cameras are evidence, never render cameras.
    for obj in scene.objects:
        if obj.type == "LIGHT":
            obj.hide_render = True
    for name, location, energy, size in (
        ("Photo_Key", (-3.5, -4.0, 5.5), 850, 4.0),
        ("Photo_Fill", (4.0, -1.0, 3.0), 420, 4.0),
        ("Photo_Rim", (2.0, 4.0, 4.5), 650, 3.0),
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = location
        light.rotation_euler = (Vector((0, 0, 0.5)) - light.location).to_track_quat("-Z", "Y").to_euler()


def clear_frame_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for old in directory.glob("frame-*.png"):
        old.unlink()


def render_animation(scene: bpy.types.Scene, directory: Path, expected: int) -> None:
    clear_frame_dir(directory)
    scene.render.filepath = str(directory / "frame-")
    bpy.ops.render.render(animation=True)
    frames = sorted(directory.glob("frame-*.png"))
    if len(frames) != expected:
        raise SystemExit(f"rendered {len(frames)} of {expected} frames in {directory}")


def render_static(lane: str, state: str | None, geometry: list[bpy.types.Object]) -> dict:
    scene = bpy.context.scene
    low, high = world_bbox(geometry)
    center = (low + high) / 2
    max_dim = max(high - low)
    target_name = f"{lane_key(lane, state)}-turntable"
    camera = new_camera("Render_Turntable", center, -90, 18, max_dim * 3.6, 58)
    scene.camera = camera
    scene.frame_start = 1
    scene.frame_end = 24
    for frame in range(1, 25):
        azimuth = -90 + 360 * (frame - 1) / 24
        az = math.radians(azimuth)
        el = math.radians(18)
        camera.location = center + Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az),
                                           math.sin(el))) * max_dim * 3.6
        camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_euler", frame=frame)
    directory = FRAME_ROOT / lane_key(lane, state) / target_name
    render_animation(scene, directory, 24)
    return {target_name: {"frames_dir": str(directory), "frame_count": 24, "fps": 8}}


def render_ready2jet(geometry: list[bpy.types.Object]) -> dict:
    scene = bpy.context.scene
    rig = bpy.data.objects.get("RigRoot")
    if rig is None or not rig.animation_data or not rig.animation_data.action:
        raise SystemExit("Ready2Jet rig/action missing")
    original_action = rig.animation_data.action
    outputs = {}
    low, high = world_bbox(geometry)
    center = (low + high) / 2
    max_dim = max(high - low)

    rig.animation_data.action = None
    for prop in ("stage_prepare", "stage_thumb_switch", "stage_handle_lever", "stage_auto_fold", "stage_secure"):
        rig[prop] = 0.0
    scene.frame_start, scene.frame_end = 1, 72
    camera = new_camera("Render_OpenTurntable", center, -90, 18, max_dim * 3.4, 58)
    for frame in range(1, 73):
        azimuth = -90 + 360 * (frame - 1) / 72
        az, el = math.radians(azimuth), math.radians(18)
        camera.location = center + Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az),
                                           math.sin(el))) * max_dim * 3.4
        camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_euler", frame=frame)
    directory = FRAME_ROOT / "ready2jet" / "open-turntable"
    render_animation(scene, directory, 72)
    outputs["open-turntable"] = {"frames_dir": str(directory), "frame_count": 72, "fps": 24}
    bpy.data.objects.remove(camera, do_unlink=True)

    rig.animation_data.action = original_action
    for target_name, location, look_at in (
        ("fold-official-angle", (-1.45, -1.42, 1.08), (0.03, 0.0, 0.48)),
        ("fold-novel-rear-right", (1.72, 1.65, 1.25), (0.08, 0.0, 0.46)),
    ):
        camera = new_camera(f"Render_{target_name}", Vector(look_at), 0, 0, 1, 58)
        camera.location = location
        camera.rotation_euler = (Vector(look_at) - camera.location).to_track_quat("-Z", "Y").to_euler()
        scene.camera = camera
        scene.frame_start, scene.frame_end = 1, 96
        directory = FRAME_ROOT / "ready2jet" / target_name
        render_animation(scene, directory, 96)
        outputs[target_name] = {"frames_dir": str(directory), "frame_count": 96, "fps": 24}
        bpy.data.objects.remove(camera, do_unlink=True)
    return outputs


def render(lane: str, state: str | None) -> None:
    geometry = open_geometry(lane, state, projected=True)
    scene = bpy.context.scene
    setup_render_scene(scene)
    outputs = render_ready2jet(geometry) if lane == "ready2jet" else render_static(lane, state, geometry)
    record = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "resolution_px": [RENDER_RESOLUTION, RENDER_RESOLUTION],
        "watermark": WATERMARK,
        "internal_only": True,
        "external_spend_usd": 0,
        "outputs": outputs,
    }
    (state_dir(lane, state) / "frame-manifest.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=("ready2jet", "levoit", "macbook", "bose"))
    parser.add_argument("--state", choices=("open", "closed"))
    parser.add_argument("--phase", required=True, choices=("build", "gate-raw", "gate-final", "project", "render"))
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if args.lane != "macbook" and args.state:
        raise SystemExit("--state is only valid for macbook")
    if args.phase == "build":
        build(args.lane, args.state)
    elif args.phase == "gate-raw":
        gate_raw(args.lane, args.state)
    elif args.phase == "gate-final":
        gate_final(args.lane, args.state)
    elif args.phase == "project":
        project(args.lane, args.state)
    else:
        render(args.lane, args.state)


if __name__ == "__main__":
    main()
