# Ready2Jet fold kinematics - Stage A evidence study

**Source:** official Graco fold video `src_r2j_fold_video_v1`, SHA-256
`9b1af25362a0b78187c6a4ced7228abcbbf5886e3617356277958392233af0fa`,
29.97002997 fps, 1920x1080.  The selected lossless frames and their hashes are
in `fold-study-frames/index.json`; regenerate with `extract_fold_study.py`.

People are present in these frames because they are evidence-study material,
not generative-model input.  They remain internal-only under the vault rights
note.

## Ordered procedure ground truth

All claims below are `CANDIDATE`, not owner-published.  Their manual wording is
still the required sequence for this internal POC.

| Order | Claim | Action | Manual evidence | Animation treatment |
|---:|---|---|---|---|
| 1 | `claim_r2j_step_fold_1` | Remove infant car seat if in use. | p.33 | Precondition; no car seat exists in twin |
| 2 | `claim_r2j_step_fold_2` | Unlock brakes. | p.33 | Precondition/state annotation; brake pedal is not animated |
| 3 | `claim_r2j_step_fold_3` | Fold the canopy. | p.33 | Stage parameter `canopy_fold` |
| 4 | `claim_r2j_step_fold_4` | Slide thumb switch. | p.34 | Stage parameter `thumb_switch` |
| 5 | `claim_r2j_step_fold_5` | Squeeze handle lever. | p.34 | Stage parameter `handle_lever`; releases automatic fold |
| 6 | `claim_r2j_step_fold_6` | Check that the stroller is secure. | p.35 | Final latch state / hold frame |
| 7 | `claim_r2j_step_fold_7` | Carry by belly bar. | p.35 | Belly bar remains fixed and exposed; carrying is out of animation scope |

Optional preparation claims: `claim_r2j_step_fold_tips_1` rotates the cup
holder for a more compact fold; `claim_r2j_step_fold_tips_2` pulls the stroller
to rotate the front wheels.  The default action includes both preparation
states before release.

## Observable timeline

| Frame | Time | Observation | Evidence strength |
|---:|---:|---|---|
| 488 | 16.283 s | Presenter pushes the canopy rearward; no frame member moves. | DOCUMENTED video + fold step 3 |
| 611 | 20.387 s | Canopy is collapsed against the handle before mechanism release. | DOCUMENTED video |
| 731 | 24.391 s | Front caster is pulled/rolled into the manual's compact-fold orientation. | DOCUMENTED video + optional tip 2 |
| 1127 | 37.604 s | Close-up establishes thumb switch on top and squeeze lever below the center handle. | DOCUMENTED video; actuation travel is partially occluded by hand |
| 1153 | 38.472 s | Hand holds the two controls at the end of the close-up. | DOCUMENTED video; exact internal latch travel is not visible |
| 1166 | 38.906 s | Cut to wide shot; stroller remains fully open immediately before automatic motion. | DOCUMENTED video |
| 1173 | 39.139 s | First visible motion: upper handle/seat-back region begins moving forward and down. | DOCUMENTED video |
| 1180 | 39.373 s | Handle has folded about its mid pivot; front-leg and handle members rotate toward the rear-leg reference around the side hub. Seat/backrest follows the collapsing frame. | DOCUMENTED video + US20220169297A1 Figs. 3-11C |
| 1186 | 39.573 s | Wheelbase rapidly collapses; front wheel assembly travels rearward while the handle/seat package continues down. | DOCUMENTED video + patent Figs. 11C-11D |
| 1193 | 39.806 s | First upright folded pose: front/rear wheels cluster, belly bar remains high and usable as carry handle. | DOCUMENTED video + patent Figs. 11E-11F |
| 1206 | 40.240 s | Folded pose is settled and self-standing without the presenter's hand. | DOCUMENTED video + manual p.35 |

## Kinematic interpretation used by the rig

1. The rear-leg assembly is the visual reference member.  Left/right side hubs
   connect the front legs, lower handle, and rear legs.
2. The upper handle folds forward/down relative to the lower handle about the
   patent's pivot 118.  That motion releases the hub linkage.
3. The front-leg assembly and lower handle rotate toward the rear-leg assembly
   about the side-hub axis.  The patent documents the internal synchronized
   linkage; the video documents the external result.
4. The seat/backrest follows the upper frame through a separate side pivot.
   Its exact linkage is not exposed in any source, so its axis/range is
   `INFERRED` from frames 1166-1193.
5. Front casters swivel for compact packing but wheel axles do not drive the
   fold.  Wheel spin/swivel beyond the documented preparation pose is
   `INFERRED` and kept minimal.
6. No lateral narrowing is observed.  Rear/unseen surfaces and the exact left/
   right linkage symmetry are `INFERRED`; the twin uses mirrored external
   members only.

## Folded dimensions

Neither the official manual nor the Graco PDP publishes folded W x D x H.
Stage A therefore records **INFERRED** dimensions of **52.07 x 29.21 x 76.20
cm (20.5 x 11.5 x 30.0 in), W x D x H**:

- Width is retained from the official open width because the patent and video
  show a planar fold with no lateral-width mechanism.
- Height/depth are estimated from the final official-video pose relative to the
  known open envelope and checked against the manual's folded drawing.
- A manufacturer-authored answer hosted on Target independently reports
  `20.5 W x 11.5 D x 30 H`; this is corroboration, not promoted to an official
  PDP specification.

The dimension check must display the `INFERRED` label and should use a looser
10% diagnostic band.  It is not a product-spec acceptance gate.

## Evidence gaps / INFERRED inventory after Stage A

- Seat/backrest-to-frame linkage axis and nonlinear relationship.
- Canopy linkage details; only the visible collapsed/open states are known.
- Exact actuation travel and internal routing for thumb switch, squeeze lever,
  cables, hub latch, slider, and spring.
- Left/right internal linkage symmetry and all rear-facing surface geometry.
- Wheel swivel angles between sampled frames and any passive caster dynamics.
- Folded dimensions, as described above.
