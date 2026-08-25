# Digital Twin Phase: Decisions and Execution Plan

*Written 2026-08-13. This doc records the eight decisions made after reviewing
every POC result to date, and turns each into an executable step. It is the
bridge between the probe phase (Higgsfield, Seedance, keyframe chain, WAN
VACE — all complete) and POC 5/6 of the
[master plan](./product-page-video-poc-plan.md), which are written but
unstarted.*

---

## Where we stand

Four generation probes produced one consistent conclusion:

| Evidence | Finding |
|---|---|
| [Higgsfield corrected runs](./higgsfield-poc-findings.md) | 0/3 — prompt-only generation cannot show a real mechanism |
| [Seedance a-probe](./seedance-poc-findings.md) | Correct endpoints, wrong motion — pinning does not buy mechanical truth |
| [Keyframe chain](./seedance-keyframe-chain-poc-findings.md) | A real mid-state helps direction but proves nothing about hinges |
| [WAN VACE probe](../poc-wanvace-control-video/) | Motion inherited from a real video holds up; needs a motion source |

Every path that produced truthful motion got it from **outside the video
model** — authored renders, real photos, a real video. The most complete
"outside source" is a **movable (articulated) digital twin**: a 3D model of
the product with segmented parts and rigged joints, verified once against the
documented states. After that, mechanical and spatial answers are rendered,
not generated, and cannot be wrong.

The hard sub-problem is not the mesh (buyable) but **joint inference**: the
mechanism is invisible in every PDP asset, and today rigging is skilled human
work. This phase exists to (a) buy the easy half, (b) measure the true cost of
the hard half, and (c) tighten the verification loop around both.

---

## Decision 1: POC 5 tool shortlist — Meshy v6, Rodin, Hunyuan 3D, Tripo3D, run comparatively

**Decision.** Execute POC 5 (static 3D from PDP images) as a four-way
comparison of Meshy v6, Rodin, Hunyuan 3D, and Tripo3D, rather than picking
one tool up front. (Tripo3D added 2026-08-20 at the product owner's
suggestion — same inputs, same scorecard, same license check as the others.)

**Why.** These are the current production image-to-3D services (surfaced via
reseller marketing — wavespeed.ai, pixeldojo.ai — so all quality claims are
unverified sales copy until we score them ourselves). The stroller is close to
worst-case input for this tool class: thin dark tubes, see-through mesh
basket, semi-reflective frame. Which tool survives that is an empirical
question.

**How.**

- Same inputs for all tools: the Ready2Jet gallery crops, person-free
  (the [ByteDance likeness rejection](../poc-seedance-keyframe-fold/README.md)
  taught us lifestyle imagery is unusable program-wide; assume other providers
  may behave the same). Use **multi-image mode** wherever the tool supports
  it — never single-image.
- Hold out one source view for validation, per the master plan.
- Also run the **rigid control product** from the three-product test set. If
  all tools fail there too, the tool class is out; if they pass there and fail
  on the stroller, we have mapped the catalog eligibility boundary (feeds
  POC 8).
- Score against the POC 5 pass conditions as written: held-out silhouette
  overlap ≥ 0.85, landmarks within 3% of image diagonal, dimensions within 5%
  after scaling to verified figures, no invented parts, and **explicitly
  inspect part fusion** — whether frame, hinges, and fabric came out as one
  welded mesh. Fusion severity is the input cost driver for Decision 2's
  rigging work.
- Verify each tool's commercial license/API terms before anything ships
  (RLDX-1 lesson: capability without a usable license is a dead end).
  Note: Hunyuan 3D is open-weights under Tencent's own community license,
  which must be read; API terms differ from model licenses.

**Deliverables.** `poc-3d-static-twin/` following the standard artifact
layout (source manifest with hashes, per-tool run directories, scorecards,
report.md). Budget: within the master plan's $20–100. Effort: 2–4 days.

---

## Decision 2: Buy the stroller — scan, film the real fold, macro the controls

**Decision.** Purchase one Graco Ready2Jet (model 2212125, ~$150–200) for the
hero-product lane.

**Why.** The POC plan's PDP-only constraint exists to answer "what does the
*scalable catalog pipeline* get from product-page inputs" — and it keeps that
job. But the hero-demo lane is a different question, and one purchase
substitutes for CAD at a fraction of the cost of pursuing it. We assessed
getting engineering CAD from Graco/Newell as unlikely (IP, counterfeiting,
liability); the realistic long-term manufacturer ask is their *marketing 3D
asset*, not STEP files. The physical unit gives us today:

