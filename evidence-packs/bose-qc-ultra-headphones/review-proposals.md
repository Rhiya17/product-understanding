# Review Proposals — bose-qc-ultra-headphones

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `64`
- Existing human decisions: `7`
- Undecided claims covered here: `57`
- Existing decisions reopened by v2 alarms: `1`
- Total owner action items: `58`
- Proposed `NEEDS_RECHECK`: `14`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `44`
- Batch-eligible C0/C1: `33`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (14)

### `claim_bqcu2_aptx_adaptive_codec_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `bluetooth_codec_aptx_adaptive`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote states audio streams automatically using aptX Adaptive once headphones are connected, but does not mention any requirement for the device to be Snapdragon Sound-certified. Adding this condition in the projection introduces an unsupported governing condition, narrowing the scope beyond what the quote supports.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "codec": "aptX Adaptive",
  "condition": "when connected to a Snapdragon Sound-certified device"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `32`

```text
Once you connect the headphones, your device will  automatically stream audio using the aptX  Adaptive Bluetooth codec.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote states audio streams automatically using aptX Adaptive once headphones are connected, but does not mention any requirement for the device to be Snapdragon Sound-certified. Adding this condition in the projection introduces an unsupported governing condition, narrowing the scope beyond what the quote supports.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_bluetooth_device_name_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `SPEC` / `bluetooth_device_name`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds 'replaced by any name set in the Bose app', which is not mentioned or implied in the quote. The quote only states that if no name is set, the default appears — it does not assert that the default is replaceable via the app, nor does it specify the mechanism of replacement. This is an unsupported semantic addition.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "qualifier": "default name; replaced by any name set in the Bose app",
  "value": "BOSE QC ULTRA 2 HP"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `28`

```text
If you didn’t name your headphones, the default name appears. BOSE QC ULTRA 2 HP
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'replaced by any name set in the Bose app', which is not mentioned or implied in the quote. The quote only states that if no name is set, the default appears — it does not assert that the default is replaceable via the app, nor does it specify the mechanism of replacement. This is an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_bluetooth_range_1` — REOPENED AFTER V2 ALARM

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `bluetooth_range`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Prior decision status: **REOPENED** — explicitly reconfirm or amend the existing human disposition.
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; Conflict triage: DIFFERENT_SCOPE_OR_EVENT — Claim A describes operational conditions for reconnection (devices must be within 30 ft and powered on), while Claim B reports published Bluetooth range specifications (~30 ft or up to 33 ft) from product documentation, reflecting different contexts: usage behavior vs. technical specification.
- Proposed rationale: Verifier found a meaning change: The projection presents the range (30 ft / 9 m) as an unconditional value, but the quote explicitly conditions it on devices being both within range AND powered on — omitting the power condition wrongly implies the range alone is sufficient.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "unit": "ft",
  "unit_metric": "m",
  "value": 30,
  "value_metric": 9
}
```

Quote — binding 0, source `src_owners_guide_en`, page `28`

```text
The devices must be within range (30 ft or 9 m) and powered on.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection presents the range (30 ft / 9 m) as an unconditional value, but the quote explicitly conditions it on devices being both within range AND powered on — omitting the power condition wrongly implies the range alone is sufficient.

Extractor notes: The support specifications article reportedly states 'up to 33 feet' (per manifest notes), but that source has no local capture, so only the owner's-guide 30 ft / 9 m figure is claimed. Potential conflict to check when the article is captured.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_care_firmware_update_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `firmware_update_method`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds an unsupported assertion that updates can also be run from the Bose updater website (btu.Bose.com), which is not mentioned or implied in the quote. The quote only states updates begin automatically when connected to the Bose app and an update is available — no alternative method is referenced.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "instruction": "Updates begin automatically when connected to the Bose app and an update is available; updates can also be run from the Bose updater website (btu.Bose.com)."
}
```

Quote — binding 0, source `src_owners_guide_en`, page `44`

```text
The headphones begin updating automatically when connected to the Bose app and an update is available.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported assertion that updates can also be run from the Bose updater website (btu.Bose.com), which is not mentioned or implied in the quote. The quote only states updates begin automatically when connected to the Bose app and an update is available — no alternative method is referenced.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_compat_bose_speakers_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `COMPATIBILITY` / `simplesync_bose_speaker_compatibility`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The quote only states that headphones can connect to any Bose Smart Speaker or Bose Smart Soundbar, but the projection introduces 'SimpleSync' as a feature and lists specific models (including 'Bose Smart Ultra Soundbar' and 'Bose Portable Smart Speaker/Bose Portable Home Speaker') without any supporting quote asserting that these specific models or the 'SimpleSync' feature are involved in the connection capability. This adds unsupported semantic content.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "counterpart": "Bose Smart Speakers and Bose Smart Soundbars",
  "feature": "SimpleSync",
  "notes_list": [
    "Bose Smart Ultra Soundbar",
    "Bose Smart Soundbar",
    "Bose Portable Smart Speaker/Bose Portable Home Speaker"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `39`

```text
You can connect the headphones to any Bose Smart Speaker or  Bose Smart Soundbar.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote only states that headphones can connect to any Bose Smart Speaker or Bose Smart Soundbar, but the projection introduces 'SimpleSync' as a feature and lists specific models (including 'Bose Smart Ultra Soundbar' and 'Bose Portable Smart Speaker/Bose Portable Home Speaker') without any supporting quote asserting that these specific models or the 'SimpleSync' feature are involved in the connection capability. This adds unsupported semantic content.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_compat_fast_pair_android_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `COMPATIBILITY` / `fast_pair_android_requirement`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The quote only requires Android 6.0 or higher; the projection adds unmentioned requirements for Bluetooth and Location features to be enabled, which are not supported by any quote in the union.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "counterpart": "Android devices",
  "feature": "Google Fast Pair",
  "requirement": "Android 6.0 or higher, with Bluetooth and Location features enabled"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `31`

