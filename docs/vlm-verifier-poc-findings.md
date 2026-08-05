# Robot Judge Experiment: Can an AI Watch Our Video and Spot the Mistakes?

*Written 2026-08-05. First result from the VLM-verifier probe in
[`poc-seedance-keyframe-fold/verify_with_vlm.py`](../poc-seedance-keyframe-fold/verify_with_vlm.py).
One run per judge so far — a very promising start, but not yet a full pass.*

---

## Why are we doing this? 🤔

Last week, Seedance made a video of our Graco Ready2Jet stroller folding
itself ([full story](./seedance-poc-findings.md)). We watched it with our own
eyes and found:

* ✅ Good: same stroller the whole time, and it really folds.
* ❌ Bad #1: it folds the **wrong way** (the top flops *backward*; the real
  stroller drops its handle *forward*).
* ❌ Bad #2: the **view slowly turns**. Our instructions told the AI:
  film this like a phone on a tripod — one fixed viewpoint, no moving
  around. (There is no real camera in an AI video, so "camera" just means
  the viewpoint the AI draws the scene from.) Instead, the stroller
  gradually turns to a different angle: the video starts showing it from
  the front-left and ends showing it from the side. That breaks a direct
  instruction, and a turning view makes a how-to video harder to follow —
  you can't tell "a part moved" from "the view moved."

Our master plan says a human should not have to watch every AI video. We want
a cheap "AI judge" that watches first and throws out the bad ones. So the
question for this experiment was:

> **If we show an AI judge the video and the official Graco evidence — but
> tell it NOTHING about the mistakes we found — will it find the same
> mistakes on its own?**

We tested two judges on the exact same questions:

1. **Qwen3-VL** (a big open model, 235B size) — the judge we planned to use.
2. **Claude Sonnet 4.5** — a well-known paid model, as a comparison.

No new accounts were needed. Both judges run through fal.ai, where we already
have a key from the Seedance experiment.

---

## Exactly what we fed the judges (the inputs) 📥

Every input is a real file in this repo. The judges saw pictures only — never
our opinions.

**The video being judged** (turned into 12 still pictures, in time order):

* 🎥 The video: [`out/a-probe/video.mp4`](../poc-seedance-keyframe-fold/out/a-probe/video.mp4)
* 🖼️ The 12 frames: [`out/a-probe/frames/`](../poc-seedance-keyframe-fold/out/a-probe/frames/)
* 🖼️ All 12 on one sheet: [`out/a-probe/contact-sheet.png`](../poc-seedance-keyframe-fold/out/a-probe/contact-sheet.png)

**Test 1 — "Basic honesty check."** We gave each judge:

1. The official photo of the OPEN stroller:
   [`references/open-product-only.png`](../poc-seedance-keyframe-fold/references/open-product-only.png)
2. The official photo of the FOLDED stroller:
   [`references/folded-product-only.png`](../poc-seedance-keyframe-fold/references/folded-product-only.png)
3. The 12 video frames.

Then we asked: Is it the same stroller the whole time? Does it really fold?
Does it end like the official folded photo? Does the camera stay still? Do
any parts appear or disappear?

**Test 2 — "Did it fold the RIGHT way?"** We gave each judge:

1. Graco's official fold-sequence picture (it shows a real halfway-folded
   state):
   [`official-fold-sequence.png`](../poc-higgsfield-one-hand-fold/references/official-fold-sequence.png)
2. Page 34 of the official manual (it shows the fold buttons and steps):
   [`manual-fold-page-34.png`](../poc-higgsfield-one-hand-fold/references/manual-fold-page-34.png)
3. The same 12 video frames.

Then we asked: How does the real fold work, according to the manual? What
happens in the video? Do the middle steps match? Would this video teach a
person the right way to fold?

The exact question wording is saved in
[`verify_with_vlm.py`](../poc-seedance-keyframe-fold/verify_with_vlm.py), so
anyone can check that we never leaked the answers.

---

## What the judges said (the outputs) 📤

The judges' full answers are saved word-for-word here:

