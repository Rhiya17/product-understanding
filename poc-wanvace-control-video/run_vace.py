#!/usr/bin/env python3
"""Wan VACE depth-control probe: reskin the official Ready2Jet fold clip.

Option 2 from docs/pocs/video-generation-alternatives.md ("make the AI trace a
skeleton"), using the real fold motion from the official Graco how-to video
as the skeleton. The fal endpoint computes the depth control internally
(preprocess=true); we supply the trimmed source clip plus a product-only
reference image for identity.

Artifact discipline mirrors the Seedance POC: every run saves submission.json
(with input SHA-256s), result.json, video.mp4, frames/, contact-sheet.png
under out/<label>/.

Usage:
  set -a; source ../poc-seedance-keyframe-fold/.env; set +a
  python run_vace.py --label probe-01 --resolution 480p
"""

import argparse
import hashlib
import json
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

import fal_client
import requests

HERE = Path(__file__).resolve().parent
CONTROL_CLIP = HERE / "references" / "fold-control-clip.mp4"
REF_IMAGE = HERE.parent / "poc-seedance-keyframe-fold" / "references" / "openfold.png"
UPLOAD_CACHE = HERE / "out" / "upload-cache.json"
ENDPOINT = "fal-ai/wan-vace-14b/depth"

PROMPT = """\
A professional studio product demonstration video of the exact Graco Ready2Jet \
compact stroller shown in the reference image. The stroller self-folds: the \
handlebar drops forward toward the front wheels, the frame compresses downward, \
and it finishes compact, upright, and self-standing on its wheels. A woman in \
dark jeans stands behind the stroller; her hand releases the handlebar as the \
fold begins. The stroller keeps its exact identity throughout: black frame, \
dark gray fabric, tan leather handle grip, cup holder, mesh basket, four wheels. \
Bright neutral lighting, pale blue wall with tall windows, light wooden floor. \
Fixed camera, no cuts, no text, no logos."""

NEGATIVE = "morphing, warping, extra wheels, extra parts, distorted hands, text, watermark, cartoon"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upload(path: Path, cache: dict) -> str:
    digest = sha256_of(path)
    if digest not in cache:
        print(f"  uploading {path.name}…")
        cache[digest] = fal_client.upload_file(str(path))
        UPLOAD_CACHE.parent.mkdir(exist_ok=True)
        UPLOAD_CACHE.write_text(json.dumps(cache, indent=2))
    return cache[digest]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--resolution", default="480p",
                    choices=["240p", "360p", "480p", "580p", "720p"])
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42001)
    args = ap.parse_args()

    if not os.environ.get("FAL_KEY"):
        sys.exit("Set FAL_KEY before running.")

    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}
    video_url = upload(CONTROL_CLIP, cache)
    ref_url = upload(REF_IMAGE, cache)

    arguments = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE,
        "video_url": video_url,
        "ref_image_urls": [ref_url],
        "preprocess": True,
        "match_input_num_frames": True,
        "match_input_frames_per_second": True,
        "resolution": args.resolution,
        "num_inference_steps": args.steps,
        "seed": args.seed,
    }

    out_dir = HERE / "out" / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "submission.json").write_text(json.dumps({
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "arguments": arguments,
        "inputs": {
            "control_clip": {"path": str(CONTROL_CLIP), "sha256": sha256_of(CONTROL_CLIP),
                             "provenance": "user-provided official Graco 'Ready2Jet: How to Fold and Unfold' video; trimmed 38.65s-42.0s (continuous wide-shot fold take)"},
            "ref_image": {"path": str(REF_IMAGE), "sha256": sha256_of(REF_IMAGE),
                          "provenance": "person-removed crop of official fold-sequence panel 1 (same colorway as source video)"},
        },
    }, indent=2))

    print(f"VACE run {args.label} ({ENDPOINT}, {args.resolution}, seed {args.seed}): submitting…")
    result = fal_client.subscribe(ENDPOINT, arguments=arguments, with_logs=True,
                                  on_queue_update=lambda u: None)
    (out_dir / "result.json").write_text(json.dumps(result, indent=2, default=str))

    video_out = (result.get("video") or {}).get("url")
    if not video_out:
        sys.exit(f"Completed but no video URL; see {out_dir / 'result.json'}")
    video_path = out_dir / "video.mp4"
    with requests.get(video_out, stream=True, timeout=300) as r:
        r.raise_for_status()
        with video_path.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 16):
                fh.write(chunk)

    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path),
                    "-vf", "fps=12/3.37", str(frames_dir / "frame-%02d.png")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path),
                    "-vf", "fps=12/3.37,scale=240:-2,tile=6x2", "-frames:v", "1",
                    str(out_dir / "contact-sheet.png")], check=True)
    print(f"  done -> {video_path}")


if __name__ == "__main__":
    main()
