"""Deterministic gate for evidence packs.

Validates every evidence-packs/<product>/claims.json against:
  1. Schema (LLD §6.6 claim record shape, CANDIDATE-only, C0-C3, known types).
  2. Source bindings: every source_id exists in the product's vault manifest.
  3. Anti-fabrication quote gate: every quote must literally appear in the
     cited local source (PDF page, or whole text file for md/txt/html).
     Claims bound to sources with no local file, or to images/videos, are
     counted as UNVERIFIABLE and reported — they cannot fail this gate.
  4. Anti-hallucination bounding-box gate: PART_LOCATION coordinates must be
     null with annotation_status PENDING unless status is MEASURED.
  5. Work-order contract (evidence-packs/workorders/<product>.json): claim
     subject, total-count floor, per-type floors, mandated conflict pairs,
     and checklist coverage. Every unmet expectation must be waived by an
     explicit machine-readable gap in <product>/gaps.json — the honest-gap
     protocol. Unwaived shortfalls are hard failures.

Run: python3 evidence-packs/validate.py [path/to/claims.json]
Exit 0 only if every pack passes. Each pack also emits one SUMMARY_JSON
line for telemetry aggregation.
"""

import glob
import html
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

SCHEMA_REQUIRED = ["claim_id", "version", "status", "consequence_ceiling", "type",
                   "predicate", "subject", "applicability", "object", "source_bindings",
                   "authority", "extractor", "extracted_at"]
ALLOWED_STATUS = ["CANDIDATE"]
ALLOWED_CEILINGS = ["C0", "C1", "C2", "C3"]
ALLOWED_TYPES = ["LIMIT", "SPEC", "STEP", "WARNING", "PART_LOCATION",
                 "COMPATIBILITY", "CARE", "POLICY", "STATE"]
ALLOWED_AUTHORITIES = ["MANUFACTURER_MANUAL", "MANUFACTURER_SPEC_PAGE",
                       "MANUFACTURER_SUPPORT_PAGE"]
ALLOWED_GAP_KINDS = ["SOURCE_MISSING", "NOT_EXTRACTED", "UNDERIVABLE"]
ALLOWED_DISPOSITIONS = ["APPROVED_FOR_PUBLISH", "REJECTED_FOR_SERVING", "NEEDS_RECHECK"]
ALLOWED_VERDICTS = ["ENTAILED", "MEANING_CHANGED", "CANNOT_JUDGE"]
ALLOWED_VERIFICATION_STATUS = ["COMPLETE", "PARTIAL", "FAILED"]
ALLOWED_CONFLICT_RESULTS = ["GENUINE_CONFLICT", "DIFFERENT_SCOPE_OR_EVENT",
                            "CANNOT_JUDGE"]
VISUAL_SOURCE_TYPES = ["IMAGE", "VIDEO", "VIDEO_URL"]

TEXT_EXTS = (".md", ".txt", ".html", ".htm")
QUOTE_CORE_LEN = 60

_PUNCT_MAP = str.maketrans({"’": "'", "‘": "'", "“": '"',
                            "”": '"', "–": "-", "—": "-",
                            " ": " "})

_PDF_CACHE = {}
_TEXT_CACHE = {}


def normalize(s):
    return re.sub(r"\s+", " ", s.translate(_PUNCT_MAP)).lower().strip()


def _pdf_reader(path):
    if path not in _PDF_CACHE:
        _PDF_CACHE[path] = PdfReader(path)
    return _PDF_CACHE[path]


def _pdf_page_text(path, page):
    key = (path, page)
    if key not in _TEXT_CACHE:
        _TEXT_CACHE[key] = normalize(_pdf_reader(path).pages[page - 1].extract_text() or "")
    return _TEXT_CACHE[key]


