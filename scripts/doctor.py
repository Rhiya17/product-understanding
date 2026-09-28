"""Check the local ShowMe runtime. Reports presence only, never secret values.

    .venv/bin/python scripts/doctor.py

Exit status is non-zero when a required item is missing. Optional items
(rendering runtime, provider credentials) are reported but never required:
offline work must run without them.
"""

import importlib.metadata
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = REPO_ROOT / "system" / "requirements.txt"
PROVIDER_ENV_VARS = ("FAL_KEY", "OPENAI_API_KEY")
SECRET_PATTERN = re.compile(r"""(FAL_KEY|API_KEY|SECRET|TOKEN)["']?\]?\s*=\s*["'][^"']{12,}""")


def pinned_requirements():
    for line in REQUIREMENTS.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "==" in line:
            name, version = line.split("==", 1)
            yield name, version


def tool_version(command):
    path = shutil.which(command[0])
    if not path:
        return None
    output = subprocess.run(command, capture_output=True, text=True).stdout
    return (output.splitlines() or [path])[0][:80]


def sqlite_wal_ok():
    with tempfile.TemporaryDirectory() as directory:
        connection = sqlite3.connect(Path(directory) / "check.db")
        try:
            mode = connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
        finally:
            connection.close()
    return mode.lower() == "wal"


def embedded_secrets():
    hits = []
    for path in [REPO_ROOT / "run_acceptance.py",
                 *REPO_ROOT.glob("scripts/*.py"),
                 *REPO_ROOT.glob("app/*.py"), *REPO_ROOT.glob("system/*.py")]:
        if path.name == "doctor.py":
            continue
        if SECRET_PATTERN.search(path.read_text(errors="replace")):
            hits.append(str(path.relative_to(REPO_ROOT)))
    return hits


def main():
    rows = []  # (required, ok, label, detail)

    in_venv = sys.prefix != sys.base_prefix
    rows.append((True, sys.version_info[:2] == (3, 11), "Python 3.11",
                 f"{sys.version.split()[0]} at {sys.executable}"))
    rows.append((True, in_venv, "project virtual environment",
                 "active" if in_venv else "use .venv/bin/python"))
    for name, version in pinned_requirements():
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        rows.append((True, installed == version, f"package {name}",
                     f"installed {installed or 'missing'}, pinned {version}"))

    rows.append((True, sqlite_wal_ok(), "SQLite WAL",
                 f"sqlite {sqlite3.sqlite_version}"))
    for command in (["ffmpeg", "-version"], ["ffprobe", "-version"]):
        version = tool_version(command)
        rows.append((True, version is not None, command[0], version or "missing"))
    for command in (["node", "--version"], ["npm", "--version"]):
        version = tool_version(command)
        rows.append((False, version is not None, command[0],
                     (version or "missing") + " (needed from P3)"))

    blender = tool_version(["blender", "--version"])
    try:
        bpy_version = importlib.metadata.version("bpy")
    except importlib.metadata.PackageNotFoundError:
        bpy_version = None
    rows.append((False, bool(blender or bpy_version), "Blender runtime",
                 f"blender={blender or 'missing'}, bpy={bpy_version or 'missing'}; "
                 "run-02 was built with bpy 5.0.1 on Python 3.11 (needed at P4)"))

    data_dir = Path(os.environ.get("SHOWME_DATA_DIR", REPO_ROOT / "data"))
    rows.append((False, data_dir.exists(), "SHOWME_DATA_DIR",
                 f"{data_dir} ({'exists' if data_dir.exists() else 'created at P2'})"))

    for name in PROVIDER_ENV_VARS:
        present = bool(os.environ.get(name))
        rows.append((False, True, f"credential {name}",
                     ("present" if present else "absent")
                     + "; paid use still needs an approved manifest"))

    secrets = embedded_secrets()
    rows.append((True, not secrets, "no embedded credentials",
                 ", ".join(secrets) if secrets else "none found in code"))

    failed = False
    for required, ok, label, detail in rows:
        mark = "ok  " if ok else ("FAIL" if required else "info")
        failed = failed or (required and not ok)
        print(f"[{mark}] {label}: {detail}")
    print("doctor: " + ("missing required items" if failed else "required items present"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
