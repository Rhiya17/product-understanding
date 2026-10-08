import bpy, math
from mathutils import Vector, Euler
from math import sin, cos, pi

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
sc = bpy.context.scene
sc.frame_start = 1
sc.frame_end = 288
sc.render.fps = 24
sc.unit_settings.system = 'METRIC'
sc.unit_settings.scale_length = 1


def mat(name, color, rough=.6, metal=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    return m

black = mat('Satin black frame', (.026, .031, .034), .38, .25)
rubber = mat('Rubber', (.015, .019, .022), .83)
plastic = mat('Black molded plastic', (.041, .047, .051), .48)
brakemat = mat('Brake pedal molded black', (.055, .060, .064), .4)
fabric = mat('Grey upholstery', (.26, .275, .285), .94)
meshmat = mat('Basket textile', (.042, .046, .05), 1)
silver = mat('Wheel silver edging', (.62, .66, .68), .28, .7)
brown = mat('Brown handle wrap', (.25, .12, .066), .65)
shoe = mat('Illustrative shoe', (.43, .49, .56), .84)
solemat = mat('Illustrative sole', (.77, .79, .77), .9)
floor = mat('Warm studio floor', (.69, .72, .73), .9)
noise = fabric.node_tree.nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 360
noise.inputs['Detail'].default_value = 2
bump = fabric.node_tree.nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = .13
bump.inputs['Distance'].default_value = .0005
fabric.node_tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
fabric.node_tree.links.new(bump.outputs['Normal'], fabric.node_tree.nodes.get('Principled BSDF').inputs['Normal'])


def finish(o, name, material):
    o.name = name
    if material:
        o.data.materials.append(material)
    return o


def box(name, loc, size, material, bev=.006, parent=None, rot=None):
    bpy.ops.mesh.primitive_cube_add()
    o = finish(bpy.context.object, name, material)
    o.parent = parent
    o.location = loc
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rot:
        o.rotation_euler = rot
    if bev:
        mod = o.modifiers.new('Rounded edges', 'BEVEL')
        mod.width = bev
        mod.segments = 3
        o.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return o


def rod(name, a, b, radius, material, parent=None):
    a, b = Vector(a), Vector(b)
    direction = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=radius, depth=direction.length)
    o = finish(bpy.context.object, name, material)
    o.parent = parent
    o.location = (a + b) / 2
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = direction.to_track_quat('Z', 'Y')
    for polygon in o.data.polygons:
        polygon.use_smooth = True
    return o


def curve(name, points, radius, material, parent=None, smooth=False):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = radius
    data.bevel_resolution = 2
    data.resolution_u = 12
    spline = data.splines.new('BEZIER' if smooth else 'POLY')
    if smooth:
        spline.bezier_points.add(len(points) - 1)
        for point, co in zip(spline.bezier_points, points):
            point.co = co
            point.handle_left_type = 'AUTO'
            point.handle_right_type = 'AUTO'
    else:
        spline.points.add(len(points) - 1)
        for point, co in zip(spline.points, points):
            point.co = (*co, 1)
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.parent = parent
    data.materials.append(material)
    return o


def surface(name, vertices, faces, material, thick=0):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    mesh.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    if thick:
        mod = o.modifiers.new('Cloth thickness', 'SOLIDIFY')
        mod.thickness = thick
    return o


def torus(name, loc, major, minor, material):
    bpy.ops.mesh.primitive_torus_add(major_segments=48, minor_segments=10, location=loc, major_radius=major, minor_radius=minor, rotation=(0, pi / 2, 0))
    o = finish(bpy.context.object, name, material)
    for polygon in o.data.polygons:
        polygon.use_smooth = True
    return o


def empty(name, loc):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.location = loc
    return o


