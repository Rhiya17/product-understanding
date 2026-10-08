#!/usr/bin/env python3
"""Local HTTP server for published product answers."""

import argparse
import datetime
import hashlib
import json
import mimetypes
import os
import re
import sys
import tempfile
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = APP_ROOT / "static"
DEFAULT_CACHE_ROOT = APP_ROOT / "cache"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from system import answer  # noqa: E402
from system.answer_engine import AnswerEngine  # noqa: E402
from system.luna_planner import (  # noqa: E402
    LunaPlanner,
    apply_presentation,
    deterministic_presentation,
    media_modality,
)
from app.video_jobs import VideoJobManager  # noqa: E402
from app import dev_media  # noqa: E402
from app.pipeline import service as video_service  # noqa: E402
from app.pipeline.store import Store as VideoStore  # noqa: E402


_HASH_CACHE = {}
_HASH_CACHE_LOCK = threading.Lock()
_PAGE_RENDER_LOCK = threading.Lock()
_REVIEW_WRITE_LOCKS = {}
_REVIEW_WRITE_LOCKS_LOCK = threading.Lock()
_FEEDBACK_WRITE_LOCK = threading.Lock()
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_REVIEW_DISPOSITIONS = {
    "APPROVED_FOR_PUBLISH",
    "REJECTED_FOR_SERVING",
    "NEEDS_REWORK",
}


class MediaIntegrityError(RuntimeError):
    """Raised when a registered source no longer matches its manifest hash."""


def _catalog_products(vault_root):
    """Return the public subset of product catalog fields."""
    return [{
        "id": product.get("product_id"),
        "dir": product.get("dir"),
        "brand": product.get("brand"),
        "model": product.get("model"),
        "category": product.get("category"),
    } for product in answer.load_catalog(vault_root)]


def _verified_hash(path, expected_hash):
    """Verify a file against its manifest hash, caching unchanged files."""
    path = Path(path)
    stat = path.stat()
    cache_key = (str(path.resolve()), expected_hash)
    fingerprint = (stat.st_mtime_ns, stat.st_size)
    with _HASH_CACHE_LOCK:
        cached = _HASH_CACHE.get(cache_key)
    if cached and cached[:2] == fingerprint:
        return cached[2]

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    matches = digest.hexdigest() == expected_hash
    with _HASH_CACHE_LOCK:
        _HASH_CACHE[cache_key] = (*fingerprint, matches)
    return matches


def _media_url(product_dir, local_path):
    product = quote(product_dir, safe="")
    relative = quote(Path(local_path).as_posix(), safe="/")
    return f"/media/{product}/{relative}"


def _derived_media_url(product_dir, asset_id, pending=False, poster=False):
    url = "/derived-media/{}/{}".format(
        quote(product_dir, safe=""), quote(asset_id, safe=""))
    query = []
    if pending:
        query.append("preview=1")
    if poster:
        query.append("poster=1")
    return f"{url}?{'&'.join(query)}" if query else url


def _derived_assets(packs_root, product_dir):
    document = answer.load_json(
        Path(packs_root) / product_dir / "derived-assets.json", {})
    return {asset.get("asset_id"): asset
            for asset in document.get("assets", [])
            if isinstance(asset, dict) and asset.get("asset_id")}


def _media_index(packs_root, vault_root, preview):
    """Index approved (or explicitly previewed) bindings by claim id."""
    index = {}
    for product in answer.load_catalog(vault_root):
        product_dir = product.get("dir")
        manifest = answer.load_json(
            vault_root / product_dir / "manifest.json", {})
        sources = {source.get("source_id"): source
                   for source in manifest.get("sources", [])}
        media_doc = answer.load_json(
            packs_root / product_dir / "media-bindings.json", {})
        derived_assets = _derived_assets(packs_root, product_dir)
        for binding in media_doc.get("bindings", []):
            kind = binding.get("kind")
            asset = (derived_assets.get(binding.get("source_id"))
                     if kind == "DERIVED_ASSET" else None)
            approved = bool(binding.get("approved_by") or
                            (asset or {}).get("approved_by"))
            if not approved and not preview:
                continue
            source = sources.get(binding.get("source_id"), {})
            if kind == "DERIVED_ASSET":
                if asset is None:
                    continue
                media_url = _derived_media_url(
                    product_dir, asset.get("asset_id"), pending=not approved)
            elif kind == "VIDEO_URL":
                media_url = source.get("origin_url")
            else:
                local_path = source.get("local_path")
                media_url = (_media_url(product_dir, local_path)
                             if local_path else None)
            media = {
                "id": binding.get("binding_id"),
                "kind": kind,
                "url": media_url,
                "asset_type": (asset or {}).get("type"),
                "page": binding.get("page"),
                "start_seconds": binding.get("start_seconds"),
                "end_seconds": binding.get("end_seconds"),
                "rationale": binding.get("rationale"),
                "awaiting_approval": not approved,
                "rights_note": (source.get("rights_note")
                                if kind == "VIDEO_FILE" else
                                (asset or {}).get("rights_note")),
                "label": (asset or {}).get("label"),
                "provenance": (asset or {}).get("provider"),
                "watermark": (asset or {}).get("watermark"),
            }
            if kind == "DERIVED_ASSET" and (asset or {}).get(
                    "poster_local_path"):
                media["poster_url"] = _derived_media_url(
                    product_dir, asset.get("asset_id"),
                    pending=not approved, poster=True)
            for claim_id in binding.get("claim_ids", []):
                index.setdefault(claim_id, []).append(media)
    for media_items in index.values():
        poster_url = next((item.get("url") for item in media_items
                           if item.get("kind") == "IMAGE" and item.get("url")),
                          None)
        if poster_url:
            for item in media_items:
                if item.get("kind") == "VIDEO_FILE":
                    item["poster_url"] = poster_url
    return index


def _review_lock(path):
    key = str(Path(path).resolve())
    with _REVIEW_WRITE_LOCKS_LOCK:
        return _REVIEW_WRITE_LOCKS.setdefault(key, threading.Lock())


