# Review Proposals — bose-qc-ultra-headphones

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `64`
- Existing human decisions: `7`
- Undecided claims covered here: `57`
- Proposed `NEEDS_RECHECK`: `40`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `17`
- Batch-eligible C0/C1: `13`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (40)

### `claim_bqcu2_aptx_adaptive_codec_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `bluetooth_codec_aptx_adaptive`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds a condition ('when connected to a Snapdragon Sound-certified device') not present in the quote, which restricts the behavior to a specific device type, whereas the quote states the behavior occurs automatically upon connecting headphones without any such qualification.

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

Verifier: `MEANING_CHANGED` — The translation adds a condition ('when connected to a Snapdragon Sound-certified device') not present in the quote, which restricts the behavior to a specific device type, whereas the quote states the behavior occurs automatically upon connecting headphones without any such qualification.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_aux_cable_spec_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `aux_cable_type`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'aux_cable_type' as a predicate and 'SPEC' as type, which are not in the quote; it also rephrases 'listen to audio from your source device' as 'wired listening', which is a generalization not present in the original and may imply broader usage than stated.

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

Verifier: `MEANING_CHANGED` — The translation adds 'aux_cable_type' as a predicate and 'SPEC' as type, which are not in the quote; it also rephrases 'listen to audio from your source device' as 'wired listening', which is a generalization not present in the original and may imply broader usage than stated.

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
- Proposed rationale: Verifier found a meaning change: The translation adds 'replaced by any name set in the Bose app', which is not stated in the quote. The quote only says the default name appears if no name is set — it does not mention the Bose app or replacement behavior.

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

Verifier: `MEANING_CHANGED` — The translation adds 'replaced by any name set in the Bose app', which is not stated in the quote. The quote only says the default name appears if no name is set — it does not mention the Bose app or replacement behavior.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_box_contents_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `box_contents`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation drops the registered trademark symbol '®' from 'USB-C®', altering the legal and branding specificity of the original quote.

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

Verifier: `MEANING_CHANGED` — The translation drops the registered trademark symbol '®' from 'USB-C®', altering the legal and branding specificity of the original quote.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_care_clean_exterior_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `exterior_cleaning`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation drops the conditional 'If...need to be cleaned', making the instruction unconditional, which changes the meaning by implying the action is always required rather than situational.

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

Verifier: `MEANING_CHANGED` — The translation drops the conditional 'If...need to be cleaned', making the instruction unconditional, which changes the meaning by implying the action is always required rather than situational.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_care_firmware_update_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `CARE` / `firmware_update_method`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds information not in the quote: that updates can also be run from the Bose updater website (btu.Bose.com). The original quote only mentions automatic updates via the Bose app, with no reference to an alternative method.

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

Verifier: `MEANING_CHANGED` — The translation adds information not in the quote: that updates can also be run from the Bose updater website (btu.Bose.com). The original quote only mentions automatic updates via the Bose app, with no reference to an alternative method.

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
- Proposed rationale: Verifier found a meaning change: The translation adds 'SimpleSync' as a feature and lists specific models not mentioned in the quote, implying a technical requirement or limitation absent from the original. The quote states general compatibility with any Bose Smart Speaker or Soundbar; the translation narrows it to devices supporting SimpleSync and enumerates models, altering scope and conditions.

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

Verifier: `MEANING_CHANGED` — The translation adds 'SimpleSync' as a feature and lists specific models not mentioned in the quote, implying a technical requirement or limitation absent from the original. The quote states general compatibility with any Bose Smart Speaker or Soundbar; the translation narrows it to devices supporting SimpleSync and enumerates models, altering scope and conditions.

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
- Proposed rationale: Verifier found a meaning change: The translation adds 'with Bluetooth and Location features enabled' as a requirement, which is not stated in the original quote. The original only specifies Android 6.0 or higher; adding unmentioned conditions changes the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds 'with Bluetooth and Location features enabled' as a requirement, which is not stated in the original quote. The original only specifies Android 6.0 or higher; adding unmentioned conditions changes the meaning.

