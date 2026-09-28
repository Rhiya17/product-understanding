"""Offline contract tests: providers are fakes; real queue and publication logic."""
from pathlib import Path

import pytest

from app import worker
from app.pipeline import authoring as a
from app.pipeline.store import Store

STEPS = [{"claim_id": "step1", "text": "Connect the cable"}]
BRIEF = {"steps": STEPS, "references": [{"id": "manual:p3"}]}


def test_standalone_generation_loads_saved_credentials(tmp_path, monkeypatch):
    import os
    monkeypatch.setattr(a, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(a.generative, "REPO_ROOT", tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    (tmp_path / ".env").write_text(
        'OPENAI_API_KEY="test-openai"\nANTHROPIC_API_KEY="test-anthropic"\n')
    monkeypatch.setattr(worker, "blender_executable", lambda: "/test/blender")
    monkeypatch.setattr(a.shutil, "which", lambda name: "/test/" + name)
    monkeypatch.setattr(a.sys, "platform", "darwin")
    monkeypatch.setattr(a.generative.Budget, "can_start_video", lambda _: True)
    store = Store(tmp_path / "data")

    class ConfigLoaded(Exception):
        pass

    def question(job_id):
        assert os.environ["OPENAI_API_KEY"] == "test-openai"
        assert os.environ["ANTHROPIC_API_KEY"] == "test-anthropic"
        raise ConfigLoaded

    monkeypatch.setattr(store, "question_for_job", question)
    with pytest.raises(ConfigLoaded):
        a.generate(store, {"id": "test-job"}, STEPS, "Product")


def test_generation_reports_configuration_failure_before_creating_work(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "readiness", lambda _: "Astra needs OPENAI_API_KEY configured on this server.")
    store = Store(tmp_path / "data")
    with pytest.raises(a.AuthoringError, match="OPENAI_API_KEY"):
        a.generate(store, {"id": "test-job"}, STEPS, "Product")
    assert not (store.root / "work" / "test-job").exists()


def proposal(ready=False):
    return a.Proposal(ready=ready, python="" if ready else "import bpy", camera="Camera",
                      last_frame=24, parts=["Cable"], notes="", missing_evidence=[],
                      coverage=[a.Coverage(claim_id="step1", start_frame=1, end_frame=24,
                                           mode="motion", explanation="Cable enters port")])


def result(defects=()):
    return a.Critique(reviewed_claim_ids=["step1"], defects=list(defects), missing_evidence=[])


def defect(category="wrong_action", **changes):
    return a.Defect(**(dict(category=category, claim_id="step1", reference_id="manual:p3",
                           seconds=0, observation="wrong port", expected="round port",
                           repair="move the connector to the round port") | changes))


def builder(p, work):
    work.mkdir(parents=True, exist_ok=True)
    return [(0, work / "preview.png")]


def author_sequence(items):
    calls = []
    items = iter(items)
    def author(*args):
        calls.append(args)
        return next(items)
    return author, calls


def test_critic_runs_only_after_astra_preview_self_check(tmp_path):
    author, calls = author_sequence([proposal(), proposal(True)])
    reviews = []
    def review(*args):
        reviews.append(args)
        assert len(calls) == 2 and calls[1][3]
        return result()
    _, _, metrics = a.create_candidate(BRIEF, tmp_path, author, review, builder)
    assert metrics == dict(author_calls=2, builds=1, critic_calls=1, critic_repairs=0)


def test_one_targeted_repair_then_recheck(tmp_path):
    author, calls = author_sequence([proposal(), proposal(True), proposal(), proposal(True)])
    reviews = iter([result([defect()]), result()])
    _, _, metrics = a.create_candidate(BRIEF, tmp_path, author, lambda *args: next(reviews), builder)
    assert metrics["critic_calls"] == 2 and metrics["critic_repairs"] == 1
    assert calls[2][2]["defects"][0]["repair"] == "move the connector to the round port"


def test_critic_cannot_start_second_repair(tmp_path):
    author, calls = author_sequence([proposal(), proposal(True), proposal(), proposal(True)])
    with pytest.raises(a.AuthoringError, match="after one repair"):
        a.create_candidate(BRIEF, tmp_path, author, lambda *args: result([defect()]), builder)
    assert len(calls) == 4


def test_cosmetic_feedback_does_not_trigger_repair(tmp_path):
    author, calls = author_sequence([proposal(), proposal(True)])
    a.create_candidate(BRIEF, tmp_path, author, lambda *args: result([defect("cosmetic")]), builder)
    assert len(calls) == 2


@pytest.mark.parametrize("changes", [{"reference_id": "invented"}, {"seconds": 5},
                                      {"claim_id": "fake"}, {"repair": ""}])
def test_unsupported_feedback_cannot_rewrite_or_publish(changes):
    with pytest.raises(a.AuthoringError, match="unsupported finding"):
        a.actionable_defects(result([defect(**changes)]), BRIEF, [(0, Path("x"))])


def test_missing_evidence_stops_without_critic(tmp_path):
    p = proposal(); p.missing_evidence = ["Unknown connector"]
    author, calls = author_sequence([p])
    with pytest.raises(a.AuthoringError, match="Missing evidence"):
        a.create_candidate(BRIEF, tmp_path, author, lambda *a: pytest.fail("critic called"), builder)


def test_exterior_disclosure_reaches_preview_and_critic(tmp_path):
    limitation = "Unbranded 3.5 mm plug housing; connector size and socket are documented."
    initial, ready = proposal(), proposal(True)
    initial.visual_limitations = ready.visual_limitations = [limitation]
    author, calls = author_sequence([initial, ready])
    reviews = []
    def review(brief, candidate, frames, pass_number):
        reviews.append(candidate)
        assert candidate.visual_limitations == [limitation]
        assert frames
        return result()
    accepted, _, metrics = a.create_candidate(BRIEF, tmp_path, author, review, builder)
    assert accepted.visual_limitations == [limitation]
    assert len(reviews) == 1 and metrics["builds"] == 1


def test_disclosure_cannot_override_action_evidence_blocker(tmp_path):
    p = proposal()
    p.visual_limitations = ["Simplified cable housing"]
    p.missing_evidence = ["Connector diameter and compatible socket are unknown"]
    author, _ = author_sequence([p])
    with pytest.raises(a.AuthoringError, match="Missing evidence"):
        a.create_candidate(BRIEF, tmp_path, author,
                           lambda *args: pytest.fail("critic called"),
                           lambda *args: pytest.fail("unsupported scene built"))


def test_critic_action_evidence_gap_still_blocks():
    review = result()
    review.missing_evidence = ["Socket location is not documented"]
    with pytest.raises(a.AuthoringError, match="Missing evidence"):
        a.actionable_defects(review, BRIEF, [(0, Path("preview.png"))])


@pytest.mark.parametrize("stops,expected_calls,passes", [
    (["max_tokens", "end_turn"], 2, True),
    (["max_tokens", "max_tokens"], 2, False),
    (["refusal"], 1, False),
    (["end_turn"], 1, True),
])
def test_critic_response_recovery_is_bounded_and_metered(tmp_path, monkeypatch,
                                                        stops, expected_calls, passes):
    import anthropic
    from types import SimpleNamespace
    calls, reserved, settled = [], [], []
    responses = iter(stops)
    def parse(**kwargs):
        calls.append(kwargs)
        stop = next(responses)
        return SimpleNamespace(
            stop_reason=stop, parsed_output=result() if stop == "end_turn" else None,
            model="test", usage=SimpleNamespace(input_tokens=10, output_tokens=20),
            model_dump=lambda **kw: {"stop_reason": stop})
    client = SimpleNamespace(
        messages=SimpleNamespace(count_tokens=lambda **kw: SimpleNamespace(input_tokens=10)),
        beta=SimpleNamespace(messages=SimpleNamespace(parse=parse)))
    monkeypatch.setattr(anthropic, "Anthropic", lambda **kw: client)
    budget = SimpleNamespace(reserve=lambda *args: reserved.append(args) or len(reserved),
                             settle=lambda *args: settled.append(args))
    brief = {"steps": STEPS, "references": []}
    if passes:
        assert a.critique(brief, proposal(), [], budget, "job", tmp_path, 1) == result()
    else:
        with pytest.raises(a.AuthoringError):
            a.critique(brief, proposal(), [], budget, "job", tmp_path, 1)
    assert len(calls) == len(reserved) == len(settled) == expected_calls
    assert len(list(tmp_path.glob("critic-1-response-*.json"))) == expected_calls
    if expected_calls == 2:
        assert calls[1]["max_tokens"] == calls[0]["max_tokens"] * 2
        assert calls[1]["messages"] == calls[0]["messages"]


def test_worker_detects_changed_pipeline_code(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "REPO_ROOT", tmp_path)
    folder = tmp_path / "app" / "pipeline"
    folder.mkdir(parents=True)
    path = folder / "authoring.py"
    path.write_text("VERSION = 'one'")
    old = worker.pipeline_code_version()
    path.write_text("VERSION = 'two'")
    assert worker.pipeline_code_version() != old


@pytest.mark.parametrize("change", [None, "evidence", "scene", "preview"])
def test_retry_restores_only_intact_candidate_with_same_evidence(tmp_path, change):
    import json
    store = Store(tmp_path)
    work = store.root / "work" / "job_abc" / "authoring"
    candidate = work / "build-1"
    candidate.mkdir(parents=True)
    (candidate / "scene.py").write_text(proposal().python)
    (candidate / "scene.blend").write_bytes(b"saved scene fixture")
    (candidate / "preview.png").write_bytes(b"preview fixture")
    a.write_json(candidate / "checks.json", {
        "problems": [], "previews": [{"path": "preview.png", "seconds": 0}]})
    brief = dict(question="connect", products=["product"], view="main", steps=STEPS,
                 version="v1", references=[{"id": "manual", "sha256": "source-hash"}])
    a.save_checkpoint(work, brief, proposal(), candidate,
                      dict(author_calls=2, builds=1, critic_calls=1), reviewed=True)
    fresh_brief = json.loads(json.dumps(brief))
    if change == "evidence":
        fresh_brief["references"][0]["sha256"] = "changed"
    elif change == "scene":
        (candidate / "scene.blend").write_bytes(b"modified")
    elif change == "preview":
        (candidate / "preview.png").write_bytes(b"modified")
    target = store.root / "work" / "job_def" / "authoring"
    target.mkdir(parents=True)
    restored = a.restore_checkpoint(store, {"resume_from": "job_abc"}, fresh_brief, target)
    if change:
        assert restored is None
    else:
        assert restored["reviewed"]
        assert restored["proposal"] == proposal()
        assert (restored["candidate_dir"] / "scene.blend").is_file()


def test_pending_review_resume_does_not_rebuild_scene(tmp_path):
    candidate = tmp_path / "build-1"
    candidate.mkdir()
    resume = dict(proposal=proposal(), candidate_dir=candidate, frames=[(0, candidate / "preview.png")],
                  metrics=dict(author_calls=2, builds=1, critic_calls=0))
    _, _, metrics = a.create_candidate(
        BRIEF, tmp_path, lambda *args: pytest.fail("unnecessary author call"),
        lambda *args: result(), lambda *args: pytest.fail("unnecessary rebuild"), resume=resume)
    assert metrics == dict(author_calls=2, builds=1, critic_calls=1, critic_repairs=0)


def test_reviewed_retry_renders_without_provider_calls(tmp_path, monkeypatch):
    store = Store(tmp_path)
    monkeypatch.setattr(a, "readiness", lambda _: None)
    monkeypatch.setattr(store, "question_for_job", lambda _: "connect")
    monkeypatch.setattr(a, "version_for", lambda *args: "version")
    monkeypatch.setattr(a, "evidence_bundle", lambda *args: BRIEF)
    resume = dict(reviewed=True, proposal=proposal(), candidate_dir=tmp_path / "candidate",
                  metrics=dict(author_calls=2, builds=1, critic_calls=1))
    monkeypatch.setattr(a, "restore_checkpoint", lambda *args: resume)
    monkeypatch.setattr(a, "save_checkpoint", lambda *args, **kwargs: None)
    monkeypatch.setattr(a, "create_candidate", lambda *args, **kwargs: pytest.fail("rebuilt scene"))
    monkeypatch.setattr(a.Astra, "__call__", lambda *args: pytest.fail("paid author call"))
    monkeypatch.setattr(a, "critique", lambda *args: pytest.fail("paid critic call"))
    def finish(*args):
        assert args[6:9] == (resume["proposal"], resume["candidate_dir"], resume["metrics"])
        return {"path": "finished.mp4"}
    monkeypatch.setattr(a, "finish_candidate", finish)
    job = dict(id="job_def", product_dir="product", scene_version="version", resume_from="job_abc")
    assert a.generate(store, job, STEPS, "Product") == {"path": "finished.mp4"}


def test_final_render_uses_longer_deadline_and_refreshes_runner(tmp_path, monkeypatch):
    source = tmp_path / "repo" / "app" / "render"
    source.mkdir(parents=True)
    (source / "authored_scene.py").write_text("# current trusted runner")
    monkeypatch.setattr(a, "REPO_ROOT", tmp_path / "repo")
    candidate = tmp_path / "candidate"; candidate.mkdir()
    (candidate / "runner.py").write_text("# stale runner")
    frames = candidate / "frames"; frames.mkdir()
    for frame in range(1, 25):
        (frames / f"frame-{frame:04d}.png").write_bytes(b"fixture")
    calls = []
    monkeypatch.setattr(a, "blender_run", lambda work, timeout: calls.append((work, timeout)))
    monkeypatch.setattr(worker, "encode", lambda *args: (tmp_path / "clip.mp4", tmp_path / "poster.jpg"))
    monkeypatch.setattr(worker, "check_video", lambda *args: 1.0)
    a.render_final(proposal(), candidate, tmp_path, lambda *args: None)
    assert calls == [(candidate, 3600)]
    assert (candidate / "runner.py").read_text() == "# current trusted runner"


def test_completed_evidence_rejection_removes_recovery_checkpoint(tmp_path):
    def saved_builder(p, work):
        frames = builder(p, work)
        (work / "scene.py").write_text(p.python)
        (work / "scene.blend").write_bytes(b"fixture")
        (work / "preview.png").write_bytes(b"fixture")
        a.write_json(work / "checks.json", {
            "problems": [], "previews": [{"path": "preview.png", "seconds": 0}]})
        return frames
    author, _ = author_sequence([proposal(), proposal(True)])
    review = result(); review.missing_evidence = ["Unknown connector compatibility"]
    with pytest.raises(a.AuthoringError, match="Missing evidence"):
        a.create_candidate(BRIEF, tmp_path, author, lambda *args: review, saved_builder)
    assert not (tmp_path / "candidate-checkpoint.json").exists()


def test_build_failures_are_bounded_before_critic(tmp_path):
    def broken(*args):
        raise ValueError("invalid geometry")
    with pytest.raises(a.AuthoringError, match="build limit"):
        a.create_candidate(BRIEF, tmp_path, lambda *args: proposal(),
                           lambda *args: pytest.fail("critic called"), broken)


def test_self_check_cannot_change_metadata_without_render(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "MAX_AUTHOR_CALLS", 2)
    ready = proposal(True); ready.camera = "Other"
    author, _ = author_sequence([proposal(), ready])
    with pytest.raises(a.AuthoringError, match="authoring limit"):
        a.create_candidate(BRIEF, tmp_path, author,
                           lambda *args: pytest.fail("critic called"), builder)


def test_new_website_requests_use_author_and_dedupe(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "readiness", lambda _: None)
    monkeypatch.setattr(a, "version_for", lambda q, p: "astra-" + q)
    store = Store(tmp_path)
    first = store.create_request("a", "product", "Product", "connect", "Connect", "side", "question")
    again = store.create_request("b", "product", "Product", "connect", "Connect", "side", "question")
    other = store.create_request("c", "product", "Product", "connect", "Connect", "side", "different")
    assert first["job_id"] == again["job_id"] != other["job_id"]
    assert store.claim_job()["kind"] == "author"


def test_author_job_automatically_publishes_without_human_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "readiness", lambda _: None)
    monkeypatch.setattr(a, "version_for", lambda *args: "astra-test")
    monkeypatch.setattr(worker, "procedure_steps", lambda *args: (STEPS, "Product"))
    store = Store(tmp_path)
    request = store.create_request("a", "product", "Product", "connect", "Connect", "main", "q")
    job = store.claim_job()
    def generated(*args, **kwargs):
        path = tmp_path / "video.mp4"; path.write_bytes(b"fake")
        return {"product_dir": "product", "procedure_id": "connect", "view": "main",
                "scene_version": "astra-test", "path": str(path), "sha256": "fake",
                "audience": "customer", "label": "3D demonstration", "caveat": "Illustration",
                "chapters": {"step1": 0}, "duration": 1}
    assert worker.process_authoring(store, job, generated) == "succeeded"
    done = store.request("a", request["id"])
    assert done["state"] == "ready" and not done["seen"]


def test_interrupted_author_job_never_auto_replays(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "readiness", lambda _: None)
    monkeypatch.setattr(a, "version_for", lambda *args: "astra-test")
    store = Store(tmp_path)
    request = store.create_request("a", "product", "Product", "connect", "Connect", "main", "q")
    job = store.claim_job()
    assert store.recover_jobs() == 1
    assert store.job(job["id"])["state"] == "failed"
    assert store.request("a", request["id"])["state"] == "failed"


def test_source_or_question_changes_invalidate_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(a.director, "mentioned_products", lambda *args: [])
    p = tmp_path / "evidence-packs" / "product"; p.mkdir(parents=True)
    claims = p / "claims.json"; claims.write_text('{"version":1}')
    v1 = a.version_for("Connect to Mac", "product")
    assert a.version_for("Connect to phone", "product") != v1
    claims.write_text('{"version":2}')
    assert a.version_for("Connect to Mac", "product") != v1


def test_no_unknown_or_dropped_step_can_pass_contract():
    p = proposal(); p.coverage[0].claim_id = "invented"
    with pytest.raises(ValueError, match="every verified step"):
        a.validate_proposal(p, STEPS)


def test_sandbox_environment_has_no_provider_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "run_process", lambda cmd, cwd, log, timeout, env:
                        captured.append((cmd, env)))
    captured = []
    monkeypatch.setenv("OPENAI_API_KEY", "secret")
    a.blender_run(tmp_path, 3)
    cmd, env = captured[0]
    assert cmd[0] == "sandbox-exec" and "OPENAI_API_KEY" not in env
    profile = (tmp_path / "sandbox.sb").read_text()
    assert "(deny default)" in profile and "network" not in profile


