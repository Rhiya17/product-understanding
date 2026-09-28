"""Paid semantic verification that writes version-bound receipts.

    python scripts/run_verifier_receipts.py plan --run-id RUN --cap 1.00
    python scripts/run_verifier_receipts.py execute --run-id RUN --approval-id APPR

`plan` freezes a manifest of every approved claim with at least one text
binding and no current receipt, prints its digest and price bounds, and
spends nothing. `execute` runs only with an owner approval recorded for that
exact manifest digest (system/spend_guard.py) and FAL_KEY in the environment.
"""

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from system import evidence_status, spend_guard  # noqa: E402
from system import verify_claims as verifier  # noqa: E402

MANIFEST_DIR = REPO_ROOT / "docs" / "workorders" / "approvals" / "manifests"


def claims_needing_receipts():
    selected = []
    for pack_dir in sorted(p.parent for p in (REPO_ROOT / "evidence-packs").glob("*/claims.json")):
        pack = evidence_status.PackEvidence(pack_dir.name)
        types = verifier.source_types(REPO_ROOT / "source-vault", pack_dir.name)
        for claim_id, claim in pack.claims.items():
            if pack.dispositions.get(claim_id) != "APPROVED_FOR_PUBLISH":
                continue
            if not any(types.get(b.get("source_id")) not in verifier.VISUAL_SOURCE_TYPES
                       for b in claim.get("source_bindings", [])):
                continue
            digest = evidence_status.claim_digest(claim)
            if pack.current_receipt(claim_id, digest):
                continue
            prompt = verifier.build_prompt(claim)
            selected.append({"product_dir": pack_dir.name, "claim_id": claim_id,
                             "claim_digest": digest,
                             "estimate_usd": verifier.estimated_cost(prompt),
                             "worst_case_usd": verifier.worst_case_cost(prompt)})
    return selected


def plan(args):
    selected = claims_needing_receipts()
    manifest = {
        "run_id": args.run_id,
        "category": "answer_verifier",
        "purpose": "Version-bound semantic receipts for approved claims (P1 eligibility).",
        "provider": "fal.ai OpenRouter route " + verifier.ENDPOINT,
        "model": verifier.MODEL_ID,
        "inputs": {"claims": [{k: s[k] for k in ("product_dir", "claim_id", "claim_digest")}
                              for s in selected]},
        "max_calls": len(selected),
        "cap_usd": args.cap,
        "retry_policy": ("One malformed-output retry per claim inside its reservation; "
                         "provider failure stops the run; no automatic rerun."),
    }
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    path = MANIFEST_DIR / f"{args.run_id}.json"
    path.write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"manifest: {path.relative_to(REPO_ROOT)}")
    print(f"digest: {spend_guard.manifest_digest(manifest)}")
    print(f"claims: {len(selected)}")
    print(f"list-price estimate: ${sum(s['estimate_usd'] for s in selected):.4f}")
    print(f"worst-case bound: ${sum(s['worst_case_usd'] for s in selected):.4f}; cap ${args.cap:.2f}")
    return 0


def execute(args):
    if not os.environ.get("FAL_KEY"):
        sys.exit("FAL_KEY is not set in the environment.")
    manifest = json.loads((MANIFEST_DIR / f"{args.run_id}.json").read_text())
    guard = spend_guard.SpendGuard()
    run = guard.authorize(manifest, args.approval_id)
    by_product = {}
    for item in manifest["inputs"]["claims"]:
        by_product.setdefault(item["product_dir"], []).append(item["claim_id"])
    totals = {"verified": 0, "results": {}}
    stopped = None
    for product_dir, claim_ids in by_product.items():
        summary = verifier.verify_claims_to_receipts(
            REPO_ROOT / "evidence-packs" / product_dir, claim_ids, run, args.run_id)
        totals["verified"] += summary["verified"]
        for result in summary["results"].values():
            totals["results"][result] = totals["results"].get(result, 0) + 1
        print(f"{product_dir}: {summary['verified']}/{len(claim_ids)} "
              f"{summary['results'] and sorted(set(summary['results'].values()))}")
        if summary["stopped"]:
            stopped = summary["stopped"]
            break
    run.finish("stopped: " + stopped if stopped else "complete")
    spent = run.cap - run.remaining_usd() if run.remaining_usd() <= run.cap else 0
    print(f"verified {totals['verified']}/{len(manifest['inputs']['claims'])}: {totals['results']}")
    print(f"counted spend (actual, or worst case where unreported): ${spent:.4f}")
    if stopped:
        print(f"STOPPED: {stopped}")
    return 1 if stopped else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--run-id", required=True)
    plan_parser.add_argument("--cap", type=float, default=1.0)
    plan_parser.set_defaults(func=plan)
    exec_parser = sub.add_parser("execute")
    exec_parser.add_argument("--run-id", required=True)
    exec_parser.add_argument("--approval-id", required=True)
    exec_parser.set_defaults(func=execute)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