Extractor notes: Quote preserves the PDF text-extraction artifact 'T o' (rendered 'To' in the printed guide).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_compat_snapdragon_sound_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C2`
- Type / predicate: `COMPATIBILITY` / `snapdragon_sound_requirement`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; C2; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'aptX Adaptive' as a feature under 'Snapdragon Sound', which is not mentioned in the source quote and introduces unverified technical specificity.

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

Verifier: `MEANING_CHANGED` — The translation adds 'aptX Adaptive' as a feature under 'Snapdragon Sound', which is not mentioned in the source quote and introduces unverified technical specificity.

Extractor notes: Quote preserves the PDF text-extraction artifact 'T o' (rendered 'To' in the printed guide).

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_device_list_capacity_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `paired_device_list_capacity`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation omits the critical detail that headphones can be actively connected to up to two devices at a time (multi-point connection), reducing the specification to only storage capacity. This drops a key functional constraint and misrepresents the product’s behavior.

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

Verifier: `MEANING_CHANGED` — The translation omits the critical detail that headphones can be actively connected to up to two devices at a time (multi-point connection), reducing the specification to only storage capacity. This drops a key functional constraint and misrepresents the product’s behavior.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_full_charge_time_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `full_charge_time`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds the qualifier 'charging is slower while headphones are in use', which is not mentioned in the original quote. This introduces new conditional information not present in the source, altering the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds the qualifier 'charging is slower while headphones are in use', which is not mentioned in the original quote. This introduces new conditional information not present in the source, altering the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_limit_single_audio_stream_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `LIMIT` / `max_simultaneous_audio_streams`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'multi-point connection: two devices connected' which is not stated in the quote. The quote only restricts playing audio from one device at a time, without specifying that two devices are connected or that this is a multi-point scenario. This addition changes the meaning by implying a specific setup not mentioned in the source.

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

Verifier: `MEANING_CHANGED` — The translation adds 'multi-point connection: two devices connected' which is not stated in the quote. The quote only restricts playing audio from one device at a time, without specifying that two devices are connected or that this is a multi-point scenario. This addition changes the meaning by implying a specific setup not mentioned in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_multipoint_max_active_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `multipoint_max_active_devices`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation omits 'by default' and 'at a time', implying the limit is absolute rather than the default behavior, and drops the temporal qualifier 'at a time', which may imply concurrency — altering the condition under which the specification applies.

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

Verifier: `MEANING_CHANGED` — The translation omits 'by default' and 'at a time', implying the limit is absolute rather than the default behavior, and drops the temporal qualifier 'at a time', which may imply concurrency — altering the condition under which the specification applies.

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
- Proposed rationale: Verifier found a meaning change: The translation adds specific location details (left earcup, labeled in controls diagram, aux procedure connects cable) not present in the source quote, which only states '2.5 mm AUX audio port' without any spatial or procedural context.

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

Verifier: `MEANING_CHANGED` — The translation adds specific location details (left earcup, labeled in controls diagram, aux procedure connects cable) not present in the source quote, which only states '2.5 mm AUX audio port' without any spatial or procedural context.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_part_controls_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `headphone_controls_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds specific details (Bluetooth/Power button, Multi-function button, volume strip) not present in the original quote, which only generically refers to 'headphone controls' without specifying their types or functions.

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

Verifier: `MEANING_CHANGED` — The translation adds specific details (Bluetooth/Power button, Multi-function button, volume strip) not present in the original quote, which only generically refers to 'headphone controls' without specifying their types or functions.

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
- Proposed rationale: Verifier found a meaning change: The translation adds specific instructions ('under the inner fabric', 'ear cushion and fabric must be peeled back to view it') not present in the quote, which alters the meaning by implying a required action and location detail not stated.

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

Verifier: `MEANING_CHANGED` — The translation adds specific instructions ('under the inner fabric', 'ear cushion and fabric must be peeled back to view it') not present in the quote, which alters the meaning by implying a required action and location detail not stated.

Extractor notes: Assigned C2 (not C1): viewing the serial number requires removing the ear cushion and peeling the inner fabric, which the guide cautions can damage the headphones if done wrong.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_part_usb_c_port_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `usb_c_port_location`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote instructs to connect a USB-C cable to the port on the left earcup, implying an action; the translation only states the port's location without mentioning the connection action, thus omitting a key directive.

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

