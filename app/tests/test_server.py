import hashlib
import json
import os
import struct
import threading
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import server


FIXTURE_PDF = Path(__file__).resolve().parent / "fixtures" / "manual-fixture.pdf"


def make_claim(claim_id, predicate, obj, quote, tier="C0", claim_type="SPEC"):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": tier,
        "type": claim_type,
        "predicate": predicate,
        "object": obj,
        "source_bindings": [{
            "source_id": "src_spec", "page": None, "quote": quote,
        }],
    }


def make_step_claim(claim_id, step_number, action):
    return {
        "claim_id": claim_id,
        "consequence_ceiling": "C1",
        "type": "STEP",
        "predicate": "procedure_step",
        "object": {
            "procedure": "calibrate_widget",
            "step_number": step_number,
            "action": action,
        },
        "source_bindings": [{
            "source_id": "src_manual", "page": 1, "quote": action,
        }],
    }


def build_fixture(tmp_path, approve_media=False, include_derived=False):
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
        (vault / product_dir / "manuals").mkdir(parents=True)
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
        pdf_bytes = FIXTURE_PDF.read_bytes()
        (vault / product_dir / "images" / "spec.png").write_bytes(image_bytes)
        (vault / product_dir / "videos" / "demo.mp4").write_bytes(video_bytes)
        (vault / product_dir / "manuals" / "manual.pdf").write_bytes(pdf_bytes)
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
            }, {
                "source_id": "src_manual",
                "type": "MANUAL_PDF",
                "local_path": "manuals/manual.pdf",
                "sha256": hashlib.sha256(pdf_bytes).hexdigest(),
                "authority": "MANUFACTURER",
            }],
        }), encoding="utf-8")
        claims = [
            make_claim(f"claim_{product_id}_weight", "product_weight",
                       {"value": weight, "unit": "lb"}, f"Weight {weight} lb"),
            make_claim(f"claim_{product_id}_noise", "noise_level",
                       {"value": 24, "unit": "dB"}, "Noise level 24 dB",
                       tier="C3"),
            make_claim(f"claim_{product_id}_old", "product_weight",
                       {"value": 99, "unit": "lb"}, "Old weight 99 lb"),
            make_step_claim(f"claim_{product_id}_calibrate_1", 1,
                            "Open the calibration panel."),
            make_step_claim(f"claim_{product_id}_calibrate_2", 2,
                            "Press the calibration button."),
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
                {"claim_id": claims[3]["claim_id"],
                 "reviewer": "owner@example.com",
                 "disposition": "APPROVED_FOR_PUBLISH"},
            ],
        }), encoding="utf-8")
        (packs / product_dir / "verdicts.json").write_text(
            json.dumps({"verdicts": []}), encoding="utf-8")
        (packs / product_dir / "gaps.json").write_text(json.dumps({
            "gaps": [{
                "gap_id": f"gap_{product_id}_warp_drive",
                "kind": "SOURCE_MISSING",
                "reason": "The warp drive source is missing and the feature is not documented.",
                "closes_when": "A manufacturer source documents warp drive support.",
            }],
        }), encoding="utf-8")
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
            }, {
                "binding_id": f"mb_{product_id}_manual_page",
                "claim_ids": [claims[3]["claim_id"]],
                "source_id": "src_manual",
                "kind": "PDF_PAGE",
                "page": 1,
                "start_seconds": None,
                "end_seconds": None,
                "rationale": "The registered manual page illustrates the first calibration step.",
                "proposed_by": "agent",
                "approved_by": approval,
            }],
        }), encoding="utf-8")
        if include_derived:
            derived_bytes = b"GIF89a derived fixture"
            derived_path = tmp_path / "derived" / f"{product_dir}.gif"
            derived_path.parent.mkdir(exist_ok=True)
            derived_path.write_bytes(derived_bytes)
            (packs / product_dir / "derived-assets.json").write_text(json.dumps({
                "schema_version": 1,
                "product_id": product_id,
                "assets": [{
                    "asset_id": f"derived_{product_id}_turntable",
                    "type": "TURNTABLE_GIF",
                    "label": f"{brand} {model} turntable",
                    "watermark": "INTERNAL ONLY — NOT FOR DISTRIBUTION",
                    "local_path": f"derived/{product_dir}.gif",
                    "sha256": hashlib.sha256(derived_bytes).hexdigest(),
                    "provider": "local deterministic fixture",
                    "approved_by": None,
                    "internal_only": True,
                }],
            }), encoding="utf-8")
            media_path = packs / product_dir / "media-bindings.json"
            media_doc = json.loads(media_path.read_text())
            media_doc["bindings"].append({
                "binding_id": f"mb_{product_id}_derived",
                "claim_ids": [claims[0]["claim_id"]],
                "source_id": f"derived_{product_id}_turntable",
                "kind": "DERIVED_ASSET",
                "page": None,
                "start_seconds": None,
                "end_seconds": None,
                "rationale": "The provenance-backed turntable shows the fixture product.",
                "proposed_by": "agent",
                "approved_by": None,
            })
            media_path.write_text(json.dumps(media_doc), encoding="utf-8")
    vault.mkdir(exist_ok=True)
    (vault / "catalog.json").write_text(
        json.dumps({"products": catalog}), encoding="utf-8")
    return packs, vault


