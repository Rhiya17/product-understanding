"""Submit a Meshy v6 multi-image-to-3D run via fal.ai and collect artifacts.

POC 5 (static digital twin) — see docs/pocs/poc5-digital-twin-runbook.md.
Mirrors the artifact discipline of run_seedance.py: every run saves the exact
submission (with input SHA-256s), the raw result, and all downloadable model
files under runs/<label>/.

Endpoint schema verified live on 2026-08-13 via
https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/meshy/v6/multi-image-to-3d
  required: image_urls (1-4 images)
  no seed parameter exists -> runs are stochastic; do 3 runs.

Usage:
  set -a; source .env; set +a          # .env provides FAL_KEY
  python3 run_meshy.py --label meshy-run-01 --dry-run
  python3 run_meshy.py --label meshy-run-01
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "inputs" / "source-manifest.json"
IMAGES_DIR = HERE / "inputs" / "images"
UPLOAD_CACHE = HERE / "runs" / "upload-cache.json"
ENDPOINT = "fal-ai/meshy/v6/multi-image-to-3d"

# Order matters: anchor view first.
INPUT_VIEWS = [
    "view-01-front-3q.png",
    "view-02-top-3q.png",
    "view-03-undercarriage.png",
    "view-04-side-profile.png",
]

# Highest-geometry-quality settings (runbook Stage 2). symmetry_mode is OFF
# deliberately: the cup holder is one-sided and auto/on symmetry risks
# mirroring it into invented geometry (hard-fail check 4d).
GENERATION_ARGS = {
    "topology": "triangle",
    "target_polycount": 100000,
    "symmetry_mode": "off",
    "should_remesh": True,
    "should_texture": True,
    "enable_pbr": True,
    # Character-rigging features are irrelevant to a product and stay off.
    "enable_rigging": False,
    "enable_animation": False,
}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upload(path: Path, cache: dict) -> str:
    import fal_client
    digest = sha256_of(path)
    if digest not in cache:
        print(f"  uploading {path.name}…")
        cache[digest] = fal_client.upload_file(str(path))
        UPLOAD_CACHE.parent.mkdir(exist_ok=True)
        UPLOAD_CACHE.write_text(json.dumps(cache, indent=2))
    return cache[digest]


def pack_fingerprint(manifest: dict, refs: list[dict]) -> dict:
    """Version + content hash of the input pack, recorded in every submission."""
    version = manifest.get("pack_version")
    if not version:
        sys.exit("source-manifest.json must declare pack_version (e.g. 'v2').")
    combined = hashlib.sha256(
        (version + "".join(sorted(r["sha256"] for r in refs))).encode()
    ).hexdigest()
    return {"pack_version": version, "pack_hash": combined}


def verify_inputs_against_manifest() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text())
    refs = []
    for name in INPUT_VIEWS:
        path = IMAGES_DIR / name
        if not path.is_file():
            sys.exit(f"Missing input image: {path}")
        digest = sha256_of(path)
        entry = manifest["images"].get(name)
        if entry is None:
            sys.exit(f"{name} is not in source-manifest.json — add provenance first.")
        if entry["sha256"] != digest:
            sys.exit(f"{name} hash mismatch vs manifest — inputs changed without provenance update.")
        if entry["role"] != "input":
            sys.exit(f"{name} role is {entry['role']!r}, not 'input'.")
        refs.append({"file": name, "sha256": digest})
    return refs


def download(url: str, dest: Path) -> None:
    import requests
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    print(f"  saved {dest.name} ({dest.stat().st_size:,} bytes)")


def collect_outputs(result: dict, out_dir: Path) -> None:
    model_dir = out_dir / "model"
    model_dir.mkdir(exist_ok=True)
    glb = (result.get("model_glb") or {}).get("url")
    if glb:
        download(glb, model_dir / "model.glb")
    for fmt, url in (result.get("model_urls") or {}).items():
        if isinstance(url, str) and url.startswith("http") and fmt != "glb":
            download(url, model_dir / f"model.{fmt}")
        elif isinstance(url, dict) and url.get("url"):
            download(url["url"], model_dir / f"model.{fmt}")
    thumb = (result.get("thumbnail") or {}).get("url") if isinstance(result.get("thumbnail"), dict) else result.get("thumbnail")
    if isinstance(thumb, str) and thumb.startswith("http"):
        download(thumb, out_dir / "thumbnail.png")
    tex_dir = out_dir / "textures"
    for i, tex in enumerate(result.get("texture_urls") or []):
        url = tex.get("url") if isinstance(tex, dict) else tex
        if isinstance(url, str) and url.startswith("http"):
            tex_dir.mkdir(exist_ok=True)
            ext = url.split("?")[0].rsplit(".", 1)[-1][:4] or "bin"
            download(url, tex_dir / f"texture-{i:02d}.{ext}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    refs = verify_inputs_against_manifest()
    manifest = json.loads(MANIFEST.read_text())
    pack = pack_fingerprint(manifest, refs)
    out_dir = HERE / "runs" / args.label
    if out_dir.exists() and any(out_dir.iterdir()):
        sys.exit(f"Refusing to overwrite existing run: {out_dir}")

    if args.dry_run:
        print(json.dumps({"endpoint": ENDPOINT, "pack": pack, "inputs": refs,
                          "arguments": {**GENERATION_ARGS, "image_urls": ["<uploaded>"] * len(refs)}}, indent=2))
        return

    if not os.environ.get("FAL_KEY"):
        sys.exit("Set FAL_KEY before running (set -a; source .env; set +a).")
    import fal_client

    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.is_file() else {}
    image_urls = [upload(IMAGES_DIR / r["file"], cache) for r in refs]
    arguments = {**GENERATION_ARGS, "image_urls": image_urls}

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "submission.json").write_text(json.dumps({
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "pack": pack,
        "arguments": arguments,
        "image_refs": [{**r, "url": u} for r, u in zip(refs, image_urls)],
    }, indent=2))

    print(f"POC5 run {args.label} ({ENDPOINT}): submitting…")
    result = fal_client.subscribe(
        ENDPOINT,
        arguments=arguments,
        with_logs=True,
        on_queue_update=lambda u: print(f"  {type(u).__name__}"),
    )
    (out_dir / "result.json").write_text(json.dumps(result, indent=2, default=str))
    collect_outputs(result, out_dir)
    print(f"done -> {out_dir}")


if __name__ == "__main__":
    main()
