#!/usr/bin/env python3
"""Blind Qwen verification for evidence-pack claim translations.

The verifier sees only a binding's quote, the claim translation, and the
consequence tier.  It never receives extractor notes, neighboring claims, or
prior verdicts.  Provider calls are isolated behind ``call_provider`` so the
offline suite can exercise the complete pipeline with a deterministic mock.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"
VAULT_ROOT = REPO_ROOT / "source-vault"
CACHE_PATH = REPO_ROOT / "system" / "cache" / "verifier-cache.json"

# Policy constants: substitutions, if ever required, must remain exact qwen/* IDs.
MODEL_ID = "qwen/qwen3-vl-235b-a22b-instruct"
ENDPOINT = "openrouter/router/vision"
PROMPT_VERSION = "v1"
VERDICTS = {"ENTAILED", "MEANING_CHANGED", "CANNOT_JUDGE"}
TRIAGE_RESULTS = {"GENUINE_CONFLICT", "DIFFERENT_SCOPE_OR_EVENT", "CANNOT_JUDGE"}
VISUAL_SOURCE_TYPES = {"IMAGE", "VIDEO", "VIDEO_URL"}

EXIT_OK = 0
EXIT_ALARM = 10
EXIT_PARTIAL = 20
EXIT_PROVIDER = 30
EXIT_MALFORMED = 40

# OpenRouter's published list prices as of 2026-08-24. fal may bill differently,
# so this is explicitly an estimate rather than claimed provider spend.
INPUT_USD_PER_MILLION_TOKENS = 0.20
OUTPUT_USD_PER_MILLION_TOKENS = 0.88
ESTIMATED_OUTPUT_TOKENS = 60

PROMPT_FRAME = """\
You are a strict verifier auditing a fact extracted from a product manual.
Below are the EXACT QUOTE from the source and the TRANSLATION a different
system produced. Assume the translation changed the meaning and try to prove
it. Small changes matter: a different number, unit, direction, actor,
condition, or an added/dropped qualifier is a meaning change. If the
translation adds information the quote does not state, that is a meaning
change. The CONSEQUENCE TIER is context for how strict to be, not evidence.

EXACT QUOTE:
{quote_json}

TRANSLATION (type, predicate, and object only):
{translation_json}

CONSEQUENCE TIER:
{tier_json}

Answer in JSON only:
{{"verdict":"ENTAILED|MEANING_CHANGED|CANNOT_JUDGE",\
"note":"one sentence: the discrepancy, or why it is faithful"}}
"""

CONFLICT_PROMPT = """\
You are a strict independent verifier reviewing two extracted claims that were
flagged as a possible conflict. Decide only from the two exact quote sets and
their surrounding source-page context. Do not choose which source wins and do
not issue a publication decision. Determine whether the quotes genuinely
contradict each other or describe different scopes, events, or revisions.

CLAIM A QUOTES:
{quotes_a}

CLAIM A SURROUNDING CONTEXT:
{context_a}

CLAIM B QUOTES:
{quotes_b}

CLAIM B SURROUNDING CONTEXT:
{context_b}

