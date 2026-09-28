"""Saved 3D scenes that can render a procedure, and the views each supports.

A scene entry is a capability: only (product, procedure, view) triples listed
here can be promised as a rendered video. Everything else is recorded as
needing a new scene. Chapters map step claims to seconds in the clip.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# run-02 action-event-map.json at 24 fps: preparation frames 1-37 (steps 1-3),
# thumb slide 43-55 (step 4), lever squeeze 58-70 (step 5), collapse 73-137,
# secure/carry is text only (steps 6-7 share the collapse chapter).
R2J_FOLD_CHAPTERS = {
    "claim_r2j_step_fold_1": 0.0, "claim_r2j_step_fold_2": 0.0,
    "claim_r2j_step_fold_3": 0.0, "claim_r2j_step_fold_4": 1.75,
    "claim_r2j_step_fold_5": 2.42, "claim_r2j_step_fold_6": 5.71,
    "claim_r2j_step_fold_7": 5.71,
}

SCENES = {
    ("graco-ready2jet-2212125", "fold_stroller"): {
        "scene_version": "r2j-run02",
        "blend": "poc-astra-ready2jet/run-02/final/ready2jet.blend",
        "frames": (1, 193),
        "fps": 24,
        "size": (1280, 720),
        "audience": "research",
        "label": "Ready2Jet fold · 3D model (Astra + Blender)",
        "caveat": ("Rendered from a reference 3D model; exact 2212125 match not "
                   "confirmed. Checking it's secure and carrying are text-only."),
        "chapters": R2J_FOLD_CHAPTERS,
        "views": {
            "main": {"camera": "Camera_Reference", "shift_x": 0.13, "samples": 24,
                     "label": "Main view",
                     "imported": "poc-astra-ready2jet/run-02/final/fold-main.mp4"},
            "rear": {"camera": "Camera_RearRight", "shift_x": 0.13, "samples": 20,
                     "label": "Rear view",
                     "imported": "poc-astra-ready2jet/run-02/final/fold-rear-right.mp4"},
            "side": {"camera": "Camera_Side", "shift_x": 0.0, "samples": 24,
                     "label": "Side view"},
            "front": {"camera": "Camera_Hero", "shift_x": 0.0, "samples": 24,
                      "label": "Front view"},
        },
    },
}

VIEW_ORDER = ("main", "rear", "side", "front")
VIEW_LABELS = {"main": "Main view", "rear": "Rear view", "side": "Side view",
               "front": "Front view"}


def scene_for(product_dir, procedure_id):
    return SCENES.get((product_dir, procedure_id))


def supports(product_dir, procedure_id, view):
    scene = scene_for(product_dir, procedure_id)
    return bool(scene and view in scene["views"])
