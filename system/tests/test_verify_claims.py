import json

from system import verify_claims as verifier


def claim(claim_id, tier="C3", value=30, source_id="src_text",
          notes="private extractor rationale"):
    return {
        "claim_id": claim_id,
        "type": "LIMIT",
        "predicate": "maximum_weight",
        "object": {"value": value, "unit": "lb"},
        "consequence_ceiling": tier,
        "source_bindings": [{
            "source_id": source_id,
            "page": None,
            "quote": "The maximum supported weight is 30 lb.",
        }],
        "extraction_notes": notes,
    }


def make_pack(tmp_path, claims, reviews=None):
    root = tmp_path / "scratch-repository"
    pack = root / "evidence-packs" / "test-product"
    vault = root / "source-vault" / "test-product"
    pack.mkdir(parents=True)
    vault.mkdir(parents=True)
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    (vault / "source.md").write_text(
        "The maximum supported weight is 30 lb.\n", encoding="utf-8")
    (vault / "visual.png").write_bytes(b"not-a-real-image")
    manifest = {
        "sources": [
            {"source_id": "src_text", "type": "SPEC_PAGE",
             "local_path": "source.md"},
            {"source_id": "src_visual", "type": "IMAGE",
             "local_path": "visual.png"},
        ]
    }
    (vault / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    if reviews is not None:
        (pack / "reviews.json").write_text(
            json.dumps({"reviews": reviews}, indent=2) + "\n", encoding="utf-8")
    return pack, root / "source-vault", root / "cache.json"


class SemanticProvider:
    def __init__(self):
        self.arguments = []

    def __call__(self, arguments):
        self.arguments.append(arguments)
        prompt = arguments["prompt"]
        changed = '"value":35' in prompt
        result = {
            "verdict": "MEANING_CHANGED" if changed else "ENTAILED",
            "note": ("The translation changes 30 lb to 35 lb."
                     if changed else "The translation faithfully states 30 lb."),
        }
        return {
            "output": json.dumps(result),
            "model": verifier.MODEL_ID,
            "usage": {"cost": 0.0001},
        }


def test_faithful_routing_visual_skip_and_prompt_blindness(tmp_path):
    c0 = claim("claim_c0", tier="C0")
    c3 = claim("claim_c3", tier="C3")
    c3["source_bindings"].append({
        "source_id": "src_visual",
        "page": None,
        "quote": "Visual overlay says 30 lb.",
    })
    pack, vault, cache = make_pack(tmp_path, [c0, c3])
    provider = SemanticProvider()

    run = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                               provider=provider, date="2026-08-24")

    assert run["exit_code"] == verifier.EXIT_OK
    assert run["status"] == "COMPLETE"
    assert run["alarms"] == 0
    assert run["cannot_judge"] == 1
    assert len(provider.arguments) == 2
    for arguments in provider.arguments:
        assert arguments["model"].startswith("qwen/")
        assert "private extractor rationale" not in arguments["prompt"]
        assert "claim_c0" not in arguments["prompt"]
        assert "claim_c3" not in arguments["prompt"]

    assert not (pack / "reviews.json").exists()

    document = json.loads((pack / "verdicts.json").read_text())
    assert document["status"] == "COMPLETE"
    assert len(document["verdicts"]) == 3
    assert document["run_metadata"]["verification_scope"] == \
        verifier.VERIFICATION_SCOPE
    assert document["run_metadata"]["model_attestation"] == "EXACT_MATCH"
    assert document["run_metadata"]["serving_models"] == [verifier.MODEL_ID]
    assert all(entry["basis"] == verifier.VERIFICATION_SCOPE
               for entry in document["verdicts"])


def test_warm_cache_misses_when_translation_changes(tmp_path):
    pack, vault, cache = make_pack(tmp_path, [claim("claim_drift", tier="C3")])
    provider = SemanticProvider()
    first = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                                 provider=provider, date="2026-08-24")
    assert first["exit_code"] == verifier.EXIT_OK
    assert len(provider.arguments) == 1

    claims = json.loads((pack / "claims.json").read_text())
    claims[0]["object"]["value"] = 35
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    second = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                                  provider=provider, date="2026-08-24")

    assert len(provider.arguments) == 2, "translation mutation must be a cache miss"
    assert second["exit_code"] == verifier.EXIT_ALARM
    assert second["alarms"] == 1
    verdict = json.loads((pack / "verdicts.json").read_text())["verdicts"][0]
    assert verdict["verdict"] == "MEANING_CHANGED"


