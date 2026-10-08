"""Saved video requests, the render worker lifecycle and answer video decisions."""
import json
import threading
import urllib.request

import pytest

from app import worker
from app.pipeline import scenes, service
from app.pipeline.store import Store

R2J = "graco-ready2jet-2212125"
FOLD = "fold_stroller"


@pytest.fixture(autouse=True)
def legacy_generation_route(monkeypatch):
    """Keep exercising the opt-in Seedance path; Astra has its own suite."""
    monkeypatch.setenv("SHOWME_VIDEO_PIPELINE", "seedance")


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "data")


def fake_pipeline(monkeypatch, tmp_path, fail=None):
    """Replace Blender/ffmpeg/ffprobe with instant fakes."""
    def renderer(job, scene, view, frames_dir, on_progress):
        if fail:
            raise fail
        on_progress(1.0)

    def encode(frames_dir, scene, out_dir):
        (out_dir / "video.mp4").write_bytes(b"mp4")
        (out_dir / "poster.jpg").write_bytes(b"jpg")
        return out_dir / "video.mp4", out_dir / "poster.jpg"

    monkeypatch.setattr(worker, "encode", encode)
    monkeypatch.setattr(worker, "check_video", lambda video, scene: 8.04)
    return renderer


def test_request_with_scene_queues_one_shared_job(store):
    first = store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller", "side", "q")
    again = store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller", "side", "q")
    other = store.create_request("v_b", R2J, "Graco Ready2Jet", FOLD, "Fold stroller", "side", "q")
    assert first["state"] == "queued" and first["job_id"]
    assert again["id"] == first["id"]
    assert other["id"] != first["id"] and other["job_id"] == first["job_id"]


def no_budget(monkeypatch, tmp_path):
    from app.pipeline import generative
    monkeypatch.setattr(generative, "BUDGET_MANIFEST", tmp_path / "missing.json")
    monkeypatch.setattr(generative.Budget, "providers_ready", staticmethod(lambda: True))


def test_request_without_scene_or_budget_is_recorded_not_promised(store, monkeypatch, tmp_path):
    no_budget(monkeypatch, tmp_path)
    row = store.create_request("v_a", "bose-qc-ultra-headphones", "Bose QC Ultra",
                               "bluetooth_pairing", "Bluetooth pairing", "main", "q")
    assert row["state"] == "needs_scene" and row["job_id"] is None
    assert "budget" in row["message"]
    assert store.claim_job() is None


def test_worker_publishes_asset_and_marks_request_unread(store, monkeypatch, tmp_path):
    monkeypatch.setenv("SHOWME_SERVE_RESEARCH_MEDIA", "1")
    request = store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller",
                                   "side", "q")
    job = store.claim_job()
    assert store.request("v_a", request["id"])["state"] == "rendering"
    assert worker.process_job(store, job, fake_pipeline(monkeypatch, tmp_path)) == "succeeded"
    done = store.request("v_a", request["id"])
    assert done["state"] == "ready" and done["seen"] == 0 and done["asset_id"]
    assert "side" in store.assets_for(R2J, FOLD)


def test_research_render_waits_for_review_when_not_allowed(store, monkeypatch, tmp_path):
    request = store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller",
                                   "front", "q")
    worker.process_job(store, store.claim_job(), fake_pipeline(monkeypatch, tmp_path))
    assert store.request("v_a", request["id"])["state"] == "needs_review"
    assert store.assets_for(R2J, FOLD) == {}


def test_transient_failure_retries_then_fails_with_message(store, monkeypatch, tmp_path):
    request = store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller",
                                   "side", "q")
    renderer = fake_pipeline(monkeypatch, tmp_path,
                             fail=worker.RenderError("crash", transient=True))
    assert worker.process_job(store, store.claim_job(), renderer) == "queued"
    assert worker.process_job(store, store.claim_job(), renderer) == "failed"
    failed = store.request("v_a", request["id"])
    assert failed["state"] == "failed" and "couldn't make" in failed["message"]
    retried = store.retry_request("v_a", request["id"])
    assert retried["state"] == "queued"


