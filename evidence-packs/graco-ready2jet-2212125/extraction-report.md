# Extraction Report: Graco Ready2Jet (2212125)

## Overview
This report summarizes the candidate claims extracted from the Graco Ready2Jet `source-vault` artifacts (primarily the instruction manual `src_r2j_manual_v1`).

### Extracted Claims
- **LIMIT (3):** Maximum child weight (50 lb), maximum child height (45 in), and maximum storage basket weight (10 lb).
- **WARNING (4):** Unattended child hazard, harness requirement, brakes for loading hazard, and basket overload (tipping) hazard.
- **PART_LOCATION (3):** Belly bar, thumb switch, and handle lever.
- **STEP (13):** Complete fold procedure (7 steps), unfold procedure (4 steps), and fold tips (2 steps).
- **CARE (3):** Seat cleaning, frame cleaning, and wheel lubrication.

### Methodology Notes
- **Fabricated Visual Steps Removed:** The manual text for folding ends with squeezing the lever and checking for security. Previous iterations asserted a "Push stroller frame downward" step based on visual diagrams; this was removed to adhere strictly to the literal text. Future visual parsing can bind state transitions to this text.
- **Bounding Boxes:** Coordinates for part locations were set to `null` with `annotation_status: "PENDING"` to prevent hallucinated/estimated coordinates from entering the verified pipeline. These require measured annotation.
- **Strict Verbatim Quotes:** Quotes were modified to ensure they represent the exact, literal string from the source manual (e.g., the basket tipping hazard).

## Identified Gaps
1. **Missing Specifications:** General stroller specifications (such as stroller empty weight, folded dimensions, open dimensions) are not explicitly present in the provided instruction manual text. These must not be hallucinated and should be captured from a missing SPEC sheet if one becomes available.
2. **Missing Video Coverage:** Based on the manifest, the official fold video (`src_r2j_fold_video_v1`) has a known coverage gap and does not clearly show the thumb-switch actuation.
3. **Spin 360:** As noted in the manifest, 360 spin availability is unverified. 

## Validation Results
```text
Validation successful for graco-ready2jet-2212125/claims.json
--- Counts ---
Types:
  LIMIT: 3
  WARNING: 4
  PART_LOCATION: 3
  STEP: 13
  CARE: 3
Consequence Ceilings:
  C3: 7
  C1: 14
  C0: 5
```

## v2 Top-Up (2026-08-24)

Top-up pass by `evidence-pack-agent-v2` to bring the pack to the hardened
work-order contract (`evidence-packs/workorders/graco-ready2jet-2212125.json`).
The 26 v1 claims were left byte-identical (append-only; verified by snapshot
comparison during the merge). 53 new claims were appended, all extracted from
the manual (`src_r2j_manual_v1`) via pypdf text — the same extraction the
validator's quote gate uses — so every quote is verbatim page text.

### What was added (53 claims)
- **WARNING (21, all C3):** every remaining English warning bullet on pages
  4-5 (finger entrapment, strangulation, stairs/escalators, walking speed
  only, tipping via handle/canopy loads, hot liquids, basket not a carrier,
  no standing on basket, head toward footrest, not a toy, discontinue if
  damaged, caregiver assist, adult assembly, and the four car-seat warnings)
  plus the section warnings: zip tie (p10), belly bar not a restraint (p16),
  apply both brakes (p20), seat-adjustment clearance (p22).
- **STEP (22):** canopy (3, p19), brake (2, p20), recline (2, p22),
  rear-wheel attach (2, p14, C2), front-wheel attach (2, p15, C2), wheel
  removal (1, p36, C2), car-seat attach/remove (5, pp30-32, C3), belly bar
  (3, pp16-17), 5-point harness open/close (2, p23, C3).
- **LIMIT (2, C3):** cup holder 1 lb (p4); one child at a time (p4).
- **SPEC (1, C0):** assembly requires no tools ("No tools required.", p10) —
  the only spec-type fact literally stated in the manual text.
- **COMPATIBILITY (1, C3):** "COMPATIBLE WITH MOST GRACO® INFANT CAR SEATS"
  (p5) — generic statement, not a per-model chart.
- **PART_LOCATION (1, C3):** Click Connect mounts (p31 diagram,
  `bounding_box: null`, `annotation_status: PENDING`).
- **CARE (5):** periodic inspection (C1), sun/heat exposure (C0), drying
  after wet (C0), beach cleaning (C2), cup holder dishwasher-safe (C0).

### Gaps recorded (gaps.json, with full checklist coverage map)
1. **gap_specs_1 (SOURCE_MISSING):** no product weight, open/folded
   dimensions, box-contents enumeration, or warranty terms anywhere in the
   manual text (p10 parts list is diagram-only; p40 gives warranty contact
   channels only). Closes when gap-closure Task 1 lands
   `source-vault/graco-ready2jet-2212125/specs/specs.md`.
2. **gap_fold_visual_1 (UNDERIVABLE):** the fold-page text still ends at
   "squeeze handle lever" / "CHECK that the stroller is secure." — the
   frame-collapse motion is diagram-only and was again NOT invented as a step.
