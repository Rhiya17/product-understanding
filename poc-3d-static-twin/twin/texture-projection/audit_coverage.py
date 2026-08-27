"""Stage A: deterministic scan/twin alignment and surface-coverage audit.

This script is read-only with respect to the mechanism twin.  It opens the
hash-pinned rigged blend, applies the already disclosed Stage-S scan alignment
to an in-memory BVH, and measures evaluated twin surfaces against that BVH.

Coverage is area weighted.  Long triangles are subdivided until their longest
edge is at most 7.5 mm, then each leaf triangle contributes its centroid and
surface area.  The acceptance threshold is 15 mm, as required by the work
order.  No mesh, rig, action, material, or evidence data is changed.

Usage:
  Blender --background --python texture-projection/audit_coverage.py
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


HERE = Path(__file__).resolve().parent
TWIN_DIR = HERE.parent
ROOT = TWIN_DIR.parent.parent
SOURCE_BLEND = TWIN_DIR / "ready2jet-rigged.blend"
ALIGNMENT_REPORT = TWIN_DIR / "skinning-report.json"
SCAN_GLB = ROOT / "poc-3d-static-twin" / "runs" / "tripo-probe-01" / "pbr_model-k11lDWbp1BeH5sJR6lO6C_model.glb"
ACTION_SPEC = TWIN_DIR / "action-spec.json"
JOINT_EVIDENCE = TWIN_DIR / "joint-evidence.json"
OUT = HERE / "coverage.json"
SCAN_OBJECT = "REFERENCE_TripoProbe01_DO_NOT_RENDER"

EXPECTED_HASHES = {
    "source_twin": "83d80dc107d46edecbe89d4d97dabf726887012dd4c0917f8da8e2961a9dc79d",
    "scan_glb": "95e0fe44bba9a303b31849cfbec1d7d517d2ed2c6361ab505e025cf7ef80716b",
    "action_spec": "42d43c0cab6d4f320a1c473c534020d1e91176ba2f6d9eec8e8ff5b944b5d3c2",
    "joint_evidence": "e2a1ad9ddb091f00a59aba553287b844427ef8e84e846d8dc09ab9a98fc8f361",
}

MAX_PROJECTION_DISTANCE_M = 0.015
MAX_SAMPLE_EDGE_M = 0.0075
KEY_GATE_MINIMUM = 0.60

KEY_GROUPS = {
    "seat": ("SeatBack", "SeatBase", "CalfSupport"),
    "canopy": ("CanopyFabric",),
    "frame_tubes": (
        "RearLeg110_L", "RearLeg110_R", "RearAxle",
        "FrontLeg108_L", "FrontLeg108_R", "FrontCrossbar",
        "LowerHandle124_L", "LowerHandle124_R",
        "UpperHandle120_L", "UpperHandle120_R",
    ),
    "handle_grip": ("HandleGrip",),
    "wheels": (
        "Wheel_FL_Tire", "Wheel_FL_Hub", "Wheel_FL_Spoke1", "Wheel_FL_Spoke2", "Wheel_FL_Spoke3",
        "Wheel_FR_Tire", "Wheel_FR_Hub", "Wheel_FR_Spoke1", "Wheel_FR_Spoke2", "Wheel_FR_Spoke3",
        "Wheel_RL_Tire", "Wheel_RL_Hub", "Wheel_RL_Spoke1", "Wheel_RL_Spoke2", "Wheel_RL_Spoke3",
        "Wheel_RR_Tire", "Wheel_RR_Hub", "Wheel_RR_Spoke1", "Wheel_RR_Spoke2", "Wheel_RR_Spoke3",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs() -> dict[str, str]:
    paths = {
        "source_twin": SOURCE_BLEND,
        "scan_glb": SCAN_GLB,
        "action_spec": ACTION_SPEC,
        "joint_evidence": JOINT_EVIDENCE,
    }
    actual = {name: sha256(path) for name, path in paths.items()}
    for name, expected in EXPECTED_HASHES.items():
        if actual[name] != expected:
            raise SystemExit(f"protected input hash changed for {name}: {actual[name]} != {expected}")
    return actual


def build_scan_bvh(alignment: Matrix) -> BVHTree:
    scan = bpy.data.objects.get(SCAN_OBJECT)
    if scan is None or scan.type != "MESH":
        raise SystemExit(f"missing source scan object {SCAN_OBJECT}")
    world = alignment @ scan.matrix_world
    vertices = [world @ vertex.co for vertex in scan.data.vertices]
    polygons = [list(polygon.vertices) for polygon in scan.data.polygons]
    if not polygons:
        raise SystemExit("source scan contains no polygons")
    return BVHTree.FromPolygons(vertices, polygons, all_triangles=False)


def triangle_area(a: Vector, b: Vector, c: Vector) -> float:
    return 0.5 * (b - a).cross(c - a).length


def leaf_samples(a: Vector, b: Vector, c: Vector, depth: int = 0):
    """Yield (centroid, area) for adaptively subdivided triangle leaves."""
    edges = ((a, b, (a - b).length, c), (b, c, (b - c).length, a), (c, a, (c - a).length, b))
    first, second, length, opposite = max(edges, key=lambda item: item[2])
    if length <= MAX_SAMPLE_EDGE_M or depth >= 12:
        area = triangle_area(a, b, c)
        if area > 0:
            yield (a + b + c) / 3.0, area
        return
    midpoint = (first + second) / 2.0
    yield from leaf_samples(first, midpoint, opposite, depth + 1)
    yield from leaf_samples(midpoint, second, opposite, depth + 1)


def measure_object(obj: bpy.types.Object, tree: BVHTree, depsgraph) -> dict:
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    total_area = 0.0
    covered_area = 0.0
    weighted_distance = 0.0
    weighted_distance_sq = 0.0
    maximum_distance = 0.0
    sample_count = 0
    distances: list[tuple[float, float]] = []
    try:
        mesh.calc_loop_triangles()
        world = evaluated.matrix_world
        for triangle in mesh.loop_triangles:
            a, b, c = (world @ mesh.vertices[index].co for index in triangle.vertices)
            for point, area in leaf_samples(a, b, c):
                nearest = tree.find_nearest(point)
                if nearest is None:
                    raise SystemExit(f"scan BVH returned no nearest surface for {obj.name}")
                distance = float(nearest[3])
                sample_count += 1
                total_area += area
                covered_area += area if distance <= MAX_PROJECTION_DISTANCE_M else 0.0
                weighted_distance += area * distance
                weighted_distance_sq += area * distance * distance
                maximum_distance = max(maximum_distance, distance)
                distances.append((distance, area))
    finally:
        evaluated.to_mesh_clear()
    if total_area <= 0:
        raise SystemExit(f"evaluated mesh has no measurable area: {obj.name}")
    distances.sort(key=lambda item: item[0])
    p95_target = 0.95 * total_area
    running = 0.0
    p95 = distances[-1][0]
    for distance, area in distances:
        running += area
        if running >= p95_target:
            p95 = distance
            break
    return {
        "surface_area_m2": total_area,
        "covered_area_m2": covered_area,
        "coverage_fraction": covered_area / total_area,
        "fallback_fraction": 1.0 - covered_area / total_area,
        "mean_distance_m": weighted_distance / total_area,
        "rms_distance_m": math.sqrt(weighted_distance_sq / total_area),
        "p95_distance_m": p95,
        "maximum_distance_m": maximum_distance,
        "sample_count": sample_count,
        "render_visible": not obj.hide_render,
    }


def aggregate(names: tuple[str, ...], parts: dict[str, dict]) -> dict:
    missing = [name for name in names if name not in parts]
    if missing:
        raise SystemExit(f"key coverage group is missing objects: {missing}")
    area = sum(parts[name]["surface_area_m2"] for name in names)
    covered = sum(parts[name]["covered_area_m2"] for name in names)
    weighted_mean = sum(parts[name]["mean_distance_m"] * parts[name]["surface_area_m2"] for name in names)
    weighted_rms_sq = sum(parts[name]["rms_distance_m"] ** 2 * parts[name]["surface_area_m2"] for name in names)
    return {
        "objects": list(names),
        "surface_area_m2": area,
        "covered_area_m2": covered,
        "coverage_fraction": covered / area,
        "fallback_fraction": 1.0 - covered / area,
        "mean_distance_m": weighted_mean / area,
        "rms_distance_m": math.sqrt(weighted_rms_sq / area),
    }


def main() -> None:
    started = time.monotonic()
    started_at = datetime.now(timezone.utc)
    input_hashes = verify_inputs()
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE_BLEND))
    scene = bpy.context.scene
    scene.frame_set(1)
    bpy.context.view_layer.update()
    if scene.get("correct_action") != "Ready2Jet_Fold_Correct":
        raise SystemExit("motion authority changed; refusing coverage audit")
    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        raise SystemExit("internal-only license guard changed; refusing coverage audit")

    alignment_data = json.loads(ALIGNMENT_REPORT.read_text())["alignment"]
    alignment = Matrix(alignment_data["applied_matrix_world_before_bake"])
    tree = build_scan_bvh(alignment)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    geometry = bpy.data.collections.get("TWIN_GEOMETRY")
    if geometry is None:
        raise SystemExit("missing TWIN_GEOMETRY collection")
    objects = sorted(
        (obj for obj in geometry.objects if obj.type == "MESH" and not obj.name.startswith("REFERENCE_")),
        key=lambda obj: obj.name,
    )
    parts = {obj.name: measure_object(obj, tree, depsgraph) for obj in objects}
    key_groups = {name: aggregate(object_names, parts) for name, object_names in KEY_GROUPS.items()}
    key_average = sum(group["coverage_fraction"] for group in key_groups.values()) / len(key_groups)
    total_area = sum(part["surface_area_m2"] for part in parts.values())
    total_covered = sum(part["covered_area_m2"] for part in parts.values())
    total_rms_sq = sum(part["rms_distance_m"] ** 2 * part["surface_area_m2"] for part in parts.values())
    ended_at = datetime.now(timezone.utc)
    report = {
        "schema_version": 1,
        "stage": "A_alignment_and_coverage",
        "status": "PASS" if key_average >= KEY_GATE_MINIMUM else "STOP_GATE_FAILED",
        "internal_only": True,
        "external_spend_usd": 0,
        "appearance_only": True,
        "measurement": {
            "projection_distance_m": MAX_PROJECTION_DISTANCE_M,
            "maximum_sample_triangle_edge_m": MAX_SAMPLE_EDGE_M,
            "area_weighted": True,
            "sample_method": "evaluated twin triangles recursively split to <=7.5 mm longest edge; leaf centroids queried against aligned scan BVH",
            "pose_frame": 1,
        },
        "alignment": {
            "method": alignment_data["method"],
            "refinement": "none; reused the disclosed Stage-S transform exactly",
            "applied_matrix_world": alignment_data["applied_matrix_world_before_bake"],
            "applied_scale_xyz": alignment_data["applied_scale_xyz"],
            "area_weighted_twin_to_scan_rms_surface_distance_m": math.sqrt(total_rms_sq / total_area),
            "area_weighted_twin_to_scan_mean_surface_distance_m": sum(part["mean_distance_m"] * part["surface_area_m2"] for part in parts.values()) / total_area,
        },
        "gate": {
            "key_groups": list(KEY_GROUPS),
            "aggregation": "arithmetic mean of the five area-weighted logical key-group coverage fractions",
            "minimum_fraction": KEY_GATE_MINIMUM,
            "actual_fraction": key_average,
            "passed": key_average >= KEY_GATE_MINIMUM,
            "on_failure": "stop before Stage B baking; report disclosed dress-material fallback coverage",
        },
        "overall": {
            "surface_area_m2": total_area,
            "covered_area_m2": total_covered,
            "coverage_fraction": total_covered / total_area,
            "fallback_fraction": 1.0 - total_covered / total_area,
        },
        "key_part_groups": key_groups,
        "parts": parts,
        "provenance": {
            "source_twin": str(SOURCE_BLEND.relative_to(ROOT)),
            "source_scan_run_id": "tripo-probe-01",
            "source_scan": str(SCAN_GLB.relative_to(ROOT)),
            "input_sha256": input_hashes,
            "alignment_report": str(ALIGNMENT_REPORT.relative_to(ROOT)),
        },
        "timing": {
            "started_at_utc": started_at.isoformat(),
            "ended_at_utc": ended_at.isoformat(),
            "script_elapsed_seconds": time.monotonic() - started,
            "script_elapsed_hours": (time.monotonic() - started) / 3600.0,
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "key_average_fraction": key_average,
        "overall_fraction": report["overall"]["coverage_fraction"],
        "rms_m": report["alignment"]["area_weighted_twin_to_scan_rms_surface_distance_m"],
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
