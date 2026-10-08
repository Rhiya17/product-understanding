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


def test_linked_reset_steps_must_be_reviewed_and_can_trigger_repair(tmp_path):
    brief = dict(BRIEF, steps=[dict(STEPS[0], supporting_procedures=[{
        'procedure_id': 'reset', 'steps': [{'claim_id': 'reset_power'}, {'claim_id': 'reset_off'}]}])])
    with pytest.raises(a.AuthoringError, match='every instruction'):
        a.actionable_defects(result(), brief, [(0, Path('preview.png'))])
    review = a.Critique(reviewed_claim_ids=['step1', 'reset_power', 'reset_off'],
                       defects=[defect(claim_id='reset_power')], missing_evidence=[])
    assert a.actionable_defects(review, brief, [(0, Path('preview.png'))])[0]['claim_id'] == 'reset_power'
    author, calls = author_sequence([proposal(), proposal(True), proposal(), proposal(True)])
    reviews = iter([review, review.model_copy(update={'defects': []})])
    _, _, metrics = a.create_candidate(brief, tmp_path, author, lambda *args: next(reviews), builder)
    assert metrics['critic_repairs'] == 1
    assert calls[2][2]['defects'][0]['claim_id'] == 'reset_power'


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


@pytest.mark.parametrize('via_question', [False, True])
def test_website_request_through_worker_to_playback(tmp_path, monkeypatch, via_question):
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
        if via_question:
            from urllib.parse import urlencode
            req = urllib.request.Request(base + '/api/answer?' + urlencode({
                'q': 'How do I replace the filter in my Levoit Core 300S?', 'generate': '1'}))
        with urllib.request.urlopen(req) as response:
            cookie = response.headers["Set-Cookie"].split(";")[0]
            body = json.load(response)
            created = body['answer_document']['video']['request'] if via_question else body['request']
        assert created["state"] == "queued"
        job = store.claim_job()
        assert job['kind'] == 'author'
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


def test_zero_exit_blender_error_is_actionable_build_feedback(tmp_path, monkeypatch):
    def failed_build(work, timeout):
        (work / 'blender.log').write_text(
            'Traceback:\n  File "scene.py", line 17\n'
            'TypeError: BLENDER_EEVEE_NEXT is not a supported engine\n')
    monkeypatch.setattr(a, 'blender_run', failed_build)
    with pytest.raises(ValueError, match='BLENDER_EEVEE_NEXT'):
        a.build_preview(proposal(), tmp_path / 'build')


def test_anthropic_credit_failure_names_the_review_provider(tmp_path, monkeypatch):
    import anthropic
    import httpx
    monkeypatch.setattr(a, 'readiness', lambda _: None)
    monkeypatch.setattr(a, 'version_for', lambda *args: 'astra-test')
    monkeypatch.setattr(worker, 'procedure_steps', lambda *args: (STEPS, 'Product'))
    store = Store(tmp_path)
    request = store.create_request('a', 'product', 'Product', 'connect', 'Connect', 'main', 'q')
    job = store.claim_job()
    def fail(*args, **kwargs):
        raise anthropic.BadRequestError('Your credit balance is too low', response=httpx.Response(
            400, request=httpx.Request('POST', 'https://api.anthropic.com/v1/messages')), body=None)
    assert worker.process_authoring(store, job, fail) == 'failed'
    assert 'Anthropic API credits' in store.request('a', request['id'])['message']
    assert store.claim_job() is None


def test_failed_code_seed_still_requires_author_build_self_check_and_review(tmp_path):
    seed = dict(proposal=proposal(), feedback='Fix the saved build error against current evidence.')
    author, calls = author_sequence([proposal(True), proposal(), proposal(True)])
    reviews = []
    a.create_candidate(BRIEF, tmp_path, author,
                       lambda *args: reviews.append(args) or result(), builder, seed=seed)
    # A premature ready response cannot skip the new build or its self-check.
    assert len(calls) == 3
    assert calls[0][1] == seed['proposal']
    assert 'must build and view' in calls[1][2]
    assert calls[2][3]
    assert len(reviews) == 1