def test_restart_recovers_interrupted_job(store):
    store.create_request("v_a", R2J, "Graco Ready2Jet", FOLD, "Fold stroller", "side", "q")
    job = store.claim_job()
    reopened = Store(store.root)
    assert reopened.recover_jobs() == 1
    assert reopened.job(job["id"])["state"] == "queued"


def test_second_worker_is_refused(store):
    first = worker.acquire_lock(store)
    try:
        assert first is not None
        assert worker.acquire_lock(store) is None
    finally:
        first.close()


def fold_document(visual_requested=False, kind="procedure"):
    return {"status": "ready", "product": {"product_dir": R2J, "name": "Graco Ready2Jet"},
            "coverage": {"procedure_id": FOLD}, "headline": "Fold stroller — Graco Ready2Jet",
            "visual": {"requested": visual_requested}, "interpretation": {"kind": kind}}


def test_prerendered_clip_plays_immediately(store, monkeypatch):
    monkeypatch.setenv("SHOWME_SERVE_RESEARCH_MEDIA", "1")
    store.import_scene_assets()
    video = service.video_for_document(store, fold_document(), "How do I fold it?", "v_a")
    assert video["state"] == "ready"
    assert [a["view"] for a in video["assets"]][:2] == ["main", "rear"]
    assert video["assets"][0]["chapters"]["claim_r2j_step_fold_4"] == 1.75


def test_new_view_request_is_saved_and_queued(store, monkeypatch):
    monkeypatch.setenv("SHOWME_SERVE_RESEARCH_MEDIA", "1")
    store.import_scene_assets()
    video = service.video_for_document(store, fold_document(True, "view"),
                                       "Show it from the side", "v_a")
    assert video["state"] == "requested"
    assert video["request"]["view"] == "side" and video["request"]["state"] == "queued"


def test_facts_and_unrequested_misses_queue_nothing(store, monkeypatch, tmp_path):
    no_budget(monkeypatch, tmp_path)
    fact = {"status": "ready", "product": {"product_dir": R2J}, "coverage": None}
    assert service.video_for_document(store, fact, "How much does it weigh?", "v_a") is None
    offer = service.video_for_document(store, fold_document(), "How do I fold it?", "v_a")
    assert offer["state"] == "offer"
    assert store.claim_job() is None


def test_plain_website_question_queues_once_and_resumes_saved_work(store):
    first = service.video_for_document(store, fold_document(), 'How do I fold it?',
                                       'v_a', auto_generate=True)
    assert first['state'] == 'requested'
    request_id = first['request']['id']
    first_job = store.request('v_a', request_id)['job_id']
    assert first_job
    again = service.video_for_document(store, fold_document(), 'How do I fold it?',
                                       'v_a', auto_generate=True)
    assert again['request']['id'] == request_id
    assert store.request('v_a', request_id)['job_id'] == first_job
    store.fail_job(first_job, 'recoverable build failure', retry=False)
    retried = service.video_for_document(store, fold_document(), 'How do I fold it?',
                                         'v_a', auto_generate=True)
    assert retried['request']['id'] == request_id
    next_job = store.request('v_a', request_id)['job_id']
    assert next_job != first_job
    assert store.job(next_job)['resume_from'] == first_job


def test_automatic_generation_does_not_invent_a_procedure(store):
    fact = {'status': 'ready', 'product': {'product_dir': R2J}, 'coverage': None}
    assert service.video_for_document(store, fact, 'How heavy is it?', 'v_a',
                                      auto_generate=True) is None
    assert store.claim_job() is None


