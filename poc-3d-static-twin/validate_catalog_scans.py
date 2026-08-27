"""Validate Stage T scan/skip completeness, provenance, hashes, and rights."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOG = HERE / "catalog-scans"
RIGHTS = "Tripo3D license check OPEN — do not ship"
PRODUCTS = [
    "levoit-core-300s",
    "graco-snugride-35-lite-lx",
    "bose-qc-ultra-headphones",
    "apple-macbook-air-13-m3",
]
PRODUCT_IDS = {
    "bose-qc-ultra-headphones": "prod_bose_qc_ultra_headphones",
    "apple-macbook-air-13-m3": "prod_apple_macbook_air_13_m3",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_input_hashes(product: str, manifest: dict) -> None:
    source_manifest = load(ROOT / "source-vault" / product / "manifest.json")
    by_id = {s["source_id"]: s for s in source_manifest["sources"]}
    for ref in manifest.get("selected_inputs", []):
        require(ref.get("person_free") is True, f"{product}: person-free guard")
        path = ROOT / ref["local_path"]
        require(path.is_file(), f"{product}: selected input missing")
        actual = digest(path)
        require(actual == ref["sha256"], f"{product}: input-manifest hash")
        source = by_id[ref["source_id"]]
        require(source["sha256"] == actual, f"{product}: source-vault hash")


def main() -> None:
    ledger = load(CATALOG / "spend-ledger.json")
    entries = {e["product"]: e for e in ledger["entries"]}
    total = sum(float(e["spend_usd"]) for e in entries.values())
    require(total <= float(ledger["ceiling_usd"]), "spend ceiling")
    checks = []
    for product in PRODUCTS:
        product_dir = CATALOG / product
        manifest = load(product_dir / "input-manifest.json")
        require(manifest["rights_note"] == RIGHTS, f"{product}: rights note")
        require(manifest["approved_by"] is None, f"{product}: approved_by")
        require(manifest["internal_only"] is True, f"{product}: internal only")
        validate_input_hashes(product, manifest)
        entry = entries[product]
        if manifest["status"].startswith("SKIPPED"):
            require(not manifest["selected_inputs"], f"{product}: skipped inputs")
            require(manifest["request_id"] is None, f"{product}: skipped request")
            require(entry["status"] == "skipped" and entry["spend_usd"] == 0,
                    f"{product}: skipped spend")
            checks.append({"product": product, "status": "PASS_SKIP"})
            continue

        request = load(product_dir / "request.json")
        submission = load(product_dir / "submission.json")
        require(request["request_id"] == manifest["request_id"] == entry["request_id"],
                f"{product}: request id persistence")
        require(entry["status"] == "complete", f"{product}: ledger completion")
        require(submission["rights_note"] == RIGHTS and submission["approved_by"] is None,
                f"{product}: submission rights")
        require([x["sha256"] for x in submission["inputs"]] ==
                [x["sha256"] for x in manifest["selected_inputs"]],
                f"{product}: submitted input hashes")
        downloads = load(product_dir / "downloads.json")
        for item in downloads:
            require(digest(product_dir / item["file"]) == item["sha256"],
                    f"{product}: download hash {item['file']}")
        rights = load(product_dir / "artifact-rights.json")
        require(rights["rights_note"] == RIGHTS and rights["approved_by"] is None,
                f"{product}: artifact rights")
        for item in rights["artifacts"]:
            require(digest(product_dir / item["file"]) == item["sha256"],
                    f"{product}: artifact hash {item['file']}")
        analysis = load(product_dir / "mesh-analysis.json")
        require(analysis["rights_note"] == RIGHTS and analysis["approved_by"] is None,
                f"{product}: analysis rights")
        render = load(product_dir / "render-manifest.json")
        gif = product_dir / render["gif"]
        require(digest(gif) == render["gif_sha256"], f"{product}: gif hash")
        with Image.open(gif) as im:
            require(im.n_frames == 24 and im.size == (1024, 1024),
                    f"{product}: gif dimensions/frames")
        require(len(render["frame_sha256"]) == 24, f"{product}: frame manifest")
        for item in render["frame_sha256"]:
            frame = product_dir / render["frames_dir"] / item["file"]
            require(digest(frame) == item["sha256"], f"{product}: frame hash")
        derived = load(ROOT / "evidence-packs" / product / "derived-assets.json")
        require(derived["product_id"] == PRODUCT_IDS[product], f"{product}: product id")
        asset = derived["assets"][0]
        require(asset["request_id"] == request["request_id"], f"{product}: derived request")
        require(asset["sha256"] == digest(ROOT / asset["local_path"]),
                f"{product}: derived hash")
        require(asset["rights_note"] == RIGHTS and asset["approved_by"] is None,
                f"{product}: derived rights")
        checks.append({
            "product": product,
            "status": "PASS_SCAN",
            "request_id": request["request_id"],
            "spend_usd": entry["spend_usd"],
        })
    report = {
        "status": "PASS",
        "provider_spend_usd": total,
        "spend_ceiling_usd": ledger["ceiling_usd"],
        "checks": checks,
    }
    (CATALOG / "validation-catalog-scans.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
