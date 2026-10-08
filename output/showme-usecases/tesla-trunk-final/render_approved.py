"""Render the user's approved trunk-focused revision with the normal renderer."""
import json
import shutil
from pathlib import Path

from app.pipeline import authoring as a, fit_brief
from app.pipeline.store import Store, now
from app.render.fit_checks import compare
from app.worker import acquire_lock, file_sha256

s = Store()
jid = "job_633c80e3161f"
root = Path(__file__).resolve().parent
candidate = root / "preview"
lock = acquire_lock(s)
if lock is None:
    raise RuntimeError("Another worker owns the render queue")
p = a.Proposal.model_validate_json((root / "proposal.json").read_text())
fit = json.loads((root / "fit.json").read_text())
checks = json.loads((candidate / "checks.json").read_text())
assert not checks["problems"]
assert not compare(fit["checks"], checks["fit"])
assert (candidate / "scene.py").read_text() == p.python
current = fit_brief.build("graco-ready2jet-2212125", "tesla-model-y")
assert current["scene"]["evidence_fingerprint"] == fit["scene"]["evidence_fingerprint"]
question = s.question_for_job(jid)
version = a.version_for(question, "graco-ready2jet-2212125")
with s.tx() as db:
    assert not db.execute("SELECT id FROM jobs WHERE state IN ('queued','running')").fetchall(), "Another job is active"
    assert db.execute("SELECT state FROM jobs WHERE id=?", (jid,)).fetchone()[0] == "failed"
    db.execute("UPDATE jobs SET state='running',stage='rendering',progress=.65,error=NULL,finished_at=NULL,started_at=?,scene_version=? WHERE id=?", (now(), version, jid))
    db.execute("UPDATE requests SET state='rendering',asset_id=NULL,message=NULL,updated_at=? WHERE job_id=?", (now(), jid))
j = s.job(jid)
out = s.root / "assets" / jid
out.mkdir(parents=True, exist_ok=True)
try:
    print("RENDER_STARTED", jid, flush=True)
    video, poster, duration = a.render_final(p, candidate, out, lambda stage, fraction: s.update_job_stage(jid, stage, fraction))
    current = fit_brief.build("graco-ready2jet-2212125", "tesla-model-y")
    assert current["scene"]["evidence_fingerprint"] == fit["scene"]["evidence_fingerprint"], "Fit evidence changed during rendering"
    assert a.version_for(question, j["product_dir"]) == version, "Source evidence changed during rendering"
    for name in ("scene.blend", "scene.py", "checks.json"):
        shutil.copyfile(candidate / name, out / name)
    provenance = {
        "review": "User approved trunk-focused strategy and inches-first labels, and explicitly requested final generation. Updated preview frames inspected by Codex before rendering.",
        "automatic_geometry_checks_passed": True,
        "independent_critic_passed": False,
        "source_job": jid,
        "fit": {"verdict": fit["scene"]["verdict"], "evidence_fingerprint": fit["scene"]["evidence_fingerprint"], "checks": fit["checks"], "results": checks["fit"]},
        "scene_sha256": file_sha256(out / "scene.blend"),
        "video_sha256": file_sha256(video),
        "api_calls_for_this_edit_and_render": 0,
    }
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2))
    asset = s.complete_job(jid, {
        "product_dir": j["product_dir"], "procedure_id": j["procedure_id"], "view": j["view"],
        "scene_version": version, "path": str(video), "poster": str(poster), "sha256": file_sha256(video),
        "audience": "customer", "label": "Ready2Jet in a Tesla Model Y trunk · Fit illustration",
        "caveat": "Likely fits, not confirmed. The width between the wheel arches is unverified and illustrated; this shows the calculated placement, not proof of fit.",
        "chapters": {c.claim_id: (c.start_frame - 1) / a.FPS for c in p.coverage}, "duration": duration,
    })
    print("VIDEO_READY", asset, video, duration, flush=True)
except Exception as exc:
    s.fail_job(jid, str(exc), retry=False)
    raise
