"""Text-directed persistent set POC. Run with Blender Python (bpy)."""
import bpy
import math
import json
import hashlib
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, color, metallic=0, roughness=.5):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    return m

ivory = material('Shell • warm ceramic', (.88,.86,.75), roughness=.3)
sand = material('Podium • sandstone', (.48,.32,.18))
water = material('Harbour • blue', (.018,.13,.19), .5,.22)
glass = material('Facade • dark glazing', (.025,.10,.13), .6,.18)
wood = material('Interior • timber', (.27,.10,.035))
red = material('Seats • rust upholstery', (.44,.045,.025))
white = material('Ferry • white', (.9,.92,.88))

def cube(name, loc, scale, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object
    o.name=name
    o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=3
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

cube('Harbour', (0,0,-.7), (700,700,1), water)
cube('Plaza', (0,0,.1), (105,135,1.6), sand, 1)
cube('Podium', (0,6,2), (70,94,3), sand,.5)
for i in range(12):
    cube(f'Plaza.Step.{i:02}',(0,-54+i*.9,.9+i*.18),(62,1.1,.3),sand)

# Deliberately stylized paired pointed vaults, not a surveyed shell reconstruction.
def shell(name, cx, cy, width, length, height):
    verts=[]; faces=[]; nu=32; nv=32
    for i in range(nu+1):
        u=i/nu
        breadth=width*(math.sin(math.pi*u/2)**.8)
        ridge=height*u**.8
        for j in range(nv+1):
            v=-1+2*j/nv
            verts.append((cx+breadth*v,cy+length*(u-.5),4+ridge*(1-abs(v))**.7))
    for i in range(nu):
        for j in range(nv):
            a=i*(nv+1)+j
            faces.append((a,a+1,a+nv+2,a+nv+1))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o)
    o.data.materials.append(ivory)
    for p in mesh.polygons:p.use_smooth=True
    mod=o.modifiers.new('Shell thickness','SOLIDIFY'); mod.thickness=.22
    return o

for side,x in [('West',-17),('East',17)]:
    for i,(y,l,h,w) in enumerate([(-20,31,19,13),(1,39,29,15),(27,39,35,16)]):
        shell(f'Sail.{side}.{i+1:02}',x,y,w,l,h*(1 if side=='West' else .82))
    for end_y in [-28,46]:
        cube(f'Facade.{side}.{end_y}',(x,end_y,6),(22,.3,5),glass)
shell('Sail.Restaurant',-37,-30,9,23,12)

# A fictional interior inside the east hall, accessible by a saved camera.
cube('Interior.Floor',(17,29,4.1),(20,32,.3),wood)
cube('Interior.Wall.Left',(6.8,29,7.4),(.35,32,6.5),wood)
cube('Interior.Wall.Right',(27.2,29,7.4),(.35,32,6.5),wood)
cube('Interior.Stage',(17,41,4.6),(17,6,1),wood,.1)
for row in range(8):
    for col in range(12):
        x=8.6+col*1.5+(1 if col>=6 else 0); y=20+row*2.2
        cube(f'Seat.{row+1:02}.{col+1:02}.Cushion',(x,y,4.9),(1.05,1.05,.25),red,.1)
        cube(f'Seat.{row+1:02}.{col+1:02}.Back',(x,y-.48,5.4),(1.05,.2,1.15),red,.1)

ferry=cube('Ferry.Hull',(-75,-25,.7),(7,19,2),white,1)
cube('Ferry.Cabin',(-75,-25,2.3),(5.5,12,1.5),glass,.5)
cube('Ferry.Roof',(-75,-25,3.3),(6,13,.4),white,.2)

def camera(name, loc, target, lens=45):
    d=bpy.data.cameras.new(name); o=bpy.data.objects.new(name,d)
    bpy.context.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d.lens=lens; d.clip_end=2000
    return o

cameras=[camera('Camera.Harbour',(-155,-185,102),(0,5,10)),
         camera('Camera.Plaza',(115,-130,62),(0,8,12)),
         camera('Camera.Interior',(17,16,8),(17,40,6.5),21)]
ld=bpy.data.lights.new('Sun','SUN'); sun=bpy.data.objects.new('Sun',ld)
bpy.context.collection.objects.link(sun); sun.rotation_euler=(.5,-.6,-.5); ld.energy=3
ld.angle=.12
ld2=bpy.data.lights.new('Interior.Softbox','AREA'); li=bpy.data.objects.new('Interior.Softbox',ld2)
bpy.context.collection.objects.link(li); li.location=(17,30,12); ld2.energy=2200; ld2.shape='DISK'; ld2.size=15
scene=bpy.context.scene
scene.world.color=(.25,.25,.25)
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=16
scene.cycles.use_denoising=True
scene.render.resolution_x=960; scene.render.resolution_y=640; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'

def geometry_hash():
    data=[]
    for o in sorted(scene.objects,key=lambda o:o.name):
        if o.type=='MESH':
            data.append((o.name,[list(v.co) for v in o.data.vertices],
                         [list(p.vertices) for p in o.data.polygons],list(o.location),list(o.rotation_euler),list(o.scale)))
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()

baseline=geometry_hash(); results=[]
for name,cam in zip(['01-harbour-day','02-plaza-day','03-interior-day'],cameras):
    scene.camera=cam; scene.render.filepath=str(OUT/f'{name}.png')
    bpy.ops.render.render(write_still=True)
    results.append({'render':name,'geometry_sha256':geometry_hash(),'unchanged':geometry_hash()==baseline})
scene.camera=cameras[0]; sun.rotation_euler=(1.4,-.4,-1.3); sun.data.color=(1,.48,.2); sun.data.energy=2
scene.render.filepath=str(OUT/'04-harbour-sunset.png'); bpy.ops.render.render(write_still=True)
results.append({'render':'04-harbour-sunset','geometry_sha256':geometry_hash(),'unchanged':geometry_hash()==baseline})
sun.rotation_euler=(.5,-.6,-.5); sun.data.color=(1,1,1); sun.data.energy=3
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'opera-inspired-set.blend'))
# Prove a named object can be changed without modifying the rest of the set.
wall=bpy.data.objects['Interior.Wall.Right']; initial=wall.location.x
wall.location.x+=2
edit_changes_hash=geometry_hash()!=baseline
wall.location.x=initial
report={'blender':bpy.app.version_string,'renderer':'Cycles CPU','samples':16,
        'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'renders':results,
        'named_wall_edit_changes_geometry':edit_changes_hash,'restored_hash_matches':geometry_hash()==baseline,
        'scope':'Stylized invented set; not an accurate Sydney Opera House reconstruction.',
        'objects':[o.name for o in scene.objects]}
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
assert all(r['unchanged'] for r in results) and edit_changes_hash and geometry_hash()==baseline
print('POC PASSED',OUT,flush=True)
