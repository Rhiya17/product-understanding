# Review Proposals — graco-ready2jet-2212125

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `94`
- Existing human decisions: `1`
- Undecided claims covered here: `93`
- Existing decisions reopened by v2 alarms: `0`
- Total owner action items: `93`
- Proposed `NEEDS_RECHECK`: `7`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `86`
- Batch-eligible C0/C1: `35`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (7)

### `claim_r2j_care_wet_drying`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `drying_after_wet`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection omits the governing condition 'IF STROLLER BECOMES WET', making the instruction unconditional. The original quote only prescribes opening the canopy and drying when the stroller is wet; the projection wrongly implies this is always required before storing, which broadens the scope and removes a necessary condition.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection omits the governing condition 'IF STROLLER BECOMES WET', making the instruction unconditional. The original quote only prescribes opening the canopy and drying when the stroller is wet; the projection wrongly implies this is always required before storing, which broadens the scope and removes a necessary condition.

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
- Proposed rationale: Verifier found a meaning change: The projection adds an unsupported verification instruction (calling Graco or scanning a code) not present in the quote. The quote only states compatibility with most Graco infant car seats as a safety warning; it does not mention any verification method or customer service contact. This is an unsupported semantic addition.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported verification instruction (calling Graco or scanning a code) not present in the quote. The quote only states compatibility with most Graco infant car seats as a safety warning; it does not mention any verification method or customer service contact. This is an unsupported semantic addition.

Extractor notes: Generic manufacturer statement, not a per-model chart. Page 29 restates it without the word MOST ('COMPATIBLE WITH GRACO® INFANT CAR SEATS'); same source, so not recorded as a conflict. Per-model compatibility (e.g. SnugRide chart) is not in this product's vault.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_limit_cup_holder_weight`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_cup_holder_weight`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection states a value of 1 lb without specifying it applies only to the cup holder; the quote explicitly limits 1 lb to the cup holder and separately limits 10 lb for the stroller storage basket. Omitting the governing condition (cup holder) wrongly implies the 1 lb limit applies unconditionally or broadly, which contradicts the quote’s scoped restriction.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection states a value of 1 lb without specifying it applies only to the cup holder; the quote explicitly limits 1 lb to the cup holder and separately limits 10 lb for the stroller storage basket. Omitting the governing condition (cup holder) wrongly implies the 1 lb limit applies unconditionally or broadly, which contradicts the quote’s scoped restriction.

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
- Proposed rationale: Verifier found a meaning change: The quote specifies attaching the 'child’s belly bar' onto 'belly bar mounts' but does not describe the location as 'across the front of the stroller seat'. This spatial description is an unsupported addition not present in the source, broadening the claim beyond what is asserted.

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

Verifier (claim quote union): `MEANING_CHANGED` — The quote specifies attaching the 'child’s belly bar' onto 'belly bar mounts' but does not describe the location as 'across the front of the stroller seat'. This spatial description is an unsupported addition not present in the source, broadening the claim beyond what is asserted.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_r2j_part_handle_lever`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `handle_lever_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote 'squeeze handle lever' does not specify location ('underside of the stroller handle') or sequence ('after sliding the thumb switch'). These additions are unsupported semantic expansions that broaden the claim beyond what the quote entails.

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

Verifier (claim quote union): `MEANING_CHANGED` — The quote 'squeeze handle lever' does not specify location ('underside of the stroller handle') or sequence ('after sliding the thumb switch'). These additions are unsupported semantic expansions that broaden the claim beyond what the quote entails.

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
- Proposed rationale: Verifier found a meaning change: The quote 'slide thumb switch' describes an action or feature but provides no information about location; projecting 'Located on the top center of the stroller handle' adds unsupported spatial detail not implied by any quote.

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

Verifier (claim quote union): `MEANING_CHANGED` — The quote 'slide thumb switch' describes an action or feature but provides no information about location; projecting 'Located on the top center of the stroller handle' adds unsupported spatial detail not implied by any quote.

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
- Proposed rationale: Verifier found a meaning change: The projection adds 'shipped with the product', which is not stated or implied in the quote. The quote only instructs to remove and discard the zip tie without specifying its origin or context, so adding that it was 'shipped with the product' is an unsupported semantic addition.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'shipped with the product', which is not stated or implied in the quote. The quote only instructs to remove and discard the zip tie without specifying its origin or context, so adding that it was 'shipped with the product' is an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (45)

