import json
from pathlib import Path
from app.server import render_pdf_page, DEFAULT_CACHE_ROOT

def evidence_images(packs_root, vault_root, product_dir, claim_ids, cache_root=DEFAULT_CACHE_ROOT):
    packs_root = Path(packs_root)
    vault_root = Path(vault_root)
    product_dir = str(product_dir)
    claim_ids = set(claim_ids)
    
    # Load media bindings
    media_path = packs_root / product_dir / "media-bindings.json"
    try:
        with open(media_path) as f:
            media_bindings = json.load(f).get("bindings", [])
    except (FileNotFoundError, json.JSONDecodeError):
        media_bindings = []

    # Load vault manifest
    manifest_path = vault_root / product_dir / "manifest.json"
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
            sources = {s.get("source_id"): s for s in manifest.get("sources", [])}
    except (FileNotFoundError, json.JSONDecodeError):
        sources = {}

    results = []
    
    for binding in media_bindings:
        # Check if binding applies to any of our claim_ids
        bound_claims = set(binding.get("claim_ids", []))
        overlap = bound_claims & claim_ids
        if not overlap:
            continue
            
        source_id = binding.get("source_id")
        source = sources.get(source_id)
        if not source:
            continue
            
        kind = binding.get("kind")
        if kind not in ("IMAGE", "PDF_PAGE"):
            continue
            
        origin_url = source.get("origin_url")
        local_path = None
        page = None
        
        if kind == "IMAGE":
            # Direct image file
            rel_path = source.get("local_path")
            if rel_path:
                local_path = str(vault_root / product_dir / rel_path)
            out_kind = "IMAGE"
        elif kind == "PDF_PAGE":
            # Need to render the page
            rel_path = source.get("local_path")
            page = binding.get("page")
            expected_hash = source.get("sha256")
            if rel_path and page and expected_hash:
                pdf_path = vault_root / product_dir / rel_path
                rendered_path = render_pdf_page(pdf_path, page, cache_root, expected_hash)
                local_path = str(rendered_path)
            out_kind = "PDF_FIGURE"
        else:
            continue
            
        if not local_path:
            continue
            
        for c_id in overlap:
            results.append({
                "claim_id": c_id,
                "source_id": source_id,
                "local_path": local_path,
                "origin_url": origin_url,
                "kind": out_kind,
                "page": page
            })
            
    return results
