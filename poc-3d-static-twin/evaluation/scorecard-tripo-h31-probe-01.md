# POC 5 scorecard — Tripo3D H3.1, run tripo-probe-01

**EXPLORATORY CAPABILITY PROBE (2026-08-28).** Input pack v1.2 has no valid
independent held-out and Tripo's semantic slots take only two of the four
Meshy inputs (front + left), so this run is NOT the runbook's controlled
cross-tool comparison. It answers the Decision-1/Decision-2 cost questions:
fusion severity, identity plausibility, and scale behavior. Silhouette-IoU
and landmark checks: NOT SCORABLE with this pack (by design of the probe).

Run: endpoint `tripo3d/h3.1/multiview-to-3d`, submitted 2026-08-28 UTC,
seeds model/texture 20260827 (reproducible), face_limit 100000,
geometry/texture "detailed", pbr on, `auto_size` on. Inputs: view-01 (front
slot), view-04 (left slot), byte-identical to their Meshy-pilot versions.
Artifacts in `../runs/tripo-probe-01/` (submission, request id, result,
GLBs, provider preview). Cost: ~$0.60 (provider-listed pricing).

| Check | Result | Threshold | Verdict |
|---|---|---|---|
| Held-out silhouette IoU | not scorable — no independent held-out in pack v1.2 | ≥ 0.85 | n/a (pack) |
| Landmark max offset | not scorable (same reason) | ≤ 3% | n/a (pack) |
| Dimensional error, OBB vs official 52.07 × 68.58 × 109.22 cm | sorted extents 45.5 / 76.1 / 116.5 cm → **−12.6% / +11.0% / +6.6%**; absolute scale came from `auto_size` with NO fitting step | ≤ 5% after scaling | **FAIL at 5%**, but materially better than Meshy (worst axis +21.2% after least-squares fit); OBB-vs-W/D/H convention mismatch pending Blender pose alignment |
| Identity components present | provider preview: canopy, tan handle grip, belly bar, one-sided cup holder on the correct side, basket, four wheel assemblies | all | provisional PASS — Blender orbit inspection pending (wheel spoke design unverified; Meshy failed exactly there) |
| Invented geometry | rear surfaces inferred by construction (no rear input); orbit inspection pending | none | pending |
| Fusion grade | **one welded shell: 97.2% of faces in the largest position-welded component** (3 components on welded mesh: 96,608 / 2,742 / 1 faces) | info | **F2-class, same as Meshy (97.8%)** |
| Face count | 99,351 vs 100k requested — valid hit | info | — |

## Probe conclusions

1. **Fusion is a tool-class property, not a Meshy defect.** Two independent
   production tools produced one welded shell. Plan accordingly: POC 6
   rigging must budget for manual mesh segmentation (cutting the shell into
   parts in Blender) for ANY tool in this class; "separable parts out of the
   box" is off the table without new evidence.
2. **Tripo's scale/proportion behavior is better.** auto_size landed within
   ~13% absolute with zero fitting; Meshy needed a fitted scale and still
   missed by +21% on depth. If proportions survive pose-aligned re-scoring,
   Tripo is the stronger statue candidate.
3. **Reproducibility is real.** Seeded runs mean a re-run of this exact
   submission is expected to reproduce this mesh — cheap regression checks.
4. Owner decision 2026-08-27: no physical stroller purchase. Decision 2
   capture is off; the independent-held-out and rear-view gaps stay open,
   and mechanism ground truth remains manual + patents + official video.

## Open items

- Blender pose-aligned dimension re-score and orbit inspection (wheel
  design, rear surfaces, texture bleed).
- Tripo3D commercial license/API terms check — still OPEN; must close
  before anything derived from this mesh ships (Decision 1).