### `claim_r2j_limit_max_weight`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_child_weight`
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
  "unit": "lb",
  "value": 50
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'a child weighing more than 50 lb (22.5 kg)', which directly supports the projection's value of 50 and unit of lb. The projection is a faithful subset of the source; no condition, direction, or qualifier is omitted that would broaden or alter the meaning. The unit and value are correctly extracted without unsupported addition.

Extractor notes: None recorded.

### `claim_r2j_limit_max_height`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_child_height`
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
  "unit": "in",
  "value": 45
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'taller than 45 in. (114 cm)', which directly supports the projection's value of 45 and unit of 'in'. The projection is a faithful subset of the source, omitting only the comparative direction ('taller than') and the metric equivalent, which does not broaden or alter the semantic assertion of the value and unit themselves.

Extractor notes: None recorded.

### `claim_r2j_warning_unattended`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `requires_child_supervision`
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
  "description": "NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly reproduces the text of the single quote without omission, addition, or alteration. No condition, direction, or qualifier is lost or broadened. The projection asserts nothing beyond what is stated in the quote.

Extractor notes: None recorded.

### `claim_r2j_warning_seat_belt`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `requires_harness_use`
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
  "description": "AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is an exact verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning, condition, direction, or scope occurs. All assertions in the projection are directly and fully supported by the quote.

Extractor notes: None recorded.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is an exact restatement of the single quote. No conditions, directions, actors, numbers, units, or qualifiers are added, omitted, or altered. The union of quotes fully supports the projection as written.

Extractor notes: None recorded.

### `claim_r2j_dimension_basket_capacity`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_storage_basket_weight`
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
  "unit": "lb",
  "value": 10
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
Do not place more than 10 lb (4.5 kg) in the stroller storage basket
```

Verifier (claim quote union): `ENTAILED` — The projection 'unit: lb, value: 10' is directly supported by the quote's explicit limit of '10 lb', with no omitted condition or direction that alters the meaning; the unit and value are faithfully extracted.

Extractor notes: None recorded.

### `claim_r2j_warning_basket_overload`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `basket_overload_hazard`
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
  "description": "Overloading the basket can create a hazardous unstable condition.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
EXCESSIVE WEIGHT MAY CAUSE A HAZARDOUS UNSTABLE CONDITION TO EXIST.
```

Verifier (claim quote union): `ENTAILED` — The projection 'Overloading the basket can create a hazardous unstable condition' is semantically supported by the quote 'EXCESSIVE WEIGHT MAY CAUSE A HAZARDOUS UNSTABLE CONDITION TO EXIST.' 'Overloading' implies excessive weight, and 'can create' aligns with 'may cause.' The projection does not broaden scope, misstate direction, or omit a governing condition — the hazard is conditionally tied to excess weight in both, and no additional constraints are implied or dropped.

Extractor notes: None recorded.

### `claim_r2j_limit_single_occupant`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `LIMIT` / `maximum_occupants`
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
  "unit": "child",
  "value": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
Use the stroller with only one child at a time.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly restricts use to 'only one child at a time,' which directly supports the projection's assertion of 'value': 1 with 'unit': 'child.' No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### `claim_r2j_warning_finger_entrapment`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `finger_entrapment_hazard`
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
  "description": "Use care when folding and unfolding the stroller; ensure it is fully erected and latched before allowing the child near it.",
  "hazard_type": "entrapment_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID FINGER ENTRAPMENT: Use care when folding and unfolding the stroller. Be certain the stroller is fully erected and latched before allowing your child near the stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: it preserves the instruction to use care during folding/unfolding and the condition that the stroller must be fully erected and latched before allowing the child near it. No qualifiers, conditions, or directions are omitted or broadened; the union of quotes fully supports the semantic assertions in the projection.

Extractor notes: None recorded.

### `claim_r2j_warning_strangulation`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `strangulation_hazard`
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
  "description": "Do not place items with a string around the child's neck, suspend strings from the product, or attach strings to toys.",
  "hazard_type": "strangulation_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
AVOID STRANGULATION: DO NOT place items with a string around your child’s neck, suspend strings from this product, or attach strings to toys.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection faithfully restates the warning from the quote, preserving all prohibitions (placing items with string around child’s neck, suspending strings from product, attaching strings to toys) without adding, omitting, or altering conditions, directions, or scope. The quote’s imperative tone and subject ('your child') are appropriately generalized to 'the child' without semantic loss.

