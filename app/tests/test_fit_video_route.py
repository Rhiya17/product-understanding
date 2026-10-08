"""Cargo-fit questions through the normal question -> video workflow.

Real answer engine, evidence packs, store, HTTP server and worker; only the paid
authoring call (Astra + critic + render) is faked. No provider is contacted.
"""
import json
import shutil
import subprocess
import threading
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

import pytest

from app import worker
from app.pipeline import authoring as a
from app.pipeline import fit_brief, service
from app.pipeline.store import REPO_ROOT, Store
from app.render import fit_checks
from system import fit_answer, fit_engine

R2J, TMY = "graco-ready2jet-2212125", "tesla-model-y"
QUESTION = "Can i fit Ready2jet stroller in tesla model y trunk"
PARAPHRASE = "Will the Ready2Jet stroller fit in my Tesla Model Y trunk?"
PROCEDURE = fit_answer.procedure_id(TMY)


@pytest.fixture(autouse=True)
def astra_route(monkeypatch):
    monkeypatch.setenv("SHOWME_VIDEO_PIPELINE", "astra")
    fit_answer._cache.clear()
    yield
    fit_answer._cache.clear()


@pytest.fixture
def server(tmp_path, monkeypatch):
    from app.server import create_server
    monkeypatch.setattr(a, "readiness", lambda _: None)
    store = Store(tmp_path / "data")
    srv = create_server(port=0, video_store=store)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        yield store, f"http://127.0.0.1:{srv.server_port}"
    finally:
        srv.shutdown()
        srv.server_close()
        thread.join(timeout=3)


def ask(base, question, cookie=None, generate=True):
    query = {"q": question, **({"generate": "1"} if generate else {})}
    req = urllib.request.Request(base + "/api/answer?" + urlencode(query),
                                 headers={"Cookie": cookie} if cookie else {})
    with urllib.request.urlopen(req) as response:
        set_cookie = response.headers.get("Set-Cookie")
        return json.load(response)["answer_document"], (
            set_cookie.split(";")[0] if set_cookie else cookie)


def fake_generate(tmp_path, seen):
    def generate(store, job, steps, product_name, progress=lambda *x: None, fit=None):
        seen.append({"job": dict(job), "steps": steps, "fit": fit})
        path = tmp_path / f"{job['id']}.mp4"
        path.write_bytes(b"fake-mp4-stream")
        return {"product_dir": job["product_dir"], "procedure_id": job["procedure_id"],
                "view": job["view"], "scene_version": job["scene_version"],
                "path": str(path), "sha256": a.file_sha256(path), "audience": "customer",
                "label": fit["label"], "caveat": fit["caveat"],
                "chapters": {s["claim_id"]: i * 2.0 for i, s in enumerate(steps)}, "duration": 8}
    return generate


def test_fit_question_on_the_website_makes_a_checked_video_through_the_worker(
        server, tmp_path, monkeypatch):
    store, base = server
    doc, cookie = ask(base, QUESTION)
    assert doc["coverage"]["procedure_id"] == PROCEDURE
    assert doc["video"]["state"] == "requested"
    job = store.claim_job()
    assert job["kind"] == "author" and job["procedure_id"] == PROCEDURE
    assert job["product_dir"] == R2J
    seen = []
    monkeypatch.setattr(a, "generate", fake_generate(tmp_path, seen))
    assert worker.process_job(store, job) == "succeeded"
    brief = seen[0]
    # The brief is assembled from the fit calculation, not supplied by hand.
    assert [s["claim_id"] for s in brief["steps"]] == list(fit_answer.STEP_IDS)
    scene = brief["fit"]["scene"]
    assert scene["verdict"] == doc["coverage"]["fit"]["verdict"]
    assert scene["evidence_fingerprint"] == doc["coverage"]["fit"]["evidence_fingerprint"]
    assert scene["object"]["orientation"]["vertical"] == "object_folded_depth"
    assert brief["fit"]["checks"]["space_targets_m"]["closed_ceiling_height"] == pytest.approx(0.68)
    # Playback: the published asset now answers the question, with chapters.
    doc, _ = ask(base, QUESTION, cookie)
    video = doc["video"]
    assert video["state"] == "ready" and video["assets"][0]["url"].startswith("/video/")
    assert set(video["assets"][0]["chapters"]) == set(fit_answer.STEP_IDS)
    with urllib.request.urlopen(urllib.request.Request(
            base + video["assets"][0]["url"], headers={"Range": "bytes=0-3"})) as response:
        assert response.status == 206 and response.read() == b"fake"


