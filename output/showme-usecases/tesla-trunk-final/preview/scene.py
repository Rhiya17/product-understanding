import bpy, math
from mathutils import Vector, Matrix

# Construction only. The trusted runner saves and renders.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 352
scene.render.fps = 24
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
W, H, D = .5207, .7869, .2921
DEPTH, HEIGHT, ARCH, APERTURE = 1.060, .680, .887, 1.140
GROUND = -.600
REST_X = DEPTH - .025 - W/2


def material(name, color, rough=.5, metal=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    return m


def emissive(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*color, 1)
    e.inputs['Strength'].default_value = 1
    out = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0], out.inputs['Surface'])
    return m


def textile(name, color):
    m = material(name, color, .92)
    n = m.node_tree.nodes
    noise = n.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 180
    noise.inputs['Detail'].default_value = 2
    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .15
    bump.inputs['Distance'].default_value = .001
    m.node_tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    m.node_tree.links.new(bump.outputs['Normal'], n.get('Principled BSDF').inputs['Normal'])
    return m


def inspection_skin(name, color, rough=.3, metal=.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    clear = n.new('ShaderNodeBsdfTransparent')
    clear.inputs['Color'].default_value = (1,1,1,1)
    solid = n.new('ShaderNodeBsdfPrincipled')
    solid.inputs['Base Color'].default_value = (*color,1)
    solid.inputs['Roughness'].default_value = rough
    solid.inputs['Metallic'].default_value = metal
    mix = n.new('ShaderNodeMixShader')
    out = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(clear.outputs[0],mix.inputs[1])
    m.node_tree.links.new(solid.outputs[0],mix.inputs[2])
    m.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
    for frame,opacity in [(1,1),(278,1),(279,0),(352,0)]:
        mix.inputs[0].default_value = opacity
        mix.inputs[0].keyframe_insert(data_path='default_value',frame=frame)
    return m


black = material('Graphite frame', (.016,.019,.022), .38, .25)
rubber = material('Wheel rubber', (.018,.020,.023), .83)
rim = material('Wheel hubs', (.042,.047,.052), .4)
silver = material('Pale spoke edging', (.49,.52,.53), .34, .5)
cloth = textile('Folded grey canopy', (.23,.25,.26))
seatcloth = textile('Dark stroller seat', (.085,.097,.110))
meshcloth = textile('Basket textile', (.025,.030,.036))
stitch = material('Fold seam', (.34,.36,.37), .95)
brown = material('Brown bumper grip', (.31,.15,.078), .66)
paint = material('Red vehicle paint', (.42,.012,.023), .27, .62)
carpet = textile('Dark charcoal cargo carpet', (.075,.080,.086))
trim = material('Dark charcoal interior trim', (.032,.036,.042), .72)
seatmat = material('Rear seat upholstery', (.043,.049,.057), .65)
glass = material('Dark panoramic glazing', (.012,.025,.039), .17, .35)
aero = material('Aero wheel finish', (.035,.043,.054), .38, .45)
red = emissive('Rear red lenses', (.58,.012,.018))
white = emissive('Callout white', (1,1,1))
nearblack = emissive('Opaque callout panels', (.003,.004,.006))
headlamp = material('Headlamp lens', (.52,.60,.67), .2, .45)
stage = material('Studio floor', (.58,.63,.67), .88)
proxy_mat = material('Hidden collision proxy material', (.15,.15,.15))
hatch_paint = inspection_skin('Red hatch paint inspection cutaway', (.42,.012,.023), .27, .62)
hatch_glass = inspection_skin('Hatch glazing inspection cutaway', (.012,.025,.039), .18, .3)
hatch_trim = inspection_skin('Hatch lining inspection cutaway', (.032,.036,.042), .7, 0)

# Retain the previously corrected interior and stroller reflectance.
reflectance_repairs = [
    (carpet, (.011,.014,.018), .16),
    (trim, (.008,.010,.014), .20),
    (seatmat, (.008,.010,.014), .20),
    (black, (.0045,.0055,.0070), .18),
    (rubber, (.007,.008,.010), .12),
    (rim, (.015,.018,.022), .20),
    (cloth, (.140,.153,.165), .20),
    (seatcloth, (.025,.030,.036), .16),
    (meshcloth, (.008,.010,.013), .14)
]
for mat, rgb, specular in reflectance_repairs:
    p = mat.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*rgb,1)
    if 'Specular IOR Level' in p.inputs:
        p.inputs['Specular IOR Level'].default_value = specular
