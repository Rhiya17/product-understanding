# POC Plan: Product Videos From Product Detail Pages

*Written 2026-07-30. This plan assumes the only inputs we can reliably obtain
are an Amazon-style product detail page and, sometimes, a product manual. It
does not assume access to the physical product, manufacturer CAD, unpublished
photos, or a real demonstration video.*

---

## What these POCs need to answer

The goal is not to find one AI model that can make every product video. The
goal is to determine:

> **Which kinds of useful product video can we create from product-page
> evidence, what input evidence does each kind require, and where must we stop
> because the result would be misleading?**

The experiments deliberately move from low-risk appearance videos to
high-risk mechanical instructions:

```text
Static showcase
    ↓
Novel product views
    ↓
Before/after state transition
    ↓
Manual-based illustrated instruction
    ↓
Static reconstructed 3D asset
    ↓
Articulated 3D mechanism
    ↓
Photorealistic rendering of verified motion
```

Each POC should produce a useful decision even when it fails.

---

## Inputs we are allowed to use

For each product, build an evidence pack from:

- product title, brand, model number, variant, and color;
- gallery and hero images;
- lifestyle images;
- 360-degree spins or product-page videos, when present;
- images of alternate states such as open, folded, assembled, or stored;
- dimensions and weight, after distinguishing product dimensions from package
  dimensions;
- A+ content, feature diagrams, and callouts;
- the official manual, when linked.

We must not silently combine:

- different model numbers;
- sibling products with similar names;
- different colors when their geometry may differ;
- accessories or configurations not included with the selected product;
- package dimensions and product dimensions.

Every source asset should retain its page URL, retrieval date, product
identifier, and source location.

---

## Evidence grades

Every product receives an evidence grade before video generation.

| Grade | Evidence available | Maximum defensible output |
|---|---|---|
| **E0** | Text plus one usable product image | Static image, cutout, callouts, or very limited image animation |
| **E1** | Several views of one product state | Identity-preserving showcase or approximate static 3D |
| **E2** | Several views plus documented open/closed states | Before/after comparison and experimental state interpolation |
| **E3** | E2 plus a manual with clear parts, actions, and step diagrams | Illustrated instruction or candidate articulated 3D model |
| **E4** | Real motion, 360 capture, CAD, or equivalent evidence | High-confidence mechanism reconstruction |

E4 is not expected from a normal product detail page. The point of the POCs is
to learn how much value can be delivered at E0–E3.

---

## Test-product set

Do not test only the stroller. A stroller failure would not tell us whether
the approach works for simpler products.

Use three products representing different difficulty:

1. **Rigid product:** no moving parts, at least four clean gallery views.
   Example class: appliance, luggage, or storage container.
2. **Simple articulated product:** one obvious hinge or slider and documented
   start/end states. Example class: folding handle, hinged lid, or step stool.
3. **Complex articulated product:** several linked parts and occlusions.
   The Graco Ready2Jet stroller remains the hard target.

Prefer products for which the detail page exposes a normal, realistic mix of
studio photos, lifestyle images, dimensions, and a manual. Do not choose only
unusually complete pages.

---

## Common test protocol

All generative conditions must follow the same protocol:

- Use three predeclared seeds or three independent runs.
- Save the exact model name, model version, date, prompt, settings, and input
  asset hashes.
- Disable prompt rewriting and automatic camera effects where the API permits.
- Keep comparison clips at the same duration, frame rate, resolution, and
  aspect ratio.
- Generate a contact sheet and extract start, quarter, middle, three-quarter,
  and final frames.
- Score the result before looking at cost or aesthetic preference.
- Keep unsuccessful outputs; they are experimental evidence.

For an instructional video, one attractive run out of three is not a pass. A
method must be repeatable enough to support a production review process.

The existing Higgsfield prompt-only stroller test is the baseline control and
should not be repeated unless a materially different model or input control is
being evaluated. See [Higgsfield POC findings](./higgsfield-poc-findings.md).

---

## POC 1: Can we create a safe static-product video?

### Question

Can a single PDP image become a short, useful video without changing the
product or implying an undocumented action?

### Inputs

- One high-resolution hero image.
- Product title and a small number of verified feature facts.

### Build

Create two versions:

1. **Deterministic 2.5D:** background removal, depth-based parallax, a slow
   camera push, feature highlights, and text overlays.
2. **Generative image-to-video:** request a locked product with only a small
   camera or lighting change.

No doors, handles, wheels, latches, or other product parts may move.

### Pass conditions

