# Work Order: POC 8 — Rigid-Body Connection Scene (Bose QC Ultra → MacBook Air)

**Date issued:** 2026-08-29
**For:** an autonomous agent with repository access (no prior conversation
context assumed). Blender 5.2.0 LTS is installed at
`/Users/vbp/Applications/Blender.app` and must be driven headless
(`--background --python`).
**Question under test:** can two static Tripo3D twins plus a modeled cable,
arranged and animated deterministically in Blender, produce a *correct-by-
construction* video of "connect the Bose QuietComfort Ultra headphones to a
MacBook Air with the audio cable" — with zero generative freedom in the
primary arm?
**Output:** a deterministic rendered connection video (primary arm), a
VACE-skinned photoreal variant (experimental arm, expected hard), a findings
doc, and a registration decision.
**Budget:** primary arm $0 external. Hard ceiling **$10** external spend
total (VACE runs + VLM checks + optional Seedance comparison). Stop at the
ceiling regardless of state.

---

## 0. Governing rules

1. **Nothing invented silently.** Every scene decision — port side, plug
   end, object pose, cable color — cites a claim, an official image, or is
   labeled `INFERRED` in the evidence map and surfaced in the report.
2. **Internal-only.** The Tripo3D license check is still OPEN
   (docs/pocs/tripo3d-license-review.md) and both twins are
   `internal_only: true`. Every artifact from this POC is internal-only,
   watermarked, and registered (if at all) with `internal_only: true`.
3. **Deterministic and reproducible.** All Blender work is committed
   scripts and versioned `.blend` files: fixed cameras, fixed frame ranges,
   named actions driven by a small set of parameters (mirrors POC 6 rule 3).
4. **Fail closed, stop-and-report:** evidence contradicts the scene; a
   stage gate fails twice; anything would exceed the budget ceiling.

## 1. Assets that already exist (verify, do not recreate)

