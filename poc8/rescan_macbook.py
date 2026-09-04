#!/usr/bin/env python3
"""POC 8 owner-approved MacBook twin re-scan (Tripo3D H3.1 multiview).

Replaces the failed catalog scan whose inputs mixed an open front with a
closed guide diagram (Gate 1 FAIL, 2026-08-30). Inputs here are one vault
original plus two derivation-recorded crops of a newly captured vault source
— all the same OPEN state, midnight, official Apple renders.

Owner approval: chat, 2026-08-29 ("rescan with tripo3d is fine").
Spend is reserved in poc8/out/spend-ledger.json under the POC 8 $10 ceiling.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "twins" / "macbook-rescan"
LEDGER = HERE / "out" / "spend-ledger.json"
UPLOAD_CACHE = HERE / "out" / "upload-cache.json"
ENDPOINT = "tripo3d/h3.1/multiview-to-3d"
RIGHTS = "Tripo3D license check OPEN — do not ship"
ESTIMATE_USD = 0.60
GENERATION_ARGS = {
    "model_seed": 20260829,
    "texture_seed": 20260829,
    "face_limit": 100000,
    "geometry_quality": "detailed",
    "texture_quality": "detailed",
    "texture": True,
    "pbr": True,
    "quad": False,
    "auto_size": True,
    "orientation": "default",
}

VAULT = ROOT / "source-vault" / "apple-macbook-air-13-m3"
INPUTS = [
    {
        "slot": "front",
        "source_id": "src_img_store_midnight",
        "path": VAULT / "images" / "store-color-midnight.jpg",
        "derivation": None,
        "semantic_assessment": "official open front view, midnight, clean background",
    },
    {
        "slot": "left",
        "source_id": "src_img_store_open_side_profiles",
        "path": HERE / "inputs" / "macbook-left-side-open.png",
        "derivation": "right half of store-open-side-profiles-midnight.jpg, whitespace-trimmed (unit showing the LEFT side: MagSafe + 2 Thunderbolt)",
        "semantic_assessment": "official open true-left profile, midnight",
    },
    {
        "slot": "right",
        "source_id": "src_img_store_open_side_profiles",
        "path": HERE / "inputs" / "macbook-right-side-open.png",
        "derivation": "left half of store-open-side-profiles-midnight.jpg, whitespace-trimmed (unit showing the RIGHT side: 3.5 mm jack)",
        "semantic_assessment": "official open true-right profile with headphone jack, midnight",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    if not os.environ.get("FAL_KEY"):
        key = os.environ.get("FAL_API_KEY")
        if key:
            os.environ["FAL_KEY"] = key
        else:
            sys.exit("FAL_KEY / FAL_API_KEY is not set")
    if (OUT / "submission.json").exists():
        sys.exit("submission.json exists; refusing duplicate spend")

    vault_manifest = json.loads((VAULT / "manifest.json").read_text())
    sources = {s["source_id"]: s for s in vault_manifest["sources"]}
    refs = []
    for spec in INPUTS:
        source = sources[spec["source_id"]]
        parent = VAULT / source["local_path"]
        if spec["derivation"] is None and parent.resolve() != spec["path"].resolve():
            sys.exit(f"{spec['slot']}: vault path mismatch")
        if sha256_of(parent) != source["sha256"]:
            sys.exit(f"{spec['slot']}: parent source hash mismatch — refusing")
        refs.append({
            "slot": spec["slot"],
            "source_id": spec["source_id"],
            "parent_sha256": source["sha256"],
            "input_sha256": sha256_of(spec["path"]),
            "local_path": str(spec["path"].relative_to(ROOT)),
            "derivation": spec["derivation"],
            "person_free": True,
            "semantic_assessment": spec["semantic_assessment"],
        })

    ledger = json.loads(LEDGER.read_text())
    spent = ledger.get("estimated_spend_usd", 0.0)
    if spent + ESTIMATE_USD > ledger["spend_ceiling_usd"]:
        sys.exit("spend ceiling would be exceeded")

    submission = {
        "endpoint": ENDPOINT,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "product": "apple-macbook-air-13-m3",
        "purpose": "POC8 Gate-1 remediation re-scan (owner approved 2026-08-29)",
        "inputs": refs,
        "slot_order": [r["slot"] for r in refs],
        "arguments": GENERATION_ARGS,
        "estimated_spend_usd": ESTIMATE_USD,
        "rights_note": RIGHTS,
        "internal_only": True,
        "approved_by": None,
    }
    write_json(OUT / "submission.json", submission)

    import fal_client
    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}

    def upload(path: Path) -> str:
        digest = sha256_of(path)
        if digest not in cache:
            print(f"  uploading {path.name}…", flush=True)
            cache[digest] = fal_client.upload_file(str(path))
            write_json(UPLOAD_CACHE, cache)
        return cache[digest]

    image_urls = [upload(Path(ROOT / r["local_path"])) for r in refs]
    print(f"submitting {ENDPOINT} …", flush=True)
    handle = fal_client.submit(
        ENDPOINT, arguments={"image_urls": image_urls, **GENERATION_ARGS})
    ledger["entries"].append({
        "request_id": handle.request_id,
        "label": "macbook-rescan-tripo-h31",
        "endpoint": ENDPOINT,
        "model": "tripo3d/h3.1",
        "estimated_cost_usd": ESTIMATE_USD,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "status": "submitted",
    })
    ledger["estimated_spend_usd"] = round(spent + ESTIMATE_USD, 2)
    ledger["remaining_ceiling_usd"] = round(
        ledger["spend_ceiling_usd"] - ledger["estimated_spend_usd"], 2)
    write_json(LEDGER, ledger)
    write_json(OUT / "request.json", {
        "request_id": handle.request_id,
        "persisted_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
    })

    result = handle.get()
    write_json(OUT / "result.json", result)
    for entry in ledger["entries"]:
        if entry.get("request_id") == handle.request_id:
            entry["status"] = "completed"
            entry["completed_at"] = datetime.now(timezone.utc).isoformat()
    write_json(LEDGER, ledger)

    import urllib.request
    urls = result.get("model_urls") or {}
    candidates = {
        "model_mesh": (result.get("model_mesh") or {}).get("url"),
        **{k: (v or {}).get("url") for k, v in urls.items()},
        "rendered_image": (result.get("rendered_image") or {}).get("url"),
    }
    downloads = []
    for kind, url in candidates.items():
        if not url:
            continue
        name = f"{kind}-{Path(url.split('?')[0]).name}"
        target = OUT / name
        print(f"  downloading {name}…", flush=True)
        with urllib.request.urlopen(url, timeout=300) as response, \
                target.open("wb") as fh:
            for chunk in iter(lambda: response.read(1 << 20), b""):
                fh.write(chunk)
        downloads.append({"kind": kind, "file": name,
                          "sha256": sha256_of(target),
                          "bytes": target.stat().st_size})
    write_json(OUT / "downloads.json", downloads)
    print(json.dumps(downloads, indent=2))


if __name__ == "__main__":
    main()
