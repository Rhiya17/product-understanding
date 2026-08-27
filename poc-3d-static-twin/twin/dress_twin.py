"""Visual dress pass for the POC 6 twin. Kinematics are untouched.

Applies product-accurate materials (Kingston: charcoal melange fabric, black
frame, tan leather grip — evidence: input views and official video), cushion
modifiers on seat/canopy proxies, smooth shading, and a three-light studio
setup. Geometry positions, rig, actions, and evidence markers are not
modified; this is presentation only.

Usage (headless):
  Blender --background --python dress_twin.py -- [--save] [--stills DIR]
"""

import math
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
BLEND = HERE / "ready2jet-rigged.blend"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SAVE = "--save" in argv
STILLS = None
if "--stills" in argv:
    STILLS = Path(argv[argv.index("--stills") + 1])


def principled(material):
    return material.node_tree.nodes.get("Principled BSDF")


def set_base(material, color, metallic=None, roughness=None):
    bsdf = principled(material)
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    if metallic is not None:
        bsdf.inputs["Metallic"].default_value = metallic
    if roughness is not None:
        bsdf.inputs["Roughness"].default_value = roughness
    material.diffuse_color = (*color, material.diffuse_color[3])


def add_fabric_bump(material, scale=380.0, strength=0.28):
    tree = material.node_tree
    bsdf = principled(material)
    noise = tree.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = 4.0
    bump = tree.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])


def dress_materials():
    mats = bpy.data.materials
    set_base(mats["Frame_Black"], (0.012, 0.013, 0.016), 0.35, 0.32)
    set_base(mats["Plastic_Dark"], (0.020, 0.022, 0.026), 0.05, 0.48)
    set_base(mats["Kingston_Gray"], (0.055, 0.058, 0.066), 0.0, 0.92)
    add_fabric_bump(mats["Kingston_Gray"])
    set_base(mats["Kingston_Light"], (0.105, 0.109, 0.118), 0.0, 0.92)
    add_fabric_bump(mats["Kingston_Light"])
    set_base(mats["Grip_Tan"], (0.285, 0.132, 0.052), 0.0, 0.42)
    add_fabric_bump(mats["Grip_Tan"], scale=140.0, strength=0.12)
    set_base(mats["Wheel_Silver"], (0.055, 0.058, 0.063), 0.55, 0.38)
    set_base(mats["Control_Blue"], (0.030, 0.160, 0.420), 0.05, 0.35)
    set_base(mats["Basket_INFERRED"], (0.018, 0.020, 0.023), 0.0, 0.9)
    if "QA_Floor" in mats:
        set_base(mats["QA_Floor"], (0.80, 0.80, 0.78), 0.0, 0.85)


CUSHION_OBJECTS = ("SeatBack", "SeatBase", "CalfSupport", "CanopyFabric")


def dress_geometry():
    for name in CUSHION_OBJECTS:
        obj = bpy.data.objects.get(name)
        if obj is None:
            continue
        if "cushion_bevel" not in obj.modifiers:
            bevel = obj.modifiers.new("cushion_bevel", "BEVEL")
            bevel.width = 0.011
            bevel.segments = 4
        if "cushion_smooth" not in obj.modifiers:
            subsurf = obj.modifiers.new("cushion_smooth", "SUBSURF")
            subsurf.levels = subsurf.render_levels = 2
    # Canopy: rounder dome, ribs recessed into the fabric instead of tent
    # poles sitting proud of it. The bevel modifiers add tight edge loops
    # that pin the subdivision surface flat, so they are removed here and
    # the subdivision does the rounding on the raw station polyline.
    canopy = bpy.data.objects.get("CanopyFabric")
    if canopy:
        for name in ("soft_edges", "cushion_bevel"):
            if name in canopy.modifiers:
                canopy.modifiers.remove(canopy.modifiers[name])
        if "cushion_smooth" in canopy.modifiers:
            canopy.modifiers["cushion_smooth"].levels = 3
            canopy.modifiers["cushion_smooth"].render_levels = 3
    for index in range(1, 6):
        rib = bpy.data.objects.get(f"Canopy_Rib_{index}")
        if rib:
            # The subdivided fabric pulls inside the station polyline, so the
            # rib proxies float visibly. They are INFERRED decoration; keep
            # them in the scene for the evidence map but out of renders.
            rib.hide_render = True
    for obj in bpy.data.objects:
        if obj.type == "MESH" and not obj.name.startswith("REFERENCE_"):
            obj.select_set(False)
            with bpy.context.temp_override(object=obj):
                try:
                    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(38))
                except Exception:
                    bpy.ops.object.shade_smooth()


def dress_lighting():
    world = bpy.context.scene.world
    background = world.node_tree.nodes["Background"]
    background.inputs[0].default_value = (0.93, 0.945, 0.965, 1)
    background.inputs[1].default_value = 0.32

    key = bpy.data.lights.get("QA_Key")
    if key:
        key.energy = 330
        key.size = 5.0
        key.color = (1.0, 0.972, 0.93)
        bpy.data.objects["QA_Key"].location = (-2.2, -2.9, 3.3)
    fill = bpy.data.lights.get("QA_Fill")
    if fill:
        fill.energy = 120
        fill.size = 4.0
        fill.color = (0.90, 0.94, 1.0)
        bpy.data.objects["QA_Fill"].location = (2.6, -1.2, 2.0)
    if "Dress_Rim" not in bpy.data.objects:
        rim_data = bpy.data.lights.new("Dress_Rim", "AREA")
        rim_data.energy = 260
        rim_data.size = 3.0
        rim_data.color = (0.95, 0.97, 1.0)
        rim = bpy.data.objects.new("Dress_Rim", rim_data)
        (bpy.data.collections.get("QA_ONLY") or
         bpy.context.scene.collection).objects.link(rim)
        rim.location = (2.6, 2.8, 2.6)
        rim.rotation_euler = (math.radians(-135), 0, math.radians(40))

    scene = bpy.context.scene
    for attr, value in (("use_raytracing", True), ("use_gtao", True),
                        ("use_shadows", True)):
        if hasattr(scene.eevee, attr):
            setattr(scene.eevee, attr, value)
    scene.view_settings.look = "AgX - Punchy"


def render_stills(out_dir):
    from mathutils import Vector
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.render.resolution_x = scene.render.resolution_y = 768
    scene.render.image_settings.file_format = "PNG"
    cam_data = bpy.data.cameras.new("Dress_Camera")
    cam_data.lens = 58
    cam = bpy.data.objects.new("Dress_Camera", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    for label, loc, target in (
        ("front-3q", (-1.45, -1.42, 1.02), (0.0, 0.0, 0.47)),
        ("rear-right", (1.55, 1.45, 1.10), (0.05, 0.0, 0.45)),
    ):
        cam.location = loc
        direction = Vector(target) - Vector(loc)
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        scene.render.filepath = str(out_dir / f"dress-{label}.png")
        bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    dress_materials()
    dress_geometry()
    dress_lighting()
    scene = bpy.context.scene
    scene["dress_pass"] = "v1 2026-08-28 presentation-only; kinematics untouched"
    if STILLS:
        render_stills(STILLS)
    if SAVE:
        bpy.ops.wm.save_mainfile(filepath=str(BLEND))
        print("saved", BLEND)


if __name__ == "__main__":
    main()
