import json
from pathlib import Path
from app.pipeline.store import Store, now
from app.pipeline import authoring as a
from app.worker import file_sha256
s=Store(); jid='job_7afa5618cb92'; root=Path('output/showme-usecases/brakes-arrows').resolve()
p=a.Proposal.model_validate_json((root/'proposal.json').read_text());candidate=root/'spaced-preview'
checks=json.loads((candidate/'checks.json').read_text())
assert not checks['problems']
assert (candidate/'scene.py').read_text()==p.python
with s.tx() as db:
    active=db.execute("SELECT id FROM jobs WHERE state IN ('queued','running')").fetchall()
    if active: raise RuntimeError('Another job is active; do not start parallel rendering')
    db.execute("UPDATE jobs SET state='running',stage='rendering',error=NULL WHERE id=?",(jid,))
    db.execute("UPDATE requests SET state='rendering',message=NULL,updated_at=? WHERE job_id=?",(now(),jid))
j=s.job(jid);out=s.root/'assets'/jid;out.mkdir(parents=True,exist_ok=True)
try:
    video,poster,duration=a.render_final(p,candidate,out,lambda stage,fraction:s.update_job_stage(jid,stage,fraction))
    version=a.version_for(s.question_for_job(jid),j['product_dir'])
    provenance={'review':'User explicitly approved arrow-only preview and requested final rendering.','automatic_geometry_checks':checks['problems'],'independent_critic_passed':False,'scene_sha256':file_sha256(candidate/'scene.blend'),'video_sha256':file_sha256(video),'api_calls_for_this_edit_and_render':0}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2))
    s.complete_job(jid,{'product_dir':j['product_dir'],'procedure_id':j['procedure_id'],'view':j['view'],'scene_version':version,'path':str(video),'poster':str(poster),'sha256':file_sha256(video),'audience':'customer','label':'Ready2Jet brakes · 3D demonstration','caveat':'Illustrative demonstration. Arrows show pedal movement; no person is shown.','chapters':{c.claim_id:(c.start_frame-1)/24 for c in p.coverage},'duration':duration})
    print('VIDEO_READY',video,flush=True)
except Exception as exc:
    s.fail_job(jid,str(exc),retry=False)
    raise
