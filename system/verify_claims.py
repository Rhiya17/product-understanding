#!/usr/bin/env python3
"""Blind Qwen verification for evidence-pack claim translations.

The verifier sees the union of a claim's exact quotes, a semantic-only
projection of its object, and the consequence tier. It never receives claim
IDs, extractor notes, neighboring claims, or prior verdicts. Provider calls
are isolated behind ``call_provider`` so the offline suite can exercise the
complete pipeline with a deterministic mock.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import ssl
import sys
import tempfile
import urllib.request
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
ENDPOINT = "openrouter/router/openai/v1/chat/completions"
ENDPOINT_URL = f"https://fal.run/{ENDPOINT}"
PROMPT_VERSION = "v2"
VERIFICATION_SCOPE = "CLAIM_QUOTE_UNION"
VERDICTS = {"ENTAILED", "MEANING_CHANGED", "CANNOT_JUDGE"}
TRIAGE_RESULTS = {"GENUINE_CONFLICT", "DIFFERENT_SCOPE_OR_EVENT", "CANNOT_JUDGE"}
VISUAL_SOURCE_TYPES = {"IMAGE", "VIDEO", "VIDEO_URL"}

EXIT_OK = 0
EXIT_ALARM = 10
EXIT_PARTIAL = 20
EXIT_PROVIDER = 30
EXIT_MALFORMED = 40
EXIT_MODEL_ATTESTATION = 50

# OpenRouter's published list prices as of 2026-08-24. fal may bill differently,
# so this is explicitly an estimate rather than claimed provider spend.
INPUT_USD_PER_MILLION_TOKENS = 0.20
OUTPUT_USD_PER_MILLION_TOKENS = 0.88
ESTIMATED_OUTPUT_TOKENS = 60

PROMPT_FRAME = """\
You are a strict verifier auditing one structured product claim. Try to find a
real contradiction, scope broadening, wrong number/unit/direction/actor, lost
governing condition, or other unsupported semantic addition.

Judge the EXACT QUOTES AS A UNION: every semantic assertion may be supported by
any quote in the set. Do not require every individual quote to entail the full
claim.

The SEMANTIC PROJECTION intentionally omits schema scaffolding. JSON field
names and structure are labels, not extra factual assertions. Do not penalize
procedure names, step numbers, target-part IDs, state IDs, diagram metadata,
or a value and unit being stored in separate fields; those are not being
asserted here. The projection itself is the complete text/value content to
audit.

Omission alone is not a meaning change: a claim may state a faithful subset of
the source. But if dropping a condition or direction makes the projection
assert something more broadly than the quotes support, that is an unsupported
addition and is MEANING_CHANGED. In particular, a bare range or limit is read
as unconditional: if a quote requires that range or limit together with an
operating condition (for example, devices must be within range and powered
on), omitting the condition wrongly implies the range alone is sufficient.
Exact qualifiers, limits, conditions, and directions still matter. Keep an
adversarial stance after applying these rules.

EXACT QUOTES (union):
{quotes_json}

SEMANTIC PROJECTION:
{translation_json}

CONSEQUENCE TIER:
{tier_json}

Answer in JSON only:
{{"verdict":"ENTAILED|MEANING_CHANGED|CANNOT_JUDGE",\
"note":"one sentence: the semantic discrepancy, or why the quote union supports every assertion"}}
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


class ModelAttestationFailure(Exception):
    """The provider did not attest to the exact requested serving model."""

    def __init__(self, serving_model):
        super().__init__("provider serving-model attestation missing or mismatched")
        self.serving_model = serving_model


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


def semantic_projection(claim):
    """Remove non-semantic claim-schema scaffolding before model review."""
    obj = claim.get("object")
    if not isinstance(obj, dict):
        return obj
    if claim.get("type") == "STEP" and isinstance(obj.get("action"), str):
        return {"action": obj["action"]}
    if (claim.get("type") == "PART_LOCATION"
            and isinstance(obj.get("location_description"), str)):
        return {"location_description": obj["location_description"]}
    if claim.get("type") == "WARNING" and isinstance(obj.get("description"), str):
        return {"warning": obj["description"]}
    if claim.get("type") == "STATE" and isinstance(obj.get("description"), str):
        return {"description": obj["description"]}
    scaffolding = {
        "procedure", "step_number", "target_parts", "initial_state",
        "resulting_state", "diagram_binding", "part", "hazard_type",
    }
    return {key: value for key, value in obj.items() if key not in scaffolding}


