"""Dev-only video previews for answer documents.

Enabled only with SHOWME_DEV_MEDIA=1. These clips are unverified research or
generated media (unresolved exact-model match, internal audience) and are
always labeled that way. They never count as eligible customer media; the
real registry and eligibility checks arrive in P4.

Files come from this fixed registry only; requests name an ID, never a path.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUN02 = "poc-astra-ready2jet/run-02/final"

# Step chapters for the run-02 fold, from run-02/action-event-map.json at
# 24 fps: preparation frames 1-37 (steps 1-3), thumb slide 43-55 (step 4),
# lever squeeze 58-70 (step 5), collapse 73-137, secure/carry text 138-193.
RUN02_FOLD_CHAPTERS = {
    "claim_r2j_step_fold_1": 0.0, "claim_r2j_step_fold_2": 0.0,
    "claim_r2j_step_fold_3": 0.0, "claim_r2j_step_fold_4": 1.75,
    "claim_r2j_step_fold_5": 2.42, "claim_r2j_step_fold_6": 5.71,
    "claim_r2j_step_fold_7": 5.71,
}

DEV_MEDIA = {
    "r2j-fold-main": {
        "product_dir": "graco-ready2jet-2212125", "procedure_id": "fold_stroller",
        "path": f"{RUN02}/fold-main.mp4", "view": "main",
        "label": "Fold · main view (Astra + Blender, run-02)",
        "caveat": "Built from a reference model; exact 2212125 match not confirmed. "
                  "Secure and carry are text-only.",
        "chapters": RUN02_FOLD_CHAPTERS,
    },
    "r2j-fold-rear": {
        "product_dir": "graco-ready2jet-2212125", "procedure_id": "fold_stroller",
        "path": f"{RUN02}/fold-rear-right.mp4", "view": "rear",
        "label": "Fold · rear view (Astra + Blender, run-02)",
        "caveat": "Built from a reference model; exact 2212125 match not confirmed.",
        "chapters": RUN02_FOLD_CHAPTERS,
    },
    "r2j-fold-seedance": {
        "product_dir": "graco-ready2jet-2212125", "procedure_id": "fold_stroller",
        "path": "generated-assets/graco-ready2jet-2212125/fold-stroller-walkthrough.mp4",
        "view": "generated", "label": "Fold · Seedance generated walkthrough",
        "caveat": "AI-generated video; not a verified demonstration.",
        "chapters": {},
    },
    "mba-bluetooth-walkthrough": {
        "product_dir": "apple-macbook-air-13-m3", "procedure_id": "pair_bluetooth_device",
        "path": "generated-assets/apple-macbook-air-13-m3/bluetooth-pairing-walkthrough.mp4",
        "view": "slides", "label": "Bluetooth pairing · generated slide walkthrough",
        "caveat": "Text slides, not a product-motion demonstration.",
        "chapters": {},
    },
}


def enabled():
    return os.environ.get("SHOWME_DEV_MEDIA") == "1"


def for_document(document):
    """Dev clips for the answer's procedure, the requested view first."""
    coverage = document.get("coverage") or {}
    product = (document.get("product") or {}).get("product_dir")
    procedure = coverage.get("procedure_id")
    clips = [dict(id=clip_id, url=f"/dev-media/{clip_id}", **{
                 k: v for k, v in clip.items() if k != "path"})
             for clip_id, clip in DEV_MEDIA.items()
             if clip["product_dir"] == product and clip["procedure_id"] == procedure
             and (REPO_ROOT / clip["path"]).exists()]
    wants_rear = document.get("interpretation", {}).get("kind") == "view"
    clips.sort(key=lambda c: (c["view"] != ("rear" if wants_rear else "main"),))
    return clips


def path_for(clip_id):
    clip = DEV_MEDIA.get(clip_id)
    return REPO_ROOT / clip["path"] if clip else None
