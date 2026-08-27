"""Deterministically extract the held-out validation image for input pack v1.1.

The source is the official Graco fold video already registered in the vault
(`src_r2j_fold_video_v1`, authority MANUFACTURER). Its 1-second title card
shows the full open stroller — Kingston colorway, canopy fully extended,
person-free — which is exactly the independent global view the v1 pack
lacked for the held-out silhouette check (scorecard defect: close-up
held-out made IoU unsatisfiable).

Regenerate with:
  python3 extract_heldout.py
The script verifies the vault video hash before extracting, and prints the
SHA-256 of the produced PNG so the manifest entry can be checked.
"""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = (HERE.parent / "source-vault" / "graco-ready2jet-2212125"
         / "videos" / "official-fold-video.mp4")
VIDEO_SHA256 = "9b1af25362a0b78187c6a4ced7228abcbbf5886e3617356277958392233af0fa"
OUT = HERE / "inputs" / "images" / "heldout-05-front-3q.png"

FRAME_INDEX = 29          # t ~= 1.0 s at 29.97 fps (title card, static)
CROP = (120, 1000, 1030, 1830)   # y0, y1, x0, x1 in the 1920x1080 frame


def main():
    digest = hashlib.sha256(VIDEO.read_bytes()).hexdigest()
    if digest != VIDEO_SHA256:
        sys.exit(f"vault video hash mismatch: {digest}")
    import cv2
    capture = cv2.VideoCapture(str(VIDEO))
    capture.set(cv2.CAP_PROP_POS_FRAMES, FRAME_INDEX)
    ok, frame = capture.read()
    if not ok:
        sys.exit("could not read the title-card frame")
    y0, y1, x0, x1 = CROP
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUT), frame[y0:y1, x0:x1]):
        sys.exit(f"could not write {OUT}")
    print(OUT)
    print("sha256", hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
