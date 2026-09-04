#!/usr/bin/env python3
"""Run the bounded Stage B identity/proportion gate against official images."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import fal_client
import requests


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "out" / "gate1"
LEDGER = HERE / "out" / "spend-ledger.json"
UPLOAD_CACHE = HERE / "out" / "upload-cache.json"
CONFIG = json.loads((HERE / "config.json").read_text())
ENDPOINT = "fal-ai/any-llm/vision"
MODEL = "qwen/qwen3-vl-235b-a22b-instruct"
SCHEMA_URL = "https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/any-llm/vision"
PRICING_URL = "https://api.fal.ai/v1/models/pricing?endpoint_id=fal-ai/any-llm/vision"


def load_parse_verdict():
    """Reuse the application's fail-closed parser without importing app state."""
    path = ROOT / "app" / "keyframe_video.py"
    spec = importlib.util.spec_from_file_location("poc8_keyframe_video", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.parse_verdict


parse_verdict = load_parse_verdict()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def committed_spend(ledger: dict) -> float:
    return round(sum(float(entry["estimated_cost_usd"]) for entry in ledger["entries"]), 6)


def save_ledger(ledger: dict) -> None:
    spent = committed_spend(ledger)
    ceiling = float(ledger["spend_ceiling_usd"])
    ledger["estimated_spend_usd"] = spent
    ledger["remaining_ceiling_usd"] = round(ceiling - spent, 6)
    if spent > ceiling:
        raise SystemExit("STOP: ledger exceeds POC 8 hard spend ceiling")
    atomic_json(LEDGER, ledger)


def append_ledger(entry: dict) -> None:
    ledger = load_json(LEDGER)
    if any(item.get("request_id") == entry["request_id"] for item in ledger["entries"]):
        raise SystemExit(f"duplicate request id: {entry['request_id']}")
    ledger["entries"].append(entry)
    save_ledger(ledger)


def update_ledger(request_id: str, **changes: object) -> None:
    ledger = load_json(LEDGER)
    matches = [item for item in ledger["entries"] if item.get("request_id") == request_id]
    if len(matches) != 1:
        raise SystemExit(f"could not update unique ledger request {request_id}")
    matches[0].update(changes)
    save_ledger(ledger)


def preflight() -> float:
    if not os.environ.get("FAL_KEY"):
        raise SystemExit("Set FAL_KEY ephemerally before running Gate 1")
    schema_response = requests.get(SCHEMA_URL, timeout=30)
    schema_response.raise_for_status()
    schema = schema_response.json()
    candidates = [
        value
        for name, value in schema["components"]["schemas"].items()
        if name.lower().endswith("visioninput")
    ]
    if len(candidates) != 1:
        raise SystemExit(f"unexpected verifier input schemas: {len(candidates)}")
    fields = set(candidates[0].get("properties", {}))
    required = {"model", "prompt", "image_urls", "temperature", "max_tokens"}
    if not required <= fields:
        raise SystemExit(f"verifier schema missing fields: {sorted(required - fields)}")
    pricing_response = requests.get(
        PRICING_URL,
        headers={"Authorization": f"Key {os.environ['FAL_KEY']}"},
        timeout=30,
    )
    pricing_response.raise_for_status()
    prices = pricing_response.json().get("prices", [])
    if len(prices) != 1 or prices[0].get("unit") != "requests":
        raise SystemExit(f"unexpected verifier pricing response: {prices}")
    price = float(prices[0]["unit_price"])
    atomic_json(OUT / "live-preflight.json", {
        "verified_at": utcnow(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "schema_url": SCHEMA_URL,
        "pricing_url": PRICING_URL,
        "unit_price_usd": price,
        "unit": "requests",
        "required_fields": sorted(required),
        "status": "PASS",
    })
    return price


def upload(path: Path, cache: dict) -> str:
    digest = sha256(path)
    if digest not in cache:
        cache[digest] = fal_client.upload_file(str(path))
        atomic_json(UPLOAD_CACHE, cache)
    return cache[digest]


def prompt_for(product: str, attempt: int) -> str:
    if product == "bose":
        specifics = (
            "The official image shows the Bose QuietComfort Ultra Headphones (2nd Gen), "
            "including the padded headband, two asymmetric earcups/cushions, metal yokes, "
            "and visible control/port layout. The render need not include the cable already "
            "present in the official image."
        )
    else:
        specifics = (
            "The official image establishes the right-side profile of the Apple MacBook Air "
            "13-inch M3: a thin two-slab aluminum laptop with the single 3.5 mm jack on that "
            "right side. Reject detached debris, invented fins/callouts, extra ports, impossible "
            "stacking, or a shape that is not a credible MacBook Air."
        )
    retry = (
        "This is the second and final camera/framing attempt; remain strict and fail if identity "
        "is still not visibly established."
        if attempt == 2
        else "This is the first fixed-camera attempt."
    )
    return f"""You are the strict Stage B gate for a product digital twin.
Image 1 is an authoritative official product image. Image 2 is an INTERNAL-ONLY
deterministic render of a repaired Tripo3D scan. Judge the PRODUCT GEOMETRY and
recognizable identity, not background, lighting, watermark, camera crop, or
the render's missing presentation props. {specifics} {retry}

Fail if the rendered object is not recognizably the same product/model family,
if major proportions are implausible relative to Image 1, or if major parts are
missing/invented. Answer JSON only:
{{
  "recognizable_same_product": {{"answer":"yes|no|unsure","evidence":"..."}},
  "major_proportions_plausible": {{"answer":"yes|no|unsure","evidence":"..."}},
  "missing_or_invented_major_parts": {{"answer":"yes|no|unsure","evidence":"..."}},
  "verdict":"pass|fail",
  "verdict_reason":"..."
}}"""


def verify(product: str, attempt: int, unit_price: float, cache: dict) -> dict:
    spec = CONFIG["products"][product]
    official = ROOT / spec["official_image"]
    rendered = OUT / f"attempt-{attempt}" / f"{product}.png"
    if not official.is_file() or not rendered.is_file():
        raise SystemExit(f"missing verifier input for {product} attempt {attempt}")
    ledger = load_json(LEDGER)
    if committed_spend(ledger) + unit_price > float(ledger["spend_ceiling_usd"]):
        raise SystemExit("STOP: next Gate 1 request would exceed the $10 ceiling")

    arguments = {
        "model": MODEL,
        "prompt": prompt_for(product, attempt),
        "image_urls": [upload(official, cache), upload(rendered, cache)],
        "temperature": 0,
        "max_tokens": 700,
    }
    check_dir = OUT / f"attempt-{attempt}" / product
    check_dir.mkdir(parents=True, exist_ok=True)
    atomic_json(check_dir / "submission.json", {
        "prepared_at": utcnow(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "arguments": arguments,
        "inputs": [
            {"role": "official_ground_truth", "path": str(official.relative_to(ROOT)), "sha256": sha256(official)},
            {"role": "repaired_twin_render", "path": str(rendered.relative_to(ROOT)), "sha256": sha256(rendered)},
        ],
        "estimated_cost_usd": unit_price,
        "internal_only": True,
        "approved_by": None,
    })
    handle = fal_client.submit(ENDPOINT, arguments=arguments)
    request = {
        "request_id": handle.request_id,
        "submitted_at": utcnow(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "estimated_cost_usd": unit_price,
        "response_url": handle.response_url,
        "status_url": handle.status_url,
        "cancel_url": handle.cancel_url,
    }
    atomic_json(check_dir / "request.json", request)
    append_ledger({
        "request_id": handle.request_id,
        "label": f"gate1-attempt-{attempt}-{product}",
        "endpoint": ENDPOINT,
        "model": MODEL,
        "estimated_cost_usd": unit_price,
        "submitted_at": request["submitted_at"],
        "status": "submitted",
    })
    print(f"{product} attempt {attempt}: request {handle.request_id} persisted", flush=True)
    try:
        result = handle.get()
    except Exception as error:
        update_ledger(handle.request_id, status="provider_error", error=repr(error), updated_at=utcnow())
        raise
    verdict = parse_verdict(result)
    atomic_json(check_dir / "result.json", result)
    atomic_json(check_dir / "verdict.json", verdict)
    update_ledger(handle.request_id, status="completed", completed_at=utcnow())
    return {
        "attempt": attempt,
        "request_id": handle.request_id,
        "verdict": verdict.get("verdict", "fail"),
        "verdict_reason": verdict.get("verdict_reason", "missing reason"),
        "verdict_path": str((check_dir / "verdict.json").relative_to(ROOT)),
    }


def main() -> None:
    stage = load_json(OUT / "stage-b-report.json")
    if not stage.get("dimension_gate_all_pass"):
        raise SystemExit("STOP: Stage B dimension gate did not pass; identity requests forbidden")
    existing = OUT / "gate1-verdict.json"
    if existing.exists():
        raise SystemExit(f"fresh Gate 1 verdict required; existing file: {existing}")
    unit_price = preflight()
    cache = load_json(UPLOAD_CACHE) if UPLOAD_CACHE.exists() else {}

    results = {"bose": [], "macbook": []}
    first = {product: verify(product, 1, unit_price, cache) for product in results}
    for product, result in first.items():
        results[product].append(result)
    # Exactly one retry, and only for products that failed the first attempt.
    for product in results:
        if results[product][-1]["verdict"] != "pass":
            results[product].append(verify(product, 2, unit_price, cache))

    product_pass = {
        product: attempts[-1]["verdict"] == "pass" for product, attempts in results.items()
    }
    gate_pass = all(product_pass.values())
    verdict = {
        "stage": "B / Gate 1",
        "completed_at": utcnow(),
        "dimension_gate": "PASS",
        "products": results,
        "product_identity_pass": product_pass,
        "identity_gate": "PASS" if gate_pass else "FAIL",
        "gate1_status": "PASS" if gate_pass else "FAIL",
        "next_step": (
            "Run Stage C cable gate." if gate_pass else
            "STOP-AND-REPORT: one or both twins need a new scan; no connection scene may be authored from these twins."
        ),
        "external_spend_usd": committed_spend(load_json(LEDGER)),
        "internal_only": True,
        "approved_by": None,
    }
    atomic_json(existing, verdict)
    stage["identity_gate_status"] = verdict["identity_gate"]
    stage["gate1_status"] = verdict["gate1_status"]
    stage["next_step"] = verdict["next_step"]
    stage["gate1_verdict"] = str(existing.relative_to(ROOT))
    atomic_json(OUT / "stage-b-report.json", stage)
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()

