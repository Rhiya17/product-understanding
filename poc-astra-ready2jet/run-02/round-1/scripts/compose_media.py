"""Compose diagnostic presentation media from clean Blender frames and local sources."""
from pathlib import Path
import argparse,json,subprocess,statistics
from PIL import Image,ImageDraw,ImageFont,ImageOps
RUN=Path(__file__).resolve().parents[1];ROOT=RUN.parents[1];FINAL=RUN/'final'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def ft(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def wrap(d,text,xy,width,font,fill,leading=1.28):
 if '\n' in text:
  x,y=xy
  for paragraph in text.split('\n'):y=wrap(d,paragraph,(x,y),width,font,fill,leading)
  return y
 x,y=xy;line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=font)>width and line:d.text((x,y),line,font=font,fill=fill);y+=int(font.size*leading);line=word
  else:line=test
 if line:d.text((x,y),line,font=font,fill=fill);y+=int(font.size*leading)
 return y
def stage(f):
 if f<=37:return ('01','Preparation','Empty stroller; no infant car seat. Brakes are assumed unlocked. Canopy gathers and cup holder rotates illustratively. Casters start aligned.','Manual pp. 33-34 / preparation retimed')
 if f<=73:return ('02','Release controls','Slide the thumb switch, then squeeze the handle lever. The manual establishes this order; exact control travel is not established.','Manual p. 34 / travel is illustrative')
 if f<=137:return ('03','Frame collapse','Split handle doubles back. Front and rear wheel assemblies converge. Fabric follows an inferred deformation, without cloth physics.','Source 38.906-40.240 s / 2x slow motion')
 return ('04','Secure and carry','The manual calls for checking that the stroller is secure, then carrying it by the belly bar. These actions are communicated here and are not simulated.','Manual p. 35 / final presentation hold')
def panel(frame,cam):
 im=Image.open(FINAL/('frames-main' if cam=='main' else 'frames-rear')/f'Camera_{"Reference" if cam=="main" else "RearRight"}-{frame:04d}.png').convert('RGB')
 out=Image.new('RGB',(1280,720),'#12242e');out.paste(im,(0,0));d=ImageDraw.Draw(out)
 d.text((28,22),'A / REFERENCE VIEW' if cam=='main' else 'B / REAR-RIGHT DIAGNOSTIC',font=ft(16,True),fill='#132934')
 d.rounded_rectangle((22,668,235,700),radius=4,fill='#12242e');d.text((34,675),'INTERNAL RESEARCH',font=ft(17,True),fill='#e7eff0')
 x=756;d.text((x,36),'KINGSTON REFERENCE',font=ft(18,True),fill='#a8c0c5')
 d.text((x,72),'Fold study',font=ft(44,True),fill='#f0f2ef')
 d.text((x,128),'Partial illustrative result',font=ft(20),fill='#e2bd84')
 d.line((x,177,1236,177),fill='#39505a',width=1)
 num,title,body,cite=stage(frame)
 d.text((x,207),num,font=ft(19,True),fill='#82bbb6');d.text((x+42,201),title,font=ft(27,True),fill='#eff3f0')
 y=wrap(d,body,(x,250),470,ft(22),'#d4dee0')
 if 38<=frame<=73:
  manual=Image.open(RUN/'references/control-crop.png').convert('RGB');manual=ImageOps.contain(manual,(265,176));out.paste(manual,(x,410))
  wrap(d,'DOCUMENTED order\nINFERRED travel',(x+285,437),185,ft(16),'#b4c7cc')
 elif cam=='rear':
  wrap(d,'Rear surfaces and the hidden production linkage remain unverified.',(x,440),465,ft(20),'#a7bdc3')
 else:
  d.text((x,440),'SAME MODEL / SAME CAMERA',font=ft(16,True),fill='#82bbb6')
  wrap(d,'Rigid part dimensions stay constant. The rear-wheel support approximation does not simulate balance or operator forces.',(x,474),470,ft(18),'#a7bdc3')
 d.text((x,605),cite,font=ft(17),fill='#e2bd84')
 d.line((x,645,1235,645),fill='#39505a',width=3);d.line((x,645,x+479*(frame-1)/192,645),fill='#82bbb6',width=3)
 d.text((x,666),'Exact SKU applicability unresolved.',font=ft(17),fill='#a7bdc3')
 return out
