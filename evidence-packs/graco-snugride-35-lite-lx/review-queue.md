# Review Queue — graco-snugride-35-lite-lx

Verification status: `COMPLETE`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.

## 1. MEANING_CHANGED alarms (89)

### claim_srl_care_buckle

- Claim: `claim_srl_care_buckle`
- Tier: `C3`
- Type/predicate: `CARE` / `buckle_cleaning`

Object

```json
{
  "instructions": [
    "place in a cup of warm water and gently agitate",
    "press the red button several times while in the water",
    "air dry",
    "repeat until it fastens with a click"
  ],
  "method": "agitate_in_warm_water",
  "restrictions": [
    "do not submerge the buckle strap",
    "no soaps, household detergents, or lubricants"
  ]
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
To clean, place in a cup of warm water and gently agitate the buckle. Press the red button several times while in the water.
```

Verifier: `MEANING_CHANGED` — Translation adds 'air dry' and 'repeat until it fastens with a click', which are not in the quote; also adds restrictions ('do not submerge the buckle strap', 'no soaps...') not mentioned; alters method by implying a multi-step process beyond the quote's scope.

Quote — binding 1, source `src_snugride_manual_en_v1`

```text
DO NOT SUBMERGE THE BUCKLE STRAP . DO NOT USE SOAPS, HOUSEHOLD DETERGENTS or LUBRICANTS.
```

Verifier: `MEANING_CHANGED` — The translation adds specific cleaning instructions (e.g., 'place in a cup of warm water', 'press the red button', 'repeat until it fastens with a click') not present in the original quote, which only states prohibitions. This constitutes an unauthorized addition of procedural detail, altering the meaning.

Extractor notes: Assigned C3 (higher of C2/C3): buckle cleaning directly affects harness latching; manual pairs it with a latching-failure warning on page 78.

### claim_srl_care_harness

- Claim: `claim_srl_care_harness`
- Tier: `C3`
- Type/predicate: `CARE` / `harness_and_lower_anchor_strap_cleaning`

Object

```json
{
  "instructions": [
    "mild soap and damp cloth"
  ],
  "method": "surface_wash_only",
  "restrictions": [
    "do not immerse harness straps or lower anchor attachment strap in water — may weaken straps"
  ]
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Surface wash only with mild soap and damp cloth. DO NOT IMMERSE THE HARNESS STRAPS or LOWER ANCHOR ATTACHMENT STRAP IN WATER. Doing so may weaken the straps.
```

Verifier: `MEANING_CHANGED` — The translation merges 'harness straps' and 'lower anchor attachment strap' into a single object 'harness_and_lower_anchor_strap_cleaning', implying they are a single unit or subject to identical care rules, whereas the original quote treats them as separate items with distinct restrictions. Also, the translation drops the causal warning 'Doing so may weaken the straps' as a separate consequence, embedding it as part of the restriction clause, which alters the emphasis and structure of the warning.

Extractor notes: Assigned C3 (higher of C2/C3): improper harness cleaning can weaken restraint straps.

### claim_srl_compat_base_gomax

- Claim: `claim_srl_compat_base_gomax`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `incompatible_with_gomax_base`

Object

```json
{
  "compatible": false,
  "counterpart": "GoMax Infant Car Seat Base",
  "counterpart_name": "GoMax Infant Car Seat Base",
  "counterpart_type": "infant_car_seat_base",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
GoMax Infant Car Seat Base - ✓
```

Verifier: `MEANING_CHANGED` — The quote simply states 'GoMax Infant Car Seat Base - ✓', implying compatibility or approval, while the translation falsely asserts 'incompatible_with_gomax_base', directly contradicting the original meaning.

Extractor notes: Chart marks '-' in the SnugRide Infant Car Seats column for this base: NOT compatible. From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_base_graco_premier

