#!/usr/bin/env python3
"""VLM-as-verifier probe: can a vision-language model verify the Seedance
a-probe fold video against official evidence?

Two blind checks per model (the prompts never reveal the human scoring):

  check1  gross integrity   — same product? does a fold occur? does the end
                              state match the official folded photo? camera
                              fixed? invented parts?
  check2  mechanism accuracy — given the official fold-sequence image and
                              manual page 34, does the candidate's
                              intermediate motion match the documented
                              mechanism?

Usage:
  set -a; source .env; set +a
  python verify_with_vlm.py                         # default: qwen3-vl-235b
  python verify_with_vlm.py --model anthropic/claude-sonnet-4.5
"""

import argparse
import json
import time
from pathlib import Path

import fal_client

HERE = Path(__file__).parent
FRAMES_DIR = HERE / "out" / "a-probe" / "frames"
OUT_DIR = HERE / "out" / "a-probe" / "verification"
REFS = HERE / "references"
HIGGS_REFS = HERE.parent / "poc-higgsfield-one-hand-fold" / "references"

ENDPOINT = "fal-ai/any-llm/vision"

UPLOAD_CACHE = HERE / "out" / "vlm-upload-cache.json"


def upload(path: Path, cache: dict) -> str:
    key = str(path.resolve())
    if key not in cache:
        cache[key] = fal_client.upload_file(str(path))
        UPLOAD_CACHE.write_text(json.dumps(cache, indent=2))
    return cache[key]


CHECK1_PROMPT = """\
You are a strict verifier for AI-generated product videos. Judge only what is
visible. Do not give the benefit of the doubt.

Image 1: official photo of a stroller in its OPEN state (ground truth start).
Image 2: official photo of the same stroller FOLDED (ground truth end).
Images 3-14: twelve chronological frames (frame 1 ... frame 12) sampled evenly
from a candidate video that is supposed to show this exact stroller folding
itself, with a fixed camera and no people.

Answer in JSON only, with these keys:
{
  "same_product": {"answer": "yes|no|unsure", "evidence": "..."},
  "fold_occurs": {"answer": "yes|no|unsure", "evidence": "..."},
  "end_state_matches_official_folded_photo": {"answer": "yes|no|unsure", "evidence": "..."},
  "camera_and_object_orientation_fixed": {"answer": "yes|no|unsure", "evidence": "..."},
  "invented_or_vanishing_parts": {"answer": "yes|no|unsure", "evidence": "..."},
  "verdict": "pass|fail",
  "verdict_reason": "..."
}
"same_product" means the candidate keeps the exact product identity of images
1-2 in every frame: canopy fabric pattern, wheel design, frame color, basket,
cup holder. Note any drift.
"camera_and_object_orientation_fixed" means the viewpoint and the stroller's
orientation relative to the camera stay constant apart from the folding motion
itself; report any rotation, pan, or zoom.
"""

CHECK2_PROMPT = """\
You are a strict verifier deciding whether an AI-generated video is
trustworthy as FOLDING INSTRUCTIONS for a specific stroller. Judge only what
is visible.

Image 1: the manufacturer's official fold-sequence image for this stroller,
including a genuine intermediate (mid-fold) state.
Image 2: page 34 of the manufacturer's manual, showing the fold controls and
steps for this stroller.
Images 3-14: twelve chronological frames (frame 1 ... frame 12) sampled evenly
from a candidate video that is supposed to demonstrate this stroller's fold.

Answer in JSON only, with these keys:
{
  "official_mechanism": "in 2-3 sentences: per images 1-2, how does this fold work? Which part moves first, and in which direction relative to the stroller (e.g. handle toward the front wheels, seat collapsing down)?",
  "candidate_motion": "in 2-3 sentences: what actually moves in the candidate frames, in what order and direction?",
  "intermediate_states_match_official": {"answer": "yes|no|unsure", "evidence": "compare the candidate's mid-fold frames to the official intermediate state"},
  "controls_shown_correctly": {"answer": "yes|no|not_visible", "evidence": "does the candidate show or respect the fold controls documented in image 2?"},
  "safe_as_instructions": "yes|no",
  "reason": "..."
}
"safe_as_instructions" = could a person watch this video and correctly learn
the real fold procedure, without being misled about any motion or control?
"""


def run_check(model: str, prompt: str, image_urls: list, label: str) -> dict:
    t0 = time.time()
    handle = fal_client.submit(
        ENDPOINT,
        arguments={
            "model": model,
            "prompt": prompt,
            "image_urls": image_urls,
            "temperature": 0,
            "max_tokens": 2000,
        },
    )
    result = handle.get()
    elapsed = round(time.time() - t0, 1)
    print(f"  {label}: {elapsed}s")
    return {"model": model, "check": label, "elapsed_s": elapsed,
            "image_urls": image_urls, "result": result}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen/qwen3-vl-235b-a22b-instruct")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}

    frames = sorted(FRAMES_DIR.glob("frame-*.png"))
    assert len(frames) == 12, f"expected 12 frames, found {len(frames)}"
    frame_urls = [upload(p, cache) for p in frames]

    open_ref = upload(REFS / "open-product-only.png", cache)
    folded_ref = upload(REFS / "folded-product-only.png", cache)
    fold_seq = upload(HIGGS_REFS / "official-fold-sequence.png", cache)
    manual_p34 = upload(HIGGS_REFS / "manual-fold-page-34.png", cache)

    slug = args.model.replace("/", "-")
    print(f"model: {args.model}")

    out1 = run_check(args.model, CHECK1_PROMPT,
                     [open_ref, folded_ref] + frame_urls, "check1-gross")
    (OUT_DIR / f"{slug}-check1.json").write_text(json.dumps(out1, indent=2))

    out2 = run_check(args.model, CHECK2_PROMPT,
                     [fold_seq, manual_p34] + frame_urls, "check2-mechanism")
    (OUT_DIR / f"{slug}-check2.json").write_text(json.dumps(out2, indent=2))

    for out in (out1, out2):
        print(f"\n===== {out['check']} =====")
        print(out["result"].get("output", out["result"]))


if __name__ == "__main__":
    main()
