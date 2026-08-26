#!/usr/bin/env python3
"""Stage and gate one Claude Detective extraction per product.

No Detective writes into a real evidence pack. Each attempt receives an
isolated repository-shaped staging root, and only a gate-green pack can be
atomically exchanged into place. Top-ups additionally enforce the M0 claim
hash baseline and an unchanged-prefix-plus-appends rule.
"""

import argparse
import asyncio
import ctypes
import datetime as dt
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BRIEF_PATH = REPO_ROOT / "evidence-packs" / "workorders" / "extraction-agent-brief.md"
BASELINE_PATH = REPO_ROOT / "system" / "baseline-hashes.json"
STAGING_ROOT = REPO_ROOT / "system" / "staging"
RUNS_ROOT = REPO_ROOT / "system" / "runs"
MAX_ATTEMPTS = 3

PROTECTED_TOPUP_FILES = ("reviews.json", "verdicts.json")
READ_ONLY_BASH_COMMANDS = {
    "file", "find", "grep", "head", "ls", "pdfinfo", "pdftotext", "pwd",
    "rg", "shasum", "stat", "tail", "wc",
}


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def claim_hash(claim):
    return hashlib.sha256(canonical_json(claim).encode("utf-8")).hexdigest()


def file_hash(path):
    path = Path(path)
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def atomic_write_json(path, value):
    try:
        from system.verify_claims import atomic_write_json as write_json
    except ModuleNotFoundError:
        from verify_claims import atomic_write_json as write_json
    write_json(path, value)


def baseline_product(repo_root, product):
    baseline_path = Path(repo_root) / "system" / "baseline-hashes.json"
    baseline = load_json(baseline_path)
    product_baseline = baseline.get(product)
    if not isinstance(product_baseline, dict):
        raise ValueError(f"M0 baseline has no pack {product}")
    return product_baseline


def verify_claim_hashes(claims_path, expected):
    claims = load_json(claims_path)
    if not isinstance(claims, list):
        return ["claims.json root is not a list"]
    errors = []
    by_id = {}
    for claim in claims:
        claim_id = claim.get("claim_id")
        if claim_id in by_id:
            errors.append(f"duplicate claim_id {claim_id}")
        by_id[claim_id] = claim_hash(claim)
    for claim_id, expected_hash in expected.items():
        if claim_id not in by_id:
            errors.append(f"missing pre-existing claim {claim_id}")
        elif by_id[claim_id] != expected_hash:
            errors.append(f"changed pre-existing claim {claim_id}")
    return errors


def verify_topup_unchanged(original_claims, staged_claims):
    original = load_json(original_claims)
    staged = load_json(staged_claims)
    errors = []
    if not isinstance(original, list) or not isinstance(staged, list):
        return ["top-up claims roots must both be lists"]
    if len(staged) < len(original):
        errors.append("top-up removed one or more pre-existing claims")
        return errors
    for index, prior in enumerate(original):
        if canonical_json(prior) != canonical_json(staged[index]):
            errors.append(
                f"top-up changed/reordered pre-existing claim at index {index} "
                f"({prior.get('claim_id')})")
    staged_ids = [claim.get("claim_id") for claim in staged]
    if len(staged_ids) != len(set(staged_ids)):
        errors.append("top-up introduced a duplicate claim_id")
    return errors


