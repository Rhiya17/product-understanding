"""Fresh, editable Ready2Jet reference reconstruction. No historical geometry imports.
Run with installed bpy Python or Blender --background --python ... -- <arguments>.
"""
import sys, math, json, time, argparse, platform
from pathlib import Path
import bpy
from mathutils import Vector
RUN=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).parent))
from geometry import build, studio
from rig import pose, bake
p=argparse.ArgumentParser()
p.add_argument('mode',choices=['smoke','build','render','reproduce'])
p.add_argument('--revision',type=int,default=0)
p.add_argument('--directory',default='early')
p.add_argument('--camera',default='Camera_Reference')
p.add_argument('--frames',default='1,73,109,145,169')
p.add_argument('--size',type=int,default=640)
p.add_argument('--samples',type=int,default=16)
p.add_argument('--clay',action='store_true')
p.add_argument('--blend',default='final/ready2jet.blend')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
dest=RUN/args.directory;dest.mkdir(parents=True,exist_ok=True)
start=time.time()
def render(frame,name):
 s=bpy.context.scene;s.frame_set(frame);s.render.filepath=str(dest/name)
 t=time.time();bpy.ops.render.render(write_still=True);return time.time()-t
if args.mode=='smoke':
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.mesh.primitive_uv_sphere_add(radius=.3,location=(0,0,.31))
 bpy.context.object.name='SMOKE_EDITABLE_MESH'
 studio();s=bpy.context.scene;s.camera=bpy.data.objects['Camera_Reference'];s.render.resolution_x=384;s.render.resolution_y=384;s.cycles.samples=8
 file=RUN/'smoke/smoke.blend';bpy.ops.wm.save_as_mainfile(filepath=str(file));bpy.ops.wm.open_mainfile(filepath=str(file))
 dest=RUN/'smoke';s=bpy.context.scene;secs=render(1,'smoke.png')
 (dest/'runtime.json').write_text(json.dumps(dict(blender=bpy.app.version_string,python=sys.version,platform=platform.platform(),engine=s.render.engine,device=s.cycles.device,render_seconds=secs,save_reopen_render=True),indent=2))
elif args.mode=='build':
 build(args.revision);studio();bake()
 s=bpy.context.scene;s['revision']=args.revision;s['identity']='Kingston-reference reconstruction; exact SKU applicability unresolved';s['rights']='INTERNAL RESEARCH; source manufacturer rights restrictions retained';s['axes']='meters: X forward, Y left, Z up'
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(dest/'ready2jet.blend'))
else:
 bpy.ops.wm.open_mainfile(filepath=str(RUN/args.blend))
 s=bpy.context.scene
 s.camera=bpy.data.objects[args.camera]
 s.render.resolution_x=args.size;s.render.resolution_y=args.size;s.cycles.samples=args.samples
 if args.clay:
  mat=bpy.data.materials.new('Clay_override');mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.25,.29,.32,1);mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8;s.view_layers[0].material_override=mat
 frames=list(range(*[int(v) for v in args.frames.split(':')])) if ':' in args.frames else [int(v) for v in args.frames.split(',')]
 timings=[];measure=[]
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update()
  if args.mode=='reproduce':
   dg=bpy.context.evaluated_depsgraph_get();verts=[];partbounds=[]
   for o in s.objects:
    if o.get('part_id') and o.type in {'MESH','CURVE','FONT'}:
     ev=o.evaluated_get(dg);me=ev.to_mesh();pv=[ev.matrix_world@v.co for v in me.vertices];verts.extend(pv);ev.to_mesh_clear()
     if pv:partbounds.append(dict(part=o.name,min=[min(v[i] for v in pv) for i in range(3)],max=[max(v[i] for v in pv) for i in range(3)]))
   lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)]
   measure.append(dict(frame=f,min_xyz=lo,max_xyz=hi,dimensions_DWH=[hi[i]-lo[i] for i in range(3)],extremal_min_parts=[min(partbounds,key=lambda p:p['min'][i])['part'] for i in range(3)],extremal_max_parts=[max(partbounds,key=lambda p:p['max'][i])['part'] for i in range(3)]))
  timings.append(dict(frame=f,seconds=render(f,f'{args.camera}-{f:04d}.png')))
 (dest/f'{args.camera}-timing.json').write_text(json.dumps(timings,indent=2))
 if measure:(dest/'dimensions.json').write_text(json.dumps(measure,indent=2))
print(json.dumps({'mode':args.mode,'elapsed_seconds':time.time()-start,'output':str(dest)}),flush=True)
