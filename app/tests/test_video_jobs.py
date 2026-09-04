import json
import threading
import time

from app.video_jobs import VideoJobManager


STEPS = [
    {"step_number": 1, "action": "Open the calibration panel.",
     "claim_id": "claim_acme_calibrate_1"},
    {"step_number": 2, "action": "Press the calibration button.",
     "claim_id": "claim_acme_calibrate_2"},
]


def fake_generator(calls=None, gate=None, metadata=None):
    def generate(product_label, procedure, steps, output, poster,
                 reference_image=None, product_dir=None):
        if calls is not None:
            calls.append({
                "product_label": product_label,
                "procedure": procedure,
                "reference_image": reference_image,
                "product_dir": product_dir,
            })
        if gate is not None:
            assert gate.wait(timeout=5)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"fake mp4 bytes")
        poster.write_bytes(b"fake png bytes")
        return metadata
    return generate


def wait_for_state(manager, job_id, state, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        job = manager.status(job_id)
        if job and job["state"] == state:
            return job
        time.sleep(0.02)
    raise AssertionError(f"job never reached state {state}: "
                         f"{manager.status(job_id)}")


def make_pack(tmp_path):
    packs = tmp_path / "packs"
    (packs / "acme-widget-9000").mkdir(parents=True)
    return packs


def test_generation_registers_pending_asset_and_binding(tmp_path):
    packs = make_pack(tmp_path)
    manager = VideoJobManager(packs, generator=fake_generator())
    job = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                         "calibrate_widget", STEPS)
    assert job["state"] in {"queued", "running", "ready"}
    ready = wait_for_state(manager, job["job_id"], "ready")
    assert ready["asset_id"] == "derived_generated_calibrate_widget_walkthrough"
    assert ready["binding_id"] == "mb_generated_calibrate_widget_walkthrough"

    pack_dir = packs / "acme-widget-9000"
    assets = json.loads((pack_dir / "derived-assets.json").read_text())["assets"]
    asset = next(a for a in assets if a["asset_id"] == ready["asset_id"])
    assert asset["type"] == "PROCEDURE_VIDEO_MP4"
    assert asset["approved_by"] is None
    assert asset["provisional_unverified"] is True
    assert asset["local_path"] == (
        "generated-assets/acme-widget-9000/calibrate-widget-walkthrough.mp4")
    generated = tmp_path / asset["local_path"]
    assert generated.read_bytes() == b"fake mp4 bytes"
    assert (tmp_path / asset["poster_local_path"]).is_file()

    bindings = json.loads(
        (pack_dir / "media-bindings.json").read_text())["bindings"]
    binding = next(b for b in bindings
                   if b["binding_id"] == ready["binding_id"])
    assert binding["source_id"] == ready["asset_id"]
    assert binding["kind"] == "DERIVED_ASSET"
    assert binding["approved_by"] is None
    assert binding["claim_ids"] == [
        "claim_acme_calibrate_1", "claim_acme_calibrate_2"]


def test_repeat_questions_share_one_job_and_one_generation(tmp_path):
    packs = make_pack(tmp_path)
    calls, gate = [], threading.Event()
    manager = VideoJobManager(packs, generator=fake_generator(calls, gate))
    first = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                           "calibrate_widget", STEPS)
    second = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                            "calibrate_widget", STEPS)
    assert first["job_id"] == second["job_id"]
    gate.set()
    wait_for_state(manager, first["job_id"], "ready")
    assert len(calls) == 1


def test_reregistration_upserts_instead_of_duplicating(tmp_path):
    packs = make_pack(tmp_path)
    for _ in range(2):
        manager = VideoJobManager(packs, generator=fake_generator())
        job = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                             "calibrate_widget", STEPS)
        wait_for_state(manager, job["job_id"], "ready")
    pack_dir = packs / "acme-widget-9000"
    assets = json.loads((pack_dir / "derived-assets.json").read_text())["assets"]
    bindings = json.loads(
        (pack_dir / "media-bindings.json").read_text())["bindings"]
    assert len(assets) == 1
    assert len(bindings) == 1


def test_generator_failure_marks_the_job_failed(tmp_path):
    packs = make_pack(tmp_path)

    def broken(product_label, procedure, steps, output, poster,
               reference_image=None, product_dir=None):
        raise RuntimeError("renderer exploded")

    manager = VideoJobManager(packs, generator=broken)
    job = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                         "calibrate_widget", STEPS)
    failed = wait_for_state(manager, job["job_id"], "failed")
    assert failed.get("error") is None or "renderer" not in str(
        failed.get("error"))


