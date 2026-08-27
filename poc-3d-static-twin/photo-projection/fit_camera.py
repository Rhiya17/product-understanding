"""Fit and finalize the binding per-image silhouette camera gate.

The preliminary phase selects a 3-D angle and solves distance plus sensor
shift.  Blender then renders that exact solved camera.  The finalize phase
measures the unmodified final render against the source product mask; only
that value controls the IoU >= 0.75 projection decision.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text())
RESOLUTION = 256


def stem(source_id: str) -> str:
    return source_id.replace("#", "-").replace("/", "-")


def state_dir(lane: str, state: str | None) -> Path:
    base = HERE / lane
    return base / state if state else base


def read_mask(path: Path, alpha: bool = False) -> np.ndarray:
    image = Image.open(path).convert("RGBA" if alpha else "L")
    channel = image.getchannel("A") if alpha else image
    channel = channel.resize((RESOLUTION, RESOLUTION), Image.Resampling.LANCZOS)
    return (np.asarray(channel, dtype=np.uint8) >= 96).astype(np.uint8)


def iou(left: np.ndarray, right: np.ndarray) -> float:
    intersection = int(np.logical_and(left, right).sum())
    union = int(np.logical_or(left, right).sum())
    return intersection / union if union else 0.0


def centroid(mask: np.ndarray) -> tuple[float, float]:
    moments = cv2.moments(mask.astype(np.uint8))
    if moments["m00"] == 0:
        return RESOLUTION / 2, RESOLUTION / 2
    return moments["m10"] / moments["m00"], moments["m01"] / moments["m00"]


def fit_2d(raw: np.ndarray, target: np.ndarray) -> dict:
    center = (RESOLUTION - 1) / 2
    target_center = centroid(target)
    best = {"iou": -1.0}
    for scale in np.linspace(0.55, 2.35, 91):
        base = np.array([[scale, 0, (1 - scale) * center],
                         [0, scale, (1 - scale) * center]], dtype=np.float32)
        scaled = cv2.warpAffine(raw, base, (RESOLUTION, RESOLUTION), flags=cv2.INTER_NEAREST)
        scaled_center = centroid(scaled)
        dx = target_center[0] - scaled_center[0]
        dy = target_center[1] - scaled_center[1]
        transform = np.array([[1, 0, dx], [0, 1, dy]], dtype=np.float32)
        fitted = cv2.warpAffine(scaled, transform, (RESOLUTION, RESOLUTION), flags=cv2.INTER_NEAREST)
        score = iou(fitted, target)
        if score > best["iou"]:
            best = {"iou": score, "scale": float(scale), "translation_px": [float(dx), float(dy)]}
    # Small deterministic refinement around the winning scale/centroid.
    coarse_scale = best["scale"]
    for scale in np.linspace(max(0.5, coarse_scale - 0.035), coarse_scale + 0.035, 15):
        base = np.array([[scale, 0, (1 - scale) * center],
                         [0, scale, (1 - scale) * center]], dtype=np.float32)
        scaled = cv2.warpAffine(raw, base, (RESOLUTION, RESOLUTION), flags=cv2.INTER_NEAREST)
        scaled_center = centroid(scaled)
        align_x = target_center[0] - scaled_center[0]
        align_y = target_center[1] - scaled_center[1]
        for offset_y in range(-3, 4):
            for offset_x in range(-3, 4):
                dx, dy = align_x + offset_x, align_y + offset_y
                transform = np.array([[1, 0, dx], [0, 1, dy]], dtype=np.float32)
                fitted = cv2.warpAffine(scaled, transform, (RESOLUTION, RESOLUTION), flags=cv2.INTER_NEAREST)
                score = iou(fitted, target)
                if score > best["iou"]:
                    best = {"iou": score, "scale": float(scale), "translation_px": [float(dx), float(dy)]}
    return best


def prepared_sources(lane: str) -> dict[str, dict]:
    document = json.loads((HERE / lane / "source-preparation.json").read_text())
    return {source["source_id"]: source for source in document["sources"]}


def preliminary(lane: str, state: str | None) -> None:
    directory = state_dir(lane, state) / "camera-gates"
    raw = json.loads((directory / "raw-attempts.json").read_text())
    prepared = prepared_sources(lane)
    selected = {}
    all_attempts = {}
    for source_id, attempts in raw["attempts"].items():
        target = read_mask(ROOT / prepared[source_id]["mask_local_path"])
        scored = []
        for attempt in attempts:
            rendered = read_mask(ROOT / attempt["mask_local_path"], alpha=True)
            fit = fit_2d(rendered, target)
            scored.append({**attempt, "predicted_fit_iou": round(fit["iou"], 6),
                           "image_scale": fit["scale"], "translation_px": fit["translation_px"]})
        scored.sort(key=lambda item: item["predicted_fit_iou"], reverse=True)
        all_attempts[source_id] = scored
        winner = scored[0]
        scale = winner["image_scale"]
        dx, dy = winner["translation_px"]
        selected[source_id] = {
            "source_id": source_id,
            "selected_raw_mask_local_path": winner["mask_local_path"],
            "predicted_fit_iou": winner["predicted_fit_iou"],
            "azimuth_deg": winner["azimuth_deg"],
            "elevation_deg": winner["elevation_deg"],
            "lens_mm": winner["lens_mm"],
            "base_distance_m": winner["base_distance_m"],
            "fitted_distance_m": winner["base_distance_m"] / scale,
            "target_xyz_m": winner["target_xyz_m"],
            "image_scale": scale,
            "translation_px": [dx, dy],
            # Perspective sensor shift is the exact Blender-side translation
            # knob; distance supplies scale.  Sign conventions are verified by
            # the mandatory final render rather than trusted analytically.
            "shift_x": -dx / RESOLUTION,
            "shift_y": dy / RESOLUTION,
        }
    output = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "angle grid + deterministic distance/sensor-shift fit; final Blender render is authoritative",
        "resolution_px": [RESOLUTION, RESOLUTION],
        "all_attempts": all_attempts,
        "selected": selected,
    }
    (directory / "camera-fits-preliminary.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({key: value["predicted_fit_iou"] for key, value in selected.items()}, indent=2))


def finalize(lane: str, state: str | None) -> None:
    directory = state_dir(lane, state) / "camera-gates"
    preliminary_doc = json.loads((directory / "camera-fits-preliminary.json").read_text())
    final_doc = json.loads((directory / "final-renders.json").read_text())
    prepared = prepared_sources(lane)
    threshold = float(CONFIG["camera_gate_iou"])
    matches = {}
    for source_id, rendered_record in final_doc["renders"].items():
        target = read_mask(ROOT / prepared[source_id]["mask_local_path"])
        rendered = read_mask(ROOT / rendered_record["mask_local_path"], alpha=True)
        score = iou(rendered, target)
        preliminary_fit = preliminary_doc["selected"][source_id]
        matches[source_id] = {
            "source_id": source_id,
            "status": "PASS" if score >= threshold else "FAIL",
            "silhouette_iou": round(score, 6),
            "gate_threshold": threshold,
            "camera_type": "PERSP",
            "focal_length_mm": rendered_record["focal_length_mm"],
            "position_xyz_m": rendered_record["position_xyz_m"],
            "rotation_euler_rad": rendered_record["rotation_euler_rad"],
            "azimuth_deg": preliminary_fit["azimuth_deg"],
            "elevation_deg": preliminary_fit["elevation_deg"],
            "distance_m": preliminary_fit["fitted_distance_m"],
            "target_xyz_m": preliminary_fit["target_xyz_m"],
            "shift_x": rendered_record["shift_x"],
            "shift_y": rendered_record["shift_y"],
            "target_mask_local_path": prepared[source_id]["mask_local_path"],
            "rendered_mask_local_path": rendered_record["mask_local_path"],
            "projection_eligible": score >= threshold,
        }
    output = {
        "schema_version": 1,
        "lane": CONFIG["lanes"][lane]["lane"],
        "state": state,
        "finalized_at": datetime.now(timezone.utc).isoformat(),
        "gate_threshold": threshold,
        "measurement": "pixel IoU of unmodified final Blender RGBA silhouette vs official-image product mask at 256x256",
        "all_angle_attempts_file": str((directory / "camera-fits-preliminary.json").relative_to(ROOT)),
        "matches": matches,
    }
    (directory / "camera-matches.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({key: {"status": value["status"], "iou": value["silhouette_iou"]}
                      for key, value in matches.items()}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=("ready2jet", "levoit", "macbook", "bose"))
    parser.add_argument("--state", choices=("open", "closed"))
    parser.add_argument("--phase", required=True, choices=("preliminary", "finalize"))
    args = parser.parse_args()
    if args.lane != "macbook" and args.state:
        raise SystemExit("--state only applies to macbook")
    if args.phase == "preliminary":
        preliminary(args.lane, args.state)
    else:
        finalize(args.lane, args.state)


if __name__ == "__main__":
    main()
