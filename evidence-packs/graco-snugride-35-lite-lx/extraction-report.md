# Extraction Report — Graco SnugRide Lite LX (`graco-snugride-35-lite-lx`)

**Work order:** `evidence-packs/workorders/graco-snugride-35-lite-lx.json` (wo_extract_snugride_v1)
**Extractor:** evidence-pack-agent-v2 · **Date:** 2026-08-24
**Subject:** `prod_graco_snugride_lite_lx` · **SKU:** 2110186
**Status of every claim:** CANDIDATE (nothing published)

## What was extracted — 90 claims

| Type | Count | Notes |
|---|---|---|
| STEP | 35 | 5 procedures: `install_base_lower_anchor` (10, §3-B), `install_base_seat_belt` (9, §3-C), `install_carrier_seat_belt` (6, §3-D baseless), `secure_child_in_car_seat` (7, §4-C), `remove_child` (3, §4-D). All C3. |
| COMPATIBILITY | 22 | All 15 stroller rows + all 6 base rows of the official APR 2026 chart, plus the manual's Click Connect-only requirement (p60). Ready2Jet row carries counterpart `prod_graco_ready2jet` and `applicability.revision` = "Ready2Jet models produced 2025 & later only". GoMax base row recorded as **compatible: false**. |
| SPEC | 11 | Model number, dimensions, weights, harness type, base features, install methods, FMVSS 213, aircraft certification, base recline (4), handle positions (4). |
| WARNING | 9 | Air bag, crash replacement, unattended child, no dual belt+LATCH install, bulky clothing, soft-surface suffocation, elevated-surface fall, non-Graco strollers, strings/cords. All C3. |
| LIMIT | 8 | 30 lb / 35 lb conflict pair, 4 lb min, 32 in max, 1 in head clearance, 12 lb body-support max, 7-year expiration, 80% base-on-seat minimum. |
| CARE | 3 | Seat pad/canopy machine wash (C2); buckle cleaning and harness surface-wash escalated to C3 (see judgment calls). |
| PART_LOCATION | 2 | Harness release lever, rear-facing belt path — both bound to the manual p14 features diagram with `bounding_box: null`, `annotation_status: "PENDING"`. |

Ceilings: **C3 = 85, C0 = 4, C2 = 1.** Nearly everything in this pack is child-restraint domain, as expected.

## The mandated conflict (reviewers: start here)

- **`claim_srl_limit_max_weight_current`** — 30 lb, bound to manual p12: "This child restraint must only be used with children weighing between 4-30 lb (1.8-13.6 kg) and 32” (81 cm) or less."
- **`claim_srl_limit_max_weight_legacy_img`** — 35 lb, bound to the official PDP gallery image `src_img_in_car_installed`, whose text overlay reads "Supports infants from 4-35 lb and up to 32 in" (transcribed; image bindings are mechanically unverifiable).

Both carry `extraction_notes: "CONFLICT: contradicts claim_<other>"`. Not resolved, per §4 of the work order. The legacy claim's `applicability.revision` marks it as legacy SnugRide 35 Lite LX (2106696-era) marketing.

## Other things a reviewer should look at first

1. **All 35 STEP claims and 9 WARNINGs are C3** — child restraint installation and harness use. Quotes are verbatim from the manual's numbered step blocks.
2. **Ready2Jet compatibility is revision-gated**: the chart says "(Only with models produced in 2025 & later)"; the catalog's pilot Ready2Jet (2212125) predates 2025. Flagged in that claim's notes.
3. **Chart footnote ambiguity** (`gap_chart_cell_marks_1`): the chart's per-cell marks are graphical; the Modes-row criteria "(Stroller frame & rear facing use mode only)" may attach to the GoMax column rather than the SnugRide column. Needs a human/vision look at the PDF.
4. **Carrier weight discrepancy inside one source**: PDP spec table says 7.5 lb, PDP marketing copy says 7.2 lb. Recorded the spec-table value with a note (not the two-official-sources conflict pattern — same source, so noted rather than paired).
5. **Aircraft certification found**: the vault's collection notes said FAA certification was unverified; manual p10 states it explicitly. `claim_srl_spec_aircraft_certified` closes that collection gap.
6. **Manual anomaly, p38**: the English manual's text layer contains what appears to be a leftover author/editor note ("I hope marketing doesn't point out the fact that the base is facing the wrong way here…"). Not extracted as a claim; flagged for curiosity/QA.

## Gaps recorded (gaps.json — 5, none waiving contract floors)