def _pdf_full_text(path):
    key = (path, None)
    if key not in _TEXT_CACHE:
        reader = _pdf_reader(path)
        _TEXT_CACHE[key] = normalize(" ".join((p.extract_text() or "") for p in reader.pages))
    return _TEXT_CACHE[key]


def _text_file_text(path):
    if path not in _TEXT_CACHE:
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        if path.lower().endswith((".html", ".htm")):
            raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        _TEXT_CACHE[path] = normalize(raw)
    return _TEXT_CACHE[path]


def check_quote(quote, src_path, page, counters):
    """Returns an error string, or None if the quote passes (or is unverifiable)."""
    core = normalize(quote)[:QUOTE_CORE_LEN]
    if not src_path or not os.path.exists(src_path):
        counters["unverifiable_no_local_file"] += 1
        return None
    lower = src_path.lower()
    if lower.endswith(".pdf"):
        if PdfReader is None:
            counters["quote_checks_skipped_no_pypdf"] += 1
            return None
        if page is not None:
            try:
                found = core in _pdf_page_text(src_path, page)
            except IndexError:
                return f"cited page {page} is out of range for {os.path.basename(src_path)}"
            if not found:
                return (f"quote not found on cited page {page} of "
                        f"{os.path.basename(src_path)} — possible fabricated or "
                        f"mis-cited quote: '{quote[:70]}'")
        else:
            counters["pdf_bindings_missing_page"] += 1
            if core not in _pdf_full_text(src_path):
                return (f"quote not found anywhere in {os.path.basename(src_path)} "
                        f"— possible fabricated quote: '{quote[:70]}'")
        counters["quotes_verified"] += 1
        return None
    if lower.endswith(TEXT_EXTS):
        if core not in _text_file_text(src_path):
            return (f"quote not found in {os.path.basename(src_path)} — possible "
                    f"fabricated quote: '{quote[:70]}'")
        counters["quotes_verified"] += 1
        return None
    counters["unverifiable_binary_source"] += 1  # image/video: quote describes a visual
    return None


