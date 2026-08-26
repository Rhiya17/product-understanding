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


def source_urls(vault_root, product_dir):
    manifest = load_json(vault_root / product_dir / "manifest.json", {})
    return {source.get("source_id"): source.get("origin_url")
            for source in manifest.get("sources", [])}


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
        urls = source_urls(vault_root, product["dir"])
        for claim in claims:
            score = score_claim(question_tokens, claim)
            if score <= 0:
                continue
            status = claim_status(claim["claim_id"], dispositions, alarms)
            if status not in wanted:
                if status in hidden:
                    hidden[status] += 1
                continue
            results.append({
                "score": score,
                "status": status,
                "product": f"{product.get('brand', '')} "
                           f"{product.get('model', '')}".strip(),
                "claim_id": claim["claim_id"],
                "tier": claim.get("consequence_ceiling"),
                "predicate": claim.get("predicate"),
                "answer": render_object(claim),
                "citations": [{
                    "source_id": binding.get("source_id"),
                    "quote": binding.get("quote", ""),
                    "origin_url": urls.get(binding.get("source_id")),
                } for binding in claim.get("source_bindings", [])],
            })
    results.sort(key=lambda row: (-row["score"], row["claim_id"]))
    return results[:top], hidden


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
