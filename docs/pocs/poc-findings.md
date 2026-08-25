# What We Learned From Testing Higgsfield (POC Findings)

*Written 2026-07-22. Simple-language summary of two experiments. Every finding
is included, with paths to the pictures and videos so you can see the proof
yourself.*

---

## The big question we were testing

Our product wants to answer questions with videos. When no real video exists,
we want an AI (Higgsfield) to make one. But the video must be **true** — it
must show the real product doing the real thing.

So we asked: **can Higgsfield make videos that stay true, and how do we
control it?**

We ran two experiments:

| Experiment | Folder | Question |
|---|---|---|
| 1. Boxes in a trunk | `../poc-higgsfield-geometry/` | If we compute exactly where a stroller fits in a car trunk, can Higgsfield show it without messing it up? |
| 2. One-hand stroller fold | `../poc-higgsfield-one-hand-fold/` | If we describe a real stroller's fold trick very carefully in words, can Higgsfield show it correctly? |

---

## Finding 1: You can only give Higgsfield two things — a picture and a sentence

We read the docs and poked the API directly. To make a video, Higgsfield
accepts:

- **one picture** (as a web link, not a file upload),
- **a text prompt** (a description in words),
- and optionally a "camera move" style and a video length.

That's it. There is **no way** to give it measurements, coordinates, or 3D
shapes. So if we compute "the stroller fits at exactly this angle," there is no
input slot to tell Higgsfield that. The only trick left: **draw the answer into
the picture ourselves** and hope Higgsfield doesn't ruin it. That trick is what
Experiment 1 tests.

Smaller things we learned while connecting (useful for whoever builds this):

- Logging in needs **two** codes: a short "key ID" and a long "secret." The
  official docs describe it slightly wrong; we found the real way by testing.
- The picture must be hosted on a public link. Some free image hosts were
  rejected by Higgsfield; one (litter.catbox.moe) worked.
- API credits are separate from a normal Higgsfield subscription. With zero
  credits you get an error that says `not_enough_credits`.
- **Hidden discovery:** the API has secret, undocumented modes called
  `first-last-frame`. They let you give **two** pictures — the first frame AND
  the last frame of the video. This turned out to be the most important
  discovery of the day (see Finding 3).
- **Warning:** the server quietly changes your request unless you stop it. It
  rewrote our prompt (`enhance_prompt: true` is on by default) and added a
  random camera-move effect at full strength that we never asked for. This
  matters a lot in Experiment 2.

---

## Experiment 1: Boxes in a trunk

### The setup

1. A small math program figures out which ways a folded stroller box
   (52×44×18 cm) fits inside a simplified Tesla trunk box (97×100×46 cm).
   Pure math — no AI — so this part is always correct. It found 3 valid ways.
2. We draw the answer as a picture: gray see-through trunk, blue stroller box
   sitting in the computed spot. Every pixel of this drawing is true.
   - Drawing of position 1: `../poc-higgsfield-geometry/out/placement_0.png`
   - Drawing of position 2: `../poc-higgsfield-geometry/out/placement_1.png`
3. We give the drawing to Higgsfield and ask for a video.

### Test A — one picture + "please hold still" (FAILED)

We sent picture 1 with the prompt: *"slow smooth camera orbit around the
scene, objects perfectly still, keep the blue box exactly in place."*

**What happened:** for about 2 seconds, Higgsfield behaved. Then it got
"creative." It turned our trunk into a glass display case sitting on a white
pedestal, added a big dome over everything, and — worst of all — changed our
solid blue box into an **open-top tray**. It invented a whole new scene.

See it yourself:

- The video: `../poc-higgsfield-geometry/out/e2_orbit.mp4`
- Still OK at 1.5 seconds: `../poc-higgsfield-geometry/out/e2_orbit_frames/frame_004.png`
- Gone wrong at 3.5 seconds: `../poc-higgsfield-geometry/out/e2_orbit_frames/frame_008.png`
- Fully invented ending: `../poc-higgsfield-geometry/out/e2_orbit_frames/frame_011.png`

We also measured it with a number: we compared every moment of the video to
the picture we gave it (0 = identical, bigger = more different). The
difference score was 0.02 at 1 second and **0.37** by 5 seconds — it drifted
far away from the truth.