1. **Our own 360° capture in both states** — phone photogrammetry
   (Scaniverse-class apps are free) beats any PDP spin and upgrades the
   product to E4 evidence.
2. **The real fold filmed from chosen angles** — simultaneously a
   retrieval-tier answer video and a clean, longer VACE control source
   (the [probe-01](../poc-wanvace-control-video/) trim was 3.35 s and got
   flagged for a "magical instant fold"; our own footage can include the
   thumb-switch/lever close-up).
3. **Macro shots of the thumb switch and handle lever** — no PDP asset shows
   them usably.
4. **Physical ground truth** for verifying the rig, the manual
   interpretation, and every generated candidate.

**How.** One afternoon of capture, following the common test protocol
(record device, lighting, capture pattern; store with hashes and provenance
in a source manifest that marks these assets `observed/self-captured` —
distinct from PDP-derived assets, so catalog-scale claims never silently
depend on them).

**Deliverables.** A `references/self-captured/` evidence pack: two-state scan
sets, fold video (wide + close-up takes), control macros. Cost: ~$200 + one
day.

---

## Decision 3: Patent search — the fold mechanism's missing documentation

**Decision.** Search Google Patents / USPTO for Graco (Newell Brands /
Graco Children's Products) filings on compact-stroller fold mechanisms before
any rigging work starts.

**Why.** Joint inference is the hard sub-problem precisely because the
mechanism is invisible in photos and described only *functionally* in the
manual ("slide thumb switch, squeeze handle lever"). Fold mechanisms are
exactly what juvenile-products companies patent, and patent drawings document
hinge geometry, latch placement, and pivot relationships with labeled parts —
the geometric evidence nothing else in our pack provides. Free, public, and
legally unencumbered as reference material.

**How.** Search terms combining assignee (Graco, Newell) with mechanism
vocabulary (one-hand fold, self-folding stroller, fold latch, telescoping
handle release). Match candidate patents against the Ready2Jet's visible
hardware from the manual pages and Decision 2's macro shots — a patent for a
*sibling* mechanism is the same trap as the wikiHow illustrations we rejected
(wrong mechanism leaks into the rig as invented geometry, a scorecard hard
failure).

**Deliverables.** A short evidence note (`docs/` or the twin POC folder)
listing matched patents, the relevant figures, and a mapping from patent part
numbers to the parts visible on the real product. Effort: half a day.

---

## Decision 4: Verifier benchmark — label what we already have, measure Qwen

**Decision.** Build a small quantitative benchmark for the Qwen3-VL verifier
from the ~10 videos we already own, before trusting it as a gate.

**Why.** The [chain POC](./seedance-keyframe-chain-poc-findings.md) showed
Qwen flip-flopping on mechanism verdicts (seg2 unsafe → stitched safe), and
the [verifier POC](./vlm-verifier-poc-findings.md) is one run per model on
one bad video. We currently cannot state the verifier's accuracy or
run-to-run consistency as numbers. A benchmark converts "promising" into a
measurement — the discipline gap identified when comparing our hand
scorecards against properly harnessed evals (Pass@k-style repeated runs
against a held-out labeled set).

**How.**

- Corpus: 3 corrected Higgsfield fails, Seedance a-probe, seg1/seg2/stitched
  chain clips, VACE probe-01, plus the official Graco fold video as the
  known-good control (answers the false-rejection question the verifier POC
  left open).
- Human-label each against the per-question checks (same product, reaches
  end state, grounded, fixed view, motion direction, controls shown, safe as
  instruction segment).
- Run each check **N=5 times per video**; report per-question accuracy vs
  human labels *and* consistency (how often 5 runs agree with each other).
- Replace the broad "safe" question with small concrete ones ("does the
  handle move toward the front wheels?") — the chain POC's own
  recommendation — and measure whether decomposition improves consistency.

**Deliverables.** `poc-verifier-benchmark/` with the labeled corpus manifest,
runner, per-question accuracy/consistency table, and a go/no-go rule for
using Qwen as the automated first gate. Cost: pennies per check × ~350
checks — under $20. Effort: 1–2 days.

---

## Decision 5: Architecture commitment — scene-graph-first; generation is a skin

**Decision.** The system's source of truth for mechanical and spatial answers
is structured scene state (the twin + evidence graph), manipulated
deterministically; video *generation* is demoted to an optional realism layer
over deterministic renders.

**Why.** Every probe failure came from asking a pixel model to originate
truth; every success came from feeding it truth it merely decorated. The
working end-state is: an LLM plans against structured state ("highlight the
lever, orbit to the rear, play the fold"), a deterministic engine
(Blender-class) renders it, and VACE-style stylization (POC 7) is applied
only when reviewers prefer it *and* it passes the mask-overlap gates. This is
also the pattern proven in adjacent industry work (LLM agents editing
game-engine scene graphs rather than generating pixels).

**Consequences.**

- The [HLD](./high-level-design.md) building blocks "Video Answer Planner"
  and "Video Compositor" target the twin's scene graph, not a generation API.
- Prompt-only generation remains prohibited for operations (trust rule 10 —
  unchanged), and pinned/keyframe generation is *labeled* as
  transition-tier, never instruction-tier.
- Verification effort shifts from per-video to per-product: the twin is
  verified once against manual + state photos + patents + real footage; its
  renders inherit that verification.

**Deliverables.** This section is the record; the HLD gets a short amendment
pointing here when the twin POC produces its first rendered answer.

---

## Decision 6: Synthetic-training-data loop — the twin renders wrong folds

**Decision.** Once a rigged twin exists, use it to mass-produce *labeled*
correct **and deliberately wrong** fold videos (reversed direction, floating,
wrong hinge, skipped states) as future fine-tuning and benchmark data for the
verifier.

**Why.** Fine-tuning beats prompt-engineering when domain data exists
(industry reference point: +15% Pass@3 from fine-tuning on 25k domain pairs),
but we have no natural corpus of labeled bad product videos — today's corpus
is ~10 clips (Decision 4). The twin closes the loop: it can render unlimited
mechanically-wrong videos *with perfect labels for free*, because we control
exactly what is wrong in each render. The verifier's known weakness —
inconsistent mechanism judgment — is precisely the check synthetic negatives
train and test best.

**How (deferred until the twin exists).** Define a defect taxonomy from real
observed failures (wrong direction, float, rotation, morphing, missing
controls, impossible path); render N variants per defect; fine-tune or
few-shot Qwen3-VL against it; evaluate on the *real* labeled corpus from
Decision 4 so synthetic training is never graded on synthetic data alone.

**Deliverables.** None now. Recorded so the rigging work in POC 6 keeps
renders scriptable (defect injection must be a parameter, not hand
animation).

---

## Decision 7: Tiering — hero twin / mid transitions / tail static

**Decision.** Products get one of three answer tiers, set by evidence grade
and product value; no tier pretends to be a higher one.

| Tier | Who qualifies | Mechanical/how-to answers | Spatial/appearance answers |
|---|---|---|---|
| **Hero** | High-value SKUs worth per-product investment (twin authored per POC 6) | Rendered from the rigged twin; VACE skin optional | Any camera path, fit engine + twin |
| **Mid** | E2–E3 products (documented states, manual) | **Manual-animated illustrated instructions** (POC 4 — no invented motion, every frame traceable) | Seedance endpoint-pinned before/after, *labeled as transitions, not instructions* |
| **Tail** | E0–E1 products | Text + evidence-graph facts, manual excerpts | Static showcase / 2.5D callouts within photographed angles |

**Why.** The twin does not scale to a catalog at 3–7 authoring days per
complex product, and most FAQ classes (weight limits, warranty,
compatibility, care) never needed a twin — they come from the evidence
graph. The tiering keeps the integrity rule enforceable: the *strongest lane
the evidence supports*, and endpoint-pinned output is never presented as an
instruction (the interpretation rule every Seedance experiment confirmed).

**Consequences.** POC 4 (manual-animation) is promoted to the mid-tier
instruction workhorse and should be executed; it remains unstarted despite
requiring almost no generative spend. Tier assignment happens at ingestion,
from the evidence grade.

---

## Decision 8: 360-spin availability — selection criterion and POC 8 audit column

**Decision.** (a) Prefer products with 360° spin imagery when choosing the
first-wave test set; (b) add "has 360 spin (photo vs CGI)" as a measured
column in the POC 8 catalog audit.

**Why.** Dense views largely eliminate the inverse problem's worst failure —
hallucinated unseen geometry — and give POC 5 dozens of held-out validation
views instead of one. This de-risks and cheapens the *static* half so that
when POC 6 struggles, we know the failure is articulation, not a hallucinated
back side (removes a confound). Two facts to record while auditing:

- Spins are almost always **one state, one elevation** — they contribute
  nothing to joint inference. The hard problem is untouched.
- Many PDP spins are **CGI renders, not photos** — which is a tell that the
  manufacturer has a 3D asset, making the marketing-asset partnership ask
  (Decision 2's "why") concrete for those SKUs.

**How.** Check the Ready2Jet's Graco and Amazon listings for a spin (not yet
verified — do not assume either way). In POC 8, record per product: spin
present, frame count, photographic vs CGI, states covered.

**Deliverables.** One column in the POC 8 audit sheet; a note in the
stroller's evidence pack once checked.

---

## Decision 9: Close the generator learning loop — recipes, calibrated verifier, hard negatives

**Decision.** Treat every offline verification verdict as reusable learning
signal for generation, in three priority-ordered loops: (1) versioned
generation **recipes** with cross-job pass-rate aggregation; (2) **verifier
calibration** (D4) as a hard precondition before any verdict signal drives
automated learning; (3) a **hard-negative library** built from rejected
candidates. Generator **fine-tuning is explicitly deferred**. (Normative
contract: LLD §7.8.)

**Why.** Every pass-rate improvement so far came from recipe rules discovered
manually — disable provider prompt rewriting, zero unrequested motion
effects, product-only references, keyframe pinning, shared ground line,
matched angles — not from model changes. Systematizing recipe selection
captures that learning automatically, across jobs and across providers. The
calibration precondition exists because Qwen's mechanism verdicts flip-flopped
in the Aug 5 POC (Segment 2 "unsafe," the stitched video containing it
"safe"): optimizing generation against an unreliable judge produces videos
that fool the judge, not videos that are correct. D4 therefore gates this
entire decision.

**How.**

- Add a versioned `recipe_id` to every `AssetGenerationSpec` (LLD §7.3):
  pin configuration, prompt template, camera policy, provider and tier.
- An offline aggregation job joins verification verdicts to recipes and
  maintains pass-rate tables per lane × product category. Recipe promotion is
  a versioned policy change — never a silent prompt edit.
- Only verifier signals that pass D4's reliability benchmark may drive
  automated recipe promotion; unreliable signals (mechanism verdicts today)
  require human labels.
- Retain every rejected candidate with its structured failure reason as
  (a) a permanent verifier regression suite and (b) optional negative
  exemplars for generation prompts. Seed the corpus with the three Higgsfield
  failures and the backward-fold Seedance video already in the repo.
- Fine-tuning the generator is re-evaluated only after POC 6/7 show whether
  generation keeps owning motion at all; if pursued, it is category-level
  (never per-SKU), on rights-cleared data only (`generate_from`), with the
  twin's synthetic renders (D6) as the preferred rights-clean corpus.

**Deliverables.** `recipe_id` field and attempt-record join (small
engineering); pass-rate dashboard per recipe version; seeded hard-negative
corpus with failure-reason labels.

---

## Execution order

```text
Now (parallel, independent):
  D3  patent search                     (½ day, $0)
  D4  verifier benchmark                (1–2 days, <$20)
  D1  POC 5 four-tool comparison        (2–4 days, $20–100)
  D2  buy + capture the stroller        (~$200, 1 day)
  D8a check Ready2Jet for a 360 spin    (minutes)
  D9a recipe_id field + pass-rate aggregation   (small engineering, $0)

Next (depends on D4):
  D9b automated recipe promotion + hard-negative regression suite

Next (depends on D1 + D2 + D3):
  POC 6 — segment + rig the fold, log human hours   ← the decisive number
  POC 4 — manual-animated instructions (mid-tier workhorse, independent)

Then (depends on POC 6):
  POC 7 — VACE skin over twin renders, judged by D4's benchmark
  D6  — synthetic defect corpus → verifier fine-tune
```

The single most important measurement in this phase is unchanged from the
master plan: **the human hours POC 6 takes.** Everything else in this doc
exists to make that measurement clean, cheap, and trustworthy.
