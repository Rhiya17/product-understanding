#!/usr/bin/env python3
"""CI gate: the LLD markdown and its HTML rendering must agree on version.

This session's history shows the md/html pair drifts when edited by hand.
The check is cheap: extract '**Version:** X.Y' from low-level-design.md and
require the same version string in the three places the HTML displays it
(TOC title, header chip, footer citation).

Exit 0 = in sync, 1 = drift (prints what disagrees).
"""
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs" / "architecture"

def main() -> int:
    md = (DOCS / "low-level-design.md").read_text()
    html = (DOCS / "low-level-design.html").read_text()

    m = re.search(r"\*\*Version:\*\*\s*([0-9.]+)", md)
    if not m:
        print("could not find version in low-level-design.md")
        return 1
    version = m.group(1)

    required = [
        (f"ShowMe LLD v{version}", "TOC title"),
        (f"<strong>Version</strong> {version}", "header chip"),
        (f"(v{version},", "footer citation"),
    ]
    failures = [where for needle, where in required if needle not in html]

    if failures:
        print(f"LLD markdown is v{version} but the HTML disagrees at: {', '.join(failures)}")
        return 1
    print(f"LLD md/html in sync at v{version}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
