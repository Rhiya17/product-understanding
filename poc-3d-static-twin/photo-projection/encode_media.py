"""Encode stamped Blender frames into internal-only GIFs and QA sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def state_dir(lane: str, state: str | None) -> Path:
    base = HERE / lane
    return base / state if state else base


def watermark_pixel_check(frame: Image.Image) -> bool:
    rgb = np.asarray(frame.convert("RGB"), dtype=np.uint8)
    header = rgb[:48, :700]
    red = (header[:, :, 0] > 180) & (header[:, :, 1] < 130) & (header[:, :, 2] < 110)
    return int(red.sum()) >= 500


def contact_sheet(frames: list[Image.Image], labels: list[str], output: Path) -> None:
    indices = [round(index * (len(frames) - 1) / 5) for index in range(6)]
    tile_size = 360
    header = 42
    sheet = Image.new("RGB", (tile_size * 3, (tile_size + header) * 2), (32, 35, 40))
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    draw = ImageDraw.Draw(sheet)
    for slot, index in enumerate(indices):
        image = frames[index].copy()
        image.thumbnail((tile_size, tile_size), Image.Resampling.LANCZOS)
        x = (slot % 3) * tile_size
        y = (slot // 3) * (tile_size + header)
        sheet.paste(image, (x + (tile_size - image.width) // 2, y + header))
        draw.text((x + 10, y + 10), labels[index], fill="white", font=font)
    sheet.save(output, optimize=True)


def encode(lane: str, state: str | None) -> None:
    directory = state_dir(lane, state)
    frame_manifest = json.loads((directory / "frame-manifest.json").read_text())
    output_records = {}
    for target, record in frame_manifest["outputs"].items():
        paths = sorted(Path(record["frames_dir"]).glob("frame-*.png"))
        if len(paths) != record["frame_count"]:
            raise SystemExit(f"{target}: expected {record['frame_count']} frames, found {len(paths)}")
        source_frames = [Image.open(path).convert("RGB") for path in paths]
        if any(frame.size != (1024, 1024) for frame in source_frames):
            raise SystemExit(f"{target}: source frame is not 1024x1024")
        if not all(watermark_pixel_check(frame) for frame in source_frames):
            raise SystemExit(f"{target}: visible watermark pixel check failed")
        if record["frame_count"] > 24:
            selected_indices = list(range(0, record["frame_count"], 3))
            if selected_indices[-1] != record["frame_count"] - 1:
                selected_indices.append(record["frame_count"] - 1)
        else:
            selected_indices = list(range(record["frame_count"]))
        selected = [source_frames[index] for index in selected_indices]
        quantized = [
            frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            for frame in selected
        ]
        gif_path = directory / f"{target}-internal-only.gif"
        quantized[0].save(
            gif_path, save_all=True, append_images=quantized[1:], duration=125,
            loop=0, optimize=True, disposal=2,
        )
        sheet_path = directory / f"{target}-qa-contact-sheet.png"
        contact_sheet(source_frames, [path.name for path in paths], sheet_path)
        output_records[target] = {
            "gif_local_path": str(gif_path.relative_to(ROOT)),
            "gif_sha256": sha256(gif_path),
            "qa_contact_sheet_local_path": str(sheet_path.relative_to(ROOT)),
            "qa_contact_sheet_sha256": sha256(sheet_path),
            "source_frame_count": len(paths),
            "encoded_frame_count": len(selected),
            "resolution_px": [1024, 1024],
            "watermark_pixel_check": "PASS",
        }
        for frame in (*source_frames, *quantized):
            frame.close()
    blend = directory / f"{lane}{'-' + state if state else ''}-photo-projected.blend"
    manifest = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "geometry_blend_local_path": str(blend.relative_to(ROOT)),
        "geometry_blend_sha256": sha256(blend),
        "camera_matches_local_path": str((directory / "camera-gates/camera-matches.json").relative_to(ROOT)),
        "coverage_local_path": str((directory / "coverage.json").relative_to(ROOT)),
        "source_preparation_local_path": str((HERE / lane / "source-preparation.json").relative_to(ROOT)),
        "scripts": [
            "poc-3d-static-twin/photo-projection/prepare_sources.py",
            "poc-3d-static-twin/photo-projection/blender_pipeline.py",
            "poc-3d-static-twin/photo-projection/fit_camera.py",
            "poc-3d-static-twin/photo-projection/encode_media.py"
        ],
        "watermark": CONFIG["watermark"],
        "appearance_policy": "hash-verified manufacturer imagery only; neutral fallback",
        "rights_note": "Manufacturer imagery cleared for internal research only; reuse rights review OPEN — do not ship",
        "tripo_texture_ancestry": False,
        "approved_by": None,
        "internal_only": True,
        "external_spend_usd": 0,
        "outputs": output_records,
    }
    (directory / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(output_records, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=("ready2jet", "levoit", "macbook", "bose"))
    parser.add_argument("--state", choices=("open", "closed"))
    args = parser.parse_args()
    encode(args.lane, args.state)


if __name__ == "__main__":
    main()