```text
T o use Fast Pair, you need an Android device running Android 6.0 or higher.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote only requires Android 6.0 or higher; the projection adds unmentioned requirements for Bluetooth and Location features to be enabled, which are not supported by any quote in the union.

Extractor notes: Quote preserves the PDF text-extraction artifact 'T o' (rendered 'To' in the printed guide).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_full_charge_time_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `full_charge_time`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds an unsupported qualifier: 'charging is slower while headphones are in use'. The quote only states 'Allow up to 3 hours to fully charge the headphones' — it does not mention usage affecting charge speed. This addition introduces a new conditional behavior not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "qualifier": "up to; charging is slower while headphones are in use",
  "unit": "hours",
  "value": 3
}
```

Quote — binding 0, source `src_owners_guide_en`, page `36`

```text
Allow up to 3 hours to fully charge the headphones.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported qualifier: 'charging is slower while headphones are in use'. The quote only states 'Allow up to 3 hours to fully charge the headphones' — it does not mention usage affecting charge speed. This addition introduces a new conditional behavior not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_part_aux_port_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `aux_port_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote only identifies the existence of a '2.5 mm AUX audio port' without specifying its location (left earcup), labeling in a diagram, or procedural context (aux procedure connecting cable). The projection adds spatial, diagrammatic, and procedural assertions unsupported by the quote.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 13,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "The 2.5 mm AUX audio port is on the left earcup (labeled in the controls diagram; the aux procedure connects the cable to the 2.5 mm port on the left earcup).",
  "part": "aux_audio_port"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `13`

```text
2.5 mm AUX audio port
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote only identifies the existence of a '2.5 mm AUX audio port' without specifying its location (left earcup), labeling in a diagram, or procedural context (aux procedure connecting cable). The projection adds spatial, diagrammatic, and procedural assertions unsupported by the quote.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_part_serial_number_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `PART_LOCATION` / `serial_number_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds specific instructions ('under the inner fabric', 'ear cushion and fabric must be peeled back to view it') not present in the quote, which only states the serial number is 'located inside the left earcup' without specifying access method or layering. This introduces an unsupported procedural condition and physical detail.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 45,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "The serial number is inside the left earcup, under the inner fabric (ear cushion and fabric must be peeled back to view it).",
  "part": "serial_number_marking"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `45`

```text
The serial number is located inside the left earcup.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds specific instructions ('under the inner fabric', 'ear cushion and fabric must be peeled back to view it') not present in the quote, which only states the serial number is 'located inside the left earcup' without specifying access method or layering. This introduces an unsupported procedural condition and physical detail.

Extractor notes: Assigned C2 (not C1): viewing the serial number requires removing the ear cushion and peeling the inner fabric, which the guide cautions can damage the headphones if done wrong.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_state_auto_sleep_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `auto_sleep_behavior`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds an unsupported wake behavior ('wake by putting them on or pressing the Bluetooth/Power button') not mentioned in the quote, which only describes the sleep condition. This is an unsupported semantic addition.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "behavior": "Headphones automatically sleep after 20 minutes disconnected with earcups laid flat, or 10 minutes in any other orientation; wake by putting them on or pressing the Bluetooth/Power button."
}
```

Quote — binding 0, source `src_owners_guide_en`, page `16`

```text
After the headphones are disconnected for 20 minutes with the earcups laid flat or 10 minutes in any other orientation, the headphones automatically sleep to conserve battery.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported wake behavior ('wake by putting them on or pressing the Bluetooth/Power button') not mentioned in the quote, which only describes the sleep condition. This is an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_state_default_power_on_mode_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `default_power_on_mode`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote states that headphones power on in Quiet mode by default, implying a fixed initial state. The projection adds a conditional behavior — 'after settings are changed, the headphones power on with the last settings used' — which is not supported by the quote. This introduces an unsupported semantic addition about persistence of user settings, contradicting the default-only assertion.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "qualifier": "after settings are changed, the headphones power on with the last settings used",
  "value": "Quiet mode"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `22`

```text
By default, the headphones power on in Quiet mode.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote states that headphones power on in Quiet mode by default, implying a fixed initial state. The projection adds a conditional behavior — 'after settings are changed, the headphones power on with the last settings used' — which is not supported by the quote. This introduces an unsupported semantic addition about persistence of user settings, contradicting the default-only assertion.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_state_lay_flat_disconnect_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `lay_flat_disconnect_behavior`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote specifies disconnection after 3 seconds only when earcups are laid flat or stored in the case; it does not mention any 10-minute disconnection for other orientations. Adding 'in any other orientation they disconnect after 10 minutes' introduces an unsupported condition and duration not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "behavior": "Headphones disconnect 3 seconds after being removed from the head with earcups laid flat or stored in the case; in any other orientation they disconnect after 10 minutes."
}
```

Quote — binding 0, source `src_owners_guide_en`, page `16`

```text
The headphones disconnect from your devices after 3 seconds when they are removed from your head with the earcups laid flat or when they are stored in the case.
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote specifies disconnection after 3 seconds only when earcups are laid flat or stored in the case; it does not mention any 10-minute disconnection for other orientations. Adding 'in any other orientation they disconnect after 10 minutes' introduces an unsupported condition and duration not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_step_pairing_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds specific product names ('BOSE QC ULTRA 2 HP' and 'name set in the Bose app') not mentioned in the quote, which only says 'Select the headphones from the list of available products.' This introduces unsupported semantic additions about default naming and app configuration, broadening the scope beyond what the quote supports.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Select the headphones (default name BOSE QC ULTRA 2 HP, or the name set in the Bose app) from the device's list of available products.",
  "procedure": "bluetooth_pairing",
  "step_number": 3,
  "target_parts": []
}
```

Quote — binding 0, source `src_owners_guide_en`, page `28`

```text
Select the headphones from the list of available products.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds specific product names ('BOSE QC ULTRA 2 HP' and 'name set in the Bose app') not mentioned in the quote, which only says 'Select the headphones from the list of available products.' This introduces unsupported semantic additions about default naming and app configuration, broadening the scope beyond what the quote supports.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_warning_vehicle_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `vehicle_operation_use`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The projection adds an unsupported condition: 'stop use immediately if the headphones interfere with attentiveness or hearing alarms and warning signals.' This directive does not appear in the source quote, which only advises caution and following applicable laws — it does not mandate immediate cessation under specified interference conditions. This constitutes an unsupported semantic addition.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Use while operating a vehicle is not recommended and may be prohibited by law in some locations; stop use immediately if the headphones interfere with attentiveness or hearing alarms and warning signals.",
  "hazard_type": "situational_awareness"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
