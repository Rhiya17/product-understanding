"""Extract the deterministic Ready2Jet fold-study frame set.

The source remains read-only.  Frames are selected by integer index so the
Stage A kinematics evidence can be reproduced without timestamp seeking drift.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
VIDEO = (
    HERE.parent.parent
    / "source-vault"
    / "graco-ready2jet-2212125"
    / "videos"
    / "official-fold-video.mp4"
)
OUT = HERE / "fold-study-frames"
VIDEO_SHA256 = "9b1af25362a0b78187c6a4ced7228abcbbf5886e3617356277958392233af0fa"

# Frame index -> observable event.  Source is 29.97002997 fps, 1920x1080.
FRAMES = {
    488: "canopy collapse in progress",
    611: "canopy collapsed before mechanism release",
    731: "front caster alignment close-up",
    1127: "thumb switch and squeeze lever close-up",
    1153: "release controls held at end of close-up",
    1166: "wide open pose immediately before automatic motion",
    1173: "first observable frame/seat motion",
    1180: "mid-fold handle and front-leg convergence",
    1186: "near-fold wheelbase collapse",
    1193: "first self-standing folded pose",
    1206: "settled and secure folded pose",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    digest = sha256(VIDEO)
    if digest != VIDEO_SHA256:
        sys.exit(f"video hash mismatch: {digest}")

    import cv2

    capture = cv2.VideoCapture(str(VIDEO))
    fps = capture.get(cv2.CAP_PROP_FPS)
    OUT.mkdir(parents=True, exist_ok=True)
    index = {
        "source": str(VIDEO.relative_to(HERE.parent.parent)),
        "source_sha256": digest,
        "fps": fps,
        "frames": [],
    }
    for frame_index, event in FRAMES.items():
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ok, frame = capture.read()
        if not ok:
            sys.exit(f"could not read frame {frame_index}")
        elapsed = frame_index / fps
        name = f"frame-{frame_index:04d}-{elapsed:06.3f}s.png"
        target = OUT / name
        if not cv2.imwrite(str(target), frame):
            sys.exit(f"could not write {target}")
        index["frames"].append(
            {
                "frame": frame_index,
                "seconds": round(elapsed, 6),
                "file": name,
                "sha256": sha256(target),
                "event": event,
            }
        )
    capture.release()
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"wrote {len(FRAMES)} frames and index -> {OUT}")


if __name__ == "__main__":
    main()
