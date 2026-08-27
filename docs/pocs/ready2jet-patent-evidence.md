# Ready2Jet patent evidence

**Stage A finding (2026-08-27): one usable mechanism patent found.**

This note treats patent evidence as mechanism documentation, not proof of a
retail SKU association.  The accepted patent does not say "Ready2Jet".  Its
association is a high-confidence visual and functional match to the official
manual and video, recorded explicitly so a later contradiction can invalidate
the rig rather than being explained away.

## Accepted candidate

### US20220169297A1 - Systems, methods, and apparatus for providing a compact automatic folding stroller

- Primary record: <https://patents.google.com/patent/US20220169297A1/en>
- Assignee: Graco Children's Products Inc.; priority 2020-11-30; published
  2022-06-02.
- Status: abandoned application.  Status does not reduce its value as public
  technical evidence, but this note makes no legal or freedom-to-operate
  inference.
- Match confidence: **HIGH**, not product-name-confirmed.

The match is unusually specific:

| Patent evidence | Ready2Jet evidence | Finding |
|---|---|---|
| Claim 7 / Fig. 3-4: first release is a thumb button or switch and second release is a squeeze button on the handle | Manual p.34: `claim_r2j_step_fold_4` then `claim_r2j_step_fold_5`; official video frames 1127-1153 | Exact control type and order |
| Figs. 1-2: handle member 106, front leg 108, rear leg 110 meet at side hub 112 | Manual p.34 fold drawing and video frames 1166-1186 show the same common side-hub architecture | Visible frame topology matches |
| Figs. 3-5: upper handle 120 folds at pivot 118 relative to lower handle 124 | Video frames 1173-1186 and official folded-state image show the handle doubled over at a mid-handle pivot | Visible moving part matches |
| Figs. 6-10: handle arm 614 and front-leg arm 616 couple through slider/rear-leg arm 618 at pivot 620 inside hub 112 | Internal linkage is not visible in Ready2Jet evidence | Patent documents the hidden coupling; product mapping inherits the HIGH-not-explicit caveat |
| Figs. 11A-11F: handle and front leg rotate toward rear leg; wheelbase collapses; final pose is upright and wheel-clustered | Official video frames 1166-1206 and manual pp.34-35 | Fold direction, sequence, and final pose match |
| Fig. 1: compact four-wheel stroller, one-sided cup holder, belly bar, seat/canopy arrangement | Official product imagery | Overall product architecture matches; cosmetic wheel-spoke differences are not used as mechanism evidence |

### Patent part map used by POC 6

| Patent part | Description | Twin interpretation |
|---|---|---|
| 102 | stroller frame | rig root / assembled frame |
| 106 | handle member | upper and lower handle assemblies |
| 108 | front leg member | front-leg assembly |
| 110 | rear leg member | rear-leg assembly / reference member |
| 112 | hub mechanism | left/right principal fold hubs |
| 118 | handle pivot device | upper-handle fold hinge |
| 120 | upper handle portion | grip-side handle section |
| 124 | lower handle portion | hub-side handle section |
| 126 | release mechanism | thumb switch + squeeze lever control housing |
| 400 | handle cable | hidden release coupling; not modeled externally |
| 600 | hub lock | hidden latch; represented as a rig state, not invented surface geometry |
| 612 | hub linkage | hidden kinematic coupling |
| 614 | handle arm | linkage from hub to handle plate |
| 616 | front-leg arm | linkage from hub to front-leg plate |
| 618 | slider / rear-leg arm | linkage reference inside rear leg |
| 620 | linkage pivot | common linkage pivot |
| 622 | rear-leg cable | hidden cable; behavior only, no visible geometry |
| 702 | front-leg hub plate | front-leg rotation member |
| 704 | handle hub plate | handle rotation member |
| 1000 | spring | automatic-fold bias; behavior only |

The internal cables, latch, linkage plates, slider, and spring are documented
by the patent but are not visible in the product evidence.  POC 6 uses their
documented *effect* to coordinate external parts; it does not invent or expose
internal surface geometry.

## Rejected candidates

| Candidate | Rejection reason |
|---|---|
| US20140028003A1, *Foldable Stroller* | Push bar and front leg telescope through a guide section using a push-pull tape strip. Ready2Jet evidence shows rotation about a common hub and a folding upper handle, not this telescoping architecture. |
| US20090278335A1 / US8186706B2, *One-Hand Fold Stroller Frame* | A three-dimensional, laterally narrowing frame. Ready2Jet's observed fold is planar: width is retained while front/handle members converge toward the rear legs. |
| US6068284A, *Stroller with one hand release mechanism* | Generic and much older release architecture; it lacks the exact recent thumb-switch/squeeze-button, split-handle, hub sequence already documented by US20220169297A1. |
| US20120242062A1 / US8905428B2, *Foldable stroller and fold joint* | Different exposed fold-joint/tray architecture; no exact visible match to the compact Ready2Jet frame. |

## Governing limitation

If future product evidence contradicts US20220169297A1, all rig joints relying
on it must be downgraded to `INFERRED` or replaced.  The patent is not permission
to add unobserved exterior geometry, and it does not close the Tripo output
license check.