Use of this product while operating a vehicle is not recommended and may be prohibited by law in some locations. Use caution and follow applicable laws regarding headphone use while operating a vehicle.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds an unsupported condition: 'stop use immediately if the headphones interfere with attentiveness or hearing alarms and warning signals.' This directive does not appear in the source quote, which only advises caution and following applicable laws — it does not mandate immediate cessation under specified interference conditions. This constitutes an unsupported semantic addition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (8)

### `claim_bqcu2_warning_hearing_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `hearing_damage_volume`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Do not use the headphones at high volume; turn the volume down before putting them on, then raise gradually to a comfortable, moderate level.",
  "hazard_type": "hearing_damage"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
To avoid hearing damage, do not use your headphones at a high volume. Turn the volume down on your product before placing the headphones in/on your ears, then turn the volume up gradually until you reach a comfortable, moderate listening level.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the core warnings and instructions from the quote: avoiding high volume, turning volume down before placement, and raising gradually to a comfortable moderate level. No condition, direction, or qualifier is added or omitted that alters the meaning.

Extractor notes: None recorded.

### `claim_bqcu2_warning_awareness_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `surrounding_sound_awareness`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Do not use the headphones where the inability to hear surrounding sounds may present a danger, e.g. cycling or walking in or near traffic, construction sites, or railroads.",
  "hazard_type": "situational_awareness"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
Do not use the headphones when the inability to clearly hear surrounding sounds may present a danger to yourself or others, for example while riding a bicycle or walking in or near traffic, a construction site, railroad, etc.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote, preserving the core condition (inability to hear surrounding sounds presenting danger) and the examples (cycling, walking near traffic, construction sites, railroads). No scope broadening, wrong actor/direction/unit, or lost governing condition occurs. The rephrasing is semantically equivalent.

Extractor notes: None recorded.

### `claim_bqcu2_warning_hinge_pinch_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `hinge_pinch_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Hold the middle of each earcup when rotating, folding, and casing the headphones; keep fingers away from the hinges to avoid pinching.",
  "hazard_type": "pinch_hazard"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
Place your hands around the middle of each earcup when rotating, folding, and placing the headphones in the case and removing from the case. Keep your fingers away from the hinges to avoid pinching.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully summarizes the quote: 'Hold the middle of each earcup' matches 'Place your hands around the middle of each earcup'; 'when rotating, folding, and casing' covers 'rotating, folding, and placing... in the case and removing from the case' (casing implies both insertion and removal); 'keep fingers away from the hinges to avoid pinching' is verbatim. No condition, direction, or qualifier is lost or broadened.

Extractor notes: None recorded.

### `claim_bqcu2_warning_not_for_children_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `not_for_children`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "The product is not intended for use by children.",
  "hazard_type": "child_safety"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
Product is not intended for use by children.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the assertion in the quote: 'Product is not intended for use by children.' No conditions, qualifiers, or directions are omitted or added. The projection does not broaden scope or introduce unsupported elements.

Extractor notes: None recorded.

### `claim_bqcu2_warning_choking_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `choking_hazard_small_parts`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Contains small parts which may be a choking hazard; not suitable for children under age 3.",
  "hazard_type": "choking_hazard"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `2`

```text
Contains small parts which may be a choking hazard. Not suitable for children under age 3.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the content of the quote: it preserves the warning about small parts being a choking hazard and the unsuitability for children under age 3, without adding, omitting, or altering any condition, direction, or qualifier.

Extractor notes: None recorded.

### `claim_bqcu2_warning_magnetic_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `magnetic_material_medical_devices`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "The product contains magnetic material; consult a physician about effects on implantable medical devices.",
  "hazard_type": "medical_device_interference"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `2`

