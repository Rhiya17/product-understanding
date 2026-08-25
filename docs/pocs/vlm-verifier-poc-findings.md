# AI Video Verifier POC: Can It Catch Video Errors?

*Written 2026-08-05. First result from the VLM verifier in
[`verify_with_vlm.py`](../poc-seedance-keyframe-fold/verify_with_vlm.py).
This is an early result based on one run per model.*

## Executive summary

We tested whether a vision-language model (VLM)—an AI that can inspect
images—could find errors in an AI-generated stroller video without being told
what was wrong.

The result was promising:

- **Qwen3-VL matched the human review on all six checks**, including the most
  important error: the stroller folds in the wrong direction.
- **Claude Sonnet 4.5 matched the human review on five of six checks.** It
  correctly rejected the video, but it missed the incorrect folding motion.
- **Both models agreed the video is not safe to use as instructions.**

This supports using a VLM verifier as an automated first check. It does not yet
support removing human review: we tested only one bad video, with one run per
model.

## What we tested

The video came from the earlier
[Seedance folding POC](./seedance-poc-findings.md). Human review had already
found two major problems:

1. **The stroller folds the wrong way.** The real stroller's handle moves
   forward toward the front wheels. In the generated video, the handle and
   canopy move backward first.
2. **The viewpoint changes.** The video begins at a front-left angle and ends
   at a side angle, even though the prompt required a fixed view.

We wanted to know whether a VLM could find these problems on its own. We tested:

- **Qwen3-VL-235B**, the model planned for the verifier.
- **Claude Sonnet 4.5**, as a comparison.

Each model received the same images and questions. We did not tell either model
what the human review had found.

Each check took 12–25 seconds. Both models ran through the existing fal.ai
setup, and each check cost only pennies.

## Test design

We split the review into two checks. Both used the same 12 snapshots in the
same order. Only the official reference images changed.

### What are the 12 video frames?

The judges did not receive the 8-second video file. The AI service we used
accepts images, not video files, so our script saved **12 evenly spaced
snapshots** from the video—like a comic-strip version of it:

- Frame 1 shows the stroller open at the start.
- Frames 2–11 show the fold in progress.
- Frame 12 shows the stroller folded at the end.

The [12 frame files](../poc-seedance-keyframe-fold/out/a-probe/frames/) are
named `frame-01.png` through `frame-12.png`. The
[contact sheet](../poc-seedance-keyframe-fold/out/a-probe/contact-sheet.png)
shows all 12 together on one page.

### Check 1: Product and video consistency

Each judge received:

- The official [open stroller photo](../poc-seedance-keyframe-fold/references/open-product-only.png)
- The official [folded stroller photo](../poc-seedance-keyframe-fold/references/folded-product-only.png)
- [12 frames from the generated video](../poc-seedance-keyframe-fold/out/a-probe/frames/)

We asked whether the video:

- Keeps the same stroller throughout
- Shows a real fold
- Ends in the correct folded state
- Keeps the viewpoint fixed
- Adds or removes any parts

### Check 2: Folding accuracy

Each judge received:

- The official [fold sequence](../poc-higgsfield-one-hand-fold/references/official-fold-sequence.png)
- [Page 34 of the product manual](../poc-higgsfield-one-hand-fold/references/manual-fold-page-34.png)
- The same 12 video frames

We asked whether the video shows the correct controls, motion, and intermediate
folding states, and whether it is safe to use as instructions.

The exact prompts are in
[`verify_with_vlm.py`](../poc-seedance-keyframe-fold/verify_with_vlm.py).

## Results

| Expected result from human review | Qwen3-VL | Claude Sonnet 4.5 |
|---|:---:|:---:|
| Same stroller throughout | Correct | Correct |
| Stroller folds and reaches the correct end state | Correct | Correct |
| Viewpoint changes despite the fixed-camera instruction | Correct | Correct |
| **Folding motion is wrong** | **Correct** | **Missed** |
| Required fold controls are not shown | Correct | Correct |
| Video is not safe as instructions | Correct | Correct |
| **Total** | **6/6** | **5/6** |

Both models rejected the video. The important difference was *why*.

### Qwen3-VL caught the wrong folding motion

Qwen first identified the official motion: the handle should move toward the
front wheels while the seat folds down. It then compared that motion with the
video and found that the handle tilts back while the canopy folds over the
seat.

That matches the human review. Qwen rejected the video because both the folding
motion and the user controls were wrong or missing.

### Claude missed the main motion error

Claude said the video's intermediate states matched the official sequence. It
also described part of the official motion backward.

Claude still rejected the video because it did not show the thumb switch and
handle lever required to start the fold. It also identified the viewpoint
change more precisely, placing the largest shift between frames 11 and 12.

## What this means

This run gives us three useful signals:

1. **An evidence-based AI judge can catch meaningful video errors.** Qwen found
   the subtle wrong-way fold without being given the answer.
2. **The reference evidence matters.** The manual page and official fold image
   gave the judges a product-specific standard. Without them, a model could
   only judge whether the motion looked plausible.
3. **Qwen3-VL is the stronger verifier candidate from this run.** It found every
   expected result and is already available through the fal.ai setup used for
   the Seedance experiment.

## Limitations

This is an early signal, not a final evaluation.

- **Only one run per model:** We do not yet know whether the answers are stable.
- **Only one video:** The test used a known bad video. We also need a correct
  video to measure false rejections.
- **Frame sampling:** The judges saw 12 still frames, not the full video. They
  could miss errors between frames.
- **Human review is still required:** For exact operating instructions, the AI
  judge should filter candidates before a person performs the final check.

## Next steps

1. **Test known failures:** Run both judges on the three failed
   [Higgsfield videos](./higgsfield-poc-findings.md). They should reject all
   three.
2. **Test stability:** Repeat this evaluation three times per judge.
3. **Measure false rejections:** Test a correct folding video and confirm that
   the judges accept it.
4. **Add the first gate:** If the results remain stable, use the verifier as the
   automated first check for Seedance Condition B.

## Experiment artifacts

- [Generated video](../poc-seedance-keyframe-fold/out/a-probe/video.mp4)
- [12-frame contact sheet](../poc-seedance-keyframe-fold/out/a-probe/contact-sheet.png)
- Qwen results: [check 1](../poc-seedance-keyframe-fold/out/a-probe/verification/qwen-qwen3-vl-235b-a22b-instruct-check1.json), [check 2](../poc-seedance-keyframe-fold/out/a-probe/verification/qwen-qwen3-vl-235b-a22b-instruct-check2.json)
- Claude results: [check 1](../poc-seedance-keyframe-fold/out/a-probe/verification/anthropic-claude-sonnet-4.5-check1.json), [check 2](../poc-seedance-keyframe-fold/out/a-probe/verification/anthropic-claude-sonnet-4.5-check2.json)