def test_failed_seed_is_never_a_reviewed_checkpoint(tmp_path):
    import json
    store = Store(tmp_path)
    old_work = store.root / 'work' / 'job_abc' / 'authoring'
    old_work.mkdir(parents=True)
    brief = dict(question='connect', products=['product'], view='main', steps=STEPS,
                 version='old-evidence', references=[])
    (old_work / 'brief.json').write_text(json.dumps(brief))
    (old_work / 'astra-1.json').write_text(proposal().model_dump_json())
    current = brief | {'version': 'new-evidence'}
    seed = a.failed_proposal_seed(store, {'resume_from': 'job_abc'}, current)
    assert seed['proposal'] == proposal()
    assert 'CURRENT evidence' in seed['feedback']
    assert 'reviewed' not in seed
    assert a.failed_proposal_seed(store, {'resume_from': 'job_abc'},
                                  current | {'products': ['other-product']}) is None


def test_retry_after_evidence_change_updates_request_identity(tmp_path, monkeypatch):
    monkeypatch.setattr(a, 'readiness', lambda _: None)
    monkeypatch.setattr(a, 'version_for', lambda *args: 'astra-old')
    store = Store(tmp_path)
    first = store.create_request('visitor', 'product', 'Product', 'brake', 'Brake', 'main', 'q')
    store.fail_job(first['job_id'], 'build error', retry=False)
    monkeypatch.setattr(a, 'version_for', lambda *args: 'astra-new')
    retried = store.retry_request('visitor', first['id'])
    assert retried['variant'] == 'astra-new'
    assert retried['job_id'] != first['job_id']
    assert store.job(retried['job_id'])['resume_from'] == first['job_id']
    assert store.open_request_for('visitor', 'product', 'brake', 'main', 'astra-new')['id'] == first['id']


def test_seed_survives_credit_failure_and_keeps_visual_review(tmp_path, monkeypatch):
    import json
    store = Store(tmp_path)
    brief = dict(question='brakes', products=['product'], view='main', steps=STEPS)
    for job_id in ('job_abc', 'job_def'):
        work = store.root / 'work' / job_id / 'authoring'
        work.mkdir(parents=True)
        (work / 'brief.json').write_text(json.dumps(brief))
    draft = store.root / 'work' / 'job_abc' / 'authoring'
    (draft / 'astra-1.json').write_text(proposal().model_dump_json())
    (draft / 'critic-1.json').write_text(json.dumps({'defects': ['Pedals must visibly move']}))
    monkeypatch.setattr(store, 'job', lambda job_id: {'resume_from': 'job_abc'})
    seed = a.failed_proposal_seed(store, {'resume_from': 'job_def'}, brief)
    assert seed['source_job'] == 'job_abc'
    assert 'Pedals must visibly move' in seed['feedback']
    (draft / 'astra-1.json').unlink()
    assert a.failed_proposal_seed(store, {'resume_from': 'job_def'}, brief) is None

@pytest.mark.parametrize('statuses, succeeds', [(['incomplete', 'completed'], True), (['incomplete', 'incomplete'], False), (['completed-invalid'], False)])
def test_author_saves_and_accounts_before_parsing(tmp_path, monkeypatch, statuses, succeeds):
    import json
    from types import SimpleNamespace
    import openai
    calls, settled, reserved = [], [], []
    remaining = iter(statuses)
    def create(**kwargs):
        calls.append(kwargs)
        status = next(remaining)
        usage = SimpleNamespace(input_tokens=100, output_tokens=200,
                                input_tokens_details=SimpleNamespace(cached_tokens=0),
                                model_dump=lambda: {'input_tokens': 100, 'output_tokens': 200})
        return SimpleNamespace(status=status.split('-')[0], model=a.MODEL, id=f'resp_{len(calls)}',
                               incomplete_details=SimpleNamespace(reason='max_output_tokens'), usage=usage,
                               output_text=proposal().model_dump_json() if status == 'completed' else '{"python":"cut',
                               model_dump=lambda **_: {'status': status, 'usage': usage.model_dump()})
    monkeypatch.setattr(openai, 'OpenAI', lambda **_: SimpleNamespace(responses=SimpleNamespace(
        create=create, input_tokens=SimpleNamespace(count=lambda **_: SimpleNamespace(input_tokens=100)))))
    budget = SimpleNamespace(reserve=lambda *args: reserved.append(args) or len(reserved),
                             settle=lambda *args: settled.append(args))
    author = a.Astra(budget, 'job', tmp_path)
    if succeeds:
        assert author({'references': [], 'steps': STEPS}) == proposal()
        assert [c['max_output_tokens'] for c in calls] == [20000, 30000]
    else:
        with pytest.raises(a.AuthoringError, match='response'):
            author({'references': [], 'steps': STEPS})
    assert all(c['background'] is True and c['store'] is False for c in calls)
    assert len(calls) == len(settled) == len(reserved) == len(statuses)
    assert len(json.loads((tmp_path / 'astra-usage.json').read_text())) == len(statuses)
    assert len(list(tmp_path.glob('astra-*-response.json'))) == len(statuses)


