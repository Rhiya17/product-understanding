# POC 5 scorecard — Meshy v6, run meshy-v1-pilot-run-01

**FROZEN AS V1 PILOT (2026-08-14).** This run used input pack v1 (conflicting
canopy states, no rear view, close-up held-out) and does NOT count toward the
v2 three-run consistency matrix. Its role: pilot evidence that Meshy produces
a recognizable stroller while failing exact-product geometry and identity.
The two orphaned same-pack submissions stopped mid-flight on 2026-08-13 are
`../runs/meshy-v1-pilot-orphan-02/` and `-03/` (fal billing to be checked
before any new spend).

Run date 2026-08-13; scored 2026-08-14. Endpoint
`fal-ai/meshy/v6/multi-image-to-3d`, 4 input views, no seed parameter
(stochastic), `symmetry_mode: off`, `target_polycount: 100000`. Artifacts in
`../runs/meshy-v1-pilot-run-01/`.

| Check | Result | Threshold | Pass? |
|---|---|---|---|
| Held-out silhouette IoU | **not measurable** — held-out image is a close-up; no independent global view exists in the input pack | ≥ 0.85 | n/a (input-pack defect, not a tool result) |
| Landmark max offset | not yet measured (needs Blender camera match) | ≤ 3% | pending |
| Dimensional error (worst axis) | **D +21.2%**, H −9.7%, W −6.7% after least-squares uniform fit to official 68.58 × 109.22 × 52.07 cm (D/H/W); axis mapping assumed Y-up/x-depth, to be confirmed visually | ≤ 5% | **FAIL** (pending axis-mapping confirmation) |
| Identity components present | thumbnail: 4 wheels, handle, canopy, cup holder, basket present; belly-bar region shows suspect tan-tipped bar (real belly bar is all black) — verify in Blender | all | pending |
| Invented geometry | rear surfaces are inferred by construction (no rear input view); suspect tan bar; needs orbit inspection | none | pending |
| Fusion grade | **one welded shell: 97.8% of faces in a single position-welded component** (13 components on welded GLB; 3 on OBJ). NOT separable by connectivity — F1 vs F2 requires Blender inspection of moving-part boundaries (handle/frame, seat/chassis, wheels/legs) | info | F1–F2 pending |
| Face count | 100,964 faces vs 100k target — valid hit. (Vertex counts vary by format: GLB duplicates vertices at UV/normal seams; weld before any connectivity analysis) | info | — |

## Method corrections applied (2026-08-14)

1. First-pass "4,089 components" was an artifact of splitting unwelded GLB
   geometry (vertices duplicated at attribute seams). Position-welded
   analysis shows one dominant shell. Connectivity diagnostics must always
   weld coincident positions first.
2. First-pass "proportions promising" compared against generic stroller
   dimensions. Scoring uses the official Graco spec only:
   W 20.5 × D 27 × H 43 in = 52.07 × 68.58 × 109.22 cm (identical for
   2209064 and 2212125).

## Blender inspection (2026-08-14, Blender 5.2.0 LTS build 2026-07-14)

Renders in `../validation/renders/meshy-v1-pilot-run-01/` (5 orthographic
views, 4 close-ups, 36-frame turntable GIF; render resolution 1024,
turntable 512). Filenames were corrected to semantic names on 2026-08-14
after the axis check: `ortho-front/rear/side-left/side-right/top.png`.
Model orientation for this mesh: stroller front = Blender −X, rear = +X,
left side = −Y (left/right in the parent-behind-handle convention).
Verify facing per run before trusting the names on future meshes.

**Axis mapping confirmed visually:** Blender X = depth (1.599), Z = height
(1.898), Y = width (0.934) — the least-squares assumption was correct, so
the dimensional result is final.

**Defects found:**

1. **Invented wheel design (identity mutation).** Mesh wheels are 5-spoke
   automotive-style; the real product has tri-spoke Y-arm wheels, clearly
   visible in input view-03. Analogue of the generation POCs' "invented
   control" hard failure.
2. **Belly-bar tan texture bleed.** Real belly bar is all black; the mesh
   wraps a tan leather section onto it (handle-grip texture bleed).
3. **Melted seat/footwell region.** Footwell fabric forms a slab-like bulge
   projecting forward; likely contributes to the +21% depth error together
   with the over-extended canopy (canopy-state conflict across inputs).
4. **Garbled basket texture and logo** (expected from generation; noted).
5. Wavy/dented frame tubes near junctions; melted strap geometry at the
   canopy/handle junction (rear, fully inferred region, structurally
   plausible overall).

**Fusion grade: F2.** One welded shell (97.8%); wheel-to-frame,
handle-to-frame, and seat-to-chassis boundaries are continuous melted
junctions, not clean cuttable seams. Segmentation for POC 6 would mean days
of remodeling, not hours of cutting.

## Final verdict: FAIL

- Dimensions: FAIL (depth +21.2% after best uniform fit; threshold 5%).
- Component identity: FAIL (invented wheel design; belly-bar mutation).
- Fusion: F2 — even a passing mesh of this quality would be expensive to rig.
- Not measurable: silhouette IoU (no global held-out view in the pack).

## Input-pack validity decision (runbook step: repeat or fix first)

**Do not spend runs 02–03 on this input pack.** Two of its defects
(three conflicting canopy states; no rear view) are plausible causes of the
depth failure and rear inference, so repeating measures a confounded
experiment. But the invented wheel design happened despite clear evidence
in view-03 — that one is on the tool, and runs 02–03 remain worth doing
*after* the pack is fixed, to separate tool failure from input failure.

Pack fixes required before further spend:
1. State-consistent views (single canopy configuration) — harvest from the
   official fold video's wide shots and/or PDP gallery scrape.
2. At least one true rear or rear-three-quarter view.
3. One clean global three-quarter view reserved as held-out (restores the
   silhouette IoU check).
4. Confirm view-02's SKU or drop it.
