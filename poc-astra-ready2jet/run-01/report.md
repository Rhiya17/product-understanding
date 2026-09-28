# Ready2Jet reconstruction and fold study

**Outcome: partial illustrative result.** Folded compactness and handle placement improve over the archived twin. The editable scene, construction/rig/render scripts, source comparisons, full diagnostic clips and fresh-process reproduction are delivered. Shape and motion reference fit remain incomplete; this is not a validated product model or manufacturing CAD.

**Kingston-reference reconstruction; exact SKU applicability unresolved.** The input pack identifies gray/tan Kingston as 2209064; the source vault and candidate claims identify 2212125. The original Ready2Jet-family manual has the expected fold sequence on printed/PDF pages 33–35, but this run does not establish exact Kingston SKU/revision applicability.

## Evidence and provenance

The 21 selected archived files with recorded hashes all matched. Three manual page rasters were additionally hashed. Five archived video stages were independently decoded from the original 1920×1080, 30000/1001 fps video. Frame geometry and zero-based timestamps agree; the historical OpenCV PNGs and current FFmpeg decode differ by small RGB conversion amounts (maximum 7/255), documented in `records/frame-verification.json`. Comparisons use the freshly decoded original frames.

The extended-canopy studio photograph, prepared/collapsed-canopy video shot and folded photograph are treated as different states. The unresolved top-view variant is excluded from binding geometry. The edited side image informs only its visibly supported frame/wheel regions; its original marketing sequence was inspected. No title-card duplicate is counted as independent evidence. The local-only held-out close-up was not used or uploaded. The FastAction/seat-strap directory was excluded. The prior patent note informed only a possible topology; no patent hidden internals are asserted to be the production mechanism.

All manufacturer restrictions remain **internal research; generate_from NOT cleared**. No source or asset was submitted to a generative-image/video provider. The model is newly authored curves and meshes, with no old scaffold, Tripo or Meshy import.

## Three bounded revision rounds

| Stage | Correction and evidence | Remaining issue |
|---|---|---|
| Early milestone | Same coarse assembly saved and rendered open/middle/folded before detailed work. Split handle and converging wheels established. | Flat seat, thin canopy, sparse body; initial curve bounding-box measurement was invalid and replaced by evaluated geometry extents. |
| Round 1 | Added a shaped calf/seat surface, upholstery/harness, canopy seams, hollow cup holder, rim details and mesh basket. Lowered middle-stage handle toward video 1180. | Folded handle still protruded rearward; measured depth 37.9 cm. |
| Round 2 | Added side wings and canopy lining, refined wheel trim, darkened materials. Compared fixed-camera source/render poses. | Rear lining looked over-corrugated; seat rotation occurred too early. |
| Round 3 + final review | Rotated folded upper handle toward the observed near-vertical orientation, lowered carry-bar height, delayed seat rotation to the middle/late source stages, softened rear lining and folded basket floor. | Canopy/padding and rear fabric still look simplified; stop at this qualified result instead of further open-ended refinement. |

The final scene contains four wheel/caster assemblies, front/rear frame members, separate lower/upper handle assemblies, main and split hubs, controls, seat/back/harness, foot U-support, canopy, basket, belly bar and cup holder. No rigid member shrinks, swaps or disappears to force compactness. Only named fabric envelopes deform. No lateral narrowing is introduced.

## Practical check A: reference comparison

The final three-stage and five-stage sheets use one unchanged Blender camera and one unchanged source crop throughout the continuous wide shot. The open appearance comparison uses the extended-canopy studio image separately. These are **reference-fit checks used during modeling**, not unseen or independent validation. Camera pose is approximate and no pixel-accuracy score is claimed.

Improved: tan split handle; rounded front U-frame; three-spoke wheel motif; separate moving assemblies; upper handle folded into the body; exposed carry arch; closer overall folded envelope. The previous twin's high, rearward handle and deep folded body are visibly reduced.

Still different: the canopy dome/visor shape and gathered canopy volume; the long, smooth seat/back surfaces and shallow padding; the fine mesh/basket profile; wheel molding and spokes; hub housings. The folded body remains less densely layered than the photograph. The rear fabric and its attachment topology are especially weak. Intermediate handle/seat trajectories follow the broad folding direction but do not achieve detailed source agreement. This fails a claim of faithful reconstruction even though the mechanical illustration is useful.