| gap_id | kind | Summary |
|---|---|---|
| gap_legacy_manual_1 | SOURCE_MISSING | Legacy 4-35 lb manual not in vault; 35 lb conflict side rests on an image binding only. |
| gap_harness_height_steps_1 | NOT_EXTRACTED | §4-A (12 harness-height actions) and §4-B (buckle position) deferred to stay within the 90-claim ceiling; harness_steps checklist covered by §4-C/§4-D. |
| gap_chart_cell_marks_1 | UNDERIVABLE | Chart per-cell marks/footnote attachment are graphical; row-level facts recorded, cell-level attachment needs visual review. |
| gap_video_transcripts_1 | SOURCE_MISSING | Official videos are URL-only; no claims bound to them. |
| gap_spanish_manual_1 | NOT_EXTRACTED | Spanish manual duplicates English content. |

## Extraction Telemetry

**(a) Validator runs to green: 1.** The pack passed with 0 errors on the first run.

**(b) Distinct validator failures hit, verbatim: none.** No FAIL lines were ever emitted. This was not luck: before writing any claim I dumped the manual and chart with pypdf (the validator's own extractor) and composed every quote by joining the extracted lines with single spaces, and pre-verified the trickiest chart-row quotes against a reimplementation of the validator's `normalize()`. The one warning on the green run (retained deliberately):

```
WARNING: same quote used by multiple claims ['claim_srl_compat_stroller_duoglider', 'claim_srl_compat_stroller_ready2grow_20', 'claim_srl_compat_stroller_ready2grow_lx_20'] (source src_compatibility_chart_apr2026, page 1): '+Can only be used with the rear seat'
```
That is the chart's single criteria-key footnote legitimately cited by the three rows it marks; deduplicating it would lose fidelity.

**(c) Judgment calls the mechanical rules could not decide:**
1. **Quote construction against pypdf's text layer.** The manual's two-column layout extracts with hyphenated line breaks ("Rear-\nFacing" → "Rear- Facing") and interleaved repeated blocks across pages. Verbatim-under-normalization required preserving those artifacts (e.g. "DO NOT SUBMERGE THE BUCKLE STRAP ." keeps the extractor's stray space). A quote gate keyed to raw layout text makes "verbatim" mean "verbatim in the extraction," which a human transcribing from the rendered page would fail.
2. **Chart column semantics.** Deciding that "✓ -" rows (Premier Merge, Outpace LX) mean compatible-for-SnugRide, and that the GoMax **base** row's "-" means incompatible, required reading the two-column table structure; the text layer alone doesn't say which mark belongs to which column. Recorded row-level with notes + `gap_chart_cell_marks_1`.
3. **Consequence escalation.** Buckle cleaning and harness cleaning are "care" (C2 by table) but directly affect restraint function — escalated to C3 with notes, per the "when unsure, higher tier" rule. Same for harness-type, base, install-method, aircraft SPEC claims and the carry-handle rule.
4. **Scope trimming to the 90 ceiling.** With 3 install procedures fully extracted, including §4-A/§4-B step-by-step would have pushed the pack to ~105 claims ("facts split too thin"). Deferred them via an explicit NOT_EXTRACTED gap rather than silently or via renumbered partial procedures (which would have violated the contiguous-numbering spirit).
5. **Subject ID mismatch.** The vault manifest says `prod_graco_snugride_35_lite_lx` but the work order (and catalog.json) say `prod_graco_snugride_lite_lx`; the work order governs `subject`, so the latter is used throughout.
6. **The 35 lb conflict binding.** Transcribed the gallery image's overlay text as the quote knowing the validator cannot check image text — the honest choice was a `region` note, an unverifiability note on the claim, and `gap_legacy_manual_1`.

**(d) Unverifiable-binding counts:** 1 binding on an image source (`claim_srl_limit_max_weight_legacy_img` → `src_img_in_car_installed`), reported by the validator as `unverifiable_binary_source: 1`. 0 bindings to sources with no local file. All other 99 quotes mechanically verified.

## Final validator output

```
--- Validating evidence-packs/graco-snugride-35-lite-lx/claims.json ---
WARNING: same quote used by multiple claims ['claim_srl_compat_stroller_duoglider', 'claim_srl_compat_stroller_ready2grow_20', 'claim_srl_compat_stroller_ready2grow_lx_20'] (source src_compatibility_chart_apr2026, page 1): '+Can only be used with the rear seat'
SUMMARY_JSON: {"ceilings": {"C0": 4, "C2": 1, "C3": 85}, "claims": 90, "errors": 0, "gaps_recorded": 5, "product": "graco-snugride-35-lite-lx", "quotes_verified": 99, "types": {"CARE": 3, "COMPATIBILITY": 22, "LIMIT": 8, "PART_LOCATION": 2, "SPEC": 11, "STEP": 35, "WARNING": 9}, "unverifiable_binary_source": 1, "unverifiable_no_local_file": 0, "warnings": 1, "workorder_enforced": true}
Validation successful for evidence-packs/graco-snugride-35-lite-lx/claims.json
```

## Harness-height top-up (2026-08-24)

The project owner rejected `gap_harness_height_steps_1` under the 2026-08-24
"procedures are never skippable" policy (the work order's `expected_total.max`
was raised to 120 with a revision note). This pass appends 18 claims (90 → 108),
touching nothing in the original 90:

- **`adjust_harness_to_fit_child` (§4-A, pages 46–52): 12 STEP claims**,
  `claim_srl_step_harnessfit_1` … `_12`, all C3. Covers loosening/unbuckling,
  child placement, the two harness-height checks, and the full re-threading
  through the splitter plate, including the smaller-baby (upper loops) and
  larger-baby (lower loops) slot/loop selection steps.
- **`adjust_buckle_to_fit_child` (§4-B, pages 53–54): 4 STEP claims**,
  `claim_srl_step_bucklefit_1` … `_4`, all C3. Step 2's quote preserves the
  manual's typo "an shell" verbatim from the pypdf text layer.
- **`shorten_buckle_low_birth_weight` (page 54): 1 STEP claim**,
  `claim_srl_step_shortenbuckle_1` — the un-numbered low-birth-weight
  (minimum 4 lb / 1.8 kg) crotch-slot sub-procedure printed inside §4-B,
  recorded as its own single-step procedure to keep §4-B numbering contiguous.
- **1 LIMIT claim**, `claim_srl_limit_harness_strap_height` (C3): harness
  straps must be at or just below the child's shoulders (the §4-A slot-position
  rule). The other associated safeguards were already in the pack and were NOT
  duplicated: head clearance (`claim_srl_limit_head_clearance`) and the
  bulky-clothing warning (`claim_srl_warning_bulky_clothing`); the new step
  claims cross-reference them in `extraction_notes`.

`gaps.json`: removed `gap_harness_height_steps_1`; the 18 new claim_ids were
appended to the `harness_steps` coverage entry (now 30 ids). Reviewer
attention: all 18 new claims are C3; the conditional steps 11/12 and the
un-numbered shorten-buckle sub-procedure carry stated ambiguities.

### Extraction Telemetry (top-up)

**(a) Validator runs to green: 1.** 0 errors on the first run after the append.

**(b) Distinct validator failures hit, verbatim: none.** As in the original
pass, all pages (44–59) were dumped with pypdf first and every quote composed
from that extraction, joining lines with single spaces and preserving
artifacts ("an shell", curly apostrophes, "1” (2.5 cm)").

**(c) Judgment calls the mechanical rules could not decide:**
1. **§4-A steps 11/12 are conditional alternatives**, not sequential actions
   (smaller vs larger baby); extracted both with the manual's own numbering to
   keep the procedure contiguous, ambiguity stated in `extraction_notes` on
   both — per the policy, extracted rather than skipped.
2. **The shorten-buckle instruction is un-numbered.** Folding it into §4-B as
   a step 5 would fabricate numbering; modeled as a separate one-step
   procedure with the ambiguity noted.
3. **§4-A step 7 restates an existing LIMIT** (head clearance) and step 6
   embeds the new harness-height LIMIT; kept the manual's numbered actions as
   STEPs and cross-referenced the LIMIT claims instead of dropping either.
4. **pypdf repeats §4-B steps 3–4 on page 55** (layout artifact bleeding into
   the §4-C spread); cited page 54 where the steps belong, noted on both claims.
5. **Quote-span differentiation**: the harness-height LIMIT quotes only the
   rule sentence while STEP 6 quotes the full numbered block, so the validator's
   duplicate-quote heuristic stays quiet without weakening either binding.

**(d) Unverifiable-binding counts: 0 new.** All 18 new bindings are to
`src_snugride_manual_en_v1` pages and were mechanically verified
(`quotes_verified` rose 99 → 117). Pack-wide counts unchanged otherwise:
`unverifiable_binary_source: 1`, `unverifiable_no_local_file: 0`.

### Final validator output (after top-up)

```
--- Validating evidence-packs/graco-snugride-35-lite-lx/claims.json ---
WARNING: same quote used by multiple claims ['claim_srl_compat_stroller_duoglider', 'claim_srl_compat_stroller_ready2grow_20', 'claim_srl_compat_stroller_ready2grow_lx_20'] (source src_compatibility_chart_apr2026, page 1): '+Can only be used with the rear seat'
SUMMARY_JSON: {"ceilings": {"C0": 4, "C2": 1, "C3": 103}, "claims": 108, "errors": 0, "gaps_recorded": 4, "product": "graco-snugride-35-lite-lx", "quotes_verified": 117, "reviews_recorded": 2, "types": {"CARE": 3, "COMPATIBILITY": 22, "LIMIT": 9, "PART_LOCATION": 2, "SPEC": 11, "STEP": 52, "WARNING": 9}, "unverifiable_binary_source": 1, "unverifiable_no_local_file": 0, "warnings": 1, "workorder_enforced": true}
Validation successful for evidence-packs/graco-snugride-35-lite-lx/claims.json
```
(The single warning is the pre-existing compatibility-chart footnote share,
unchanged by this top-up.)
