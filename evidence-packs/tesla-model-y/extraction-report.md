# Extraction report: Tesla Model Y (2025+ body), `prod_tesla_model_y`

- Work order: `evidence-packs/workorders/tesla-model-y.json` (`wo_extract_tesla_my_v1`), brief v2.
- Extractor: `evidence-pack-agent-v2`, extracted 2026-10-07. Every claim is `CANDIDATE`.
- Files: `claims.json` (213 claims), `gaps.json` (coverage for all 9 checklist items, 9 gaps).

## Summary

- **213 claims**: SPEC 81, STEP 60, WARNING 31, STATE 21, PART_LOCATION 10, LIMIT 8, COMPATIBILITY 2. Tiers: C0 83, C1 67, C2 12, C3 51.
- **All 336 quote bindings pass the literal-quote gate.** A stricter local check also confirmed every full quote, not only the first 60 characters the validator checks.
- **The official validator fails on one thing only: authority.** The 27 third-party claims use `authority: "THIRD_PARTY_MEASUREMENT"`, as the orchestrator instructed and as the vault manifest labels those sources. `validate.py` does not list that value in `ALLOWED_AUTHORITIES`. I did not edit `validate.py`, because it is outside this pack. I also did not relabel the claims as manufacturer claims, because that would misstate where they come from. A scratch copy of the validator that adds this one value passes with 0 errors (output below). **Action for the orchestrator:** add `THIRD_PARTY_MEASUREMENT` to `ALLOWED_AUTHORITIES`, or tell me which authority to use instead.
- **Over the count band:** 213 claims against a maximum of 170. Procedures alone account for 60 STEP claims, and procedures are never skipped. The trim tables also produce one claim per row per trim. Rows that are identical across trims are already merged into a single claim each. Please raise the band.
- **Three conflict pairs are recorded and left unresolved** (details below), including the required liftgate 8 ft vs 7.5 ft pair.

## Sources used

| source_id | What it is | Used for |
|---|---|---|
| `src_ty_manual_live_html` | Verbatim live owner's manual sections, software 2026.32 | Dimensions, Rear Trunk, Front Trunk storage, seats, Vehicle Loading |
| `src_ty_manual_pdf_2025_12` | Owner's manual PDF, Dec 2025, software 2025.44, 313 pp. It covers Standard and Premium 5-seat only | Second binding wherever the PDF agrees with the live text; frunk open/close and no-power hood steps; vehicle-label pages |
| `src_ty_spec_page` | tesla.com spec panels and shop pages as captured | Trim identity: seating, displays, wheels, parcel shelf, liner styles; spec-page height for the Premium conflict |
| `src_oeamtc_adac_autotest_2025` | ÖAMTC/ADAC Autotest, EU Maximum Range RWD, in German | Volumes, 68 cm load lip, flush floor, under-floor layout, payload |
| `src_12365auto_2025_practicality_test_utf8` | 12365auto practicality test, in Chinese (UTF-8 transcode) | Opening 1190 / 1140 mm, depth 1060 mm, floor-to-top 680 mm |
| `src_d1ev_2025_model_y_review` | d1ev review, in Chinese | Depth 108.5 cm, "same as legacy", frunk 117 L, power fold and raise |

`geometry/trunk-geometry.md` was used only as a map of where each number lives. No claim cites it.

Third-party quotes are kept in the original German or Chinese. The English meaning, the units, the measured vehicle and any ambiguity in the measuring point are in `object` and `extraction_notes`.

## Review these first

### Conflicts (recorded, not resolved)

1. **Liftgate maximum opening height** (`liftgate_max_opening_height`). Both claims carry a live and a PDF binding.
   - `claim_tmy_limit_liftgate_height_8ft`: the Dimensions page says about 8 ft (2.4 m), depending on wheel selection.
   - `claim_tmy_limit_liftgate_height_7_5ft`: the Rear Trunk page says about 7.5 ft (2.3 m), depending on suspension height or wheel selection.
2. **Premium overall height** (`overall_height_premium`).
   - `claim_tmy_ext_pre_height_live`: the live manual says 64.0 in.
   - `claim_tmy_ext_pre_height_pdf`: the PDF and tesla.com say 63.9 in.
   - All three sources say 1624 mm, so only the inch figure disagrees.