def describe_missing(pack_dir, workorder):
    claims = load_json(Path(pack_dir) / "claims.json")
    gaps = load_json(Path(pack_dir) / "gaps.json")
    type_counts = {}
    for claim in claims:
        claim_type = claim.get("type")
        type_counts[claim_type] = type_counts.get(claim_type, 0) + 1
    missing = []
    minimum = workorder.get("expected_total", {}).get("min", 0)
    if len(claims) < minimum:
        missing.append(f"total claims: need at least {minimum - len(claims)} more")
    for claim_type, floor in workorder.get("required_types", {}).items():
        shortfall = floor - type_counts.get(claim_type, 0)
        if shortfall > 0:
            missing.append(f"type {claim_type}: need {shortfall} more")
    coverage = gaps.get("coverage", {}) if isinstance(gaps, dict) else {}
    waived = {waiver for gap in gaps.get("gaps", []) for waiver in gap.get("waives", [])} \
        if isinstance(gaps, dict) else set()
    for item in workorder.get("checklist", []):
        checklist_id = item.get("id")
        if not coverage.get(checklist_id) and f"checklist:{checklist_id}" not in waived:
            missing.append(f"checklist {checklist_id}: no coverage or waiver")
    return missing or ["no current contract shortfall; preserve the pack unchanged"]


def assemble_prompt(brief, workorder_text, vault_dir, pack_dir, today,
                    topup=False, missing=None, prior_fail_lines=None):
    parts = [
        brief,
        "\nPRODUCT WORK ORDER JSON (VERBATIM):\n" + workorder_text,
        "\nRESOLVED PATHS:",
        f"vault_dir: {Path(vault_dir).resolve()}",
        f"pack_dir: {Path(pack_dir).resolve()}",
        f"today: {today}",
        "Write extraction outputs only inside pack_dir.",
    ]
    if topup:
        parts.extend([
            "\nTOP-UP MODE: this pack already exists. It is append-only. Do not "
            "edit, reorder, renumber, or delete any existing claim.",
            "Missing contract coverage:",
            *[f"- {item}" for item in (missing or [])],
        ])
    if prior_fail_lines:
        parts.extend([
            "\nPRIOR GATE FAIL LINES (VERBATIM):",
            *prior_fail_lines,
        ])
    return "\n".join(parts)


def _is_within(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


def _bash_is_read_only(command):
    if not isinstance(command, str) or not command.strip():
        return False
    if any(token in command for token in (">", ";", "`", "$(", "\n", "\r")):
        return False
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return False
    if not tokens:
        return False
    segments = []
    current = []
    for token in tokens:
        if token in {"|", "&&", "||", ";"}:
            if token != "|" or not current:
                return False
            segments.append(current)
            current = []
        else:
            current.append(token)
    if current:
        segments.append(current)
    if not segments or not all(Path(segment[0]).name in READ_ONLY_BASH_COMMANDS
                               for segment in segments):
        return False
    for segment in segments:
        command_name = Path(segment[0]).name
        if command_name == "pdftotext" and segment[-1] != "-":
            return False
        if command_name == "find" and any(
                token in {"-delete", "-exec", "-execdir", "-ok", "-okdir",
                          "-fprint", "-fprintf"} for token in segment[1:]):
            return False
    return True


def make_pre_tool_guard(pack_dir, read_roots):
    async def guard(hook_input, _tool_use_id, _context):
        tool = hook_input.get("tool_name")
        tool_input = hook_input.get("tool_input", {})
        allow = True
        reason = ""
        if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
            file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
            allow = bool(file_path) and _is_within(file_path, pack_dir)
            reason = "writes are restricted to the staged product pack"
        elif tool in {"Read", "Glob", "Grep"}:
            file_path = tool_input.get("file_path") or tool_input.get("path") or pack_dir
            allow = any(_is_within(file_path, root) for root in read_roots)
            reason = "reads are restricted to the staged product inputs"
        elif tool == "Bash":
            allow = _bash_is_read_only(tool_input.get("command", ""))
            reason = "Bash is restricted to read-only inspection commands"
        if allow:
            return {"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "allow",
            }}
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}
    return guard