def test_my_videos_are_private_to_the_visitor(monkeypatch):
    from app.server import create_server
    monkeypatch.setenv("SHOWME_SERVE_RESEARCH_MEDIA", "1")
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        def call(path, cookie=None, body=None):
            request = urllib.request.Request(base + path, data=body and json.dumps(body).encode(),
                                             headers={"Cookie": cookie or "",
                                                      "Content-Type": "application/json"})
            with urllib.request.urlopen(request) as response:
                return response.headers.get("Set-Cookie"), json.loads(response.read())

        set_cookie, _ = call("/api/my-videos")
        mine = set_cookie.split(";")[0]
        _, created = call("/api/video-requests", mine,
                          {"product_dir": R2J, "procedure_id": FOLD, "view": "side",
                           "question": "Show the fold from the side"})
        assert created["request"]["state"] == "queued"
        _, listed = call("/api/my-videos", mine)
        assert [r["id"] for r in listed["requests"]] == [created["request"]["id"]]
        _, stranger = call("/api/my-videos", "showme_visitor=v_" + "0" * 24)
        assert stranger["requests"] == []
    finally:
        server.shutdown()
        server.server_close()


def test_every_scene_view_names_a_camera():
    for scene in scenes.SCENES.values():
        for view in scene["views"].values():
            assert view["camera"].startswith("Camera_")


# ---- automatic generation (no 3D scene) ------------------------------

def budget_manifest(monkeypatch, tmp_path, per_video=1.5, total=6.0):
    from app.pipeline import generative
    from system import spend_guard
    manifest = {"run_id": "test_budget", "category": "video_generation", "purpose": "t",
                "provider": "fal.ai", "model": "m", "inputs": {}, "max_calls": 10,
                "cap_usd": total, "per_video_cap_usd": per_video, "retry_policy": "none"}
    path = tmp_path / "budget.json"
    path.write_text(json.dumps(manifest))
    approvals, ledger = tmp_path / "approvals.jsonl", tmp_path / "ledger.jsonl"
    monkeypatch.setattr(generative, "BUDGET_MANIFEST", path)
    monkeypatch.setattr(spend_guard, "DEFAULT_APPROVALS", approvals)
    monkeypatch.setattr(spend_guard, "DEFAULT_LEDGER", ledger)
    spend_guard.record_owner_approval(manifest, "test owner", approvals_path=approvals)
    monkeypatch.setattr(generative.Budget, "providers_ready", staticmethod(lambda: True))


def test_request_without_scene_queues_generation_within_budget(store, monkeypatch, tmp_path):
    budget_manifest(monkeypatch, tmp_path)
    row = store.create_request("v_a", "bose-qc-ultra-headphones", "Bose QC Ultra",
                               "connect_aux_cable", "Connect AUX cable", "main", "q")
    assert row["state"] == "queued"
    job = store.claim_job()
    assert job["kind"] == "generate"


def test_generation_job_publishes_and_never_auto_retries(store, monkeypatch, tmp_path):
    from app.pipeline import generative
    monkeypatch.setenv("SHOWME_SERVE_RESEARCH_MEDIA", "1")
    budget_manifest(monkeypatch, tmp_path)
    request = store.create_request("v_a", "bose-qc-ultra-headphones", "Bose QC Ultra",
                                   "connect_aux_cable", "Connect AUX cable", "main", "q")
    job = store.claim_job()

    def fake_generate(store_, job_, out_dir, packs_root, steps, name, question="", **kwargs):
        assert [s["claim_id"] for s in steps] == ["claim_bqcu2_step_aux_1",
                                                  "claim_bqcu2_step_aux_2"]
        (out_dir / "video.mp4").write_bytes(b"x")
        (out_dir / "poster.jpg").write_bytes(b"x")
        return out_dir / "video.mp4", out_dir / "poster.jpg", {"claim_bqcu2_step_aux_2": 4.0}, {}

    monkeypatch.setattr(worker.subprocess, "run",
                        lambda *a, **k: type("R", (), {"stdout": "8.0"})())
    assert worker.process_generation(store, job, fake_generate) == "succeeded"
    assert store.request("v_a", request["id"])["state"] == "ready"

    again = store.create_request("v_b", "bose-qc-ultra-headphones", "Bose QC Ultra",
                                 "connect_usb_audio", "Connect USB audio", "main", "q")
    failing = store.claim_job()
    boom = lambda *a: (_ for _ in ()).throw(generative.BudgetExceeded("cap"))  # noqa: E731
    assert worker.process_generation(store, failing, boom) == "failed"
    assert store.request("v_b", again["id"])["state"] == "failed"


