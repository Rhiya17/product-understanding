#!/usr/bin/env python3
"""Create the Stage B audit contact sheet from official and rendered stills."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "out" / "gate1"
WIDTH = 1280
CELL_HEIGHT = 420
LABEL_HEIGHT = 58


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contain(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (32, 34, 39))
    canvas.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return canvas


def main() -> None:
    rows = [
        (
            "Bose official evidence",
            ROOT / "source-vault/bose-qc-ultra-headphones/images/black-earcup-controls-wired-35mm.png",
            "Bose repaired twin - attempt 1 - PASS",
            OUT / "attempt-1/bose.png",
        ),
        (
            "MacBook official right side",
            ROOT / "source-vault/apple-macbook-air-13-m3/images/guide-right-side-headphone-jack.png",
            "MacBook repaired twin - attempt 1 - FAIL",
            OUT / "attempt-1/macbook.png",
        ),
        (
            "MacBook official right side",
            ROOT / "source-vault/apple-macbook-air-13-m3/images/guide-right-side-headphone-jack.png",
            "MacBook repaired twin - attempt 2 - FAIL",
            OUT / "attempt-2/macbook.png",
        ),
    ]
    for row in rows:
        for path in (row[1], row[3]):
            if not path.is_file():
                raise SystemExit(f"missing contact-sheet input: {path}")

    sheet = Image.new("RGB", (WIDTH, len(rows) * (CELL_HEIGHT + LABEL_HEIGHT) + 64), (18, 19, 23))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=24)
    small = ImageFont.load_default(size=18)
    draw.text((24, 17), "POC 8 - GATE 1 - INTERNAL ONLY", fill=(255, 95, 90), font=font)

    cell_width = WIDTH // 2
    y = 64
    inputs = []
    for left_label, left_path, right_label, right_path in rows:
        draw.rectangle((0, y, WIDTH, y + LABEL_HEIGHT), fill=(41, 44, 52))
        draw.text((18, y + 16), left_label, fill=(235, 235, 238), font=small)
        verdict_color = (120, 230, 150) if right_label.endswith("PASS") else (255, 115, 110)
        draw.text((cell_width + 18, y + 16), right_label, fill=verdict_color, font=small)
        y += LABEL_HEIGHT
        sheet.paste(contain(left_path, (cell_width, CELL_HEIGHT)), (0, y))
        sheet.paste(contain(right_path, (cell_width, CELL_HEIGHT)), (cell_width, y))
        draw.line((cell_width, y, cell_width, y + CELL_HEIGHT), fill=(90, 93, 102), width=2)
        inputs.extend((left_path, right_path))
        y += CELL_HEIGHT

    output = OUT / "contact-sheet.png"
    sheet.save(output, optimize=True)
    manifest = {
        "artifact": str(output.relative_to(ROOT)),
        "sha256": sha256(output),
        "inputs": [{"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in inputs],
        "watermark": "POC 8 - GATE 1 - INTERNAL ONLY",
        "internal_only": True,
        "approved_by": None,
    }
    (OUT / "contact-sheet.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
