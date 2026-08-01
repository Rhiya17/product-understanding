# Seedance Video Experiment: Can Two Real Photos Make an Honest Fold Video?

*Written 2026-07-31. First result from the
[Seedance keyframe POC](../poc-seedance-keyframe-fold/README.md). One probe
run so far — promising, but not yet a pass.*

## Why are we doing this?

Last time, we tested an AI video maker called Higgsfield. We gave it one photo
of our Graco Ready2Jet stroller and careful written instructions, and asked it
to show the stroller folding. It failed 3 out of 3 times — it never folded
the stroller, and it even morphed it into a different stroller.
(Full story: [Higgsfield findings](./higgsfield-poc-findings.md).)

But we learned one big clue from those tests: **when we pin the video down
with real photos at the start AND the end, the AI behaves much better.** So
this new experiment asks: if we give a newer AI (Seedance 2.0, made by
ByteDance) a real photo of the open stroller and a real photo of the folded
stroller, can it fill in the middle honestly?

## Exactly what we fed the AI (the input files)

Every input is a real file in this repo. Nothing was invented by us:

1. **Start photo (open stroller):**
   [`poc-seedance-keyframe-fold/references/open-product-only.png`](../poc-seedance-keyframe-fold/references/open-product-only.png)
2. **End photo (folded stroller):**
   [`poc-seedance-keyframe-fold/references/folded-product-only.png`](../poc-seedance-keyframe-fold/references/folded-product-only.png)

   Both photos are simple crops (like trimming a screenshot — no AI editing)
   of one official Graco studio picture that was already in our repo:
   [`poc-higgsfield-one-hand-fold/references/official-open-and-folded.png`](../poc-higgsfield-one-hand-fold/references/official-open-and-folded.png).
   It shows the open stroller on the left and a small folded stroller in the
   corner, with nobody in the picture.

3. **The written instructions (prompt):**
   [`poc-seedance-keyframe-fold/conditions/condition-a-prompt.txt`](../poc-seedance-keyframe-fold/conditions/condition-a-prompt.txt)
   — it tells the AI: keep the camera still, no people, keep the exact same
   stroller, and self-fold from the first picture to the last picture.

4. **The exact order we sent** (photos, prompt, settings, and the random seed
   all together) is saved in
   [`poc-seedance-keyframe-fold/out/a-probe/submission.json`](../poc-seedance-keyframe-fold/out/a-probe/submission.json),
   so anyone can check precisely what the AI received.

## A surprise roadblock: no people allowed 🙅

We first tried to use our older photos — the ones with a person demonstrating
the fold
([`start-frame.png`](../poc-higgsfield-one-hand-fold/references/start-frame.png)
and
[`end-frame.png`](../poc-higgsfield-one-hand-fold/references/end-frame.png)).
Seedance **refused** them. Its safety filter blocks any input photo that shows
a real person's face or body.

**What this means for us:** most "lifestyle" product photos (the ones with
smiling parents) can never be used as inputs for this AI. We must use
product-only photos. That's why we made the two people-free crops above.

## What came out 🎬

* 🎥 **Watch the video:**
  [`poc-seedance-keyframe-fold/out/a-probe/video.mp4`](../poc-seedance-keyframe-fold/out/a-probe/video.mp4)
* 🖼️ **See it as 12 still frames:**
  [`poc-seedance-keyframe-fold/out/a-probe/contact-sheet.png`](../poc-seedance-keyframe-fold/out/a-probe/contact-sheet.png)

The good news (things Higgsfield could never do):

* ✅ The stroller **actually folds** — start open, end folded and standing on
  its own, just like the real end photo.
* ✅ It stays the **same stroller** the whole time: same speckled canopy
  pattern, same wheels, same cup holder. No morphing into a different product.
* ✅ Cost about **$2** and took a few minutes.

The bad news (why this is not a pass yet):

* ❌ **It folds the wrong way.** The real Ready2Jet drops its handle
  *forward* and collapses down. The video shows the canopy flopping
  *backward* first. A person copying this video would be confused.
* ❌ **The stroller slowly rotates** during the fold, even though we said
  "keep the camera completely still."

## What did we learn? 🧠

The AI did not "figure out" how the stroller works. It has watched millions of
videos, so it knows what stroller-folding *usually looks like* — but it knows
nothing about *this* stroller's buttons and hinges. Our two real photos forced
it to start and end at the truth, and it invented the prettiest-looking path
in between. Pretty, but partly wrong.

So the scoreboard reads:

| Thing we wanted | Result |
|---|---|
| Same product start to finish | ✅ Yes |
| Correct final folded state | ✅ Yes |
| Correct folding motion in the middle | ❌ No — it guessed |

This matches the rule we wrote before running anything: **correct endpoints
do not prove correct middle motion.** Today's video would be fine as a
"before and after" clip, but not as instructions.

## What's next 🔜

1. Run the same test 3 more times at higher quality (pre-chosen seeds, about
   $7) to see if these results repeat.
2. Run **Condition B**: same two photos PLUS the official manual's fold
   diagrams
   ([`manual-fold-page-34.png`](../poc-higgsfield-one-hand-fold/references/manual-fold-page-34.png))
   as extra reference images. The question: does showing the AI the *middle
   steps* fix the wrong-way fold?
3. If Condition B still guesses the middle wrong, the answer for instruction
   videos is Option 2 from our
   [alternatives doc](./video-generation-alternatives.md): we animate the
   motion ourselves and let the AI only paint the surface.
