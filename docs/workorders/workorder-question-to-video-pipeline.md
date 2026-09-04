# Work order: question → grounded video pipeline (agent handoff)

*Written 2026-08-28. Owner-approved design from the grounded-video discussion.
This document is the build spec for the implementing agent. It extends
[workorder-grounded-video-pipeline.md](workorder-grounded-video-pipeline.md)
(segment interpolation + verification, already built) with the stages that
feed it: intent understanding, fact-card retrieval, image retrieval, and
evidence-anchored image synthesis for missing keyframes.*

## Purpose

Answer "show me how to X" questions with a real motion video that is
**provably grounded in the product's evidence pack**, generated once,
asynchronously, and served pending owner review. The generative models are
never allowed to decide what is true — they only compose retrieved evidence
into stills and interpolate motion between verified stills.

## Non-negotiable principles

1. **No text-only generation.** Every generated image is anchored on
   retrieved evidence images; claim text only steers the *state change*.
   (Higgsfield POC: text + one photo → 0/3, product morphed. This rule is
   why.)
2. **Fail closed.** Any gate failure at any stage → that artifact is not
   registered and not served; the text+image answer stands, with no
   placeholder promising a video that will not come.
3. **Everything registered, nothing published.** All generated artifacts
   land in the evidence pack as pending media (`approved_by: null`) with full
   provenance (inputs, model, request id, seed, verdicts) for the owner
   review pass.
4. **Generate once, serve forever.** Results are cached in the pack; a repeat
   question serves the registered asset, it never re-generates.

## Pipeline overview

```
question
  │
  A. intent understanding        (EXISTS: Luna planner, system/luna_planner.py)
  │     → product, procedure, requested modality
  B. fact-card retrieval         (EXISTS: system/answer.py; serve text answer NOW)
  │     → ordered step claims with quotes + tiers
  C. image retrieval             (BUILD: fact-card → image links helper)
  │     → evidence images bound to each claim (+ manual page figures)
  D. state graph + keyframes     (BUILD: the new core)
  │     → visually distinct states; keyframe per state:
  │        retrieved if evidence exists, SYNTHESIZED if missing
  │        (multi-image composition anchored on evidence) → VLM gate
  E. image-to-video segments     (EXISTS: app/keyframe_video.py)
  │     → Seedance first/last-frame per adjacent state pair → VLM gate
  F. stitch + register + serve   (EXISTS: keyframe_video + video_jobs + UI)
        → one MP4 + poster + verification.json, pending review;
          UI placeholder swaps in the video when ready
```

Stages A–B run synchronously (the user gets the text+steps+images answer
immediately). Stages D–F run inside the existing async video job
(`app/video_jobs.py`); the UI already shows "Video generating…" and polls
`/api/video-status`.

## Stage specs

### A. Intent understanding (exists — do not rebuild)