def find_bounding_boxes(obj, path="object"):
    """Yield (json_path, container) for every dict carrying a bounding_box key."""
    if isinstance(obj, dict):
        if "bounding_box" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from find_bounding_boxes(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from find_bounding_boxes(v, f"{path}[{i}]")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_pack(claims_path):
    print(f"\n--- Validating {claims_path} ---")
    errors, warnings = [], []
    counters = defaultdict(int)

    pack_dir = os.path.dirname(os.path.abspath(claims_path))
    product_dir = os.path.basename(pack_dir)
    root = os.path.normpath(os.path.join(pack_dir, "..", ".."))
    manifest_path = os.path.join(root, "source-vault", product_dir, "manifest.json")
    workorder_path = os.path.join(root, "evidence-packs", "workorders", f"{product_dir}.json")
    gaps_path = os.path.join(pack_dir, "gaps.json")

    if not os.path.exists(manifest_path):
        print(f"ERROR: no vault manifest at {manifest_path}")
        return False, counters

    manifest = load_json(manifest_path)
    valid_source_ids, source_paths, source_types = set(), {}, {}
    for src in manifest.get("sources", []):
        valid_source_ids.add(src.get("source_id"))
        source_types[src.get("source_id")] = src.get("type")
        if src.get("local_path"):
            source_paths[src["source_id"]] = os.path.join(
                os.path.dirname(manifest_path), src["local_path"])

    try:
        claims = load_json(claims_path)
    except Exception as e:
        print(f"ERROR: cannot parse {claims_path}: {e}")
        return False, counters
    if not isinstance(claims, list):
        print("ERROR: claims.json root must be a list")
        return False, counters

    workorder = load_json(workorder_path) if os.path.exists(workorder_path) else None
    gaps_doc = load_json(gaps_path) if os.path.exists(gaps_path) else None

    # ---- gaps.json structural validation + waiver set ----
    waivers = set()
    coverage = {}
    if gaps_doc is not None:
        coverage = gaps_doc.get("coverage", {})
        for g in gaps_doc.get("gaps", []):
            if g.get("kind") not in ALLOWED_GAP_KINDS:
                errors.append(f"gaps.json: gap {g.get('gap_id')} has invalid kind {g.get('kind')}")
            if not g.get("reason"):
                errors.append(f"gaps.json: gap {g.get('gap_id')} has no reason")
            for w in g.get("waives", []):
                waivers.add(w)
        counters["gaps_recorded"] = len(gaps_doc.get("gaps", []))

    # ---- per-claim checks ----
    seen_ids = set()
    seen_quotes = defaultdict(list)
    procedures = defaultdict(list)
    type_counts = defaultdict(int)
    ceiling_counts = defaultdict(int)
    predicate_claims = defaultdict(list)

    for i, claim in enumerate(claims):
        cid = claim.get("claim_id", f"<index {i}>")
        for req in SCHEMA_REQUIRED:
            if req not in claim:
                errors.append(f"{cid}: missing required field {req}")
        if claim.get("claim_id") in seen_ids:
            errors.append(f"duplicate claim_id: {cid}")
        seen_ids.add(claim.get("claim_id"))
        if claim.get("status") not in ALLOWED_STATUS:
            errors.append(f"{cid}: invalid status {claim.get('status')}")
        if claim.get("consequence_ceiling") not in ALLOWED_CEILINGS:
            errors.append(f"{cid}: invalid consequence_ceiling {claim.get('consequence_ceiling')}")
        if claim.get("type") not in ALLOWED_TYPES:
            errors.append(f"{cid}: invalid type {claim.get('type')}")
        if claim.get("authority") not in ALLOWED_AUTHORITIES:
            errors.append(f"{cid}: invalid authority {claim.get('authority')}")
        if workorder and claim.get("subject") != workorder["product_id"]:
            errors.append(f"{cid}: subject {claim.get('subject')} != work order "
                          f"product_id {workorder['product_id']}")

        bindings = claim.get("source_bindings", [])
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"{cid}: empty source_bindings")
            bindings = []
        for b in bindings:
            sid, quote, page = b.get("source_id"), b.get("quote"), b.get("page")
            if sid not in valid_source_ids:
                errors.append(f"{cid}: invalid source_id {sid}")
                continue
            if not quote or not isinstance(quote, str) or not quote.strip():
                errors.append(f"{cid}: empty or missing quote")
                continue
            if page is not None and (not isinstance(page, int) or page <= 0):
                errors.append(f"{cid}: invalid page {page}")
                continue
            err = check_quote(quote, source_paths.get(sid), page, counters)
            if err:
                errors.append(f"{cid}: {err}")
            seen_quotes[(sid, page, quote.strip())].append(cid)

        # nested diagram bindings + bounding-box hallucination gate
        for path, box_holder in find_bounding_boxes(claim.get("object", {})):
            dsid = box_holder.get("source_id")
            if dsid and dsid not in valid_source_ids:
                errors.append(f"{cid}: invalid diagram source_id {dsid} at {path}")
            bbox = box_holder.get("bounding_box")
            status = box_holder.get("annotation_status")
            if bbox is not None and status != "MEASURED":
                errors.append(f"{cid}: non-null bounding_box at {path} with "
                              f"annotation_status={status!r} — coordinates must be "
                              f"measured, never estimated; use null + PENDING")
            if bbox is None and status not in ("PENDING", "MEASURED"):
                warnings.append(f"{cid}: null bounding_box at {path} should carry "
                                f"annotation_status PENDING")

        if claim.get("type") == "STEP" and isinstance(claim.get("object"), dict):
            proc = claim["object"].get("procedure")
            num = claim["object"].get("step_number")
            if proc and num is not None:
                procedures[proc].append(num)

        type_counts[claim.get("type")] += 1
        ceiling_counts[claim.get("consequence_ceiling")] += 1
        predicate_claims[claim.get("predicate")].append(claim)

    for proc, steps in procedures.items():
        s = sorted(steps)
        if s[0] != 1 or s != list(range(1, len(s) + 1)):
            errors.append(f"procedure '{proc}' steps not contiguous from 1: {s}")

    for key, cids in seen_quotes.items():
        if len(cids) > 1:
            warnings.append(f"same quote used by multiple claims {cids} "
                            f"(source {key[0]}, page {key[1]}): '{key[2][:60]}'")

    # ---- work-order contract enforcement ----
    if workorder:
        total = len(claims)
        lo, hi = workorder["expected_total"]["min"], workorder["expected_total"]["max"]
        if total < lo and "total" not in waivers:
            errors.append(f"work order: {total} claims < expected minimum {lo} "
                          f"(waive with 'total' in gaps.json if sources genuinely "
                          f"cannot support more)")
        if total > hi:
            warnings.append(f"work order: {total} claims > expected maximum {hi} — "
                            f"facts may be split too thin")
        for t, floor in workorder.get("required_types", {}).items():
            if type_counts.get(t, 0) < floor and f"type:{t}" not in waivers:
                errors.append(f"work order: {type_counts.get(t, 0)} {t} claims < "
                              f"floor {floor} (waive with 'type:{t}')")
        for conf in workorder.get("required_conflicts", []):
            pred = conf["predicate"]
            if f"conflict:{pred}" in waivers:
                continue
            group = predicate_claims.get(pred, [])
            flagged = [c for c in group
                       if "CONFLICT" in (c.get("extraction_notes") or "")]
            if len(flagged) < 2:
                errors.append(f"work order: mandated conflict on '{pred}' not "
                              f"recorded — need >=2 claims with that predicate, "
                              f"each carrying extraction_notes 'CONFLICT: "
                              f"contradicts claim_<id>' ({conf.get('note', '')})")
        checklist_ids = {c["id"] for c in workorder.get("checklist", [])}
        for c in workorder.get("checklist", []):
            covered = coverage.get(c["id"])
            waived = f"checklist:{c['id']}" in waivers
            if not covered and not waived:
                errors.append(f"work order: checklist item '{c['id']}' has no "
                              f"coverage entry in gaps.json and no waiver — "
                              f"every item is a claim or a recorded gap")
            if covered:
                missing = [x for x in covered if x not in seen_ids]
                if missing:
                    errors.append(f"gaps.json coverage for '{c['id']}' references "
                                  f"unknown claim_ids: {missing}")
        for cov_id in coverage:
            if cov_id not in checklist_ids:
                warnings.append(f"gaps.json coverage has unknown checklist id '{cov_id}'")
        if gaps_doc is None and (workorder.get("checklist") or
                                 workorder.get("required_types")):
            warnings.append("no gaps.json — pack passes only if every contract "
                            "expectation is met outright")
    else:
        warnings.append(f"no work order at {workorder_path} — contract checks skipped")

    # ---- review layer (human decisions; claims themselves stay CANDIDATE) ----
    reviews_path = os.path.join(pack_dir, "reviews.json")
    review_count = 0
    if os.path.exists(reviews_path):
        for r in load_json(reviews_path).get("reviews", []):
            rid = r.get("review_id", "<unnamed review>")
            if r.get("claim_id") not in seen_ids:
                errors.append(f"reviews.json: {rid} references unknown claim_id "
                              f"{r.get('claim_id')}")
            if r.get("disposition") not in ALLOWED_DISPOSITIONS:
                errors.append(f"reviews.json: {rid} has invalid disposition "
                              f"{r.get('disposition')}")
            for req in ("reviewer", "date", "rationale"):
                if not r.get(req):
                    errors.append(f"reviews.json: {rid} missing {req}")
            review_count += 1

    # ---- verifier layer (independent machine findings; never claim edits) ----
    verdicts_path = os.path.join(pack_dir, "verdicts.json")
    verdict_count = meaning_changed = cannot_judge = 0
    verification_status = None
    if os.path.exists(verdicts_path):
        try:
            verdicts_doc = load_json(verdicts_path)
        except Exception as e:  # noqa: BLE001
            errors.append(f"verdicts.json: cannot parse document: {e}")
            verdicts_doc = None

        if not isinstance(verdicts_doc, dict):
            errors.append("verdicts.json: root must be an object")
        else:
            root_fields = {"model", "prompt_version", "date", "status", "reason",
                           "verdicts", "conflict_triage"}
            required_root = {"model", "prompt_version", "date", "status",
                             "verdicts", "conflict_triage"}
            missing_root = sorted(required_root - set(verdicts_doc))
            unknown_root = sorted(set(verdicts_doc) - root_fields)
            if missing_root:
                errors.append(f"verdicts.json: missing root fields {missing_root}")
            if unknown_root:
                errors.append(f"verdicts.json: unknown root fields {unknown_root}")

            model = verdicts_doc.get("model")
            if not isinstance(model, str) or not model.startswith("qwen/"):
                errors.append("verdicts.json: model must be an exact qwen/* model id")
            if not isinstance(verdicts_doc.get("prompt_version"), str) or not \
                    verdicts_doc.get("prompt_version", "").strip():
                errors.append("verdicts.json: prompt_version must be nonempty")
            try:
                date.fromisoformat(verdicts_doc.get("date"))
            except (TypeError, ValueError):
                errors.append("verdicts.json: date must be an ISO date")

            verification_status = verdicts_doc.get("status")
            if verification_status not in ALLOWED_VERIFICATION_STATUS:
                errors.append(f"verdicts.json: invalid status {verification_status}")
            if verification_status in ("PARTIAL", "FAILED") and not \
                    (isinstance(verdicts_doc.get("reason"), str)
                     and verdicts_doc["reason"].strip()):
                errors.append(f"verdicts.json: status {verification_status} "
                              "requires a nonempty root reason")

            claims_by_id = {claim.get("claim_id"): claim for claim in claims}
            recorded_pairs = set()
            verdict_entries = verdicts_doc.get("verdicts")
            if not isinstance(verdict_entries, list):
                errors.append("verdicts.json: verdicts must be a list")
                verdict_entries = []
            for i, verdict in enumerate(verdict_entries):
                verdict_count += 1
                label = f"verdicts.json: verdict index {i}"
                if not isinstance(verdict, dict):
                    errors.append(f"{label} must be an object")
                    continue
                entry_fields = {"claim_id", "binding_index", "verdict", "note"}
                missing_fields = sorted(entry_fields - set(verdict))
                unknown_fields = sorted(set(verdict) - entry_fields)
                if missing_fields:
                    errors.append(f"{label} missing fields {missing_fields}")
                if unknown_fields:
                    errors.append(f"{label} has unknown fields {unknown_fields}; "
                                  "model, prompt version, date, and status belong "
                                  "only at the document root")

                claim_id = verdict.get("claim_id")
                binding_index = verdict.get("binding_index")
                claim = claims_by_id.get(claim_id)
                if claim is None:
                    errors.append(f"{label} references unknown claim_id {claim_id}")
                if (not isinstance(binding_index, int)
                        or isinstance(binding_index, bool)
                        or binding_index < 0
                        or claim is None
                        or binding_index >= len(claim.get("source_bindings", []))):
                    errors.append(f"{label} has invalid binding_index {binding_index} "
                                  f"for claim {claim_id}")
                else:
                    pair = (claim_id, binding_index)
                    if pair in recorded_pairs:
                        errors.append(f"verdicts.json: duplicate verdict for {pair}")
                    recorded_pairs.add(pair)

                result = verdict.get("verdict")
                if result not in ALLOWED_VERDICTS:
                    errors.append(f"{label} has invalid verdict {result}")
                if not isinstance(verdict.get("note"), str) or not \
                        verdict.get("note", "").strip():
                    errors.append(f"{label} has empty note")
                meaning_changed += result == "MEANING_CHANGED"
                cannot_judge += result == "CANNOT_JUDGE"

            if verification_status == "COMPLETE":
                required_pairs = set()
                for claim in claims:
                    for binding_index, binding in enumerate(
                            claim.get("source_bindings", [])):
                        if source_types.get(binding.get("source_id")) not in \
                                VISUAL_SOURCE_TYPES:
                            required_pairs.add((claim.get("claim_id"), binding_index))
                missing_pairs = sorted(required_pairs - recorded_pairs)
                if missing_pairs:
                    errors.append("verdicts.json: COMPLETE document is missing "
                                  f"{len(missing_pairs)} text-binding verdict(s): "
                                  f"{missing_pairs[:5]}")

            triage_entries = verdicts_doc.get("conflict_triage")
            if not isinstance(triage_entries, list):
                errors.append("verdicts.json: conflict_triage must be a list")
                triage_entries = []
            for i, triage in enumerate(triage_entries):
                label = f"verdicts.json: conflict_triage index {i}"
                if not isinstance(triage, dict):
                    errors.append(f"{label} must be an object")
                    continue
                fields = {"pair", "result", "note", "context_sha256"}
                missing_fields = sorted(fields - set(triage))
                unknown_fields = sorted(set(triage) - fields)
                if missing_fields:
                    errors.append(f"{label} missing fields {missing_fields}")
                if unknown_fields:
                    errors.append(f"{label} has unknown fields {unknown_fields}")
                pair = triage.get("pair")
                if (not isinstance(pair, list) or len(pair) != 2
                        or pair[0] == pair[1]
                        or any(claim_id not in claims_by_id for claim_id in pair)):
                    errors.append(f"{label} has invalid claim pair {pair}")
                if triage.get("result") not in ALLOWED_CONFLICT_RESULTS:
                    errors.append(f"{label} has invalid result {triage.get('result')}")
                if not isinstance(triage.get("note"), str) or not \
                        triage.get("note", "").strip():
                    errors.append(f"{label} has empty note")
                context_hash = triage.get("context_sha256")
                if not isinstance(context_hash, str) or not re.fullmatch(
                        r"[0-9a-f]{64}", context_hash):
                    errors.append(f"{label} has invalid context_sha256")

    # ---- report ----
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"FAIL: {e}")

    summary = {
        "product": product_dir,
        "claims": len(claims),
        "types": dict(type_counts),
        "ceilings": dict(ceiling_counts),
        "errors": len(errors),
        "warnings": len(warnings),
        "quotes_verified": counters["quotes_verified"],
        "unverifiable_no_local_file": counters["unverifiable_no_local_file"],
        "unverifiable_binary_source": counters["unverifiable_binary_source"],
        "gaps_recorded": counters["gaps_recorded"],
        "reviews_recorded": review_count,
        "verdicts_recorded": verdict_count,
        "meaning_changed": meaning_changed,
        "cannot_judge": cannot_judge,
        "verification_status": verification_status,
        "workorder_enforced": workorder is not None,
    }
    print("SUMMARY_JSON: " + json.dumps(summary, sort_keys=True))
    if errors:
        print(f"Validation FAILED for {claims_path} ({len(errors)} errors)")
        return False, counters
    print(f"Validation successful for {claims_path}")
    return True, counters


if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = [sys.argv[1]]
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        files = sorted(glob.glob(os.path.join(base, "*", "claims.json")))
    if not files:
        print("No claims.json files found to validate.")
        sys.exit(1)
    ok = True
    for f in files:
        passed, _ = validate_pack(f)
        ok = ok and passed
    sys.exit(0 if ok else 1)