def test_budget_refuses_calls_past_the_caps(store, monkeypatch, tmp_path):
    from app.pipeline import generative
    budget_manifest(monkeypatch, tmp_path, per_video=1.0, total=1.2)
    budget = generative.Budget(store)
    budget.reserve("job_a", "seedance", 0.96)
    with pytest.raises(generative.BudgetExceeded, match="per-video"):
        budget.reserve("job_a", "image", 0.15)
    with pytest.raises(generative.BudgetExceeded, match="total"):
        budget.reserve("job_b", "seedance", 0.96)
    assert not budget.can_start_video()




# ---- Claude director + critic -------------------------------------------

BOSE = "bose-qc-ultra-headphones"
MAC = "apple-macbook-air-13-m3"
AUX_STEPS = [
    {"claim_id": "claim_bqcu2_step_aux_1", "text": "Connect the cable to the 2.5 mm port on the left earcup.",
     "parts": ["aux_audio_port"], "quote": "q1"},
    {"claim_id": "claim_bqcu2_step_aux_2", "text": "Connect the other end to the 3.5 mm port on the source device.",
     "parts": [], "quote": "q2"},
]


def test_question_naming_a_mac_brings_in_the_macbook():
    from app.pipeline import director, generative
    assert director.mentioned_products("How to connect QuietComfort to Mac using the cable", BOSE) == [MAC]
    assert director.mentioned_products("How do I connect the aux cable?", BOSE) == []
    assert generative.version_for("connect to my mac", BOSE).endswith("+" + MAC)


def shot(ids, device, photo, strategy="forward_from_before_photo", crop=()):
    from app.pipeline import director
    return director.Shot(step_claim_ids=ids, device_product_dir=device, photo_id=photo,
                         crop=list(crop), strategy=strategy, motion_prompt="m",
                         must_be_visible=["x"])


def test_plan_that_drops_the_mac_step_is_rejected_before_spending():
    from app.pipeline import director
    plan = director.ShotPlan(devices_involved=[BOSE], notes="",
                             shots=[shot(["claim_bqcu2_step_aux_1"], BOSE, "src_img_black_controls")],
                             not_shown=[])
    with pytest.raises(director.PlanRejected, match="drops steps"):
        director.validate_plan(plan, AUX_STEPS, BOSE, [MAC])


def test_plan_may_only_use_official_photos_of_named_products():
    from app.pipeline import director
    bad_photo = director.ShotPlan(devices_involved=[], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1", "claim_bqcu2_step_aux_2"], BOSE, "made_up_photo")])
    with pytest.raises(director.PlanRejected, match="not an official photo"):
        director.validate_plan(bad_photo, AUX_STEPS, BOSE, [MAC])
    other_product = director.ShotPlan(devices_involved=[], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1", "claim_bqcu2_step_aux_2"], "levoit-core-300s", "x")])
    with pytest.raises(director.PlanRejected, match="not in the question"):
        director.validate_plan(other_product, AUX_STEPS, BOSE, [MAC])


def test_valid_two_device_plan_passes():
    from app.pipeline import director
    plan = director.ShotPlan(devices_involved=[BOSE, MAC], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1"], BOSE, "src_img_black_controls", "reverse_from_after_photo",
             crop=(0, 100, 1500, 1000)),
        shot(["claim_bqcu2_step_aux_2"], MAC, "src_img_store_open_side_profiles",
             crop=(560, 1200, 1240, 1583))])
    assert director.validate_plan(plan, AUX_STEPS, BOSE, [MAC]) is plan


def test_thin_strip_crops_are_rejected():
    from app.pipeline import director
    plan = director.ShotPlan(devices_involved=[], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1", "claim_bqcu2_step_aux_2"], MAC,
             "src_img_store_open_side_profiles", crop=(100, 1400, 1300, 1600))])
    with pytest.raises(director.PlanRejected, match="16:9"):
        director.validate_plan(plan, AUX_STEPS, BOSE, [MAC])