def append_review(pack_dir, reviewer, claim, disposition, rationale=None):
    """Atomically append one human decision without changing older records."""
    if not isinstance(reviewer, str) or not _EMAIL_RE.fullmatch(reviewer):
        raise ValueError("A valid reviewer email is required")
    if disposition not in _REVIEW_DISPOSITIONS:
        raise ValueError("Invalid review disposition")
    claim_id = claim.get("claim_id")
    defaults = {
        "APPROVED_FOR_PUBLISH": "approved via app review mode",
        "REJECTED_FOR_SERVING": "rejected via app review mode",
        "NEEDS_REWORK": "marked for rework via app review mode",
    }
    rationale = str(rationale or "").strip() or defaults[disposition]
    if len(rationale) > 2000:
        raise ValueError("rationale must be at most 2000 characters")
    now = datetime.datetime.now(datetime.timezone.utc)
    safe_claim = re.sub(r"[^a-z0-9]+", "_", str(claim_id).lower()).strip("_")
    record = {
        "review_id": (f"rev_app_{safe_claim}_{now.strftime('%Y%m%d%H%M%S%f')}"
                      f"_{uuid.uuid4().hex[:8]}"),
        "date": now.date().isoformat(),
        "reviewer": reviewer,
        "scope": f"app_review:{claim_id}",
        "claim_id": claim_id,
        "disposition": disposition,
        "rationale": rationale,
    }
    reviews_path = Path(pack_dir) / "reviews.json"
    reviews_path.parent.mkdir(parents=True, exist_ok=True)
    with _review_lock(reviews_path):
        document = answer.load_json(reviews_path, {"reviews": []})
        if (not isinstance(document, dict)
                or not isinstance(document.get("reviews"), list)):
            raise ValueError("reviews.json does not contain a reviews array")
        document = dict(document)
        document["reviews"] = list(document["reviews"]) + [record]
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                    "w", encoding="utf-8", dir=reviews_path.parent,
                    prefix=f".{reviews_path.name}.", suffix=".tmp",
                    delete=False) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(document, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, reviews_path)
            directory_fd = os.open(str(reviews_path.parent), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
    return record


def append_feedback(feedback_path, question, claim_id=None, note=None):
    """Append one bounded local JSONL feedback record."""
    question = str(question or "").strip()
    note = str(note or "").strip() or None
    if not question or len(question) > 1000:
        raise ValueError("question must be between 1 and 1000 characters")
    if note is not None and len(note) > 2000:
        raise ValueError("note must be at most 2000 characters")
    record = {
        "question": question,
        "claim_id": claim_id,
        "timestamp": datetime.datetime.now(
            datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if note is not None:
        record["note"] = note
    encoded = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    feedback_path = Path(feedback_path)
    feedback_path.parent.mkdir(parents=True, exist_ok=True)
    with _FEEDBACK_WRITE_LOCK:
        descriptor = os.open(
            str(feedback_path), os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(descriptor, encoded)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    return record


def matching_gap(question, packs_root, products):
    """Return the most relevant recorded gap using deterministic token overlap."""
    question_tokens = set(answer.tokenize(question))
    best = None
    for product in products:
        gap_doc = answer.load_json(
            Path(packs_root) / product["dir"] / "gaps.json", {})
        for gap in gap_doc.get("gaps", []):
            searchable = " ".join(str(gap.get(field, "")) for field in
                                  ("gap_id", "kind", "reason", "closes_when"))
            score = len(question_tokens & set(answer.tokenize(searchable)))
            candidate = (score, str(gap.get("gap_id", "")), product, gap)
            if score >= 2 and (best is None or candidate[:2] > best[:2]):
                best = candidate
    if best is None:
        return None
    _, _, product, gap = best
    return {
        "gap_id": gap.get("gap_id"),
        "kind": gap.get("kind"),
        "reason": gap.get("reason"),
        "product": f"{product.get('brand', '')} {product.get('model', '')}".strip(),
        "product_dir": product.get("dir"),
    }


def _claims_with_status(packs_root, product_dir):
    """Load claims and derive their serving status with system.answer."""
    pack_dir = Path(packs_root) / product_dir
    claims = answer.records(answer.load_json(pack_dir / "claims.json", []),
                            "claims")
    dispositions = answer.latest_dispositions(
        answer.load_json(pack_dir / "reviews.json", {}))
    alarms = answer.alarmed_claims(
        answer.load_json(pack_dir / "verdicts.json", {}))
    return [(claim, answer.claim_status(claim.get("claim_id"),
                                       dispositions, alarms))
            for claim in claims]


def _procedure_groups(packs_root, product_dir):
    groups = {}
    for claim, status in _claims_with_status(packs_root, product_dir):
        obj = claim.get("object")
        if (claim.get("type") != "STEP" or not isinstance(obj, dict)
                or not isinstance(obj.get("procedure"), str)
                or not isinstance(obj.get("step_number"), int)):
            continue
        if status == "REJECTED":
            continue
        procedure = answer.canonical_procedure_id(obj["procedure"])
        groups.setdefault(procedure, []).append((claim, status))
    for steps in groups.values():
        steps.sort(key=lambda item: (item[0]["object"]["step_number"],
                                     item[0].get("claim_id", "")))
    return groups


def _pdf_binding_for_claim(packs_root, product_dir, claim_id, preview):
    media_doc = answer.load_json(
        Path(packs_root) / product_dir / "media-bindings.json", {})
    matches = [binding for binding in media_doc.get("bindings", [])
               if binding.get("kind") == "PDF_PAGE"
               and claim_id in binding.get("claim_ids", [])
               and (binding.get("approved_by") or preview)]
    return sorted(matches, key=lambda item: item.get("binding_id", ""))[0] \
        if matches else None


def discover_procedures(packs_root, product_dir, preview=False):
    """Return procedures with at least one step allowed by serving policy."""
    wanted = answer.PREVIEW_STATUSES if preview else answer.SERVABLE_DEFAULT
    procedures = []
    for name, grouped_steps in sorted(
            _procedure_groups(packs_root, product_dir).items()):
        visible = [(claim, status) for claim, status in grouped_steps
                   if status in wanted]
        if not visible:
            continue
        published_count = sum(status == "PUBLISHED"
                              for _, status in grouped_steps)
        if published_count == len(grouped_steps):
            publication_state = "published"
        elif published_count:
            publication_state = "partial"
        else:
            publication_state = "pending"
        procedures.append({
            "name": name,
            "step_count": len(grouped_steps),
            "served_step_count": len(visible),
            "fully_published": all(status == "PUBLISHED"
                                   for _, status in grouped_steps),
            "publication_state": publication_state,
        })
    return procedures


def procedure_payload(packs_root, product_dir, procedure, preview=False):
    """Build an ordered, status-aware procedure response."""
    grouped_steps = _procedure_groups(packs_root, product_dir).get(procedure)
    if grouped_steps is None:
        return None
    wanted = answer.PREVIEW_STATUSES if preview else answer.SERVABLE_DEFAULT
    steps = []
    for claim, status in grouped_steps:
        if status not in wanted:
            continue
        claim_id = claim.get("claim_id")
        binding = _pdf_binding_for_claim(
            packs_root, product_dir, claim_id, preview)
        page_image_url = None
        if binding:
            product_part = quote(product_dir, safe="")
            claim_part = quote(claim_id, safe="")
            page_image_url = (
                f"/page-image/{product_part}/{claim_part}.png"
                f"?preview={1 if preview else 0}")
        steps.append({
            "step_number": claim["object"]["step_number"],
            "action": claim["object"].get("action", ""),
            "claim_id": claim_id,
            "status": status,
            "page_image_url": page_image_url,
        })
    return {
        "product": product_dir,
        "procedure": procedure,
        "fully_published": all(status == "PUBLISHED"
                               for _, status in grouped_steps),
        "steps": steps,
    }


def _planner_scope(question, catalog, product_dir, packs_root, preview):
    """Build the request-scoped product/procedure allowlist for Luna."""
    if product_dir:
        scoped = [product for product in catalog
                  if product.get("dir") == product_dir]
    else:
        scoped = answer.detect_products(answer.tokenize(question), catalog)
    products = [{
        "id": product.get("dir"),
        "brand": product.get("brand"),
        "model": product.get("model"),
        "category": product.get("category"),
    } for product in scoped]
    procedures = {
        product["id"]: [item["name"] for item in discover_procedures(
            packs_root, product["id"], preview)]
        for product in products if product.get("id")
    }
    return products, procedures


def _direct_procedure_result(packs_root, vault_root, product_dir, procedure,
                             preview):
    """Retrieve a validated procedure ID without relying on lexical scoring."""
    product = next((item for item in answer.load_catalog(vault_root)
                    if item.get("dir") == product_dir), None)
    grouped_steps = _procedure_groups(packs_root, product_dir).get(procedure)
    if product is None or grouped_steps is None:
        return None
    wanted = answer.PREVIEW_STATUSES if preview else answer.SERVABLE_DEFAULT
    sources = answer.source_details(vault_root, product)
    steps = []
    for claim, status in grouped_steps:
        if status not in wanted:
            continue
        obj = claim.get("object") if isinstance(claim.get("object"), dict) else {}
        steps.append({
            "step_number": obj.get("step_number"),
            "action": obj.get("action"),
            "claim_id": claim.get("claim_id"),
            "status": status,
            "tier": claim.get("consequence_ceiling"),
            "citations": [{
                "source_id": binding.get("source_id"),
                "quote": binding.get("quote", ""),
                **sources.get(binding.get("source_id"), {}),
            } for binding in claim.get("source_bindings", [])],
        })
    if not steps:
        return None
    steps.sort(key=lambda step: (step["step_number"] is None,
                                 step["step_number"]))
    statuses = {step["status"] for step in steps}
    tiers = [step["tier"] for step in steps if step.get("tier")]
    summary = answer.PROCEDURE_SUMMARIES.get(
        procedure,
        f"{answer.readable_label(procedure)} has {len(steps)} documented steps.")
    return {
        "score": 1.0,
        "status": ("PUBLISHED" if statuses == {"PUBLISHED"}
                   else "CANDIDATE"),
        "product": f"{product.get('brand', '')} {product.get('model', '')}".strip(),
        "product_dir": product_dir,
        "claim_id": f"procedure:{procedure}",
        "tier": max(tiers) if tiers else None,
        "type": "PROCEDURE",
        "procedure": procedure,
        "predicate": procedure,
        "answer": summary,
        "display_text": summary,
        "raw_answer": f"{len(steps)} documented steps",
        "steps": steps,
        "citations": [],
    }


def _retrieve_for_plan(question, intent_outcome, packs_root, vault_root,
                       product_dir, preview, top):
    """Execute only validated local tools; fall back to lexical retrieval."""
    plan = intent_outcome.get("plan") if intent_outcome.get("ok") else None
    executed_tool = "search_evidence"
    tool_fallback_reason = None
    if plan and plan.get("tool") == "show_procedure":
        executed_tool = "show_procedure"
        procedure = plan["procedure_id"]
        direct = _direct_procedure_result(
            packs_root, vault_root, plan["product_id"], procedure, preview)
        if direct:
            return [direct], {
                "SUSPENDED": 0, "CANDIDATE": 0, "REJECTED": 0,
            }, executed_tool, None
        executed_tool = "search_evidence"
        tool_fallback_reason = "procedure_not_retrieved"
    elif plan and plan.get("tool") == "report_unsupported_question":
        # Luna cannot establish that evidence is absent. Search once before
        # the server reports the question as unsupported.
        tool_fallback_reason = "unsupported_requires_evidence_check"

    routed_product = (plan.get("product_id") if plan else None) or product_dir
    results, not_served = answer.search(
        question,
        packs_root=packs_root,
        vault_root=vault_root,
        product_dir=routed_product,
        preview=preview,
        top=top,
    )
    return results, not_served, executed_tool, tool_fallback_reason


def _attach_video_jobs(results, video_jobs, preview):
    """Queue walkthrough generation for the top procedure lacking a video.

    Only in preview mode: a freshly generated asset is unapproved, so under a
    published-only policy the finished video could never be served anyway.
    """
    if video_jobs is None or not preview:
        return
    for result in results:
        if result.get("type") != "PROCEDURE" or not result.get("steps"):
            continue
        if any(media_modality(media) == "video"
               for media in result.get("media", [])):
            continue
        if not video_jobs.can_generate(result.get("product_dir"),
                                       result.get("procedure")):
            # No grounded keyframes registered: the honest text+image
            # answer stands, with no placeholder promising a video.
            continue
        steps = [{
            "step_number": step.get("step_number"),
            "action": step.get("action") or "",
            "claim_id": step.get("claim_id"),
        } for step in result["steps"]]
        job = video_jobs.ensure(
            result.get("product_dir"), result.get("product"),
            result.get("procedure"), steps)
        result["video_job"] = {
            "job_id": job["job_id"],
            "state": job["state"],
            "poll_url": "/api/video-status?job=" + quote(
                job["job_id"], safe=""),
        }
        return


def _attach_eligible_media(results, media_by_claim):
    for result in results:
        member_ids = ([step["claim_id"] for step in result.get("steps", [])]
                      or [result["claim_id"]])
        seen, media = set(), []
        for member_id in member_ids:
            for item in media_by_claim.get(member_id, []):
                if item["id"] not in seen:
                    seen.add(item["id"])
                    media.append(item)
        result["media"] = media
    return results


def render_pdf_page(pdf_path, page_number, cache_root, expected_hash):
    """Render one entire PDF page at 144 DPI and return its cache path."""
    pdf_path = Path(pdf_path).resolve()
    cache_root = Path(cache_root).resolve()
    if not isinstance(expected_hash, str) or not _verified_hash(
            pdf_path, expected_hash):
        raise MediaIntegrityError("PDF source does not match its manifest hash")
    cache_key = hashlib.sha256(
        f"{pdf_path}:{expected_hash}:{page_number}:144".encode()).hexdigest()[:24]
    output_path = cache_root / f"page-{cache_key}.png"
    if output_path.is_file():
        return output_path

    with _PAGE_RENDER_LOCK:
        if output_path.is_file():
            return output_path
        import pypdfium2 as pdfium

        document = pdfium.PdfDocument(str(pdf_path))
        try:
            if page_number < 1 or page_number > len(document):
                raise IndexError("PDF page is out of range")
            page = document[page_number - 1]
            try:
                bitmap = page.render(scale=2.0)
                try:
                    image = bitmap.to_pil()
                    cache_root.mkdir(parents=True, exist_ok=True)
                    temporary = output_path.with_suffix(".tmp")
                    image.save(temporary, format="PNG")
                    temporary.replace(output_path)
                finally:
                    bitmap.close()
            finally:
                page.close()
        finally:
            document.close()
    return output_path


def resolve_answer_engine(answer_engine=None):
    """The customer answer path: "v2" (default) or "legacy" (reversible flag)."""
    mode = (answer_engine or os.environ.get("SHOWME_ANSWER_ENGINE") or "v2").lower()
    if mode not in {"v2", "legacy"}:
        raise ValueError(f"unknown answer engine {mode!r}")
    return mode


def parse_answer_context(raw, known_products):
    """Accept only the fields a follow-up needs; ignore anything else."""
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        return None
    if not isinstance(value, dict) or value.get("product_dir") not in known_products:
        return None
    context = {"product_dir": value["product_dir"]}
    if isinstance(value.get("procedure_id"), str) and re.fullmatch(r"[a-z0-9_]{1,80}", value["procedure_id"]):
        context["procedure_id"] = value["procedure_id"]
    return context


def make_handler(packs_root, vault_root, cache_root=DEFAULT_CACHE_ROOT,
                 reviewer=None, feedback_path=None, luna_planner=None,
                 video_jobs=None, answer_engine=None, video_store=None):
    """Build a request handler bound to explicit content roots."""
    packs_root = Path(packs_root).resolve()
    vault_root = Path(vault_root).resolve()
    cache_root = Path(cache_root).resolve()
    feedback_path = Path(feedback_path or APP_ROOT / "feedback.jsonl").resolve()
    luna_planner = luna_planner or LunaPlanner()
    video_jobs = video_jobs or VideoJobManager(
        packs_root, vault_root=vault_root)
    engine_mode = resolve_answer_engine(answer_engine)
    engine = (AnswerEngine(packs_root, vault_root) if engine_mode == "v2" else None)
    video_store = video_store or VideoStore()
    video_store.import_scene_assets()

    class AnswerHandler(BaseHTTPRequestHandler):
        server_version = "ShowMeAnswer/0"

        def _visitor(self):
            """Anonymous persistent visitor id (cookie) that owns saved video requests."""
            if getattr(self, "_visitor_id", None):
                return self._visitor_id
            match = re.search(r"(?:^|;\s*)showme_visitor=(v_[0-9a-f]{24})\b",
                              self.headers.get("Cookie", ""))
            if match:
                self._visitor_id = match.group(1)
            else:
                self._visitor_id = "v_" + uuid.uuid4().hex[:24]
                self._set_visitor_cookie = True
            return self._visitor_id

        def _send_json(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            if getattr(self, "_set_visitor_cookie", False):
                self.send_header("Set-Cookie", f"showme_visitor={self._visitor_id}; Path=/; "
                                 "Max-Age=31536000; HttpOnly; SameSite=Lax")
                self._set_visitor_cookie = False
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _send_file(self, path, cache_control="no-cache"):
            file_size = path.stat().st_size
            content_type = mimetypes.guess_type(path.name)[0]
            if path.suffix == ".js":
                content_type = "text/javascript"
            content_type = content_type or "application/octet-stream"
            if content_type.startswith("text/"):
                content_type = f"{content_type}; charset=utf-8"

            start, end, status = 0, file_size - 1, 200
            range_header = self.headers.get("Range")
            if range_header and range_header.startswith("bytes="):
                try:
                    start_text, end_text = range_header[6:].split("-", 1)
                    start = int(start_text) if start_text else 0
                    end = int(end_text) if end_text else file_size - 1
                    if start < 0 or end < start or end >= file_size:
                        raise ValueError
                    status = 206
                except ValueError:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{file_size}")
                    self.end_headers()
                    return

            length = end - start + 1
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Accept-Ranges", "bytes")
            if status == 206:
                self.send_header("Content-Range",
                                 f"bytes {start}-{end}/{file_size}")
            self.send_header("Cache-Control", cache_control)
            self.end_headers()
            with path.open("rb") as handle:
                handle.seek(start)
                remaining = length
                try:
                    while remaining:
                        chunk = handle.read(min(1024 * 1024, remaining))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    # Browsers routinely cancel speculative media ranges.
                    return

        def _read_json_body(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send_json(400, {"error": "Invalid Content-Length"})
                return None
            if length < 1 or length > 32768:
                self._send_json(400, {
                    "error": "JSON body is required and must be at most 32 KB",
                })
                return None
            try:
                payload = json.loads(self.rfile.read(length))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json(400, {
                    "error": "Request body must be valid JSON",
                })
                return None
            if not isinstance(payload, dict):
                self._send_json(400, {
                    "error": "Request body must be a JSON object",
                })
                return None
            return payload

        def _serve_static(self, request_path):
            relative = "index.html" if request_path == "/" else unquote(
                request_path.removeprefix("/static/"))
            candidate = (STATIC_ROOT / relative).resolve()
            if STATIC_ROOT not in candidate.parents or not candidate.is_file():
                self._send_json(404, {"error": "Not found"})
                return
            self._send_file(candidate)

        def _serve_products(self):
            self._send_json(200, {"products": _catalog_products(vault_root)})

        def _serve_review_config(self):
            self._send_json(200, {
                "enabled": bool(reviewer),
                "reviewer": reviewer,
                "recording_note": "Decisions are recorded to this product's evidence-pack reviews.json.",
            })

        def _preview_value(self, query):
            preview_value = query.get("preview", ["0"])[0]
            if preview_value not in {"0", "1"}:
                self._send_json(400, {"error": "preview must be 0 or 1"})
                return None
            return preview_value == "1"

        def _known_product(self, query, required=True):
            product_dir = query.get("product", [""])[0].strip()
            if not product_dir:
                if required:
                    self._send_json(400, {"error": "product must not be empty"})
                    return None
                return ""
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Unknown product"})
                return None
            return product_dir

        def _serve_media(self, request_path):
            relative = unquote(request_path.removeprefix("/media/"))
            parts = Path(relative).parts
            if (len(parts) < 2 or any(part in {"", ".", ".."}
                                      for part in parts)):
                self._send_json(404, {"error": "Media not found"})
                return
            product_dir = parts[0]
            local_path = Path(*parts[1:]).as_posix()
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Media not found"})
                return

            product_root = (vault_root / product_dir).resolve()
            candidate = (product_root / local_path).resolve()
            if product_root not in candidate.parents or not candidate.is_file():
                self._send_json(404, {"error": "Media not found"})
                return

            manifest = answer.load_json(product_root / "manifest.json", {})
            source = next((item for item in manifest.get("sources", [])
                           if item.get("local_path") == local_path), None)
            if source is None:
                self._send_json(404, {"error": "Media not found"})
                return
            if source.get("type") == "VIDEO":
                secure = (
                    source.get("authority") == "MANUFACTURER"
                    and bool(source.get("rights_note"))
                    and isinstance(source.get("sha256"), str)
                    and _verified_hash(candidate, source["sha256"])
                )
                if not secure:
                    self._send_json(500, {"error": "Media integrity check failed"})
                    return
            self._send_file(candidate, cache_control="no-store")

        def _serve_derived_media(self, request_path, query):
            relative = unquote(request_path.removeprefix("/derived-media/"))
            parts = Path(relative).parts
            if (len(parts) != 2 or any(part in {"", ".", ".."}
                                       for part in parts)):
                self._send_json(404, {"error": "Derived media not found"})
                return
            product_dir, asset_id = parts
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Derived media not found"})
                return
            asset = _derived_assets(packs_root, product_dir).get(asset_id)
            if asset is None or not asset.get("local_path"):
                self._send_json(404, {"error": "Derived media not found"})
                return
            media_doc = answer.load_json(
                packs_root / product_dir / "media-bindings.json", {})
            bindings = [binding for binding in media_doc.get("bindings", [])
                        if binding.get("kind") == "DERIVED_ASSET"
                        and binding.get("source_id") == asset_id]
            approved = bool(asset.get("approved_by") or any(
                binding.get("approved_by") for binding in bindings))
            preview = query.get("preview", ["0"])[0] == "1"
            if not bindings or (not approved and not preview):
                self._send_json(404, {"error": "Derived media not found"})
                return
            poster = query.get("poster", ["0"])[0] == "1"
            local_path = (asset.get("poster_local_path") if poster
                          else asset.get("local_path"))
            expected_hash = (asset.get("poster_sha256") if poster
                             else asset.get("sha256"))
            if not local_path:
                self._send_json(404, {"error": "Derived media not found"})
                return
            repo_root = packs_root.parent.resolve()
            candidate = (repo_root / local_path).resolve()
            if repo_root not in candidate.parents or not candidate.is_file():
                self._send_json(404, {"error": "Derived media not found"})
                return
            if (not isinstance(expected_hash, str)
                    or not _verified_hash(candidate, expected_hash)):
                self._send_json(500, {"error": "Media integrity check failed"})
                return
            self._send_file(candidate, cache_control="no-store")

        def _serve_procedures(self, query):
            product_dir = self._known_product(query)
            if product_dir is None:
                return
            preview = self._preview_value(query)
            if preview is None:
                return
            self._send_json(200, {
                "product": product_dir,
                "procedures": discover_procedures(
                    packs_root, product_dir, preview),
            })

        def _serve_procedure(self, query):
            product_dir = self._known_product(query)
            if product_dir is None:
                return
            preview = self._preview_value(query)
            if preview is None:
                return
            procedure = query.get("procedure", [""])[0].strip()
            if not procedure:
                self._send_json(400, {"error": "procedure must not be empty"})
                return
            payload = procedure_payload(
                packs_root, product_dir, procedure, preview)
            if payload is None:
                self._send_json(404, {"error": "Unknown procedure"})
                return
            self._send_json(200, payload)

        def _serve_page_image(self, request_path, query):
            preview = self._preview_value(query)
            if preview is None:
                return
            relative = unquote(request_path.removeprefix("/page-image/"))
            parts = Path(relative).parts
            if (len(parts) != 2 or any(part in {"", ".", ".."}
                                      for part in parts)
                    or not parts[1].endswith(".png")):
                self._send_json(404, {"error": "Page image not found"})
                return
            product_dir = parts[0]
            claim_id = parts[1][:-4]
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Page image not found"})
                return

            claim_status = next((status for claim, status in
                                 _claims_with_status(packs_root, product_dir)
                                 if claim.get("claim_id") == claim_id
                                 and claim.get("type") == "STEP"), None)
            wanted = (answer.PREVIEW_STATUSES if preview
                      else answer.SERVABLE_DEFAULT)
            if claim_status not in wanted:
                self._send_json(404, {"error": "Page image not found"})
                return
            binding = _pdf_binding_for_claim(
                packs_root, product_dir, claim_id, preview)
            if binding is None:
                self._send_json(404, {"error": "Page image not found"})
                return

            product_root = (vault_root / product_dir).resolve()
            manifest = answer.load_json(product_root / "manifest.json", {})
            source = next((item for item in manifest.get("sources", [])
                           if item.get("source_id") == binding.get("source_id")),
                          None)
            if source is None or not source.get("local_path"):
                self._send_json(404, {"error": "Page image not found"})
                return
            pdf_path = (product_root / source["local_path"]).resolve()
            if (product_root not in pdf_path.parents or not pdf_path.is_file()
                    or pdf_path.suffix.lower() != ".pdf"):
                self._send_json(404, {"error": "Page image not found"})
                return
            try:
                rendered = render_pdf_page(
                    pdf_path, binding["page"], cache_root,
                    source.get("sha256"))
            except MediaIntegrityError:
                self._send_json(500, {"error": "Media integrity check failed"})
                return
            except IndexError:
                self._send_json(500, {"error": "Registered PDF page is invalid"})
                return
            self._send_file(rendered, cache_control="no-cache")

        def _serve_answer(self, query):
            question = query.get("q", [""])[0].strip()
            if not question:
                self._send_json(400, {"error": "Question must not be empty"})
                return

            preview = self._preview_value(query)
            if preview is None:
                return

            product_dir = self._known_product(query, required=False)
            if product_dir is None:
                return
            product_dir = product_dir or None

            if engine is not None and not preview:
                # Customer path. Owner preview stays on the legacy tools until
                # P2 adds an authenticated owner workspace.
                known = {item["dir"] for item in _catalog_products(vault_root)}
                context = parse_answer_context(
                    query.get("context", [""])[0], known)
                document = engine.answer(question, product_dir, context).to_dict()
                video = video_service.video_for_document(
                    video_store, document, question, self._visitor(), context,
                    auto_generate=query.get("generate", ["0"])[0] == "1")
                document["video"] = video
                if video and (video["assets"] or video["state"] == "requested"):
                    document["visual"]["message"] = None
                self._send_json(200, {
                    "question": question,
                    "mode": ("clarify" if document["status"] == "needs_input"
                             else "answer"),
                    "engine": document["engine"],
                    "answer_document": document,
                    "results": [],
                    "not_served": {"SUSPENDED": 0, "CANDIDATE": 0, "REJECTED": 0},
                    "gap": None,
                    "presentation": None,
                })
                return

            catalog = answer.load_catalog(vault_root)
            if product_dir is None:
                candidates = answer.clarification_candidates(question, catalog)
                if candidates:
                    self._send_json(200, {
                        "question": question,
                        "mode": "clarify",
                        "clarify": {
                            "prompt": "Which product did you mean?",
                            "candidates": [{
                                "product_dir": product.get("dir"),
                                "product": f"{product.get('brand', '')} {product.get('model', '')}".strip(),
                            } for product in candidates],
                        },
                        "results": [],
                        "not_served": {"SUSPENDED": 0, "CANDIDATE": 0,
                                       "REJECTED": 0},
                        "gap": None,
                    })
                    return

            try:
                top = int(query.get("top", ["3"])[0])
            except ValueError:
                self._send_json(400, {"error": "top must be an integer"})
                return
            if top < 1 or top > 100:
                self._send_json(400, {"error": "top must be between 1 and 100"})
                return

            planner_products, procedures_by_product = _planner_scope(
                question, catalog, product_dir, packs_root, preview)
            intent_outcome = luna_planner.plan_intent(
                question, planner_products, procedures_by_product)
            intent_plan = (intent_outcome.get("plan")
                           if intent_outcome.get("ok") else None)
            if (intent_plan
                    and intent_plan.get("tool") == "ask_clarification"):
                self._send_json(200, {
                    "question": question,
                    "mode": "clarify",
                    "clarify": {
                        "prompt": intent_plan["clarification_question"],
                        "candidates": [],
                    },
                    "results": [],
                    "not_served": {"SUSPENDED": 0, "CANDIDATE": 0,
                                   "REJECTED": 0},
                    "gap": None,
                    "planning": {
                        "intent": intent_outcome["metadata"],
                        "composition": None,
                        "requested_tool": intent_plan["tool"],
                        "executed_tool": "ask_clarification",
                        "tool_fallback_reason": None,
                    },
                    "presentation": None,
                })
                return

            results, not_served, executed_tool, tool_fallback_reason = (
                _retrieve_for_plan(
                    question, intent_outcome, packs_root, vault_root,
                    product_dir, preview, top))
            _attach_eligible_media(
                results, _media_index(packs_root, vault_root, preview))
            _attach_video_jobs(results, video_jobs, preview)
            composition_outcome = luna_planner.compose_response(
                question, intent_outcome, results)
            if composition_outcome.get("ok"):
                presentation = composition_outcome["plan"]
                apply_presentation(results, presentation)
            else:
                presentation = deterministic_presentation(
                    results,
                    composition_outcome["metadata"].get("reason")
                    or "composition_fallback",
                )
            if product_dir:
                gap_products = [product for product in catalog
                                if product.get("dir") == product_dir]
            else:
                gap_products = answer.detect_products(
                    answer.tokenize(question), catalog)
            gap = (matching_gap(question, packs_root, gap_products)
                   if not results else None)
            self._send_json(200, {
                "question": question,
                "mode": "answer",
                "results": results,
                "not_served": not_served,
                "gap": gap,
                "planning": {
                    "intent": intent_outcome["metadata"],
                    "composition": composition_outcome["metadata"],
                    "requested_tool": (intent_plan or {}).get("tool"),
                    "executed_tool": executed_tool,
                    "tool_fallback_reason": tool_fallback_reason,
                },
                "presentation": presentation,
            })

        def _serve_video_status(self, query):
            job_id = query.get("job", [""])[0].strip()
            if not job_id:
                self._send_json(400, {"error": "job must not be empty"})
                return
            job = video_jobs.status(job_id)
            if job is None:
                self._send_json(404, {"error": "Unknown video job"})
                return
            payload = {
                "job_id": job["job_id"],
                "state": job["state"],
                "product_dir": job["product_dir"],
                "procedure": job["procedure"],
                "media": None,
            }
            if job["state"] == "ready" and job.get("binding_id"):
                media_by_claim = _media_index(
                    packs_root, vault_root, preview=True)
                payload["media"] = next(
                    (item
                     for claim_id in job["claim_ids"]
                     for item in media_by_claim.get(claim_id, [])
                     if item.get("id") == job["binding_id"]),
                    None)
            self._send_json(200, payload)

        def _record_review(self):
            payload = self._read_json_body()
            if payload is None:
                return
            if not reviewer:
                self._send_json(403, {
                    "error": "Review writing is disabled: restart with --reviewer owner@example.com",
                })
                return
            if "claim_ids" in payload:
                self._send_json(400, {
                    "error": "Bulk review is not supported; C2/C3 claims require one explicit per-claim click.",
                })
                return
            product_dir = str(payload.get("product", "")).strip()
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Unknown product"})
                return
            claim_id = str(payload.get("claim_id", "")).strip()
            pack_dir = packs_root / product_dir
            claims = answer.records(
                answer.load_json(pack_dir / "claims.json", []), "claims")
            claim = next((item for item in claims
                          if item.get("claim_id") == claim_id), None)
            if claim is None:
                self._send_json(404, {"error": "Unknown claim"})
                return
            disposition = payload.get("disposition")
            try:
                record = append_review(
                    pack_dir, reviewer, claim, disposition,
                    payload.get("rationale"))
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
                return
            alarms = answer.alarmed_claims(
                answer.load_json(pack_dir / "verdicts.json", {}))
            status = answer.claim_status(
                claim_id, {claim_id: disposition}, alarms)
            self._send_json(201, {"review": record, "status": status})

        def _record_feedback(self):
            payload = self._read_json_body()
            if payload is None:
                return
            product_dir = str(payload.get("product", "")).strip()
            claim_id = payload.get("claim_id")
            if claim_id is not None:
                claim_id = str(claim_id).strip()
                pack_dir = packs_root / product_dir
                known_claims = {
                    claim.get("claim_id") for claim in answer.records(
                        answer.load_json(pack_dir / "claims.json", []),
                        "claims")
                }
                if not product_dir or claim_id not in known_claims:
                    self._send_json(404, {"error": "Unknown claim"})
                    return
            try:
                record = append_feedback(
                    feedback_path, payload.get("question"), claim_id,
                    payload.get("note"))
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
                return
            self._send_json(201, {"feedback": record})

        def _serve_my_videos(self):
            rows = video_store.requests_for(self._visitor())
            items = [video_service.request_payload(row, video_store) for row in rows]
            self._send_json(200, {"requests": items,
                                  "unread": sum(1 for i in items if not i["seen"]),
                                  "active": sum(1 for i in items if i["state"] in
                                                ("queued", "rendering", "checking"))})

        def _create_video_request(self):
            payload = self._read_json_body()
            if payload is None:
                return
            product_dir = str(payload.get("product_dir", ""))
            procedure_id = str(payload.get("procedure_id", ""))
            view = str(payload.get("view", "main"))
            if view not in ("main", "rear", "side", "front"):
                self._send_json(400, {"error": "Unknown view"})
                return
            product = engine.products().get(product_dir) if engine else None
            procedure = product.procedures.get(procedure_id) if product else None
            if procedure is None:
                self._send_json(404, {"error": "Unknown product procedure"})
                return
            if not all(product.eligible(step["claim_id"]) for step in procedure["steps"]):
                self._send_json(409, {"error": "This procedure isn't fully verified, "
                                               "so we can't make a video of it yet."})
                return
            from system.answer_engine import readable_procedure
            row = video_store.create_request(
                self._visitor(), product_dir, product.name, procedure_id,
                readable_procedure(procedure_id), view,
                str(payload.get("question", ""))[:300] or readable_procedure(procedure_id))
            full = video_store.open_request_for(self._visitor(), product_dir, procedure_id, view,
                                                row.get("variant", ""))
            self._send_json(201, {"request": video_service.request_payload(full or row,
                                                                         video_store)})

        def _update_my_videos(self, action):
            payload = self._read_json_body()
            if payload is None:
                return
            request_id = payload.get("id")
            if action == "seen":
                video_store.mark_seen(self._visitor(), request_id)
                self._send_json(200, {"ok": True})
                return
            row = video_store.retry_request(self._visitor(), str(request_id or ""))
            if row is None:
                self._send_json(409, {"error": "This request can't be retried."})
                return
            self._send_json(200, {"request": video_service.request_payload(row, video_store)})

        def _serve_video(self, path):
            parts = path.removeprefix("/video/").split("/")
            asset = video_store.asset(parts[0])
            if not video_store.servable(asset):
                self._send_json(404, {"error": "Video not found"})
                return
            target = Path(asset["poster"] if parts[1:] == ["poster"] else asset["path"]) \
                if (parts[1:] in ([], ["poster"])) else None
            if target is None or not target.is_file():
                self._send_json(404, {"error": "Video not found"})
                return
            self._send_file(target, cache_control="private, max-age=3600")

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            try:
                if parsed.path == "/api/my-videos":
                    self._serve_my_videos()
                elif parsed.path.startswith("/video/"):
                    self._serve_video(parsed.path)
                elif parsed.path == "/api/answer":
                    self._serve_answer(parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path == "/api/products":
                    self._serve_products()
                elif parsed.path == "/api/review-config":
                    self._serve_review_config()
                elif parsed.path == "/api/video-status":
                    self._serve_video_status(
                        parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path == "/api/procedures":
                    self._serve_procedures(
                        parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path == "/api/procedure":
                    self._serve_procedure(
                        parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path.startswith("/page-image/"):
                    self._serve_page_image(
                        parsed.path,
                        parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path.startswith("/dev-media/") and dev_media.enabled():
                    clip = dev_media.path_for(parsed.path.removeprefix("/dev-media/"))
                    if clip is None or not clip.exists():
                        self._send_json(404, {"error": "Media not found"})
                    else:
                        self._send_file(clip, cache_control="no-cache")
                elif parsed.path.startswith("/derived-media/"):
                    self._serve_derived_media(
                        parsed.path,
                        parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path.startswith("/media/"):
                    self._serve_media(parsed.path)
                elif parsed.path == "/" or parsed.path.startswith("/static/"):
                    self._serve_static(parsed.path)
                else:
                    self._send_json(404, {"error": "Not found"})
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception:  # Keep internal details out of the HTTP response.
                self._send_json(500, {"error": "Internal server error"})

        def do_POST(self):  # noqa: N802
            parsed = urlparse(self.path)
            try:
                if parsed.path == "/api/reviews":
                    self._record_review()
                elif parsed.path == "/api/video-requests":
                    self._create_video_request()
                elif parsed.path == "/api/my-videos/seen":
                    self._update_my_videos("seen")
                elif parsed.path == "/api/my-videos/retry":
                    self._update_my_videos("retry")
                elif parsed.path == "/api/feedback":
                    self._record_feedback()
                else:
                    self._send_json(404, {"error": "Not found"})
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception:
                self._send_json(500, {"error": "Internal server error"})

        def log_message(self, format_string, *args):
            sys.stderr.write(
                f"{self.address_string()} - {format_string % args}\n")

    return AnswerHandler


def create_server(port=8765, packs_root=None, vault_root=None, cache_root=None,
                  reviewer=None, feedback_path=None, luna_planner=None,
                  video_jobs=None, answer_engine=None, video_store=None):
    """Create the app server. Passing port 0 lets the OS choose a test port."""
    handler = make_handler(
        packs_root or REPO_ROOT / "evidence-packs",
        vault_root or REPO_ROOT / "source-vault",
        cache_root or DEFAULT_CACHE_ROOT,
        reviewer,
        feedback_path,
        luna_planner,
        video_jobs,
        answer_engine,
        video_store,
    )
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Serve the local answer app")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--packs-root", type=Path,
                        default=REPO_ROOT / "evidence-packs")
    parser.add_argument("--vault-root", type=Path,
                        default=REPO_ROOT / "source-vault")
    parser.add_argument("--reviewer",
                        help="owner email used for append-only review records")
    parser.add_argument("--no-worker", action="store_true",
                        help="don't start the render worker (run python -m app.worker yourself)")
    args = parser.parse_args(argv)

    from app.pipeline.config import load_local_settings
    load_local_settings()

    if args.reviewer and not _EMAIL_RE.fullmatch(args.reviewer):
        parser.error("--reviewer must be a valid email address")

    luna_planner = LunaPlanner()
    server = create_server(
        args.port, args.packs_root, args.vault_root, reviewer=args.reviewer,
        luna_planner=luna_planner)
    print(f"Answer app listening on http://localhost:{server.server_port}")
    print("Owner review writes: " + (
        f"enabled as {args.reviewer}" if args.reviewer else
        "disabled (start with --reviewer owner@example.com)"))
    print(f"Answer engine: {resolve_answer_engine()} "
          "(set SHOWME_ANSWER_ENGINE=legacy to revert)")
    luna_status = luna_planner.status
    print("Luna planning: " + (
        f"enabled ({luna_status['model']})" if luna_status["enabled"] else
        f"deterministic fallback ({luna_status['reason']})"))
    from app.video_jobs import fal_credentials_present, renderer_mode
    mode = renderer_mode()
    descriptions = {
        "keyframe": ("grounded keyframe pipeline (Seedance interpolation + "
                     "VLM verification); procedures without registered "
                     "keyframes get no video"),
        "fal": "EXPERIMENTAL direct fal.ai generation (ungrounded)",
        "deterministic": "deterministic slide renderer (offline fallback)",
    }
    note = ("" if mode == "deterministic" or fal_credentials_present()
            else " — FAL_KEY missing, generation jobs will fail")
    from app.pipeline import authoring
    if resolve_answer_engine() == "v2" and authoring.enabled():
        problem = authoring.readiness(VideoStore())
        print("Video generation: Astra → Blender → bounded Claude critic" +
              (f" — {problem}" if problem else " — configured"))
    else:
        print(f"Video generation: {descriptions[mode]}{note}")
    import signal

    def stop_on_sigterm(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop_on_sigterm)
    worker = None
    if not args.no_worker:
        import subprocess
        worker = subprocess.Popen([sys.executable, "-m", "app.worker"], cwd=str(REPO_ROOT))
        print(f"Render worker: started (pid {worker.pid}); saved requests in "
              f"{VideoStore().root}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if worker is not None:
            worker.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