def test_paraphrased_fit_question_reuses_the_checked_video(server, tmp_path, monkeypatch):
    store, base = server
    ask(base, QUESTION)
    job = store.claim_job()
    monkeypatch.setattr(a, "generate", fake_generate(tmp_path, []))
    assert worker.process_job(store, job) == "succeeded"
    doc, _ = ask(base, PARAPHRASE)
    assert doc["video"]["state"] == "ready"
    assert store.claim_job() is None  # no second paid job


def test_fit_version_follows_products_and_evidence_not_wording():
    assert a.version_for(QUESTION, R2J) == a.version_for(PARAPHRASE, R2J)
    assert a.version_for(QUESTION, R2J) != a.version_for("How do I fold it?", R2J)


@pytest.mark.parametrize("verdict", ["DOES_NOT_FIT", "UNKNOWN"])
def test_no_video_is_offered_or_made_without_a_placement(verdict, tmp_path, monkeypatch):
    real = fit_engine.run_case

    def forced(case, **kwargs):
        result = real(case, **kwargs)
        result["verdict"] = verdict
        if verdict == "UNKNOWN":
            result.pop("recommended", None)
        return result

    monkeypatch.setattr(fit_engine, "run_case", forced)
    from system.answer_engine import AnswerEngine
    doc = AnswerEngine().answer(QUESTION).to_dict()
    assert not doc["direct_answer"].lower().startswith(("yes", "very likely"))
    store = Store(tmp_path / "data")
    assert service.video_for_document(store, doc, QUESTION, "v", auto_generate=True) is None
    with pytest.raises(worker.RenderError):
        worker.job_steps({"product_dir": R2J, "procedure_id": PROCEDURE})


def test_image_to_video_path_refuses_fit_jobs(tmp_path):
    store = Store(tmp_path / "data")
    job = {"id": "job_x", "product_dir": R2J, "procedure_id": PROCEDURE, "view": "main",
           "resume_from": None}
    called = []
    assert worker.process_generation(store, job, generate=lambda *x, **k: called.append(1)) \
        in (None, "failed")
    assert not called


def test_brief_cites_only_servable_evidence_and_discloses_unknowns():
    brief = fit_brief.build(R2J, TMY)
    from system.evidence_status import PackEvidence
    packs = {d: PackEvidence(d) for d in (R2J, TMY)}
    for param in brief["scene"]["evidence"].values():
        for claim in param["claims"]:
            assert packs[claim["product_dir"]].eligible(claim["claim_id"])
    result = brief["result"]
    for name in result["recommended"]["unknown_constraints"]:
        if name == "floor_width":
            assert "floor_width_between_arches" in brief["scene"]["space"]["unverified"]
    if result["verdict"] != "FITS_CONFIRMED":
        assert brief["scene"]["disclosure"] and "Not confirmed" in brief["caveat"]
    measured = brief["scene"]["space"]["measured"]
    assert all(v["status"] == "EVIDENCED" for v in measured.values())
    photos = brief["scene"]["reference_photo_ids"][TMY]
    assert photos and all("trunk" in p or "liftgate" in p for p in photos[:2])
    assert any("studio_front" in p for p in photos), "fit scenes need full-vehicle references"


def test_evidence_bundle_uses_the_fit_references(tmp_path):
    fit = fit_brief.build(R2J, TMY)
    job = {"product_dir": R2J, "view": "main", "scene_version": "v"}
    bundle = a.evidence_bundle(job, QUESTION, fit["steps"], "Graco Ready2Jet", tmp_path, fit=fit)
    ids = [r["id"] for r in bundle["references"]]
    for product, wanted in fit["scene"]["reference_photo_ids"].items():
        for sid in wanted:
            assert f"{product}/{sid}" in ids
    assert bundle["fit"]["verdict"] == fit["scene"]["verdict"]
    assert json.loads((tmp_path / "brief.json").read_text())["fit"]["kind"] == "cargo_fit"


def test_display_units_preserve_unrounded_fit_geometry_and_uncertainty():
    brief = fit_brief.build(R2J, TMY)
    scene = brief["scene"]
    display = scene["display_units"]
    assert display["primary"] == "in" and display["secondary"] == "cm"
    assert display["object_envelope"]["lateral"] == "31 in (78.7 cm)"
    assert display["space_measured"]["floor_depth"] == "41.7 in (106 cm)"
    assert "unverified, illustrative" in display["space_illustrative"]["floor_width_between_arches"]
    assert " mm" not in " ".join(step["text"] for step in brief["steps"])
    assert scene["object"]["envelope_mm"]["lateral"] == pytest.approx(786.9)
    assert brief["checks"]["object_envelope_m"][1] == pytest.approx(.7869)
    assert brief["checks"]["clearance_m"] == .025


