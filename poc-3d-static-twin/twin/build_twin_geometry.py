"""Build the POC 6 rig-ready Ready2Jet geometry over the Tripo scaffold.

Every Blender operation is scripted.  The Tripo mesh is imported into a
hidden reference collection with run/pack/hash provenance; the articulated
geometry is rebuilt from clean named primitives and evidence-driven pivots.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GLB = ROOT / "poc-3d-static-twin" / "runs" / "tripo-probe-01" / "glb-k11lDWbp1BeH5sJR6lO6C_model.glb"
GLB_SHA256 = "95e0fe44bba9a303b31849cfbec1d7d517d2ed2c6361ab505e025cf7ef80716b"
PACK_HASH = "da454173c3733e0227d90f869925145897669e96df8f7c593f0f45be94d8a83f"
OUT_BLEND = HERE / "ready2jet-stage-b.blend"
OUT_REPORT = HERE / "geometry-report.json"
QA_DIR = HERE / "stage-b-qa"
TARGET_DWH_M = (0.6858, 0.5207, 1.0922)  # Blender X, Y, Z


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in list(bpy.data.collections):
        if coll.name != "Collection":
            bpy.data.collections.remove(coll)


def new_collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def move_to(obj, coll):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    coll.objects.link(obj)


def mat(name, color, metallic=0.0, roughness=0.45, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color[:3], alpha)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color[:3], alpha)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha < 1:
        bsdf.inputs["Alpha"].default_value = alpha
        material.surface_render_method = "DITHERED"
    return material


def empty(name, location, coll, confidence="DOCUMENTED"):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = 0.045
    obj.location = location
    obj["confidence"] = confidence
    coll.objects.link(obj)
    return obj


def parent_keep_world(obj, parent):
    bpy.context.view_layer.update()
    matrix = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = matrix
    bpy.context.view_layer.update()


def mark(obj, confidence, evidence):
    obj["confidence"] = confidence
    obj["evidence"] = evidence
    return obj


def beam(name, a, b, radius, coll, material, confidence="DOCUMENTED", evidence=""):
    a, b = Vector(a), Vector(b)
    delta = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=radius, depth=delta.length, location=(a + b) / 2)
    obj = bpy.context.object
    obj.name = name
    # A Y-axis beam is parallel to the usual up hint, which makes Blender's
    # track quaternion degenerate.  Switch the hint for lateral members.
    up_axis = "X" if abs(delta.normalized().y) > 0.98 else "Y"
    obj.rotation_euler = delta.to_track_quat("Z", up_axis).to_euler()
    obj.data.materials.append(material)
    move_to(obj, coll)
    return mark(obj, confidence, evidence)


def rounded_box(name, location, scale, coll, material, bevel=0.008, confidence="DOCUMENTED", evidence=""):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    modifier = obj.modifiers.new("edge_round", "BEVEL")
    modifier.width = bevel
    modifier.segments = 3
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.data.materials.append(material)
    move_to(obj, coll)
    return mark(obj, confidence, evidence)


def panel_between(name, a, b, width_y, thickness, coll, material, confidence, evidence):
    a, b = Vector(a), Vector(b)
    direction = (b - a).normalized()
    normal = Vector((-direction.z, 0, direction.x))
    y = Vector((0, width_y / 2, 0))
    n = normal * thickness / 2
    verts = []
    for point in (a, b):
        verts.extend([point - y - n, point + y - n, point + y + n, point - y + n])
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5),
        (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0),
    ]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    coll.objects.link(obj)
    obj.data.materials.append(material)
    return mark(obj, confidence, evidence)


def cylinder_axis_y(name, location, radius, depth, coll, material, confidence="DOCUMENTED", evidence=""):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth, location=location, rotation=(math.pi / 2, 0, 0))
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    move_to(obj, coll)
    return mark(obj, confidence, evidence)


def wheel(name, location, radius, coll, tire_mat, spoke_mat, inferred=False):
    evidence = "official input view-03 tri-spoke wheel; video frames 731,1166-1206"
    root = empty(name, location, coll, "INFERRED" if inferred else "DOCUMENTED")
    root["evidence"] = evidence
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius * 0.80,
        minor_radius=radius * 0.13,
        major_segments=36,
        minor_segments=10,
        location=location,
        rotation=(math.pi / 2, 0, 0),
    )
    tire = bpy.context.object
    tire.name = name + "_Tire"
    tire.data.materials.append(tire_mat)
    move_to(tire, coll)
    parent_keep_world(tire, root)
    cylinder_axis_y(name + "_Hub", location, radius * 0.22, 0.052, coll, tire_mat, evidence=evidence)
    hub = bpy.context.object
    parent_keep_world(hub, root)
    for index, angle in enumerate((0, 2 * math.pi / 3, 4 * math.pi / 3), 1):
        endpoint = Vector(location) + Vector((math.cos(angle) * radius * 0.64, 0, math.sin(angle) * radius * 0.64))
        spoke = beam(name + f"_Spoke{index}", location, endpoint, radius * 0.075, coll, spoke_mat, evidence=evidence)
        parent_keep_world(spoke, root)
    return root


def canopy_surface(coll, material, root):
    # Five documented envelope stations from the open product views; the soft
    # fabric between ribs is simplified and its deformation remains inferred.
    stations = [
        (0.145, 0.845), (0.115, 0.995), (0.045, 1.092),
        (-0.065, 1.045), (-0.155, 0.945),
    ]
    half_width = 0.205
    verts = []
    for x, z in stations:
        verts.extend([(x, -half_width, z), (x, half_width, z)])
    faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(stations) - 1)]
    mesh = bpy.data.meshes.new("CanopyFabricMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("CanopyFabric", mesh)
    coll.objects.link(obj)
    obj.data.materials.append(material)
    solid = obj.modifiers.new("fabric_thickness", "SOLIDIFY")
    solid.thickness = 0.006
    bevel = obj.modifiers.new("soft_edges", "BEVEL")
    bevel.width = 0.008
    bevel.segments = 3
    mark(obj, "INFERRED", "visible open/collapsed canopy envelopes; linkage and fabric deformation inferred")
    parent_keep_world(obj, root)
    for index, (x, z) in enumerate(stations):
        rib = beam(f"Canopy_Rib_{index + 1}", (x, -half_width, z), (x, half_width, z), 0.006, coll, material, "INFERRED", "visible canopy ribs approximated from official views")
        parent_keep_world(rib, root)


def world_bbox(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH" or obj.hide_render:
            continue
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return lo, hi


def setup_qa_render(qa_coll, geometry_coll):
    floor_mat = mat("QA_Floor", (0.70, 0.78, 0.84), roughness=0.9)
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.005))
    floor = bpy.context.object
    floor.name = "QA_Floor"
    floor.data.materials.append(floor_mat)
    move_to(floor, qa_coll)
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.90, 0.95, 0.98, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.75
    key_data = bpy.data.lights.new("QA_Key", "AREA")
    key_data.energy = 850
    key_data.shape = "DISK"
    key_data.size = 4
    key = bpy.data.objects.new("QA_Key", key_data)
    qa_coll.objects.link(key)
    key.location = (-2.4, -3.2, 4.0)
    fill_data = bpy.data.lights.new("QA_Fill", "AREA")
    fill_data.energy = 500
    fill_data.size = 3
    fill = bpy.data.objects.new("QA_Fill", fill_data)
    qa_coll.objects.link(fill)
    fill.location = (2.5, 1.8, 2.2)
    cam_data = bpy.data.cameras.new("QA_Camera")
    cam = bpy.data.objects.new("QA_Camera", cam_data)
    qa_coll.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.data.lens = 58
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 768
    scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    return cam


def aim(cam, location, target):
    cam.location = location
    cam.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def render(path):
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    QA_DIR.mkdir(parents=True, exist_ok=True)
    if sha256(GLB) != GLB_SHA256:
        raise SystemExit("Tripo scaffold hash mismatch")
    clear_scene()
    reference = new_collection("REFERENCE_SCAFFOLD_INTERNAL_ONLY")
    geometry = new_collection("TWIN_GEOMETRY")
    qa = new_collection("QA_ONLY")

    black = mat("Frame_Black", (0.025, 0.032, 0.04), metallic=0.5, roughness=0.32)
    dark = mat("Plastic_Dark", (0.04, 0.05, 0.06), roughness=0.42)
    gray = mat("Kingston_Gray", (0.34, 0.36, 0.39), roughness=0.82)
    gray_light = mat("Kingston_Light", (0.54, 0.56, 0.59), roughness=0.9)
    tan = mat("Grip_Tan", (0.40, 0.18, 0.07), roughness=0.68)
    silver = mat("Wheel_Silver", (0.55, 0.58, 0.62), metallic=0.65, roughness=0.25)
    blue = mat("Control_Blue", (0.04, 0.25, 0.58), metallic=0.1, roughness=0.4)
    basket_mat = mat("Basket_INFERRED", (0.035, 0.04, 0.045), roughness=0.9, alpha=0.82)

    bpy.ops.import_scene.gltf(filepath=str(GLB))
    scaffold = next(obj for obj in bpy.context.selected_objects if obj.type == "MESH")
    scaffold.name = "REFERENCE_TripoProbe01_DO_NOT_RENDER"
    move_to(scaffold, reference)
    scaffold.hide_render = True
    scaffold.hide_viewport = True
    scaffold["run_id"] = "tripo-probe-01"
    scaffold["pack_hash"] = PACK_HASH
    scaffold["glb_sha256"] = GLB_SHA256
    scaffold["license_status"] = "OPEN_INTERNAL_ONLY"

    rig_root = empty("RigRoot", (0, 0, 0), geometry)
    rear_root = empty("RearFrame_ROOT", (0.0, 0, 0.52), geometry)
    front_root = empty("FrontFrame_ROOT", (0.0, 0, 0.52), geometry)
    lower_handle_root = empty("LowerHandle_ROOT", (0.0, 0, 0.52), geometry)
    upper_handle_root = empty("UpperHandle_ROOT", (0.17, 0, 0.79), geometry)
    seat_root = empty("SeatUnit_ROOT", (-0.01, 0, 0.53), geometry, "INFERRED")
    canopy_root = empty("Canopy_ROOT", (0.145, 0, 0.845), geometry, "INFERRED")
    belly_root = empty("BellyBar_ROOT", (-0.02, 0, 0.59), geometry)
    cup_root = empty("CupHolder_ROOT", (0.14, -0.205, 0.80), geometry, "INFERRED")
    for child in (rear_root, front_root, lower_handle_root, upper_handle_root, seat_root, canopy_root, belly_root, cup_root):
        parent_keep_world(child, rig_root)

    hub_evidence = "US20220169297A1 figs 1-2,5-11; video frames 1166-1206"
    for side, y in (("L", -0.205), ("R", 0.205)):
        hub = cylinder_axis_y(f"Hub112_{side}", (0, y, 0.52), 0.052, 0.038, geometry, dark, evidence=hub_evidence)
        parent_keep_world(hub, rear_root)
        rear_leg = beam(f"RearLeg110_{side}", (0, y, 0.52), (0.28, y, 0.09), 0.014, geometry, black, evidence=hub_evidence)
        parent_keep_world(rear_leg, rear_root)
        front_leg = beam(f"FrontLeg108_{side}", (0, y, 0.52), (-0.28, y, 0.075), 0.014, geometry, black, evidence=hub_evidence)
        parent_keep_world(front_leg, front_root)
        lower = beam(f"LowerHandle124_{side}", (0, y, 0.52), (0.17, y, 0.79), 0.014, geometry, black, evidence=hub_evidence)
        parent_keep_world(lower, lower_handle_root)
        upper = beam(f"UpperHandle120_{side}", (0.17, y, 0.79), (0.235, y, 0.995), 0.014, geometry, black, evidence="US20220169297A1 figs 3-5; video frames 1173-1186")
        parent_keep_world(upper, upper_handle_root)
        pivot = cylinder_axis_y(f"HandlePivot118_{side}", (0.17, y, 0.79), 0.027, 0.04, geometry, dark, evidence="US20220169297A1 part 118")
        parent_keep_world(pivot, lower_handle_root)

    parent_keep_world(beam("RearAxle", (0.28, -0.235, 0.075), (0.28, 0.235, 0.075), 0.009, geometry, black, "INFERRED", "rear axle surface minimally inferred from official views"), rear_root)
    parent_keep_world(beam("FrontCrossbar", (-0.28, -0.205, 0.16), (-0.28, 0.205, 0.16), 0.010, geometry, black, evidence="official front view and video"), front_root)

    wheel_fl = wheel("Wheel_FL", (-0.28, -0.235, 0.065), 0.065, geometry, dark, silver)
    wheel_fr = wheel("Wheel_FR", (-0.28, 0.235, 0.065), 0.065, geometry, dark, silver)
    wheel_rl = wheel("Wheel_RL", (0.28, -0.235, 0.075), 0.075, geometry, dark, silver, inferred=True)
    wheel_rr = wheel("Wheel_RR", (0.28, 0.235, 0.075), 0.075, geometry, dark, silver, inferred=True)
    for root in (wheel_fl, wheel_fr):
        parent_keep_world(root, front_root)
    for root in (wheel_rl, wheel_rr):
        parent_keep_world(root, rear_root)

    grip = beam("HandleGrip", (0.235, -0.205, 0.995), (0.235, 0.205, 0.995), 0.021, geometry, tan, evidence="official Kingston views and video control close-up")
    parent_keep_world(grip, upper_handle_root)
    housing = rounded_box("ControlHousing126", (0.235, 0, 0.995), (0.038, 0.055, 0.025), geometry, dark, 0.012, evidence="manual p.34; patent part 126; video frame 1127")
    switch = rounded_box("ThumbSwitch", (0.235, 0, 1.024), (0.018, 0.023, 0.007), geometry, blue, 0.004, evidence="claim_r2j_step_fold_4; video frames 1127-1153")
    lever = rounded_box("SqueezeLever", (0.235, 0, 0.965), (0.027, 0.033, 0.007), geometry, blue, 0.004, evidence="claim_r2j_step_fold_5; video frames 1127-1153")
    for obj in (housing, switch, lever):
        parent_keep_world(obj, upper_handle_root)

    seat_back = panel_between("SeatBack", (-0.015, 0, 0.52), (0.13, 0, 0.88), 0.35, 0.045, geometry, gray, "INFERRED", "visible pose in official views/video; exact linkage not documented")
    seat_base = panel_between("SeatBase", (-0.20, 0, 0.44), (-0.015, 0, 0.52), 0.35, 0.045, geometry, gray_light, "INFERRED", "visible seat envelope")
    calf = panel_between("CalfSupport", (-0.255, 0, 0.34), (-0.20, 0, 0.44), 0.34, 0.035, geometry, gray_light, "INFERRED", "visible calf-support envelope")
    for obj in (seat_back, seat_base, calf):
        parent_keep_world(obj, seat_root)

    canopy_surface(geometry, gray, canopy_root)

    for side, y in (("L", -0.18), ("R", 0.18)):
        arm = beam(f"BellyBarArm_{side}", (-0.02, y, 0.59), (-0.135, y, 0.665), 0.013, geometry, dark, evidence="manual p.35 carry handle; official views")
        parent_keep_world(arm, belly_root)
    belly_grip = beam("BellyBarGrip", (-0.135, -0.18, 0.665), (-0.135, 0.18, 0.665), 0.018, geometry, dark, evidence="claim_r2j_step_fold_7; manual p.35")
    parent_keep_world(belly_grip, belly_root)

    basket = rounded_box("Basket_INFERRED", (0.015, 0, 0.245), (0.22, 0.185, 0.055), geometry, basket_mat, 0.035, "INFERRED", "visible basket envelope; rear/unseen surfaces minimal")
    parent_keep_world(basket, rear_root)

    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=0.043, depth=0.085, location=(0.14, -0.230, 0.775))
    cup = bpy.context.object
    cup.name = "CupHolder_INFERRED"
    cup.data.materials.append(dark)
    move_to(cup, geometry)
    mark(cup, "INFERRED", "official views and optional fold tip; mount and wall details simplified")
    parent_keep_world(cup, cup_root)

    # Provenance and governing state live in the saved scene as well as JSON.
    scene = bpy.context.scene
    scene["poc"] = "POC 6 articulated Ready2Jet"
    scene["stage"] = "B geometry"
    scene["internal_only"] = True
    scene["license_status"] = "Tripo3D OPEN - DO NOT SHIP"
    scene["scaffold_run_id"] = "tripo-probe-01"
    scene["scaffold_pack_hash"] = PACK_HASH
    scene["scaffold_glb_sha256"] = GLB_SHA256
    scene["geometry_strategy"] = "parametric rebuild over hidden Tripo scaffold"

    lo, hi = world_bbox(list(geometry.objects))
    size = hi - lo
    error_pct = [100 * (size[i] - TARGET_DWH_M[i]) / TARGET_DWH_M[i] for i in range(3)]
    report = {
        "blender_version": bpy.app.version_string,
        "strategy": "B2 rebuild",
        "scaffold": {"run_id": "tripo-probe-01", "pack_hash": PACK_HASH, "glb_sha256": GLB_SHA256},
        "target_open_dimensions_m_DWH": TARGET_DWH_M,
        "geometry_bbox_min_xyz": list(lo),
        "geometry_bbox_max_xyz": list(hi),
        "geometry_dimensions_m_DWH": list(size),
        "open_dimension_error_percent_DWH": error_pct,
        "mesh_object_count": sum(1 for o in geometry.objects if o.type == "MESH"),
        "named_roots": [o.name for o in geometry.objects if o.type == "EMPTY"],
        "required_parts": {
            "front_and_rear_frame": True,
            "handle_with_controls": True,
            "seat_backrest": True,
            "canopy_fold_relevant": True,
            "four_tri_spoke_wheels": True,
            "basket_simplified": True,
            "belly_bar": True,
            "cup_holder": True,
        },
        "inferred_objects": sorted(o.name for o in geometry.objects if o.get("confidence") == "INFERRED"),
        "external_spend_usd": 0,
        "internal_only": True,
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2) + "\n")

    cam = setup_qa_render(qa, geometry)
    aim(cam, (-1.35, -1.25, 1.15), (0, 0, 0.52))
    render(QA_DIR / "open-three-quarter.png")
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 1.3
    aim(cam, (0, -2.2, 0.55), (0, 0, 0.55))
    render(QA_DIR / "open-side.png")
    cam.data.type = "PERSP"
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
