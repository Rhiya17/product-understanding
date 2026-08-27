# POC 6 report — articulated Ready2Jet twin

**Status:** COMPLETE FOR INTERNAL RESEARCH. **INTERNAL ONLY — DO NOT SHIP.**

The result is a deterministic evidence-mapped mechanism study, not a product-accurate hero asset. It performs the documented preparation and control sequence, converges the front/rear wheel centers, reaches an upright compact pose, and can expose the fold from a rear-right view absent from the official video. It also makes the remaining fidelity gap measurable instead of hiding it.

## Outputs

- `ready2jet-rigged.blend` — saved Blender 5.2.0 LTS scene, hidden Tripo scaffold, internal-only/license metadata.
- `joint-evidence.json` — 13 mapped joints, soft-envelope motions, support motion, and latch state; every entry cites evidence and every absent detail is `INFERRED`.
- `action-spec.json` — ordered 0..1 stage controls and three render-time defect parameters.
- `renders/open-turntable.gif` — 72-frame 24 fps Blender source sequence, 25-frame 1024 px GIF.
- `renders/fold-official-angle.gif` — 96-frame source sequence, 33-frame 1024 px GIF from the approximate official angle.
- `renders/fold-novel-rear-right.gif` — 96-frame source sequence, 33-frame 1024 px GIF from the new rear-right angle.
- `verification/fold-pose-contact-sheet.png` — five matched official/rendered pose pairs.
- `verification/dimension-check.json` — open and folded D/W/H with signed errors.

GIF is an allowed work-order deliverable. It was selected because this Blender build exposes no FFmpeg output codec and no local system encoder is installed. The source animation still renders every frame at 1024 x 1024; committed `render_twin.py` and `encode_gifs.py` reproduce the result without a network call.

## Hours and spend

| Stage | Hours | Outcome |
|---|---:|---|
| A | 0.3 | Claims, patent candidates, video kinematics, and folded-size estimate assembled. |
| B | 0.2 | B1/B2 handle spike and full clean geometry rebuild. |
| C | 0.3 | Evidence map, parameter rig, correct action, and defect parameters. |
| D | 3.0 | Rendering, visual reframing, contact sheet, measurements, report, validators. |
| **Total** | **3.8** | **$0 external spend.** |

Timing is agent wall-clock time rounded to 0.1 hour. Stage D includes the rejected cropped camera passes and their full rerenders; that cost is part of the honest measurement.

## Stage B spike verdict

Rebuild won. The Tripo handle surgery selected 15,982 faces but produced 40 components, 2,208 boundary edges before fill, and 964 remaining non-manifold edges after cleanup. The parametric rebuild produced ten separate manifold parts with zero aggregate boundary edges and explicit pivot/control objects. The source Tripo mesh remains hidden as an internal-only dimensional scaffold with run id, pack hash, and GLB hash recorded in the `.blend`.

## Fold action and evidence

The action order is fixed:

1. prepare: fold canopy, rotate cup holder, align casters;
2. slide thumb switch;
3. squeeze handle lever;
4. automatic frame/handle/seat fold;
5. secure-latch check.

The principal frame and split-handle directions follow US20220169297A1 figures 3–11F and official-video frames 1166–1193. Manual STEP claims provide the user-visible order. The patent is a high visual/functional mechanism match, but it does not explicitly identify the Ready2Jet model, so it is not treated as proof of exact production tolerances.

The correct action is `Ready2Jet_Fold_Correct`. Render-time defects are `defect_reverse_direction`, `defect_skip_handle_release`, and `defect_skip_latch`; the last drives `effective_latch_state` to zero while allowing the motion to complete.

## Pose comparison

The contact sheet supports three conclusions:

- **Matched:** fold direction, front/rear wheel convergence, upright final state, and a visibly ordered release-before-fold sequence.
- **Approximate:** the real seat, basket, and canopy deform through linked fabric structures; the twin uses explicit `INFERRED` rigid/soft-envelope proxies. The real U-handle settles above the dense folded body; the twin's simplified split handle stays farther rearward.
- **Divergent:** the real final body is materially denser in depth and width. The twin is appropriate for kinematic diagnostics and deliberately wrong-fold generation, not fit guarantees or a hero render.

The novel rear-right view earns its keep by revealing the paired wheel convergence, basket compression proxy, and the minimally modeled rear surfaces that the official fixed camera occludes. It also makes those inferred surfaces visibly auditable.

## Dimension check

| State | Target D/W/H (m) | Measured D/W/H (m) | Error D/W/H |
|---|---|---|---|
| Open (`OFFICIAL`) | 0.6858 / 0.5207 / 1.0922 | 0.6902 / 0.5340 / 1.0935 | +0.6% / +2.6% / +0.1% |
| Folded (`INFERRED`) | 0.2921 / 0.5207 / 0.7620 | 0.4769 / 0.5909 / 0.8257 | +63.3% / +13.5% / +8.4% |

The folded depth miss is the largest open technical issue. The target itself is inferred from the official video and a manufacturer-authored retailer answer, but the error is too large to claim folded-fit accuracy even with that uncertainty. Further compaction would require better linkage/attachment evidence; it was not invented to force a passing number.

## `INFERRED` inventory

- seat-follow pivot, -22° range, and 0.15 m rearward/downward translation;
- canopy linkage, 35° range, and soft-envelope collapse scale;
- basket soft-envelope collapse scale;
- cup-holder pivot and travel;
- front-caster exact travel and right-side symmetry;
- thumb-switch and squeeze-lever exact travel/translation model;
- 75 mm operator-supported whole-stroller lift arc during the fold;
- rear/unseen surfaces;
- hidden cable, spring, slider, and latch surface geometry.

## Open risks and next evidence

- No physical stroller/rear capture exists by owner decision; rear structure stays minimal and `INFERRED`.
- The folded dimensions are not published by Graco in the manual/PDP and remain `INFERRED`.
- The matched patent does not name the Ready2Jet; exact internal production geometry is unverified.
- The Tripo3D commercial-license question remains OPEN. Nothing from this twin may ship.
- The fold-video rights note limits the source evidence to internal research; these renders inherit the internal-only restriction.
- The optional Qwen advisory verifier was not run: it is unbenchmarked and unnecessary for the required local checks.

No stop-and-report condition fired: evidence did not contradict the direction-level rig, stage outcomes were reached, and external spend remained zero.