(A bonus accidental run with a junk prompt behaved similarly:
`../poc-higgsfield-geometry/out/probe.mp4`.)

**Lesson: words like "keep it exactly in place" are treated as a suggestion,
not a rule. After ~2 seconds the AI starts inventing.**

### Test B — TWO pictures, first frame and last frame (WORKED)

Using the hidden `first-last-frame` mode, we gave Higgsfield **both** ends of
the video: our drawing of position 1 as the first frame, and our drawing of
position 2 as the last frame. Higgsfield only had to invent the middle.

**What happened:** night-and-day difference. The trunk stayed a trunk for all
5 seconds. The box stayed a solid box. The video starts exactly at our first
drawing and lands almost perfectly on our second drawing. The difference score
peaked at just 0.04 in the middle and came back down to 0.016 at the end —
about **20 times better** than Test A.

See it yourself:

- The video: `../poc-higgsfield-geometry/out/e5_firstlast.mp4`
- The middle of the move: `../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_006.png`
- The ending (compare with `placement_1.png` — nearly identical):
  `../poc-higgsfield-geometry/out/e5_firstlast_frames/frame_011.png`

**Two catches:**

1. The **middle** of the video is still the AI's invention. To move the box
   between the two positions, it tipped the box up on its edge — that looks
   nice, but nobody checked if that path would actually fit in a real trunk.
   So: the start and end are true, the journey is a guess.
2. Small text in the picture (our title label) got slightly scrambled during
   the video. Don't put important text inside frames you give it.

**Lesson: pinning both ends with pictures we drew ourselves keeps the video
honest at both ends. This is our best control tool.**

---

## Experiment 2: The one-hand stroller fold

### The setup

A real product: the **Graco Ready2Jet** stroller (model 2212125). Its real
trick, from Graco's own manual: slide a thumb switch on the handle, squeeze
the lever under it with the same hand, and the stroller folds itself.

We gave Higgsfield:

- a real official Graco photo of a person with one hand on the handle:
  `../poc-higgsfield-one-hand-fold/references/start-frame.png`
- an explicit prompt describing the exact switch, exact squeeze, one hand only,
  locked camera, and product-identity constraints. The corrected test uses a
  shorter action-first version at
  `../poc-higgsfield-one-hand-fold/prompt-corrected.txt`.

The real manual pages we used as truth:
`../poc-higgsfield-one-hand-fold/references/manual-fold-page-34.png` and
`.../manual-fold-page-35.png`, plus Graco's own fold pictures:
`.../references/official-fold-sequence.png`.

### First run: failed, but had uncontrolled defaults

The stroller **never folded**. Instead, Higgsfield:

- slowly changed it into a different, bigger stroller,
- invented big red controls that don't exist on the real product,
- had the person use **both** hands (the whole point was one hand),
- moved the camera even though we said "locked camera,"
- ended the video with the stroller still open.

See it yourself:

- The video: `../poc-higgsfield-one-hand-fold/out/ready2jet-one-hand-fold.mp4`
- All 11 frames on one page: `../poc-higgsfield-one-hand-fold/out/contact-sheet.png`
- The detailed scorecard: `../poc-higgsfield-one-hand-fold/result-analysis.md`

