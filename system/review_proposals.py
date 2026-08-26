#!/usr/bin/env python3
"""Render owner-facing review proposals without writing dispositions."""

import argparse
from collections import Counter
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from system import review_queue
except ModuleNotFoundError:
    import review_queue


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"

# Manual post-run audit of v2 survivors. These remain visible as alarms, but
# the owner should not spend time treating value/unit serialization as a claim
# defect when each metric sibling already carries its own unit.
POST_RUN_AUDIT_NOTES = {
    claim_id: (
        "LIKELY VERIFIER NOISE — the primary value/unit pair and the metric "
        "sibling are unambiguous in the object, and each matches the quote. "
        "The verifier incorrectly treated the primary unit as global."
    )
    for claim_id in {
        "claim_c300s_spec_dimensions",
        "claim_c300s_spec_weight_300s",
        "claim_c300s_spec_weight_300sp",
        "claim_c300s_spec_cadr",
        "claim_c300s_spec_operating_conditions",
    }
}


def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def classify(pack_dir):
    pack_dir = Path(pack_dir)
    product = pack_dir.name
    claims = load_json(pack_dir / "claims.json", [])
    verdicts_doc = load_json(pack_dir / "verdicts.json", None)
    reviews_doc = load_json(pack_dir / "reviews.json", {"reviews": []})
    reviews = reviews_doc.get("reviews", [])
    human = review_queue.human_reviewed_claims(reviews)
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

    triage_by_pair = {}
    triage_by_claim = {}
    if isinstance(verdicts_doc, dict):
        for entry in verdicts_doc.get("conflict_triage", []):
            pair = entry.get("pair")
            if isinstance(pair, list) and len(pair) == 2:
                key = tuple(sorted(pair))
                triage_by_pair[key] = entry
                for claim_id in key:
                    triage_by_claim.setdefault(claim_id, []).append(entry)

    unresolved_pairs = [
        pair for pair in review_queue.conflict_pairs(claims)
        if pair[0] not in human and pair[1] not in human
        and pair[0] not in alarm_ids and pair[1] not in alarm_ids
    ]
    conflict_ids = {claim_id for pair in unresolved_pairs for claim_id in pair}

    alarms = [by_id[claim_id] for claim_id in sorted(alarm_ids)]
    conflict_claims = []
    seen_conflicts = set()
    for pair in unresolved_pairs:
        for claim_id in pair:
            if claim_id not in seen_conflicts:
                conflict_claims.append(by_id[claim_id])
                seen_conflicts.add(claim_id)

    c3 = [claim for claim in claims
          if claim.get("consequence_ceiling") == "C3"
          and claim["claim_id"] not in human | alarm_ids | conflict_ids]
    c2 = [claim for claim in claims
          if claim.get("consequence_ceiling") == "C2"
          and claim["claim_id"] not in human | alarm_ids | conflict_ids]

    unresolved = []
    batch_eligible = []
    for claim in claims:
        claim_id = claim["claim_id"]
        if claim.get("consequence_ceiling") not in {"C0", "C1"}:
            continue
        if claim_id in human | alarm_ids | conflict_ids:
            continue
        reason = review_queue.unresolved_reason(
            claim, verification_status, verdicts_by_claim.get(claim_id, []))
        if reason:
            unresolved.append((claim, reason))
        else:
            batch_eligible.append(claim)

    sample = review_queue.spot_audit_sample(product, batch_eligible)
    sample_ids = {claim["claim_id"] for claim in sample}
    undecided = {claim["claim_id"] for claim in claims} - human
    action_items = undecided | reopened_alarm_ids
    classified = (
        {claim["claim_id"] for claim in alarms}
        | {claim["claim_id"] for claim in conflict_claims}
        | {claim["claim_id"] for claim in c3}
        | {claim["claim_id"] for claim in c2}
        | {claim["claim_id"] for claim, _reason in unresolved}
        | {claim["claim_id"] for claim in batch_eligible}
    )
    if classified != action_items:
        missing = sorted(action_items - classified)
        extra = sorted(classified - action_items)
        raise ValueError(
            f"proposal classification mismatch; missing={missing}, extra={extra}")

    return {
        "product": product,
        "claims": claims,
        "human": human,
        "reopened_alarm_ids": reopened_alarm_ids,
        "verification_status": verification_status,
        "verdicts_by_claim": verdicts_by_claim,
        "triage_by_pair": triage_by_pair,
        "triage_by_claim": triage_by_claim,
        "alarms": alarms,
        "conflict_pairs": unresolved_pairs,
        "conflict_claims": conflict_claims,
        "c3": c3,
        "c2": c2,
        "unresolved": unresolved,
        "batch_eligible": batch_eligible,
        "sample_ids": sample_ids,
        "gaps": load_json(pack_dir / "gaps.json", {"gaps": []}).get("gaps", []),
    }


