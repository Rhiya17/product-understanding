"""Build the Bose QC Ultra (2nd Gen) demonstration scenes in Blender.

    Blender --background --factory-startup --python scenes/bose-qc-ultra-headphones/build_scene.py \
        -- --procedure connect_aux_cable --out scenes/bose-qc-ultra-headphones/out/connect_aux_cable.blend

Evidence used (owner's guide, src_owners_guide_en):
  p13  controls on the back of the RIGHT earcup (Bluetooth/Power button,
       Multi-function button, volume strip); status light, USB-C port and
       2.5 mm AUX port on the LEFT earcup, along its lower rear edge.
  p33  AUX: cable into the 2.5 mm port on the left earcup (plug enters from
       below), other end into the 3.5 mm port on the source device.
  p35  USB audio: USB-C cable into the USB-C port on the left earcup, other
       end into a USB-C source such as a computer.
  p27-28, p37  pairing: hold Bluetooth/Power; two white blinks, then the
       status light pulses blue; enable Bluetooth on the device; select the
       headphones (default name BOSE QC ULTRA 2 HP).
  MacBook Air pack: 3.5 mm jack on the right side; USB-C ports on the left.
Shapes are measured from the official product photos by eye (INFERRED
dimensions); no manufacturer CAD. Coordinates: meters, Z up, the camera side
is -Y ("behind" the wearer, as in the manual's controls diagram), the
wearer's LEFT earcup is at -X.
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector

FPS = 24
CUP_H, CUP_W, CUP_T = 0.092, 0.074, 0.034      # earcup height, width, thickness
CUP_X = 0.088                                   # earcup centre offset from midline
CUP_Z = 0.0
SPLAY = math.radians(28)                        # cups turned so outer faces show
BAND_TOP = 0.165

# ---------------------------------------------------------------- materials

def material(name, color, rough=0.45, metal=0.0, coat=0.0, emission=None, strength=0.0,
             specular=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Specular IOR Level"].default_value = specular
    if emission:
        b.inputs["Emission Color"].default_value = (*emission, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def leather(name, color):
    m = material(name, color, rough=0.66, specular=0.28)
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = 900.0
    tex.inputs["Detail"].default_value = 6.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.18
    bump.inputs["Distance"].default_value = 0.0004
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
    return m


def materials():
    return {
        "shell": material("Matte shell (black)", (0.014, 0.014, 0.015), rough=0.42, specular=0.3),
        "leather": leather("Protein leather (black)", (0.008, 0.008, 0.009)),
        "chrome": material("Polished yoke", (0.8, 0.8, 0.82), rough=0.06, metal=1.0),
        "button": material("Button", (0.03, 0.03, 0.032), rough=0.3),
        "hole": material("Port cavity", (0.0, 0.0, 0.0), rough=0.9),
        "pin": material("Plug pin", (0.85, 0.85, 0.86), rough=0.15, metal=1.0),
        "insulator": material("Plug insulator", (0.01, 0.01, 0.01), rough=0.5),
        "cable": material("Cable jacket", (0.02, 0.02, 0.022), rough=0.55),
        "light": material("Status light", (0.02, 0.02, 0.02), rough=0.3,
                          emission=(1, 1, 1), strength=0.0),
        "cue": material("Press cue", (0.3, 0.6, 1.0), rough=0.5,
                        emission=(0.35, 0.65, 1.0), strength=0.0),
        "alu": material("Laptop aluminium", (0.55, 0.57, 0.6), rough=0.32, metal=0.9),
        "keys": material("Keyboard", (0.02, 0.02, 0.025), rough=0.6),
        "screen": material("Screen", (0.01, 0.01, 0.012), rough=0.08,
                           emission=(0.93, 0.94, 0.96), strength=0.0),
        "ui_text": material("Screen text", (0.05, 0.05, 0.06), rough=0.5),
        "ui_accent": material("Screen accent", (0.05, 0.4, 0.95), rough=0.5,
                              emission=(0.05, 0.4, 0.95), strength=0.0),
        "floor": material("Studio floor", (0.42, 0.42, 0.43), rough=0.8),
    }


# ---------------------------------------------------------------- helpers

def link(obj, name, part=None):
    obj.name = name
    if part:
        obj["part_id"] = part
    return obj


def smooth(obj, bevel=0.0, segments=4, subsurf=1):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    if bevel:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = segments
        mod.limit_method = "ANGLE"
    if subsurf:
        mod = obj.modifiers.new("Subsurf", "SUBSURF")
        mod.levels = subsurf
        mod.render_levels = subsurf
    return obj


def cylinder(name, radius, depth, loc, rot=(0, 0, 0), mat=None, verts=48, part=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rot)
    obj = link(bpy.context.object, name, part)
    if mat:
        obj.data.materials.append(mat)
    return obj


def box(name, size, loc, rot=(0, 0, 0), mat=None, part=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    obj = link(bpy.context.object, name, part)
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def parent(child, parent_obj):
    child.parent = parent_obj
    child.matrix_parent_inverse = parent_obj.matrix_world.inverted()


# ---------------------------------------------------------------- headphones

def rim_point(t, inset=0.0):
    """Point and outward normal on the oval rim, t=0 at top, pi at bottom (local YZ)."""
    a, b = CUP_W / 2 - inset, CUP_H / 2 - inset
    y, z = a * math.sin(t), b * math.cos(t)
    normal = Vector((0, math.sin(t) / a, math.cos(t) / b)).normalized()
    return Vector((0, y, z)), normal


def earcup(side, mats):
    """side=-1 left (wearer), +1 right. Returns the cup root empty."""
    root = bpy.data.objects.new(f"{'Left' if side < 0 else 'Right'} earcup", None)
    bpy.context.collection.objects.link(root)
    root.location = (side * CUP_X, 0, CUP_Z)
    root.rotation_euler = (0, 0, -side * SPLAY)
    root["part_id"] = "left_earcup" if side < 0 else "right_earcup"
    bpy.context.view_layer.update()

    # Outer shell: an oval puck, axis along X.
    shell = cylinder("shell", 1, 1, (0, 0, 0), (0, math.pi / 2, 0), mats["shell"], verts=64)
    shell.scale = (CUP_H / 2, CUP_W / 2, CUP_T)
    shell.location = (side * CUP_T * 0.15, 0, 0)
    bpy.ops.object.transform_apply(scale=True)
    smooth(shell, bevel=0.011, segments=6, subsurf=1)
    parent(shell, root)
    shell.matrix_world = root.matrix_world @ shell.matrix_world

    # Cushion on the inner side.
    bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.26, major_segments=64,
                                     minor_segments=24, location=(0, 0, 0))
    cushion = link(bpy.context.object, "cushion")
    # Torus normal is +Z; turn it to X. Local X becomes height, local Y width.
    cushion.scale = (CUP_H / 2 * 0.84, CUP_W / 2 * 0.84, 0.034)
    cushion.rotation_euler = (0, math.pi / 2, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    cushion.location = (-side * (CUP_T / 2 + 0.008), 0, 0)
    cushion.data.materials.append(mats["leather"])
    smooth(cushion, subsurf=1)
    cushion.matrix_world = root.matrix_world @ cushion.matrix_world
    parent(cushion, root)

    # Chrome yoke hugging the upper outer face.
    curve = bpy.data.curves.new("yoke", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.0034
    curve.bevel_resolution = 6
    spline = curve.splines.new("POLY")
    pts = []
    for i in range(25):
        t = -1.25 + 2.5 * i / 24
        p, _ = rim_point(t, inset=-0.0015)
        pts.append(p + Vector((side * (CUP_T * 0.62), 0, 0)))
    spline.points.add(len(pts) - 1)
    for sp, p in zip(spline.points, pts):
        sp.co = (*p, 1)
    yoke = bpy.data.objects.new("yoke", curve)
    bpy.context.collection.objects.link(yoke)
    yoke.data.materials.append(mats["chrome"])
    yoke.matrix_world = root.matrix_world.copy()
    parent(yoke, root)
    arm = box("yoke arm", (0.006, 0.014, 0.03), (side * CUP_T * 0.62, 0, CUP_H / 2 + 0.013),
              mat=mats["chrome"])
    smooth(arm, bevel=0.002, subsurf=1)
    arm.matrix_world = root.matrix_world @ arm.matrix_world
    parent(arm, root)
    return root, shell


def cup_local(root, local_point, local_dir):
    """World position and direction for a point defined in cup-local space."""
    mw = root.matrix_world
    return mw @ local_point, (mw.to_3x3() @ local_dir).normalized()


def surface(shell, root, t, face_x):
    """Exact point/normal on the evaluated shell surface for rim angle t."""
    p, n = rim_point(t)
    mw = root.matrix_world
    origin = mw @ (p + n * 0.02 + Vector((face_x, 0, 0)))
    direction = (mw.to_3x3() @ -n).normalized()
    inv = shell.matrix_world.inverted()
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, normal, _ = shell.evaluated_get(dg).ray_cast(inv @ origin,
                                                        (inv.to_3x3() @ direction).normalized())
    assert hit, f"no shell surface at t={t}"
    return shell.matrix_world @ loc, (shell.matrix_world.to_3x3() @ normal).normalized()


def mount(obj, root, pos, normal, lift=0.0):
    obj.location = pos + normal * lift
    obj.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    parent(obj, root)


def place_on(obj, root, local_point, local_normal):
    pos, normal = cup_local(root, local_point, local_normal)
    obj.location = pos
    obj.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    parent(obj, root)


def left_cup_features(root, shell, mats):
    face_x = -CUP_T * 0.15                      # middle of the rim band
    # 2.5 mm AUX port at the very bottom of the rim (p13 / p33).
    pos, n = surface(shell, root, math.pi - 0.08, face_x)
    ring = cylinder("2.5 mm AUX port ring", 0.0023, 0.0004, (0, 0, 0), mat=mats["chrome"],
                    part="aux_audio_port")
    mount(ring, root, pos, n, 0.0001)
    hole = cylinder("2.5 mm AUX port", 0.00145, 0.0004, (0, 0, 0), mat=mats["hole"])
    mount(hole, root, pos, n, 0.00025)
    # USB-C port just above it toward the rear.
    pos_u, n_u = surface(shell, root, math.pi - 0.42, face_x)
    usb = box("USB-C port", (0.0088, 0.0032, 0.0004), (0, 0, 0), mat=mats["hole"], part="usb_c_port")
    mount(usb, root, pos_u, n_u, 0.00015)
    # Status light above the USB-C port.
    pos_l, n_l = surface(shell, root, math.pi - 0.72, face_x)
    light = cylinder("status light", 0.0011, 0.0003, (0, 0, 0), mat=mats["light"], part="status_light")
    mount(light, root, pos_l, n_l, 0.00015)
    return {"aux": (ring, pos, n), "usb": (usb, pos_u, n_u), "light": light}


def right_cup_features(root, shell, mats):
    face_x = CUP_T * 0.15
    features = {}
    for name, t, size, part in (("Bluetooth/Power button", math.pi - 0.2, (0.0055, 0.0055, 0.0016),
                                 "bluetooth_power_button"),
                                ("Multi-function button", math.pi - 0.95, (0.0055, 0.009, 0.0016),
                                 "multifunction_button")):
        pos, n = surface(shell, root, t, face_x)
        button = box(name, size, (0, 0, 0), mat=mats["button"], part=part)
        smooth(button, bevel=0.0007, subsurf=1)
        mount(button, root, pos, n, 0.0003)
        features[part] = (button, pos, n)
    pos, n = surface(shell, root, math.pi - 0.58, face_x)
    strip = box("Volume strip", (0.0022, 0.02, 0.0004), (0, 0, 0), mat=mats["button"],
                part="volume_strip")
    mount(strip, root, pos, n, 0.0001)
    # Blue press cue ring around the Bluetooth/Power button (pairing only).
    button, pos, n = features["bluetooth_power_button"]
    bpy.ops.mesh.primitive_torus_add(major_radius=0.0052, minor_radius=0.00045)
    cue = link(bpy.context.object, "press cue")
    cue.data.materials.append(mats["cue"])
    mount(cue, root, pos, n, 0.0006)
    features["cue"] = cue
    return features


def headband(mats):
    curve = bpy.data.curves.new("headband", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_mode = "PROFILE"
    curve.bevel_depth = 0.0
    curve.extrude = 0.0
    spline = curve.splines.new("POLY")
    pts = []
    for i in range(41):
        a = math.pi * i / 40
        x = -(CUP_X + 0.004) * math.cos(a)
        z = CUP_H / 2 + 0.035 + (BAND_TOP - CUP_H / 2 - 0.035) * math.sin(a) ** 0.8
        pts.append((x, 0, z))
    spline.points.add(len(pts) - 1)
    for sp, p in zip(spline.points, pts):
        sp.co = (*p, 1)
    # Rounded rectangle cross-section.
    prof = bpy.data.curves.new("band profile", "CURVE")
    ps = prof.splines.new("POLY")
    corners = []
    for cx, cy, a0 in ((0.016, 0.005, 0), (-0.016, 0.005, 90), (-0.016, -0.005, 180),
                       (0.016, -0.005, 270)):
        for k in range(5):
            a = math.radians(a0 + 90 * k / 4)
            corners.append((cx + 0.003 * math.cos(a), cy + 0.003 * math.sin(a), 0))
    ps.points.add(len(corners) - 1)
    for sp, p in zip(ps.points, corners):
        sp.co = (*p, 1)
    ps.use_cyclic_u = True
    prof_obj = bpy.data.objects.new("band profile", prof)
    bpy.context.collection.objects.link(prof_obj)
    prof_obj.hide_render = True
    prof_obj.hide_viewport = True
    curve.bevel_mode = "OBJECT"
    curve.bevel_object = prof_obj
    band = bpy.data.objects.new("Headband", curve)
    bpy.context.collection.objects.link(band)
    band.data.materials.append(mats["leather"])
    band["part_id"] = "headband"
    return band


# ---------------------------------------------------------------- laptop

LAPTOP_LOC = Vector((-0.34, 0.12, -0.2))


def laptop(mats):
    root = bpy.data.objects.new("Source laptop", None)
    bpy.context.collection.objects.link(root)
    root.location = LAPTOP_LOC
    root.rotation_euler = (0, 0, math.radians(28))
    root["part_id"] = "source_device"
    bpy.context.view_layer.update()
    base = box("laptop base", (0.304, 0.215, 0.011), (0, 0, 0), mat=mats["alu"])
    smooth(base, bevel=0.003, subsurf=0)
    parent(base, root)
    base.matrix_world = root.matrix_world @ base.matrix_world
    keys = box("keyboard", (0.26, 0.1, 0.0008), (0, 0.035, 0.0058), mat=mats["keys"])
    keys.matrix_world = root.matrix_world @ keys.matrix_world
    parent(keys, root)
    hinge = bpy.data.objects.new("lid hinge", None)
    bpy.context.collection.objects.link(hinge)
    hinge.location = (0, 0.1075, 0.0055)
    hinge.rotation_euler = (math.radians(-12), 0, 0)
    hinge.matrix_world = root.matrix_world @ hinge.matrix_world
    parent(hinge, root)
    bpy.context.view_layer.update()
    lid = box("lid", (0.304, 0.008, 0.21), (0, 0.004, 0.105), mat=mats["alu"])
    smooth(lid, bevel=0.003, subsurf=0)
    lid.matrix_world = hinge.matrix_world @ lid.matrix_world
    parent(lid, hinge)
    screen = box("screen", (0.284, 0.0006, 0.184), (0, -0.0003, 0.107), mat=mats["screen"])
    screen.matrix_world = hinge.matrix_world @ screen.matrix_world
    parent(screen, hinge)
    # 3.5 mm headphone jack on the RIGHT side (MacBook Air evidence), USB-C on the left.
    jack = cylinder("3.5 mm headphone jack", 0.0019, 0.006, (0.152, 0.07, 0.0), (0, math.pi / 2, 0),
                    mat=mats["hole"], part="headphone_jack_3_5mm")
    jack.matrix_world = root.matrix_world @ jack.matrix_world
    parent(jack, root)
    usb = box("laptop USB-C port", (0.006, 0.009, 0.0033), (-0.152, 0.07, 0.0), mat=mats["hole"],
              part="usb_c_port_laptop")
    usb.matrix_world = root.matrix_world @ usb.matrix_world
    parent(usb, root)
    bpy.context.view_layer.update()
    return {"root": root, "hinge": hinge, "screen": screen, "jack": jack, "usb": usb}


def screen_ui(lap, mats):
    """A minimal Bluetooth settings panel on the laptop screen (pairing only)."""
    hinge = lap["hinge"]
    items = {}

    def text(name, body, local, size, mat):
        curve = bpy.data.curves.new(name, "FONT")
        curve.body = body
        curve.size = size
        curve.align_x = "LEFT"
        obj = bpy.data.objects.new(name, curve)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(mat)
        obj.location = local
        obj.rotation_euler = (math.pi / 2, 0, 0)
        obj.matrix_world = hinge.matrix_world @ obj.matrix_world
        parent(obj, hinge)
        return obj

    y = -0.0012
    items["title"] = text("ui title", "Bluetooth", (-0.12, y, 0.175), 0.012, mats["ui_text"])
    items["toggle"] = box("ui toggle", (0.024, 0.0004, 0.012), (0.1, y, 0.178), mat=mats["ui_accent"])
    items["toggle"].matrix_world = hinge.matrix_world @ items["toggle"].matrix_world
    parent(items["toggle"], hinge)
    items["label"] = text("ui nearby", "Nearby devices", (-0.12, y, 0.145), 0.007, mats["ui_text"])
    items["row"] = box("ui row", (0.25, 0.0004, 0.018), (0.0, y + 0.0002, 0.122),
                       mat=mats["ui_accent"])
    items["row"].matrix_world = hinge.matrix_world @ items["row"].matrix_world
    parent(items["row"], hinge)
    items["device"] = text("ui device", "BOSE QC ULTRA 2 HP", (-0.11, y - 0.0004, 0.119), 0.008,
                           mats["ui_text"])
    items["status"] = text("ui status", "Connected", (0.055, y - 0.0004, 0.119), 0.0065,
                           mats["ui_text"])
    return items


# ---------------------------------------------------------------- cables

def plug_25(mats, name="2.5 mm plug"):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    parts = [
        cylinder("pin tip", 0.00125, 0.004, (0, 0, 0.012), mat=mats["pin"], verts=24),
        cylinder("pin ring 1", 0.00126, 0.0006, (0, 0, 0.0097), mat=mats["insulator"], verts=24),
        cylinder("pin sleeve", 0.00125, 0.0035, (0, 0, 0.0075), mat=mats["pin"], verts=24),
        cylinder("pin ring 2", 0.00126, 0.0006, (0, 0, 0.0054), mat=mats["insulator"], verts=24),
        cylinder("pin base", 0.00125, 0.0028, (0, 0, 0.0035), mat=mats["pin"], verts=24),
        cylinder("plug housing", 0.0032, 0.016, (0, 0, -0.006), mat=mats["insulator"], verts=32),
        cylinder("strain relief", 0.0019, 0.012, (0, 0, -0.02), mat=mats["cable"], verts=24),
    ]
    for p in parts:
        smooth(p, subsurf=0)
        parent(p, root)
    return root


def plug_35(mats):
    root = plug_25(mats, "3.5 mm plug")
    root.scale = (1.4, 1.4, 1.25)
    return root


def plug_usbc(mats, name):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    tongue = box("USB-C tongue", (0.0083, 0.0026, 0.0065), (0, 0, 0.0033), mat=mats["pin"])
    smooth(tongue, bevel=0.0011, subsurf=0)
    housing = box("USB-C housing", (0.012, 0.0055, 0.018), (0, 0, -0.009), mat=mats["insulator"])
    smooth(housing, bevel=0.002, subsurf=0)
    relief = cylinder("strain relief", 0.0022, 0.012, (0, 0, -0.024), mat=mats["cable"], verts=24)
    for p in (tongue, housing, relief):
        parent(p, root)
    return root


def cable_between(mats, start_obj, end_obj, sag=0.12, tail=0.03):
    """A cable whose ends follow two plug objects (hooked Bezier curve)."""
    curve = bpy.data.curves.new("cable", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.0017
    curve.bevel_resolution = 4
    curve.resolution_u = 24
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(2)
    cable = bpy.data.objects.new("audio cable", curve)
    bpy.context.collection.objects.link(cable)
    cable.data.materials.append(mats["cable"])
    for index, handle_len, target in ((0, tail, start_obj), (2, tail, end_obj)):
        point = spline.bezier_points[index]
        point.handle_left_type = point.handle_right_type = "FREE"
        hook_empty = bpy.data.objects.new(f"cable hook {index}", None)
        bpy.context.collection.objects.link(hook_empty)
        hook_empty.parent = target
        hook_empty.location = (0, 0, -0.026)
        bpy.context.view_layer.update()
        world = hook_empty.matrix_world.translation
        down = (target.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()
        point.co = world
        point.handle_left = world - down * handle_len if index == 0 else world + down * handle_len
        point.handle_right = world + down * handle_len if index == 0 else world - down * handle_len
        mod = cable.modifiers.new(f"hook {index}", "HOOK")
        mod.object = hook_empty
        mod.vertex_indices_set([index * 3, index * 3 + 1, index * 3 + 2])
    mid = spline.bezier_points[1]
    a = spline.bezier_points[0].co
    b = spline.bezier_points[2].co
    mid.co = (a + b) / 2 + Vector((0, -0.03, -sag))
    mid.handle_left_type = mid.handle_right_type = "AUTO"
    return cable


# ---------------------------------------------------------------- studio

def studio(mats):
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, -0.2055))
    floor = bpy.context.object
    floor.name = "STUDIO floor"
    floor.data.materials.append(mats["floor"])
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.42, 0.43, 0.45, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.22
    for name, loc, energy, size in (("Key", (-0.6, -0.9, 0.9), 90, 0.9),
                                    ("Fill", (0.9, -0.7, 0.3), 35, 1.2),
                                    ("Rim", (0.2, 0.9, 0.8), 60, 0.6),
                                    ("Under", (0.0, -0.5, -0.15), 12, 0.5)):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.size = size
        light = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(light)
        light.location = loc
        light.rotation_euler = (Vector((0, 0, -0.02)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def camera(name, lens=50):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.002
    data.dof.use_dof = True
    data.dof.aperture_fstop = 8.0
    cam = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(cam)
    target = bpy.data.objects.new(name + " target", None)
    bpy.context.collection.objects.link(target)
    constraint = cam.constraints.new("TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    data.dof.focus_object = target
    return cam, target


def key(obj, frame, **values):
    for attr, value in values.items():
        setattr(obj, attr, value)
        obj.keyframe_insert(attr, frame=frame)


def ease_all():
    for action in bpy.data.actions:
        for fcurve in getattr(action, "fcurves", []):
            for kp in fcurve.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.easing = "AUTO"


def key_emission(mat, frame, strength, color=None):
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    if color is not None:
        bsdf.inputs["Emission Color"].default_value = (*color, 1)
        bsdf.inputs["Emission Color"].keyframe_insert("default_value", frame=frame)
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=frame)


# ---------------------------------------------------------------- procedures

def aim_plug(plug, target_pos, axis, distance):
    """Place plug so its pin points along `axis` into target, `distance` back."""
    plug.rotation_euler = axis.to_track_quat("Z", "Y").to_euler()
    plug.location = target_pos - axis * distance


def build_wired(proc, mats, left_root, left_feat, lap):
    scene = bpy.context.scene
    usb = proc == "connect_usb_audio"
    # Headphone end: enters the left earcup port from outside along -normal.
    if usb:
        _, port_pos, normal = left_feat["usb"]
        head_plug = plug_usbc(mats, "USB-C plug (headphone end)")
        insert = 0.0066
    else:
        _, port_pos, normal = left_feat["aux"]
        head_plug = plug_25(mats)
        insert = 0.0128
    into_cup = -normal
    # Source end: into the laptop side port along -X (right side) or +X (left side).
    lap_root = lap["root"]
    lap_port = lap["usb"] if usb else lap["jack"]
    lap_pos = lap_port.matrix_world.translation.copy()
    side = Vector((-1, 0, 0)) if not usb else Vector((1, 0, 0))
    into_lap = (lap_root.matrix_world.to_3x3() @ side).normalized()
    src_plug = plug_usbc(mats, "USB-C plug (source end)") if usb else plug_35(mats)

    # Timeline (24 fps): 0-1 s settle, 1-3.5 s step 1, 3.5-4 s hold,
    # 4-6.5 s step 2, 6.5-8 s hold.
    aim_plug(head_plug, port_pos, into_cup, 0.05 + insert)
    key(head_plug, 1, location=head_plug.location.copy())
    key(head_plug, 24, location=head_plug.location.copy())
    aim_plug(head_plug, port_pos, into_cup, 0.014 + insert)
    key(head_plug, 60, location=head_plug.location.copy())
    # Final: plug housing seated against the shell, pin fully inside.
    aim_plug(head_plug, port_pos, into_cup, 0.0 if usb else 0.0021)
    key(head_plug, 80, location=head_plug.location.copy())

    aim_plug(src_plug, lap_pos, into_lap, 0.07)
    src_plug.location += Vector((0, 0, -0.03))
    key(src_plug, 1, location=src_plug.location.copy())
    key(src_plug, 96, location=src_plug.location.copy())
    aim_plug(src_plug, lap_pos, into_lap, 0.02)
    key(src_plug, 136, location=src_plug.location.copy())
    aim_plug(src_plug, lap_pos, into_lap, 0.0 if usb else 0.0025)
    key(src_plug, 156, location=src_plug.location.copy())
    bpy.context.view_layer.update()
    scene.frame_set(1)
    cable_between(mats, head_plug, src_plug, sag=0.09)

    cam, target = camera("Camera_Main", lens=50)
    heads = Vector((0, 0, 0.03))
    key(target, 1, location=heads)
    key(cam, 1, location=heads + Vector((-0.16, -0.52, 0.06)))
    key(target, 20, location=heads + Vector((-0.04, 0, -0.02)))
    key(cam, 20, location=heads + Vector((-0.16, -0.48, 0.03)))
    close = port_pos + Vector((0, 0, -0.018))
    key(target, 44, location=close)
    key(cam, 44, location=close + Vector((-0.06, -0.15, -0.035)))
    key(target, 86, location=close + Vector((0, 0, 0.004)))
    key(cam, 86, location=close + Vector((-0.05, -0.13, -0.03)))
    lap_close = lap_pos + Vector((0, 0, 0.005))
    key(target, 112, location=lap_close)
    key(cam, 112, location=lap_close + Vector((0.13, -0.17, 0.07)))
    key(target, 160, location=lap_close)
    key(cam, 160, location=lap_close + Vector((0.1, -0.13, 0.05)))
    mid = (port_pos + lap_pos) / 2 + Vector((0, 0, 0.04))
    key(target, 193, location=mid)
    key(cam, 193, location=mid + Vector((0.08, -0.72, 0.2)))
    wide, wide_target = camera("Camera_Wide", lens=35)
    wide_target.location = mid
    wide.location = mid + Vector((0.05, -0.75, 0.22))
    return cam


def build_pairing(mats, left_feat, right_feat, lap):
    scene = bpy.context.scene
    button, p, n = right_feat["bluetooth_power_button"]
    rest = button.location.copy()
    pressed = rest - n * 0.0009 if False else rest   # button is parented; move in local -Z
    cue = right_feat["cue"]
    light = left_feat["light"]
    screen_mat = mats["screen"]
    ui = screen_ui(lap, mats)

    # Hold the Bluetooth/Power button 1.0-3.4 s (frames 24-82).
    key(button, 1, location=button.location.copy())
    key(button, 22, location=button.location.copy())
    local_in = button.matrix_parent_inverse.to_3x3().inverted() @ Vector((0, 0, 0))
    direction = (button.parent.matrix_world.to_3x3().inverted()
                 @ (button.matrix_world.to_3x3() @ Vector((0, 0, -0.0009))))
    key(button, 26, location=button.location + direction)
    key(button, 80, location=button.location.copy())
    key(button, 84, location=button.location - direction)
    key_emission(mats["cue"], 1, 0.0)
    key_emission(mats["cue"], 22, 0.0)
    key_emission(mats["cue"], 26, 6.0)
    key_emission(mats["cue"], 80, 6.0)
    key_emission(mats["cue"], 86, 0.0)
    # Status light: two white blinks (power-off tone), then pulsing blue (p27, p37).
    white, blue = (1, 1, 1), (0.1, 0.35, 1.0)
    key_emission(mats["light"], 1, 0.0, white)
    for start in (38, 50):
        key_emission(mats["light"], start, 0.0, white)
        key_emission(mats["light"], start + 3, 40.0, white)
        key_emission(mats["light"], start + 7, 0.0, white)
    key_emission(mats["light"], 64, 0.0, blue)
    for k in range(6):
        key_emission(mats["light"], 70 + 20 * k, 45.0, blue)
        key_emission(mats["light"], 80 + 20 * k, 4.0, blue)
    # Laptop: screen on; Bluetooth list shows the headphones, then Connected.
    key_emission(screen_mat, 1, 1.4)
    for name, show in (("title", 96), ("toggle", 96), ("label", 108), ("row", 132),
                       ("device", 118), ("status", 150)):
        obj = ui[name]
        key(obj, 1, hide_render=True)
        key(obj, show - 1, hide_render=True)
        key(obj, show, hide_render=False)
    for fcurve in _fcurves(ui):
        for kp in fcurve.keyframe_points:
            kp.interpolation = "CONSTANT"
    key_emission(mats["ui_accent"], 1, 0.0)
    key_emission(mats["ui_accent"], 131, 0.0)
    key_emission(mats["ui_accent"], 132, 0.6)

    cam, target = camera("Camera_Main", lens=60)
    btn_pos = button.matrix_world.translation.copy()
    light_pos = light.matrix_world.translation.copy()
    screen_pos = lap["screen"].matrix_world.translation.copy()
    key(target, 1, location=btn_pos)
    key(cam, 1, location=btn_pos + Vector((0.08, -0.2, -0.05)))
    key(target, 34, location=btn_pos)
    key(cam, 34, location=btn_pos + Vector((0.05, -0.15, -0.04)))
    key(target, 58, location=light_pos)
    key(cam, 58, location=light_pos + Vector((-0.05, -0.15, -0.045)))
    key(target, 92, location=light_pos)
    key(cam, 92, location=light_pos + Vector((-0.045, -0.14, -0.04)))
    key(target, 118, location=screen_pos)
    key(cam, 118, location=screen_pos + Vector((0.0, -0.36, 0.02)))
    key(target, 193, location=screen_pos)
    key(cam, 193, location=screen_pos + Vector((0.0, -0.33, 0.02)))
    wide, wide_target = camera("Camera_Wide", lens=45)
    wide_target.location = (btn_pos + screen_pos) / 2
    wide.location = wide_target.location + Vector((0.0, -0.8, 0.22))
    return cam


def _fcurves(ui):
    for obj in ui.values():
        if obj.animation_data and obj.animation_data.action:
            yield from getattr(obj.animation_data.action, "fcurves", [])


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--procedure", required=True,
                        choices=["connect_aux_cable", "connect_usb_audio", "bluetooth_pairing"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--preview", help="render frames a,b,c to this directory")
    args = parser.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, 193
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.cycles.samples = 32
    mats = materials()
    studio(mats)
    left_root, left_shell = earcup(-1, mats)
    right_root, right_shell = earcup(1, mats)
    headband(mats)
    bpy.context.view_layer.update()
    left_feat = left_cup_features(left_root, left_shell, mats)
    right_feat = right_cup_features(right_root, right_shell, mats)
    lap = laptop(mats)
    if args.procedure == "bluetooth_pairing":
        cam = build_pairing(mats, left_feat, right_feat, lap)
        mats["screen"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.4
    else:
        cam = build_wired(args.procedure, mats, left_root, left_feat, lap)
        key_emission(mats["screen"], 1, 0.6)
        key_emission(mats["light"], 1, 8.0, (1, 1, 1))
    ease_all()
    scene.camera = cam
    scene["identity"] = "Bose QC Ultra Headphones (2nd Gen); geometry INFERRED from official photos"
    scene["procedure"] = args.procedure
    scene["rights"] = "INTERNAL RESEARCH"
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    print("SAVED", out, flush=True)
    if args.preview:
        prev = Path(args.preview)
        prev.mkdir(parents=True, exist_ok=True)
        scene.cycles.samples = 16
        for frame in (1, 45, 80, 130, 160, 193):
            scene.frame_set(frame)
            scene.render.filepath = str(prev / f"{args.procedure}-{frame:04d}.png")
            bpy.ops.render.render(write_still=True)
        print("PREVIEW", prev, flush=True)


main()