def test_director_gets_the_manual_pages_its_steps_cite():
    from app.worker import procedure_steps
    from app.pipeline import director
    steps, _ = procedure_steps(BOSE, "connect_aux_cable")
    pages = {(s, p) for s, p, _ in director.manual_page_images(BOSE, steps)}
    assert ("src_owners_guide_en", 33) in pages and ("src_owners_guide_en", 13) in pages


def test_filter_video_includes_referenced_reset_page_and_conditional_instructions():
    from app.worker import procedure_steps
    from app.pipeline import director
    steps, _ = procedure_steps("levoit-core-300s", "replace_filter")
    reset = steps[-1]
    assert len(steps) == 6
    assert reset["claim_id"] == "claim_c300s_step_replace_filter_6"
    assert {p["procedure_id"] for p in reset["supporting_procedures"]} == {
        "reset_check_filter_indicator", "reset_check_filter_indicator_early"}
    instructions = [s for p in reset["supporting_procedures"] for s in p["steps"]]
    assert all(s["condition"] and s["quotes"] for s in instructions)
    assert any("3 seconds" in s["text"] and "Sleep Mode" in s["text"] for s in instructions)
    pages = {(s, p) for s, p, _ in director.manual_page_images("levoit-core-300s", steps)}
    assert ("src_manual_core300sp_us", 13) in pages
    assert ("src_manual_core300sp_us", 14) in pages


def test_required_video_manual_pages_are_never_silently_truncated(monkeypatch):
    from app.pipeline import director
    monkeypatch.setattr(director, "MAX_MANUAL_PAGES", 1)
    steps = [{"required_manual_pages": [("src_owners_guide_en", 13), ("src_owners_guide_en", 33)]}]
    with pytest.raises(ValueError, match="Required manual evidence exceeds"):
        director.manual_page_images(BOSE, steps)


def test_required_video_manual_reference_must_exist():
    from app.pipeline import director
    with pytest.raises(ValueError, match="Required manual reference is unavailable"):
        director.manual_page_images(BOSE, [{"required_manual_pages": [("not-a-source", 1)]}])


