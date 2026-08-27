#!/usr/bin/env python3
"""Submit one ordered POC 7 VACE run with hard spend and artifact guards."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import cv2
import fal_client
import requests


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT_ROOT = HERE / "out"
UPLOAD_CACHE = OUT_ROOT / "poc7-upload-cache.json"
LEDGER = OUT_ROOT / "poc7-spend-ledger.json"
PREFLIGHT = OUT_ROOT / "poc7-preflight" / "schema-verification.json"
CONTROL_MANIFEST = HERE / "references" / "twin-skin-control-manifest.json"
REF_IMAGE = REPO / "source-vault" / "graco-ready2jet-2212125" / "images" / "view-01-front-3q.png"
ENDPOINT = "fal-ai/wan-vace-14b/depth"
SPEND_CEILING_USD = 15.0
SEED = 42001
PROMPT = (
    "A photoreal professional studio product video of the exact Graco Ready2Jet "
    "compact stroller in the Kingston colorway shown in the reference image. "
    "Exact gray heather fabric, matte black frame, tan leather-look handle grip, "
    "black mesh basket, black belly bar, and original black tri-spoke wheels. "
    "The tan handle grip is uninterrupted and bare, with no attached device or "
    "accessory. The belly bar is matte black plastic, never tan. "
    "Clean neutral light-gray studio background, soft grounded shadow, bright "
    "diffuse product lighting, realistic fabric weave, molded plastic, powder-coated "
    "metal, and rubber materials. Product-only scene, no people, no text, no logos."
)
NEGATIVE_PROMPT = (
    "morphing, warping, extra wheels, missing wheels, extra parts, invented controls, "
    "invented parts, altered wheel design, non-tri-spoke wheels, duplicate parts, "
    "handle-mounted device, silver handle controls, tan belly bar, pseudo-branding, "
    "orange label, "
    "people, person, hands, face, text, captions, watermark, cartoon, illustration, "
    "cluttered background, low quality"
)
WATERMARK_LINE_1 = "INTERNAL ONLY"
WATERMARK_LINE_2 = "DO NOT SHIP"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temp.replace(path)


def ffmpeg_bin() -> str:
    configured = shutil.which("ffmpeg")
    if configured:
        return configured
    bundled = Path("/Users/vbp/Documents/ChatGPT/ShowMe/ffmpeg-darwin-arm64")
    if bundled.is_file():
        return str(bundled)
    raise SystemExit("ffmpeg is required")


def watermark_filter() -> str:
    font = "/System/Library/Fonts/Supplemental/Arial.ttf"
    return (
        "drawbox=x=iw-130:y=10:w=120:h=48:color=0x780000@0.94:t=fill,"
        f"drawtext=fontfile={font}:text='{WATERMARK_LINE_1}':x=w-124:y=16:"
        "fontsize=12:fontcolor=white,"
        f"drawtext=fontfile={font}:text='{WATERMARK_LINE_2}':x=w-124:y=38:"
        "fontsize=8:fontcolor=white"
    )


def upload(path: Path, cache: dict) -> str:
    digest = sha256_of(path)
    if digest not in cache:
        cache[digest] = fal_client.upload_file(str(path))
        atomic_json(UPLOAD_CACHE, cache)
    return cache[digest]


def load_preflight() -> dict:
    if not PREFLIGHT.is_file():
        raise SystemExit("live schema preflight is missing; run verify_vace_schema.py first")
    record = json.loads(PREFLIGHT.read_text())
    if record.get("status") != "PASS" or record.get("endpoint") != ENDPOINT:
        raise SystemExit("live schema preflight did not pass for the required endpoint")
    return record


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"spend_ceiling_usd": SPEND_CEILING_USD, "entries": []}


def committed_spend(ledger: dict) -> float:
    return round(sum(float(entry["estimated_cost_usd"]) for entry in ledger["entries"]), 6)


def append_ledger(entry: dict) -> None:
    ledger = load_ledger()
    if any(item.get("request_id") == entry.get("request_id") for item in ledger["entries"]):
        raise SystemExit("request id already exists in spend ledger")
    ledger["entries"].append(entry)
    ledger["estimated_spend_usd"] = committed_spend(ledger)
    ledger["remaining_ceiling_usd"] = round(SPEND_CEILING_USD - ledger["estimated_spend_usd"], 6)
    atomic_json(LEDGER, ledger)


def update_ledger(request_id: str, **changes: object) -> None:
    ledger = load_ledger()
    matches = [entry for entry in ledger["entries"] if entry.get("request_id") == request_id]
    if len(matches) != 1:
        raise SystemExit(f"could not update unique spend entry for {request_id}")
    matches[0].update(changes)
    ledger["estimated_spend_usd"] = committed_spend(ledger)
    ledger["remaining_ceiling_usd"] = round(SPEND_CEILING_USD - ledger["estimated_spend_usd"], 6)
    atomic_json(LEDGER, ledger)


def video_metadata(path: Path) -> dict:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"could not read video metadata: {path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()
    return {
        "width": width,
        "height": height,
        "fps": fps,
        "num_frames": frames,
        "duration_seconds": frames / fps if fps else None,
    }


def download(url: str, output: Path) -> None:
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with output.open("wb") as stream:
            for chunk in response.iter_content(chunk_size=1 << 16):
                stream.write(chunk)


def create_artifacts(raw_video: Path, out_dir: Path) -> dict:
    video = out_dir / "video.mp4"
    subprocess.run(
        [
            ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(raw_video),
            "-vf", watermark_filter(), "-c:v", "libx264", "-preset", "slow",
            "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video),
        ],
        check=True,
    )
    frames_dir = out_dir / "frames"
    frames_dir.mkdir()
    subprocess.run(
        [ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(video), str(frames_dir / "frame-%04d.png")],
        check=True,
    )
    subprocess.run(
        [
            ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(video),
            "-vf", "fps=12,scale=480:-2:flags=lanczos", "-loop", "0", str(out_dir / "video.gif"),
        ],
        check=True,
    )
    metadata = video_metadata(video)
    metadata.update(
        {
            "sha256": sha256_of(video),
            "gif_sha256": sha256_of(out_dir / "video.gif"),
            "watermark": [WATERMARK_LINE_1, WATERMARK_LINE_2],
            "internal_only": True,
        }
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument(
        "--control",
        choices=("official", "novel", "defect_reverse_direction"),
        required=True,
    )
    parser.add_argument("--resolution", choices=("480p", "720p"), required=True)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--steps", type=int, default=30)
    args = parser.parse_args()

    if not os.environ.get("FAL_KEY"):
        raise SystemExit("Set FAL_KEY ephemerally before running")
    preflight = load_preflight()
    controls = json.loads(CONTROL_MANIFEST.read_text())
    control_record = controls["controls"][args.control]
    control_clip = Path(control_record["control_clip"])
    if not control_clip.is_file() or sha256_of(control_clip) != control_record["control_clip_sha256"]:
        raise SystemExit("control clip missing or hash mismatch")
    if sha256_of(REF_IMAGE) != controls["reference_image_sha256"]:
        raise SystemExit("reference image hash mismatch")

    out_dir = OUT_ROOT / args.label
    if out_dir.exists():
        raise SystemExit(f"fresh label required; directory already exists: {out_dir}")
    out_dir.mkdir(parents=True)

    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}
    control_url = upload(control_clip, cache)
    ref_url = upload(REF_IMAGE, cache)
    arguments = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "video_url": control_url,
        "ref_image_urls": [ref_url],
        "preprocess": True,
        "match_input_num_frames": True,
        "match_input_frames_per_second": True,
        "resolution": args.resolution,
        "num_inference_steps": args.steps,
        "seed": args.seed,
        "enable_safety_checker": True,
        "enable_prompt_expansion": False,
    }
    control_frames = int(control_record["source_frame_count"])
    billing_fps = int(preflight["billing_frames_per_second"])
    price = float(preflight["pricing_usd_per_billed_video_second"][args.resolution])
    estimated_cost = round(control_frames / billing_fps * price, 6)
    ledger = load_ledger()
    if committed_spend(ledger) + estimated_cost > SPEND_CEILING_USD:
        raise SystemExit("STOP: this submission would exceed the $15 hard spend ceiling")

    submission = {
        "prepared_at": utcnow(),
        "status": "prepared",
        "endpoint": ENDPOINT,
        "label": args.label,
        "arguments": arguments,
        "inputs": {
            "control_clip": {
                "path": str(control_clip),
                "sha256": sha256_of(control_clip),
                "provenance": (
                    f"deterministic dressed twin {control_record.get('motion_authority', 'Ready2Jet_Fold_Correct; unchanged')} "
                    "PNG sequence; 24 fps; visibly watermarked internal-only"
                ),
                "motion_authority": control_record.get("motion_authority", "sole motion authority"),
            },
            "reference_image": {
                "path": str(REF_IMAGE),
                "sha256": sha256_of(REF_IMAGE),
                "provenance": "official product-only Kingston studio image; appearance authority only",
            },
            "source_blend": {
                "path": controls["source_blend"],
                "sha256": controls["source_blend_sha256"],
            },
        },
        "person_free_inputs": True,
        "prompt_scope": "appearance only",
        "estimated_cost_usd": estimated_cost,
        "spend_ceiling_usd": SPEND_CEILING_USD,
        "schema_verification": str(PREFLIGHT),
        "trust_label": "TWIN_RENDER_VACE_SKIN",
        "internal_only": True,
        "approved_by": None,
    }
    atomic_json(out_dir / "submission.json", submission)

    print(f"submitting {args.label}: {ENDPOINT} {args.resolution} seed={args.seed}")
    handle = fal_client.submit(ENDPOINT, arguments=arguments)
    request_record = {
        "request_id": handle.request_id,
        "submitted_at": utcnow(),
        "endpoint": ENDPOINT,
        "label": args.label,
        "estimated_cost_usd": estimated_cost,
        "response_url": handle.response_url,
        "status_url": handle.status_url,
        "cancel_url": handle.cancel_url,
    }
    atomic_json(out_dir / "request.json", request_record)
    submission["submitted_at"] = request_record["submitted_at"]
    submission["status"] = "submitted"
    submission["request_id"] = handle.request_id
    atomic_json(out_dir / "submission.json", submission)
    append_ledger({
        "request_id": handle.request_id,
        "label": args.label,
        "endpoint": ENDPOINT,
        "resolution": args.resolution,
        "estimated_cost_usd": estimated_cost,
        "submitted_at": request_record["submitted_at"],
        "status": "submitted",
    })
    print(f"request id persisted: {handle.request_id}")

    try:
        result = handle.get()
    except Exception as error:
        update_ledger(handle.request_id, status="provider_error", error=repr(error), updated_at=utcnow())
        raise
    atomic_json(out_dir / "result.json", result)
    video_url = (result.get("video") or {}).get("url")
    if not video_url:
        update_ledger(handle.request_id, status="completed_no_video", updated_at=utcnow())
        raise SystemExit("STOP: provider completed without a video; see result.json")

    with tempfile.TemporaryDirectory(prefix="poc7-vace-raw-") as temp_dir:
        raw_video = Path(temp_dir) / "provider-output.mp4"
        download(video_url, raw_video)
        artifacts = create_artifacts(raw_video, out_dir)
    atomic_json(out_dir / "artifact-manifest.json", {
        "created_at": utcnow(),
        "request_id": handle.request_id,
        "video": "video.mp4",
        "gif": "video.gif",
        "frames": "frames/",
        "video_metadata": artifacts,
        "trust_label": "TWIN_RENDER_VACE_SKIN",
        "internal_only": True,
        "approved_by": None,
    })
    update_ledger(
        handle.request_id,
        status="completed",
        completed_at=utcnow(),
        output_num_frames=artifacts["num_frames"],
        output_duration_seconds=artifacts["duration_seconds"],
    )
    print(f"completed -> {out_dir}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("interrupted; inspect request.json and the fal queue before retrying")
