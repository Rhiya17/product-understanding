# Review Proposals — graco-ready2jet-2212125

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `94`
- Existing human decisions: `1`
- Undecided claims covered here: `93`
- Proposed `NEEDS_RECHECK`: `79`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `14`
- Batch-eligible C0/C1: `2`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (79)

### `claim_r2j_care_beach_cleaning`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `beach_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'method':'complete cleaning after beach use', which implies a specific procedure not stated in the quote; the quote only says 'completely clean your stroller afterward' without specifying it as a 'method' or labeling it as 'after beach use' as a standalone category. Also, 'beach_cleaning' as predicate overgeneralizes the context — the quote is a conditional instruction ('WHEN USING...'), not a standalone category.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "contaminants": [
    "sand",
    "salt"
  ],
  "method": "complete cleaning after beach use",
  "targets": [
    "mechanisms",
    "wheel assemblies"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
WHEN USING YOUR STROLLER AT THE BEACH completely clean your stroller afterward to remove sand and salt from mechanisms and wheel assemblies.
```

Verifier: `MEANING_CHANGED` — The translation adds 'method':'complete cleaning after beach use', which implies a specific procedure not stated in the quote; the quote only says 'completely clean your stroller afterward' without specifying it as a 'method' or labeling it as 'after beach use' as a standalone category. Also, 'beach_cleaning' as predicate overgeneralizes the context — the quote is a conditional instruction ('WHEN USING...'), not a standalone category.

Extractor notes: C2 because the cleaning involves wheel-assembly removal (same bullet continues 'Push release button to remove wheel assemblies.', extracted as claim_r2j_step_wheel_removal_1).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_frame`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `frame_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation incorrectly implies that 'household soap' and 'warm water' are agents performing the cleaning, rather than materials to be used. The original quote does not assign agency to these items; it prescribes their use as tools or substances. This misattribution of actor changes the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "agents": [
    "household soap",
    "warm water"
  ],
  "restrictions": [
    "NO BLEACH or detergent"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
TO CLEAN STROLLER FRAME, use only household soap and warm water. NO BLEACH or detergent.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly implies that 'household soap' and 'warm water' are agents performing the cleaning, rather than materials to be used. The original quote does not assign agency to these items; it prescribes their use as tools or substances. This misattribution of actor changes the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_inspection`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `CARE` / `periodic_inspection`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation omits the imperative instruction to 'Replace or repair the parts as needed,' which is a critical action directive in the original. It also restructures the content into a schema that implies a static 'method' and 'restrictions' rather than conveying the active, conditional guidance of the source. This alters the operational meaning and removes user agency implied by 'as needed.'

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "method": "periodic_check",
  "restrictions": [
    "Use only Graco replacement parts"
  ],
  "targets": [
    "loose screws",
    "worn parts",
    "torn material or stitching"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
FROM TIME TO TIME CHECK YOUR STROLLER  for loose screws, worn parts, torn material or stitching. Replace or repair the parts as needed. Use only Graco replacement parts.
```

Verifier: `MEANING_CHANGED` — The translation omits the imperative instruction to 'Replace or repair the parts as needed,' which is a critical action directive in the original. It also restructures the content into a schema that implies a static 'method' and 'restrictions' rather than conveying the active, conditional guidance of the source. This alters the operational meaning and removes user agency implied by 'as needed.'

Extractor notes: Assigned C1 rather than C0 because the check targets structural wear affecting safe use; noted per the assign-higher-when-unsure rule.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_seat`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `seat_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation incorrectly assigns 'mild soap' as an agent rather than a cleaning agent/tool; 'agents' implies active doers, which misrepresents the source. Also, 'wipe_only' is not explicitly stated — the quote says 'should only be wiped', which is a recommendation, not an exclusive method. The structure implies the restrictions are properties of the method, but the quote lists them as separate imperative instructions.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "agents": [
    "mild soap"
  ],
  "method": "wipe_only",
  "restrictions": [
    "DO NOT MACHINE WASH SEAT",
    "taking care not to soak the material",
    "NO BLEACH"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
DO NOT MACHINE WASH SEAT. It should only be wiped with a mild soap, taking care not to soak the material. NO BLEACH.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 'mild soap' as an agent rather than a cleaning agent/tool; 'agents' implies active doers, which misrepresents the source. Also, 'wipe_only' is not explicitly stated — the quote says 'should only be wiped', which is a recommendation, not an exclusive method. The structure implies the restrictions are properties of the method, but the quote lists them as separate imperative instructions.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_sun_exposure`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `sun_heat_exposure`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds a prescriptive restriction 'avoid excessive exposure to sun or heat' which is not stated in the original quote. The original only describes a potential consequence ('could cause'), not a directive or care instruction. This addition changes the meaning from a warning to a command.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "effect": "fading or warping of parts",
  "restriction": "avoid excessive exposure to sun or heat"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
EXCESSIVE EXPOSURE TO SUN OR HEAT could cause fading or warping of parts.
```

Verifier: `MEANING_CHANGED` — The translation adds a prescriptive restriction 'avoid excessive exposure to sun or heat' which is not stated in the original quote. The original only describes a potential consequence ('could cause'), not a directive or care instruction. This addition changes the meaning from a warning to a command.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_wet_drying`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `drying_after_wet`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation replaces 'allow to dry thoroughly' with 'air dry thoroughly', which adds the specific method 'air' not present in the original. The original permits any drying method (e.g., towel, fan, sun) as long as it's thorough; the translation restricts it to air drying, altering the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "method": "open canopy and air dry thoroughly before storing"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
IF STROLLER BECOMES WET, open canopy and allow to dry thoroughly before storing.
```

Verifier: `MEANING_CHANGED` — The translation replaces 'allow to dry thoroughly' with 'air dry thoroughly', which adds the specific method 'air' not present in the original. The original permits any drying method (e.g., towel, fan, sun) as long as it's thorough; the translation restricts it to air drying, altering the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_care_wheel_oil`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `wheel_lubrication`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation omits the conditional 'IF WHEEL SQUEAKS', making the instruction unconditional, which changes the meaning. It also drops the instruction to 'get the oil into... as illustrated', removing the visual guidance and procedural nuance.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "agents": [
    "light oil",
    "3-in-1",
    "sewing machine oil"
  ],
  "target_location": "axle and wheel assembly"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
IF WHEEL SQUEAKS, use a light oil (e.g., 3-in-1, or sewing machine oil). It is important to get the oil into the axle and wheel assembly as illustrated.
```

Verifier: `MEANING_CHANGED` — The translation omits the conditional 'IF WHEEL SQUEAKS', making the instruction unconditional, which changes the meaning. It also drops the instruction to 'get the oil into... as illustrated', removing the visual guidance and procedural nuance.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_compat_graco_infant_car_seats`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `COMPATIBILITY` / `compatible_infant_car_seats`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds a verification instruction (calling customer service or scanning a code) not present in the quote, which changes the meaning by implying an action required to confirm compatibility, whereas the quote simply states compatibility without any condition or verification step.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "counterpart": "Graco infant car seats",
  "qualifier": "most",
  "verification": "Call Graco customer service 1-800-345-4109 or scan the in-manual code for compatibility."
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
TO AVOID INJURY TO YOUR CHILD: THIS PRODUCT IS COMPATIBLE WITH MOST GRACO® INFANT CAR SEATS.
```

Verifier: `MEANING_CHANGED` — The translation adds a verification instruction (calling customer service or scanning a code) not present in the quote, which changes the meaning by implying an action required to confirm compatibility, whereas the quote simply states compatibility without any condition or verification step.

Extractor notes: Generic manufacturer statement, not a per-model chart. Page 29 restates it without the word MOST ('COMPATIBLE WITH GRACO® INFANT CAR SEATS'); same source, so not recorded as a conflict. Per-model compatibility (e.g. SnugRide chart) is not in this product's vault.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_dimension_basket_capacity`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_storage_basket_weight`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation omits the metric equivalent (4.5 kg) and the imperative 'Do not', reducing a safety warning to a neutral limit statement, which alters the directive nature and completeness of the original.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "unit": "lb",
  "value": 10
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
Do not place more than 10 lb (4.5 kg) in the stroller storage basket
```

Verifier: `MEANING_CHANGED` — The translation omits the metric equivalent (4.5 kg) and the imperative 'Do not', reducing a safety warning to a neutral limit statement, which alters the directive nature and completeness of the original.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_limit_cup_holder_weight`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_cup_holder_weight`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation omits the stroller storage basket limit (10 lb / 4.5 kg) and only reports the cup holder limit (1 lb / 0.45 kg), thereby dropping critical information and altering the scope of the original warning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "unit": "lb",
  "value": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
Do not place more than 10 lb (4.5 kg) in the stroller storage basket, 1 lb (.45 kg) in the cup holder.
```

Verifier: `MEANING_CHANGED` — The translation omits the stroller storage basket limit (10 lb / 4.5 kg) and only reports the cup holder limit (1 lb / 0.45 kg), thereby dropping critical information and altering the scope of the original warning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_limit_max_height`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_child_height`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation presents 'maximum_child_height' as a hard limit, while the quote states exceeding 45 in. causes excessive wear and stress — implying risk or degradation, not a strict boundary. The quote also includes weight (50 lb) as a parallel condition, which the translation omits entirely.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "unit": "in",
  "value": 45
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier: `MEANING_CHANGED` — The translation presents 'maximum_child_height' as a hard limit, while the quote states exceeding 45 in. causes excessive wear and stress — implying risk or degradation, not a strict boundary. The quote also includes weight (50 lb) as a parallel condition, which the translation omits entirely.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_limit_max_weight`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_child_weight`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation reduces the warning to a single limit (maximum_child_weight: 50 lb) but omits the height restriction (taller than 45 in.) and the consequence (excessive wear and stress on the stroller), which are critical parts of the original meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "unit": "lb",
  "value": 50
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier: `MEANING_CHANGED` — The translation reduces the warning to a single limit (maximum_child_weight: 50 lb) but omits the height restriction (taller than 45 in.) and the consequence (excessive wear and stress on the stroller), which are critical parts of the original meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_limit_single_occupant`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_occupants`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The quote specifies 'only one child at a time' as a usage rule, implying exclusivity and safety constraint. The translation reifies this as a 'maximum_occupants' limit of 1, which structurally implies a capacity ceiling but omits the temporal restriction ('at a time') and the imperative tone ('Use... with only...'). This could mislead into thinking multiple children are allowed if not simultaneously, or that it’s merely a recommendation rather than a requirement.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "unit": "child",
  "value": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
Use the stroller with only one child at a time.
```

Verifier: `MEANING_CHANGED` — The quote specifies 'only one child at a time' as a usage rule, implying exclusivity and safety constraint. The translation reifies this as a 'maximum_occupants' limit of 1, which structurally implies a capacity ceiling but omits the temporal restriction ('at a time') and the imperative tone ('Use... with only...'). This could mislead into thinking multiple children are allowed if not simultaneously, or that it’s merely a recommendation rather than a requirement.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_part_belly_bar`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `belly_bar_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'across the front of the stroller seat' and implies a specific spatial location not stated in the quote; the quote only instructs to attach the belly bar to the mounts without specifying orientation or position relative to the stroller seat.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
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
    "page": 16,
    "source_id": "src_r2j_manual_v1"
  },
  "location_description": "Attaches across the front of the stroller seat into belly bar mounts.",
  "part": "belly_bar"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `16`

```text
Attach child’s belly bar onto belly bar mounts.
```

Verifier: `MEANING_CHANGED` — The translation adds 'across the front of the stroller seat' and implies a specific spatial location not stated in the quote; the quote only instructs to attach the belly bar to the mounts without specifying orientation or position relative to the stroller seat.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_part_click_connect_mounts`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `PART_LOCATION` / `click_connect_mounts_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation describes the location and function of the Click Connect™ mounts but omits the critical action 'push down on car seat until the latches snap' — a procedural instruction essential to the original meaning. The translation also adds 'In the stroller seat' and 'infant car seat latches', which are not in the quote, implying context not stated. This alters the directive nature of the original and adds unverified details.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
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
    "page": 31,
    "source_id": "src_r2j_manual_v1"
  },
  "location_description": "In the stroller seat; the infant car seat latches snap into these mounts.",
  "part": "click_connect_mounts"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `31`