@contextmanager
def running_server(tmp_path, approve_media=False, yield_roots=False,
                   reviewer=None, feedback_path=None, include_derived=False):
    packs, vault = build_fixture(
        tmp_path, approve_media=approve_media,
        include_derived=include_derived)
    httpd = server.create_server(
        0, packs, vault, tmp_path / "page-cache", reviewer=reviewer,
        feedback_path=feedback_path)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{httpd.server_port}"
        yield (base_url, packs, vault) if yield_roots else base_url
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


@contextmanager
def serving_roots(packs, vault, tmp_path, reviewer=None, feedback_path=None):
    httpd = server.create_server(
        0, packs, vault, tmp_path / "restart-cache", reviewer=reviewer,
        feedback_path=feedback_path)
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


def post_json(base_url, path, payload):
    request = Request(
        f"{base_url}{path}", data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=2) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


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
            "q": "acme widget noise and weight", "preview": 1, "top": 20,
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


def test_procedure_discovery_applies_step_status_policy(tmp_path):
    with running_server(tmp_path) as base_url:
        _, default = get_json(base_url, "/api/procedures", {
            "product": "acme-widget-9000", "preview": 0,
        })
        _, preview = get_json(base_url, "/api/procedures", {
            "product": "acme-widget-9000", "preview": 1,
        })
    assert default["procedures"] == [{
        "name": "calibrate_widget",
        "step_count": 2,
        "served_step_count": 1,
        "fully_published": False,
        "publication_state": "partial",
    }]
    assert preview["procedures"][0]["served_step_count"] == 2
    assert not preview["procedures"][0]["fully_published"]
    assert preview["procedures"][0]["publication_state"] == "partial"


def test_procedure_steps_are_ordered_and_allow_no_page_fallback(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/procedure", {
            "product": "acme-widget-9000",
            "procedure": "calibrate_widget",
            "preview": 1,
        })
    assert [step["step_number"] for step in payload["steps"]] == [1, 2]
    assert [step["status"] for step in payload["steps"]] == [
        "PUBLISHED", "CANDIDATE",
    ]
    assert payload["steps"][0]["page_image_url"]
    assert payload["steps"][1]["page_image_url"] is None
    assert not payload["fully_published"]


def test_default_procedure_hides_candidate_and_unapproved_page(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/procedure", {
            "product": "acme-widget-9000",
            "procedure": "calibrate_widget",
            "preview": 0,
        })
    assert [step["status"] for step in payload["steps"]] == ["PUBLISHED"]
    assert payload["steps"][0]["page_image_url"] is None
    assert not payload["fully_published"]


def test_pdf_render_smoke_is_whole_page_at_144_dpi(tmp_path):
    digest = hashlib.sha256(FIXTURE_PDF.read_bytes()).hexdigest()
    rendered = server.render_pdf_page(
        FIXTURE_PDF, 1, tmp_path / "render-cache", digest)
    png = rendered.read_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", png[16:24]) == (600, 400)
    assert server.render_pdf_page(
        FIXTURE_PDF, 1, tmp_path / "render-cache", digest) == rendered


