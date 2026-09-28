import json
import os
import hashlib
from pathlib import Path
import urllib.request

# Multi-image composition endpoint details:
# Endpoint ID: fal-ai/nano-banana-pro/edit
# Input schema:
#   - prompt: string
#   - image_urls: list of strings (URLs to reference images)


def synthesize_and_verify_state(state, procedure, packs_root, product_dir, fal_client, upload_cache=None):
    from system.image_retrieval import evidence_images
    from app.keyframe_video import parse_verdict, VLM_ENDPOINT, DEFAULT_VLM_MODEL
    
    repo_root = Path(packs_root).parent
    vault_root = repo_root / "source-vault"
    assets_root = repo_root / "generated-assets"
    
    state_id = state["state_id"]
    output_path = assets_root / product_dir / "keyframes" / f"{procedure}-{state_id}.png"
    prov_path = output_path.with_name(f"{output_path.name}.provenance.json")
    
    if output_path.is_file():
        valid_cache = False
        if prov_path.is_file():
            try:
                import re
                with open(prov_path, "r", encoding="utf-8") as f:
                    prov_data = json.load(f)
                v = prov_data.get("verdict", {})
                req_id = prov_data.get("request_id")
                
                if isinstance(v, dict) and v.get("verdict") == "pass":
                    if isinstance(req_id, str) and req_id.strip():
                        if not re.search(r"(?i)mock|fake|test|dummy", req_id):
                            valid_cache = True
            except Exception:
                pass
        
        if valid_cache:
            return output_path
        else:
            output_path.unlink()
            if prov_path.is_file():
                prov_path.unlink()
    claim_ids = state.get("claim_ids", [])
    # Reference photos may come from other claims than the ones this state
    # must satisfy (e.g. a "before" state edited from the "after" photo).
    ev_images = evidence_images(packs_root, vault_root, product_dir,
                                state.get("reference_claim_ids", claim_ids))
    
    assertions = []
    try:
        with open(Path(packs_root) / product_dir / "claims.json", "r", encoding="utf-8") as f:
            all_claims = json.load(f)
            for c in all_claims:
                if c.get("claim_id") in claim_ids:
                    for sb in c.get("source_bindings", []):
                        q = sb.get("quote")
                        if q:
                            assertions.append(q)
    except Exception:
        pass
        
    if upload_cache is None:
        upload_cache = {}
        
    def upload(path):
        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if digest not in upload_cache:
            upload_cache[digest] = fal_client.upload_file(str(path))
        return upload_cache[digest]
        
    # Get endpoints and models from env
    compose_endpoint = os.environ.get("SHOWME_IMAGE_COMPOSE_MODEL", "fal-ai/nano-banana-pro/edit")
    vlm_model = os.environ.get("SHOWME_VIDEO_VLM_MODEL", DEFAULT_VLM_MODEL)
    
    # Base prompt
    prompt = f"Product demonstration. State description: {state.get('description', '')}. no other objects, no text, no logo changes, keep both products exactly as in the reference images."
    if state.get("edit_prompt"):
        # An explicit photo edit (e.g. undo an action) replaces the keep-as-is prompt.
        prompt = state["edit_prompt"]
        # Edit one real photo; rendered manual pages (page-*.png) are line drawings.
        photos = [ev for ev in ev_images
                  if not Path(str(ev.get("local_path", ""))).name.startswith("page-")]
        ev_images = photos[:1] or ev_images[:1]

    image_urls = []
    source_ids = []
    for ev in ev_images[:4]:  # max 4 images
        image_urls.append(upload(ev["local_path"]))
        source_ids.append(ev["source_id"])
        
    # If no evidence images and no claims, this is tricky. The spec says 2-4 retrieved evidence images.
    # We should get a default image for the product.
    if not image_urls:
        try:
            with open(vault_root / product_dir / "manifest.json", "r", encoding="utf-8") as f:
                manifest = json.load(f)
                for src in manifest.get("sources", []):
                    if src.get("type") == "IMAGE" and src.get("local_path"):
                        local_p = (vault_root / product_dir / src["local_path"]).resolve()
                        if local_p.is_file():
                            image_urls.append(upload(str(local_p)))
                            source_ids.append(src["source_id"])
                            break
        except Exception:
            pass

    def attempt(prompt_addition=""):
        args = {
            "prompt": prompt + prompt_addition,
            "image_urls": image_urls,
        }
        handle = fal_client.submit(compose_endpoint, arguments=args)
        req_id = getattr(handle, "request_id", None)
        result = handle.get()
        # Seedream typically returns "images" or "image"
        images = result.get("images", [])
        if not images:
            img_obj = result.get("image")
            if img_obj:
                images = [img_obj]
        if not images or not images[0].get("url"):
            raise RuntimeError(f"Composition failed to return an image URL for state {state_id}")
            
        gen_url = images[0]["url"]
        
        # Download temporarily to verify
        import tempfile
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.close()
        
        with urllib.request.urlopen(gen_url, timeout=300) as response, open(tmp.name, "wb") as handle2:
            for chunk in iter(lambda: response.read(1024 * 1024), b""):
                handle2.write(chunk)
                
        # Verification (D4)
        verify_prompt = f"""\
You are a strict verifier for AI-generated product demonstration images.
We generated this candidate image from the provided evidence images.
State description: {state.get('description', '')}
"""
        if assertions:
            verify_prompt += "\nCheck these ground-truth assertions derived from the documentation:\n"
            for i, a in enumerate(assertions, 1):
                verify_prompt += f"{i}. {a}\n"
                
        verify_prompt += """
Answer in JSON only, with these keys:
{
  "same_product": {"answer": "yes|no|unsure", "evidence": "..."},
  "state_matches": {"answer": "yes|no|unsure", "evidence": "..."},
  "invented_or_vanishing_parts": {"answer": "yes|no|unsure", "evidence": "..."}"""

        if assertions:
            verify_prompt += """,
  "assertion_checks": [
    {"assertion": "...", "answer": "yes|no|unsure", "evidence": "..."}
  ]"""

        verify_prompt += """,
  "verdict": "pass|fail",
  "verdict_reason": "..."
}
"""
        verify_args = {
            "model": vlm_model,
            "prompt": verify_prompt,
            "image_urls": image_urls + [upload(tmp.name)],
            "temperature": 0,
            "max_tokens": 2000,
        }
        
        v_handle = fal_client.submit(VLM_ENDPOINT, arguments=verify_args)
        verdict = parse_verdict(v_handle.get())
        
        if "assertion_checks" in verdict:
            for chk in verdict["assertion_checks"]:
                if str(chk.get("answer")).lower() != "yes":
                    verdict["verdict"] = "fail"
                    verdict["verdict_reason"] = f"Assertion failed: {chk.get('assertion')} - {chk.get('evidence')}"
                    break
        
        return tmp.name, verdict, req_id
        
    tmp_path, verdict, req_id = attempt()
    if verdict.get("verdict") != "pass":
        # Retry once
        reason = verdict.get("verdict_reason", "failed verification")
        os.unlink(tmp_path)
        tmp_path, verdict, req_id = attempt(prompt_addition=f" MUST AVOID: {reason}")
        if verdict.get("verdict") != "pass":
            os.unlink(tmp_path)
            raise RuntimeError(f"State {state_id} failed verification twice: {verdict.get('verdict_reason')}")
            
    # Move tmp_path to output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(tmp_path, str(output_path))
    
    # Write provenance
    provenance = {
        "composed_from": source_ids,
        "model": compose_endpoint,
        "request_id": req_id,
        "verdict": verdict
    }
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump(provenance, f, ensure_ascii=False, indent=2)
        
    return output_path

