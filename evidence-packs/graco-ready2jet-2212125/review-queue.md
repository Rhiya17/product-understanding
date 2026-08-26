# Review Queue — graco-ready2jet-2212125

Verification status: `COMPLETE`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.
A v2 alarm reopens `0` existing human disposition(s); those decisions must be explicitly reconfirmed or amended.

## 1. MEANING_CHANGED alarms (7)

### claim_r2j_care_wet_drying

- Claim: `claim_r2j_care_wet_drying`
- Tier: `C0`
- Type/predicate: `CARE` / `drying_after_wet`

Object

```json
{
  "method": "open canopy and air dry thoroughly before storing"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
IF STROLLER BECOMES WET, open canopy and allow to dry thoroughly before storing.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection omits the governing condition 'IF STROLLER BECOMES WET', making the instruction unconditional. The original quote only prescribes opening the canopy and drying when the stroller is wet; the projection wrongly implies this is always required before storing, which broadens the scope and removes a necessary condition.

Extractor notes: None recorded.

### claim_r2j_compat_graco_infant_car_seats

- Claim: `claim_r2j_compat_graco_infant_car_seats`
- Tier: `C3`
- Type/predicate: `COMPATIBILITY` / `compatible_infant_car_seats`

Object

```json
{
  "counterpart": "Graco infant car seats",
  "qualifier": "most",
  "verification": "Call Graco customer service 1-800-345-4109 or scan the in-manual code for compatibility."
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
TO AVOID INJURY TO YOUR CHILD: THIS PRODUCT IS COMPATIBLE WITH MOST GRACO® INFANT CAR SEATS.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported verification instruction (calling Graco or scanning a code) not present in the quote. The quote only states compatibility with most Graco infant car seats as a safety warning; it does not mention any verification method or customer service contact. This is an unsupported semantic addition.

Extractor notes: Generic manufacturer statement, not a per-model chart. Page 29 restates it without the word MOST ('COMPATIBLE WITH GRACO® INFANT CAR SEATS'); same source, so not recorded as a conflict. Per-model compatibility (e.g. SnugRide chart) is not in this product's vault.

### claim_r2j_limit_cup_holder_weight

- Claim: `claim_r2j_limit_cup_holder_weight`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_cup_holder_weight`

Object

```json
{
  "unit": "lb",
  "value": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Do not place more than 10 lb (4.5 kg) in the stroller storage basket, 1 lb (.45 kg) in the cup holder.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection states a value of 1 lb without specifying it applies only to the cup holder; the quote explicitly limits 1 lb to the cup holder and separately limits 10 lb for the stroller storage basket. Omitting the governing condition (cup holder) wrongly implies the 1 lb limit applies unconditionally or broadly, which contradicts the quote’s scoped restriction.

Extractor notes: None recorded.

### claim_r2j_part_belly_bar

- Claim: `claim_r2j_part_belly_bar`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `belly_bar_location`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Attach child’s belly bar onto belly bar mounts.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote specifies attaching the 'child’s belly bar' onto 'belly bar mounts' but does not describe the location as 'across the front of the stroller seat'. This spatial description is an unsupported addition not present in the source, broadening the claim beyond what is asserted.

Extractor notes: None recorded.

### claim_r2j_part_handle_lever

- Claim: `claim_r2j_part_handle_lever`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `handle_lever_location`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
squeeze handle lever
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote 'squeeze handle lever' does not specify location ('underside of the stroller handle') or sequence ('after sliding the thumb switch'). These additions are unsupported semantic expansions that broaden the claim beyond what the quote entails.

Extractor notes: None recorded.

### claim_r2j_part_thumb_switch

- Claim: `claim_r2j_part_thumb_switch`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `thumb_switch_location`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
slide thumb switch
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote 'slide thumb switch' describes an action or feature but provides no information about location; projecting 'Located on the top center of the stroller handle' adds unsupported spatial detail not implied by any quote.

Extractor notes: None recorded.

### claim_r2j_warning_zip_tie

- Claim: `claim_r2j_warning_zip_tie`
- Tier: `C3`
- Type/predicate: `WARNING` / `zip_tie_disposal`

Object

```json
{
  "description": "Remove and immediately discard the zip tie shipped with the product.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Remove and IMMEDIATELY discard the zip tie.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'shipped with the product', which is not stated or implied in the quote. The quote only instructs to remove and discard the zip tie without specifying its origin or context, so adding that it was 'shipped with the product' is an unsupported semantic addition.

Extractor notes: None recorded.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (45)

### claim_r2j_limit_max_weight

- Claim: `claim_r2j_limit_max_weight`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_child_weight`

Object

```json
{
  "unit": "lb",
  "value": 50
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'a child weighing more than 50 lb (22.5 kg)', which directly supports the projection's value of 50 and unit of lb. The projection is a faithful subset of the source; no condition, direction, or qualifier is omitted that would broaden or alter the meaning. The unit and value are correctly extracted without unsupported addition.

Extractor notes: None recorded.

### claim_r2j_limit_max_height

- Claim: `claim_r2j_limit_max_height`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_child_height`

Object

```json
{
  "unit": "in",
  "value": 45
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
USE OF THE STROLLER with a child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive wear and stress on the stroller.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'taller than 45 in. (114 cm)', which directly supports the projection's value of 45 and unit of 'in'. The projection is a faithful subset of the source, omitting only the comparative direction ('taller than') and the metric equivalent, which does not broaden or alter the semantic assertion of the value and unit themselves.

Extractor notes: None recorded.

### claim_r2j_warning_unattended

- Claim: `claim_r2j_warning_unattended`
- Tier: `C3`
- Type/predicate: `WARNING` / `requires_child_supervision`

Object

```json
{
  "description": "NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
NEVER LEAVE CHILD UNATTENDED. Always keep child in view while in stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly reproduces the text of the single quote without omission, addition, or alteration. No condition, direction, or qualifier is lost or broadened. The projection asserts nothing beyond what is stated in the quote.

Extractor notes: None recorded.

### claim_r2j_warning_seat_belt

- Claim: `claim_r2j_warning_seat_belt`
- Tier: `C3`
- Type/predicate: `WARNING` / `requires_harness_use`

Object

```json
{
  "description": "AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
AVOID SERIOUS INJURY from falling or sliding out. Always use seat belt. After fastening buckles, adjust belts to get a snug fit around your child.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is an exact verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning, condition, direction, or scope occurs. All assertions in the projection are directly and fully supported by the quote.

Extractor notes: None recorded.

### claim_r2j_warning_brakes_loading

- Claim: `claim_r2j_warning_brakes_loading`
- Tier: `C3`
- Type/predicate: `WARNING` / `requires_brakes_for_loading`

Object

```json
{
  "description": "CAREGIVER MUST always ensure the brakes are engaged when placing child into stroller.",
  "hazard_type": "rolling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
CAREGIVER MUST always ensure the brakes are engaged when placing child into stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is an exact restatement of the single quote. No conditions, directions, actors, numbers, units, or qualifiers are added, omitted, or altered. The union of quotes fully supports the projection as written.

Extractor notes: None recorded.

### claim_r2j_dimension_basket_capacity

- Claim: `claim_r2j_dimension_basket_capacity`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_storage_basket_weight`

Object

```json
{
  "unit": "lb",
  "value": 10
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Do not place more than 10 lb (4.5 kg) in the stroller storage basket
```

Verifier (claim quote union): `ENTAILED` — The projection 'unit: lb, value: 10' is directly supported by the quote's explicit limit of '10 lb', with no omitted condition or direction that alters the meaning; the unit and value are faithfully extracted.

Extractor notes: None recorded.

### claim_r2j_warning_basket_overload

- Claim: `claim_r2j_warning_basket_overload`
- Tier: `C3`
- Type/predicate: `WARNING` / `basket_overload_hazard`

Object

```json
{
  "description": "Overloading the basket can create a hazardous unstable condition.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
EXCESSIVE WEIGHT MAY CAUSE A HAZARDOUS UNSTABLE CONDITION TO EXIST.
```

Verifier (claim quote union): `ENTAILED` — The projection 'Overloading the basket can create a hazardous unstable condition' is semantically supported by the quote 'EXCESSIVE WEIGHT MAY CAUSE A HAZARDOUS UNSTABLE CONDITION TO EXIST.' 'Overloading' implies excessive weight, and 'can create' aligns with 'may cause.' The projection does not broaden scope, misstate direction, or omit a governing condition — the hazard is conditionally tied to excess weight in both, and no additional constraints are implied or dropped.

Extractor notes: None recorded.

### claim_r2j_limit_single_occupant

- Claim: `claim_r2j_limit_single_occupant`
- Tier: `C3`
- Type/predicate: `LIMIT` / `maximum_occupants`

Object

```json
{
  "unit": "child",
  "value": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Use the stroller with only one child at a time.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly restricts use to 'only one child at a time,' which directly supports the projection's assertion of 'value': 1 with 'unit': 'child.' No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### claim_r2j_warning_finger_entrapment

- Claim: `claim_r2j_warning_finger_entrapment`
- Tier: `C3`
- Type/predicate: `WARNING` / `finger_entrapment_hazard`

Object

```json
{
  "description": "Use care when folding and unfolding the stroller; ensure it is fully erected and latched before allowing the child near it.",
  "hazard_type": "entrapment_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
AVOID FINGER ENTRAPMENT: Use care when folding and unfolding the stroller. Be certain the stroller is fully erected and latched before allowing your child near the stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: it preserves the instruction to use care during folding/unfolding and the condition that the stroller must be fully erected and latched before allowing the child near it. No qualifiers, conditions, or directions are omitted or broadened; the union of quotes fully supports the semantic assertions in the projection.

Extractor notes: None recorded.

### claim_r2j_warning_strangulation

- Claim: `claim_r2j_warning_strangulation`
- Tier: `C3`
- Type/predicate: `WARNING` / `strangulation_hazard`

Object

```json
{
  "description": "Do not place items with a string around the child's neck, suspend strings from the product, or attach strings to toys.",
  "hazard_type": "strangulation_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
AVOID STRANGULATION: DO NOT place items with a string around your child’s neck, suspend strings from this product, or attach strings to toys.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection faithfully restates the warning from the quote, preserving all prohibitions (placing items with string around child’s neck, suspending strings from product, attaching strings to toys) without adding, omitting, or altering conditions, directions, or scope. The quote’s imperative tone and subject ('your child') are appropriately generalized to 'the child' without semantic loss.

Extractor notes: None recorded.

### claim_r2j_warning_stairs

- Claim: `claim_r2j_warning_stairs`
- Tier: `C3`
- Type/predicate: `WARNING` / `stairs_escalators_prohibited`

Object

```json
{
  "description": "Never use the stroller on stairs or escalators; use extra care on steps or curbs.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
NEVER USE STROLLER ON STAIRS or escalators. You may suddenly lose control of the stroller or your child may fall out. Also, use extra care when going up or down a step or curb.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully summarizes the warning: 'Never use the stroller on stairs or escalators' directly quotes the prohibition, and 'use extra care on steps or curbs' is a valid paraphrase of 'use extra care when going up or down a step or curb.' No condition, direction, or qualifier is omitted or broadened in a way that changes meaning.

Extractor notes: None recorded.

### claim_r2j_warning_walking_speed

- Claim: `claim_r2j_warning_walking_speed`
- Tier: `C3`
- Type/predicate: `WARNING` / `walking_speed_only`

Object

```json
{
  "description": "Use only at walking speed; not intended for jogging, skating, etc.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
STROLLER TO BE USED only at walking speed. Product not intended for use while jogging, skating, etc.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: 'Use only at walking speed; not intended for jogging, skating, etc.' matches the original assertion that the stroller is to be used only at walking speed and is not intended for jogging, skating, etc. No condition, direction, or qualifier is omitted or broadened.

Extractor notes: None recorded.

### claim_r2j_warning_tipping_handle_canopy

- Claim: `claim_r2j_warning_tipping_handle_canopy`
- Tier: `C3`
- Type/predicate: `WARNING` / `tipping_hazard_handle_loads`

Object

```json
{
  "description": "Never place purses, shopping bags, parcels or non-approved accessory items on the handle; never place anything on the canopy.",
  "hazard_type": "tipping_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
TO PREVENT TIPPING, never place purses, shopping bags, parcels or accessory items (other than approved Graco stroller bags) on the handle. Never place anything on the canopy.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the prohibition: 'purses, shopping bags, parcels or accessory items (other than approved Graco stroller bags)' becomes 'purses, shopping bags, parcels or non-approved accessory items' — preserving the exclusion of approved bags. The second clause 'never place anything on the canopy' is verbatim from the quote. No condition, direction, or qualifier is lost or broadened.

Extractor notes: None recorded.

### claim_r2j_warning_hot_liquids

- Claim: `claim_r2j_warning_hot_liquids`
- Tier: `C3`
- Type/predicate: `WARNING` / `burn_hazard_cup_holder`

Object

```json
{
  "description": "Never put hot liquids in the cup holder.",
  "hazard_type": "burn_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
TO AVOID BURNS, never put hot liquids in the cup holder.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Never put hot liquids in the cup holder.' is a direct subset of the quote 'TO AVOID BURNS, never put hot liquids in the cup holder.' The projection omits the rationale ('TO AVOID BURNS') but does not broaden, contradict, or add unsupported conditions — it faithfully restates the core prohibition. Omission of the purpose clause does not change the meaning of the imperative itself.

Extractor notes: None recorded.

### claim_r2j_warning_basket_not_carrier

- Claim: `claim_r2j_warning_basket_not_carrier`
- Tier: `C3`
- Type/predicate: `WARNING` / `basket_not_child_carrier`

Object

```json
{
  "description": "Do not use the storage basket as a child carrier.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
DO NOT use storage basket as a child carrier.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the exact prohibition in the quote, preserving the imperative 'Do not use' and the object 'storage basket as a child carrier' without adding, omitting, or altering any condition, direction, or qualifier.

Extractor notes: None recorded.

### claim_r2j_warning_basket_standing

- Claim: `claim_r2j_warning_basket_standing`
- Tier: `C3`
- Type/predicate: `WARNING` / `basket_standing_hazard`

Object

```json
{
  "description": "Do not allow the child to stand on the basket; it may collapse and cause injury.",
  "hazard_type": "collapse_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
DO NOT ALLOW your child to stand on the basket. It may collapse and cause injury.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: prohibiting a child from standing on the basket due to risk of collapse and injury. No condition, direction, actor, or qualifier is added, omitted, or altered in a way that broadens scope or introduces unsupported meaning.

Extractor notes: None recorded.

### claim_r2j_warning_head_toward_footrest

- Claim: `claim_r2j_warning_head_toward_footrest`
- Tier: `C3`
- Type/predicate: `WARNING` / `child_orientation`

Object

```json
{
  "description": "Never place the child in the stroller with head toward the footrest.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
NEVER PLACE child in the stroller with head toward footrest.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote’s prohibition: 'Never place the child in the stroller with head toward the footrest.' No qualifiers, conditions, or directions are omitted or added; the projection is a faithful restatement of the quoted warning.

Extractor notes: None recorded.

### claim_r2j_warning_not_a_toy

- Claim: `claim_r2j_warning_not_a_toy`
- Tier: `C3`
- Type/predicate: `WARNING` / `not_a_toy`

Object

```json
{
  "description": "Never allow the stroller to be used as a toy.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
NEVER ALLOW YOUR STROLLER to be used as a toy.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote’s imperative and scope: 'Never allow the stroller to be used as a toy' is a direct, faithful restatement of 'NEVER ALLOW YOUR STROLLER to be used as a toy.' No condition, direction, actor, or qualifier is added, omitted, or altered in a way that broadens or contradicts the original. The union of quotes supports the projection without unsupported addition.

Extractor notes: None recorded.

### claim_r2j_warning_damaged_discontinue

- Claim: `claim_r2j_warning_damaged_discontinue`
- Tier: `C3`
- Type/predicate: `WARNING` / `discontinue_if_damaged`

Object

```json
{
  "description": "Discontinue using the stroller should it become damaged or broken.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
DISCONTINUE USING YOUR STROLLER should it become damaged or broken.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection faithfully restates the exact warning from the quote: 'Discontinue using the stroller should it become damaged or broken.' No conditions, directions, actors, or qualifiers are added, omitted, or altered in a way that changes meaning. The imperative and conditional structure is preserved.

Extractor notes: None recorded.

### claim_r2j_warning_caregiver_assist

- Claim: `claim_r2j_warning_caregiver_assist`
- Tier: `C3`
- Type/predicate: `WARNING` / `caregiver_assist_entry_exit`

Object

```json
{
  "description": "Caregiver must always help the child get into and out of the stroller.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
CAREGIVER MUST always help child get into and out of the stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the assertion in the quote: 'Caregiver must always help the child get into and out of the stroller.' No qualifiers, conditions, directions, or actors are added, omitted, or altered in a way that changes meaning. The union of quotes supports the projection fully.

Extractor notes: None recorded.

### claim_r2j_warning_adult_assembly

- Claim: `claim_r2j_warning_adult_assembly`
- Tier: `C3`
- Type/predicate: `WARNING` / `adult_assembly_required`

Object

```json
{
  "description": "Adult assembly required.",
  "hazard_type": "general_safety"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
ADULT ASSEMBLY REQUIRED.
```

Verifier (claim quote union): `ENTAILED` — The projection 'Adult assembly required.' is a direct, faithful paraphrase of the exact quote 'ADULT ASSEMBLY REQUIRED.' with no added, omitted, or altered semantic conditions, directions, or qualifiers. The capitalization and punctuation differences do not affect the semantic assertion.

Extractor notes: Assigned C3 per work-order rule that every safety warning in the manual is a C3 WARNING claim, although this is an assembly requirement rather than an in-use hazard.

### claim_r2j_warning_car_seat_other_brands

- Claim: `claim_r2j_warning_car_seat_other_brands`
- Tier: `C3`
- Type/predicate: `WARNING` / `car_seat_brand_restriction`

Object

```json
{
  "description": "Improper use of this stroller with other manufacturers' car seats may result in serious injury or death.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Improper use of this stroller with other manufacturers’ car seats may result in serious injury or death.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The warning is faithfully preserved without any unsupported semantic addition or contradiction.

Extractor notes: None recorded.

### claim_r2j_warning_car_seat_fall_hazard

- Claim: `claim_r2j_warning_car_seat_fall_hazard`
- Tier: `C3`
- Type/predicate: `WARNING` / `car_seat_attachment_check`

Object

```json
{
  "description": "Always check that the infant car seat is securely attached to the stroller by pulling up on the car seat.",
  "hazard_type": "fall_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
FALL HAZARD: Always check that infant car seat is securely attached to stroller by pulling up on the car seat.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, faithful restatement of the warning in the quote, omitting only the label 'FALL HAZARD:' which is metadata not asserted as factual content. The core instruction — checking secure attachment by pulling up — is fully supported by the quote.

Extractor notes: None recorded.

### claim_r2j_warning_car_seat_harness

- Claim: `claim_r2j_warning_car_seat_harness`
- Tier: `C3`
- Type/predicate: `WARNING` / `car_seat_harness_required`

Object

```json
{
  "description": "Always secure the child with the car seat harness when using the car seat in the stroller.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
ALWAYS SECURE your child with the car seat harness when using the car seat in the stroller.  If your child is already in the car seat, check that the child is secured with the harness.
```

Verifier (claim quote union): `ENTAILED` — The projection exactly mirrors the first sentence of the quote, which is a direct imperative without omitted conditions or qualifiers. The second sentence in the quote is not required to support the projection, as the projection is a faithful subset of the source.

Extractor notes: None recorded.

### claim_r2j_warning_car_seat_read_manual

- Claim: `claim_r2j_warning_car_seat_read_manual`
- Tier: `C3`
- Type/predicate: `WARNING` / `car_seat_manual_required_reading`

Object

```json
{
  "description": "Read the manual provided with the Graco car seat before using it with the stroller; see the car seat owner's manual for maximum child size.",
  "hazard_type": "child_restraint_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
READ THE MANUAL provided with your Graco car seat before using it with your stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately combines the two quotes: it instructs to read the manual before using the car seat with the stroller (from quote 0), and directs to consult the owner’s manual for maximum child size (from quote 1). No condition, direction, unit, or actor is misrepresented or broadened. The union of quotes fully supports the semantic assertions in the projection.

Quote — binding 1, source `src_r2j_manual_v1`

```text
See Graco infant car seat owners manual for maximum size of child.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately combines the two quotes: it instructs to read the manual before using the car seat with the stroller (from quote 0), and directs to consult the owner’s manual for maximum child size (from quote 1). No condition, direction, unit, or actor is misrepresented or broadened. The union of quotes fully supports the semantic assertions in the projection.

Extractor notes: None recorded.

### claim_r2j_warning_belly_bar_not_restraint

- Claim: `claim_r2j_warning_belly_bar_not_restraint`
- Tier: `C3`
- Type/predicate: `WARNING` / `belly_bar_not_restraint`

Object

```json
{
  "description": "The belly bar is not a restraint device; always secure the child with the seat belt, and use care when installing the belly bar with a child in the stroller.",
  "hazard_type": "falling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Always secure your child with the seat belt. The belly bar is not a restraint device. Use care when installing the belly bar on the stroller with a child in the stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates all semantic assertions from the quote: (1) the belly bar is not a restraint device, (2) always secure the child with the seat belt, and (3) use care when installing the belly bar with a child in the stroller. No condition, direction, or qualifier is omitted or broadened; the union of quotes fully supports the projection.

Extractor notes: None recorded.

### claim_r2j_warning_apply_both_brakes

- Claim: `claim_r2j_warning_apply_both_brakes`
- Tier: `C3`
- Type/predicate: `WARNING` / `apply_both_brakes`

Object

```json
{
  "description": "Always apply both brakes; check that brakes are on by trying to push the stroller.",
  "hazard_type": "rolling_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Always apply both brakes. Check that brakes are on by trying to  push stroller.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the exact instructions from the quote: applying both brakes and verifying their engagement by attempting to push the stroller. No condition, direction, actor, or qualifier is added, omitted, or altered in a way that changes meaning.

Extractor notes: None recorded.

### claim_r2j_warning_recline_clearance

- Claim: `claim_r2j_warning_recline_clearance`
- Tier: `C3`
- Type/predicate: `WARNING` / `seat_adjustment_clearance`

Object

```json
{
  "description": "When adjusting the stroller seat, keep the child's head, arms, and legs clear of moving seat parts and the stroller frame.",
  "hazard_type": "entrapment_hazard"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
When making adjustments to the stroller seat, make sure child’s head, arms, and legs are clear of moving seat parts and stroller frame.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote, preserving the imperative to keep the child’s body parts clear of moving parts and frame during seat adjustment. No condition, direction, or qualifier is added or omitted that alters the meaning.

Extractor notes: None recorded.

### claim_r2j_part_click_connect_mounts

- Claim: `claim_r2j_part_click_connect_mounts`
- Tier: `C3`
- Type/predicate: `PART_LOCATION` / `click_connect_mounts_location`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
push down on car seat until the latches snap into the Click Connect™ mounts.
```

Verifier (claim quote union): `ENTAILED` — The quote describes pushing down on the car seat until latches snap into Click Connect™ mounts, which implies the mounts are located in the stroller seat where the latching occurs. The projection’s description of the location and function is semantically supported by the quote’s action and result.

Extractor notes: Location wording 'in the stroller seat' grounded in the page 31 text 'Find mounts in seat.'; diagram on page 31 labels the mount.

### claim_r2j_step_car_seat_1

- Claim: `claim_r2j_step_car_seat_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Recline the stroller seat back to its lowest position. Fold the canopy.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the union of quoted text; no additional conditions, directions, or qualifiers are introduced or omitted in a way that alters meaning.

Extractor notes: None recorded.

### claim_r2j_step_car_seat_2

- Claim: `claim_r2j_step_car_seat_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Find mounts in seat.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote's assertion without adding, omitting, or altering any condition, direction, actor, or scope. The union of quotes contains only this single statement, and the projection faithfully reproduces it.

Extractor notes: None recorded.

### claim_r2j_step_car_seat_3

- Claim: `claim_r2j_step_car_seat_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Insert car seat into stroller and push down on car seat until the latches snap into the Click Connect™ mounts.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote, including the sequence (insert, then push down) and the condition for completion (until latches snap into Click Connect mounts). No qualifiers, conditions, or directions are omitted or altered. The trademark symbol ™ is omitted, but that is a formatting detail, not a semantic assertion.

Extractor notes: None recorded.

### claim_r2j_step_car_seat_4

- Claim: `claim_r2j_step_car_seat_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Check that infant car seat is  securely attached by pulling  up on it.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the assertion in the quote: checking secure attachment of the infant car seat by pulling up on it. No condition, direction, unit, actor, or scope is added, omitted, or altered in a way that changes meaning. The union of quotes supports the projection fully.

Extractor notes: None recorded.

### claim_r2j_step_car_seat_5

- Claim: `claim_r2j_step_car_seat_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To remove car seat: squeeze release handle at back of car seat, and lift car seat out of the stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No qualifiers, conditions, directions, or scope have been added, removed, or altered. The projection faithfully restates the exact instruction without any unsupported semantic addition or omission that changes meaning.

Extractor notes: Removal action; kept in the attach_car_seat procedure as step 5 to mirror the manual's own numbering in section 4-G.

### claim_r2j_step_harness_1

- Claim: `claim_r2j_step_harness_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To open, press button on buckle to release the waist straps.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim copy of the single quote. No addition, omission, or alteration of meaning occurs. All semantic assertions in the projection are fully supported by the quote.

Extractor notes: None recorded.

### claim_r2j_step_harness_2

- Claim: `claim_r2j_step_harness_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To close, slide shoulder strap  connectors onto waist straps and insert into buckle.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of conditions, directions, actors, or scope occurs. The projection asserts nothing beyond what is explicitly stated in the quote.

Extractor notes: None recorded.

### claim_r2j_step_harness_3pt_1

- Claim: `claim_r2j_step_harness_3pt_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To open, press button on buckle to release the waist straps.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All semantic assertions in the projection are directly supported by the quote.

Extractor notes: First step of the '3 Point Harness' section (page 24). Identical wording to secure_child_5pt step 1 (page 23); the manual restates it at the start of the conversion sequence.

### claim_r2j_step_harness_3pt_2

- Claim: `claim_r2j_step_harness_3pt_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Slide shoulder strap connectors off of waist straps.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the quoted instruction: 'Slide shoulder strap connectors off of waist straps.' No conditions, directions, units, actors, or scope have been added, removed, or altered. The projection is a faithful subset of the source quote.

Extractor notes: None recorded.

### claim_r2j_step_harness_3pt_3

- Claim: `claim_r2j_step_harness_3pt_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Remove shoulder straps from stroller.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the single quote's assertion: 'Remove shoulder straps from stroller.' No conditions, qualifiers, or directions are omitted or added. The action is stated plainly and unconditionally in both, and no broader claim is made.

Extractor notes: None recorded.

### claim_r2j_step_harness_3pt_4

- Claim: `claim_r2j_step_harness_3pt_4`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Attach waist straps to harness buckle as shown.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote without adding, omitting, or altering any condition, direction, or qualifier. The phrase 'as shown' is preserved, maintaining the original instruction’s dependency on visual guidance.

Extractor notes: 'as shown' refers to the page 25 illustration of the 3-point buckle configuration; the attaching action itself is stated in text.

### claim_r2j_step_harness_3pt_5

- Claim: `claim_r2j_step_harness_3pt_5`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Use slide adjuster at waist for tighter adjustment.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion without adding, omitting, or altering any condition, direction, actor, or scope. No unsupported semantic addition or contradiction exists.

Extractor notes: Manual numbers the 3 Point Harness section continuously: steps 1-4 perform the conversion; steps 5-6 are use of the converted 3-point harness.

### claim_r2j_step_harness_3pt_6

- Claim: `claim_r2j_step_harness_3pt_6`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To open, press button on buckle to release the waist straps.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote; no addition, omission, or alteration of meaning occurs. All assertions in the projection are directly supported by the quote.

Extractor notes: Opening the converted 3-point harness; the manual keeps this in the same numbered sequence as the conversion steps.

### claim_r2j_step_harness_height_1

- Claim: `claim_r2j_step_harness_height_1`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To adjust harness height, insert shoulder straps into desired loop.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No conditions, qualifiers, directions, or units are omitted or altered. The action described is fully supported by the quote without any broadening, contradiction, or unsupported addition.

Extractor notes: Extracted because page 24's slide-adjuster step points here ('To adjust harness height, see page 27.') and the revision note names harness height among the deferred procedures.

### claim_r2j_step_harness_height_2

- Claim: `claim_r2j_step_harness_height_2`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Use slide adjuster for further adjustment.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the quote's assertion without adding, omitting, or altering any condition, direction, actor, or scope. The union of quotes contains only this single statement, and the projection faithfully reproduces it as-is.

Extractor notes: None recorded.

### claim_r2j_step_harness_height_3

- Claim: `claim_r2j_step_harness_height_3`
- Tier: `C3`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Use slide adjuster at shoulder and waist for further adjustment. Repeat on other side.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a verbatim copy of the single quote in the union. No addition, omission, or alteration of meaning occurs. All assertions in the projection are directly supported by the quote.

Extractor notes: This instruction is present as text on page 27 but is unnumbered in the manual (it sits beside the labeled diagram); numbered 3 here to keep the procedure sequence contiguous. Not diagram-only: the action, including 'Repeat on other side.', is stated in text.

## 4. C2 claims (6)

### claim_r2j_step_rear_wheels_1

- Claim: `claim_r2j_step_rear_wheels_1`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Turn stroller over. Locate tab (a) on pin of rear wheels and slot (b) in stroller and align them. Attach rear wheels to stroller as shown.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully combines and rephrases the sequence of actions from the quote without adding, omitting, or altering any semantic conditions, directions, or actors. All steps — turning over, locating, aligning, attaching — are explicitly stated in the quote and preserved in the projection.

Extractor notes: None recorded.

### claim_r2j_step_rear_wheels_2

- Claim: `claim_r2j_step_rear_wheels_2`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
CHECK that wheels are securely attached by pulling on wheel assemblies.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: checking wheel attachment by pulling on assemblies. No conditions, qualifiers, or directions are omitted or added that alter the meaning. The imperative 'Check' corresponds to 'CHECK' in the quote, and the method ('by pulling on wheel assemblies') is preserved verbatim in meaning.

Extractor notes: None recorded.

### claim_r2j_step_front_wheels_1

- Claim: `claim_r2j_step_front_wheels_1`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Attach front wheels to stroller as shown.
```

Verifier (claim quote union): `ENTAILED` — The projection 'Attach front wheels to stroller.' is a faithful subset of the quote 'Attach front wheels to stroller as shown.' The omitted phrase 'as shown' does not add a required condition or constraint that changes the core action; it merely indicates a visual reference, which is not semantically necessary for the action assertion itself.

Extractor notes: None recorded.

### claim_r2j_step_front_wheels_2

- Claim: `claim_r2j_step_front_wheels_2`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
CHECK that wheels are securely attached by pulling on wheel assemblies.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: checking wheel attachment by pulling on assemblies. No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The imperative 'Check' is semantically equivalent to 'CHECK' in context, and the rest of the phrasing is identical.

Extractor notes: None recorded.

### claim_r2j_step_wheel_removal_1

- Claim: `claim_r2j_step_wheel_removal_1`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Push release button to remove wheel assemblies.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion: 'Push release button to remove wheel assemblies.' No qualifiers, conditions, directions, or units are omitted or added that alter the meaning. The action described is fully supported by the quote.

Extractor notes: The manual's only wheel-removal instruction (Care & Maintenance, beach-cleaning bullet; pages 14-15 point here via 'For wheel removal see Care & Maintenance.'). Release button location is shown only in the page 36 illustration; text states the action only.

### claim_r2j_care_beach_cleaning

- Claim: `claim_r2j_care_beach_cleaning`
- Tier: `C2`
- Type/predicate: `CARE` / `beach_cleaning`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
WHEN USING YOUR STROLLER AT THE BEACH completely clean your stroller afterward to remove sand and salt from mechanisms and wheel assemblies.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quote: contaminants (sand, salt) are explicitly named; method (complete cleaning after beach use) matches 'completely clean your stroller afterward'; targets (mechanisms, wheel assemblies) are directly cited. No unsupported addition, condition loss, or semantic overreach.

Extractor notes: C2 because the cleaning involves wheel-assembly removal (same bullet continues 'Push release button to remove wheel assemblies.', extracted as claim_r2j_step_wheel_removal_1).

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (4)

### gap_specs_1

- Kind: `SOURCE_MISSING`
- Waives: `[]`

Reason: The manual (src_r2j_manual_v1), the only text source in this product's vault, states no product empty weight, no open or folded dimensions, no enumerated box contents (the page 10 parts list is diagram-only; the text only says to check that all parts are present), and no warranty terms (page 40 gives only contact channels for warranty information). The single spec-type fact literally stated in the text is 'No tools required.' (page 10), extracted as claim_r2j_spec_assembly_no_tools; it satisfies the SPEC floor but not the intent of the specs_limits checklist item. The remaining core specs cannot be extracted without fabrication.

Closes when: docs/workorders/workorder-ready2jet-gap-closure.md Task 1 lands source-vault/graco-ready2jet-2212125/specs/specs.md (official PDP spec transcription: product weight, open/folded dimensions, box contents, warranty), after which SPEC claims for those facts can be extracted.

### gap_fold_visual_1

- Kind: `UNDERIVABLE`
- Waives: `[]`

Reason: The manual's fold-page text (pages 33-35) ends at 'squeeze handle lever' followed by 'CHECK that the stroller is secure.' The physical frame-collapse motion between those two states is shown only in diagrams and is not stated in text, so no STEP claim for it was written (no inventing steps from diagrams).

Closes when: A measured visual annotation pass over the page 34-35 diagrams or the official fold video (src_r2j_fold_video_v1), or a manufacturer text source describing the collapse motion; see also the manifest collection_gaps entry on thumb-switch/handle-lever macro imagery.

### gap_compat_chart_1

- Kind: `SOURCE_MISSING`
- Waives: `[]`

Reason: The manual states only a generic compatibility claim ('COMPATIBLE WITH MOST GRACO® INFANT CAR SEATS', extracted as claim_r2j_compat_graco_infant_car_seats) and directs users to customer service or a QR code for specifics. No per-model compatibility chart exists in this product's vault, so per-counterpart COMPATIBILITY claims cannot be extracted here.

Closes when: The official compatibility chart PDF (held in the SnugRide product's vault per docs/workorders/evidence-pack-extraction-workorder.md §6.2) is cross-referenced during review, or a Ready2Jet-side compatibility source is added to this vault.

### gap_harness_reconvert_1

- Kind: `UNDERIVABLE`
- Waives: `[]`

Reason: The manual documents converting the 5-point harness to 3-point (pages 24-25) but states no dedicated reverse (3-point back to 5-point) sequence, in text or diagrams (pages 23-27 checked). Reattachment of the shoulder straps appears only implicitly, via the 5-point close step ('To close, slide shoulder strap connectors onto waist straps and insert into buckle.', page 23, claim_r2j_step_harness_2) and the harness-height loop insertion (page 27, claim_r2j_step_harness_height_1), so no convert_back procedure could be extracted without inventing a sequence.

Closes when: A manufacturer text source stating the 3-point-to-5-point reconversion sequence, or a reviewer decision that the page 23 close step plus the page 27 height-adjustment steps constitute the documented reverse path.

## 7. Batch-eligible C0/C1 spot-audit (35)

Spot-audit sample: `5` of `35` eligible claims. The sample is the five lowest SHA-256 ranks of `review-completion-v1\0<product>\0<claim_id>`, so it is stable and reproducible.

A clean sample may be confirmed as one explicit human batch decision. A failed sample removes batch eligibility; review every batch member individually.

Batch members

- `claim_r2j_step_fold_1`
- `claim_r2j_step_fold_2`
- `claim_r2j_step_fold_3`
- `claim_r2j_step_fold_4`
- `claim_r2j_step_fold_5`
- `claim_r2j_step_fold_6`
- `claim_r2j_step_fold_7`
- `claim_r2j_step_fold_tips_1`
- `claim_r2j_step_fold_tips_2`
- `claim_r2j_step_unfold_1`
- `claim_r2j_step_unfold_2`
- `claim_r2j_step_unfold_3`
- `claim_r2j_step_unfold_4`
- `claim_r2j_care_seat`
- `claim_r2j_care_frame`
- `claim_r2j_care_wheel_oil`
- `claim_r2j_spec_assembly_no_tools`
- `claim_r2j_step_canopy_1`
- `claim_r2j_step_canopy_2`
- `claim_r2j_step_canopy_3`
- `claim_r2j_step_brake_1`
- `claim_r2j_step_brake_2`
- `claim_r2j_step_recline_1`
- `claim_r2j_step_recline_2`
- `claim_r2j_step_belly_bar_1`
- `claim_r2j_step_belly_bar_2`
- `claim_r2j_step_belly_bar_3`
- `claim_r2j_care_inspection`
- `claim_r2j_care_sun_exposure`
- `claim_r2j_care_cup_holder`
- `claim_r2j_step_footrest_1`
- `claim_r2j_step_footrest_2`
- `claim_r2j_step_cup_holder_1`
- `claim_r2j_step_cup_holder_2`
- `claim_r2j_step_cup_holder_3`

Sample details

### claim_r2j_step_fold_tips_2

- Claim: `claim_r2j_step_fold_tips_2`
- Tier: `C0`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Pull stroller to rotate front wheels as shown.",
  "procedure": "fold_stroller_tips",
  "step_number": 2
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Pull stroller to rotate front wheels as shown.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote’s assertion without adding, omitting, or altering any condition, direction, actor, or scope. No unsupported semantic addition or contradiction exists.

Extractor notes: None recorded.

### claim_r2j_step_fold_1

- Claim: `claim_r2j_step_fold_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
1. Before folding stroller: (a) remove infant car seat if in use
```

Verifier (claim quote union): `ENTAILED` — The projection 'Remove infant car seat if in use.' is directly supported by the quote '1. Before folding stroller: (a) remove infant car seat if in use'. The projection omits the procedural context ('Before folding stroller'), but this omission does not broaden the claim or add unsupported semantics — it merely restates the conditional action without the parent step. No condition, direction, actor, or unit is misrepresented or lost in a way that changes meaning.

Extractor notes: None recorded.

### claim_r2j_step_canopy_3

- Claim: `claim_r2j_step_canopy_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Pull canopy visor out for use, push back under rim of canopy when not in use.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action instructions in the quote: pulling the canopy visor out for use and pushing it back under the rim when not in use. No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The union of quotes fully supports the projection as a faithful restatement.

Extractor notes: None recorded.

### claim_r2j_step_brake_2

- Claim: `claim_r2j_step_brake_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Push up on brake to unlock brakes.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's assertion: 'Push up on brake to unlock brakes.' No conditions, directions, units, or actors are added, omitted, or altered. The projection is a faithful subset of the source content.

Extractor notes: None recorded.

### claim_r2j_step_fold_2

- Claim: `claim_r2j_step_fold_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
(b) unlock brakes
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Unlock brakes.' is directly supported by the quote '(b) unlock brakes', which asserts the same action without adding or omitting any governing condition, direction, or qualifier. No unsupported semantic addition or contradiction exists.

Extractor notes: None recorded.