| Judge | Test 1 answer | Test 2 answer |
|---|---|---|
| Qwen3-VL-235B | [`qwen...check1.json`](../poc-seedance-keyframe-fold/out/a-probe/verification/qwen-qwen3-vl-235b-a22b-instruct-check1.json) | [`qwen...check2.json`](../poc-seedance-keyframe-fold/out/a-probe/verification/qwen-qwen3-vl-235b-a22b-instruct-check2.json) |
| Claude Sonnet 4.5 | [`anthropic...check1.json`](../poc-seedance-keyframe-fold/out/a-probe/verification/anthropic-claude-sonnet-4.5-check1.json) | [`anthropic...check2.json`](../poc-seedance-keyframe-fold/out/a-probe/verification/anthropic-claude-sonnet-4.5-check2.json) |

Each test took 12–25 seconds and cost only pennies.

---

## The scoreboard 🏆

We compare each judge against what we humans found by watching the video:

| What we humans found | Qwen3-VL | Claude Sonnet 4.5 |
|---|---|---|
| Same stroller the whole time ✅ | ✅ agreed | ✅ agreed |
| It really folds, ends correctly ✅ | ✅ agreed | ✅ agreed |
| The stroller rotates (camera not still) ❌ | ✅ caught it | ✅ caught it |
| **It folds the WRONG WAY** ❌ | ✅ **caught it** | ❌ **missed it** |
| The fold buttons are never shown ❌ | ✅ caught it | ✅ caught it |
| Final verdict: not safe as instructions | ✅ said "no" | ✅ said "no" |

**Qwen3-VL: 6 out of 6. Claude Sonnet 4.5: 5 out of 6.**

---

## Exactly how Qwen3 did better 🔍

The wrong-way fold was the hardest mistake to catch. To catch it, a judge had
to do three things in a row: read the manual page, understand the official
halfway picture, and compare both against the video frames.

**Qwen3-VL did all three.** In its own words:

> Official mechanism: *"...the handle moving toward the front wheels and the
> seat folding down."* ← correct, straight from the manual.
>
> The video: *"...the handle already tilted far back and the canopy folding
> over the seat, which is a different sequence and geometry than the official
> guide."* ← this is exactly the backward-flop we saw with our own eyes.

**Claude Sonnet missed this.** It said the middle of the video *"matches the
documented fold progression"* — in other words, it approved the wrong-way
fold. It even described the official mechanism partly backward (*"the handle
rotates backward/upward"*). Sonnet still voted "not safe as instructions,"
but only because the video never shows the fold buttons — not because the
motion was wrong.

Why this matters: a wrong motion that *looks* right is the sneakiest kind of
mistake in our whole project. Our safety rules exist because of it. In this
one test, the open model we can run cheaply at scale caught it, and the
famous paid model did not.

(To be fair: Sonnet was better at one small thing — it pinpointed the camera
jump to exactly frames 11→12, while Qwen described the rotation more
loosely.)

---

## What did we learn? 🧠

1. **The "AI judge" idea from our plan works.** A judge that sees the
   official evidence can catch real mistakes — even the sneaky wrong-way
   fold — without any hints from us.
2. **Evidence is the secret ingredient.** The judge only caught the wrong-way
   fold because we handed it the manual page and the official fold-sequence
   picture. A judge with no evidence can only catch obvious mistakes.
3. **Qwen3-VL is a serious candidate for the job.** It won this round 6/6,
   it is open (Apache 2.0, fine for commercial use), and it runs through the
   fal.ai key we already have.

---

## Be careful: what this does NOT prove yet ⚠️

* **One run per judge is not proof.** We ran each judge once. We need
  repeats to know the answers are stable.
* **We only tested a BAD video.** A good judge must also say "yes" to a
  correct video. We have not measured how often these judges cry wolf.
* **12 frames is not the full video.** Something between frames could be
  missed.
* **A "6/6" judge is still not a human.** Our safety rule stands: for exact
  operating instructions, the AI judge filters first, and a human still does
  the final check.

---

## What's next 🔜

1. **Calibration check:** run the same judges on the three failed Higgsfield
   videos ([findings](./higgsfield-poc-findings.md)). They should fail all
   three easily.
2. **Stability check:** repeat this exact test 3 times per judge.
3. **False-alarm check:** find or film a CORRECT fold video and make sure the
   judges pass it.
4. **Wire it in:** use the judge as the automatic first gate when we run
   Seedance Condition B (endpoints + manual pages).