3. **gap_compat_chart_1 (SOURCE_MISSING):** no per-model compatibility chart
   in this vault; only the generic p5/p29 statement exists.

No waivers were needed: every floor (including SPEC >= 1) and every checklist
item is satisfied by claims; the gaps document what the sources cannot support.

### Reviewer attention first
- All 25 C3 WARNING claims and the C3 car-seat/harness STEP claims.
- `claim_r2j_spec_assembly_no_tools`: the SPEC floor is met by a real but
  minor fact; the intended specs are still missing (gap_specs_1).
- `claim_r2j_compat_graco_infant_car_seats`: p5 says "MOST", p29 omits it —
  same source, noted in extraction_notes rather than recorded as a conflict.

### Final validator output
```text
--- Validating evidence-packs/graco-ready2jet-2212125/claims.json ---
WARNING: same quote used by multiple claims ['claim_r2j_limit_max_weight', 'claim_r2j_limit_max_height'] (source src_r2j_manual_v1, page 4): 'USE OF THE STROLLER with a child weighing more than 50 lb (2'
SUMMARY_JSON: {"ceilings": {"C0": 9, "C1": 25, "C2": 6, "C3": 39}, "claims": 79, "errors": 0, "gaps_recorded": 3, "product": "graco-ready2jet-2212125", "quotes_verified": 80, "types": {"CARE": 8, "COMPATIBILITY": 1, "LIMIT": 5, "PART_LOCATION": 4, "SPEC": 1, "STEP": 35, "WARNING": 25}, "unverifiable_binary_source": 0, "unverifiable_no_local_file": 0, "warnings": 1, "workorder_enforced": true}
Validation successful for evidence-packs/graco-ready2jet-2212125/claims.json
```
(The single warning is a duplicate quote shared by two v1 claims — one manual
sentence states both the weight and height limits. v1 claims are frozen, so it
was left as-is.)

### Extraction Telemetry
- **(a) Validator runs to green:** 1 (passed on the first run after the
  top-up merge; the quote gate was pre-run manually against a per-page pypdf
  text dump of the manual before any claim was written).
- **(b) Distinct validator failures hit along the way:** none — zero FAIL
  lines across all runs.
- **(c) Judgment calls the mechanical rules could not decide:**
  - Counting "No tools required." (p10) as the SPEC-floor claim instead of
    waiving `type:SPEC`: it is a literal, genuine spec-type fact, but it does
    not cover the intent (weight/dimensions/warranty/box contents), so
    gap_specs_1 was recorded alongside it.
  - "ADULT ASSEMBLY REQUIRED." kept at C3 because the work order mandates C3
    for every manual safety warning, though it is not an in-use hazard.
  - Car-seat removal kept as step 5 of `attach_car_seat` to mirror the
    manual's own 4-G numbering rather than split into a separate procedure.
  - p24's "Use slide adjuster on shoulder, waist and crotch straps..." sits
    ambiguously between the 5-point and 3-point harness sequences on the
    page; it was not extracted rather than guessed into a procedure. The
    3-point-conversion sequence (pp24-26) and footrest/cup-holder steps were
    deliberately left out to stay within the 80-claim ceiling without
    splitting facts thin (79 total).
  - p23's "Falling Hazard: Always use the seat belt." was not re-extracted:
    near-duplicate of the v1 seat-belt warning (p4).
  - Periodic-inspection CARE assigned C1 (higher of C0/C1) per the
    assign-higher-when-unsure rule; beach cleaning C2 because it entails
    wheel-assembly removal.
- **(d) Unverifiable bindings:** 0. All 53 new claims (54 bindings) bind to
  the manual PDF and passed the literal quote gate; no image/URL-only
  bindings were added (the one new diagram_binding carries null coordinates,
  PENDING).

## Deferred-procedures top-up (2026-08-24)

Top-up run under the 2026-08-24 "procedures are never skippable" policy
(work-order max raised to 110 with revision note). The three procedures the
previous run deliberately omitted — plus the harness-height adjustment the
revision note names — are now extracted. 15 STEP claims appended (79 → 94);
no existing claim was modified or renumbered.

### What was added

- **Footrest adjustment** (§4-C, p21, C1): `adjust_footrest` steps 1-2
  (`claim_r2j_step_footrest_1..2`). Raise is lift-up; lower uses the buttons
  on the bottom of the footrest.
- **Parent cup holder attach/use** (§3-E, p18, C1): `attach_cup_holder`
  steps 1-3 (`claim_r2j_step_cup_holder_1..3`): align/press onto mount,
  pull-down security check, pull-up removal. Step 3 cross-references the
  existing 1 lb limit (`claim_r2j_limit_cup_holder_weight`), hot-liquids
  warning, and dishwasher CARE claim in its extraction_notes.
