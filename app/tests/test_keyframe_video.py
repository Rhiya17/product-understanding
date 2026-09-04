import json
import sys
import types

import numpy as np
import pytest

from app import keyframe_video


def write_clip(path, frames=48, size=(320, 180), seed=1):
    import cv2
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(path), cv2.VideoWriter_fourcc(*"avc1"), 24, size)
    rng = np.random.default_rng(seed)
    for _ in range(frames):
        writer.write(rng.integers(0, 255, (size[1], size[0], 3),
                                  dtype=np.uint8))
    writer.release()
    return path


def write_png(path, seed=1):
    import cv2
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    cv2.imwrite(str(path), rng.integers(0, 255, (180, 320, 3),
                                        dtype=np.uint8))
    return path


def make_registry(packs, product_dir, procedure="fold_stroller",
                  segments=None):
    pack_dir = packs / product_dir
    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "procedure-keyframes.json").write_text(json.dumps({
        "schema_version": 1,
        "procedures": [{
            "procedure": procedure,
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "keyframe_provenance": "test fixtures",
            "segments": segments or [],
        }],
    }))


def test_registry_entry_finds_only_registered_procedures(tmp_path):
    packs = tmp_path / "packs"
    make_registry(packs, "acme", segments=[
        {"segment_id": "seg1", "start_path": "a.png", "end_path": "b.png",
         "motion_prompt": "move"},
    ])
    assert keyframe_video.registry_entry(packs, "acme",
                                         "fold_stroller") is not None
    assert keyframe_video.registry_entry(packs, "acme", "other") is None
    assert keyframe_video.registry_entry(packs, "missing",
                                         "fold_stroller") is None


def test_parse_verdict_is_strict_and_fails_closed():
    passing = {"output": '```json\n{"verdict": "pass", "verdict_reason": "ok"}\n```'}
    assert keyframe_video.parse_verdict(passing)["verdict"] == "pass"
    failing = {"output": '{"verdict": "fail", "verdict_reason": "morphed"}'}
    assert keyframe_video.parse_verdict(failing)["verdict"] == "fail"
    assert keyframe_video.parse_verdict({"output": "not json"})["verdict"] == "fail"
    assert keyframe_video.parse_verdict({})["verdict"] == "fail"
    assert keyframe_video.parse_verdict(
        {"output": '{"no_verdict": true}'})["verdict"] == "fail"


def test_stitch_segments_concatenates_clips(tmp_path):
    import cv2
    seg1 = write_clip(tmp_path / "seg1.mp4", frames=48, seed=1)
    seg2 = write_clip(tmp_path / "seg2.mp4", frames=48, seed=2)
    output = tmp_path / "stitched.mp4"
    keyframe_video.stitch_segments([seg1, seg2], output)
    capture = cv2.VideoCapture(str(output))
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    assert total == 96


def test_unregistered_procedure_raises_keyframes_missing(tmp_path):
    packs = tmp_path / "packs"
    packs.mkdir()
    generate = keyframe_video.make_generator(packs)
    with pytest.raises(keyframe_video.KeyframesMissingError):
        generate("Acme", "fold_stroller", [], tmp_path / "out.mp4",
                 tmp_path / "poster.png", product_dir="acme")


def _stub_fal(monkeypatch, tmp_path, verdicts):
    """Stub fal_client: seedance returns a canned clip, VLM canned verdicts."""
    clip = write_clip(tmp_path / "canned-segment.mp4")
    calls = {"seedance": [], "vlm": []}
    verdict_iter = iter(verdicts)

    class Handle:
        def __init__(self, endpoint, arguments):
            self.endpoint, self.arguments = endpoint, arguments
            self.request_id = f"req_{len(calls['seedance']) + len(calls['vlm'])}"

        def get(self):
            if self.endpoint == keyframe_video.VLM_ENDPOINT:
                return {"output": json.dumps(next(verdict_iter))}
            return {"video": {"url": clip.as_uri()}}

    stub = types.ModuleType("fal_client")

    def submit(endpoint, arguments=None):
        handle = Handle(endpoint, arguments)
        calls["vlm" if endpoint == keyframe_video.VLM_ENDPOINT
              else "seedance"].append(arguments)
        return handle

    stub.submit = submit
    stub.upload_file = lambda p: f"https://fal.media/fake/{p}"
    monkeypatch.setitem(sys.modules, "fal_client", stub)
    return calls