Extractor notes: None recorded.

### `claim_r2j_warning_stairs`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `stairs_escalators_prohibited`
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
  "description": "Never use the stroller on stairs or escalators; use extra care on steps or curbs.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER USE STROLLER ON STAIRS or escalators. You may suddenly lose control of the stroller or your child may fall out. Also, use extra care when going up or down a step or curb.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully summarizes the warning: 'Never use the stroller on stairs or escalators' directly quotes the prohibition, and 'use extra care on steps or curbs' is a valid paraphrase of 'use extra care when going up or down a step or curb.' No condition, direction, or qualifier is omitted or broadened in a way that changes meaning.

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: 'Use only at walking speed; not intended for jogging, skating, etc.' matches the original assertion that the stroller is to be used only at walking speed and is not intended for jogging, skating, etc. No condition, direction, or qualifier is omitted or broadened.

Extractor notes: None recorded.

### `claim_r2j_warning_tipping_handle_canopy`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `tipping_hazard_handle_loads`
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
  "description": "Never place purses, shopping bags, parcels or non-approved accessory items on the handle; never place anything on the canopy.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
TO PREVENT TIPPING, never place purses, shopping bags, parcels or accessory items (other than approved Graco stroller bags) on the handle. Never place anything on the canopy.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the prohibition: 'purses, shopping bags, parcels or accessory items (other than approved Graco stroller bags)' becomes 'purses, shopping bags, parcels or non-approved accessory items' — preserving the exclusion of approved bags. The second clause 'never place anything on the canopy' is verbatim from the quote. No condition, direction, or qualifier is lost or broadened.

Extractor notes: None recorded.

### `claim_r2j_warning_hot_liquids`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `burn_hazard_cup_holder`
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
  "description": "Never put hot liquids in the cup holder.",
  "hazard_type": "burn_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
TO AVOID BURNS, never put hot liquids in the cup holder.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Never put hot liquids in the cup holder.' is a direct subset of the quote 'TO AVOID BURNS, never put hot liquids in the cup holder.' The projection omits the rationale ('TO AVOID BURNS') but does not broaden, contradict, or add unsupported conditions — it faithfully restates the core prohibition. Omission of the purpose clause does not change the meaning of the imperative itself.

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the exact prohibition in the quote, preserving the imperative 'Do not use' and the object 'storage basket as a child carrier' without adding, omitting, or altering any condition, direction, or qualifier.

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: prohibiting a child from standing on the basket due to risk of collapse and injury. No condition, direction, actor, or qualifier is added, omitted, or altered in a way that broadens scope or introduces unsupported meaning.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote’s prohibition: 'Never place the child in the stroller with head toward the footrest.' No qualifiers, conditions, or directions are omitted or added; the projection is a faithful restatement of the quoted warning.

Extractor notes: None recorded.

### `claim_r2j_warning_not_a_toy`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `not_a_toy`
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
  "description": "Never allow the stroller to be used as a toy.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
NEVER ALLOW YOUR STROLLER to be used as a toy.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote’s imperative and scope: 'Never allow the stroller to be used as a toy' is a direct, faithful restatement of 'NEVER ALLOW YOUR STROLLER to be used as a toy.' No condition, direction, actor, or qualifier is added, omitted, or altered in a way that broadens or contradicts the original. The union of quotes supports the projection without unsupported addition.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection faithfully restates the exact warning from the quote: 'Discontinue using the stroller should it become damaged or broken.' No conditions, directions, actors, or qualifiers are added, omitted, or altered in a way that changes meaning. The imperative and conditional structure is preserved.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the assertion in the quote: 'Caregiver must always help the child get into and out of the stroller.' No qualifiers, conditions, directions, or actors are added, omitted, or altered in a way that changes meaning. The union of quotes supports the projection fully.

Extractor notes: None recorded.

### `claim_r2j_warning_adult_assembly`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `adult_assembly_required`
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
  "description": "Adult assembly required.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `4`

```text
ADULT ASSEMBLY REQUIRED.
```

Verifier (claim quote union): `ENTAILED` — The projection 'Adult assembly required.' is a direct, faithful paraphrase of the exact quote 'ADULT ASSEMBLY REQUIRED.' with no added, omitted, or altered semantic conditions, directions, or qualifiers. The capitalization and punctuation differences do not affect the semantic assertion.