- **5-pt → 3-pt harness conversion** (pp24-26, C3): `convert_to_3pt_harness`
  steps 1-6 (`claim_r2j_step_harness_3pt_1..6`). Steps 1-4 perform the
  conversion (open buckle, slide connectors off, remove shoulder straps,
  attach waist straps to buckle); steps 5-6 are use of the converted 3-point
  harness — the manual numbers the section continuously, noted on step 5.
- **The formerly-skipped ambiguous p24 slide-adjuster step** (C3): extracted
  as `claim_r2j_step_harness_3` (secure_child_5pt step 3), NOT skipped. The
  ambiguity is stated precisely in its extraction_notes: p24 interleaves the
  tail of the 5-point section with the head of the 3-point section in pypdf
  reading order; the step was assigned to the 5-point sequence because the
  3-point sequence already has its own step 3 on p25, and because the step
  adjusts shoulder AND crotch straps, which are only in use in the 5-point
  configuration. Flagged for reviewer confirmation against the printed
  layout.
- **Shoulder-harness height adjustment** (p27, C3): `adjust_harness_height`
  steps 1-3 (`claim_r2j_step_harness_height_1..3`) — p24's step points to
  p27 and the revision note lists harness height among the deferred items.
  Step 3 ("Use slide adjuster at shoulder and waist... Repeat on other
  side.") is text on p27 but unnumbered in the manual; numbered 3 here to
  keep the sequence contiguous (noted on the claim).

### Diagram-only findings

- **Reverse conversion (3-pt → 5-pt): not documented.** Neither text nor
  the pp23-27 diagrams state a dedicated reconversion sequence; shoulder-
  strap reattachment appears only implicitly via the 5-point close step
  (p23) and the p27 loop insertion. Recorded as UNDERIVABLE gap
  `gap_harness_reconvert_1` — no convert-back procedure was invented.
- No other target procedure was diagram-only: footrest step 1, conversion
  step 4, and harness-height steps all carry "as shown" diagram references,
  but the actions themselves are stated in text (noted per claim).

### Coverage mapping

The checklist has no dedicated ids for these procedures, so the new
claim_ids were filed under the closest existing coverage entries:
footrest → `recline` (nearest seat-adjustment item); cup holder →
`specs_limits` (where its 1 lb limit already lives); all harness claims
(5-pt step 3, 3-pt conversion, harness height) → `safety_warnings`
(child-restraint content; note these are C3 STEP claims, not WARNINGs —
that entry's desc says "each a WARNING claim at C3", so this is an
acknowledged stretch pending a dedicated checklist id).

### Final validator output

```
--- Validating evidence-packs/graco-ready2jet-2212125/claims.json ---
WARNING: same quote used by multiple claims ['claim_r2j_limit_max_weight', 'claim_r2j_limit_max_height'] (source src_r2j_manual_v1, page 4): 'USE OF THE STROLLER with a child weighing more than 50 lb (2'
SUMMARY_JSON: {"ceilings": {"C0": 9, "C1": 30, "C2": 6, "C3": 49}, "claims": 94, "errors": 0, "gaps_recorded": 4, "product": "graco-ready2jet-2212125", "quotes_verified": 95, "reviews_recorded": 0, "types": {"CARE": 8, "COMPATIBILITY": 1, "LIMIT": 5, "PART_LOCATION": 4, "SPEC": 1, "STEP": 50, "WARNING": 25}, "unverifiable_binary_source": 0, "unverifiable_no_local_file": 0, "warnings": 1, "workorder_enforced": true}
Validation successful for evidence-packs/graco-ready2jet-2212125/claims.json
```

(The one warning is pre-existing from the v1 pack — a shared p4 quote
backing two LIMIT claims — not introduced by this top-up.)

### Extraction Telemetry (top-up)

- **(a) Validator runs to green:** 1. All quotes were copied from a pypdf
  dump of pp16-27 before writing, so the append passed on the first run.
- **(b) Validator failures hit, verbatim:** none.
- **(c) Judgment calls the mechanical rules could not decide:**
  - Assigning the ambiguous p24 slide-adjuster step to `secure_child_5pt`
    (step 3) rather than the 3-point sequence — rationale in that claim's
    extraction_notes; reviewer confirmation requested.
  - Treating 3-point steps 5-6 (p26) as part of `convert_to_3pt_harness`
    because the manual numbers the section continuously, rather than
    splitting a separate "use 3-pt harness" procedure.
  - Numbering the unnumbered p27 instruction as `adjust_harness_height`
    step 3 to satisfy contiguous numbering without dropping stated text.
  - Recording the absent reverse conversion as UNDERIVABLE
    (`gap_harness_reconvert_1`) instead of composing one from p23/p27 steps.
  - Coverage placement of the new claims under `recline`, `specs_limits`,
    and `safety_warnings` (no dedicated checklist ids exist).
  - Ceilings: footrest and cup holder C1 (comfort/accessory operation,
    matching existing C1 steps); everything harness-related C3 (child
    restraint), matching the existing `secure_child_5pt` steps.
- **(d) Unverifiable bindings:** 0. All 15 new claims bind to the manual
  PDF with page numbers and passed the literal quote gate.
