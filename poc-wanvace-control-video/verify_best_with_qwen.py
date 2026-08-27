#!/usr/bin/env python3
"""Run four small advisory Qwen checks on the best POC 7 run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import fal_client
import requests


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT_ROOT = HERE / "out"
ENDPOINT = "fal-ai/any-llm/vision"
MODEL = "qwen/qwen3-vl-235b-a22b-instruct"
SCHEMA_URL = (
    "https://fal.ai/api/openapi/queue/openapi.json"
    "?endpoint_id=fal-ai/any-llm/vision"
)
PRICING_URL = "https://api.fal.ai/v1/models/pricing?endpoint_id=fal-ai/any-llm/vision"
LEDGER = OUT_ROOT / "poc7-spend-ledger.json"
UPLOAD_CACHE = OUT_ROOT / "poc7-qwen-upload-cache.json"
SPEND_CEILING_USD = 15.0
OFFICIAL_OPEN = REPO / "source-vault" / "graco-ready2jet-2212125" / "images" / "view-01-front-3q.png"
OFFICIAL_FOLDED = REPO / "poc-seedance-keyframe-fold" / "references" / "folded-product-only.png"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temp.replace(path)


def input_schema(openapi: dict) -> dict:
    candidates = [
        schema
        for name, schema in openapi["components"]["schemas"].items()
        if name.lower().endswith("visioninput")
    ]
    if len(candidates) != 1:
        raise SystemExit(f"expected one vision input schema, found {len(candidates)}")
    return candidates[0]


def live_preflight(output_dir: Path) -> float:
    schema_response = requests.get(SCHEMA_URL, timeout=30)
    schema_response.raise_for_status()
    openapi = schema_response.json()
    properties = input_schema(openapi).get("properties", {})
    needed = {"model", "prompt", "image_urls", "temperature", "max_tokens"}
    if not needed <= properties.keys():
        raise SystemExit(f"Qwen verifier live schema missing fields: {sorted(needed - properties.keys())}")
    pricing_response = requests.get(
        PRICING_URL,
        headers={"Authorization": f"Key {os.environ['FAL_KEY']}"},
        timeout=30,
    )
    pricing_response.raise_for_status()
    prices = pricing_response.json().get("prices", [])
    if len(prices) != 1 or prices[0].get("unit") != "requests":
        raise SystemExit(f"unexpected Qwen verifier pricing: {prices}")
    price = float(prices[0]["unit_price"])
    atomic_json(output_dir / "live-preflight.json", {
        "verified_at": utcnow(),
        "endpoint": ENDPOINT,
        "schema_url": SCHEMA_URL,
        "schema_sha256": hashlib.sha256(
            json.dumps(openapi, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "verified_fields": sorted(needed),
        "pricing_url": PRICING_URL,
        "unit_price_usd": price,
        "unit": "requests",
        "status": "PASS",
    })
    return price


def load_ledger() -> dict:
    return json.loads(LEDGER.read_text())


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


def upload(path: Path, cache: dict) -> str:
    digest = sha256_of(path)
    if digest not in cache:
        cache[digest] = fal_client.upload_file(str(path))
        atomic_json(UPLOAD_CACHE, cache)
    return cache[digest]


def parse_json_output(result: dict) -> object:
    raw = result.get("output", "")
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0]
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"parse_error": True, "raw_output": raw}


def questions(run_dir: Path) -> list[dict]:
    frames = run_dir / "frames"
    output_samples = [frames / f"frame-{index:04d}.png" for index in (1, 20, 39, 58, 77, 96)]
    return [
        {
            "slug": "same-product",
            "prompt": (
                "Image 1 is an official product-only Kingston reference image. Images 2-7 are "
                "chronological frames from a candidate realism-skin video. Is the exact same "
                "product identity preserved across the candidate frames? Treat any invented or "
                "missing part, added handle control, altered belly-bar material/color, or changed "
                "wheel design as NO. Answer JSON only: "
                '{"answer":"yes|no|unsure","evidence":"visible concise evidence"}'
            ),
            "paths": [OFFICIAL_OPEN, *output_samples],
        },
        {
            "slug": "fixed-camera",
            "prompt": (
                "These six images are chronological frames from one candidate video. Apart from "
                "the product's articulated shape changing, do the camera viewpoint and the "
                "product's orientation relative to the camera remain fixed, with no pan, orbit, "
                "zoom, or reframing? Answer JSON only: "
                '{"answer":"yes|no|unsure","evidence":"visible concise evidence"}'
            ),
            "paths": output_samples,
        },
        {
            "slug": "motion-direction",
            "prompt": (
                "This contact sheet has five chronological rows. In every row the deterministic "
                "control is on the left and the candidate realism-skin output at the same timestamp "
                "is on the right. Does the candidate's product silhouette progress in the same "
                "direction and fold-stage order as the control across all five rows? Answer JSON "
                'only: {"answer":"yes|no|unsure","evidence":"visible concise evidence"}'
            ),
            "paths": [run_dir / "contact-sheet.png"],
        },
        {
            "slug": "reaches-folded-state",
            "prompt": (
                "Image 1 is an official product-only folded-state reference. Image 2 is the first "
                "candidate frame and Image 3 is the final candidate frame. By Image 3, does the "
                "candidate clearly reach a compact folded state rather than remain open or only "
                "part-folded? Answer JSON only: "
                '{"answer":"yes|no|unsure","evidence":"visible concise evidence"}'
            ),
            "paths": [OFFICIAL_FOLDED, frames / "frame-0001.png", frames / "frame-0096.png"],
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    if not os.environ.get("FAL_KEY"):
        raise SystemExit("Set FAL_KEY ephemerally before running")
    run_dir = OUT_ROOT / args.label
    verification_dir = run_dir / "verification" / "qwen"
    if verification_dir.exists():
        raise SystemExit(f"fresh verifier directory required: {verification_dir}")
    verification_dir.mkdir(parents=True)
    unit_price = live_preflight(verification_dir)
    checks = questions(run_dir)
    for check in checks:
        for path in check["paths"]:
            if not path.is_file():
                raise SystemExit(f"missing verifier input: {path}")
    ledger = load_ledger()
    if committed_spend(ledger) + unit_price * len(checks) > SPEND_CEILING_USD:
        raise SystemExit("STOP: Qwen advisory checks would exceed the hard spend ceiling")
    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}

    for check in checks:
        check_dir = verification_dir / check["slug"]
        check_dir.mkdir()
        urls = [upload(path, cache) for path in check["paths"]]
        arguments = {
            "model": MODEL,
            "prompt": check["prompt"],
            "image_urls": urls,
            "temperature": 0,
            "max_tokens": 500,
        }
        atomic_json(check_dir / "submission.json", {
            "prepared_at": utcnow(),
            "endpoint": ENDPOINT,
            "model": MODEL,
            "question": check["slug"],
            "arguments": arguments,
            "inputs": [
                {"path": str(path), "sha256": sha256_of(path)} for path in check["paths"]
            ],
            "estimated_cost_usd": unit_price,
            "advisory_only": True,
            "internal_only": True,
            "approved_by": None,
        })
        handle = fal_client.submit(ENDPOINT, arguments=arguments)
        request = {
            "request_id": handle.request_id,
            "submitted_at": utcnow(),
            "endpoint": ENDPOINT,
            "question": check["slug"],
            "estimated_cost_usd": unit_price,
            "response_url": handle.response_url,
            "status_url": handle.status_url,
            "cancel_url": handle.cancel_url,
        }
        atomic_json(check_dir / "request.json", request)
        append_ledger({
            "request_id": handle.request_id,
            "label": f"{args.label}-qwen-{check['slug']}",
            "endpoint": ENDPOINT,
            "estimated_cost_usd": unit_price,
            "submitted_at": request["submitted_at"],
            "status": "submitted",
        })
        print(f"{check['slug']} request id persisted: {handle.request_id}", flush=True)
        try:
            result = handle.get()
        except Exception as error:
            update_ledger(handle.request_id, status="provider_error", error=repr(error), updated_at=utcnow())
            raise
        atomic_json(check_dir / "result.json", result)
        atomic_json(check_dir / "verdict.json", parse_json_output(result))
        update_ledger(handle.request_id, status="completed", completed_at=utcnow())
    print(verification_dir)


if __name__ == "__main__":
    main()