Extractor notes: Assigned C3 per work-order rule that every safety warning in the manual is a C3 WARNING claim, although this is an assembly requirement rather than an in-use hazard.

### `claim_r2j_warning_car_seat_other_brands`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_brand_restriction`
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
  "description": "Improper use of this stroller with other manufacturers' car seats may result in serious injury or death.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
Improper use of this stroller with other manufacturers’ car seats may result in serious injury or death.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The warning is faithfully preserved without any unsupported semantic addition or contradiction.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, faithful restatement of the warning in the quote, omitting only the label 'FALL HAZARD:' which is metadata not asserted as factual content. The core instruction — checking secure attachment by pulling up — is fully supported by the quote.

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

Verifier (claim quote union): `ENTAILED` — The projection exactly mirrors the first sentence of the quote, which is a direct imperative without omitted conditions or qualifiers. The second sentence in the quote is not required to support the projection, as the projection is a faithful subset of the source.

Extractor notes: None recorded.

### `claim_r2j_warning_car_seat_read_manual`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `car_seat_manual_required_reading`
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
  "description": "Read the manual provided with the Graco car seat before using it with the stroller; see the car seat owner's manual for maximum child size.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `5`

```text
READ THE MANUAL provided with your Graco car seat before using it with your stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately combines the two quotes: it instructs to read the manual before using the car seat with the stroller (from quote 0), and directs to consult the owner’s manual for maximum child size (from quote 1). No condition, direction, unit, or actor is misrepresented or broadened. The union of quotes fully supports the semantic assertions in the projection.

Quote — binding 1, source `src_r2j_manual_v1`, page `5`

```text
See Graco infant car seat owners manual for maximum size of child.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately combines the two quotes: it instructs to read the manual before using the car seat with the stroller (from quote 0), and directs to consult the owner’s manual for maximum child size (from quote 1). No condition, direction, unit, or actor is misrepresented or broadened. The union of quotes fully supports the semantic assertions in the projection.

Extractor notes: None recorded.

### `claim_r2j_warning_belly_bar_not_restraint`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `belly_bar_not_restraint`
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
  "description": "The belly bar is not a restraint device; always secure the child with the seat belt, and use care when installing the belly bar with a child in the stroller.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `16`

```text
Always secure your child with the seat belt. The belly bar is not a restraint device. Use care when installing the belly bar on the stroller with a child in the stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates all semantic assertions from the quote: (1) the belly bar is not a restraint device, (2) always secure the child with the seat belt, and (3) use care when installing the belly bar with a child in the stroller. No condition, direction, or qualifier is omitted or broadened; the union of quotes fully supports the projection.

Extractor notes: None recorded.

### `claim_r2j_warning_apply_both_brakes`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `apply_both_brakes`
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
  "description": "Always apply both brakes; check that brakes are on by trying to push the stroller.",
  "hazard_type": "rolling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `20`

```text
Always apply both brakes. Check that brakes are on by trying to  push stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the exact instructions from the quote: applying both brakes and verifying their engagement by attempting to push the stroller. No condition, direction, actor, or qualifier is added, omitted, or altered in a way that changes meaning.

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote, preserving the imperative to keep the child’s body parts clear of moving parts and frame during seat adjustment. No condition, direction, or qualifier is added or omitted that alters the meaning.

Extractor notes: None recorded.

### `claim_r2j_part_click_connect_mounts`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `PART_LOCATION` / `click_connect_mounts_location`
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

Verifier (claim quote union): `ENTAILED` — The quote describes pushing down on the car seat until latches snap into Click Connect™ mounts, which implies the mounts are located in the stroller seat where the latching occurs. The projection’s description of the location and function is semantically supported by the quote’s action and result.

Extractor notes: Location wording 'in the stroller seat' grounded in the page 31 text 'Find mounts in seat.'; diagram on page 31 labels the mount.

### `claim_r2j_step_car_seat_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the union of quoted text; no additional conditions, directions, or qualifiers are introduced or omitted in a way that alters meaning.

Extractor notes: None recorded.

### `claim_r2j_step_car_seat_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote's assertion without adding, omitting, or altering any condition, direction, actor, or scope. The union of quotes contains only this single statement, and the projection faithfully reproduces it.

Extractor notes: None recorded.

### `claim_r2j_step_car_seat_3`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote, including the sequence (insert, then push down) and the condition for completion (until latches snap into Click Connect mounts). No qualifiers, conditions, or directions are omitted or altered. The trademark symbol ™ is omitted, but that is a formatting detail, not a semantic assertion.