def test_verifier_never_mutates_human_reviews(tmp_path):
    human = {
        "review_id": "rev_human",
        "date": "2026-08-24",
        "reviewer": "reviewer@example.com",
        "scope": "manual",
        "claim_id": "claim_c0",
        "disposition": "NEEDS_RECHECK",
        "rationale": "Human decision must win.",
    }
    pack, vault, cache = make_pack(
        tmp_path, [claim("claim_c0", tier="C0")], reviews=[human])
    before = (pack / "reviews.json").read_bytes()
    provider = SemanticProvider()

    first = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                                 provider=provider, date="2026-08-24")
    second = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                                  provider=provider, date="2026-08-24")

    assert first["status"] == "COMPLETE"
    assert second["status"] == "COMPLETE"
    assert (pack / "reviews.json").read_bytes() == before
    reviews = json.loads(before)["reviews"]
    assert reviews == [human]


def test_malformed_response_retries_then_records_cannot_judge(tmp_path):
    pack, vault, cache = make_pack(tmp_path, [claim("claim_bad", tier="C3")])
    calls = []

    def malformed(arguments):
        calls.append(arguments)
        return {"output": "not json", "model": verifier.MODEL_ID}

    run = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                               provider=malformed, date="2026-08-24")
    assert len(calls) == 2
    assert run["exit_code"] == verifier.EXIT_MALFORMED
    assert run["status"] == "COMPLETE"
    assert run["verdicts"][0]["verdict"] == "CANNOT_JUDGE"


def test_provider_failure_is_sanitized_and_writes_failed_artifact(tmp_path):
    pack, vault, cache = make_pack(tmp_path, [claim("claim_fail", tier="C3")])

    def failed(_arguments):
        raise verifier.ProviderFailure("credential=super-secret-value")

    run = verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                               provider=failed, date="2026-08-24")
    document_text = (pack / "verdicts.json").read_text()
    document = json.loads(document_text)
    assert run["exit_code"] == verifier.EXIT_PROVIDER
    assert document["status"] == "FAILED"
    assert document["verdicts"] == []
    assert "super-secret-value" not in document_text


def test_model_positive_allowlist():
    assert verifier.MODEL_ID.startswith("qwen/")
    assert verifier.MODEL_ID == "qwen/qwen3-vl-235b-a22b-instruct"
    assert verifier.ENDPOINT == \
        "openrouter/router/openai/v1/chat/completions"
    assert verifier.PROMPT_VERSION == "v2"
    assert verifier.VERIFICATION_SCOPE == "CLAIM_QUOTE_UNION"


def test_conflict_triage_parses_caches_and_writes_artifact(tmp_path):
    first = claim("claim_a", tier="C3")
    second = claim("claim_b", tier="C3")
    first["extraction_notes"] = "CONFLICT: contradicts claim_b — compare sources."
    second["extraction_notes"] = "CONFLICT: contradicts claim_a — compare sources."
    pack, vault, cache = make_pack(tmp_path, [first, second])
    semantic = SemanticProvider()
    verifier.verify_pack(pack, vault_root=vault, cache_path=cache,
                         provider=semantic, date="2026-08-24")
    calls = []

    def triage(arguments):
        calls.append(arguments)
        assert "compare sources" not in arguments["prompt"]
        return {"output": json.dumps({
            "result": "DIFFERENT_SCOPE_OR_EVENT",
            "note": "The passages describe different operating events.",
        }), "model": verifier.MODEL_ID}

    first_run = verifier.triage_conflicts(
        pack, vault_root=vault, cache_path=cache, provider=triage)
    second_run = verifier.triage_conflicts(
        pack, vault_root=vault, cache_path=cache, provider=triage)

    assert first_run["exit_code"] == verifier.EXIT_OK
    assert second_run["exit_code"] == verifier.EXIT_OK
    assert len(calls) == 1
    entry = json.loads((pack / "verdicts.json").read_text())["conflict_triage"][0]
    assert entry["pair"] == ["claim_a", "claim_b"]
    assert entry["result"] == "DIFFERENT_SCOPE_OR_EVENT"
    assert len(entry["context_sha256"]) == 64


