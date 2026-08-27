#!/usr/bin/env python3
"""Verify and persist the live fal Wan VACE depth schema before POC 7 spend."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "poc7-preflight"
ENDPOINT = "fal-ai/wan-vace-14b/depth"
SCHEMA_URL = (
    "https://fal.ai/api/openapi/queue/openapi.json"
    "?endpoint_id=fal-ai/wan-vace-14b/depth"
)
MODEL_URL = "https://fal.ai/models/fal-ai/wan-vace-14b/depth"
DOCS_URL = MODEL_URL + "/api"
REQUIRED_FIELDS = {
    "prompt",
    "negative_prompt",
    "video_url",
    "ref_image_urls",
    "preprocess",
    "match_input_num_frames",
    "match_input_frames_per_second",
    "resolution",
    "num_inference_steps",
    "seed",
}
EXPECTED_RESOLUTIONS = {"480p", "720p"}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def input_schema(openapi: dict) -> dict:
    schemas = openapi["components"]["schemas"]
    candidates = [
        value
        for key, value in schemas.items()
        if key.lower().endswith("depthinput")
    ]
    if len(candidates) != 1:
        raise SystemExit(f"expected one depth input schema, found {len(candidates)}")
    return candidates[0]


def parse_prices(page: str) -> tuple[dict[str, float], int]:
    plain = re.sub(r"<[^>]+>", " ", page)
    plain = re.sub(r"\s+", " ", plain)
    pattern = re.compile(
        r"\$(?P<price>0\.\d+) per video second for (?P<resolution>\d+p)"
    )
    prices = {m.group("resolution"): float(m.group("price")) for m in pattern.finditer(plain)}
    fps_match = re.search(r"Video seconds are calculated at (\d+) frames per second", plain)
    if not fps_match:
        raise SystemExit("could not verify fal billing FPS from the live model page")
    if not EXPECTED_RESOLUTIONS <= prices.keys():
        raise SystemExit(f"live pricing is missing required resolutions: {prices}")
    return prices, int(fps_match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    schema_response = requests.get(SCHEMA_URL, timeout=30)
    schema_response.raise_for_status()
    openapi = schema_response.json()
    model_response = requests.get(MODEL_URL, timeout=30)
    model_response.raise_for_status()

    schema = input_schema(openapi)
    properties = schema.get("properties", {})
    missing = sorted(REQUIRED_FIELDS - properties.keys())
    if missing:
        raise SystemExit(f"live schema is missing required fields: {missing}")
    resolutions = set(properties["resolution"].get("enum", []))
    if not EXPECTED_RESOLUTIONS <= resolutions:
        raise SystemExit(f"live schema lacks required resolutions: {sorted(resolutions)}")
    prices, billing_fps = parse_prices(model_response.text)

    fetched_at = datetime.now(timezone.utc).isoformat()
    record = {
        "verified_at": fetched_at,
        "endpoint": ENDPOINT,
        "schema_url": SCHEMA_URL,
        "model_url": MODEL_URL,
        "documentation_url": DOCS_URL,
        "schema_sha256": hashlib.sha256(canonical_bytes(openapi)).hexdigest(),
        "verified_fields": sorted(REQUIRED_FIELDS),
        "resolution_enum": sorted(resolutions),
        "alternative_not_run": "fal-ai/wan-vace-14b/pose",
        "pricing_usd_per_billed_video_second": prices,
        "billing_frames_per_second": billing_fps,
        "status": "PASS",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    atomic_json(args.output / "live-openapi.json", openapi)
    atomic_json(args.output / "schema-verification.json", record)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
