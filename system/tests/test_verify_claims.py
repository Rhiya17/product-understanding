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
        return {"output": json.dumps(result)}


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

    reviews = json.loads((pack / "reviews.json").read_text())["reviews"]
    assert [entry["claim_id"] for entry in reviews] == ["claim_c0"]
    assert reviews[0]["reviewer"] == verifier.AUTO_REVIEWER
    assert reviews[0]["scope"] == "verifier_auto"
    assert all(entry["claim_id"] != "claim_c3" for entry in reviews)

    document = json.loads((pack / "verdicts.json").read_text())
    assert document["status"] == "COMPLETE"
    assert len(document["verdicts"]) == 3


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


def test_human_review_precedence_survives_repeated_runs(tmp_path):
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

    assert first["auto_approvals"]["human_precedence"] == 1
    assert second["auto_approvals"]["human_precedence"] == 1
    assert (pack / "reviews.json").read_bytes() == before
    reviews = json.loads(before)["reviews"]
    assert reviews == [human]


def test_malformed_response_retries_then_records_cannot_judge(tmp_path):
    pack, vault, cache = make_pack(tmp_path, [claim("claim_bad", tier="C3")])
    calls = []

    def malformed(arguments):
        calls.append(arguments)
        return {"output": "not json"}

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
        })}

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