# Open stroller: front is -Y; handle, rear axle and brake tabs are +Y.
for label, side in [('L', -1), ('R', 1)]:
    x = side * .202
    curve('Frame_' + label, [(x, -.323, .174), (x, -.294, .278), (x, -.036, .574), (x, .281, .947)], .0125, black, smooth=True)
    rod('RearLeg_' + label, (x, .284, .098), (x, -.018, .575), .012, black)
    rod('SideJoint_' + label, (x - side * .013, -.015, .567), (x + side * .014, -.015, .567), .031, plastic)
    rod('FrontSwivel_' + label, (x, -.326, .123), (x, -.326, .204), .022, plastic)
    curve('FrontFork_' + label, [(x + side * .012, -.326, .147), (x + side * .017, -.342, .105), (x + side * .018, -.352, .066)], .016, plastic)
    rod('RearBrakeHousing_' + label, (side * .193, .285, .101), (side * .234, .285, .101), .023, plastic)

curve('Handlebar', [(-.202, .279, .934), (-.202, .339, 1.022), (-.159, .365, 1.046), (.159, .365, 1.046), (.202, .339, 1.022), (.202, .279, .934)], .014, black, smooth=True)
curve('Handle_Grip', [(-.16, .365, 1.046), (-.11, .372, 1.05), (.11, .372, 1.05), (.16, .365, 1.046)], .017, brown, smooth=True)
curve('Front_Footrest', [(-.202, -.323, .196), (-.174, -.365, .195), (.174, -.365, .195), (.202, -.323, .196)], .017, plastic, smooth=True)
rod('Rear_Axle', (-.231, .285, .084), (.231, .285, .084), .009, black)
box('Seat_Base', (0, -.14, .435), (.347, .285, .055), fabric, .022)
box('Seat_Legrest', (0, -.301, .401), (.344, .11, .048), fabric, .017, rot=(.28, 0, 0))
backangle = -math.atan2(.255, .423)
box('Seat_Back', (0, .081, .653), (.347, .055, .492), fabric, .026, rot=(backangle, 0, 0))
for label, side in [('L', -1), ('R', 1)]:
    surface('Seat_Wing_' + label, [(side * .176, -.265, .446), (side * .176, .025, .445), (side * .188, .246, .868), (side * .188, .147, .668)], [(0, 1, 2, 3)], meshmat, .004)
    box('ShoulderStrap_' + label, (side * .069, .027, .69), (.024, .007, .286), rubber, .002, rot=(backangle, 0, 0))
    box('HarnessPad_' + label, (side * .069, -.005, .625), (.047, .027, .128), fabric, .012, rot=(backangle, 0, 0))
    curve('LapStrap_' + label, [(side * .164, -.091, .472), (side * .087, -.13, .477), (0, -.14, .486)], .011, rubber)
box('Harness_Buckle', (0, -.147, .49), (.059, .022, .041), plastic, .006)
curve('Bumper_Bar', [(-.198, -.066, .541), (-.189, -.231, .596), (-.135, -.275, .619), (.135, -.275, .619), (.189, -.231, .596), (.198, -.066, .541)], .016, plastic, smooth=True)

# Curved grey canopy.
rows = [(.238, .832, 1.009, .207), (.102, .825, 1.069, .226), (-.126, .811, 1.034, .236), (-.337, .793, .941, .226)]
vertices = []
count = 25
for y, z, height, width in rows:
    for j in range(count):
        angle = pi * j / (count - 1)
        vertices.append((-width * cos(angle), y, z + (height - z) * sin(angle) ** .8))
faces = []
for i in range(len(rows) - 1):
    for j in range(count - 1):
        k = i * count + j
        faces.append((k, k + 1, k + 1 + count, k + count))
surface('Canopy', vertices, faces, fabric, .003)
for k in [0, 1, 3]:
    curve('Canopy_Seam_' + str(k), vertices[k * count:(k + 1) * count], .002, meshmat)
front = vertices[-count:]
valance = front + [(x, y + .008, z - .047) for x, y, z in front]
surface('Canopy_Valance', valance, [(j, j + 1, j + 1 + count, j + count) for j in range(count - 1)], fabric, .003)