Verifier: `MEANING_CHANGED` — The quote instructs to connect a USB-C cable to the port on the left earcup, implying an action; the translation only states the port's location without mentioning the connection action, thus omitting a key directive.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_spec_headphone_weight_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `headphone_weight`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'headphones only, without case' and metric conversion (264g), which are not stated in the quote; the quote only gives dimensions and weight without specifying exclusion of case or providing metric equivalents. Translation adds 'without case' which is not stated in the quote; quote only says 'Headphones only', which may or may not imply exclusion of case.

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

Verifier: `MEANING_CHANGED` — The translation adds 'headphones only, without case' and metric conversion (264g), which are not stated in the quote; the quote only gives dimensions and weight without specifying exclusion of case or providing metric equivalents.

Quote — binding 1, source `src_specs_curated_v1`, page `None`

```text
Headphones only: 0.583 lb (~264 g)
```

Verifier: `MEANING_CHANGED` — Translation adds 'without case' which is not stated in the quote; quote only says 'Headphones only', which may or may not imply exclusion of case.

Extractor notes: Closes gap_weight_1. Primary binding is the raw product-page capture; curated transcription corroborates and adds the metric figure.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_spec_usb_audio_format_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `usb_audio_format`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'USB-C' and 'lossless' which are not mentioned in the quote; the quote only states capability to receive audio signals at specified bit depth and sample rates from compatible source files, without specifying interface or quality type. Translation omits 'from compatible source files', implying the device always outputs lossless audio at those specs regardless of source, which contradicts the conditional in the quote.

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

Verifier: `MEANING_CHANGED` — The translation adds 'USB-C' and 'lossless' which are not mentioned in the quote; the quote only states capability to receive audio signals at specified bit depth and sample rates from compatible source files, without specifying interface or quality type.

Quote — binding 1, source `src_specs_curated_v1`, page `None`

```text
supports lossless digital audio over the included USB-C cable at 16-bit, 44.1 kHz or 48 kHz from compatible source files
```

Verifier: `MEANING_CHANGED` — Translation omits 'from compatible source files', implying the device always outputs lossless audio at those specs regardless of source, which contradicts the conditional in the quote.

Extractor notes: Closes gap_usb_lossless_1.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_state_auto_sleep_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `auto_sleep_behavior`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: Translation adds 'wake by putting them on or pressing the Bluetooth/Power button,' which is not stated in the quote and introduces new behavioral information not present in the source.

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

Verifier: `MEANING_CHANGED` — Translation adds 'wake by putting them on or pressing the Bluetooth/Power button,' which is not stated in the quote and introduces new behavioral information not present in the source.

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
- Proposed rationale: Verifier found a meaning change: The translation adds the condition 'after settings are changed, the headphones power on with the last settings used', which is not mentioned in the quote. The quote states a simple default behavior without any conditional or historical dependency.

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

Verifier: `MEANING_CHANGED` — The translation adds the condition 'after settings are changed, the headphones power on with the last settings used', which is not mentioned in the quote. The quote states a simple default behavior without any conditional or historical dependency.

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
- Proposed rationale: Verifier found a meaning change: The translation adds a condition not in the quote: 'in any other orientation they disconnect after 10 minutes.' The original only specifies disconnection after 3 seconds under two conditions (earcups laid flat or stored in case) and says nothing about other orientations or a 10-minute timeout.

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

