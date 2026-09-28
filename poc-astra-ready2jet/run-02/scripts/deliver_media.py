"""Compose internal-research outputs from native renders; no product upscaling."""
from pathlib import Path
import json,subprocess,argparse
from PIL import Image,ImageDraw,ImageFont,ImageOps
RUN=Path(__file__).resolve().parents[1];ROOT=RUN.parents[1];FINAL=RUN/'final'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def ft(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def image(path):return Image.open(path).convert('RGB')
def text(d,xy,s,n=22,color='#dde6e9',bold=False):d.text(xy,s,font=ft(n,bold),fill=color)
def wrap(d,xy,s,w=330,n=22):
 x,y=xy;line=''
 for word in s.split():
  if d.textlength((line+' '+word).strip(),font=ft(n))>w:
   text(d,(x,y),line,n);y+=n+9;line=word
  else:line=(line+' '+word).strip()
 text(d,(x,y),line,n);return y+n+9

def comparisons():
 out=Image.new('RGB',(1800,785),'#142630');d=ImageDraw.Draw(out)
 text(d,(28,22),'CANOPY + UPHOLSTERY / CONTROLLED APPEARANCE COMPARISON',28,bold=True)
 text(d,(28,65),'INTERNAL RESEARCH  |  Same camera, lighting, exposure and scale for both model renders.',21)
 source=image(ROOT/'poc-3d-static-twin/inputs/images/view-01-front-3q.png').crop((425,150,1600,1900));source=ImageOps.contain(source,(565,585))
 out.paste(source,((600-source.width)//2,132+(585-source.height)//2))
 for x,folder in [(600,RUN/'baseline/photo'),(1200,FINAL/'reproduction')]:out.paste(image(folder/'Camera_Photo-0001.png').resize((585,585)),(x+7,132))
 for x,label in [(0,'Manufacturer / extended canopy'),(600,'Before / delivered run-01'),(1200,'After / run-02, partial improvement')]:text(d,(x+20,738),label,22,bold=True)
 out.save(FINAL/'open-appearance-comparison.jpg',quality=95)
 out=Image.new('RGB',(1280,745),'#142630');d=ImageDraw.Draw(out);text(d,(20,20),'BEFORE',25,bold=True);text(d,(660,20),'AFTER / INTERNAL RESEARCH',25,bold=True)
 for x,folder in [(0,RUN/'baseline/photo'),(640,FINAL/'reproduction')]:out.paste(image(folder/'Camera_Photo-0001.png'),(x,68))
 text(d,(20,714),'Identical perspective camera and neutral studio. Geometry + materials changed; no beauty lighting.',18)
 out.save(FINAL/'before-after.jpg',quality=95)
 # Geometry-only comparison: both rows share exact camera and clay override.
 out=Image.new('RGB',(1800,1325),'#142630');d=ImageDraw.Draw(out)
 text(d,(25,20),'GEOMETRY / BASELINE ABOVE / REFINEMENT BELOW / INTERNAL RESEARCH',27,bold=True)
 for i,f in enumerate([1,95,145]):
  for row,folder in enumerate([RUN/'baseline/clay',FINAL/'clay']):out.paste(image(folder/f'Camera_Photo-{f:04d}.png').resize((590,590)),(i*600+5,72+row*615))
  text(d,(i*600+20,1295),{1:'Extended open',95:'Middle fold',145:'Settled folded'}[f],20)
 out.save(FINAL/'geometry-before-after.jpg',quality=94)

def stage(f):
 if f<=37:return '01  Preparation','Empty stroller. Brakes assumed unlocked. Canopy gathers; cup rotates. Casters start aligned.','Manual pp. 33-34 / timing inferred'
 if f<=73:return '02  Release','Slide the thumb switch, then squeeze the handle lever. Order is documented; travel is inferred.','Manual p. 34 / see source panel'
 if f<=137:return '03  Collapse','One persistent model. Fabric follows controlled shape keys. No cloth or rigid-body simulation.','Source 38.906-40.240 s / 2x slow motion'
 return '04  Secure and carry','Check that the stroller is secure, then carry by the belly bar. These source-backed instructions are not simulated.','Manual p. 35 / final held pose'

def presentation(f,cam):
 cname='Camera_Reference' if cam=='main' else 'Camera_RearRight';folder='frames-main' if cam=='main' else 'frames-rear'
 im=image(FINAL/folder/f'{cname}-{f:04d}.png');assert im.size==(1280,720);d=ImageDraw.Draw(im)
 d.rectangle((884,0,1279,719),fill='#142630')
 text(d,(910,28),'KINGSTON REFERENCE',18,'#94bdc4',True)
 text(d,(910,69),'Fold study',36,bold=True)
 text(d,(910,120),'Partial realism improvement',18,'#e4c19a')
 title,body,cite=stage(f);text(d,(910,198),title,26,bold=True);wrap(d,(910,249),body,337,22)
 if 38<=f<=73:
  crop=ImageOps.contain(image(RUN/'references/control-crop.png'),(210,143));im.paste(crop,(910,431))
 else:wrap(d,(910,440),'Main diagnostic view' if cam=='main' else 'Rear-right diagnostic view',337,21)
 wrap(d,(910,584),cite,337,17);wrap(d,(910,655),'Exact SKU applicability unresolved.',337,17)
 d.rounded_rectangle((22,674,255,707),radius=5,fill='#142630');text(d,(34,681),'INTERNAL RESEARCH',18,bold=True)
 return im

def encode(cam):
 dest=FINAL/('fold-main.mp4' if cam=='main' else 'fold-rear-right.mp4')
 proc=subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1280x720','-framerate','24','-i','-','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(dest)],stdin=subprocess.PIPE)
 for f in range(1,194):
  im=presentation(f,cam);proc.stdin.write(im.tobytes())
  if f in [1,61,95,145]:im.save(FINAL/f'{cam}-presentation-{f:04d}.jpg',quality=94)
 proc.stdin.close();assert proc.wait()==0

def review():
 frames=[1,13,19,25,37,49,61,73,79,84,89,95,100,105,110,116,137,193]
 for cam,folder in [('Camera_Reference','frames-main'),('Camera_RearRight','frames-rear')]:
  out=Image.new('RGB',(1800,1010),'#142630');d=ImageDraw.Draw(out)
  for i,f in enumerate(frames):
   im=image(FINAL/folder/f'{cam}-{f:04d}.png').crop((114,0,834,720)).resize((300,300));x=i%6*300;y=i//6*337;out.paste(im,(x,y));text(d,(x+10,y+309),f'Frame {f}',18)
  out.save(FINAL/('main-sampled-animation-review.jpg' if cam=='Camera_Reference' else 'rear-sampled-animation-review.jpg'),quality=94)
 out=Image.new('RGB',(1620,1140),'#142630');d=ImageDraw.Draw(out)
 text(d,(22,20),'REFERENCE STATES / SAME MODEL / INTERNAL RESEARCH',26,bold=True)
 for i,(sf,f,name) in enumerate([(1166,73,'PREPARED'),(1180,95,'MIDDLE'),(1206,145,'FOLDED')]):
  x=i*540;text(d,(x+20,69),name,22,bold=True)
  im=ImageOps.contain(image(RUN/f'references/original-frame-{sf}.png').crop((680,80,1580,1080)),(505,470));out.paste(im,(x+(540-im.width)//2,110))
  im=image(FINAL/f'frames-main/Camera_Reference-{f:04d}.png').crop((114,0,834,720)).resize((510,510));out.paste(im,(x+15,603));text(d,(x+20,580),f'Source {sf*1001/30000:.3f}s / model {f}',17)
 out.save(FINAL/'open-mid-folded-comparison.jpg',quality=94)

def stills():
 for f,n in [(1,'open-product'),(145,'folded-product')]:
  im=image(FINAL/f'stills-clean/Camera_Photo-{f:04d}.png');d=ImageDraw.Draw(im);d.rounded_rectangle((25,im.height-66,345,im.height-23),radius=5,fill='#142630');text(d,(39,im.height-56),'INTERNAL RESEARCH',26,bold=True);im.save(FINAL/f'{n}.jpg',quality=96)
 specs=[('Camera_Material','CANOPY / WOVEN FACE'),('Camera_SeatDetail','UPHOLSTERY / BINDING'),('Camera_BasketDetail','BASKET / MESH + FRAME'),('Camera_GripDetail','GRIP / MOLDING')]
 out=Image.new('RGB',(1600,1710),'#142630');d=ImageDraw.Draw(out)
 text(d,(22,20),'MATERIAL DETAIL / NEUTRAL STUDIO / INTERNAL RESEARCH',27,bold=True)
 for i,(cam,label) in enumerate(specs):
  im=image(FINAL/f'details/{cam}-0001.png').resize((790,790));x=i%2*800+5;y=70+i//2*820;out.paste(im,(x,y));text(d,(x+10,y+795),label,19,bold=True)
 out.save(FINAL/'material-detail-sheet.jpg',quality=95)

def checks():
 rows=[]
 for n in ['fold-main.mp4','fold-rear-right.mp4','release-control-source-panel.mp4']:
  p=FINAL/n;probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate,nb_frames,codec_name','-of','json',str(p)]));subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True);rows.append({'file':n,'probe':probe,'decode':'passed','visual_review':'sampled frames only; no normal-speed visual playback'})
 (RUN/'records/media-checks.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--comparisons-only',action='store_true');a=p.parse_args();comparisons()
 if not a.comparisons_only:
  stills();encode('main');encode('rear');review();checks()
  subprocess.run(['ffmpeg','-v','error','-i',str(FINAL/'fold-main.mp4'),'-vf','fps=12,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse','-loop','0','-y',str(FINAL/'fold-main-preview.gif')],check=True)
 print('Composition complete.')
