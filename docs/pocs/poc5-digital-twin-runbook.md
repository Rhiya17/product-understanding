# POC 5 Runbook: Generating the Static Digital Twin

*Written 2026-08-13. Step-by-step execution guide for POC 5 of the
[master plan](./product-page-video-poc-plan.md), using the tool shortlist
and rules decided in the
[digital-twin phase plan](./digital-twin-phase-plan.md) (Decision 1). Read
those two docs first; this one is only the "how."*

**What this produces:** a static (immovable) 3D twin of the product from
product-page images — a scored, dimensionally verified mesh per tool, and a
decision about which tool (if any) feeds POC 6 rigging.

**What this does not produce:** articulation. The output is a statue. Joints
are POC 6.

---

## Stage 0 — Prerequisites and live-API check

1. Accounts/keys needed: **`FAL_KEY` only** — already used by the Seedance
   and VACE POCs. All three tools are served by fal.ai pay-per-use (no
   Meshy subscription required):
   - Meshy v6: `fal-ai/meshy/v6/multi-image-to-3d` (1–4 images; REST queue
     `https://queue.fal.run/fal-ai/meshy/v6/multi-image-to-3d`); the
     single-image variant is `fal-ai/meshy/v6/image-to-3d`.
   - Rodin and Hunyuan 3D: their current fal endpoints.
2. **Verify the live API surface before designing requests.** The Higgsfield
   POC learned this the hard way (`dop-standard` documented but rejected;
   hidden defaults silently applied). For each tool, before spending:
   - confirm the current endpoint IDs on the fal dashboard (Meshy's is
     confirmed above; verify `fal-ai/hyper3d/rodin` and the current
     `fal-ai/hunyuan3d*` variant);
   - confirm multi-image input support and the parameter that carries it;
   - confirm seed control, if offered;
   - save one cheap probe response per tool and check the echoed parameters
     match what was sent.
3. Local tooling: Blender (headless renders, mesh inspection), Python with
   `numpy`/`Pillow` (silhouette IoU), `ffmpeg` (turntable strips). All
   already used elsewhere in the repo except Blender.
4. Record tool versions and (per Decision 1) read each tool's commercial
   license/API terms; note them in the report. A tool we cannot ship
   disqualifies itself regardless of quality.

---

## Stage 1 — Build the input pack

Directory: `poc-3d-static-twin/inputs/`.

1. **Collect the gallery.** Pull every distinct product-only view of the
   exact SKU (Ready2Jet 2212125, Splatter Art) from the official PDP —
   the same source discipline as
   [`evidence.json`](../poc-higgsfield-one-hand-fold/evidence.json). Target
   3–8 views; at least two meaningfully different viewpoints. Amazon listing
   images may supplement **only after** confirming they show the identical
   model/colorway — no sibling products, per the master plan's
   do-not-combine rules.
2. **Person-free only.** Crop or exclude any frame with a person (likeness
   rejection is provider policy at ByteDance and must be assumed possible
   elsewhere; it also degrades reconstruction).
3. **One state only.** All images must show the same state (open). Folded
   images are a separate optional run (a folded static twin is what the fit
   engine needs) — never mix states in one reconstruction job.
4. **Hold out one view.** Choose the most informative held-out view (a
   three-quarter angle not represented by the remaining set). It is used
   only for validation and must not be uploaded to any tool.
5. **Record verified dimensions** (open W×D×H and folded, from the official
   Graco spec) in the manifest. Distinguish product from package dimensions.
   These calibrate scale in Stage 3 — do not proceed without them.
6. **Write `inputs/source-manifest.json`**, following the repo convention:
   per image — source URL, retrieval date, SHA-256, viewpoint label
   (front / rear / left / right / three-quarter / top), state, and role
   (`input` or `held-out`). Mark every asset `observed`; anything derived
   (crops, background removals) lists its parent and the operation.
