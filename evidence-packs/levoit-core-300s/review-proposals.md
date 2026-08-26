# Review Proposals — levoit-core-300s

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `57`
- Existing human decisions: `8`
- Undecided claims covered here: `49`
- Existing decisions reopened by v2 alarms: `3`
- Total owner action items: `52`
- Proposed `NEEDS_RECHECK`: `18`
- Proposed `REJECTED_FOR_SERVING`: `1`
- Proposed `APPROVED_FOR_PUBLISH`: `33`
- Batch-eligible C0/C1: `18`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (17)

### `claim_c300s_care_filter_lifespan`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `filter_replacement_interval`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds unsupported signals (increased noise, decreased airflow, etc.) not mentioned in any quote; the quotes only specify replacement interval and app tracking, not diagnostic indicators. The projection adds unsupported signals (increased noise, decreased airflow, etc.) not mentioned in any quote; the quotes only specify replacement interval and app tracking, not diagnostic indicators.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "interval": "every 6-8 months",
  "signals": [
    "increased noise",
    "decreased airflow",
    "unusual odors",
    "visibly clogged filter"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
The filter should be replaced every 6–8 months. Y ou may need to replace your filter earlier or later depending on how often you use your air purifier.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds unsupported signals (increased noise, decreased airflow, etc.) not mentioned in any quote; the quotes only specify replacement interval and app tracking, not diagnostic indicators.

Quote — binding 1, source `src_spec_page_core300s`, page `None`

```text
Filter lifespan: 6–8 months; filter life tracked in the VeSync app
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds unsupported signals (increased noise, decreased airflow, etc.) not mentioned in any quote; the quotes only specify replacement interval and app tracking, not diagnostic indicators.

Extractor notes: The 'Y ou' spacing in the first quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_care_housing_cleaning`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `CARE` / `housing_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds 'unplug first' and 'vacuum the inside', which are not mentioned in the quote. The quote only specifies wiping the outside and housing with dry or damp cloth and immediate drying. No instruction to unplug or vacuum interior is supported. Also, the restriction about abrasive chemicals or flammable agents is not mentioned in the quote, making it an unsupported addition.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "method": "wipe with a soft, dry cloth; damp cloth if necessary, then immediately dry; unplug first; vacuum the inside",
  "restrictions": [
    "Do not clean with abrasive chemicals or flammable cleaning agents"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
Wipe the outside of the air purifier with a soft, dry cloth. If necessary, wipe the housing with a damp cloth, then immediately dry.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'unplug first' and 'vacuum the inside', which are not mentioned in the quote. The quote only specifies wiping the outside and housing with dry or damp cloth and immediate drying. No instruction to unplug or vacuum interior is supported. Also, the restriction about abrasive chemicals or flammable agents is not mentioned in the quote, making it an unsupported addition.

Extractor notes: C1 assigned: everyday reversible wipe-down, not disassembly-level care.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_care_prefilter_cleaning`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `prefilter_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds two restrictions not present in the quote: 'Do not clean the filter with water or other liquids' and 'Main filter: do not clean'. The quote only describes cleaning the outer pre-filter with a soft brush or vacuum hose, and does not mention water, liquids, or the main filter at all. These are unsupported semantic additions that broaden the claim beyond what is asserted.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "interval": "every 2-4 weeks",
  "method": "soft brush or vacuum hose",
  "restrictions": [
    "Do not clean the filter with water or other liquids",
    "Main filter: do not clean"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
The outer pre-filter should be cleaned every 2–4 weeks to increase efficiency and extend the life of your filter. Clean the pre-filter using a soft brush or vacuum hose to remove hair, dust, and large particles.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds two restrictions not present in the quote: 'Do not clean the filter with water or other liquids' and 'Main filter: do not clean'. The quote only describes cleaning the outer pre-filter with a soft brush or vacuum hose, and does not mention water, liquids, or the main filter at all. These are unsupported semantic additions that broaden the claim beyond what is asserted.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_care_sensor_cleaning`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `dust_sensor_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The quote only states to 'Clean the sensor every 3 months' without specifying any method, let alone the detailed procedure involving unplugging, using a vacuum cleaner, or running it for at least 10 seconds. The projection adds unsupported operational details not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "interval": "every 3 months",
  "method": "unplug; place a vacuum cleaner over the sensor openings; run the vacuum for at least 10 seconds"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
The AirSight Plus Laser Dust Sensor can be blocked by dust, which affects the sensor’s accuracy. Clean the sensor every 3 months.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote only states to 'Clean the sensor every 3 months' without specifying any method, let alone the detailed procedure involving unplugging, using a vacuum cleaner, or running it for at least 10 seconds. The projection adds unsupported operational details not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_limit_room_size`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `LIMIT` / `effective_room_size`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection presents '20 m²' and '219 ft²' as equivalent metrics with no condition, but the quote explicitly states the room must be smaller than that size for effectiveness — omitting the 'smaller than' condition and the effectiveness caveat wrongly implies the values are absolute limits or targets, not upper bounds under a performance condition.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "metric": "20 m²",
  "unit": "ft²",
  "value": 219
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `16`

```text
Make sure the room is smaller than 219 ft² / 20 m². The air purifier may not be as effective in larger rooms.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection presents '20 m²' and '219 ft²' as equivalent metrics with no condition, but the quote explicitly states the room must be smaller than that size for effectiveness — omitting the 'smaller than' condition and the effectiveness caveat wrongly implies the values are absolute limits or targets, not upper bounds under a performance condition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_part_airsight_sensor`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `dust_sensor_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote only identifies the component as 'P. AirSight™ Plus Laser Dust Sensor' without specifying its physical location, orientation, or relationship to slotted openings, housing sections, or diagram labels. The projection adds unsupported spatial and structural details (e.g., 'behind slotted openings on the back of the housing, upper section', 'labeled P in the parts diagram', 'shown on the 'Back' view'), which are not entailed by the quote and broaden the claim beyond what is asserted.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 5,
    "source_id": "src_manual_core300sp_us"
  },
  "location_description": "The AirSight Plus Laser Dust Sensor sits behind slotted openings on the back of the housing, upper section (labeled P in the parts diagram, shown on the 'Back' view).",
  "part": "airsight_plus_laser_dust_sensor"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `5`

```text
P. AirSight™ Plus Laser Dust Sensor
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote only identifies the component as 'P. AirSight™ Plus Laser Dust Sensor' without specifying its physical location, orientation, or relationship to slotted openings, housing sections, or diagram labels. The projection adds unsupported spatial and structural details (e.g., 'behind slotted openings on the back of the housing, upper section', 'labeled P in the parts diagram', 'shown on the 'Back' view'), which are not entailed by the quote and broaden the claim beyond what is asserted.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_part_filter_cover`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `filter_cover_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds 'clockwise to lock' and 'Labeled R in the parts diagram' — neither is supported by the quotes. The quotes only state twisting counterclockwise to remove; no direction for locking is mentioned. Also, while 'R. Filter Cover' implies a label 'R', the projection asserts it is 'in the parts diagram', which is not stated or implied in the quotes. The projection adds 'clockwise to lock' and 'Labeled R in the parts diagram' — neither is supported by the quotes. The quotes only state twisting counterclockwise to remove; no direction for locking is mentioned. Also, while 'R. Filter Cover' implies a label 'R', the projection asserts it is 'in the parts diagram', which is not stated or implied in the quotes.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 5,
    "source_id": "src_manual_core300sp_us"
  },
  "location_description": "The filter cover is on the bottom of the unit (the unit is flipped over to access it); it twists counterclockwise to remove and clockwise to lock. Labeled R in the parts diagram.",
  "part": "filter_cover"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `5`