| Asset | Path |
|---|---|
| MacBook Air twin (Tripo H3.1, PBR GLB, 37,906 verts) | `poc-3d-static-twin/catalog-scans/apple-macbook-air-13-m3/pbr_model-wTBg81hlp4aYRYEHUDwqP_model.glb` |
| Bose QC Ultra twin (Tripo H3.1, PBR GLB, 54,612 verts, single shell) | `poc-3d-static-twin/catalog-scans/bose-qc-ultra-headphones/pbr_model-zTFUED2CgtA628PGPOxHI_model.glb` |
| Mesh analyses + scorecards | `mesh-analysis.json`, `scorecard.md` beside each GLB |
| Known Bose defect | worst-axis scale error 147% (recorded in the Bose pack's derived-assets disposition) — Stage B exists to fix this |
| Official Mac right-side jack photo | `source-vault/apple-macbook-air-13-m3/images/guide-right-side-headphone-jack.png` (`src_img_guide_right_side`) |
| Official Bose earcup + cable photo | `source-vault/bose-qc-ultra-headphones/images/black-earcup-controls-wired-35mm.png` (`src_img_black_controls`) |
| Blender photo-projection precedent | `poc-3d-static-twin/photo-projection/` (Blender 5.2.0 headless scripts to copy patterns from) |
| VACE runner + gates precedent | `poc-wanvace-control-video/run_vace.py`, `docs/pocs/poc7-vace-skin-findings.md` |

## 2. Exact models

| Role | Model / tool | Notes |
|---|---|---|
| Primary arm renderer | **Blender 5.2.0 LTS (Eevee)** — not a generative model | $0, deterministic, local |
| Experimental skin arm | **`fal-ai/wan-vace-14b/depth`** (WAN VACE 14B, depth control) | POC 7's endpoint; $0.24/4s @480p, $0.48 @720p; seeds 42001 then 42002 |
| Verifier | **`qwen/qwen3-vl-235b-a22b-instruct`** via **`fal-ai/any-llm/vision`** | temperature 0, JSON verdicts, `parse_verdict` from `app/keyframe_video.py` |
| Optional comparison arm | **`bytedance/seedance-2.0/image-to-video`** (first/last frame) | only if budget remains; twin renders as keyframes |
| Twin re-scan (NOT in this POC) | `tripo3d/h3.1/multiview-to-3d` via fal | out of scope — Stage B rescales the existing mesh instead |

Credentials: `~/.config/showme/fal.env` exports `FAL_API_KEY`; map it to
`FAL_KEY` before importing `fal_client` (pattern in `app/fal_video.py`).

## 3. Stage A — ground truth and the correctness checklist

Assemble from the packs (these claims exist; verify IDs before use):

- `claim_bqcu2_step_aux_1`: audio cable → **2.5 mm port on the LEFT earcup**
- `claim_bqcu2_step_aux_2`: other end → **3.5 mm port on the source device**
- `claim_bqcu2_aux_cable_spec_1`: the cable is **"2.5 mm to 3.5 mm audio cable"** (asymmetric!)
- `claim_bqcu2_part_aux_port_1`: 2.5 mm AUX port location on the left earcup
- `claim_mba_part_headphone_jack`: Mac 3.5 mm jack is on the **RIGHT side**
- `claim_mba_spec_height` / `_width` / `_depth`: Mac dimensions (for scale)
- Bose dimension claims if present; else take dimensions from the vault's
  official spec source and record the source id (do NOT invent numbers).

Deliverable: `poc8/evidence-map.md` — the correctness checklist every later
gate scores against: (1) 2.5 mm end into LEFT earcup, (2) 3.5 mm end into
Mac's RIGHT-side jack, (3) both products match official photos, (4) nothing
else in scene moves or appears.

## 4. Stage B — twin QA and deterministic scale repair (gate 1)

1. Load each GLB headless; log axis-aligned extents (compare with the
   committed `mesh-analysis.json`).
2. **Per-axis rescale to claimed dimensions** — a deterministic, evidence-
   cited correction of the known 147% Bose defect (each scale factor cites
   the dimension claim it satisfies).
3. Render each repaired twin from the official photo's viewpoint; VLM check
   against the official image (identity + proportions). One retry after
   parameter fixes.
4. **Gate 1:** post-repair worst-axis error vs claimed dimensions ≤ 5%, and
   VLM identity verdict `pass` for both twins. Fail twice → stop-and-report
   (the twin needs a re-scan; that is a separate spend decision for the
   owner, not this POC).

## 5. Stage C — the cable (built, and itself evidence-checked)

Model in Blender: a curve-following cable with a **2.5 mm plug on end A**
and a **3.5 mm plug on end B** (plug barrel diameters are the connector
spec itself — cite `claim_bqcu2_aux_cable_spec_1`; black finish cites the
official earcup photo; every other visual choice is `INFERRED`). Static
render of the cable alone → VLM check against the earcup photo's visible
cable. Gate 2: verdict `pass` (one retry).

## 6. Stage D — scene assembly and named-action animation

- Desk plane, neutral studio world lighting (fixed values in script).
- MacBook right side toward camera (jack visible — matches
  `guide-right-side-headphone-jack.png` framing); headphones beside it,
  left earcup accessible.
- Two shots, static camera each (POC 7 showed camera motion is the enemy):
  - **Shot 1 (4 s / 96 frames @24 fps):** end A travels a follow-path into
    the left-earcup port; ends fully seated.
  - **Shot 2 (4 s / 96 frames):** end B into the Mac's right-side jack.
- All motion as named actions driven by 2–3 parameters (path progress,
  seat depth) so wrong-fold-style defect renders remain possible later.
- Deliverables: `poc8/scene.blend`, `poc8/animate_connection.py`.

## 7. Stage E — deterministic render (primary arm)

Render both shots at 1280×720/24 fps + a stitched full video + poster frame
+ per-frame **depth passes** (the VACE control input, mirroring
`render_defect_control.py` patterns). Advisory VLM check of sampled frames
against the Stage A checklist — for this arm the render is correct by
construction, so the check is measuring *twin fidelity*, not motion truth.
Record verdicts either way. **Gate 3:** checklist items 1–2 visibly true in
the rendered frames (this catches scene-authoring errors, e.g. wrong side).

## 8. Stage F — experimental VACE skin arm (expect difficulty; bounded)

POC 7 verdict stands: every skin run failed identity (invented parts,
pseudo-brand text). Run at most **3 attempts** on Shot 1 only:
480p seed 42001 probe → if silhouette mean IoU ≥ 0.85, 720p seeds
42001/42002. Prompt additions this time: appearance-only instruction plus
explicit negatives ("no added controls, buttons, badges, text, or logos of
any kind") and the two official photos as reference conditioning if the
endpoint accepts them. Gates (from POC 7): silhouette IoU ≥ 0.85 mean /
0.80 min AND VLM identity `pass`. Expected spend ≤ $1.50. A third
consecutive identity failure closes the arm with "confirms POC 7" —
that is a *valid finding*, not a POC failure.

## 9. Stage G — optional Seedance comparison arm (budget-permitting)

If ≥ $3 of ceiling remains: feed Shot 1's first and last *rendered frames*
to `bytedance/seedance-2.0/image-to-video` (4 s, seed 42001) and VLM-verify
— one data point comparing "deterministic motion" vs "interpolated motion
between deterministic keyframes" on the same scene. Skip silently if budget
is short.

## 10. Stage H — report and registration decision

1. `docs/pocs/poc8-connection-scene-findings.md`: per-stage outcomes, spend
   ledger with request IDs, contact sheets, the evidence map, INFERRED list,
   and an explicit verdict per arm against the Stage A checklist.
2. If Gates 1–3 all passed: register the stitched CG video in the Bose pack
   (`derived-assets.json` + binding to `claim_bqcu2_step_aux_1/2`) as
   `internal_only: true`, `approved_by: null`, watermark
   "INTERNAL ONLY — TWIN RENDER", provider
   "local Blender 5.2.0 deterministic twin scene", with the verification
   JSON path. The license rule (0.2) keeps it off any external surface.
3. Update `docs/workorders/workorder-question-to-video-pipeline.md` routing
   table status: rigid-body row marked "POC8: <verdict>".

## Acceptance criteria

- A watchable deterministic video exists showing the 2.5 mm end seated in
  the LEFT earcup and the 3.5 mm end seated in the Mac's RIGHT-side jack.
- Every scene decision is claim-cited or listed as `INFERRED`.
- All gate verdicts (pass or fail) are recorded with evidence.
- Total external spend ≤ $10, itemized.
- Nothing from this POC is served externally or auto-approved.