def recommendation(claim, verdicts, queue_section, unresolved_reason=None):
    revision = str(claim.get("applicability", {}).get("revision") or "").lower()
    retired_only = any(marker in revision for marker in (
        "absent from 300s-p",
        "original revision only",
        "legacy revision only",
        "retired revision",
    ))
    if retired_only:
        result = "REJECTED_FOR_SERVING"
        rationale = (
            "Latest-revision-only policy: this claim applies only to an older "
            "hardware revision and is not documented for the current revision; "
            "retain the CANDIDATE record but do not serve it.")
    elif queue_section == "alarm":
        result = "NEEDS_RECHECK"
        changed = [entry.get("note", "Verifier reported a meaning change.")
                   for entry in verdicts
                   if entry.get("verdict") == "MEANING_CHANGED"]
        rationale = "Verifier found a meaning change: " + " ".join(changed)
    elif queue_section in {"conflict", "unresolved"}:
        result = "NEEDS_RECHECK"
        rationale = (unresolved_reason or
                     "The unresolved source conflict requires an owner authority ruling.")
    else:
        result = "APPROVED_FOR_PUBLISH"
        rationale = (
            "Every source binding is ENTAILED by the pinned verifier and no "
            "unresolved conflict applies; publication still requires owner confirmation.")
    return result, rationale


def review_focus(claim, section, triage_entries):
    flags = []
    if section == "alarm":
        flags.append("HARD REVIEW — verifier MEANING_CHANGED")
    if claim.get("consequence_ceiling") == "C3":
        flags.append("HARD REVIEW — C3; individual decision required")
    if claim.get("consequence_ceiling") == "C2":
        flags.append("C2; individual decision required")
    notes = (claim.get("extraction_notes") or "").lower()
    if any(word in notes for word in
           ("ambiguous", "applicability", "legacy", "revision", "judgment")):
        flags.append("Extractor flagged applicability or interpretation context")
    for entry in triage_entries:
        flags.append(
            f"Conflict triage: {entry.get('result')} — {entry.get('note')}")
    return flags or ["Standard review"]


def claim_lines(claim, verdicts, section, triage_entries,
                unresolved_reason=None, sample=False, reopened=False):
    disposition, rationale = recommendation(
        claim, verdicts, section, unresolved_reason=unresolved_reason)
    lines = [
        f"### `{claim['claim_id']}`"
        + (" — REOPENED AFTER V2 ALARM" if reopened else "")
        + (" — SPOT-AUDIT SAMPLE" if sample else ""),
        "",
        f"- Proposed disposition: **`{disposition}`**",
        f"- Owner decision: [ ] confirm recommendation  [ ] override: __________",
        f"- Claim tier: `{claim.get('consequence_ceiling')}`",
        f"- Type / predicate: `{claim.get('type')}` / `{claim.get('predicate')}`",
        f"- Source authority: `{claim.get('authority')}`",
        f"- Queue section: `{section}`",
        *( ["- Prior decision status: **REOPENED** — explicitly reconfirm or "
             "amend the existing human disposition."] if reopened else []),
        "- Review focus: " + "; ".join(
            review_focus(claim, section, triage_entries)),
        *( ["- Agent post-run audit: " + POST_RUN_AUDIT_NOTES[claim["claim_id"]]]
           if claim["claim_id"] in POST_RUN_AUDIT_NOTES else []),
        "- Proposed rationale: " + rationale,
        "",
        "Applicability",
        "",
        review_queue.fenced(claim.get("applicability"), "json"),
        "",
        "Object",
        "",
        review_queue.fenced(claim.get("object"), "json"),
    ]
    for binding_index, binding in enumerate(claim.get("source_bindings", [])):
        lines.extend([
            "",
            f"Quote — binding {binding_index}, source `{binding.get('source_id')}`, "
            f"page `{binding.get('page')}`",
            "",
            review_queue.fenced(binding.get("quote", ""), "text"),
        ])
        matching = [entry for entry in verdicts
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
    ])
    if disposition == "NEEDS_RECHECK":
        if claim.get("type") == "STEP":
            path = ("Rewrite the procedure step to contain only details supported by "
                    "its cited span, or add an authoritative binding that supports the "
                    "full action; then re-run verification so the procedure can become "
                    "servable for video generation.")
        else:
            path = ("Correct the structured translation or add an authoritative quote "
                    "that supports every stated detail, then re-run verification.")
        lines.extend(["", "Rework path: " + path])
    lines.append("")
    return lines


