# Stage S report — skinned Ready2Jet fold

**Status:** complete, internal-only.

**Rights:** Tripo3D license check OPEN — do not ship.

**Approval:** none (`approved_by: null`).
**Provider spend:** $0 (reused the hash-pinned `tripo-probe-01` scan).

## What exists

- `ready2jet-skinned.blend`: the photo-derived Tripo shell aligned to the rig rest envelope and bound to `Ready2Jet_SkinArmature_INTERNAL_ONLY`.
- `renders/skinned-fold-official-angle.gif`: 1024 × 1024 official-angle fold, visibly stamped internal-only.
- `renders/skinned-fold-novel-rear-right.gif`: 1024 × 1024 fixed rear-right diagnostic fold, visibly stamped internal-only.
- `verification/skinned-fold-pose-contact-sheet.png`: the same five poses used in Stage D, official video left and skinned rig right.
- Reproducible build, motion validation, deformation measurement, render, GIF encoding, and contact-sheet scripts.

## Motion authority and validation

No object-rig motion was changed.  The armature's 16 bones copy the evaluated world transforms of the existing evidence-mapped objects; `RigRoot` still owns `Ready2Jet_Fold_Correct` and all three defect parameters.  `validate_skin_motion.py` checked 96 frames for the correct action and for each defect scenario.

| Check | Result |
|---|---:|
| Maximum armature/object joint-angle trace error | **0.0 rad** (required ≤ 1e-4 rad) |
| Maximum relative translation error | **0.0 m** |
| Maximum relative scale error | **0.0** |
| Maximum latch-state error | **0.0** |
| Unweighted scan vertices | **0 / 59,099** |
| Maximum normalized-weight error | **2.98e-8** |

The full traces are in `motion-traces-stage-s.json`; the validator result is `validation-stage-s.json`.

## Alignment and binding

The scan's baked lean and axes were retained.  Its Tripo auto-sized AABB was fit to the existing rig rest envelope with a disclosed, axis-preserving scale of **[0.797774, 0.796847, 1.116506]** and translation **[0.004814, -0.005993, 0.551328] m**.  This is alignment, not a hidden geometry repair.

Weights begin with the nearest evidence-mapped proxy surface.  Only three declared hinge bands may blend, and only inside 3 cm; 696 vertices (1.18%) received blended weights.  Wheels and handle surfaces are rigid.  The provider reconstruction collapses the far-side wheels and cup-side surface inward, away from the documented rig pivots.  Those surfaces therefore use disclosed rigid parent masks rather than being pulled toward invented corrected geometry.  The detailed counts and masks are in `skinning-report.json`.

## Honest deformation result

The open pose looks like the photographed Kingston product.  Once the fused 97.2%-single-shell scan articulates, connected triangles bridge parts that the evidence rig moves independently.  The result is recognizably the stroller folding with the verified motion, but it is **not a clean photoreal fold**: tearing/stretching becomes obvious during the automatic-fold interval and in the final pose.

Every one of the scan's 158,045 edges was measured on all 96 frames.  A ratio over 1.6 is flagged as a visible artifact.

| Joint band | Edges | Worst ratio | Frame | Visible artifact |
|---|---:|---:|---:|:---:|
| Front frame / hub 112 | 726 | 29.648× | 84 | YES |
| Lower handle / hub 112 | 696 | 29.648× | 84 | YES |
| Upper handle / pivot 118 | 2,121 | 15.607× | 84 | YES |
| Seat follow | 5,911 | 71.874× | 84 | YES |
| Canopy fold | 1,888 | 11.978× | 82 | YES |
| Belly bar follow | 2,557 | 17.074× | 84 | YES |
| Cup-holder band | 0 | n/a | n/a | not scorable |
| Front caster, near side | 2,064 | 8.733× | 50 | YES |
| Front caster, far side | 0 | n/a | n/a | not scorable |
| Basket soft envelope | 21,613 | 25.783× | 84 | YES |

The whole-mesh worst edge reaches **192.556× at frame 84**.  This is dominated by very short provider-mesh edges crossing rigid part masks, but it is still a real visible defect and is not normalized away.  The two zero-edge bands mean the asymmetric provider reconstruction has no scan surface in the documented spatial band; they are not zero-stretch passes.  Full definitions and edge indices are in `stretch-qa-stage-s.json` and `stretch-qa-stage-s.md`.

## Viewer answer and POC 7

There is now a video in both requested cameras.  It combines a photo-realistic open scan with the proven mechanism motion, but the fused-shell topology prevents the articulated interval from being fully photorealistic.  The correct next step for that bar remains **POC 7 VACE skinning**: use these rig-verified renders as the person-free motion/control sequence and synthesize appearance per frame, then re-run fixed-camera, identity, part-persistence, and fold-pose checks.  POC 7 has not been run by this work order.

The Tripo3D commercial-license check remains the single blocker to any customer-facing use of the scan, these renders, or derivatives made from them.