SPEC = {"object_prefix": "STROLLER_", "colliders": fit_brief.COLLIDERS,
        "object_envelope_m": [0.52, 0.79, 0.29], "object_tolerance": 0.06,
        "space_tolerance": 0.02, "space_targets_m": {"floor_depth": 1.06,
                                                      "closed_ceiling_height": 0.68},
        "clearance_m": 0.025}
GOOD = {"penetrations": {}, "below_floor_frames": [], "final": {
    "object_dimensions_m": [0.52, 0.79, 0.29],
    "min_distance_m": {"floor": 0.0, "seatback": 0.03, "liftgate": 0.30, "side_left": 0.04,
                       "side_right": 0.05, "ceiling": 0.38},
    "space_m": {"floor_depth": 1.06, "closed_ceiling_height": 0.68}}}


def test_fit_checks_pass_a_clean_scene():
    assert fit_checks.compare(SPEC, GOOD) == []


@pytest.mark.parametrize("change, expected", [
    (lambda m: m["penetrations"].update({"40": ["FIT_SIDE_L"]}), "passes through FIT_SIDE_L"),
    (lambda m: m["below_floor_frames"].append(12), "sinks below the floor"),
    (lambda m: m["final"]["min_distance_m"].update(floor=0.05), "not resting on the floor"),
    (lambda m: m["final"]["min_distance_m"].update(seatback=0.01), "clearance to seatback"),
    (lambda m: m["final"].update(object_dimensions_m=[0.45, 0.79, 0.29]), "evidence gives"),
    (lambda m: m["final"]["space_m"].update(closed_ceiling_height=0.75), "closed_ceiling_height"),
])
def test_fit_checks_catch_each_geometry_failure(change, expected):
    measured = json.loads(json.dumps(GOOD))
    change(measured)
    problems = fit_checks.compare(SPEC, measured)
    assert any(expected in p for p in problems), problems


BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
SCENE = """
import bpy
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
def box(name, size, loc):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o
box("FIT_FLOOR", (1.06, 0.94, 0.02), (0.53, 0, -0.01))
box("FIT_CEILING", (1.06, 0.94, 0.02), (0.53, 0, 0.69))
box("FIT_SEATBACK", (0.05, 0.94, 0.68), (1.085, 0, 0.34))
box("FIT_SIDE_L", (1.06, 0.05, 0.68), (0.53, 0.495, 0.34))
box("FIT_SIDE_R", (1.06, 0.05, 0.68), (0.53, -0.495, 0.34))
gate = box("FIT_LIFTGATE", (0.03, 1.0, 0.7), (-0.05, 0, 0.35))
s = box("STROLLER_body", (0.52, 0.79, 0.29), (-0.8, 0, 0.145 + @LIFT@))
s.location.x = -0.8; s.keyframe_insert("location", frame=1)
s.location.z = 0.15; s.keyframe_insert("location", frame=6)
s.location.x = @END_X@; s.location.z = 0.145; s.keyframe_insert("location", frame=12)
gate.location.z = 1.9; gate.keyframe_insert("location", frame=1)
gate.keyframe_insert("location", frame=12)
gate.location.z = 0.35; gate.keyframe_insert("location", frame=20)
bpy.ops.object.camera_add(location=(-2.5, 0, 1.2), rotation=(1.2, 0, -1.5708))
bpy.context.object.name = "Camera"
"""


@pytest.mark.skipif(not BLENDER.is_file(), reason="Blender is not installed")
@pytest.mark.parametrize("end_x, lift, ok", [(0.75, 0.75, True), (0.95, 0.75, False)])
def test_trusted_runner_measures_a_real_blender_fit_scene(tmp_path, end_x, lift, ok):
    work = tmp_path / "build"
    work.mkdir()
    (work / "scene.py").write_text(SCENE.replace("@END_X@", str(end_x)).replace("@LIFT@", str(lift)))
    shutil.copyfile(REPO_ROOT / "app" / "render" / "authored_scene.py", work / "runner.py")
    shutil.copyfile(REPO_ROOT / "app" / "render" / "fit_checks.py", work / "fit_checks.py")
    (work / "contract.json").write_text(json.dumps({
        "mode": "preview", "camera": "Camera", "last_frame": 20, "parts": ["STROLLER_body"],
        "coverage": [], "fit_checks": SPEC}))
    subprocess.run([str(BLENDER), "--background", "--factory-startup", "--python",
                    str(work / "runner.py")], cwd=work, check=True, capture_output=True,
                   timeout=600)
    report = json.loads((work / "checks.json").read_text())
    fit_problems = [p for p in report["problems"] if p.startswith("fit:")]
    if ok:
        assert fit_problems == [], fit_problems
        assert report["fit"]["final"]["min_distance_m"]["floor"] < 0.003
    else:
        # Pushed 20 cm too far: it passes through the seatback.
        assert any("FIT_SEATBACK" in p for p in fit_problems), fit_problems