def test_page_image_route_is_preview_gated_and_path_safe(tmp_path):
    with running_server(tmp_path) as base_url:
        default_url = (
            f"{base_url}/page-image/acme-widget-9000/"
            "claim_prod_acme_calibrate_1.png?preview=0")
        try:
            urlopen(default_url, timeout=3)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("unapproved page image unexpectedly served")

        _, procedure = get_json(base_url, "/api/procedure", {
            "product": "acme-widget-9000",
            "procedure": "calibrate_widget",
            "preview": 1,
        })
        page_url = procedure["steps"][0]["page_image_url"]
        with urlopen(f"{base_url}{page_url}", timeout=5) as response:
            png = response.read()
            assert response.headers["Content-Type"] == "image/png"
            assert png[:8] == b"\x89PNG\r\n\x1a\n"

        try:
            urlopen(
                f"{base_url}/page-image/%2e%2e/claim.png?preview=1",
                timeout=3)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("page-image traversal unexpectedly succeeded")


def test_page_image_route_refuses_tampered_pdf(tmp_path):
    with running_server(tmp_path, yield_roots=True) as fixture:
        base_url, _, vault = fixture
        manual = vault / "acme-widget-9000" / "manuals" / "manual.pdf"
        manual.write_bytes(manual.read_bytes() + b"tampered")
        page_url = (
            f"{base_url}/page-image/acme-widget-9000/"
            "claim_prod_acme_calibrate_1.png?preview=1")
        try:
            urlopen(page_url, timeout=5)
        except HTTPError as error:
            assert error.code == 500
            assert json.loads(error.read())["error"] == "Media integrity check failed"
        else:
            raise AssertionError("tampered PDF unexpectedly rendered")


def test_default_serving_includes_labeled_candidates_mvp_exception(tmp_path):
    # Owner decision 2026-08-27 (MVP exception): with no preview param, the
    # API serves CANDIDATE facts so the demo answers before the review pass.
    # TODO: when the owner review pass promotes the catalog, revert the
    # server default to published-only and update this test.
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "acme widget noise and weight", "top": 20,
        })
    statuses = {row["claim_id"]: row["status"] for row in payload["results"]}
    assert statuses.get("claim_prod_acme_noise") == "CANDIDATE"
    assert "CANDIDATE" in statuses.values() and "PUBLISHED" in statuses.values()
    # The rejected claim (claims[2] in the fixture) must stay out even now.
    assert all(row["status"] != "REJECTED" for row in payload["results"])


def test_owner_review_api_appends_approve_and_reject_and_survives_restart(tmp_path):
    packs, vault = build_fixture(tmp_path)
    acme_reviews = packs / "acme-widget-9000" / "reviews.json"
    beta_reviews = packs / "beta-widget-2" / "reviews.json"
    acme_before = json.loads(acme_reviews.read_text())["reviews"]
    beta_before = json.loads(beta_reviews.read_text())["reviews"]

    with serving_roots(packs, vault, tmp_path,
                       reviewer="owner@example.com") as base_url:
        approve_status, approved = post_json(base_url, "/api/reviews", {
            "product": "acme-widget-9000",
            "claim_id": "claim_prod_acme_noise",
            "disposition": "APPROVED_FOR_PUBLISH",
            "rationale": "Owner verified the source beside the answer.",
        })
        reject_status, rejected = post_json(base_url, "/api/reviews", {
            "product": "beta-widget-2",
            "claim_id": "claim_prod_beta_noise",
            "disposition": "REJECTED_FOR_SERVING",
        })
        bulk_status, bulk = post_json(base_url, "/api/reviews", {
            "product": "acme-widget-9000",
            "claim_ids": ["claim_prod_acme_noise"],
            "disposition": "APPROVED_FOR_PUBLISH",
        })

    assert approve_status == reject_status == 201
    assert approved["status"] == "PUBLISHED"
    assert rejected["status"] == "REJECTED"
    assert bulk_status == 400
    assert "C2/C3" in bulk["error"]

    acme_after = json.loads(acme_reviews.read_text())["reviews"]
    beta_after = json.loads(beta_reviews.read_text())["reviews"]
    assert acme_after[:len(acme_before)] == acme_before
    assert beta_after[:len(beta_before)] == beta_before
    assert set(acme_after[-1]) == {
        "review_id", "date", "reviewer", "scope", "claim_id",
        "disposition", "rationale",
    }
    assert beta_after[-1]["rationale"] == "rejected via app review mode"

    with serving_roots(packs, vault, tmp_path) as base_url:
        _, acme = get_json(base_url, "/api/answer", {
            "q": "acme noise", "preview": 0, "top": 10,
        })
        _, beta = get_json(base_url, "/api/answer", {
            "q": "beta noise", "preview": 1, "top": 10,
        })
    assert any(row["claim_id"] == "claim_prod_acme_noise"
               and row["status"] == "PUBLISHED" for row in acme["results"])
    assert all(row["claim_id"] != "claim_prod_beta_noise"
               for row in beta["results"])