```text
This product contains magnetic material. Consult your physician on whether this might affect your implantable medical device.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the core warning from the quote: magnetic material presence and the advisory to consult a physician regarding implantable medical devices. No unsupported addition, contradiction, or broadening of scope is introduced; the omission of 'your' before 'implantable medical device' does not alter the meaning, as the advisory is inherently personal and contextually implied.

Extractor notes: None recorded.

### `claim_bqcu2_warning_battery_removal_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `battery_removal_prohibited`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Do not attempt to remove the rechargeable lithium-ion battery; removal must be done by a Bose retailer or other qualified professional.",
  "hazard_type": "battery_hazard"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `5`

```text
DON’T attempt to remove the rechargeable lithium-ion battery from this product. Contact your local Bose retailer or other qualified professional for removal.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the warning from the quote: it prohibits user removal of the battery and restricts removal to Bose retailers or qualified professionals, exactly as stated in the source.

Extractor notes: None recorded.

### `claim_bqcu2_warning_unusual_noise_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `loud_unusual_noise`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c3`
- Review focus: HARD REVIEW — C3; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "description": "Do not use the headphones if they emit any loud unusual noise; turn them off and contact Bose customer service.",
  "hazard_type": "product_malfunction"
}
```

Quote — binding 0, source `src_safety_instructions_ml`, page `1`

```text
Do NOT use the headphones if they emit any loud unusual noise. If this  happens, turn the headphones off and contact Bose customer service.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the warning from the quote: do not use the headphones if they emit loud unusual noise, and in that case, turn them off and contact Bose customer service. The semicolon structure preserves the conditional sequence and imperative actions without adding, omitting, or altering any governing conditions, directions, or actors. All semantic assertions in the projection are directly supported by the quote.

Extractor notes: None recorded.

## 4. C2 claims (3)

### `claim_bqcu2_care_clean_exterior_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `exterior_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "instruction": "Gently wipe headband and exterior surfaces with a slightly damp cloth."
}
```

Quote — binding 0, source `src_owners_guide_en`, page `44`

```text
If the headband or other exterior surfaces need to be cleaned, gently wipe with a slightly damp cloth.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the instruction from the quote: 'gently wipe headband and exterior surfaces with a slightly damp cloth' is a direct paraphrase of 'gently wipe with a slightly damp cloth' applied to 'headband or other exterior surfaces'. No condition, direction, or qualifier is omitted or broadened; the imperative is preserved and matches the scope of the original conditional instruction.

Extractor notes: None recorded.

### `claim_bqcu2_care_no_cleaning_products_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `cleaning_product_prohibition`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "instruction": "Use only a water-dampened cloth; do not use cleaning products; do not let moisture enter through the ports or earcups."
}
```

Quote — binding 0, source `src_owners_guide_en`, page `44`

```text
Use only a water dampened cloth. Don’t use cleaning products. Don’t allow any moisture to enter the headphones through the ports or earcups.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates all semantic assertions from the quote: using only a water-dampened cloth, avoiding cleaning products, and preventing moisture entry through ports or earcups. No condition, direction, or qualifier is omitted or broadened; the union of quotes fully supports the projection.

Extractor notes: None recorded.

### `claim_bqcu2_compat_snapdragon_sound_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `COMPATIBILITY` / `snapdragon_sound_requirement`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `c2`
- Review focus: C2; individual decision required
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "counterpart": "Snapdragon Sound-certified devices",
  "feature": "Snapdragon Sound / aptX Adaptive",
  "requirement": "A Snapdragon Sound-certified device, such as a compatible Android device"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `32`

```text
T o experience Snapdragon Sound, you need a  Snapdragon Sound-certified device, such as a compatible Android device.
```

Verifier (claim quote union): `ENTAILED` — The projection's requirement exactly matches the quote's condition for experiencing Snapdragon Sound: a Snapdragon Sound-certified device, such as a compatible Android device. The counterpart and feature labels are not asserted as factual claims in the quote but are schema scaffolding per instructions; they do not introduce unsupported semantic additions. No contradiction, scope broadening, or lost condition exists.

Extractor notes: Quote preserves the PDF text-extraction artifact 'T o' (rendered 'To' in the printed guide).

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (4)

### `gap_macbook_1`

- Kind: `UNDERIVABLE`
- Waives: `["checklist:macbook_compatibility"]`
- Reason: No collected source on either side states MacBook pairing or wired compatibility. The owner's guide mentions 'a computer' only as a USB-C power source for charging/USB audio and never names MacBook; the aux instructions name only a generic 'source device'. The spec-page sources (src_product_page, src_specifications_article, src_support_product_page) have no local capture, and their manifest notes record no MacBook statement. Cross-product compatibility is underivable from this vault.
- Closes when: An official Bose or Apple source explicitly stating QC Ultra Headphones (2nd Gen) compatibility with MacBook (Bluetooth and/or 3.5 mm wired) is added to the vault — e.g. the Apple-side pairing guide in the apple-macbook-air-13-m3 vault, if it names third-party headphones, or a captured Bose support article.

### `gap_codecs_1`

- Kind: `UNDERIVABLE`
- Waives: `[]`
- Reason: The full Bluetooth codec list (e.g. SBC/AAC) is not enumerated in any collected source. The owner's guide documents only aptX Adaptive via Snapdragon Sound (claimed). The manifest's own collection_gaps confirms: 'Bluetooth codec list beyond aptX Adaptive (Snapdragon Sound) is not explicitly enumerated on official pages checked; SBC/AAC support not officially confirmed in collected sources.'
- Closes when: An official Bose source enumerating supported Bluetooth codecs is found and added to the vault.

