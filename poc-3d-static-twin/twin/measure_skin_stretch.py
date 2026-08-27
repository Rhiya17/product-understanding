"""Measure Stage S fused-shell edge stretch at every declared joint band.

For each frame, evaluated armature-deformed edge lengths are divided by the
frame-1 rest lengths.  The report is deliberately diagnostic: ratios above
1.6 are flagged as visible artifacts and never hidden by invented geometry.

Usage:
  Blender --background --python measure_skin_stretch.py
"""

from __future__ import annotations

import json
from pathlib import Path

import bpy
import numpy as np


HERE = Path(__file__).resolve().parent
BLEND = HERE / "ready2jet-skinned.blend"
OUT_JSON = HERE / "stretch-qa-stage-s.json"
OUT_MD = HERE / "stretch-qa-stage-s.md"
SKIN = "Ready2Jet_PhotoSkin_INTERNAL_ONLY"
VISIBLE_ARTIFACT_RATIO = 1.6
RIGHTS_NOTE = "Tripo3D license check OPEN — do not ship"


# Axis is the hinge-line direction.  Radius is the honest measurement band,
# not a geometry-edit region.  The basket is a documented soft-envelope scale
# rather than a hinge; its larger local envelope is measured explicitly.
JOINT_BANDS = (
    {"joint": "front_frame_about_hub112", "bones": ("front_frame", "rear_frame"), "pivot": (0.0, 0.0, 0.52), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "lower_handle_about_hub112", "bones": ("lower_handle", "rear_frame"), "pivot": (0.0, 0.0, 0.52), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "upper_handle_pivot118", "bones": ("upper_handle", "lower_handle"), "pivot": (0.17, 0.0, 0.79), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "seat_follow", "bones": ("seat_unit", "rear_frame"), "pivot": (-0.01, 0.0, 0.53), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "canopy_fold", "bones": ("canopy", "seat_unit"), "pivot": (0.145, 0.0, 0.845), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "belly_bar_follow", "bones": ("belly_bar", "seat_unit"), "pivot": (-0.02, 0.0, 0.59), "axis": (0.0, 1.0, 0.0), "radius_m": 0.04},
    {"joint": "cup_holder_compact_rotation", "bones": ("cup_holder", "lower_handle"), "pivot": (0.14, -0.205, 0.80), "axis": (1.0, 0.0, 0.0), "radius_m": 0.04},
    {"joint": "front_caster_left_prepare", "bones": ("wheel_FL", "front_frame"), "pivot": (-0.28, -0.235, 0.065), "axis": (0.0, 0.0, 1.0), "radius_m": 0.04},
    {"joint": "front_caster_right_prepare", "bones": ("wheel_FR", "front_frame"), "pivot": (-0.28, 0.235, 0.065), "axis": (0.0, 0.0, 1.0), "radius_m": 0.04},
    {"joint": "basket_soft_envelope_collapse", "bones": ("basket", "rear_frame"), "pivot": (0.015, 0.0, 0.245), "axis": (1.0, 0.0, 0.0), "radius_m": 0.12},
)


def evaluated_coordinates(obj, depsgraph) -> np.ndarray:
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        flat = np.empty(len(mesh.vertices) * 3, dtype=np.float64)
        mesh.vertices.foreach_get("co", flat)
        coordinates = flat.reshape((-1, 3))
        matrix = np.array(evaluated.matrix_world, dtype=np.float64)
        homogeneous = np.concatenate((coordinates, np.ones((len(coordinates), 1))), axis=1)
        return (homogeneous @ matrix.T)[:, :3]
    finally:
        evaluated.to_mesh_clear()


