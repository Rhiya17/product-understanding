"""Validate the launch evidence shortlist against current claim and source bytes.

    python scripts/validate_launch_evidence.py [--out REPORT.json]

Offline and $0. Checks recorded file hashes, that every listed claim still
exists unchanged, its latest review disposition and verifier entries, that
each quote appears in full on its cited source page, and that each required
procedure lists every step claim the pack holds for it. The output is an
inventory check, not a verification receipt or approval.
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from system.answer import latest_dispositions, load_json, records  # noqa: E402

SHORTLIST = REPO_ROOT / "docs" / "workorders" / "showme-launch-evidence.json"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalize(text):
    text = unicodedata.normalize("NFKC", text or "").lower()
    text = text.replace("­", "")
    text = re.sub(r"[‘’‛`]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


class SourceText:
    """Page text for PDFs, whole text for other readable sources."""

    def __init__(self):
        self._cache = {}

    def pages(self, path):
        path = Path(path)
        if path not in self._cache:
            if path.suffix.lower() == ".pdf":
                import pypdfium2 as pdfium
                document = pdfium.PdfDocument(str(path))
                try:
                    pages = []
                    for index in range(len(document)):
                        page = document[index]
                        textpage = page.get_textpage()
                        pages.append(normalize(textpage.get_text_bounded()))
                        textpage.close()
                        page.close()
                finally:
                    document.close()
            else:
                pages = [normalize(path.read_text(errors="replace"))]
            self._cache[path] = pages
        return self._cache[path]


def quote_check(texts, source_path, page, quote):
    pages = texts.pages(source_path)
    wanted = normalize(quote)
    if not wanted:
        return "empty_quote"
    if page and 1 <= page <= len(pages) and wanted in pages[page - 1]:
        return "found_on_cited_page"
    if len(pages) == 1 and wanted in pages[0]:
        return "found_in_text_source"
    hits = [i + 1 for i, text in enumerate(pages) if wanted in text]
    if hits:
        return f"found_on_other_page:{hits}"
    return "not_found_in_extracted_text"


def validate(shortlist_path):
    shortlist = json.loads(Path(shortlist_path).read_text())
    problems, notes = [], []
    report = {"shortlist": str(Path(shortlist_path).relative_to(REPO_ROOT)),
              "shortlist_sha256": sha256(shortlist_path)}

    # Recorded product file hashes.
    packs = {}
    file_checks = []
    for product in shortlist["products"]:
        pack_dir = REPO_ROOT / "evidence-packs" / product["product_dir"]
        vault_dir = REPO_ROOT / "source-vault" / product["product_dir"]
        for label, path in (("claims", pack_dir / "claims.json"),
                            ("reviews", pack_dir / "reviews.json"),
                            ("verdicts", pack_dir / "verdicts.json"),
                            ("manifest", vault_dir / "manifest.json")):
            recorded = product.get(f"{label}_file_sha256")
            observed = sha256(path)
            file_checks.append({"product_dir": product["product_dir"],
                                "file": label, "matches": recorded == observed})
            if recorded != observed:
                problems.append(f"{product['product_dir']} {label} changed "
                                "since the shortlist was frozen")
        claims = {c["claim_id"]: c for c in records(
            load_json(pack_dir / "claims.json", []), "claims")}
        verdict_rows = records(load_json(pack_dir / "verdicts.json", {}), "verdicts")
        packs[product["product_dir"]] = {
            "claims": claims,
            "dispositions": latest_dispositions(
                load_json(pack_dir / "reviews.json", {})),
            "verdicts": verdict_rows,
            "manifest": {s["source_id"]: s for s in load_json(
                vault_dir / "manifest.json", {}).get("sources", [])},
        }
    report["file_hash_checks"] = file_checks

    # Sources.
    source_checks = []
    for source in shortlist["sources"]:
        path = REPO_ROOT / source["local_path"]
        observed = sha256(path) if path.exists() else None
        manifest = packs[source["product_dir"]]["manifest"].get(source["source_id"], {})
        ok = observed == source["manifest_sha256"] == manifest.get("sha256")
        source_checks.append({"source_id": source["source_id"],
                              "exists": path.exists(), "hash_matches": ok})
        if not ok:
            problems.append(f"source {source['source_id']} hash mismatch or missing")
    report["source_checks"] = source_checks

    # Claims.
    texts = SourceText()
    source_paths = {s["source_id"]: REPO_ROOT / s["local_path"]
                    for s in shortlist["sources"]}
    claim_checks = []
    for entry in shortlist["claims"]:
        pack = packs[entry["product_dir"]]
        claim = pack["claims"].get(entry["claim_id"])
        row = {"claim_id": entry["claim_id"], "exists": claim is not None}
        if claim is None:
            problems.append(f"claim {entry['claim_id']} missing from pack")
            claim_checks.append(row)
            continue
        row["version_matches"] = claim.get("version") == entry["claim_version"]
        row["object_matches"] = claim.get("object") == entry["object_as_recorded"]
        row["bindings_match"] = (claim.get("source_bindings")
                                 == entry["source_bindings_as_recorded"])
        row["latest_disposition"] = pack["dispositions"].get(entry["claim_id"])
        row["disposition_matches"] = (row["latest_disposition"]
                                      == entry["legacy_latest_disposition"])
        verdicts = [v for v in pack["verdicts"] if v.get("claim_id") == entry["claim_id"]]
        row["verifier_verdicts"] = sorted({v.get("verdict") for v in verdicts})
        row["unresolved_meaning_changed"] = "MEANING_CHANGED" in row["verifier_verdicts"]
        row["quote_checks"] = []
        for binding in claim.get("source_bindings", []):
            path = source_paths.get(binding.get("source_id"))
            result = ("source_not_in_shortlist" if path is None else
                      quote_check(texts, path, binding.get("page"), binding.get("quote")))
            row["quote_checks"].append({"source_id": binding.get("source_id"),
                                        "page": binding.get("page"),
                                        "result": result})
        for key in ("version_matches", "object_matches", "bindings_match",
                    "disposition_matches"):
            if not row[key]:
                problems.append(f"claim {entry['claim_id']}: {key} is false")
        if row["unresolved_meaning_changed"]:
            problems.append(f"claim {entry['claim_id']} has a MEANING_CHANGED verdict")
        if not verdicts:
            notes.append(f"claim {entry['claim_id']} has no verifier ledger entry")
        for check in row["quote_checks"]:
            if check["result"] not in ("found_on_cited_page", "found_in_text_source"):
                notes.append(f"claim {entry['claim_id']} quote {check['result']} "
                             f"({check['source_id']} p{check['page']}); needs "
                             "visual source check")
        claim_checks.append(row)
    report["claim_checks"] = claim_checks

    # Procedure completeness: every step claim the pack holds for the
    # procedure, whatever its review status, must be in the required set.
    procedure_checks = []
    for contract in shortlist["procedure_contract_candidates"]:
        pack = packs[contract["product_dir"]]
        pack_steps = sorted(
            (c for c in pack["claims"].values()
             if c.get("type") == "STEP"
             and (c.get("object") or {}).get("procedure") == contract["procedure_id"]),
            key=lambda c: (c["object"].get("step_number") or 0, c["claim_id"]))
        pack_ids = [c["claim_id"] for c in pack_steps]
        required = contract["required_step_claim_ids_in_order"]
        extra = [cid for cid in pack_ids if cid not in required]
        extra_status = {cid: pack["dispositions"].get(cid, "UNREVIEWED")
                        for cid in extra}
        numbers = Counter(c["object"].get("step_number") for c in pack_steps
                          if c["claim_id"] in required)
        row = {
            "product_dir": contract["product_dir"],
            "procedure_id": contract["procedure_id"],
            "required_count": len(required),
            "pack_step_claims": len(pack_ids),
            "missing_from_pack": [cid for cid in required if cid not in pack_ids],
            "pack_steps_not_in_required_set": extra_status,
            "duplicate_step_numbers_in_required_set": sorted(
                n for n, k in numbers.items() if k > 1),
        }
        if row["missing_from_pack"]:
            problems.append(f"{contract['procedure_id']}: required steps missing "
                            f"{row['missing_from_pack']}")
        approved_extra = [cid for cid, s in extra_status.items()
                          if s == "APPROVED_FOR_PUBLISH"]
        if approved_extra:
            problems.append(f"{contract['procedure_id']}: approved step claims "
                            f"outside the required set {approved_extra}")
        elif extra:
            notes.append(f"{contract['procedure_id']}: {len(extra)} non-approved "
                         "step claims outside the required set (superseded or "
                         "rejected versions)")
        procedure_checks.append(row)
    report["procedure_checks"] = procedure_checks

    counts = shortlist["counts"]
    observed_counts = {
        "questions": len(shortlist["questions"]),
        "existing_claims_to_verify": len(shortlist["claims"]),
        "text_source_records": len(shortlist["sources"]),
        "required_procedures": len(shortlist["procedure_contract_candidates"]),
        "required_step_claims": sum(len(p["required_step_claim_ids_in_order"])
                                    for p in shortlist["procedure_contract_candidates"]),
        "claims_without_legacy_verifier_entries": sum(
            1 for row in claim_checks if row.get("exists")
            and not row.get("verifier_verdicts")),
    }
    for key, value in observed_counts.items():
        if counts.get(key) != value:
            problems.append(f"count {key}: recorded {counts.get(key)}, observed {value}")
    report["counts_observed"] = observed_counts
    report["problems"] = problems
    report["notes"] = notes
    report["status"] = "pass" if not problems else "fail"
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--shortlist", type=Path, default=SHORTLIST)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    report = validate(args.shortlist)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=1) + "\n")
    print(f"status: {report['status']}")
    for problem in report["problems"]:
        print("PROBLEM", problem)
    for note in report["notes"]:
        print("NOTE", note)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