`LunaPlanner.plan_intent` maps the question to a request-scoped tool
(`show_procedure` / `search_evidence` / clarify / unsupported) with product
and procedure IDs from an allowlist. Requested modalities (e.g. "show me a
video") are captured in `requested_modalities`. No changes required beyond:
pass `requested_modalities` through to the video job so a question that
explicitly excluded video never enqueues one.

### B. Fact-card retrieval (exists — do not rebuild)

`system/answer.py` retrieves and composes ordered STEP claims into one
procedure answer (score, status, tier, citations with quotes). This is the
text answer served immediately and the authoritative step list for stages
C–D. The claims are the only permitted source of state semantics.

### C. Image retrieval: fact-card → image links (small build)

Today images reach claims through `media-bindings.json` (claim_ids ↔ image
sources). Build a helper that, given a claim id, returns its evidence images
with local paths and provenance:

```
evidence_images(packs_root, vault_root, product_dir, claim_ids) ->
  [{claim_id, source_id, local_path, origin_url, kind: "IMAGE"|"PDF_FIGURE",
    page}]
```

Include manual-page figures: a claim's `source_bindings` carry `page`
numbers; render that page (the `render_pdf_page` helper in app/server.py
already does this at 144 DPI) — manual figures are documented state truth
and the strongest anchor for intermediate states. This helper is also how a
"fact card links to its image" requirement is met without schema changes; if
the owner wants explicit links later, add `image_source_ids` to claims as a
derived, validated field — do not hand-edit claims.

### D. State graph + keyframe acquisition (the new core — build)

**D1. Derive the state graph.** For one procedure, map the ordered claims
onto *visually distinct states*. Rule: a keyframe per distinct state, a
segment per continuous motion between adjacent states — NOT per claim.
Claims map N:1 onto states ("check that it is secure" changes nothing
visually; it maps to the previous state). Output, appended to the existing
registry `evidence-packs/<product>/procedure-keyframes.json`:

```json
{
  "procedure": "connect_aux_cable",
  "states": [
    {"state_id": "s0", "description": "headphones and Mac separate, cable loose",
     "claim_ids": []},
    {"state_id": "s1", "description": "2.5 mm end seated in LEFT earcup port",
     "claim_ids": ["claim_bqcu2_step_aux_1"]},
    {"state_id": "s2", "description": "3.5 mm end seated in the Mac jack",
     "claim_ids": ["claim_bqcu2_step_aux_2"]}
  ],
  "segments": [
    {"segment_id": "seg1", "start_state": "s0", "end_state": "s1",
     "motion_prompt": "...", "duration_seconds": 4},
    {"segment_id": "seg2", "start_state": "s1", "end_state": "s2",
     "motion_prompt": "...", "duration_seconds": 4}
  ]
}
```

The graph may be drafted by an LLM from the claims but is **curated data**:
it is written to the registry, reviewed like any pack file, and the pipeline
executes only what is registered. Keep `start_path`/`end_path` support for
already-curated procedures (Graco fold) — a state may resolve either to a
curated file or to a synthesis spec.

**D2. Acquire each state's keyframe — retrieve first.** Keyframe sources, in
preference order:

1. an evidence image that *already shows the state* (e.g. the Bose earcup
   photo with cable attached ≈ s1) — register it directly;
2. a manual figure rendered from the bound page (documented state truth);
3. a **3D twin render** (Tripo3D / photo-projection): render the exact
   angle or state from the product's twin. Allowed ONLY when the twin's
   verdict file shows it passed the scale and camera gates AND its license
   check is cleared — the existing Bose twin fails both (147% worst-axis
   scale error, `license_status: OPEN — do not ship`) and must not be used
   until re-scanned/cleared. A gated twin render is also a first-class
   *anchor input* to D3 composition, not just a standalone keyframe.

Synthesis (D3) is only for states none of these sources show.

**D3. Synthesize missing keyframes (evidence-anchored composition).**
Inputs: 2–4 retrieved evidence images (product photo(s), the Mac side view
showing the real jack, the cable/earcup photo, the manual figure for the
step) + a composition prompt derived from the claim text. Model: a fal
multi-image composition/edit endpoint (Seedream / nano-banana class — the
implementing agent picks the current endpoint from fal's catalog and records
it; make it env-configurable like the other engines). The prompt must
restate the claim's physical specifics ("the 2.5 mm end of the cable, into
the port on the LEFT earcup") and forbid invention ("no other objects, no
text, no logo changes, keep both products exactly as in the reference
images").

**D4. Keyframe verification gate (before registration).** VLM check
(`fal-ai/any-llm/vision`, qwen3-vl, temperature 0, JSON verdict — reuse
`parse_verdict` in app/keyframe_video.py) with the *evidence images and
claim quotes as ground truth*:

- same exact products as the reference images (identity, colors, parts)?
- state matches the claim (checklist generated from claim text: correct
  cable end, correct earcup side, correct Mac port position vs the side-view
  photo)?
- invented or vanishing parts?
- verdict pass|fail

Fail → one recompose retry with the failure reason appended to the prompt;
second fail → state unresolved → procedure refused (no video job attached;
`can_generate` returns false). Passing keyframes are written to
`generated-assets/<product>/keyframes/<procedure>-<state_id>.png`, hashed,
and referenced from the registry with provenance
(`composed_from: [source_ids]`, model, request id, verdict path).

**Storyboard bonus (serve early):** once all states pass D4, the keyframe
sequence is itself serveable as an ordered image answer (bind as pending
IMAGE-like derived assets to the step claims). Video is the upgrade, not the
prerequisite.

### E. Image-to-video segments (exists — extend only)

`app/keyframe_video.py`: per segment, Seedance 2.0 first/last-frame
(`bytedance/seedance-2.0/image-to-video`; `fast` tier via env), then the
segment VLM gate (same product vs keyframes, reaches end state, no invented
parts, fixed camera). One failed segment fails the job. Extend only to
resolve `start_state`/`end_state` through the state graph (D) in addition to
the current literal `start_path`/`end_path`. Segments are pinned by
*images* at both ends, so drift cannot compound across the chain. Kling v3
start/end-frame is an approved second engine behind the same interface —
add only after an A/B on one registered procedure justifies it.

### F. Stitch, register, serve (exists — do not rebuild)

Stitch passing segments (OpenCV), poster from the first keyframe, register
asset + claim bindings in the pack (pending, watermarked, provenance +
verification JSON), serve through the existing async job / placeholder /
poll / swap UI. Renderer policy stays: `auto` = this grounded pipeline with
refusal; `fal` (direct wan) and `deterministic` (slides) remain explicit
experimental flags.

## Gates summary (all fail-closed)

| Gate | Ground truth | On fail |
|---|---|---|
| D4 keyframe | evidence images + claim quotes | 1 retry, then refuse procedure |
| E segment | the segment's own two keyframes | fail whole job, serve nothing |
| Owner review | human, in-app review mode | stays pending / rejected |

## Engines and knobs

| Purpose | Default | Env |
|---|---|---|
| Composition (D3) | agent picks current fal Seedream/nano-banana endpoint | `SHOWME_IMAGE_COMPOSE_MODEL` |
| Interpolation (E) | `bytedance/seedance-2.0/image-to-video` | `SHOWME_VIDEO_SEEDANCE_TIER`, `SHOWME_VIDEO_SEED` |
| Verification (D4, E) | `fal-ai/any-llm/vision` + `qwen/qwen3-vl-235b-a22b-instruct` | `SHOWME_VIDEO_VLM_MODEL` |
| Renderer policy | `auto` (grounded, refuses unregistered) | `SHOWME_VIDEO_RENDERER` |

## Rigid-body route status

| Route | Status | Serving decision |
|---|---|---|
| Deterministic twin connection scene | **POC8 runs 1–3: FAIL at Gate 1.** Bose twin PASSES. Owner-approved Tripo re-scan (high-quality consistent official inputs) recovered Mac geometry and proportions but invented mirrored port slots and no 3.5 mm jack — scan-based twins lack port-level detail. Recommended next: parametric evidence-modeled Mac (Stage B-alt), dims from claims, jack per `claim_mba_part_headphone_jack` + `src_img_store_closed_side_ports`, photo-projected surfaces. | Disabled; no artifact registered ($0.69 of $10 spent) |

Credentials: `~/.config/showme/fal.env` exports `FAL_API_KEY`; map to
`FAL_KEY` before importing `fal_client` (already handled in app code — keep
the pattern).

## Costs (per procedure, generated once)

Composition images + VLM checks: cents. Segments: ~$1–1.2 per 4s quality
segment → a 2-segment procedure ≈ $2–2.5. Failed verification wastes that
segment's spend; the single-retry cap bounds it.

## Worked example the build must pass: Bose `connect_aux_cable`

Inputs already in the vault/pack: `images/black-earcup-controls-wired-35mm.png`
(earcup + attached cable — covers s1), owner's-guide PDF (step figures,
pages bound to `claim_bqcu2_step_aux_1/2`), claims quoting "2.5 mm port on
the left earcup" and "3.5 mm port on your source device". Needed: a MacBook
Air side-view image in the vault (capture as a proper source with hash +
origin URL first — it is evidence). Then: s0 and s2 synthesized via D3,
gated via D4, segments s0→s1→s2 via E, stitched and registered via F.
Acceptance: the original question — "Show me a video of how to connect Bose
QuietComfort Ultra headphones to a MacBook Air using the audio cable." —
returns text+steps immediately, placeholder, then a verified motion video;
`fold_stroller` (curated keyframes) still works unchanged; an unregistered
procedure still gets no placeholder.

## Build order for the implementing agent

1. **C helper** `evidence_images(...)` incl. manual-page figure rendering.
   Tests: resolves bound images and page figures for the Bose aux claims.
2. **Registry v2**: states + segments-by-state (keep literal-path segments
   working). Tests: Graco fold registry still validates and generates.
3. **D3+D4 keyframe synthesis module** (compose → verify → retry once →
   register file + provenance). Tests: stubbed fal client — pass path,
   fail-retry path, fail-refuse path; verdict parsing reused.
4. **D1 state-graph drafting** (LLM-drafted, written to registry, validated:
   every segment's states exist, every state's claims exist).
5. **E extension**: state-ref resolution in `make_generator`.
6. **`can_generate`**: true only when every state of the procedure is
   resolvable (curated file, retrieved evidence, or passing synthesis spec).
7. **Storyboard serving** (optional, after video path works).
8. **Live acceptance run**: Bose aux end-to-end on the real pack; record
   spend and verdicts in the pack; owner reviews in-app.

Out of scope: self-hosted video models (Open-Sora/CogVideoX — violates
local-first, no-GPU-rental constraint; keep engines as pay-per-use APIs),
Kling adapter (until A/B justified), retry policies beyond the single
recompose, automatic approval of anything.