7. **If a 360 spin exists** (Decision 8: check, don't assume): extract
   frames, note photo-vs-CGI, and treat ~8–12 evenly spaced frames as the
   input set with several held-out frames. This is the best-case input and
   should be run as an additional condition, not mixed with the gallery
   condition.

---

## Stage 2 — Generate: one identical protocol, three tools

Run each tool with the **same input images, same order, same prompt-free
settings** (no text guidance unless a tool requires it; if required, use the
same neutral string everywhere and record it).

Per tool, per run:

```text
poc-3d-static-twin/runs/<tool>-run-01/
  submission.json      exact request: endpoint, params, input hashes, seed
  result.json          raw API response
  model/               downloaded outputs: GLB (required), plus FBX/OBJ/USDZ
  textures/            if delivered separately
```

Protocol rules (carried over from the common test protocol):

- **Three runs per tool** where the tool is stochastic (fixed seeds if
  supported; otherwise three independent runs). One lucky mesh is not a
  result.
- Multi-image mode always; never single-image.
- **Input caps:** Meshy multi-image accepts at most 4 images. When the input
  pack has more usable views, rank by angular coverage and send the best 4
  (e.g., front three-quarter, side, rear, elevated); the rest join the
  held-out pool as extra validation views. Use the same 4 for every tool.
- Highest geometry-quality settings each tool offers (this POC measures
  ceiling, not speed); record every setting.
- Cache uploads by content hash (reuse the `upload-cache.json` pattern from
  `run_seedance.py`).
- Download GLB as the canonical format for scoring; keep whatever else the
  tool exports.

Budget check: all three tools × 3 runs should stay inside the master plan's
$20–100 envelope; abort and re-plan if a probe shows otherwise.

---

## Stage 3 — Normalize: scale, orient, floor

For each mesh, in Blender (scripted, saved as `normalize.py` in the POC
folder so every mesh gets identical treatment):

1. Import GLB.
2. **Scale to truth:** uniformly scale so the mesh's bounding box best fits
   the verified open-state dimensions from Stage 1. Record the scale factor
   and the per-axis residual error — the residuals are scored later, the
   uniform scaling is not (tools output arbitrary units; only *shape* error
   counts against them).
3. Orient to a canonical frame (wheels down, front axis +Y) and drop to the
   ground plane.
4. Export `normalized.glb` alongside the original.

---

## Stage 4 — Validate

All checks are scripted where possible; every number lands in the scorecard.

### 4a. Held-out-view silhouette (pass: IoU ≥ 0.85)

1. Estimate the held-out photo's camera (manual placement in Blender is
   acceptable at POC scale; record the camera params).
2. Render the normalized mesh from that camera, transparent background.
3. Extract both silhouettes (photo: background removal; render: alpha) and
   compute IoU with a small Python script (`silhouette_iou.py`, checked into
   the POC folder).
4. Repeat for each source view as a sanity curve — source views should score
   higher than the held-out view; if not, the camera estimates are bad, fix
   before concluding anything.

### 4b. Landmark accuracy (pass: within 3% of image diagonal)

Pick 6–10 identity-critical landmarks visible in the held-out view (wheel
hubs, handle grip ends, canopy pivot, cup holder, basket corners). Mark
pixel positions in photo vs render; report max and mean offset as % of the
image diagonal.

### 4c. Dimensional accuracy (pass: within 5%)

After uniform scaling, compare non-fitted measurements against spec —
e.g., if scale was fitted on overall height, check wheelbase and width
independently. Report per-axis error.

### 4d. Invented / missing geometry (hard fail if violated)

Orbit the mesh and compare against all source views + the held-out view:

- every identity-critical component present (4 wheels, handle, canopy, cup
  holder, belly bar, basket, frame tubes);
- **no invented** controls, openings, extra wheels, or hallucinated rear
  detail (the back is the highest-risk region when input coverage is thin);
- mark surfaces `observed` vs `inferred` (any region no input image saw is
  inferred by definition — list them; customer-facing camera paths must be
  able to avoid them, per the master plan).

### 4e. Part-fusion inspection (not pass/fail — the POC 6 cost driver)

