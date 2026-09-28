"""Reproducible build / render / measure entry point. All outputs constrained to this run."""
import sys,json,time,platform,argparse
from pathlib import Path
import bpy
from mathutils import Vector
RUN=Path(__file__).resolve().parents[1];sys.path.insert(0,str(RUN/'scripts'))
import realism
p=argparse.ArgumentParser();p.add_argument('mode',choices=['build','render','reproduce']);p.add_argument('--round',type=int,default=2);p.add_argument('--directory',required=True);p.add_argument('--blend',default='final/ready2jet.blend');p.add_argument('--camera',default='Camera_Photo');p.add_argument('--frames',default='1,95,145');p.add_argument('--size',type=int,default=640);p.add_argument('--width',type=int,default=0);p.add_argument('--samples',type=int,default=24);p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]);dest=(RUN/a.directory).resolve();assert dest.is_relative_to(RUN);dest.mkdir(parents=True,exist_ok=True);bpy.context.preferences.filepaths.save_version=0;t0=time.time()
if a.mode=='build':
 realism.build(a.round);s=bpy.context.scene;s.render.filepath=str(dest/'render.png');bpy.ops.wm.save_as_mainfile(filepath=str(dest/'ready2jet.blend'),compress=True)
else:
 source=(RUN/a.blend).resolve();assert source.is_relative_to(RUN);bpy.ops.wm.open_mainfile(filepath=str(source));realism.cameras();s=bpy.context.scene;s.camera=bpy.data.objects[a.camera]
 s.render.resolution_x=a.width or a.size;s.render.resolution_y=a.size;s.render.resolution_percentage=100;s.cycles.samples=a.samples;s.cycles.seed=0;s.render.image_settings.file_format='PNG';s.cycles.use_denoising=True
 if a.width:
  # Keep vertical ortho framing constant across landscape media.
  if s.camera.data.type=='ORTHO':s.camera.data.ortho_scale=1.35*a.width/a.size
 if a.clay:
  m=bpy.data.materials.new('Neutral geometry override');m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(.30,.32,.34,1);b.inputs['Roughness'].default_value=.8;s.view_layers[0].material_override=m
 frames=list(range(*map(int,a.frames.split(':')))) if ':' in a.frames else list(map(int,a.frames.split(',')));times=[];measures=[]
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update()
  if a.mode=='reproduce':
   dg=bpy.context.evaluated_depsgraph_get();vs=[]
   for o in s.objects:
    if o.get('part_id') and o.type in ['MESH','CURVE']:
     ev=o.evaluated_get(dg);me=ev.to_mesh();vs.extend([ev.matrix_world@v.co for v in me.vertices]);ev.to_mesh_clear()
   lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)];measures.append({'frame':f,'min_xyz':lo,'max_xyz':hi,'dimensions_DWH':[hi[i]-lo[i] for i in range(3)]})
  s.render.filepath=str(dest/f'{a.camera}-{f:04d}.png');t=time.time();bpy.ops.render.render(write_still=True);times.append({'frame':f,'seconds':time.time()-t})
 (dest/(a.camera+'-timing.json')).write_text(json.dumps(times,indent=2))
 if measures:(dest/'dimensions.json').write_text(json.dumps(measures,indent=2))
record={'mode':a.mode,'seconds':time.time()-t0,'blender':bpy.app.version_string,'python':sys.version,'platform':platform.platform(),'engine':s.render.engine,'device':s.cycles.device,'render_size':[s.render.resolution_x,s.render.resolution_y],'samples':s.cycles.samples,'color_management':{'transform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure},'external_images':[i.filepath for i in bpy.data.images if i.source=='FILE']}
(dest/f'runtime-{a.mode}-{a.camera}.json').write_text(json.dumps(record,indent=2));print(json.dumps(record),flush=True)
