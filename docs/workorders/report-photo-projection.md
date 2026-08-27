# Photo-Projection Catalog Execution Report

**Work order:** `docs/workorders/workorder-photo-projection-catalog.md`

**Executed:** 2026-08-27

**Toolchain:** local Blender 5.2.0 LTS, headless

**External spend:** $0

**Distribution:** **INTERNAL ONLY — MANUFACTURER IMAGERY — DO NOT SHIP**

## Executive result

All five lanes were executed in the required order and have explicit terminal outcomes. Three new photo-derived assets were registered: one Levoit turntable and separate closed/open MacBook turntables. Ready2Jet stopped at the binding camera-match gate, Bose retained its labeled Tripo interim asset after the curved parametric attempt failed, and SnugRide received the expected audit skip.

The hoped-for Ready2Jet headline deliverable was **not** produced. Every eligible exact-product/person-free source missed the required silhouette IoU of 0.75. Under §0.7, producing a projected fold anyway would have violated the work order. The mechanism rig, joint evidence, and action specification remain byte-for-byte unchanged; the existing measured dress-pass fold remains the honest fallback.

All appearance pixels in the three new assets come from hash-verified official vault imagery. Derived alpha masks control coverage but do not replace source RGB. Uncovered areas use neutral deterministic materials. No new asset has Tripo texture ancestry, all rendered frames carry the required visible watermark, and `approved_by` remains `null`.

## Lane outcomes

| Lane | Product | Terminal outcome | Logged hours | Spend |
|---|---|---|---:|---:|
| 1 | Graco Ready2Jet | `SKIPPED_CAMERA_MATCH_GATE`; no projection or new asset | 0.4 | $0 |
| 2 | Levoit Core 300S | Registered `derived_levoit_levoit_turntable_20260827` | 0.2 | $0 |
| 3 | Apple MacBook Air 13-inch M3 | Registered closed and open turntables | 0.1 | $0 |
| 4 | Bose QC Ultra | `SKIPPED_PROJECTED_TWIN_RETAIN_TRIPO_INTERIM` | 0.0 | $0 |
| 5 | Graco SnugRide 35 Lite LX | `AUDIT_SKIP_NO_TWIN_SERVE_OFFICIAL_MEDIA` | 0.0 | $0 |

Hours are agent wall-clock/active execution measurements rounded to the nearest 0.1 hour. Lane 2 includes a final-validation correction after the ordered lane pass: the control panel was moved from 99% to the exact published overall height, then its scene, gates, renders, hashes, and registry were rebuilt. The detailed, sequential timestamps and this rework interval are in each lane's `hours.json`.

## Camera-match gate

Every eligible candidate was measured before projection. Only rows at or above 0.75 were allowed to contribute pixels; failed rows were not projected. Full camera grids, raw masks, final unmodified Blender masks, overlays, and parameters are retained under each lane's `camera-gates/` directory.

| Product / state | Official source | Final silhouette IoU | Verdict |
|---|---|---:|---|
| Ready2Jet | front three-quarter | 0.657560 | FAIL — lane stopped |
| Ready2Jet | side profile | 0.256960 | FAIL — lane stopped |
| Ready2Jet | official video title at 0 ms | 0.489569 | FAIL — lane stopped |
| Levoit | elevated three-quarter | 0.963177 | PASS — projected |
| Levoit | top panel | 0.862217 | PASS — projected only to top parts |
| MacBook closed | store closed top | 0.951498 | PASS — projected to lid |
| MacBook closed | left profile | 0.487876 | FAIL — not projected |
| MacBook closed | right profile | 0.542522 | FAIL — not projected |
| MacBook open | store Midnight front | 0.853629 | PASS — projected to display inset |
| MacBook open | newsroom keyboard/deck | 0.749616 | FAIL — not projected |
| Bose | front | 0.619714 | FAIL |
| Bose | three-quarter | 0.526289 | FAIL |
| Bose | side | 0.772118 | PASS, but insufficient alone |

The MacBook keyboard source missed by 0.000384. The threshold was enforced literally: no keys, legends, or deck detail were modeled, painted, or projected.

## Lane 1 — Graco Ready2Jet

The exact-product/person-free audit excluded the unregistered `heldout-05-front-3q.png`, person-containing fold sequence/demonstration frames, and a top-three-quarter pavement image whose boundary failed no-invention mask QA. The three remaining candidates all failed the camera gate because the measured mechanism twin's canopy, seat, undercarriage, wheels, and recline silhouette materially differ from the photographed stroller.

Section 0.7 therefore stopped the lane before projection. No derived scene, fold render, contact sheet, turntable, registry, or proposed media binding was created. The terminal record is `poc-3d-static-twin/photo-projection/ready2jet/verdict.json`. Protected hashes prove the stroller rig and evidence files were untouched.

## Lane 2 — Levoit Core 300S