| State | Reference D × W × H (cm) | This run (cm) | Signed difference |
|---|---|---|---|
| Open | 68.58 × 52.07 × 109.22, recorded manufacturer specification | 68.85 × 53.20 × 110.30 | +0.4% / +2.2% / +1.0% |
| Folded | 29.21 × 52.07 × 76.20, **INFERRED** | 31.26 × 53.20 × 77.16 | +7.0% / +2.2% / +1.3% |
| Archived twin, folded | Same inferred target | 47.69 × 59.09 × 82.57 | +63.3% / +13.5% / +8.4% |

Measurements use world-space evaluated product vertices, excluding studio objects, at open/prepared and settled folded poses. The baseline uses the archived XYZ=DWH envelope record and was not rerun. Axes and states are compatible, but its measurement implementation was not revalidated here. Folded depth is **16.43 cm smaller (34.5%)** than the archived result. The uncertain target and a matching envelope do not prove luggage fit, stability or production linkage accuracy. No arbitrary pass threshold was imposed.

## Practical check B: animation review and procedure

The continuous fold maps source frames 1166–1206 (38.906–40.240 s) to presentation frames about 73–137, at **2× slow motion**. Sampled integer frames round this mapping by at most about 0.01 source seconds. Preparation, controls and final hold use declared presentation timing. All landmarks in a pose share that mapping; cameras do not change by pose.

The complete main and rear streams are encoded and decoded for media integrity. Visual review here is **sampled-frame inspection, not a full normal-speed playback review**. Both cameras were inspected across preparation, release, early/middle/late collapse and the hold, with denser samples around collapse. Contact sheets support this limited review.

The rear-wheel axle anchors support; the frame rotates about it while front wheels converge. There is no arbitrary whole-stroller lift or copied old translation. This approximates the source's support situation; it does not simulate balance, operator contact, wheel friction or forces. Sampled views show no wholesale disappearance or rigid-member stretching. Small clearances, fabric/frame intersections and exact support contact are not validated. Rear fabric remains an obvious simplification, exposed by the diagnostic view.

The model starts empty with brakes assumed unlocked. Canopy gathering and an illustrative cup rotation cover preparation; casters start aligned rather than simulating the pull-to-orient tip. The thumb switch precedes lever squeeze, with explicitly inferred travel. A readable original-manual source panel supplies control direction/order. Secure-state checking and carrying by the belly bar appear as source-backed text; neither is physically simulated. No latch engagement, click, hidden spring, cable dynamics or force is invented.

## Practical check C: reproduction and preservation

The final `.blend` was opened by a fresh bpy process and reproduced frames 1, 73, 95 and 145. A separate smoke test built a mesh, saved, reopened and rendered it. Procedural materials need no external texture paths. Full clean PNG sequences and working commands accompany the MP4s. Media probe/decode results and final measurements are under `records/` and `final/reproduction/`.

All new project work stays under `poc-astra-ready2jet/run-01/`. Source hashes and prior-file modification checks are recorded at completion. No unrelated acceptance scripts, providers, purchases, cloud renders, publishing, application integration or approval-record edits were run. No custom scoring framework, collision validator or test suite was built.

## Time, review input and usage

Actual runtime: Blender 5.0.1, Python 3.11.4, macOS arm64, Cycles CPU, FFmpeg 8.0.1. Final main frames are 720×720 at 16 samples; rear frames use 12 samples, transparently retaining all 193 action frames. They are composed into 1280×720, 24 fps clips. A three-frame benchmark took about 2 seconds per frame under concurrent work. No high-sample beauty-render pass was spent on the incomplete geometry.

The measured authoring/review/render window was **32.1 minutes**. Main rendering took **412.9 seconds** and rear rendering **391.8 seconds**, running concurrently across about **6.9 minutes** of wall time. The sum of saved frame timing records across previews and finals is **14.7 process-minutes**; active authoring time was not separately metered. Details are in `records/run-accounting.json`. The recorded window starts at 16:03:47 UTC; initial reference reading and runtime discovery preceded that checkpoint. Authoring and rendering overlapped, so summed frame render time is not added to elapsed wall time. Review input was the listed local manufacturer references and assistant self-review; no independent reviewer was used. Per-task model token usage and session charge are **UNKNOWN**, not zero. No paid external generation job was submitted. This single assisted run establishes no causal model-superiority claim.
