"""Claim eligibility: one decision used by every serving path.

A claim can be served only when all of these hold for its current version:

1. Its latest review disposition is APPROVED_FOR_PUBLISH, or, when no human
   disposition exists, the latest automatic policy decision for its current
   digest is AUTO_APPROVED (system/auto_publish.py). A human disposition always
   takes precedence over an automatic one.
2. No semantic alarm is outstanding. An alarm (a MEANING_CHANGED verdict in
   the legacy verdicts file or the receipt ledger) persists until a later
   ENTAILED recheck of the same claim digest and an explicit resolution
   record clear it. Provider failures never change alarm state.
3. Every text binding's quote appears in full, as one span, on its cited
   page of the hash-pinned source. Visual bindings need a recorded source
   check. A missing parser is reported, never treated as a pass.
4. A verification receipt is bound to the current claim digest: an ENTAILED
   semantic check, or a recorded human source check.

Receipts live in an append-only ledger per pack,
``evidence-packs/<product>/verification-receipts.jsonl``.
"""

import hashlib
import html
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = REPO_ROOT / "evidence-packs"
VAULT_ROOT = REPO_ROOT / "source-vault"
TEXT_CACHE_DIR = REPO_ROOT / "system" / "cache" / "source-text"
RECEIPTS_FILE = "verification-receipts.jsonl"
AUTO_DECISIONS_FILE = "auto-publish-decisions.jsonl"

VISUAL_SOURCE_TYPES = {"IMAGE", "VIDEO", "VIDEO_URL"}
AUTHENTICATED = {"found_on_cited_page", "found_in_text_source"}
SEMANTIC_RESULTS = {"ENTAILED", "MEANING_CHANGED", "CANNOT_JUDGE"}


class ParserUnavailable(Exception):
    """The PDF text parser cannot be imported in this runtime."""


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def claim_digest(claim):
    """Digest of everything a verdict depends on. Status and notes excluded."""
    fields = {key: claim.get(key) for key in (
        "claim_id", "version", "type", "predicate", "subject",
        "applicability", "object", "source_bindings", "consequence_ceiling")}
    return hashlib.sha256(canonical_json(fields).encode("utf-8")).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text):
    text = unicodedata.normalize("NFKC", text or "").lower()
    text = text.replace("­", "")
    text = re.sub(r"[‘’‛`]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _compact(text):
    return re.sub(r"\s+", "", text)


def _pdf_pages(path):
    try:
        import pypdfium2 as pdfium
    except ImportError as exc:
        raise ParserUnavailable("pypdfium2 is not installed") from exc
    document = pdfium.PdfDocument(str(path))
    try:
        pages = []
        for index in range(len(document)):
            page = document[index]
            textpage = page.get_textpage()
            pages.append(textpage.get_text_bounded())
            textpage.close()
            page.close()
        return pages
    finally:
        document.close()


def _html_text(raw):
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


class SourceText:
    """Normalized page texts per source file, cached by file hash."""

    def __init__(self, cache_dir=TEXT_CACHE_DIR, pdf_parser=_pdf_pages):
        self.cache_dir = Path(cache_dir)
        self.pdf_parser = pdf_parser
        self._memory = {}

    def pages(self, path, sha256):
        if sha256 in self._memory:
            return self._memory[sha256]
        cached = self.cache_dir / f"{sha256}.json"
        if cached.exists():
            pages = json.loads(cached.read_text())
        else:
            path = Path(path)
            suffix = path.suffix.lower()
            if suffix == ".pdf":
                pages = [normalize(page) for page in self.pdf_parser(path)]
            elif suffix in (".html", ".htm"):
                pages = [normalize(_html_text(path.read_text(errors="replace")))]
            else:
                pages = [normalize(path.read_text(errors="replace"))]
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cached.write_text(json.dumps(pages))
        self._memory[sha256] = pages
        return pages


def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _records(payload, key):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    return []


def read_receipts(pack_dir):
    path = Path(pack_dir) / RECEIPTS_FILE
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_receipt(pack_dir, receipt):
    receipt = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **receipt}
    path = Path(pack_dir) / RECEIPTS_FILE
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")
    return receipt


