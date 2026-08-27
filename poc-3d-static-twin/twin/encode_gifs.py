"""Encode Stage D Blender PNG sequences as 1024px internal-only GIFs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
FRAME_ROOT = Path("/tmp/poc6-articulated-twin-frames")
OUT = HERE / "renders"
MANIFEST = OUT / "render-manifest.json"
TARGETS = ("open-turntable", "fold-official-angle", "fold-novel-rear-right")


def encode(stem):
    files = sorted((FRAME_ROOT / stem).glob("frame-*.png"))
    expected = 72 if stem == "open-turntable" else 96
    if len(files) != expected:
        raise SystemExit(f"{stem}: expected {expected} PNGs, found {len(files)}")
    selected = files[::3]
    if selected[-1] != files[-1]:
        selected.append(files[-1])
    source_frames = [Image.open(path).convert("RGB") for path in selected]
    if any(frame.size != (1024, 1024) for frame in source_frames):
        raise SystemExit(f"{stem}: at least one source frame is not 1024x1024")
    frames = [
        frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for frame in source_frames
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / f"{stem}.gif"
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0,
        optimize=True,
        disposal=2,
    )
    with Image.open(output) as encoded:
        encoded_frame_count = encoded.n_frames
    for frame in (*frames, *source_frames):
        frame.close()
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"schema_version": 1, "internal_only": True, "external_spend_usd": 0, "renders": {}}
    manifest["renders"][stem] = {
        "file": output.name,
        "resolution_px": [1024, 1024],
        "source_frame_count": expected,
        "source_fps": 24,
        "selected_frame_count": len(frames),
        "encoded_frame_count": encoded_frame_count,
        "encoded_frame_step": 3,
        "encoded_frame_duration_ms": 125,
        "format_reason": "GIF is an allowed work-order format and was used because the installed Blender build has no FFmpeg codec and no local system encoder is present.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"encoded {output} ({output.stat().st_size} bytes, {encoded_frame_count} GIF frames from {expected} source frames, 1024px)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=(*TARGETS, "all"), default="all")
    args = parser.parse_args()
    targets = TARGETS if args.target == "all" else (args.target,)
    for target in targets:
        encode(target)


if __name__ == "__main__":
    main()
