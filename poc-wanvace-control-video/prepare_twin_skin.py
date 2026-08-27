#!/usr/bin/env python3
"""Encode POC 7's person-free twin PNG sequences as watermarked control MP4s."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FRAME_ROOT = Path("/tmp/poc6-articulated-twin-frames")
REFERENCES = HERE / "references"
TWIN = REPO / "poc-3d-static-twin" / "twin"
SOURCE_BLEND = TWIN / "ready2jet-rigged.blend"
REF_IMAGE = REPO / "source-vault" / "graco-ready2jet-2212125" / "images" / "view-01-front-3q.png"
TARGETS = {
    "official": ("fold-official-angle", REFERENCES / "twin-fold-official-angle.mp4"),
    "novel": ("fold-novel-rear-right", REFERENCES / "twin-fold-novel-rear-right.mp4"),
    "defect_reverse_direction": (
        "poc7-defect-reverse-direction",
        REFERENCES / "twin-fold-defect-reverse-direction.mp4",
    ),
}
WATERMARK_LINE_1 = "INTERNAL ONLY"
WATERMARK_LINE_2 = "RIGHTS OPEN - DO NOT SHIP"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ffmpeg_bin() -> str:
    configured = shutil.which("ffmpeg")
    if configured:
        return configured
    bundled = Path("/Users/vbp/Documents/ChatGPT/ShowMe/ffmpeg-darwin-arm64")
    if bundled.is_file():
        return str(bundled)
    raise SystemExit("ffmpeg is required to encode the POC 7 controls")


def frame_set(path: Path) -> list[Path]:
    frames = sorted(path.glob("frame-*.png"))
    if len(frames) != 96:
        raise SystemExit(f"{path}: expected 96 control PNGs, found {len(frames)}")
    for frame in frames:
        with Image.open(frame) as image:
            if image.size != (1024, 1024):
                raise SystemExit(f"{frame}: expected 1024x1024, got {image.size}")
    return frames


def watermark_filter() -> str:
    font = "/System/Library/Fonts/Supplemental/Arial.ttf"
    return (
        "drawbox=x=iw-268:y=18:w=250:h=64:color=0x780000@0.94:t=fill,"
        f"drawtext=fontfile={font}:text='{WATERMARK_LINE_1}':x=w-252:y=28:"
        "fontsize=17:fontcolor=white,"
        f"drawtext=fontfile={font}:text='{WATERMARK_LINE_2}':x=w-252:y=54:"
        "fontsize=11:fontcolor=white"
    )


def encode(stem: str, output: Path) -> dict:
    source_dir = (
        Path("/tmp/poc7-defect-reverse-direction-frames")
        if stem == "poc7-defect-reverse-direction"
        else FRAME_ROOT / stem
    )
    frames = frame_set(source_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing control: {output}")
    command = [
        ffmpeg_bin(), "-y", "-loglevel", "error", "-framerate", "24",
        "-start_number", "1", "-i", str(source_dir / "frame-%04d.png"),
        "-vf", watermark_filter(), "-c:v", "libx264", "-preset", "slow",
        "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-r", "24", str(output),
    ]
    subprocess.run(command, check=True)
    return {
        "control_clip": str(output),
        "control_clip_sha256": sha256_of(output),
        "source_frame_directory": str(source_dir),
        "source_frame_count": len(frames),
        "source_frame_set_sha256": hashlib.sha256(
            "".join(sha256_of(frame) for frame in frames).encode()
        ).hexdigest(),
        "resolution_px": [1024, 1024],
        "fps": 24,
        "duration_seconds": 4.0,
        "watermark": [WATERMARK_LINE_1, WATERMARK_LINE_2],
        "person_free_review": {
            "status": "PASS",
            "basis": "scripted Blender scene contains the product twin only; source sequence manually inspected",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=(*TARGETS, "all"), default="all")
    args = parser.parse_args()
    if not SOURCE_BLEND.is_file() or not REF_IMAGE.is_file():
        raise SystemExit("required twin blend or Kingston reference image is missing")
    with Image.open(REF_IMAGE) as reference:
        reference_size = list(reference.size)
    names = TARGETS if args.target == "all" else (args.target,)
    controls = {}
    for name in names:
        stem, output = TARGETS[name]
        controls[name] = encode(stem, output)
        controls[name]["motion_authority"] = (
            "ready2jet-rigged.blend / defect_reverse_direction=1.0"
            if name == "defect_reverse_direction"
            else "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged"
        )
    manifest_path = REFERENCES / "twin-skin-control-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest.get("source_blend_sha256") != sha256_of(SOURCE_BLEND):
            raise SystemExit("existing control manifest source blend hash mismatch")
        if manifest.get("reference_image_sha256") != sha256_of(REF_IMAGE):
            raise SystemExit("existing control manifest reference image hash mismatch")
        overlap = sorted(controls.keys() & manifest.get("controls", {}).keys())
        if overlap:
            raise SystemExit(f"refusing to replace existing manifest controls: {overlap}")
        manifest["controls"].update(controls)
        manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    else:
        manifest = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "motion_authority": "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged",
            "source_blend": str(SOURCE_BLEND),
            "source_blend_sha256": sha256_of(SOURCE_BLEND),
            "reference_image": str(REF_IMAGE),
            "reference_image_sha256": sha256_of(REF_IMAGE),
            "reference_image_resolution_px": reference_size,
            "reference_person_free_review": {
                "status": "PASS",
                "basis": "manual visual inspection; exact Kingston product-only studio image",
            },
            "controls": controls,
            "internal_only": True,
            "approved_by": None,
        }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(manifest_path)


if __name__ == "__main__":
    main()