def test_unknown_job_status_is_none(tmp_path):
    manager = VideoJobManager(make_pack(tmp_path),
                              generator=fake_generator())
    assert manager.status("vidjob_missing") is None


def test_generator_metadata_overrides_registered_provenance(tmp_path):
    packs = make_pack(tmp_path)
    manager = VideoJobManager(packs, generator=fake_generator(metadata={
        "provider": "fal.ai / alibaba/wan-3.0/image-to-video",
        "request_id": "req_123",
        "license_status": "AI_GENERATED_PENDING_REVIEW",
        "external_spend_usd": None,
        "generator": "app/fal_video.py",
    }))
    job = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                         "calibrate_widget", STEPS)
    wait_for_state(manager, job["job_id"], "ready")
    assets = json.loads((packs / "acme-widget-9000" /
                         "derived-assets.json").read_text())["assets"]
    asset = assets[0]
    assert asset["provider"].startswith("fal.ai /")
    assert asset["request_id"] == "req_123"
    assert asset["license_status"] == "AI_GENERATED_PENDING_REVIEW"
    assert asset["external_spend_usd"] is None
    assert asset["generator"] == "app/fal_video.py"
    assert asset["approved_by"] is None


def test_reference_image_is_resolved_from_bound_evidence(tmp_path):
    packs = make_pack(tmp_path)
    vault = tmp_path / "vault"
    image = vault / "acme-widget-9000" / "images" / "spec.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"png bytes")
    (vault / "acme-widget-9000" / "manifest.json").write_text(json.dumps({
        "sources": [{"source_id": "src_image", "type": "IMAGE",
                     "local_path": "images/spec.png"}],
    }))
    (packs / "acme-widget-9000" / "media-bindings.json").write_text(
        json.dumps({"bindings": [{
            "binding_id": "mb_image", "kind": "IMAGE",
            "source_id": "src_image",
            "claim_ids": ["claim_acme_calibrate_1"],
        }]}))
    calls = []
    manager = VideoJobManager(packs, generator=fake_generator(calls),
                              vault_root=vault)
    job = manager.ensure("acme-widget-9000", "Acme Widget 9000",
                         "calibrate_widget", STEPS)
    wait_for_state(manager, job["job_id"], "ready")
    assert calls[0]["reference_image"] == image.resolve()


def test_renderer_defaults_to_grounded_keyframe_mode(monkeypatch):
    from app import video_jobs
    monkeypatch.delenv("SHOWME_VIDEO_RENDERER", raising=False)
    assert video_jobs.renderer_mode() == "keyframe"
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "auto")
    assert video_jobs.renderer_mode() == "keyframe"
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "fal")
    assert video_jobs.renderer_mode() == "fal"
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "deterministic")
    assert video_jobs.renderer_mode() == "deterministic"
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "nonsense")
    assert video_jobs.renderer_mode() == "keyframe"


def test_grounded_mode_refuses_unregistered_procedures(tmp_path, monkeypatch):
    monkeypatch.delenv("SHOWME_VIDEO_RENDERER", raising=False)
    packs = make_pack(tmp_path)
    manager = VideoJobManager(packs)
    assert manager.can_generate("acme-widget-9000",
                                "calibrate_widget") is False

    (packs / "acme-widget-9000" / "procedure-keyframes.json").write_text(
        json.dumps({"schema_version": 1, "procedures": [{
            "procedure": "calibrate_widget",
            "segments": [{"segment_id": "seg1",
                          "start_path": "a.png", "end_path": "b.png",
                          "motion_prompt": "move"}],
        }]}))
    assert manager.can_generate("acme-widget-9000",
                                "calibrate_widget") is True
    assert manager.can_generate("acme-widget-9000", "other") is False

    # Explicit experimental renderers never refuse.
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "fal")
    assert manager.can_generate("acme-widget-9000", "other") is True
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "deterministic")
    assert manager.can_generate("acme-widget-9000", "other") is True

    from app import fal_video
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "fal")
    assert manager._resolve_generator() is fal_video.generate
    monkeypatch.setenv("SHOWME_VIDEO_RENDERER", "deterministic")
    from app.video_jobs import _deterministic_generator
    assert manager._resolve_generator() is _deterministic_generator


def test_fal_prompt_is_grounded_in_steps_and_forbids_text():
    from app.fal_video import build_prompt
    prompt = build_prompt("Acme Widget 9000", "calibrate_widget", STEPS)
    assert "Acme Widget 9000" in prompt
    assert "calibrate widget" in prompt
    assert "Open the calibration panel." in prompt
    assert "Press the calibration button." in prompt
    assert "no on-screen text" in prompt
