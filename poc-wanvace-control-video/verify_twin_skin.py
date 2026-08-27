#!/usr/bin/env python3
"""Compute POC 7 silhouette IoU and build same-timestamp gate artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
POSE_FRACTIONS = (47 / 95, 56 / 95, 65 / 95, 74 / 95, 83 / 95)
MEAN_THRESHOLD = 0.80
MIN_THRESHOLD = 0.65


def atomic_json(path: Path, value: object) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def read_video(path: Path) -> tuple[list[np.ndarray], float]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"could not open {path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frames = []
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frames.append(frame)
    capture.release()
    if not frames:
        raise SystemExit(f"no frames decoded from {path}")
    return frames, fps


def product_mask(frame: np.ndarray) -> np.ndarray:
    height, width = frame.shape[:2]
    # Ignore the governed top-right watermark rectangle.
    work = frame.copy()
    raw_border = np.concatenate(
        (frame[-16:, :].reshape(-1, 3), frame[:, :16].reshape(-1, 3)), axis=0
    )
    work[: min(95, height // 4), int(width * 0.72) :] = np.median(raw_border, axis=0)
    border = np.concatenate(
        (
            work[-16:, :].reshape(-1, 3),
            work[:, :16].reshape(-1, 3),
            work[:, -16:].reshape(-1, 3),
        ),
        axis=0,
    )
    gray = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY)
    border_gray = cv2.cvtColor(border.reshape(-1, 1, 3), cv2.COLOR_BGR2GRAY).reshape(-1)
    # The fifth-percentile border is the darkest neutral backdrop tone. Staying
    # below it excludes both wall and floor while adapting to brighter VACE studios.
    foreground_ceiling = max(20.0, float(np.percentile(border_gray, 5)) - 8.0)
    mask = (gray < foreground_ceiling).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if count <= 1:
        return np.zeros((height, width), dtype=np.uint8)
    candidates = []
    for label in range(1, count):
        x, y, w, h, area = stats[label]
        if area >= height * width * 0.002 and y + h > height * 0.45:
            candidates.append((area, label))
    if not candidates:
        return np.zeros((height, width), dtype=np.uint8)
    largest = max(candidates)[1]
    return (labels == largest).astype(np.uint8)


def iou(left: np.ndarray, right: np.ndarray) -> float:
    intersection = np.logical_and(left, right).sum()
    union = np.logical_or(left, right).sum()
    return float(intersection / union) if union else 0.0


def correspondence(control_count: int, output_count: int) -> list[tuple[int, int]]:
    if min(control_count, output_count) < 2:
        raise SystemExit("motion gates cannot be computed with fewer than two frames")
    return [
        (index, round(index * (output_count - 1) / (control_count - 1)))
        for index in range(control_count)
    ]


def annotate(frame: np.ndarray, label: str, width: int = 480) -> Image.Image:
    height = round(frame.shape[0] * width / frame.shape[1])
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb).resize((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height + 34), "#1f2328")
    canvas.paste(image, (0, 34))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
    draw.text((10, 8), label, fill="white", font=font)
    return canvas


def make_contact_sheet(
    control_frames: list[np.ndarray], output_frames: list[np.ndarray], output: Path
) -> list[dict]:
    rows = []
    records = []
    for number, fraction in enumerate(POSE_FRACTIONS, start=1):
        ci = round(fraction * (len(control_frames) - 1))
        oi = round(fraction * (len(output_frames) - 1))
        left = annotate(control_frames[ci], f"POSE {number}  CONTROL  frame {ci + 1}")
        right = annotate(output_frames[oi], f"POSE {number}  VACE OUTPUT  frame {oi + 1}")
        row = Image.new("RGB", (left.width + right.width, left.height), "#1f2328")
        row.paste(left, (0, 0))
        row.paste(right, (left.width, 0))
        rows.append(row)
        records.append({"pose": number, "fraction": fraction, "control_frame": ci + 1, "output_frame": oi + 1})
    sheet = Image.new("RGB", (rows[0].width, sum(row.height for row in rows)), "#1f2328")
    y = 0
    for row in rows:
        sheet.paste(row, (0, y))
        y += row.height
    sheet.save(output, optimize=True)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    out_dir = HERE / "out" / args.label
    submission = json.loads((out_dir / "submission.json").read_text())
    control_path = Path(submission["inputs"]["control_clip"]["path"])
    output_path = out_dir / "video.mp4"
    control_frames, control_fps = read_video(control_path)
    output_frames, output_fps = read_video(output_path)

    pairs = correspondence(len(control_frames), len(output_frames))
    per_frame = []
    for control_index, output_index in pairs:
        control = control_frames[control_index]
        output = cv2.resize(output_frames[output_index], (control.shape[1], control.shape[0]), interpolation=cv2.INTER_AREA)
        score = iou(product_mask(control), product_mask(output))
        per_frame.append({
            "control_frame": control_index + 1,
            "output_frame": output_index + 1,
            "iou": round(score, 6),
        })
    scores = [row["iou"] for row in per_frame]
    mean_iou = float(np.mean(scores))
    min_iou = float(np.min(scores))
    silhouette_pass = mean_iou >= MEAN_THRESHOLD and min_iou >= MIN_THRESHOLD
    poses = make_contact_sheet(control_frames, output_frames, out_dir / "contact-sheet.png")
    verification_dir = out_dir / "verification"
    verification_dir.mkdir(exist_ok=True)
    record = {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "control": {"path": str(control_path), "num_frames": len(control_frames), "fps": control_fps},
        "output": {"path": str(output_path), "num_frames": len(output_frames), "fps": output_fps},
        "frame_correspondence": "normalized same-timestamp mapping from first to last frame",
        "silhouette_gate": {
            "mean_iou": round(mean_iou, 6),
            "minimum_iou": round(min_iou, 6),
            "mean_threshold": MEAN_THRESHOLD,
            "minimum_threshold": MIN_THRESHOLD,
            "pass": silhouette_pass,
            "segmentation": "dynamic neutral-background distance/luminance threshold, morphology, largest grounded component",
        },
        "pose_sequence_gate": {"status": "PENDING_MANUAL", "contact_sheet": "contact-sheet.png", "poses": poses},
        "identity_gate": {"status": "PENDING_MANUAL"},
        "all_serving_gates_pass": False,
        "trust_label_if_passed": "TWIN_RENDER_VACE_SKIN",
        "internal_only": True,
    }
    atomic_json(verification_dir / "silhouette-per-frame.json", per_frame)
    atomic_json(verification_dir / "gates.json", record)
    print(json.dumps(record["silhouette_gate"], indent=2))


if __name__ == "__main__":
    main()
