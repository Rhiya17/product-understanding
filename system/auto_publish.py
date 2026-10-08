#!/usr/bin/env python3
"""Automatic, auditable publishing policy (replaces the human-review dependency).

A claim is AUTO_APPROVED for its current digest only when every check passes:

1. source_support: every binding is a text binding whose full quote is found
   in the hash-pinned source (``PackEvidence.authenticate_binding``).
2. product_match: the claim's subject is the pack's product, and its
   applicability does not name a different SKU, market or body than the pack
   identity supports (see ``_product_match``).
3. independent_verification: the latest semantic receipt for this exact digest
   is ENTAILED from a non-Claude ``qwen/*`` model, and no alarm is outstanding.
4. no_unresolved_contradiction: if the claim is in a recorded CONFLICT group,
   an automatic resolution (rules in docs/architecture/auto-publish-policy.md)
   must let it be served.

Decisions and resolutions are appended to
``evidence-packs/<product>/auto-publish-decisions.jsonl``. They are machine
decisions, never presented as human review; a human disposition in
reviews.json always takes precedence. The policy runs only on the packs it is
invoked for.

    python -m system.auto_publish --product tesla-model-y [--dry-run]
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from system import evidence_status  # noqa: E402

POLICY_VERSION = "auto-publish-v1"
DECISIONS_FILE = evidence_status.AUTO_DECISIONS_FILE
DECIDED_BY = "system/auto_publish.py (automated policy; not a human review)"
SERVABLE_OUTCOMES = {"SERVE", "SERVE_SCOPED", "SERVE_AS_RANGE"}
CONFLICT_RE = re.compile(r"CONFLICT:\s*contradicts\s+([^.]*)", re.I)
CLAIM_ID_RE = re.compile(r"claim_[a-z0-9_]+")

# Rule R1: rank by who actually made the statement (lower is stronger).
AUTHORITY_RANK = {
    "MANUFACTURER": 0,
    "BRAND_STATEMENT": 1,
    "THIRD_PARTY_MEASUREMENT": 2,
    "RETAILER": 3,
    "COMMUNITY": 4,
    "UNKNOWN": 5,
}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def statement_authority(claim, sources):
    """Who authored the statement: object.authority_note beats the file label."""
    note = str((claim.get("object") or {}).get("authority_note") or "").lower()
    if note:
        if "not brand-authored" in note or "retailer data" in note:
            return "RETAILER"
        if "consumer care" in note or "brand account" in note or "brand-authored" in note:
            return "BRAND_STATEMENT"
        if "retailer" in note:
            return "RETAILER"
    authorities = []
    for binding in claim.get("source_bindings", []):
        source = sources.get(binding.get("source_id")) or {}
        authority = str(source.get("authority") or claim.get("authority") or "UNKNOWN").upper()
        if authority.startswith("MANUFACTURER"):
            authorities.append("MANUFACTURER")
        elif authority in AUTHORITY_RANK:
            authorities.append(authority)
        else:
            authorities.append("UNKNOWN")
    if not authorities:
        return "UNKNOWN"
    return min(authorities, key=AUTHORITY_RANK.get)


def unusable_value(claim):
    """Rule R3: unlabeled axes or bound-only statements cannot be applied."""
    obj = claim.get("object") or {}
    if "axes" in obj and obj.get("axes") is None and obj.get("values"):
        return "axes_not_labelled"
    qualifier = str(obj.get("qualifier") or "").lower()
    if "upper bound" in qualifier or "less than" in qualifier:
        return "bound_only_statement"
    return None


def _scope_key(claim):
    app = claim.get("applicability") or {}
    return (app.get("market"), app.get("body"), app.get("trim"), app.get("configuration"))


def conflict_groups(claims):
    """Connected components of the CONFLICT graph from extraction notes."""
    edges = {}
    for claim_id, claim in claims.items():
        for match in CONFLICT_RE.finditer(str(claim.get("extraction_notes") or "")):
            for other in CLAIM_ID_RE.findall(match.group(1)):
                if other in claims and other != claim_id:
                    edges.setdefault(claim_id, set()).add(other)
                    edges.setdefault(other, set()).add(claim_id)
    seen, groups = set(), []
    for start in sorted(edges):
        if start in seen:
            continue
        stack, group = [start], set()
        while stack:
            node = stack.pop()
            if node in group:
                continue
            group.add(node)
            stack.extend(edges.get(node, ()))
        seen |= group
        groups.append(sorted(group))
    return groups


def resolve_conflict(group, claims, sources):
    """Apply rules R2 (scope), R3 (unusable), R1 (authority), R4 (range)."""
    outcomes, rationale = {}, []
    scopes = {cid: _scope_key(claims[cid]) for cid in group}
    if len(set(scopes.values())) == len(group):
        for cid in group:
            outcomes[cid] = "SERVE_SCOPED"
        rationale.append("R2: every claim has a distinct applicability scope "
                         "(market/body/trim/configuration); not a contradiction.")
        return "R2_SCOPE", outcomes, rationale
    usable = []
    for cid in group:
        reason = unusable_value(claims[cid])
        if reason:
            outcomes[cid] = "EXCLUDED"
            rationale.append(f"R3: {cid} excluded ({reason}).")
        else:
            usable.append(cid)
    if not usable:
        return "R3_UNUSABLE", outcomes, rationale
    ranks = {cid: AUTHORITY_RANK[statement_authority(claims[cid], sources)] for cid in usable}
    best = min(ranks.values())
    top = [cid for cid in usable if ranks[cid] == best]
    rule = "R1_AUTHORITY"
    if len(top) == 1:
        outcomes[top[0]] = "SERVE"
        rationale.append(f"R1: {top[0]} has the strongest statement authority "
                         f"({statement_authority(claims[top[0]], sources)}).")
    else:
        rule = "R4_RANGE"
        for cid in top:
            outcomes[cid] = "SERVE_AS_RANGE"
        rationale.append("R4: equal-authority statements disagree; serve them together as "
                         "a range and use the safety-conservative value in warnings and "
                         "fit checks.")
    for cid in usable:
        if cid not in top:
            outcomes[cid] = "SUPERSEDED"
            rationale.append(f"R1: {cid} superseded by a stronger statement; still usable "
                             "as a conservative bound in deterministic fit checks (R5).")
    return rule, outcomes, rationale


def _identity(pack):
    manifest = evidence_status.load_json(pack.vault_dir / "manifest.json", {})
    return manifest.get("product_id"), manifest.get("identity") or {}


def _product_match(claim, product_id, identity):
    problems = []
    if claim.get("subject") != product_id:
        problems.append(f"subject {claim.get('subject')!r} is not {product_id!r}")
    app = claim.get("applicability") or {}
    skus = {identity.get("model_number")} | set(identity.get("equivalent_skus") or [])
    skus.discard(None)
    if app.get("sku") and skus and app["sku"] not in skus:
        problems.append(f"sku {app['sku']} not in identity {sorted(skus)}")
    body = str(app.get("body") or "").lower()
    if body and ("legacy" in body or "2020" in body):
        problems.append(f"body {app.get('body')!r} is a superseded body")
    market = app.get("market")
    if market and identity.get("market") and market != identity["market"]:
        shared = identity.get("body_equivalence") or {}
        if market not in (shared.get("markets") or []) or not claim_is_physical(claim):
            problems.append(f"market {market} differs from {identity['market']} "
                            "without a recorded body equivalence")
    return problems


def claim_is_physical(claim):
    obj = claim.get("object") or {}
    text = " ".join([str(claim.get("predicate") or ""), str(obj.get("measured_quantity") or "")])
    return claim.get("type") == "SPEC" and bool(re.search(
        r"dimension|length|width|height|depth|opening|lip|floor|volume|clearance", text, re.I))


def evaluate(pack, resolutions):
    product_id, identity = _identity(pack)
    by_claim = {}
    for res in resolutions:
        for cid, outcome in res["outcomes"].items():
            by_claim[cid] = (res, outcome)
    in_conflict = {cid for res in resolutions for cid in res["claims"]}
    decisions = []
    for claim_id, claim in pack.claims.items():
        digest = evidence_status.claim_digest(claim)
        checks, reasons = {}, []
        bindings = [pack.authenticate_binding(b) for b in claim.get("source_bindings", [])]
        support = bool(bindings) and all(s in evidence_status.AUTHENTICATED for s in bindings)
        checks["source_support"] = {"pass": support, "bindings": bindings}
        if not support:
            reasons.append("source_support")
        problems = _product_match(claim, product_id, identity)
        checks["product_match"] = {"pass": not problems, "problems": problems}
        if problems:
            reasons.append("product_match")
        receipt = pack.current_receipt(claim_id, digest)
        model = (receipt or {}).get("serving_model") or (receipt or {}).get("model") or ""
        verified = (receipt is not None and receipt.get("kind") == "semantic_check"
                    and receipt.get("result") == "ENTAILED" and model.startswith("qwen/")
                    and not pack.alarm_outstanding(claim_id, digest))
        checks["independent_verification"] = {
            "pass": verified, "receipt_id": (receipt or {}).get("receipt_id"),
            "result": (receipt or {}).get("result"), "model": model or None}
        if not verified:
            reasons.append("independent_verification")
        if claim_id in in_conflict:
            res, outcome = by_claim[claim_id]
            ok = outcome in SERVABLE_OUTCOMES
            checks["no_unresolved_contradiction"] = {
                "pass": ok, "resolution_id": res["resolution_id"], "outcome": outcome}
            if not ok:
                reasons.append(f"contradiction_{outcome.lower()}")
        else:
            checks["no_unresolved_contradiction"] = {"pass": True, "resolution_id": None}
        decisions.append({
            "kind": "auto_decision", "claim_id": claim_id, "claim_digest": digest,
            "decision": "AUTO_APPROVED" if not reasons else "AUTO_HELD",
            "failed_checks": reasons, "checks": checks,
            "consequence_ceiling": claim.get("consequence_ceiling"),
            "policy": POLICY_VERSION, "decided_by": DECIDED_BY})
    return decisions


def build_resolutions(pack):
    _, identity = _identity(pack)
    sources = pack.sources
    out = []
    for group in conflict_groups(pack.claims):
        rule, outcomes, rationale = resolve_conflict(group, pack.claims, sources)
        digests = {cid: evidence_status.claim_digest(pack.claims[cid]) for cid in group}
        rid = "cres_" + hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()[:12]
        out.append({"kind": "conflict_resolution", "resolution_id": rid, "claims": group,
                    "claim_digests": digests, "rule": rule, "outcomes": outcomes,
                    "rationale": rationale, "policy": POLICY_VERSION, "decided_by": DECIDED_BY})
    return out


def run(product_dir, packs_root=evidence_status.PACKS_ROOT,
        vault_root=evidence_status.VAULT_ROOT, dry_run=False):
    pack = evidence_status.PackEvidence(product_dir, packs_root=packs_root, vault_root=vault_root)
    resolutions = build_resolutions(pack)
    decisions = evaluate(pack, resolutions)
    if not dry_run:
        path = Path(pack.pack_dir) / DECISIONS_FILE
        with path.open("a", encoding="utf-8") as handle:
            for record in resolutions + decisions:
                handle.write(json.dumps({"at": _now(), **record},
                                        ensure_ascii=False, sort_keys=True) + "\n")
    return resolutions, decisions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--product", required=True, action="append")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    for product in args.product:
        resolutions, decisions = run(product, dry_run=args.dry_run)
        approved = sum(d["decision"] == "AUTO_APPROVED" for d in decisions)
        held = {}
        for d in decisions:
            for reason in d["failed_checks"]:
                held[reason] = held.get(reason, 0) + 1
        print(f"{product}: {approved}/{len(decisions)} AUTO_APPROVED; "
              f"{len(resolutions)} conflict resolution(s); held by check: {held}")
        for res in resolutions:
            print(f"  {res['resolution_id']} {res['rule']}: {res['outcomes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
