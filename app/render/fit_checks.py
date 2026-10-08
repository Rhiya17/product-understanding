"""Deterministic fit checks for authored cargo-fit scenes.

Copied next to the trusted runner into the build sandbox. ``measure`` reads the
built Blender scene; ``compare`` is pure and decides pass/fail from numbers, so
it is unit-tested without Blender. The spec comes from the fit brief, never
from the authoring model.

Scene contract (stated in the brief): meters; +Z up. Object parts are named
with ``spec["object_prefix"]``. Cargo-space colliders use the names in
``spec["colliders"]``: floor, seatback, liftgate (its closed pose at the last
frame), side_left, side_right and ceiling (the closed floor-to-top limit).
"""

FLOOR_CONTACT_M = 0.003
PENETRATION_TOLERANCE_M = 0.001


def compare(spec, measured):
    """Problems (strings) from measured scene numbers; [] means pass."""
    problems = []
    for frame, names in measured.get("penetrations", {}).items():
        problems.append(f"fit: object passes through {', '.join(sorted(names))} at frame {frame}")
    for frame in measured.get("below_floor_frames", []):
        problems.append(f"fit: object sinks below the floor at frame {frame}")
    final = measured.get("final") or {}
    if not final:
        problems.append("fit: final pose could not be measured")
        return problems
    clearance = spec["clearance_m"]
    for name, distance in final.get("min_distance_m", {}).items():
        if name == "floor":
            if distance > FLOOR_CONTACT_M:
                problems.append(f"fit: object is not resting on the floor at the end "
                                f"({distance * 1000:.0f} mm gap)")
        elif distance < clearance - 0.005:
            problems.append(f"fit: only {distance * 1000:.0f} mm clearance to {name} at the end; "
                            f"the brief requires {clearance * 1000:.0f} mm")
    envelope = sorted(spec["object_envelope_m"])
    dims = sorted(final.get("object_dimensions_m", []))
    if len(dims) == 3:
        for want, have in zip(envelope, dims):
            if abs(have - want) > spec["object_tolerance"] * want:
                problems.append(f"fit: object is {have * 1000:.0f} mm on an axis the evidence "
                                f"gives as {want * 1000:.0f} mm")
    else:
        problems.append("fit: object dimensions could not be measured")
    for name, target in spec.get("space_targets_m", {}).items():
        have = final.get("space_m", {}).get(name)
        if have is None:
            problems.append(f"fit: modelled {name} could not be measured")
        elif abs(have - target) > spec["space_tolerance"] * target:
            problems.append(f"fit: modelled {name} is {have * 1000:.0f} mm; the evidence gives "
                            f"{target * 1000:.0f} mm")
    return problems


def _world_bbox(objects):
    from mathutils import Vector
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for obj in objects:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            lo = Vector(map(min, lo, p))
            hi = Vector(map(max, hi, p))
    return lo, hi


def _bvh(obj, depsgraph):
    """World-space tree (BVHTree.FromObject would be in object-local space)."""
    from mathutils.bvhtree import BVHTree
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    matrix = obj.matrix_world
    verts = [matrix @ v.co for v in mesh.vertices]
    polys = [tuple(p.vertices) for p in mesh.polygons]
    evaluated.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys)


def measure(bpy, spec, last_frame):
    """Read the built scene at every frame. Returns the dict ``compare`` expects."""
    scene = bpy.context.scene
    names = spec["colliders"]
    colliders = {role: bpy.data.objects.get(name) for role, name in names.items()}
    missing = [names[r] for r, o in colliders.items() if o is None or o.type != "MESH"]
    parts = [o for o in bpy.data.objects
             if o.name.startswith(spec["object_prefix"]) and o.type == "MESH"]
    out = {"penetrations": {}, "below_floor_frames": [], "missing": missing}
    if missing or not parts:
        out["final"] = {}
        out["missing"] = missing + ([] if parts else [spec["object_prefix"] + "*"])
        return out
    for frame in range(1, last_frame + 1):
        scene.frame_set(frame)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        # The liftgate is checked in every pose: open during loading, closed at the end.
        trees = {role: _bvh(obj, depsgraph) for role, obj in colliders.items()}
        part_trees = [_bvh(p, depsgraph) for p in parts]
        hits = set()
        for role, tree in trees.items():
            if role == "floor":
                continue
            if any(pt.overlap(tree) for pt in part_trees):
                hits.add(names[role])
        if hits:
            out["penetrations"][str(frame)] = sorted(hits)
        lo, hi = _world_bbox(parts)
        flo, fhi = _world_bbox([colliders["floor"]])
        over_floor = lo.x < fhi.x and hi.x > flo.x and lo.y < fhi.y and hi.y > flo.y
        if over_floor and lo.z < fhi.z - PENETRATION_TOLERANCE_M - 0.002:
            out["below_floor_frames"].append(frame)
    scene.frame_set(last_frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    lo, hi = _world_bbox(parts)
    distances = {}
    trees = {role: _bvh(obj, depsgraph) for role, obj in colliders.items()}
    for role, tree in trees.items():
        best = 1e9
        for part in parts:
            evaluated = part.evaluated_get(depsgraph)
            mesh = evaluated.to_mesh()
            matrix = part.matrix_world
            for vertex in mesh.vertices:
                hit = tree.find_nearest(matrix @ vertex.co)
                if hit[0] is not None:
                    best = min(best, hit[3])
            evaluated.to_mesh_clear()
        distances[role] = best
    flo, fhi = _world_bbox([colliders["floor"]])
    clo, _ = _world_bbox([colliders["ceiling"]])
    out["final"] = {
        "object_dimensions_m": [hi.x - lo.x, hi.y - lo.y, hi.z - lo.z],
        "min_distance_m": distances,
        "space_m": {"floor_depth": fhi.x - flo.x, "closed_ceiling_height": clo.z - fhi.z},
    }
    return out
