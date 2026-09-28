"""Sampled external motion hypothesis; rigid members retain constant local geometry.
No force, latch, cable or hidden production-linkage simulation is claimed.
"""
import math,bpy
from mathutils import Vector
from math import sin,cos,pi
from geometry import HUB, HINGE, REAR
EVENTS=[(73,1166,0,0,0,0),(84.2,1173,-1,0,-12,23),(95.4,1180,-4,8,-62,80),(105,1186,-12,22,-81,105),(116.2,1193,-24,44,-108,158),(137,1206,-24,44,-108,158)]
def clamp(x):return max(0,min(1,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def interp(frame,col):
 if frame<=EVENTS[0][0]:return EVENTS[0][col]
 for a,b in zip(EVENTS,EVENTS[1:]):
  if frame<=b[0]:t=(frame-a[0])/(b[0]-a[0]);return a[col]*(1-t)+b[col]*t
 return EVENTS[-1][col]
def moved(name,p):
 # Original geometry uses parent inverse matrices to retain open world coordinates.
 o=bpy.data.objects[name];rest={'RIG_support':REAR,'RIG_front':HUB,'RIG_lower_handle':HUB,'RIG_upper_handle':HINGE,'RIG_seat':(.045,0,.465)}[name]
 return o.matrix_world@Vector(tuple(p[i]-rest[i] for i in range(3)))
def back(u,v,f):
 a=moved('RIG_upper_handle',(-.278,0,.989));b=moved('RIG_support',(.045,0,.465));q=a.lerp(b,u)
 q.z-=sin(pi*u)*(.025+.265*f*f)
 q.x+=sin(pi*u)*(.028-.020*f)+.013*sin(pi*v)**2*sin(pi*u)
 q.y=(v*2-1)*(.158+.008*sin(pi*u));q.z+=.012*(2*v-1)**2
 return q
def soft_coords(o,frame):
 kind=o['soft_kind'];nu=o['nu'];nv=o['nv'];f=clamp((interp(frame,4))/-108);prep=smooth((frame-7)/30);sgn=o.get('sign',1);vs=[]
 for i in range(nu+1):
  u=i/nu
  for j in range(nv+1):
   v=j/nv
   if kind in ['back','bolster','strap','harnesspad','backseam']:
    vv=v if kind=='back' else ((.03+v*.075) if sgn<0 else (.895+v*.075)) if kind=='bolster' else (.29+v*.12 if sgn<0 else .59+v*.12) if kind=='harnesspad' else (.035+v*.007 if sgn<0 else .958+v*.007) if kind=='backseam' else (.32+v*.065 if sgn<0 else .615+v*.065)
    uu=.34+u*.27 if kind=='harnesspad' else .16+u*.73 if kind=='strap' else u
    q=back(uu,vv,f)
    if kind=='bolster':q.x+=.018*sin(pi*v);q.z+=.005
    if kind=='strap':q.x+=.013;q.z+=.011
    if kind=='harnesspad':q.x+=.027+.012*sin(pi*v);q.z+=.012
    if kind=='backseam':q.x+=.01;q.z+=.008
   elif kind in ['seat','seatseam']:
    if kind=='seatseam':u=o['along']+(i/nu-.5)*.005
    x=.045+.235*sin(u*pi/2);z=.468-.145*u**3+.025*sin(pi*u)*sin(pi*v)
    q=moved('RIG_seat',(x,(v*2-1)*(.165-.016*u**4)*(1-.045*cos(v*2*pi)),z+(.022 if kind=='seatseam' else 0)))
   elif kind in ['canopy','canopyseam']:
    if kind=='canopyseam':u=o['along']+(i/nu-.5)*.008
    # Fan shell around transverse mounting line. Preparation gathers ribs.
    angle=(-.36+(1-prep)*1.96*u+.16*prep*u)
    width=.19*sin(pi*v);yy=-.194*cos(pi*v)
    rr=.272+.010*sin(u*3*pi)*(1-prep)+.015*sin(u*10*pi)*prep+(.006 if kind=='canopyseam' else 0)
    x=-.16+rr*sin(angle)*sin(pi*v);z=.797+rr*cos(angle)*sin(pi*v)
    # side tips sit at mounts; top/crown remains behind fold controls
    q=moved('RIG_upper_handle',(x,yy,z))
   elif kind=='canopylining':
    # Gathered liner remains fabric throughout preparation. No mesh swaps.
    yy=(v*2-1)*.182
    z=.80+.22*sin(pi*v)*(.25+.75*u)
    x=-.27+.065*u+.018*sin(v*12*pi+u*pi)*prep+.01*sin(u*8*pi)
    q=moved('RIG_upper_handle',(x,yy,z))
   elif kind=='sidewing':
    if u<=.72:
     bu=u/.72;q=back(bu,0 if sgn<0 else 1,f);q.x+=(.015+.060*sin(pi*bu)**2)*(v)*((1-f)*.8+.2);q.y+=sgn*(.004+.020*v);q.z+=.008*sin(pi*v)
    else:
     su=(u-.72)/.28;x=.045+.235*sin(su*pi/2);z=.468-.145*su**3
     q=moved('RIG_seat',(x,sgn*(.159+.023*v),z-.044*sin(pi*su)*v))
   elif kind=='basketfloor':
    a=moved('RIG_support',(-.21,(v*2-1)*.177,.135));b=moved('RIG_front',(.243,(v*2-1)*.177,.185));q=a.lerp(b,u);q.z-=.035*sin(pi*u)*sin(pi*v)
   elif kind in ['basketside','basketbinding']:
    if kind=='basketbinding':v=.88+v*.12
    bottomA=moved('RIG_support',(-.20,sgn*.177,.145))
    bottomB=moved('RIG_front',(.245,sgn*.177,.18));a=bottomA.lerp(bottomB,u)
    topA=moved('RIG_support',(-.13,sgn*.184,.30))
    topB=moved('RIG_front',(.18,sgn*.184,.28));b=topA.lerp(topB,u);q=a.lerp(b,v)
   vs.append(q)
 return vs
def pose(frame):
 root=bpy.data.objects['RIG_support'];root.rotation_euler[1]=math.radians(interp(frame,2));root['source_time']=interp(frame,1)*1001/30000
 root['frame_collapse']=clamp((frame-73)/(116.2-73));root['canopy_fold']=smooth((frame-7)/30);root['thumb_slide']=smooth((frame-43)/12);root['lever_squeeze']=smooth((frame-58)/12)
 bpy.data.objects['RIG_front'].rotation_euler[1]=math.radians(interp(frame,3))
 bpy.data.objects['RIG_lower_handle'].rotation_euler[1]=math.radians(interp(frame,4))
 bpy.data.objects['RIG_upper_handle'].rotation_euler[1]=math.radians(interp(frame,5))
 bpy.data.objects['RIG_seat'].rotation_euler[1]=math.radians(88*clamp(-interp(frame,4)/108))
 bpy.data.objects['RIG_thumb'].location.y=-.008*root['thumb_slide']
 bpy.data.objects['RIG_lever'].location.z=1.047+.007*root['lever_squeeze']
 bpy.data.objects['RIG_cup'].rotation_euler[0]=math.radians(-18*smooth((frame-15)/22))
 bpy.context.view_layer.update()
def bake():
 s=bpy.context.scene
 rigs=[o for o in s.objects if o.name.startswith('RIG_')]
 for f in range(1,194):
  pose(f)
  for o in rigs:
   o.keyframe_insert('rotation_euler',frame=f);o.keyframe_insert('location',frame=f)
  for k in ['canopy_fold','thumb_slide','lever_squeeze','frame_collapse','source_time']:
   bpy.data.objects['RIG_support'].keyframe_insert(data_path=f'["{k}"]',frame=f)
 times=[1,7,19,37,73,84.2,95.4,105,116.2,137,193]
 for o in [o for o in s.objects if o.get('soft_kind')]:
  pose(1);coords=soft_coords(o,1)
  for v,co in zip(o.data.vertices,coords):v.co=co
  o.shape_key_add(name='Basis')
  for t in times[1:]:
   pose(t);key=o.shape_key_add(name=f'pose_{t:06.1f}')
   for v,co in zip(key.data,soft_coords(o,t)):v.co=co
   for other in times:key.value=1. if other==t else 0.;key.keyframe_insert('value',frame=other)
 # Linear interpolation avoids easing artifacts between observed samples.
 for action in bpy.data.actions:
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
 pose(1);s.frame_set(1)