def test_critic_pass_is_rechecked_against_every_claimed_step():
    from app.pipeline import director
    plan = director.ShotPlan(devices_involved=[], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1"], BOSE, "p"), shot(["claim_bqcu2_step_aux_2"], MAC, "p")])
    lenient = director.Critique(answers_the_question=True, devices_correct=True,
                                invented_or_wrong=[], verdict="pass", fix_notes="",
                                steps=[director.StepVerdict(claim_id="claim_bqcu2_step_aux_1",
                                                            shown=True, evidence="")],
                                shots=[director.ShotVerdict(shot=i, approved=True, issues=[])
                                       for i in (1, 2)])
    assert any("not visible" in p for p in director.accept(lenient, plan))


def test_generate_replans_once_from_critic_notes_then_publishes(store, monkeypatch, tmp_path):
    from app.pipeline import director, generative
    budget_manifest(monkeypatch, tmp_path)
    monkeypatch.setattr(generative, "load_provider_key", lambda: True)
    monkeypatch.setattr(director, "claude_client", lambda: object())
    good = director.ShotPlan(devices_involved=[BOSE, MAC], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1"], BOSE, "src_img_black_controls", "reverse_from_after_photo"),
        shot(["claim_bqcu2_step_aux_2"], MAC, "src_img_store_open_side_profiles")])
    calls = {"plan": 0, "review": 0}

    def plan_shots(client, budget, job_id, question, product, steps, devices, critique=None,
                   approved=()):
        calls["plan"] += 1
        budget.reserve(job_id, "director", 0.01)
        assert devices == [MAC] and (critique is None) == (calls["plan"] == 1)
        return good, {}

    def review_video(client, budget, job_id, question, steps, plan, frames, durations, product_dir):
        calls["review"] += 1
        budget.reserve(job_id, "critic", 0.01)
        ok = calls["review"] > 1
        # Round 1: the earcup step is VISIBLE but the shot invents a hole -> not approved.
        return director.Critique(
            answers_the_question=ok, devices_correct=True, invented_or_wrong=[],
            verdict="pass" if ok else "fail", fix_notes="fix the earcup port",
            steps=[director.StepVerdict(claim_id="claim_bqcu2_step_aux_1", shown=True, evidence=""),
                   director.StepVerdict(claim_id="claim_bqcu2_step_aux_2", shown=True, evidence="")],
            shots=[director.ShotVerdict(shot=1, approved=ok, issues=[] if ok else ["extra hole"]),
                   director.ShotVerdict(shot=2, approved=True, issues=[])]), {}

    monkeypatch.setattr(director, "plan_shots", plan_shots)
    monkeypatch.setattr(director, "review_video", review_video)
    monkeypatch.setattr(director, "validate_plan", lambda plan, *a: plan)
    approve = director.PlanCheck(shots=[director.ShotCheck(shot=i, part_in_frame=True,
                                                           state_matches_strategy=True,
                                                           motion_matches_manual=True, issues=[])
                                         for i in (1, 2)],
                                 covers_the_question=True, approve=True, fix_notes="")
    monkeypatch.setattr(director, "preflight_plan", lambda *a: (approve, {}))
    generated = []

    def fake_shot(store_, shot_dir, fal, s):
        generated.append(tuple(s.step_claim_ids))
        shot_dir.mkdir(parents=True, exist_ok=True)
        (shot_dir / "clip.mp4").write_bytes(b"x")
        return shot_dir / "clip.mp4"

    def fake_stitch(parts, output, work):
        output.write_bytes(b"video")
        return [4.0] * len(parts)

    monkeypatch.setattr(generative, "MeteredFal", lambda budget, job_id: None)
    monkeypatch.setattr(generative, "execute_shot", fake_shot)
    monkeypatch.setattr(generative, "stitch", fake_stitch)
    monkeypatch.setattr(generative, "review_frames", lambda video, out: [])
    monkeypatch.setattr(generative.subprocess, "run", lambda *a, **k: None)
    job = {"id": "job_x", "product_dir": BOSE, "procedure_id": "connect_aux_cable",
           "scene_version": generative.version_for("connect to Mac", BOSE)}
    out = tmp_path / "out"
    out.mkdir()
    video, poster, chapters, prov = generative.generate(
        store, job, out, None, AUX_STEPS, "Bose QC Ultra", question="connect to Mac")
    assert calls == {"plan": 2, "review": 2}
    # The Mac shot passed review in round 1, so it is not paid for again in round 2.
    assert generated == [("claim_bqcu2_step_aux_1",), ("claim_bqcu2_step_aux_2",),
                         ("claim_bqcu2_step_aux_1",)]
    assert chapters == {"claim_bqcu2_step_aux_1": 0.0, "claim_bqcu2_step_aux_2": 4.0}
    assert prov["devices"] == [MAC]
    # Both approved shots are now in the durable library for any later request.
    library = store.library_shots(BOSE, "connect_aux_cable", f"{generative.TIER}-{generative.RESOLUTION}")
    assert set(library) == {frozenset({"claim_bqcu2_step_aux_1"}), frozenset({"claim_bqcu2_step_aux_2"})}


def test_no_video_is_promised_without_provider_keys(store, monkeypatch, tmp_path):
    from app.pipeline import generative
    budget_manifest(monkeypatch, tmp_path)
    monkeypatch.setattr(generative.Budget, "providers_ready", staticmethod(lambda: False))
    row = store.create_request("v_a", BOSE, "Bose QC Ultra", "connect_aux_cable",
                               "Connect AUX cable", "main", "connect to Mac")
    assert row["state"] == "needs_scene" and "isn't set up" in row["message"]


