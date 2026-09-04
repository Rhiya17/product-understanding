# Work order: grounded procedure-video pipeline (keyframe-pinned, verified)

*Written 2026-08-28. Owner decision: direct text/image-to-video calls (wan 3.0
via fal) are rejected for serving — the output is unverifiable and anyone can
call fal directly, so it adds no product value. This work order replaces the
generation backend behind the existing async video job with our own pipeline.*

## Why (what we already know)

- Higgsfield POC: text + one photo → 0/3 usable folds, product morphed every
  run. Video models score ~29/100 on physical mechanism understanding
  ([video-generation-alternatives](../pocs/video-generation-alternatives.md)).
- Seedance keyframe POC: pinning **both endpoints of each segment** with
  verified photos, then stitching segments, preserved product identity and
  reached the documented end state (chain-01; Qwen VLM check1 passed identity
  and end state, flagged camera rotation — exactly the drift class the
  verifier exists to catch).
- Conclusion: generative models are allowed to do **motion in-betweening
  between pinned truths only**. Identity, states, and ordering come from our
  evidence (official photos, manual figures, twin renders).

## Outcomes

1. A question that resolves to a procedure with **registered keyframes** gets
   the async flow: instant text+image answer, "Video generating…" placeholder,
   then a stitched, per-segment-verified video registered as pending media.
2. A procedure **without** registered keyframes gets no placeholder and no
   video — the honest text+image answer stands. No ungrounded generation.
3. Every served video carries provenance: model, request ids, seed, keyframe
   sources, and the VLM verification verdicts, all pending owner review.

## Design

### Keyframe registry (per product, curated upfront)

`evidence-packs/<product>/procedure-keyframes.json`:

```json
{
  "schema_version": 1,
  "procedures": [{
    "procedure": "fold_stroller",
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "keyframe_provenance": "where the keyframes come from",
    "segments": [{
      "segment_id": "seg1",
      "start_path": "<repo-relative image>",
      "end_path": "<repo-relative image>",
      "motion_prompt": "<full curated Seedance prompt>",
      "duration_seconds": 4
    }]
  }]
}
```

Keyframes are evidence: official photos, manual step figures, or gated twin
renders. Curating this file is part of product ingestion ("twin upfront").
Registry paths are repo-root-relative so they can point at vault files, POC
references, or `generated-assets/` twin renders.

### Pipeline (app/keyframe_video.py, runs inside the existing job manager)

Per segment: upload start/end keyframes → Seedance 2.0 first/last-frame
(`bytedance/seedance-2.0/image-to-video`, quality tier; `fast` via
`SHOWME_VIDEO_SEEDANCE_TIER`) → download → sample frames → Qwen VLM
verification (`fal-ai/any-llm/vision`, `qwen/qwen3-vl-235b-a22b-instruct`):
same product vs keyframes, reaches end state, no invented parts, fixed camera
→ JSON verdict. **Any segment failing verification fails the whole job** —
nothing is registered or served. Passing segments are stitched (OpenCV),
poster = first keyframe, verification verdicts written beside the video and
referenced from the asset record.

### Renderer selection (SHOWME_VIDEO_RENDERER)

- `auto` (default) = `keyframe`: grounded pipeline; refuses procedures with no
  registry entry (server attaches no video job at all).
- `fal`: direct wan image/text-to-video — experimental only, kept for A/B.
- `deterministic`: local typographic slides — offline/dev fallback.

### Engines

Seedance 2.0 is the default interpolation engine (validated by POC; accepts
start+end frames + reference images). Kling v3 start/end-frame mode is a
candidate second engine behind the same segment interface — needs an input
adapter; do not add until a quality/cost comparison on one registered
procedure justifies it.

## Costs

Seedance quality ≈ $0.24–0.30/s → ~$1–1.2 per 4s segment; fold = 2 segments
≈ $2–2.5 per generated procedure video, generated once and cached in the
pack. VLM checks are cents. Failed verification wastes the segment spend —
acceptable at MVP volume; revisit if retry loops appear.

## Rollout

1. Registry + pipeline + refusal default (this change).
2. First registered procedure: Graco Ready2Jet `fold_stroller`, reusing the
   POC's canvas keyframes and validated segment prompts.
3. Next: curate keyframes for Bose `connect_aux_cable` (needs an end-state
   image: cable seated in 2.5 mm port — official gallery or twin render) and
   MacBook procedures.

## Open questions

- Retry policy on verification failure (different seed? different engine?).
- Whether check2 (mechanism-vs-manual) should also gate serving, or only
  check1-style identity/end-state gating (current choice: identity gate only,
  mechanism review left to the human owner pass).