```text
push down on car seat until the latches snap into the Click Connect™ mounts.
```

Verifier: `MEANING_CHANGED` — The translation describes the location and function of the Click Connect™ mounts but omits the critical action 'push down on car seat until the latches snap' — a procedural instruction essential to the original meaning. The translation also adds 'In the stroller seat' and 'infant car seat latches', which are not in the quote, implying context not stated. This alters the directive nature of the original and adds unverified details.

Extractor notes: Location wording 'in the stroller seat' grounded in the page 31 text 'Find mounts in seat.'; diagram on page 31 labels the mount.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_part_handle_lever`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `handle_lever_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote 'squeeze handle lever' is a simple imperative action, while the translation adds specific spatial and procedural details (underside of stroller handle, after sliding thumb switch) not present in the original, altering meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
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
    "page": 34,
    "source_id": "src_r2j_manual_v1"
  },
  "location_description": "Located on the underside of the stroller handle, squeezed after sliding the thumb switch.",
  "part": "handle_lever"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
squeeze handle lever
```

Verifier: `MEANING_CHANGED` — The quote 'squeeze handle lever' is a simple imperative action, while the translation adds specific spatial and procedural details (underside of stroller handle, after sliding thumb switch) not present in the original, altering meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_part_thumb_switch`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `thumb_switch_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote 'slide thumb switch' describes an action or feature (sliding), while the translation describes a static location ('Located on the top center of the stroller handle'), omitting the action and adding spatial detail not present in the original.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
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
    "page": 34,
    "source_id": "src_r2j_manual_v1"
  },
  "location_description": "Located on the top center of the stroller handle.",
  "part": "thumb_switch"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
slide thumb switch
```