3. **Premium laden ground clearance** (`ground_clearance_laden_premium`).
   - `claim_tmy_ext_pre_gc_laden_live`: the live manual says 4.8 in / 122 mm.
   - `claim_tmy_ext_pre_gc_laden_pdf`: the PDF says 5.4 in / 138 mm.

Differences that are noted but not flagged as conflicts:

- **Trunk depth:** 12365auto measured 1060 mm and d1ev measured 108.5 cm. These are different measurers using undefined end points, and neither is an official source.
- **Frunk volume:** ADAC measured about 80 L and Tesla states 114–116 L. The measurement methods differ.
- **tesla.com "Cargo" headline:** the figures (74 / 74.8 / 76 cu ft) do not define what they measure (`claim_tmy_spec_cargo_headline`).

### C3 items (51)

- **31 WARNING claims.** These are every trunk, liftgate, frunk, seat-folding and cargo-loading WARNING or CAUTION in the two manual texts, plus the child-seat-lock warning. Two loading instructions without a WARNING/CAUTION label are included at C3 under the higher-tier rule: "Secure all cargo…" and "Distribute the weight…".
- **7 LIMIT claims:**
  - rear trunk: 88 lb lower compartment, 198 lb upper compartment
  - frunk: 110 lb or 65 lb, depending on the frunk variant
  - GVWR, which has no number in the vault
  - liftgate height: 8 ft and 7.5 ft (the conflict pair)
  - ADAC measured payload of 533 kg
- **7 STEP claims:** the 6 load-limit calculation steps and the child-seat-lock step.
- **6 STATE claims:**
  - liftgate obstruction stop
  - grasp-to-stop override
  - frunk open while driving
  - the two child-seat-lock behaviours

## Coverage by checklist item

| Checklist id | Claims | Notes |
|---|---|---|
| `exterior_dimensions` | 27 | Standard, Premium 5/7-seat and Performance, one claim per table row. Rows identical across trims (width ×3, wheelbase, rear overhang) are one claim each. Model Y L is excluded |
| `interior_dimensions` | 10 | Head, leg, shoulder and hip room per trim table. Standard's second-row shoulder room is 1386 mm; Premium 5 and Performance is 1351 mm |
| `cargo_volumes` | 25 | 16 manual volumes, 1 spec-page headline, 7 ADAC measurements (420 / 540 / 850 / 1380 / 105 / 80 L, plus 11 crates), 1 d1ev frunk figure (117 L) |
| `load_limits` | 12 | 7 LIMIT claims and the 6-step load-limit procedure. Two LIMIT claims (the liftgate-height pair) are listed under `liftgate_operation` instead |
| `trunk_linear_measurements` | 12 | All from third parties. Values are listed below |
| `liftgate_operation` | 42 | Procedures: open, stop/reverse, hands-free, adjust/save/reset height, close, parcel shelf (fold, unfold, remove), cargo-area access, frunk open/close, hood with no power. Plus parts, behaviours and the conflict pair |
| `rear_seat_folding` | 39 | Power side switch (fold, unfold, incremental, seated recline), front and rear touchscreen, trunk switch, center seat, pre-fold positioning, release straps (recline, fold, raise, center), 7-seat slide, child seat locks |
| `cargo_safety_warnings` | 32 | 31 WARNING claims and the obstruction-stop behaviour |
| `trim_identity` | 13 | Seating, displays, wheels, parcel shelf (included vs $135 accessory), floor-liner and well-liner styles, liner compatibility, two frunk variants, rear-trunk outlet, ADAC under-floor layout and parcel-shelf stowing |

### `trunk_linear_measurements` values

