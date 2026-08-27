"""Offline validator for the persisted Stage S render/report artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
RIGHTS_NOTE = "Tripo3D license check OPEN — do not ship"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    errors = []
    motion = json.loads((HERE / "validation-stage-s.json").read_text())
    stretch = json.loads((HERE / "stretch-qa-stage-s.json").read_text())
    render = json.loads((HERE / "renders" / "skinned-render-manifest.json").read_text())
    if motion.get("status") != "PASS" or motion.get("max_joint_angle_error_rad", 1) > 1e-4:
        errors.append("motion validation is not a ≤1e-4 rad PASS")
    if stretch.get("status") != "MEASURED" or stretch.get("frame_count") != 96:
        errors.append("stretch QA is missing or incomplete")
    if not stretch.get("severe_joint_count"):
        errors.append("stretch report must honestly retain severe fused-shell flags")
    if render.get("rights_note") != RIGHTS_NOTE or render.get("approved_by") is not None or render.get("internal_only") is not True:
        errors.append("render-manifest rights/approval guard changed")

    required = {"skinned-fold-official-angle", "skinned-fold-novel-rear-right"}
    if set(render.get("renders", {})) != required:
        errors.append("required Stage S camera renders are missing")
    for stem in sorted(required):
        entry = render.get("renders", {}).get(stem, {})
        path = HERE / "renders" / entry.get("file", "")
        if not path.is_file():
            errors.append(f"{stem}: GIF missing")
            continue
        if sha256(path) != entry.get("sha256"):
            errors.append(f"{stem}: GIF hash mismatch")
        with Image.open(path) as image:
            if image.size != (1024, 1024) or image.n_frames < 2:
                errors.append(f"{stem}: GIF must be animated at 1024px")
        if entry.get("rights_note") != RIGHTS_NOTE or entry.get("approved_by") is not None:
            errors.append(f"{stem}: rights or approval guard changed")

    contact = HERE / "verification" / "skinned-fold-pose-contact-sheet.png"
    if not contact.is_file():
        errors.append("five-pose contact sheet missing")
    else:
        with Image.open(contact) as image:
            if image.size != (1536, 2324):
                errors.append(f"contact sheet has unexpected size {image.size}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "motion_max_error_rad": motion.get("max_joint_angle_error_rad"),
        "stretch_severe_joint_count": stretch.get("severe_joint_count"),
        "render_count": len(render.get("renders", {})),
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