class PackEvidence:
    """Eligibility decisions for one product pack."""

    def __init__(self, product_dir, packs_root=PACKS_ROOT, vault_root=VAULT_ROOT,
                 source_text=None):
        self.product_dir = product_dir
        self.pack_dir = Path(packs_root) / product_dir
        self.vault_dir = Path(vault_root) / product_dir
        self.source_text = source_text or SourceText()
        self.claims = {c["claim_id"]: c for c in _records(
            load_json(self.pack_dir / "claims.json", []), "claims")}
        self.dispositions = {}
        for review in _records(load_json(self.pack_dir / "reviews.json", {}), "reviews"):
            if isinstance(review.get("claim_id"), str) and review.get("disposition"):
                self.dispositions[review["claim_id"]] = review["disposition"]
        self.legacy_alarms = {
            entry.get("claim_id") for entry in _records(
                load_json(self.pack_dir / "verdicts.json", {}), "verdicts")
            if entry.get("verdict") == "MEANING_CHANGED"}
        self.receipts = read_receipts(self.pack_dir)
        self.auto_decisions = {}
        auto_path = self.pack_dir / AUTO_DECISIONS_FILE
        if auto_path.exists():
            for line in auto_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("kind") == "auto_decision":
                    self.auto_decisions[(record["claim_id"], record["claim_digest"])] = record
        manifest = load_json(self.vault_dir / "manifest.json", {})
        self.sources = {s.get("source_id"): s for s in manifest.get("sources", [])}
        self._source_state = {}
        self._decisions = {}

    # Sources -----------------------------------------------------------
    def _source(self, source_id):
        if source_id in self._source_state:
            return self._source_state[source_id]
        source = self.sources.get(source_id)
        state = {"source": source, "problem": None, "sha256": None}
        if source is None:
            state["problem"] = "source_not_in_manifest"
        elif not source.get("local_path"):
            state["problem"] = "no_local_file"
        else:
            path = self.vault_dir / source["local_path"]
            if not path.exists():
                state["problem"] = "source_missing"
            else:
                observed = file_sha256(path)
                state["sha256"] = observed
                state["path"] = path
                if source.get("sha256") and source["sha256"] != observed:
                    state["problem"] = "source_hash_mismatch"
        self._source_state[source_id] = state
        return state

    def authenticate_binding(self, binding):
        state = self._source(binding.get("source_id"))
        source = state["source"] or {}
        if source.get("type") in VISUAL_SOURCE_TYPES:
            return "visual_source"
        if state["problem"]:
            return state["problem"]
        try:
            pages = self.source_text.pages(state["path"], state["sha256"])
        except ParserUnavailable:
            return "parser_unavailable"
        wanted = normalize(binding.get("quote"))
        if not wanted:
            return "empty_quote"
        # PDF text layers split or join words ("Y ou", "T o"); compare the
        # full character sequence with whitespace removed. Every character
        # of the quote must still appear, in order, as one span.
        compact = _compact(wanted)
        page = binding.get("page")
        if len(pages) == 1 and compact in _compact(pages[0]):
            return "found_in_text_source"
        if (isinstance(page, int) and 1 <= page <= len(pages)
                and compact in _compact(pages[page - 1])):
            return "found_on_cited_page"
        if any(compact in _compact(text) for text in pages):
            return "found_on_other_page"
        return "quote_not_found"

    # Receipts ----------------------------------------------------------
    def _receipts_for(self, claim_id, digest=None):
        return [r for r in self.receipts if r.get("claim_id") == claim_id
                and (digest is None or r.get("claim_digest") == digest)]

    def alarm_outstanding(self, claim_id, digest):
        receipts = self._receipts_for(claim_id)
        alarmed = claim_id in self.legacy_alarms or any(
            r.get("kind") == "semantic_check" and r.get("result") == "MEANING_CHANGED"
            for r in receipts)
        if not alarmed:
            return False
        entailed = {r.get("receipt_id") for r in receipts
                    if r.get("kind") == "semantic_check"
                    and r.get("result") == "ENTAILED" and r.get("claim_digest") == digest}
        return not any(r.get("kind") == "alarm_resolution"
                       and r.get("claim_digest") == digest
                       and r.get("recheck_receipt_id") in entailed
                       for r in receipts)

    def current_receipt(self, claim_id, digest):
        """Latest usable verification for this exact digest, if any."""
        usable = [r for r in self._receipts_for(claim_id, digest)
                  if (r.get("kind") == "semantic_check"
                      and r.get("result") in SEMANTIC_RESULTS)
                  or (r.get("kind") == "source_check"
                      and r.get("reviewer_kind") == "human")]
        return usable[-1] if usable else None

    # Decision ----------------------------------------------------------
    def approval_basis(self, claim_id, digest):
        """'human' or 'auto:<policy>' when publication is authorized, else None."""
        disposition = self.dispositions.get(claim_id)
        if disposition is not None:
            return "human" if disposition == "APPROVED_FOR_PUBLISH" else None
        record = self.auto_decisions.get((claim_id, digest))
        if record and record.get("decision") == "AUTO_APPROVED":
            return "auto:" + str(record.get("policy"))
        return None

    def decision(self, claim_id):
        if claim_id in self._decisions:
            return self._decisions[claim_id]
        claim = self.claims.get(claim_id)
        if claim is None:
            result = {"eligible": False, "reasons": ["unknown_claim"], "bindings": []}
            self._decisions[claim_id] = result
            return result
        digest = claim_digest(claim)
        reasons = []
        approval = self.approval_basis(claim_id, digest)
        if approval is None:
            reasons.append("not_approved")
        if self.alarm_outstanding(claim_id, digest):
            reasons.append("unresolved_alarm")
        bindings = []
        human_source_check = any(
            r.get("kind") == "source_check" and r.get("reviewer_kind") == "human"
            and r.get("result") == "VERIFIED"
            for r in self._receipts_for(claim_id, digest))
        for index, binding in enumerate(claim.get("source_bindings", [])):
            status = self.authenticate_binding(binding)
            bindings.append({"index": index, "source_id": binding.get("source_id"),
                             "page": binding.get("page"), "status": status})
            if status in AUTHENTICATED:
                continue
            if status == "visual_source" and human_source_check:
                continue
            reasons.append(f"binding_{index}:{status}")
        receipt = self.current_receipt(claim_id, digest)
        if receipt is None:
            reasons.append("no_receipt_for_current_version")
        elif receipt.get("kind") == "semantic_check" and receipt.get("result") != "ENTAILED":
            reasons.append(f"verifier_{receipt.get('result', 'unknown').lower()}")
        result = {"eligible": not reasons, "reasons": reasons, "bindings": bindings,
                  "claim_digest": digest, "approval_basis": approval,
                  "receipt_id": receipt.get("receipt_id") if receipt else None}
        self._decisions[claim_id] = result
        return result

    def eligible(self, claim_id):
        return self.decision(claim_id)["eligible"]