async def _run_claude_agent(prompt, attempt_root, pack_dir, repo_root):
    try:
        from claude_agent_sdk import (
            ClaudeAgentOptions, ClaudeSDKClient, HookMatcher, ResultMessage,
        )
    except ImportError:
        raise RuntimeError("claude-agent-sdk is not installed") from None

    product = Path(pack_dir).name
    read_roots = [
        attempt_root,
        Path(repo_root) / "source-vault" / product,
        Path(repo_root) / "evidence-packs" / "workorders",
    ]
    guard = make_pre_tool_guard(pack_dir, read_roots)
    options = ClaudeAgentOptions(
        cwd=str(Path(attempt_root).resolve()),
        allowed_tools=["Read", "Glob", "Grep", "Write", "Edit", "Bash"],
        disallowed_tools=["WebSearch", "WebFetch", "Task"],
        permission_mode="acceptEdits",
        setting_sources=[],
        sandbox={
            "enabled": True,
            "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False,
            "excludedCommands": [],
        },
        hooks={
            "PreToolUse": [HookMatcher(
                matcher="Read|Glob|Grep|Write|Edit|MultiEdit|NotebookEdit|Bash",
                hooks=[guard],
            )],
        },
        max_turns=80,
    )
    result = {"cost_usd": 0.0, "session_id": None}
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                result["cost_usd"] = float(message.total_cost_usd or 0.0)
                result["session_id"] = message.session_id
                if message.is_error:
                    raise RuntimeError("Claude Detective returned an error result")
    return result


def run_detective(prompt, attempt_root, pack_dir, repo_root):
    return asyncio.run(_run_claude_agent(prompt, attempt_root, pack_dir, repo_root))


def prepare_attempt(repo_root, run_stage, attempt, product, topup):
    attempt_root = Path(run_stage) / f"attempt-{attempt}"
    pack_dir = attempt_root / "evidence-packs" / product
    pack_dir.parent.mkdir(parents=True)
    if topup:
        shutil.copytree(Path(repo_root) / "evidence-packs" / product, pack_dir)
    else:
        pack_dir.mkdir()
    os.symlink(Path(repo_root) / "source-vault",
               attempt_root / "source-vault", target_is_directory=True)
    os.symlink(Path(repo_root) / "evidence-packs" / "workorders",
               attempt_root / "evidence-packs" / "workorders",
               target_is_directory=True)
    return attempt_root, pack_dir


def run_gate(repo_root, claims_path, ignore_stale_verdicts=False):
    claims_path = Path(claims_path)
    verdicts_path = claims_path.parent / "verdicts.json"
    verdicts_bytes = None
    if ignore_stale_verdicts and verdicts_path.exists():
        # A top-up adds claims before the post-promotion verifier runs. The
        # protected prior verdict document is necessarily incomplete for that
        # staged claim set, so hide it only for the deterministic claim gate and
        # restore it byte-for-byte immediately afterward.
        verdicts_bytes = verdicts_path.read_bytes()
        verdicts_path.unlink()
    try:
        process = subprocess.run(
            [sys.executable, str(Path(repo_root) / "evidence-packs" / "validate.py"),
             str(claims_path)],
            cwd=repo_root, capture_output=True, text=True, check=False)
    finally:
        if verdicts_bytes is not None:
            verdicts_path.write_bytes(verdicts_bytes)
    fail_lines = [line for line in process.stdout.splitlines()
                  if line.startswith("FAIL:")]
    summary = None
    for line in process.stdout.splitlines():
        if line.startswith("SUMMARY_JSON:"):
            try:
                summary = json.loads(line.removeprefix("SUMMARY_JSON:").strip())
            except json.JSONDecodeError:
                pass
    return {
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "fail_lines": fail_lines,
        "summary": summary,
    }


def _atomic_exchange(first, second):
    first = Path(first)
    second = Path(second)
    if first.stat().st_dev != second.stat().st_dev:
        raise OSError("atomic promotion requires staging and pack on one filesystem")
    libc = ctypes.CDLL(None, use_errno=True)
    first_bytes = os.fsencode(first)
    second_bytes = os.fsencode(second)
    if sys.platform == "darwin" and hasattr(libc, "renameatx_np"):
        function = libc.renameatx_np
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                             ctypes.c_char_p, ctypes.c_uint]
        result = function(-2, first_bytes, -2, second_bytes, 0x00000002)
    elif hasattr(libc, "renameat2"):
        function = libc.renameat2
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                             ctypes.c_char_p, ctypes.c_uint]
        result = function(-100, first_bytes, -100, second_bytes, 0x00000002)
    else:
        raise OSError("platform does not expose an atomic directory exchange")
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