- Product silhouette and component count remain unchanged.
- Logo, controls, and visible attachments stay in the same locations.
- No unsupported back side or hidden surface is revealed.
- The video communicates at least one verified product fact.
- For the generative method, at least three of three runs pass the identity
  gates.

### What this POC tells us

This establishes the lowest-risk video category available to nearly every
product. It also tells us whether generative motion provides enough value over
simple deterministic motion graphics to justify its risk.

### Expected effort

Half a day to one day. Experimental API budget: under $20.

---

## POC 2: Can several PDP images preserve product identity across viewpoints?

### Question

Can gallery images produce a short orbit or novel camera move without turning
the product into a sibling model?

### Inputs

- Three to eight images of the same variant and state.
- At least two meaningfully different viewpoints.

### Build

Compare two tracks:

1. **Direct multi-reference video:** provide the gallery images as identity or
   keyframe references to a video model.
2. **Reconstruct then render:** estimate a static 3D representation from the
   gallery images and render the camera move deterministically.

The camera path must remain within the angular coverage supported by the input
images. Do not request a full orbit when the back of the product was never
shown.

### Pass conditions

- Visible parts, proportions, branding, and material remain consistent.
- The output does not reveal obviously invented controls or openings.
- The camera transition is temporally stable.
- A render corresponding to each source viewpoint resembles that source.
- Any inferred surface is labeled internally and excluded from unsupported
  customer-facing angles.

### What this POC tells us

It separates two different capabilities:

- making plausible video from several references;
- building a reusable spatial asset from those references.

The second is more valuable if the asset can later support many questions.

### Expected effort

One to two days. Experimental compute/API budget: under $50.

---

## POC 3: Can verified product states be connected?

### Question

If the PDP or manual shows both an open and a closed state, can a model produce
a useful transition between them?

### Inputs

- Verified start and end images of the exact product.
- Preferably one or more intermediate states.
- Manual text describing the action.

### Build

Run three conditions:

1. Start image plus text only.
2. Start and end images.
3. A chain of short start/end segments using every verified intermediate
   state.

Normalize crop, scale, viewpoint, and background before generation. Run a
second condition with the source images as-is to measure how badly mismatched
viewpoints hurt the method.

### Pass conditions

- Every pinned state is reached correctly.
- The product retains the exact SKU identity.
- No part appears, disappears, melts, or passes through another rigid part.
- The action order agrees with the manual.
- The video does not invent a hand position or control that contradicts the
  manual.

### Interpretation rule

Correct endpoints do not prove correct intermediate mechanics. Results from
this POC may support:

- an illustrative before/after transition;
- a non-instructional product-state video;

but not a mechanical instruction unless the intermediate motion independently
passes review.

### What this POC tells us

This measures the limit of keyframe control using only evidence that is
realistically available on a product page.

### Expected effort

One to two days. Experimental API budget: under $50.

---

## POC 4: Can the manual become an instructional video without inventing 3D?

### Question

Can we generate a genuinely useful instruction video by animating the manual's
evidence instead of synthesizing photorealistic motion?

### Inputs

- Official manual PDF.
- Product-page images for visual identity.
- Exact product model and manual revision.

### Build

1. Extract the relevant manual steps and diagrams.
2. Convert each step into:
   - starting state;
   - part being manipulated;
   - action and direction;
   - release point or control;
   - resulting state;
   - source page and figure.
3. Clean or redraw the manual line art.
4. Animate highlights, arrows, ghosted start/end positions, zooms, and cuts.
5. Use product photos for an opening identity shot and final state comparison.

Continuous motion is optional. When the manual does not show the path, use a
cut or dissolve rather than inventing it.

### Pass conditions

- Every visible action is traceable to a manual page.
- Steps appear in the correct order.
- No undocumented intermediate mechanism is shown.
- A reviewer can recover the complete documented sequence from the video and
  manual together.
- The result remains understandable without narration.

### What this POC tells us

This tests whether “video generation” needs to mean photorealistic video at
all. It may be the most scalable trustworthy instruction format available
from manuals.

### Expected effort

One to two days for the first product and substantially less after a reusable
template exists. Little or no generative-video spend is required.

---

## POC 5: Can PDP images become a useful static 3D asset?

### Question

Can we create a reusable product representation from ordinary gallery images,
without CAD or a physical scan?

### Inputs

- Four or more useful product viewpoints when available.
- Published product dimensions.
- One source image reserved as a held-out validation view.

### Build

Compare:

1. A product-focused image-to-3D or sparse-view reconstruction pipeline.
2. A scene/world-generation system such as World Labs Marble as a benchmark,
   not as the assumed winner.