Extractor notes: None recorded.

### `claim_r2j_step_car_seat_4`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the assertion in the quote: checking secure attachment of the infant car seat by pulling up on it. No condition, direction, unit, actor, or scope is added, omitted, or altered in a way that changes meaning. The union of quotes supports the projection fully.

Extractor notes: None recorded.

### `claim_r2j_step_car_seat_5`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The projection faithfully restates the exact instruction without any unsupported semantic addition or omission that changes meaning.

Extractor notes: Removal action; kept in the attach_car_seat procedure as step 5 to mirror the manual's own numbering in section 4-G.

### `claim_r2j_step_harness_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim copy of the single quote. No addition, omission, or alteration of meaning occurs. All semantic assertions in the projection are fully supported by the quote.

Extractor notes: None recorded.

### `claim_r2j_step_harness_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of conditions, directions, actors, or scope occurs. The projection asserts nothing beyond what is explicitly stated in the quote.

Extractor notes: None recorded.

### `claim_r2j_step_harness_3pt_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All semantic assertions in the projection are directly supported by the quote.

Extractor notes: First step of the '3 Point Harness' section (page 24). Identical wording to secure_child_5pt step 1 (page 23); the manual restates it at the start of the conversion sequence.

### `claim_r2j_step_harness_3pt_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the quoted instruction: 'Slide shoulder strap connectors off of waist straps.' No conditions, directions, units, actors, or scope have been added, removed, or altered. The projection is a faithful subset of the source quote.

Extractor notes: None recorded.

### `claim_r2j_step_harness_3pt_3`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the single quote's assertion: 'Remove shoulder straps from stroller.' No conditions, qualifiers, or directions are omitted or added. The action is stated plainly and unconditionally in both, and no broader claim is made.

Extractor notes: None recorded.

### `claim_r2j_step_harness_3pt_4`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote without adding, omitting, or altering any condition, direction, or qualifier. The phrase 'as shown' is preserved, maintaining the original instruction’s dependency on visual guidance.

Extractor notes: 'as shown' refers to the page 25 illustration of the 3-point buckle configuration; the attaching action itself is stated in text.

### `claim_r2j_step_harness_3pt_5`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion without adding, omitting, or altering any condition, direction, actor, or scope. No unsupported semantic addition or contradiction exists.

Extractor notes: Manual numbers the 3 Point Harness section continuously: steps 1-4 perform the conversion; steps 5-6 are use of the converted 3-point harness.

### `claim_r2j_step_harness_3pt_6`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote; no addition, omission, or alteration of meaning occurs. All assertions in the projection are directly supported by the quote.

Extractor notes: Opening the converted 3-point harness; the manual keeps this in the same numbered sequence as the conversion steps.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No conditions, qualifiers, directions, or units are omitted or altered. The action described is fully supported by the quote without any broadening, contradiction, or unsupported addition.

Extractor notes: Extracted because page 24's slide-adjuster step points here ('To adjust harness height, see page 27.') and the revision note names harness height among the deferred procedures.

### `claim_r2j_step_harness_height_2`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote's assertion without adding, omitting, or altering any condition, direction, actor, or scope. The union of quotes contains only this single statement, and the projection faithfully reproduces it as-is.

Extractor notes: None recorded.

### `claim_r2j_step_harness_height_3`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All assertions in the projection are directly supported by the quote.

Extractor notes: This instruction is present as text on page 27 but is unnumbered in the manual (it sits beside the labeled diagram); numbered 3 here to keep the procedure sequence contiguous. Not diagram-only: the action, including 'Repeat on other side.', is stated in text.

## 4. C2 claims (6)

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully combines and rephrases the sequence of actions from the quote without adding, omitting, or altering any semantic conditions, directions, or actors. All steps — turning over, locating, aligning, attaching — are explicitly stated in the quote and preserved in the projection.

Extractor notes: None recorded.

### `claim_r2j_step_rear_wheels_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: checking wheel attachment by pulling on assemblies. No conditions, qualifiers, or directions are omitted or added that alter the meaning. The imperative 'Check' corresponds to 'CHECK' in the quote, and the method ('by pulling on wheel assemblies') is preserved verbatim in meaning.

Extractor notes: None recorded.

### `claim_r2j_step_front_wheels_1`

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

