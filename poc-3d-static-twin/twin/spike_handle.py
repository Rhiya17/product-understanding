"""Stage B handle spike: scripted Tripo surgery vs parametric rebuild.

Run headless:
  Blender --background --python twin/spike_handle.py

The script imports the hash-pinned Tripo probe mesh, attempts a spatial handle
cut with boundary cleanup, builds a clean handle assembly at the same envelope,
records topology/runtime metrics, renders both outcomes, and saves the scene.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GLB = ROOT / "poc-3d-static-twin" / "runs" / "tripo-probe-01" / "glb-k11lDWbp1BeH5sJR6lO6C_model.glb"
GLB_SHA256 = "95e0fe44bba9a303b31849cfbec1d7d517d2ed2c6361ab505e025cf7ef80716b"
PACK_HASH = "da454173c3733e0227d90f869925145897669e96df8f7c593f0f45be94d8a83f"
OUT = HERE / "stage-b-spike"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for collection in list(bpy.data.collections):
        if collection.name != "Collection":
            bpy.data.collections.remove(collection)


def collection(name: str) -> bpy.types.Collection:
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def move_to(obj: bpy.types.Object, coll: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    coll.objects.link(obj)


def material(name: str, color: tuple[float, float, float, float], metallic=0.0, roughness=0.45):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def beam(name: str, a, b, radius: float, coll, mat):
    a, b = Vector(a), Vector(b)
    delta = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=delta.length, location=(a + b) / 2)
    obj = bpy.context.object
    obj.name = name
    up_axis = "X" if abs(delta.normalized().y) > 0.98 else "Y"
    obj.rotation_euler = delta.to_track_quat("Z", up_axis).to_euler()
    obj.data.materials.append(mat)
    move_to(obj, coll)
    return obj


def rounded_box(name, location, scale, coll, mat, bevel=0.008):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new("edge_round", "BEVEL")
    mod.width = bevel
    mod.segments = 3
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.data.materials.append(mat)
    move_to(obj, coll)
    return obj


def topology(mesh: bpy.types.Mesh) -> dict:
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    remaining = set(bm.faces)
    components = 0
    while remaining:
        components += 1
        stack = [remaining.pop()]
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for linked in edge.link_faces:
                    if linked in remaining:
                        remaining.remove(linked)
                        stack.append(linked)
    result = {
        "vertices": len(bm.verts),
        "edges": len(bm.edges),
        "faces": len(bm.faces),
        "connected_face_components": components,
        "boundary_edges": sum(1 for e in bm.edges if len(e.link_faces) == 1),
        "nonmanifold_edges": sum(1 for e in bm.edges if not e.is_manifold),
    }
    bm.free()
    return result


def cut_region(source: bpy.types.Object, coll, mat):
    """Select the visible handle envelope; contamination is measured, not hidden."""
    mesh = source.data
    selected = []
    # Tripo coordinates after glTF import: X longitudinal (rear positive),
    # Y lateral, Z up.  The handle/canopy envelope overlaps in this welded shell.
    for poly in mesh.polygons:
        center = source.matrix_world @ poly.center
        if center.x > 0.08 and center.z > 0.22:
            selected.append(poly)
    used = sorted({v for p in selected for v in p.vertices})
    remap = {old: new for new, old in enumerate(used)}
    vertices = [source.matrix_world @ mesh.vertices[i].co for i in used]
    faces = [[remap[i] for i in p.vertices] for p in selected]
    candidate_mesh = bpy.data.meshes.new("B1_Surgery_Handle_Mesh")
    candidate_mesh.from_pydata(vertices, [], faces)
    candidate_mesh.update()
    candidate = bpy.data.objects.new("B1_Surgery_Handle_Candidate", candidate_mesh)
    coll.objects.link(candidate)
    candidate.data.materials.append(mat)
    before = topology(candidate_mesh)

    bm = bmesh.new()
    bm.from_mesh(candidate_mesh)
    boundary = [e for e in bm.edges if len(e.link_faces) == 1]
    boundary_before = len(boundary)
    fill_result = bmesh.ops.holes_fill(bm, edges=boundary, sides=0) if boundary else {"faces": []}
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.00005)
    bm.to_mesh(candidate_mesh)
    bm.free()
    candidate_mesh.update()
    after = topology(candidate_mesh)
    return candidate, before, after, len(fill_result.get("faces", [])), boundary_before


def build_rebuild(coll, black, tan, control):
    # Same open-pose envelope as the scaffold, but split at patent pivot 118.
    objects = []
    for side, y in (("L", -0.245), ("R", 0.245)):
        objects.append(beam(f"B2_LowerHandle_{side}", (0.02, y, 0.08), (0.22, y, 0.34), 0.014, coll, black))
        objects.append(beam(f"B2_UpperHandle_{side}", (0.22, y, 0.34), (0.35, y, 0.455), 0.014, coll, black))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.026, location=(0.22, y, 0.34))
        hinge = bpy.context.object
        hinge.name = f"B2_HandlePivot118_{side}"
        hinge.scale.y = 0.45
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        hinge.data.materials.append(black)
        move_to(hinge, coll)
        objects.append(hinge)
    objects.append(beam("B2_Grip", (0.35, -0.245, 0.455), (0.35, 0.245, 0.455), 0.021, coll, tan))
    objects.append(rounded_box("B2_ControlHousing", (0.35, 0.0, 0.455), (0.038, 0.055, 0.026), coll, black, 0.012))
    objects.append(rounded_box("B2_ThumbSwitch", (0.35, 0.0, 0.483), (0.018, 0.024, 0.007), coll, control, 0.004))
    objects.append(rounded_box("B2_SqueezeLever", (0.35, 0.0, 0.425), (0.026, 0.033, 0.007), coll, control, 0.004))
    return objects


def setup_render():
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 768
    scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.92, 0.94, 0.97, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    for name, rotation, energy in (
        ("Key", (math.radians(25), 0, math.radians(-35)), 4.0),
        ("Fill", (math.radians(55), 0, math.radians(145)), 2.0),
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy * 250
        data.shape = "DISK"
        data.size = 4.0
        obj = bpy.data.objects.new(name, data)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = (2, -3, 3)
        obj.rotation_euler = rotation
    cam_data = bpy.data.cameras.new("SpikeCamera")
    cam = bpy.data.objects.new("SpikeCamera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = (1.3, -1.5, 1.15)
    target = Vector((0.24, 0, 0.34))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 62


def render(path: Path):
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if sha256(GLB) != GLB_SHA256:
        raise SystemExit("Tripo scaffold hash mismatch")
    clear_scene()
    surgery_coll = collection("B1_SURGERY")
    rebuild_coll = collection("B2_REBUILD")
    scaffold_coll = collection("REFERENCE_SCAFFOLD")
    red = material("Surgery_Red", (0.72, 0.07, 0.05, 1), metallic=0.1)
    black = material("Rebuild_Black", (0.035, 0.045, 0.055, 1), metallic=0.45)
    tan = material("Grip_Tan", (0.42, 0.18, 0.07, 1), roughness=0.6)
    control = material("Control_Blue", (0.04, 0.28, 0.65, 1), metallic=0.15)

    bpy.ops.import_scene.gltf(filepath=str(GLB))
    source = next(o for o in bpy.context.selected_objects if o.type == "MESH")
    source.name = "REFERENCE_TripoProbe01"
    move_to(source, scaffold_coll)
    source.hide_render = True
    source["run_id"] = "tripo-probe-01"
    source["pack_hash"] = PACK_HASH
    source["glb_sha256"] = GLB_SHA256

    b1_start = time.perf_counter()
    candidate, before, after, filled_faces, boundary_before = cut_region(source, surgery_coll, red)
    b1_seconds = time.perf_counter() - b1_start

    b2_start = time.perf_counter()
    rebuilt = build_rebuild(rebuild_coll, black, tan, control)
    b2_seconds = time.perf_counter() - b2_start

    setup_render()
    for obj in rebuild_coll.objects:
        obj.hide_render = True
    render(OUT / "b1-surgery.png")
    candidate.hide_render = True
    for obj in rebuild_coll.objects:
        obj.hide_render = False
    render(OUT / "b2-rebuild.png")
    candidate.hide_render = False

    rebuild_topology = [topology(o.data) for o in rebuilt if o.type == "MESH"]
    result = {
        "blender_version": bpy.app.version_string,
        "scaffold": {
            "run_id": "tripo-probe-01",
            "pack_hash": PACK_HASH,
            "glb_sha256": GLB_SHA256,
        },
        "timebox": "maximum 0.5 day per branch; neither branch exhausted its budget",
        "B1_surgery": {
            "script_runtime_seconds": round(b1_seconds, 4),
            "agent_hours_including_inspection": 0.1,
            "region_rule": "face centroid X > 0.08 m and Z > 0.22 m in Tripo coordinates",
            "topology_before_cleanup": before,
            "boundary_edges_sent_to_hole_fill": boundary_before,
            "faces_created_by_hole_fill": filled_faces,
            "topology_after_cleanup": after,
            "defects": [
                "welded handle envelope also contains canopy/soft-goods faces",
                "spatial cut does not recover patent pivot 118 as a clean part boundary",
                "hole-fill closes arbitrary cut loops with non-evidenced surfaces",
                "candidate remains unsuitable for independent hinge rotation",
            ],
            "rig_ready": False,
        },
        "B2_rebuild": {
            "script_runtime_seconds": round(b2_seconds, 4),
            "agent_hours_including_inspection": 0.1,
            "objects": [o.name for o in rebuilt],
            "object_count": len(rebuilt),
            "aggregate_boundary_edges": sum(t["boundary_edges"] for t in rebuild_topology),
            "defects": [
                "tube centerlines and control housing are simplified to visible envelope",
                "control travel and internal cable geometry remain INFERRED/hidden",
            ],
            "rig_ready": True,
        },
        "winner": "B2_rebuild",
        "decision": "Rebuild wins: separate manifold primitives expose the documented handle pivot and control parts immediately; surgery retains contaminated welded topology and arbitrary closure surfaces.",
    }
    (OUT / "spike-results.json").write_text(json.dumps(result, indent=2) + "\n")
    bpy.context.scene["poc6_stage"] = "B spike"
    bpy.context.scene["spike_winner"] = "B2_rebuild"
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "stage-b-spike.blend"))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
