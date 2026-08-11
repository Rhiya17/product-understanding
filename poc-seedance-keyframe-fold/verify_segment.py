#!/usr/bin/env python3
"""Generalized VLM verification for a generated fold clip.

Runs the same two blind checks as verify_with_vlm.py, but for any run
directory: check 1 (gross integrity vs pinned start/end refs) and check 2
(mechanism vs official fold-sequence + manual page 34).

Usage:
  set -a; source .env; set +a
  python verify_segment.py --run-dir out/seg1-chain-01 \
      --start-ref references/openfold-canvas.png \
      --end-ref references/midfold-canvas.png \
      [--model qwen/qwen3-vl-235b-a22b-instruct] [--label seg1]
"""

import argparse
import json
import time
from pathlib import Path

import fal_client

HERE = Path(__file__).parent
HIGGS_REFS = HERE.parent / "poc-higgsfield-one-hand-fold" / "references"
ENDPOINT = "fal-ai/any-llm/vision"
UPLOAD_CACHE = HERE / "out" / "vlm-upload-cache.json"


def upload(path: Path, cache: dict) -> str:
    key = str(path.resolve())
    if key not in cache:
        cache[key] = fal_client.upload_file(str(path))
        UPLOAD_CACHE.write_text(json.dumps(cache, indent=2))
    return cache[key]


def check1_prompt(n: int) -> str:
    return f"""\
You are a strict verifier for AI-generated product videos. Judge only what is
visible. Do not give the benefit of the doubt.

Image 1: verified photo of a stroller in the state the video must START in.
Image 2: verified photo of the same stroller in the state the video must END in.
Images 3-{n + 2}: {n} chronological frames (frame 1 ... frame {n}) sampled
evenly from a candidate video that is supposed to move this exact stroller
from the start state to the end state, with a fixed camera, no people, and
the stroller staying in place on the ground.

Answer in JSON only, with these keys:
{{
  "same_product": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "reaches_end_state": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "camera_and_object_orientation_fixed": {{"answer": "yes|no|unsure", "evidence": "report any rotation, pan, zoom, or change of viewing angle"}},
  "stays_grounded": {{"answer": "yes|no|unsure", "evidence": "does the stroller keep realistic ground contact, or does it float, levitate, sink, or slide?"}},
  "invented_or_vanishing_parts": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "physically_impossible_motion": {{"answer": "yes|no|unsure", "evidence": "parts passing through each other, rubber-band stretching, teleporting"}},
  "verdict": "pass|fail",
  "verdict_reason": "..."
}}"""


def check2_prompt(n: int) -> str:
    return f"""\
You are a strict verifier deciding whether an AI-generated clip is trustworthy
as part of FOLDING INSTRUCTIONS for a specific stroller. Judge only what is
visible.

Image 1: the manufacturer's official fold-sequence image (open, mid-fold, and
folded states).
Image 2: page 34 of the manufacturer's manual, showing the fold controls and
steps.
Images 3-{n + 2}: {n} chronological frames (frame 1 ... frame {n}) sampled
evenly from a candidate clip covering PART of the fold.

Answer in JSON only, with these keys:
{{
  "official_mechanism": "2-3 sentences: per images 1-2, how does this fold work? Which part moves, in which direction relative to the stroller?",
  "candidate_motion": "2-3 sentences: what actually moves in the candidate frames, in what order and direction?",
  "motion_direction_matches_official": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "intermediate_states_plausible": {{"answer": "yes|no|unsure", "evidence": "do the in-between poses look like real configurations of this mechanism?"}},
  "safe_as_instruction_segment": "yes|no",
  "reason": "..."
}}"""


def run_check(model: str, prompt: str, image_urls: list, label: str) -> dict:
    t0 = time.time()
    handle = fal_client.submit(
        ENDPOINT,
        arguments={"model": model, "prompt": prompt, "image_urls": image_urls,
                   "temperature": 0, "max_tokens": 2000},
    )
    result = handle.get()
    print(f"  {label}: {round(time.time() - t0, 1)}s")
    return {"model": model, "check": label, "image_urls": image_urls,
            "result": result}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--start-ref", required=True)
    ap.add_argument("--end-ref", required=True)
    ap.add_argument("--model", default="qwen/qwen3-vl-235b-a22b-instruct")
    ap.add_argument("--label", default=None)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    label = args.label or run_dir.name
    out_dir = run_dir / "verification"
    out_dir.mkdir(exist_ok=True)
    cache = json.loads(UPLOAD_CACHE.read_text()) if UPLOAD_CACHE.exists() else {}

    frames = sorted((run_dir / "frames").glob("frame-*.png"))
    n = len(frames)
    frame_urls = [upload(p, cache) for p in frames]
    start_url = upload(Path(args.start_ref), cache)
    end_url = upload(Path(args.end_ref), cache)
    fold_seq = upload(HIGGS_REFS / "official-fold-sequence.png", cache)
    manual = upload(HIGGS_REFS / "manual-fold-page-34.png", cache)

    slug = args.model.replace("/", "-")
    print(f"{label} ({n} frames), model {args.model}")

    out1 = run_check(args.model, check1_prompt(n),
                     [start_url, end_url] + frame_urls, "check1-gross")
    (out_dir / f"{slug}-check1.json").write_text(json.dumps(out1, indent=2))

    out2 = run_check(args.model, check2_prompt(n),
                     [fold_seq, manual] + frame_urls, "check2-mechanism")
    (out_dir / f"{slug}-check2.json").write_text(json.dumps(out2, indent=2))

    for out in (out1, out2):
        print(f"\n===== {label} {out['check']} =====")
        print(out["result"].get("output", out["result"]))


if __name__ == "__main__":
    main()