def quote_union(claim):
    return [
        {"binding_index": index, "quote": binding.get("quote", "")}
        for index, binding in enumerate(claim.get("source_bindings", []))
    ]


def cache_key(claim, model_id=MODEL_ID):
    translation = semantic_projection(claim)
    components = [
        claim.get("claim_id"),
        [sha256_text(item["quote"]) for item in quote_union(claim)],
        sha256_text(canonical_json(translation)),
        claim.get("consequence_ceiling"),
        model_id,
        ENDPOINT,
        PROMPT_VERSION,
        VERIFICATION_SCOPE,
    ]
    return sha256_text(canonical_json(components))


def build_prompt(claim):
    return PROMPT_FRAME.format(
        quotes_json=json.dumps(quote_union(claim), ensure_ascii=False),
        translation_json=canonical_json(semantic_projection(claim)),
        tier_json=json.dumps(claim.get("consequence_ceiling")),
    )


def provider_arguments(prompt, model_id=MODEL_ID):
    return {
        "model": model_id,
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 250,
    }


def _tls_context():
    """python.org builds ship without system CA certificates; use certifi's."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def call_provider(arguments):
    """The sole fal.ai call site. Tests inject a callable with this signature.

    The OpenAI-compatible route is deliberate: unlike fal's compact queued
    vision response, the chat-completion envelope reports the serving model.
    """
    try:
        request_body = {
            "model": arguments["model"],
            "messages": [{"role": "user", "content": arguments["prompt"]}],
            "temperature": arguments["temperature"],
            "max_tokens": arguments["max_tokens"],
        }
        request = urllib.request.Request(
            ENDPOINT_URL,
            data=json.dumps(request_body).encode("utf-8"),
            headers={
                "Authorization": f"Key {os.environ['FAL_KEY']}",
                "Content-Type": "application/json",
                "X-OpenRouter-Metadata": "enabled",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=180,  # noqa: S310
                                    context=_tls_context()) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        # Never include the provider's message: it may echo credentials or input.
        raise ProviderFailure(f"provider request failed ({type(exc).__name__})") from None


def _response_output(response):
    if isinstance(response, str):
        return response
    if isinstance(response, dict) and isinstance(response.get("output"), str):
        return response["output"]
    if isinstance(response, dict):
        choices = response.get("choices")
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            message = choices[0].get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
    raise MalformedResponse("provider response has no string output")


def response_serving_model(response):
    """Read the serving-model attestation from known router response shapes."""
    if not isinstance(response, dict):
        return None
    candidates = [
        response.get("model"),
        response.get("serving_model"),
    ]
    for container_name in ("usage", "metadata", "data"):
        container = response.get(container_name)
        if isinstance(container, dict):
            candidates.extend((container.get("model"), container.get("serving_model")))
    return next((value for value in candidates
                 if isinstance(value, str) and value.strip()), None)


def response_usage_cost(response):
    if not isinstance(response, dict) or not isinstance(response.get("usage"), dict):
        return 0.0
    value = response["usage"].get("cost")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return 0.0


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


def _valid_cached_verdict(value, model_id=MODEL_ID):
    return (isinstance(value, dict)
            and value.get("verdict") in VERDICTS
            and isinstance(value.get("note"), str)
            and bool(value["note"].strip())
            and value.get("serving_model") == model_id)


def _attest_response(response, model_id):
    serving_model = response_serving_model(response)
    if serving_model != model_id:
        raise ModelAttestationFailure(serving_model)
    return serving_model, response_usage_cost(response)


def _invoke_for_verdict(prompt, provider, model_id=MODEL_ID):
    total_usage_cost = 0.0
    for attempt in range(2):
        response = provider(provider_arguments(prompt, model_id))
        serving_model, usage_cost = _attest_response(response, model_id)
        total_usage_cost += usage_cost
        try:
            return (parse_verdict_response(response), serving_model, total_usage_cost,
                    False, attempt + 1)
        except MalformedResponse:
            pass
    return ({
        "verdict": "CANNOT_JUDGE",
        "note": "Malformed provider output after one retry.",
    }, serving_model, total_usage_cost, True, 2)


def _invoke_for_triage(prompt, provider, model_id=MODEL_ID):
    total_usage_cost = 0.0
    for attempt in range(2):
        response = provider(provider_arguments(prompt, model_id))
        serving_model, usage_cost = _attest_response(response, model_id)
        total_usage_cost += usage_cost
        try:
            return (parse_triage_response(response), serving_model, total_usage_cost,
                    False, attempt + 1)
        except MalformedResponse:
            pass
    return ({
        "result": "CANNOT_JUDGE",
        "note": "Malformed provider output after one retry.",
    }, serving_model, total_usage_cost, True, 2)


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
    conflict_triage = (original_conflicts.get("conflict_triage", [])
                       if original_conflicts.get("prompt_version") == PROMPT_VERSION
                       else [])
    if not isinstance(conflict_triage, list):
        conflict_triage = []

    total = sum(len(claim.get("source_bindings", [])) for claim in claims)
    records = []
    claim_results = {}
    provider_failed = malformed_seen = attestation_failed = False
    provider_available = True
    cache_changed = False
    estimate = 0.0
    actual_cost = 0.0
    serving_models = set()

    for processed, claim in enumerate(claims, 1):
        bindings = claim.get("source_bindings", [])
        text_indexes = [
            index for index, binding in enumerate(bindings)
            if types.get(binding.get("source_id")) not in VISUAL_SOURCE_TYPES
        ]
        visual_indexes = set(range(len(bindings))) - set(text_indexes)
        if not text_indexes:
            result = {
                "verdict": "CANNOT_JUDGE",
                "note": "Claim has only visual bindings; text-only verification is unavailable.",
            }
            claim_results[claim["claim_id"]] = result
            for binding_index in visual_indexes:
                records.append({
                    "claim_id": claim["claim_id"],
                    "binding_index": binding_index,
                    "verdict": "CANNOT_JUDGE",
                    "note": result["note"],
                    "basis": VERIFICATION_SCOPE,
                })
            print(f"[{product}] claim {processed}/{len(claims)} visual-only "
                  "-> CANNOT_JUDGE")
            continue

        key = cache_key(claim, model_id)
        cached = cache.get(key)
        if _valid_cached_verdict(cached, model_id):
            result = {"verdict": cached["verdict"], "note": cached["note"]}
            serving_model = cached["serving_model"]
            serving_models.add(serving_model)
            source = "cache"
        else:
            if not provider_available:
                continue
            prompt = build_prompt(claim)
            try:
                (result, serving_model, usage_cost, malformed,
                 provider_calls) = _invoke_for_verdict(
                    prompt, provider, model_id=model_id)
            except ModelAttestationFailure as exc:
                attestation_failed = True
                provider_available = False
                if exc.serving_model:
                    serving_models.add(exc.serving_model)
                print(f"[{product}] claim {processed}/{len(claims)} "
                      "serving-model attestation failure")
                continue
            except ProviderFailure:
                provider_failed = True
                provider_available = False
                print(f"[{product}] claim {processed}/{len(claims)} "
                      "provider failure (sanitized)")
                continue
            estimate += estimated_cost(prompt) * provider_calls
            actual_cost += usage_cost
            serving_models.add(serving_model)
            malformed_seen = malformed_seen or malformed
            if not malformed:
                cache[key] = {
                    **result,
                    "serving_model": serving_model,
                }
                cache_changed = True
            source = "provider"

        claim_results[claim["claim_id"]] = result
        for binding_index in range(len(bindings)):
            if binding_index in visual_indexes:
                verdict = "CANNOT_JUDGE"
                note = ("Visual binding is not authenticated by text-only verification; "
                        f"the claim quote union result was {result['verdict']}.")
            else:
                verdict = result["verdict"]
                note = result["note"]
            records.append({
                "claim_id": claim["claim_id"],
                "binding_index": binding_index,
                "verdict": verdict,
                "note": note,
                "basis": VERIFICATION_SCOPE,
            })
        print(f"[{product}] claim {processed}/{len(claims)} {source} "
              f"-> {result['verdict']} (estimated spend ${estimate:.4f})")

    if cache_changed:
        atomic_write_json(cache_path, cache)

    # Every fresh verdict is also appended to the durable receipt ledger, so
    # alarm history survives later rewrites of verdicts.json.
    from system import evidence_status
    for claim in claims:
        result = claim_results.get(claim["claim_id"])
        if result is not None:
            evidence_status.append_receipt(pack_dir, {
                "kind": "semantic_check", "claim_id": claim["claim_id"],
                "claim_digest": evidence_status.claim_digest(claim),
                "result": result["verdict"], "note": result["note"],
                "model": model_id, "prompt_version": PROMPT_VERSION,
                "run": f"verify_pack:{date}",
                "receipt_id": f"rcpt_{sha256_text(claim['claim_id'] + date + result['verdict'])[:16]}"})

    # A failed or partial run never erases earlier verdicts (and so never
    # clears an alarm): claims without a fresh verdict keep their prior ones.
    fresh_count = len(records)
    carried = [entry for entry in original_conflicts.get("verdicts", [])
               if entry.get("claim_id") not in claim_results
               and entry.get("claim_id") in {c["claim_id"] for c in claims}]
    records.extend(carried)

    if fresh_count == total:
        status = "COMPLETE"
        reason = None
    elif fresh_count:
        status = "PARTIAL"
        reason = ("Serving-model attestation failed; subsequent claims were not "
                  "verified." if attestation_failed else
                  "One or more provider requests failed; some bindings have no verdict.")
    else:
        status = "FAILED"
        reason = ("Serving-model attestation failed; no claims were accepted."
                  if attestation_failed else
                  "Provider verification was unavailable; no bindings were verified.")

    if carried and reason:
        reason += (f" Earlier verdicts for {len({e['claim_id'] for e in carried})} "
                   "claim(s) without a fresh result were kept.")

    document = {
        "model": model_id,
        "prompt_version": PROMPT_VERSION,
        "date": date,
        "status": status,
        "run_metadata": {
            "endpoint": ENDPOINT,
            "verification_scope": VERIFICATION_SCOPE,
            "model_attestation": ("FAILED" if attestation_failed
                                  else "EXACT_MATCH"),
            "serving_models": sorted(serving_models),
            "estimated_spend_usd": round(estimate, 8),
            "provider_reported_spend_usd": round(actual_cost, 8),
        },
    }
    if reason:
        document["reason"] = reason
    document["verdicts"] = records
    document["conflict_triage"] = conflict_triage
    atomic_write_json(pack_dir / "verdicts.json", document)

    alarms = sum(v["verdict"] == "MEANING_CHANGED"
                 for v in claim_results.values())
    cannot_judge = sum(v["verdict"] == "CANNOT_JUDGE" for v in records)

    if attestation_failed:
        exit_code = EXIT_MODEL_ATTESTATION
    elif provider_failed:
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
        print(f"ALARM [{product}]: {alarms} MEANING_CHANGED claim(s)", file=sys.stderr)
    print(f"[{product}] status={status} verdicts={len(records)}/{total} "
          f"alarm_claims={alarms} cannot_judge_bindings={cannot_judge} "
          f"serving_models={sorted(serving_models)} "
          f"estimated_spend=${estimate:.4f} provider_spend=${actual_cost:.4f}")
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
    cache_changed = malformed_seen = provider_failed = attestation_failed = False
    results = []
    estimate = 0.0
    actual_cost = 0.0
    serving_models = set()
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
            "conflict", list(pair), payload_hash, model_id, ENDPOINT,
            PROMPT_VERSION,
        ]))
        cached = cache.get(key)
        if (isinstance(cached, dict) and cached.get("result") in TRIAGE_RESULTS
                and isinstance(cached.get("note"), str) and cached["note"].strip()
                and cached.get("serving_model") == model_id):
            result = {"result": cached["result"], "note": cached["note"]}
            serving_models.add(cached["serving_model"])
            source = "cache"
        else:
            prompt = CONFLICT_PROMPT.format(
                quotes_a=json.dumps(payload["quotes_a"], ensure_ascii=False),
                context_a=payload["context_a"],
                quotes_b=json.dumps(payload["quotes_b"], ensure_ascii=False),
                context_b=payload["context_b"],
            )
            try:
                (result, serving_model, usage_cost, malformed,
                 provider_calls) = _invoke_for_triage(
                    prompt, provider, model_id=model_id)
            except ModelAttestationFailure as exc:
                attestation_failed = True
                if exc.serving_model:
                    serving_models.add(exc.serving_model)
                print(f"[{product}] conflict {index}/{len(pairs)} "
                      "serving-model attestation failure")
                break
            except ProviderFailure:
                provider_failed = True
                print(f"[{product}] conflict {index}/{len(pairs)} provider failure "
                      "(sanitized)")
                continue
            estimate += estimated_cost(prompt) * provider_calls
            actual_cost += usage_cost
            serving_models.add(serving_model)
            malformed_seen = malformed_seen or malformed
            if not malformed:
                cache[key] = {**result, "serving_model": serving_model}
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
    run_metadata = document.setdefault("run_metadata", {})
    existing_models = run_metadata.get("serving_models", [])
    run_metadata["serving_models"] = sorted(
        set(existing_models) | serving_models)
    if attestation_failed:
        run_metadata["model_attestation"] = "FAILED"
    run_metadata["conflict_estimated_spend_usd"] = round(estimate, 8)
    run_metadata["conflict_provider_reported_spend_usd"] = round(actual_cost, 8)
    atomic_write_json(pack_dir / "verdicts.json", document)
    if cache_changed:
        atomic_write_json(cache_path, cache)

    if attestation_failed:
        exit_code = EXIT_MODEL_ATTESTATION
    elif provider_failed:
        exit_code = EXIT_PROVIDER
    elif malformed_seen:
        exit_code = EXIT_MALFORMED
    elif len(results) != len(pairs):
        exit_code = EXIT_PARTIAL
    else:
        exit_code = EXIT_OK
    return {"exit_code": exit_code, "results": results,
            "estimated_spend_usd": estimate,
            "provider_reported_spend_usd": actual_cost,
            "serving_models": sorted(serving_models)}


def combine_exit_codes(codes):
    for code in (EXIT_MODEL_ATTESTATION, EXIT_MALFORMED, EXIT_PROVIDER,
                 EXIT_PARTIAL, EXIT_ALARM):
        if code in codes:
            return code
    return EXIT_OK


def worst_case_cost(prompt):
    """Conservative bound for one claim: two attempts at the maximum output,
    input counted at 3 characters per token, times 3 for unknown router markup."""
    input_tokens = max(1, len(prompt) // 3)
    per_attempt = (input_tokens * INPUT_USD_PER_MILLION_TOKENS
                   + 250 * OUTPUT_USD_PER_MILLION_TOKENS) / 1_000_000
    return per_attempt * 2 * 3


def verify_claims_to_receipts(pack_dir, claim_ids, run, run_id,
                              provider=call_provider, model_id=MODEL_ID):
    """Verify named claims and append version-bound receipts.

    ``run`` is a spend_guard.RunAuthorization; each claim reserves its worst
    case before the provider call. Never rewrites verdicts.json. A provider
    or attestation failure is recorded as its own receipt kind and stops the
    run with unknown billing; it never changes a claim's alarm state.
    """
    from system import evidence_status
    from system.spend_guard import SpendRefused

    pack_dir = Path(pack_dir)
    claims = {c["claim_id"]: c for c in load_json(pack_dir / "claims.json", [])}
    summary = {"verified": 0, "results": {}, "stopped": None}
    for claim_id in claim_ids:
        claim = claims[claim_id]
        prompt = build_prompt(claim)
        try:
            reservation = run.reserve(worst_case_cost(prompt), claim_id)
        except SpendRefused as exc:
            summary["stopped"] = str(exc)
            break
        base = {"claim_id": claim_id,
                "claim_digest": evidence_status.claim_digest(claim),
                "model": model_id, "prompt_version": PROMPT_VERSION,
                "run": run_id, "approval_id": run.approval_id,
                "receipt_id": f"rcpt_{run_id}_{claim_id}"}
        try:
            (result, serving_model, usage_cost, malformed,
             calls) = _invoke_for_verdict(prompt, provider, model_id=model_id)
        except (ProviderFailure, ModelAttestationFailure) as exc:
            run.settle(reservation, None, type(exc).__name__)
            evidence_status.append_receipt(pack_dir, {
                **base, "kind": "provider_failure", "result": type(exc).__name__})
            summary["stopped"] = f"{type(exc).__name__} on {claim_id}"
            break
        # A missing provider cost is counted at the reserved worst case.
        actual = usage_cost if usage_cost > 0 else run_reserved(run, reservation)
        run.settle(reservation, actual, "malformed" if malformed else "ok")
        evidence_status.append_receipt(pack_dir, {
            **base, "kind": "semantic_check", "result": result["verdict"],
            "note": result["note"], "serving_model": serving_model,
            "provider_calls": calls, "usage_usd": usage_cost})
        summary["verified"] += 1
        summary["results"][claim_id] = result["verdict"]
    return summary


def run_reserved(run, reservation_id):
    for entry in reversed(run.guard._run_events(run.approval_id)):
        if entry.get("reservation_id") == reservation_id and entry["event"] == "reserve":
            return entry["worst_case_usd"]
    return None


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
