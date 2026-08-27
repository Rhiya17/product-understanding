"""Hash-verify and mask official, person-free projection sources.

No source-vault file is changed.  RGB pixels in the derived RGBA textures are
copied byte-for-byte from the registered source after decoding; only alpha is
derived.  Masks are analytical geometry aids, not appearance inputs.

Usage:
  python3 prepare_sources.py --lane ready2jet [--ffmpeg PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_index(vault_slug: str) -> dict[str, dict]:
    manifest_path = ROOT / "source-vault" / vault_slug / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    return {source["source_id"]: source for source in manifest["sources"]}


def largest_components(mask: np.ndarray, minimum_share: float = 0.001) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if count <= 1:
        return mask.astype(np.uint8)
    areas = stats[1:, cv2.CC_STAT_AREA]
    largest = int(areas.max())
    keep = np.zeros_like(mask, dtype=np.uint8)
    for label, area in enumerate(areas, start=1):
        if area >= max(8, int(largest * minimum_share)):
            keep[labels == label] = 1
    return keep


def alpha_mask(image: Image.Image) -> np.ndarray:
    rgba = image.convert("RGBA")
    alpha = np.asarray(rgba.getchannel("A"), dtype=np.uint8)
    return (alpha >= 24).astype(np.uint8)


def corner_background_mask(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    h, w = rgb.shape[:2]
    patch = max(4, min(h, w) // 40)
    corners = np.concatenate(
        [
            rgb[:patch, :patch].reshape(-1, 3),
            rgb[:patch, -patch:].reshape(-1, 3),
            rgb[-patch:, :patch].reshape(-1, 3),
            rgb[-patch:, -patch:].reshape(-1, 3),
        ],
        axis=0,
    )
    background = np.median(corners.astype(np.float32), axis=0)
    distance = np.linalg.norm(rgb.astype(np.float32) - background, axis=2)
    luminance = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    # Seeded GrabCut keeps neutral product surfaces while classifying soft
    # studio-floor shadows as background.  The color-distance seed also
    # handles the Ready2Jet's pale-blue side image.
    saturation = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[:, :, 1]
    gc = np.full((h, w), cv2.GC_PR_BGD, dtype=np.uint8)
    border = max(2, min(h, w) // 80)
    gc[:border, :] = gc[-border:, :] = cv2.GC_BGD
    gc[:, :border] = gc[:, -border:] = cv2.GC_BGD
    probable = (distance > 58.0) | (luminance < 190) | (saturation > 34)
    definite = (distance > 105.0) | (luminance < 145) | (saturation > 70)
    gc[probable] = cv2.GC_PR_FGD
    gc[definite] = cv2.GC_FGD
    bg = np.zeros((1, 65), np.float64)
    fg = np.zeros((1, 65), np.float64)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.grabCut(bgr, gc, None, bg, fg, 5, cv2.GC_INIT_WITH_MASK)
    mask = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return largest_components(mask, minimum_share=0.002)


def grabcut_mask(image: Image.Image, title: bool = False) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    if title:
        # Official title card: the product occupies the right-hand block.  The
        # rectangle excludes all title text; GrabCut separates it from the
        # cyan studio graphic without painting or synthesizing product pixels.
        rect = (int(w * 0.59), int(h * 0.08), int(w * 0.33), int(h * 0.82))
    else:
        rect = (int(w * 0.04), int(h * 0.04), int(w * 0.92), int(h * 0.92))
    gc = np.zeros((h, w), np.uint8)
    bg = np.zeros((1, 65), np.float64)
    fg = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, gc, rect, bg, fg, 6, cv2.GC_INIT_WITH_RECT)
    mask = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    return largest_components(mask, minimum_share=0.001)


def mac_profile_mask(image: Image.Image) -> np.ndarray:
    base = corner_background_mask(image)
    h, _ = base.shape
    ys = np.flatnonzero(base.any(axis=1))
    if ys.size == 0:
        return base
    # Callout text and leader lines live above/below the product.  Keep the
    # densest horizontal product band only.
    row_counts = base.sum(axis=1)
    center = int(row_counts.argmax())
    half = max(5, int(h * 0.13))
    band = np.zeros_like(base)
    band[max(0, center - half):min(h, center + half + 1)] = 1
    product_band = (base & band).astype(np.uint8)
    product_band = cv2.morphologyEx(product_band, cv2.MORPH_OPEN, np.ones((1, 11), np.uint8))
    return largest_components(product_band, minimum_share=0.004)


def registered_source_mask(image: Image.Image, reference: Image.Image, reference_mask: np.ndarray) -> np.ndarray:
    """Warp a mask from the byte-registered studio source into its title-card use.

    The video title frame is a documented composite of the same official
    front-three-quarter studio asset.  Feature registration recovers only the
    geometric transform; the title card still supplies every projected RGB
    pixel.
    """
    target = np.asarray(image.convert("RGB"), dtype=np.uint8)
    source = np.asarray(reference.convert("RGB"), dtype=np.uint8)
    target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    source_gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    sift = cv2.SIFT_create(nfeatures=4000)
    key_source, desc_source = sift.detectAndCompute(source_gray, None)
    key_target, desc_target = sift.detectAndCompute(target_gray, None)
    if desc_source is None or desc_target is None:
        raise RuntimeError("title-card feature registration produced no descriptors")
    matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(desc_source, desc_target, k=2)
    good = [first for first, second in matches if first.distance < 0.72 * second.distance]
    if len(good) < 12:
        raise RuntimeError(f"title-card feature registration has only {len(good)} matches")
    src = np.float32([key_source[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([key_target[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    homography, inliers = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if homography is None or int(inliers.sum()) < 10:
        raise RuntimeError("title-card homography failed the inlier floor")
    warped = cv2.warpPerspective(
        (reference_mask * 255).astype(np.uint8), homography,
        (target.shape[1], target.shape[0]), flags=cv2.INTER_NEAREST,
    )
    return (warped >= 128).astype(np.uint8)


def make_mask(image: Image.Image, method: str) -> np.ndarray:
    if method == "alpha":
        return alpha_mask(image)
    if method == "corner_background":
        return corner_background_mask(image)
    if method == "grabcut_center":
        return grabcut_mask(image)
    if method == "grabcut_title_product":
        return grabcut_mask(image, title=True)
    if method == "mac_profile_band":
        return mac_profile_mask(image)
    raise ValueError(f"unknown mask method: {method}")


def extract_title_frame(destination: Path, ffmpeg: Path) -> None:
    source = ROOT / "source-vault/graco-ready2jet-2212125/videos/official-fold-video.mp4"
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [str(ffmpeg), "-hide_banner", "-loglevel", "error", "-ss", "0", "-i", str(source),
         "-frames:v", "1", "-y", str(destination)],
        check=True,
    )


def prepare(lane_name: str, ffmpeg: Path | None) -> None:
    lane = CONFIG["lanes"][lane_name]
    if lane.get("audit_only"):
        raise SystemExit(f"{lane_name} is audit-only and has no projection sources")
    vault_root = ROOT / "source-vault" / lane["vault_slug"]
    registered = source_index(lane["vault_slug"])
    lane_dir = HERE / lane_name
    masks_dir = lane_dir / "masks"
    textures_dir = lane_dir / "textures"
    derivatives_dir = lane_dir / "source-derivatives"
    masks_dir.mkdir(parents=True, exist_ok=True)
    textures_dir.mkdir(parents=True, exist_ok=True)
    derivatives_dir.mkdir(parents=True, exist_ok=True)
    records = []
    prepared_masks: dict[str, tuple[Image.Image, np.ndarray]] = {}

    for spec in lane["sources"]:
        if spec.get("person_free") is not True:
            raise SystemExit(f"{spec['source_id']}: person_free is not explicitly true")
        parent_id = spec.get("parent_source_id", spec["source_id"])
        if parent_id not in registered:
            raise SystemExit(f"{spec['source_id']}: source is not vault-registered")
        manifest_source = registered[parent_id]
        parent_path = vault_root / manifest_source["local_path"]
        if sha256(parent_path) != manifest_source["sha256"]:
            raise SystemExit(f"{parent_id}: vault hash mismatch")

        if "derived_local_path" in spec:
            source_path = lane_dir / spec["derived_local_path"]
            if not source_path.exists():
                if ffmpeg is None:
                    raise SystemExit("Lane 1 title-frame extraction requires --ffmpeg")
                extract_title_frame(source_path, ffmpeg)
        else:
            source_path = vault_root / spec["local_path"]
            if source_path != parent_path:
                raise SystemExit(f"{spec['source_id']}: config path differs from manifest path")

        image = Image.open(source_path).convert("RGBA")
        if spec["mask_method"] == "registered_source_mask":
            try:
                reference_image, reference_mask = prepared_masks["src_r2j_view_front3q_v1"]
            except KeyError as exc:
                raise SystemExit("registered_source_mask requires the front-three-quarter source first") from exc
            mask = registered_source_mask(image, reference_image, reference_mask)
        else:
            mask = make_mask(image, spec["mask_method"])
        if not mask.any():
            raise SystemExit(f"{spec['source_id']}: empty product mask")
        # Preserve source RGB exactly; feather only the analytical alpha edge.
        hard_alpha = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
        feathered_alpha = hard_alpha.filter(ImageFilter.GaussianBlur(radius=max(0.8, min(image.size) / 1800)))
        rgba = image.copy()
        rgba.putalpha(feathered_alpha)
        stem = spec["source_id"].replace("#", "-").replace("/", "-")
        mask_path = masks_dir / f"{stem}.png"
        texture_path = textures_dir / f"{stem}.png"
        hard_alpha.save(mask_path, optimize=True)
        rgba.save(texture_path, optimize=True)
        prepared_masks[spec["source_id"]] = (image, mask)
        records.append(
            {
                "source_id": spec["source_id"],
                "parent_source_id": parent_id,
                "parent_local_path": str(parent_path.relative_to(ROOT)),
                "parent_sha256": manifest_source["sha256"],
                "derived_source_local_path": str(source_path.relative_to(ROOT)),
                "derived_source_sha256": sha256(source_path),
                "mask_local_path": str(mask_path.relative_to(ROOT)),
                "mask_sha256": sha256(mask_path),
                "masked_texture_local_path": str(texture_path.relative_to(ROOT)),
                "masked_texture_sha256": sha256(texture_path),
                "mask_method": spec["mask_method"],
                "mask_area_fraction": round(float(mask.mean()), 6),
                "person_free": True,
                "rgb_policy": "decoded source RGB copied unchanged; only alpha is derived/feathered",
            }
        )

    output = {
        "schema_version": 1,
        "lane": lane["lane"],
        "product_id": lane["product_id"],
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "vault_manifest": str((vault_root / "manifest.json").relative_to(ROOT)),
        "vault_hashes_verified": True,
        "person_free_only": True,
        "appearance_policy": "official vault imagery only; no generated or hand-painted RGB pixels",
        "external_spend_usd": 0,
        "sources": records,
        "audited_exclusions": lane.get("audited_exclusions", []),
    }
    (lane_dir / "source-preparation.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True, choices=tuple(CONFIG["lanes"]))
    parser.add_argument("--ffmpeg", type=Path)
    args = parser.parse_args()
    prepare(args.lane, args.ffmpeg)


if __name__ == "__main__":
    main()
