import json
import threading
from contextlib import contextmanager
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from app import server


def make_claim(claim_id, predicate, obj, quote):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": "C0",
        "type": "SPEC",
        "predicate": predicate,
        "object": obj,
        "source_bindings": [{
            "source_id": "src_spec", "page": None, "quote": quote,
        }],
    }


def build_fixture(tmp_path):
    vault = tmp_path / "vault"
    packs = tmp_path / "packs"
    products = [
        ("acme-widget-9000", "prod_acme", "Acme", "Widget 9000", 7.5),
        ("beta-widget-2", "prod_beta", "Beta", "Widget 2", 4.0),
    ]
    catalog = []
    for product_dir, product_id, brand, model, weight in products:
        (vault / product_dir).mkdir(parents=True)
        (packs / product_dir).mkdir(parents=True)
        catalog.append({
            "product_id": product_id,
            "dir": product_dir,
            "brand": brand,
            "model": model,
            "category": "widget",
        })
        (vault / product_dir / "manifest.json").write_text(json.dumps({
            "sources": [{
                "source_id": "src_spec",
                "origin_url": f"https://example.com/{product_dir}/spec",
            }],
        }), encoding="utf-8")
        claims = [
            make_claim(f"claim_{product_id}_weight", "product_weight",
                       {"value": weight, "unit": "lb"}, f"Weight {weight} lb"),
            make_claim(f"claim_{product_id}_noise", "noise_level",
                       {"value": 24, "unit": "dB"}, "Noise level 24 dB"),
            make_claim(f"claim_{product_id}_old", "product_weight",
                       {"value": 99, "unit": "lb"}, "Old weight 99 lb"),
        ]
        (packs / product_dir / "claims.json").write_text(
            json.dumps(claims), encoding="utf-8")
        (packs / product_dir / "reviews.json").write_text(json.dumps({
            "reviews": [
                {"claim_id": claims[0]["claim_id"],
                 "reviewer": "owner@example.com",
                 "disposition": "APPROVED_FOR_PUBLISH"},
                {"claim_id": claims[2]["claim_id"],
                 "reviewer": "owner@example.com",
                 "disposition": "REJECTED_FOR_SERVING"},
            ],
        }), encoding="utf-8")
        (packs / product_dir / "verdicts.json").write_text(
            json.dumps({"verdicts": []}), encoding="utf-8")
    vault.mkdir(exist_ok=True)
    (vault / "catalog.json").write_text(
        json.dumps({"products": catalog}), encoding="utf-8")
    return packs, vault


@contextmanager
def running_server(tmp_path):
    packs, vault = build_fixture(tmp_path)
    httpd = server.create_server(0, packs, vault)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def get_json(base_url, path, params=None):
    query = f"?{urlencode(params)}" if params else ""
    with urlopen(f"{base_url}{path}{query}", timeout=2) as response:
        return response.status, json.loads(response.read())


def test_default_serves_only_published_and_never_rejected(tmp_path):
    with running_server(tmp_path) as base_url:
        status, payload = get_json(base_url, "/api/answer", {
            "q": "what is the product weight and noise?", "preview": 0,
            "top": 10,
        })
    assert status == 200
    assert payload["results"]
    assert {row["status"] for row in payload["results"]} == {"PUBLISHED"}
    assert all("_old" not in row["claim_id"] for row in payload["results"])
    assert payload["not_served"]["CANDIDATE"] == 2
    assert payload["not_served"]["REJECTED"] == 2


def test_preview_adds_labeled_candidates_but_not_rejected(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "widget noise and weight", "preview": 1, "top": 20,
        })
    statuses = {row["claim_id"]: row["status"] for row in payload["results"]}
    assert "CANDIDATE" in statuses.values()
    assert "PUBLISHED" in statuses.values()
    assert all("_old" not in claim_id for claim_id in statuses)


def test_product_filter_restricts_results(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "product weight", "product": "beta-widget-2", "top": 10,
        })
    assert [row["product"] for row in payload["results"]] == ["Beta Widget 2"]


def test_empty_question_returns_400_json(tmp_path):
    with running_server(tmp_path) as base_url:
        try:
            get_json(base_url, "/api/answer", {"q": "   "})
        except HTTPError as error:
            assert error.code == 400
            assert json.loads(error.read())["error"] == "Question must not be empty"
        else:
            raise AssertionError("empty question unexpectedly succeeded")


def test_unknown_product_returns_404(tmp_path):
    with running_server(tmp_path) as base_url:
        try:
            get_json(base_url, "/api/answer", {
                "q": "product weight", "product": "missing-product",
            })
        except HTTPError as error:
            assert error.code == 404
            assert json.loads(error.read())["error"] == "Unknown product"
        else:
            raise AssertionError("unknown product unexpectedly succeeded")
