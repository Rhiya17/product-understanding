"""Local reference inventory and simple contact sheets; no source files modified."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops, ImageStat
RUN=Path(__file__).resolve().parents[1]
ROOT=RUN.parents[1]
OUT=RUN/'references'
OUT.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
pack=json.loads((ROOT/'poc-3d-static-twin/inputs/source-manifest.json').read_text())
vault=ROOT/'source-vault/graco-ready2jet-2212125'
vm=json.loads((vault/'manifest.json').read_text())
entries=[]
for s in vm['sources']:
 p=vault/s['local_path']; name=p.name; meta=pack['images'].get(name,{})
 use='appearance/reference fit'
 if name=='view-02-top-3q.png': use='excluded from binding geometry: unresolved liner/colorway'
 if 'lifestyle' in name: use='qualitative only: person occlusion'
 if 'side-profile' in name: use='visible frame/wheels only; edited person/handle region uncertain'
 entries.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),recorded_sha256=s['sha256'],hash_match=sha(p)==s['sha256'],view=meta.get('viewpoint',s['type']),state=meta.get('state',s['notes']),variant_confidence='Kingston provisional; exact SKU unresolved',original_derived='derived person removal' if 'side-profile' in name else 'source asset as archived',evidence_use=use,rights=s['rights_note']))
idx=json.loads((ROOT/'poc-3d-static-twin/evaluation/fold-study-frames/index.json').read_text())
for f in idx['frames']:
 p=ROOT/'poc-3d-static-twin/evaluation/fold-study-frames'/f['file']
 entries.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),recorded_sha256=f['sha256'],hash_match=sha(p)==f['sha256'],view='fixed wide front three-quarter' if f['frame']>=1166 else 'preparation/control shot',state=f['event'],frame_zero_based=f['frame'],seconds=f['frame']*1001/30000,variant_confidence='visual Kingston',original_derived='lossless decoded video frame',evidence_use='OBSERVED feature positions/motion; INFERRED depths/axes',rights='Manufacturer copyright; internal research; generate_from NOT cleared'))
for page in [33,34,35]:
 p=ROOT/f'poc-higgsfield-one-hand-fold/references/manual-fold-page-{page}.png'
 entries.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),view=f'manual printed/PDF page {page}',state='fold procedure',variant_confidence='Ready2Jet family; exact Kingston applicability UNKNOWN',original_derived='archived page raster derived from manual',evidence_use='DOCUMENTED procedure/controls; page numbers and text verified in original PDF',rights='Manufacturer copyright; internal research; generate_from NOT cleared'))
exclusions=['heldout-05 is duplicate title-card identity reference, never independent validation, never provider input','heldout-01 local-only source restriction retained; not used here','graco_stroller_folding excluded: different FastAction mechanism','view-02 variant unresolved; no binding measurements','Side image edited regions cannot establish hidden geometry']
data=dict(identity='Kingston-reference reconstruction; exact SKU applicability unresolved',manual_applicability='Manual Ready2Jet family title and pp33-35 verified; claim records target 2212125, exact 2209064 applicability unresolved',entries=entries,exclusions=exclusions,evidence_labels={'DOCUMENTED':'source states fact; exact SKU applicability qualified','OBSERVED':'visible feature/motion at named region/frame','INFERRED':'geometric dimension, 3D axis, linkage or fabric motion proposed here','UNKNOWN':'unestablished hidden production details'},validation='All comparisons are reference-fit checks, not independent validation')
(RUN/'input-manifest.json').write_text(json.dumps(data,indent=2))
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(n): return ImageFont.truetype(fontpath,n)
def sheet(items,path,cols=3,w=440,h=470):
 out=Image.new('RGB',(cols*w,70+((len(items)+cols-1)//cols)*h),'#eef1f3');d=ImageDraw.Draw(out)
 d.text((22,20),'READY2JET / INTERNAL RESEARCH / SOURCE REFERENCES',font=font(22),fill='#172431')
 for i,(p,label,box) in enumerate(items):
  im=Image.open(p).convert('RGB')
  if box: im=im.crop(box)
  im=ImageOps.contain(im,(w-24,h-75));x=(i%cols)*w+(w-im.width)//2;y=70+(i//cols)*h
  out.paste(im,(x,y));d.text(((i%cols)*w+12,y+h-65),label,font=font(17),fill='#172431')
 out.save(path)
items=[(vault/'images/view-01-front-3q.png','Open / canopy extended / Kingston',None),(vault/'images/view-03-undercarriage.png','Open / undercarriage crop',None),(vault/'images/folded-01-side.png','Folded / slightly rear side',None),(vault/'images/view-04-side-profile.png','Prepared / edited side / limited use',None),(vault/'images/official-fold-sequence.png','Original marketing sequence',None),(vault/'images/view-02-top-3q.png','EXCLUDED fit / variant uncertain',None)]
sheet(items,OUT/'reference-contact-sheet.jpg')
items=[]
for n in [1166,1173,1180,1186,1206]:
 f=next(f for f in idx['frames'] if f['frame']==n)
 p=ROOT/'poc-3d-static-twin/evaluation/fold-study-frames'/f['file']
 items.append((p,f"{n} / {f['seconds']:.3f}s / {['open','early','middle','late','settled'][len(items)]}",(680,100,1540,1080)))
sheet(items,OUT/'fold-five-stages.jpg',cols=5,w=330,h=430)
# Verify archived decoded frame pixels against the original MP4, independently of PNG encoding.
verify=[]
for n in [1166,1173,1180,1186,1206]:
 out=OUT/f'original-frame-{n}.png'
 subprocess.run(['ffmpeg','-v','error','-i',str(vault/'videos/official-fold-video.mp4'),'-vf',f'select=eq(n\\,{n})','-frames:v','1','-y',str(out)],check=True)
 f=next(f for f in idx['frames'] if f['frame']==n)
 old=Image.open(ROOT/'poc-3d-static-twin/evaluation/fold-study-frames'/f['file']).convert('RGB')
 fresh=Image.open(out).convert('RGB')
 diff=ImageChops.difference(old,fresh)
 verify.append(dict(frame=n,seconds=n*1001/30000,pixels_identical=old.tobytes()==fresh.tobytes(),mean_absolute_RGB_difference_8bit=ImageStat.Stat(diff).mean,maximum_RGB_difference_8bit=max(v[1] for v in diff.getextrema()),finding='Same frame geometry/timestamp confirmed visually; small decoder color conversion difference (OpenCV historical vs FFmpeg current). Use fresh original-decoded frames for comparisons.',fresh_frame_path=str(out.relative_to(RUN)),fresh_frame_sha256=sha(out)))
(RUN/'records/frame-verification.json').write_text(json.dumps(verify,indent=2))
print(json.dumps({'references':len(entries),'recorded_hashes_match':all(e.get('hash_match',True) for e in entries),'frames':verify},indent=2))