# Open cupholder shell.
vertices = []
for z, radius in [(.775, .031), (.849, .042), (.849, .036), (.786, .026)]:
    for j in range(32):
        angle = 2 * pi * j / 32
        vertices.append((-.263 + radius * cos(angle), .237 + radius * sin(angle), z))
faces = []
for k in range(3):
    for j in range(32):
        faces.append((k * 32 + j, k * 32 + (j + 1) % 32, (k + 1) * 32 + (j + 1) % 32, (k + 1) * 32 + j))
faces.append(tuple(range(96, 128)))
surface('Cupholder', vertices, faces, plastic)

# Basket: flat textile base and open woven sides.
box('Basket_Base', (0, -.015, .178), (.364, .477, .022), meshmat, .025)
for label, side in [('L', -1), ('R', 1)]:
    x = side * .182
    def panel(u, w):
        return (x, -.252 + .477 * u, .188 + w * (.093 + .06 * u))
    data = bpy.data.curves.new('Basket weave ' + label, 'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = .00065
    data.bevel_resolution = 0
    for sign in [-1, 1]:
        for k in range(-28, 57):
            h = k / 28
            hits = []
            for u, w in [(0, h), (1, h - sign), (h / sign, 0), ((h - 1) / sign, 1)]:
                if 0 <= u <= 1 and 0 <= w <= 1:
                    point = panel(u, w)
                    if point not in hits:
                        hits.append(point)
            if len(hits) >= 2:
                spline = data.splines.new('POLY')
                spline.points.add(1)
                for point, co in zip(spline.points, hits[:2]):
                    point.co = (*co, 1)
    o = bpy.data.objects.new('Basket_Mesh_' + label, data)
    bpy.context.collection.objects.link(o)
    data.materials.append(meshmat)
    curve('Basket_Binding_' + label, [panel(0, 0), panel(0, 1), panel(1, 1), panel(1, 0)], .007, meshmat)

# Four single wheels with three-spoke silver edging.
for end, y, z, radius in [('Rear', .285, .077, .076), ('Front', -.352, .066, .065)]:
    for label, side in [('L', -1), ('R', 1)]:
        x = side * (.245 if end == 'Rear' else .216)
        name = end + 'Wheel_' + label
        torus(name + '_Tire', (x, y, z), radius - .013, .013, rubber)
        torus(name + '_Rim', (x, y, z), radius - .025, .007, plastic)
        vertices = []
        for j in range(96):
            angle = 2 * pi * j / 96
            spoke_radius = radius * (.405 + .265 * cos(3 * angle))
            vertices.append((x + side * .013, y + spoke_radius * sin(angle), z + spoke_radius * cos(angle)))
        surface(name + '_Spokes', vertices, [tuple(range(96))], plastic, .007)
        curve(name + '_SilverEdge', [(a + side * .004, b, c) for a, b, c in vertices] + [(vertices[0][0] + side * .004, vertices[0][1], vertices[0][2])], .0018, silver)
        rod(name + '_Hub', (x - side * .019, y, z), (x + side * .022, y, z), radius * .225, plastic)


# Explicit solid brake-tab meshes. Vertices remain pivot-local.
def brake_tab(name, parent):
    outline = [(-.014, -.0055), (.014, -.0055), (.019, -.0005), (.019, .0545), (.014, .0615), (-.014, .0615), (-.019, .0545), (-.019, -.0005)]
    vertices = [(x, y, z) for z in [-.0065, .0065] for x, y in outline]
    faces = [tuple(reversed(range(8))), tuple(range(8, 16))]
    for j in range(8):
        k = (j + 1) % 8
        faces.append((j, k, k + 8, j + 8))
    material_ids = [0] * len(faces)
    for yc in [.025, .036, .047]:
        k = len(vertices)
        vertices.extend([(-.014, yc - .0015, .0065), (.014, yc - .0015, .0065), (.014, yc + .0015, .0065), (-.014, yc + .0015, .0065), (-.014, yc - .0015, .0095), (.014, yc - .0015, .0095), (.014, yc + .0015, .0095), (-.014, yc + .0015, .0095)])
        for face in [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            faces.append(tuple(k + i for i in face))
            material_ids.append(1)
    mesh = bpy.data.meshes.new(name + '_Mesh')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    o.parent = parent
    o.location = (0, 0, 0)
    o.rotation_euler = (0, 0, 0)
    o.scale = (1, 1, 1)
    mesh.materials.append(brakemat)
    mesh.materials.append(rubber)
    for polygon, material_index in zip(mesh.polygons, material_ids):
        polygon.material_index = material_index
    mod = o.modifiers.new('Molded tab edge bevel', 'BEVEL')
    mod.width = .0013
    mod.segments = 3
    o.modifiers.new('Tab weighted normals', 'WEIGHTED_NORMAL')
    o.hide_render = False
    o.hide_viewport = False
    o['component'] = 'Visible rear-wheel brake pedal'
    return o

# The raised pose now projects clear of the axle in the elevated rear view.
# Pedal dimensions, hinges and housing positions are unchanged.
up = math.radians(25)
down = math.radians(-22)
joints = {}
for label, side in [('L', -1), ('R', 1)]:
    joint = empty('BrakePivot_' + label, (side * .183, .285, .102))
    joint.rotation_mode = 'XYZ'
    joints[label] = joint
    brake_tab('Brake_Pedal_' + label, joint)
    rod('BrakePivotCap_' + label, (side * .16, .285, .102), (side * .208, .285, .102), .012, plastic)
    if label == 'R':
        keys = [(1, up), (94, up), (118, down), (191, down), (209, up), (288, up)]
    else:
        keys = [(1, up), (136, up), (155, down), (236, down), (252, up), (288, up)]
    for frame, angle in keys:
        joint.rotation_euler = (angle, 0, 0)
        joint.keyframe_insert(data_path='rotation_euler', frame=frame)

# The same rigid demonstration shoe; its geometry and dimensions are unchanged.
foot = empty('Demonstration_Foot', (0, 0, 0))
foot.rotation_mode = 'QUATERNION'
box('Demo_Shoe_Sole', (0, .088, .007), (.067, .213, .014), solemat, .008, foot)
box('Demo_Shoe_Upper', (0, .087, .034), (.062, .191, .043), shoe, .012, foot)
box('Shoe_Heel_Collar', (0, .153, .058), (.049, .05, .022), shoe, .009, foot)
for j in range(4):
    curve('Shoe_Lace_' + str(j), [(-.021, .055 + j * .014, .057), (.021, .061 + j * .014, .057)], .0015, solemat, foot)


def contact_pose(label, angle, under=False):
    side = 1 if label == 'R' else -1
    pedal_rotation = Euler((angle, 0, 0)).to_matrix()
    if under:
        # Preserve the toe-under lifting gesture and low heel.
        progress = max(0, min(1, (angle - down) / (up - down)))
        pitch = math.radians(-12) * progress
        point = Vector((0, .059, -.0065))
        corner_angle = max(0, angle - pitch)
        shoe_contact = Vector((0, .0035 - .012 * sin(corner_angle), .0435 + .012 * cos(corner_angle)))
        shoe_rotation = Euler((pitch, 0, 0)).to_matrix()
        position = Vector(joints[label].location) + pedal_rotation @ point - shoe_rotation @ shoe_contact
        position.x -= side * .033
    else:
        # A real point on the flat sole contacts the inner half of the last
        # pedal rib. Turning the heel inward exposes the outer pedal edge.
        # Both contact points are transformed analytically every press frame.
        point = Vector((-side * .009, .047, .0095))
        shoe_contact = Vector((side * .023, -.007, 0))
        yaw = Euler((0, 0, side * math.radians(55))).to_matrix()
        shoe_rotation = pedal_rotation @ yaw
        position = Vector(joints[label].location) + pedal_rotation @ point - shoe_rotation @ shoe_contact
    return position, shoe_rotation.to_quaternion()


def shifted(pose, y=0, z=0):
    return pose[0] + Vector((0, y, z)), pose[1].copy()


neutral = Euler((0, 0, 0)).to_quaternion()
home = (Vector((.43, .61, .002)), neutral.copy())
retreat = (Vector((.43, .68, .055)), neutral.copy())
poses = {
    1: home, 78: home,
    86: shifted(contact_pose('R', up), .06, .05),
    90: shifted(contact_pose('R', up), .018, .025),
    94: contact_pose('R', up),
    118: contact_pose('R', down),
    126: contact_pose('R', down),
    130: shifted(contact_pose('R', down), .045, .025),
    133: shifted(contact_pose('L', up), .015, .025),
    136: contact_pose('L', up),
    155: contact_pose('L', down),
    159: contact_pose('L', down),
    166: retreat, 175: retreat,
    184: shifted(contact_pose('R', down, True), .12),
    191: contact_pose('R', down, True),
    209: contact_pose('R', up, True),
    212: contact_pose('R', up, True),
    219: shifted(contact_pose('R', up, True), .13),
    229: shifted(contact_pose('L', down, True), .12),
    236: contact_pose('L', down, True),
    252: contact_pose('L', up, True),
    255: contact_pose('L', up, True),
    262: shifted(contact_pose('L', up, True), .15),
    264: home, 288: home
}

# Rotation starts at first contact. Every intervening contact pose is baked,
# so there is no independent shoe interpolation across the moving tab.
for label, start, end, angle_a, angle_b, under in [
    ('R', 94, 118, up, down, False),
    ('L', 136, 155, up, down, False),
    ('R', 191, 209, down, up, True),
    ('L', 236, 252, down, up, True)
]:
    for frame in range(start, end + 1):
        angle = angle_a + (angle_b - angle_a) * (frame - start) / (end - start)
        poses[frame] = contact_pose(label, angle, under)
for frame, (position, rotation) in sorted(poses.items()):
    foot.location = position
    foot.rotation_quaternion = rotation
    foot.keyframe_insert(data_path='location', frame=frame)
    foot.keyframe_insert(data_path='rotation_quaternion', frame=frame)


def set_linear(o):
    if not o.animation_data or not o.animation_data.action:
        return
    action = o.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fcurve in bag.fcurves:
                    for key in fcurve.keyframe_points:
                        key.interpolation = 'LINEAR'


for o in list(joints.values()) + [foot]:
    set_linear(o)

# Existing studio lighting is preserved.
box('Studio_Floor', (0, 0, -.024), (200, 200, .04), floor, 0)
world = bpy.data.worlds.new('Studio World')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (.72, .78, .84, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = .35
sc.world = world
for name, loc, power, size, target in [
    ('Key', (2, -3, 4), 380, 3, (0, 0, .4)),
    ('Rear fill', (-2, 2.6, 3), 300, 2.5, (0, 0, .4)),
    ('Brake fill', (.3, 3, 1.6), 120, 1.8, (0, 0, .4)),
    ('Low pedal fill', (0, .98, .165), 24, .55, (0, .32, .12))
]:
    data = bpy.data.lights.new(name, 'AREA')
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.location = loc
    data.energy = power
    data.shape = 'DISK'
    data.size = size
    o.rotation_euler = (Vector(target) - o.location).to_track_quat('-Z', 'Y').to_euler()

# The establishing shot is unchanged. A higher rear close-up exposes the
# toe/sole contact and projects the raised tab tips beyond the axle tube.
data = bpy.data.cameras.new('Instruction Camera')
cam = bpy.data.objects.new('Instruction Camera', data)
bpy.context.collection.objects.link(cam)
sc.camera = cam
data.lens = 50
data.clip_start = .025
data.clip_end = 250
cam.rotation_mode = 'QUATERNION'
for frame, position, target in [
    (1, (2.85, -4.125, 2.055), (0, 0, .54)),
    (42, (2.85, -4.125, 2.055), (0, 0, .54)),
    (59, (1.75, .22, 1.08), (0, .12, .39)),
    (78, (.035, .77, 1.015), (0, .310, .112)),
    (288, (.035, .77, 1.015), (0, .310, .112))
]:
    cam.location = position
    cam.rotation_quaternion = (Vector(target) - cam.location).to_track_quat('-Z', 'Y')
    cam.keyframe_insert(data_path='location', frame=frame)
    cam.keyframe_insert(data_path='rotation_quaternion', frame=frame)


def emission(name, color):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    shader = nodes.new('ShaderNodeEmission')
    shader.inputs['Color'].default_value = (*color, 1)
    material.node_tree.links.new(shader.outputs[0], output.inputs[0])
    return material


ink = emission('Caption panel', (.008, .011, .015))
white = emission('Caption white', (.98, .98, .98))
red = emission('Instruction arrow red', (.82, .018, .012))


def visible_between(o, start, end):
    keys = [(1, False), (end + 1, True)] if start == 1 else [(1, True), (start, False), (end + 1, True)]
    for frame, hidden in keys:
        o.hide_render = hidden
        o.keyframe_insert(data_path='hide_render', frame=frame)
    if hasattr(o, 'visible_shadow'):
        o.visible_shadow = False


# Arrows clarify direction; the physical tabs perform the actions.
def direction_arrow(name, side, lifting, start, end):
    x = side * .100
    y = .405
    a = Vector((x, y, .104 if lifting else .183))
    b = Vector((x, y, .183 if lifting else .104))
    direction = (b - a).normalized()
    head_length = .019
    shaft = rod(name + '_Shaft', a, b - direction * head_length, .0027, red)
    bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=.009, radius2=0, depth=head_length)
    head = finish(bpy.context.object, name + '_Head', red)
    head.location = b - direction * head_length / 2
    head.rotation_mode = 'QUATERNION'
    head.rotation_quaternion = direction.to_track_quat('Z', 'Y')
    for o in (shaft, head):
        o['instructional_annotation'] = True
        visible_between(o, start, end)


direction_arrow('LockArrow_R', 1, False, 79, 130)
direction_arrow('LockArrow_L', -1, False, 133, 166)
direction_arrow('UnlockArrow_R', 1, True, 175, 219)
direction_arrow('UnlockArrow_L', -1, True, 229, 262)

# Existing camera-facing captions and their occlusion repair are preserved.
box('Header_Panel', (0, .112, -.7), (.481, .047, .001), ink, .003, cam)
box('Footer_Panel', (0, -.12, -.7), (.481, .029, .001), ink, .003, cam)


def caption(name, body, y, size, start, end):
    data = bpy.data.curves.new(name, 'FONT')
    data.body = body
    data.size = size
    data.align_y = 'CENTER'
    data.materials.append(white)
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.parent = cam
    o.location = (-.225, y, -.697)
    visible_between(o, start, end)
    return o


caption('Opening_Title', 'Graco Ready2Jet | Brakes', .112, .019, 1, 78)
caption('Lock_Instruction', '1  Push DOWN to lock brakes', .112, .018, 79, 174)
caption('Unlock_Instruction', '2  Push UP to unlock brakes', .112, .018, 175, 288)
caption('Opening_Detail', 'Rear-wheel brake pedals', -.12, .014, 1, 78)
caption('Lock_Detail', 'Press each pedal. Always apply both brakes.', -.12, .0127, 79, 174)
caption('Unlock_Detail', 'Lift each rear-wheel pedal with your toe.', -.12, .0127, 175, 288)

for o in bpy.data.objects:
    if o.parent == cam:
        o.location *= .05
        o.scale *= .05
        if hasattr(o, 'visible_shadow'):
            o.visible_shadow = False

sc['product'] = 'Graco Ready2Jet'
sc['instruction_source'] = 'Ready2Jet manual, page 20'
sc['step_1_claim'] = 'claim_r2j_step_brake_1'
sc['step_2_claim'] = 'claim_r2j_step_brake_2'
sc.frame_set(1)

# User requested arrows only; retain brake animation.
for obj in bpy.data.objects:
    if "shoe" in obj.name.lower() or obj.name == "Demonstration_Foot":
        obj.hide_render = True
        obj.hide_viewport = True
