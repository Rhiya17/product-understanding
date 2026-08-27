"""Stage S: bind the hash-pinned Tripo scan to the evidence-mapped rig.

The object rig remains the sole motion authority.  This script adds an
armature whose bones copy the evaluated transforms of the existing rig
objects; it does not add or change motion, pivots, axes, action curves, or
defect controls.  The fused photo-derived shell is aligned once, then
weighted reproducibly by nearest proxy part with a 3 cm decision-boundary
smoothing band.  Wheels, handle parts, controls, belly bar, and cup holder
remain fully rigid.

INTERNAL ONLY: the Tripo3D commercial-license check is open.

Usage:
  Blender --background --python skin_twin.py
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


HERE = Path(__file__).resolve().parent
SOURCE_BLEND = HERE / "ready2jet-rigged.blend"
OUT_BLEND = HERE / "ready2jet-skinned.blend"
OUT_REPORT = HERE / "skinning-report.json"
SCAN_OBJECT = "REFERENCE_TripoProbe01_DO_NOT_RENDER"
SKIN_OBJECT = "Ready2Jet_PhotoSkin_INTERNAL_ONLY"
ARMATURE_OBJECT = "Ready2Jet_SkinArmature_INTERNAL_ONLY"
SKIN_COLLECTION = "SKINNED_TWIN_INTERNAL_ONLY"
SMOOTHING_BAND_M = 0.03
RIGHTS_NOTE = "Tripo3D license check OPEN — do not ship"


# All deforming bones are driven from existing evaluated rig objects.  The
# three validation-only controls ensure the visible handle-release defect and
# latch-state defect remain testable even though the scan has no separable
# switch/lever geometry.
BONE_SPECS = {
    "rig_root": {"target": "RigRoot", "parent": None},
    "rear_frame": {"target": "RearFrame_ROOT", "parent": "rig_root"},
    "front_frame": {"target": "FrontFrame_ROOT", "parent": "rig_root"},
    "lower_handle": {"target": "LowerHandle_ROOT", "parent": "rig_root"},
    "upper_handle": {"target": "UpperHandle_ROOT", "parent": "lower_handle"},
    "seat_unit": {"target": "SeatUnit_ROOT", "parent": "rig_root"},
    "canopy": {"target": "Canopy_ROOT", "parent": "seat_unit"},
    "belly_bar": {"target": "BellyBar_ROOT", "parent": "seat_unit"},
    "cup_holder": {"target": "CupHolder_ROOT", "parent": "lower_handle"},
    "basket": {"target": "Basket_INFERRED", "parent": "rear_frame"},
    "wheel_FL": {"target": "Wheel_FL", "parent": "front_frame"},
    "wheel_FR": {"target": "Wheel_FR", "parent": "front_frame"},
    "wheel_RL": {"target": "Wheel_RL", "parent": "rear_frame"},
    "wheel_RR": {"target": "Wheel_RR", "parent": "rear_frame"},
    "thumb_switch_validation": {"target": "ThumbSwitch", "parent": "upper_handle", "deform": False},
    "squeeze_lever_validation": {"target": "SqueezeLever", "parent": "upper_handle", "deform": False},
}


# Proxy surfaces are the evidence-mapped Stage B geometry.  They classify
# scan vertices only; they are hidden from Stage S renders after binding.
PROXY_OBJECTS = {
    "rear_frame": ["Hub112_L", "Hub112_R", "RearLeg110_L", "RearLeg110_R", "RearAxle"],
    "front_frame": ["FrontLeg108_L", "FrontLeg108_R", "FrontCrossbar"],
    "lower_handle": ["LowerHandle124_L", "LowerHandle124_R", "HandlePivot118_L", "HandlePivot118_R"],
    "upper_handle": ["UpperHandle120_L", "UpperHandle120_R", "HandleGrip", "ControlHousing126", "ThumbSwitch", "SqueezeLever"],
    "seat_unit": ["SeatBack", "SeatBase", "CalfSupport"],
    "canopy": ["CanopyFabric", "Canopy_Rib_1", "Canopy_Rib_2", "Canopy_Rib_3", "Canopy_Rib_4", "Canopy_Rib_5"],
    "belly_bar": ["BellyBarArm_L", "BellyBarArm_R", "BellyBarGrip"],
    "cup_holder": ["CupHolder_INFERRED"],
    "basket": ["Basket_INFERRED"],
    "wheel_FL": ["Wheel_FL_Tire", "Wheel_FL_Hub", "Wheel_FL_Spoke1", "Wheel_FL_Spoke2", "Wheel_FL_Spoke3"],
    "wheel_FR": ["Wheel_FR_Tire", "Wheel_FR_Hub", "Wheel_FR_Spoke1", "Wheel_FR_Spoke2", "Wheel_FR_Spoke3"],
    "wheel_RL": ["Wheel_RL_Tire", "Wheel_RL_Hub", "Wheel_RL_Spoke1", "Wheel_RL_Spoke2", "Wheel_RL_Spoke3"],
    "wheel_RR": ["Wheel_RR_Tire", "Wheel_RR_Hub", "Wheel_RR_Spoke1", "Wheel_RR_Spoke2", "Wheel_RR_Spoke3"],
}


FORCE_RIGID = {
    "lower_handle", "upper_handle", "belly_bar", "cup_holder",
    "wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR",
}


# Compact hard-surface features need spatial masks because the fused provider
# shell can put a wheel surface closer to a leg proxy (or the cup wall closer
# to the handle) than to its own simplified proxy.  These are rest-pose masks,
# not geometry edits; their centers/radii come directly from the existing rig.
RIGID_OVERRIDE_SPHERES = (
    {"bone": "wheel_FL", "center": (-0.28, -0.235, 0.065), "radius_m": 0.105, "reason": "aligned scan feature is close to documented caster pivot"},
    {"bone": "wheel_RL", "center": (0.28, -0.235, 0.075), "radius_m": 0.115, "reason": "aligned scan feature is close to documented rear-wheel pivot"},
    {"bone": "front_frame", "center": (-0.267, 0.064, 0.114), "radius_m": 0.09, "reason": "provider reconstruction collapsed far-side wheel inward; rigidly follow its documented parent instead of orbiting around an invented corrected pivot"},
    {"bone": "rear_frame", "center": (0.156, 0.010, 0.122), "radius_m": 0.09, "reason": "provider reconstruction collapsed far-side wheel inward; rigidly follow its documented parent instead of orbiting around an invented corrected pivot"},
    {"bone": "lower_handle", "center": (0.14, 0.15, 0.775), "radius_m": 0.055, "reason": "provider reconstruction places the cup-side surface away from the documented cup pivot; rigid parent mask avoids invented alignment"},
)


# Only these fused-shell transition bands are allowed to blend.  The handle,
# wheels, cup holder, and belly bar are intentionally absent because the work
# order requires their weights to remain rigid.
SMOOTHING_JOINTS = (
    {"name": "front_frame_about_hub112", "bones": ("front_frame", "rear_frame"), "pivot": (0.0, 0.0, 0.52), "axis": (0.0, 1.0, 0.0)},
    {"name": "seat_follow", "bones": ("seat_unit", "rear_frame"), "pivot": (-0.01, 0.0, 0.53), "axis": (0.0, 1.0, 0.0)},
    {"name": "canopy_fold", "bones": ("canopy", "seat_unit"), "pivot": (0.145, 0.0, 0.845), "axis": (0.0, 1.0, 0.0)},
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_rows(matrix: Matrix) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def ensure_clean_output_names() -> None:
    for name in (SKIN_OBJECT, ARMATURE_OBJECT):
        obj = bpy.data.objects.get(name)
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)
    collection = bpy.data.collections.get(SKIN_COLLECTION)
    if collection is not None:
        bpy.data.collections.remove(collection)


def add_skin_collection() -> bpy.types.Collection:
    collection = bpy.data.collections.new(SKIN_COLLECTION)
    bpy.context.scene.collection.children.link(collection)
    collection["internal_only"] = True
    collection["rights_note"] = RIGHTS_NOTE
    return collection


def aligned_skin(collection: bpy.types.Collection) -> tuple[bpy.types.Object, dict]:
    reference = bpy.data.objects.get(SCAN_OBJECT)
    if reference is None or reference.type != "MESH":
        raise SystemExit(f"missing mesh scaffold {SCAN_OBJECT}")

    skin = reference.copy()
    skin.data = reference.data.copy()
    skin.name = SKIN_OBJECT
    skin.data.name = f"{SKIN_OBJECT}_Mesh"
    collection.objects.link(skin)
    skin.hide_render = False
    skin.hide_viewport = False
    skin.hide_set(False)

    world_points = [reference.matrix_world @ Vector(corner) for corner in reference.bound_box]
    low = Vector(tuple(min(point[i] for point in world_points) for i in range(3)))
    high = Vector(tuple(max(point[i] for point in world_points) for i in range(3)))
    center = (low + high) / 2.0

    # Pose/scale the statue into the rig's evidence-mapped rest envelope.  A
    # per-axis fit is intentional and disclosed: Tripo auto_size missed the
    # official dimensions by up to ~13%, and an unscaled scan leaves its wheel
    # centers outside the mechanism pivots.  Axis directions and the baked
    # lean are retained; no vertex-level geometry is invented or edited.
    rig_meshes = [
        obj for obj in bpy.data.collections["TWIN_GEOMETRY"].objects
        if obj.type == "MESH" and not obj.name.startswith("REFERENCE_")
    ]
    rig_points = [obj.matrix_world @ Vector(corner) for obj in rig_meshes for corner in obj.bound_box]
    rig_low = Vector(tuple(min(point[i] for point in rig_points) for i in range(3)))
    rig_high = Vector(tuple(max(point[i] for point in rig_points) for i in range(3)))
    rig_center = (rig_low + rig_high) / 2.0
    source_size = high - low
    rig_size = rig_high - rig_low
    scale = Vector(tuple(rig_size[i] / source_size[i] for i in range(3)))
    scale_matrix = Matrix.Diagonal((scale.x, scale.y, scale.z, 1.0))
    translation = rig_center - Vector((scale.x * center.x, scale.y * center.y, scale.z * center.z))
    alignment = Matrix.Translation(translation) @ scale_matrix
    skin.matrix_world = alignment @ reference.matrix_world
    applied = skin.matrix_world.copy()

    # Bake the near-identity translation into the private duplicate only.
    bpy.context.view_layer.objects.active = skin
    skin.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    skin.select_set(False)
    skin["source_object"] = SCAN_OBJECT
    skin["source_run_id"] = "tripo-probe-01"
    skin["internal_only"] = True
    skin["rights_note"] = RIGHTS_NOTE
    skin["alignment_transform_applied"] = json.dumps(matrix_rows(applied))

    aligned_points = [skin.matrix_world @ Vector(corner) for corner in skin.bound_box]
    aligned_low = [min(point[i] for point in aligned_points) for i in range(3)]
    aligned_high = [max(point[i] for point in aligned_points) for i in range(3)]
    report = {
        "method": "axis-preserving non-uniform bbox fit to the evidence-mapped rig rest envelope; baked scan lean retained",
        "source_matrix_world": matrix_rows(reference.matrix_world),
        "applied_matrix_world_before_bake": matrix_rows(applied),
        "source_bbox_min_xyz_m": list(low),
        "source_bbox_max_xyz_m": list(high),
        "rig_rest_bbox_min_xyz_m": list(rig_low),
        "rig_rest_bbox_max_xyz_m": list(rig_high),
        "applied_scale_xyz": list(scale),
        "aligned_bbox_min_xyz_m": aligned_low,
        "aligned_bbox_max_xyz_m": aligned_high,
    }
    return skin, report


def create_armature(collection: bpy.types.Collection) -> bpy.types.Object:
    scene = bpy.context.scene
    scene.frame_set(1)
    bpy.context.view_layer.update()

    arm_data = bpy.data.armatures.new(f"{ARMATURE_OBJECT}_Data")
    armature = bpy.data.objects.new(ARMATURE_OBJECT, arm_data)
    collection.objects.link(armature)
    armature.show_in_front = True
    armature["motion_authority"] = "existing object rig only"
    armature["internal_only"] = True
    armature["rights_note"] = RIGHTS_NOTE

    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for bone_name, spec in BONE_SPECS.items():
        target = bpy.data.objects[spec["target"]]
        head = target.matrix_world.translation.copy()
        bone = arm_data.edit_bones.new(bone_name)
        bone.head = head
        # Blender bones use local +Y from head to tail.  Keeping every edit
        # bone on +Y makes its rest rotation the identity, matching the
        # zero-rotation object roots and preventing a bind-pose offset when
        # the WORLD-space copy constraint first evaluates.
        bone.tail = head + Vector((0.0, 0.08, 0.0))
        bone.use_deform = spec.get("deform", True)
    for bone_name, spec in BONE_SPECS.items():
        if spec["parent"]:
            arm_data.edit_bones[bone_name].parent = arm_data.edit_bones[spec["parent"]]
            arm_data.edit_bones[bone_name].use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    for bone_name, spec in BONE_SPECS.items():
        constraint = armature.pose.bones[bone_name].constraints.new("COPY_TRANSFORMS")
        constraint.name = f"MotionAuthority_{spec['target']}"
        constraint.target = bpy.data.objects[spec["target"]]
        constraint.target_space = "WORLD"
        constraint.owner_space = "WORLD"
        constraint.mix_mode = "REPLACE"
    bpy.ops.object.mode_set(mode="OBJECT")
    armature.select_set(False)

    # State-only latch channel: a direct driver copy of the existing rig
    # property, used by the validator for defect_skip_latch.
    armature["effective_latch_state"] = 0.0
    fcurve = armature.driver_add('["effective_latch_state"]')
    driver = fcurve.driver
    driver.type = "SCRIPTED"
    driver.expression = "secure*(1-skip)"
    for name, data_path in (("secure", '["stage_secure"]'), ("skip", '["defect_skip_latch"]')):
        variable = driver.variables.new()
        variable.name = name
        variable.type = "SINGLE_PROP"
        variable.targets[0].id = bpy.data.objects["RigRoot"]
        variable.targets[0].data_path = data_path
    return armature


def combined_bvh(object_names: list[str], depsgraph) -> BVHTree:
    vertices: list[Vector] = []
    polygons: list[list[int]] = []
    for name in object_names:
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != "MESH":
            raise SystemExit(f"binding proxy missing: {name}")
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            offset = len(vertices)
            vertices.extend(evaluated.matrix_world @ vertex.co for vertex in mesh.vertices)
            polygons.extend([[offset + index for index in polygon.vertices] for polygon in mesh.polygons])
        finally:
            evaluated.to_mesh_clear()
    if not polygons:
        raise SystemExit(f"binding proxy has no faces: {object_names}")
    return BVHTree.FromPolygons(vertices, polygons, all_triangles=False)


def bind_weights(skin: bpy.types.Object, armature: bpy.types.Object) -> dict:
    scene = bpy.context.scene
    scene.frame_set(1)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    trees = {bone: combined_bvh(names, depsgraph) for bone, names in PROXY_OBJECTS.items()}
    groups = {bone: skin.vertex_groups.new(name=bone) for bone in PROXY_OBJECTS}
    primary_counts: Counter[str] = Counter()
    smoothed_pair_counts: Counter[str] = Counter()
    smoothed_vertices = 0

    distances_by_vertex: list[dict[str, float]] = []
    labels: list[str] = []
    rigid_override_locked: list[bool] = []
    rigid_override_counts: Counter[str] = Counter()
    for vertex in skin.data.vertices:
        point = skin.matrix_world @ vertex.co
        distances: list[tuple[float, str]] = []
        distance_map: dict[str, float] = {}
        for bone, tree in trees.items():
            nearest = tree.find_nearest(point)
            distance = float(nearest[3]) if nearest is not None else float("inf")
            distances.append((distance, bone))
            distance_map[bone] = distance
        distances.sort()
        distances_by_vertex.append(distance_map)
        label = distances[0][1]
        locked = False
        for override in RIGID_OVERRIDE_SPHERES:
            if (point - Vector(override["center"])).length <= override["radius_m"]:
                label = override["bone"]
                rigid_override_counts[label] += 1
                locked = True
                break
        labels.append(label)
        rigid_override_locked.append(locked)

    # Remove isolated nearest-surface label speckles, which otherwise turn
    # single triangles into long spikes.  Two deterministic 75%-neighbor
    # majority passes preserve large part regions and only regularize noisy
    # boundaries in the provider mesh.
    neighbors: list[list[int]] = [[] for _ in skin.data.vertices]
    for edge in skin.data.edges:
        a, b = edge.vertices
        neighbors[a].append(b)
        neighbors[b].append(a)
    relabeled_total = 0
    for _ in range(2):
        updated = list(labels)
        for index, adjacent in enumerate(neighbors):
            if not adjacent:
                continue
            counts = Counter(labels[other] for other in adjacent)
            dominant, count = counts.most_common(1)[0]
            threshold = max(3, math.ceil(0.75 * len(adjacent)))
            if (not rigid_override_locked[index] and dominant != labels[index] and count >= threshold
                    and dominant not in FORCE_RIGID and labels[index] not in FORCE_RIGID):
                updated[index] = dominant
                relabeled_total += 1
        labels = updated

    for vertex in skin.data.vertices:
        first_bone = labels[vertex.index]
        primary_counts[first_bone] += 1
        point = skin.matrix_world @ vertex.co
        blend = None
        if rigid_override_locked[vertex.index]:
            groups[first_bone].add([vertex.index], 1.0, "REPLACE")
            continue
        for joint in SMOOTHING_JOINTS:
            first, second = joint["bones"]
            if first_bone not in (first, second):
                continue
            pivot = Vector(joint["pivot"])
            axis = Vector(joint["axis"]).normalized()
            offset = point - pivot
            radial_distance = (offset - axis * offset.dot(axis)).length
            if radial_distance > SMOOTHING_BAND_M:
                continue
            other_bone = second if first_bone == first else first
            first_distance = distances_by_vertex[vertex.index][first_bone]
            other_distance = distances_by_vertex[vertex.index][other_bone]
            delta = abs(other_distance - first_distance)
            if delta >= SMOOTHING_BAND_M:
                continue
            other_weight = 0.5 * (1.0 - delta / SMOOTHING_BAND_M)
            blend = (other_bone, other_weight, joint["name"])
            break
        if blend is None:
            groups[first_bone].add([vertex.index], 1.0, "REPLACE")
            continue
        other_bone, other_weight, joint_name = blend
        groups[first_bone].add([vertex.index], 1.0 - other_weight, "REPLACE")
        groups[other_bone].add([vertex.index], other_weight, "REPLACE")
        smoothed_vertices += 1
        smoothed_pair_counts[joint_name] += 1

    modifier = skin.modifiers.new("EvidenceRig_Skin", "ARMATURE")
    modifier.object = armature
    modifier.use_vertex_groups = True
    modifier.use_deform_preserve_volume = False

    return {
        "method": "nearest evidence-mapped proxy surface",
        "smoothing_band_m": SMOOTHING_BAND_M,
        "smoothing_definition": "only declared hinge-axis bands blend: radial distance and the two proxy-distance difference must both be < 0.03 m",
        "smoothing_joints": list(SMOOTHING_JOINTS),
        "force_rigid_bones": sorted(FORCE_RIGID),
        "vertex_count": len(skin.data.vertices),
        "primary_vertex_counts": dict(sorted(primary_counts.items())),
        "smoothed_vertex_count": smoothed_vertices,
        "smoothed_vertex_fraction": smoothed_vertices / len(skin.data.vertices),
        "smoothed_pair_counts": dict(sorted(smoothed_pair_counts.items())),
        "topology_majority_relabels": relabeled_total,
        "rigid_override_spheres": list(RIGID_OVERRIDE_SPHERES),
        "rigid_override_vertex_counts": dict(sorted(rigid_override_counts.items())),
    }


def main() -> None:
    if not SOURCE_BLEND.exists():
        raise SystemExit(f"missing source rig: {SOURCE_BLEND}")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    scene = bpy.context.scene
    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        raise SystemExit("license guard changed; refusing to build Stage S")
    if scene.get("correct_action") != "Ready2Jet_Fold_Correct":
        raise SystemExit("motion authority action changed; refusing to build Stage S")

    ensure_clean_output_names()
    collection = add_skin_collection()
    skin, alignment_report = aligned_skin(collection)
    armature = create_armature(collection)
    binding_report = bind_weights(skin, armature)

    # The evidence-mapped proxy stays in the file for provenance/validation,
    # but only the photo-derived skin is visible in Stage S renders.
    for obj in bpy.data.collections["TWIN_GEOMETRY"].objects:
        if obj.type == "MESH":
            obj.hide_render = True

    scene["stage"] = "S skinned fold"
    scene["internal_only"] = True
    scene["external_publication_forbidden"] = True
    scene["rights_note"] = RIGHTS_NOTE
    scene["motion_authority"] = "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged"
    scene["skin_source_run_id"] = "tripo-probe-01"
    scene["skin_binding_script"] = "skin_twin.py"
    scene["skin_smoothing_band_m"] = SMOOTHING_BAND_M

    report = {
        "status": "BUILT_PENDING_VALIDATION",
        "blender_version": bpy.app.version_string,
        "source_rig": SOURCE_BLEND.name,
        "source_rig_sha256": sha256(SOURCE_BLEND),
        "source_scan_object": SCAN_OBJECT,
        "source_scan_run_id": "tripo-probe-01",
        "source_scan_glb_sha256": scene.get("scaffold_glb_sha256"),
        "output_blend": OUT_BLEND.name,
        "motion_authority": "existing object rig; pose bones COPY_TRANSFORMS in WORLD space",
        "action": "Ready2Jet_Fold_Correct",
        "defect_parameters": ["defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch"],
        "bone_targets": {bone: spec["target"] for bone, spec in BONE_SPECS.items()},
        "alignment": alignment_report,
        "binding": binding_report,
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
        "external_spend_usd": 0,
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2) + "\n")
    scene.frame_set(1)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