### `gap_included_cable_lengths_1`

- Kind: `UNDERIVABLE`
- Waives: `[]`
- Reason: NARROWED 2026-08-24: USB-C cable length now claimed (39 in, claim_bqcu2_spec_usbc_cable_length_1); only the 3.5 mm-to-2.5 mm aux cable length remains unpublished in any source.
- Closes when: Bose publishes the aux cable length, or it is measured on a physical unit.

### `gap_spec_article_raw_capture_1`

- Kind: `SOURCE_MISSING`
- Waives: `[]`
- Reason: The support specifications article cannot be captured over HTTP (returns a JavaScript application shell with no content — attempted 2026-08-24). Bluetooth 5.4 and the 33 ft range currently rest on the registered curated transcription (src_specs_curated_v1).
- Closes when: The article is captured via a browser session and registered; then rebind claim_bqcu2_bluetooth_version_2 and claim_bqcu2_bluetooth_range_33ft_1 to the raw capture.

## 7. Batch-eligible C0/C1 spot-audit (33)

Batch ID: `batch_bose-qc-ultra-headphones_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `33` members of `batch_bose-qc-ultra-headphones_20260826`.
- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below individually.
- Owner / date: ______________________________

### `claim_bqcu2_battery_life_anc_on_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_life_anc_on_immersive_off`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "conditions": "noise cancellation On, immersive audio Off",
  "unit": "hours",
  "value": 30
}
```

Quote — binding 0, source `src_owners_guide_en`, page `36`

```text
30 hours with noise cancellation set to On and immersive audio set to Off.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the conditions (noise cancellation On, immersive audio Off) and the value (30 hours) as stated in the quote. No unsupported addition, contradiction, or scope broadening is present.

Extractor notes: None recorded.

### `claim_bqcu2_battery_life_anc_immersive_on_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_life_anc_on_immersive_on`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "conditions": "noise cancellation On, immersive audio On",
  "unit": "hours",
  "value": 23
}
```

Quote — binding 0, source `src_owners_guide_en`, page `36`

```text
23 hours with noise cancellation and immersive audio set to On.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the conditions (noise cancellation On, immersive audio On) and the value (23 hours) explicitly stated in the quote. No unsupported addition, contradiction, or scope broadening is present.

Extractor notes: None recorded.

### `claim_bqcu2_battery_life_all_off_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_life_anc_off_immersive_off`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "conditions": "noise cancellation Off, immersive audio Off",
  "unit": "hours",
  "value": 45
}
```

Quote — binding 0, source `src_owners_guide_en`, page `36`

```text
45 hours with noise cancellation and immersive audio set to Off.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '45 hours with noise cancellation and immersive audio set to Off,' which directly supports the projected conditions (both features Off), unit (hours), and value (45). No unsupported addition or contradiction exists.

Extractor notes: None recorded.

### `claim_bqcu2_multipoint_max_active_1` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `multipoint_max_active_devices`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "feature": "multi-point connection",
  "unit": "devices",
  "value": 2
}
```

Quote — binding 0, source `src_owners_guide_en`, page `29`

```text
By default, the headphones can  be actively connected to up to two devices at a time  (multi-point connection).
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states that headphones can be actively connected to up to two devices at a time via multi-point connection. The projection accurately captures the feature (multi-point connection), unit (devices), and value (2) without adding unsupported conditions, directions, or scope. No governing condition is omitted that would broaden the claim, and the value is directly supported by the quote.

Extractor notes: None recorded.

### `claim_bqcu2_device_list_capacity_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `paired_device_list_capacity`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "unit": "devices",
  "value": 6
}
```

Quote — binding 0, source `src_owners_guide_en`, page `27`

```text
You can store up to six devices in the headphone device list, and the headphones can  be actively connected to up to two devices at a time (multi-point  connection).
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'You can store up to six devices in the headphone device list,' which directly supports the projection's assertion of 'value': 6 with 'unit': 'devices'. No condition, direction, or qualifier is omitted that would broaden or alter the meaning; the projection is a faithful subset of the source claim.

Extractor notes: None recorded.

### `claim_bqcu2_box_contents_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `box_contents`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "items": [
    "Bose QuietComfort Ultra Headphones (2nd Gen)",
    "Carry case",
    "USB-C to USB-C cable",
    "3.5 mm to 2.5 mm audio cable"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `11`

```text
Confirm that the following parts are included: Bose QuietComfort Ultra Headphones (2nd Gen) Carry case USB-C® to USB-C cable 3.5 mm to 2.5 mm audio cable
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the items named in the quote without adding, omitting, or altering any semantic qualifiers, conditions, or directions; the union of quotes fully supports the asserted items.

Extractor notes: None recorded.

### `claim_bqcu2_aux_cable_spec_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `aux_cable_type`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "usage": "wired listening when a Bluetooth connection isn't available",
  "value": "2.5 mm to 3.5 mm audio cable"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `33`

```text
Use the 2.5 mm to 3.5 mm audio cable to listen to audio from your source device when a Bluetooth connection isn’t available.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the quote: the 2.5 mm to 3.5 mm audio cable is for wired listening specifically when Bluetooth is unavailable. No unsupported addition, contradiction, or scope broadening is present.

Extractor notes: None recorded.

### `claim_bqcu2_usb_audio_support_1` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `usb_c_audio_support`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "interface": "USB-C",
  "value": true
}
```

Quote — binding 0, source `src_owners_guide_en`, page `34`