def source_panel():
 path=ROOT/'poc-higgsfield-one-hand-fold/references/manual-fold-page-34.png'
 im=Image.open(path);im.crop((180,810,490,1065)).save(RUN/'references/control-crop.png')
 crop=Image.open(RUN/'references/control-crop.png').convert('RGB')
 out=Image.new('RGB',(1280,720),'#12242e');d=ImageDraw.Draw(out)
 d.text((55,38),'RELEASE CONTROLS / SOURCE PANEL',font=ft(30,True),fill='#eff3f0')
 crop=ImageOps.contain(crop,(500,440));out.paste(crop,(60,145))
 wrap(d,'1  Slide thumb switch\n2  Squeeze handle lever',(625,160),590,ft(31,True),'#eff3f0')
 wrap(d,'The original Ready2Jet manual, page 34, establishes the location, direction and order. Exact travel is obscured in the video; the model uses an illustrative movement.',(625,280),540,ft(23),'#c3d3d7')
 wrap(d,'Manual applies to the archived Ready2Jet family. Exact Kingston SKU applicability remains unresolved.',(625,470),540,ft(20),'#e2bd84')
 d.text((55,657),'INTERNAL RESEARCH / MANUFACTURER SOURCE / NO HIDDEN LATCH CLAIM',font=ft(18,True),fill='#82bbb6')
 out.save(FINAL/'release-control-source-panel.png')
 subprocess.run(['ffmpeg','-v','error','-loop','1','-i',str(FINAL/'release-control-source-panel.png'),'-t','3','-r','24','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(FINAL/'release-control-source-panel.mp4')],check=True)
def encode(cam):
 target=FINAL/('fold-main.mp4' if cam=='main' else 'fold-rear-right.mp4')
 cmd=['ffmpeg','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1280x720','-framerate','24','-i','-','-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(target)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for f in range(1,194):
  im=panel(f,cam);proc.stdin.write(im.tobytes())
  if f in [1,55,95,145]:im.save(FINAL/f'{cam}-presentation-{f:04d}.jpg',quality=92)
 proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('ffmpeg encoding failed')
 return target
def comparisons():
 # Fixed source crop and fixed Blender camera for every frame in the continuous shot.
 cols=[(1166,73,'OPEN / PREPARED'),(1180,95,'MIDDLE'),(1206,145,'SETTLED / FOLDED')]
 out=Image.new('RGB',(1620,1155),'#12242e');d=ImageDraw.Draw(out)
 d.text((25,22),'READY2JET / REFERENCE FIT / INTERNAL RESEARCH',font=ft(28,True),fill='#eff3f0')
 d.text((25,65),'Manufacturer source above; same editable model below. These are fitting references, not independent validation.',font=ft(19),fill='#b8cbd0')
 for i,(n,f,title) in enumerate(cols):
  x=i*540
  d.text((x+22,110),title,font=ft(21,True),fill='#82bbb6')
  a=Image.open(RUN/f'references/original-frame-{n}.png').crop((680,80,1580,1080));a=ImageOps.contain(a,(510,445));out.paste(a,(x+(540-a.width)//2,145))
  d.text((x+23,601),f'Source {n*1001/30000:.3f} s',font=ft(17),fill='#c8d7db')
  b=Image.open(FINAL/f'frames-main/Camera_Reference-{f:04d}.png').resize((495,495));out.paste(b,(x+22,635))
  d.text((x+29,1100),'INFERRED exterior geometry and motion',font=ft(15),fill='#203b48')
 out.save(FINAL/'open-mid-folded-comparison.jpg',quality=94)
 # All five selected motion stages, at declared global source-time mapping.
 out=Image.new('RGB',(1280,2480),'#12242e');d=ImageDraw.Draw(out)
 d.text((25,22),'FIVE-STAGE REFERENCE FIT / FIXED CAMERA',font=ft(26,True),fill='#eff3f0')
 for i,(n,f) in enumerate([(1166,73),(1173,84),(1180,95),(1186,105),(1206,145)]):
  a=Image.open(RUN/f'references/original-frame-{n}.png').crop((680,80,1580,1080));a=ImageOps.contain(a,(600,435));b=Image.open(FINAL/f'frames-main/Camera_Reference-{f:04d}.png').resize((435,435));y=80+i*480
  out.paste(a,((640-a.width)//2,y));out.paste(b,(740,y));d.text((22,y+442),f'Source {n} / {n*1001/30000:.3f}s',font=ft(20),fill='white');d.text((660,y+442),f'Render {f} / inferred motion',font=ft(20),fill='white')
 out.save(FINAL/'five-stage-comparison.jpg',quality=93)
 # Appearance reference uses its extended-canopy state.
 out=Image.new('RGB',(1440,825),'#12242e');d=ImageDraw.Draw(out);d.text((24,20),'OPEN APPEARANCE / EXTENDED CANOPY / INTERNAL RESEARCH',font=ft(25,True),fill='white')
 a=Image.open(ROOT/'poc-3d-static-twin/inputs/images/view-01-front-3q.png').crop((425,150,1600,1900));a=ImageOps.contain(a,(670,690));out.paste(a,((720-a.width)//2,78));b=Image.open(FINAL/'frames-main/Camera_Reference-0001.png').resize((690,690));out.paste(b,(735,78))
 d.text((24,785),'Manufacturer studio reference',font=ft(21),fill='#c8d7db');d.text((750,785),'Reconstruction / shape fit incomplete',font=ft(21),fill='#e2bd84');out.save(FINAL/'open-appearance-comparison.jpg',quality=94)
def review_sheet(cam):
 frames=[1,19,37,49,61,73,79,84,89,95,100,105,110,116,125,137,153,193]
 out=Image.new('RGB',(1800,1020),'#12242e');d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  p=FINAL/('frames-main' if cam=='main' else 'frames-rear')/f'Camera_{"Reference" if cam=="main" else "RearRight"}-{f:04d}.png'
  im=Image.open(p).resize((300,300));x=i%6*300;y=i//6*340;out.paste(im,(x,y));d.text((x+12,y+309),f'Frame {f} / {(f-1)/24:.2f}s',font=ft(17),fill='white')
 out.save(FINAL/f'{cam}-sampled-animation-review.jpg',quality=92)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--panels-only',action='store_true');args=p.parse_args();source_panel()
 if not args.panels_only:
  targets=[encode('main'),encode('rear')];comparisons();review_sheet('main');review_sheet('rear')
  subprocess.run(['ffmpeg','-v','error','-i',str(targets[0]),'-vf','fps=12,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse','-loop','0','-y',str(FINAL/'fold-main-preview.gif')],check=True)
  records=[]
  for t in targets+[FINAL/'release-control-source-panel.mp4']:
   info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate,nb_frames,codec_name','-of','json',str(t)]));subprocess.run(['ffmpeg','-v','error','-i',str(t),'-f','null','-'],check=True);records.append(dict(file=t.name,probe=info,full_stream_decode='passed; not a visual playback review'))
  (RUN/'records/media-checks.json').write_text(json.dumps(records,indent=2))
 print('Media composition complete.')
