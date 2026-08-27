"""Validate Stage D render, comparison, measurement, report, and hours artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
OUT = HERE / "validation-stage-d.json"


def main():
    errors = []
    manifest = json.loads((HERE / "renders" / "render-manifest.json").read_text())
    expected = {
        "open-turntable": 72,
        "fold-official-angle": 96,
        "fold-novel-rear-right": 96,
    }
    render_checks = {}
    for stem, source_count in expected.items():
        entry = manifest.get("renders", {}).get(stem)
        if not entry:
            errors.append(f"render manifest missing {stem}")
            continue
        path = HERE / "renders" / entry["file"]
        if not path.exists() or path.stat().st_size < 100_000:
            errors.append(f"render missing or too small: {path}")
            continue
        with Image.open(path) as image:
            size = image.size
            frame_count = getattr(image, "n_frames", 1)
        if size != (1024, 1024):
            errors.append(f"{stem} is {size}, not 1024x1024")
        if entry.get("source_frame_count") != source_count:
            errors.append(f"{stem} source frame count is not {source_count}")
        if frame_count != entry.get("encoded_frame_count"):
            errors.append(f"{stem} GIF frame count disagrees with manifest")
        render_checks[stem] = {"bytes": path.stat().st_size, "size_px": size, "encoded_frames": frame_count, "source_frames": source_count}

    contact = HERE / "verification" / "fold-pose-contact-sheet.png"
    with Image.open(contact) as image:
        contact_size = image.size
    if contact_size != (1536, 2316):
        errors.append(f"contact sheet has unexpected size {contact_size}")
    for frame in (48, 57, 66, 75, 84):
        path = HERE / "verification" / "rendered-official-frames" / f"render-{frame:04d}.png"
        with Image.open(path) as image:
            if image.size != (1024, 1024):
                errors.append(f"verification frame {frame} is not 1024px")

    dimension = json.loads((HERE / "verification" / "dimension-check.json").read_text())
    if dimension.get("external_spend_usd") != 0 or dimension.get("internal_only") is not True:
        errors.append("dimension check violates spend/internal-only state")
    if dimension.get("open", {}).get("target_confidence") != "OFFICIAL":
        errors.append("open dimension confidence changed")
    if dimension.get("folded", {}).get("target_confidence") != "INFERRED":
        errors.append("folded dimension confidence changed")

    hours = json.loads((HERE / "hours.json").read_text())
    if set(hours.get("stages", {})) != {"A", "B", "C", "D"}:
        errors.append("hours log does not contain exactly stages A-D")
    if any(stage.get("external_spend_usd") != 0 for stage in hours.get("stages", {}).values()):
        errors.append("nonzero external spend in hours log")
    if abs(hours.get("total_hours", -1) - sum(stage["hours"] for stage in hours["stages"].values())) > 1e-6:
        errors.append("total hours do not sum")

    report = (HERE / "report.md").read_text()
    for phrase in ("INTERNAL ONLY", "`INFERRED` inventory", "$0 external spend", "+63.3%"):
        if phrase not in report:
            errors.append(f"report missing required disclosure: {phrase}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "render_checks": render_checks,
        "contact_sheet_size_px": contact_size,
        "matched_pose_count": 5,
        "open_dimension_error_percent_DWH": dimension["open"]["error_percent_DWH"],
        "folded_dimension_error_percent_DWH": dimension["folded"]["error_percent_DWH"],
        "folded_dimension_confidence": dimension["folded"]["target_confidence"],
        "total_hours": hours.get("total_hours"),
        "external_spend_usd": 0,
        "internal_only": True,
        "errors": errors,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
