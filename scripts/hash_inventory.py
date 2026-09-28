"""Record or verify SHA-256 hashes of preserved evidence, vault and POC files.

    python scripts/hash_inventory.py record OUT.json
    python scripts/hash_inventory.py verify OUT.json

`verify` exits non-zero if any recorded file changed or disappeared. New files
are reported but are not failures: evidence packs are append-only.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PRESERVED_ROOTS = (
    "evidence-packs",
    "source-vault",
    "generated-assets",
    "poc-astra-ready2jet",
    "poc-astra-scene",
)
IGNORED_PARTS = {"__pycache__", ".DS_Store"}


def iter_files(roots):
    for root in roots:
        base = REPO_ROOT / root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and not IGNORED_PARTS & set(path.parts):
                yield path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(roots):
    return {str(path.relative_to(REPO_ROOT)): sha256(path)
            for path in iter_files(roots)}


def record(out_path, roots):
    files = snapshot(roots)
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "roots": list(roots),
        "file_count": len(files),
        "files": files,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    print(f"Recorded {len(files)} files to {out_path}")
    return 0


def verify(in_path):
    recorded = json.loads(in_path.read_text())
    current = snapshot(recorded["roots"])
    changed = [p for p, h in recorded["files"].items()
               if p in current and current[p] != h]
    missing = [p for p in recorded["files"] if p not in current]
    added = [p for p in current if p not in recorded["files"]]
    for label, paths in (("CHANGED", changed), ("MISSING", missing),
                         ("ADDED", added)):
        for path in paths:
            print(f"{label} {path}")
    print(f"{len(recorded['files'])} recorded, {len(changed)} changed, "
          f"{len(missing)} missing, {len(added)} added")
    return 1 if changed or missing else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=("record", "verify"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.mode == "record":
        return record(args.path, PRESERVED_ROOTS)
    return verify(args.path)


if __name__ == "__main__":
    sys.exit(main())
