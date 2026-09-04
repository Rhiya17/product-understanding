"""Stage B: import, measure, per-axis repair, and render the two twins.

Run only with Blender 5.2.0 LTS:
  Blender --background --python poc8/repair_twins.py

The script never edits the input GLBs. Generated files are confined to
``poc8/out/gate1`` and the two repaired ``.blend`` files in ``poc8``.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import bpy
from mathutils import Vector


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONFIG = json.loads((HERE / "config.json").read_text())
OUT = HERE / "out" / "gate1"
EXPECTED_BLENDER = CONFIG["blender_version"]


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for blocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.images,
    ):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)


def mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def world_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    if not objects:
        raise RuntimeError("no mesh objects were imported")
    # ``Object.bound_box`` remains cached after direct vertex edits until a
    # dependency-graph rebuild. Measuring actual vertices makes the repair
    # check independent of that Blender cache behavior.
    points = [obj.matrix_world @ vertex.co for obj in objects for vertex in obj.data.vertices]
    minimum = Vector(tuple(min(point[index] for point in points) for index in range(3)))
    maximum = Vector(tuple(max(point[index] for point in points) for index in range(3)))
    return minimum, maximum


def extents(objects: list[bpy.types.Object]) -> Vector:
    minimum, maximum = world_bounds(objects)
    return maximum - minimum


def scale_meshes_in_world(
    objects: list[bpy.types.Object], center: Vector, factors: Vector
) -> None:
    """Scale all mesh vertices around a shared world-space center.

    Both source GLBs currently contain one mesh object, but this formulation
    remains deterministic if a future download splits the shell into objects.
    Object origins are also moved so modifiers/children remain aligned.
    """

    for obj in objects:
        matrix = obj.matrix_world.copy()
        inverse = matrix.inverted()
        for vertex in obj.data.vertices:
            world = matrix @ vertex.co
            repaired = center + Vector(
                tuple((world[index] - center[index]) * factors[index] for index in range(3))
            )
            vertex.co = inverse @ repaired
        obj.data.update()


def translate_scene_meshes(objects: list[bpy.types.Object], offset: Vector) -> None:
    imported = set(objects)
    roots = [obj for obj in objects if obj.parent not in imported]
    for obj in roots:
        obj.location += offset


def material(name: str, rgba: tuple[float, float, float, float], emission: bool = False):
    value = bpy.data.materials.new(name)
    value.diffuse_color = rgba
    value.use_nodes = True
    node = value.node_tree.nodes.get("Principled BSDF")
    if emission:
        node.inputs["Base Color"].default_value = rgba
        node.inputs["Emission Color"].default_value = rgba
        node.inputs["Emission Strength"].default_value = 2.0
        node.inputs["Roughness"].default_value = 0.5
    else:
        node.inputs["Base Color"].default_value = rgba
        node.inputs["Roughness"].default_value = 0.75
    return value


def aim(obj: bpy.types.Object, target: Vector) -> None:
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def configure_render(product: str, attempt: int, objects: list[bpy.types.Object]) -> None:
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = CONFIG["render"]["width"]
    scene.render.resolution_y = CONFIG["render"]["height"]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.use_file_extension = True
    scene.render.image_settings.color_mode = "RGBA"
    scene.world.color = (0.035, 0.04, 0.05)
    scene.view_settings.look = "AgX - Medium High Contrast"

    minimum, maximum = world_bounds(objects)
    center = (minimum + maximum) / 2
    size = maximum - minimum
    camera_spec = CONFIG["products"][product]["camera_attempts"][attempt - 1]
    direction = Vector(camera_spec["direction"]).normalized()

    camera_data = bpy.data.cameras.new(f"Gate1_{product}_Attempt{attempt}_Camera")
    camera = bpy.data.objects.new(camera_data.name, camera_data)
    scene.collection.objects.link(camera)
    camera_data.lens = camera_spec["lens_mm"]
    camera_data.sensor_width = 36
    # Fit conservatively to both horizontal and vertical fields of view.
    aspect = scene.render.resolution_x / scene.render.resolution_y
    horizontal = max(size.x, size.y * 0.25)
    vertical = max(size.z, horizontal / aspect * 0.45)
    hfov = 2 * math.atan(camera_data.sensor_width / (2 * camera_data.lens))
    vfov = 2 * math.atan(math.tan(hfov / 2) / aspect)
    distance = max(
        horizontal / max(2 * math.tan(hfov / 2), 1e-6),
        vertical / max(2 * math.tan(vfov / 2), 1e-6),
    ) * 1.55
    distance = max(distance, max(size) * 1.5)
    camera.location = center + direction * distance
    aim(camera, center)
    scene.camera = camera

    # Presentation-only render corrections (2026-08-29, run 3): glTF import
    # left materials on HASHED alpha and the area lights overexposed the dark
    # PBR textures into a translucent silver look, which run 2's verifier
    # correctly failed. Opaque blend + reduced energy + -0.5 EV show the
    # twin's actual textures; no twin content is altered.
    for mat in bpy.data.materials:
        if hasattr(mat, "blend_method"):
            mat.blend_method = "OPAQUE"
    scene.view_settings.exposure = -0.5

    # Fixed neutral studio floor and three-point lighting are presentation-only.
    floor_mat = material("Neutral_Desk_INFERRED", (0.08, 0.09, 0.11, 1.0))
    bpy.ops.mesh.primitive_plane_add(size=max(size) * 8, location=(center.x, center.y, minimum.z - 0.0003))
    floor = bpy.context.object
    floor.name = "Neutral_Desk_INFERRED"
    floor.data.materials.append(floor_mat)

    for name, position, energy, area_size in (
        ("Key_INFERRED", center + Vector((-max(size), -max(size), max(size) * 2.5)), 21.0, 0.8),
        ("Fill_INFERRED", center + Vector((max(size), -max(size) * 0.5, max(size))), 11.0, 0.7),
        ("Rim_INFERRED", center + Vector((0, max(size), max(size) * 1.7)), 17.0, 0.6),
    ):
        light_data = bpy.data.lights.new(name, "AREA")
        light_data.energy = energy
        light_data.shape = "DISK"
        light_data.size = area_size
        light = bpy.data.objects.new(name, light_data)
        scene.collection.objects.link(light)
        light.location = position
        aim(light, center)

    # Camera-local red text keeps every still unmistakably internal-only.
    watermark_mat = material("Internal_Watermark_Red", (0.8, 0.01, 0.01, 1.0), emission=True)
    bpy.ops.object.text_add()
    watermark = bpy.context.object
    watermark.name = "INTERNAL_ONLY_WATERMARK"
    watermark.data.body = CONFIG["watermark"]
    watermark.data.align_x = "RIGHT"
    watermark.data.size = math.tan(vfov / 2) * 0.17
    watermark.data.extrude = 0
    watermark.data.materials.append(watermark_mat)
    watermark.parent = camera
    watermark.location = (math.tan(hfov / 2) * 0.92, math.tan(vfov / 2) * 0.78, -1.0)
    watermark.rotation_euler = (0, 0, 0)


def repair_product(product: str) -> dict:
    spec = CONFIG["products"][product]
    glb = ROOT / spec["glb"]
    analysis_path = ROOT / spec["mesh_analysis"]
    if not glb.is_file() or not analysis_path.is_file():
        raise FileNotFoundError(f"missing source asset for {product}")

    clear_scene()
    bpy.ops.import_scene.gltf(filepath=str(glb))
    objects = mesh_objects()
    if not objects:
        raise RuntimeError(f"{product}: GLB imported no mesh objects")
    before = extents(objects)
    minimum, maximum = world_bounds(objects)
    center = (minimum + maximum) / 2
    target = Vector(spec["target_extents_m_xyz"])
    factors = Vector(tuple(target[index] / before[index] for index in range(3)))
    scale_meshes_in_world(objects, center, factors)

    # Place the repaired product on Z=0 and center it in X/Y.
    repaired_min, repaired_max = world_bounds(objects)
    repaired_center = (repaired_min + repaired_max) / 2
    translate_scene_meshes(objects, Vector((-repaired_center.x, -repaired_center.y, -repaired_min.z)))
    after = extents(objects)
    errors = [abs(after[index] - target[index]) / target[index] * 100 for index in range(3)]

    scene = bpy.context.scene
    scene["poc"] = "POC8"
    scene["workorder"] = CONFIG["workorder"]
    scene["product_id"] = spec["product_id"]
    scene["internal_only"] = True
    scene["approved_by"] = ""
    scene["watermark"] = CONFIG["watermark"]
    scene["source_glb"] = str(glb)
    scene["source_glb_sha256"] = sha256(glb)
    scene["dimension_claim_ids_xyz"] = json.dumps(spec["dimension_claim_ids_xyz"])
    scene["target_extents_m_xyz"] = json.dumps(list(target))
    scene["scale_factors_xyz"] = json.dumps(list(factors))
    scene["dimension_source_note"] = spec["dimension_source_note"]
    scene["tripo_license_status"] = "OPEN — DO NOT SHIP"

    blend = HERE / f"{product}-repaired.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))

    analysis = json.loads(analysis_path.read_text())
    committed = Vector(analysis["axis_aligned_extents_m"])
    import_deltas = [
        abs(before[index] - committed[index]) / max(abs(committed[index]), 1e-12) * 100
        for index in range(3)
    ]
    report = {
        "product": product,
        "product_id": spec["product_id"],
        "measured_at": utcnow(),
        "source_glb": str(glb.relative_to(ROOT)),
        "source_glb_sha256": sha256(glb),
        "source_mesh_analysis": str(analysis_path.relative_to(ROOT)),
        "mesh_object_count": len(objects),
        "committed_axis_aligned_extents_m_xyz": list(committed),
        "fresh_import_extents_m_xyz": list(before),
        "fresh_vs_committed_error_percent_xyz": import_deltas,
        "target_extents_m_xyz": list(target),
        "target_axis_semantics_xyz": spec["target_axis_semantics_xyz"],
        "dimension_claim_ids_xyz": spec["dimension_claim_ids_xyz"],
        "scale_factors_xyz": list(factors),
        "post_repair_extents_m_xyz": list(after),
        "post_repair_error_percent_xyz": errors,
        "worst_axis_error_percent": max(errors),
        "dimension_gate": "PASS" if max(errors) <= 5.0 else "FAIL",
        "dimension_source_note": spec["dimension_source_note"],
        "repaired_blend": str(blend.relative_to(ROOT)),
        "repaired_blend_sha256": sha256(blend),
        "internal_only": True,
        "approved_by": None,
    }
    write_json(OUT / product / "scale-repair.json", report)

    # Each attempt reopens the same repaired geometry and varies only documented
    # camera parameters. This makes the retry reproducible rather than subjective.
    for attempt in (1, 2):
        bpy.ops.wm.open_mainfile(filepath=str(blend))
        rendered_objects = mesh_objects()
        configure_render(product, attempt, rendered_objects)
        attempt_dir = OUT / f"attempt-{attempt}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        render_path = attempt_dir / f"{product}.png"
        scene = bpy.context.scene
        scene["gate1_attempt"] = attempt
        scene.render.filepath = str(render_path)
        bpy.ops.render.render(write_still=True)
        write_json(attempt_dir / f"{product}-render.json", {
            "attempt": attempt,
            "product": product,
            "rendered_at": utcnow(),
            "render": str(render_path.relative_to(ROOT)),
            "render_sha256": sha256(render_path),
            "official_image": spec["official_image"],
            "official_image_sha256": sha256(ROOT / spec["official_image"]),
            "camera": spec["camera_attempts"][attempt - 1],
            "watermark": CONFIG["watermark"],
            "internal_only": True,
            "approved_by": None,
        })
    return report


def main() -> None:
    if bpy.app.version_string != EXPECTED_BLENDER:
        raise SystemExit(
            f"Blender binding changed: expected {EXPECTED_BLENDER}, got {bpy.app.version_string}"
        )
    if OUT.exists():
        # Never destroy a previous run's audit trail (a rerun on 2026-08-29
        # erased one verification round before this guard existed).
        from datetime import datetime, timezone
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        OUT.rename(OUT.parent / f"gate1-archived-{stamp}")
    OUT.mkdir(parents=True)
    reports = [repair_product(product) for product in ("bose", "macbook")]
    summary = {
        "stage": "B",
        "generated_at": utcnow(),
        "blender_version": bpy.app.version_string,
        "products": reports,
        "dimension_gate_all_pass": all(item["dimension_gate"] == "PASS" for item in reports),
        "identity_gate_status": "PENDING",
        "gate1_status": "PENDING",
        "next_step": "Run poc8/verify_gate1.py; it supplies the two official-image identity attempts.",
        "internal_only": True,
        "approved_by": None,
    }
    write_json(OUT / "stage-b-report.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
