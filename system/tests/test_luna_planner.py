import json
from types import SimpleNamespace

import system.luna_planner as luna_planner_module
from system.luna_planner import (
    LunaPlanner,
    apply_presentation,
    deterministic_presentation,
)


class FakeResponses:
    def __init__(self, intent_name="search_evidence", intent_arguments=None,
                 composition=None, error=None):
        self.intent_name = intent_name
        self.intent_arguments = intent_arguments or {
            "product_id": "product-a",
            "normalized_question": "How do I pair the device?",
            "requested_modalities": [],
            "excluded_modalities": [],
            "reason_code": "PROCEDURE_REQUEST",
            "confidence": 0.9,
        }
        self.composition = composition or {
            "primary_modality": "text",
            "supplemental_modalities": [],
            "asset_ids": [],
            "reason_code": "TEXT_IS_SUFFICIENT",
            "confidence": 0.9,
        }
        self.error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        usage = SimpleNamespace(
            input_tokens=20, output_tokens=10, total_tokens=30)
        if "tools" in kwargs:
            return SimpleNamespace(
                id="resp_intent",
                output=[SimpleNamespace(
                    type="function_call",
                    name=self.intent_name,
                    arguments=json.dumps(self.intent_arguments),
                    call_id="call_intent",
                )],
                usage=usage,
            )
        return SimpleNamespace(
            id="resp_composition",
            output_text=json.dumps(self.composition),
            usage=usage,
        )


def fake_client(responses):
    return SimpleNamespace(responses=responses)


def scope():
    products = [{
        "id": "product-a", "brand": "Acme", "model": "A",
        "category": "device",
    }]
    procedures = {"product-a": ["pair_device", "wired_or_wireless"]}
    return products, procedures


def results_with_media():
    return [{
        "claim_id": "procedure:pair_device",
        "type": "PROCEDURE",
        "procedure": "pair_device",
        "display_text": "Pair the device in three steps.",
        "media": [{
            "id": "image-1", "kind": "IMAGE", "asset_type": None,
        }, {
            "id": "video-1", "kind": "DERIVED_ASSET",
            "asset_type": "PROCEDURE_VIDEO_MP4",
        }],
    }]


def test_missing_api_key_selects_explicit_deterministic_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("SHOWME_LUNA_ENABLED", raising=False)
    planner = LunaPlanner()
    products, procedures = scope()

    outcome = planner.plan_intent("How do I pair it?", products, procedures)

    assert not outcome["ok"]
    assert outcome["metadata"]["reason"] == "credentials_missing"
    assert planner.status == {
        "enabled": False,
        "model": "gpt-5.6-luna",
        "reason": "credentials_missing",
    }