def test_fit_review_cannot_pass_without_visual_checks():
    brief = dict(BRIEF, fit={'object': {}})
    with pytest.raises(a.AuthoringError, match='omitted required'):
        a.actionable_defects(result(), brief, [(0, Path('frame.png'))])


def test_fit_review_requires_grounded_readability_and_layout_checks():
    brief = dict(BRIEF, fit={'object': {}})
    checks = [a.VisualCheck(criterion=k, passed=True, reference_id='manual:p3', seconds=0,
                            observation='Visible comparison to supplied reference') for k in sorted(a.FIT_VISUAL_CRITERIA)]
    review = result().model_copy(update={'visual_checks': checks})
    assert a.actionable_defects(review, brief, [(0, Path('frame.png'))]) == []
    checks[0].passed = False
    with pytest.raises(a.AuthoringError, match='failed without'):
        a.actionable_defects(review, brief, [(0, Path('frame.png'))])

@pytest.mark.parametrize('phase', ['token_count', 'scene_generation'])
@pytest.mark.parametrize('timeout_type', ['ConnectTimeout', 'ReadTimeout', 'WriteTimeout', 'PoolTimeout'])
def test_author_timeout_diagnostics(tmp_path, monkeypatch, phase, timeout_type):
    import json
    import httpx
    import openai
    from types import SimpleNamespace
    reserved, settled = [], []
    def fail(**kwargs):
        try:
            raise getattr(httpx, timeout_type)('secret-payload-must-not-be-logged')
        except httpx.TimeoutException as cause:
            raise openai.APITimeoutError(request=httpx.Request('POST', 'https://api.openai.com/v1/responses')) from cause
    count = fail if phase == 'token_count' else lambda **_: SimpleNamespace(input_tokens=100)
    monkeypatch.setattr(openai, 'OpenAI', lambda **_: SimpleNamespace(responses=SimpleNamespace(
        create=fail, input_tokens=SimpleNamespace(count=count))))
    budget = SimpleNamespace(reserve=lambda *args: reserved.append(args) or 'reservation',
                             settle=lambda *args: settled.append(args))
    with pytest.raises(openai.APITimeoutError):
        a.Astra(budget, 'test-job', tmp_path)({'references': [], 'steps': STEPS})
    raw = (tmp_path / f'astra-1-{phase}-diagnostics.json').read_text()
    record = json.loads(raw)
    assert record['phase'] == phase and record['status'] == 'failed'
    assert record['timeout_kind'] == timeout_type
    assert record['elapsed_seconds'] >= 0
    assert record['exception_chain'][0]['type'] == 'APITimeoutError'
    assert record['exception_chain'][0]['traceback']
    assert 'secret-payload' not in raw
    assert len(reserved) == (phase == 'scene_generation')
    assert not settled  # A timeout does not prove the provider charged nothing.