def test_critic_repair_cannot_skip_rebuild(tmp_path, monkeypatch):
    monkeypatch.setattr(a, "MAX_AUTHOR_CALLS", 3)
    author, _ = author_sequence([proposal(), proposal(True), proposal(True)])
    reviews = []
    def review(*args):
        reviews.append(args)
        return result([defect()])
    with pytest.raises(a.AuthoringError, match="authoring limit"):
        a.create_candidate(BRIEF, tmp_path, author, review, builder)
    assert len(reviews) == 1


def test_website_request_through_worker_to_playback(tmp_path, monkeypatch):
    import json
    import threading
    import urllib.request
    from app.server import create_server
    monkeypatch.setattr(a, "readiness", lambda _: None)
    monkeypatch.setattr(a, "version_for", lambda *args: "astra-http-test")
    store = Store(tmp_path / "data")
    server = create_server(port=0, video_store=store)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        req = urllib.request.Request(base + "/api/video-requests", data=json.dumps({
            "product_dir": "bose-qc-ultra-headphones", "procedure_id": "connect_aux_cable",
            "view": "main", "question": "Connect the cable to my Mac"}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as response:
            cookie = response.headers["Set-Cookie"].split(";")[0]
            created = json.load(response)["request"]
        assert created["kind"] == "author" and created["state"] == "queued"
        job = store.claim_job()
        def generate(s, j, steps, name, **kwargs):
            s.update_job_stage(j["id"], "refining", .3)
            path = tmp_path / "video.mp4"; path.write_bytes(b"fake-mp4-stream")
            return {"product_dir": j["product_dir"], "procedure_id": j["procedure_id"],
                    "view": j["view"], "scene_version": j["scene_version"],
                    "path": str(path), "sha256": a.file_sha256(path), "audience": "customer",
                    "label": "3D demonstration", "caveat": "Illustration", "chapters": {}, "duration": 1}
        monkeypatch.setattr(a, "generate", generate)
        assert worker.process_job(store, job) == "succeeded"
        req = urllib.request.Request(base + "/api/my-videos", headers={"Cookie": cookie})
        with urllib.request.urlopen(req) as response:
            payload = json.load(response)
        assert payload["unread"] == 1 and payload["active"] == 0
        item = payload["requests"][0]
        assert item["state"] == "ready" and item["asset"]["audience"] == "customer"
        req = urllib.request.Request(base + item["asset"]["url"], headers={"Range": "bytes=0-3"})
        with urllib.request.urlopen(req) as response:
            assert response.status == 206 and response.read() == b"fake"
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=3)


@pytest.mark.parametrize('code', ['credit_balance_exhausted', 'insufficient_quota', 'rate_limit_exceeded'])
def test_provider_quota_failure_explained_without_retry(tmp_path, monkeypatch, code):
    import httpx
    import openai
    monkeypatch.setattr(a, 'readiness', lambda _: None)
    monkeypatch.setattr(a, 'version_for', lambda *args: 'astra-test')
    monkeypatch.setattr(worker, 'procedure_steps', lambda *args: (STEPS, 'Product'))
    store = Store(tmp_path)
    request = store.create_request('a', 'product', 'Product', 'connect', 'Connect', 'main', 'q')
    job = store.claim_job()

    def fail(*args, **kwargs):
        response = httpx.Response(429, request=httpx.Request('POST', 'https://api.openai.com/v1/responses'))
        raise openai.RateLimitError('provider rejected request', response=response,
                                   body={'code': code, 'message': 'provider detail'})

    assert worker.process_authoring(store, job, fail) == 'failed'
    done = store.request('a', request['id'])
    assert done['state'] == 'failed'
    assert ('API account' in done['message']) == (code != 'rate_limit_exceeded')
    assert store.claim_job() is None