def test_pipeline_generates_verifies_and_stitches(tmp_path, monkeypatch):
    packs = tmp_path / "packs"
    start = write_png(tmp_path / "refs" / "open.png", seed=1)
    mid = write_png(tmp_path / "refs" / "mid.png", seed=2)
    end = write_png(tmp_path / "refs" / "closed.png", seed=3)
    make_registry(packs, "acme", segments=[
        {"segment_id": "seg1", "start_path": "refs/open.png",
         "end_path": "refs/mid.png", "motion_prompt": "fold halfway",
         "duration_seconds": 4},
        {"segment_id": "seg2", "start_path": "refs/mid.png",
         "end_path": "refs/closed.png", "motion_prompt": "finish the fold",
         "duration_seconds": 4},
    ])
    calls = _stub_fal(monkeypatch, tmp_path, verdicts=[
        {"verdict": "pass", "verdict_reason": "ok"},
        {"verdict": "pass", "verdict_reason": "ok"},
    ])
    generate = keyframe_video.make_generator(packs)
    output = tmp_path / "generated-assets" / "acme" / "fold.mp4"
    poster = output.with_name("fold-poster.png")
    metadata = generate("Acme Stroller", "fold_stroller", [], output, poster,
                        product_dir="acme")
    assert output.is_file() and poster.is_file()
    assert len(calls["seedance"]) == 2
    assert len(calls["vlm"]) == 2
    assert calls["seedance"][0]["image_url"].endswith("open.png")
    assert calls["seedance"][0]["end_image_url"].endswith("mid.png")
    assert calls["seedance"][0]["aspect_ratio"] == "9:16"
    assert metadata["license_status"] == "GROUNDED_GENERATED_PENDING_REVIEW"
    assert "keyframe-pinned" in metadata["provider"]
    verification = json.loads(
        (tmp_path / metadata["verification_local_path"]).read_text())
    assert [seg["verdict"]["verdict"]
            for seg in verification["segments"]] == ["pass", "pass"]


def test_failed_verification_fails_the_job_and_serves_nothing(
        tmp_path, monkeypatch):
    packs = tmp_path / "packs"
    write_png(tmp_path / "refs" / "open.png", seed=1)
    write_png(tmp_path / "refs" / "mid.png", seed=2)
    make_registry(packs, "acme", segments=[
        {"segment_id": "seg1", "start_path": "refs/open.png",
         "end_path": "refs/mid.png", "motion_prompt": "fold halfway"},
    ])
    _stub_fal(monkeypatch, tmp_path, verdicts=[
        {"verdict": "fail", "verdict_reason": "product morphed"},
    ])
    generate = keyframe_video.make_generator(packs)
    output = tmp_path / "generated-assets" / "acme" / "fold.mp4"
    with pytest.raises(keyframe_video.SegmentVerificationError):
        generate("Acme Stroller", "fold_stroller", [], output,
                 output.with_name("fold-poster.png"), product_dir="acme")
    assert not output.exists()
    verification = json.loads(
        output.with_name("fold-verification.json").read_text())
    assert verification["segments"][0]["verdict"]["verdict"] == "fail"


def test_registry_v2_dangling_state_and_unknown_claim_refused(tmp_path):
    packs = tmp_path / "packs"
    pack_dir = packs / "acme"
    pack_dir.mkdir(parents=True, exist_ok=True)
    
    # Valid claim_id
    (pack_dir / "claims.json").write_text(json.dumps([{"claim_id": "claim_1"}]), encoding="utf-8")
    
    registry_path = pack_dir / "procedure-keyframes.json"
    
    # 1. Valid registry
    registry_path.write_text(json.dumps({
        "schema_version": 2,
        "procedures": [{
            "procedure": "fold",
            "states": [
                {"state_id": "s1", "claim_ids": ["claim_1"]},
                {"state_id": "s2", "claim_ids": []}
            ],
            "segments": [
                {"start_state": "s1", "end_state": "s2"}
            ]
        }]
    }))
    assert keyframe_video.registry_entry(packs, "acme", "fold") is not None
    
    # 2. Unknown claim id
    registry_path.write_text(json.dumps({
        "schema_version": 2,
        "procedures": [{
            "procedure": "fold",
            "states": [
                {"state_id": "s1", "claim_ids": ["claim_unknown"]},
                {"state_id": "s2", "claim_ids": []}
            ],
            "segments": [
                {"start_state": "s1", "end_state": "s2"}
            ]
        }]
    }))
    assert keyframe_video.registry_entry(packs, "acme", "fold") is None
    
    # 3. Dangling state ref in segment
    registry_path.write_text(json.dumps({
        "schema_version": 2,
        "procedures": [{
            "procedure": "fold",
            "states": [
                {"state_id": "s1", "claim_ids": ["claim_1"]}
            ],
            "segments": [
                {"start_state": "s1", "end_state": "s_missing"}
            ]
        }]
    }))
    assert keyframe_video.registry_entry(packs, "acme", "fold") is None
