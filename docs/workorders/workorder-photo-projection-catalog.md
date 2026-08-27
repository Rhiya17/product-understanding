# Work Order: Photo-Projected Twins — Stroller Fold + Catalog Turntables

**Date issued:** 2026-08-27
**For:** an autonomous agent with repository access (no prior conversation context assumed). Blender 5.2.0 LTS at `/Users/vbp/Applications/Blender.app`, headless only.
**Depends on:** `poc-3d-static-twin/twin/ready2jet-rigged.blend` (mechanism twin), `source-vault/<product>/` (official imagery + manifests), published dimension claims in `evidence-packs/*/claims.json`, prior findings: texture-projection report (scan-to-twin projection FAILED coverage — do not retry it), POC 7 findings (generative repaint FAILED identity — do not retry here)
**Goal:** real-looking product visuals whose appearance pixels come ONLY from official vault imagery projected onto deterministic geometry — no generative appearance, no Tripo texture ancestry. One articulated deliverable (stroller fold) + static turntables for the rest of the catalog where honestly feasible.
**Spend:** $0 external. All local.

---

## 0. Governing rules

1. **Appearance pixels come only from vault-registered official images** of
   the exact product/colorway, hash-verified against the manifest before
   use. No generative fill, no hand-painted product details, no textures
   from Tripo scans. Uncovered regions keep a neutral dress-pass material
   and are recorded in a coverage map — disclosed fallback, never invented.
2. **Geometry is deterministic and dimension-grounded.** New geometry (for
   products without a twin) is parametric, built to the product's published
   dimension claims (cite claim ids in the scene metadata); visible-detail
   proportions may be traced from official images; unseen surfaces minimal
   and `INFERRED`.
3. **The stroller's rig is untouched** — same rule as every twin work
   order: no joint, action, or evidence-map change.
4. **Person-free imagery only.** An image containing any person is not a
   projection source, full stop.
5. **INTERNAL ONLY.** Manufacturer imagery is cleared for internal research
   use, not for shipping; every rendered GIF/MP4 is watermarked and
   registered in `derived-assets.json` with provenance (geometry hash,
   source image ids/hashes, scripts). `approved_by` untouched. Rights note:
   this chain has NO Tripo ancestry — the open rights question is
   manufacturer-imagery reuse, which goes to the owner's rights review.
6. **Honest per-product verdicts.** A product that cannot meet these rules
   gets a recorded skip with reasons — like the Stage T skips — not a
   degraded asset.
7. **Stop-and-report:** any rule above; a per-product budget exhausted
   without its outcome; camera-match residual too poor to project (§2.2).

## 1. Method (applies to every product)

1. **Camera match:** for each usable official image, solve a Blender camera
   (position, rotation, focal length) that aligns the geometry's silhouette
   to the photographed product. Record the per-image silhouette IoU between
   the rendered geometry mask and the image's product mask; require
   **IoU ≥ 0.75** for the image to qualify as a projection source
   (record all attempts, pass or fail).
2. **Project:** UV-project each qualifying image onto the geometry faces
   visible from its matched camera (front-facing threshold ~60° to avoid
   smear); later images fill only still-uncovered regions (best-view-first
   ordering). Bake to per-part textures; feather boundaries in the shader
   mask, not by inventing pixels.
3. **Coverage + identity QA:** per-part coverage table; the POC 7 checklist
   as pixel checks where applicable (correct part colors per official
   imagery, no text the product doesn't carry, no cross-part bleed —
   per-part UV isolation as before).
4. **Render:** dress-pass lighting, 1024px, existing GIF encoder,
   watermarked.

## 2. Product lanes (work in this order)

### Lane 1 — Graco Ready2Jet (the fold video; budget: 1.5 days)

- Geometry: the existing mechanism twin, rest pose.
- Projection sources (candidates, all in `poc-3d-static-twin/inputs/images/`
  and the vault): `view-01-front-3q.png`, `view-04-side-profile.png`,
  `heldout-05-front-3q.png`, official fold-video title frames — each must
  pass the §1.1 camera-match gate individually.
- Deliverables: re-rendered `fold-official-angle`, `fold-novel-rear-right`,
  `open-turntable` with projected appearance; three-way contact sheet
  (schematic dress pass vs POC 7 run 2 vs this); coverage table; report.
- Expectation to verify: front/left coverage strong; rear falls back to
  dress pass — acceptable and disclosed (both fold cameras favor covered
  angles; state this measured, not assumed).

### Lane 2 — Levoit Core 300S (budget: 1 day)

- Geometry: parametric build — the product is a cylinder with a control
  face and vents (`claim_c300s_spec_dimensions`: 8.7 × 8.7 × 14.2 in);
  trace vent/panel proportions from official imagery.
- Projection: official front/three-quarter and top images from the vault.
  A cylinder's rotational symmetry means one good side image can cover a
  wide arc honestly — document the wrap policy (real repeat vs fallback).
- Deliverable: turntable GIF + report; register as derived asset.

### Lane 3 — Apple MacBook Air 13″ M3 (budget: 1 day)

- Geometry: parametric slab + lid at the published closed dimensions
  (`claim_mba_spec_height/depth/width`); optional open-lid pose only if an
  official image supports the angle. Keyboard/deck detail comes from
  projection, not modeling.
- Projection: official top/keyboard and profile imagery (HTML-guide
  sourced; verify manifest registration first — if an image is not in the
  vault, register it through the proper curation path or skip it).
- Deliverable: closed + (if supported) open turntables; report. This
  replaces the failed Tripo slab as the MacBook's visual asset.

### Lane 4 — Bose QC Ultra (budget: half a day)

- The Tripo scan turntable already looks right but carries Tripo ancestry
  and a +147% worst-axis scale error. Decide by measurement: attempt a
  minimal parametric build (headband arc + earcup volumes at published
  dims) with photo projection. If the §1.1 gate fails on the curved
  geometry within budget, record the verdict and keep the scan turntable
  as the interim internal asset — explicitly labeled with its ancestry.

### Lane 5 — Graco SnugRide 35 Lite LX (budget: half a day, audit only)

- Complex organic shell with almost no person-free semantic views — the
  Stage T skip logic likely applies to geometry too. Do the audit only:
  inventory usable vault images, estimate feasibility honestly, and write
  the verdict (expected: serve official imagery via the app's existing
  media bindings; no twin this round). Building nothing here is an
  acceptable, expected outcome.

## 3. Definition of done

1. Lane 1 fold videos exist with projected photo appearance and pass the
   identity QA; contact sheet included.
2. Lanes 2–5 each end in a registered derived asset **or** a recorded
   skip/audit verdict — no silent gaps; every lane's hours logged.
3. All renders watermarked internal-only; provenance registered; protected
   files untouched (`claims.json`, `reviews.json`, `verdicts.json`,
   `source-vault/` read-only except through the curation path in Lane 3);
   repo clean; tests/validators green; $0 external spend.
4. Final report `docs/workorders/report-photo-projection.md`: per-lane
   results, coverage tables, the rights-review items for the owner
   (manufacturer-imagery reuse; Tripo ancestry now relevant only to the
   Bose interim asset), and what the answer app can serve once the owner
   approves bindings.
