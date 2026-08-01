# POC: Keyframe-Pinned Fold Video with Seedance 2.0 (Option 1)

*Written 2026-07-31. This is the POC for Option 1 in
[video-generation-alternatives.md](../docs/video-generation-alternatives.md):
pin the video down with more real photos. It reuses the evidence pack and the
test protocol from the
[Higgsfield one-hand-fold POC](../poc-higgsfield-one-hand-fold/), whose
controlled result (0/3 folds, product morphed every time) is the baseline this
experiment must beat.*

---

## The question

> Given verified photos of the Graco Ready2Jet in its open and folded states,
> plus the fold-step images from the official manual, can Seedance 2.0 produce
> a video of the fold that keeps the exact product identity and reaches every
> pinned state — where Higgsfield, given one photo and text, could not?

Why Seedance specifically: it accepts exactly the inputs Higgsfield lacked.

| Input | Higgsfield | Seedance 2.0 (fal.ai) |
|---|---|---|
| Start image | 1 (public URL only) | `image_url`, uploaded from local disk |
| End image | Only via hidden `first-last-frame` mode | `end_image_url`, documented |
| Extra reference images | No | Up to 9 (`@Image1` … syntax in prompt) |
| Reference video | No | Up to 3 clips |
| Seed control | Yes | Yes (documented `seed` parameter) |
| Cost | ~$ per clip, 3–7 min | $0.24–0.30/sec (~$2–2.42 per 8s clip) |

The Higgsfield POC's one success (geometry Test B) came from pinning both
endpoints. This POC extends that idea: pin the endpoints **and** hand the model
the intermediate evidence, so it has as little room to guess as possible.

## What we already know (do not re-learn this)

From the [Higgsfield findings](../docs/higgsfield-poc-findings.md):

1. Text descriptions of mechanics are ignored; the model guesses and guesses
   wrong. Baseline control: 0/3, no fold shown, product morphed.
2. Pinning endpoints with real images works dramatically better (geometry POC).
3. Providers apply hidden defaults (prompt rewriting, camera motion). Verify
   what the server actually received before trusting any run.
4. Generation is slow and asynchronous. Submit, poll, download.

New learning from this POC (2026-07-31): **fal/ByteDance rejects input
images containing real-person likenesses** (`content_policy_violation`,
`partner_validation_failed`). The official lifestyle photos with the
demonstrator are unusable as Seedance inputs. All conditions therefore use
person-free product crops from the studio shot
(`official-open-and-folded.png`), and prompts describe the hands-free
self-fold. This constraint applies program-wide: PDP lifestyle imagery with
models cannot feed ByteDance-partnered video APIs.

## Evidence sources: what's in and what's out

**In:** official Graco assets only — the PDP photo crops (start frame, end
frame, marketing fold-sequence with a genuine mid-fold state) and manual page
34 (prep steps + thumb-switch/lever diagrams). All already in
`../poc-higgsfield-one-hand-fold/references/`.

**Evaluated and rejected:**

- *Third-party YouTube videos* — decision: do not depend on downloaded YouTube
  content for POC inputs.
- *wikiHow "Fold a Graco Stroller"* — inspected 2026-07-31: cartoon
  illustrations of generic older-model Graco travel-system strollers with a
  strap-pull/seat-tilt fold. Wrong product class, wrong mechanism, not
  photographic. Feeding it to the model invites sibling-mechanism leakage —
  a scorecard hard failure (invented controls).

## Conditions

All conditions use the same product, prompt discipline (locked camera, exact
identity preservation, no invented parts), duration, aspect ratio, and
resolution. Three runs each with pre-declared seeds (42001–42003).

### Condition A — endpoints only (parity with the Higgsfield trick)

`image-to-video` endpoint with `image_url` (open state) + `end_image_url`
(folded state). No manual images. This measures whether Seedance can connect
two verified states of a *mechanism* — something the Higgsfield hidden mode
was never tested on for the fold.

### Condition B — endpoints + manual step evidence (the real Option 1 test)

`reference-to-video` endpoint. Inputs, in `@Image` order:

1. `@Image1` — start frame (open stroller, official photo)
2. `@Image2` — end frame (folded stroller, official photo)
3. `@Image3` — official fold-sequence image (contains a real mid-fold state)
4. `@Image4` — manual page 34 (prep steps + control diagrams)

The prompt maps each step of the fold to its evidence image. This is the
condition the whole POC exists for: does intermediate visual evidence buy us
correct intermediate motion?

### Condition C (stretch, optional) — add a reference video

Condition B plus a short rights-cleared clip of a similar-mechanism fold in
`video_urls`. Only run if A or B shows promise and a legitimate clip is
available (e.g., filmed ourselves, or licensed). Note the risk: the reference
stroller's mechanism may leak into the output and corrupt SKU identity —
score it, don't assume it helps.

### Scoring note: the manual's prep steps

Manual page 34 documents two prep steps (rotate cup holder, rotate front
wheels) that the official marketing fold-sequence omits. **Decision, made
before scoring:** runs are scored against the simplified marketing sequence
(the fold action itself); prep steps are not required, but showing a *wrong*
prep action still counts as an invented action (hard failure).

## Protocol

Follows the [common test protocol](../docs/product-page-video-poc-plan.md):
three pre-declared seeds, exact request/response capture, contact sheets,
score before looking at cost. Specifics for this POC:

- Provider: fal.ai. Endpoints `bytedance/seedance-2.0/image-to-video` and
  `bytedance/seedance-2.0/reference-to-video` (plus `/fast/` variants for
  probes). Local files are uploaded via fal storage at submit time — no
  external image hosting.
- First run is a cheap `--tier fast` probe to validate the request shape and
  check for prompt rewriting before spending on the quality tier.
- Duration 8s, aspect ratio 9:16 (matches the portrait start frame), 720p,
  audio off.
- `run_seedance.py` saves `submission.json` (with per-file SHA-256),
  `result.json`, the video, extracted frames, and a contact sheet per run —
  same artifact layout as the Higgsfield POC.

## Scoring

Use the [shared scorecard](../docs/product-page-video-poc-plan.md#shared-scorecard)
(0–2 on SKU identity, component integrity, state accuracy, motion accuracy,
temporal stability, instruction completeness, camera discipline, source
traceability). Hard failures apply — inventing or relocating a control, model
change, or a physically impossible transition fails the run regardless of
total score.

Interpretation rule carried over from POC 3 of the master plan: **correct
endpoints do not prove correct intermediate mechanics.** A condition that pins
the endpoints but invents the motion qualifies as a before/after transition,
not an instruction video.

## Decisions this POC feeds

| Outcome | What it means |
|---|---|
| A fails endpoints | Seedance is not better than Higgsfield for us; deprioritize Option 1 |
| A passes, B no better than A | Manual images don't transfer; Option 1 caps out at before/after transitions |
| B shows evidence-backed motion in ≥2/3 runs | Option 1 is viable for instruction candidates; expand to the 3-product set from the master plan |
| B helps but motion unverified | Pair Option 1 output with Option 2 (skeleton tracing) for the motion-critical middle |

## Running it

```bash
pip install fal-client requests
export FAL_KEY=...               # from fal.ai dashboard
# 1. Cheap probe to validate the API shape:
python run_seedance.py --condition a --run-label probe --tier fast
# 2. Scored runs:
python run_seedance.py --condition a --runs 3
python run_seedance.py --condition b --runs 3
```

Budget: standard tier is $0.3024/sec → an 8s clip is ~$2.42. Two conditions
x 3 runs + probes ≈ **$16–$20**, well under the $50 cap the master plan sets
for POC 3-class work.
