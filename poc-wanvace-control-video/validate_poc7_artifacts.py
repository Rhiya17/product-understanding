#!/usr/bin/env python3
"""Validate POC 7 artifact, trust, watermark, request-ID, and spend discipline."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / "out"
RUNS = (
    "twin-skin-1",
    "twin-skin-2",
    "twin-skin-3",
    "twin-skin-4",
    "twin-skin-defect-reverse-direction",
)
QWEN_CHECKS = ("same-product", "fixed-camera", "motion-direction", "reaches-folded-state")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_watermark(video: Path) -> None:
    capture = cv2.VideoCapture(str(video))
    count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_number in (0, max(0, count // 2), max(0, count - 1)):
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = capture.read()
        assert ok, f"could not read frame {frame_number + 1} from {video}"
        height, width = frame.shape[:2]
        region = frame[0 : max(100, height // 4), int(width * 0.68) : width]
        b, g, r = (region[:, :, index].astype(np.float32) for index in range(3))
        red_fraction = np.mean((r > 60) & (r > g * 1.5) & (r > b * 1.5))
        assert red_fraction > 0.05, f"red internal watermark not detected: {video}"
    capture.release()


def main() -> None:
    preflight = load(OUT / "poc7-preflight" / "schema-verification.json")
    assert preflight["status"] == "PASS"
    assert preflight["endpoint"] == "fal-ai/wan-vace-14b/depth"
    assert {"480p", "720p"} <= set(preflight["resolution_enum"])

    controls = load(HERE / "references" / "twin-skin-control-manifest.json")
    assert controls["internal_only"] is True and controls["approved_by"] is None
    assert controls["reference_person_free_review"]["status"] == "PASS"
    for name in ("official", "novel", "defect_reverse_direction"):
        record = controls["controls"][name]
        clip = Path(record["control_clip"])
        assert clip.is_file() and sha256_of(clip) == record["control_clip_sha256"]
        assert record["person_free_review"]["status"] == "PASS"
        assert record["source_frame_count"] == 96 and record["fps"] == 24
        assert_watermark(clip)

    request_ids = set()
    for label in RUNS:
        run_dir = OUT / label
        for relative in (
            "submission.json",
            "request.json",
            "result.json",
            "artifact-manifest.json",
            "video.mp4",
            "video.gif",
            "contact-sheet.png",
            "verification/gates.json",
            "verification/silhouette-per-frame.json",
        ):
            assert (run_dir / relative).is_file(), f"missing {label}/{relative}"
        frames = sorted((run_dir / "frames").glob("frame-*.png"))
        assert len(frames) == 96, f"{label}: expected 96 extracted frames, found {len(frames)}"
        submission = load(run_dir / "submission.json")
        request = load(run_dir / "request.json")
        artifact = load(run_dir / "artifact-manifest.json")
        gates = load(run_dir / "verification" / "gates.json")
        assert submission["request_id"] == request["request_id"]
        assert request["request_id"] not in request_ids
        request_ids.add(request["request_id"])
        assert submission["person_free_inputs"] is True
        assert submission["prompt_scope"] == "appearance only"
        assert submission["internal_only"] is True and submission["approved_by"] is None
        assert artifact["internal_only"] is True and artifact["approved_by"] is None
        assert artifact["trust_label"] == "TWIN_RENDER_VACE_SKIN"
        assert sha256_of(run_dir / "video.mp4") == artifact["video_metadata"]["sha256"]
        assert sha256_of(run_dir / "video.gif") == artifact["video_metadata"]["gif_sha256"]
        assert artifact["video_metadata"]["num_frames"] == 96
        assert artifact["video_metadata"]["internal_only"] is True
        assert gates["pose_sequence_gate"]["status"] == "PASS"
        assert gates["identity_gate"]["status"] == "FAIL"
        assert gates["all_serving_gates_pass"] is False
        assert len(load(run_dir / "verification" / "silhouette-per-frame.json")) == 96
        assert_watermark(run_dir / "video.mp4")

    defect = load(OUT / "twin-skin-defect-reverse-direction" / "verification" / "gates.json")
    assert defect["negative_control_gate"]["status"] == "PASS"
    assert defect["negative_control_gate"]["preserves_defect_reverse_direction"] is True

    qwen_root = OUT / "twin-skin-2" / "verification" / "qwen"
    qwen_preflight = load(qwen_root / "live-preflight.json")
    assert qwen_preflight["status"] == "PASS" and qwen_preflight["unit_price_usd"] == 0.01
    for slug in QWEN_CHECKS:
        check = qwen_root / slug
        for filename in ("submission.json", "request.json", "result.json", "verdict.json"):
            assert (check / filename).is_file(), f"missing Qwen {slug}/{filename}"
        request_id = load(check / "request.json")["request_id"]
        assert request_id not in request_ids
        request_ids.add(request_id)

    ledger = load(OUT / "poc7-spend-ledger.json")
    ledger_ids = [entry["request_id"] for entry in ledger["entries"]]
    assert len(ledger_ids) == len(set(ledger_ids)) == len(request_ids)
    assert set(ledger_ids) == request_ids
    assert all(entry["status"] == "completed" for entry in ledger["entries"])
    assert abs(ledger["estimated_spend_usd"] - 1.72) < 1e-9
    assert ledger["estimated_spend_usd"] <= ledger["spend_ceiling_usd"] == 15.0
    assert abs(ledger["remaining_ceiling_usd"] - 13.28) < 1e-9

    findings = REPO / "docs" / "pocs" / "poc7-vace-skin-findings.md"
    report = findings.read_text()
    for phrase in (
        "INTERNAL ONLY — DO NOT SHIP",
        "does not yet deliver a serving-safe photoreal fold",
        "TWIN_RENDER_VACE_SKIN",
        "Total POC spend",
        "$1.72",
        "derived-assets.json",
    ):
        assert phrase in report, f"findings missing required phrase: {phrase}"

    derived = REPO / "evidence-packs" / "graco-ready2jet-2212125" / "derived-assets.json"
    if derived.exists():
        text = derived.read_text()
        assert not any(request_id in text for request_id in request_ids), (
            "a failed POC 7 run was registered as a derived asset"
        )

    print(
        "POC 7 validation PASS: 5 VACE runs, 4 Qwen checks, 9 unique request IDs, "
        "all media watermarked/internal-only, no serving pass, spend $1.72/$15.00"
    )


if __name__ == "__main__":
    main()