def resolve_state(state, procedure, packs_root, product_dir, fal_client, upload_cache):
    from system.image_retrieval import evidence_images
    
    # Keyframe sources in preference order (D2)
    # 1. curated_path
    if "curated_path" in state:
        return Path(packs_root).parent / state["curated_path"]
        
    # 2. evidence_source_id
    if "evidence_source_id" in state:
        source_id = state["evidence_source_id"]
        vault_dir = Path(packs_root).parent / "source-vault" / product_dir
        manifest_path = vault_dir / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for src in manifest.get("sources", []):
            if src.get("source_id") == source_id:
                local_path = src.get("local_path")
                if local_path:
                    keyframe_path = (vault_dir / local_path).resolve()
                    prov_path = (Path(packs_root).parent / "generated-assets" / product_dir / "keyframes" / f"{procedure}-{state['state_id']}.png.provenance.json")
                    prov_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(prov_path, "w", encoding="utf-8") as f:
                        json.dump({"retrieved_from": source_id}, f, ensure_ascii=False, indent=2)
                    return keyframe_path

    # 3. manual_page
    if "manual_page" in state:
        vault_dir = Path(packs_root).parent / "source-vault" / product_dir
        manifest_path = vault_dir / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for src in manifest.get("sources", []):
            if src.get("type") in ("MANUAL_PDF", "GUIDE", "SPEC_DOC_PDF"):
                local_path = src.get("local_path")
                if local_path:
                    pdf_path = (vault_dir / local_path).resolve()
                    cache_root = Path(packs_root).parent / "app" / "cache" / "pdf-figures"
                    try:
                        from app.server import render_pdf_page
                    except ImportError:
                        import sys
                        sys.path.insert(0, str(Path(packs_root).parent))
                        from app.server import render_pdf_page
                    rendered_path = render_pdf_page(
                        pdf_path=pdf_path,
                        page_number=state["manual_page"],
                        cache_root=cache_root,
                        expected_hash=src.get("sha256")
                    )
                    prov_path = (Path(packs_root).parent / "generated-assets" / product_dir / "keyframes" / f"{procedure}-{state['state_id']}.png.provenance.json")
                    prov_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(prov_path, "w", encoding="utf-8") as f:
                        json.dump({"retrieved_from_pdf": src.get("source_id"), "page": state["manual_page"]}, f, ensure_ascii=False, indent=2)
                    return rendered_path
                    
    # 4. Synthesis
    return synthesize_and_verify_state(state, procedure, packs_root, product_dir, fal_client, upload_cache)