```text
R. Filter Cover
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'clockwise to lock' and 'Labeled R in the parts diagram' — neither is supported by the quotes. The quotes only state twisting counterclockwise to remove; no direction for locking is mentioned. Also, while 'R. Filter Cover' implies a label 'R', the projection asserts it is 'in the parts diagram', which is not stated or implied in the quotes.

Quote — binding 1, source `src_manual_core300sp_us`, page `7`

```text
Flip the air purifier over. Twist the filter cover counterclockwise and remove it.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'clockwise to lock' and 'Labeled R in the parts diagram' — neither is supported by the quotes. The quotes only state twisting counterclockwise to remove; no direction for locking is mentioned. Also, while 'R. Filter Cover' implies a label 'R', the projection asserts it is 'in the parts diagram', which is not stated or implied in the quotes.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified). Official photo src_img_three_quarter_elevated_3000 shows the dark bottom cover edge.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_cadr`

- Proposed disposition: **`REJECTED_FOR_SERVING`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `clean_air_delivery_rate`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Agent post-run audit: LIKELY VERIFIER NOISE — the primary value/unit pair and the metric sibling are unambiguous in the object, and each matches the quote. The verifier incorrectly treated the primary unit as global.
- Proposed rationale: Latest-revision-only policy: this claim applies only to an older hardware revision and is not documented for the current revision; retain the CANDIDATE record but do not serve it.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series (CADR row absent from 300S-P manual spec table)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "metric": "240 m³/h",
  "unit": "CFM",
  "value": 141
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
CADR: 141 CFM / 240 m³/h
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection assigns 'CFM' as the unit for the value 141, but the quote pairs 141 with 'CFM' and 240 with 'm³/h' — swapping the unit assignment misattributes the metric and creates a false equivalence.

Extractor notes: Also stated on pages 2 and 11 of src_manual_core300s_us ('CADR (CFM) 141 CFM / 240 m³/h'; 'Clean Air Delivery Rate of 141 cubic feet per minute (CFM), or 240 m³/h'), visually verified. The 300S-P manual spec table omits CADR; not treated as a conflict (absence, not disagreement).

### `claim_c300s_spec_coverage`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `room_coverage`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; Extractor flagged applicability or interpretation context
- Proposed rationale: Verifier found a meaning change: The projection misattributes 219 ft² as 'ideal_room_size_ft2' without specifying it applies only at 4.8 ACH, wrongly implying it is the general ideal size; also adds unsupported conversion to 20 m² without source.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "extended_coverage_ft2_at_1ach": 1051,
  "ideal_room_size_ft2": 219,
  "ideal_room_size_m2": 20
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Ideal room size (coverage): 1,051 ft² at 1 air change per hour; 219 ft² at 4.8 ACH
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection misattributes 219 ft² as 'ideal_room_size_ft2' without specifying it applies only at 4.8 ACH, wrongly implying it is the general ideal size; also adds unsupported conversion to 20 m² without source.

Extractor notes: 300S manual page 2 states 'Ideal Room Size 219 ft² / 20 m²' and page 11 states 'an air change per hour of 5' (visually verified) — slight tension with the spec page's '4.8 ACH'; flagged for reviewer, not a 300S vs 300S-P revision conflict. See also claim_c300s_limit_room_size.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_dimensions`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `product_dimensions`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Agent post-run audit: LIKELY VERIFIER NOISE — the primary value/unit pair and the metric sibling are unambiguous in the object, and each matches the quote. The verifier incorrectly treated the primary unit as global.
- Proposed rationale: Verifier found a meaning change: The projection assigns 'unit':'in' globally but also includes metric dimensions without indicating they are separate units; the quotes present both imperial and metric as parallel, not as a single unit system, so treating 'in' as the sole unit misrepresents the dual-unit assertion. The projection assigns 'unit':'in' globally but also includes metric dimensions without indicating they are separate units; the quotes present both imperial and metric as parallel, not as a single unit system, so treating 'in' as the sole unit misrepresents the dual-unit assertion.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical across revisions)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "metric": "22 x 22 x 36 cm",
  "unit": "in",
  "value": {
    "depth_in": 8.7,
    "height_in": 14.2,
    "width_in": 8.7
  }
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Dimensions: 8.7 x 8.7 x 14.2 in / 22 x 22 x 36 cm
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection assigns 'unit':'in' globally but also includes metric dimensions without indicating they are separate units; the quotes present both imperial and metric as parallel, not as a single unit system, so treating 'in' as the sole unit misrepresents the dual-unit assertion.

Quote — binding 1, source `src_manual_core300sp_us`, page `2`

