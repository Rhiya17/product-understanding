#!/usr/bin/env python3
"""Render ordered, human-readable evidence-pack review queues."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"


def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def human_reviewed_claims(reviews):
    return {
        review.get("claim_id") for review in reviews
        if isinstance(review.get("reviewer"), str)
        and not review["reviewer"].startswith("system:")
        and review.get("disposition")
    }


SPOT_AUDIT_SIZE = 5


def spot_audit_sample(product, claims, size=SPOT_AUDIT_SIZE):
    """Select a stable, auditable pseudo-random sample from eligible claims."""
    ranked = sorted(
        claims,
        key=lambda claim: hashlib.sha256(
            f"review-completion-v1\0{product}\0{claim['claim_id']}".encode()
        ).hexdigest(),
    )
    return ranked[:size]


def conflict_pairs(claims):
    try:
        from system.verify_claims import conflict_pairs as find_pairs
    except ModuleNotFoundError:
        from verify_claims import conflict_pairs as find_pairs
    return find_pairs(claims)


def fenced(value, language):
    if language == "json":
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    else:
        text = str(value)
    return f"```{language}\n{text}\n```"


def claim_block(claim, verdict_entries, heading=None, unresolved_reason=None):
    title = heading or claim["claim_id"]
    lines = [
        f"### {title}",
        "",
        f"- Claim: `{claim['claim_id']}`",
        f"- Tier: `{claim.get('consequence_ceiling')}`",
        f"- Type/predicate: `{claim.get('type')}` / `{claim.get('predicate')}`",
    ]
    if unresolved_reason:
        lines.append(f"- Verifier state: {unresolved_reason}")
    lines.extend(["", "Object", "", fenced(claim.get("object"), "json")])
    for binding_index, binding in enumerate(claim.get("source_bindings", [])):
        lines.extend([
            "",
            f"Quote — binding {binding_index}, source `{binding.get('source_id')}`",
            "",
            fenced(binding.get("quote", ""), "text"),
        ])
        matching = [entry for entry in verdict_entries
                    if entry.get("binding_index") == binding_index]
        if matching:
            entry = matching[0]
            basis = (" (claim quote union)"
                     if entry.get("basis") == "CLAIM_QUOTE_UNION" else "")
            lines.extend([
                "",
                f"Verifier{basis}: `{entry.get('verdict')}` — "
                f"{entry.get('note')}",
            ])
        else:
            lines.extend(["", "Verifier: no verdict recorded."])
    lines.extend([
        "",
        "Extractor notes: " + (claim.get("extraction_notes") or "None recorded."),
        "",
    ])
    return lines


def conflict_block(pair, by_id, verdicts_by_claim, triage):
    lines = [f"### Conflict: `{pair[0]}` ↔ `{pair[1]}`", ""]
    annotation = triage.get(tuple(pair))
    if annotation:
        lines.append(
            f"Triage (advisory): `{annotation.get('result')}` — {annotation.get('note')}")
        lines.append("")
    else:
        lines.extend(["Triage (advisory): not run.", ""])
    for claim_id in pair:
        claim = by_id[claim_id]
        lines.extend(claim_block(
            claim, verdicts_by_claim.get(claim_id, []),
            heading=f"{claim_id} ({claim.get('consequence_ceiling')})"))
    return lines


def unresolved_reason(claim, verification_status, entries):
    if verification_status is None:
        return "no verdicts.json exists"
    if verification_status in {"PARTIAL", "FAILED"}:
        return f"document status is {verification_status}"
    expected = set(range(len(claim.get("source_bindings", []))))
    present = {entry.get("binding_index") for entry in entries}
    if present != expected:
        return "one or more binding verdicts are missing"
    if any(entry.get("verdict") == "CANNOT_JUDGE" for entry in entries):
        return "one or more bindings are CANNOT_JUDGE"
    if any(entry.get("verdict") != "ENTAILED" for entry in entries):
        return "the verdict set is not all-ENTAILED"
    return None


def render_pack(pack_dir):
    pack_dir = Path(pack_dir)
    product = pack_dir.name
    claims = load_json(pack_dir / "claims.json", [])
    gaps_doc = load_json(pack_dir / "gaps.json", {"gaps": []})
    verdicts_doc = load_json(pack_dir / "verdicts.json", None)
    reviews_doc = load_json(pack_dir / "reviews.json", {"reviews": []})
    reviews = reviews_doc.get("reviews", [])
    human = human_reviewed_claims(reviews)
    by_id = {claim["claim_id"]: claim for claim in claims}

    verdict_entries = verdicts_doc.get("verdicts", []) \
        if isinstance(verdicts_doc, dict) else []
    verification_status = verdicts_doc.get("status") \
        if isinstance(verdicts_doc, dict) else None
    verdicts_by_claim = {}
    for entry in verdict_entries:
        verdicts_by_claim.setdefault(entry.get("claim_id"), []).append(entry)

    alarm_ids = {
        claim_id for claim_id, entries in verdicts_by_claim.items()
        if any(entry.get("verdict") == "MEANING_CHANGED" for entry in entries)
    }
    reopened_alarm_ids = alarm_ids & human

    triage = {}
    if isinstance(verdicts_doc, dict):
        for entry in verdicts_doc.get("conflict_triage", []):
            pair = entry.get("pair")
            if isinstance(pair, list) and len(pair) == 2:
                triage[tuple(sorted(pair))] = entry
    unresolved_pairs = [
        pair for pair in conflict_pairs(claims)
        if pair[0] not in human and pair[1] not in human
        and pair[0] not in alarm_ids and pair[1] not in alarm_ids
    ]
    conflict_ids = {claim_id for pair in unresolved_pairs for claim_id in pair}

    c3 = [claim for claim in claims
          if claim.get("consequence_ceiling") == "C3"
          and claim["claim_id"] not in human | alarm_ids | conflict_ids]
    c2 = [claim for claim in claims
          if claim.get("consequence_ceiling") == "C2"
          and claim["claim_id"] not in human | alarm_ids | conflict_ids]

    unresolved = []
    for claim in claims:
        claim_id = claim["claim_id"]
        if claim.get("consequence_ceiling") not in {"C0", "C1"}:
            continue
        if claim_id in human | alarm_ids | conflict_ids:
            continue
        reason = unresolved_reason(
            claim, verification_status, verdicts_by_claim.get(claim_id, []))
        if reason:
            unresolved.append((claim, reason))

    batch_eligible = []
    for claim in claims:
        claim_id = claim["claim_id"]
        if claim.get("consequence_ceiling") not in {"C0", "C1"}:
            continue
        if claim_id in human | alarm_ids | conflict_ids:
            continue
        if unresolved_reason(
                claim, verification_status,
                verdicts_by_claim.get(claim_id, [])) is None:
            batch_eligible.append(claim)
    audit_sample = spot_audit_sample(product, batch_eligible)
    open_gaps = gaps_doc.get("gaps", []) if isinstance(gaps_doc, dict) else []

    sections = []
    sections.append(("1. MEANING_CHANGED alarms", [by_id[cid] for cid in sorted(alarm_ids)]))
    sections.append(("2. Unresolved conflict pairs", unresolved_pairs))
    sections.append(("3. C3 claims", c3))
    sections.append(("4. C2 claims", c2))
    sections.append(("5. Unresolved verifier — C0/C1", unresolved))
    sections.append(("6. Open gaps", open_gaps))
    sections.append(("7. Batch-eligible C0/C1 spot-audit", audit_sample))

    lines = [
        f"# Review Queue — {product}",
        "",
        f"Verification status: `{verification_status or 'NOT_RUN'}`",
        "",
        "Work top-to-bottom. Record human dispositions in `reviews.json`; do not "
        "edit claims or verifier verdicts.",
        f"A v2 alarm reopens `{len(reopened_alarm_ids)}` existing human "
        "disposition(s); those decisions must be explicitly reconfirmed or amended.",
        "",
    ]
    for section_index, (title, items) in enumerate(sections, 1):
        item_count = len(batch_eligible) if section_index == 7 else len(items)
        lines.extend([f"## {title} ({item_count})", ""])
        if not items:
            lines.extend(["None.", ""])
            continue
        if section_index == 2:
            for pair in items:
                lines.extend(conflict_block(
                    pair, by_id, verdicts_by_claim, triage))
        elif section_index == 5:
            for claim, reason in items:
                lines.extend(claim_block(
                    claim, verdicts_by_claim.get(claim["claim_id"], []),
                    unresolved_reason=reason))
        elif section_index == 6:
            for gap in items:
                lines.extend([
                    f"### {gap.get('gap_id', '<unnamed gap>')}",
                    "",
                    f"- Kind: `{gap.get('kind')}`",
                    f"- Waives: `{json.dumps(gap.get('waives', []), ensure_ascii=False)}`",
                    "",
                    "Reason: " + (gap.get("reason") or "None recorded."),
                    "",
                    "Closes when: " + (gap.get("closes_when") or "Not recorded."),
                    "",
                ])
        elif section_index == 7:
            lines.extend([
                f"Spot-audit sample: `{len(audit_sample)}` of "
                f"`{len(batch_eligible)}` eligible claims. The sample is the "
                "five lowest SHA-256 ranks of "
                "`review-completion-v1\\0<product>\\0<claim_id>`, so it is "
                "stable and reproducible.",
                "",
                "A clean sample may be confirmed as one explicit human batch "
                "decision. A failed sample removes batch eligibility; review "
                "every batch member individually.",
                "",
                "Batch members",
                "",
            ])
            lines.extend(f"- `{claim['claim_id']}`" for claim in batch_eligible)
            lines.extend(["", "Sample details", ""])
            for claim in items:
                lines.extend(claim_block(
                    claim, verdicts_by_claim.get(claim["claim_id"], [])))
        else:
            for claim in items:
                reopened_reason = None
                if section_index == 1 and claim["claim_id"] in reopened_alarm_ids:
                    reopened_reason = (
                        "REOPENED: v2 MEANING_CHANGED conflicts with an existing "
                        "human disposition")
                lines.extend(claim_block(
                    claim, verdicts_by_claim.get(claim["claim_id"], []),
                    unresolved_reason=reopened_reason))

    output = "\n".join(lines).rstrip() + "\n"
    (pack_dir / "review-queue.md").write_text(output, encoding="utf-8")
    return {
        "product": product,
        "alarms": len(alarm_ids),
        "reopened_alarms": len(reopened_alarm_ids),
        "conflicts": len(unresolved_pairs),
        "c3": len(c3),
        "c2": len(c2),
        "unresolved_verifier": len(unresolved),
        "gaps": len(open_gaps),
        "batch_eligible": len(batch_eligible),
        "spot_audit_sample": len(audit_sample),
        "path": str(pack_dir / "review-queue.md"),
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", help="render one product; default is all packs")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.product:
        packs = [PACKS_ROOT / args.product]
    else:
        packs = sorted(path.parent for path in PACKS_ROOT.glob("*/claims.json"))
    if not packs or any(not (pack / "claims.json").exists() for pack in packs):
        print("ERROR: requested evidence pack does not exist", file=sys.stderr)
        return 1
    for pack in packs:
        result = render_pack(pack)
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