Verifier (claim quote union): `ENTAILED` — The projection 'Attach front wheels to stroller.' is a faithful subset of the quote 'Attach front wheels to stroller as shown.' The omitted phrase 'as shown' does not add a required condition or constraint that changes the core action; it merely indicates a visual reference, which is not semantically necessary for the action assertion itself.

Extractor notes: None recorded.

### `claim_r2j_step_front_wheels_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: checking wheel attachment by pulling on assemblies. No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The imperative 'Check' is semantically equivalent to 'CHECK' in context, and the rest of the phrasing is identical.

Extractor notes: None recorded.

### `claim_r2j_step_wheel_removal_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion: 'Push release button to remove wheel assemblies.' No qualifiers, conditions, directions, or units are omitted or added that alter the meaning. The action described is fully supported by the quote.

Extractor notes: The manual's only wheel-removal instruction (Care & Maintenance, beach-cleaning bullet; pages 14-15 point here via 'For wheel removal see Care & Maintenance.'). Release button location is shown only in the page 36 illustration; text states the action only.

### `claim_r2j_care_beach_cleaning`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `beach_cleaning`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quote: contaminants (sand, salt) are explicitly named; method (complete cleaning after beach use) matches 'completely clean your stroller afterward'; targets (mechanisms, wheel assemblies) are directly cited. No unsupported addition, condition loss, or semantic overreach.

Extractor notes: C2 because the cleaning involves wheel-assembly removal (same bullet continues 'Push release button to remove wheel assemblies.', extracted as claim_r2j_step_wheel_removal_1).

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

## 7. Batch-eligible C0/C1 spot-audit (35)

Batch ID: `batch_graco-ready2jet-2212125_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `35` members of `batch_graco-ready2jet-2212125_20260826`.
- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below individually.
- Owner / date: ______________________________

### `claim_r2j_step_fold_1` — SPOT-AUDIT SAMPLE

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

Verifier (claim quote union): `ENTAILED` — The projection 'Remove infant car seat if in use.' is directly supported by the quote '1. Before folding stroller: (a) remove infant car seat if in use'. The projection omits the procedural context ('Before folding stroller'), but this omission does not broaden the claim or add unsupported semantics — it merely restates the conditional action without the parent step. No condition, direction, actor, or unit is misrepresented or lost in a way that changes meaning.

Extractor notes: None recorded.

### `claim_r2j_step_fold_2` — SPOT-AUDIT SAMPLE

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Unlock brakes.' is directly supported by the quote '(b) unlock brakes', which asserts the same action without adding or omitting any governing condition, direction, or qualifier. No unsupported semantic addition or contradiction exists.

Extractor notes: None recorded.

### `claim_r2j_step_fold_3`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Fold the canopy.' is a direct, faithful restatement of the quoted imperative '(c) fold the canopy.' No conditions, qualifiers, or directions are omitted that would broaden or alter the meaning. The projection captures the exact action asserted in the quote.

Extractor notes: None recorded.

### `claim_r2j_step_fold_4`

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

Verifier (claim quote union): `ENTAILED` — The projection 'Slide thumb switch.' is a direct, faithful subset of the quoted instruction '2. To fold stroller: (a) slide thumb switch;'. No condition, direction, unit, or actor is added or altered; the action is asserted exactly as stated in the quote.

Extractor notes: None recorded.

### `claim_r2j_step_fold_5`

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

Verifier (claim quote union): `ENTAILED` — The projection 'Squeeze handle lever.' is a direct, faithful semantic subset of the quote '(b) squeeze handle lever', with no added conditions, directions, actors, or scope broadening. The imperative form matches the action described, and no governing condition is omitted that would alter meaning.

Extractor notes: None recorded.

### `claim_r2j_step_fold_6`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Check that the stroller is secure.' is fully supported by the quote '3. CHECK that the stroller is secure.' The imperative form and content are preserved; no condition, direction, or qualifier is omitted or broadened. The step number '3.' and capitalization are procedural/syntactic and not semantic assertions under the given rules.

Extractor notes: None recorded.

### `claim_r2j_step_fold_7`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Carry by belly bar.' is a direct, faithful subset of the quote '4. Carry by belly bar.' No conditions, qualifiers, directions, or units are omitted that would broaden or alter the meaning. The projection does not add unsupported assertions or drop governing conditions.

Extractor notes: None recorded.

### `claim_r2j_step_fold_tips_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's assertion without adding, omitting, or altering any condition, direction, actor, or qualifier. No unsupported semantic addition or contradiction exists.

