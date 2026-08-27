"""Blender-side position-welded connectivity and PCA OBB analysis for GLBs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--glb", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return parser.parse_args(argv)


class UnionFind:
    def __init__(self):
        self.parent = []

    def add(self):
        i = len(self.parent)
        self.parent.append(i)
        return i

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[b] = a


def main():
    args = parse_args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(args.glb))
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    points = []
    faces = []
    face_areas = []
    offset = 0
    for obj in meshes:
        world = obj.matrix_world
        verts = [world @ v.co for v in obj.data.vertices]
        points.extend(tuple(v) for v in verts)
        for poly in obj.data.polygons:
            indices = [offset + i for i in poly.vertices]
            faces.append(indices)
            # triangulation-independent polygon area in world space.
            if len(indices) >= 3:
                origin = Vector(points[indices[0]])
                area = sum(((Vector(points[indices[i]]) - origin).cross(
                            Vector(points[indices[i + 1]]) - origin)).length / 2
                           for i in range(1, len(indices) - 1))
            else:
                area = 0.0
            face_areas.append(area)
        offset += len(verts)
    arr = np.asarray(points, dtype=float)
    lo, hi = arr.min(axis=0), arr.max(axis=0)
    diag = float(np.linalg.norm(hi - lo))
    tolerance = max(diag * 1e-6, 1e-9)
    uf = UnionFind()
    weld = {}
    vertex_node = []
    for point in arr:
        key = tuple(np.rint(point / tolerance).astype(np.int64))
        if key not in weld:
            weld[key] = uf.add()
        vertex_node.append(weld[key])
    for face in faces:
        nodes = [vertex_node[i] for i in face]
        for node in nodes[1:]:
            uf.union(nodes[0], node)
    component_faces = {}
    component_area = {}
    for face, area in zip(faces, face_areas):
        root = uf.find(vertex_node[face[0]])
        component_faces[root] = component_faces.get(root, 0) + 1
        component_area[root] = component_area.get(root, 0.0) + area
    counts = sorted(component_faces.values(), reverse=True)
    areas = sorted(component_area.values(), reverse=True)
    total_area = sum(areas)

    centered = arr - arr.mean(axis=0)
    _, _, vh = np.linalg.svd(centered, full_matrices=False)
    projected = centered @ vh.T
    obb = projected.max(axis=0) - projected.min(axis=0)
    result = {
        "glb": args.glb.name,
        "object_count": len(meshes),
        "vertex_count": len(points),
        "face_count": len(faces),
        "weld_tolerance_m": tolerance,
        "welded_component_count": len(counts),
        "component_face_counts_desc": counts,
        "largest_shell_face_share": counts[0] / len(faces) if faces else None,
        "component_surface_areas_desc_m2": areas,
        "largest_shell_area_share": areas[0] / total_area if total_area else None,
        "axis_aligned_extents_m": (hi - lo).tolist(),
        "pca_obb_extents_m": obb.tolist(),
        "pca_obb_extents_sorted_m": sorted(obb.tolist()),
        "analysis_note": "Position weld uses 1e-6 of mesh diagonal; largest-shell headline uses face share, matching the existing Tripo probe scorecard convention.",
        "rights_note": "Tripo3D license check OPEN — do not ship",
        "approved_by": None,
        "internal_only": True,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
