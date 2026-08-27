"""Watermark and encode a 24-frame catalog scan turntable as an internal GIF."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RIGHTS = "Tripo3D license check OPEN — do not ship"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-dir", type=Path, required=True)
    parser.add_argument("--frames", type=Path, required=True)
    args = parser.parse_args()
    paths = sorted(args.frames.glob("frame-*.png"))
    if len(paths) != 24:
        raise SystemExit(f"expected exactly 24 frames, found {len(paths)}")
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    images = []
    for path in paths:
        frame = Image.open(path).convert("RGB")
        draw = ImageDraw.Draw(frame, "RGBA")
        draw.rounded_rectangle((18, 18, 610, 98), radius=10, fill=(120, 0, 0, 255))
        draw.text((34, 26), "INTERNAL ONLY", font=font, fill="white")
        draw.text((34, 61), "Tripo3D license check OPEN — do not ship", font=small, fill="white")
        frame.save(path, optimize=True)
        images.append(frame)
    output = args.product_dir / "turntable-internal-only.gif"
    images[0].save(output, save_all=True, append_images=images[1:], duration=120,
                   loop=0, optimize=True, disposal=2)
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "frame_count": 24,
        "resolution_px": [1024, 1024],
        "gif": output.name,
        "gif_sha256": sha256_of(output),
        "frames_dir": str(args.frames.relative_to(args.product_dir)),
        "frame_sha256": [{"file": p.name, "sha256": sha256_of(p)} for p in paths],
        "rights_note": RIGHTS,
        "approved_by": None,
        "internal_only": True,
    }
    (args.product_dir / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