- Claim: `claim_srl_compat_base_graco_premier`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_graco_premier_base`

Object

```json
{
  "compatible": true,
  "counterpart": "Graco Premier Infant Car Seat Bases",
  "counterpart_name": "Graco Premier Infant Car Seat Bases",
  "counterpart_type": "infant_car_seat_base",
  "qualifier": "Graco Premier car seats are sold with bases that are not sold separately (criteria key *)",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Graco Premier Infant Car Seat Bases* ✓
```

Verifier: `MEANING_CHANGED` — The translation adds the qualifier that 'Graco Premier car seats are sold with bases that are not sold separately (criteria key *)', which is not stated in the exact quote and introduces a new condition about sales packaging not present in the source.

Quote — binding 1, source `src_compatibility_chart_apr2026`

```text
*Graco® Premier car seats are sold with bases that are not sold separately.
```

Verifier: `MEANING_CHANGED` — The translation adds 'compatible_with_graco_premier_base' and implies functional compatibility, while the quote only states that bases are included with car seats and not sold separately — no claim of compatibility or click-in functionality is made.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_base_snuglock_load_leg

- Claim: `claim_srl_compat_base_snuglock_load_leg`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_snuglock_load_leg_base`

Object

```json
{
  "compatible": true,
  "counterpart": "SnugLock Infant Car Seat Base ft. Load Leg Technology",
  "counterpart_name": "SnugLock Infant Car Seat Base ft. Load Leg Technology",
  "counterpart_type": "infant_car_seat_base",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
SnugLock® Infant Car Seat Base ft. Load Leg Technology ✓
```

Verifier: `MEANING_CHANGED` — The translation adds 'carrier clicks into stay-in-car base' and 'compatible_with_snuglock_load_leg_base' which are not stated in the quote; the quote only names the product and includes a checkmark, implying a feature, not compatibility or installation behavior.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_base_snugride_lite

- Claim: `claim_srl_compat_base_snugride_lite`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_snugride_lite_base`

Object

```json
{
  "compatible": true,
  "counterpart": "SnugRide Lite Infant Car Seat Base",
  "counterpart_name": "SnugRide Lite Infant Car Seat Base",
  "counterpart_type": "infant_car_seat_base",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
SnugRide® Lite Infant Car Seat Base ✓
```

Verifier: `MEANING_CHANGED` — The quote only names the product 'SnugRide® Lite Infant Car Seat Base' without stating any compatibility or functional relationship; the translation adds unmentioned claims about 'carrier clicks into stay-in-car base' and 'compatible_with_snugride_lite_base', altering meaning.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_base_snugride_snugfit

- Claim: `claim_srl_compat_base_snugride_snugfit`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_snugride_snugfit_base`

Object

```json
{
  "compatible": true,
  "counterpart": "SnugRide SnugFit Infant Car Seat Base",
  "counterpart_name": "SnugRide SnugFit Infant Car Seat Base",
  "counterpart_type": "infant_car_seat_base",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
SnugRide® SnugFit Infant Car Seat Base ✓
```

Verifier: `MEANING_CHANGED` — The quote only states the product name 'SnugRide® SnugFit Infant Car Seat Base' with a checkmark, implying availability or inclusion, but the translation adds specific functional claims (e.g., 'carrier clicks into stay-in-car base') and a compatibility predicate not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_base_snugride_snuglock

- Claim: `claim_srl_compat_base_snugride_snuglock`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_snugride_snuglock_base`

Object

```json
{
  "compatible": true,
  "counterpart": "SnugRide SnugLock Infant Car Seat Base",
  "counterpart_name": "SnugRide SnugLock Infant Car Seat Base",
  "counterpart_type": "infant_car_seat_base",
  "relationship": "carrier clicks into stay-in-car base"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
SnugRide® SnugLock® Infant Car Seat Base ✓
```

Verifier: `MEANING_CHANGED` — The quote merely names a product ('SnugRide® SnugLock® Infant Car Seat Base') with a checkmark, implying availability or inclusion, while the translation falsely asserts a compatibility relationship ('carrier clicks into stay-in-car base') and invents functional behavior not stated in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_click_connect_requirement

- Claim: `claim_srl_compat_click_connect_requirement`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `stroller_system_requirement`

Object

```json
{
  "compatible": true,
  "counterpart": "Graco Click Connect travel system strollers",
  "counterpart_type": "stroller_system",
  "relationship": "carrier may only be used with strollers in the Graco Click Connect travel system",
  "restriction": "Never use with any other manufacturer's strollers."
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
USE ONLY WITH STROLLERS THAT ARE PART OF THE GRACO CLICK CONNECT TRAVEL SYSTEM.
```

Verifier: `MEANING_CHANGED` — The translation adds a restriction not in the quote: 'Never use with any other manufacturer's strollers,' which introduces a new prohibition not stated in the original.

Extractor notes: None recorded.

### claim_srl_compat_stroller_duoglider

- Claim: `claim_srl_compat_stroller_duoglider`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_duoglider`

Object

```json
{
  "compatible": true,
  "counterpart": "DuoGlider",
  "counterpart_name": "DuoGlider",
  "counterpart_type": "stroller",
  "qualifier": "Can only be used with the rear seat (criteria key +)",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
DuoGlider ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote 'DuoGlider ✓ ✓' is ambiguous and minimal, offering no information about compatibility, seat position, travel system function, or counterpart type; the translation invents specific technical details not present in the source.

Quote — binding 1, source `src_compatibility_chart_apr2026`

```text
+Can only be used with the rear seat
```

Verifier: `MEANING_CHANGED` — The translation adds 'infant car seat clicks into stroller (travel system)' and specifies 'DuoGlider' as the counterpart, neither of which is stated in the exact quote; it also misrepresents the condition as a compatibility predicate rather than a usage restriction.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_fastaction_fold_jogger

- Claim: `claim_srl_compat_stroller_fastaction_fold_jogger`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_fastaction_fold_jogger`

Object

```json
{
  "compatible": true,
  "counterpart": "FastAction Fold Jogger",
  "counterpart_name": "FastAction Fold Jogger",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
FastAction Fold Jogger ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote only states 'FastAction Fold Jogger ✓ ✓' with no mention of compatibility, infant car seats, or travel systems; the translation invents a detailed compatibility claim not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_fastaction_jogger_lx

- Claim: `claim_srl_compat_stroller_fastaction_jogger_lx`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_fastaction_jogger_lx`

Object

```json
{
  "compatible": true,
  "counterpart": "FastAction Jogger LX",
  "counterpart_name": "FastAction Jogger LX",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
FastAction Jogger LX ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote only states 'FastAction Jogger LX ✓ ✓' with no mention of compatibility, infant car seats, travel systems, or stroller type — the translation invents specific functional relationships and object attributes not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_fastaction_se_20

- Claim: `claim_srl_compat_stroller_fastaction_se_20`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_fastaction_se_20`

Object

```json
{
  "compatible": true,
  "counterpart": "FastAction SE 2.0",
  "counterpart_name": "FastAction SE 2.0",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
FastAction SE 2.0 ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote merely states 'FastAction SE 2.0 ✓ ✓' with no explicit claim about compatibility, infant car seat integration, or travel system functionality; the translation invents a detailed compatibility relationship not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_gomax

- Claim: `claim_srl_compat_stroller_gomax`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_gomax`

Object

```json
{
  "compatible": true,
  "counterpart": "GoMax",
  "counterpart_name": "GoMax",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
GoMax ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote 'GoMax ✓ ✓' provides no information about compatibility, infant car seats, travel systems, or strollers; the translation invents a detailed functional relationship not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_graco_merge

- Claim: `claim_srl_compat_stroller_graco_merge`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_graco_merge`

Object

```json
{
  "compatible": true,
  "counterpart": "Graco Merge",
  "counterpart_name": "Graco Merge",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Graco Merge ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote 'Graco Merge ✓ ✓' is ambiguous and does not specify compatibility, counterpart type, relationship, or predicate; the translation adds detailed structured claims not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_graco_premier_merge

- Claim: `claim_srl_compat_stroller_graco_premier_merge`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_graco_premier_merge`

Object

```json
{
  "compatible": true,
  "counterpart": "Graco Premier Merge",
  "counterpart_name": "Graco Premier Merge",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Graco Premier Merge ✓ -
```

Verifier: `MEANING_CHANGED` — The quote is a fragment with no predicate or object, only a product name and a checkmark; the translation invents a full compatibility relationship with specific attributes not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_modes

- Claim: `claim_srl_compat_stroller_modes`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_modes`

Object

```json
{
  "compatible": true,
  "counterpart": "Graco Modes Strollers",
  "counterpart_name": "Graco Modes Strollers",
  "counterpart_type": "stroller",
  "qualifier": "With the exception of Modes 3 Lite DLX & Modes 3 Lite Platinum (criteria key *)",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Graco® Modes® Strollers ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote merely lists 'Graco® Modes® Strollers' with checkmarks, implying compatibility or inclusion without specifying conditions; the translation adds a detailed qualifier excluding two specific models and defines a precise relationship (infant car seat clicks into stroller), which is not stated or implied in the original.

Quote — binding 1, source `src_compatibility_chart_apr2026`

```text
* With the exception of Modes 3 Lite DLX & Modes 3 Lite Platinum
```

Verifier: `MEANING_CHANGED` — The translation adds the phrase '(criteria key *)' not present in the quote, implying a metadata or indexing system that the original does not state, thus altering meaning.

Extractor notes: Per-cell footnote-marker placement is ambiguous in mechanical text extraction of the chart (marks are graphical); the '(Stroller frame & rear facing use mode only)' criteria appears adjacent to this row and may apply to the GoMax column — consult chart PDF visually. From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_outpace_lx

- Claim: `claim_srl_compat_stroller_outpace_lx`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_outpace_lx`

Object

```json
{
  "compatible": true,
  "counterpart": "Outpace LX",
  "counterpart_name": "Outpace LX",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Outpace® LX ✓ -
```

Verifier: `MEANING_CHANGED` — The quote 'Outpace® LX ✓ -' contains no information about compatibility, infant car seats, travel systems, or strollers; the translation fabricates a detailed compatibility claim not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_ready2grow_20

- Claim: `claim_srl_compat_stroller_ready2grow_20`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_ready2grow_20`

Object

```json
{
  "compatible": true,
  "counterpart": "Ready2Grow 2.0",
  "counterpart_name": "Ready2Grow 2.0",
  "counterpart_type": "stroller",
  "qualifier": "Can only be used with the rear seat (criteria key +)",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Ready2Grow 2.0 ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote only states 'Ready2Grow 2.0 ✓ ✓' with no context, while the translation adds specific compatibility details (e.g., 'can only be used with the rear seat', 'infant car seat clicks into stroller'), which are not present or implied in the original.

Quote — binding 1, source `src_compatibility_chart_apr2026`

```text
+Can only be used with the rear seat
```

Verifier: `MEANING_CHANGED` — The translation adds specific product names ('Ready2Grow 2.0'), relationship details ('infant car seat clicks into stroller'), and a structured compatibility predicate not present in the quote, which only states a generic restriction: 'Can only be used with the rear seat'.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_ready2grow_lx_20

- Claim: `claim_srl_compat_stroller_ready2grow_lx_20`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_ready2grow_lx_20`

Object

```json
{
  "compatible": true,
  "counterpart": "Ready2Grow LX 2.0",
  "counterpart_name": "Ready2Grow LX 2.0",
  "counterpart_type": "stroller",
  "qualifier": "Can only be used with the rear seat (criteria key +)",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Ready2Grow LX 2.0 ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote only states 'Ready2Grow LX 2.0 ✓ ✓' with no context, while the translation adds specific compatibility details (e.g., 'infant car seat clicks into stroller', 'rear seat only', 'travel system') not present in the original, altering the meaning.

Quote — binding 1, source `src_compatibility_chart_apr2026`

```text
+Can only be used with the rear seat
```

Verifier: `MEANING_CHANGED` — The translation adds specific product names ('Ready2Grow LX 2.0') and a functional relationship ('infant car seat clicks into stroller') not present in the quote, which only states a positional constraint ('Can only be used with the rear seat').

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_ready2jet

- Claim: `claim_srl_compat_stroller_ready2jet`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_ready2jet`

Object

```json
{
  "compatible": true,
  "counterpart": "prod_graco_ready2jet",
  "counterpart_name": "Ready2Jet",
  "counterpart_type": "stroller",
  "qualifier": "Only with models produced in 2025 & later",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Ready2Jet® ✓ ✓ (Only with models produced in 2025 & later)
```

Verifier: `MEANING_CHANGED` — The translation adds the predicate 'infant car seat clicks into stroller (travel system)' and object type 'stroller', which are not mentioned in the quote; the quote only states compatibility conditionally for 2025+ models without specifying function or product type.

Extractor notes: Counterpart is catalog product prod_graco_ready2jet. The catalog's pilot Ready2Jet (2212125) predates 2025, so compatibility with that specific unit is revision-dependent per the chart qualifier. From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_ready2roll_wagon

- Claim: `claim_srl_compat_stroller_ready2roll_wagon`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_ready2roll_wagon`

Object

```json
{
  "compatible": true,
  "counterpart": "Ready2Roll Wagon",
  "counterpart_name": "Ready2Roll Wagon",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Ready2Roll Wagon ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote merely states 'Ready2Roll Wagon ✓ ✓' with no mention of compatibility, infant car seats, travel systems, or strollers; the translation invents a detailed compatibility relationship not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_snugrider_elite

- Claim: `claim_srl_compat_stroller_snugrider_elite`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_snugrider_elite`

Object

```json
{
  "compatible": true,
  "counterpart": "SnugRider Elite",
  "counterpart_name": "SnugRider Elite",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
SnugRider® Elite ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote only states 'SnugRider® Elite ✓ ✓' with no context, while the translation adds specific claims about compatibility, relationship to a stroller, and function as a travel system — none of which are present or implied in the original.

Extractor notes: SnugRider Elite is a car seat carrier frame. From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_compat_stroller_verb

- Claim: `claim_srl_compat_stroller_verb`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_with_verb`

Object

```json
{
  "compatible": true,
  "counterpart": "Verb",
  "counterpart_name": "Verb",
  "counterpart_type": "stroller",
  "relationship": "infant car seat clicks into stroller (travel system)"
}
```

Quote — binding 0, source `src_compatibility_chart_apr2026`

```text
Verb® ✓ ✓
```

Verifier: `MEANING_CHANGED` — The quote 'Verb® ✓ ✓' provides no information about compatibility, strollers, infant car seats, or travel systems; the translation invents a detailed compatibility relationship not present in the source.

Extractor notes: From official APR 2026 compatibility chart; chart states it supersedes any individual product's instruction manual.

### claim_srl_limit_base_80pct

- Claim: `claim_srl_limit_base_80pct`
- Tier: `C3`
- Type/predicate: `LIMIT` / `minimum_base_support_on_vehicle_seat`

Object

```json
{
  "unit": "percent",
  "value": 80
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Note: Make sure base is a minimum of 80% on vehicle seat.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly implies the base must provide 80% support on the vehicle seat, while the quote only requires the base to occupy a minimum of 80% of the vehicle seat’s surface — a spatial requirement, not a functional support claim.

Extractor notes: None recorded.

### claim_srl_limit_body_support_max_weight

- Claim: `claim_srl_limit_body_support_max_weight`
- Tier: `C3`
- Type/predicate: `LIMIT` / `body_support_maximum_child_weight`

Object

```json
{
  "unit": "lb",
  "value": 12
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
The body support can ONLY be used for infants 12 lb (5 kg) or less.
```

Verifier: `MEANING_CHANGED` — The translation omits the critical qualifier 'ONLY' and the metric equivalent '5 kg', reducing the constraint to a mere maximum weight limit without emphasizing exclusivity or providing dual units, thus altering the original meaning.

Extractor notes: None recorded.

### claim_srl_limit_expiration_7yr

- Claim: `claim_srl_limit_expiration_7yr`
- Tier: `C3`
- Type/predicate: `LIMIT` / `useful_life_years`

Object

```json
{
  "rule": "Stop using and discard the car seat 7 years after date of manufacture; date label is on back of car seat.",
  "unit": "years",
  "value": 7
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
STOP using this car seat and throw it away 7 years after the date of manufacture.
```

Verifier: `MEANING_CHANGED` — The translation adds information not in the quote: 'date label is on back of car seat.' The original quote does not specify where the date of manufacture is located, so this addition changes the meaning by introducing an unstated detail.

Extractor notes: None recorded.

### claim_srl_limit_harness_strap_height

- Claim: `claim_srl_limit_harness_strap_height`
- Tier: `C3`
- Type/predicate: `LIMIT` / `harness_strap_height`

Object

```json
{
  "rule": "For rear-facing use, the harness straps must be at or just below the child's shoulders.",
  "unit": null,
  "value": "at or just below the child's shoulders"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Harness Straps MUST BE AT OR JUST BELOW the Child’s Shoulders
```

Verifier: `MEANING_CHANGED` — The translation adds the condition 'For rear-facing use,' which is not present in the original quote. This introduces a contextual restriction not stated in the source, altering the scope and applicability of the rule.

Extractor notes: Stated as the check in 4-A step 6 and repeated in step 10 ('At or Just Below the Child’s Shoulders'); slot selection detail (upper vs lower loops) is in claim_srl_step_harnessfit_11/12.

### claim_srl_limit_head_clearance

- Claim: `claim_srl_limit_head_clearance`
- Tier: `C3`
- Type/predicate: `LIMIT` / `minimum_head_clearance_below_seat_top`

Object

```json
{
  "rule": "Top of child's head must be at least 1 in (2.5 cm) below the top of the car seat.",
  "unit": "in",
  "value": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Top of Head MUST BE AT LEAST 1” (2.5 cm) BELOW the Top of the Car Seat
```

Verifier: `MEANING_CHANGED` — The translation adds 'child's' before 'head', which is not in the original quote and introduces an assumption about the subject that may not be intended (e.g., could apply to a dummy or other object).

Extractor notes: None recorded.

### claim_srl_limit_max_height

- Claim: `claim_srl_limit_max_height`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_child_height`

Object

```json
{
  "unit": "in",
  "value": 32
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Rear-Facing: 4-30 lb (1.8- 13.6 kg) 32” (81 cm) or less
```

Verifier: `MEANING_CHANGED` — The quote specifies a maximum height of 32” (81 cm) for rear-facing use, but the translation incorrectly labels it as 'maximum_child_height' without specifying that this limit applies only to rear-facing configuration; also, the quote includes weight limits (4-30 lb) which the translation omits entirely, altering scope and conditions.

Extractor notes: None recorded.

### claim_srl_limit_min_weight

- Claim: `claim_srl_limit_min_weight`
- Tier: `C3`
- Type/predicate: `LIMIT` / `minimum_child_weight`

Object

```json
{
  "unit": "lb",
  "value": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
This car seat is for children 4-30 lb (1.8-13.6 kg) and 32” (81 cm) or less.
```

Verifier: `MEANING_CHANGED` — The translation only states the minimum child weight (4 lb) but omits the maximum weight (30 lb) and the height limit (32" or less), altering the full meaning of the safety constraint.

Extractor notes: None recorded.

### claim_srl_part_harness_release_lever

- Claim: `claim_srl_part_harness_release_lever`
- Tier: `C3`
- Type/predicate: `PART_LOCATION` / `harness_release_lever_location`

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 14,
    "source_id": "src_snugride_manual_en_v1"
  },
  "location_description": "Under the seat pad at the front of the carrier; pressed down to loosen harness straps.",
  "part": "harness_release_lever"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
H  Harness Release Lever (Under Pad)
```

Verifier: `MEANING_CHANGED` — The translation adds specific operational detail ('pressed down to loosen harness straps') and precise location ('at the front of the carrier') not present in the source, which only states 'Under Pad' without direction or function.

Extractor notes: None recorded.

### claim_srl_part_rearfacing_belt_path

- Claim: `claim_srl_part_rearfacing_belt_path`
- Tier: `C3`
- Type/predicate: `PART_LOCATION` / `rear_facing_belt_path_location`

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 14,
    "source_id": "src_snugride_manual_en_v1"
  },
  "location_description": "Belt path on the carrier used when installing without the base; marked with a blue label.",
  "part": "rear_facing_belt_path"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
E  Rear-Facing Belt Path (When Used Without Base)
```

Verifier: `MEANING_CHANGED` — The translation adds 'marked with a blue label' and 'on the carrier', which are not present in the exact quote; it also reifies the concept as a 'PART_LOCATION' with structured metadata not implied by the source.

Extractor notes: None recorded.

### claim_srl_spec_aircraft_certified

- Claim: `claim_srl_spec_aircraft_certified`
- Tier: `C3`
- Type/predicate: `SPEC` / `aircraft_certification`

Object

```json
{
  "certified": true,
  "restriction": "Use only on forward-facing aircraft seats; follow vehicle installation instructions (sections 3-C, 3-D, 6-D lap belt installation)."
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
This child restraint is certified for use in aircraft. Use only on forward-facing aircraft seats.
```

Verifier: `MEANING_CHANGED` — The translation adds 'follow vehicle installation instructions (sections 3-C, 3-D, 6-D lap belt installation)' which is not mentioned in the original quote. This introduces new conditions and references to vehicle-specific instructions not present in the source, altering the meaning.

Extractor notes: Closes vault collection gap 'FAA/aircraft certification ... unverified' — the manual states aircraft certification on pages 10-11.

### claim_srl_spec_base_features

- Claim: `claim_srl_spec_base_features`
- Tier: `C3`
- Type/predicate: `SPEC` / `base_features`

Object

```json
{
  "features": [
    "LATCH-equipped stay-in-car base",
    "4-position adjustable",
    "easy-to-read level indicator"
  ],
  "included": true
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Base | Included; LATCH-equipped stay-in-car base, 4-position adjustable, with easy-to-read level indicator |
```

Verifier: `MEANING_CHANGED` — The translation incorrectly implies that all listed features are independently included, while the quote specifies that only the 'LATCH-equipped stay-in-car base' is included, and the other features describe that base.

Extractor notes: None recorded.

### claim_srl_spec_base_recline_positions

- Claim: `claim_srl_spec_base_recline_positions`
- Tier: `C3`
- Type/predicate: `SPEC` / `base_recline_positions`

Object

```json
{
  "value": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Base Has 4 Recline Positions Squeeze the base recline lever and lift the base to extend the foot.
```

Verifier: `MEANING_CHANGED` — The translation omits the instruction to 'squeeze the base recline lever and lift the base to extend the foot,' which is a critical operational step. The quote describes both a feature (4 positions) and an action required to use it; the translation only captures the feature, thereby changing the meaning by dropping essential procedural context.

Extractor notes: None recorded.

### claim_srl_spec_carrier_weight

- Claim: `claim_srl_spec_carrier_weight`
- Tier: `C0`
- Type/predicate: `SPEC` / `carrier_weight_without_base`

Object

```json
{
  "unit": "lb",
  "value": 7.5
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Carrier weight without base | 7.5 lb (spec table); marketing copy says "weighs just 7.2 lb" |
```

Verifier: `MEANING_CHANGED` — The translation omits the marketing claim of '7.2 lb', which is explicitly present in the quote and creates a discrepancy with the spec table's 7.5 lb. This omission changes the meaning by erasing a key contrast the source highlights.

Extractor notes: PDP spec table says 7.5 lb while PDP marketing copy says 7.2 lb; spec-table value recorded. Reviewer may want a second source.

### claim_srl_spec_dimensions

- Claim: `claim_srl_spec_dimensions`
- Tier: `C0`
- Type/predicate: `SPEC` / `product_dimensions`

Object

```json
{
  "depth": 18.07,
  "height": 27.4,
  "unit": "in",
  "width": 15.5
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Product width | 15.5 in |
```

Verifier: `MEANING_CHANGED` — The translation adds depth (18.07 in) and height (27.4 in) dimensions not mentioned in the quote, which only specifies width (15.5 in). Adding unmentioned attributes changes the meaning.

Quote — binding 1, source `src_pdp_specs_page`

```text
| Product height | 27.4 in |
```

Verifier: `MEANING_CHANGED` — The translation adds depth and width dimensions not present in the quote, which only specifies height; this introduces new information and alters the meaning.

Quote — binding 2, source `src_pdp_specs_page`

```text
| Product depth | 18.07 in |
```

Verifier: `MEANING_CHANGED` — The translation adds height (27.4 in) and width (15.5 in) dimensions not present in the quote, which only specifies depth (18.07 in). Adding unmentioned attributes constitutes a meaning change.

Extractor notes: None recorded.

### claim_srl_spec_fmvss213

- Claim: `claim_srl_spec_fmvss213`
- Tier: `C3`
- Type/predicate: `SPEC` / `safety_standard_certification`

Object

```json
{
  "standard": "FMVSS 213"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
This child restraint meets or exceeds all applicable requirements of Federal motor vehicle safety standard 213 for use in motor vehicles.
```

Verifier: `MEANING_CHANGED` — The translation reduces the claim to a certification against FMVSS 213, omitting the critical qualifier 'meets or exceeds all applicable requirements' and dropping the context of 'for use in motor vehicles'. This removes the comparative strength ('or exceeds') and the specific application domain, altering the scope and assurance level of the original statement.

Extractor notes: None recorded.

### claim_srl_spec_handle_positions

- Claim: `claim_srl_spec_handle_positions`
- Tier: `C3`
- Type/predicate: `SPEC` / `carry_handle_positions`

Object

```json
{
  "rule": "Handle must be upright in position A when carrying; any locked position is allowed in the vehicle.",
  "value": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Handle Has 4 Positions Rotate handle to any of the 4 locked positions.
```

Verifier: `MEANING_CHANGED` — The translation adds specific conditions (upright in position A when carrying, any locked position in vehicle) and assigns a rule not present in the quote; the quote only states 4 locked positions exist without specifying usage context or orientation.

Quote — binding 1, source `src_snugride_manual_en_v1`

```text
Carry handle MUST be upright in position A when carrying. Handle can be in any locked position when used in the vehicle.
```

Verifier: `MEANING_CHANGED` — The translation omits the imperative 'MUST' for the first condition, replacing it with a weaker 'must', and drops the explicit distinction that the handle 'can be in any locked position' only 'when used in the vehicle' — instead implying 'any locked position is allowed in the vehicle' without specifying the context of use. This softens the requirement and removes the conditional scope, altering the meaning.

Extractor notes: Assigned C3 (carry-handle rule is a child-carrying safety constraint).

### claim_srl_spec_harness_type

- Claim: `claim_srl_spec_harness_type`
- Tier: `C3`
- Type/predicate: `SPEC` / `harness_type`

Object

```json
{
  "value": "5-point, front-adjust"
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Harness | 5-point, front-adjust (per official feature-callout gallery image) |
```

Verifier: `MEANING_CHANGED` — The translation drops the critical qualifier 'per official feature-callout gallery image', which limits the claim to a visual reference rather than asserting it as a factual specification. This omission changes the meaning by presenting the harness type as a direct product spec rather than an observation from an image.

Extractor notes: Harness spec assigned C3 because it touches the child-restraint harness system.

### claim_srl_spec_install_methods

- Claim: `claim_srl_spec_install_methods`
- Tier: `C3`
- Type/predicate: `SPEC` / `base_installation_methods`

Object

```json
{
  "methods": [
    "vehicle seat belt",
    "lower anchor attachment (LATCH)"
  ],
  "restriction": "Do not use both at the same time; carrier without base installs with vehicle seat belt only."
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
This infant car seat base can be installed in your vehicle using either the vehicle seat belt OR the Lower anchor attachment system. Both are equally safe to use. DO NOT USE BOTH AT THE SAME TIME.
```

Verifier: `MEANING_CHANGED` — Translation adds unmentioned restriction: 'carrier without base installs with vehicle seat belt only,' which is not in the quote and alters the scope of installation instructions.

Quote — binding 1, source `src_snugride_manual_en_v1`

```text
This infant car seat carrier can be installed in your vehicle using only the vehicle seat belt. Lower anchor attachment is not available to install the carrier.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly implies that 'lower anchor attachment (LATCH)' is a valid installation method with a restriction ('Do not use both at the same time'), while the quote explicitly states lower anchor attachment is 'not available' — meaning it cannot be used at all.

Extractor notes: None recorded.

### claim_srl_step_baseless_1

- Claim: `claim_srl_step_baseless_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the car seat on the vehicle back seat and push it back until the front of the car seat touches the vehicle seat back.",
  "procedure": "install_carrier_seat_belt",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Place Car Seat in Back Seat of the Vehicle Place the car seat on the vehicle seat. Push it back until the front of the car seat touches the vehicle seat back.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly combines 'Back Seat of the Vehicle' into 'vehicle back seat', which may imply a specific part (e.g., rear bench) rather than the general rear seating area. Also, the original specifies placing the car seat on 'the vehicle seat' (any seat in the back), while the translation implies placement directly on 'the vehicle back seat' as a single unit, potentially altering the intended scope of acceptable placement.

Extractor notes: None recorded.

### claim_srl_step_baseless_3

- Claim: `claim_srl_step_baseless_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Lock the vehicle seat belt: slowly pull the shoulder belt all the way out, let it retract, then pull to confirm it is locked.",
  "procedure": "install_carrier_seat_belt",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Lock the Vehicle Seat Belt In most vehicles today, slowly pull the shoulder belt all the way out and then let it go back in. You will hear a “clicking” sound.
```

Verifier: `MEANING_CHANGED` — The translation adds 'pull to confirm it is locked,' which is not mentioned in the original quote. The original only describes pulling the belt out and letting it retract, with a clicking sound indicating lock; no confirmation step is stated.

Extractor notes: None recorded.

### claim_srl_step_baseless_5

- Claim: `claim_srl_step_baseless_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Test for tightness: push and pull the car seat at the seat belt side to side and front to back; it must move less than 1 in (2.5 cm).",
  "procedure": "install_carrier_seat_belt",
  "step_number": 5
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
5. Test For Tightness Grab the sides of the car seat where the seat belt is and push and pull the car seat from side to side and front to back.
```

Verifier: `MEANING_CHANGED` — The translation adds a quantitative requirement ('it must move less than 1 in (2.5 cm)') not present in the original quote, which only instructs to push and pull the car seat without specifying any acceptable movement threshold.

Extractor notes: None recorded.

### claim_srl_step_baseless_6

- Claim: `claim_srl_step_baseless_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check the rear-facing level line: the red level line on the side of the seat must be level with the ground, checked with the child in the restraint.",
  "procedure": "install_carrier_seat_belt",
  "step_number": 6
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
6. Check the Rear Facing Level Line The red level line on the side of the seat MUST BE LEVEL with the ground.
```

Verifier: `MEANING_CHANGED` — The translation adds 'checked with the child in the restraint,' which is not mentioned in the original quote. This introduces a new condition (child must be present during check) that alters the meaning and scope of the instruction.

Extractor notes: None recorded.

### claim_srl_step_beltbase_1

- Claim: `claim_srl_step_beltbase_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Store the lower anchor attachment connectors on the plastic bars on the sides of the base and remove the slack.",
  "procedure": "install_base_seat_belt",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Store Lower Anchor Attachment Connectors Attach the Lower anchor attachment connectors to the plastic bars on sides of base as shown. Remove the slack.
```

Verifier: `MEANING_CHANGED` — The translation changes 'Attach the Lower anchor attachment connectors to the plastic bars' to 'Store the lower anchor attachment connectors on the plastic bars', replacing the action 'attach' with 'store', which alters the intended procedure.

Extractor notes: None recorded.

### claim_srl_step_beltbase_2

- Claim: `claim_srl_step_beltbase_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the base flat on the vehicle back seat and push it back until the front of the base touches the vehicle seat back.",
  "procedure": "install_base_seat_belt",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Place Base in Back Seat of the Vehicle Place the base flat on the vehicle seat. Push it back until the front of the base touches the vehicle seat back.
```

Verifier: `MEANING_CHANGED` — The translation adds 'seat belt' to the procedure name ('install_base_seat_belt'), which is not mentioned in the original quote. The quote only describes placing the base on the back seat and pushing it back — no reference to seat belts or their use is made. This addition introduces new information not present in the source, altering the meaning.

Extractor notes: None recorded.

### claim_srl_step_beltbase_5

- Claim: `claim_srl_step_beltbase_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Lock the vehicle seat belt: slowly pull the shoulder belt all the way out, let it retract, then pull to confirm it is locked.",
  "procedure": "install_base_seat_belt",
  "step_number": 5
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
5. Lock the Vehicle Seat Belt In most vehicles today, slowly pull the shoulder belt all the way out and then let it go back in. You will hear a “clicking” sound.
```

Verifier: `MEANING_CHANGED` — The translation adds 'pull to confirm it is locked,' which is not mentioned in the original quote. The quote only describes pulling the belt out and letting it retract, with a clicking sound indicating lock; no confirmation pull is stated.

Extractor notes: None recorded.

### claim_srl_step_beltbase_6

- Claim: `claim_srl_step_beltbase_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Press down firmly in the center of the base and pull on the shoulder belt to tighten while feeding the slack back into the retractor.",
  "procedure": "install_base_seat_belt",
  "step_number": 6
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
6. Tighten the Vehicle Seat Belt Press down firmly in the center of the base. Pull on the shoulder belt to tighten while feeding the slack back in the retractor.
```

Verifier: `MEANING_CHANGED` — The translation merges two distinct actions ('Press down firmly in the center of the base' and 'Pull on the shoulder belt...') into a single compound action without preserving the sequential or conditional relationship implied in the original. The original implies these are separate steps or simultaneous but distinct actions; the translation presents them as a single fused action, altering the procedural meaning.

Extractor notes: None recorded.

### claim_srl_step_beltbase_7

- Claim: `claim_srl_step_beltbase_7`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Test for tightness: push and pull the base at the seat belt side to side and front to back; it must move less than 1 in (2.5 cm).",
  "procedure": "install_base_seat_belt",
  "step_number": 7
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
7. Test For Tightness Grab the sides of the base where the seat belt is and push and pull the base from side to side and front to back.
```

Verifier: `MEANING_CHANGED` — The translation adds a quantitative requirement ('it must move less than 1 in (2.5 cm)') not present in the original quote, which only instructs to push and pull the base without specifying any measurement or tolerance.

Extractor notes: None recorded.

### claim_srl_step_beltbase_8

- Claim: `claim_srl_step_beltbase_8`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the car seat into the base and push down on the front of the car seat and handle until it clicks; pull up on the front corners to confirm attachment.",
  "procedure": "install_base_seat_belt",
  "step_number": 8
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
8. Attach Car Seat to Base Place car seat into the base. Push down on the front of the car seat and handle until you hear a “click”.
```

Verifier: `MEANING_CHANGED` — The translation adds 'pull up on the front corners to confirm attachment,' which is not mentioned in the original quote. This introduces a new action and verification step not present in the source, altering the meaning.

Extractor notes: None recorded.

### claim_srl_step_beltbase_9

- Claim: `claim_srl_step_beltbase_9`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Re-check the level indicator with the child in the restraint; the vehicle must be level with the ground.",
  "procedure": "install_base_seat_belt",
  "step_number": 9
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
9. Check the Level Indicator Vehicle MUST be level with the ground. Check the level indicator with child in the child restraint.
```

Verifier: `MEANING_CHANGED` — The translation adds 'Re-check', implying a repeated action not stated in the original. The original says 'Check' (first-time action), while 'Re-check' suggests a prior check occurred, altering the procedural meaning.

Extractor notes: None recorded.

### claim_srl_step_bucklefit_1

- Claim: `claim_srl_step_bucklefit_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check the buckle position: the correct slot is the one closest to the child without being underneath them.",
  "procedure": "adjust_buckle_to_fit_child",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Check the Buckle Position The correct slot is the one that is closest to your child without being underneath them.
```

Verifier: `MEANING_CHANGED` — The translation adds 'adjust_buckle_to_fit_child' as a procedure, which is not mentioned or implied in the original quote. The quote only instructs to check the buckle position, not to perform an adjustment. This addition introduces a new action not present in the source, altering the meaning.

Extractor notes: None recorded.

### claim_srl_step_bucklefit_2

- Claim: `claim_srl_step_bucklefit_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "To change the buckle position: remove the child from the seat; from the bottom of the car seat insert the buckle's metal clip up through the shell and pad, then from the front pull the buckle out of the pad and shell.",
  "procedure": "adjust_buckle_to_fit_child",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. To Change Buckle Position Remove child from the seat. From the bottom of car seat, insert the buckle’s metal clip up through shell and pad. From the front, pull buckle out of the pad an shell.
```

Verifier: `MEANING_CHANGED` — The translation adds 'then' and 'adjust_buckle_to_fit_child' which are not in the original; 'then' implies a strict sequence not stated, and 'adjust_buckle_to_fit_child' adds a purpose not mentioned in the quote.

Extractor notes: Quote preserves the manual's typo 'an shell' (should read 'and shell') verbatim from the pypdf text layer.

### claim_srl_step_bucklefit_3

- Claim: `claim_srl_step_bucklefit_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Insert the metal clip into the new location: push the metal clip down through the pad and shell, making sure the buckle's red button is facing out.",
  "procedure": "adjust_buckle_to_fit_child",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Insert Metal Clip Into New Location Push metal clip down through the pad and shell. Make sure the buckle’s red button is facing out.
```

Verifier: `MEANING_CHANGED` — The translation adds 'adjust_buckle_to_fit_child' as a procedure, which is not mentioned in the quote. The quote only describes a mechanical action (inserting a clip) without specifying the purpose or context of fitting a child, thus altering the meaning by introducing unmentioned intent.

Extractor notes: pypdf also repeats this step's text on page 55 (page-layout extraction artifact); the step belongs to 4-B and is cited on page 54.

### claim_srl_step_bucklefit_4

- Claim: `claim_srl_step_bucklefit_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Pull up on the buckle to check it is secured, making sure the buckle's metal clip is completely through the pad and shell.",
  "procedure": "adjust_buckle_to_fit_child",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Pull Up On Buckle To Check It Is Secured Make sure buckle’s metal clip is completely through pad and shell.
```

Verifier: `MEANING_CHANGED` — The translation adds the phrase 'making sure' which implies an ongoing or continuous action, whereas the original quote uses 'Make sure' as a discrete imperative instruction. This subtle shift alters the procedural tone and could imply a different level of attention or duration required.

Extractor notes: pypdf also repeats this step's text on page 55 (page-layout extraction artifact); the step belongs to 4-B and is cited on page 54.

### claim_srl_step_harnessfit_1

- Claim: `claim_srl_step_harnessfit_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Loosen the harness straps: push down on the harness release lever while pulling out on the harness straps at the chest clip.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Loosen Harness Straps Push down on the harness release lever while pulling out on the harness straps at the chest clip.
```

Verifier: `MEANING_CHANGED` — The translation adds 'adjust_harness_to_fit_child' as a procedure, which is not stated in the quote; the quote only describes a mechanical action without specifying the purpose or context of fitting a child.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_10

- Claim: `claim_srl_step_harnessfit_10`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Insert the harness straps into the new slot location at or just below the child's shoulders, making sure the straps are not twisted and are at the same height.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 10
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
10. Insert Harness Straps Into the New Location At or Just Below the Child’s Shoulders Make sure the harness straps are not twisted and are at the same height.
```

Verifier: `MEANING_CHANGED` — The translation adds 'slot' to 'new location', implying a specific hardware feature (slots) not mentioned in the original quote, which could mislead users into expecting a physical slot rather than a general location. This is an unwarranted addition that changes meaning.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_2

- Claim: `claim_srl_step_harnessfit_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Release the chest clip: squeeze the chest clip release buttons and pull apart.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Release the Chest Clip Squeeze the chest clip release buttons and pull apart.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, type, predicate) not present in the quote, which alters the meaning by implying a formal procedure context and categorization the original text does not state.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_3

- Claim: `claim_srl_step_harnessfit_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Unbuckle the buckle: press the red button, pull the buckle tongues out, and place the harness straps off to the sides.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Unbuckle the Buckle Press the red button and pull buckle tongues out. Place harness straps off to the sides.
```

Verifier: `MEANING_CHANGED` — The translation adds the phrase 'adjust_harness_to_fit_child' as a procedure, which is not mentioned or implied in the original quote. The original only describes the mechanical action of unbuckling and positioning straps, without specifying intent or context such as fitting a child. This addition alters the meaning by introducing an unstated purpose.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_4

- Claim: `claim_srl_step_harnessfit_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the child in the seat, making sure their back is flat against the car seat back.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Place Your Child in the Seat Make sure their back is flat against the car seat back.
```

Verifier: `MEANING_CHANGED` — The translation adds 'adjust_harness_to_fit_child' as a procedure, which is not mentioned or implied in the exact quote. The quote only instructs to place the child and ensure their back is flat against the seat back; it does not mention harness adjustment at all.

Extractor notes: The manual attaches a WARNING to this step about bulky clothing/snowsuits in cold weather; that warning is already recorded as claim_srl_warning_bulky_clothing.

### claim_srl_step_harnessfit_5

- Claim: `claim_srl_step_harnessfit_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the harness straps over the child's shoulders.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 5
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
5. Place Harness Straps Over Child’s Shoulders
```

Verifier: `MEANING_CHANGED` — The translation adds the phrase 'adjust_harness_to_fit_child' as a procedure, which is not mentioned or implied in the original quote. The original only instructs to place straps over shoulders; it does not specify adjusting for fit, thus introducing new procedural intent.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_6

- Claim: `claim_srl_step_harnessfit_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check the harness height: the harness straps must be at or just below the child's shoulders.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 6
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
6. Check Harness Height Harness Straps MUST BE AT OR JUST BELOW the Child’s Shoulders
```

Verifier: `MEANING_CHANGED` — The translation adds the procedure 'adjust_harness_to_fit_child' and step_number 6, which are not stated in the exact quote. The quote only instructs to check the harness height condition; it does not prescribe an adjustment action or assign a step number.

Extractor notes: Embedded limit also recorded as claim_srl_limit_harness_strap_height.

### claim_srl_step_harnessfit_7

- Claim: `claim_srl_step_harnessfit_7`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check that the top of the child's head is at least 1 in (2.5 cm) below the top of the car seat.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 7
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
7. Top of Head MUST BE AT LEAST 1” (2.5 cm) BELOW the Top of the Car Seat
```

Verifier: `MEANING_CHANGED` — The translation adds 'the child's' before 'head', which is not in the original quote and introduces an assumption about the subject that may not be universally valid (e.g., could apply to a dummy or test object).

Extractor notes: Restates the head-clearance limit already recorded as claim_srl_limit_head_clearance; kept as a STEP because the manual numbers it as an action in procedure 4-A.

### claim_srl_step_harnessfit_8

- Claim: `claim_srl_step_harnessfit_8`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "To change harness height positions: with the harness straps loose, from the back of the car seat remove the left and right side harness strap loops from the splitter plate.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 8
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
8. To Change Harness Height Positions With harness straps loose, from the back of the car seat, remove the left and right side harness strap loops from the splitter plate.
```

Verifier: `MEANING_CHANGED` — The translation adds the procedure label 'adjust_harness_to_fit_child' and step_number:8, which are not present in the original quote. The original only states the action without assigning it to a specific child-fitting context or numbering it as step 8 within a larger procedure — this addition changes the meaning by implying intent and structure not stated.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_9

- Claim: `claim_srl_step_harnessfit_9`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Pull the harness straps out from the front of the car seat.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 9
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
9. Pull Harness Straps Out From the Front of Car Seat
```

Verifier: `MEANING_CHANGED` — The translation adds the purpose 'adjust_harness_to_fit_child' and labels it as a 'procedure_step', which are not stated in the original quote. The original is a bare imperative instruction without context or intent, while the translation implies a procedural step within a larger child-fitting process.

Extractor notes: None recorded.

### claim_srl_step_latch_1

- Claim: `claim_srl_step_latch_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Remove the lower anchor attachment connectors from their storage position.",
  "procedure": "install_base_lower_anchor",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Remove Lower Anchor Attachment Connectors from Storage Location Unhook the Lower anchor attachment connectors and remove from storage position.
```

Verifier: `MEANING_CHANGED` — The translation adds 'their' and rephrases 'Unhook the Lower anchor attachment connectors and remove from storage position' as a single action 'Remove...from their storage position,' omitting the explicit instruction to 'Unhook' first, which is a procedural step change.

Extractor notes: None recorded.

### claim_srl_step_latch_10

- Claim: `claim_srl_step_latch_10`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Re-check the level indicator with the child in the restraint; the vehicle must be level with the ground.",
  "procedure": "install_base_lower_anchor",
  "step_number": 10
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
10. Check the Level Indicator Vehicle MUST be level with the ground. Check the level indicator with child in the child restraint.
```

Verifier: `MEANING_CHANGED` — The translation adds 'Re-check', implying a prior check occurred, which the original does not state. Also, it reorders and merges instructions into a single clause, altering the procedural emphasis and potentially omitting the distinct requirement to first ensure the vehicle is level before checking the indicator.

Extractor notes: None recorded.

### claim_srl_step_latch_4

- Claim: `claim_srl_step_latch_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the base flat on the vehicle back seat, push it back until it touches the vehicle seat back, and center it between the lower anchors.",
  "procedure": "install_base_lower_anchor",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Place Base in Back Seat of the Vehicle Place the base flat on the vehicle seat. Push it back until the front of the base touches the vehicle seat back. Center the base between the lower Lower anchor attachment anchors.
```

Verifier: `MEANING_CHANGED` — The translation omits 'Lower anchor attachment' before 'anchors', which changes the specificity of the anchors being referenced. The original specifies 'lower Lower anchor attachment anchors' — a precise technical term — while the translation simplifies to 'lower anchors', potentially misleading the user about which anchors are meant.

Extractor notes: None recorded.

### claim_srl_step_latch_5

- Claim: `claim_srl_step_latch_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check the level indicator; the vehicle must be level with the ground.",
  "procedure": "install_base_lower_anchor",
  "step_number": 5
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
5. Check the Level Indicator Vehicle MUST be level with the ground.
```

Verifier: `MEANING_CHANGED` — The translation adds the phrase 'install_base_lower_anchor' as a procedure, which is not mentioned or implied in the exact quote. This introduces new information not present in the source, altering the meaning by associating the step with a specific procedure that the original text does not specify.

Extractor notes: None recorded.

### claim_srl_step_latch_6

- Claim: `claim_srl_step_latch_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Connect the lower anchor attachment connectors to the vehicle's lower anchors; the strap should lie flat and not be twisted, and hooks must not be attached upside down.",
  "procedure": "install_base_lower_anchor",
  "step_number": 6
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
6. Connect Lower Anchor Attachment Connectors to the Vehicle’s Lower Anchor Attachment Anchors Lower anchor attachment strap should lay as flat as possible and not be twisted.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hooks must not be attached upside down,' which is not mentioned in the original quote. This introduces a new condition not present in the source, altering the meaning.

Extractor notes: None recorded.

### claim_srl_step_latch_7

- Claim: `claim_srl_step_latch_7`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Press down firmly in the center of the base while tightening the lower anchor attachment strap.",
  "procedure": "install_base_lower_anchor",
  "step_number": 7
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
7. Tighten the Lower Anchor Attachment Strap Press down firmly in the center of the base while tightening the Lower anchor attachment strap.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, type) not present in the quote, which changes meaning by implying a formal procedure schema the original does not state.

Extractor notes: None recorded.

### claim_srl_step_latch_8

- Claim: `claim_srl_step_latch_8`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Test for tightness: push and pull the base at the strap side to side and front to back; it must move less than 1 in (2.5 cm).",
  "procedure": "install_base_lower_anchor",
  "step_number": 8
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
8. Test For Tightness Grab the sides of the base where the Lower anchor attachment strap is and push and pull the base from side to side and front to back.
```

Verifier: `MEANING_CHANGED` — The translation adds a quantitative requirement ('it must move less than 1 in (2.5 cm)') not present in the original quote, which only instructs to push and pull the base without specifying any acceptable movement threshold.

Extractor notes: None recorded.

### claim_srl_step_latch_9

- Claim: `claim_srl_step_latch_9`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the car seat into the base and push down on the front of the car seat and handle until it clicks; pull up on the front corners to confirm attachment.",
  "procedure": "install_base_lower_anchor",
  "step_number": 9
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
9. Attach Car Seat to Base Place car seat into the base. Push down on the front of the car seat and handle until you hear a “click”.
```

Verifier: `MEANING_CHANGED` — The translation adds 'pull up on the front corners to confirm attachment,' which is not mentioned in the original quote. This introduces a new action and verification step not present in the source, altering the procedure's meaning.

Extractor notes: None recorded.

### claim_srl_step_removechild_1

- Claim: `claim_srl_step_removechild_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Loosen the harness straps: push down on the harness release lever while pulling out on the harness straps at the chest clip.",
  "procedure": "remove_child",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Loosen Harness Straps Push down on the harness release lever while pulling out on the harness straps at the chest clip.
```

Verifier: `MEANING_CHANGED` — The translation adds a 'procedure' field ('remove_child') and 'step_number' not present in the quote, which introduces unverified context and alters meaning by implying a specific use case not stated.

Extractor notes: None recorded.

### claim_srl_step_removechild_2

- Claim: `claim_srl_step_removechild_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Release the chest clip: squeeze the chest clip release buttons and pull apart.",
  "procedure": "remove_child",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Release the Chest Clip Squeeze the chest clip release buttons and pull apart.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (e.g., 'procedure':'remove_child', 'step_number':2) not present in the original quote, which alters meaning by implying context and intent not stated. Also, wrapping the instruction in an object with keys like 'action' and 'predicate' imposes a semantic structure absent in the source.

Extractor notes: None recorded.

### claim_srl_step_removechild_3

- Claim: `claim_srl_step_removechild_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Unbuckle the child: press the red button, remove the buckle tongues, and remove the child from the seat.",
  "procedure": "remove_child",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Unbuckle Your Child Press in on the red button and remove the buckle tongues. Remove Child from the seat.
```

Verifier: `MEANING_CHANGED` — The translation rephrases 'Unbuckle Your Child' as 'Unbuckle the child', which changes the imperative address from the user ('Your') to a generic object ('the'), subtly altering the instructional tone and ownership. Also, the translation merges three distinct actions into a single run-on sentence without preserving the original step structure, potentially obscuring the sequence or emphasis. Though minor, these changes affect instructional clarity and user direction, which matters under strict auditing.

Extractor notes: None recorded.

### claim_srl_step_secure_2

- Claim: `claim_srl_step_secure_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Buckle the harness: listen for a click when the buckle tongues attach, and pull up on each tongue to confirm it is secure.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Buckle You will hear a “click” when buckle tongues are securely attached. Pull up on each buckle tongue to make sure it is securely attached.
```

Verifier: `MEANING_CHANGED` — The translation adds 'the harness' and 'secure_child_in_car_seat' which are not mentioned in the quote; it also rephrases 'buckle tongues are securely attached' as 'buckle tongues attach' (present tense, implying action rather than state), and omits the imperative 'You will hear' in favor of 'listen for', changing the actor and instruction tone.

Extractor notes: None recorded.

### claim_srl_step_secure_3

- Claim: `claim_srl_step_secure_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Buckle the chest clip: listen for a click when it is securely buckled.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Buckle the Chest Clip You will hear a “click” when the chest clip is securely buckled.
```

Verifier: `MEANING_CHANGED` — The translation adds 'listen for a click' as an explicit instruction, while the original only states 'You will hear a “click”' — implying passive observation, not active listening. This changes the actor’s required behavior and adds an imperative not present in the source.

Extractor notes: None recorded.

### claim_srl_step_secure_4

- Claim: `claim_srl_step_secure_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Pull all the slack out from around the waist: pull up on the harness strap while pushing the chest clip down, on both sides.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Pull All the Slack Out From Around the Waist Pull up on the harness strap while pushing the chest clip down. Do this to both sides.
```

Verifier: `MEANING_CHANGED` — The translation restructures the instruction into a single concatenated sentence without preserving the imperative tone or the explicit 'Do this to both sides' as a separate directive. It also adds 'secure_child_in_car_seat' and 'step_number:4' which are not present in the original quote, introducing metadata not stated in the source. These additions alter the meaning by implying context and structure not originally provided.

Extractor notes: None recorded.

### claim_srl_step_secure_5

- Claim: `claim_srl_step_secure_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Tighten the harness by pulling the harness adjustment strap until no harness webbing can be pinched at the child's shoulder.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 5
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
5. Tighten the Harness by Pulling the Harness Adjustment Strap When you are not able to pinch any of the harness webbing at your child’s shoulder, the harness is tight enough.
```

Verifier: `MEANING_CHANGED` — The translation omits the conditional clause 'When you are not able to pinch any of the harness webbing at your child’s shoulder, the harness is tight enough,' replacing it with an imperative 'until no harness webbing can be pinched,' which changes the meaning from a verification condition to a continuous action directive.

Extractor notes: None recorded.

### claim_srl_step_secure_7

- Claim: `claim_srl_step_secure_7`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check tightness again and tighten more if needed.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 7
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
7. Check Tightness Tighten more if needed.
```

Verifier: `MEANING_CHANGED` — The translation adds 'again' to 'Check tightness', implying a repeated action not stated in the original quote. The original only says 'Check Tightness' without suggesting it is a repeat step.

Extractor notes: None recorded.

### claim_srl_warning_airbag

- Claim: `claim_srl_warning_airbag`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_active_front_airbag_position`

Object

```json
{
  "description": "NEVER place this child restraint rear-facing in a vehicle seating location that has an active front air bag. An inflating air bag can hit the child and car seat with great force and cause serious injury or death.",
  "hazard_type": "airbag_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
NEVER PLACE THIS CHILD RESTRAINT REAR-FACING IN A VEHICLE SEATING LOCATION THAT HAS AN ACTIVE FRONT AIR BAG.
```

Verifier: `MEANING_CHANGED` — The translation adds a causal explanation ('An inflating air bag can hit the child and car seat with great force and cause serious injury or death') not present in the exact quote, which only states a prohibition without elaborating on consequences.

Extractor notes: None recorded.

### claim_srl_warning_bulky_clothing

- Claim: `claim_srl_warning_bulky_clothing`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_bulky_clothing_under_harness`

Object

```json
{
  "description": "In cold weather do not put snowsuits or bulky garments on the child in the car seat; bulky clothing prevents proper harness tightening. Buckle the child first, then place a blanket over them or the coat on backwards.",
  "hazard_type": "harness_fit_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
WARNING! In cold weather do not put snowsuits or bulky garments on your child when placing them in the car seat. Bulky clothing can prevent the harness straps from being tightened properly.
```

Verifier: `MEANING_CHANGED` — The translation adds instructions not in the quote: 'Buckle the child first, then place a blanket over them or the coat on backwards.' The original only warns against bulky clothing and explains why; it does not prescribe any alternative action.

Extractor notes: None recorded.

### claim_srl_warning_crash_replace

- Claim: `claim_srl_warning_crash_replace`
- Tier: `C3`
- Type/predicate: `WARNING` / `requires_replacement_after_crash`

Object

```json
{
  "description": "If the car seat is in a crash it must be replaced and never used again; a crash can cause unseen damage.",
  "hazard_type": "structural_integrity"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
If car seat is in a crash, it must be replaced. DO NOT use it again! A crash can cause unseen damage and using it again could result in serious injury or death.
```

Verifier: `MEANING_CHANGED` — Translation omits the explicit warning 'DO NOT use it again!' and the consequence 'could result in serious injury or death,' which are critical to the original warning's severity and intent.

Extractor notes: None recorded.

### claim_srl_warning_other_strollers

- Claim: `claim_srl_warning_other_strollers`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_non_graco_strollers`

Object

```json
{
  "description": "Never use a Graco infant carrier with any other manufacturer's strollers; this can result in serious injury or death.",
  "hazard_type": "attachment_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
NEVER use a Graco infant carrier with any other manufacturer’s strollers. This can result in serious injury or death.
```

Verifier: `MEANING_CHANGED` — The translation adds a structured object with 'hazard_type': 'attachment_hazard', which is not stated or implied in the original quote. The original only warns against using non-Graco strollers and mentions injury/death risk, but does not classify or label the hazard type. This addition introduces new information not present in the source.

Extractor notes: None recorded.

### claim_srl_warning_strings_cords

- Claim: `claim_srl_warning_strings_cords`
- Tier: `C3`
- Type/predicate: `WARNING` / `requires_keeping_strings_away`

Object

```json
{
  "description": "Keep strings and cords away from the child; they can cause strangulation. Do not place the carrier near windows with blind or drape cords, hang strings on the carrier, or attach strings to toys.",
  "hazard_type": "strangulation_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
KEEP STRINGS AND CORDS AWAY FROM CHILD. Strings and cords can cause strangulation. DO NOT place carrier near windows where cords from blinds or drapes can strangle a child.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hang strings on the carrier, or attach strings to toys' which are not mentioned in the original quote. The original only warns against placing the carrier near windows with blind/drape cords; it does not prohibit hanging strings on the carrier or attaching strings to toys.

Extractor notes: None recorded.

### claim_srl_warning_unattended

- Claim: `claim_srl_warning_unattended`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_leaving_child_unattended`

Object

```json
{
  "description": "Never leave the child unattended, even when sleeping; a child may become tangled in harness straps and suffocate or strangle.",
  "hazard_type": "strangulation_suffocation_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Never leave child unattended, even when sleeping. Child may become tangled in harness straps and suffocate or strangle.
```

Verifier: `MEANING_CHANGED` — The translation adds 'a child' as the subject of the hazard clause, implying a general risk to any child, while the original quote uses 'Child' (capitalized, singular) which may refer to the specific child in context. Also, the translation rephrases the original into a semicolon-separated compound sentence, altering the syntactic structure and potentially implying a stronger causal link than the original's simple period separation. These changes, though subtle, alter the grammatical actor and sentence structure, which can affect interpretation in safety contexts.

Extractor notes: None recorded.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (14)

### claim_srl_step_latch_2

- Claim: `claim_srl_step_latch_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Make sure the lower anchor attachment strap is in the rear-facing belt path, marked with a blue label.",
  "procedure": "install_base_lower_anchor",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Make Sure Lower Anchor Attachment Strap is in the Rear- Facing Belt Path, Marked With a Blue Label
```

Verifier: `ENTAILED` — The translation faithfully reproduces the exact quote without adding, dropping, or altering any factual elements, qualifiers, or conditions.

Extractor notes: None recorded.

### claim_srl_step_latch_3

- Claim: `claim_srl_step_latch_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Extend the lower anchor attachment strap to its maximum length by pressing the gray button and pulling on the strap.",
  "procedure": "install_base_lower_anchor",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Extend the Lower Anchor Attachment Strap Extend the Lower anchor attachment strap to its maximum length by pressing the gray button and pulling on the strap.
```

Verifier: `ENTAILED` — The translation accurately preserves the action, method, and step number from the exact quote without adding, dropping, or altering any qualifiers, actors, or conditions.

Extractor notes: None recorded.

### claim_srl_step_beltbase_3

- Claim: `claim_srl_step_beltbase_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Check the level indicator; the vehicle must be level with the ground.",
  "procedure": "install_base_seat_belt",
  "step_number": 3
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
3. Check the Level Indicator Vehicle MUST be level with the ground.
```

Verifier: `ENTAILED` — The translation faithfully reproduces the exact instruction from the quote: 'Check the Level Indicator Vehicle MUST be level with the ground.' The semicolon and capitalization are stylistic; the core meaning — checking the level indicator under the condition that the vehicle must be level with the ground — is preserved without addition, omission, or alteration of any factual element.

Extractor notes: None recorded.

### claim_srl_step_beltbase_4

- Claim: `claim_srl_step_beltbase_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Thread the vehicle seat belt through the rear-facing belt path (marked with a blue label) and buckle it; the belt should lie flat and not be twisted.",
  "procedure": "install_base_seat_belt",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Route the Vehicle Seat Belt Thread vehicle seat belt through the rear-facing belt path (marked with a blue label) and buckle it. The seat belt should lay as flat as possible and not be twisted.
```

Verifier: `ENTAILED` — The translation accurately captures the core instructions: threading the belt through the rear-facing path (blue label), buckling it, and ensuring it lies flat and untwisted. No meaning-altering changes in actor, action, condition, or qualifier.

Extractor notes: None recorded.

### claim_srl_step_baseless_2

- Claim: `claim_srl_step_baseless_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Thread the vehicle seat belt through the rear-facing belt path (marked with a blue label) and buckle it; the belt should not be twisted.",
  "procedure": "install_carrier_seat_belt",
  "step_number": 2
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
2. Route the Vehicle Seat Belt Thread vehicle seat belt through the rear-facing belt path (marked with a blue label) and buckle it. The seat belt should not be twisted.
```

Verifier: `ENTAILED` — The translation accurately preserves the core instruction: threading the seat belt through the rear-facing path (blue label), buckling it, and ensuring it is not twisted. The step number and procedure context are added for structure but do not alter the factual meaning of the original quote.

Extractor notes: None recorded.

### claim_srl_step_baseless_4

- Claim: `claim_srl_step_baseless_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Lay a forearm across the car seat at the belt path and push down; pull on the shoulder belt to tighten while feeding the slack back into the retractor.",
  "procedure": "install_carrier_seat_belt",
  "step_number": 4
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
4. Tighten the Vehicle Seat Belt Lay your forearm across the car seat at the belt path and push down. Pull on the shoulder belt to tighten while feeding the slack back in the retractor.
```

Verifier: `ENTAILED` — The translation accurately preserves the actions, sequence, and intent of the original quote: laying the forearm, pushing down, pulling the shoulder belt, and feeding slack back into the retractor. No added, dropped, or altered qualifiers, numbers, units, or actors. The structure is rephrased as a procedure step but does not change meaning.

Extractor notes: None recorded.

### claim_srl_step_secure_1

- Claim: `claim_srl_step_secure_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Place the harness straps over the child's shoulders.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
1. Place Harness Straps Over Child’s Shoulders
```

Verifier: `ENTAILED` — The translation faithfully restates the exact instruction from the quote without adding, dropping, or altering any semantic element. The action, object, and step number match precisely.

Extractor notes: None recorded.

### claim_srl_step_secure_6

- Claim: `claim_srl_step_secure_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Raise the chest clip to the child's armpit level.",
  "procedure": "secure_child_in_car_seat",
  "step_number": 6
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
6. Raise the Chest Clip to Child’s Armpit Level
```

Verifier: `ENTAILED` — The translation accurately preserves the instruction: 'Raise the chest clip to the child's armpit level' matches the quote exactly in action, object, and condition. No meaning change detected.

Extractor notes: None recorded.

### claim_srl_warning_no_dual_install

- Claim: `claim_srl_warning_no_dual_install`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_simultaneous_belt_and_lower_anchor`

Object

```json
{
  "description": "Do not use both the vehicle seat belt and the lower anchor attachment at the same time when using the car seat rear-facing.",
  "hazard_type": "installation_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Do not use both the vehicle seat belt and Lower anchor attachment at the same time when using the car seat rear-facing.
```

Verifier: `ENTAILED` — The translation faithfully reproduces the exact quote without adding, dropping, or altering any factual elements, conditions, or qualifiers. The predicate and object merely repackage the same prohibition without changing meaning.

Extractor notes: None recorded.

### claim_srl_warning_suffocation_soft_surface

- Claim: `claim_srl_warning_suffocation_soft_surface`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_carrier_on_soft_surfaces`

Object

```json
{
  "description": "Suffocation hazard: the infant carrier can roll over on soft surfaces and suffocate the child. Never place the carrier on beds, sofas, or other soft surfaces.",
  "hazard_type": "suffocation_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
SUFFOCATION HAZARD: Infant carrier can roll over on soft surfaces and suffocate child. NEVER place carrier on beds, sofas, or other soft surfaces.
```

Verifier: `ENTAILED` — The translation faithfully preserves the original warning’s meaning: suffocation hazard due to carrier rolling over on soft surfaces, and prohibition of placing it on beds, sofas, or other soft surfaces. No added, dropped, or altered qualifiers, numbers, units, actors, or conditions.

Extractor notes: None recorded.

### claim_srl_warning_fall_elevated

- Claim: `claim_srl_warning_fall_elevated`
- Tier: `C3`
- Type/predicate: `WARNING` / `prohibits_carrier_on_elevated_surfaces`

Object

```json
{
  "description": "Fall hazard: the child's movements can move the carrier. Never place the carrier on counter tops, tables, or any other elevated surfaces.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
FALL HAZARD: Child’s movements can move carrier. NEVER place carrier on counter tops, tables or any other elevated surfaces.
```

Verifier: `ENTAILED` — The translation accurately preserves the meaning of the original quote: it conveys the fall hazard due to child movement, the prohibition against placing the carrier on elevated surfaces, and correctly identifies the hazard type and predicate without adding, dropping, or altering any critical detail.

Extractor notes: None recorded.

### claim_srl_step_harnessfit_11

- Claim: `claim_srl_step_harnessfit_11`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "For a smaller baby (child's shoulders even with or just above the lowest 2 slots): use the upper loops on the harness straps; thread the upper harness strap loops onto the splitter plate, making sure the straps are on top of the splitter plate and completely on.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 11
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
11. For Smaller Baby If the child’s shoulders are even with or just above the lowest 2 slots, use the upper loops on the harness straps. Thread the upper harness straps loops onto the splitter plate. Make sure the straps are on top of the splitter plate and are completely on.
```

Verifier: `ENTAILED` — The translation accurately preserves all key elements: condition (smaller baby, shoulders at/above lowest 2 slots), action (use upper loops, thread onto splitter plate), and verification (straps on top and completely on). No numbers, units, actors, conditions, or qualifiers are added, dropped, or altered. The procedural framing as 'adjust_harness_to_fit_child' is a valid abstraction consistent with the quote’s intent.

Extractor notes: AMBIGUITY: steps 11 and 12 are conditional alternatives (child-size dependent) rather than sequential actions; only one applies per child. Both retained with the manual's own numbering to keep 4-A contiguous.

### claim_srl_step_harnessfit_12

- Claim: `claim_srl_step_harnessfit_12`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "For a larger baby (child's shoulders even with or just above the upper 2 slots): use the lower loops on the harness straps; thread the lower harness strap loops onto the splitter plate, making sure the straps are completely on the splitter plate.",
  "procedure": "adjust_harness_to_fit_child",
  "step_number": 12
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
12. For Larger Baby If the child’s shoulders are even with or just above the upper 2 slots, use the lower loops on the harness straps. Thread the lower harness straps loops onto the splitter plate. Make sure the straps are completely on the splitter plate.
```

Verifier: `ENTAILED` — The translation accurately preserves all key elements: condition (larger baby, shoulders at/above upper 2 slots), action (use lower loops, thread onto splitter plate), and requirement (straps completely on splitter plate). No numbers, units, actors, conditions, or qualifiers are added, dropped, or altered. The procedural framing as 'adjust_harness_to_fit_child' is a valid abstraction consistent with the quote’s intent.

Extractor notes: AMBIGUITY: conditional alternative to step 11 (see claim_srl_step_harnessfit_11).

### claim_srl_step_shortenbuckle_1

- Claim: `claim_srl_step_shortenbuckle_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "To shorten the buckle for low birth weight infants (minimum weight 4 lb / 1.8 kg): with the crotch strap clip in the rear crotch slot, insert the clip into the front crotch slot in the seat but not through the seat pad; the crotch strap clip should remain flat against the seat.",
  "procedure": "shorten_buckle_low_birth_weight",
  "step_number": 1
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
To Shorten Buckle for Low Birth Weight Infants: (Minimum weight is 4 lb (1.8 kg)): When crotch strap clip is in rear crotch slot, insert clip into front crotch slot in seat but not through seat pad. Crotch strap clip should remain flat against seat.
```

Verifier: `ENTAILED` — The translation faithfully reproduces the exact quote without adding, dropping, or altering any factual detail, condition, direction, or qualifier. All elements — including weight specification, clip placement, and orientation — are preserved verbatim in meaning.

Extractor notes: AMBIGUITY: this is an un-numbered sub-procedure printed inside 4-B after step 4, applicable only to low-birth-weight infants; recorded as its own single-step procedure rather than a numbered 4-B step to preserve 4-B's contiguous numbering. Also restates the 4 lb minimum-weight limit (see claim_srl_limit_min_weight).

## 4. C2 claims (1)

### claim_srl_care_seat_pad

- Claim: `claim_srl_care_seat_pad`
- Tier: `C2`
- Type/predicate: `CARE` / `seat_pad_and_canopy_cleaning`

Object

```json
{
  "instructions": [
    "cold water",
    "delicate cycle",
    "drip-dry"
  ],
  "method": "machine_wash",
  "restrictions": [
    "DO NOT USE BLEACH"
  ]
}
```

Quote — binding 0, source `src_snugride_manual_en_v1`

```text
Machine wash pad and canopy in cold water on delicate cycle and drip-dry. DO NOT USE BLEACH.
```

Verifier: `ENTAILED` — The translation accurately captures all key elements: machine wash, cold water, delicate cycle, drip-dry, and prohibition of bleach; no meaning is added, dropped, or altered.

Extractor notes: None recorded.

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (4)

### gap_legacy_manual_1

- Kind: `SOURCE_MISSING`
- Waives: `[]`

Reason: The legacy 4-35 lb 'SnugRide 35 Lite LX' manual (model 2106696) is not in the vault (exists only on third-party ManualsLib, excluded by the official-sources-only rule). The 35 lb side of the mandated maximum_child_weight conflict is therefore bound only to the official PDP gallery image (src_img_in_car_installed), whose text overlay is mechanically unverifiable. The conflict pair itself is fully recorded; this gap notes the weaker binding.

Closes when: An official legacy manual or archived gracobaby.com page stating 4-35 lb is added to the vault.

### gap_chart_cell_marks_1

- Kind: `UNDERIVABLE`
- Waives: `[]`

Reason: The compatibility chart's per-cell check/dash marks and footnote-marker placement are graphical; pypdf text extraction interleaves them ambiguously (e.g. whether the '(Stroller frame & rear facing use mode only)' criteria attaches to the Modes row's SnugRide column or the GoMax column cannot be derived mechanically from the text layer). Row-level compatibility for the SnugRide column is recorded; ambiguous criteria are flagged in extraction_notes on the affected claims.

Closes when: A human reviewer (or vision pass) reads the chart PDF visually and confirms per-cell marks and footnote attachment.

### gap_video_transcripts_1

- Kind: `SOURCE_MISSING`
- Waives: `[]`

Reason: The three official Graco installation/harness videos are URL references only (videos/video-sources.md); no downloaded media or transcript exists in the vault, so no claims are bound to them.

Closes when: Video transcripts or downloaded media are added to the vault.

### gap_spanish_manual_1

- Kind: `NOT_EXTRACTED`
- Waives: `[]`

Reason: The Spanish manual (src_snugride_manual_es_v1) duplicates the English manual's content; extracting it would double claims without adding facts. English manual used as the sole manual source.

Closes when: A market/language-specific extraction pass is requested.

## 7. Batch-eligible C0/C1 spot-audit (2)

Spot-audit sample: `2` of `2` eligible claims. The sample is the five lowest SHA-256 ranks of `review-completion-v1\0<product>\0<claim_id>`, so it is stable and reproducible.

A clean sample may be confirmed as one explicit human batch decision. A failed sample removes batch eligibility; review every batch member individually.

Batch members

- `claim_srl_spec_model_number`
- `claim_srl_spec_weight_with_base`

Sample details

### claim_srl_spec_weight_with_base

- Claim: `claim_srl_spec_weight_with_base`
- Tier: `C0`
- Type/predicate: `SPEC` / `product_weight_with_base`

Object

```json
{
  "unit": "lb",
  "value": 12.3
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Product weight (with base) | 12.3 lb |
```

Verifier: `ENTAILED` — The translation accurately preserves the value (12.3), unit (lb), and condition (with base) from the exact quote without adding, dropping, or altering any semantic element.

Extractor notes: None recorded.

### claim_srl_spec_model_number

- Claim: `claim_srl_spec_model_number`
- Tier: `C0`
- Type/predicate: `SPEC` / `model_number`

Object

```json
{
  "value": "2110186"
}
```

Quote — binding 0, source `src_pdp_specs_page`

```text
| Model # (Studio color, current) | 2110186 |
```

Verifier: `ENTAILED` — The translation accurately extracts the model number '2110186' from the quote without adding, dropping, or altering any qualifiers, units, or conditions.

Extractor notes: None recorded.
