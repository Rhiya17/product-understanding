# Ready2Jet realism pass — run-02

**Outcome: partial realism improvement.** The controlled comparisons show a distinct canopy visor, visible seat construction and a more legible suspended basket. The canopy crown remains too angular, upholstery is not as full or irregular as the photograph, and rear/folded cloth still looks constructed from simple surfaces. These unresolved appearance problems prevent a successful photographic-realism outcome. The editable model, complete action, reproduction code and diagnostic evidence are retained.

**Kingston-reference reconstruction; exact SKU applicability unresolved.** Manufacturer-source restrictions remain internal research. No manufacturer photograph became a material texture. No external generative provider, purchased asset, cloud renderer, physical dynamics solver or application integration was used.

## Baseline and three bounded rounds

The final delivered run-01 scene was copied without changes. Its current revision-3 scripts were separately rebuilt into run-02. Identical 640-square / 16-sample renders at frames 1, 95 and 145 had **zero pixel differences**, including the corrected final seat timing. This establishes the saved baseline/current implementation agreement; the older revision-3 scene was not substituted.

| Round | Change and inspected evidence | Decision |
|---|---|---|
| 1 | Four-section canopy profile with shallow visor; attached interior liner replaces unsupported rear flap. Seat/back pillow shape; revised three-lobe wheel inset. Open, prepared, middle, late, folded and rear views. | Keep canopy/lining improvement. Fix basket binding anchors and Solidify direction; old offset hid the new seat seams. |
| 2 | Corrected seat/back/canopy thickness orientation; shared basket anchors, additional rear wall, visible seat divisions/edge binding. Rest-metric UVs and procedural yarn/mesh material. | Keep. Shoulder pads remained rectangular and net repeat averaged away at small scale. |
| 3 | Rounded shoulder-pad outlines, bounded folded back compression, slightly coarser/lower-coverage net pattern. Added simple inferred housing cheeks so the squeeze lever is visibly connected. Final photo camera estimate and complete denser rear checks. | Deliver this checkpoint as partial. Stop at three modeling rounds; preserve all checkpoints. |

Camera corrections were assessed separately. The studio photograph and original video diagnostic face different lateral sides. `Camera_Photo` supplies an approximate perspective studio fit, while the original orthographic cameras remain available. Both baseline and candidate were rerendered with the final comparison camera and identical illumination. `records/camera-fit.md` identifies wheel centers, hub and handle landmarks, display crops and remaining ambiguity. The camera is not calibrated; the source cup visibility, handle lean and wheel layout do not align exactly.

## What improved and what remains wrong

**Shape and construction.** The canopy has separate bow/visor boundaries instead of one continuous helmet shape, and the rear liner no longer protrudes as a detached-looking flap. Seat thickness, two transverse compressed divisions, edge binding and rounded shoulder pads add readable construction. The basket now has suspended walls, sag, opaque binding and mesh, with common attachment coordinates throughout folding. Wheel accents use one inset following a three-lobe contour rather than separate silver loops.

The crown is still too tent-like and lacks the source's rounded front bow and fuller rear panel. The seat/back remain long and smooth; side wings, harness and underside do not reproduce the source's sewn, compressed layers. Wheel tread, trim, caster forms, belly-bar profile and tan grip are still stylized. Close-up grip grain is weak; grip ends and tube transitions remain visibly simplified. Folded cloth layers and rear structure are especially uncertain. Close-ups also reveal a slightly lifted seat-edge piping line and overly tubular waist webbing with crude end transitions. These are retained, explicitly qualified defects of the partial result. Fine clearances and cloth/frame contact are not validated. These are material limitations of the delivered result, not independent validation findings.

**Materials.** A rest-metric UV system drives crossed procedural yarns, mild heather variation and restrained bump; the pattern stays assigned to corresponding vertices through shape keys. Basket mesh holes are visible in the close-up, with opaque edge fabric. Cloth, rubber, molded plastic, frame and grip use different roughness responses. Numeric properties and weave dimensions are **INFERRED**. Fine weave is not fully resolved at full-product display scale; basket net can alias or average into a translucent face. No physical fiber species, alloy/coating or strain-preserving cloth behavior is established.

**Photography.** A perspective comparison camera corrects the gross studio-view handedness and framing. Separate 1600-pixel product stills use broader, brighter lighting and keep the product in focus. These beauty settings are excluded from controlled geometry/material comparisons. The background, gray value and source shadow pattern remain approximate.

## Practical checks