def render_pack(pack_dir, date=None):
    pack_dir = Path(pack_dir)
    data = classify(pack_dir)
    date = date or dt.date.today().isoformat()
    batch_id = f"batch_{data['product']}_{date.replace('-', '')}"
    verdicts_by_claim = data["verdicts_by_claim"]
    triage_by_claim = data["triage_by_claim"]
    undecided_count = len(data["claims"]) - len(data["human"])
    reopened_count = len(data["reopened_alarm_ids"])
    proposal_items = []
    proposal_items.extend((claim, "alarm", None) for claim in data["alarms"])
    proposal_items.extend(
        (claim, "conflict", None) for claim in data["conflict_claims"])
    proposal_items.extend((claim, "c3", None) for claim in data["c3"])
    proposal_items.extend((claim, "c2", None) for claim in data["c2"])
    proposal_items.extend(
        (claim, "unresolved", reason) for claim, reason in data["unresolved"])
    proposal_items.extend(
        (claim, "batch_eligible", None) for claim in data["batch_eligible"])
    proposed_counts = Counter(
        recommendation(
            claim, verdicts_by_claim.get(claim["claim_id"], []), section,
            unresolved_reason=reason)[0]
        for claim, section, reason in proposal_items
    )

    lines = [
        f"# Review Proposals — {data['product']}",
        "",
        f"Generated: `{date}`",
        f"Verification status: `{data['verification_status'] or 'NOT_RUN'}`",
        "",
        "This is an advisory proposal document, not a publication record. Only "
        "the product owner may mark decisions here. An unmarked item is undecided.",
        "",
        "## Decision summary",
        "",
        f"- Claims in pack: `{len(data['claims'])}`",
        f"- Existing human decisions: `{len(data['human'])}`",
        f"- Undecided claims covered here: `{undecided_count}`",
        f"- Existing decisions reopened by v2 alarms: `{reopened_count}`",
        f"- Total owner action items: `{undecided_count + reopened_count}`",
        f"- Proposed `NEEDS_RECHECK`: `{proposed_counts['NEEDS_RECHECK']}`",
        f"- Proposed `REJECTED_FOR_SERVING`: "
        f"`{proposed_counts['REJECTED_FOR_SERVING']}`",
        f"- Proposed `APPROVED_FOR_PUBLISH`: "
        f"`{proposed_counts['APPROVED_FOR_PUBLISH']}`",
        f"- Batch-eligible C0/C1: `{len(data['batch_eligible'])}`",
        "",
        "For C2/C3, mark every item individually. For section 7, inspect every "
        "designated sample item; then either confirm the batch statement or mark "
        "the sample as failed and decide every batch member individually.",
        "",
        "## 1. MEANING_CHANGED alarms " + f"({len(data['alarms'])})",
        "",
    ]
    if not data["alarms"]:
        lines.extend(["None.", ""])
    for claim in data["alarms"]:
        claim_id = claim["claim_id"]
        lines.extend(claim_lines(
            claim, verdicts_by_claim.get(claim_id, []), "alarm",
            triage_by_claim.get(claim_id, []),
            reopened=claim_id in data["reopened_alarm_ids"]))

    lines.extend([
        "## 2. Unresolved conflict claims " +
        f"({len(data['conflict_claims'])} claims / {len(data['conflict_pairs'])} pairs)",
        "",
    ])
    if not data["conflict_claims"]:
        lines.extend(["None outside section 1 or existing human decisions.", ""])
    for pair in data["conflict_pairs"]:
        annotation = data["triage_by_pair"].get(tuple(sorted(pair)))
        if annotation:
            lines.extend([
                f"Pair `{pair[0]}` ↔ `{pair[1]}`: `{annotation.get('result')}` — "
                f"{annotation.get('note')}",
                "",
            ])
    for claim in data["conflict_claims"]:
        claim_id = claim["claim_id"]
        lines.extend(claim_lines(
            claim, verdicts_by_claim.get(claim_id, []), "conflict",
            triage_by_claim.get(claim_id, [])))

    for number, title, key in (
            (3, "C3 claims", "c3"), (4, "C2 claims", "c2")):
        claims = data[key]
        lines.extend([f"## {number}. {title} ({len(claims)})", ""])
        if not claims:
            lines.extend(["None.", ""])
        for claim in claims:
            claim_id = claim["claim_id"]
            lines.extend(claim_lines(
                claim, verdicts_by_claim.get(claim_id, []), key,
                triage_by_claim.get(claim_id, [])))

    lines.extend([
        "## 5. Unresolved verifier — C0/C1 " +
        f"({len(data['unresolved'])})",
        "",
    ])
    if not data["unresolved"]:
        lines.extend(["None.", ""])
    for claim, reason in data["unresolved"]:
        claim_id = claim["claim_id"]
        lines.extend(claim_lines(
            claim, verdicts_by_claim.get(claim_id, []), "unresolved",
            triage_by_claim.get(claim_id, []), unresolved_reason=reason))

    lines.extend([f"## 6. Open gaps ({len(data['gaps'])})", ""])
    if not data["gaps"]:
        lines.extend(["None.", ""])
    for gap in data["gaps"]:
        lines.extend([
            f"### `{gap.get('gap_id', '<unnamed gap>')}`",
            "",
            f"- Kind: `{gap.get('kind')}`",
            f"- Waives: `{json.dumps(gap.get('waives', []), ensure_ascii=False)}`",
            f"- Reason: {gap.get('reason') or 'None recorded.'}",
            f"- Closes when: {gap.get('closes_when') or 'Not recorded.'}",
            "",
        ])

    lines.extend([
        "## 7. Batch-eligible C0/C1 spot-audit " +
        f"({len(data['batch_eligible'])})",
        "",
    ])
    if not data["batch_eligible"]:
        lines.extend(["None.", ""])
    else:
        lines.extend([
            f"Batch ID: `{batch_id}`",
            "",
            f"- [ ] OWNER CONFIRMS: I reviewed all "
            f"`{len(data['sample_ids'])}` designated sample claims and confirm "
            f"`APPROVED_FOR_PUBLISH` for all "
            f"`{len(data['batch_eligible'])}` members of `{batch_id}`.",
            "- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below "
            "individually.",
            "- Owner / date: ______________________________",
            "",
        ])
        for claim in data["batch_eligible"]:
            claim_id = claim["claim_id"]
            lines.extend(claim_lines(
                claim, verdicts_by_claim.get(claim_id, []), "batch_eligible",
                triage_by_claim.get(claim_id, []),
                sample=claim_id in data["sample_ids"]))

    output = "\n".join(lines).rstrip() + "\n"
    path = pack_dir / "review-proposals.md"
    path.write_text(output, encoding="utf-8")
    return {
        "product": data["product"],
        "undecided": undecided_count,
        "reopened_alarms": reopened_count,
        "needs_recheck": proposed_counts["NEEDS_RECHECK"],
        "proposed_reject": proposed_counts["REJECTED_FOR_SERVING"],
        "proposed_approve": proposed_counts["APPROVED_FOR_PUBLISH"],
        "batch_eligible": len(data["batch_eligible"]),
        "sample": len(data["sample_ids"]),
        "path": str(path),
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
        print(json.dumps(render_pack(pack), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
