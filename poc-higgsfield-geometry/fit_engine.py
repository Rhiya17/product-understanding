"""Deterministic box-fit engine (POC).

Answers: does a folded stroller (approximated as a rigid box) fit in a trunk
(approximated as a rectangular cavity behind a rectangular opening), and in
which axis-aligned orientations?

PLACEHOLDER DIMENSIONS — replace with verified numbers before drawing any
real conclusion. The POC is about the Higgsfield pipeline, not these values.
All units are centimeters.
"""

from dataclasses import dataclass
from itertools import permutations

# Babyzen YOYO2 folded, approximate published figures.
STROLLER_FOLDED = (52.0, 44.0, 18.0)

# Tesla Model Y rear trunk, rough approximation of the lower well + main floor
# treated as one simple cavity. Real trunks are irregular; that irregularity is
# one of the things this POC exists to discuss.
TRUNK_CAVITY = (97.0, 100.0, 46.0)   # depth (into car), width, height
TRUNK_OPENING = (100.0, 44.0)        # opening width, opening height

CLEARANCE = 2.0  # required free space on every axis, cm


@dataclass
class Placement:
    orientation: tuple  # stroller dims as placed: (along depth, along width, along height)
    clearances: tuple   # free space per axis after placement


def fits_through_opening(w: float, h: float) -> bool:
    ow, oh = TRUNK_OPENING
    return (w + CLEARANCE <= ow and h + CLEARANCE <= oh) or (
        h + CLEARANCE <= ow and w + CLEARANCE <= oh
    )


def valid_placements() -> list[Placement]:
    d, w, h = TRUNK_CAVITY
    placements = []
    for o in set(permutations(STROLLER_FOLDED)):
        sd, sw, sh = o
        inside = sd + CLEARANCE <= d and sw + CLEARANCE <= w and sh + CLEARANCE <= h
        # The face presented to the opening is (width-axis, height-axis).
        through = fits_through_opening(sw, sh)
        if inside and through:
            placements.append(Placement(o, (d - sd, w - sw, h - sh)))
    # Most clearance first.
    placements.sort(key=lambda p: -min(p.clearances))
    return placements


if __name__ == "__main__":
    ps = valid_placements()
    if not ps:
        print("RESULT: does not fit in any axis-aligned orientation")
    else:
        print(f"RESULT: fits — {len(ps)} valid orientation(s)")
        for i, p in enumerate(ps):
            print(f"  [{i}] stroller placed as {p.orientation} cm, "
                  f"clearances {tuple(round(c, 1) for c in p.clearances)} cm")
