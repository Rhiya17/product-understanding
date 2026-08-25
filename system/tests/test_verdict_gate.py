import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = REPO_ROOT / "evidence-packs" / "validate.py"


def make_gate_pack(tmp_path):
    root = tmp_path / "scratch-repository"
    pack = root / "evidence-packs" / "test-product"
    vault = root / "source-vault" / "test-product"
    pack.mkdir(parents=True)
    vault.mkdir(parents=True)
    quote = "The maximum supported weight is 30 lb."
    (vault / "source.md").write_text(quote + "\n", encoding="utf-8")
    (vault / "manifest.json").write_text(json.dumps({
        "sources": [{
            "source_id": "src_text",
            "type": "SPEC_PAGE",
            "local_path": "source.md",
        }]
    }), encoding="utf-8")
    claim = {
        "claim_id": "claim_one",
        "version": 1,
        "status": "CANDIDATE",
        "consequence_ceiling": "C0",
        "type": "LIMIT",
        "predicate": "maximum_weight",
        "subject": "product_one",
        "applicability": {},
        "object": {"value": 30, "unit": "lb"},
        "source_bindings": [{
            "source_id": "src_text", "page": None, "quote": quote,
        }],
        "authority": "MANUFACTURER_SPEC_PAGE",
        "extractor": "test",
        "extracted_at": "2026-08-24",
    }
    (pack / "claims.json").write_text(json.dumps([claim]), encoding="utf-8")
    return pack


def verdict_document(entries, status="COMPLETE", reason=None):
    document = {
        "model": "qwen/qwen3-vl-235b-a22b-instruct",
        "prompt_version": "v1",
        "date": "2026-08-24",
        "status": status,
        "verdicts": entries,
        "conflict_triage": [],
    }
    if reason is not None:
        document["reason"] = reason
    return document


def run_gate(pack):
    return subprocess.run(
        [sys.executable, str(GATE), str(pack / "claims.json")],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False)


def write_verdicts(pack, document):
    (pack / "verdicts.json").write_text(
        json.dumps(document, indent=2) + "\n", encoding="utf-8")


def test_valid_verdicts_are_counted_in_summary(tmp_path):
    pack = make_gate_pack(tmp_path)
    entry = {
        "claim_id": "claim_one", "binding_index": 0,
        "verdict": "ENTAILED", "note": "The value and unit match.",
    }
    write_verdicts(pack, verdict_document([entry]))
    result = run_gate(pack)
    assert result.returncode == 0, result.stdout + result.stderr
    assert '"verdicts_recorded": 1' in result.stdout
    assert '"verification_status": "COMPLETE"' in result.stdout


def test_duplicate_out_of_range_and_incomplete_complete_are_hard_errors(tmp_path):
    pack = make_gate_pack(tmp_path)
    duplicate = {
        "claim_id": "claim_one", "binding_index": 0,
        "verdict": "ENTAILED", "note": "Duplicate entry for the test.",
    }
    write_verdicts(pack, verdict_document([duplicate, duplicate]))
    result = run_gate(pack)
    assert result.returncode != 0
    assert "duplicate verdict" in result.stdout

    out_of_range = {
        "claim_id": "claim_one", "binding_index": 3,
        "verdict": "ENTAILED", "note": "Invalid index for the test.",
    }
    write_verdicts(pack, verdict_document([out_of_range]))
    result = run_gate(pack)
    assert result.returncode != 0
    assert "invalid binding_index" in result.stdout
    assert "COMPLETE document is missing" in result.stdout


def test_partial_and_failed_documents_require_reason(tmp_path):
    pack = make_gate_pack(tmp_path)
    write_verdicts(pack, verdict_document([], status="PARTIAL"))
    result = run_gate(pack)
    assert result.returncode != 0
    assert "requires a nonempty root reason" in result.stdout

    write_verdicts(pack, verdict_document(
        [], status="FAILED", reason="Provider credentials unavailable."))
    result = run_gate(pack)
    assert result.returncode == 0, result.stdout + result.stderr