def test_v2_projection_strips_scaffolding_and_unions_quotes():
    step = {
        "type": "STEP",
        "predicate": "procedure_step",
        "object": {
            "procedure": "fold_stroller", "step_number": 6,
            "action": "Check that the stroller is secure.",
            "target_parts": ["stroller_frame"],
            "initial_state": "FOLD_LEVER_SQUEEZED",
            "resulting_state": "FOLDED_SECURED",
        },
        "consequence_ceiling": "C3",
        "source_bindings": [{
            "source_id": "manual", "quote": "CHECK that the stroller is secure.",
        }],
    }
    prompt = verifier.build_prompt(step)
    assert "Check that the stroller is secure." in prompt
    for scaffolding in ("fold_stroller", "step_number", "stroller_frame",
                        "FOLD_LEVER_SQUEEZED", "FOLDED_SECURED"):
        assert scaffolding not in prompt

    dimensions = {
        "type": "SPEC", "predicate": "dimensions",
        "object": {"width": 15.5, "height": 27.4, "depth": 18.07,
                   "unit": "in"},
        "consequence_ceiling": "C1",
        "source_bindings": [
            {"source_id": "spec", "quote": "Product width 15.5 in"},
            {"source_id": "spec", "quote": "Product height 27.4 in"},
            {"source_id": "spec", "quote": "Product depth 18.07 in"},
        ],
    }
    prompt = verifier.build_prompt(dimensions)
    assert all(text in prompt for text in (
        "Product width 15.5 in", "Product height 27.4 in",
        "Product depth 18.07 in"))
    assert "Judge the EXACT QUOTES AS A UNION" in prompt
    assert "JSON field\nnames and structure are labels" in prompt


def test_v2_prompt_preserves_three_known_genuine_catches():
    cases = [
        ({"value": 219, "unit": "ft²", "metric": "20 m²"},
         "Make sure the room is smaller than 219 ft² / 20 m²."),
        ({"value": 30, "unit": "ft", "value_metric": 9, "unit_metric": "m"},
         "The devices must be within range (30 ft or 9 m) and powered on."),
        ({"counterpart": "Bose Smart Speakers and Bose Smart Soundbars",
          "feature": "SimpleSync",
          "notes_list": ["Bose Smart Ultra Soundbar", "Bose Smart Soundbar"]},
         "You can connect the headphones to any Bose Smart Speaker or Bose Smart Soundbar."),
    ]
    prompts = []
    for index, (obj, quote_text) in enumerate(cases):
        item = {
            "type": "LIMIT" if index == 0 else "SPEC",
            "predicate": f"catch_{index}", "object": obj,
            "consequence_ceiling": "C2",
            "source_bindings": [{"source_id": "src", "quote": quote_text}],
        }
        prompts.append(verifier.build_prompt(item))

    assert "smaller than 219" in prompts[0]
    assert "powered on" in prompts[1]
    assert "SimpleSync" in prompts[2]
    assert "Bose Smart Ultra Soundbar" in prompts[2]
    for prompt in prompts:
        assert "lost\ngoverning condition" in prompt
        assert "assert something more broadly" in prompt


def test_serving_model_mismatch_stops_and_records_failed_attestation(tmp_path):
    pack, vault, cache = make_pack(tmp_path, [claim("claim_model", tier="C0")])

    def wrong_model(_arguments):
        return {
            "output": json.dumps({"verdict": "ENTAILED", "note": "faithful"}),
            "model": "qwen/a-different-model",
        }

    run = verifier.verify_pack(
        pack, vault_root=vault, cache_path=cache, provider=wrong_model,
        date="2026-08-26")
    document = json.loads((pack / "verdicts.json").read_text())

    assert run["exit_code"] == verifier.EXIT_MODEL_ATTESTATION
    assert document["status"] == "FAILED"
    assert document["run_metadata"]["model_attestation"] == "FAILED"
    assert document["run_metadata"]["serving_models"] == [
        "qwen/a-different-model"]


def test_missing_serving_model_stops_and_chat_envelope_parses(tmp_path):
    response = {
        "choices": [{"message": {"content": json.dumps({
            "verdict": "ENTAILED", "note": "faithful",
        })}}],
        "model": verifier.MODEL_ID,
        "usage": {"cost": 0.0002},
    }
    parsed, serving_model, cost, malformed, calls = \
        verifier._invoke_for_verdict("prompt", lambda _arguments: response)
    assert parsed["verdict"] == "ENTAILED"
    assert serving_model == verifier.MODEL_ID
    assert cost == 0.0002
    assert malformed is False
    assert calls == 1

    pack, vault, cache = make_pack(tmp_path, [claim("claim_no_model", tier="C0")])

    def missing_model(_arguments):
        return {"output": json.dumps({
            "verdict": "ENTAILED", "note": "faithful",
        })}

    run = verifier.verify_pack(
        pack, vault_root=vault, cache_path=cache, provider=missing_model,
        date="2026-08-26")
    document = json.loads((pack / "verdicts.json").read_text())
    assert run["exit_code"] == verifier.EXIT_MODEL_ATTESTATION
    assert document["run_metadata"]["model_attestation"] == "FAILED"
    assert document["run_metadata"]["serving_models"] == []