The deterministic stacked-cylinder/control-panel geometry uses `claim_c300s_spec_dimensions`: 8.7 × 8.7 × 14.2 in (0.22098 × 0.22098 × 0.36068 m). The official three-quarter image supplies the camera-facing side appearance; the official top image is isolated to `TopRim` and `ControlPanel`. No cylindrical texture repeat is used. The unobserved rear arc stays neutral.

Registered asset: `derived_levoit_levoit_turntable_20260827`

GIF: `poc-3d-static-twin/photo-projection/levoit/levoit-turntable-internal-only.gif`

Geometry: `poc-3d-static-twin/photo-projection/levoit/levoit-photo-projected.blend`

QA: `poc-3d-static-twin/photo-projection/levoit/levoit-turntable-qa-contact-sheet.png`

## Lane 3 — Apple MacBook Air 13-inch M3

The closed deterministic slab is exact to `claim_mba_spec_height`, `claim_mba_spec_depth`, and `claim_mba_spec_width`: 0.0113 × 0.215 × 0.3041 m. The closed lid carries only the official store top image. Failed profile sources do not contribute pixels.

The optional open pose is supported by the passing official store image; its 75-degree lid angle and display inset are labeled inferred. The display wallpaper is projected official imagery. Because the keyboard/deck source failed the hard gate, the deck remains neutral and contains no invented keys or text.

Registered assets:

- `derived_macbook_closed_macbook_closed_turntable_20260827` — `poc-3d-static-twin/photo-projection/macbook/closed/macbook-closed-turntable-internal-only.gif`
- `derived_macbook_open_macbook_open_turntable_20260827` — `poc-3d-static-twin/photo-projection/macbook/open/macbook-open-turntable-internal-only.gif`

The older MacBook Tripo artifact remains in the registry for audit history, but it is superseded by the closed photo-projected asset and is not proposed for app serving.

## Lane 4 — Bose QC Ultra

The minimal deterministic attempt used the published 1.772 × 6.299 × 8.071 in dimensions cited through `claim_bqcu2_spec_headphone_weight_1`, mapped to the product's wearing orientation. Only the side silhouette passed. The identity-bearing front and three-quarter curved geometry failed, so the side alone could not justify a degraded projected twin.

No projected scene or render was created. Existing asset `derived_bose_tripo_h31_turntable_20260827` remains the interim internal visual and is now explicitly labeled with `tripo_ancestry: true`, `worst_axis_scale_error_percent: 147.0`, and its open Tripo license review.

## Lane 5 — Graco SnugRide 35 Lite LX

The audit inventoried all 12 registered official images: three are person-free, only one is a clean distinct semantic view, and none provides a person-free side or rear. The only useful side view contains a human arm and hand and is barred by §0.4. One front-three-quarter view cannot dimension-ground the organic shell, canopy, handle pivots, base, harness, and infant-support volumes.

No geometry or derived asset was created. The recorded disposition is to serve exact official imagery through the existing media bindings after owner approval.

## Coverage and fallback

Coverage is full renderable-mesh surface area, including unseen caps and rear surfaces. It is intentionally conservative.

| Asset | Official-photo coverage | Neutral fallback | Disclosure |
|---|---:|---:|---|
| Levoit turntable | 0.273002 | 0.726998 | Front/top projected; rear arc and unseen areas neutral |
| MacBook closed | 0.239267 | 0.760733 | Lid projected; sides/underside neutral |
| MacBook open | 0.085678 | 0.914322 | Display projected; deck/body/rear neutral |

Ready2Jet, Bose, and SnugRide have no new projected asset, so coverage is not applicable rather than silently reported as zero.

## Rights review and answer-app disposition

Owner review is still required before any new binding or shipment. No media bindings were modified and every derived asset has `approved_by: null`.

- **Levoit and MacBook:** review manufacturer-imagery reuse. Their new appearance chain has no Tripo ancestry.
- **Bose:** the retained interim remains subject to the separate open Tripo3D license review and the disclosed scale error.
- **Ready2Jet:** continue serving only the existing measured dress-pass fold visual; do not label it photo-projected.
- **SnugRide:** serve official source imagery via existing proposed bindings after approval; no twin this round.
- **MacBook historical artifact:** the old Tripo registry entry is retained only for provenance/audit history, not as the proposed visual.

After approval, the answer app can serve the new Levoit turntable, the MacBook closed turntable as the primary visual, the MacBook open turntable as supporting media with its neutral-deck disclosure, the labeled Bose interim, exact SnugRide official imagery, and the existing Ready2Jet measured dress-pass asset.

## Validation

The fail-closed validation result is `poc-3d-static-twin/photo-projection/validation.json` and reports five terminal lane outcomes, three registered new assets, protected-file integrity, visible watermarks, and $0 external spend. The Blender-side result is `poc-3d-static-twin/photo-projection/validation-blends.json`.

Final checks:

- photo-projection output validator: PASS
- Blender dimensions/projection metadata validator: PASS (Blender 5.2.0 LTS)
- vault hash validator: PASS (82 hashed files)
- media-binding validator: PASS (26 bindings)
- existing catalog-scan validator: PASS
- LLD documentation sync: PASS
- repository test suite: PASS (53 tests)
