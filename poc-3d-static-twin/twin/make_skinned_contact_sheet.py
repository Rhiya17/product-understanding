"""Build the Stage S rendered-vs-official five-pose contact sheet."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
OFFICIAL = HERE.parent / "evaluation" / "fold-study-frames"
RENDERED = HERE / "verification" / "skinned-rendered-official-frames"
OUT = HERE / "verification" / "skinned-fold-pose-contact-sheet.png"
PAIRS = [
    ("OPEN / RELEASED", "frame-1166-38.906s.png", "render-0048.png"),
    ("FIRST MOTION", "frame-1173-39.139s.png", "render-0057.png"),
    ("MID FOLD", "frame-1180-39.373s.png", "render-0066.png"),
    ("NEAR FOLDED", "frame-1186-39.573s.png", "render-0075.png"),
    ("FOLDED", "frame-1193-39.806s.png", "render-0084.png"),
]


def fitted(image, size):
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (245, 245, 245))
    canvas.paste(copy, ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2))
    return canvas


def main() -> None:
    font = ImageFont.load_default()
    width = 1536
    header = 64
    row_height = 452
    sheet = Image.new("RGB", (width, header + row_height * len(PAIRS)), (28, 31, 35))
    draw = ImageDraw.Draw(sheet)
    draw.text((20, 14), "OFFICIAL VIDEO (LEFT) | PHOTO-DERIVED SKIN ON VERIFIED RIG (RIGHT)", fill="white", font=font)
    draw.text((20, 34), "INTERNAL ONLY — TRIPO3D LICENSE CHECK OPEN — FUSED-SHELL STRETCH DISCLOSED IN stretch-qa-stage-s.md", fill=(255, 110, 70), font=font)
    for index, (label, official_name, rendered_name) in enumerate(PAIRS):
        y = header + index * row_height
        with Image.open(OFFICIAL / official_name) as official_source:
            official = fitted(official_source.convert("RGB"), (768, 432))
        with Image.open(RENDERED / rendered_name) as rendered_source:
            rendered = fitted(rendered_source.convert("RGB"), (768, 432))
        sheet.paste(official, (0, y + 20))
        sheet.paste(rendered, (768, y + 20))
        draw.rectangle((0, y, width, y + 20), fill=(28, 31, 35))
        draw.text((10, y + 4), label, fill="white", font=font)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, optimize=True)
    print(f"wrote {OUT} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