Verifier: `MEANING_CHANGED` — The quote 'slide thumb switch' describes an action or feature (sliding), while the translation describes a static location ('Located on the top center of the stroller handle'), omitting the action and adding spatial detail not present in the original.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_spec_assembly_no_tools`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `assembly_tools_required`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'to assemble the stroller,' which specifies a context (assembly of a stroller) not present in the original quote. The original is a general statement with no subject or action限定, while the translation implies a specific use case, altering the scope and meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "detail": "No tools are required to assemble the stroller.",
  "value": "none"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `10`

```text
No tools required.
```

Verifier: `MEANING_CHANGED` — The translation adds 'to assemble the stroller,' which specifies a context (assembly of a stroller) not present in the original quote. The original is a general statement with no subject or action限定, while the translation implies a specific use case, altering the scope and meaning.

Extractor notes: Only spec-type fact literally stated in the manual text. Core specs (product weight, open/folded dimensions, box contents enumeration, warranty terms) are absent from the manual — see gaps.json gap_specs_1.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_step_belly_bar_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation merges two distinct instructions — 'Attach...' and 'CHECK...' — into a single action ('Attach...; check...'), implying they are part of one continuous step without emphasizing the CHECK as a separate verification step. The original explicitly uses 'CHECK' in all caps, signaling a mandatory verification, which the translation downgrades to a casual conjunction. This alters the procedural emphasis and intent.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Attach child's belly bar onto belly bar mounts; check that the Graco logo is aligned.",
  "procedure": "belly_bar",
  "step_number": 1,
  "target_parts": [
    "belly_bar",
    "belly_bar_mounts"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `16`

```text
Attach child’s belly bar onto belly bar mounts. CHECK that Graco logo is aligned as shown.
```

Verifier: `MEANING_CHANGED` — The translation merges two distinct instructions — 'Attach...' and 'CHECK...' — into a single action ('Attach...; check...'), implying they are part of one continuous step without emphasizing the CHECK as a separate verification step. The original explicitly uses 'CHECK' in all caps, signaling a mandatory verification, which the translation downgrades to a casual conjunction. This alters the procedural emphasis and intent.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_belly_bar_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure step with numbered sequence and part references, whereas the quote is a simple imperative instruction without any such context.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Pull on child's belly bar to ensure it is secure.",
  "procedure": "belly_bar",
  "step_number": 2,
  "target_parts": [
    "belly_bar"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `17`

```text
Pull on child’s belly bar to ensure it is secure.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure step with numbered sequence and part references, whereas the quote is a simple imperative instruction without any such context.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_belly_bar_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (type, predicate, object with step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure step with identifiers the source does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To remove child's belly bar, press buttons on inside of both ends, and pull off.",
  "procedure": "belly_bar",
  "step_number": 3,
  "target_parts": [
    "belly_bar"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `17`

```text
To remove child’s belly bar, press buttons on inside of both ends, and pull off.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (type, predicate, object with step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure step with identifiers the source does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_brake_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (type, predicate, object with step_number, target_parts) not present in the original quote. The original is a simple imperative instruction; the translation reifies it as a formal procedure step with attributes like 'step_number':1 and 'target_parts':['brakes'], which are not stated or implied in the source. This constitutes an addition of information and structural interpretation beyond the quote’s scope.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Push down on brake to lock brakes.",
  "procedure": "brake",
  "step_number": 1,
  "target_parts": [
    "brakes"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `20`

```text
Push down on brake to lock brakes.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (type, predicate, object with step_number, target_parts) not present in the original quote. The original is a simple imperative instruction; the translation reifies it as a formal procedure step with attributes like 'step_number':1 and 'target_parts':['brakes'], which are not stated or implied in the source. This constitutes an addition of information and structural interpretation beyond the quote’s scope.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_brake_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (e.g., 'procedure', 'step_number', 'target_parts') not present in the original quote. The original is a simple imperative instruction; the translation frames it as a formal procedure step with numbered context and part references, which alters the meaning by implying structure and context the source does not provide.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Push up on brake to unlock brakes.",
  "procedure": "brake",
  "step_number": 2,
  "target_parts": [
    "brakes"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `20`

```text
Push up on brake to unlock brakes.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (e.g., 'procedure', 'step_number', 'target_parts') not present in the original quote. The original is a simple imperative instruction; the translation frames it as a formal procedure step with numbered context and part references, which alters the meaning by implying structure and context the source does not provide.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_canopy_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (type, predicate, object with fields like 'step_number', 'target_parts') not present in the original quote. The original is a simple imperative instruction; the translation reifies it as a formal procedure step with attributes, which changes the meaning by implying structure, context, and metadata the source does not contain.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Pull forward to open canopy.",
  "procedure": "canopy",
  "step_number": 1,
  "target_parts": [
    "canopy"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `19`

```text
Pull forward to open canopy.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (type, predicate, object with fields like 'step_number', 'target_parts') not present in the original quote. The original is a simple imperative instruction; the translation reifies it as a formal procedure step with attributes, which changes the meaning by implying structure, context, and metadata the source does not contain.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_canopy_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (e.g., 'step_number': 2, 'target_parts': ['canopy']) not present in the original quote. The original is a simple imperative instruction; the translation implies a procedural step with numbered sequence and part targeting, which alters meaning by introducing unverified context.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Push backwards to close canopy.",
  "procedure": "canopy",
  "step_number": 2,
  "target_parts": [
    "canopy"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `19`

```text
Push backwards to close canopy.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (e.g., 'step_number': 2, 'target_parts': ['canopy']) not present in the original quote. The original is a simple imperative instruction; the translation implies a procedural step with numbered sequence and part targeting, which alters meaning by introducing unverified context.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_canopy_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation reformats the instruction as a structured procedure step with metadata (e.g., 'step_number': 3, 'target_parts': ['canopy_visor']), which is not present in the original quote. The original is a simple imperative sentence without any procedural numbering or part labeling. Adding such structure implies a context and organization not stated, thus changing the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Pull canopy visor out for use; push back under rim of canopy when not in use.",
  "procedure": "canopy",
  "step_number": 3,
  "target_parts": [
    "canopy_visor"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `19`

```text
Pull canopy visor out for use, push back under rim of canopy when not in use.
```

Verifier: `MEANING_CHANGED` — The translation reformats the instruction as a structured procedure step with metadata (e.g., 'step_number': 3, 'target_parts': ['canopy_visor']), which is not present in the original quote. The original is a simple imperative sentence without any procedural numbering or part labeling. Adding such structure implies a context and organization not stated, thus changing the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_car_seat_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure: 'attach_car_seat', step_number: 1, target_parts: ['seat','canopy']) not present in the original quote. The original is a simple imperative instruction without any procedural context, step numbering, or part labeling — adding these constitutes a meaning change.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Recline the stroller seat back to its lowest position. Fold the canopy.",
  "procedure": "attach_car_seat",
  "step_number": 1,
  "target_parts": [
    "seat",
    "canopy"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `30`

```text
Recline the stroller seat back to its lowest position. Fold the canopy.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure: 'attach_car_seat', step_number: 1, target_parts: ['seat','canopy']) not present in the original quote. The original is a simple imperative instruction without any procedural context, step numbering, or part labeling — adding these constitutes a meaning change.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_car_seat_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote. The quote is a simple imperative; the translation implies a specific procedure context and part names, altering the meaning by introducing unstated conditions and scope.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Find mounts in seat.",
  "procedure": "attach_car_seat",
  "step_number": 2,
  "target_parts": [
    "click_connect_mounts"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `31`

```text
Find mounts in seat.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote. The quote is a simple imperative; the translation implies a specific procedure context and part names, altering the meaning by introducing unstated conditions and scope.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_car_seat_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation drops the trademark symbol '™' from 'Click Connect™ mounts', which may imply a generic term rather than a branded, proprietary system, potentially altering legal or technical specificity.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Insert car seat into stroller and push down on car seat until the latches snap into the Click Connect mounts.",
  "procedure": "attach_car_seat",
  "step_number": 3,
  "target_parts": [
    "infant_car_seat",
    "click_connect_mounts"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `31`

```text
Insert car seat into stroller and push down on car seat until the latches snap into the Click Connect™ mounts.
```

Verifier: `MEANING_CHANGED` — The translation drops the trademark symbol '™' from 'Click Connect™ mounts', which may imply a generic term rather than a branded, proprietary system, potentially altering legal or technical specificity.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_car_seat_4`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure context the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Check that infant car seat is securely attached by pulling up on it.",
  "procedure": "attach_car_seat",
  "step_number": 4,
  "target_parts": [
    "infant_car_seat"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `32`

```text
Check that infant car seat is  securely attached by pulling  up on it.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure context the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_car_seat_5`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying a formalized procedure step with identifiers and context not stated in the original.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To remove car seat: squeeze release handle at back of car seat, and lift car seat out of the stroller.",
  "procedure": "attach_car_seat",
  "step_number": 5,
  "target_parts": [
    "car_seat_release_handle",
    "infant_car_seat"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `32`

```text
To remove car seat: squeeze release handle at back of car seat, and lift car seat out of the stroller.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying a formalized procedure step with identifiers and context not stated in the original.

Extractor notes: Removal action; kept in the attach_car_seat procedure as step 5 to mirror the manual's own numbering in section 4-G.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_cup_holder_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying a formalized, numbered procedure with identified parts — information not stated or implied in the original instruction.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Line up opening in cup holder with mount on stroller and press onto stroller tube.",
  "procedure": "attach_cup_holder",
  "step_number": 1,
  "target_parts": [
    "cup_holder",
    "cup_holder_mount",
    "stroller_tube"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `18`

```text
Line up opening in cup holder with mount on stroller and press onto stroller tube.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying a formalized, numbered procedure with identified parts — information not stated or implied in the original instruction.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_cup_holder_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and part identifiers that the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "MAKE SURE cup holder is snapped securely into mount by pulling down.",
  "procedure": "attach_cup_holder",
  "step_number": 2,
  "target_parts": [
    "cup_holder",
    "cup_holder_mount"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `18`

```text
MAKE SURE cup holder is snapped securely into mount by pulling down.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and part identifiers that the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_cup_holder_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (e.g., 'procedure', 'step_number', 'target_parts') not present in the source quote, which alters the meaning by implying a formal procedure step with numbered sequence and part references that the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To remove, pull up on cup holder.",
  "procedure": "attach_cup_holder",
  "step_number": 3,
  "target_parts": [
    "cup_holder"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `18`

```text
To remove, pull up on cup holder.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (e.g., 'procedure', 'step_number', 'target_parts') not present in the source quote, which alters the meaning by implying a formal procedure step with numbered sequence and part references that the original does not state.

Extractor notes: Use-limit context for this accessory already extracted elsewhere: 1 lb (.45 kg) maximum load (claim_r2j_limit_cup_holder_weight), no hot liquids (claim_r2j_warning_hot_liquids), top-rack dishwasher cleaning (claim_r2j_care_cup_holder).

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata not present in the quote, such as 'initial_state', 'resulting_state', 'step_number', and 'target_parts', which alter the meaning by implying a formal state machine or procedural framework not stated in the original. The quote is a simple imperative; the translation encodes it as a structured step with side effects and state transitions.

Applicability

```json
{
  "condition": "if car seat is in use",
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Remove infant car seat if in use.",
  "initial_state": "OPEN_WITH_CAR_SEAT",
  "procedure": "fold_stroller",
  "resulting_state": "OPEN",
  "step_number": 1,
  "target_parts": [
    "infant_car_seat"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `33`

```text
1. Before folding stroller: (a) remove infant car seat if in use
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata not present in the quote, such as 'initial_state', 'resulting_state', 'step_number', and 'target_parts', which alter the meaning by implying a formal state machine or procedural framework not stated in the original. The quote is a simple imperative; the translation encodes it as a structured step with side effects and state transitions.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (initial_state, resulting_state, step_number, target_parts, procedure) not present in the source quote, which only states '(b) unlock brakes' — a simple imperative. These additions imply context and state transitions the original does not specify.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Unlock brakes.",
  "initial_state": "OPEN",
  "procedure": "fold_stroller",
  "resulting_state": "OPEN_UNBRAKED",
  "step_number": 2,
  "target_parts": [
    "brakes"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `33`

```text
(b) unlock brakes
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (initial_state, resulting_state, step_number, target_parts, procedure) not present in the source quote, which only states '(b) unlock brakes' — a simple imperative. These additions imply context and state transitions the original does not specify.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context (step number, initial/resulting states, target parts, procedure name) not present in the source quote, which only states 'fold the canopy' without any conditions, sequence, or state changes.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Fold the canopy.",
  "initial_state": "OPEN_UNBRAKED",
  "procedure": "fold_stroller",
  "resulting_state": "OPEN_CANOPY_FOLDED",
  "step_number": 3,
  "target_parts": [
    "canopy"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `33`

```text
(c) fold the canopy.
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context (step number, initial/resulting states, target parts, procedure name) not present in the source quote, which only states 'fold the canopy' without any conditions, sequence, or state changes.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_4`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'initial_state: OPEN_CANOPY_FOLDED' and 'resulting_state: FOLD_SWITCH_SLID', which are not mentioned in the quote. The quote only states to slide the thumb switch as part of folding the stroller, without specifying any state before or after. These added states constitute an unwarranted expansion of meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Slide thumb switch.",
  "initial_state": "OPEN_CANOPY_FOLDED",
  "procedure": "fold_stroller",
  "resulting_state": "FOLD_SWITCH_SLID",
  "step_number": 4,
  "target_parts": [
    "thumb_switch"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
2. To fold stroller: (a) slide thumb switch;
```

Verifier: `MEANING_CHANGED` — The translation adds 'initial_state: OPEN_CANOPY_FOLDED' and 'resulting_state: FOLD_SWITCH_SLID', which are not mentioned in the quote. The quote only states to slide the thumb switch as part of folding the stroller, without specifying any state before or after. These added states constitute an unwarranted expansion of meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_5`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context (step number, initial/resulting states, target parts, procedure name) not present in the exact quote 'squeeze handle lever', which is a bare imperative. The quote does not specify any state transitions, step ordering, or system-specific identifiers like 'FOLD_SWITCH_SLID' or 'FOLD_LEVER_SQUEEZED'.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Squeeze handle lever.",
  "initial_state": "FOLD_SWITCH_SLID",
  "procedure": "fold_stroller",
  "resulting_state": "FOLD_LEVER_SQUEEZED",
  "step_number": 5,
  "target_parts": [
    "handle_lever"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
(b) squeeze handle lever
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context (step number, initial/resulting states, target parts, procedure name) not present in the exact quote 'squeeze handle lever', which is a bare imperative. The quote does not specify any state transitions, step ordering, or system-specific identifiers like 'FOLD_SWITCH_SLID' or 'FOLD_LEVER_SQUEEZED'.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_6`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context (fold_stroller, step_number 6, initial_state, resulting_state, target_parts) not present in the quote, which only states a generic instruction to check stroller security without specifying conditions, steps, or parts.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Check that the stroller is secure.",
  "initial_state": "FOLD_LEVER_SQUEEZED",
  "procedure": "fold_stroller",
  "resulting_state": "FOLDED_SECURED",
  "step_number": 6,
  "target_parts": [
    "stroller_frame"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `35`

```text
3. CHECK that the stroller is secure.
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context (fold_stroller, step_number 6, initial_state, resulting_state, target_parts) not present in the quote, which only states a generic instruction to check stroller security without specifying conditions, steps, or parts.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_7`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context (e.g., 'FOLDED_SECURED', 'fold_stroller', 'step_number:7') and state transitions not present in the original quote, which only states 'Carry by belly bar.' without any conditions, steps, or target part specifications.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Carry by belly bar.",
  "initial_state": "FOLDED_SECURED",
  "procedure": "fold_stroller",
  "resulting_state": "FOLDED_CARRIED",
  "step_number": 7,
  "target_parts": [
    "belly_bar"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `35`

```text
4. Carry by belly bar.
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context (e.g., 'FOLDED_SECURED', 'fold_stroller', 'step_number:7') and state transitions not present in the original quote, which only states 'Carry by belly bar.' without any conditions, steps, or target part specifications.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_tips_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation wraps the exact quote into a structured object with added metadata (procedure, step_number, type, predicate) not present in the source. This adds procedural context and categorization the original quote does not contain, altering its meaning by implying it is a formal step in a stroller-folding procedure, which the source does not specify.

Applicability

```json
{
  "condition": "optional for more compact fold",
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Rotate cup holder for more compact fold.",
  "procedure": "fold_stroller_tips",
  "step_number": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
Rotate cup holder for more compact fold.
```

Verifier: `MEANING_CHANGED` — The translation wraps the exact quote into a structured object with added metadata (procedure, step_number, type, predicate) not present in the source. This adds procedural context and categorization the original quote does not contain, altering its meaning by implying it is a formal step in a stroller-folding procedure, which the source does not specify.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_fold_tips_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation wraps the exact quote inside a structured object with added metadata (procedure, step_number, type, predicate) that is not present in the source. This adds information and context not stated in the original quote, altering its meaning by implying a procedural structure and categorization the source does not provide.

Applicability

```json
{
  "condition": "optional to position wheels",
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Pull stroller to rotate front wheels as shown.",
  "procedure": "fold_stroller_tips",
  "step_number": 2
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `34`

```text
Pull stroller to rotate front wheels as shown.
```

Verifier: `MEANING_CHANGED` — The translation wraps the exact quote inside a structured object with added metadata (procedure, step_number, type, predicate) that is not present in the source. This adds information and context not stated in the original quote, altering its meaning by implying a procedural structure and categorization the source does not provide.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_footrest_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the original quote, which alters the meaning by implying a formalized procedure with numbered steps and specific parts — information not stated or implied in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To raise footrest, lift up as shown.",
  "procedure": "adjust_footrest",
  "step_number": 1,
  "target_parts": [
    "footrest"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `21`

```text
To raise footrest, lift up as shown.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the original quote, which alters the meaning by implying a formalized procedure with numbered steps and specific parts — information not stated or implied in the source.

Extractor notes: 'as shown' refers to the page 21 illustration; the raising action itself is stated in text, so this is not a diagram-only step.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_footrest_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation incorrectly treats the entire quote as an 'action' field within an object, while the quote is a procedural instruction. The original does not specify step number, procedure name, or target parts — these are added by the translation, which alters meaning by imposing structure and metadata not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To lower, press buttons on bottom of foot rest and raise or lower footrest.",
  "procedure": "adjust_footrest",
  "step_number": 2,
  "target_parts": [
    "footrest",
    "footrest_buttons"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `21`

```text
To lower, press buttons on bottom of foot rest and raise or lower footrest.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly treats the entire quote as an 'action' field within an object, while the quote is a procedural instruction. The original does not specify step number, procedure name, or target parts — these are added by the translation, which alters meaning by imposing structure and metadata not present in the source.

Extractor notes: Manual's step 2 is headed 'To lower' but its own text says 'raise or lower footrest'; the buttons are needed only for lowering (step 1 raises without them). 'foot rest' spacing is verbatim from the manual.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_front_wheels_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (step_number: 1, procedure: 'attach_front_wheels', target_parts: ['front_wheels']) not present in the quote, which implies a specific procedural context and part list the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Attach front wheels to stroller.",
  "procedure": "attach_front_wheels",
  "step_number": 1,
  "target_parts": [
    "front_wheels"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `15`

```text
Attach front wheels to stroller as shown.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (step_number: 1, procedure: 'attach_front_wheels', target_parts: ['front_wheels']) not present in the quote, which implies a specific procedural context and part list the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_front_wheels_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying context and specificity the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Check that wheels are securely attached by pulling on wheel assemblies.",
  "procedure": "attach_front_wheels",
  "step_number": 2,
  "target_parts": [
    "front_wheels"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `15`

```text
CHECK that wheels are securely attached by pulling on wheel assemblies.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying context and specificity the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and specific components, whereas the quote is a simple imperative instruction without any procedural context or part labeling.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To open, press button on buckle to release the waist straps.",
  "procedure": "secure_child_5pt",
  "step_number": 1,
  "target_parts": [
    "harness_buckle",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `23`

```text
To open, press button on buckle to release the waist straps.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and specific components, whereas the quote is a simple imperative instruction without any procedural context or part labeling.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To close, slide shoulder strap connectors onto waist straps and insert into buckle.",
  "procedure": "secure_child_5pt",
  "step_number": 2,
  "target_parts": [
    "shoulder_strap_connectors",
    "waist_straps",
    "harness_buckle"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `23`

```text
To close, slide shoulder strap  connectors onto waist straps and insert into buckle.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (convert_to_3pt_harness) and step order that the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To open, press button on buckle to release the waist straps.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 1,
  "target_parts": [
    "harness_buckle",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `24`

```text
To open, press button on buckle to release the waist straps.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (convert_to_3pt_harness) and step order that the original does not state.

Extractor notes: First step of the '3 Point Harness' section (page 24). Identical wording to secure_child_5pt step 1 (page 23); the manual restates it at the start of the conversion sequence.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying context and structure the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Slide shoulder strap connectors off of waist straps.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 2,
  "target_parts": [
    "shoulder_strap_connectors",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `24`

```text
Slide shoulder strap connectors off of waist straps.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying context and structure the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context ('procedure':'convert_to_3pt_harness', 'step_number':3) and structure ('target_parts') not present in the original quote, which is a simple imperative instruction without any step number, procedure name, or part list. This constitutes an addition of information that changes the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Remove shoulder straps from stroller.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 3,
  "target_parts": [
    "shoulder_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `25`

```text
Remove shoulder straps from stroller.
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context ('procedure':'convert_to_3pt_harness', 'step_number':3) and structure ('target_parts') not present in the original quote, which is a simple imperative instruction without any step number, procedure name, or part list. This constitutes an addition of information that changes the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_4`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (3pt harness conversion, step 4) not stated in the original.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Attach waist straps to harness buckle as shown.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 4,
  "target_parts": [
    "waist_straps",
    "harness_buckle"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `25`

```text
Attach waist straps to harness buckle as shown.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (3pt harness conversion, step 4) not stated in the original.

Extractor notes: 'as shown' refers to the page 25 illustration of the 3-point buckle configuration; the attaching action itself is stated in text.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_5`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context ('procedure':'convert_to_3pt_harness', 'step_number':5, 'target_parts':['slide_adjuster','waist_straps']) not present in the source quote, which only states a general instruction without specifying a procedure, step number, or target parts.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Use slide adjuster at waist for tighter adjustment.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 5,
  "target_parts": [
    "slide_adjuster",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `26`

```text
Use slide adjuster at waist for tighter adjustment.
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context ('procedure':'convert_to_3pt_harness', 'step_number':5, 'target_parts':['slide_adjuster','waist_straps']) not present in the source quote, which only states a general instruction without specifying a procedure, step number, or target parts.

Extractor notes: Manual numbers the 3 Point Harness section continuously: steps 1-4 perform the conversion; steps 5-6 are use of the converted 3-point harness.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_3pt_6`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (3pt harness conversion) and step sequence that the original quote does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To open, press button on buckle to release the waist straps.",
  "procedure": "convert_to_3pt_harness",
  "step_number": 6,
  "target_parts": [
    "harness_buckle",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `26`

```text
To open, press button on buckle to release the waist straps.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a specific context (3pt harness conversion) and step sequence that the original quote does not state.

Extractor notes: Opening the converted 3-point harness; the manual keeps this in the same numbered sequence as the conversion steps.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_height_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Use slide adjuster for further adjustment.",
  "procedure": "adjust_harness_height",
  "step_number": 2,
  "target_parts": [
    "slide_adjuster"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `27`

```text
Use slide adjuster for further adjustment.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_harness_height_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which implies specific system context and part names (e.g., 'adjust_harness_height', 'shoulder_straps', 'waist_straps') that are not stated or implied in the original text. This constitutes an addition of information and reinterpretation beyond the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Use slide adjuster at shoulder and waist for further adjustment. Repeat on other side.",
  "procedure": "adjust_harness_height",
  "step_number": 3,
  "target_parts": [
    "slide_adjuster",
    "shoulder_straps",
    "waist_straps"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `27`

```text
Use slide adjuster at shoulder and waist for further adjustment. Repeat on other side.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which implies specific system context and part names (e.g., 'adjust_harness_height', 'shoulder_straps', 'waist_straps') that are not stated or implied in the original text. This constitutes an addition of information and reinterpretation beyond the source.

Extractor notes: This instruction is present as text on page 27 but is unnumbered in the manual (it sits beside the labeled diagram); numbered 3 here to keep the procedure sequence contiguous. Not diagram-only: the action, including 'Repeat on other side.', is stated in text.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_rear_wheels_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds specific procedural context ('attach_rear_wheels', 'step_number': 2, 'target_parts': ['rear_wheels']) not present in the quote, which generically refers to 'wheels' without specifying rear wheels or step number, thus altering the scope and meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Check that wheels are securely attached by pulling on wheel assemblies.",
  "procedure": "attach_rear_wheels",
  "step_number": 2,
  "target_parts": [
    "rear_wheels"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `14`

```text
CHECK that wheels are securely attached by pulling on wheel assemblies.
```

Verifier: `MEANING_CHANGED` — The translation adds specific procedural context ('attach_rear_wheels', 'step_number': 2, 'target_parts': ['rear_wheels']) not present in the quote, which generically refers to 'wheels' without specifying rear wheels or step number, thus altering the scope and meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_recline_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying context and structure the original does not state.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To raise, pull both straps up.",
  "procedure": "recline_seat",
  "step_number": 2,
  "target_parts": [
    "recline_straps",
    "seat"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `22`

```text
To raise, pull both straps up.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which changes the meaning by implying context and structure the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_unfold_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'initial_state':'FOLDED' and 'resulting_state':'UNFOLD_SWITCH_SLID', which are not mentioned in the source quote; it also implies a state transition not stated, thereby altering the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Slide thumb switch.",
  "initial_state": "FOLDED",
  "procedure": "unfold_stroller",
  "resulting_state": "UNFOLD_SWITCH_SLID",
  "step_number": 1,
  "target_parts": [
    "thumb_switch"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `12`

```text
1. To open stroller: (a) slide thumb switch;
```

Verifier: `MEANING_CHANGED` — The translation adds 'initial_state':'FOLDED' and 'resulting_state':'UNFOLD_SWITCH_SLID', which are not mentioned in the source quote; it also implies a state transition not stated, thereby altering the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_unfold_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (initial_state, procedure, resulting_state, step_number, target_parts) not present in the quote, which alters the meaning by implying context and structure the original does not provide.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Squeeze handle lever and lift up.",
  "initial_state": "UNFOLD_SWITCH_SLID",
  "procedure": "unfold_stroller",
  "resulting_state": "UNFOLDING",
  "step_number": 2,
  "target_parts": [
    "handle_lever"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `12`

```text
(b) squeeze handle lever and lift up
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (initial_state, procedure, resulting_state, step_number, target_parts) not present in the quote, which alters the meaning by implying context and structure the original does not provide.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_unfold_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds procedural context (e.g., 'UNFOLDING', 'OPEN_LATCH_STATUS_UNVERIFIED', 'step_number': 3, 'target_parts') and structure not present in the source quote '(c) lift up handle', which is a simple imperative instruction without any state, step number, or system status.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Lift up handle.",
  "initial_state": "UNFOLDING",
  "procedure": "unfold_stroller",
  "resulting_state": "OPEN_LATCH_STATUS_UNVERIFIED",
  "step_number": 3,
  "target_parts": [
    "handle"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `12`

```text
(c) lift up handle
```

Verifier: `MEANING_CHANGED` — The translation adds procedural context (e.g., 'UNFOLDING', 'OPEN_LATCH_STATUS_UNVERIFIED', 'step_number': 3, 'target_parts') and structure not present in the source quote '(c) lift up handle', which is a simple imperative instruction without any state, step number, or system status.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_unfold_4`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (e.g., 'initial_state', 'resulting_state', 'step_number', 'target_parts') not present in the original quote, which alters the meaning by implying a formal procedure state machine and part targeting not stated in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "CHECK that the stroller is completely latched open every time you open the stroller.",
  "initial_state": "OPEN_LATCH_STATUS_UNVERIFIED",
  "procedure": "unfold_stroller",
  "resulting_state": "OPEN_LATCH_VERIFIED",
  "step_number": 4,
  "target_parts": [
    "stroller_frame"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `13`

```text
2. CHECK that the stroller is completely latched open every time you open the stroller and before continuing with the rest of the assembly steps.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (e.g., 'initial_state', 'resulting_state', 'step_number', 'target_parts') not present in the original quote, which alters the meaning by implying a formal procedure state machine and part targeting not stated in the source.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_step_wheel_removal_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and specific part identifiers, whereas the quote is a simple imperative instruction.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Push release button to remove wheel assemblies.",
  "procedure": "remove_wheels",
  "step_number": 1,
  "target_parts": [
    "wheel_release_button",
    "wheel_assemblies"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
Push release button to remove wheel assemblies.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formalized procedure with numbered steps and specific part identifiers, whereas the quote is a simple imperative instruction.

Extractor notes: The manual's only wheel-removal instruction (Care & Maintenance, beach-cleaning bullet; pages 14-15 point here via 'For wheel removal see Care & Maintenance.'). Release button location is shown only in the page 36 illustration; text states the action only.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_r2j_warning_adult_assembly`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `adult_assembly_required`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (hazard_type: 'general_safety', type: 'WARNING') not present in the original quote, which only states 'ADULT ASSEMBLY REQUIRED.' without any classification or hazard context. This constitutes an addition of information that changes the meaning by implying a safety warning category not stated in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Adult assembly required.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
ADULT ASSEMBLY REQUIRED.
```

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (hazard_type: 'general_safety', type: 'WARNING') not present in the original quote, which only states 'ADULT ASSEMBLY REQUIRED.' without any classification or hazard context. This constitutes an addition of information that changes the meaning by implying a safety warning category not stated in the source.

Extractor notes: Assigned C3 per work-order rule that every safety warning in the manual is a C3 WARNING claim, although this is an assembly requirement rather than an in-use hazard.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_apply_both_brakes`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `apply_both_brakes`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'hazard_type':'rolling_hazard', which is not stated or implied in the exact quote. The quote is a procedural warning, not a classified hazard type; adding this qualifier changes the meaning by introducing a categorization not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Always apply both brakes; check that brakes are on by trying to push the stroller.",
  "hazard_type": "rolling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `20`

```text
Always apply both brakes. Check that brakes are on by trying to  push stroller.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type':'rolling_hazard', which is not stated or implied in the exact quote. The quote is a procedural warning, not a classified hazard type; adding this qualifier changes the meaning by introducing a categorization not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_basket_overload`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `basket_overload_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'the basket' as the specific object being overloaded, which is not mentioned in the original quote. The original refers generically to 'EXCESSIVE WEIGHT' without specifying what is being overloaded, while the translation narrows it to 'basket', introducing a specific context not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Overloading the basket can create a hazardous unstable condition.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
EXCESSIVE WEIGHT MAY CAUSE A HAZARDOUS UNSTABLE CONDITION TO EXIST.
```

Verifier: `MEANING_CHANGED` — The translation adds 'the basket' as the specific object being overloaded, which is not mentioned in the original quote. The original refers generically to 'EXCESSIVE WEIGHT' without specifying what is being overloaded, while the translation narrows it to 'basket', introducing a specific context not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_belly_bar_not_restraint`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `belly_bar_not_restraint`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation merges three distinct instructions into a single compound sentence, implying they are equally weighted or causally linked, whereas the original separates them for emphasis. The original explicitly commands to 'Always secure your child with the seat belt' as a primary directive, then states 'The belly bar is not a restraint device' as a standalone warning, and finally adds a conditional caution about installation. The translation collapses these into a single clause, potentially diminishing the imperative force of the seat belt instruction and conflating the warning about the belly bar’s non-restraint status with the installation caution. This restructuring alters the emphasis and hierarchical intent of the original safety instructions.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "The belly bar is not a restraint device; always secure the child with the seat belt, and use care when installing the belly bar with a child in the stroller.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `16`

```text
Always secure your child with the seat belt. The belly bar is not a restraint device. Use care when installing the belly bar on the stroller with a child in the stroller.
```

Verifier: `MEANING_CHANGED` — The translation merges three distinct instructions into a single compound sentence, implying they are equally weighted or causally linked, whereas the original separates them for emphasis. The original explicitly commands to 'Always secure your child with the seat belt' as a primary directive, then states 'The belly bar is not a restraint device' as a standalone warning, and finally adds a conditional caution about installation. The translation collapses these into a single clause, potentially diminishing the imperative force of the seat belt instruction and conflating the warning about the belly bar’s non-restraint status with the installation caution. This restructuring alters the emphasis and hierarchical intent of the original safety instructions.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_car_seat_other_brands`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_brand_restriction`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'hazard_type': 'child_restraint_hazard' and 'type': 'WARNING', which are not present in the original quote. These additions introduce new categorical and typological information not stated in the source, altering the meaning by implying a formal hazard classification and warning type that the original text does not specify.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Improper use of this stroller with other manufacturers' car seats may result in serious injury or death.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
Improper use of this stroller with other manufacturers’ car seats may result in serious injury or death.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type': 'child_restraint_hazard' and 'type': 'WARNING', which are not present in the original quote. These additions introduce new categorical and typological information not stated in the source, altering the meaning by implying a formal hazard classification and warning type that the original text does not specify.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_car_seat_read_manual`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_manual_required_reading`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'see the car seat owner's manual for maximum child size,' which is not mentioned in the exact quote. This introduces new information not present in the source, altering the meaning. The translation adds the instruction to 'read the manual... before using it with the stroller,' which is not mentioned in the quote. The quote only directs users to see the manual for the maximum child size; it does not mention strollers or pre-use reading requirements.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Read the manual provided with the Graco car seat before using it with the stroller; see the car seat owner's manual for maximum child size.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
READ THE MANUAL provided with your Graco car seat before using it with your stroller.
```

Verifier: `MEANING_CHANGED` — The translation adds 'see the car seat owner's manual for maximum child size,' which is not mentioned in the exact quote. This introduces new information not present in the source, altering the meaning.

Quote — binding 1, source `src_r2j_manual_v1`, page `5`

```text
See Graco infant car seat owners manual for maximum size of child.
```

Verifier: `MEANING_CHANGED` — The translation adds the instruction to 'read the manual... before using it with the stroller,' which is not mentioned in the quote. The quote only directs users to see the manual for the maximum child size; it does not mention strollers or pre-use reading requirements.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_finger_entrapment`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `finger_entrapment_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation incorrectly assigns the predicate 'finger_entrapment_hazard' to the entire instruction, while the quote only warns to 'AVOID FINGER ENTRAPMENT' as a header — the actual instruction is about safe folding/unfolding and ensuring the stroller is fully erected and latched. The translation falsely implies the hazard type applies to the action described, rather than being a general warning header. Also, 'the child' is used instead of 'your child', subtly altering the actor's relationship to the child.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Use care when folding and unfolding the stroller; ensure it is fully erected and latched before allowing the child near it.",
  "hazard_type": "entrapment_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID FINGER ENTRAPMENT: Use care when folding and unfolding the stroller. Be certain the stroller is fully erected and latched before allowing your child near the stroller.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns the predicate 'finger_entrapment_hazard' to the entire instruction, while the quote only warns to 'AVOID FINGER ENTRAPMENT' as a header — the actual instruction is about safe folding/unfolding and ensuring the stroller is fully erected and latched. The translation falsely implies the hazard type applies to the action described, rather than being a general warning header. Also, 'the child' is used instead of 'your child', subtly altering the actor's relationship to the child.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_hot_liquids`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `burn_hazard_cup_holder`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'hazard_type': 'burn_hazard' and a structured predicate 'burn_hazard_cup_holder', which are not present in the original quote. The original is a general safety warning; the translation imposes a specific hazard classification and structured predicate not stated in the source, altering the meaning by adding unmentioned metadata.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Never put hot liquids in the cup holder.",
  "hazard_type": "burn_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
TO AVOID BURNS, never put hot liquids in the cup holder.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type': 'burn_hazard' and a structured predicate 'burn_hazard_cup_holder', which are not present in the original quote. The original is a general safety warning; the translation imposes a specific hazard classification and structured predicate not stated in the source, altering the meaning by adding unmentioned metadata.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_not_a_toy`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `not_a_toy`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'hazard_type': 'general_safety' and 'type': 'WARNING', which are not present in the quote. The quote is a direct instruction, not explicitly labeled as a 'WARNING' or categorized by hazard type. Also, the predicate 'not_a_toy' is a reification not found in the original text, which simply prohibits using the stroller as a toy without asserting a categorical property.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Never allow the stroller to be used as a toy.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER ALLOW YOUR STROLLER to be used as a toy.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type': 'general_safety' and 'type': 'WARNING', which are not present in the quote. The quote is a direct instruction, not explicitly labeled as a 'WARNING' or categorized by hazard type. Also, the predicate 'not_a_toy' is a reification not found in the original text, which simply prohibits using the stroller as a toy without asserting a categorical property.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_seat_belt`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `requires_harness_use`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'hazard_type':'falling_hazard' and 'predicate':'requires_harness_use', which are not stated in the quote. The quote mentions 'seat belt', not 'harness', and does not classify the hazard type. These additions change the meaning by introducing unmentioned concepts.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.
```

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type':'falling_hazard' and 'predicate':'requires_harness_use', which are not stated in the quote. The quote mentions 'seat belt', not 'harness', and does not classify the hazard type. These additions change the meaning by introducing unmentioned concepts.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_stairs`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `stairs_escalators_prohibited`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation omits the explicit warning about losing control of the stroller or the child falling out, which is a critical hazard explanation in the original. It also collapses two distinct instructions (prohibition on stairs/escalators + caution on steps/curbs) into a single concatenated sentence, potentially diluting the severity of the prohibition. The original emphasizes 'NEVER USE' as a hard rule with consequences; the translation softens it to a general caution without conveying the risk of injury.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Never use the stroller on stairs or escalators; use extra care on steps or curbs.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER USE STROLLER ON STAIRS or escalators. You may suddenly lose control of the stroller or your child may fall out. Also, use extra care when going up or down a step or curb.
```

Verifier: `MEANING_CHANGED` — The translation omits the explicit warning about losing control of the stroller or the child falling out, which is a critical hazard explanation in the original. It also collapses two distinct instructions (prohibition on stairs/escalators + caution on steps/curbs) into a single concatenated sentence, potentially diluting the severity of the prohibition. The original emphasizes 'NEVER USE' as a hard rule with consequences; the translation softens it to a general caution without conveying the risk of injury.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_strangulation`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `strangulation_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation drops the imperative 'AVOID STRANGULATION:' and the directive 'DO NOT', replacing them with a passive description. This removes the direct command and urgency, altering the tone and legal/functional intent of the warning. Also, 'your child’s neck' becomes 'the child's neck', which removes the personal address to the caregiver, potentially reducing perceived responsibility.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Do not place items with a string around the child's neck, suspend strings from the product, or attach strings to toys.",
  "hazard_type": "strangulation_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID STRANGULATION: DO NOT place items with a string around your child’s neck, suspend strings from this product, or attach strings to toys.
```

Verifier: `MEANING_CHANGED` — The translation drops the imperative 'AVOID STRANGULATION:' and the directive 'DO NOT', replacing them with a passive description. This removes the direct command and urgency, altering the tone and legal/functional intent of the warning. Also, 'your child’s neck' becomes 'the child's neck', which removes the personal address to the caregiver, potentially reducing perceived responsibility.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_tipping_handle_canopy`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `tipping_hazard_handle_loads`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation replaces 'accessory items (other than approved Graco stroller bags)' with 'non-approved accessory items', which omits the explicit reference to 'Graco stroller bags' and implies a broader category of disallowed items. This changes the scope of the restriction and removes brand-specific approval context, altering the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Never place purses, shopping bags, parcels or non-approved accessory items on the handle; never place anything on the canopy.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
TO PREVENT TIPPING, never place purses, shopping bags, parcels or accessory items (other than approved Graco stroller bags) on the handle. Never place anything on the canopy.
```

Verifier: `MEANING_CHANGED` — The translation replaces 'accessory items (other than approved Graco stroller bags)' with 'non-approved accessory items', which omits the explicit reference to 'Graco stroller bags' and implies a broader category of disallowed items. This changes the scope of the restriction and removes brand-specific approval context, altering the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_unattended`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `requires_child_supervision`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'requires_child_supervision' as a predicate, which is not stated in the quote; the quote only gives a direct instruction ('NEVER LEAVE CHILD UNATTENDED...') without labeling it as a requirement or using that specific terminology.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.
```

Verifier: `MEANING_CHANGED` — The translation adds 'requires_child_supervision' as a predicate, which is not stated in the quote; the quote only gives a direct instruction ('NEVER LEAVE CHILD UNATTENDED...') without labeling it as a requirement or using that specific terminology.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_warning_zip_tie`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `zip_tie_disposal`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'shipped with the product,' which is not in the original quote and introduces an unverified condition about the zip tie's origin.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Remove and immediately discard the zip tie shipped with the product.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `10`

```text
Remove and IMMEDIATELY discard the zip tie.
```

Verifier: `MEANING_CHANGED` — The translation adds 'shipped with the product,' which is not in the original quote and introduces an unverified condition about the zip tie's origin.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (11)

### `claim_r2j_warning_brakes_loading`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `requires_brakes_for_loading`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "CAREGIVER MUST always ensure the brakes are engaged when placing child into stroller.",
  "hazard_type": "rolling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
CAREGIVER MUST always ensure the brakes are engaged when placing child into stroller.
```

Verifier: `ENTAILED` — The translation preserves the exact meaning of the quote: the caregiver must always ensure brakes are engaged during child placement. No added, dropped, or altered qualifiers, actors, conditions, or units. The hazard_type and predicate are metadata not altering the core instruction.

Extractor notes: None recorded.

### `claim_r2j_warning_walking_speed`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `walking_speed_only`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Use only at walking speed; not intended for jogging, skating, etc.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
STROLLER TO BE USED only at walking speed. Product not intended for use while jogging, skating, etc.
```

Verifier: `ENTAILED` — The translation accurately preserves the core restriction: use only at walking speed and not for jogging, skating, etc. No numerical, directional, conditional, or actor changes; no added or dropped qualifiers. The structured format does not alter meaning.

Extractor notes: None recorded.

### `claim_r2j_warning_basket_not_carrier`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `basket_not_child_carrier`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Do not use the storage basket as a child carrier.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
DO NOT use storage basket as a child carrier.
```

Verifier: `ENTAILED` — The translation faithfully restates the exact warning without adding, dropping, or altering any condition, actor, or qualifier. The object description mirrors the quote verbatim, and the predicate and type are metadata not altering the core meaning.

Extractor notes: None recorded.

### `claim_r2j_warning_basket_standing`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `basket_standing_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Do not allow the child to stand on the basket; it may collapse and cause injury.",
  "hazard_type": "collapse_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
DO NOT ALLOW your child to stand on the basket. It may collapse and cause injury.
```

Verifier: `ENTAILED` — The translation faithfully preserves the core warning: prohibiting a child from standing on the basket due to risk of collapse and injury. The structured format (type, predicate, object) does not alter meaning — it merely reorganizes the same content without adding, dropping, or changing any factual element, qualifier, or condition.

Extractor notes: None recorded.

### `claim_r2j_warning_head_toward_footrest`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `child_orientation`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Never place the child in the stroller with head toward the footrest.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER PLACE child in the stroller with head toward footrest.
```

Verifier: `ENTAILED` — The translation faithfully reproduces the exact instruction from the quote without adding, omitting, or altering any condition, actor, direction, or qualifier. The object description mirrors the quote verbatim, and the predicate and type are metadata not present in the quote but do not alter the meaning of the extracted fact.

Extractor notes: None recorded.

### `claim_r2j_warning_damaged_discontinue`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `discontinue_if_damaged`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Discontinue using the stroller should it become damaged or broken.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
DISCONTINUE USING YOUR STROLLER should it become damaged or broken.
```

Verifier: `ENTAILED` — The translation accurately preserves the core instruction: discontinue use if the stroller becomes damaged or broken. No numbers, units, directions, actors, conditions, or qualifiers are altered or added. The hazard_type and predicate are metadata for categorization and do not alter the meaning of the original quote.

Extractor notes: None recorded.

### `claim_r2j_warning_caregiver_assist`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `caregiver_assist_entry_exit`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Caregiver must always help the child get into and out of the stroller.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
CAREGIVER MUST always help child get into and out of the stroller.
```

Verifier: `ENTAILED` — The translation faithfully preserves the core requirement: the caregiver must always assist the child with entering and exiting the stroller. No meaning-altering changes in actor, action, condition, or qualifier are present.

Extractor notes: None recorded.

### `claim_r2j_warning_car_seat_fall_hazard`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_attachment_check`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Always check that the infant car seat is securely attached to the stroller by pulling up on the car seat.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
FALL HAZARD: Always check that infant car seat is securely attached to stroller by pulling up on the car seat.
```

Verifier: `ENTAILED` — The translation faithfully preserves the exact instruction and hazard type from the quote without adding, dropping, or altering any condition, actor, direction, or qualifier.

Extractor notes: None recorded.

### `claim_r2j_warning_car_seat_harness`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_harness_required`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "Always secure the child with the car seat harness when using the car seat in the stroller.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
ALWAYS SECURE your child with the car seat harness when using the car seat in the stroller.  If your child is already in the car seat, check that the child is secured with the harness.
```

Verifier: `ENTAILED` — The translation accurately captures the core instruction from the quote: securing the child with the car seat harness when using the car seat in the stroller. The added 'hazard_type' and 'type' fields are metadata for classification and do not alter the meaning of the instruction itself. No factual, numerical, directional, or conditional changes are present.

Extractor notes: None recorded.

### `claim_r2j_warning_recline_clearance`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `seat_adjustment_clearance`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "description": "When adjusting the stroller seat, keep the child's head, arms, and legs clear of moving seat parts and the stroller frame.",
  "hazard_type": "entrapment_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `22`

```text
When making adjustments to the stroller seat, make sure child’s head, arms, and legs are clear of moving seat parts and stroller frame.
```

Verifier: `ENTAILED` — The translation accurately preserves the core instruction: ensuring the child’s head, arms, and legs are clear of moving parts during seat adjustment. The added 'hazard_type' and 'predicate' are metadata, not part of the translated meaning, and do not alter the factual content of the quote.

Extractor notes: None recorded.

### `claim_r2j_step_harness_height_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required; Extractor flagged applicability or interpretation context
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To adjust harness height, insert shoulder straps into desired loop.",
  "procedure": "adjust_harness_height",
  "step_number": 1,
  "target_parts": [
    "shoulder_straps",
    "harness_loops"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `27`

```text
To adjust harness height, insert shoulder straps into desired loop.
```

Verifier: `ENTAILED` — The translation preserves the exact instruction from the quote without adding, dropping, or altering any factual element; it merely structures the same content into a procedural format.

Extractor notes: Extracted because page 24's slide-adjuster step points here ('To adjust harness height, see page 27.') and the revision note names harness height among the deferred procedures.

## 4. C2 claims (1)

### `claim_r2j_step_rear_wheels_1`

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
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "Turn stroller over; locate tab (a) on pin of rear wheels and slot (b) in stroller, align them, and attach rear wheels to stroller.",
  "procedure": "attach_rear_wheels",
  "step_number": 1,
  "target_parts": [
    "rear_wheels"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `14`

```text
Turn stroller over. Locate tab (a) on pin of rear wheels and slot (b) in stroller and align them. Attach rear wheels to stroller as shown.
```

Verifier: `ENTAILED` — The translation accurately captures all actions, objects, and sequence from the quote without adding, omitting, or altering any detail. The structure is reorganized for machine readability but preserves the original meaning.

Extractor notes: None recorded.

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (4)

### `gap_specs_1`

- Kind: `SOURCE_MISSING`
- Waives: `[]`
- Reason: The manual (src_r2j_manual_v1), the only text source in this product's vault, states no product empty weight, no open or folded dimensions, no enumerated box contents (the page 10 parts list is diagram-only; the text only says to check that all parts are present), and no warranty terms (page 40 gives only contact channels for warranty information). The single spec-type fact literally stated in the text is 'No tools required.' (page 10), extracted as claim_r2j_spec_assembly_no_tools; it satisfies the SPEC floor but not the intent of the specs_limits checklist item. The remaining core specs cannot be extracted without fabrication.
- Closes when: docs/workorders/workorder-ready2jet-gap-closure.md Task 1 lands source-vault/graco-ready2jet-2212125/specs/specs.md (official PDP spec transcription: product weight, open/folded dimensions, box contents, warranty), after which SPEC claims for those facts can be extracted.

### `gap_fold_visual_1`

- Kind: `UNDERIVABLE`
- Waives: `[]`
- Reason: The manual's fold-page text (pages 33-35) ends at 'squeeze handle lever' followed by 'CHECK that the stroller is secure.' The physical frame-collapse motion between those two states is shown only in diagrams and is not stated in text, so no STEP claim for it was written (no inventing steps from diagrams).
- Closes when: A measured visual annotation pass over the page 34-35 diagrams or the official fold video (src_r2j_fold_video_v1), or a manufacturer text source describing the collapse motion; see also the manifest collection_gaps entry on thumb-switch/handle-lever macro imagery.

### `gap_compat_chart_1`

- Kind: `SOURCE_MISSING`
- Waives: `[]`
- Reason: The manual states only a generic compatibility claim ('COMPATIBLE WITH MOST GRACO® INFANT CAR SEATS', extracted as claim_r2j_compat_graco_infant_car_seats) and directs users to customer service or a QR code for specifics. No per-model compatibility chart exists in this product's vault, so per-counterpart COMPATIBILITY claims cannot be extracted here.
- Closes when: The official compatibility chart PDF (held in the SnugRide product's vault per docs/workorders/evidence-pack-extraction-workorder.md §6.2) is cross-referenced during review, or a Ready2Jet-side compatibility source is added to this vault.

### `gap_harness_reconvert_1`

- Kind: `UNDERIVABLE`
- Waives: `[]`
- Reason: The manual documents converting the 5-point harness to 3-point (pages 24-25) but states no dedicated reverse (3-point back to 5-point) sequence, in text or diagrams (pages 23-27 checked). Reattachment of the shoulder straps appears only implicitly, via the 5-point close step ('To close, slide shoulder strap connectors onto waist straps and insert into buckle.', page 23, claim_r2j_step_harness_2) and the harness-height loop insertion (page 27, claim_r2j_step_harness_height_1), so no convert_back procedure could be extracted without inventing a sequence.
- Closes when: A manufacturer text source stating the 3-point-to-5-point reconversion sequence, or a reviewer decision that the page 23 close step plus the page 27 height-adjustment steps constitute the documented reverse path.

## 7. Batch-eligible C0/C1 spot-audit (2)

Batch ID: `batch_graco-ready2jet-2212125_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `2` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `2` members of `batch_graco-ready2jet-2212125_20260826`.
- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below individually.
- Owner / date: ______________________________

### `claim_r2j_step_recline_1` — SPOT-AUDIT SAMPLE

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
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "action": "To recline, push button down and pull seat towards the rear.",
  "procedure": "recline_seat",
  "step_number": 1,
  "target_parts": [
    "recline_button",
    "seat"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `22`

```text
To recline, push button down and pull seat towards the rear.
```

Verifier: `ENTAILED` — The translation preserves the exact procedural instruction from the quote without adding, dropping, or altering any action, direction, actor, or condition. The structure is reformatted as metadata but does not change the meaning.

Extractor notes: None recorded.

### `claim_r2j_care_cup_holder` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `cup_holder_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "2212125",
  "state": null
}
```

Object

```json
{
  "method": "dishwasher",
  "restrictions": [
    "top rack only"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `18`

```text
Cup holder is dishwasher safe (top rack only.)
```

Verifier: `ENTAILED` — The translation accurately captures the core meaning: the cup holder can be cleaned in a dishwasher with the restriction of top rack only. The structured format does not add or omit any factual conditions from the quote.

Extractor notes: None recorded.
