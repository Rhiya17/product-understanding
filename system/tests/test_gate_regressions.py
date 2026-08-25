import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = REPO_ROOT / "evidence-packs" / "validate.py"
PRODUCT = "graco-ready2jet-2212125"


def stage_real_pack(root):
    evidence_root = root / "evidence-packs"
    evidence_root.mkdir(parents=True)
    shutil.copytree(REPO_ROOT / "evidence-packs" / PRODUCT,
                    evidence_root / PRODUCT)
    os.symlink(REPO_ROOT / "evidence-packs" / "workorders",
               evidence_root / "workorders", target_is_directory=True)
    vault_root = root / "source-vault"
    vault_root.mkdir()
    os.symlink(REPO_ROOT / "source-vault" / PRODUCT,
               vault_root / PRODUCT, target_is_directory=True)
    return evidence_root / PRODUCT / "claims.json"


def run_gate(claims_path):
    return subprocess.run(
        [sys.executable, str(GATE), str(claims_path)],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False)


def rewrite_claims(path, claims):
    path.write_text(json.dumps(claims, indent=2) + "\n", encoding="utf-8")


def find_box(value):
    if isinstance(value, dict):
        if "bounding_box" in value:
            return value
        for nested in value.values():
            found = find_box(nested)
            if found is not None:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = find_box(nested)
            if found is not None:
                return found
    return None


def test_existing_gate_traps_still_hard_fail_on_staged_pack(tmp_path):
    fabricated_path = stage_real_pack(tmp_path / "fabricated")
    fabricated = json.loads(fabricated_path.read_text())
    fabricated[0]["source_bindings"][0]["quote"] = (
        "This sentence was fabricated and is absent from the source.")
    rewrite_claims(fabricated_path, fabricated)
    result = run_gate(fabricated_path)
    assert result.returncode != 0
    assert "quote not found" in result.stdout

    bbox_path = stage_real_pack(tmp_path / "bbox")
    bbox_claims = json.loads(bbox_path.read_text())
    holder = next(find_box(claim.get("object")) for claim in bbox_claims
                  if find_box(claim.get("object")) is not None)
    holder["bounding_box"] = [0.1, 0.1, 0.2, 0.2]
    holder["annotation_status"] = "PENDING"
    rewrite_claims(bbox_path, bbox_claims)
    result = run_gate(bbox_path)
    assert result.returncode != 0
    assert "coordinates must be measured, never estimated" in result.stdout

    wrong_page_path = stage_real_pack(tmp_path / "wrong-page")
    wrong_page_claims = json.loads(wrong_page_path.read_text())
    target = next(claim for claim in wrong_page_claims
                  if claim["claim_id"] == "claim_r2j_limit_max_weight")
    assert target["source_bindings"][0]["page"] == 4
    target["source_bindings"][0]["page"] = 1
    rewrite_claims(wrong_page_path, wrong_page_claims)
    result = run_gate(wrong_page_path)
    assert result.returncode != 0
    assert "quote not found on cited page 1" in result.stdout