def test_api_diagnostics_records_request_id(tmp_path):
    import httpx
    import openai
    import json
    response = httpx.Response(429, headers={'x-request-id': 'req_test'},
                              request=httpx.Request('POST', 'https://api.openai.com/v1/responses'))
    with pytest.raises(openai.RateLimitError):
        with a.api_diagnostics(tmp_path / 'astra-1', 'scene_generation', 'job'):
            raise openai.RateLimitError('private message', response=response, body=None)
    data = json.loads((tmp_path / 'astra-1-scene_generation-diagnostics.json').read_text())
    assert data['request_id'] == 'req_test'
    assert data['status_code'] == 429


def test_seed_crosses_setup_failure_without_brief(tmp_path, monkeypatch):
    import json
    store = Store(tmp_path)
    brief = dict(question='brakes', products=['product'], view='main', steps=STEPS)
    draft = store.root / 'work' / 'job_abc' / 'authoring'
    draft.mkdir(parents=True)
    (draft / 'brief.json').write_text(json.dumps(brief))
    (draft / 'astra-1.json').write_text(proposal().model_dump_json())
    monkeypatch.setattr(store, 'job', lambda jid: {'resume_from': 'job_abc'} if jid == 'job_def' else None)
    seed = a.failed_proposal_seed(store, {'resume_from': 'job_def'}, brief)
    assert seed['source_job'] == 'job_abc'
    assert a.failed_proposal_seed(store, {'resume_from': 'job_def'}, dict(brief, question='different')) is None
    monkeypatch.setattr(store, 'job', lambda jid: {'resume_from': 'job_def'})
    assert a.failed_proposal_seed(store, {'resume_from': 'job_def'}, brief) is None


def test_background_poll_reuses_id_after_timeout(tmp_path, monkeypatch):
    import json, httpx, openai
    from types import SimpleNamespace
    monkeypatch.setattr(a.time, 'sleep', lambda _: None)
    ids = []
    def retrieve(response_id):
        saved = json.loads((tmp_path / 'astra-1-background.json').read_text())
        assert saved['response_id'] == response_id == 'resp_one'
        ids.append(response_id)
        if len(ids) == 1:
            raise openai.APITimeoutError(request=httpx.Request('GET', 'https://api.openai.com'))
        return SimpleNamespace(id=response_id, status='completed')
    client = SimpleNamespace(responses=SimpleNamespace(retrieve=retrieve))
    result = a.await_background_response(client, SimpleNamespace(id='resp_one', status='queued'),
                                          tmp_path / 'astra-1', 'job', 'reservation')
    assert result.status == 'completed'
    assert ids == ['resp_one', 'resp_one']


def test_background_poll_deadline_cancels(tmp_path, monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(a, 'BACKGROUND_TIMEOUT', 0)
    calls = []
    def cancel(rid):
        calls.append(rid)
        return SimpleNamespace(id=rid, status='cancelled')
    client = SimpleNamespace(responses=SimpleNamespace(cancel=cancel))
    result = a.await_background_response(client, SimpleNamespace(id='resp_one', status='queued'),
                                          tmp_path / 'astra-1', 'job', 'reservation')
    assert result.status == 'cancelled' and calls == ['resp_one']


def test_background_poll_failures_are_bounded(tmp_path, monkeypatch):
    import httpx, openai, json
    from types import SimpleNamespace
    monkeypatch.setattr(a.time, 'sleep', lambda _: None)
    calls = []
    def retrieve(rid):
        calls.append(rid)
        raise openai.APITimeoutError(request=httpx.Request('GET', 'https://api.openai.com'))
    client = SimpleNamespace(responses=SimpleNamespace(retrieve=retrieve))
    with pytest.raises(openai.APITimeoutError):
        a.await_background_response(client, SimpleNamespace(id='resp_one', status='queued'),
                                    tmp_path / 'astra-1', 'job', 'reservation')
    assert calls == ['resp_one'] * 3
    assert json.loads((tmp_path / 'astra-1-background.json').read_text())['response_id'] == 'resp_one'


def test_ready_contract_ignores_only_coverage_explanation():
    before = proposal()
    after = before.model_copy(deep=True)
    after.coverage[0].explanation = 'Same animation, reworded description.'
    assert a.ready_contract(before) == a.ready_contract(after)
    after.coverage[0].end_frame += 1
    assert a.ready_contract(before) != a.ready_contract(after)
