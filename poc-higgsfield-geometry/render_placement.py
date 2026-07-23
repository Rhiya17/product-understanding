"""Render a computed placement as an image (POC).

This is the load-bearing trick of the whole experiment: Higgsfield's API only
accepts an image + a prompt, so the ONLY way to feed it verified geometry is to
render that geometry into the start image ourselves. Higgsfield then animates
a frame whose placement is already correct, instead of inventing one.

Usage:
    python render_placement.py [orientation_index]  ->  out/placement_<i>.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from fit_engine import TRUNK_CAVITY, valid_placements

OUT = Path(__file__).parent / "out"


def box_faces(origin, size):
    x, y, z = origin
    dx, dy, dz = size
    v = [(x, y, z), (x + dx, y, z), (x + dx, y + dy, z), (x, y + dy, z),
         (x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)]
    idx = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]
    return [[v[i] for i in face] for face in idx]


def render(index: int) -> Path:
    placements = valid_placements()
    if not placements:
        raise SystemExit("No valid placement to render.")
    p = placements[index % len(placements)]

    fig = plt.figure(figsize=(10, 7), dpi=110)
    ax = fig.add_subplot(111, projection="3d")

    trunk = Poly3DCollection(box_faces((0, 0, 0), TRUNK_CAVITY), alpha=0.08,
                             facecolor="gray", edgecolor="black", linewidths=1.2)
    ax.add_collection3d(trunk)

    sd, sw, sh = p.orientation
    d, w, h = TRUNK_CAVITY
    origin = ((d - sd) / 2, (w - sw) / 2, 0)  # centered on the floor
    stroller = Poly3DCollection(box_faces(origin, p.orientation), alpha=0.85,
                                facecolor="#2b6cb0", edgecolor="#1a365d", linewidths=1.5)
    ax.add_collection3d(stroller)

    ax.set_xlim(0, d); ax.set_ylim(0, w); ax.set_zlim(0, h * 1.6)
    ax.set_box_aspect((d, w, h * 1.6))
    ax.view_init(elev=28, azim=-55)  # roughly "looking into an open trunk"
    ax.set_axis_off()
    ax.set_title(f"orientation {index}: {p.orientation} cm in trunk {TRUNK_CAVITY} cm",
                 fontsize=9)

    OUT.mkdir(exist_ok=True)
    path = OUT / f"placement_{index}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


if __name__ == "__main__":
    i = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print(render(i))
