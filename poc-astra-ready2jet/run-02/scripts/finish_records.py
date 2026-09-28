"""Lightweight completion records for this bounded run; no evaluation framework."""
from pathlib import Path
import json,hashlib,time,os,subprocess
RUN=Path(__file__).resolve().parents[1];ROOT=RUN.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
session=json.loads((RUN/'records/session.json').read_text());end=time.time()
rows=json.loads((RUN/'records/preservation-start.json').read_text());checked=[]
for row in rows:
 actual=sha(ROOT/row['path']);checked.append({**row,'sha256_end':actual,'unchanged':actual==row['sha256']})
# Verify the additional primary input paths against the inherited/source manifest.
for row in json.loads((RUN/'input-manifest.json').read_text())['entries']:
 if row['path'] not in {x['path'] for x in checked}:
  actual=sha(ROOT/row['path']);checked.append({'path':row['path'],'sha256':row['sha256'],'sha256_end':actual,'unchanged':actual==row['sha256']})
assert all(r['unchanged'] for r in checked)
modified=[]
for base,dirs,files in os.walk(ROOT):
 dirs[:]=[d for d in dirs if d not in ['.git','node_modules','.next','.venv','__pycache__'] and not (Path(base)/d).resolve().is_relative_to(RUN)]
 for name in files:
  p=Path(base)/name
  try:
   if p.stat().st_mtime>session['start_epoch']:modified.append({'path':str(p.relative_to(ROOT)),'mtime':p.stat().st_mtime})
  except OSError:pass
pres={'hashes':checked,'all_selected_hashes_unchanged':True,'outside_run_files_modified_since_start':modified,'scope':'Metadata scan of project files excluding .git, node_modules, .next, .venv, __pycache__. Not full-repository content hashing.','git_status_end':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)}
(RUN/'records/preservation-end.json').write_text(json.dumps(pres,indent=2))
animations={};intervals=[]
for side,cam in [('main','Camera_Reference'),('rear','Camera_RearRight')]:
 folder=RUN/f'final/frames-{side}';timings=json.loads((folder/f'{cam}-timing.json').read_text());rt=json.loads((folder/f'runtime-render-{cam}.json').read_text());assert len(timings)==193;assert len(list(folder.glob(f'{cam}-*.png')))==193
 animations[side]={'sum_frame_render_seconds':sum(v['seconds'] for v in timings),'process_wall_seconds':rt['seconds'],'frame_count':193,'native_render_size':rt['render_size'],'start_epoch':rt['start_epoch'],'end_epoch':rt['end_epoch']};intervals.append((rt['start_epoch'],rt['end_epoch']))
render_sum=0.;timing_files=[]
for p in RUN.rglob('*-timing.json'):
 v=json.loads(p.read_text());secs=sum(x['seconds'] for x in v);render_sum+=secs;timing_files.append({'path':str(p.relative_to(RUN)),'seconds':secs})
account={'start_epoch':session['start_epoch'],'end_epoch':end,'elapsed_wall_seconds':end-session['start_epoch'],'animations':animations,'animation_span_wall_seconds':max(x[1] for x in intervals)-min(x[0] for x in intervals),'animation_overlap_seconds':max(0,min(x[1] for x in intervals)-max(x[0] for x in intervals)),'saved_frame_timing_sum_seconds':render_sum,'timing_files':timing_files,'accounting_limits':'Authoring, rendering and other renders overlap. Sum of frame time is not elapsed time. Superseded preview timings overwritten during camera correction are not included. Initial prompt/context reading preceded preservation-start.','token_usage':'UNKNOWN','session_cost':'UNKNOWN'}
(RUN/'records/run-accounting.json').write_text(json.dumps(account,indent=2))
report=RUN/'report.md';txt=report.read_text().split('\n## Final measured completion')[0];txt+='\n## Final measured completion\n\n'
txt+=f'Measured preservation-to-delivery window: **{account["elapsed_wall_seconds"]/60:.1f} minutes**. Main frame rendering: **{animations["main"]["sum_frame_render_seconds"]:.1f} s**; rear: **{animations["rear"]["sum_frame_render_seconds"]:.1f} s**. Their process intervals span **{account["animation_span_wall_seconds"]/60:.1f} wall minutes**, with **{account["animation_overlap_seconds"]/60:.1f} minutes overlapping**. Saved preview/still/animation frame timing totals **{render_sum/60:.1f} process-minutes**, not added to elapsed wall time. Superseded camera-preview timings are excluded. Usage/cost: **UNKNOWN**.\n\n'
txt+=f'All **{len(checked)} selected baseline/source hash checks are unchanged**. The outside-run metadata scan found **{len(modified)} files** modified during the measured window; see the preservation record for scope/details. Both MP4 streams pass full decoding; visual review remains sampled frames only.\n'
report.write_text(txt)
files=[RUN/'README.md',RUN/'report.md',RUN/'input-manifest.json',RUN/'part-joint-evidence.json',RUN/'action-event-map.json']+list((RUN/'scripts').glob('*.py'))+list((RUN/'final').glob('*'))
index=[{'path':str(p.relative_to(RUN)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files if p.is_file()]
(RUN/'records/deliverable-index.json').write_text(json.dumps(index,indent=2));print(json.dumps({'elapsed_minutes':account['elapsed_wall_seconds']/60,'selected_hashes_unchanged':len(checked),'outside_run_modified':modified,'animations':animations},indent=2))