Verifier: `MEANING_CHANGED` — The translation adds a condition not in the quote: 'in any other orientation they disconnect after 10 minutes.' The original only specifies disconnection after 3 seconds under two conditions (earcups laid flat or stored in case) and says nothing about other orientations or a 10-minute timeout.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_state_pairing_light_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STATE` / `bluetooth_pairing_indicator`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured fields ('light_activity', 'system_state', 'predicate', 'type') and implies a Bluetooth pairing context not present in the quote, which only states 'Pulsing blue Ready to connect' without specifying Bluetooth or system state semantics.

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

Verifier: `MEANING_CHANGED` — The translation adds structured fields ('light_activity', 'system_state', 'predicate', 'type') and implies a Bluetooth pairing context not present in the quote, which only states 'Pulsing blue Ready to connect' without specifying Bluetooth or system state semantics.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_step_aux_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'audio' to 'cable', specifying a type not present in the original quote, which simply says 'cable'. This introduces an unwarranted qualifier that changes the meaning by implying a specific cable type.

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

Verifier: `MEANING_CHANGED` — The translation adds 'audio' to 'cable', specifying a type not present in the original quote, which simply says 'cable'. This introduces an unwarranted qualifier that changes the meaning by implying a specific cable type.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_aux_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation drops 'your' before 'source device', which changes the meaning by removing the possessive qualifier that implies the device belongs to the user. This is a subtle but meaningful change in instruction context.

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

Verifier: `MEANING_CHANGED` — The translation drops 'your' before 'source device', which changes the meaning by removing the possessive qualifier that implies the device belongs to the user. This is a subtle but meaningful change in instruction context.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_clearlist_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not specify.

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying context and structure the original does not specify.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_clearlist_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation incorrectly states 'Delete the headphones from the Bluetooth list on each previously-connected device,' implying the headphones are deleted from the list on those other devices. The original quote instructs to delete the headphones from the Bluetooth list on 'your device' and to repeat this action for each previously-connected device — meaning the user's own device, not the other devices. This misattributes the location of the deletion action, changing the meaning.

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

Verifier: `MEANING_CHANGED` — The translation incorrectly states 'Delete the headphones from the Bluetooth list on each previously-connected device,' implying the headphones are deleted from the list on those other devices. The original quote instructs to delete the headphones from the Bluetooth list on 'your device' and to repeat this action for each previously-connected device — meaning the user's own device, not the other devices. This misattributes the location of the deletion action, changing the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_pairing_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds '(pairing mode)' which is not mentioned in the original quote; this implies a specific functional state not stated in the source, altering the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds '(pairing mode)' which is not mentioned in the original quote; this implies a specific functional state not stated in the source, altering the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_pairing_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'source device' which is not in the original quote; the original says 'your device', which is generic and does not specify 'source' as a role in a pairing context. This introduces a new qualifier that changes the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds 'source device' which is not in the original quote; the original says 'your device', which is generic and does not specify 'source' as a role in a pairing context. This introduces a new qualifier that changes the meaning.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_pairing_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds specific product names (BOSE QC ULTRA 2 HP) and mentions the Bose app, which are not present in the original quote. It also adds procedural context (bluetooth_pairing, step_number, target_parts) not stated in the source, altering the meaning by introducing unverified details.

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

Verifier: `MEANING_CHANGED` — The translation adds specific product names (BOSE QC ULTRA 2 HP) and mentions the Bose app, which are not present in the original quote. It also adds procedural context (bluetooth_pairing, step_number, target_parts) not stated in the source, altering the meaning by introducing unverified details.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_store_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds specific target parts ('left_earcup', 'right_earcup') and procedural context ('store_headphones', 'step_number':1) not present in the original quote, which only generically instructs to 'Place your hands around each earcup' without specifying which earcup or for what procedure.

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

Verifier: `MEANING_CHANGED` — The translation adds specific target parts ('left_earcup', 'right_earcup') and procedural context ('store_headphones', 'step_number':1) not present in the original quote, which only generically instructs to 'Place your hands around each earcup' without specifying which earcup or for what procedure.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_store_2`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote. The quote is a simple imperative instruction; the translation frames it as a formal procedure step with identifiers and parts, which changes its meaning by implying context, structure, and purpose not stated.

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote. The quote is a simple imperative instruction; the translation frames it as a formal procedure step with identifiers and parts, which changes its meaning by implying context, structure, and purpose not stated.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_store_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure context the original does not state.

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters the meaning by implying a formal procedure context the original does not state.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_step_usbaudio_3`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds specific procedural details (connect_usb_audio, step_number: 3, target_parts: bluetooth_power_button) not present in the source quote, which only generically instructs to 'Power on the headphones (see page 14)'. These additions alter the meaning by implying a specific method, sequence, and component, which the source does not specify.

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

Verifier: `MEANING_CHANGED` — The translation adds specific procedural details (connect_usb_audio, step_number: 3, target_parts: bluetooth_power_button) not present in the source quote, which only generically instructs to 'Power on the headphones (see page 14)'. These additions alter the meaning by implying a specific method, sequence, and component, which the source does not specify.

Extractor notes: None recorded.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_bqcu2_warning_awareness_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `surrounding_sound_awareness`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: Translation drops 'to yourself or others' from the original, narrowing the scope of danger from including others to only situational awareness, which alters the intended safety warning.

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

Verifier: `MEANING_CHANGED` — Translation drops 'to yourself or others' from the original, narrowing the scope of danger from including others to only situational awareness, which alters the intended safety warning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_warning_battery_removal_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `battery_removal_prohibited`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds 'removal must be done by a Bose retailer or other qualified professional,' which is not stated in the quote; the quote only says to 'Contact... for removal,' implying a request for service, not a mandatory assignment of the action to those parties.

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

Verifier: `MEANING_CHANGED` — The translation adds 'removal must be done by a Bose retailer or other qualified professional,' which is not stated in the quote; the quote only says to 'Contact... for removal,' implying a request for service, not a mandatory assignment of the action to those parties.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_warning_hinge_pinch_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `hinge_pinch_hazard`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation replaces 'placing the headphones in the case and removing from the case' with 'casing the headphones', which is ambiguous and omits the explicit instruction to handle removal. This drops a critical action (removal) and changes the scope of the directive, altering the meaning.

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

Verifier: `MEANING_CHANGED` — The translation replaces 'placing the headphones in the case and removing from the case' with 'casing the headphones', which is ambiguous and omits the explicit instruction to handle removal. This drops a critical action (removal) and changes the scope of the directive, altering the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_warning_magnetic_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `magnetic_material_medical_devices`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: Translation drops the conditional 'whether this might affect' and replaces it with a direct instruction to 'consult a physician about effects', implying certainty of risk rather than possibility, altering the original cautionary nuance.

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

Verifier: `MEANING_CHANGED` — Translation drops the conditional 'whether this might affect' and replaces it with a direct instruction to 'consult a physician about effects', implying certainty of risk rather than possibility, altering the original cautionary nuance.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_warning_unusual_noise_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `loud_unusual_noise`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation merges the two separate instructions ('turn the headphones off' and 'contact Bose customer service') into a single compound sentence without preserving the conditional sequence: the original requires turning off ONLY if the noise happens, while the translation implies both actions follow the condition simultaneously without clarifying that turning off is the immediate response to the noise event. Also, the original uses 'Do NOT use' as a prohibition, while the translation softens it to 'Do not use', which may imply advisory rather than imperative tone — though minor, this affects compliance urgency in safety context.

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

Verifier: `MEANING_CHANGED` — The translation merges the two separate instructions ('turn the headphones off' and 'contact Bose customer service') into a single compound sentence without preserving the conditional sequence: the original requires turning off ONLY if the noise happens, while the translation implies both actions follow the condition simultaneously without clarifying that turning off is the immediate response to the noise event. Also, the original uses 'Do NOT use' as a prohibition, while the translation softens it to 'Do not use', which may imply advisory rather than imperative tone — though minor, this affects compliance urgency in safety context.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_bqcu2_warning_vehicle_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C3`
- Type / predicate: `WARNING` / `vehicle_operation_use`
- Source authority: `MANUFACTURER_MANUAL`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; HARD REVIEW — C3; individual decision required
- Proposed rationale: Verifier found a meaning change: The translation adds a new instruction: 'stop use immediately if the headphones interfere with attentiveness or hearing alarms and warning signals,' which is not present in the original quote. The original only advises caution and following applicable laws, without specifying an immediate cessation condition.

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