p = next(n for n in hatch_trim.node_tree.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled')
p.inputs['Base Color'].default_value = (.008,.010,.014,1)
if 'Specular IOR Level' in p.inputs:
    p.inputs['Specular IOR Level'].default_value = .20


def assign(o, m):
    o.data.materials.append(m)
    return o


def box(name, loc, size, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, mat)
    if bevel:
        mod = o.modifiers.new('Manufactured edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return o


def mesh_obj(name, vertices, faces, mat, smooth=False):
    me = bpy.data.meshes.new(name + '_Mesh')
    me.from_pydata(vertices, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    assign(o, mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


def tube(name, points, radius, mat, convert=True):
    cu = bpy.data.curves.new(name + '_Path', 'CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = 1
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.use_fill_caps = True
    sp = cu.splines.new('POLY')
    sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):
        p.co = (*co,1)
    o = bpy.data.objects.new(name,cu)
    bpy.context.collection.objects.link(o)
    assign(o,mat)
    if convert:
        bpy.ops.object.select_all(action='DESELECT')
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.convert(target='MESH')
        o = bpy.context.object
        for p in o.data.polygons:
            p.use_smooth = True
    return o


def cylinder(name, a, b, radius, mat, vertices=24):
    a,b = Vector(a),Vector(b)
    v = b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=v.length,location=(a+b)/2)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = v.to_track_quat('Z','Y').to_euler()
    assign(o,mat)
    for p in o.data.polygons:
        p.use_smooth = len(p.vertices)==4
    return o


def torus(name, loc, major, minor, mat, axis='X'):
    bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=12,location=loc,major_radius=major,minor_radius=minor)
    o = bpy.context.object
    o.name = name
    if axis=='X':
        o.rotation_euler[1] = math.pi/2
    elif axis=='Y':
        o.rotation_euler[0] = math.pi/2
    assign(o,mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def joined(name, objects):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return o


def empty(name, loc=(0,0,0), parent=None):
    o = bpy.data.objects.new(name,None)
    bpy.context.collection.objects.link(o)
    o.parent = parent
    o.location = loc
    o.empty_display_size = .05
    return o


def skin(name, rows, mat, offset):
    nr,nc = len(rows),len(rows[0])
    vs = [tuple(p) for row in rows for p in row]
    count = len(vs)
    delta = Vector(offset)
    vs += [tuple(Vector(p)+delta) for p in vs[:count]]
    fs = []
    for j in range(nr-1):
        for i in range(nc-1):
            a = j*nc+i
            q = (a,a+1,a+nc+1,a+nc)
            fs.append(q)
            fs.append(tuple(v+count for v in reversed(q)))
    edge = list(range(nc))+[j*nc+nc-1 for j in range(1,nr)]+[(nr-1)*nc+i for i in range(nc-2,-1,-1)]+[j*nc for j in range(nr-2,0,-1)]
    for i,a in enumerate(edge):
        b = edge[(i+1)%len(edge)]
        fs.append((a,b,b+count,a+count))
    return mesh_obj(name,vs,fs,mat,True)


def exterior_profile(x, stations):
    if x<=stations[0][0]:
        return stations[0][1]
    if x>=stations[-1][0]:
        return stations[-1][1]
    slopes = [(stations[i+1][1]-stations[i][1])/(stations[i+1][0]-stations[i][0]) for i in range(len(stations)-1)]
    def tangent(i):
        if i==0:
            return slopes[0]
        if i==len(stations)-1:
            return slopes[-1]
        a,b = slopes[i-1],slopes[i]
        if a*b<=0:
            return 0.0
        return 2*a*b/(a+b)
    for i in range(len(stations)-1):
        a,va = stations[i]
        b,vb = stations[i+1]
        if x<=b:
            h = b-a
            t = (x-a)/h
            return (2*t**3-3*t*t+1)*va+(t**3-2*t*t+t)*h*tangent(i)+(-2*t**3+3*t*t)*vb+(t**3-t*t)*h*tangent(i+1)


def action_curves(action):
    if action is None:
        return []
    try:
        return list(action.fcurves)
    except AttributeError:
        curves = []
        for layer in action.layers:
            for strip in layer.strips:
                for slot in action.slots:
                    try:
                        bag = strip.channelbag(slot)
                        if bag:
                            curves.extend(bag.fcurves)
                    except (AttributeError,RuntimeError):
                        pass
        return curves


def smooth_action(o):
    if not o.animation_data:
        return
    for fc in action_curves(o.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = 'AUTO_CLAMPED'
            kp.handle_right_type = 'AUTO_CLAMPED'


# The rigid folded stroller is unchanged.
stroller = []
for sign,side in [(-1,'L'),(1,'R')]:
    x = sign*.192
    rods = [tube('_rail',[(x,.071,.096),(x,.032,.596)],.012,black),tube('_rail',[(x,-.083,.103),(x,-.074,.248),(x,.027,.582)],.011,black),tube('_rail',[(x,.063,.101),(x,.095,.247),(x,.049,.538)],.010,black),tube('_fork',[(x,-.083,.063),(x,-.083,.155),(x,-.055,.203)],.014,black)]
    stroller.append(joined('STROLLER_Frame_'+side,rods))
    pieces = []
    for y,z,r in [(.031,.594,.027),(-.061,.252,.022)]:
        pieces.append(cylinder('_hinge',(x-.014,y,z),(x+.014,y,z),r,black))
        pieces.append(cylinder('_pin',(x+sign*.014,y,z),(x+sign*.017,y,z),.005,silver))
    stroller.append(joined('STROLLER_Hinges_'+side,pieces))
handle = [(-.185,.027,.577),(-.185,.033,.657),(-.179,.057,.728),(-.162,.079,.766),(-.143,.081,.7729),(.143,.081,.7729),(.162,.079,.766),(.179,.057,.728),(.185,.033,.657),(.185,.027,.577)]
stroller.append(tube('STROLLER_PushHandle',handle,.014,black))
stroller.append(joined('STROLLER_CrossBraces',[cylinder('_brace',(-.19,.059,.123),(.19,.059,.123),.009,black),cylinder('_brace',(-.18,.022,.568),(.18,.022,.568),.010,black),cylinder('_brace',(-.176,-.032,.237),(.176,-.032,.237),.008,black)]))
for front in [False,True]:
    for sign,side in [(-1,'L'),(1,'R')]:
        r = .063 if front else .074
        x = sign*(.192 if front else .24635)
        y = -.08305 if front else .07205
        z = r
        minor = .012 if front else .014
        pieces = [torus('_tire',(x,y,z),r-minor,minor,rubber)]
        pieces.append(torus('_rim',(x,y,z),r*.69,.005,rim))
        pieces.append(cylinder('_hub',(x-.012,y,z),(x+.012,y,z),.017,rim))
        face_x = x+sign*.010
        for k in range(3):
            angle = math.radians(90+k*120)
            dy,dz = math.cos(angle),math.sin(angle)
            pieces.append(cylinder('_spoke',(x,y+dy*.011,z+dz*.011),(x,y+dy*r*.70,z+dz*r*.70),.008,rim,16))
            pts = []
            for rr,off in [(.18,-.18),(.52,-.19),(.71,0),(.52,.19),(.18,.18)]:
                a = angle+off
                pts.append((face_x,y+math.cos(a)*r*rr,z+math.sin(a)*r*rr))
            pieces.append(tube('_spoke_edge',pts,.0017,silver))
        stroller.append(joined('STROLLER_'+('FrontWheel_' if front else 'RearWheel_')+side,pieces))
stroller.append(box('STROLLER_FoldedSeat',(0,-.004,.400),(.342,.083,.401),seatcloth,.025))
nx,nz = 12,18
verts = []
for back in [False,True]:
    for j in range(nz+1):
        t = j/nz
        zz = .211+.425*t
        half = .149+.025*math.sin(t*math.pi/2)
        for i in range(nx+1):
            u = 2*i/nx-1
            yy = -.086+.012*math.cos(u*math.pi*3)+.008*math.sin(t*math.pi*4+u)
            yy += .019 if back else 0
            verts.append((u*half,yy,zz-.013*u*u*math.sin(math.pi*t)))
stride = nx+1
layer = stride*(nz+1)
faces = []
for k in range(2):
    off = k*layer
    for j in range(nz):
        for i in range(nx):
            a = off+j*stride+i
            q = (a,a+1,a+stride+1,a+stride)
            faces.append(q if k==0 else tuple(reversed(q)))
edge = list(range(stride))+[j*stride+nx for j in range(1,nz+1)]+[nz*stride+i for i in range(nx-1,-1,-1)]+[j*stride for j in range(nz-1,0,-1)]
for i,a in enumerate(edge):
    b = edge[(i+1)%len(edge)]
    faces.append((a,b,b+layer,a+layer))
stroller.append(mesh_obj('STROLLER_FoldedCanopy',verts,faces,cloth,True))
seams = []
for u in [-.92,-.56,.56,.92]:
    pts = []
    for j in range(19):
        t = j/18
        half = .149+.025*math.sin(t*math.pi/2)
        pts.append((u*half,-.088+.012*math.cos(u*math.pi*3)+.008*math.sin(t*math.pi*4+u),.211+.425*t-.013*u*u*math.sin(math.pi*t)))
    seams.append(tube('_seam',pts,.0013,stitch))
stroller.append(joined('STROLLER_CanopySeams',seams))
stroller.append(box('STROLLER_FoldedBasket',(0,.071,.363),(.312,.038,.226),meshcloth,.018))
stroller.append(joined('STROLLER_BasketStraps',[tube('_strap',[(-.158,.076,.259),(-.17,.068,.437),(-.16,.042,.524)],.004,black),tube('_strap',[(.158,.076,.259),(.17,.068,.437),(.16,.042,.524)],.004,black)]))
stroller.append(joined('STROLLER_BumperBar',[tube('_bar',[(-.165,-.077,.435),(-.172,-.102,.499),(-.153,-.116,.558),(-.122,-.121,.581),(.122,-.121,.581),(.153,-.116,.558),(.172,-.102,.499),(.165,-.077,.435)],.012,black),cylinder('_grip',(-.117,-.121,.581),(.117,-.121,.581),.017,brown)]))
verts,faces = [],[]
N = 32
for rad,zz in [(.026,.310),(.037,.395),(.033,.395),(.023,.316)]:
    for i in range(N):
        a = 2*math.pi*i/N
        verts.append((.209+rad*math.cos(a),-.089+rad*math.sin(a),zz))
for ring in range(3):
    for i in range(N):
        k = ring*N+i
        kn = ring*N+(i+1)%N
        faces.append((k,kn,kn+N,k+N))
faces.append(tuple(reversed(range(N))))
faces.append(tuple(range(3*N,4*N)))
stroller.append(mesh_obj('STROLLER_CupHolder',verts,faces,black,True))

bpy.context.view_layer.update()
points = [o.matrix_world @ v.co for o in stroller for v in o.data.vertices]
low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
mid = (low+high)/2
factor = Vector((W/(high.x-low.x),D/(high.y-low.y),H/(high.z-low.z)))
rig = empty('STROLLER_RIG')
locked = empty('STROLLER_FoldLockedJoint',parent=rig)
for o in stroller:
    transform = o.matrix_world.copy()
    for v in o.data.vertices:
        p = transform @ v.co-mid
        v.co = (p.x*factor.x,p.y*factor.y,p.z*factor.z)
    o.matrix_world = Matrix.Identity(4)
    o.parent = locked
    o.matrix_parent_inverse = Matrix.Identity(4)
    o['rigid_part'] = True
rig['folded_envelope_mm'] = 'width 520.7; height 786.9; depth 292.1'
rig['final_world_envelope_mm'] = 'along X 520.7; lateral 786.9; vertical 292.1'


# Exact cargo colliders: unchanged geometry, locations and animation.
def extruded_polygon(name, poly, z0, z1, mat):
    n = len(poly)
    vs = [(x,y,z) for z in [z0,z1] for x,y in poly]
    fs = [tuple(reversed(range(n))),tuple(range(n,2*n))]
    for i in range(n):
        j = (i+1)%n
        fs.append((i,j,j+n,i+n))
    return mesh_obj(name,vs,fs,mat)

outline = [(0,-.570),(.220,-.4435),(1.060,-.4435),(1.060,.4435),(.220,.4435),(0,.570)]
floor = extruded_polygon('FIT_FLOOR',outline,-.055,0,proxy_mat)
seatback = box('FIT_SEATBACK',(1.090,0,.340),(.060,1.140,.680),proxy_mat)
ceiling = box('FIT_CEILING',(.530,0,.695),(1.060,1.140,.030),proxy_mat)

def side_collider(name,sign):
    vs = []
    for x,inner in [(0,.570),(.220,.4435),(1.060,.4435)]:
        cross = [(inner,0),(.690,0),(.690,.680),(.570,.680),(.570,.355),(inner,.255)]
        vs.extend((x,sign*y,z) for y,z in cross)
    fs = [tuple(reversed(range(6))),tuple(range(12,18))]
    for s in range(2):
        for i in range(6):
            j = (i+1)%6
            fs.append((s*6+i,s*6+j,(s+1)*6+j,(s+1)*6+i))
    if sign<0:
        fs = [tuple(reversed(f)) for f in fs]
    return mesh_obj(name,vs,fs,proxy_mat)

side_l = side_collider('FIT_SIDE_L',1)
side_r = side_collider('FIT_SIDE_R',-1)
hinge = empty('LIFTGATE_HINGE',(0,0,.760))
gate = box('FIT_LIFTGATE',(-.0275,0,-.380),(.055,1.250,.760),proxy_mat)
gate.parent = hinge
proxies = [floor,seatback,ceiling,side_l,side_r,gate]
for o in proxies:
    o.hide_render = True
    o.hide_set(True)
    o.display_type = 'WIRE'
    o['collision_proxy_only'] = True
floor['measured_depth_mm'] = 1060.0
ceiling['underside_height_mm'] = 680.0
seatback['inner_face_x'] = 1.060
gate['closed_inner_plane_x'] = 0.0
for o in [side_l,side_r]:
    o['illustrative_arch_width_mm'] = 887.0
    o['aperture_span_mm'] = 1140.0

# Cargo appearance, parcel shelf and shelf-removal motion are unchanged.
extruded_polygon('CAR_CargoCarpet',outline,-.054,0,carpet)
box('CAR_UprightSeatbacks',(1.110,0,.325),(.098,1.240,.650),seatmat,.018)
box('CAR_SeatbackSplit',(1.059,.105,.340),(.003,.006,.580),trim)
for sign,side in [(-1,'R'),(1,'L')]:
    box('CAR_Headrest_'+side,(1.155,sign*.355,.723),(.130,.235,.190),seatmat,.037)
    box('CAR_ArchTrim_'+side,(.640,sign*.562,.147),(.840,.237,.294),carpet,.040)
    box('CAR_CargoSideTrim_'+side,(.590,sign*.628,.401),(1.020,.108,.570),trim,.035)
    tube('CAR_TrimShoulder_'+side,[(.02,sign*.584,.33),(.24,sign*.58,.365),(.67,sign*.58,.37),(1.045,sign*.58,.39)],.013,trim)
box('CAR_LoadSill',(-.077,0,-.031),(.154,1.185,.050),trim,.012)
shelf_rig = empty('PARCEL_SHELF_RIG',(.580,0,.454))
poly = [(-.470,-.490),(-.430,-.554),(.420,-.554),(.470,-.500),(.470,.500),(.420,.554),(-.430,.554),(-.470,.490)]
shelf = extruded_polygon('CAR_ParcelShelf',poly,-.012,.012,carpet)
shelf.parent = shelf_rig
shelf_edge = tube('CAR_ParcelShelfEdge',[(x,y,.008) for x,y in poly]+[(poly[0][0],poly[0][1],.008)],.006,trim)
shelf_edge.parent = shelf_rig
for frame,loc in [(1,(.580,0,.454)),(33,(.580,0,.454)),(48,(.580,0,.563)),(66,(-1.10,0,.563)),(78,(-1.10,1.70,.563)),(88,(-1.10,1.70,GROUND+.012)),(352,(-1.10,1.70,GROUND+.012))]:
    shelf_rig.location = loc
    shelf_rig.keyframe_insert(data_path='location',frame=frame)
smooth_action(shelf_rig)

# Exterior-only repair. Capture the protected scene before building exterior parts.
protected_names = set(o.name for o in bpy.data.objects)
# Bring the rear axle closer to the tail; retain the 2.890 m wheelbase.
rear_axle,front_axle = .570,3.460
# Larger tyres, closely fitted arches and raised rocker edges establish crossover stance.
wheel_radius = .385
wheel_z = GROUND+wheel_radius
arch_radius = .408
width_stations = [(-.270,.690),(-.130,.850),(.180,.929),(.700,.954),(1.300,.960),(2.400,.960),(3.250,.945),(3.820,.910),(4.220,.861),(4.490,.755)]
belt_stations = [(-.270,.395),(-.130,.505),(.180,.615),(.700,.655),(1.300,.642),(2.400,.588),(3.250,.521),(3.820,.461),(4.220,.372),(4.490,.288)]
roof_height = [(.160,.658),(.300,.790),(.570,.984),(.900,1.047),(1.350,1.100),(1.800,1.113),(2.150,1.073),(2.400,1.006),(2.750,.815),(3.170,.565),(3.310,.530)]
roof_width = [(.160,.878),(.300,.754),(.570,.585),(.900,.641),(1.350,.687),(1.800,.707),(2.150,.728),(2.400,.749),(2.750,.794),(3.170,.850),(3.310,.868)]
P = exterior_profile
body = []


def upper_side_y(x,z):
    base = P(x,belt_stations)
    top = P(x,roof_height)
    low_y = P(x,width_stations)-.051
    high_y = P(x,roof_width)
    t = max(0.0,min(1.0,(z-base)/max(.001,top-base)))
    return low_y+(high_y-low_y)*t+.008*math.sin(math.pi*t)


def window_limits(x):
    base = P(x,belt_stations)+.022
    taper = min(1.0,max(0.0,(x-.285)/.230),max(0.0,(3.185-x)/.190))
    top = base+max(0.0,P(x,roof_height)-.038-base)*taper
    return base,top


for sign,side in [(-1,'R'),(1,'L')]:
    rows = []
    for i in range(221):
        x = -.270+4.760*i/220
        top = P(x,belt_stations)
        width = P(x,width_stations)
        bottom = -.350
        for axle in [rear_axle,front_axle]:
            dx = x-axle
            if abs(dx)<arch_radius:
                bottom = max(bottom,wheel_z+math.sqrt(arch_radius**2-dx**2))
        row = []
        for j in range(10):
            t = j/9
            yy = width-.051*t**3-.044*(1-t)**3+.010*math.sin(math.pi*t)
            row.append((x,sign*yy,bottom+(top-bottom)*t))
        rows.append(row)
    body.append(skin('_crossover_lower_'+side,rows,paint,(0,-sign*.018,0)))
    tube('CAR_Rocker_'+side,[(1.02,sign*.904,-.349),(1.96,sign*.913,-.354),(3.01,sign*.902,-.341)],.026,trim)
    rows = []
    for i in range(81):
        x = .160+3.150*i/80
        low_z,high_z = P(x,belt_stations),P(x,roof_height)
        rows.append([(x,sign*upper_side_y(x,low_z+(high_z-low_z)*j/8),low_z+(high_z-low_z)*j/8) for j in range(9)])
    body.append(skin('_crossover_shoulder_'+side,rows,paint,(0,-sign*.016,0)))
    rows = []
    for i in range(81):
        x = .285+2.900*i/80
        base,top = window_limits(x)
        rows.append([(x,sign*(upper_side_y(x,base+(top-base)*j/6)+.007),base+(top-base)*j/6) for j in range(7)])
    skin('CAR_SideGlazing_'+side,rows,glass,(0,-sign*.004,0))
    window_top,window_base = [],[]
    for i in range(65):
        x = .285+2.900*i/64
        base,top = window_limits(x)
        window_top.append((x,sign*(upper_side_y(x,top)+.011),top))
        window_base.append((x,sign*(upper_side_y(x,base)+.011),base))
    tube('CAR_WindowUpperTrim_'+side,window_top,.008,trim)
    tube('CAR_WindowLowerTrim_'+side,window_base,.007,trim)
    rail_pts = [(x,sign*P(x,roof_width),P(x,roof_height)) for x in [.570+i*(3.310-.570)/56 for i in range(57)]]
    body.append(tube('_roof_rail_'+side,rail_pts,.018,paint))
    x = 1.91
    base,top = window_limits(x)
    tube('CAR_B_Pillar_'+side,[(x,sign*(upper_side_y(x,z)+.014),z) for z in [base+(top-base)*i/8 for i in range(9)]],.025,trim)
    x = .925
    base,top = window_limits(x)
    tube('CAR_QuarterGlassSplit_'+side,[(x,sign*(upper_side_y(x,z)+.011),z) for z in [base+(top-base)*i/8 for i in range(9)]],.008,trim)
    for x0 in [1.46,2.92]:
        yy = P(x0,width_stations)
        tube('CAR_DoorSeam_'+side+'_'+str(x0),[(x0,sign*(yy-.041),-.310),(x0,sign*(yy+.003),.12),(x0-.024,sign*(yy-.018),.43),(x0-.040,sign*(yy-.047),P(x0,belt_stations)-.008)],.002,trim)
    for x0 in [1.33,2.66]:
        yy = P(x0,width_stations)-.025
        box('CAR_FlushHandle_'+side+'_'+str(x0),(x0,sign*yy,P(x0,belt_stations)-.090),(.142,.015,.019),trim,.005)
    box('CAR_Mirror_'+side,(3.015,sign*1.010,.616),(.208,.166,.100),paint,.043)
    tube('CAR_MirrorStem_'+side,[(3.025,sign*.856,.565),(3.015,sign*.980,.600)],.019,trim)
    for axle,label in [(rear_axle,'Rear'),(front_axle,'Front')]:
        pts = []
        for k in range(57):
            a = math.radians(-19+218*k/56)
            xx = axle+arch_radius*math.cos(a)
            pts.append((xx,sign*(P(xx,width_stations)-.028),wheel_z+arch_radius*math.sin(a)))
        tube('CAR_'+label+'WheelArch_'+side,pts,.010,trim)
        body.append(tube('_painted_arch_'+label+side,[(x,y-sign*.007,z+.010) for x,y,z in pts],.014,paint))
        torus('CAR_'+label+'Wheel_'+side,(axle,sign*.887,wheel_z),.322,.063,rubber,'Y')
        hub_scale = wheel_radius/.390
        pieces = [cylinder('_barrel',(axle,sign*.900,wheel_z),(axle,sign*.949,wheel_z),.279*hub_scale,rim,48),torus('_wheel_rim',(axle,sign*.952,wheel_z),.271*hub_scale,.008,aero,'Y')]
        for k in range(5):
            a = 2*math.pi*k/5+.18
            vs = []
            for rad,da in [(.041,-.32),(.256,-.15),(.265,.22),(.103,.43)]:
                r = rad*hub_scale
                vs.append((axle+r*math.cos(a+da),sign*.957,wheel_z+r*math.sin(a+da)))
            vs += [(x,y-sign*.014,z) for x,y,z in vs[:4]]
            pieces.append(mesh_obj('_aero_spoke',vs,[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],aero))
        pieces.append(cylinder('_center',(axle,sign*.952,wheel_z),(axle,sign*.963,wheel_z),.051*hub_scale,aero))
        joined('CAR_'+label+'Hub_'+side,pieces)
    wrap = [(-.226,.595,-.018,-.241,.806),(-.228,.626,.165,-.189,.879),(-.181,.643,.374,-.090,.915),(-.086,.642,.546,.090,.914),(.075,.622,.699,.290,.843),(.291,.590,.863,.455,.719),(.554,.574,.975,.638,.625)]
    rows = []
    for xi,yi,z,xo,yo in wrap:
        rows.append([(xi+(xo-xi)*j/8,sign*(yi+(yo-yi)*j/8),z+.012*math.sin(math.pi*j/8)) for j in range(9)])
    body.append(skin('_rear_quarter_wrap_'+side,rows,paint,(.014,-sign*.009,0)))
    opening = [(xi,sign*yi,z) for xi,yi,z,xo,yo in wrap]
    body.append(tube('_hatch_surround_'+side,opening,.020,paint))
    tube('CAR_HatchSeal_'+side,[(x+.012,y-sign*.017,z) for x,y,z in opening],.008,trim)
    path = [(-.166,sign*.647,.459),(-.120,sign*.748,.478),(-.034,sign*.840,.495),(.090,sign*.893,.514)]
    joined('CAR_Taillight_'+side,[tube('_lamp_housing',path,.021,trim),tube('_red_lens',[(x-.008,y,z+.002) for x,y,z in path],.007,red)])

rows = []
for i in range(49):
    x = .570+(2.420-.570)*i/48
    z,half = P(x,roof_height),P(x,roof_width)-.017
    rows.append([(x,half*u,z+.011*(1-u*u)) for u in [j/16 for j in range(-16,17)]])
skin('CAR_PanoramicRoof',rows,glass,(0,0,-.010))
rows = []
for i in range(33):
    x = 2.420+(3.310-2.420)*i/32
    z,half = P(x,roof_height),P(x,roof_width)-.017
    rows.append([(x,half*u,z+.017*(1-u*u)) for u in [j/16 for j in range(-16,17)]])
skin('CAR_Windshield',rows,glass,(0,0,-.010))
body.append(tube('_rear_roof_header',[(.570,-.572,.979),(.570,-.330,.991),(.570,0,.995),(.570,.330,.991),(.570,.572,.979)],.018,paint))
rows = []
hood_stations = [(3.305,.530),(3.580,.502),(3.950,.435),(4.270,.356),(4.490,.294)]
for i in range(41):
    x = 3.305+1.185*i/40
    z = P(x,hood_stations)
    half = P(x,width_stations)-.035
    rows.append([(x,half*u,z+.024*(1-u*u)) for u in [j/16 for j in range(-16,17)]])
body.append(skin('_hood',rows,paint,(0,0,-.020)))
for rear in [True,False]:
    rows = []
    if rear:
        specs = [(-.018,.803,-.262),(-.110,.858,-.294),(-.220,.838,-.278),(-.292,.778,-.207)]
    else:
        specs = [(.295,.757,4.481),(.163,.796,4.505),(-.065,.806,4.470),(-.303,.755,4.340)]
    for z,half,xx in specs:
        rows.append([(xx+(.160 if rear else -.160)*abs(u)**4,half*u,z+.012*u*u) for u in [j/16 for j in range(-16,17)]])
    body.append(skin('_rear_bumper' if rear else '_front_bumper',rows,paint,((.024 if rear else -.024),0,0)))
    z = -.276 if rear else -.292
    xx = -.217 if rear else 4.360
    tube('CAR_RearValance' if rear else 'CAR_FrontValance',[(xx+(.13 if rear else -.13)*u*u,.750*u,z+.017*u*u) for u in [j/16 for j in range(-16,17)]],.025,trim)
for sign,side in [(-1,'R'),(1,'L')]:
    path = [(4.477,sign*.27,.303),(4.454,sign*.55,.312),(4.354,sign*.751,.336),(4.208,sign*.835,.371)]
    joined('CAR_Headlamp_'+side,[tube('_headlamp_surround',path,.016,trim),tube('_headlamp_lens',[(x+.003,y,z+.003) for x,y,z in path],.006,headlamp)])
box('CAR_Underbody',(2.730,0,-.354),(3.340,1.560,.034),trim,.015)
joined('CAR_FullBody',body)

# The hatch is constructed closed, then rebuilt coherently with the roof below.
VIS_HINGE_X,VIS_HINGE_Z = .570,.984
visual_hinge = empty('CAR_ExteriorLiftgateJoint',(VIS_HINGE_X,0,VIS_HINGE_Z))

def hatch_local(points):
    return [(x-VIS_HINGE_X,y,z-VIS_HINGE_Z) for x,y,z in points]

parts = []
rows = []
for x,z,half in [(-.245,.028,.580),(-.261,.115,.617),(-.246,.272,.640),(-.185,.411,.636),(-.142,.472,.616)]:
    rows.append(hatch_local([(x+.017*u*u,half*u,z+.006*u*u) for u in [i/16 for i in range(-16,17)]]))
parts.append(skin('_hatch_lower_panel',rows,hatch_paint,(-.012,0,0)))
rows = []
for x,z,half in [(-.184,.415,.634),(-.154,.451,.625),(-.132,.478,.614)]:
    rows.append(hatch_local([(x+.018*u*u,half*u,z+.004*u*u) for u in [i/16 for i in range(-16,17)]]))
parts.append(skin('_hatch_belt',rows,hatch_paint,(-.013,0,0)))
rows = []
for x,z in [(.510,.950),(.548,.974),(.566,.980)]:
    rows.append(hatch_local([(x+.006*u*u,.562*u,z-.010*u*u) for u in [i/12 for i in range(-12,13)]]))
parts.append(skin('_hatch_top_edge',rows,paint,(0,0,-.010)))
shell = joined('CAR_LiftgateShell',parts)
shell.parent = visual_hinge
outline_gate = [(-.245,-.580,.028),(-.251,-.622,.165),(-.202,-.645,.368),(-.130,-.624,.478),(.090,-.609,.700),(.302,-.587,.857),(.553,-.562,.965),(.558,0,.981),(.553,.562,.965),(.302,.587,.857),(.090,.609,.700),(-.130,.624,.478),(-.202,.645,.368),(-.251,.622,.165),(-.245,.580,.028),(-.245,0,.024),(-.245,-.580,.028)]
edge_gate = tube('CAR_LiftgatePerimeter',hatch_local(outline_gate),.020,paint)
edge_gate.parent = visual_hinge
rows = []
rear_glass_x = [(.490,-.119),(.630,.026),(.790,.210),(.906,.410),(.958,.541)]
rear_glass_width = [(.490,.600),(.630,.596),(.790,.579),(.906,.558),(.958,.541)]
for j in range(33):
    z = .490+.468*j/32
    x = P(z,rear_glass_x)
    half = P(z,rear_glass_width)
    rows.append(hatch_local([(x-.010*(1-u*u),half*u,z+.006*(1-u*u)) for u in [i/16 for i in range(-16,17)]]))
rear_glass = skin('CAR_RearGlass',rows,hatch_glass,(-.006,0,0))
rear_glass.parent = visual_hinge
lining = box('CAR_LiftgateInnerTrim',(-.217-VIS_HINGE_X,0,.225-VIS_HINGE_Z),(.020,1.050,.330),hatch_trim,.025)
lining.parent = visual_hinge
light_points = hatch_local([(-.160+.017*u*u,.622*u,.450+.006*u*u) for u in [i/24 for i in range(-24,25)]])
bar = joined('CAR_LiftgateLightBar',[tube('_lamp_base',light_points,.017,trim),tube('_red_band',[(x-.010,y,z+.002) for x,y,z in light_points],.0065,red)])
bar.parent = visual_hinge

# Bake the supported silhouette correction into exterior vertices only.
# This is construction-time shaping, NOT animated deformation or a saved driver.
# Moving the upper rear roof/header forward shortens the horizontal roof and
# creates the reference's descending fastback line into the sloped hatch.
def smoothstep(a,b,value):
    t = max(0.0,min(1.0,(value-a)/(b-a)))
    return t*t*(3-2*t)


def crossover_shape(p):
    x,y,z = p
    upper = smoothstep(.35,.85,z)
    # Advance windshield/cabin toward the front, tapering to zero at the nose.
    front = smoothstep(1.9,3.15,x)*(1-smoothstep(3.3,4.5,x))
    dx = .32*front*upper
    # Fill the high crossover shoulder beneath side glazing without lifting roof.
    shoulder = smoothstep(.0,.48,z)*(1-smoothstep(.60,1.1,z))
    dz = .095*shoulder
    return Vector((x+dx,y,z+dz))

bpy.context.view_layer.update()
exterior_objects = [o for o in bpy.data.objects if o.name not in protected_names and o.type=='MESH']
exterior_vertices = []
for o in exterior_objects:
    exterior_vertices.append((o,[crossover_shape(o.matrix_world @ v.co) for v in o.data.vertices]))
visual_hinge.location = crossover_shape(Vector((VIS_HINGE_X,0,VIS_HINGE_Z)))
bpy.context.view_layer.update()
for o,vertices in exterior_vertices:
    inv = o.matrix_world.inverted()
    for v,p in zip(o.data.vertices,vertices):
        v.co = inv @ p
    o.data.update()
    o['exterior_only_repair'] = True
assert all(o.name not in protected_names for o in exterior_objects)
assert not any(o in exterior_objects for o in proxies+stroller)

# Preserve the stroller's lift, turn, slide and rest animation exactly.
rig.rotation_mode = 'XYZ'
poses = [(1,(-1.075,0,GROUND+H/2),0),(88,(-1.075,0,GROUND+H/2),0),(126,(-1.075,0,.470),0),(164,(-1.075,0,.470),90),(178,(-1.075,0,.470),90),(232,(REST_X,0,.470),90),(260,(REST_X,0,D/2),90),(352,(REST_X,0,D/2),90)]
for frame,loc,angle in poses:
    rig.location = loc
    rig.rotation_euler = (math.radians(angle),0,0)
    rig.keyframe_insert(data_path='location',frame=frame)
    rig.keyframe_insert(data_path='rotation_euler',frame=frame)
# Exact original collision-proxy animation.
hinge.rotation_mode = 'XYZ'
for frame,angle in [(1,103),(278,103),(326,0),(352,0)]:
    hinge.rotation_euler = (0,math.radians(angle),0)
    hinge.keyframe_insert(data_path='rotation_euler',frame=frame)
# The more raked exterior hatch needs less angular travel to reach its raised pose.
# Timing and fully closed pose are retained; this never transforms a cargo proxy.
visual_hinge.rotation_mode = 'XYZ'
for frame,angle in [(1,57),(278,57),(326,0),(352,0)]:
    visual_hinge.rotation_euler = (0,math.radians(angle),0)
    visual_hinge.keyframe_insert(data_path='rotation_euler',frame=frame)
smooth_action(rig)
smooth_action(hinge)
smooth_action(visual_hinge)
for m in [hatch_paint,hatch_glass,hatch_trim]:
    for fc in action_curves(m.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = 'CONSTANT'

# Retained studio, lighting and camera.
box('STUDIO_Ground',(0,0,GROUND-.035),(80,80,.070),stage)
world = bpy.data.worlds.new('Studio world')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (.72,.79,.86,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = .55
scene.world = world


def area(name,loc,energy,size,target):
    data = bpy.data.lights.new(name,'AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    ob = bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    return ob

area('Key_softbox',(-3,-4,6),1500,5,(.6,0,.2))
area('Fill_softbox',(-2,4,3.8),1050,4,(.3,0,.2))
area('Roof_softbox',(4,1,5),1800,5,(2,0,.2))
area('Cargo_fill',(-3,0,2.6),160,2,(.65,0,.25))
area('Cargo_detail_softbox',(.18,-.08,.650),8,.48,(.80,0,.12))
camdata = bpy.data.cameras.new('Camera_Main')
cam = bpy.data.objects.new('Camera_Main',camdata)
bpy.context.collection.objects.link(cam)
camdata.type = 'PERSP'
camdata.lens = 50
camdata.sensor_width = 36
camdata.sensor_fit = 'HORIZONTAL'
camdata.clip_start = .025
camdata.clip_end = 150
cam.rotation_mode = 'QUATERNION'
scene.camera = cam
camera_poses = [(1,(-6.8,-.14,1.65),(-.05,0,-.10)),(126,(-6.8,-.14,1.65),(-.05,0,-.10)),(164,(-4.75,-.06,1.65),(.17,0,.23)),(352,(-4.75,-.06,1.65),(.17,0,.23))]
for frame,loc,target in camera_poses:
    cam.location = loc
    cam.rotation_quaternion = (Vector(target)-cam.location).to_track_quat('-Z','Y')
    cam.keyframe_insert(data_path='location',frame=frame)
    cam.keyframe_insert(data_path='rotation_quaternion',frame=frame)
smooth_action(cam)

# Retained opaque, camera-facing callouts.
def panel(name,x,y,w,h):
    o = box(name,(0,0,0),(w,h,.001),nearblack)
    o.parent = cam
    o.location = (x,y,-1.006)
    o.visible_shadow = False
    return o


def hud_text(name,body,x,y,size=.0205):
    cu = bpy.data.curves.new(name+'_Font','FONT')
    cu.body = body
    cu.size = size
    cu.align_x = 'LEFT'
    cu.space_line = 1.10
    o = bpy.data.objects.new(name,cu)
    bpy.context.collection.objects.link(o)
    assign(o,white)
    o.parent = cam
    o.location = (x,y,-1.000)
    o.visible_shadow = False
    return o


def visibility_interval(objects,start,end):
    for o in objects:
        for frame,hidden in [(1,True),(start,False),(end,False),(end+1,True)]:
            o.hide_render = hidden
            o.keyframe_insert(data_path='hide_render',frame=frame)
        for fc in action_curves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'

panel('HUD_Header',0,.174,.750,.060)
hud_text('HUD_Title','Graco Ready2Jet / Tesla Model Y',-.343,.179,.022)
hud_text('HUD_Verdict','LIKELY FITS - NOT CONFIRMED',-.343,.152,.0205)
panel('HUD_Footer',0,-.166,.750,.080)
hud_text('HUD_Unverified','Arch width unverified: 34.9 in (88.7 cm) illustrated.',-.343,-.171,.0180)
hud_text('HUD_Limitation','Calculated placement only; not proof of fit.',-.343,-.196,.0200)
caption_specs = [(1,32,'1  Folded: 31 x 20.5 x 11.5 in (78.7 x 52.1 x 29.2 cm)'),(33,48,'2  Hatch fully open. Lift the removable cargo cover.'),(49,88,'2  Remove the cover and set it aside before loading.'),(89,126,'3  Lift the folded stroller clear of the load floor.'),(127,178,'3  Lay flat, with its 31 in (78.7 cm) side across.'),(179,232,'3  Slide inward above the flush load lip.'),(233,278,'3  Lower to floor; leave 1 in (2.5 cm) at seatbacks.'),(279,326,'4  Close hatch. CUTAWAY: outer panels hidden.'),(327,352,'4  Closed cutaway: 11.5 in (29.2 cm) stroller height.')]
for i,(start,end,body_text) in enumerate(caption_specs):
    o = hud_text('HUD_Step_%02d'%i,body_text,-.343,-.143,.0180)
    visibility_interval([o],start,end)
scene.frame_set(260)
bpy.context.view_layer.update()


def project(p):
    v = cam.matrix_world.inverted() @ Vector(p)
    return (v.x/-v.z,v.y/-v.z)


def hud_line(name,xy,radius=.00065):
    objects = []
    for suffix,r,z,mat in [('_outline',radius*2.2,-1.000,nearblack),('_white',radius,-.997,white)]:
        o = tube(name+suffix,[(x,y,z) for x,y in xy],r,mat,False)
        o.parent = cam
        o.visible_shadow = False
        objects.append(o)
    return objects


def dimension_callout(name,line1,line2,cx,cy,a,b,toward,start=179,anchor='mid'):
    objects = [panel(name+'_Panel',cx,cy,.200,.086)]
    objects.append(hud_text(name+'_Value',line1.split('|')[0],cx-.093,cy+.022,.0220))
    objects.append(hud_text(name+'_Metric',line1.split('|')[1],cx-.093,cy-.002,.0170))
    objects.append(hud_text(name+'_Meaning',line2,cx-.093,cy-.027,.0180))
    pa,pb = project(a),project(b)
    objects += hud_line(name+'_Dimension',[pa,pb])
    dx,dy = pb[0]-pa[0],pb[1]-pa[1]
    length = max(math.sqrt(dx*dx+dy*dy),1e-8)
    tx,ty = -dy/length*.0035,dx/length*.0035
    for label,p in [('A',pa),('B',pb)]:
        objects += hud_line(name+'_Tick'+label,[(p[0]-tx,p[1]-ty),(p[0]+tx,p[1]+ty)])
    if anchor=='left':
        target = min([pa,pb],key=lambda p:p[0])
    else:
        target = ((pa[0]+pb[0])/2,(pa[1]+pb[1])/2)
    edge = (cx+(.100 if toward>0 else -.100),cy)
    objects += hud_line(name+'_Leader',[edge,(edge[0]+toward*.009,cy),target])
    visibility_interval(objects,start,352)


dimension_callout('HUD_Depth','41.7 in|(106 cm)','floor depth',-.246,.070,(0,.520,.006),(1.060,.520,.006),1)
dimension_callout('HUD_Opening','44.9 in|(114 cm)','opening',-.246,-.029,(-.010,-.570,.018),(-.010,.570,.018),1,anchor='left')
dimension_callout('HUD_Height','26.8 in|(68 cm)','height limit',.246,.070,(.030,-.592,0),(.030,-.592,.680),-1)
dimension_callout('HUD_StrollerHeight','11.5 in|(29.2 cm)','stroller height',.246,-.029,(REST_X,-.407,0),(REST_X,-.407,D),-1,start=260)

# Construction-time checks only; no handlers or executable text blocks.
scene.frame_set(352)
bpy.context.view_layer.update()
points = [o.matrix_world @ v.co for o in stroller for v in o.data.vertices]
lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
expected = Vector((W,H,D))
assert all(abs((hi-lo)[i]-expected[i])<1e-6 for i in range(3)), 'Folded envelope mismatch'
assert abs(lo.z)<1e-6, 'Stroller must rest on the cargo floor'
assert abs(DEPTH-hi.x-.025)<1e-6, 'Seatback clearance mismatch'
assert lo.x>=.025
assert lo.y>=-ARCH/2+.025-1e-6 and hi.y<=ARCH/2-.025+1e-6
assert hi.z<=HEIGHT-.025
assert abs(hinge.rotation_euler.y)<1e-6
assert abs(visual_hinge.rotation_euler.y)<1e-6
assert all(o.hide_render for o in proxies)
assert abs(front_axle-rear_axle-2.890)<1e-9
assert abs(wheel_z-wheel_radius-GROUND)<1e-9
for o in stroller:
    assert o.name.startswith('STROLLER_')
    assert all(abs(s-1)<1e-6 for s in o.scale)
for m in [hatch_paint,hatch_glass,hatch_trim]:
    mix = next(n for n in m.node_tree.nodes if n.bl_idname=='ShaderNodeMixShader')
    assert abs(mix.inputs[0].default_value)<1e-8, 'Inspection skin must be fully clear'
# Verify the protected measurement boundaries independently of the new exterior.
floor_points = [floor.matrix_world @ v.co for v in floor.data.vertices]
ceiling_points = [ceiling.matrix_world @ v.co for v in ceiling.data.vertices]
assert abs(min(p.x for p in floor_points))<1e-7
assert abs(max(p.x for p in floor_points)-1.060)<1e-6
assert abs(max(p.z for p in floor_points))<1e-7
assert abs(min(p.z for p in ceiling_points)-.680)<1e-6
assert abs(seatback.location.x-seatback.dimensions.x/2-1.060)<1e-6
scene['fit_verdict'] = 'LIKELY_FITS_UNCONFIRMED'
scene['fit_frame'] = '+X from load lip to rear seatbacks; +Z up; floor top Z=0; lip inner edge X=0'
scene['clearance_note'] = 'Floor contact intentional. Seatback gap 25 mm; illustrated side gaps 50.05 mm; height gap 387.9 mm.'
scene['dimension_authority'] = 'Authoritative brief.fit: final envelope 520.7 x 786.9 x 292.1 mm. This takes precedence over the conflicting 30-inch quotation.'
scene['scope'] = 'Rear trunk, second row upright. Cargo measurements concern a refreshed 2025+ Model Y; verify the individual vehicle.'
scene['visual_disclosure'] = '887 mm between arches is illustrative, not verified. Calculated placement is not proof of fit. Exterior proportions and 600 mm load-floor ground height are illustrative. Closure inspection optically removes hatch skins; this is not transparent production bodywork.'
scene['collision_proxy_names'] = ','.join(o.name for o in proxies)
scene['repair_summary'] = 'Exterior silhouette only: larger tyres with close-fitting arches, raised rocker and bumper undersides, higher shoulder and cabin crown, shortened rear overhang by moving both axles rearward while retaining 2.890 m wheelbase, and a shortened roof transitioning into a more sloped hatch. Exterior hatch hinge and raised angle follow that geometry. Cargo meshes, every FIT collider and its animation, stroller geometry and placement, red paint, materials, lighting, cameras, shelf removal, labels and timing are retained.'
scene.frame_set(1)
bpy.context.view_layer.update()
