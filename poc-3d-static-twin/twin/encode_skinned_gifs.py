"""Encode Stage S 1024px PNG sequences as internal-only GIFs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
FRAME_ROOT = Path("/tmp/product-understanding-stage-s-frames")
OUT = HERE / "renders"
MANIFEST = OUT / "skinned-render-manifest.json"
TARGETS = ("skinned-fold-official-angle", "skinned-fold-novel-rear-right")
RIGHTS_NOTE = "Tripo3D license check OPEN — do not ship"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(stem: str) -> dict:
    files = sorted((FRAME_ROOT / stem).glob("frame-*.png"))
    if len(files) != 96:
        raise SystemExit(f"{stem}: expected 96 PNGs, found {len(files)}")
    selected = files[::3]
    if selected[-1] != files[-1]:
        selected.append(files[-1])
    source_frames = [Image.open(path).convert("RGB") for path in selected]
    if any(frame.size != (1024, 1024) for frame in source_frames):
        raise SystemExit(f"{stem}: source frame resolution is not 1024x1024")
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
        encoded_count = encoded.n_frames
        encoded_size = list(encoded.size)
    for frame in (*frames, *source_frames):
        frame.close()
    return {
        "file": output.name,
        "sha256": sha256(output),
        "resolution_px": encoded_size,
        "source_frame_count": 96,
        "source_fps": 24,
        "selected_frame_count": len(selected),
        "encoded_frame_count": encoded_count,
        "encoded_frame_step": 3,
        "encoded_frame_duration_ms": 125,
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
    }


def main() -> None:
    manifest = {
        "schema_version": 1,
        "source_blend": "ready2jet-skinned.blend",
        "motion_authority": "ready2jet-rigged.blend / Ready2Jet_Fold_Correct; unchanged",
        "rights_note": RIGHTS_NOTE,
        "approved_by": None,
        "internal_only": True,
        "external_spend_usd": 0,
        "renders": {},
    }
    for target in TARGETS:
        manifest["renders"][target] = encode(target)
        print(f"encoded {target}")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {MANIFEST}")


if __name__ == "__main__":
    main()
