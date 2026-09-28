"""Reference-driven exterior surfaces. All coordinates are proposed (INFERRED), meters."""
import bpy, math
from mathutils import Vector
from math import sin,cos,pi
M={}; SOFT=[]
HUB=(.035,0,.49); HINGE=(-.18,0,.77); REAR=(-.22,0,.074)
def material(name,color,rough=.5,metal=0,fabric=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal
 if fabric:
  n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=410;n.inputs['Detail'].default_value=2
  ramp=m.node_tree.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(*(v*.73 for v in color),1);ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=(*(v*1.12 for v in color),1)
  bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.0006
  l=m.node_tree.links;l.new(n.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],b.inputs['Base Color']);l.new(n.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],b.inputs['Normal'])
 return m
def tag(o,name,mat=None,parent=None):
 o.name=name;o['part_id']=name;o['geometry_evidence']='INFERRED dimensions; OBSERVED exterior category';
 if mat:o.data.materials.append(M[mat])
 if parent:
  bpy.context.view_layer.update();o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 return o
def empty(name,point,parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=point;o.empty_display_size=.035;o.empty_display_type='PLAIN_AXES'
 if parent:
  bpy.context.view_layer.update();o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 o['joint_axis']='Y lateral; INFERRED';return o
def mesh(name,verts,faces,mat,parent=None,sub=0,thick=0):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);tag(o,name,mat,parent)
 if sub: mod=o.modifiers.new('Soft surface subdivision','SUBSURF');mod.levels=sub;mod.render_levels=sub
 if thick:mod=o.modifiers.new('Material thickness','SOLIDIFY');mod.thickness=thick
 return o
def tube(name,points,r,mat,parent=None,cyclic=False):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=12;c.bevel_depth=r;c.bevel_resolution=3
 s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for b,p in zip(s.bezier_points,points):b.co=p;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 s.use_cyclic_u=cyclic;o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);return tag(o,name,mat,parent)
def cyl(name,center,r,depth,mat,parent=None,axis='Y'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=center)
 o=bpy.context.object
 if axis=='Y':o.rotation_euler[0]=pi/2
 if axis=='X':o.rotation_euler[1]=pi/2
 bev=o.modifiers.new('Molded edge','BEVEL');bev.width=.002;bev.segments=2
 return tag(o,name,mat,parent)
def box(name,center,dims,mat,parent=None,bevel=.008):
 bpy.ops.mesh.primitive_cube_add(size=1,location=center);o=bpy.context.object;o.scale=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:m=o.modifiers.new('Rounded upholstery/molding','BEVEL');m.width=bevel;m.segments=4
 return tag(o,name,mat,parent)
def ring(name,c,r,minor,mat,parent=None):
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=minor,major_segments=56,minor_segments=12,location=c,rotation=(pi/2,0,0))
 return tag(bpy.context.object,name,mat,parent)
def wheel(name,c,r,parent,revision):
 ring(name+'_rubber_tire',c,r-.0105,.0105,'rubber',parent)
 ring(name+'_outer_rim',c,r-.021,.005,'black',parent)
 cyl(name+'_axle',c,.016,.037,'black',parent)
 for side in [-1,1]:
  y=c[1]+side*.018
  for k in range(3):
   a=k*2*pi/3+.22
   pts=[(c[0]+cos(a)*.010,y,c[2]+sin(a)*.010),(c[0]+cos(a+.28)*r*.52,y,c[2]+sin(a+.28)*r*.52),(c[0]+cos(a+.15)*r*.74,y,c[2]+sin(a+.15)*r*.74)]
   tube(name+f'_spoke_{side}_{k}',pts,.009,'black',parent)
   if revision: tube(name+f'_spoke_silver_{side}_{k}',[(x,y+side*.007,z) for x,y,z in pts],.0013,'silver',parent)
  cyl(name+f'_hubcap_{side}',(c[0],y,c[2]),.011,.003,'dark',parent)
 if revision:
  for k in range(18):
   a=k*2*pi/18
   tube(name+f'_tread_{k}',[(c[0]+(r-.0008)*cos(a+j*.045),c[1]+j*.010,c[2]+(r-.0008)*sin(a+j*.045)) for j in [-1,0,1]],.0013,'dark',parent)
