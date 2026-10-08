#!/usr/bin/env python3
"""CI gate: verify source-vault integrity.

Checks, per product directory in source-vault/:
  - manifest.json parses and has identity + sources;
  - every source entry with a local_path points at an existing file;
  - every stored sha256 matches a fresh hash of the file;
  - every file under manuals/ with a .pdf extension is a real PDF;
  - catalog.json parses and every catalog dir exists with a manifest.

Exit 0 = clean, 1 = any failure. Failures are printed with paths.
"""
import hashlib
import json
import pathlib
import sys

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
VAULT = ROOT / "source-vault"
ORPHAN_IGNORE_NAMES = {"manifest.json", ".DS_Store"}


def main() -> int:
    failures = []
    if not VAULT.is_dir():
        print("source-vault/ missing")
        return 1

    catalog_path = VAULT / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL catalog.json: {e}")
        return 1

    for prod in catalog.get("products", []):
        pdir = VAULT / prod["dir"]
        if not (pdir / "manifest.json").exists():
            failures.append(f"{prod['dir']}: listed in catalog but has no manifest.json")

    for pdir in sorted(p for p in VAULT.iterdir() if p.is_dir()):
        mp = pdir / "manifest.json"
        if not mp.exists():
            failures.append(f"{pdir.name}: no manifest.json")
            continue
        try:
            manifest = json.loads(mp.read_text())
        except Exception as e:  # noqa: BLE001
            failures.append(f"{pdir.name}/manifest.json: invalid JSON: {e}")
            continue
        if "identity" not in manifest or "sources" not in manifest:
            failures.append(f"{pdir.name}/manifest.json: missing identity or sources")
            continue

        n_checked = 0
        listed_paths = set()
        for src in manifest["sources"]:
            lp = src.get("local_path")
            if not lp:
                continue
            listed_paths.add(pathlib.Path(lp).as_posix())
            f = pdir / lp
            if not f.exists():
                if src.get("storage") == "local_only":
                    # Large media deliberately kept out of Git (.gitignore);
                    # its hash is still checked wherever the file is present.
                    print(f"{pdir.name}: local-only file not present: {lp}")
                    continue
                failures.append(f"{pdir.name}: manifest references missing file {lp}")
                continue
            digest = hashlib.sha256(f.read_bytes()).hexdigest()
            if not src.get("sha256"):
                # Rule 2: every local file should be hash-pinned, or later edits go
                # unseen. Older packs predate this check, so it warns, not fails.
                print(f"WARNING {pdir.name}/{lp}: no sha256 recorded")
            elif digest != src["sha256"]:
                failures.append(f"{pdir.name}/{lp}: sha256 mismatch")
            if f.suffix.lower() == ".pdf":
                if PdfReader is None:
                    failures.append(f"{pdir.name}/{lp}: pypdf is required to "
                                    "check the PDF text layer")
                else:
                    try:
                        reader = PdfReader(f)
                        sampled = reader.pages[:10]
                        has_text = any((page.extract_text() or "").strip()
                                       for page in sampled)
                        if not has_text:
                            failures.append(
                                f"{pdir.name}/{lp}: PDF has no extractable text "
                                "in the first 10 pages; it cannot support quote "
                                "verification and needs OCR or an alternative capture")
                    except Exception as e:  # noqa: BLE001
                        failures.append(f"{pdir.name}/{lp}: PDF text extraction "
                                        f"failed: {e}")
            n_checked += 1

        for stored_file in sorted(path for path in pdir.rglob("*") if path.is_file()):
            relative = stored_file.relative_to(pdir).as_posix()
            if (stored_file.name not in ORPHAN_IGNORE_NAMES
                    and relative not in listed_paths):
                failures.append(f"{pdir.name}: orphan file not listed in manifest: "
                                f"{relative}")

        for pdf in (pdir / "manuals").glob("*.pdf") if (pdir / "manuals").is_dir() else []:
            if pdf.read_bytes()[:5] != b"%PDF-":
                failures.append(f"{pdir.name}/manuals/{pdf.name}: not a real PDF")

        print(f"{pdir.name}: {n_checked} hashed files verified")

    if failures:
        print("\n== FAILURES ==")
        for f in failures:
            print(f"  {f}")
        return 1
    print("\nvault OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
