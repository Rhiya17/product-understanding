# Photo-texture projection report

**Date:** 2026-08-27

**Status:** STOPPED AT STAGE A COVERAGE GATE

**Distribution:** **INTERNAL ONLY — DO NOT SHIP**

**External spend:** **$0.00**

**Approval:** none (`approved_by: null`)

## Outcome

The projection experiment stopped before UV work or baking. The five binding key-part groups averaged **17.89%** scan coverage at the required maximum projection distance of 15 mm, far below the **60%** gate. Overall visible and hidden twin geometry coverage was **20.96%**. The recorded Stage-S transform produced an area-weighted twin-to-scan RMS surface distance of **117.8 mm** (mean **83.6 mm**).

Per §0.2, uncovered surfaces remain on their existing dress-pass materials. No texture pixels were fabricated. Per §0.6 and Stage A.3, Stages B–D were not run: no UV atlas, bake, textured blend, QA render, GIF/MP4, contact sheet, or derived-asset registration was created.

## Stage A — alignment and coverage

The deterministic audit reused the Stage-S transform exactly, without ICP refinement:

```text
[[0.7977742553, 0,            0,            0.0048138932],
 [0,            0.7968474030, 0,           -0.0059926119],
 [0,            0,            1.1165064573, 0.5513283014],
 [0,            0,            0,            1]]
```

Coverage is area weighted. Evaluated twin triangles were recursively subdivided to at most 7.5 mm longest edge; each leaf centroid was queried against a BVH of the aligned scan. A leaf is covered only if the nearest scan surface is no more than 15 mm away. Full per-object coverage, fallback fractions, distances, sample counts, transform, and input hashes are in `coverage.json`.

| Binding key group | Coverage | Fallback | Mean distance | RMS distance |
|---|---:|---:|---:|---:|
| Seat | 43.20% | 56.80% | 30.9 mm | 43.5 mm |
| Canopy | 0.00% | 100.00% | 202.9 mm | 220.2 mm |
| Frame tubes | 14.21% | 85.79% | 77.7 mm | 97.5 mm |
| Handle grip | 19.03% | 80.97% | 49.6 mm | 64.1 mm |
| Wheels | 13.01% | 86.99% | 110.8 mm | 136.0 mm |
| **Arithmetic key-group average** | **17.89%** | **82.11%** | — | — |

The failure is not a marginal threshold miss. The scan is a fused, asymmetric photographic reconstruction, while the twin uses evidence-mapped, mechanically correct rigid parts. In particular, canopy coverage is zero and the far-side frame/wheels are materially displaced. A global ICP refinement cannot reconcile those part-specific and topology-specific differences without altering geometry, which §0 forbids.

### Gate disposition

- Required key-group average: at least 60%.
- Measured: 17.89%.
- Result: **FAIL — stop before Stage B**.
- Honest fallback: retain all existing dress-pass materials outside the recorded covered regions; because no bake was made, the retained scene remains wholly on the existing dress pass.

## Stages B–D — not run

| Stage | Disposition | Reason |
|---|---|---|
| B — UV and bake | **SKIPPED** | Stage A binding gate failed; investing in baking would violate the stop rule. |
| C — identity and quality QA | **SKIPPED** | No textured twin exists to test. |
| D — deliverables/registration | **SKIPPED** | Stage C could not pass; no output qualifies as `TWIN_RENDER_PHOTO_TEXTURE`. |

`evidence-packs/graco-ready2jet-2212125/derived-assets.json` remains absent and approval fields remain untouched. No distributed media was created, so there was nothing new to watermark.

## Stage E — license review

Stage E ran despite the Stage A stop. The official-source review is [Tripo3D / fal.ai commercial-license review](../../../docs/pocs/tripo3d-license-review.md). It recommends conditional commercial approval for **derived renders only** after the owner documents the paid fal entitlement and source-photo/product-IP rights. The owner has not yet recorded a decision, so this scan and all descendants remain internal-only.

## Hours and spend

Durations are wall-clock active-stage measurements for this execution; the audit also records its exact Blender runtime.

| Stage | Hours | Outcome |
|---|---:|---|
| A — alignment/coverage | 0.026 | Gate failed; deterministic audit completed. |
| B — UV/bake | 0.000 | Skipped by Stage A gate. |
| C — QA | 0.000 | Skipped by Stage A gate. |
| D — deliverables | 0.000 | Skipped by Stage A gate. |
| E — license review | 0.054 | Official-source review completed; owner decision open. |
| **Total active-stage time** | **0.079** | Exact timestamps and seconds are in `hours.json`. |
| External provider spend | **$0.00** | No external generation or paid API call. |

## Protected-input guarantee

The audit refuses to run unless these hashes match:

- `ready2jet-rigged.blend`: `83d80dc107d46edecbe89d4d97dabf726887012dd4c0917f8da8e2961a9dc79d`
- scan GLB: `95e0fe44bba9a303b31849cfbec1d7d517d2ed2c6361ab505e025cf7ef80716b`
- `action-spec.json`: `42d43c0cab6d4f320a1c473c534020d1e91176ba2f6d9eec8e8ff5b944b5d3c2`
- `joint-evidence.json`: `e2a1ad9ddb091f00a59aba553287b844427ef8e84e846d8dc09ab9a98fc8f361`

Post-run validation rechecks the same protected hashes. The pre-existing untracked `twin/renders/frames-scan-turntable/` directory is unrelated user work and was preserved unchanged.
