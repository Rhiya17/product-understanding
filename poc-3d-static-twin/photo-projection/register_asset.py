"""Register a completed, camera-qualified internal-only derived asset."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text())


def state_dir(lane: str, state: str | None) -> Path:
    base = HERE / lane
    return base / state if state else base


def register(lane: str, state: str | None) -> None:
    spec = CONFIG["lanes"][lane]
    directory = state_dir(lane, state)
    render = json.loads((directory / "render-manifest.json").read_text())
    cameras = json.loads((directory / "camera-gates/camera-matches.json").read_text())
    coverage = json.loads((directory / "coverage.json").read_text())
    sources = json.loads((HERE / lane / "source-preparation.json").read_text())
    source_by_id = {source["source_id"]: source for source in sources["sources"]}
    qualified = [source_id for source_id, record in cameras["matches"].items() if record["status"] == "PASS"]
    if not qualified:
        raise SystemExit("refusing to register an asset with no passing camera match")
    minimum_iou = min(cameras["matches"][source_id]["silhouette_iou"] for source_id in qualified)
    registry_path = ROOT / "evidence-packs" / spec["vault_slug"] / "derived-assets.json"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text())
    else:
        registry = {"schema_version": 1, "product_id": spec["product_id"], "assets": []}
    if registry["product_id"] != spec["product_id"]:
        raise SystemExit("derived-assets product id mismatch")
    target_to_suffix = {target: target.replace("-", "_") for target in render["outputs"]}
    for target, output in render["outputs"].items():
        asset_id = f"derived_{lane}{'_' + state if state else ''}_{target_to_suffix[target]}_20260827"
        asset = {
            "asset_id": asset_id,
            "type": "TURNTABLE_GIF" if "turntable" in target else "FOLD_GIF",
            "local_path": output["gif_local_path"],
            "sha256": output["gif_sha256"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "provider": "local Blender 5.2.0 LTS deterministic photo projection",
            "geometry_local_path": render["geometry_blend_local_path"],
            "geometry_sha256": render["geometry_blend_sha256"],
            "geometry_claim_ids": spec.get("claim_ids", []),
            "camera_gate": {"minimum_iou": minimum_iou, "threshold": CONFIG["camera_gate_iou"],
                            "record": render["camera_matches_local_path"]},
            "coverage": {"overall_fraction": coverage["overall_coverage_fraction"],
                         "fallback_fraction": coverage["overall_fallback_fraction"],
                         "record": render["coverage_local_path"]},
            "input_sources": [
                {
                    "source_id": source_id,
                    "parent_source_id": source_by_id[source_id]["parent_source_id"],
                    "parent_sha256": source_by_id[source_id]["parent_sha256"],
                    "masked_texture_sha256": source_by_id[source_id]["masked_texture_sha256"],
                }
                for source_id in qualified
            ],
            "scripts": render["scripts"] + ["poc-3d-static-twin/photo-projection/register_asset.py"],
            "license_status": "OPEN_MANUFACTURER_IMAGERY_REUSE_REVIEW",
            "rights_note": render["rights_note"],
            "tripo_texture_ancestry": False,
            "approved_by": None,
            "internal_only": True,
            "external_spend_usd": 0,
        }
        existing = next((index for index, item in enumerate(registry["assets"])
                         if item.get("asset_id") == asset_id), None)
        if existing is None:
            registry["assets"].append(asset)
        else:
            if registry["assets"][existing].get("approved_by") is not None:
                raise SystemExit(f"refusing to overwrite approved asset {asset_id}")
            registry["assets"][existing] = asset
    registry_path.write_text(json.dumps(registry, indent=2) + "\n")
    print(registry_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=("levoit", "macbook", "bose"))
    parser.add_argument("--state", choices=("open", "closed"))
    args = parser.parse_args()
    register(args.lane, args.state)


if __name__ == "__main__":
    main()
