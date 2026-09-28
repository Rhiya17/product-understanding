"""Small scene inventory, camera settings, scale/readout and rest-UV observations."""
import bpy,json,sys
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
RUN=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(RUN/'final/ready2jet.blend'));s=bpy.context.scene;s.frame_set(1)
rigs=[o for o in s.objects if o.name.startswith('RIG_')];scales={o.name:list(o.scale) for o in rigs};checks=[]
for f in [1,19,49,61,73,79,89,95,100,105,110,116,137,145,193]:
 s.frame_set(f);checks.append({'frame':f,'all_rig_scales_unchanged':all(list(o.scale)==scales[o.name] for o in rigs),'rig_visibility_unchanged':all(not o.hide_render for o in rigs)})
s.frame_set(1);camera=bpy.data.objects['Camera_Photo']
landmarks={
 'front_wheel_R':(.28,-.205,.068),'front_wheel_L':(.28,.205,.068),'rear_wheel_R':(-.22,-.238,.074),'rear_wheel_L':(-.22,.238,.074),
 'main_hub_L':(.035,.211,.49),'handle_corner_L':(-.304,.17,1.065),'handle_corner_R':(-.304,-.17,1.065)}
projected={}
for k,v in landmarks.items():
 q=world_to_camera_view(s,camera,Vector(v));projected[k]={'world_xyz':v,'photo_normalized_uv_top_left':[q.x,1-q.y]}
cameras=[{'name':o.name,'type':o.data.type,'location':list(o.location),'rotation_euler':list(o.rotation_euler),'lens_mm':o.data.lens,'sensor_width_mm':o.data.sensor_width,'ortho_scale':o.data.ortho_scale,'shift_x':o.data.shift_x} for o in s.objects if o.type=='CAMERA']
soft=[]
for o in s.objects:
 if o.get('soft_kind'):
  keys=o.data.shape_keys.key_blocks;soft.append({'part':o.name,'kind':o['soft_kind'],'basis_vertices':len(o.data.vertices),'key_counts':[len(k.data) for k in keys],'all_correspond':all(len(k.data)==len(o.data.vertices) for k in keys),'parent':o.parent.name if o.parent else None,'uv_layers':[x.name for x in o.data.uv_layers],'modifiers':[(m.name,m.type) for m in o.modifiers]})
(RUN/'records/scene-inventory.json').write_text(json.dumps({'cameras':cameras,'rig_sample_checks':checks,'photo_landmarks':projected,'soft_parts':soft,'object_count':len(s.objects),'external_images':[i.filepath for i in bpy.data.images if i.source=='FILE'],'simulation_caches':'None: deterministic shape keys','limitations':'Small inspection record; no collision, material strain or physics validator'},indent=2))
print('Scene inventory saved.')
