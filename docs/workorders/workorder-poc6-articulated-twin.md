# Work Order: POC 6 — Articulated Twin and First Rendered Fold Video

**Date issued:** 2026-08-28
**For:** an autonomous agent with repository access (no prior conversation context assumed). Blender 5.2.0 LTS is installed at `/Users/vbp/Applications/Blender.app` and must be driven headless (`--background --python`).
**Depends on:** `poc-3d-static-twin/runs/tripo-probe-01/` (Tripo H3.1 mesh, probe scorecard), `evidence-packs/graco-ready2jet-2212125/` (fold procedure STEP claims), `source-vault/graco-ready2jet-2212125/` (manual PDF, official fold video, images), `docs/planning/digital-twin-phase-plan.md` (Decisions 3, 5, 6)
**Output:** a rigged, articulated digital twin of the Graco Ready2Jet (Kingston) in Blender, an evidence map for every joint, and the project's first deterministic rendered fold video
**Budget:** $0 external spend (all local); owner has ruled out purchasing the physical stroller — plan within PDP + vault evidence only.

---

## 0. Governing rules

1. **The mechanism is never invented.** Every joint's axis, placement, and
   motion range must cite evidence: a manual step/diagram, a patent figure,
   or specific frames of the official fold video. Where evidence is absent,
   the element is labeled `INFERRED` in the evidence map and listed in the
   report — visible, never silent.
2. **Renders are internal-only.** The Tripo3D license check is OPEN and the
   fold video's rights are internal-research-use. Nothing from this work
   order ships to any external surface.
3. **Deterministic and reproducible.** All Blender work is scripted or
   saved as versioned `.blend` files; renders come from committed scripts
   with fixed cameras and frame ranges. Defect injection must be a
   parameter (Decision 6 requires the rig to render deliberately-wrong
   folds later), so build the animation as named actions driven by a small
   set of joint parameters, not hand-keyed vertex animation.
4. **Stop-and-report:** evidence contradicts the rig; a stage budget is
   exhausted without its outcome; anything would require external spend.

## 1. Ground truth to assemble first (Stage A)

1. **Fold procedure claims:** extract the ordered fold/unfold STEP claims
   from the evidence pack (`object.procedure`, `step_number`, action text).
   These define what the animation must show, step by step.
2. **Patent search (Decision 3, still undone — do it now):** search Google
   Patents/USPTO for Graco / Newell Brands compact-stroller one-hand-fold
   mechanisms. Match candidate figures against the Ready2Jet's visible
   hardware (manual diagrams; fold-video frames). Deliverable:
   `docs/pocs/ready2jet-patent-evidence.md` mapping patent part numbers to
   visible parts, or an explicit "no usable patent found" finding. A
   sibling-product patent that does not match visible hardware must be
   rejected (wrong-mechanism contamination).
3. **Fold-video frame study:** extract frames covering the full fold
   (person present is fine for *study*, never for tool input), and write
   down the observable kinematics: which member moves first, pivot
   locations, direction of handle travel, wheel behavior, final folded
   pose. Deliverable: `poc-3d-static-twin/evaluation/fold-kinematics.md`
   with frame references.
4. **Folded-state dimensions:** record the official folded dimensions in
   the input-pack manifest (currently null). If no official figure exists,
   estimate from the fold video against known open dimensions and label
   `INFERRED`.

## 2. Geometry strategy (Stage B) — rebuild over surgery, verified by spike

Probe finding (2026-08-28, committed with scorecard-tripo-h31-probe-01): the
Tripo mesh is one welded shell (97.2%) and its local topology is fragmented
— a spatial cut around one wheel yielded 38 fragments and ~1,100 open
boundary edges. Cutting this shell into clean rig-ready parts is expected to
be more expensive than rebuilding parts over it.

**Time-boxed spike (max half a day each), one part — the handle assembly:**

- **B1 Surgery:** segment the handle off the Tripo mesh in Blender (region
  select, separate, close holes, cleanup). Record hours and defects.
- **B2 Rebuild:** model a clean parametric handle over the Tripo mesh used
  as a dimensional scaffold (curves + bevel for tube, simple shells for
  grip), snapped to the scaffold's proportions. Record hours and fidelity.

Pick the winner by cost × rig-readiness; document the decision in the
report. **Expectation to confirm or refute: rebuild wins.** Whichever wins,
the Tripo mesh remains the reference scaffold and its provenance (run id,
pack hash) is recorded in the `.blend`.

**Part list (driven by the fold procedure, nothing more):** main frame
(front legs / rear legs as evidence dictates), handle assembly with fold
lever + thumb switch (geometry from manual diagrams and video close-ups;
label INFERRED details), seat/backrest unit, canopy (fold-relevant only),
4 wheel assemblies (tri-spoke — view-03 is the reference; Meshy failed
here), basket (simplified), belly bar, cup holder. Rear/unseen surfaces:
model minimally and label INFERRED.

## 3. Rig and animate the fold (Stage C)

1. Define the kinematic chain from Stage A evidence: parent/child
   relations, joint types (hinge/slider/latch), axes, and limits. Store as
   both Blender constraints and a committed JSON evidence map:
   `poc-3d-static-twin/twin/joint-evidence.json` —
   `{joint, type, axis, range, evidence: [claim ids, patent figs, video
   frames], confidence: DOCUMENTED|INFERRED}`.
2. Author the fold as a parameterized action following the pack's fold
   STEP claims in order (slide thumb switch → squeeze lever → fold), with
   a scrubbable 0..1 fold parameter per stage so defect variants (reversed
   direction, skipped latch) are render-time parameters (Decision 6).
3. Match the folded pose to Stage A's folded-state evidence (video final
   frame; folded dimensions).

## 4. Render and verify (Stage D)

1. Render: (a) a 360° turntable of the open twin, (b) the fold from the
   official video's approximate camera angle, (c) the fold from one new
   angle the video cannot provide (the point of the twin). 1024px, fixed
   seeds/cameras, scripts committed.
2. Verify:
   - **Pose comparison:** side-by-side contact sheet of rendered fold
     frames vs official-video frames at matched stages; note divergences.
   - **Dimension check:** open and folded bounding dimensions vs recorded
     figures; report % error.
   - **Qwen verifier (optional, pennies):** run the render through
     `system/verify_claims.py`-style checks used in the VLM-verifier POC
     (same product? motion direction? reaches folded state?). Advisory
     only — the verifier is unbenchmarked (Decision 4).
3. Deliverables: `poc-3d-static-twin/twin/` containing the `.blend`, the
   joint-evidence JSON, render scripts, rendered MP4s/GIFs, verification
   contact sheets, and `report.md` with hours per stage (the true cost of
   POC 6 is this work order's most important measurement), the B1/B2 spike
   verdict, INFERRED inventory, and open risks.

## 5. Definition of done

1. The fold animation plays every documented fold STEP in order; no
   undocumented mechanism motion.
2. Every joint has an evidence-map entry; INFERRED items are enumerated in
   the report.
3. A rendered fold video exists from at least one novel camera angle.
4. Hours per stage are recorded; the repo is clean; all commits per stage;
   no external spend; nothing published externally.
