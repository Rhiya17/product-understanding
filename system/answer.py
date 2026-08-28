#!/usr/bin/env python3
"""Local evidence-graph answer tool: cited answers from reviewed claims.

Serving policy (LLD §9.2, review-completion work order):

- ``PUBLISHED``: latest human disposition is ``APPROVED_FOR_PUBLISH`` and no
  ``MEANING_CHANGED`` verdict is outstanding. Served by default.
- ``SUSPENDED``: approved, but the current verifier pass raised a
  ``MEANING_CHANGED`` alarm after the approval (a reopened decision). Not
  served by default.
- ``CANDIDATE``: no human decision yet (or ``NEEDS_RECHECK``/``NEEDS_REWORK``).
  Not served by default.
- ``REJECTED``: latest disposition is ``REJECTED_FOR_SERVING``. Never served;
  counted so the hidden-match notice stays honest.

``--preview`` additionally shows SUSPENDED and CANDIDATE matches, each
labeled. Retrieval is deliberately lexical — no model calls, no network.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"
VAULT_ROOT = REPO_ROOT / "source-vault"

SERVABLE_DEFAULT = {"PUBLISHED"}
PREVIEW_STATUSES = {"PUBLISHED", "SUSPENDED", "CANDIDATE"}

STOPWORDS = {
    "a", "an", "and", "are", "at", "be", "can", "do", "does", "for", "from",
    "how", "i", "if", "in", "is", "it", "its", "many", "much", "my", "of",
    "on", "or", "tell", "that", "the", "this", "to", "what", "whats", "when",
    "where", "which", "will", "with", "you", "your",
}

# Question vocabulary -> claim vocabulary. Kept small and literal on purpose.
SYNONYMS = {
    "weigh": "weight", "weighs": "weight", "heavy": "weight",
    "size": "dimensions", "big": "dimensions", "tall": "dimensions",
    "wide": "dimensions", "deep": "dimensions",
    "loud": "noise", "quiet": "noise", "volume": "noise",
    "folds": "fold", "folding": "fold", "collapse": "fold",
    "unfolds": "unfold", "unfolding": "unfold", "open": "unfold",
    "charging": "charge", "charges": "charge", "recharge": "charge",
    "cost": "price", "fit": "compatible", "fits": "compatible",
    "works": "compatible", "compatibility": "compatible",
    "clean": "care", "cleaning": "care", "wash": "care", "washing": "care",
    "expire": "expiration", "expires": "expiration", "expiry": "expiration",
    "looks": "dimensions", "look": "dimensions", "appearance": "dimensions",
    "pairing": "pair", "paired": "pair",
}

PREDICATE_LABELS = {
    "maximum_child_weight": "Maximum child weight",
    "minimum_child_weight": "Minimum child weight",
    "product_weight": "Product weight",
    "product_dimensions": "Product dimensions",
    "procedure_step": "Procedure step",
}

SOURCE_TYPE_LABELS = {
    "MANUAL_PDF": "owner's manual",
    "SPEC_DOC_PDF": "specification document",
    "SPEC_PAGE": "product specifications",
    "SUPPORT_PAGE": "support page",
    "GUIDE": "guide",
    "IMAGE": "manufacturer image",
    "VIDEO": "manufacturer video",
    "VIDEO_URL": "manufacturer video",
}


def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def records(payload, key):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    return []


def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", str(text).lower())
    return [SYNONYMS.get(token, token) for token in tokens
            if token not in STOPWORDS]


def semantic_projection(claim):
    try:
        from system.verify_claims import semantic_projection as project
    except ModuleNotFoundError:
        from verify_claims import semantic_projection as project
    return project(claim)


def load_catalog(vault_root=VAULT_ROOT):
    return load_json(vault_root / "catalog.json", {}).get("products", [])


def product_aliases(product):
    alias_text = " ".join(str(product.get(field, "")) for field in
                          ("brand", "model", "model_number", "category",
                           "dir", "product_id"))
    return set(tokenize(alias_text))


def product_identity_aliases(product):
    """Aliases that identify a product, excluding its shared category."""
    alias_text = " ".join(str(product.get(field, "")) for field in
                          ("brand", "model", "model_number", "dir",
                           "product_id"))
    category_tokens = set(tokenize(product.get("category", "")))
    return set(tokenize(alias_text)) - category_tokens


def detect_products(question_tokens, products):
    """Products whose aliases overlap the question; all products if none do."""
    scored = []
    for product in products:
        overlap = len(product_aliases(product) & set(question_tokens))
        if overlap:
            scored.append((overlap, product))
    if not scored:
        return products
    best = max(score for score, _ in scored)
    return [product for score, product in scored if score == best]


def clarification_candidates(question, products):
    """Return tied same-category products when no product name was supplied."""
    question_tokens = set(tokenize(question))
    if any(question_tokens & product_identity_aliases(product)
           for product in products):
        return []
    scored = []
    for product in products:
        category_tokens = set(tokenize(product.get("category", "")))
        score = len(question_tokens & category_tokens)
        if score:
            scored.append((score, product))
    if not scored:
        return []
    best = max(score for score, _ in scored)
    candidates = [product for score, product in scored if score == best]
    return candidates if len(candidates) > 1 else []


def latest_dispositions(reviews):
    dispositions = {}
    for review in records(reviews, "reviews"):
        claim_id = review.get("claim_id")
        if isinstance(claim_id, str) and review.get("disposition"):
            dispositions[claim_id] = review["disposition"]
    return dispositions


def alarmed_claims(verdicts):
    return {entry.get("claim_id")
            for entry in records(verdicts, "verdicts")
            if entry.get("verdict") == "MEANING_CHANGED"}


def claim_status(claim_id, dispositions, alarms):
    disposition = dispositions.get(claim_id)
    if disposition == "REJECTED_FOR_SERVING":
        return "REJECTED"
    if disposition == "APPROVED_FOR_PUBLISH":
        return "SUSPENDED" if claim_id in alarms else "PUBLISHED"
    return "CANDIDATE"


def score_claim(question_tokens, claim):
    predicate_tokens = set(tokenize(claim.get("predicate", "")))
    type_tokens = set(tokenize(claim.get("type", "")))
    body_tokens = set(tokenize(json.dumps(semantic_projection(claim),
                                          ensure_ascii=False)))
    quote_tokens = set()
    for binding in claim.get("source_bindings", []):
        quote_tokens.update(tokenize(binding.get("quote", "")))
    score = 0.0
    for token in set(question_tokens):
        if token in predicate_tokens:
            score += 3.0
        if token in type_tokens:
            score += 0.5
        if token in body_tokens:
            score += 1.0
        if token in quote_tokens:
            score += 1.0
    return score


def render_object(claim):
    projection = semantic_projection(claim)
    if not isinstance(projection, dict):
        return str(projection)
    parts = []
    for key, value in projection.items():
        if isinstance(value, dict):
            value = ", ".join(f"{k} {v}" for k, v in value.items())
        elif isinstance(value, list):
            value = "; ".join(str(item) for item in value)
        parts.append(f"{key}: {value}")
    return " | ".join(parts)


def readable_label(value):
    """Turn a stable identifier into restrained sentence-case copy."""
    value = str(value or "").replace("_", " ").strip()
    return value[:1].upper() + value[1:]


def _list_text(values):
    values = [str(value) for value in values]
    if len(values) < 2:
        return values[0] if values else ""
    return ", ".join(values[:-1]) + f", and {values[-1]}"


def _value_with_unit(obj):
    value = obj.get("value")
    unit = obj.get("unit")
    if isinstance(value, dict):
        dimensions = [value.get(key) for key in
                      ("width_in", "depth_in", "height_in")]
        if all(item is not None for item in dimensions):
            return " × ".join(str(item) for item in dimensions) + (
                f" {unit}" if unit else "")
        return ", ".join(str(item) for item in value.values())
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return f"{value}{f' {unit}' if unit else ''}"


def display_text(claim):
    """Render a deterministic human lead sentence for a claim.

    The underlying object is still returned separately for the Details
    disclosure. This renderer makes no factual additions and never calls a
    model.
    """
    obj = claim.get("object")
    if not isinstance(obj, dict):
        return str(obj)
    claim_type = claim.get("type")
    predicate = claim.get("predicate", "")
    label = PREDICATE_LABELS.get(predicate, readable_label(predicate))

    if claim_type == "STEP":
        procedure = readable_label(obj.get("procedure", "procedure"))
        number = obj.get("step_number")
        action = str(obj.get("action", "")).rstrip(".")
        return f"Step {number} of {procedure}: {action}."

    if claim_type == "WARNING":
        description = obj.get("description") or obj.get("warning")
        if description:
            return f"Warning: {str(description).rstrip('.')}."

    if claim_type == "COMPATIBILITY":
        counterpart = (obj.get("counterpart_name") or
                       obj.get("counterpart") or "the named product")
        if "compatible" in obj:
            verdict = "Compatible" if obj.get("compatible") else "Not compatible"
            lead = f"{verdict} with {counterpart}"
        else:
            relationship = obj.get("relationship") or obj.get("feature")
            lead = f"Works with {counterpart}"
            if relationship:
                lead += f" for {relationship}"
        qualifier = obj.get("qualifier") or obj.get("requirement")
        return lead + (f" — {qualifier}" if qualifier else "") + "."

    if claim_type == "PART_LOCATION" and obj.get("location_description"):
        return str(obj["location_description"]).rstrip(".") + "."

    if claim_type == "CARE":
        instruction = obj.get("instruction") or obj.get("method")
        if instruction:
            interval = f" {obj['interval']}" if obj.get("interval") else ""
            restrictions = obj.get("restrictions") or []
            suffix = (f" Avoid: {_list_text(restrictions)}."
                      if restrictions else "")
            return (f"{label}{interval}: {str(instruction).rstrip('.')}."
                    f"{suffix}")

    if "width" in obj and "height" in obj and "depth" in obj:
        unit = f" {obj['unit']}" if obj.get("unit") else ""
        return (f"{label}: {obj['width']} × {obj['height']} × "
                f"{obj['depth']}{unit} (width × height × depth).")

    if "value" in obj:
        lead = f"{label}: {_value_with_unit(obj)}"
        metric = obj.get("metric")
        if metric:
            lead += f" ({metric})"
        elif obj.get("metric_value") is not None:
            metric_unit = f" {obj.get('metric_unit')}" if obj.get("metric_unit") else ""
            lead += f" ({obj['metric_value']}{metric_unit})"
        context = (obj.get("context") or obj.get("conditions") or
                   obj.get("qualifier") or obj.get("rule") or obj.get("note"))
        if context:
            lead += f" — {context}"
        return lead.rstrip(".") + "."

    for field in ("description", "behavior", "instruction", "method",
                  "relationship", "state"):
        if obj.get(field):
            return f"{label}: {str(obj[field]).rstrip('.')}."

    values = []
    for value in obj.values():
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        elif isinstance(value, dict):
            values.extend(str(item) for item in value.values())
        elif value is not None:
            values.append(str(value))
    return f"{label}: {_list_text(values)}." if values else f"{label}."


def source_details(vault_root, product):
    product_dir = product["dir"]
    manifest = load_json(vault_root / product_dir / "manifest.json", {})
    brand = product.get("brand") or "Product"
    details = {}
    for source in manifest.get("sources", []):
        source_type = SOURCE_TYPE_LABELS.get(
            source.get("type"), readable_label(source.get("type", "source")))
        details[source.get("source_id")] = {
            "origin_url": source.get("origin_url"),
            "source_name": f"{brand} {source_type}",
        }
    return details


def search(question, packs_root=PACKS_ROOT, vault_root=VAULT_ROOT,
           product_dir=None, preview=False, top=3):
    all_tokens = tokenize(question)
    products = load_catalog(vault_root)
    if product_dir:
        products = [p for p in products if p.get("dir") == product_dir]
    else:
        products = detect_products(all_tokens, products)

    results, hidden = [], {"SUSPENDED": 0, "CANDIDATE": 0, "REJECTED": 0}
    wanted = PREVIEW_STATUSES if preview else SERVABLE_DEFAULT
    for product in products:
        # Product-name words select the pack; they must not score the facts.
        question_tokens = [token for token in all_tokens
                           if token not in product_aliases(product)]
        pack_dir = packs_root / product["dir"]
        claims = records(load_json(pack_dir / "claims.json", []), "claims")
        dispositions = latest_dispositions(
            load_json(pack_dir / "reviews.json", {}))
        alarms = alarmed_claims(load_json(pack_dir / "verdicts.json", {}))
        sources = source_details(vault_root, product)
        product_rows = []
        for claim in claims:
            score = score_claim(question_tokens, claim)
            if score <= 0:
                continue
            status = claim_status(claim["claim_id"], dispositions, alarms)
            if status not in wanted:
                if status in hidden:
                    hidden[status] += 1
                continue
            obj = claim.get("object") if isinstance(claim.get("object"),
                                                   dict) else {}
            product_rows.append({
                "score": score,
                "status": status,
                "product": f"{product.get('brand', '')} "
                           f"{product.get('model', '')}".strip(),
                "product_dir": product["dir"],
                "claim_id": claim["claim_id"],
                "tier": claim.get("consequence_ceiling"),
                "type": claim.get("type"),
                "procedure": (obj.get("procedure")
                              if claim.get("type") == "STEP" else None),
                "predicate": claim.get("predicate"),
                "answer": display_text(claim),
                "display_text": display_text(claim),
                "raw_answer": render_object(claim),
                "step_number": (obj.get("step_number")
                                if claim.get("type") == "STEP" else None),
                "citations": [{
                    "source_id": binding.get("source_id"),
                    "quote": binding.get("quote", ""),
                    **sources.get(binding.get("source_id"), {}),
                } for binding in claim.get("source_bindings", [])],
            })
        results.extend(compose_procedures(
            product_rows, product, claims, dispositions, alarms, wanted,
            sources))
    results.sort(key=lambda row: (-row["score"], row["claim_id"]))
    return results[:top], hidden


def compose_procedures(rows, product, claims, dispositions, alarms, wanted,
                       sources):
    """Fold multiple matched STEP rows into one ordered procedure answer.

    A question that matches two or more steps of the same procedure is a
    procedure question; answering with scattered per-step cards presents the
    steps out of order and without their siblings. The composed row carries
    the complete ordered step list (every step of that procedure whose
    serving status is allowed), each step keeping its own status, tier, and
    citations.
    """
    by_procedure = {}
    for row in rows:
        if row["procedure"]:
            by_procedure.setdefault(row["procedure"], []).append(row)

    composed, absorbed = [], set()
    for procedure, members in by_procedure.items():
        if len(members) < 2:
            continue
        steps = []
        for claim in claims:
            obj = claim.get("object") if isinstance(claim.get("object"),
                                                    dict) else {}
            if claim.get("type") != "STEP" or obj.get("procedure") != procedure:
                continue
            status = claim_status(claim["claim_id"], dispositions, alarms)
            if status not in wanted:
                continue
            steps.append({
                "step_number": obj.get("step_number"),
                "action": obj.get("action"),
                "claim_id": claim["claim_id"],
                "status": status,
                "tier": claim.get("consequence_ceiling"),
                "citations": [{
                    "source_id": binding.get("source_id"),
                    "quote": binding.get("quote", ""),
                    **sources.get(binding.get("source_id"), {}),
                } for binding in claim.get("source_bindings", [])],
            })
        steps.sort(key=lambda step: (step["step_number"] is None,
                                     step["step_number"]))
        tiers = [step["tier"] for step in steps if step["tier"]]
        statuses = {step["status"] for step in steps}
        absorbed.update(member["claim_id"] for member in members)
        composed.append({
            # Rank the assembled procedure above its own fragments.
            "score": max(member["score"] for member in members) + 1.0,
            "status": ("PUBLISHED" if statuses == {"PUBLISHED"}
                       else "CANDIDATE"),
            "product": members[0]["product"],
            "product_dir": product["dir"],
            "claim_id": f"procedure:{procedure}",
            "tier": max(tiers) if tiers else None,
            "type": "PROCEDURE",
            "procedure": procedure,
            "predicate": procedure,
            "answer": f"{readable_label(procedure)} has {len(steps)} documented steps.",
            "display_text": f"{readable_label(procedure)} has {len(steps)} documented steps.",
            "raw_answer": f"{len(steps)} documented steps",
            "steps": steps,
            "citations": [],
        })
    kept = [row for row in rows if row["claim_id"] not in absorbed]
    return kept + composed


STATUS_LABELS = {
    "PUBLISHED": "PUBLISHED",
    "SUSPENDED": "SUSPENDED — approved, verifier alarm outstanding",
    "CANDIDATE": "CANDIDATE — not human-reviewed; not a published fact",
}


def format_results(question, results, hidden, preview):
    lines = [f"Q: {question}", ""]
    if not results:
        lines.append("No published answer found.")
    for rank, row in enumerate(results, 1):
        lines.append(f"{rank}. [{STATUS_LABELS[row['status']]}] "
                     f"{row['product']} — {row['predicate']} "
                     f"(tier {row['tier']}, {row['claim_id']})")
        lines.append(f"   {row['answer']}")
        for step in row.get("steps", []):
            marker = ("" if step["status"] == "PUBLISHED"
                      else f" [{step['status']}]")
            lines.append(f"   {step['step_number']}. {step['action']}{marker}")
        for citation in row["citations"]:
            quote = " ".join(str(citation["quote"]).split())
            if len(quote) > 160:
                quote = quote[:157] + "..."
            suffix = (f" <{citation['origin_url']}>"
                      if citation.get("origin_url") else "")
            lines.append(f"   “{quote}” — "
                         f"{citation['source_id']}{suffix}")
        lines.append("")
    hidden_total = sum(hidden.values())
    if not preview and hidden_total:
        detail = ", ".join(f"{count} {status.lower()}"
                           for status, count in hidden.items() if count)
        lines.append(f"Not served: {detail} match(es). "
                     "CANDIDATE/SUSPENDED require the owner review pass; "
                     "use --preview to inspect them (clearly labeled).")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Answer a product question from reviewed evidence-pack "
                    "claims, with citations.")
    parser.add_argument("question", help="the question to answer")
    parser.add_argument("--product", help="restrict to one pack directory")
    parser.add_argument("--preview", action="store_true",
                        help="also show labeled CANDIDATE/SUSPENDED matches")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    results, hidden = search(args.question, product_dir=args.product,
                             preview=args.preview, top=args.top)
    if args.as_json:
        print(json.dumps({"question": args.question, "results": results,
                          "not_served": hidden}, ensure_ascii=False, indent=2))
    else:
        print(format_results(args.question, results, hidden, args.preview),
              end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
