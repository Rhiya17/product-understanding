"""Bounded realism pass on the verified run-01 implementation. All shapes INFERRED."""
import bpy, math
from math import sin,cos,pi,exp
from mathutils import Vector
import geometry as g
import rig
legacy_coords=rig.soft_coords
legacy_back=rig.back
ROUND=1

def smooth(x):return rig.smooth(x)
def canopy(u,v,prep):
 # Four supported panels, the final panel being a shallow visor.
 knots=[(0,-.255,1.019),(.32,-.155,1.065),(.76,.120,.965),(1,.145,.891)]
 for a,b in zip(knots,knots[1:]):
  if u<=b[0]+1e-5:
   t=(u-a[0])/(b[0]-a[0]);x=a[1]*(1-t)+b[1]*t;z=a[2]*(1-t)+b[2]*t
   z-=.009*sin(pi*t);break
 else:x,z=knots[-1][1:]
 h=max(0,sin(pi*v))**.62
 # Lower broad undulation under compression, bounded at the mounts.
 gx=-.255+.061*u+.009*sin(6*pi*u)
 gz=1.04-.026*u+.009*sin(6*pi*u+.3)
 x=x*(1-prep)+gx*prep;z=z*(1-prep)+gz*prep
 return Vector((-.17+(x+.17)*h,-.201*cos(pi*v),.795+(z-.795)*h))

def back(u,v,f):
 q=legacy_back(u,v,f)
 # Supported pad with compressed perimeter; shallow crosswise gathering at edges.
 edge=max(0,sin(pi*u)*sin(pi*v))
 q.x+=.019*edge**.55*(1-.38*f)
 q.x+=.0023*sin(u*35*pi+v*2)*exp(-min(v,1-v)*18)*sin(pi*u)
 return q

def seat(u,v):
 width=.160-.010*u**5
 x=.045+.235*sin(u*pi/2);z=.468-.145*u**3
 pillow=.028*max(0,sin(pi*u)*sin(pi*v))**.48
 # Seams compress the upholstered face, not a separate rigid slab.
 for c in [.64,.90]:pillow-=.005*exp(-((u-c)/.018)**2)*sin(pi*v)
 z+=pillow+.0025*sin(v*29*pi+u*3)*exp(-min(u,1-u)*19)*sin(pi*v)
 return Vector((x,(2*v-1)*width,z))

def basket(u,v,kind,sgn,f):
 if kind=='basketfloor':
  a=rig.moved('RIG_support',(-.21,(2*v-1)*.174,.141));b=rig.moved('RIG_front',(.241,(2*v-1)*.174,.178));q=a.lerp(b,u)
  q.z-=.026*sin(pi*u)*sin(pi*v)*(1-f)
  q.x+=.013*f*sin(5*pi*u)*sin(pi*v);q.z+=.025*f*sin(3*pi*u)*sin(pi*v)
 else:
  a=rig.moved('RIG_support',(-.20,sgn*.177,.145));b=rig.moved('RIG_front',(.243,sgn*.177,.180));bottom=a.lerp(b,u)
  a=rig.moved('RIG_support',(-.145,sgn*.182,.298));b=rig.moved('RIG_front',(.191,sgn*.182,.283));top=a.lerp(b,u);top.z-=.020*sin(pi*u)
  q=bottom.lerp(top,v);q.y+=sgn*(.012*sin(pi*u)*sin(pi*v)+.007*f*sin(5*pi*u)*sin(pi*v))
  q.z-=.014*sin(pi*u)*sin(pi*v)*(1-f);q.x+=.010*f*sin(5*pi*u)*sin(pi*v)
 return q

def soft_coords(o,frame):
 kind=o['soft_kind'];nu=o['nu'];nv=o['nv'];sgn=o.get('sign',1)
 f=rig.clamp(rig.interp(frame,4)/-108);prep=smooth((frame-7)/30)
 custom=['canopy','canopyseam','canopylining','canopyedge','seat','seatseam','seatedge','basketside','basketbinding','basketfloor','basketfront','padedge','backbinding']
 if kind not in custom:return legacy_coords(o,frame)
 out=[]
 for i in range(nu+1):
  u=i/nu
  for j in range(nv+1):
   v=j/nv
   if kind.startswith('canopy'):
    if kind=='canopyseam':u=o['along']+(i/nu-.5)*.005
    if kind=='canopyedge':v=.002+j/nv*.004 if sgn<0 else .994+j/nv*.004
    if kind=='canopylining':u=.01+i/nu*.975
    q=canopy(u,v,prep)
    if kind=='canopyseam':q.z+=.0016
    if kind=='canopylining':q.z-=.006;q.x-=.002
    q=rig.moved('RIG_upper_handle',q)
   elif kind in ['seat','seatseam','seatedge']:
    if kind=='seatseam':u=o['along']+(i/nu-.5)*.004
    if kind=='seatedge':v=.008+j/nv*.006 if sgn<0 else .986+j/nv*.006
    q=seat(u,v)
    if kind!='seat':q.z+=.0015
    q=rig.moved('RIG_seat',q)
   elif kind in ['padedge','backbinding']:
    if kind=='backbinding':q=back(u,.014+v*.005 if sgn<0 else .981+v*.005,f);q.x+=.003
    else:
     # Binding outline shares pad coordinate formula with existing harness pad.
     a=2*pi*u;vv=(.35 if sgn<0 else .65)+.058*cos(a);uu=.475+.134*sin(a)
     q=back(uu,vv,f);q.x+=.032;q.z+=.012
   else:
    if kind=='basketbinding':v=.76+v*.24
    if kind=='basketfront':
     # Suspended front mesh between basket floor and foot frame.
     q=basket(.985,v,'basketside',-1,f).lerp(basket(.985,v,'basketside',1,f),u)
    else:q=basket(u,v,kind,sgn,f)
   out.append(q)
 return out

