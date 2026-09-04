#!/usr/bin/env python3
"""Validate POC 8's fail-closed terminal state and audit trail."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "out"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_internal_watermark(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    top = image.crop((0, 0, width, max(1, height // 4)))
    pixels = list(top.getdata())
    red = sum(1 for r, g, b in pixels if r > 120 and r > g * 1.25 and r > b * 1.25)
    assert red / len(pixels) > 0.002, f"internal watermark not detected in {path}"


def main() -> None:
    config = load(HERE / "config.json")
    assert config["internal_only"] is True and config["approved_by"] is None
    assert config["external_spend_ceiling_usd"] == 10.0

    stage = load(OUT / "gate1/stage-b-report.json")
    gate = load(OUT / "gate1/gate1-verdict.json")
    assert stage["dimension_gate_all_pass"] is True
    assert gate["dimension_gate"] == "PASS"
    assert gate["product_identity_pass"] == {"bose": True, "macbook": False}
    assert gate["identity_gate"] == gate["gate1_status"] == "FAIL"
    assert len(gate["products"]["bose"]) == 1
    assert len(gate["products"]["macbook"]) == 2
    assert [item["verdict"] for item in gate["products"]["macbook"]] == ["fail", "fail"]

    for product in ("bose", "macbook"):
        repair = load(OUT / f"gate1/{product}/scale-repair.json")
        assert repair["dimension_gate"] == "PASS"
        assert repair["worst_axis_error_percent"] <= 5.0
        source = ROOT / repair["source_glb"]
        assert source.is_file() and sha256(source) == repair["source_glb_sha256"]

    request_ids = []
    for product, attempts in gate["products"].items():
        for attempt in attempts:
            request_ids.append(attempt["request_id"])
            verdict_path = ROOT / attempt["verdict_path"]
            assert verdict_path.is_file()
            assert load(verdict_path)["verdict"] == attempt["verdict"]
    assert len(request_ids) == len(set(request_ids)) == 3

    ledger = load(OUT / "spend-ledger.json")
    ledger_ids = [entry["request_id"] for entry in ledger["entries"]]
    # Run 3 history: 3 VLM checks from archived run 1 (gate1-run1-fail), the
    # owner-approved Tripo re-scan, and 3 VLM checks from the final gate run.
    assert set(request_ids) <= set(ledger_ids)
    archived = load(OUT / "gate1-run1-fail/gate1-verdict.json")
    archived_ids = [a["request_id"] for p_ in archived["products"].values() for a in p_]
    rescan = load(HERE / "twins/macbook-rescan/request.json")
    assert rescan["request_id"] in ledger_ids
    assert set(archived_ids) <= set(ledger_ids)
    assert len(ledger_ids) == len(set(ledger_ids)) == 10
    assert all(entry["status"] == "completed" for entry in ledger["entries"])
    total = round(sum(e["estimated_cost_usd"] for e in ledger["entries"]), 2)
    assert ledger["estimated_spend_usd"] == total == 0.69
    assert ledger["estimated_spend_usd"] <= ledger["spend_ceiling_usd"] == 10.0
    assert ledger["remaining_ceiling_usd"] == round(10.0 - total, 2)

    for attempt, product in ((1, "bose"), (1, "macbook"), (2, "macbook")):
        assert_internal_watermark(OUT / f"gate1/attempt-{attempt}/{product}.png")
    contact = OUT / "gate1/contact-sheet.png"
    assert contact.is_file()

    # Governing rule 4 requires absence of downstream artifacts after a twice-failed gate.
    forbidden = [
        HERE / "scene.blend",
        HERE / "shot-1.mp4",
        HERE / "shot-2.mp4",
        HERE / "connection.mp4",
        OUT / "vace",
        OUT / "seedance",
    ]
    assert not any(path.exists() for path in forbidden), "downstream artifact exists despite Gate 1 failure"

    # Failed request IDs must not leak into registered pack data.
    for relative in (
        "evidence-packs/bose-qc-ultra-headphones/derived-assets.json",
        "evidence-packs/bose-qc-ultra-headphones/media-bindings.json",
    ):
        path = ROOT / relative
        if path.exists():
            content = path.read_text()
            assert not any(request_id in content for request_id in request_ids), (
                f"failed POC 8 request registered in {relative}"
            )

    findings = ROOT / "docs/pocs/poc8-connection-scene-findings.md"
    text = findings.read_text()
    for phrase in (
        "Gate 1: FAIL",
        "$0.69",
        "NOT RUN",
        "No registration",
        "INTERNAL ONLY — TWIN RENDER",
        "re-scan",
        "port-level detail",
    ):
        assert phrase in text, f"findings missing: {phrase}"

    result = {
        "status": "PASS",
        "validated_terminal_state": "POC8 correctly stopped at failed Gate 1",
        "gate1": "FAIL",
        "dimension_gate": "PASS",
        "bose_identity": "PASS",
        "macbook_identity": "FAIL_AFTER_TWO_ATTEMPTS",
        "request_ids": request_ids,
        "spend_usd": ledger["estimated_spend_usd"],
        "spend_ceiling_usd": ledger["spend_ceiling_usd"],
        "downstream_artifacts_absent": True,
        "registration_absent": True,
        "internal_only": True,
        "approved_by": None,
    }
    (OUT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

