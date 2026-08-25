# Seedance Mid-Fold Image POC

*Written 2026-08-05. This test builds on the earlier
[Seedance POC](./seedance-poc-findings.md) and
[Qwen verifier POC](./vlm-verifier-poc-findings.md).*

## Summary

Adding a real mid-fold image helped.

Seedance kept the same stroller, reached all three real states, and avoided the
obvious wrong-way fold from the earlier video. But the new video is still
**not ready to use as folding instructions**:

- The stroller appears to float.
- The viewing angle changes during the fold.
- The motion looks better, but the exact hinge movement is not proven.
- The video does not show the person using the real fold controls.

Qwen3-VL found the clear visual problems and explained its answers. However,
its verdict about the folding mechanism changed between checks. Qwen can be
the first reviewer, but a person must make the final decision.

## Why we needed this POC

The earlier Seedance video started with the correct open stroller and ended
with the correct folded stroller. But the motion in the middle was wrong. The
handle and canopy first moved in the wrong direction.

This taught us an important lesson:

> Correct start and end images do not guarantee correct motion between them.

Seedance knew where the stroller had to start and finish, but it had to guess
how the real folding mechanism moved.

The manufacturer's fold sequence includes a real photo of the stroller
halfway through the fold. This POC asked:

> Will Seedance make a better fold if we force it through that real middle
> state?

## What “safe as instructions” means

Here, **safe** means *trustworthy enough to help someone operate the real
stroller correctly*. A video is not safe just because it looks realistic.

A folding video is safe to use as instructions only when:

- It shows the correct stroller.
- The parts move in the correct direction and order.
- The middle positions are possible on the real stroller.
- Parts do not appear, disappear, stretch, or pass through each other.
- Required user actions are not hidden or shown incorrectly.
- The stroller reaches the correct folded state.

There are also two different kinds of video:

- A **motion demonstration** shows how the stroller changes shape.
- A **complete instruction video** also shows how the user starts and performs
  the fold.

This POC intentionally removed the person and generated a hands-free fold. It
tests the stroller's motion, but it cannot be a complete instruction video.
The real fold requires the thumb switch and handle lever shown in the manual.

## What we tested

We cropped three real states from the manufacturer's official fold sequence:

1. Open
2. Halfway folded
3. Fully folded

The person was removed from the open image without changing the stroller's
pose. All three images were placed on pale canvases for Seedance.

![The three cleaned stroller states](../poc-seedance-keyframe-fold/references/cleaning-comparison-sheet.png)

We then made two short videos instead of one long video:

```text
Real open image
      ↓
4-second generated video
      ↓
Real mid-fold image
      ↓
4-second generated video
      ↓
Real folded image
```

The three real images are **pins**: Seedance must start or end each segment at
those exact states. The frames between the pins are still generated guesses.

Finally, we joined the two segments into one 8-second video.

## What we produced

| Output | What it shows |
|---|---|
| [Segment 1](../poc-seedance-keyframe-fold/out/seg1-chain-01/video.mp4) | Open → real mid-fold state |
| [Segment 2](../poc-seedance-keyframe-fold/out/seg2-chain-01/video.mp4) | Real mid-fold state → folded |
| [Stitched video](../poc-seedance-keyframe-fold/out/chain-01-stitched/video.mp4) | Both segments joined together |
| [Contact sheet](../poc-seedance-keyframe-fold/out/chain-01-stitched/contact-sheet.png) | Twelve snapshots from the stitched video |

![Twelve snapshots from the stitched video](../poc-seedance-keyframe-fold/out/chain-01-stitched/contact-sheet.png)

## How Qwen reviewed it

Qwen did not receive the video file. It received snapshots in time order,
similar to a comic strip:

- Six snapshots from each 4-second segment
- Twelve snapshots from the stitched video

Qwen ran two checks.

### Check 1: Clear visual problems

Qwen checked whether the video:

- Kept the same stroller
- Reached the pinned end state
- Kept a fixed view
- Stayed on the ground
- Added or removed parts
- Showed obviously impossible motion

### Check 2: Folding mechanism

Qwen also received the official fold sequence and manual page 34. It checked:

- Whether the parts moved in the correct direction
- Whether the middle positions looked possible
- Whether the clip was safe to use as part of folding instructions

## Does Qwen explain why something is safe or unsafe?

**Yes.** Qwen returns:

- A yes, no, or unsure answer for each question
- The visible evidence behind each answer
- A final reason for its verdict

For example, Qwen rejected the stitched video's visual check because the
stroller floated, the view changed, and the fold happened without visible
support.

But Qwen's explanation is still an AI judgment. It can sound confident even
when it is incomplete or wrong.

## Results

| Question | Result |
|---|---|
| Same stroller throughout? | **Yes** |
| Reaches the real mid-fold state? | **Yes** |
| Reaches the real folded state? | **Yes** |
| Parts appear or disappear? | **No** |
| Better folding direction than the first POC? | **Yes** |
| Exact hinge motion proven? | **No** |
| Stays on the ground? | **No** |
| View stays fixed? | **No** |
| Clean join between segments? | **Mostly; there is a short pause** |
| Ready to publish as instructions? | **No** |