def remesh_soft():
 for o in list(bpy.context.scene.objects):
  if not o.get('soft_kind'):continue
  props=dict(o.items());name=o.name;kind=o['soft_kind'];mat=o.data.materials[0].name
  nu,nv=o['nu'],o['nv'];thick=next((m.thickness for m in o.modifiers if m.type=='SOLIDIFY'),.004)
  if kind=='canopy':nu,nv,thick=60,48,.0025
  if kind=='canopylining':nu,nv,thick=40,36,.0015
  if kind=='canopyseam':props['along']={.07:.005,.55:.32,.99:.76}.get(props['along'],props['along']);nv=48;thick=.0018
  if kind=='seat':nu,nv,thick=44,32,.028
  if kind=='back':nu,nv,thick=44,32,.016
  if kind=='seatseam':props['along']=.64 if props['along']<.8 else .90;nv=32;thick=.001
  if kind=='harnesspad':nu,nv,thick=20,12,.012
  if kind in ['basketside','basketfloor']:nu,nv=30,20
  bpy.data.objects.remove(o,do_unlink=True)
  n=g.soft_grid(name,kind,nu,nv,mat,thick)
  for k,val in props.items():
   if k not in ['nu','nv']:n[k]=val
  n['replaces_run01_part']=name
  if kind in ['seat','back']:
   for m in n.modifiers:
    if m.type=='SOLIDIFY':m.offset=-.55
 for s in [-1,1]:
  for name,kind,nu,nv,mat,thick in [('CANOPY_side_binding','canopyedge',60,2,'trim',.003),('SEAT_edge_binding','seatedge',44,2,'trim',.003),('BACK_edge_binding','backbinding',44,2,'trim',.003)]:
   o=g.soft_grid(name+'_'+str(s),kind,nu,nv,mat,thick);o['sign']=s
 g.soft_grid('FABRIC_basket_front','basketfront',28,16,'mesh',.001)
 o=g.soft_grid('CANOPY_visor_hem','canopyseam',2,48,'trim',.002);o['along']=.997
 # Basis + every shape key regenerated in identical vertex order; no soft reparenting.


def wheel_details():
 # Existing stable tire/spoke identifiers retained. Replace decorative loops with
 # one inset trim following the visibly observed three-lobed molded wheel form.
 for o in list(bpy.data.objects):
  if '_spoke_silver_' in o.name:bpy.data.objects.remove(o,do_unlink=True)
 for o in list(bpy.data.objects):
  if not o.name.endswith('_rubber_tire'):continue
  c=o.location.copy();parent=o.parent;r=.074 if '_rear_' in o.name else .068;base=o.name[:-12]
  for side in [-1,1]:
   pts=[]
   for k in range(121):
    a=2*pi*k/120;r0=r*(.56+.18*cos(3*(a-.22)))
    pts.append((c.x+r0*cos(a),c.y+side*.021,c.z+r0*sin(a)))
   obj=g.tube(base+'_rim_inset_'+str(side),pts,.00085,'silver',parent,True)
   obj['replaces_run01_part']=base+'_spoke_silver_*'
 # Bind seat belt webbing around seat support, keeping legacy buckle/rig.
 for s in [-1,1]:g.tube('HARNESS_waist_'+str(s),[(.065,s*.155,.476),(.058,s*.098,.489),(.066,s*.025,.499)],.009,'dark',bpy.data.objects['RIG_seat'])