```text
The  headphones support USB-C audio.
```

Verifier (claim quote union): `ENTAILED` — The quote states that the headphones support USB-C audio, which directly supports the semantic projection asserting an interface of USB-C with a value of true. No unsupported addition, contradiction, or lost condition is present.

Extractor notes: None recorded.

### `claim_bqcu2_custom_modes_max_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `listening_modes`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "custom_modes_max": 7,
  "preconfigured_modes": [
    "Quiet",
    "Aware",
    "Immersion",
    "Cinema"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `25`

```text
You can choose between four pre-configured modes   — Quiet, Aware, Immersion, or Cinema — or create up to seven of your own custom modes.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states four pre-configured modes by name and allows creation of up to seven custom modes, which exactly matches the projection’s assertions without adding, omitting, or misrepresenting conditions.

Extractor notes: None recorded.

### `claim_bqcu2_step_pairing_1`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "With the headphones powered on, press and hold the Bluetooth/Power button; after the power off tone and two white blinks, continue holding until the status light pulses blue (pairing mode).",
  "procedure": "bluetooth_pairing",
  "step_number": 1,
  "target_parts": [
    "bluetooth_power_button",
    "status_light"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `27`

```text
With the headphones powered on, press and hold the Bluetooth/Power button. You hear the power off tone and the status light blinks white twice. Continue  holding until the status light pulses blue.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the sequence in the quote: powering on, pressing and holding the button, hearing the power off tone and two white blinks, then continuing to hold until the light pulses blue. The addition of '(pairing mode)' is a reasonable inference from the context of Bluetooth pairing behavior and does not contradict or broaden the claim beyond what the quote supports — the pulsing blue light is the standard indicator for pairing mode in such devices, and the quote’s instruction implies this state is being entered.

Extractor notes: None recorded.

### `claim_bqcu2_step_pairing_2` — SPOT-AUDIT SAMPLE

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "On the source device, enable the Bluetooth feature.",
  "procedure": "bluetooth_pairing",
  "step_number": 2,
  "target_parts": []
}
```

Quote — binding 0, source `src_owners_guide_en`, page `28`

```text
On your device, enable the Bluetooth feature.
```

Verifier (claim quote union): `ENTAILED` — The projection 'On the source device, enable the Bluetooth feature.' is semantically supported by the quote 'On your device, enable the Bluetooth feature.' — 'your device' is reasonably interpreted as the source device in context, and no governing condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### `claim_bqcu2_step_store_1`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Place your hands around each earcup.",
  "procedure": "store_headphones",
  "step_number": 1,
  "target_parts": [
    "left_earcup",
    "right_earcup"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `42`

```text
Place your hands around each earcup.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the quoted instruction without adding, omitting, or altering any condition, direction, actor, or scope. The union of quotes contains this exact assertion, and no unsupported semantic addition is present.

Extractor notes: None recorded.

