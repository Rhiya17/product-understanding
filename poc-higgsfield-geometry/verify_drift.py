"""Measure how far a generated video drifts from its start frame (POC).

This is a *proxy* verifier: because we authored the start frame from verified
geometry, "the placement stayed correct" reduces to "the object didn't move,
scale, or morph relative to frame 0." That is measurable. Recovering metric
dimensions from arbitrary generated pixels (what the HLD asks the verifier to
do) is not — this script is also the demonstration of that gap.

Usage:
    python verify_drift.py out/video.mp4
Requires ffmpeg on PATH.
"""

import subprocess
import sys
from pathlib import Path

import numpy as np
import matplotlib.image as mpimg


def extract_frames(video: Path, outdir: Path, fps: int = 2) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
         "-vf", f"fps={fps}", str(outdir / "frame_%03d.png")],
        check=True,
    )
    return sorted(outdir.glob("frame_*.png"))


def drift_curve(frames: list[Path]) -> list[float]:
    ref = mpimg.imread(frames[0]).astype(np.float32)
    curve = []
    for f in frames:
        img = mpimg.imread(f).astype(np.float32)
        if img.shape != ref.shape:
            img = img[: ref.shape[0], : ref.shape[1]]
        curve.append(float(np.mean(np.abs(img - ref))))
    return curve


if __name__ == "__main__":
    video = Path(sys.argv[1])
    frames = extract_frames(video, video.parent / f"{video.stem}_frames")
    curve = drift_curve(frames)
    print("mean-abs-diff vs frame 0 (camera motion inflates this — judge the")
    print("object region by eye alongside the numbers):")
    for i, v in enumerate(curve):
        bar = "#" * int(v * 200)
        print(f"  t={i / 2:4.1f}s  {v:.4f}  {bar}")
    print(f"\nfinal-frame drift: {curve[-1]:.4f}")
    print("Interpretation is manual for the POC: open the frames dir and check —")
    print("did the box stay put, keep its proportions, and keep its edges?")
