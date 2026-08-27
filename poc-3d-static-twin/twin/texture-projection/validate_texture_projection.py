"""Validate the stopped texture-projection work order disposition."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TWIN = HERE.parent
ROOT = TWIN.parent.parent

EXPECTED_HASHES = {
    TWIN / "ready2jet-rigged.blend": "83d80dc107d46edecbe89d4d97dabf726887012dd4c0917f8da8e2961a9dc79d",
    TWIN / "action-spec.json": "42d43c0cab6d4f320a1c473c534020d1e91176ba2f6d9eec8e8ff5b944b5d3c2",
    TWIN / "joint-evidence.json": "e2a1ad9ddb091f00a59aba553287b844427ef8e84e846d8dc09ab9a98fc8f361",
    ROOT / "poc-3d-static-twin/runs/tripo-probe-01/pbr_model-k11lDWbp1BeH5sJR6lO6C_model.glb": "95e0fe44bba9a303b31849cfbec1d7d517d2ed2c6361ab505e025cf7ef80716b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures: list[str] = []
    for path, expected in EXPECTED_HASHES.items():
        actual = sha256(path) if path.exists() else "MISSING"
        if actual != expected:
            failures.append(f"protected hash mismatch: {path.relative_to(ROOT)} {actual}")

    coverage_path = HERE / "coverage.json"
    hours_path = HERE / "hours.json"
    report_path = HERE / "report.md"
    license_path = ROOT / "docs/pocs/tripo3d-license-review.md"
    for path in (coverage_path, hours_path, report_path, license_path, HERE / "audit_coverage.py"):
        if not path.exists():
            failures.append(f"required artifact missing: {path.relative_to(ROOT)}")

    if coverage_path.exists():
        coverage = json.loads(coverage_path.read_text())
        if coverage.get("status") != "STOP_GATE_FAILED":
            failures.append("coverage status is not STOP_GATE_FAILED")
        gate = coverage.get("gate", {})
        if gate.get("passed") is not False:
            failures.append("Stage A gate did not record a binding failure")
        if gate.get("minimum_fraction") != 0.60:
            failures.append("Stage A gate threshold changed")
        actual = gate.get("actual_fraction")
        if not isinstance(actual, (int, float)) or actual >= 0.60:
            failures.append("Stage A gate failure is numerically inconsistent")
        if coverage.get("measurement", {}).get("projection_distance_m") != 0.015:
            failures.append("projection distance is not the binding 15 mm")
        if coverage.get("external_spend_usd") != 0:
            failures.append("coverage audit reports nonzero external spend")
        if coverage.get("internal_only") is not True:
            failures.append("coverage audit is not internal-only")

    if hours_path.exists():
        hours = json.loads(hours_path.read_text())
        if hours.get("external_spend_usd") != 0:
            failures.append("hours ledger reports nonzero spend")
        stages = hours.get("stages", {})
        for name in ("B", "C", "D"):
            if stages.get(name, {}).get("elapsed_hours") != 0:
                failures.append(f"Stage {name} should have zero hours after the gate stop")
        if stages.get("E", {}).get("outcome") != "RESEARCH_COMPLETE_OWNER_DECISION_OPEN":
            failures.append("mandatory Stage E is not complete")

    forbidden = [
        TWIN / "ready2jet-textured.blend",
        HERE / "maps",
        HERE / "renders",
        ROOT / "evidence-packs/graco-ready2jet-2212125/derived-assets.json",
    ]
    for path in forbidden:
        if path.exists():
            failures.append(f"gate-forbidden Stage B-D artifact exists: {path.relative_to(ROOT)}")

    if license_path.exists():
        text = license_path.read_text()
        for required in (
            "https://www.tripo3d.ai/terms",
            "https://www.tripo3d.ai/pricing",
            "https://fal.ai/legal/terms-of-service",
            "https://fal.ai/legal/api-services",
            "https://fal.ai/models/tripo3d/h3.1/multiview-to-3d/api",
            "Owner decision:** `null`",
            "Approved by:** `null`",
            "INTERNAL ONLY",
        ):
            if required not in text:
                failures.append(f"license review missing required marker: {required}")

    result = {
        "status": "PASS" if not failures else "FAIL",
        "stage_a_gate_failed": True,
        "stages_b_to_d_absent": True,
        "stage_e_complete": license_path.exists(),
        "protected_inputs_unchanged": not any(item.startswith("protected hash") for item in failures),
        "external_spend_usd": 0,
        "failures": failures,
    }
    (HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
