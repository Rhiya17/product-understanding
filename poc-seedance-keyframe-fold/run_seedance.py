"""Submit Seedance 2.0 fold-video runs via fal.ai and collect artifacts.

Mirrors the artifact discipline of ../poc-higgsfield-one-hand-fold/run_poc.py:
every run saves the exact submission, the final result, the video, extracted
frames, and a contact sheet under out/<condition>-<label>/.

Local reference files are uploaded through fal's storage API at submit time,
so no external image hosting is needed. Requires: pip install fal-client
requests, and FAL_KEY in the environment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import fal_client
import requests

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "conditions" / "manifest.json"
UPLOAD_CACHE_PATH = HERE / "out" / "upload-cache.json"

# Pre-declared seeds, continuing the numbering from the corrected Higgsfield runs.
DEFAULT_SEEDS = (42001, 42002, 42003)

ENDPOINTS = {
    ("first_last_frames", "quality"): "bytedance/seedance-2.0/image-to-video",
    ("first_last_frames", "fast"): "bytedance/seedance-2.0/fast/image-to-video",
    ("omni_reference", "quality"): "bytedance/seedance-2.0/reference-to-video",
    ("omni_reference", "fast"): "bytedance/seedance-2.0/fast/reference-to-video",
}


def require_key() -> None:
    if not os.environ.get("FAL_KEY"):
        sys.exit("Set FAL_KEY before running.")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_condition(condition: str) -> tuple[dict, dict, dict]:
    manifest = json.loads(MANIFEST_PATH.read_text())
    cond = manifest["conditions"].get(condition)
    if cond is None:
        sys.exit(f"Unknown condition {condition!r}; expected one of {sorted(manifest['conditions'])}.")
    gen = {**manifest["generation"], **cond.get("generation", {})}
    return manifest, cond, gen


def upload_refs(manifest: dict, keys: list[str], kind: str) -> list[dict]:
    """Upload local reference files to fal storage, caching by content hash."""
    cache = json.loads(UPLOAD_CACHE_PATH.read_text()) if UPLOAD_CACHE_PATH.is_file() else {}
    refs = []
    for key in keys:
        entry = manifest[kind][key]
        local = (MANIFEST_PATH.parent / entry["local"]).resolve()
        if not local.is_file():
            sys.exit(f"{kind}[{key}]: file not found: {local}")
        digest = sha256_of(local)
        if digest not in cache:
            print(f"  uploading {local.name}…")
            cache[digest] = fal_client.upload_file(str(local))
            UPLOAD_CACHE_PATH.parent.mkdir(exist_ok=True)
            UPLOAD_CACHE_PATH.write_text(json.dumps(cache, indent=2))
        refs.append({"key": key, "local": str(local), "sha256": digest, "url": cache[digest]})
    return refs


def build_arguments(cond: dict, gen: dict, prompt: str, images: list[dict],
                    videos: list[dict], seed: int) -> dict:
    args: dict = {
        "prompt": prompt,
        "resolution": gen["resolution"],
        "duration": str(gen["duration_seconds"]),
        "aspect_ratio": gen["aspect_ratio"],
        "generate_audio": gen["generate_audio"],
        "seed": seed,
    }
    if cond["mode"] == "first_last_frames":
        args["image_url"] = images[0]["url"]
        if len(images) > 1:
            args["end_image_url"] = images[1]["url"]
    else:
        args["image_urls"] = [ref["url"] for ref in images]
        if videos:
            args["video_urls"] = [ref["url"] for ref in videos]
    return args


def download_video(url: str, out_dir: Path) -> Path:
    video_path = out_dir / "video.mp4"
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with video_path.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    return video_path


def extract_frames(video_path: Path, out_dir: Path) -> None:
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path),
         "-vf", "fps=12/8", str(frames_dir / "frame-%02d.png")],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_path),
         "-vf", "fps=12/8,scale=240:-2,tile=6x2", "-frames:v", "1",
         str(out_dir / "contact-sheet.png")],
        check=True,
    )


def run_once(condition: str, label: str, tier: str, seed: int) -> None:
    manifest, cond, gen = load_condition(condition)
    prompt = (HERE / "conditions" / cond["prompt_file"]).read_text().strip()
    images = upload_refs(manifest, cond["image_keys"], "images")
    videos = upload_refs(manifest, cond["video_keys"], "videos") if cond["video_keys"] else []

    endpoint = ENDPOINTS[(cond["mode"], tier)]
    arguments = build_arguments(cond, gen, prompt, images, videos, seed)

    out_dir = HERE / "out" / f"{condition}-{label}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "submission.json").write_text(
        json.dumps(
            {
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "condition": condition,
                "tier": tier,
                "endpoint": endpoint,
                "seed": seed,
                "arguments": arguments,
                "image_refs": images,
                "video_refs": videos,
            },
            indent=2,
        )
    )

    print(f"Condition {condition} run {label} ({endpoint}, seed {seed}): submitting…")
    result = fal_client.subscribe(
        endpoint,
        arguments=arguments,
        with_logs=True,
        on_queue_update=lambda update: print(f"  {type(update).__name__}"),
    )
    (out_dir / "result.json").write_text(json.dumps(result, indent=2, default=str))

    video_url = (result.get("video") or {}).get("url")
    if not video_url:
        sys.exit(f"Completed but no video URL found; see {out_dir / 'result.json'}")
    video_path = download_video(video_url, out_dir)
    extract_frames(video_path, out_dir)
    print(f"  done -> {video_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", required=True, choices=["a", "b", "c", "seg1", "seg2"])
    parser.add_argument("--runs", type=int, default=1, help="Number of runs (uses pre-declared seeds).")
    parser.add_argument("--run-label", default=None, help="Label for a single run (default run-01…).")
    parser.add_argument("--seed", type=int, default=None, help="Seed override for a single run.")
    parser.add_argument("--tier", choices=["quality", "fast"], default="quality")
    args = parser.parse_args()

    require_key()
    if args.run_label and args.runs != 1:
        sys.exit("--run-label only makes sense with a single run.")
    if args.runs > len(DEFAULT_SEEDS) and args.seed is None:
        sys.exit(f"Only {len(DEFAULT_SEEDS)} pre-declared seeds; pass --seed for extra runs.")

    if args.run_label:
        run_once(args.condition, args.run_label, args.tier, args.seed or DEFAULT_SEEDS[0])
    else:
        for i in range(args.runs):
            run_once(args.condition, f"run-{i + 1:02d}", args.tier, args.seed or DEFAULT_SEEDS[i])


if __name__ == "__main__":
    main()