def test_no_generation_money_is_spent_on_a_plan_that_fails_preflight(store, monkeypatch, tmp_path):
    from app.pipeline import director, generative
    budget_manifest(monkeypatch, tmp_path)
    monkeypatch.setattr(generative, "load_provider_key", lambda: True)
    monkeypatch.setattr(director, "claude_client", lambda: object())
    plan = director.ShotPlan(devices_involved=[], notes="", not_shown=[], shots=[
        shot(["claim_bqcu2_step_aux_1", "claim_bqcu2_step_aux_2"], BOSE, "p")])
    monkeypatch.setattr(director, "plan_shots", lambda *a, **k: (plan, {}))
    monkeypatch.setattr(director, "validate_plan", lambda plan, *a: plan)
    reject = director.PlanCheck(shots=[director.ShotCheck(shot=1, part_in_frame=False,
                                                          state_matches_strategy=True,
                                                          motion_matches_manual=True,
                                                          issues=["port not in frame"])],
                                covers_the_question=True, approve=False, fix_notes="crop lower")
    monkeypatch.setattr(director, "preflight_plan", lambda *a: (reject, {}))
    monkeypatch.setattr(generative, "MeteredFal", lambda budget, job_id: None)
    spent = []
    monkeypatch.setattr(generative, "execute_shot", lambda *a: spent.append(1))
    job = {"id": "job_y", "product_dir": BOSE, "procedure_id": "connect_aux_cable",
           "scene_version": "gen-v3q"}
    out = tmp_path / "o"
    out.mkdir()
    with pytest.raises(RuntimeError, match="preflight"):
        generative.generate(store, job, out, None, AUX_STEPS, "Bose", question="q")
    assert spent == []


def test_reviewed_shots_skip_preflight_and_cleared_shots_stay_locked(store, monkeypatch, tmp_path):
    from app.pipeline import director, generative
    budget_manifest(monkeypatch, tmp_path)
    monkeypatch.setattr(generative, "load_provider_key", lambda: True)
    monkeypatch.setattr(director, "claude_client", lambda: object())
    quality = f"{generative.TIER}-{generative.RESOLUTION}"
    clip = tmp_path / "mac.mp4"
    clip.write_bytes(b"x")
    mac = shot(["claim_bqcu2_step_aux_2"], MAC, "src_img_store_closed_side_ports")
    store.add_library_shot(BOSE, "connect_aux_cable", ["claim_bqcu2_step_aux_2"], MAC, quality,
                           clip, mac.model_dump(), "[]", "job_old")
    good_ear = shot(["claim_bqcu2_step_aux_1"], BOSE, "src_img_black_controls", crop=(0, 0, 900, 600))
    bad_ear = shot(["claim_bqcu2_step_aux_1"], BOSE, "src_img_black_controls", crop=(1, 1, 901, 601))
    plans = iter([good_ear, bad_ear])
    checked = []

    def plan_shots(*a, **k):
        different_mac = shot(["claim_bqcu2_step_aux_2"], MAC, "src_img_store_open_side_profiles")
        return director.ShotPlan(devices_involved=[], notes="", not_shown=[],
                                 shots=[next(plans), different_mac]), {}

    def preflight(client, budget, job_id, question, steps, plan, product_dir):
        checked.append([s.step_claim_ids for s in plan.shots])
        ok = len(checked) > 1
        return director.PlanCheck(shots=[director.ShotCheck(shot=1, part_in_frame=True,
                                                            state_matches_strategy=True,
                                                            motion_matches_manual=True, issues=[])],
                                  covers_the_question=True, approve=ok, fix_notes="n"), {}

    monkeypatch.setattr(director, "plan_shots", plan_shots)
    monkeypatch.setattr(director, "validate_plan", lambda plan, *a: plan)
    monkeypatch.setattr(director, "preflight_plan", preflight)
    monkeypatch.setattr(director, "review_video", lambda *a: (director.Critique(
        answers_the_question=True, devices_correct=True, invented_or_wrong=[], verdict="pass",
        fix_notes="", steps=[director.StepVerdict(claim_id=c, shown=True, evidence="")
                             for c in ("claim_bqcu2_step_aux_1", "claim_bqcu2_step_aux_2")],
        shots=[director.ShotVerdict(shot=i, approved=True, issues=[]) for i in (1, 2)]), {}))
    used = []

    def fake_shot(store_, shot_dir, fal, s):
        used.append(tuple(s.crop))
        shot_dir.mkdir(parents=True, exist_ok=True)
        (shot_dir / "clip.mp4").write_bytes(b"x")
        return shot_dir / "clip.mp4"

    monkeypatch.setattr(generative, "MeteredFal", lambda budget, job_id: None)
    monkeypatch.setattr(generative, "execute_shot", fake_shot)
    monkeypatch.setattr(generative, "stitch", lambda parts, output, work: (output.write_bytes(b"v"), [4.0] * len(parts))[1])
    monkeypatch.setattr(generative, "review_frames", lambda video, out: [])
    monkeypatch.setattr(generative.subprocess, "run", lambda *a, **k: None)
    job = {"id": "job_z", "product_dir": BOSE, "procedure_id": "connect_aux_cable",
           "scene_version": generative.version_for("connect to Mac", BOSE)}
    out = tmp_path / "o"
    out.mkdir()
    generative.generate(store, job, out, None, AUX_STEPS, "Bose", question="connect to Mac")
    # Only the earcup shot is ever pre-flighted; the reviewed Mac clip is never re-judged.
    assert checked == [[["claim_bqcu2_step_aux_1"]], [["claim_bqcu2_step_aux_1"]]]
    # The earcup shot that passed preflight stayed locked; only one clip was generated.
    assert used == [(0, 0, 900, 600)]


