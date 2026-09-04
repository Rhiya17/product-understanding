import json
import os
from pathlib import Path

def evidence_images(packs_root, vault_root, product_dir, claim_ids):
    packs_root = Path(packs_root)
    vault_root = Path(vault_root)
    product_dir = str(product_dir)
    claim_ids = set(claim_ids)
    
    pack_dir = packs_root / product_dir
    vault_dir = vault_root / product_dir
    
    try:
        with open(pack_dir / "claims.json", "r", encoding="utf-8") as f:
            claims = json.load(f)
    except (OSError, json.JSONDecodeError):
        claims = []
        
    try:
        with open(pack_dir / "media-bindings.json", "r", encoding="utf-8") as f:
            media_bindings = json.load(f).get("bindings", [])
    except (OSError, json.JSONDecodeError):
        media_bindings = []
        
    try:
        with open(vault_dir / "manifest.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
            sources = {s["source_id"]: s for s in manifest.get("sources", [])}
    except (OSError, json.JSONDecodeError):
        sources = {}

    results = []

    # 1. Images from media-bindings.json
    for binding in media_bindings:
        if not isinstance(binding, dict):
            continue
        if binding.get("kind") != "IMAGE":
            continue
        binding_claims = set(binding.get("claim_ids", []))
        overlap = binding_claims & claim_ids
        if not overlap:
            continue
            
        source_id = binding.get("source_id")
        source = sources.get(source_id, {})
        local_path = source.get("local_path")
        if not local_path:
            continue
            
        abs_local_path = (vault_dir / local_path).resolve()
        
        for claim_id in overlap:
            results.append({
                "claim_id": claim_id,
                "source_id": source_id,
                "local_path": str(abs_local_path),
                "origin_url": source.get("origin_url"),
                "kind": "IMAGE",
                "page": None
            })

    # 2. PDF figures from claim source_bindings
    # We need to render the PDF page using app.server.render_pdf_page
    try:
        from app.server import render_pdf_page
    except ImportError:
        import sys
        sys.path.insert(0, str(packs_root.parent))
        from app.server import render_pdf_page

    cache_root = packs_root.parent / "app" / "cache" / "pdf-figures"
    cache_root.mkdir(parents=True, exist_ok=True)
    
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claim_id")
        if claim_id not in claim_ids:
            continue
            
        for s_binding in claim.get("source_bindings", []):
            if not isinstance(s_binding, dict):
                continue
            source_id = s_binding.get("source_id")
            page = s_binding.get("page")
            if page is None:
                continue
                
            source = sources.get(source_id, {})
            if source.get("type") not in ("MANUAL_PDF", "GUIDE", "SPEC_DOC_PDF"):
                continue
                
            local_path = source.get("local_path")
            if not local_path:
                continue
                
            abs_pdf_path = (vault_dir / local_path).resolve()
            expected_hash = source.get("sha256")
            
            try:
                rendered_path = render_pdf_page(
                    pdf_path=abs_pdf_path,
                    page_number=page,
                    cache_root=cache_root,
                    expected_hash=expected_hash
                )
                results.append({
                    "claim_id": claim_id,
                    "source_id": source_id,
                    "local_path": str(rendered_path),
                    "origin_url": source.get("origin_url"),
                    "kind": "PDF_FIGURE",
                    "page": page
                })
            except Exception as e:
                import sys
                sys.stderr.write(f"Failed to render PDF page {page} for {source_id}: {e}\n")

    return results
