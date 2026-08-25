# Review Queue — graco-ready2jet-2212125

Verification status: `FAILED`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.

## 1. MEANING_CHANGED alarms (0)

None.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (48)

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

Quote — binding 1, source `src_r2j_manual_v1`

```text
See Graco infant car seat owners manual for maximum size of child.
```

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

Extractor notes: Generic manufacturer statement, not a per-model chart. Page 29 restates it without the word MOST ('COMPATIBLE WITH GRACO® INFANT CAR SEATS'); same source, so not recorded as a conflict. Per-model compatibility (e.g. SnugRide chart) is not in this product's vault.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

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

Verifier: no verdict recorded.

Extractor notes: C2 because the cleaning involves wheel-assembly removal (same bullet continues 'Push release button to remove wheel assemblies.', extracted as claim_r2j_step_wheel_removal_1).

## 5. Unresolved verifier — C0/C1 (39)

### claim_r2j_part_belly_bar

- Claim: `claim_r2j_part_belly_bar`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `belly_bar_location`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_part_thumb_switch

- Claim: `claim_r2j_part_thumb_switch`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `thumb_switch_location`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_part_handle_lever

- Claim: `claim_r2j_part_handle_lever`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `handle_lever_location`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_1

- Claim: `claim_r2j_step_fold_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_2

- Claim: `claim_r2j_step_fold_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_3

- Claim: `claim_r2j_step_fold_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
(c) fold the canopy.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_4

- Claim: `claim_r2j_step_fold_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
2. To fold stroller: (a) slide thumb switch;
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_5

- Claim: `claim_r2j_step_fold_5`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
(b) squeeze handle lever
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_6

- Claim: `claim_r2j_step_fold_6`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
3. CHECK that the stroller is secure.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_7

- Claim: `claim_r2j_step_fold_7`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
4. Carry by belly bar.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_tips_1

- Claim: `claim_r2j_step_fold_tips_1`
- Tier: `C0`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

Object

```json
{
  "action": "Rotate cup holder for more compact fold.",
  "procedure": "fold_stroller_tips",
  "step_number": 1
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Rotate cup holder for more compact fold.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_fold_tips_2

- Claim: `claim_r2j_step_fold_tips_2`
- Tier: `C0`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_unfold_1

- Claim: `claim_r2j_step_unfold_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
1. To open stroller: (a) slide thumb switch;
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_unfold_2

- Claim: `claim_r2j_step_unfold_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
(b) squeeze handle lever and lift up
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_unfold_3

- Claim: `claim_r2j_step_unfold_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
(c) lift up handle
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_unfold_4

