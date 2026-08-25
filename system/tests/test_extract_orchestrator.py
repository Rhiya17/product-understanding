import copy
import hashlib
import json
import os
import shutil
from pathlib import Path

from system import extract_orchestrator as orchestrator


REPO_ROOT = Path(__file__).resolve().parents[2]
PRODUCT = "apple-macbook-air-13-m3"


def make_scratch_repo(tmp_path):
    root = tmp_path / "scratch-repository"
    (root / "evidence-packs" / "workorders").mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "evidence-packs" / "validate.py",
                 root / "evidence-packs" / "validate.py")
    for name in ("extraction-agent-brief.md", f"{PRODUCT}.json"):
        shutil.copy2(REPO_ROOT / "evidence-packs" / "workorders" / name,
                     root / "evidence-packs" / "workorders" / name)
    shutil.copytree(REPO_ROOT / "evidence-packs" / PRODUCT,
                    root / "evidence-packs" / PRODUCT)
    (root / "source-vault").mkdir()
    os.symlink(REPO_ROOT / "source-vault" / PRODUCT,
               root / "source-vault" / PRODUCT, target_is_directory=True)
    (root / "system").mkdir()
    shutil.copy2(REPO_ROOT / "system" / "baseline-hashes.json",
                 root / "system" / "baseline-hashes.json")
    return root


def pack_snapshot(pack):
    return {path.relative_to(pack).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in pack.rglob("*") if path.is_file()}


def append_valid_claim(pack_dir):
    claims_path = pack_dir / "claims.json"
    claims = json.loads(claims_path.read_text())
    added = copy.deepcopy(claims[0])
    added["claim_id"] = "claim_mba_topup_height_confirmation"
    added["predicate"] = "height_closed_confirmation"
    claims.append(added)
    claims_path.write_text(json.dumps(claims, indent=2) + "\n", encoding="utf-8")


def mock_success(_prompt, _attempt_root, pack_dir, _repo_root):
    append_valid_claim(pack_dir)
    return {"cost_usd": 0.01}


def test_topup_promotes_only_appends_and_writes_run_report(tmp_path):
    root = make_scratch_repo(tmp_path)
    pack = root / "evidence-packs" / PRODUCT
    original = json.loads((pack / "claims.json").read_text())
    protected = {name: (pack / name).read_bytes()
                 for name in orchestrator.PROTECTED_TOPUP_FILES
                 if (pack / name).exists()}
    prompts = []

    def detective(prompt, attempt_root, pack_dir, repo_root):
        prompts.append(prompt)
        return mock_success(prompt, attempt_root, pack_dir, repo_root)

    result = orchestrator.orchestrate_product(
        PRODUCT, topup=True, repo_root=root,
        staging_root=root / "system" / "staging",
        detective_runner=detective,
        verifier_runner=lambda _root, _product: 0,
        queue_runner=lambda _root, _product: 0,
        run_id="topup-success", today="2026-08-24")
    report_path = orchestrator.write_run_report(
        root, "topup-success", True, [result])

    promoted = json.loads((pack / "claims.json").read_text())
    assert result["state"] == "verified"
    assert result["attempts_used"] == 1
    assert result["promoted"] is True
    assert len(promoted) == len(original) + 1
    assert promoted[:len(original)] == original
    assert promoted[-1]["claim_id"] == "claim_mba_topup_height_confirmation"
    assert "TOP-UP MODE" in prompts[0]
    assert "append-only" in prompts[0]
    assert str((root / "source-vault" / PRODUCT).resolve()) in prompts[0]
    for name, before in protected.items():
        assert (pack / name).read_bytes() == before
    assert report_path.exists()
    report = json.loads(report_path.read_text())
    assert report["products"][0]["state"] == "verified"
    assert not (root / "system" / "staging" / "topup-success" / PRODUCT).exists()


def test_failed_attempts_leave_real_pack_byte_identical(tmp_path):
    root = make_scratch_repo(tmp_path)
    pack = root / "evidence-packs" / PRODUCT
    before = pack_snapshot(pack)

    def always_bad(_prompt, _attempt_root, pack_dir, _repo_root):
        claims_path = pack_dir / "claims.json"
        claims = json.loads(claims_path.read_text())
        claims[0]["source_bindings"][0]["quote"] = "fabricated retry quote"
        claims_path.write_text(json.dumps(claims), encoding="utf-8")
        return {"cost_usd": 0.0}

    result = orchestrator.orchestrate_product(
        PRODUCT, topup=True, repo_root=root,
        staging_root=root / "system" / "staging",
        detective_runner=always_bad,
        verifier_runner=lambda _root, _product: 0,
        queue_runner=lambda _root, _product: 0,
        run_id="topup-failed", today="2026-08-24")

    assert result["state"] == "gate_failed"
    assert result["attempts_used"] == orchestrator.MAX_ATTEMPTS
    assert result["promoted"] is False
    assert pack_snapshot(pack) == before
    assert result["fail_lines"]


def test_retry_receives_verbatim_fail_line_then_reaches_green(tmp_path):
    root = make_scratch_repo(tmp_path)
    prompts = []

    def fail_then_fix(prompt, _attempt_root, pack_dir, _repo_root):
        prompts.append(prompt)
        if len(prompts) == 1:
            claims_path = pack_dir / "claims.json"
            claims = json.loads(claims_path.read_text())
            claims[0]["source_bindings"][0]["quote"] = "fabricated retry quote"
            claims_path.write_text(json.dumps(claims), encoding="utf-8")
        else:
            append_valid_claim(pack_dir)
        return {"cost_usd": 0.0}

    result = orchestrator.orchestrate_product(
        PRODUCT, topup=True, repo_root=root,
        staging_root=root / "system" / "staging",
        detective_runner=fail_then_fix,
        verifier_runner=lambda _root, _product: 0,
        queue_runner=lambda _root, _product: 0,
        run_id="topup-retry", today="2026-08-24")

    assert result["state"] == "verified"
    assert result["attempts_used"] == 2
    assert result["fail_lines"][0] in prompts[1]
    assert "PRIOR GATE FAIL LINES (VERBATIM)" in prompts[1]


def test_tool_guard_helpers_reject_write_capable_bash(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    assert orchestrator._bash_is_read_only("pdftotext manual.pdf - | head")
    assert orchestrator._bash_is_read_only("rg procedure source-vault")
    assert not orchestrator._bash_is_read_only("cp source target")
    assert not orchestrator._bash_is_read_only("pdftotext manual.pdf output.txt")
    assert not orchestrator._bash_is_read_only("find . -delete")
    assert orchestrator._is_within(pack / "claims.json", pack)
    assert not orchestrator._is_within(tmp_path / "outside.json", pack)
