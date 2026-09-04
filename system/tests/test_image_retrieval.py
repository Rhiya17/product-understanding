import json
from pathlib import Path
from system.image_retrieval import evidence_images

def test_image_retrieval_handles_missing_manifest(tmp_path):
    packs = tmp_path / "packs"
    vault = tmp_path / "vault"
    product_dir = "acme"
    
    pack_dir = packs / product_dir
    pack_dir.mkdir(parents=True)
    (pack_dir / "claims.json").write_text(json.dumps([{"claim_id": "c1"}]), encoding="utf-8")
    
    # Missing manifest and media bindings but should not crash
    assert evidence_images(packs, vault, product_dir, ["c1"]) == []

def test_image_retrieval_pdf_figure_rendering(tmp_path, monkeypatch):
    packs = tmp_path / "packs"
    vault = tmp_path / "vault"
    product_dir = "acme"
    
    pack_dir = packs / product_dir
    vault_dir = vault / product_dir
    pack_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    
    (pack_dir / "claims.json").write_text(json.dumps([
        {"claim_id": "c1", "source_bindings": [{"source_id": "s1", "page": 42}]}
    ]), encoding="utf-8")
    
    (vault_dir / "manifest.json").write_text(json.dumps({
        "sources": [{"source_id": "s1", "type": "MANUAL_PDF", "local_path": "manual.pdf", "sha256": "abcdef"}]
    }), encoding="utf-8")
    
    import app.server
    def mock_render(pdf_path, page_number, cache_root, expected_hash):
        return Path(cache_root) / f"rendered_{page_number}.png"
        
    monkeypatch.setattr(app.server, "render_pdf_page", mock_render)
    
    res = evidence_images(packs, vault, product_dir, ["c1"])
    assert len(res) == 1
    assert res[0]["kind"] == "PDF_FIGURE"
    assert res[0]["page"] == 42
    assert "rendered_42.png" in res[0]["local_path"]

def test_image_retrieval_bound_image(tmp_path):
    packs = tmp_path / "packs"
    vault = tmp_path / "vault"
    product_dir = "acme"
    
    pack_dir = packs / product_dir
    vault_dir = vault / product_dir
    pack_dir.mkdir(parents=True)
    vault_dir.mkdir(parents=True)
    
    (pack_dir / "media-bindings.json").write_text(json.dumps({
        "bindings": [{"claim_ids": ["c1"], "kind": "IMAGE", "source_id": "img1"}]
    }), encoding="utf-8")
    
    (vault_dir / "manifest.json").write_text(json.dumps({
        "sources": [{"source_id": "img1", "local_path": "img.png"}]
    }), encoding="utf-8")
    
    res = evidence_images(packs, vault, product_dir, ["c1"])
    assert len(res) == 1
    assert res[0]["kind"] == "IMAGE"
    assert "img.png" in res[0]["local_path"]