Verifier: `MEANING_CHANGED` — The translation adds a new instruction: 'stop use immediately if the headphones interfere with attentiveness or hearing alarms and warning signals,' which is not present in the original quote. The original only advises caution and following applicable laws, without specifying an immediate cessation condition.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (3)

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

Verifier: `ENTAILED` — The translation accurately preserves the core warning about avoiding high volume to prevent hearing damage, the sequence of actions (turn down before placing, then raise gradually), and the target outcome (comfortable, moderate level). No meaning-altering changes in number, unit, direction, actor, condition, or qualifier are present.

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

Verifier: `ENTAILED` — The translation faithfully preserves the core meaning of the quote: that the product is not intended for use by children. The added 'hazard_type' and 'type' fields are metadata for categorization and do not alter the factual claim. No number, unit, direction, actor, condition, or qualifier is changed or added that affects the original meaning.

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

Verifier: `ENTAILED` — The translation accurately preserves the meaning of the original quote: it conveys that the product contains small parts posing a choking hazard and is not suitable for children under 3. No numbers, units, actors, conditions, or qualifiers are altered or added. The structured format does not change the semantic content.

Extractor notes: None recorded.

## 4. C2 claims (1)

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

Verifier: `ENTAILED` — The translation accurately preserves all key instructions: use only water-dampened cloth, prohibit cleaning products, and prevent moisture entry via ports or earcups. No meaning-altering changes in actor, condition, direction, unit, or qualifier. The added semicolon and 'let' instead of 'allow' are stylistic and do not alter meaning.