For each output:

- scale it using verified product dimensions;
- render it from the estimated source cameras;
- export a turntable;
- mark surfaces as observed or inferred;
- inspect whether moving parts are fused into one mesh.

### Pass conditions

- Held-out-view silhouette overlap is at least 0.85.
- Major visible landmarks remain within 3% of the image diagonal.
- Overall dimensions are within 5% where PDP dimensions are unambiguous.
- All identity-critical components visible in the sources are present.
- No extra handles, wheels, controls, or openings are introduced.
- At least a limited customer-facing camera path can avoid low-confidence
  surfaces.

### What this POC tells us

It determines whether generated 3D is useful as:

- a reusable visualization asset;
- a source for deterministic camera moves;
- a starting point for manual cleanup and rigging;

even if it is not yet a mechanical digital twin.

### Expected effort

Two to four days. Experimental compute/API budget: $20–$100. Artist cleanup
time must be recorded separately from model execution time.

---

## POC 6: Can a manual and generated mesh become an articulated model?

### Question

Can we turn the static asset from POC 5 into a mechanically constrained model
using only the PDP's product states and the official manual?

### Inputs

- Best static asset from POC 5.
- Open and closed reference images.
- Manual steps and diagrams.
- Verified overall dimensions.

### Build

1. Separate the generated mesh into rigid components.
2. Identify candidate hinge, slider, and latch locations.
3. Define joint axes, motion limits, and component relationships.
4. Fit the open and closed configurations to their respective source images.
5. Keyframe or solve a constrained path between the states.
6. Render an untextured diagnostic animation before attempting realism.

Human modeling and rigging are allowed. The POC measures how much human work
is required; pretending that step is automated would hide the main scaling
question.

### Pass conditions

- The raw diagnostic animation follows every documented action.
- Rigid components remain rigid.
- No component self-intersects or passes through another.
- The folded state matches the published dimensions within 5%, when the
  dimensions are reliable.
- The visible latch or control is in the correct location.
- A reviewer can explain every joint from product evidence.
- Total human authoring time is recorded.

### Stop conditions

Stop rather than fabricate when:

- the necessary hinge is never visible;
- the manual omits a required relationship between parts;
- different rigs satisfy the same visible evidence but produce materially
  different motions;
- the generated mesh is too fused or distorted to segment economically.

### What this POC tells us

This is the decisive test for exact mechanical video from PDP-only inputs. A
technical pass is not enough; the measured authoring time must also support
the intended catalog scale.

### Expected effort

Three to seven working days for the first complex product. The main cost is
3D authoring and review, not inference.

---

## POC 7: Can AI make a verified control animation photorealistic?

### Question

Once motion is correct in the diagnostic 3D animation, can a generative model
improve realism without changing that motion?

### Inputs

- The verified animation from POC 6.
- Per-frame depth, edge, segmentation, and object-ID passes.
- PDP product images as identity and texture references.
- Verified first and last frames.

### Build

Compare:

1. Normal Blender rendering with simple materials.
2. Frame-controlled generative stylization using a control-video pipeline
   such as Wan VACE or NVIDIA Cosmos Transfer.

Keep the camera locked and use short segments. Pin verified frames wherever
the chosen model permits.

### Pass conditions

- Stylized mask overlap with the control render is at least 0.95.
- Identity-critical landmarks stay within 2% of the frame diagonal.
- No rigid component changes shape or count.
- The latch and hand-contact region remain readable when hands are shown.
- Three of three runs preserve the documented action.
- Reviewers prefer the stylized result enough to justify the added failure
  surface.

### What this POC tells us

It determines whether AI should be part of the final renderer or whether a
conventional 3D render is the safer production output.

### Expected effort

One to two days once POC 6 exists. Experimental compute/API budget: $20–$100.

---

## POC 8: What percentage of a real catalog is eligible?

### Question

After the single-product experiments, how often can the pipeline produce each
video class from normal PDP evidence?

### Inputs

Select 12–20 products across:

- rigid and articulated products;
- strong and weak PDP image sets;
- products with and without manuals;
- simple and complex actions;
- multiple brands and visual styles.

### Build

Run only the automated evidence-ingestion and eligibility stages first.
Attempt the appropriate successful POCs on a stratified subset.

Measure:

- percentage qualifying for POC 1, 2, 3, 4, 5, and 6;
- processing time and human time per product;
- pass rate after review;
- cost per accepted second of video;
- percentage falling back to static or illustrated content;
- most common missing evidence.