def test_missing_sdk_is_reported_as_disabled_at_startup(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("SHOWME_LUNA_ENABLED", raising=False)
    monkeypatch.setattr(luna_planner_module, "find_spec", lambda _name: None)

    planner = LunaPlanner()

    assert planner.status == {
        "enabled": False,
        "model": "gpt-5.6-luna",
        "reason": "sdk_unavailable",
    }


def test_intent_turn_uses_required_function_call_and_validates_allowlist():
    responses = FakeResponses(
        intent_name="show_procedure",
        intent_arguments={
            "product_id": "product-a",
            "normalized_question": "How do I pair the device?",
            "requested_modalities": ["video"],
            "excluded_modalities": [],
            "reason_code": "EXACT_PROCEDURE",
            "confidence": 0.96,
            "procedure_id": "pair_device",
        })
    planner = LunaPlanner(client=fake_client(responses))
    products, procedures = scope()

    outcome = planner.plan_intent("How do I pair it?", products, procedures)

    assert outcome["ok"]
    assert outcome["plan"]["tool"] == "show_procedure"
    assert outcome["plan"]["procedure_id"] == "pair_device"
    assert outcome["metadata"]["response_id"] == "resp_intent"
    request = responses.calls[0]
    assert request["model"] == "gpt-5.6-luna"
    assert request["tool_choice"] == "required"
    assert request["parallel_tool_calls"] is False
    assert request["reasoning"] == {"effort": "low"}
    assert request["store"] is False
    assert "uniqueItems" not in json.dumps(request["tools"])


def test_intent_turn_rejects_invented_procedure_identifier():
    responses = FakeResponses(
        intent_name="show_procedure",
        intent_arguments={
            "product_id": "product-a",
            "normalized_question": "Run the secret procedure.",
            "requested_modalities": [],
            "excluded_modalities": [],
            "reason_code": "EXACT_PROCEDURE",
            "confidence": 0.7,
            "procedure_id": "invented_secret_procedure",
        })
    planner = LunaPlanner(client=fake_client(responses))
    products, procedures = scope()

    outcome = planner.plan_intent("Run it", products, procedures)

    assert not outcome["ok"]
    assert outcome["metadata"]["reason"] == "invalid_tool_arguments"


def test_composition_turn_selects_only_eligible_nonexcluded_media():
    responses = FakeResponses(composition={
        "primary_modality": "image",
        "supplemental_modalities": ["text"],
        "asset_ids": ["image-1"],
        "reason_code": "LOCATION_BENEFITS_FROM_IMAGE",
        "confidence": 0.94,
    })
    planner = LunaPlanner(client=fake_client(responses))
    intent = {
        "ok": True,
        "plan": {
            "tool": "search_evidence",
            "excluded_modalities": ["video"],
        },
        "metadata": {"response_id": "resp_intent",
                     "call_id": "call_intent"},
    }
    results = results_with_media()

    outcome = planner.compose_response("Show me, but no video", intent, results)
    apply_presentation(results, outcome["plan"])

    assert outcome["ok"]
    assert outcome["plan"]["asset_ids"] == ["image-1"]
    assert [media["id"] for media in results[0]["media"]] == ["image-1"]
    request = responses.calls[0]
    assert request["text"]["format"]["type"] == "json_schema"
    assert "uniqueItems" not in json.dumps(request["text"])
    sent = json.loads(request["input"])
    assert sent["intent_response_id"] == "resp_intent"
    assert sent["intent_call_id"] == "call_intent"


def test_composition_turn_rejects_unknown_asset_and_keeps_fallback_media():
    responses = FakeResponses(composition={
        "primary_modality": "video",
        "supplemental_modalities": ["text"],
        "asset_ids": ["invented-video"],
        "reason_code": "USE_VIDEO",
        "confidence": 0.8,
    })
    planner = LunaPlanner(client=fake_client(responses))
    intent = {
        "ok": True,
        "plan": {"tool": "search_evidence", "excluded_modalities": []},
        "metadata": {"response_id": "resp_intent", "call_id": "call"},
    }
    results = results_with_media()

    outcome = planner.compose_response("Show me", intent, results)
    presentation = deterministic_presentation(
        results, outcome["metadata"]["reason"])

    assert not outcome["ok"]
    assert outcome["metadata"]["reason"] == "invalid_structured_output"
    assert presentation["asset_ids"] == ["image-1", "video-1"]


def test_provider_timeout_never_exposes_provider_error_text():
    responses = FakeResponses(error=TimeoutError("secret request detail"))
    planner = LunaPlanner(client=fake_client(responses))
    products, procedures = scope()

    outcome = planner.plan_intent("Pair it", products, procedures)

    assert not outcome["ok"]
    assert outcome["metadata"]["reason"] == "provider_timeout"
    assert "secret" not in json.dumps(outcome)


def test_insufficient_quota_has_specific_safe_fallback_reason():
    class QuotaError(Exception):
        code = "insufficient_quota"
        status_code = 429

    responses = FakeResponses(error=QuotaError("billing detail"))
    planner = LunaPlanner(client=fake_client(responses))
    products, procedures = scope()

    outcome = planner.plan_intent("Pair it", products, procedures)

    assert not outcome["ok"]
    assert outcome["metadata"]["reason"] == "insufficient_quota"
    assert "billing detail" not in json.dumps(outcome)