- Claim: `claim_r2j_step_unfold_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
2. CHECK that the stroller is completely latched open every time you open the stroller and before continuing with the rest of the assembly steps.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_seat

- Claim: `claim_r2j_care_seat`
- Tier: `C0`
- Type/predicate: `CARE` / `seat_cleaning`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
DO NOT MACHINE WASH SEAT. It should only be wiped with a mild soap, taking care not to soak the material. NO BLEACH.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_frame

- Claim: `claim_r2j_care_frame`
- Tier: `C0`
- Type/predicate: `CARE` / `frame_cleaning`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
TO CLEAN STROLLER FRAME, use only household soap and warm water. NO BLEACH or detergent.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_wheel_oil

- Claim: `claim_r2j_care_wheel_oil`
- Tier: `C0`
- Type/predicate: `CARE` / `wheel_lubrication`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
IF WHEEL SQUEAKS, use a light oil (e.g., 3-in-1, or sewing machine oil). It is important to get the oil into the axle and wheel assembly as illustrated.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_spec_assembly_no_tools

- Claim: `claim_r2j_spec_assembly_no_tools`
- Tier: `C0`
- Type/predicate: `SPEC` / `assembly_tools_required`
- Verifier state: document status is FAILED

Object

```json
{
  "detail": "No tools are required to assemble the stroller.",
  "value": "none"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
No tools required.
```

Verifier: no verdict recorded.

Extractor notes: Only spec-type fact literally stated in the manual text. Core specs (product weight, open/folded dimensions, box contents enumeration, warranty terms) are absent from the manual — see gaps.json gap_specs_1.

### claim_r2j_step_canopy_1

- Claim: `claim_r2j_step_canopy_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Pull forward to open canopy.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_canopy_2

- Claim: `claim_r2j_step_canopy_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Push backwards to close canopy.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_canopy_3

- Claim: `claim_r2j_step_canopy_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_brake_1

- Claim: `claim_r2j_step_brake_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Push down on brake to lock brakes.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_brake_2

- Claim: `claim_r2j_step_brake_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_recline_1

- Claim: `claim_r2j_step_recline_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To recline, push button down and pull seat towards the rear.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_recline_2

- Claim: `claim_r2j_step_recline_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To raise, pull both straps up.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_belly_bar_1

- Claim: `claim_r2j_step_belly_bar_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Attach child’s belly bar onto belly bar mounts. CHECK that Graco logo is aligned as shown.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_belly_bar_2

- Claim: `claim_r2j_step_belly_bar_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Pull on child’s belly bar to ensure it is secure.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_belly_bar_3

- Claim: `claim_r2j_step_belly_bar_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To remove child’s belly bar, press buttons on inside of both ends, and pull off.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_inspection

- Claim: `claim_r2j_care_inspection`
- Tier: `C1`
- Type/predicate: `CARE` / `periodic_inspection`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
FROM TIME TO TIME CHECK YOUR STROLLER  for loose screws, worn parts, torn material or stitching. Replace or repair the parts as needed. Use only Graco replacement parts.
```

Verifier: no verdict recorded.

Extractor notes: Assigned C1 rather than C0 because the check targets structural wear affecting safe use; noted per the assign-higher-when-unsure rule.

### claim_r2j_care_sun_exposure

- Claim: `claim_r2j_care_sun_exposure`
- Tier: `C0`
- Type/predicate: `CARE` / `sun_heat_exposure`
- Verifier state: document status is FAILED

Object

```json
{
  "effect": "fading or warping of parts",
  "restriction": "avoid excessive exposure to sun or heat"
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
EXCESSIVE EXPOSURE TO SUN OR HEAT could cause fading or warping of parts.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_wet_drying

- Claim: `claim_r2j_care_wet_drying`
- Tier: `C0`
- Type/predicate: `CARE` / `drying_after_wet`
- Verifier state: document status is FAILED

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

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_care_cup_holder

- Claim: `claim_r2j_care_cup_holder`
- Tier: `C0`
- Type/predicate: `CARE` / `cup_holder_cleaning`
- Verifier state: document status is FAILED

Object

```json
{
  "method": "dishwasher",
  "restrictions": [
    "top rack only"
  ]
}
```

Quote — binding 0, source `src_r2j_manual_v1`

```text
Cup holder is dishwasher safe (top rack only.)
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_footrest_1

- Claim: `claim_r2j_step_footrest_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To raise footrest, lift up as shown.
```

Verifier: no verdict recorded.

Extractor notes: 'as shown' refers to the page 21 illustration; the raising action itself is stated in text, so this is not a diagram-only step.

### claim_r2j_step_footrest_2

- Claim: `claim_r2j_step_footrest_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To lower, press buttons on bottom of foot rest and raise or lower footrest.
```

Verifier: no verdict recorded.

Extractor notes: Manual's step 2 is headed 'To lower' but its own text says 'raise or lower footrest'; the buttons are needed only for lowering (step 1 raises without them). 'foot rest' spacing is verbatim from the manual.

### claim_r2j_step_cup_holder_1

- Claim: `claim_r2j_step_cup_holder_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
Line up opening in cup holder with mount on stroller and press onto stroller tube.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_cup_holder_2

- Claim: `claim_r2j_step_cup_holder_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
MAKE SURE cup holder is snapped securely into mount by pulling down.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_r2j_step_cup_holder_3

- Claim: `claim_r2j_step_cup_holder_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is FAILED

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

Quote — binding 0, source `src_r2j_manual_v1`

```text
To remove, pull up on cup holder.
```

Verifier: no verdict recorded.

Extractor notes: Use-limit context for this accessory already extracted elsewhere: 1 lb (.45 kg) maximum load (claim_r2j_limit_cup_holder_weight), no hot liquids (claim_r2j_warning_hot_liquids), top-rack dishwasher cleaning (claim_r2j_care_cup_holder).

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

## 7. Auto-approved spot-audit (0)

None.