def main() -> None:
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    scene = bpy.context.scene
    if scene.get("license_status") != "Tripo3D OPEN - DO NOT SHIP":
        raise SystemExit("license guard changed; refusing deformation QA")
    rig = bpy.data.objects["RigRoot"]
    for prop in ("defect_reverse_direction", "defect_skip_handle_release", "defect_skip_latch"):
        rig[prop] = 0.0
    rig.update_tag()
    skin = bpy.data.objects[SKIN]
    depsgraph = bpy.context.evaluated_depsgraph_get()

    edge_vertices_flat = np.empty(len(skin.data.edges) * 2, dtype=np.int64)
    skin.data.edges.foreach_get("vertices", edge_vertices_flat)
    edges = edge_vertices_flat.reshape((-1, 2))
    scene.frame_set(1)
    bpy.context.view_layer.update()
    rest = evaluated_coordinates(skin, depsgraph)
    rest_vectors = rest[edges[:, 1]] - rest[edges[:, 0]]
    rest_lengths = np.linalg.norm(rest_vectors, axis=1)
    valid_rest = rest_lengths > 1e-9
    midpoints = (rest[edges[:, 0]] + rest[edges[:, 1]]) / 2.0

    group_indices = {group.name: group.index for group in skin.vertex_groups}
    weights = {bone: np.zeros(len(skin.data.vertices), dtype=np.float64) for band in JOINT_BANDS for bone in band["bones"]}
    for vertex in skin.data.vertices:
        for membership in vertex.groups:
            for bone, group_index in group_indices.items():
                if group_index == membership.group and bone in weights:
                    weights[bone][vertex.index] = membership.weight
                    break

    band_masks = {}
    for band in JOINT_BANDS:
        pivot = np.array(band["pivot"], dtype=np.float64)
        axis = np.array(band["axis"], dtype=np.float64)
        axis /= np.linalg.norm(axis)
        offset = midpoints - pivot
        radial = np.linalg.norm(offset - np.outer(offset @ axis, axis), axis=1)
        a, b = band["bones"]
        involvement_a = weights[a][edges[:, 0]] + weights[b][edges[:, 0]]
        involvement_b = weights[a][edges[:, 1]] + weights[b][edges[:, 1]]
        band_masks[band["joint"]] = valid_rest & (radial <= band["radius_m"]) & (involvement_a > 0.05) & (involvement_b > 0.05)

    accumulators = {
        band["joint"]: {
            "max_ratio": 1.0,
            "min_ratio": 1.0,
            "worst_frame": 1,
            "worst_edge_index": None,
        }
        for band in JOINT_BANDS
    }
    whole_max_ratio = 1.0
    whole_worst_frame = 1
    whole_worst_edge = None

    for frame in range(1, 97):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        current = evaluated_coordinates(skin, depsgraph)
        lengths = np.linalg.norm(current[edges[:, 1]] - current[edges[:, 0]], axis=1)
        ratios = np.ones_like(lengths)
        ratios[valid_rest] = lengths[valid_rest] / rest_lengths[valid_rest]
        valid_indices = np.flatnonzero(valid_rest)
        frame_whole_local = int(np.argmax(ratios[valid_rest]))
        frame_whole_edge = int(valid_indices[frame_whole_local])
        frame_whole_ratio = float(ratios[frame_whole_edge])
        if frame_whole_ratio > whole_max_ratio:
            whole_max_ratio = frame_whole_ratio
            whole_worst_frame = frame
            whole_worst_edge = frame_whole_edge

        for band in JOINT_BANDS:
            name = band["joint"]
            mask = band_masks[name]
            indices = np.flatnonzero(mask)
            if not len(indices):
                continue
            local_max = int(np.argmax(ratios[mask]))
            edge_index = int(indices[local_max])
            maximum = float(ratios[edge_index])
            minimum = float(np.min(ratios[mask]))
            accumulator = accumulators[name]
            if maximum > accumulator["max_ratio"]:
                accumulator["max_ratio"] = maximum
                accumulator["worst_frame"] = frame
                accumulator["worst_edge_index"] = edge_index
            accumulator["min_ratio"] = min(accumulator["min_ratio"], minimum)

    bands = []
    for band in JOINT_BANDS:
        name = band["joint"]
        accumulator = accumulators[name]
        count = int(np.count_nonzero(band_masks[name]))
        maximum = accumulator["max_ratio"] if count else None
        bands.append({
            **band,
            "bones": list(band["bones"]),
            "edge_count": count,
            "max_edge_length_ratio_vs_rest": maximum,
            "min_edge_length_ratio_vs_rest": accumulator["min_ratio"] if count else None,
            "worst_frame": accumulator["worst_frame"] if count else None,
            "worst_edge_index": accumulator["worst_edge_index"] if count else None,
            "visible_artifact": bool(maximum is not None and maximum > VISIBLE_ARTIFACT_RATIO),
            "coverage_note": None if count else "No fused-shell edges in this spatial/weight band; nearest-part binding assigned no scan surface here.",
        })

    severe = [band for band in bands if band["visible_artifact"]]
    report = {
        "status": "MEASURED",
        "method": "per-frame evaluated edge length divided by frame-1 rest length",
        "frames_checked": [1, 96],
        "frame_count": 96,
        "mesh_edge_count": len(edges),
        "visible_artifact_threshold_ratio": VISIBLE_ARTIFACT_RATIO,
        "whole_mesh_max_ratio": whole_max_ratio,
        "whole_mesh_worst_frame": whole_worst_frame,
        "whole_mesh_worst_edge_index": whole_worst_edge,
        "severe_joint_count": len(severe),
        "bands": bands,
        "mitigation": "Weights are already rigid outside three declared 3 cm hinge bands. Remaining fused-shell stretch is disclosed; no geometry was invented or patched.",
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
        "external_spend_usd": 0,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")

    lines = [
        "# Stage S deformation QA — INTERNAL ONLY",
        "",
        f"**Rights:** {RIGHTS_NOTE}",
        "",
        "Every evaluated mesh edge was measured across all 96 frames as current length / frame-1 length. Ratios above 1.6 are visible artifacts. No geometry was invented to hide them.",
        "",
        "| Joint band | Edges | Worst ratio | Frame | > 1.6 |",
        "|---|---:|---:|---:|:---:|",
    ]
    for band in bands:
        maximum = "n/a" if band["max_edge_length_ratio_vs_rest"] is None else f"{band['max_edge_length_ratio_vs_rest']:.3f}×"
        frame = "n/a" if band["worst_frame"] is None else str(band["worst_frame"])
        lines.append(f"| `{band['joint']}` | {band['edge_count']} | {maximum} | {frame} | {'YES' if band['visible_artifact'] else 'no'} |")
    lines.extend([
        "",
        f"Whole-mesh worst case: **{whole_max_ratio:.3f}× at frame {whole_worst_frame}** (edge {whole_worst_edge}).",
        "",
        "Mitigation applied: rigid nearest-part masks everywhere except the declared 3 cm front-frame, seat, and canopy hinge bands. The remaining fused-shell artifacts are disclosed rather than patched with invented separations or hidden linkage geometry.",
        "",
    ])
    missing = [band for band in bands if band["edge_count"] == 0]
    if missing:
        lines.append("Bands with no measurable scan surface: " + ", ".join(f"`{band['joint']}`" for band in missing) + ". This means the nearest-part binding found no provider-mesh edges in that spatial band; it is not reported as a zero-stretch pass.")
        lines.append("")
    OUT_MD.write_text("\n".join(lines))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