def atomic_promote(staged_pack, real_pack):
    staged_pack = Path(staged_pack)
    real_pack = Path(real_pack)
    real_pack.parent.mkdir(parents=True, exist_ok=True)
    if not real_pack.exists():
        os.rename(staged_pack, real_pack)
        return
    _atomic_exchange(staged_pack, real_pack)
    shutil.rmtree(staged_pack)


def default_verifier_runner(repo_root, product):
    process = subprocess.run(
        [sys.executable, str(Path(repo_root) / "system" / "verify_claims.py"),
         "--product", product],
        cwd=repo_root, check=False)
    return process.returncode


def default_queue_runner(repo_root, product):
    renderer = Path(repo_root) / "system" / "review_queue.py"
    if not renderer.exists():
        return None
    process = subprocess.run(
        [sys.executable, str(renderer), "--product", product],
        cwd=repo_root, check=False)
    return process.returncode


def verifier_state(exit_code):
    if exit_code == 0:
        return "verified"
    if exit_code == 10:
        return "alarmed"
    if exit_code == 20:
        return "verification_partial"
    return "verification_failed"


def orchestrate_product(product, topup=False, repo_root=REPO_ROOT,
                        staging_root=None, detective_runner=run_detective,
                        verifier_runner=default_verifier_runner,
                        queue_runner=default_queue_runner, run_id=None,
                        today=None):
    repo_root = Path(repo_root).resolve()
    staging_root = Path(staging_root or (repo_root / "system" / "staging"))
    run_id = run_id or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    today = today or dt.date.today().isoformat()
    run_stage = staging_root / run_id / product
    real_pack = repo_root / "evidence-packs" / product
    if not topup and real_pack.exists():
        raise ValueError(f"{product} already exists; use --topup to preserve claims")
    if topup and not real_pack.exists():
        raise ValueError(f"cannot top up missing pack {product}")

    brief = (repo_root / "evidence-packs" / "workorders" /
             "extraction-agent-brief.md").read_text(encoding="utf-8")
    workorder_path = repo_root / "evidence-packs" / "workorders" / f"{product}.json"
    workorder_text = workorder_path.read_text(encoding="utf-8")
    workorder = json.loads(workorder_text)
    expected_baseline = baseline_product(repo_root, product) if topup else {}
    if topup:
        baseline_errors = verify_claim_hashes(
            real_pack / "claims.json", expected_baseline)
        if baseline_errors:
            raise ValueError("M0 baseline mismatch before top-up: " + "; ".join(baseline_errors))
        missing = describe_missing(real_pack, workorder)
    else:
        missing = []

    protected_before = {name: file_hash(real_pack / name)
                        for name in PROTECTED_TOPUP_FILES} if topup else {}
    prior_fail_lines = []
    all_fail_lines = []
    summaries = []
    states = []
    attempt_records = []
    started = time.monotonic()
    promoted = False

    try:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            attempt_root, staged_pack = prepare_attempt(
                repo_root, run_stage, attempt, product, topup)
            prompt = assemble_prompt(
                brief, workorder_text,
                attempt_root / "source-vault" / product,
                staged_pack, today, topup=topup, missing=missing,
                prior_fail_lines=prior_fail_lines,
            )
            record = {"attempt": attempt, "fail_lines": []}
            try:
                agent_result = detective_runner(
                    prompt, attempt_root, staged_pack, repo_root)
                record["detective_cost_usd"] = float(
                    (agent_result or {}).get("cost_usd", 0.0))
            except Exception as exc:
                record["agent_error"] = type(exc).__name__
                attempt_records.append(record)
                states.append("gate_failed")
                break

            claims_path = staged_pack / "claims.json"
            if not claims_path.exists():
                record["agent_error"] = "claims.json was not produced"
                attempt_records.append(record)
                states.append("gate_failed")
                break
            states.append("extracted")
            gate = run_gate(
                repo_root, claims_path, ignore_stale_verdicts=topup)
            record["gate_exit_code"] = gate["exit_code"]
            record["fail_lines"] = gate["fail_lines"]
            record["summary"] = gate["summary"]
            attempt_records.append(record)
            if gate["summary"] is not None:
                summaries.append(gate["summary"])
            all_fail_lines.extend(gate["fail_lines"])
            if gate["exit_code"] != 0:
                prior_fail_lines = gate["fail_lines"]
                continue

            if topup:
                immutability_errors = verify_topup_unchanged(
                    real_pack / "claims.json", staged_pack / "claims.json")
                immutability_errors.extend(verify_claim_hashes(
                    staged_pack / "claims.json", expected_baseline))
                for name, digest in protected_before.items():
                    if file_hash(staged_pack / name) != digest:
                        immutability_errors.append(f"top-up changed protected {name}")
                if immutability_errors:
                    record["immutability_errors"] = immutability_errors
                    states.append("gate_failed")
                    break

            states.append("gate_passed")
            atomic_promote(staged_pack, real_pack)
            promoted = True
            if topup:
                after_errors = verify_claim_hashes(
                    real_pack / "claims.json", expected_baseline)
                if after_errors:
                    raise RuntimeError("post-promotion baseline mismatch: "
                                       + "; ".join(after_errors))
            try:
                verify_exit = verifier_runner(repo_root, product)
            except Exception:
                verify_exit = 30
            terminal = verifier_state(verify_exit)
            states.append(terminal)
            try:
                queue_exit = queue_runner(repo_root, product)
            except Exception:
                queue_exit = 1
            break
        else:
            states.append("gate_failed")
            verify_exit = None
            queue_exit = None

        if not promoted:
            terminal = "gate_failed"
            verify_exit = None
            queue_exit = None
        return {
            "product": product,
            "state": terminal,
            "state_history": states,
            "attempts_used": len(attempt_records),
            "wall_time_s": round(time.monotonic() - started, 3),
            "fail_lines": all_fail_lines,
            "summaries": summaries,
            "attempts": attempt_records,
            "verifier_exit_code": verify_exit,
            "queue_exit_code": queue_exit,
            "baseline_verified": topup,
            "promoted": promoted,
        }
    finally:
        if run_stage.exists():
            shutil.rmtree(run_stage)


def write_run_report(repo_root, run_id, topup, products):
    report = {
        "run_id": run_id,
        "date": dt.datetime.now(dt.timezone.utc).isoformat(),
        "topup": topup,
        "products": products,
    }
    path = Path(repo_root) / "system" / "runs" / f"{run_id}.json"
    atomic_write_json(path, report)
    return path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--product", help="extract one new product pack")
    group.add_argument("--topup", metavar="PRODUCT",
                       help="append to one existing product pack")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    product = args.topup or args.product
    topup = bool(args.topup)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    try:
        result = orchestrate_product(
            product, topup=topup, run_id=run_id)
    except Exception as exc:
        result = {
            "product": product,
            "state": "gate_failed",
            "state_history": ["gate_failed"],
            "attempts_used": 0,
            "fail_lines": [],
            "error": type(exc).__name__,
            "promoted": False,
        }
    path = write_run_report(REPO_ROOT, run_id, topup, [result])
    print(f"run report: {path}")
    print(f"{product}: {result['state']} ({result['attempts_used']} attempt(s))")
    return 0 if result["state"] in {"verified", "verification_partial", "alarmed"} else 1


if __name__ == "__main__":
    sys.exit(main())