| claim_id | Value | Measured vehicle | Ambiguity |
|---|---|---|---|
| `claim_tmy_tp12365_opening_length` | 1190 mm ("开口长度") | 2025 Long Range AWD Launch Edition, China | Axis not defined by the source |
| `claim_tmy_tp12365_opening_width` | 1140 mm ("开口宽度") | same | Axis not defined by the source |
| `claim_tmy_tp12365_depth` | 1060 mm ("进深") | same | End points and seat state not stated |
| `claim_tmy_tp12365_floor_to_top` | 680 mm ("地台与顶部的垂直高度") | same | "顶部" (top) is not defined |
| `claim_tmy_tpd1ev_depth` | 108.5 cm ("纵深", "normal state") | 2025+ body, China; trim not stated (20-inch wheels) | End points not defined |
| `claim_tmy_tpd1ev_same_as_legacy` | Space "basically the same as the old model" | same | Qualitative only. Legacy numbers are not extracted |
| `claim_tmy_tpadac_load_lip_height` | 68 cm above the road | EU Maximum Range RWD, 255/40 R20 tyres | Load state not stated |
| `claim_tmy_tpadac_lip_floor_flush` | 0 (lip and floor on one level) | same | Qualitative |
| `claim_tmy_tpadac_head_clearance` | People up to about 1.95 m are clear of the open liftgate | same | Qualitative |
| `claim_tmy_tpadac_folded_floor_flat` | Nearly flat floor with seats folded | same | No step height given |
| `claim_tmy_tpd1ev_cushion_lengthened` | Rear cushion 15 mm longer than legacy | 2025+ body, China | Not stated whether measured |
| `claim_tmy_tp12365_test_vehicle` | Identifies the 12365auto test car | — | — |

## Not extracted, and why

- **Legacy 2020–24 Tesmanian measurements:** these are image-only and come from the wrong body. The work order forbids using them as 2025+ facts.
- **Collision Repair datum distances:** these exist only in an image capture, with no text source (`gap_tmy_collision_datum_1`).
- **AutoEdgeView and Car and Driver figures:** URL only, with no local file and low or unknown method.
- **Model Y L content:** excluded by the work order. This includes the 6-seater cargo-cover flip procedure and its caution.
- **Trailer cargo warnings, roof racks, charge-port release cable:** outside the trunk-fit scope.
- **Legacy-body video and URL-only videos:** no claims bound to them (`gap_tmy_videos_1`).

## Gaps (`gaps.json`)

None of the gaps waives a requirement. Every checklist item is covered by claims, and the gaps are recorded as findings.

| Gap | Kind | What is missing |
|---|---|---|
| `gap_tmy_official_trunk_linear_1` | SOURCE_MISSING | Tesla publishes no linear trunk dimensions for the 2025+ body |
| `gap_tmy_collision_datum_1` | SOURCE_MISSING | No text source for the Collision Repair datums |
| `gap_tmy_seat_mech_trim_1` | UNDERIVABLE | The manual says "If Equipped" for power-fold vs strap seats but never names the trims |
| `gap_tmy_frunk_variant_trim_1` | UNDERIVABLE | Which trims have which frunk variant |
| `gap_tmy_perf_spec_panel_1` | SOURCE_MISSING | The Performance spec panel was not captured |
| `gap_tmy_gvwr_value_1` | SOURCE_MISSING | No numeric GVWR or payload for any US trim |
| `gap_tmy_seatback_angle_1` | UNDERIVABLE | No second-row seatback angles |
| `gap_tmy_us_load_lip_1` | SOURCE_MISSING | No load-lip height for US trims |
| `gap_tmy_videos_1` | UNDERIVABLE | No usable 2025+ procedure video |

## Final validator output

Official validator, `.venv/bin/python3 evidence-packs/validate.py evidence-packs/tesla-model-y/claims.json`. The output is abridged: there are 27 FAIL lines, all of the same form.

```
--- Validating evidence-packs/tesla-model-y/claims.json ---
WARNING: work order: 213 claims > expected maximum 170 — facts may be split too thin
FAIL: claim_tmy_adac_vol_standard: invalid authority THIRD_PARTY_MEASUREMENT
... (27 FAIL lines total, all "invalid authority THIRD_PARTY_MEASUREMENT", one per third-party claim)
SUMMARY_JSON: {"cannot_judge": 0, "ceilings": {"C0": 83, "C1": 67, "C2": 12, "C3": 51}, "claims": 213, "errors": 27, "gaps_recorded": 9, "meaning_changed": 0, "product": "tesla-model-y", "quotes_verified": 336, "reviews_recorded": 0, "types": {"COMPATIBILITY": 2, "LIMIT": 8, "PART_LOCATION": 10, "SPEC": 81, "STATE": 21, "STEP": 60, "WARNING": 31}, "unverifiable_binary_source": 0, "unverifiable_no_local_file": 0, "verdicts_recorded": 0, "verification_status": null, "warnings": 1, "workorder_enforced": true}
Validation FAILED for evidence-packs/tesla-model-y/claims.json (27 errors)
```

