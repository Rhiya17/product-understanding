import hashlib
import json
import os
import threading
from contextlib import contextmanager
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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


def build_fixture(tmp_path, approve_media=False):
    vault = tmp_path / "vault"
    packs = tmp_path / "packs"
    products = [
        ("acme-widget-9000", "prod_acme", "Acme", "Widget 9000", 7.5),
        ("beta-widget-2", "prod_beta", "Beta", "Widget 2", 4.0),
    ]
    catalog = []
    for product_dir, product_id, brand, model, weight in products:
        (vault / product_dir / "images").mkdir(parents=True)
        (vault / product_dir / "videos").mkdir(parents=True)
        (packs / product_dir).mkdir(parents=True)
        catalog.append({
            "product_id": product_id,
            "dir": product_dir,
            "brand": brand,
            "model": model,
            "category": "widget",
        })
        image_bytes = b"fixture image bytes"
        video_bytes = b"fixture video bytes"
        (vault / product_dir / "images" / "spec.png").write_bytes(image_bytes)
        (vault / product_dir / "videos" / "demo.mp4").write_bytes(video_bytes)
        (vault / product_dir / "manifest.json").write_text(json.dumps({
            "identity": {"brand": brand, "model": model},
            "sources": [{
                "source_id": "src_spec",
                "origin_url": f"https://example.com/{product_dir}/spec",
            }, {
                "source_id": "src_image",
                "type": "IMAGE",
                "local_path": "images/spec.png",
                "sha256": hashlib.sha256(image_bytes).hexdigest(),
                "authority": "MANUFACTURER",
            }, {
                "source_id": "src_video",
                "type": "VIDEO",
                "local_path": "videos/demo.mp4",
                "sha256": hashlib.sha256(video_bytes).hexdigest(),
                "authority": "MANUFACTURER",
                "rights_note": "Manufacturer copyright; internal research use.",
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
        approval = "owner@example.com" if approve_media else None
        (packs / product_dir / "media-bindings.json").write_text(json.dumps({
            "bindings": [{
                "binding_id": f"mb_{product_id}_image",
                "claim_ids": [claims[0]["claim_id"]],
                "source_id": "src_image",
                "kind": "IMAGE",
                "page": None,
                "start_seconds": None,
                "end_seconds": None,
                "rationale": "The registered product image shows the fixture specification.",
                "proposed_by": "agent",
                "approved_by": approval,
            }, {
                "binding_id": f"mb_{product_id}_video",
                "claim_ids": [claims[0]["claim_id"]],
                "source_id": "src_video",
                "kind": "VIDEO_FILE",
                "page": None,
                "start_seconds": None,
                "end_seconds": None,
                "rationale": "The registered manufacturer video demonstrates the fixture specification.",
                "proposed_by": "agent",
                "approved_by": approval,
            }],
        }), encoding="utf-8")
    vault.mkdir(exist_ok=True)
    (vault / "catalog.json").write_text(
        json.dumps({"products": catalog}), encoding="utf-8")
    return packs, vault


@contextmanager
def running_server(tmp_path, approve_media=False, yield_roots=False):
    packs, vault = build_fixture(tmp_path, approve_media=approve_media)
    httpd = server.create_server(0, packs, vault)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{httpd.server_port}"
        yield (base_url, packs, vault) if yield_roots else base_url
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


def test_unapproved_media_appears_only_in_preview(tmp_path):
    with running_server(tmp_path) as base_url:
        _, default = get_json(base_url, "/api/answer", {
            "q": "acme weight", "preview": 0, "top": 10,
        })
        _, preview = get_json(base_url, "/api/answer", {
            "q": "acme weight", "preview": 1, "top": 10,
        })
    assert default["results"][0]["media"] == []
    assert {item["kind"] for item in preview["results"][0]["media"]} == {
        "IMAGE", "VIDEO_FILE",
    }
    assert all(item["awaiting_approval"]
               for item in preview["results"][0]["media"])
    video = next(item for item in preview["results"][0]["media"]
                 if item["kind"] == "VIDEO_FILE")
    assert video["rights_note"] == "Manufacturer copyright; internal research use."


def test_owner_approved_media_appears_without_preview(tmp_path):
    with running_server(tmp_path, approve_media=True) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "acme weight", "preview": 0, "top": 10,
        })
    assert len(payload["results"][0]["media"]) == 2
    assert not any(item["awaiting_approval"]
                   for item in payload["results"][0]["media"])


def test_media_route_is_registered_read_only_and_path_safe(tmp_path):
    with running_server(tmp_path) as base_url:
        with urlopen(
                f"{base_url}/media/acme-widget-9000/images/spec.png",
                timeout=2) as response:
            assert response.status == 200
            assert response.read() == b"fixture image bytes"
        try:
            urlopen(
                f"{base_url}/media/acme-widget-9000/%2e%2e/catalog.json",
                timeout=2)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("media path traversal unexpectedly succeeded")


def test_video_file_is_range_served_only_while_hash_matches(tmp_path):
    with running_server(tmp_path, yield_roots=True) as fixture:
        base_url, _, vault = fixture
        video_url = f"{base_url}/media/acme-widget-9000/videos/demo.mp4"
        request = Request(video_url, headers={"Range": "bytes=0-6"})
        with urlopen(request, timeout=2) as response:
            assert response.status == 206
            assert response.read() == b"fixture"

        video_path = vault / "acme-widget-9000" / "videos" / "demo.mp4"
        old_stat = video_path.stat()
        video_path.write_bytes(b"tampered video bytes")
        os.utime(video_path, ns=(old_stat.st_atime_ns, old_stat.st_mtime_ns + 1_000_000))
        try:
            urlopen(video_url, timeout=2)
        except HTTPError as error:
            assert error.code == 500
            assert json.loads(error.read())["error"] == "Media integrity check failed"
        else:
            raise AssertionError("tampered video unexpectedly served")