```text
Dimensions 8.7 × 8.7 × 14.2 in / 22 × 22 × 36 cm
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection assigns 'unit':'in' globally but also includes metric dimensions without indicating they are separate units; the quotes present both imperial and metric as parallel, not as a single unit system, so treating 'in' as the sole unit misrepresents the dual-unit assertion.

Extractor notes: Same value confirmed visually on page 2 of src_manual_core300s_us (no machine-readable text layer; see gaps.json gap_300s_manual_binding_1).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_filter_model_300s` — REOPENED AFTER V2 ALARM

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `SPEC` / `replacement_filter_model`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Prior decision status: **REOPENED** — explicitly reconfirm or amend the existing human disposition.
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required; Conflict triage: DIFFERENT_SCOPE_OR_EVENT — Claim A refers to the original filter part number 'Core 300-RF' for the Core 300S model, while Claim B lists 'Core 300-P-RF' as the part number for the same filter type but likely corresponds to a revised or variant product line (Core 300-P), indicating different model-specific part naming rather than a factual contradiction.
- Proposed rationale: Verifier found a meaning change: The quote identifies the filter as 'Levoit Core 300 Series Original Filter', while the projection renames it 'Levoit True HEPA 3-Stage Original Filter' — adding unmentioned attributes ('True HEPA', '3-Stage') that are not supported by the quote.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S (original revision)",
  "sku": "HEAPAPLVSUS0073",
  "state": null
}
```

Object

```json
{
  "name": "Levoit True HEPA 3-Stage Original Filter",
  "value": "Core 300-RF"
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Levoit Core 300 Series Original Filter, part "Core 300-RF"
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote identifies the filter as 'Levoit Core 300 Series Original Filter', while the projection renames it 'Levoit True HEPA 3-Stage Original Filter' — adding unmentioned attributes ('True HEPA', '3-Stage') that are not supported by the quote.

Extractor notes: CONFLICT: contradicts claim_c300s_spec_filter_model_300sp (300S-P manual lists the Original Filter as 'Core 300-P-RF'). Confirmed visually on page 12 of src_manual_core300s_us: 'Core 300-RF / Levoit True HEPA 3-Stage Original Filter'. C2 assigned because the filter model drives replacement purchases and filter replacement is a C2 procedure.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_operating_conditions`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `operating_temperature_range`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Agent post-run audit: LIKELY VERIFIER NOISE — the primary value/unit pair and the metric sibling are unambiguous in the object, and each matches the quote. The verifier incorrectly treated the primary unit as global.
- Proposed rationale: Verifier found a meaning change: The projection incorrectly assigns the unit '°F' to the metric range '-10 to 40 °C', which is a unit mismatch; the quote pairs -10°–40°C with °C and 14°–104°F with °F, so the projection falsely associates the metric value with the imperial unit.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical across revisions)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "metric": "-10 to 40 °C",
  "unit": "°F",
  "value": "14 to 104"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
Temperature: 14°–104°F / -10°–40°C
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection incorrectly assigns the unit '°F' to the metric range '-10 to 40 °C', which is a unit mismatch; the quote pairs -10°–40°C with °C and 14°–104°F with °F, so the projection falsely associates the metric value with the imperial unit.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_weight_300s` — REOPENED AFTER V2 ALARM

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `product_weight`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Prior decision status: **REOPENED** — explicitly reconfirm or amend the existing human disposition.
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; Conflict triage: GENUINE_CONFLICT — The two claims report different weights (5.95 lb vs. 7.48 lb) for the same model (Core 300S), with no indication in either context that these refer to different revisions, configurations, or measurement conditions.
- Agent post-run audit: LIKELY VERIFIER NOISE — the primary value/unit pair and the metric sibling are unambiguous in the object, and each matches the quote. The verifier incorrectly treated the primary unit as global.
- Proposed rationale: Verifier found a meaning change: The projection assigns 'unit':'lb' while the quote explicitly pairs '5.95' with 'lb' and '2.7' with 'kg'; assigning 'lb' as the unit for the value 5.95 is correct, but the projection incorrectly implies 'lb' is the unit for the metric '2.7 kg', which contradicts the quote's explicit pairing.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S (original revision)",
  "sku": "HEAPAPLVSUS0073",
  "state": null
}
```

Object

```json
{
  "metric": "2.7 kg",
  "unit": "lb",
  "value": 5.95
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Weight: 5.95 lb / 2.7 kg
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection assigns 'unit':'lb' while the quote explicitly pairs '5.95' with 'lb' and '2.7' with 'kg'; assigning 'lb' as the unit for the value 5.95 is correct, but the projection incorrectly implies 'lb' is the unit for the metric '2.7 kg', which contradicts the quote's explicit pairing.

Extractor notes: CONFLICT: contradicts claim_c300s_spec_weight_300sp (300S-P manual states 7.48lb / 3.393kg). Value confirmed visually on page 2 of src_manual_core300s_us ('Weight 5.95 lb / 2.7 kg'); that PDF has no machine-readable text layer, so the verifiable binding cites the official spec-page transcription.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_spec_weight_300sp` — REOPENED AFTER V2 ALARM

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `product_weight`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Prior decision status: **REOPENED** — explicitly reconfirm or amend the existing human disposition.
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; Extractor flagged applicability or interpretation context; Conflict triage: GENUINE_CONFLICT — The two claims report different weights (5.95 lb vs. 7.48 lb) for the same model (Core 300S), with no indication in either context that these refer to different revisions, configurations, or measurement conditions.
- Agent post-run audit: LIKELY VERIFIER NOISE — the primary value/unit pair and the metric sibling are unambiguous in the object, and each matches the quote. The verifier incorrectly treated the primary unit as global.
- Proposed rationale: Verifier found a meaning change: The projection assigns 'unit':'lb' while the quote explicitly pairs 7.48 with 'lb' and 3.393 with 'kg'; assigning 'lb' as the unit for the metric value 3.393 kg is a wrong unit assignment.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S-P (current retail revision; manual rev A2-240918)",
  "sku": "HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "metric": "3.393 kg",
  "unit": "lb",
  "value": 7.48
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
Weight 7.48lb / 3.393kg
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection assigns 'unit':'lb' while the quote explicitly pairs 7.48 with 'lb' and 3.393 with 'kg'; assigning 'lb' as the unit for the metric value 3.393 kg is a wrong unit assignment.

Extractor notes: CONFLICT: contradicts claim_c300s_spec_weight_300s (original 300S manual and live spec page state 5.95 lb / 2.7 kg). Revision difference between Core 300S and Core 300S-P.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_state_standby`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `standby_mode_definition`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote states the air purifier is in Standby Mode when turned off but plugged in, but says nothing about the laser dust sensor remaining active or reporting to the VeSync app. The projection adds unsupported functionality (sensor operation and app reporting) that contradicts the implied inactivity of Standby Mode and lacks any governing condition or textual basis in the quote.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Turned off but plugged in; the laser dust sensor still detects surrounding air quality and reports to the VeSync app.",
  "state": "STANDBY"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `9`

```text
The air purifier is in Standby Mode when it is turned off, but plugged in.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote states the air purifier is in Standby Mode when turned off but plugged in, but says nothing about the laser dust sensor remaining active or reporting to the VeSync app. The projection adds unsupported functionality (sensor operation and app reporting) that contradicts the implied inactivity of Standby Mode and lacks any governing condition or textual basis in the quote.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_step_initial_setup_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds 'cover should snap shut', which is not mentioned or implied in the quote. The quote only specifies replacing the cover and twisting clockwise to lock; it does not assert or imply any snapping action or auditory/physical feedback. This is an unsupported semantic addition.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Replace the filter cover and twist clockwise to lock (cover should snap shut).",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 3,
  "target_parts": [
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `7`

```text
3. Replace the filter cover and twist clockwise to lock. [Figure 1.3]
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'cover should snap shut', which is not mentioned or implied in the quote. The quote only specifies replacing the cover and twisting clockwise to lock; it does not assert or imply any snapping action or auditory/physical feedback. This is an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_c300s_step_initial_setup_4`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds 'away from anything that would block airflow,' which is not mentioned or implied in the quote. The quote only specifies clearance on all sides (15 in / 38 cm) and surface requirements; it does not assert or conditionally imply any requirement regarding airflow obstruction. This is an unsupported semantic addition.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Place the purifier on a flat, stable surface with the display facing up, allowing at least 15 in / 38 cm of clearance on all sides, away from anything that would block airflow.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 4,
  "target_parts": [
    "housing"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `7`

```text
4. Place the purifier on a flat, stable surface with the display facing up. Allow at least 15 inches / 38 cm of clearance on all sides.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'away from anything that would block airflow,' which is not mentioned or implied in the quote. The quote only specifies clearance on all sides (15 in / 38 cm) and surface requirements; it does not assert or conditionally imply any requirement regarding airflow obstruction. This is an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (6)

### `claim_c300s_warning_plastic_wrap`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `remove_filter_wrap_before_use`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical text on 300S manual page 3)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Do not use without removing the plastic wrap from the filter; the purifier will not filter air and may overheat, causing a fire hazard.",
  "hazard_type": "fire"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
Do not use without removing the plastic wrap from the filter. The air purifier will not filter air, and may overheat, causing a fire hazard.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: it preserves the condition (do not use without removing plastic wrap), the consequence (will not filter air), and the hazard (may overheat, causing fire hazard). No semantic addition, omission, or distortion is present.

Extractor notes: C3 assigned per work order rule: all safety warnings from the manuals.

### `claim_c300s_warning_water`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `keep_away_from_water`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Keep the air purifier away from water and wet or damp areas; never place in water or liquid.",
  "hazard_type": "electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
Keep the air purifier away from water, and wet or damp areas. Never place in water or liquid.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote without adding, omitting, or altering any condition, direction, or qualifier. The semicolon replaces 'and' but does not change meaning; the union of quotes fully supports the projection’s assertions.

Extractor notes: None recorded.

### `claim_c300s_warning_oxygen`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `oxygen_administration_distance`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Keep 5 ft / 1.5 m away from where oxygen is being administered.",
  "hazard_type": "fire"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
Keep 5 ft / 1.5 m away from where oxygen is being administered.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the warning in the quote without adding, omitting, or altering any condition, direction, unit, or actor. The quote’s instruction is fully preserved as-is.

Extractor notes: None recorded.

### `claim_c300s_warning_combustible`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `no_combustible_environments`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Do not use where combustible gases, vapors, metallic dust, aerosol products, or fumes from industrial oil are present.",
  "hazard_type": "fire_explosion"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
Do not use where combustible gases, vapors, metallic dust, aerosol (spray) products, or fumes from industrial oil are present.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the prohibition in the quote, omitting only the parenthetical '(spray)' which does not alter the meaning of 'aerosol products' as a category. No condition, direction, actor, or unit is added, removed, or misrepresented. The omission of '(spray)' is a stylistic compression that does not broaden scope or remove governing conditions.

Extractor notes: None recorded.

### `claim_c300s_warning_dimmer`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `no_solid_state_speed_controls`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Do not use this air purifier with any solid-state speed controls such as a dimmer switch.",
  "hazard_type": "fire_electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
WARNING: To reduce the risk of fire or electric shock, do not use this air purifier with any solid-state speed controls (such as a dimmer switch).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, faithful subset of the exact quote, omitting only the introductory 'WARNING:' and the safety rationale ('To reduce the risk of fire or electric shock'). These omissions do not broaden the claim, alter conditions, or add unsupported assertions — the core prohibition remains identical and unqualified in both.

Extractor notes: None recorded.

### `claim_c300s_warning_unplug_before_maintenance`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `unplug_before_maintenance`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "description": "Always unplug the air purifier before servicing, cleaning, or other maintenance such as changing the filter.",
  "hazard_type": "electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `3`

```text
Always unplug the air purifierbefore servicing ,cleaning or other maintenances(such aschanging the filter).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the content of the quote, preserving all conditions, directions, and scope. No qualifiers, limits, or governing conditions are omitted or broadened. The rephrasing of punctuation and spacing does not alter meaning.

Extractor notes: Quote is verbatim from the 300S-P manual's embedded text layer, including its missing/misplaced spaces (text-layer artifact of that PDF). The original 300S manual page 3 reads cleanly: 'Always unplug the air purifier before servicing (such as changing the filter).' (visually verified).

## 4. C2 claims (9)

### `claim_c300s_step_replace_filter_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (300S-P manual covers both; 300S manual page 14 identical except cross-reference 'page 6')",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Unplug the air purifier. Flip the air purifier over and remove the filter cover.",
  "procedure": "replace_filter",
  "step_number": 1,
  "target_parts": [
    "power_cord",
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
1. Unplug the air purifier. Flip the air purifier over and remove the filter cover (see Getting Started, page 7).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the sequence of actions stated in the quote: unplugging the air purifier, flipping it over, and removing the filter cover. No additional conditions, directions, or qualifiers are introduced or omitted in a way that alters meaning. The reference to 'see Getting Started, page 7' is metadata and not part of the asserted action sequence, so its omission does not constitute a meaning change.

Extractor notes: None recorded.

### `claim_c300s_step_replace_filter_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Remove the old filter.",
  "procedure": "replace_filter",
  "step_number": 2,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
2. Remove the old filter.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Remove the old filter.' is directly and exactly stated in the quote '2. Remove the old filter.' No conditions, qualifiers, or directions are omitted that would broaden or alter the meaning. The projection is a faithful subset of the source.

Extractor notes: None recorded.

### `claim_c300s_step_replace_filter_3`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Clean out any remaining dust or hair inside the air purifier using a vacuum hose. Do not use water or liquids.",
  "procedure": "replace_filter",
  "step_number": 3,
  "target_parts": [
    "filter_compartment"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
3. Clean out any remaining dust or hair inside the air purifier using a vacuum hose. Do not use water or liquids to clean the air purifier. [Figure 3.2]
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a faithful subset of the exact quote: it preserves the action (cleaning with a vacuum hose) and the prohibition (do not use water or liquids), omitting only non-semantic elements (figure reference) and redundant phrasing ('inside the air purifier' is implied by context). No condition, direction, or qualifier is lost that would broaden or alter the meaning.

Extractor notes: None recorded.

### `claim_c300s_step_replace_filter_4`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Unwrap the new filter and place it into the housing.",
  "procedure": "replace_filter",
  "step_number": 4,
  "target_parts": [
    "filter_cartridge",
    "housing"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
4. Unwrap the new filter and place it into the housing (see Getting Started, page 7).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Unwrap the new filter and place it into the housing.' is fully supported by the exact quote, which instructs the same action. The parenthetical reference to 'Getting Started, page 7' is procedural guidance and does not alter the core semantic assertion of the action. No condition, direction, actor, unit, or scope is added or lost that changes the meaning.

Extractor notes: Orientation detail from Getting Started: filter goes in with the handle facing up (see claim_c300s_step_initial_setup_2).

### `claim_c300s_step_replace_filter_5`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Replace the cover. Plug in the air purifier.",
  "procedure": "replace_filter",
  "step_number": 5,
  "target_parts": [
    "filter_cover",
    "power_cord"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
5. Replace the cover. Plug in the air purifier.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action sequence stated in the quote: 'Replace the cover. Plug in the air purifier.' No additional conditions, directions, units, or actors are introduced, and no governing conditions are omitted that would broaden or alter the meaning. The projection is a faithful subset of the source.

Extractor notes: None recorded.

### `claim_c300s_step_replace_filter_6`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Reset the Check Filter Indicator.",
  "procedure": "replace_filter",
  "step_number": 6,
  "target_parts": [
    "sleep_mode_button",
    "check_filter_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
6. Reset the Check Filter Indicator (see page 13).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Reset the Check Filter Indicator.' is directly supported by the quote '6. Reset the Check Filter Indicator (see page 13).' The projection omits the step number and reference, which are procedural scaffolding, not semantic assertions. No condition, direction, actor, unit, or scope is added or altered in a way that broadens or contradicts the original. Omission of the page reference does not change meaning, as it is not a governing condition for the action.

Extractor notes: Reset detail is the reset_check_filter_indicator procedure (claims claim_c300s_step_reset_filter_1..4).

### `claim_c300s_step_initial_setup_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical text on 300S manual page 6)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Flip the air purifier over. Twist the filter cover counterclockwise and remove it.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 1,
  "target_parts": [
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `7`

```text
1. Flip the air purifier over. Twist the filter cover counterclockwise and remove it. [Figure 1.1]
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly reproduces the action sequence from the quote without adding, omitting, or altering any condition, direction, or actor. The reference to [Figure 1.1] is metadata and not part of the semantic assertion being projected.

Extractor notes: C2 assigned (higher of C1/C2) because the step opens the filter compartment.

### `claim_c300s_step_initial_setup_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Remove the filter from its plastic packaging and place it back into the air purifier with the handle facing up.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 2,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `7`

```text
2. Remove the filter from its plastic packaging and place the filter back into the air purifier with the handle facing up. [Figure 1.2]
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: removing the filter from packaging, placing it back into the air purifier, and orienting the handle upward. No conditions, qualifiers, or directions are omitted or broadened. The reference to [Figure 1.2] is metadata and not part of the semantic assertion being projected.

Extractor notes: None recorded.

### `claim_c300s_compat_filter_models`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `COMPATIBILITY` / `replacement_filter_compatible_models`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "compatible_with": [
    "Core 300",
    "Core 300-P",
    "Core 300S",
    "Core 300S-P",
    "Core P350",
    "Core P350-P"
  ],
  "counterpart": "Levoit Core 300 Series Original Filter (Core 300-RF)"
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Compatible models per VeSync store: Core 300, Core 300-P, Core 300S, Core 300S-P, Core P350, Core P350-P
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the models quoted as compatible per VeSync store, and adds no unsupported conditions, directions, or scope; the counterpart reference is not contradicted by the quotes and is not required to be supported by them under the union rule.

Extractor notes: Underlying source is the official VeSync store filter page (src_support_vesync_filter_page), which has no local capture; the binding cites the vault's spec transcription that records it (see gaps.json gap_support_page_capture_1).

## 5. Unresolved verifier — C0/C1 (2)

### `claim_c300s_spec_aq_indicator`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `SPEC` / `air_quality_indicator_mapping`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `unresolved`
- Review focus: Standard review
- Proposed rationale: one or more bindings are CANNOT_JUDGE

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "mapping": [
    {
      "air_quality": "Very Good",
      "auto_mode_fan_speed": "Sleep Mode",
      "color": "Blue"
    },
    {
      "air_quality": "Good",
      "auto_mode_fan_speed": "Low",
      "color": "Green"
    },
    {
      "air_quality": "Moderate",
      "auto_mode_fan_speed": "Medium",
      "color": "Orange"
    },
    {
      "air_quality": "Bad",
      "auto_mode_fan_speed": "High",
      "color": "Red"
    }
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `9`

```text
Indicator Color Air Quality Auto Mode Fan Speed Blue Very Good Sleep Mode Green Good Low Orange Moderate Medium Red Bad High
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully maps each air quality level to its corresponding color and auto mode fan speed as explicitly listed in the first quote, and the second quote confirms this mapping is official and consistent.

Quote — binding 1, source `src_img_aq_indicator_table`, page `None`

```text
Official 'Air Quality Indicator Color Table' graphic showing the same color-to-quality-to-fan-speed mapping.
```

Verifier (claim quote union): `CANNOT_JUDGE` — Visual binding is not authenticated by text-only verification; the claim quote union result was ENTAILED.

Extractor notes: First quote is the manual's chart flattened to reading order by text extraction. Second binding is an image (visual, mechanically unverifiable).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_c300s_part_filter_reset_button`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `filter_reset_control_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `unresolved`
- Review focus: Standard review
- Proposed rationale: one or more bindings are CANNOT_JUDGE

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": null,
    "source_id": "src_img_top_panel_2048"
  },
  "location_description": "The filter reset control is the Sleep Mode (moon icon) touch button on the top control panel, left side of the ring around the central On/Off button; the label under the moon icon reads 'RESET FILTER (3S)'. Press and hold 3 seconds to reset the Check Filter Indicator.",
  "part": "sleep_mode_button_filter_reset"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `6`

```text
Sleep Mode Button • Turns Sleep Mode on (see page 9). • Press and hold for 3 seconds to reset the Check Filter Indicator.
```

Verifier (claim quote union): `ENTAILED` — Every assertion in the projection is supported by the union: the Sleep Mode button (moon icon) is on the top control panel (quote 2), its label reads 'RESET FILTER (3S)' (quotes 1, 2), and pressing/holding 3 seconds resets the Check Filter Indicator (quote 1). The location detail 'left side of the ring around the central On/Off button' is not contradicted and is plausibly inferred from the top-down photo context (quote 2), though not explicitly stated — but since omission alone is not a meaning change and no quote contradicts it, the projection does not add unsupported semantics.

Quote — binding 1, source `src_spec_page_core300s`, page `None`

```text
label under the moon icon reads "RESET FILTER (3S)"
```

Verifier (claim quote union): `ENTAILED` — Every assertion in the projection is supported by the union: the Sleep Mode button (moon icon) is on the top control panel (quote 2), its label reads 'RESET FILTER (3S)' (quotes 1, 2), and pressing/holding 3 seconds resets the Check Filter Indicator (quote 1). The location detail 'left side of the ring around the central On/Off button' is not contradicted and is plausibly inferred from the top-down photo context (quote 2), though not explicitly stated — but since omission alone is not a meaning change and no quote contradicts it, the projection does not add unsupported semantics.

Quote — binding 2, source `src_img_top_panel_2048`, page `None`

```text
Top-down control panel photo showing the moon icon button with the 'RESET FILTER (3S)' label beneath it.
```

Verifier (claim quote union): `CANNOT_JUDGE` — Visual binding is not authenticated by text-only verification; the claim quote union result was ENTAILED.

Extractor notes: There is no dedicated reset button; the Sleep Mode button carries the secondary reset function (300S manual page 5 control diagram shows 'RESET FILTER (3S)' under the moon icon, visually verified). If the filter was changed before the indicator lit, press and hold for 3 seconds twice per manual page 13 case B. Third binding is an image (visual, mechanically unverifiable). Bounding box left null PENDING per anti-hallucination rule.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

## 6. Open gaps (3)

### `gap_300s_manual_binding_1`

- Kind: `NOT_EXTRACTED`
- Waives: `[]`
- Reason: The primary source src_manual_core300s_us (and its byte-near-identical copy src_manual_core300s_vesync) has no machine-readable text layer: pypdf and pdfminer.six both extract zero characters from all 24 pages (CID-encoded fonts without usable ToUnicode maps). Every fact was read visually from rendered page images and cross-checked, but a quote bound to these source_ids can never pass the validator's mechanical anti-fabrication gate. Claims are therefore bound to src_manual_core300sp_us (whose cover states 'Product Series: Core 300S series, Core 300S-P Series' — it is the official manual for both series) and to src_spec_page_core300s, with the corresponding src_manual_core300s_us page numbers preserved in extraction_notes. No checklist item or floor is left unmet by this substitution, so nothing is waived; this gap documents why the nominal primary source carries no bindings.
- Closes when: An OCR text layer is added to the vault copy of the 300S manual (without altering the original artifact's hash record), or the validator gains a mode for verifying quotes against rendered page images.

### `gap_hepa_efficiency_1`

- Kind: `UNDERIVABLE`
- Waives: `[]`
- Reason: The HEPA efficiency figure ('H13 True HEPA Filter ... Captures at least 99.97% of airborne particles 0.3 microns (um) in size', 300S manual page 11, visually verified) appears only in src_manual_core300s_us, which has no bindable text layer. The 300S-P manual drops the True HEPA/H13 wording entirely, and specs.md says only 'True HEPA main filter' with no efficiency number. No mechanically verifiable source in the vault states the 99.97% / 0.3 micron figure, so no claim was written for it.
- Closes when: OCR text layer for the 300S manual, or a captured official spec page stating the filtration efficiency.

### `gap_support_page_capture_1`

- Kind: `SOURCE_MISSING`
- Waives: `[]`
- Reason: src_support_vesync_filter_page (official VeSync store filter page confirming Core 300-RF compatibility and 6-8 month lifespan) has local_path null - no captured file exists in the vault. Claims that rely on its facts (claim_c300s_compat_filter_models, part of claim_c300s_care_filter_lifespan) bind instead to the specs.md transcription, which attributes those facts to the VeSync store.
- Closes when: An HTML or text capture of the VeSync filter page is added to the vault with a local_path.

## 7. Batch-eligible C0/C1 spot-audit (18)

Batch ID: `batch_levoit-core-300s_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `18` members of `batch_levoit-core-300s_20260826`.
- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below individually.
- Owner / date: ______________________________

### `claim_c300s_spec_power_supply` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `power_supply`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical across revisions)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "frequency": "60Hz",
  "voltage": "AC 120V"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
Power Supply AC 120V, 60Hz
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the voltage and frequency values from the quote without adding, omitting, or altering any conditions or qualifiers.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### `claim_c300s_spec_standby_power` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `standby_power`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical across revisions)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "unit": "W",
  "value": "< 2"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
Standby Power < 2W
```

Verifier (claim quote union): `ENTAILED` — The quote 'Standby Power < 2W' directly supports the projection's value '< 2' and unit 'W'; no condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### `claim_c300s_spec_wifi_band`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `SPEC` / `wireless_connectivity`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "app": "VeSync",
  "wifi_band": "2.4 GHz"
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
WiFi (2.4 GHz) + VeSync app: remote control, schedules, timers, filter life %, PM2.5 history, Auto/Sleep modes
```

Verifier (claim quote union): `ENTAILED` — The projection asserts 'VeSync' as the app and '2.4 GHz' as the WiFi band; both are explicitly stated in the quotes. The first quote confirms 'VeSync app' and 'WiFi (2.4 GHz)', and the second quote reinforces the 2.4 GHz requirement during setup. No unsupported addition, contradiction, or lost condition is present.

Quote — binding 1, source `src_manual_core300sp_us`, page `17`

```text
During the setup process, you must be on a secure 2.4GHz WiFi network.
```

Verifier (claim quote union): `ENTAILED` — The projection asserts 'VeSync' as the app and '2.4 GHz' as the WiFi band; both are explicitly stated in the quotes. The first quote confirms 'VeSync app' and 'WiFi (2.4 GHz)', and the second quote reinforces the 2.4 GHz requirement during setup. No unsupported addition, contradiction, or lost condition is present.

Extractor notes: None recorded.

### `claim_c300s_spec_voice_control`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `SPEC` / `voice_assistant_support`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "assistants": [
    "Amazon Alexa",
    "Google Assistant"
  ],
  "requires": "VeSync account"
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
Voice control: Amazon Alexa and Google Assistant
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects that Amazon Alexa and Google Assistant are supported voice assistants, and that a VeSync account is required — both assertions are directly supported by the union of quotes.

Quote — binding 1, source `src_manual_core300sp_us`, page `8`

```text
Note: Y ou must create your own VeSync account to access voice assistants.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects that Amazon Alexa and Google Assistant are supported voice assistants, and that a VeSync account is required — both assertions are directly supported by the union of quotes.

Extractor notes: The 'Y ou' spacing in the second quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

### `claim_c300s_spec_package_contents`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `package_contents`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S-P (current retail revision; manual rev A2-240918)",
  "sku": "HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "items": [
    "1 x Smart Air Purifier",
    "1 x Pre-installed 3-Stage Original Filter",
    "1 x User Manual",
    "1 x Quick Start Guide"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
1 × Smart Air Purifier 1 × Pre-installed 3-Stage Original Filter 1 × User Manual 1 × Quick Start Guide
```

Verifier (claim quote union): `ENTAILED` — The projection exactly lists the items and quantities stated in the quote without adding, omitting, or altering any semantic conditions, directions, or qualifiers.

Extractor notes: Original 300S manual page 2 lists the same four items but names the filter 'True HEPA 3-Stage Original Filter (Pre-Installed)' (visually verified). Wording difference only; item count identical, so not recorded as a value conflict.

### `claim_c300s_spec_model_name`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `model_name`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "value": "Core 300S"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `19`

```text
Product Name Smart Air Purifier Model Core 300S
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'Model Core 300S', which directly supports the projection's value 'Core 300S' without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: Even the current 300S-P manual's warranty table lists Model: Core 300S (spec table on its page 2 says 'Model Core 300S series'). Original 300S manual page 19 identically lists Model: Core 300S (visually verified).

### `claim_c300s_spec_filtration_stages`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `filtration_stages`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "form": "single cylindrical cartridge",
  "stages": [
    "nylon pre-filter",
    "True HEPA main filter",
    "high-efficiency activated carbon filter"
  ]
}
```

Quote — binding 0, source `src_spec_page_core300s`, page `None`

```text
3-stage filter cartridge (single cylindrical unit): ultra-fine nylon pre-filter + True HEPA main filter + high-efficiency activated carbon filter
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quoted structure: a single cylindrical unit containing three stages — nylon pre-filter, True HEPA main filter, and high-efficiency activated carbon filter — with no unsupported additions or omissions altering meaning.

Extractor notes: 300S manual page 11 additionally states the H13 True HEPA filter 'Captures at least 99.97% of airborne particles 0.3 microns (μm) in size' — visually verified but not extractable as a bindable quote (see gaps.json gap_hepa_efficiency_1). The 300S-P manual drops the 'True HEPA'/H13 wording.

### `claim_c300s_limit_humidity`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `LIMIT` / `maximum_operating_humidity`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "unit": "% RH",
  "value": "< 85"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `2`

```text
Humidity: < 85% RH
```

Verifier (claim quote union): `ENTAILED` — The projection '< 85' with unit '% RH' is fully supported by the quote 'Humidity: < 85% RH', as it preserves the exact value, direction, and unit without adding or omitting any governing condition.

Extractor notes: 300S manual page 11 (Humidity section) adds that above this level 'the surface of the filter may become moldy' (visually verified).

### `claim_c300s_step_reset_filter_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "condition": "Check Filter Indicator lit up red",
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Replace the filter.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 1,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
1. Replace the filter (see page 14).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Replace the filter.' is directly supported by the quote '1. Replace the filter (see page 14).' The parenthetical reference to page 14 is omitted in the projection, but this is a procedural reference, not a semantic condition or qualifier affecting the action itself. No governing condition, direction, unit, or actor is lost or broadened. The projection faithfully asserts the core action without adding unsupported meaning.

Extractor notes: Case A of the manual's reset instructions (indicator lit red). Case B (filter changed before the indicator lit) is press-and-hold only; recorded in the PART_LOCATION claim's notes.

### `claim_c300s_step_reset_filter_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "condition": "Check Filter Indicator lit up red",
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Turn on the air purifier.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 2,
  "target_parts": [
    "on_off_button"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
2. Turn on the air purifier.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Turn on the air purifier.' is directly and exactly stated in the quote '2. Turn on the air purifier.' No conditions, qualifiers, or directions are omitted that would broaden or alter the meaning. The step number '2.' is procedural scaffolding and not part of the semantic assertion being audited.

Extractor notes: None recorded.

### `claim_c300s_step_reset_filter_3` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "condition": "Check Filter Indicator lit up red",
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Press and hold the Sleep Mode button for 3 seconds.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 3,
  "target_parts": [
    "sleep_mode_button"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
3. Press and hold for 3 seconds.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Press and hold the Sleep Mode button for 3 seconds.' is fully supported by the union of quotes: one quote specifies the duration (3 seconds) and the other explicitly names the 'Sleep Mode button' as the target, with the same duration. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Quote — binding 1, source `src_manual_core300sp_us`, page `6`

```text
Reset the Check Filter Indicator by pressing and holding the Sleep Mode button for 3 seconds.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Press and hold the Sleep Mode button for 3 seconds.' is fully supported by the union of quotes: one quote specifies the duration (3 seconds) and the other explicitly names the 'Sleep Mode button' as the target, with the same duration. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: The page 13 step shows the Sleep Mode moon icon between 'hold' and 'for'; the icon glyph does not survive text extraction. Page 6 quote names the button explicitly.

### `claim_c300s_step_reset_filter_4` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "condition": "Check Filter Indicator lit up red",
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Confirm the Check Filter Indicator turns off, indicating a successful reset.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 4,
  "target_parts": [
    "check_filter_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `13`

```text
4. will turn off when successfully reset.
```

Verifier (claim quote union): `ENTAILED` — The quote states the device 'will turn off when successfully reset,' which directly supports the projection's claim that turning off the Check Filter Indicator confirms a successful reset — the action and its meaning are semantically aligned without adding unsupported conditions or broadening scope.

Extractor notes: The Check Filter icon precedes 'will turn off' on the printed page; the icon glyph does not survive text extraction.

### `claim_c300s_step_app_setup_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series (identical text on 300S manual page 7)",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Download the VeSync app by scanning the QR code or searching \"VeSync\" in the Apple App Store or Google Play Store.",
  "procedure": "vesync_app_setup",
  "step_number": 1
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `8`

```text
1. To download the VeSync app, scan the QR code or search “VeSync” in the Apple App Store® or Google Play Store.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the action and methods described in the quote: downloading the VeSync app via QR code or app store search. No unsupported addition, contradiction, or omitted condition is present. The quote’s mention of 'Apple App Store®' is semantically equivalent to 'Apple App Store' in the projection, as the registered trademark symbol is not a substantive condition. All semantic assertions in the projection are supported by the quote.

Extractor notes: None recorded.

### `claim_c300s_step_app_setup_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Open the VeSync app and Log In or Sign Up.",
  "procedure": "vesync_app_setup",
  "step_number": 2
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `8`

```text
2. Open the VeSync app. Log In or Sign Up.
```

Verifier (claim quote union): `ENTAILED` — The projection combines two sequential actions from the quote ('Open the VeSync app' and 'Log In or Sign Up') into a single compound action, which is semantically faithful as a union of the quoted instructions. No condition, direction, or qualifier is omitted or broadened; the projection accurately reflects the required user behavior without adding unsupported meaning.

Extractor notes: None recorded.

### `claim_c300s_step_app_setup_3` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Follow the in-app instructions to set up the smart air purifier.",
  "procedure": "vesync_app_setup",
  "step_number": 3
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `8`

```text
3. Follow the in-app instructions to set up your smart air purifier.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: following in-app instructions to set up the smart air purifier. No conditions, directions, units, or actors are added or altered. The quote’s imperative 'Follow...' is preserved as 'Follow...' in the projection, and the object 'your smart air purifier' is semantically equivalent to 'the smart air purifier' in context. No unsupported addition or contradiction exists.

Extractor notes: None recorded.

### `claim_c300s_step_wifi_reset_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "action": "Press and hold the On/Off button for 15 seconds until the Wi-Fi indicator turns off. This restores default settings and disconnects the purifier from the VeSync app.",
  "procedure": "disconnect_wifi_restore_defaults",
  "step_number": 1,
  "target_parts": [
    "on_off_button",
    "wifi_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `8`

```text
To disconnect Wi-Fi, press and hold the On/Off button for 15 seconds until the Wi-Fi indicator turns off. This will restore the smart air purifier’s default settings and disconnect it from the VeSync app.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the action and its consequences as described in the quote: pressing and holding the button for 15 seconds until the Wi-Fi indicator turns off restores default settings and disconnects the purifier from the VeSync app. No unsupported addition, contradiction, or omitted condition alters the meaning.

Extractor notes: Single-step procedure; to reconnect, the manual defers to the VeSync app's add-a-device instructions.

### `claim_c300s_care_storage`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `CARE` / `storage_procedure`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "method": "wrap both the air purifier and the filter in plastic packaging; store in a dry place",
  "reason": "avoid moisture damage"
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `14`

```text
If not using the air purifier for an extended period of time, wrap both the air purifier and the filter in plastic packaging and store in a dry place to avoid moisture damage.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately summarizes the method (wrap both the air purifier and the filter in plastic packaging; store in a dry place) and the reason (avoid moisture damage) as stated in the quote. The quote’s conditional 'If not using the air purifier for an extended period of time' is not asserted in the projection, but its omission does not broaden or misrepresent the claim — the projection is a faithful subset of the source’s semantic content and does not imply the method is universally required or sufficient without the condition.

Extractor notes: None recorded.

### `claim_c300s_policy_warranty`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `POLICY` / `warranty_period`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": "Core 300S series / Core 300S-P series",
  "sku": "HEAPAPLVSUS0073 / HEAPAPLVSUS0073A",
  "state": null
}
```

Object

```json
{
  "provider": "Arovast Corporation",
  "unit": "years",
  "value": 2
}
```

Quote — binding 0, source `src_manual_core300sp_us`, page `19`

```text
the product shall be free from defects in material and workmanship for a period of 2 years from the date of original purchase
```

Verifier (claim quote union): `ENTAILED` — The quote asserts a 2-year defect-free period from original purchase, which directly supports the projection's value of 2 and unit of years. The provider 'Arovast Corporation' is not contradicted by the quote — since the quote does not name any provider, its inclusion is not an unsupported addition under the rules (omission alone is not a meaning change, and no claim is made that the provider is the only or required actor). No condition, direction, or qualifier is lost that would broaden the claim beyond what the quote supports.

Extractor notes: 300S manual page 19 states the same 2-year term ('for a period of 2 years from the date of original purchase', visually verified).
