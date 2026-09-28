"""ShowMe developer commands.

    python scripts/showme.py evaluate --launch --held-out --offline [--repeats 3]
    python scripts/showme.py test --offline

`evaluate` runs the current answer app in-process with every provider
disabled, submits the frozen launch and held-out cases the way the UI does
(published-only, top=10), scores each response against its rubric, and times
each request. Automated scoring covers outcome type and claim coverage; a
human still reviews required/forbidden wording before a P1 case counts.
"""

import argparse
import json
import os
import socket
import statistics
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

WORKORDERS = REPO_ROOT / "docs" / "workorders"
CASE_FILES = {
    "launch": WORKORDERS / "showme-launch-regression-cases.json",
    "held_out": WORKORDERS / "showme-heldout-cases.json",
    "blind_b": WORKORDERS / "showme-heldout-cases-blind-b.json",
}
PROVIDER_ENV_VARS = ("FAL_KEY", "FAL_API_KEY", "OPENAI_API_KEY",
                     "ANTHROPIC_API_KEY")


def go_offline():
    """Remove provider credentials and refuse non-loopback connections."""
    for name in PROVIDER_ENV_VARS:
        os.environ.pop(name, None)
    os.environ["SHOWME_LUNA_ENABLED"] = "0"
    original_connect = socket.socket.connect

    def guarded_connect(sock, address):
        host = address[0] if isinstance(address, tuple) else address
        if sock.family == socket.AF_UNIX or host in ("127.0.0.1", "::1", "localhost"):
            return original_connect(sock, address)
        raise RuntimeError(f"offline evaluation attempted network access to {address}")

    socket.socket.connect = guarded_connect


def start_server(engine, packs_root=None):
    from app.server import create_server
    from system.luna_planner import LunaPlanner

    server = create_server(port=0, packs_root=packs_root,
                           luna_planner=LunaPlanner(api_key=""), answer_engine=engine)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def ask(base_url, case, context=None):
    params = {"q": case["question"], "preview": "0", "top": "10",
              "product": case.get("selected_product") or ""}
    if context:
        params["context"] = json.dumps(context)
    url = base_url + "/api/answer?" + urllib.parse.urlencode(params)
    started = time.perf_counter()
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read())
    return payload, (time.perf_counter() - started) * 1000


def response_claims(result):
    ids = []
    if result.get("claim_id") and not str(result["claim_id"]).startswith("procedure:"):
        ids.append(result["claim_id"])
    ids += [step.get("claim_id") for step in result.get("steps", [])
            if step.get("claim_id")]
    return ids


def classify(payload):
    document = payload.get("answer_document")
    if document:
        return {"needs_input": "clarify", "unsupported": "missing_evidence"}.get(
            document["status"], "answer")
    if payload.get("mode") == "clarify":
        return "clarify"
    return "answer" if payload.get("results") else "missing_evidence"


def document_claims(blocks):
    return [item["claim_id"] for block in blocks for item in block["items"]
            if item.get("claim_id")]


def score(case, payload):
    document = payload.get("answer_document")
    outcome = classify(payload)
    if document:
        results = document["blocks"]
        primary = [b for b in results if b.get("primary")] or results[:1]
        lead = document_claims(primary)
        everything = document_claims(results)
    else:
        results = payload.get("results", [])
        lead = response_claims(results[0]) if results else []
        everything = [cid for result in results for cid in response_claims(result)]
    required = case["required_claim_ids"]
    acceptable = case.get("acceptable_outcomes") or [case["expected_outcome"]]
    checks = {
        "outcome": outcome in acceptable,
        "required_claims_present": all(cid in everything for cid in required),
        "leads_with_required_claim": (not required) or any(cid in lead for cid in required),
        "no_forbidden_claims": not set(case["forbidden_claim_ids"]) & set(everything),
    }
    if case.get("lead_procedure"):
        checks["lead_procedure"] = (
            document["coverage"].get("procedure_id") == case["lead_procedure"]
            if document else bool(results) and
            results[0].get("procedure") == case["lead_procedure"])
    return {
        "id": case["id"],
        "question": case["question"],
        "expected": case["expected_outcome"],
        "observed_outcome": outcome,
        "result_cards": len(results),
        "status": document["status"] if document else None,
        "direct_answer": document["direct_answer"] if document else None,
        "lead_claims": lead,
        "forbidden_present": sorted(set(case["forbidden_claim_ids"]) & set(everything)),
        "missing_required": [cid for cid in required if cid not in everything],
        "video_media": sum(1 for r in results for m in r.get("media", [])
                           if (m.get("modality") or m.get("kind") or "").startswith("video")
                           or str(m.get("path", "")).endswith(".mp4")),
        "parent_context_sent": bool(case.get("_context_sent")) if case.get("parent_context") else None,
        "checks": checks,
        "auto_pass": all(checks.values()),
    }


def percentile(values, pct):
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, round(pct / 100 * len(ordered) + 0.5) - 1))
    return ordered[index]


