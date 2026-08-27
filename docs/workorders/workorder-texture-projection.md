# Work Order: Photo-Texture Projection onto the Mechanism Twin

**Date issued:** 2026-08-27
**For:** an autonomous agent with repository access (no prior conversation context assumed). Blender 5.2.0 LTS at `/Users/vbp/Applications/Blender.app`, headless only.
**Depends on:** `poc-3d-static-twin/twin/ready2jet-rigged.blend` (mechanism twin + dress pass), `poc-3d-static-twin/runs/tripo-probe-01/` (textured scan GLB — the photo-derived appearance source), POC 7 findings (`docs/pocs/poc7-vace-skin-findings.md` §recommendation)
**Question:** can projecting the scan's photo-derived textures onto the twin's rigid parts produce a fold video that is real-looking **by construction** — no generative step, so no invented parts, no pseudo-brand text, no repainted belly bar?
**Spend:** $0 external. All local.

---

## 0. Governing rules

1. **Appearance only, and only from the scan.** Twin part geometry, the
   rig, joints, actions, and evidence map are untouched. The only new data
   is baked texture maps whose pixels come from the Tripo scan (itself
   photo-derived). No hand-painted details, no procedural logos, no
   invented markings.
2. **Coverage honesty.** Where a twin part has no usable scan coverage
   (rear surfaces, occluded regions — the scan's own rear is inferred by
   Tripo), fall back to the existing dress-pass material and record the
   region in a coverage map. Disclosed fallback beats fabricated texture.
3. **Bleed is the enemy.** The Meshy pilot's tan-on-belly-bar bleed and
   POC 7's identity drift define the failure class. §3's identity QA
   checks part-boundary bleed explicitly.
4. **INTERNAL ONLY** (Tripo ancestry): watermark distributed GIFs/MP4s;
   `derived-assets.json` provenance; approval fields untouched.
5. Deterministic, scripted, committed; measure hours per stage.
6. **Stop-and-report:** any rule above; alignment error too large to
   project (§1.3); a stage exhausts its budget without its outcome.

## 1. Stage A — Alignment and coverage audit (budget: half a day)

1. Load twin and scan in one scene; apply the recorded Stage-S alignment
   transform (`twin/stage-s-report.md`) or re-derive it; refine with a
   scripted ICP-style fit if needed. Record the final transform + RMS
   surface distance.
2. **Per-part coverage map:** for each twin part, compute the fraction of
   its surface within a projection distance `d ≤ 15 mm` of the scan
   surface. Emit `twin/texture-projection/coverage.json` (part → fraction,
   mean distance).
3. Gate: if the parts that matter most (seat, canopy, frame tubes, handle
   grip, wheels) average < 60% coverage, stop and report with the numbers —
   projection would mostly show fallback and the approach needs rethink.

## 2. Stage B — UV and bake (budget: one day)

1. UV-unwrap each twin part (scripted smart-project is acceptable; islands
   per part, no shared atlases across parts — isolation prevents cross-part
   bleed by construction).
2. Bake from the scan to each part: base color required; roughness/normal
   optional if the scan's PBR maps are usable. Use selected-to-active
   baking with a per-part cage/extrusion tuned from Stage A distances;
   pixels beyond `d` fall back per rule 0.2 (bake a coverage mask alongside
   each map).
3. Blend baked texture with the dress-pass material via the coverage mask
   so fallback regions keep the current look; no visible hard seam at the
   mask edge (feather in the shader, not by inventing texture).
4. Save as `ready2jet-textured.blend` + `twin/texture-projection/maps/`
   (PNG, committed; keep total under ~150 MB — reduce resolution before
   reducing part count).

## 3. Stage C — Identity and quality QA (budget: half a day)

Scripted renders (all sides, open + folded + three mid-fold frames), then
check and record:

1. **Belly bar is black.** (The POC 7 drift case — now a literal pixel
   check on the belly-bar region.)
2. **No text anywhere except real product branding that the scan itself
   carries.** If the scan texture contains legible real Graco markings,
   note them (trademark handling is part of the open rights review; fine
   internally).
3. **No cross-part bleed:** tan grip pixels only on the grip; fabric
   texture not on tubes. Render part-isolation passes to verify.
4. **Boundary seams:** part boundaries acceptable at 1024px viewing.
5. Compare a matched frame against the scan turntable and against POC 7
   run 2: the deliverable should beat the schematic twin clearly and be
   free of every POC 7 identity defect. Include this three-way contact
   sheet in the report.

## 4. Stage D — Deliverables

1. Re-render with the textured twin: `open-turntable`, `fold-official-
   angle`, `fold-novel-rear-right` (1024px, dress-pass lighting, GIF via
   existing encoder), plus the five-pose contact sheet vs the official
   video.
2. Register the renders in
   `evidence-packs/graco-ready2jet-2212125/derived-assets.json` with
   provenance (twin hash → scan run id → bake scripts), label
   `TWIN_RENDER_PHOTO_TEXTURE`, internal-only.
3. `twin/texture-projection/report.md`: hours per stage, coverage table,
   QA results, the three-way comparison verdict, and open items.
4. Repo clean; tests/validators green; protected files untouched.

## 5. Stage E — Close the Tripo3D license check (budget: half a day; do
this even if earlier stages stop)

The license check has been the standing ship-blocker across five reports.
Close it: read Tripo3D's commercial/API terms and fal.ai's terms for the
`tripo3d/*` endpoints (official sources only; cite URLs and retrieval
dates). Answer specifically: (a) may generated meshes/renders be used
commercially by the paying API customer? (b) any attribution, resale, or
output-ownership constraints? (c) any restriction relevant to serving
derived renders in a product? Write
`docs/pocs/tripo3d-license-review.md` with quotes + citations and a
recommended disposition for the owner. The agent researches and recommends;
the owner decides. Until the owner records a decision, everything stays
internal-only.