In Blender: separate by loose parts, count mesh islands, and probe whether
the fold-relevant boundaries (handle vs frame, seat vs chassis, wheels vs
legs) are separable surfaces or welded solid. Record a fusion severity
grade:

| Grade | Meaning for POC 6 |
|---|---|
| F0 | moving parts are distinct islands — rigging can start directly |
| F1 | fused but boundaries clean — hours of manual cutting |
| F2 | fused with melted boundaries — days of remodeling |
| F3 | geometry too distorted to segment economically — stop condition |

### 4f. Turntable export

360° turntable render (`ffmpeg` strip + mp4) per mesh — the human-review
artifact, and the first reusable *answer asset* if the mesh passes (novel
views tier).

---

## Stage 5 — Score and decide

One scorecard per run: `evaluation/scorecard-<tool>-run-XX.md`.

```markdown
# POC 5 scorecard — <tool> run <XX>
| Check | Result | Threshold | Pass? |
|---|---|---|---|
| Held-out silhouette IoU        |      | ≥ 0.85 | |
| Landmark max offset (% diag)   |      | ≤ 3%   | |
| Dimensional error (worst axis) |      | ≤ 5%   | |
| Identity components present    |      | all    | |
| Invented geometry              |      | none   | hard fail |
| Fusion grade                   | F_   | info   | — |
| Inferred-surface regions       | list | info   | — |
Consistency note (vs other runs of this tool):
License/terms note:
Verdict: pass / fail
```

Aggregate in `report.md`:

- per-tool: best run, run-to-run consistency (a tool that passes 1/3 is not
  a pass — same rule as every generation POC);
- rigid-control-product comparison (Decision 1): if all tools fail the easy
  product, the tool class is out; if they pass it and fail the stroller,
  that boundary is the finding — record it for POC 8;
- **decision:** which mesh (if any) graduates to POC 6, chosen by fusion
  grade and identity fidelity first, silhouette score second — a
  beautiful-but-welded F2 mesh may lose to a rougher F0/F1 mesh, because
  POC 6's human hours are the number that matters.

Map to the master plan's decision table: POC 5 pass → PDP-derived static 3D
is usable for turntables, placement, and supported camera paths (and the
folded-state run feeds the fit engine); POC 5 fail → hero-tier twins require
self-captured scans (Decision 2 assets) and the catalog static tier stays at
2.5D/showcase.

---

## Artifact layout (complete)

```text
poc-3d-static-twin/
  README.md                    short pointer to this runbook
  inputs/
    source-manifest.json
    images/                    input views (person-free, one state)
    held-out/                  the validation view(s)
  runs/
    meshy-run-01..03/          submission.json, result.json, model/, normalized.glb
    rodin-run-01..03/
    hunyuan-run-01..03/
  validation/
    normalize.py  silhouette_iou.py  render_heldout.py
    renders/                   per-run held-out + turntables
  evaluation/
    scorecard-<tool>-run-XX.md
  report.md
```

---

## Common failure modes to expect (from our own evidence)

- **Thin dark frame tubes** break or merge — the stroller is worst-case
  input (Decision 1). Score it honestly; the rigid control product tells you
  whether the tool or the product is at fault.
- **See-through mesh basket** may reconstruct as a solid block or a hole.
  Either is a component-integrity note, not automatically a hard fail —
  judge whether identity survives.
- **Hallucinated rear geometry** when input coverage is front-heavy — this
  is the hard-fail check 4d exists for.
- **Tool-side prompt/preprocessing defaults** — same class of hazard as
  Higgsfield's `enhance_prompt`; capture echoed params in Stage 0 and treat
  any mismatch as an invalid run.

---

## After POC 5

The graduating mesh enters POC 6 exactly as the master plan specifies:
segment into rigid components, infer joints (using manual diagrams, the
Decision 3 patent evidence, and Decision 2 macro shots), fit the documented
open/mid/folded states, and **log every human hour** — that number, not any
score in this runbook, decides whether the twin tier scales.