def evaluate(args):
    if not args.offline:
        sys.exit("Only --offline evaluation exists; live model routes need an "
                 "approved paid-run manifest.")
    go_offline()
    suites = [name for name, wanted in (("launch", args.launch),
                                        ("held_out", args.held_out),
                                        ("blind_b", args.blind_b)) if wanted]
    if not suites:
        sys.exit("choose --launch, --held-out and/or --blind-b")
    server, base_url = start_server(args.engine, args.packs_root)
    launch_cases = {c["id"].split("_")[0]: c for c in
                    json.loads(CASE_FILES["launch"].read_text())["cases"]}
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "label": args.label,
        "mode": "offline deterministic fallback; providers disabled",
        "engine": args.engine,
        "packs_root": str(args.packs_root) if args.packs_root else "evidence-packs (production)",
        "fixture_note": ("TEST-ONLY receipts in an isolated packs copy; measures selection, "
                         "not production eligibility") if args.packs_root else None,
        "surface": "current app /api/answer, published-only, top=10",
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                                     capture_output=True, text=True).stdout.strip(),
        "host": {"platform": sys.platform, "python": sys.version.split()[0],
                 "machine": os.uname().machine},
        "latency_note": ("Server round-trip on localhost, measured in-process. "
                         "Not browser time-to-first-useful-answer."),
        "suites": {},
    }
    try:
        for suite in suites:
            cases = json.loads(CASE_FILES[suite].read_text())["cases"]
            rows, latencies = [], []
            for case in cases:
                payload, context = None, None
                parent_id = (case.get("parent_context") or {}).get("parent_question_id")
                if parent_id and args.engine == "v2":
                    parent, _ = ask(base_url, launch_cases[parent_id])
                    context = (parent.get("answer_document") or {}).get("context")
                    case = dict(case, _context_sent=bool(context))
                for _ in range(args.repeats):
                    payload, elapsed = ask(base_url, case, context)
                    latencies.append(elapsed)
                row = score(case, payload)
                row["response"] = payload if args.keep_responses else None
                rows.append(row)
            passed = sum(row["auto_pass"] for row in rows)
            report["suites"][suite] = {
                "case_file": str(CASE_FILES[suite].relative_to(REPO_ROOT)),
                "auto_passed": passed,
                "denominator": len(rows),
                "latency_ms": {
                    "samples": len(latencies),
                    "p50": round(statistics.median(latencies), 1),
                    "p95": round(percentile(latencies, 95), 1),
                    "max": round(max(latencies), 1),
                },
                "cases": rows,
            }
    finally:
        server.shutdown()
        server.server_close()

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    for suite, data in report["suites"].items():
        print(f"{suite}: {data['auto_passed']}/{data['denominator']} auto-pass; "
              f"latency p50 {data['latency_ms']['p50']} ms, "
              f"p95 {data['latency_ms']['p95']} ms ({data['latency_ms']['samples']} samples)")
        for row in data["cases"]:
            failed = [name for name, ok in row["checks"].items() if not ok]
            print(f"  {'PASS' if row['auto_pass'] else 'FAIL'} {row['id']}: "
                  f"expected {row['expected']}, got {row['observed_outcome']} "
                  f"({row['result_cards']} cards)"
                  + (f"; failed {', '.join(failed)}" if failed else ""))
    return 0


def run_tests(args):
    if not args.offline:
        sys.exit("Only --offline tests exist; live canaries are separate.")
    env = dict(os.environ)
    env.pop("SHOWME_ALLOW_NETWORK", None)
    return subprocess.call([sys.executable, "-m", "pytest", "-q", "-p",
                            "no:cacheprovider", "system/tests", "app/tests"],
                           cwd=REPO_ROOT, env=env)


def main(argv=None):
    parser = argparse.ArgumentParser(description="ShowMe developer commands")
    commands = parser.add_subparsers(dest="command", required=True)
    evaluate_parser = commands.add_parser("evaluate", help="score the frozen cases")
    evaluate_parser.add_argument("--launch", action="store_true")
    evaluate_parser.add_argument("--held-out", action="store_true")
    evaluate_parser.add_argument("--blind-b", action="store_true")
    evaluate_parser.add_argument("--offline", action="store_true")
    evaluate_parser.add_argument("--engine", choices=("v2", "legacy"), default="v2")
    evaluate_parser.add_argument("--packs-root", type=Path,
                                 help="isolated fixture packs (reported as test-only)")
    evaluate_parser.add_argument("--repeats", type=int, default=3)
    evaluate_parser.add_argument("--label", default="current")
    evaluate_parser.add_argument("--keep-responses", action="store_true")
    evaluate_parser.add_argument("--out", type=Path)
    evaluate_parser.set_defaults(func=evaluate)
    test_parser = commands.add_parser("test", help="run the offline test suite")
    test_parser.add_argument("--offline", action="store_true")
    test_parser.set_defaults(func=run_tests)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
