"""Submit a Tripo3D H3.1 multiview-to-3D run via fal.ai and collect artifacts.

POC 5 (static digital twin) — see docs/pocs/poc5-digital-twin-runbook.md and
docs/planning/digital-twin-phase-plan.md Decision 1 (amended in-session
2026-08-26: Tripo3D-first sequential escalation; Meshy retired after the v1
pilot FAIL; Rodin/Hunyuan are fallbacks only if Tripo3D fails).

Endpoint schema verified live on 2026-08-27 via
https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=tripo3d/h3.1/multiview-to-3d
  required: image_urls (2-4 URLs, semantic order [front, left, back, right],
            front required)
  model_seed / texture_seed exist -> runs are REPRODUCIBLE (unlike Meshy);
  face_limit 1k-2M; geometry_quality/texture_quality standard|detailed;
  auto_size scales to real-world meters (helps the dimension check directly).

View-slot policy: we submit ONLY views that truthfully match a semantic slot.
view-01 (front three-quarter) -> front; view-04 (left side profile; front
points image-right) -> left. The top and undercarriage views are NOT
submitted in the back/right slots: mislabeling viewpoints invites exactly
the invented geometry the scorecard hard-fails (check 4d analogue).

Usage:
  set -a; source .env; set +a          # .env provides FAL_KEY (never commit)
  python3 run_tripo3d.py --label tripo-run-01 --dry-run
  python3 run_tripo3d.py --label tripo-run-01
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
ENDPOINT = "tripo3d/h3.1/multiview-to-3d"
REQUIRED_PACK_VERSION = "v1.1"

# Semantic slots per the verified schema: [front, left, back, right].
# None = no truthful asset for that slot; omitted from submission.
SLOT_VIEWS = {
    "front": "view-01-front-3q.png",
    "left": "view-04-side-profile.png",
    "back": None,
    "right": None,
}

GENERATION_ARGS = {
    # Pinned seeds -> reproducible geometry/texture. Vary ONLY via --seed.
    "model_seed": 20260827,
    "texture_seed": 20260827,
    "face_limit": 100000,          # comparability with Meshy target_polycount
    "geometry_quality": "detailed",
    "texture_quality": "detailed",
    "texture": True,
    "pbr": True,
    "quad": False,
    "auto_size": True,             # real-world meters; feeds dimension check
    "orientation": "default",
}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    version = manifest.get("pack_version")
    if version != REQUIRED_PACK_VERSION:
        sys.exit(f"input pack is {version!r}; this runner requires "
                 f"{REQUIRED_PACK_VERSION!r} (see pack_status in the manifest)")
    return manifest


def collect_inputs(manifest: dict) -> list[dict]:
    refs = []
    for slot, name in SLOT_VIEWS.items():
        if name is None:
            continue
        entry = manifest["images"].get(name)
        if entry is None:
            sys.exit(f"{name} missing from source-manifest.json")
        if entry.get("role") != "input":
            sys.exit(f"{name} role is {entry.get('role')!r}, not 'input'")
        path = IMAGES_DIR / name
        digest = sha256_of(path)
        if digest != entry["sha256"]:
            sys.exit(f"{name} hash mismatch vs manifest — refusing to submit")
        refs.append({"slot": slot, "name": name, "path": path,
                     "sha256": digest})
    if refs[0]["slot"] != "front":
        sys.exit("front view is required first")
    return refs


def pack_fingerprint(manifest: dict, refs: list[dict]) -> dict:
    combined = hashlib.sha256(
        (manifest["pack_version"]
         + "".join(sorted(r["sha256"] for r in refs))).encode()
    ).hexdigest()
    return {"pack_version": manifest["pack_version"], "pack_hash": combined}


def upload(path: Path, cache: dict) -> str:
    import fal_client
    digest = sha256_of(path)
    if digest not in cache:
        print(f"  uploading {path.name}…")
        cache[digest] = fal_client.upload_file(str(path))
        UPLOAD_CACHE.parent.mkdir(exist_ok=True)
        UPLOAD_CACHE.write_text(json.dumps(cache, indent=2))
    return cache[digest]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True,
                        help="run directory name under runs/")
    parser.add_argument("--seed", type=int, default=None,
                        help="override model_seed AND texture_seed")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    refs = collect_inputs(manifest)
    generation = dict(GENERATION_ARGS)
    if args.seed is not None:
        generation["model_seed"] = generation["texture_seed"] = args.seed

    run_dir = HERE / "runs" / args.label
    if run_dir.exists():
        sys.exit(f"{run_dir} already exists; pick a fresh label")

    submission = {
        "endpoint": ENDPOINT,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "inputs": [{k: str(v) if k == "path" else v for k, v in r.items()}
                   for r in refs],
        "slot_order": [r["slot"] for r in refs],
        "arguments": generation,
        **pack_fingerprint(manifest, refs),
    }

    if args.dry_run:
        print(json.dumps(submission, indent=2))
        print("\ndry run only — nothing submitted.")
        return

    if not os.environ.get("FAL_KEY"):
        sys.exit("FAL_KEY is not set (set -a; source .env; set +a)")

    import fal_client
    cache = (json.loads(UPLOAD_CACHE.read_text())
             if UPLOAD_CACHE.exists() else {})
    image_urls = [upload(r["path"], cache) for r in refs]

    print(f"submitting {ENDPOINT} …")
    handle = fal_client.submit(ENDPOINT,
                               arguments={"image_urls": image_urls,
                                          **generation})
    result = handle.get()

    run_dir.mkdir(parents=True)
    (run_dir / "submission.json").write_text(json.dumps(submission, indent=2))
    (run_dir / "result.json").write_text(json.dumps(result, indent=2))

    import urllib.request
    downloads = []
    urls = result.get("model_urls") or {}
    candidates = {"model_mesh": (result.get("model_mesh") or {}).get("url"),
                  **{k: (v or {}).get("url") for k, v in urls.items()},
                  "rendered_image":
                      (result.get("rendered_image") or {}).get("url")}
    for kind, url in candidates.items():
        if not url:
            continue
        name = f"{kind}-{Path(url.split('?')[0]).name}"
        target = run_dir / name
        print(f"  downloading {name}…")
        urllib.request.urlretrieve(url, target)
        downloads.append({"kind": kind, "file": name,
                          "sha256": sha256_of(target)})
    (run_dir / "downloads.json").write_text(json.dumps(downloads, indent=2))
    print(f"done → {run_dir}")


if __name__ == "__main__":
    main()