def uv_rest():
 # Metric UVs from rest arc lengths. Preserved topology/keys keep weave attached.
 for o in bpy.context.scene.objects:
  if not o.get('soft_kind'):continue
  nu,nv=o['nu'],o['nv'];vs=o.data.vertices;uv=o.data.uv_layers.new(name='RestMetric')
  us=[0.];vv=[0.]
  for i in range(1,nu+1):us.append(us[-1]+(vs[i*(nv+1)+nv//2].co-vs[(i-1)*(nv+1)+nv//2].co).length)
  for j in range(1,nv+1):vv.append(vv[-1]+(vs[(nu//2)*(nv+1)+j].co-vs[(nu//2)*(nv+1)+j-1].co).length)
  for loop in o.data.loops:
   i,j=divmod(loop.vertex_index,nv+1);uv.data[loop.index].uv=(us[i],vv[j])
  o['mapping']='RestMetric: meters along rest centerlines; follows shape keys; compression is inferred'


def fabric_material(m,color,mesh=False):
 nd=m.node_tree.nodes;nd.clear();lk=m.node_tree.links
 out=nd.new('ShaderNodeOutputMaterial');bs=nd.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.86;bs.inputs['Sheen Weight'].default_value=.18;bs.inputs['Sheen Roughness'].default_value=.8
 tex=nd.new('ShaderNodeTexCoord');sep=nd.new('ShaderNodeSeparateXYZ');lk.new(tex.outputs['UV'],sep.inputs[0])
 waves=[]
 for axis in ['X','Y']:
  mul=nd.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=2*pi/(.0022 if mesh else .00065);lk.new(sep.outputs[axis],mul.inputs[0])
  sine=nd.new('ShaderNodeMath');sine.operation='SINE';lk.new(mul.outputs[0],sine.inputs[0]);waves.append(sine)
 cross=nd.new('ShaderNodeMath');cross.operation='MULTIPLY';lk.new(waves[0].outputs[0],cross.inputs[0]);lk.new(waves[1].outputs[0],cross.inputs[1])
 noise=nd.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=160;noise.inputs['Detail'].default_value=2;lk.new(tex.outputs['UV'],noise.inputs['Vector'])
 ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*(x*.73 for x in color),1);ramp.color_ramp.elements[1].color=(*(x*1.13 for x in color),1);lk.new(noise.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs[0],bs.inputs['Base Color'])
 bump=nd.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.20;bump.inputs['Distance'].default_value=.00013;lk.new(cross.outputs[0],bump.inputs['Height']);lk.new(bump.outputs[0],bs.inputs['Normal'])
 lk.new(bs.outputs[0],out.inputs[0])
 if mesh:
  strands=[]
  for w in waves:
   n=nd.new('ShaderNodeMath');n.operation='GREATER_THAN';n.inputs[1].default_value=.62;lk.new(w.outputs[0],n.inputs[0]);strands.append(n)
  mx=nd.new('ShaderNodeMath');mx.operation='MAXIMUM';lk.new(strands[0].outputs[0],mx.inputs[0]);lk.new(strands[1].outputs[0],mx.inputs[1])
  transparent=nd.new('ShaderNodeBsdfTransparent');mix=nd.new('ShaderNodeMixShader');lk.new(mx.outputs[0],mix.inputs[0]);lk.new(transparent.outputs[0],mix.inputs[1]);lk.new(bs.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs[0])
 m['provenance']='Locally authored procedural weave; no photo textures';m['physical_properties']='INFERRED'

def materials():
 fabric_material(g.M['gray'],(.145,.147,.148));fabric_material(g.M['trim'],(.013,.016,.019));fabric_material(g.M['mesh'],(.013,.016,.018),True)
 # Distinct rubber, molded plastic and coated frame responses.
 for key,rough,col in [('rubber',.86,(.009,.011,.012)),('black',.34,(.012,.016,.020)),('dark',.60,(.007,.009,.011)),('tan',.48,(.24,.117,.060))]:
  m=g.M[key];b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Roughness'].default_value=rough;b.inputs['Base Color'].default_value=(*col,1)
  if key=='tan':
   for link in list(m.node_tree.links):
    if link.to_node==b and link.to_socket.name=='Base Color':m.node_tree.links.remove(link)
   for n in m.node_tree.nodes:
    if n.type=='BUMP':n.inputs['Strength'].default_value=.15;n.inputs['Distance'].default_value=.0002
 frame=g.M['black'].copy();frame.name='Frame_satin';frame.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.43;frame.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.22
 for o in bpy.context.scene.objects:
  if o.name.startswith(('FRAME_','HANDLE_lower','HANDLE_upper')) and o.type in ['CURVE','MESH']:o.data.materials.clear();o.data.materials.append(frame)


def cameras():
 s=bpy.context.scene
 defs=[('Camera_Photo',(2.8,4.7,2.20),(-.005,0,.55),78),('Camera_Material',(1.4,2.4,1.38),(.0,0,.60),95)]
 for name,loc,target,lens in defs:
  if name in bpy.data.objects:continue
  d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='PERSP';d.lens=lens;d.sensor_width=36;d.dof.use_dof=False
 s['photo_camera_note']='Practical +Y perspective fit to studio source; 78 mm artistic estimate, not calibrated EXIF. Original orthographic video diagnostic preserved.'


def build(round_no=1):
 global ROUND
 ROUND=round_no;g.build(3);g.studio();remesh_soft();wheel_details()
 rig.back=back;rig.soft_coords=soft_coords;rig.bake();uv_rest();cameras()
 if round_no>=2:materials()
 s=bpy.context.scene;s['realism_round']=round_no;s['identity']='Kingston-reference reconstruction; exact SKU applicability unresolved';s['rights']='INTERNAL RESEARCH';s['geometry_source']='Rebuilt from verified run-01 current scripts with procedural realism modifications';s['deformation']='INFERRED shape-key envelopes; no cloth simulation';s.frame_set(1)