Scratch copy of the validator with `THIRD_PARTY_MEASUREMENT` added to `ALLOWED_AUTHORITIES`. Nothing else is changed, and the copy lives outside the repo:

```
--- Validating evidence-packs/tesla-model-y/claims.json ---
WARNING: work order: 213 claims > expected maximum 170 — facts may be split too thin
SUMMARY_JSON: {... "claims": 213, "errors": 0, "gaps_recorded": 9, "quotes_verified": 336, "warnings": 1, "workorder_enforced": true}
Validation successful for evidence-packs/tesla-model-y/claims.json
```

## Extraction Telemetry

**(a) Validator runs to pass:** 1 run of the official validator, which fails only on authority, plus 1 run of the scratch copy, which passes. Before either run, a local strict checker compared every full normalized quote with the page text and found 0 misses on its first run.

**(b) Distinct validator failures, verbatim:**

- `FAIL: claim_tmy_<id>: invalid authority THIRD_PARTY_MEASUREMENT` (27 occurrences, one per third-party claim). This is still open, because fixing it needs a change to the validator or to the orchestrator's instruction.
- `WARNING: work order: 213 claims > expected maximum 170 — facts may be split too thin`. Also still open; the band needs to be raised.

**(c) Judgment calls the mechanical rules could not decide:**

1. **Authority vs validator.** The orchestrator's instruction and the manifest say `THIRD_PARTY_MEASUREMENT`, but the validator's enum does not allow it. I kept the truthful label and reported the failure instead of relabelling the claims as manufacturer claims.
2. **Rows identical across trims.** Width, wheelbase, rear overhang, leg and hip room, and frunk 4.1 cu ft each appear identically in several trim tables. I wrote one claim per row with all applicable trims listed, rather than three claims with the same quote. This avoids duplicate-quote warnings without stretching any number to a trim that does not state it.
3. **Alternative methods vs steps.** "Do one of the following" lists (open liftgate, close liftgate, open frunk) became one STEP claim with an `alternatives` array, not a fake sequence. Power-fold methods (side switch, front touchscreen, rear touchscreen, trunk switch) are separate one- or two-step procedures, so each can be shown on its own.
4. **Splitting one sentence into steps.** The parcel-shelf removal sentence has three clauses. I split it into steps 1–3 at the clause boundaries, quoting each verbatim, and added the stow sentence as step 4.
5. **Trim scope for seat methods.** The manual says "If Equipped" without naming trims, so the STEP claims carry an `equipment` condition and the trim mapping is a gap. The `specs.md` mapping is a compiler's inference and was not cited as Tesla's statement.
6. **Premium height 64.0 vs 63.9 in.** The mm values agree, so this may be rounding. It is still recorded as a CONFLICT, because the inch values differ and the rules say not to resolve conflicts.
7. **Tiers.** Load limits stated inside manual cautions are C3, even though their stated consequence is damage. Frunk closing and the no-power hood procedure are C2. Seat folding and liftgate steps are C1. Third-party dimensions are C0, except the ADAC payload (C3) and head clearance (C1).
8. **Unlabelled safety statements.** "Secure all cargo…", "Distribute the weight…" and the obstruction stop are not labelled WARNING or CAUTION, but are recorded at C3 under the higher-tier rule.
9. **"Cargo cover" vs "lower compartment cover".** The manual uses both terms. I treated them as the same panel because the p.33 illustration shows it, and noted that the text does not confirm it.
10. **Pre-fold "lift the bar" note.** It sits under Power Switches on the shared 5- and 7-seat page, but the bar is documented only for the 7-seat car. It is extracted as its own procedure, with the ambiguity stated.

**(d) Unverifiable bindings:** 0 quote bindings are unverifiable, because every binding cites a local PDF, markdown or HTML text. There are 13 diagram bindings (PDF pp. 25, 33, 35, 40, 41) with `bounding_box: null` and `annotation_status: "PENDING"`. Their page content was checked by rendering the pages, but no coordinates were assigned. 5 PART_LOCATION claims have `diagram_binding: null`, because no vault illustration shows the part: the exterior handle switch, the release straps (outboard and center), the 7-seat slide bar and the rear-trunk outlet.