Extractor notes: None recorded.

### `claim_r2j_step_fold_tips_2` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion without adding, omitting, or altering any condition, direction, actor, or scope. No unsupported semantic addition or contradiction exists.

Extractor notes: None recorded.

### `claim_r2j_step_unfold_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Slide thumb switch.' is a direct, faithful subset of the quoted instruction '1. To open stroller: (a) slide thumb switch;'. No condition, direction, unit, or actor is added or altered; the projection omits only the procedural context (opening stroller) which is not required for entailment under the union rule.

Extractor notes: None recorded.

### `claim_r2j_step_unfold_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Squeeze handle lever and lift up.' is a direct, faithful paraphrase of the exact quote '(b) squeeze handle lever and lift up', preserving the action, object, and direction without adding, omitting, or altering any condition, actor, or qualifier.

Extractor notes: None recorded.

### `claim_r2j_step_unfold_3`

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

Verifier (claim quote union): `ENTAILED` — The quote '(c) lift up handle' directly supports the semantic projection 'Lift up handle.' The projection is a faithful, unembellished restatement of the action described in the quote, with no added conditions, directions, units, or scope broadening.

Extractor notes: None recorded.

### `claim_r2j_step_unfold_4`

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

Verifier (claim quote union): `ENTAILED` — The projection is a faithful subset of the quote: it omits 'before continuing with the rest of the assembly steps,' which is an additional procedural instruction, not a condition or qualifier that alters the core assertion. The core action — checking that the stroller is completely latched open every time it is opened — is fully supported by the quote. No condition, direction, or scope is wrongly broadened or lost.

Extractor notes: None recorded.

### `claim_r2j_care_seat`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `seat_cleaning`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quote: 'mild soap' is the agent for wiping; 'wipe_only' matches 'should only be wiped'; restrictions include the explicit prohibitions 'DO NOT MACHINE WASH SEAT' and 'NO BLEACH', plus the caution 'taking care not to soak the material'. All assertions are directly supported by the quote without adding, broadening, or omitting conditions.

Extractor notes: None recorded.

### `claim_r2j_care_frame`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `frame_cleaning`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the agents (household soap, warm water) permitted for cleaning and the restrictions (NO BLEACH or detergent) explicitly stated in the quote. No unsupported addition, contradiction, or lost condition is present; the quote’s imperative scope is preserved.

Extractor notes: None recorded.

### `claim_r2j_care_wheel_oil`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `wheel_lubrication`
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

Verifier (claim quote union): `ENTAILED` — The quote explicitly lists 'light oil (e.g., 3-in-1, or sewing machine oil)' as agents and specifies the target location as 'axle and wheel assembly'. The projection accurately reflects these semantic elements without adding unsupported conditions, directions, or scope.

Extractor notes: None recorded.

### `claim_r2j_spec_assembly_no_tools`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `assembly_tools_required`
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
  "detail": "No tools are required to assemble the stroller.",
  "value": "none"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `10`

```text
No tools required.
```

Verifier (claim quote union): `ENTAILED` — The quote 'No tools required.' directly supports the assertion that 'No tools are required to assemble the stroller.' The projection adds context ('to assemble the stroller') which is not contradicted by the quote and is a reasonable, non-broadening inference given the product context. The value 'none' is consistent with 'No tools required.' No unsupported semantic addition, contradiction, or lost condition is present.

Extractor notes: Only spec-type fact literally stated in the manual text. Core specs (product weight, open/folded dimensions, box contents enumeration, warranty terms) are absent from the manual — see gaps.json gap_specs_1.

### `claim_r2j_step_canopy_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's assertion: 'Pull forward to open canopy.' No conditions, directions, units, or actors are added, omitted, or altered. The projection is a faithful subset of the source content.

Extractor notes: None recorded.

### `claim_r2j_step_canopy_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the quote's assertion: 'Push backwards to close canopy.' No conditions, directions, units, actors, or governing constraints are added, omitted, or altered. The projection is a faithful subset of the source content.

Extractor notes: None recorded.

### `claim_r2j_step_canopy_3` — SPOT-AUDIT SAMPLE

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action instructions in the quote: pulling the canopy visor out for use and pushing it back under the rim when not in use. No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The union of quotes fully supports the projection as a faithful restatement.

Extractor notes: None recorded.