Answer in JSON only:
{{"result":"GENUINE_CONFLICT|DIFFERENT_SCOPE_OR_EVENT|CANNOT_JUDGE",\
"note":"one sentence explaining the comparison"}}
"""


class ProviderFailure(Exception):
    """A provider operation failed; its original message is never persisted."""


class MalformedResponse(Exception):
    """The provider returned a response outside the required JSON schema."""


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_cache(path):
    data = load_json(path, {})
    if not isinstance(data, dict):
        return {}
    return data


def cache_key(claim, binding_index, model_id=MODEL_ID):
    binding = claim["source_bindings"][binding_index]
    translation = {
        "type": claim.get("type"),
        "predicate": claim.get("predicate"),
        "object": claim.get("object"),
    }
    components = [
        claim.get("claim_id"),
        binding_index,
        sha256_text(binding.get("quote", "")),
        sha256_text(canonical_json(translation)),
        claim.get("consequence_ceiling"),
        model_id,
        PROMPT_VERSION,
    ]
    return sha256_text(canonical_json(components))


def build_prompt(claim, binding_index):
    binding = claim["source_bindings"][binding_index]
    translation = {
        "type": claim.get("type"),
        "predicate": claim.get("predicate"),
        "object": claim.get("object"),
    }
    return PROMPT_FRAME.format(
        quote_json=json.dumps(binding.get("quote", ""), ensure_ascii=False),
        translation_json=canonical_json(translation),
        tier_json=json.dumps(claim.get("consequence_ceiling")),
    )


def provider_arguments(prompt, model_id=MODEL_ID):
    return {
        "model": model_id,
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 250,
    }


def call_provider(arguments):
    """The sole fal.ai call site. Tests inject a callable with this signature."""
    try:
        import fal_client
        handle = fal_client.submit(ENDPOINT, arguments=arguments)
        return handle.get()
    except Exception as exc:  # noqa: BLE001
        # Never include the provider's message: it may echo credentials or input.
        raise ProviderFailure(f"provider request failed ({type(exc).__name__})") from None


def _response_output(response):
    if isinstance(response, str):
        return response
    if isinstance(response, dict) and isinstance(response.get("output"), str):
        return response["output"]
    raise MalformedResponse("provider response has no string output")


def parse_verdict_response(response):
    try:
        parsed = json.loads(_response_output(response))
    except (json.JSONDecodeError, MalformedResponse):
        raise MalformedResponse("provider output is not JSON") from None
    if not isinstance(parsed, dict) or set(parsed) != {"verdict", "note"}:
        raise MalformedResponse("provider output has the wrong verdict fields")
    if parsed.get("verdict") not in VERDICTS:
        raise MalformedResponse("provider output has an invalid verdict")
    if not isinstance(parsed.get("note"), str) or not parsed["note"].strip():
        raise MalformedResponse("provider output has an empty note")
    return {"verdict": parsed["verdict"], "note": parsed["note"].strip()}


def parse_triage_response(response):
    try:
        parsed = json.loads(_response_output(response))
    except (json.JSONDecodeError, MalformedResponse):
        raise MalformedResponse("provider output is not JSON") from None
    if not isinstance(parsed, dict) or set(parsed) != {"result", "note"}:
        raise MalformedResponse("provider output has the wrong triage fields")
    if parsed.get("result") not in TRIAGE_RESULTS:
        raise MalformedResponse("provider output has an invalid triage result")
    if not isinstance(parsed.get("note"), str) or not parsed["note"].strip():
        raise MalformedResponse("provider output has an empty note")
    return {"result": parsed["result"], "note": parsed["note"].strip()}


def source_types(vault_root, product):
    manifest = load_json(Path(vault_root) / product / "manifest.json", {})
    return {source.get("source_id"): source.get("type")
            for source in manifest.get("sources", [])}


def estimated_cost(prompt):
    input_tokens = max(1, len(prompt) // 4)
    return (input_tokens * INPUT_USD_PER_MILLION_TOKENS
            + ESTIMATED_OUTPUT_TOKENS * OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000


def _valid_cached_verdict(value):
    return (isinstance(value, dict)
            and value.get("verdict") in VERDICTS
            and isinstance(value.get("note"), str)
            and bool(value["note"].strip()))


def _invoke_for_verdict(prompt, provider):
    for attempt in range(2):
        response = provider(provider_arguments(prompt))
        try:
            return parse_verdict_response(response), False, attempt + 1
        except MalformedResponse:
            pass
    return {
        "verdict": "CANNOT_JUDGE",
        "note": "Malformed provider output after one retry.",
    }, True, 2


def _invoke_for_triage(prompt, provider):
    for attempt in range(2):
        response = provider(provider_arguments(prompt))
        try:
            return parse_triage_response(response), False, attempt + 1
        except MalformedResponse:
            pass
    return {
        "result": "CANNOT_JUDGE",
        "note": "Malformed provider output after one retry.",
    }, True, 2


def verify_pack(pack_dir, vault_root=VAULT_ROOT, cache_path=CACHE_PATH,
                provider=call_provider, model_id=MODEL_ID, date=None):
    pack_dir = Path(pack_dir)
    product = pack_dir.name
    date = date or dt.date.today().isoformat()
    claims = load_json(pack_dir / "claims.json")
    if not isinstance(claims, list):
        raise ValueError(f"{pack_dir / 'claims.json'} root must be a list")

    types = source_types(vault_root, product)
    cache = load_cache(cache_path)
    original_conflicts = load_json(pack_dir / "verdicts.json", {}) or {}
    conflict_triage = original_conflicts.get("conflict_triage", [])
    if not isinstance(conflict_triage, list):
        conflict_triage = []

    total = sum(len(claim.get("source_bindings", [])) for claim in claims)
    records = []
    provider_failed = malformed_seen = False
    provider_available = True
    cache_changed = False
    estimate = 0.0
    processed = 0

    for claim in claims:
        for binding_index, binding in enumerate(claim.get("source_bindings", [])):
            processed += 1
            source_type = types.get(binding.get("source_id"))
            if source_type in VISUAL_SOURCE_TYPES:
                records.append({
                    "claim_id": claim["claim_id"],
                    "binding_index": binding_index,
                    "verdict": "CANNOT_JUDGE",
                    "note": "Visual binding; text-only verification is unavailable.",
                })
                print(f"[{product}] {processed}/{total} visual -> CANNOT_JUDGE")
                continue

            key = cache_key(claim, binding_index, model_id)
            cached = cache.get(key)
            if _valid_cached_verdict(cached):
                result = {"verdict": cached["verdict"], "note": cached["note"]}
                source = "cache"
            else:
                if not provider_available:
                    continue
                prompt = build_prompt(claim, binding_index)
                try:
                    result, malformed, provider_calls = _invoke_for_verdict(
                        prompt, provider)
                except ProviderFailure:
                    provider_failed = True
                    provider_available = False
                    print(f"[{product}] {processed}/{total} provider failure (sanitized)")
                    continue
                estimate += estimated_cost(prompt) * provider_calls
                malformed_seen = malformed_seen or malformed
                if not malformed:
                    cache[key] = result
                    cache_changed = True
                source = "provider"

            records.append({
                "claim_id": claim["claim_id"],
                "binding_index": binding_index,
                "verdict": result["verdict"],
                "note": result["note"],
            })
            print(f"[{product}] {processed}/{total} {source} -> {result['verdict']} "
                  f"(estimated spend ${estimate:.4f})")

    if cache_changed:
        atomic_write_json(cache_path, cache)

    if len(records) == total:
        status = "COMPLETE"
        reason = None
    elif records:
        status = "PARTIAL"
        reason = "One or more provider requests failed; some bindings have no verdict."
    else:
        status = "FAILED"
        reason = "Provider verification was unavailable; no bindings were verified."

    document = {
        "model": model_id,
        "prompt_version": PROMPT_VERSION,
        "date": date,
        "status": status,
    }
    if reason:
        document["reason"] = reason
    document["verdicts"] = records
    document["conflict_triage"] = conflict_triage
    atomic_write_json(pack_dir / "verdicts.json", document)

    alarms = sum(v["verdict"] == "MEANING_CHANGED" for v in records)
    cannot_judge = sum(v["verdict"] == "CANNOT_JUDGE" for v in records)

    if provider_failed:
        exit_code = EXIT_PROVIDER
    elif malformed_seen:
        exit_code = EXIT_MALFORMED
    elif status != "COMPLETE":
        exit_code = EXIT_PARTIAL
    elif alarms:
        exit_code = EXIT_ALARM
    else:
        exit_code = EXIT_OK

    if alarms:
        print(f"ALARM [{product}]: {alarms} MEANING_CHANGED binding(s)", file=sys.stderr)
    print(f"[{product}] status={status} verdicts={len(records)}/{total} "
          f"alarms={alarms} cannot_judge={cannot_judge} "
          f"estimated_spend=${estimate:.4f}")
    return {
        "product": product,
        "status": status,
        "exit_code": exit_code,
        "verdicts": records,
        "alarms": alarms,
        "cannot_judge": cannot_judge,
        "estimated_spend_usd": estimate,
    }


def conflict_pairs(claims):
    claim_ids = {claim.get("claim_id") for claim in claims}
    pairs = set()
    pattern = re.compile(r"CONFLICT:\s*contradicts\s+([A-Za-z0-9_-]+)")
    for claim in claims:
        match = pattern.search(claim.get("extraction_notes") or "")
        if match and match.group(1) in claim_ids:
            pairs.add(tuple(sorted((claim["claim_id"], match.group(1)))))
    return sorted(pairs)


def _context_window(text, quote, radius=500):
    words = re.findall(r"\S+", text)
    if not words:
        return ""
    quote_words = re.findall(r"\S+", quote)
    normalized = [re.sub(r"\W+", "", word).lower() for word in words]
    needle = [re.sub(r"\W+", "", word).lower() for word in quote_words[:6]]
    start = 0
    if needle:
        for index in range(max(1, len(normalized) - len(needle) + 1)):
            if normalized[index:index + len(needle)] == needle:
                start = index
                break
    left = max(0, start - radius)
    right = min(len(words), start + max(1, len(quote_words)) + radius)
    return " ".join(words[left:right])


def _binding_context(vault_root, product, binding):
    manifest = load_json(Path(vault_root) / product / "manifest.json", {})
    source = next((item for item in manifest.get("sources", [])
                   if item.get("source_id") == binding.get("source_id")), None)
    if not source or source.get("type") in VISUAL_SOURCE_TYPES:
        return ""
    local_path = source.get("local_path")
    if not local_path:
        return ""
    path = Path(vault_root) / product / local_path
    if not path.exists():
        return ""
    if path.suffix.lower() == ".pdf":
        if PdfReader is None:
            return ""
        reader = PdfReader(path)
        page = binding.get("page")
        if isinstance(page, int) and 0 < page <= len(reader.pages):
            text = reader.pages[page - 1].extract_text() or ""
        else:
            text = " ".join((item.extract_text() or "") for item in reader.pages)
    elif path.suffix.lower() in {".md", ".txt", ".html", ".htm"}:
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        return ""
    return _context_window(text, binding.get("quote", ""))


def _claim_context(vault_root, product, claim):
    windows = [_binding_context(vault_root, product, binding)
               for binding in claim.get("source_bindings", [])]
    return "\n\n".join(window for window in windows if window)


def triage_conflicts(pack_dir, vault_root=VAULT_ROOT, cache_path=CACHE_PATH,
                     provider=call_provider, model_id=MODEL_ID):
    pack_dir = Path(pack_dir)
    product = pack_dir.name
    claims = load_json(pack_dir / "claims.json")
    by_id = {claim["claim_id"]: claim for claim in claims}
    document = load_json(pack_dir / "verdicts.json")
    if not isinstance(document, dict):
        raise ValueError("run claim verification before conflict triage")

    cache = load_cache(cache_path)
    cache_changed = malformed_seen = provider_failed = False
    results = []
    estimate = 0.0
    pairs = conflict_pairs(claims)
    for index, pair in enumerate(pairs, 1):
        claim_a, claim_b = by_id[pair[0]], by_id[pair[1]]
        payload = {
            "quotes_a": [b.get("quote", "") for b in claim_a.get("source_bindings", [])],
            "context_a": _claim_context(vault_root, product, claim_a),
            "quotes_b": [b.get("quote", "") for b in claim_b.get("source_bindings", [])],
            "context_b": _claim_context(vault_root, product, claim_b),
        }
        context_hash = sha256_text(canonical_json([
            payload["context_a"], payload["context_b"],
        ]))
        payload_hash = sha256_text(canonical_json(payload))
        key = sha256_text(canonical_json([
            "conflict", list(pair), payload_hash, model_id, PROMPT_VERSION,
        ]))
        cached = cache.get(key)
        if (isinstance(cached, dict) and cached.get("result") in TRIAGE_RESULTS
                and isinstance(cached.get("note"), str) and cached["note"].strip()):
            result = {"result": cached["result"], "note": cached["note"]}
            source = "cache"
        else:
            prompt = CONFLICT_PROMPT.format(
                quotes_a=json.dumps(payload["quotes_a"], ensure_ascii=False),
                context_a=payload["context_a"],
                quotes_b=json.dumps(payload["quotes_b"], ensure_ascii=False),
                context_b=payload["context_b"],
            )
            try:
                result, malformed, provider_calls = _invoke_for_triage(
                    prompt, provider)
            except ProviderFailure:
                provider_failed = True
                print(f"[{product}] conflict {index}/{len(pairs)} provider failure "
                      "(sanitized)")
                continue
            estimate += estimated_cost(prompt) * provider_calls
            malformed_seen = malformed_seen or malformed
            if not malformed:
                cache[key] = result
                cache_changed = True
            source = "provider"
        results.append({
            "pair": list(pair),
            "result": result["result"],
            "note": result["note"],
            "context_sha256": context_hash,
        })
        print(f"[{product}] conflict {index}/{len(pairs)} {source} -> "
              f"{result['result']} (estimated spend ${estimate:.4f})")

    document["conflict_triage"] = results
    atomic_write_json(pack_dir / "verdicts.json", document)
    if cache_changed:
        atomic_write_json(cache_path, cache)

    if provider_failed:
        exit_code = EXIT_PROVIDER
    elif malformed_seen:
        exit_code = EXIT_MALFORMED
    elif len(results) != len(pairs):
        exit_code = EXIT_PARTIAL
    else:
        exit_code = EXIT_OK
    return {"exit_code": exit_code, "results": results,
            "estimated_spend_usd": estimate}


def combine_exit_codes(codes):
    for code in (EXIT_MALFORMED, EXIT_PROVIDER, EXIT_PARTIAL, EXIT_ALARM):
        if code in codes:
            return code
    return EXIT_OK


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", help="verify one evidence-pack product")
    parser.add_argument("--conflicts", action="store_true",
                        help="also run advisory conflict triage")
    parser.add_argument("--cache", type=Path, default=CACHE_PATH,
                        help="verdict cache path (defaults under system/cache)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if not MODEL_ID.startswith("qwen/"):
        print("ERROR: verifier model policy requires an exact qwen/* model", file=sys.stderr)
        return EXIT_PROVIDER

    if args.product:
        pack_dirs = [PACKS_ROOT / args.product]
    else:
        pack_dirs = sorted(path.parent for path in PACKS_ROOT.glob("*/claims.json"))
    missing = [path for path in pack_dirs if not (path / "claims.json").exists()]
    if missing:
        print(f"ERROR: no claims.json for {missing[0].name}", file=sys.stderr)
        return 2

    if not os.environ.get("FAL_KEY"):
        def unavailable_provider(_arguments):
            raise ProviderFailure("FAL_KEY is not configured")
        provider = unavailable_provider
        print("FAL_KEY is not configured; writing truthful FAILED/PARTIAL artifacts "
              "without sending provider requests.", file=sys.stderr)
    else:
        provider = call_provider

    codes = []
    total_estimate = 0.0
    for pack_dir in pack_dirs:
        run = verify_pack(pack_dir, cache_path=args.cache, provider=provider)
        codes.append(run["exit_code"])
        total_estimate += run["estimated_spend_usd"]
        if args.conflicts and run["status"] != "FAILED":
            triage = triage_conflicts(pack_dir, cache_path=args.cache,
                                       provider=provider)
            codes.append(triage["exit_code"])
            total_estimate += triage["estimated_spend_usd"]
    print(f"Verifier total estimated spend: ${total_estimate:.4f}")
    return combine_exit_codes(codes)


if __name__ == "__main__":
    sys.exit(main())
