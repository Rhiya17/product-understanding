import hashlib
import importlib.util
import json
from pathlib import Path


VALIDATOR_PATH = (Path(__file__).resolve().parents[2]
                  / "evidence-packs" / "validate_media.py")
SPEC = importlib.util.spec_from_file_location("validate_media", VALIDATOR_PATH)
validate_media = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_media)


def binding(binding_id, claim_ids, source_id, kind, page=None,
            start=None, end=None, approved_by=None):
    return {
        "binding_id": binding_id,
        "claim_ids": claim_ids,
        "source_id": source_id,
        "kind": kind,
        "page": page,
        "start_seconds": start,
        "end_seconds": end,
        "rationale": "This registered fixture asset directly supports the bound claim.",
        "proposed_by": "agent",
        "approved_by": approved_by,
    }


def build_media_fixture(tmp_path):
    packs_root = tmp_path / "packs"
    vault_root = tmp_path / "vault"
    product = "acme-widget"
    pack = packs_root / product
    vault = vault_root / product
    (vault / "images").mkdir(parents=True)
    (vault / "videos").mkdir()
    (vault / "manuals").mkdir()
    pack.mkdir(parents=True)

    image = b"image bytes"
    video = b"video bytes"
    pdf = b"%PDF-1.4 fixture"
    (vault / "images" / "widget.png").write_bytes(image)
    (vault / "videos" / "widget.mp4").write_bytes(video)
    (vault / "manuals" / "widget.pdf").write_bytes(pdf)
    claims = [{"claim_id": "claim_widget_one"},
              {"claim_id": "claim_widget_two"}]
    (pack / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    (vault / "manifest.json").write_text(json.dumps({
        "identity": {"brand": "Acme", "model": "Widget"},
        "sources": [{
            "source_id": "src_image",
            "type": "IMAGE",
            "local_path": "images/widget.png",
            "sha256": hashlib.sha256(image).hexdigest(),
            "authority": "MANUFACTURER",
        }, {
            "source_id": "src_video_url",
            "type": "VIDEO_URL",
            "origin_url": "https://example.com/widget-video",
            "authority": "MANUFACTURER",
        }, {
            "source_id": "src_video_file",
            "type": "VIDEO",
            "local_path": "videos/widget.mp4",
            "sha256": hashlib.sha256(video).hexdigest(),
            "authority": "MANUFACTURER",
            "rights_note": "Manufacturer copyright; internal research use.",
        }, {
            "source_id": "src_manual",
            "type": "MANUAL_PDF",
            "local_path": "manuals/widget.pdf",
            "sha256": hashlib.sha256(pdf).hexdigest(),
            "authority": "MANUFACTURER",
        }],
    }), encoding="utf-8")
    (vault_root / "catalog.json").write_text(json.dumps({
        "products": [{"dir": product}],
    }), encoding="utf-8")
    document = {"bindings": [
        binding("mb_widget_image", ["claim_widget_one"],
                "src_image", "IMAGE"),
        binding("mb_widget_video_url", ["claim_widget_one"],
                "src_video_url", "VIDEO_URL", start=3, end=9),
        binding("mb_widget_video_file", ["claim_widget_two"],
                "src_video_file", "VIDEO_FILE"),
        binding("mb_widget_manual_page", ["claim_widget_two"],
                "src_manual", "PDF_PAGE", page=1),
    ]}
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
    return packs_root, vault_root, pack, vault, document


def test_valid_media_document_and_owner_email_pass(tmp_path):
    packs_root, vault_root, pack, vault, document = build_media_fixture(tmp_path)
    document["bindings"][0]["approved_by"] = "owner@example.com"
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
    assert validate_media.validate_pack(pack, vault) == []
    assert validate_media.validate_all(packs_root, vault_root) == (True, [], 4)


def test_unknown_claim_source_and_invalid_approval_fail(tmp_path):
    _, _, pack, vault, document = build_media_fixture(tmp_path)
    item = document["bindings"][0]
    item["claim_ids"] = ["claim_missing"]
    item["source_id"] = "src_missing"
    item["approved_by"] = "agent"
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
    errors = validate_media.validate_pack(pack, vault)
    assert any("unknown claim_id" in error for error in errors)
    assert any("unknown source_id" in error for error in errors)
    assert any("owner email" in error for error in errors)


def test_pdf_page_and_video_times_are_strict(tmp_path):
    _, _, pack, vault, document = build_media_fixture(tmp_path)
    document["bindings"][3]["page"] = 0
    document["bindings"][1]["start_seconds"] = True
    document["bindings"][1]["end_seconds"] = 0
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
    errors = validate_media.validate_pack(pack, vault)
    assert any("positive 1-based page" in error for error in errors)
    assert any("start_seconds" in error for error in errors)


def test_video_file_requires_manufacturer_authority_rights_and_hash(tmp_path):
    _, _, pack, vault, _ = build_media_fixture(tmp_path)
    manifest_path = vault / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    source = next(item for item in manifest["sources"]
                  if item["source_id"] == "src_video_file")
    source["authority"] = "UNKNOWN"
    source["rights_note"] = ""
    source["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    errors = validate_media.validate_pack(pack, vault)
    assert any("authority must be MANUFACTURER" in error for error in errors)
    assert any("requires a rights_note" in error for error in errors)
    assert any("SHA-256 does not match" in error for error in errors)


def test_every_catalog_product_requires_a_binding_file(tmp_path):
    packs_root, vault_root, pack, _, _ = build_media_fixture(tmp_path)
    (pack / "media-bindings.json").unlink()
    success, errors, count = validate_media.validate_all(packs_root, vault_root)
    assert not success
    assert count == 0
    assert errors == ["acme-widget: missing media-bindings.json"]


def test_derived_asset_lane_requires_provenance_watermark_and_matching_hash(tmp_path):
    _, _, pack, vault, document = build_media_fixture(tmp_path)
    derived_bytes = b"GIF89a derived turntable"
    derived_file = tmp_path / "derived" / "widget-turntable.gif"
    derived_file.parent.mkdir()
    derived_file.write_bytes(derived_bytes)
    asset = {
        "asset_id": "derived_widget_turntable",
        "type": "TURNTABLE_GIF",
        "label": "Photo-projected widget turntable",
        "watermark": "INTERNAL ONLY — NOT FOR DISTRIBUTION",
        "local_path": "derived/widget-turntable.gif",
        "sha256": hashlib.sha256(derived_bytes).hexdigest(),
        "provider": "local deterministic fixture",
        "approved_by": None,
        "internal_only": True,
    }
    (pack / "derived-assets.json").write_text(json.dumps({
        "schema_version": 1, "product_id": "widget",
        "assets": [asset],
    }), encoding="utf-8")
    document["bindings"].append(binding(
        "mb_widget_derived", ["claim_widget_one"],
        "derived_widget_turntable", "DERIVED_ASSET"))
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
    assert validate_media.validate_pack(pack, vault) == []

    asset["watermark"] = ""
    (pack / "derived-assets.json").write_text(json.dumps({
        "schema_version": 1, "product_id": "widget",
        "assets": [asset],
    }), encoding="utf-8")
    errors = validate_media.validate_pack(pack, vault)
    assert any("INTERNAL ONLY watermark" in error for error in errors)


def test_derived_asset_mock_tripwires(tmp_path):
    _, _, pack, vault, document = build_media_fixture(tmp_path)
    derived_bytes = b"mock derived"
    derived_file = tmp_path / "derived" / "widget-mock.mp4"
    derived_file.parent.mkdir()
    derived_file.write_bytes(derived_bytes)
    
    # Missing verification_local_path file
    asset = {
        "asset_id": "derived_widget_mock",
        "type": "PROCEDURE_VIDEO_MP4",
        "label": "Mock generated widget",
        "watermark": "INTERNAL ONLY — MOCK",
        "local_path": "derived/widget-mock.mp4",
        "sha256": hashlib.sha256(derived_bytes).hexdigest(),
        "provider": "mock generator",
        "approved_by": None,
        "internal_only": True,
        "request_id": "mock_req_123",
        "verification_local_path": "derived/does-not-exist.json"
    }
    
    (pack / "derived-assets.json").write_text(json.dumps({
        "schema_version": 1, "product_id": "widget",
        "assets": [asset],
    }), encoding="utf-8")
    document["bindings"].append(binding(
        "mb_widget_derived_mock", ["claim_widget_one"],
        "derived_widget_mock", "DERIVED_ASSET"))
    (pack / "media-bindings.json").write_text(
        json.dumps(document), encoding="utf-8")
        
    errors = validate_media.validate_pack(pack, vault)
    assert any("request_id matches mock pattern" in error for error in errors)
    assert any("verification_local_path does not exist" in error for error in errors)