### `claim_r2j_step_brake_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's assertion: 'Push down on brake to lock brakes.' No conditions, directions, units, or actors are added, omitted, or altered. The projection is a faithful subset of the source content.

Extractor notes: None recorded.

### `claim_r2j_step_brake_2` — SPOT-AUDIT SAMPLE

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's assertion: 'Push up on brake to unlock brakes.' No conditions, directions, units, or actors are added, omitted, or altered. The projection is a faithful subset of the source content.

Extractor notes: None recorded.

### `claim_r2j_step_recline_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All asserted actions and directions are fully supported by the source text.

Extractor notes: None recorded.

### `claim_r2j_step_recline_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly reproduces the quote's content without adding, omitting, or altering any condition, direction, actor, or qualifier. The action described is fully supported by the single quote.

Extractor notes: None recorded.

### `claim_r2j_step_belly_bar_1`

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

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the two actions in the quote: attaching the belly bar and checking logo alignment. No conditions, directions, units, or actors are added or altered. The omission of 'as shown' does not broaden scope or imply unsupported semantics, as the core requirement to check alignment is preserved.

Extractor notes: None recorded.

### `claim_r2j_step_belly_bar_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: 'Pull on child’s belly bar to ensure it is secure.' No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The projection is a faithful subset of the source assertion.

Extractor notes: None recorded.

### `claim_r2j_step_belly_bar_3`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No conditions, directions, units, actors, or qualifiers are added, omitted, or altered. The union of quotes contains exactly this instruction, and the projection asserts nothing beyond it.

Extractor notes: None recorded.

### `claim_r2j_care_inspection`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `CARE` / `periodic_inspection`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quote: 'periodic_check' matches 'FROM TIME TO TIME CHECK', 'targets' lists the exact items to inspect ('loose screws', 'worn parts', 'torn material or stitching'), and 'restrictions' correctly captures the requirement to 'Use only Graco replacement parts'. No unsupported addition, contradiction, or lost condition exists.

Extractor notes: Assigned C1 rather than C0 because the check targets structural wear affecting safe use; noted per the assign-higher-when-unsure rule.

### `claim_r2j_care_sun_exposure`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `CARE` / `sun_heat_exposure`
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
  "effect": "fading or warping of parts",
  "restriction": "avoid excessive exposure to sun or heat"
}
```

Quote — binding 0, source `src_r2j_manual_v1`, page `36`

```text
EXCESSIVE EXPOSURE TO SUN OR HEAT could cause fading or warping of parts.
```

Verifier (claim quote union): `ENTAILED` — The quote states that excessive exposure to sun or heat could cause fading or warping of parts, which directly supports the projection’s effect ('fading or warping of parts') and implies the restriction ('avoid excessive exposure to sun or heat') as a logical preventive measure. No unsupported addition, contradiction, or lost condition is present.

Extractor notes: None recorded.

### `claim_r2j_care_cup_holder`

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

Verifier (claim quote union): `ENTAILED` — The quote explicitly states the cup holder is dishwasher safe with the restriction 'top rack only,' which is fully captured in the projection's method and restrictions fields.

Extractor notes: None recorded.

### `claim_r2j_step_footrest_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All assertions in the projection are fully supported by the quote.

Extractor notes: 'as shown' refers to the page 21 illustration; the raising action itself is stated in text, so this is not a diagram-only step.

### `claim_r2j_step_footrest_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All assertions in the projection are directly supported by the quote.

Extractor notes: Manual's step 2 is headed 'To lower' but its own text says 'raise or lower footrest'; the buttons are needed only for lowering (step 1 raises without them). 'foot rest' spacing is verbatim from the manual.

### `claim_r2j_step_cup_holder_1`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim reproduction of the single quote. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The action described is fully and exactly supported by the quote.

Extractor notes: None recorded.

### `claim_r2j_step_cup_holder_2`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim copy of the single quote in the union. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The projection asserts nothing beyond what the quote explicitly states.

Extractor notes: None recorded.

### `claim_r2j_step_cup_holder_3`

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

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly reproduces the quote's content without adding, omitting, or altering any condition, direction, actor, or qualifier. The action described is fully supported by the single quote.

Extractor notes: Use-limit context for this accessory already extracted elsewhere: 1 lb (.45 kg) maximum load (claim_r2j_limit_cup_holder_weight), no hot liquids (claim_r2j_warning_hot_liquids), top-rack dishwasher cleaning (claim_r2j_care_cup_holder).