### `claim_bqcu2_step_store_2`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Rotate both earcups inward so they lay flat.",
  "procedure": "store_headphones",
  "step_number": 2,
  "target_parts": [
    "left_earcup",
    "right_earcup"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `42`

```text
Rotate both earcups inward so they lay flat.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the single quote's instruction without adding, omitting, or altering any condition, direction, or qualifier. The action described is fully supported by the quote as a union.

Extractor notes: None recorded.

### `claim_bqcu2_step_store_3` — SPOT-AUDIT SAMPLE

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Slide the earcups up into the headband.",
  "procedure": "store_headphones",
  "step_number": 3,
  "target_parts": [
    "left_earcup",
    "right_earcup",
    "headband"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `43`

```text
Slide the earcups up into the headband.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly matches the action described in the quote: 'Slide the earcups up into the headband.' No conditions, directions, units, or actors are added or altered. The projection is a faithful subset of the source quote’s meaning.

Extractor notes: None recorded.

### `claim_bqcu2_step_store_4`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Fold the left earcup up toward the headband and place the headphones in the case.",
  "procedure": "store_headphones",
  "step_number": 4,
  "target_parts": [
    "left_earcup",
    "headband",
    "carry_case"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `43`

```text
Fold the left earcup up toward the headband and place the headphones in  the case.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote without adding, omitting, or altering any condition, direction, actor, or scope. The quote union supports every assertion in the projection as a direct restatement.

Extractor notes: None recorded.

### `claim_bqcu2_step_clearlist_1`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Press and hold the Bluetooth/Power button and Multi-function button simultaneously until you hear a tone.",
  "procedure": "clear_paired_device_list",
  "step_number": 1,
  "target_parts": [
    "bluetooth_power_button",
    "multi_function_button"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `30`

```text
Press and hold the Bluetooth/Power button and Multi-function button  simultaneously until you hear a tone.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: pressing and holding both buttons simultaneously until a tone is heard. No conditions, qualifiers, or directions are omitted or added that would broaden or alter the meaning. The quote supports the projection as a faithful subset.

Extractor notes: None recorded.

### `claim_bqcu2_step_clearlist_2`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Delete the headphones from the Bluetooth list on each previously-connected device.",
  "procedure": "clear_paired_device_list",
  "step_number": 2,
  "target_parts": []
}
```

Quote — binding 0, source `src_owners_guide_en`, page `30`

```text
Delete your headphones from the Bluetooth list on your device. Repeat for each previously-connected device.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately summarizes the quote: 'Delete your headphones from the Bluetooth list on your device. Repeat for each previously-connected device.' The action 'Delete the headphones from the Bluetooth list on each previously-connected device' is a faithful semantic union of the two instructions — the first specifies the action on one device, the second generalizes it to all previously-connected devices. No condition, direction, or qualifier is omitted or broadened in a way that changes meaning.

Extractor notes: None recorded.

### `claim_bqcu2_step_aux_1`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Connect the audio cable to the 2.5 mm port on the left earcup.",
  "procedure": "connect_aux_cable",
  "step_number": 1,
  "target_parts": [
    "aux_audio_port",
    "left_earcup"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `33`

```text
Connect the cable to the 2.5 mm port on the left earcup.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the action and target from the quote: 'Connect the cable' becomes 'Connect the audio cable' (a reasonable specification without adding unsupported meaning), and 'to the 2.5 mm port on the left earcup' is preserved verbatim. No condition, direction, unit, or actor is misstated or broadened.

Extractor notes: None recorded.

### `claim_bqcu2_step_aux_2`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Connect the other end of the cable to the 3.5 mm port on the source device.",
  "procedure": "connect_aux_cable",
  "step_number": 2,
  "target_parts": []
}
```

Quote — binding 0, source `src_owners_guide_en`, page `33`

```text
Connect the other end of the cable to the 3.5 mm port on your source device.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: connecting the other end of the cable to the 3.5 mm port on the source device. No conditions, directions, units, or actors are added, omitted, or altered in a way that changes meaning. The quote supports the projection as a faithful subset.

Extractor notes: None recorded.

### `claim_bqcu2_step_usbaudio_1`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Connect the USB-C cable to the USB-C port on the left earcup.",
  "procedure": "connect_usb_audio",
  "step_number": 1,
  "target_parts": [
    "usb_c_port",
    "left_earcup"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `34`

```text
Connect the USB-C cable to the USB-C port on the left earcup.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection exactly mirrors the action described in the quote: connecting the USB-C cable to the USB-C port on the left earcup. No additional conditions, directions, units, or actors are introduced, and no governing conditions are omitted that would broaden or alter the meaning. The projection is a faithful subset of the source.

Extractor notes: None recorded.

### `claim_bqcu2_step_usbaudio_2`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Connect the other end to a USB-C power source such as a computer or wall charger.",
  "procedure": "connect_usb_audio",
  "step_number": 2,
  "target_parts": []
}
```

Quote — binding 0, source `src_owners_guide_en`, page `34`

```text
Connect the other end to a USB-C power source such as a computer or  wall charger.
```

Verifier (claim quote union): `ENTAILED` — The semantic projection is a direct, verbatim restatement of the single quote. No conditions, directions, units, actors, or qualifiers are added, omitted, or altered. The union of quotes fully supports the projection as written.

Extractor notes: None recorded.

### `claim_bqcu2_step_usbaudio_3`

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
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "action": "Power on the headphones.",
  "procedure": "connect_usb_audio",
  "step_number": 3,
  "target_parts": [
    "bluetooth_power_button"
  ]
}
```

Quote — binding 0, source `src_owners_guide_en`, page `34`

```text
Power on the headphones (see page 14).
```

Verifier (claim quote union): `ENTAILED` — The semantic projection 'Power on the headphones.' is directly supported by the quote 'Power on the headphones (see page 14).' The parenthetical reference to page 14 is procedural guidance and does not alter the core action asserted; omitting it does not broaden, contradict, or add unsupported conditions to the claim.

Extractor notes: None recorded.

### `claim_bqcu2_part_controls_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `headphone_controls_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 13,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "The controls (Bluetooth/Power button, Multi-function button, volume strip) are on the back of the right earcup.",
  "part": "headphone_controls"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `13`

```text
The headphone controls are located on the back of the right earcup.
```

Verifier (claim quote union): `ENTAILED` — The quote states that 'The headphone controls are located on the back of the right earcup,' which semantically supports the projection’s more specific claim that 'The controls (Bluetooth/Power button, Multi-function button, volume strip) are on the back of the right earcup.' The projection merely elaborates on what 'controls' include, without contradicting or broadening the scope beyond what the quote permits — the location is unchanged and the listed controls are a plausible subset or specification of 'controls.' No condition, direction, or qualifier is lost or wrongly implied.

Extractor notes: None recorded.

### `claim_bqcu2_part_status_light_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `status_light_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 13,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "The status light is on the left earcup.",
  "part": "status_light"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `37`

```text
The status light is located on the left earcup.
```

Verifier (claim quote union): `ENTAILED` — The projection 'The status light is on the left earcup.' is a faithful semantic subset of the quote 'The status light is located on the left earcup.' — 'located on' and 'on' are semantically equivalent in this context, and no governing condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### `claim_bqcu2_part_usb_c_port_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `usb_c_port_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 13,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "The USB-C port is on the left earcup.",
  "part": "usb_c_port"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `35`

```text
Connect the USB-C cable to the USB-C port on the left earcup.
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states that the USB-C port is on the left earcup, which directly supports the semantic projection's claim about the port's location.

Extractor notes: None recorded.

### `claim_bqcu2_part_call_microphones_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `call_microphones_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
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
    "page": 18,
    "source_id": "src_owners_guide_en"
  },
  "location_description": "Four microphones for phone calls are on the front of the headphones — two on the left earcup and two on the right earcup.",
  "part": "call_microphones"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `18`

```text
There are four microphones on the front of the headphones for phone calls   — two on the left earcup and two on the right earcup.
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully restates the exact spatial and functional claims from the quote: four microphones for phone calls, located on the front of the headphones, with two on each earcup. No condition, direction, unit, or actor is added, omitted, or altered in a way that broadens or contradicts the original.

Extractor notes: None recorded.

### `claim_bqcu2_state_pairing_light_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `bluetooth_pairing_indicator`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "light_activity": "Pulsing blue",
  "system_state": "Ready to connect"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `37`

```text
Pulsing blue Ready to connect
```

Verifier (claim quote union): `ENTAILED` — The projection's 'light_activity' and 'system_state' fields directly map to the two semantic components in the quote: 'Pulsing blue' and 'Ready to connect', with no added conditions, directions, or unsupported qualifiers.

Extractor notes: None recorded.

### `claim_bqcu2_state_charging_light_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `charging_indicator`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "light_activity": "Solid amber while charging; solid white when fully charged",
  "system_state": "Charging / Full charge"
}
```

Quote — binding 0, source `src_owners_guide_en`, page `35`

```text
The headphones begin charging, and the status light glows solid amber. When the headphones are fully charged, the status light glows solid white.
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the light behavior described: solid amber during charging and solid white at full charge. The system states 'Charging / Full charge' are directly inferable from the quoted conditions without adding unsupported conditions, directions, or scope.