### Human review

Segment 1 is much better than the earlier video. The handle moves down and
toward the front wheels instead of making the same obvious backward flop.

The right description is:

> **Directionally correct, but mechanically unverified.**

The viewing angle changes during the fold, so it is difficult to follow each
hinge. We cannot claim that the generated movement exactly matches the real
mechanism.

The two segments meet at the same real mid-fold image. There is no large visual
jump, but both clips slow down near that image. This creates a short pause at
the join.

## Why the video failed

The two clearest failures came from our input preparation, not from a fair test
of Seedance alone.

### The stroller floats

We removed the floor line and shadow when placing the stroller on the pale
canvases. The pinned images gave Seedance no clear ground surface, so the
result looks like it is folding in mid-air.

**Fix:** Use the same ground line in all three images. Align the lowest wheel
to it and keep or add a soft contact shadow.

### The stroller rotates

The official photos were taken from different angles:

- Open: almost a pure side view
- Mid-fold: a three-quarter view
- Folded: close to a rear three-quarter view

Seedance had to rotate the stroller to hit all three pinned images. Our request
for a fixed view conflicted with our own evidence.

**Fix:** Find three states photographed from the same angle. If we cannot, we
must accept the rotation and stop asking for a fixed view.

## What we learned about Qwen

Qwen was consistent on the clear visual facts:

- Same stroller: yes
- Correct pinned endpoints: yes
- Fixed view: no
- Grounded: no
- Invented or missing parts: no

Its mechanism verdict was not consistent:

| Video | Qwen verdict | Qwen's reason |
|---|---|---|
| Segment 1 | Safe | Direction matched and middle states looked possible |
| Segment 2 | Unsafe | It believed the stroller mostly rotated instead of folding |
| Stitched video | Safe | Overall motion and middle states looked plausible |

The stitched video contains all of Segment 2, yet Qwen changed the unsafe
answer to safe. It also described Segment 1 as tilting backward in one check
and folding forward in another.

One reason may be that the word **safe** is too broad. Qwen sometimes judged
only the stroller's motion. At other times, it also required the person and
fold controls to be visible.

For the next test, we should replace one broad “safe” question with smaller,
clear questions. For example: “Did the handle move toward the front wheels?”

## What this POC proves—and what it does not

This POC shows that:

- A real middle image can reduce Seedance's room to guess.
- The chained video can keep the product and hit all three real states.
- Qwen can find and explain clear visual problems.

It does **not** show that:

- The generated hinge motion is mechanically exact.
- The current video is safe to publish as instructions.
- One Qwen verdict can replace human approval.

We tested only one chain, one seed, and the fast Seedance tier. Qwen also saw
sampled snapshots, so it could miss something between them.

## Next step

Keep the keyframe-chain approach, but reject the current video for
instructional use.

For the next run:

1. Add a shared ground line, wheel position, scale, and shadow to all pins.
2. Use state images taken from the same angle if possible.
3. Generate several seeds.
4. Ask Qwen small, visible questions about each required movement.
5. Run each mechanism check several times and use the majority answer.
6. Keep human approval as the final gate.
7. If we need complete instructions, add verified footage or graphics showing
   the real thumb-switch and handle-lever actions.

## Decision

- **Keyframe chaining: continue.** The real midpoint improved the fold.
- **Current video: reject as instructions.** It floats, rotates, omits the user
  controls, and does not prove the exact hinge path.
- **Qwen verifier: continue as the first review step.** Use it to find clear
  problems, not to make the final safety decision.

## Experiment artifacts

- [Cleaned reference comparison](../poc-seedance-keyframe-fold/references/cleaning-comparison-sheet.png)
- [Segment 1 contact sheet](../poc-seedance-keyframe-fold/out/seg1-chain-01/contact-sheet.png)
- [Segment 2 contact sheet](../poc-seedance-keyframe-fold/out/seg2-chain-01/contact-sheet.png)
- [Stitched contact sheet](../poc-seedance-keyframe-fold/out/chain-01-stitched/contact-sheet.png)
- Segment 1 Qwen results: [visual check](../poc-seedance-keyframe-fold/out/seg1-chain-01/verification/qwen-qwen3-vl-235b-a22b-instruct-check1.json), [mechanism check](../poc-seedance-keyframe-fold/out/seg1-chain-01/verification/qwen-qwen3-vl-235b-a22b-instruct-check2.json)
- Segment 2 Qwen results: [visual check](../poc-seedance-keyframe-fold/out/seg2-chain-01/verification/qwen-qwen3-vl-235b-a22b-instruct-check1.json), [mechanism check](../poc-seedance-keyframe-fold/out/seg2-chain-01/verification/qwen-qwen3-vl-235b-a22b-instruct-check2.json)
- Stitched Qwen results: [visual check](../poc-seedance-keyframe-fold/out/chain-01-stitched/verification/qwen-qwen3-vl-235b-a22b-instruct-check1.json), [mechanism check](../poc-seedance-keyframe-fold/out/chain-01-stitched/verification/qwen-qwen3-vl-235b-a22b-instruct-check2.json)
- [Verification prompts](../poc-seedance-keyframe-fold/verify_segment.py)