def test_review_write_refuses_to_run_without_reviewer_identity(tmp_path):
    with running_server(tmp_path) as base_url:
        config_status, config = get_json(base_url, "/api/review-config")
        status, payload = post_json(base_url, "/api/reviews", {
            "product": "acme-widget-9000",
            "claim_id": "claim_prod_acme_noise",
            "disposition": "APPROVED_FOR_PUBLISH",
        })
    assert config_status == 200 and not config["enabled"]
    assert status == 403
    assert "--reviewer" in payload["error"]


def test_single_step_answer_names_and_links_its_procedure(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "acme open panel", "preview": 1, "top": 10,
        })
    row = payload["results"][0]
    assert row["type"] == "STEP"
    assert row["procedure"] == "calibrate_widget"
    assert row["product_dir"] == "acme-widget-9000"
    assert row["display_text"].startswith("Step 1 of Calibrate widget:")


def test_video_has_poster_and_dropdown_marks_only_partial_procedures(tmp_path):
    with running_server(tmp_path) as base_url:
        _, answer_payload = get_json(base_url, "/api/answer", {
            "q": "acme weight", "preview": 1, "top": 10,
        })
        _, procedures = get_json(base_url, "/api/procedures", {
            "product": "acme-widget-9000", "preview": 1,
        })
    media = answer_payload["results"][0]["media"]
    image = next(item for item in media if item["kind"] == "IMAGE")
    video = next(item for item in media if item["kind"] == "VIDEO_FILE")
    assert video["poster_url"] == image["url"]
    assert procedures["procedures"][0]["publication_state"] == "partial"


def test_zero_result_returns_matching_recorded_gap(tmp_path):
    with running_server(tmp_path) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "Does the Acme widget support warp drive?", "preview": 1,
        })
    assert payload["results"] == []
    assert payload["gap"]["gap_id"] == "gap_prod_acme_warp_drive"
    assert "source is missing" in payload["gap"]["reason"]


def test_pending_derived_asset_serves_labeled_with_watermark_and_provenance(tmp_path):
    with running_server(tmp_path, include_derived=True) as base_url:
        _, payload = get_json(base_url, "/api/answer", {
            "q": "acme weight", "preview": 1, "top": 10,
        })
        derived = next(item for item in payload["results"][0]["media"]
                       if item["kind"] == "DERIVED_ASSET")
        with urlopen(f"{base_url}{derived['url']}", timeout=2) as response:
            body = response.read()
    assert derived["awaiting_approval"]
    assert derived["label"] == "Acme Widget 9000 turntable"
    assert derived["watermark"].startswith("INTERNAL ONLY")
    assert derived["provenance"] == "local deterministic fixture"
    assert body == b"GIF89a derived fixture"


def test_feedback_endpoint_accumulates_reports_and_misses(tmp_path):
    feedback_path = tmp_path / "feedback.jsonl"
    with running_server(tmp_path, feedback_path=feedback_path) as base_url:
        report_status, _ = post_json(base_url, "/api/feedback", {
            "question": "How heavy is the Acme widget?",
            "product": "acme-widget-9000",
            "claim_id": "claim_prod_acme_weight",
            "note": "The unit looks wrong.",
        })
        miss_status, _ = post_json(base_url, "/api/feedback", {
            "question": "Does it support warp drive?",
            "claim_id": None,
        })
    records = [json.loads(line) for line in feedback_path.read_text().splitlines()]
    assert report_status == miss_status == 201
    assert [record["claim_id"] for record in records] == [
        "claim_prod_acme_weight", None,
    ]
    assert all(record["timestamp"].endswith("Z") for record in records)


def test_tied_category_requires_clarification_but_named_product_does_not(tmp_path):
    with running_server(tmp_path) as base_url:
        _, tied = get_json(base_url, "/api/answer", {
            "q": "How heavy is the widget?", "preview": 1,
        })
        _, named = get_json(base_url, "/api/answer", {
            "q": "How heavy is the Acme widget?", "preview": 1,
        })
    assert tied["mode"] == "clarify"
    assert len(tied["clarify"]["candidates"]) == 2
    assert tied["results"] == []
    assert named["mode"] == "answer"
    assert {row["product_dir"] for row in named["results"]} == {
        "acme-widget-9000",
    }