Extractor notes: None recorded.

### `claim_bqcu2_limit_single_audio_stream_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `LIMIT` / `max_simultaneous_audio_streams`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "context": "multi-point connection: two devices connected, audio from one at a time",
  "unit": "device",
  "value": 1
}
```

Quote — binding 0, source `src_owners_guide_en`, page `29`

```text
You can only play audio from one device at a time.
```

Verifier (claim quote union): `ENTAILED` — The quote 'You can only play audio from one device at a time' directly supports the projection's assertion that in a multi-point connection context, audio is limited to one device at a time. The unit 'device' and value '1' are faithful to the quote’s restriction. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### `claim_bqcu2_bluetooth_version_2` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `bluetooth_version`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "value": "5.4"
}
```

Quote — binding 0, source `src_specs_curated_v1`, page `None`

```text
Bluetooth version: 5.4
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'Bluetooth version: 5.4', which directly supports the projection's value of '5.4' without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: Supersedes claim_bqcu2_bluetooth_version_1 (REJECTED_FOR_SERVING 2026-08-24 — bound only to manifest notes). Bound to the registered curated spec transcription; the raw support-article capture is still pending (gap_spec_article_raw_capture_1).

### `claim_bqcu2_spec_headphone_weight_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `headphone_weight`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "scope": "headphones only, without case",
  "unit": "lb",
  "unit_metric": "g",
  "value": 0.583,
  "value_metric": 264
}
```

Quote — binding 0, source `src_product_page_capture_v1`, page `None`

```text
Headphone 1.772" H x 6.299" W x 8.071" D (0.583 lb)
```

Verifier (claim quote union): `ENTAILED` — The projection's assertions are fully supported by the union of quotes: 'Headphones only: 0.583 lb (~264 g)' directly provides the scope, unit, value, and metric equivalent; the first quote's dimensions are irrelevant to the projection's claims and do not contradict them.

Quote — binding 1, source `src_specs_curated_v1`, page `None`

```text
Headphones only: 0.583 lb (~264 g)
```

Verifier (claim quote union): `ENTAILED` — The projection's assertions are fully supported by the union of quotes: 'Headphones only: 0.583 lb (~264 g)' directly provides the scope, unit, value, and metric equivalent; the first quote's dimensions are irrelevant to the projection's claims and do not contradict them.

Extractor notes: Closes gap_weight_1. Primary binding is the raw product-page capture; curated transcription corroborates and adds the metric figure.

### `claim_bqcu2_spec_usb_audio_format_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `usb_audio_format`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "interface": "USB-C",
  "quality": "lossless",
  "value": "16-bit, 44.1 kHz or 48 kHz"
}
```

Quote — binding 0, source `src_product_page_capture_v1`, page `None`

```text
can receive audio signals at 16-bit, 44.1kHz or 48kHz from compatible source files
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports that USB-C carries lossless audio at 16-bit, 44.1 kHz or 48 kHz from compatible source files; the projection omits the source compatibility condition but does not broaden the claim beyond what is supported, as the projection does not assert universality or unconditional operation.

Quote — binding 1, source `src_specs_curated_v1`, page `None`

```text
supports lossless digital audio over the included USB-C cable at 16-bit, 44.1 kHz or 48 kHz from compatible source files
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports that USB-C carries lossless audio at 16-bit, 44.1 kHz or 48 kHz from compatible source files; the projection omits the source compatibility condition but does not broaden the claim beyond what is supported, as the projection does not assert universality or unconditional operation.

Extractor notes: Closes gap_usb_lossless_1.

### `claim_bqcu2_spec_usbc_cable_length_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `included_usbc_cable_length`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": "QCUH2-HEADPHONEARN",
  "state": null
}
```

Object

```json
{
  "item": "USB-C to USB-C cable",
  "unit": "in",
  "value": 39
}
```

Quote — binding 0, source `src_specs_curated_v1`, page `None`

```text
USB-C to USB-C cable (39 in)
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states 'USB-C to USB-C cable (39 in)', which directly supports the projection's item, unit, and value without adding or omitting any governing conditions or semantic qualifiers.

Extractor notes: Partially closes gap_included_cable_lengths_1; the 3.5 mm-to-2.5 mm aux cable length remains unpublished.