### Pass conditions

This POC does not have one universal quality threshold. It passes if it yields
a reliable coverage and cost model that supports a product decision.

### What this POC tells us

One successful stroller demo cannot establish a scalable product. This POC
reveals the actual catalog coverage of each output level.

---

## Shared scorecard

Score every video from 0 to 2 on each dimension:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **SKU identity** | Different product | Noticeable drift | Exact visible identity preserved |
| **Component integrity** | Parts invented or lost | Minor deformation | Count and shape preserved |
| **State accuracy** | Wrong state | Approximate state | Matches verified evidence |
| **Motion accuracy** | Impossible or wrong | Plausible but unverified | Evidence-backed motion |
| **Temporal stability** | Severe morphing/flicker | Minor drift | Stable throughout |
| **Instruction completeness** | Missing critical action | Partially shown | All documented steps visible |
| **Camera discipline** | Hides or changes action | Some distraction | Supports comprehension |
| **Source traceability** | Unsupported | Partially supported | Every claim traceable |

The numeric total is useful for comparing experiments, but the following are
automatic hard failures for an instructional output:

- inventing or relocating a control;
- omitting a required step;
- changing the product model;
- violating a rigid joint;
- presenting unverified dimensions as exact;
- obscuring the critical action;
- showing a physically impossible transition.

An average score cannot compensate for a hard failure.

---

## Recommended execution order

### Sprint 1: Find the boundary of useful video

Run:

- POC 1 — static-product micro-video;
- POC 2 — multi-view identity;
- POC 3 — state interpolation;
- POC 4 — manual-based illustrated instruction.

Use the same three-product test set. This should take approximately one
working week and will identify which video classes are immediately viable.

### Sprint 2: Test whether we can manufacture reusable assets

Run:

- POC 5 — static 3D reconstruction;
- POC 6 — articulated model, only on the best-supported simple product and
  then the stroller.

This sprint answers whether PDP-derived 3D can support a product, and what the
real human cost is.

### Sprint 3: Decide the production renderer and catalog coverage

Run:

- POC 7 — controlled photorealistic stylization;
- POC 8 — catalog eligibility and unit economics.

Do not begin broad catalog testing until the earlier experiments have produced
clear acceptance rules.

---

## Decision table after the POCs

| Outcome | Product decision |
|---|---|
| POC 1 passes | Offer low-risk showcase and feature-callout videos broadly |
| POC 2 passes only through reconstruction | Build reusable static spatial assets; avoid direct novel-view video |
| POC 3 passes endpoints but not motion | Offer before/after transitions, explicitly not instructions |
| POC 4 passes | Offer manual-grounded illustrated instruction as the default instructional format |
| POC 5 passes | Use PDP-derived static 3D for turntables, placement, and supported camera paths |
| POC 6 passes at acceptable effort | Produce deterministic articulated videos for eligible hero products |
| POC 7 passes | Use generative rendering as a finish over verified motion |
| POC 7 fails | Ship conventional 3D rendering rather than sacrificing truth |
| POC 8 shows low eligibility | Keep video selective and provide static/illustrated fallbacks |

---

## Required experiment artifacts

Store each experiment under a predictable structure:

```text
pocs/product-page-video/<poc-id>/<product-id>/
  inputs/
    source-manifest.json
    images/
    manual/
  requests/
    run-01.json
    run-02.json
    run-03.json
  outputs/
    videos/
    frames/
    contact-sheets/
  evaluation/
    scorecard-run-01.md
    scorecard-run-02.md
    scorecard-run-03.md
  report.md
```

The source manifest should distinguish observed, derived, and generated
assets. This provenance is essential when an output is later used to answer a
product question.

---

## Recommendation

The first investment should not be a full stroller digital twin. Run POCs
1–4 to determine which useful video categories work from ordinary PDP inputs,
then build one static 3D asset in POC 5. Only proceed to articulated rigging
when the static asset and the manual provide enough evidence to explain the
mechanism without guessing.

This sequence gives us several chances to discover a viable product:

- broad, low-risk showcase videos;
- more selective novel-view videos;
- manual-grounded illustrated instructions;
- static 3D visualization;
- a narrow tier of verified mechanical videos.

The final product can support multiple output levels. It does not need every
SKU to qualify for photorealistic articulated video.

For the technical landscape behind these experiments, see
[Beyond Higgsfield: Every Way to Make a Truthful Product Video](./video-generation-alternatives.md)
and [Grounded Video Generation for Product Understanding](./grounded-video-generation.md).
