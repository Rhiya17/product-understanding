# Work Order: Skinned Fold Video and Catalog Static Twins

**Date issued:** 2026-08-27
**For:** an autonomous agent with repository access (no prior conversation context assumed). Blender 5.2.0 LTS at `/Users/vbp/Applications/Blender.app`, headless only.
**Depends on:** `poc-3d-static-twin/twin/` (mechanism twin: `ready2jet-rigged.blend`, `action-spec.json`, `joint-evidence.json`, dress pass), `poc-3d-static-twin/runs/tripo-probe-01/` (textured scan), `poc-3d-static-twin/run_tripo3d.py` (runner conventions), `source-vault/` (per-product images), `evidence-packs/` (media-binding schema from the MVP v0 work order)
**Output:** (1) a fold video in which the photo-derived, real-looking scan folds with the rig's verified motion; (2) a static Tripo scan + turntable for each remaining catalog product, wired into the answer app as unapproved media bindings
**Spend ceiling:** $10 total provider spend, hard stop. Expected: ~$3 (4 catalog scans + margin).

---

## 0. Governing rules

1. **Motion comes only from the rig.** The scan is a visual skin bound to
   the existing evidence-mapped rig; no joint, axis, range, or ordering may
   be changed by this work. If binding pressure suggests a rig change, stop
   and report.
2. **INTERNAL ONLY.** The Tripo3D license check is still open. Every
   render, GLB, and turntable produced here is internal; media bindings
   created here carry `"rights_note": "Tripo3D license check OPEN — do not
   ship"` and stay unapproved (`approved_by: null` — the agent never sets
   it).
3. **Person-free inputs only** for any provider submission (program rule
   from the ByteDance rejection).
4. **Honest labeling of deformation.** Skinned joints will stretch where
   the fused shell crosses a hinge; measure and disclose (§1.4), never hide
   with invented geometry.
5. Hash-verify every provider input against its vault manifest before
   upload; record run artifacts exactly as `run_tripo3d.py` does
   (submission, request id immediately on submit, results, downloads).
6. **Stop-and-report:** spend ceiling; any rule above; a product whose
   vault images cannot honestly fill Tripo's semantic view slots (omit that
   product and record why, rather than mislabeling views).

## 1. Stage S — Skin the Ready2Jet scan onto the mechanism rig

1. **Armature conversion.** In a new `ready2jet-skinned.blend` derived from
   `ready2jet-rigged.blend`: build an armature whose bones mirror the
   existing part hierarchy (rear frame, front frame, lower/upper handle,
   seat unit, canopy, belly bar, cup holder, wheels). Drive the bones from
   the existing action parameters so `Ready2Jet_Fold_Correct` and the three
   defect parameters replay identically. Validate: joint-angle traces of
   the armature match the object-rig animation within 1e-4 rad across all
   frames (script the comparison; commit it).
2. **Alignment.** Scale/pose the scan to the rig's rest pose (the rig was
   built on the scan's proportions; expect near-identity plus the scan's
   baked lean). Record the applied transform.
3. **Binding.** Weight the scan to the bones: nearest-part rigid weights
   with a small smoothing band (2–4 cm) at part boundaries. Wheels and
   handle get fully rigid weights; fabric regions may blend. Keep weights
   scripted/reproducible.
4. **Deformation QA.** Render the fold; measure worst-case edge stretch at
   each joint band (script: per-frame edge-length ratio vs rest). Report a
   table per joint; flag ratios > 1.6 as visible artifacts with frame
   references. Disclose, and where severe, prefer masking the band with the
   part's rigid region over any geometry invention.
5. **Deliverables:** `ready2jet-skinned.blend`, binding + QA scripts,
   `renders/skinned-fold-official-angle.(gif|frames)` and
   `renders/skinned-fold-novel-rear-right.(gif|frames)` at 1024px with the
   dress-pass lighting, QA stretch report, and a contact sheet vs the
   official video (same five poses as Stage D). Commit checkpoint.

## 2. Stage T — Static twins for the remaining catalog

For each of: `graco-snugride-35-lite-lx`, `bose-qc-ultra-headphones`,
`levoit-core-300s`, `apple-macbook-air-13-m3` (the Levoit is the plan's
designated rigid control product — run it first):

1. **Input selection.** From that product's vault images, choose
   person-free views that honestly fill Tripo H3.1 slots (front required;
   left/back/right only if truly those views). Record choices + hashes in
   `poc-3d-static-twin/catalog-scans/<product>/input-manifest.json`. If no
   honest front view exists, skip the product and record why.
2. **Run** via the `run_tripo3d.py` conventions (seeded, auto_size,
   face_limit 100k, request id persisted): one run per product into
   `catalog-scans/<product>/`.
3. **Score (probe-level).** Welded-component count and largest-shell share,
   OBB extents vs official dimensions from that product's published claims
   (cite the claim ids), identity components present/missing from the
   provider preview. One short scorecard per product.
4. **Turntable.** Reuse `render_scan_turntable.py` (parameterize the GLB
   path and output dir) to render and encode a 24-frame 1024px turntable
   GIF per product.
5. **Wire into the app.** Add each turntable as a `VIDEO_FILE`-style media
   binding ONLY if the MVP v0 media schema is extended for derived assets;
   otherwise register them in a new
   `evidence-packs/<product>/derived-assets.json` with provenance (run id,
   input hashes, license status) and leave app wiring as a follow-up item
   in the report. Do not modify `source-vault/`.
6. Commit checkpoint per product or batched, report
   `docs/workorders/report-catalog-scans.md`: per-product verdicts, costs,
   skipped products with reasons.

## 3. Definition of done

1. Skinned fold renders exist from both cameras; the motion validation
   (§1.1) passes; the stretch QA table is in the report.
2. Each catalog product has either a scan + scorecard + turntable or a
   recorded skip reason.
3. Total provider spend reported; ≤ $10.
4. All renders/GLBs labeled internal-only; no `approved_by` set; protected
   files untouched (`claims.json`, `reviews.json`, `verdicts.json`,
   `source-vault/`); repo clean; tests and validators green.
5. Final report: what a viewer sees now (real-looking fold video?), the
   VACE-skin follow-up recommendation (POC 7), and the license-check
   blocker status.