Extractor notes: None recorded.

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

## 7. Batch-eligible C0/C1 spot-audit (13)

Batch ID: `batch_bose-qc-ultra-headphones_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `13` members of `batch_bose-qc-ultra-headphones_20260826`.
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

Verifier: `ENTAILED` — The translation accurately captures the exact conditions (noise cancellation On, immersive audio Off), unit (hours), and value (30) from the quote without adding, dropping, or altering any meaning.

Extractor notes: None recorded.

### `claim_bqcu2_battery_life_anc_immersive_on_1` — SPOT-AUDIT SAMPLE

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: 23 hours battery life under the specified conditions (noise cancellation On, immersive audio On), with no added, dropped, or altered meaning.

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: 45 hours with both noise cancellation and immersive audio set to Off, matching the conditions, unit, and value without adding or omitting any qualifiers.

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

Verifier: `ENTAILED` — The translation accurately reflects that the headphones support USB-C audio, with no added, dropped, or altered qualifiers, numbers, units, or conditions.

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: four pre-configured modes are listed, and up to seven custom modes can be created.

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

Verifier: `ENTAILED` — The translation faithfully preserves the exact instruction from the quote without adding, dropping, or altering any detail; the structured format does not change the meaning.

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

Verifier: `ENTAILED` — The translation faithfully preserves the exact instruction from the quote without adding, dropping, or altering any detail such as actor, object, direction, or condition.

Extractor notes: None recorded.

### `claim_bqcu2_step_usbaudio_2` — SPOT-AUDIT SAMPLE

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

Verifier: `ENTAILED` — The translation faithfully preserves the exact wording and meaning of the quote, including all actors, actions, objects, and examples without adding, dropping, or altering any qualifiers, numbers, units, or conditions.

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

Verifier: `ENTAILED` — The translation 'The status light is on the left earcup.' faithfully conveys the meaning of the exact quote 'The status light is located on the left earcup.' — 'located on' and 'on' are semantically equivalent in this context, and no meaning-altering changes (e.g., number, unit, direction, actor, condition, qualifier) are present.

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

Verifier: `ENTAILED` — The translation accurately preserves the number, location, and purpose of the microphones as stated in the exact quote: four microphones on the front, two per earcup, for phone calls. No meaning-altering changes are present.

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

Verifier: `ENTAILED` — The translation accurately reflects the original quote: the status light is solid amber during charging and solid white when fully charged, with no added, dropped, or altered details.

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

Verifier: `ENTAILED` — The translation accurately captures the Bluetooth version as 5.4 without adding, dropping, or altering any qualifiers, numbers, units, or conditions.

Extractor notes: Supersedes claim_bqcu2_bluetooth_version_1 (REJECTED_FOR_SERVING 2026-08-24 — bound only to manifest notes). Bound to the registered curated spec transcription; the raw support-article capture is still pending (gap_spec_article_raw_capture_1).

### `claim_bqcu2_spec_usbc_cable_length_1` — SPOT-AUDIT SAMPLE

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: 'USB-C to USB-C cable (39 in)' is correctly parsed as an included cable with length 39 inches, matching the source without adding, dropping, or altering any meaning.

Extractor notes: Partially closes gap_included_cable_lengths_1; the 3.5 mm-to-2.5 mm aux cable length remains unpublished.