**Geometry and materials:** neutral before/after renders compare open/middle/folded geometry with one camera and material override. Rear/intermediate images expose rather than hide the rear construction. Neutral close-ups cover canopy, upholstery, basket and grip; a folded material view is retained. Shape-key vertex counts/correspondence, UV layer names and modifier order are recorded in `scene-inventory.json`. The same named soft surfaces remain present in every pose; there are no silhouette swaps.

**Motion:** release-before-collapse and the final seat timing are unchanged. All rigid joint event values and the source/presentation mapping remain inherited. The same coordinate functions place fabric and its hems; no cloth simulation or caches are used. Sampled rig scales remain unchanged. Preparation, thumb slide, squeeze, early/middle/late collapse and final hold were inspected from main and rear directions, including frames between authored keys. Controlled deformation is stable in the inspected samples, but gathered fabric is too regular and physical contact/balance remain approximate.

Visual review is **sampled-frame inspection only**, including frames from the final encoded streams. The available tools expose still frames; successful whole-stream decoding is not normal-speed visual playback review. No claim of full playback review or independently established absence of flicker is made.

**Reproduction:** the final scene was reopened in a fresh process, and the authoring command was exercised into a separate `verification/` directory. Open, middle and folded images are pixel-identical to the delivered-scene reproductions; the material close-up is also checked. No external texture images or simulation caches are needed. All replacement soft meshes regenerate Basis, all shape keys and UVs; they remain unparented world-space meshes to avoid applying rig motion twice.

**Envelope:** world-space evaluated product vertices, excluding studio objects, yield:

| Pose | Run-01 D × W × H, cm | Run-02 D × W × H, cm |
|---|---|---|
| Open, frame 1 | 68.85 × 53.20 × 110.30 | 68.85 × 53.20 × 110.30 |
| Middle, frame 95 | 71.35 × 53.20 × 79.60 | 71.35 × 53.20 × 79.60 |
| Folded, frame 145 | 31.26 × 53.20 × 77.16 | 31.26 × 53.20 × 77.16 |

Added/revised fabric stays inside the existing rigid extremal envelope; no constraint forced the old measurements. Folded reference 29.21 × 52.07 × 76.20 cm remains **INFERRED**. Envelope agreement cannot establish luggage fit, stability or mechanical accuracy. Rear wheels retain inherited near-floor support; other clearances and front-wheel contact remain illustrative.

**Procedure:** starts empty with brakes assumed unlocked. Canopy preparation and illustrative cup rotation remain; casters start aligned rather than simulating the wheel-alignment tip. Thumb switch precedes squeeze lever. The qualified manual panel is reused; secure-state checking and carrying are communicated, not physically executed. No latch click, hidden linkage, force or operator is invented.

## Render cost, preservation and accounting

Runtime: Blender/bpy 5.0.1, Python 3.11.4, macOS arm64, Cycles CPU; FFmpeg 8.0.1 / libx264; Pillow 12.3.0. The available bpy process crashes inside the sandbox and was run with normal permission escalation. The user's open Blender session was untouched.

Benchmarks used actual final geometry/materials at native 1280×720. Main frames 1/95/145 took 4.47/3.72/2.56 s; rear took 2.66/2.42/2.33 s. Main benchmark overlapped comparison rendering. Their estimates were 692 and 478 seconds respectively, before concurrent contention. Full animation timing, still/preview render sums and measured wall time are recorded in `records/run-accounting.json`; overlap is reported rather than added to elapsed time. The measured window starts when run-02 preservation began; initial prompt/context reading preceded it. Model token usage and session cost are **UNKNOWN**.

Selected baseline/source hashes are rechecked at completion. `records/preservation-end.json` records their results and the outside-run modification scan. That scan covers file modification metadata, not a full-repository hash audit; baseline scene/scripts and selected sources receive actual hash checks. All new project artifacts are under run-02, with earlier runs and sources preserved. No claim of causal superiority of a model follows from this single assisted experiment.

## Final measured completion

Measured preservation-to-delivery window: **29.2 minutes**. Main frame rendering: **974.3 s**; rear: **936.9 s**. Their process intervals span **16.3 wall minutes**, with **15.6 minutes overlapping**. Saved preview/still/animation frame timing totals **37.7 process-minutes**, not added to elapsed wall time. Superseded camera-preview timings are excluded. Usage/cost: **UNKNOWN**.

All **33 selected baseline/source hash checks are unchanged**. The outside-run metadata scan found **0 files** modified during the measured window; see the preservation record for scope/details. Both MP4 streams pass full decoding; visual review remains sampled frames only.
