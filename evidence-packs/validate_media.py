#!/usr/bin/env python3
"""Validate claim-to-media bindings without network access."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"
VAULT_ROOT = REPO_ROOT / "source-vault"

ALLOWED_KINDS = {"IMAGE", "VIDEO_URL", "VIDEO_FILE", "PDF_PAGE"}
REQUIRED_FIELDS = {
    "binding_id", "claim_ids", "source_id", "kind", "page",
    "start_seconds", "end_seconds", "rationale", "proposed_by",
    "approved_by",
}
BINDING_ID_RE = re.compile(r"^mb_[a-z0-9_]+$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _registered_file(product_vault, source, label, errors):
    local_path = source.get("local_path")
    if not isinstance(local_path, str) or not local_path:
        errors.append(f"{label}: source has no local_path")
        return None
    candidate = (product_vault / local_path).resolve()
    if product_vault.resolve() not in candidate.parents:
        errors.append(f"{label}: source local_path escapes its product vault")
        return None
    if not candidate.is_file():
        errors.append(f"{label}: registered local file does not exist")
        return None
    return candidate


def _valid_origin_url(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_pack(pack_dir, product_vault):
    """Return all validation errors for one product's bindings."""
    pack_dir = Path(pack_dir)
    product_vault = Path(product_vault)
    media_path = pack_dir / "media-bindings.json"
    errors = []

    try:
        claims_doc = load_json(pack_dir / "claims.json")
        manifest = load_json(product_vault / "manifest.json")
        media_doc = load_json(media_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{pack_dir.name}: cannot load media inputs: {exc}"]

    claims = claims_doc if isinstance(claims_doc, list) else claims_doc.get("claims", [])
    claim_ids = {claim.get("claim_id") for claim in claims}
    sources = {source.get("source_id"): source
               for source in manifest.get("sources", [])}

    if not isinstance(media_doc, dict) or set(media_doc) != {"bindings"}:
        return [f"{pack_dir.name}: media document must contain only a bindings array"]
    bindings = media_doc.get("bindings")
    if not isinstance(bindings, list):
        return [f"{pack_dir.name}: bindings must be an array"]

    seen_ids = set()
    seen_relations = set()
    for index, binding in enumerate(bindings):
        label = (binding.get("binding_id", f"binding[{index}]")
                 if isinstance(binding, dict) else f"binding[{index}]")
        if not isinstance(binding, dict):
            errors.append(f"{label}: binding must be an object")
            continue
        missing = REQUIRED_FIELDS - set(binding)
        unknown = set(binding) - REQUIRED_FIELDS
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
        if unknown:
            errors.append(f"{label}: unknown fields {sorted(unknown)}")

        binding_id = binding.get("binding_id")
        if not isinstance(binding_id, str) or not BINDING_ID_RE.fullmatch(binding_id):
            errors.append(f"{label}: invalid binding_id")
        elif binding_id in seen_ids:
            errors.append(f"{label}: duplicate binding_id")
        seen_ids.add(binding_id)

        bound_claims = binding.get("claim_ids")
        if not isinstance(bound_claims, list) or not bound_claims:
            errors.append(f"{label}: claim_ids must be a non-empty array")
            bound_claims = []
        elif len(set(bound_claims)) != len(bound_claims):
            errors.append(f"{label}: claim_ids contains duplicates")
        for claim_id in bound_claims:
            if not isinstance(claim_id, str) or claim_id not in claim_ids:
                errors.append(f"{label}: unknown claim_id {claim_id!r}")

        source_id = binding.get("source_id")
        source = sources.get(source_id)
        if source is None:
            errors.append(f"{label}: unknown source_id {source_id!r}")

        kind = binding.get("kind")
        if kind not in ALLOWED_KINDS:
            errors.append(f"{label}: invalid kind {kind!r}")

        page = binding.get("page")
        if kind == "PDF_PAGE":
            if not isinstance(page, int) or isinstance(page, bool) or page < 1:
                errors.append(f"{label}: PDF_PAGE requires a positive 1-based page")
        elif page is not None:
            errors.append(f"{label}: page must be null unless kind is PDF_PAGE")

        start = binding.get("start_seconds")
        end = binding.get("end_seconds")
        if kind in {"VIDEO_URL", "VIDEO_FILE"}:
            for field_name, value in (("start_seconds", start),
                                      ("end_seconds", end)):
                if (value is not None and
                        (not isinstance(value, int) or isinstance(value, bool)
                         or value < 0)):
                    errors.append(f"{label}: {field_name} must be a non-negative integer or null")
            if isinstance(start, int) and isinstance(end, int) and end <= start:
                errors.append(f"{label}: end_seconds must be greater than start_seconds")
        elif start is not None or end is not None:
            errors.append(f"{label}: time bounds apply only to video bindings")

        rationale = binding.get("rationale")
        if (not isinstance(rationale, str) or not rationale.strip()
                or rationale.rstrip()[-1:] not in {".", "!", "?"}):
            errors.append(f"{label}: rationale must be one non-empty sentence")
        if binding.get("proposed_by") != "agent":
            errors.append(f"{label}: proposed_by must be 'agent'")
        approved_by = binding.get("approved_by")
        if approved_by is not None and (
                not isinstance(approved_by, str)
                or not EMAIL_RE.fullmatch(approved_by)
                or approved_by.lower() == "agent"):
            errors.append(f"{label}: approved_by must be null or an owner email")

        if source is not None and kind in ALLOWED_KINDS:
            source_type = source.get("type")
            if kind == "IMAGE":
                if source_type != "IMAGE":
                    errors.append(f"{label}: IMAGE binding requires an IMAGE source")
                _registered_file(product_vault, source, label, errors)
            elif kind == "VIDEO_URL":
                if source_type != "VIDEO_URL":
                    errors.append(f"{label}: VIDEO_URL binding requires a VIDEO_URL source")
                if not _valid_origin_url(source.get("origin_url")):
                    errors.append(f"{label}: VIDEO_URL source requires an http(s) origin_url")
            elif kind == "VIDEO_FILE":
                if source_type != "VIDEO":
                    errors.append(f"{label}: VIDEO_FILE binding requires a VIDEO source")
                if source.get("authority") != "MANUFACTURER":
                    errors.append(f"{label}: VIDEO_FILE authority must be MANUFACTURER")
                if not source.get("rights_note"):
                    errors.append(f"{label}: VIDEO_FILE source requires a rights_note")
                expected_hash = source.get("sha256")
                if not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
                    errors.append(f"{label}: VIDEO_FILE source requires a lowercase SHA-256")
                video_path = _registered_file(product_vault, source, label, errors)
                if video_path is not None and isinstance(expected_hash, str):
                    actual_hash = hashlib.sha256(video_path.read_bytes()).hexdigest()
                    if actual_hash != expected_hash:
                        errors.append(f"{label}: VIDEO_FILE SHA-256 does not match the manifest")
            elif kind == "PDF_PAGE":
                pdf_path = _registered_file(product_vault, source, label, errors)
                if (pdf_path is not None and pdf_path.suffix.lower() != ".pdf"):
                    errors.append(f"{label}: PDF_PAGE source local_path must end in .pdf")
                if source_type not in {"MANUAL_PDF", "SPEC_DOC_PDF", "GUIDE"}:
                    errors.append(f"{label}: PDF_PAGE source must be a registered PDF document")

        relation = (tuple(bound_claims), source_id, kind, page, start, end)
        if relation in seen_relations:
            errors.append(f"{label}: duplicate claim-to-media relation")
        seen_relations.add(relation)

    return errors


def validate_all(packs_root=PACKS_ROOT, vault_root=VAULT_ROOT):
    """Validate every catalog product and return (success, messages, count)."""
    packs_root = Path(packs_root)
    vault_root = Path(vault_root)
    messages = []
    total = 0
    try:
        products = load_json(vault_root / "catalog.json").get("products", [])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return False, [f"cannot load catalog: {exc}"], 0

    global_ids = set()
    for product in products:
        product_dir = product.get("dir")
        pack_dir = packs_root / product_dir
        media_path = pack_dir / "media-bindings.json"
        if not media_path.is_file():
            messages.append(f"{product_dir}: missing media-bindings.json")
            continue
        errors = validate_pack(pack_dir, vault_root / product_dir)
        messages.extend(errors)
        if not errors:
            bindings = load_json(media_path)["bindings"]
            total += len(bindings)
            for binding in bindings:
                binding_id = binding["binding_id"]
                if binding_id in global_ids:
                    messages.append(f"{binding_id}: duplicate binding_id across packs")
                global_ids.add(binding_id)
    return not messages, messages, total


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate offline media bindings")
    parser.add_argument("--packs-root", type=Path, default=PACKS_ROOT)
    parser.add_argument("--vault-root", type=Path, default=VAULT_ROOT)
    args = parser.parse_args(argv)
    success, errors, count = validate_all(args.packs_root, args.vault_root)
    if errors:
        print("Media validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"media bindings OK ({count} bindings across catalog products)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