def test_persisted_local_setting_reuses_existing_fold_video(store, monkeypatch, tmp_path):
    from app.pipeline.config import load_local_settings
    config = tmp_path / '.env'
    config.write_text('SHOWME_SERVE_RESEARCH_MEDIA=1\n')
    load_local_settings(config)
    store.import_scene_assets()
    video = service.video_for_document(store, fold_document(),
                                      'How do I fold Ready2Jet stroller', 'v_local')
    assert video['state'] == 'ready'
    assert video['assets'][0]['view'] == 'main'
    assert 'offer' not in video
    assert store.claim_job() is None
    # An explicit environment choice still overrides the local configuration.
    monkeypatch.setenv('SHOWME_SERVE_RESEARCH_MEDIA', '0')
    load_local_settings(config)
    assert not store.assets_for(R2J, FOLD)


def test_shared_failed_job_retry_updates_all_visitors(store):
    first = store.create_request('v_a', R2J, 'Ready2Jet', FOLD, 'Fold', 'side', 'q')
    second = store.create_request('v_b', R2J, 'Ready2Jet', FOLD, 'Fold', 'side', 'q')
    unrelated = store.create_request('v_c', R2J, 'Ready2Jet', FOLD, 'Fold', 'front', 'q')
    assert first['job_id'] == second['job_id']
    store.fail_job(first['job_id'], 'truncated', retry=False)
    retried = store.retry_request('v_b', second['id'])
    original = store.request('v_a', first['id'])
    assert original['job_id'] == retried['job_id'] != first['job_id']
    assert original['state'] == 'queued' and original['message'] is None
    store.update_job_stage(retried['job_id'], 'refining', .1)
    assert store.request('v_a', first['id'])['state'] == 'rendering'
    assert store.request('v_c', unrelated['id'])['job_id'] == unrelated['job_id']
    assert store.request('v_a', second['id']) is None

@pytest.mark.parametrize('until, expected', [('2099-10-08T00:00:00-07:00', 10.0), ('2000-10-08T00:00:00-07:00', 5.0)])
def test_temporary_video_cap_expires(store, monkeypatch, tmp_path, until, expected):
    import json
    from app.pipeline import generative
    from system import spend_guard
    budget_manifest(monkeypatch, tmp_path)
    path = generative.BUDGET_MANIFEST
    manifest = json.loads(path.read_text())
    manifest.update(per_video_cap_usd=10.0, temporary_per_video_until=until,
                    per_video_cap_after_expiry_usd=5.0)
    path.write_text(json.dumps(manifest))
    spend_guard.record_owner_approval(manifest, 'test owner', approvals_path=spend_guard.DEFAULT_APPROVALS)
    assert generative.Budget(store).config['per_video'] == expected