When we audited this run afterward, we found the server's hidden defaults had
changed the experiment (see Finding 1's warning):

1. `enhance_prompt: true` — Higgsfield **rewrote our careful prompt** into
   something we never saw. So we didn't actually test *our* words.
2. A random **camera-move effect was added at full strength** — which likely
   caused the camera swing, which is exactly what triggers scene-inventing.
3. Only 1 run was done (the plan said 3), and on the fastest/cheapest model
   tier.

So that first run only showed: **prompt-only failed under default settings.**
It could not fairly prove that the exact prompt had failed.

### Corrected test: 3 clean runs, 0 passes

We then ran the experiment three times with predeclared seeds. Every job passed
an automatic parameter gate before generation:

- `enhance_prompt: false` was explicitly sent and echoed;
- the API-required motion entry was explicitly neutralized at strength `0.0`;
- the prompt, source image, model, motion, and seed exactly matched the server's
  echoed `input_params`;
- the live non-Lite, non-Turbo tier (`dop-preview`) was used.

The official SDK exposes `dop-standard`, but the live endpoint rejected it and
reported only `dop-lite`, `dop-preview`, and `dop-turbo` as valid. It also
rejected an empty motion list. Those validation failures happened before any
video generation. The clean test therefore used `dop-preview` and the required
motion ID at zero strength.

All three controlled videos failed in the same important way. None showed the
thumb switch, underside squeeze, or automatic fold. Each transformed the exact
compact side-view stroller into a larger, front-facing, fully open stroller.
The canopy, seat, handle, wheels, and frame changed.

- Combined result: `../poc-higgsfield-one-hand-fold/corrected-results.md`
- Runs, videos, request records, contact sheets, and scorecards:
  `../poc-higgsfield-one-hand-fold/out/corrected-preview-run-01/` through `-03/`

**Clean conclusion: prompt-only DOP generation is not dependable for exact
product-operation instructions.** This result is 0/3 under controlled settings,
not a claim that every possible Higgsfield workflow or future model must fail.

### Why words alone probably can't ever fully work here

Higgsfield learned "how strollers fold in general" from watching many videos.
It has no idea how *this exact* stroller's switch works. Words are too vague
to teach it mid-generation ("squeeze the lever" — which lever? which way?).
So it generates a *believable* fold, not the *correct* fold. Believable-but-
wrong is the most dangerous kind of answer our product could give.

---

## Finding on speed: minutes, not seconds

Every 5-second video we made took **3 to 7 minutes** to generate:

| Video | Model | Time |
|---|---|---|
| Test A (orbit) | lite | ~3 min |
| Bonus probe | lite | ~3 min |
| Test B (first-last) | lite first-last-frame | ~5 min |
| Stroller fold, uncontrolled first run | turbo ("fast" tier!) | ~7 min |
| Stroller fold, corrected runs (3) | preview (live quality tier) | 6 min 31–34 sec each |

The API is built for this: you submit a job, then check back until it's done.
There is no instant mode.

**This breaks an assumption in our design doc**, which says a generated answer
"may take a few seconds." Reality is 40–80× slower. Nobody will stare at a
spinner for 5 minutes. So:

- Generation can never be part of the live back-and-forth conversation.
- Retrieval (showing an existing video) is the only thing fast enough to feel
  interactive — it's not just cheaper, it's the whole experience.
- Smart move: pre-generate the predictable videos (fold, unfold, trunk
  positions) ahead of time, so users almost always hit the ready-made library.

---

## What all of this means for the product (the takeaways)

1. **Prompts are suggestions, not rules.** Even "keep everything still" gets
   ignored after ~2 seconds. Never rely on words to keep a video truthful.
2. **The only reliable steering wheel is pictures we make ourselves.** Our
   math computes the answer → our renderer draws it → Higgsfield animates it.
   The AI must never be the one deciding where things go or how they work.
3. **First-last-frame mode is the star.** Pin both ends with our own drawings
   and the video stays honest at both ends. Perfect for "show me another
   position that fits."
4. **The middle of any generated video is still a guess.** Fine as a visual
   flourish between two true positions. NOT fine as a how-to instruction —
   the invented path might be impossible in real life.
5. **Checking videos becomes doable.** Instead of the impossible job "measure
   centimeters from AI pixels," the checker just asks: does the first frame
   match our drawing? Does the last frame match? Did anything morph in
   between? All of those are answerable.
6. **Turn off the hidden defaults.** Always set the prompt-rewriter off and
   choose the camera motion explicitly, or the server changes your experiment
   (and your product answers) behind your back.
7. **Written instructions from the manual are still essential** — not to put
   in the prompt, but to (a) pick the right key pictures to pin, and (b) check
   the result against the truth.
8. **Speed reality:** minutes per clip. Design the product around retrieval
   and pre-generation; treat live generation as "it will appear here in a few
   minutes."
9. **Don't put text inside frames** you give Higgsfield — it garbles it.

## What we spent

All experiments together used a few dollars of the $30 API credit.

## What to test next (not done yet)

- Test a two-endpoint, image-constrained action using verified open and folded
  reference frames. Treat the invented middle as untrusted until independently
  reviewed; a matching last frame alone does not prove the mechanism is right.
- Test B with photorealistic drawings instead of diagram-style boxes (does
  realism in, mean realism out?).
- Repeat Test B a few times to check it works consistently, not just once.
