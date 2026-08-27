"""Run one internal-only catalog H3.1 probe with hash, slot, and spend guards.

The per-product ``input-manifest.json`` is authoritative. Every selected file
is checked both against it and the corresponding immutable source-vault
manifest. A conservative $0.60 reservation is persisted before network use;
the provider request id is persisted immediately after submission.
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
ROOT = HERE.parent
CATALOG = HERE / "catalog-scans"
LEDGER = CATALOG / "spend-ledger.json"
UPLOAD_CACHE = CATALOG / "upload-cache.json"
ENDPOINT = "tripo3d/h3.1/multiview-to-3d"
SLOTS = ["front", "left", "back", "right"]
RIGHTS = "Tripo3D license check OPEN — do not ship"
GENERATION_ARGS = {
    "model_seed": 20260827,
    "texture_seed": 20260827,
    "face_limit": 100000,
    "geometry_quality": "detailed",
    "texture_quality": "detailed",
    "texture": True,
    "pbr": True,
    "quad": False,
    "auto_size": True,
    "orientation": "default",
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_entry(product: str, source_id: str) -> dict:
    manifest_path = ROOT / "source-vault" / product / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    matches = [s for s in manifest["sources"] if s.get("source_id") == source_id]
    if len(matches) != 1:
        sys.exit(f"{source_id}: expected exactly one source-vault entry")
    return matches[0]


def collect_inputs(product: str, manifest: dict) -> list[dict]:
    if not str(manifest.get("status", "")).startswith("READY"):
        sys.exit(f"{product}: input manifest is not ready for submission")
    refs = manifest.get("selected_inputs", [])
    if not 2 <= len(refs) <= 4:
        sys.exit(f"{product}: H3.1 requires 2-4 selected inputs")
    slots = [r.get("slot") for r in refs]
    expected = [slot for slot in SLOTS if slot in slots]
    if slots != expected or slots[0] != "front" or len(set(slots)) != len(slots):
        sys.exit(f"{product}: slots must be unique semantic order {SLOTS}, front first")
    checked = []
    for ref in refs:
        if ref.get("person_free") is not True:
            sys.exit(f"{product}/{ref.get('source_id')}: person_free must be true")
        path = ROOT / ref["local_path"]
        if not path.is_file():
            sys.exit(f"missing selected input: {path}")
        digest = sha256_of(path)
        if digest != ref.get("sha256"):
            sys.exit(f"{path.name}: hash mismatch vs input-manifest — refusing")
        source = source_entry(product, ref["source_id"])
        source_path = ROOT / "source-vault" / product / source["local_path"]
        if source_path.resolve() != path.resolve() or source.get("sha256") != digest:
            sys.exit(f"{path.name}: path/hash mismatch vs source-vault — refusing")
        checked.append({**ref, "path": path, "sha256": digest})
    return checked


def reserve(product: str, estimate: float) -> None:
    ledger = json.loads(LEDGER.read_text())
    if any(e["product"] == product for e in ledger["entries"]):
        sys.exit(f"{product}: spend-ledger already has an entry; refusing duplicate charge")
    total = sum(float(e["spend_usd"]) for e in ledger["entries"])
    if total + estimate > float(ledger["ceiling_usd"]):
        sys.exit(f"hard spend ceiling: {total:.2f} + {estimate:.2f} > {ledger['ceiling_usd']:.2f}")
    ledger["entries"].append({
        "product": product,
        "status": "reserved",
        "spend_usd": estimate,
        "request_id": None,
        "reserved_at": datetime.now(timezone.utc).isoformat(),
    })
    write_json(LEDGER, ledger)


def update_ledger(product: str, **updates: object) -> None:
    ledger = json.loads(LEDGER.read_text())
    entry = next(e for e in ledger["entries"] if e["product"] == product)
    entry.update(updates)
    write_json(LEDGER, ledger)


def upload(path: Path, cache: dict) -> str:
    import fal_client
    digest = sha256_of(path)
    if digest not in cache:
        print(f"  uploading {path.name}…", flush=True)
        cache[digest] = fal_client.upload_file(str(path))
        write_json(UPLOAD_CACHE, cache)
    return cache[digest]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    product_dir = CATALOG / args.product
    input_path = product_dir / "input-manifest.json"
    manifest = json.loads(input_path.read_text())
    if manifest.get("product") != args.product:
        sys.exit("product mismatch in input manifest")
    if manifest.get("internal_only") is not True or manifest.get("rights_note") != RIGHTS:
        sys.exit("internal-only rights guard missing")
    if manifest.get("approved_by", "sentinel") is not None:
        sys.exit("approved_by must be null")
    refs = collect_inputs(args.product, manifest)
    estimate = float(manifest.get("expected_provider_spend_usd", 0.60))
    fingerprint = hashlib.sha256("".join(r["sha256"] for r in refs).encode()).hexdigest()
    submission = {
        "endpoint": ENDPOINT,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "product": args.product,
        "inputs": [{k: str(v) if k == "path" else v for k, v in r.items()} for r in refs],
        "slot_order": [r["slot"] for r in refs],
        "input_fingerprint": fingerprint,
        "arguments": GENERATION_ARGS,
        "scope": "internal-only exploratory catalog capability probe",
        "estimated_spend_usd": estimate,
        "rights_note": RIGHTS,
        "approved_by": None,
    }
    if args.dry_run:
        print(json.dumps(submission, indent=2))
        print("\ndry run only — no upload, submission, or spend reservation.")
        return
    if not os.environ.get("FAL_KEY"):
        sys.exit("FAL_KEY is not set")
    if (product_dir / "submission.json").exists():
        sys.exit(f"{args.product}: submission.json exists; refusing duplicate run")

    write_json(product_dir / "submission.json", submission)
    reserve(args.product, estimate)
    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}
    image_urls = [upload(r["path"], cache) for r in refs]
    import fal_client
    print(f"submitting {ENDPOINT} …", flush=True)
    handle = fal_client.submit(ENDPOINT, arguments={"image_urls": image_urls, **GENERATION_ARGS})
    request = {
        "request_id": handle.request_id,
        "persisted_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "product": args.product,
    }
    write_json(product_dir / "request.json", request)
    manifest["request_id"] = handle.request_id
    write_json(input_path, manifest)
    update_ledger(args.product, status="submitted", request_id=handle.request_id)
    result = handle.get()
    write_json(product_dir / "result.json", result)

    import urllib.request
    downloads = []
    urls = result.get("model_urls") or {}
    candidates = {
        "model_mesh": (result.get("model_mesh") or {}).get("url"),
        **{k: (v or {}).get("url") for k, v in urls.items()},
        "rendered_image": (result.get("rendered_image") or {}).get("url"),
    }
    for kind, url in candidates.items():
        if not url:
            continue
        name = f"{kind}-{Path(url.split('?')[0]).name}"
        target = product_dir / name
        print(f"  downloading {name}…", flush=True)
        urllib.request.urlretrieve(url, target)
        downloads.append({"kind": kind, "file": name, "sha256": sha256_of(target)})
    write_json(product_dir / "downloads.json", downloads)
    update_ledger(args.product, status="complete", completed_at=datetime.now(timezone.utc).isoformat())
    print(f"done → {product_dir}")


if __name__ == "__main__":
    main()