def soft_grid(name,kind,nu,nv,mat,thick=.006):
 verts=[(0,0,0) for _ in range((nu+1)*(nv+1))];faces=[]
 for i in range(nu):
  for j in range(nv):a=i*(nv+1)+j;faces.append((a,a+1,a+nv+2,a+nv+1))
 o=mesh(name,verts,faces,mat,sub=1,thick=thick);o['soft_kind']=kind;o['nu']=nu;o['nv']=nv;o['geometry_evidence']='INFERRED fabric envelope; no cloth physics';SOFT.append(o);return o
def build(revision=0):
 bpy.ops.wm.read_factory_settings(use_empty=True);SOFT.clear();M.clear()
 for name,color,rough,metal in [('black',(.023,.028,.030),.3,.1),('dark',(.009,.012,.014),.65,0),('rubber',(.019,.022,.023),.82,0),('silver',(.48,.51,.53),.28,.75),('tan',(.28,.135,.065),.52,0),('gray',(.29,.305,.31),.95,0),('trim',(.078,.083,.086),.9,0),('mesh',(.031,.036,.038),.9,0)]:
  M[name]=material(name,color,rough,metal,fabric=name in ['gray','trim','mesh','tan'])
 root=empty('RIG_support',REAR);front=empty('RIG_front',HUB,root);lower=empty('RIG_lower_handle',HUB,root);upper=empty('RIG_upper_handle',HINGE,lower);seat=empty('RIG_seat',(.045,0,.465),root)
 root['canopy_fold']=0.;root['thumb_slide']=0.;root['lever_squeeze']=0.;root['frame_collapse']=0.;root['source_time']=0.
 for sign,label in [(-1,'R'),(1,'L')]:
  y=sign*.205
  tube('FRAME_rear_'+label,[(.035,y,.49),(-.08,sign*.22,.31),(-.22,sign*.233,.09)],.012,'black',root)
  tube('FRAME_front_'+label,[(.035,y,.49),(.17,y,.31),(.255,y,.215),(.278,y,.185)],.012,'black',front)
  tube('HANDLE_lower_'+label,[(.035,sign*.188,.49),(-.06,sign*.188,.61),(-.18,sign*.188,.77)],.0105,'black',lower)
  tube('HANDLE_upper_'+label,[(-.18,sign*.19,.77),(-.263,sign*.19,.99),(-.296,sign*.173,1.064)],.010,'black',upper)
  cyl('HUB_main_'+label,(.035,sign*.211,.49),.031,.024,'black',root)
  cyl('HUB_split_handle_'+label,(-.18,sign*.195,.77),.029,.022,'black',lower)
  cyl('HUB_split_screw_'+label,(-.18,sign*.21,.77),.007,.002,'silver',lower)
  for i,(x,z) in enumerate([(.035,.49),(-.19,.12)]):cyl(f'FASTENER_{label}_{i}',(x,sign*.229,z),.004,.004,'silver',root)
  wheel('WHEEL_rear_'+label,(-.22,sign*.238,.074),.074,root,revision)
  caster=empty('RIG_caster_'+label,(.278,y,.185),front)
  cyl('CASTER_swivel_'+label,(.278,y,.175),.021,.055,'black',caster,axis='Z')
  for s in [-1,1]:
   tube(f'CASTER_fork_{label}_{s}',[(.278,y+s*.024,.161),(.286,y+s*.025,.114),(.28,y+s*.023,.068)],.010,'black',caster)
  wheel('WHEEL_front_'+label,(.28,y,.068),.068, caster,revision)
 tube('FRAME_foot_U',[(.23,-.205,.245),(.282,-.19,.204),(.298,-.13,.199),(.300,0,.195),(.298,.13,.199),(.282,.19,.204),(.23,.205,.245)],.015,'black',front)
 tube('FRAME_rear_axle',[(-.22,-.23,.083),(-.22,.23,.083)],.008,'black',root)
 box('BRAKE_cross_pedal',(-.228,0,.105),(.045,.075,.014),'black',root,.005)
 tube('HANDLE_tan_grip',[(-.282,-.19,1.02),(-.304,-.17,1.065),(-.316,-.11,1.078),(-.32,0,1.079),(-.316,.11,1.078),(-.304,.17,1.065),(-.282,.19,1.02)],.014,'tan',upper)
 box('CONTROL_center_housing',(-.322,0,1.078),(.037,.092,.034),'black',upper,.012)
 thumb=empty('RIG_thumb',(-.327,0,1.1),upper);box('CONTROL_thumb_slider',(-.327,0,1.099),(.025,.035,.008),'dark',thumb,.003)
 lever=empty('RIG_lever',(-.318,0,1.047),upper);box('CONTROL_squeeze_lever',(-.318,0,1.047),(.027,.067,.010),'dark',lever,.004)
 # Belly bar's rigid U contour stays with the main hub. It becomes the carry arch.
 tube('BELLY_carry_bar',[(.032,-.176,.485),(.098,-.176,.618),(.147,-.15,.665),(.160,-.08,.682),(.164,0,.686),(.160,.08,.682),(.147,.15,.665),(.098,.176,.618),(.032,.176,.485)],.012,'black',root)
 if revision:
  box('BELLY_center_badge',(.177,0,.682),(.005,.048,.015),'silver',root,.003)
  # Upholstered seat, side bolsters and webbing are surfaces, not box proxies.
 soft_grid('FABRIC_backrest','back',22,16,'gray',.012)
 soft_grid('FABRIC_seat_cushion','seat',12,16,'gray',.019)
 soft_grid('FABRIC_canopy','canopy',22,24,'gray',.004)
 soft_grid('FABRIC_basket_floor','basketfloor',12,12,'mesh',.003)
 for sign in [-1,1]:
  o=soft_grid('FABRIC_basket_side_'+str(sign),'basketside',16,8,'mesh',.0015);o['sign']=sign
  o=soft_grid('FABRIC_back_bolster_'+str(sign),'bolster',22,6,'trim',.014);o['sign']=sign
 if revision:
  for sign in [-1,1]:
   o=soft_grid('HARNESS_shoulder_'+str(sign),'strap',18,2,'dark',.002);o['sign']=sign
  buckle=box('HARNESS_buckle',(.066,0,.493),(.039,.047,.016),'black',seat,.005)
  cyl('HARNESS_release_button',(.074,0,.504),.010,.004,'dark',seat,axis='Z')
  for y in [-.08,0,.08]:tube('FOOT_tread_'+str(y),[(.282,y-.02,.212),(.300,y,.212),(.283,y+.02,.212)],.002,'dark',front)
 cup=empty('RIG_cup',(-.21,.238,.764),upper)
 # Hollow tapered cup with open rim, not a solid cylinder.
 verts=[];faces=[]
 for r,z in [(.032,.705),(.038,.778),(.033,.778),(.027,.714)]:
  for k in range(40):a=k*2*pi/40;verts.append((-.21+r*cos(a),.238+r*sin(a),z))
 for j in range(3):
  for k in range(40):faces.append((j*40+k,j*40+(k+1)%40,(j+1)*40+(k+1)%40,(j+1)*40+k))
 faces.append(tuple(range(120,160)));mesh('CUP_hollow_holder',verts,faces,'black',cup)
 bpy.context.scene.unit_settings.system='METRIC'
 bpy.context.scene['geometry_source']='Fresh curves and custom meshes; no old scaffold, Tripo or Meshy content'
 bpy.context.scene['revision']=revision
def studio():
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.fps=24;s.frame_start=1;s.frame_end=193
 s.view_settings.view_transform='AgX';s.world=bpy.data.worlds.new('Studio_world') if not s.world else s.world;s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.77,.82,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.004));ground=bpy.context.object;ground.name='STUDIO_floor';m=material('Floor',(.72,.75,.76),.8);ground.data.materials.append(m)
 for name,loc,power,size in [('Key',(2,-3,4),450,3),('Fill',(-2,-1,2),200,2.5),('Rim',(-1,3,3),350,2)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
 for name,loc,target,scale in [('Camera_Reference',(2.3,-3.7,2.0),(0,0,.55),1.35),('Camera_Side',(0,-4,.95),(0,0,.55),1.35),('Camera_RearRight',(-2.5,-3.2,1.75),(0,0,.55),1.35),('Camera_Hero',(2.4,-3.8,2.3),(0,0,.55),1.28),('Camera_Control',(-1.3,-1.5,1.65),(-.315,0,1.055),.28)]:
  d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale
 s.camera=bpy.data.objects['Camera_Reference']
