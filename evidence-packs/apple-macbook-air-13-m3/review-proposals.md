# Review Proposals — apple-macbook-air-13-m3

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `33`
- Existing human decisions: `0`
- Undecided claims covered here: `33`
- Proposed `NEEDS_RECHECK`: `17`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `16`
- Batch-eligible C0/C1: `16`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (17)

### `claim_mba_part_headphone_jack`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `headphone_jack_location`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds the claim that the headphone jack is 'the only port on that side,' which is not stated in the quote and introduces unsupported information.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
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
    "source_id": "src_img_guide_right_side"
  },
  "location_description": "The 3.5 mm headphone jack is on the RIGHT side of the laptop and is the only port on that side.",
  "part": "headphone_jack_3_5mm",
  "side": "RIGHT"
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
1x 3.5 mm headphone jack (the only port on the right side)
```

Verifier: `ENTAILED` — The translation accurately reflects the quote: the 3.5 mm headphone jack is on the right side and is the only port there; no meaning change.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| 3.5 mm headphone jack (high-impedance headphone support) | 1 | Right |
```

Verifier: `MEANING_CHANGED` — The translation adds the claim that the headphone jack is 'the only port on that side,' which is not stated in the quote and introduces unsupported information.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_part_magsafe_port`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `magsafe_3_port_location`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned in the original quote and introduces new spatial information not present in the source. The translation adds specific spatial details (e.g., 'front-most position toward the hinge end', 'next to the two Thunderbolt / USB 4 ports') not present in the quote, which only states 'Left' as the side. This constitutes an unwarranted expansion of meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
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
    "source_id": "src_img_guide_left_side"
  },
  "location_description": "One MagSafe 3 charging port on the LEFT side of the laptop, front-most position toward the hinge end of the left edge, next to the two Thunderbolt / USB 4 ports.",
  "part": "magsafe_3_port",
  "side": "LEFT"
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
1x MagSafe 3 charging port (front-most position toward hinge end of left edge)
```

Verifier: `MEANING_CHANGED` — The translation adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned in the original quote and introduces new spatial information not present in the source.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| MagSafe 3 charging port | 1 | Left |
```

Verifier: `MEANING_CHANGED` — The translation adds specific spatial details (e.g., 'front-most position toward the hinge end', 'next to the two Thunderbolt / USB 4 ports') not present in the quote, which only states 'Left' as the side. This constitutes an unwarranted expansion of meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_part_thunderbolt_ports`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `thunderbolt_ports_location`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'MagSafe 3 port' which is not specified in the quote; the original only says 'MagSafe', so specifying '3' introduces an unverified detail that changes the meaning. The translation adds 'next to the MagSafe 3 port' which is not mentioned in the quote, introducing new spatial information not present in the source.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "count": 2,
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": null,
    "source_id": "src_img_guide_left_side"
  },
  "location_description": "Both Thunderbolt / USB 4 ports are on the LEFT side of the laptop, next to the MagSafe 3 port.",
  "part": "thunderbolt_usb4_ports",
  "side": "LEFT"
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
2x Thunderbolt / USB 4 ports (both on the left side, next to MagSafe)
```

Verifier: `MEANING_CHANGED` — The translation adds 'MagSafe 3 port' which is not specified in the quote; the original only says 'MagSafe', so specifying '3' introduces an unverified detail that changes the meaning.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Thunderbolt / USB 4 (Thunderbolt 3 40Gb/s, USB 4 40Gb/s, DisplayPort, charging) | 2 | Left |
```

Verifier: `MEANING_CHANGED` — The translation adds 'next to the MagSafe 3 port' which is not mentioned in the quote, introducing new spatial information not present in the source.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_part_touch_id`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `touch_id_location`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'the power button' as an appositive to 'Touch ID', implying Touch ID is the power button, while the quote only says 'Touch ID (power button)' — a label or identifier, not a definition. This rephrasing changes the semantic relationship and could mislead the reader into thinking Touch ID and the power button are the same physical component, which the original does not assert.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
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
    "source_id": "src_img_guide_top_open"
  },
  "location_description": "Touch ID (the power button) is at the top-right of the keyboard.",
  "part": "touch_id_power_button",
  "side": null
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
**Touch ID (power button)**: top-right of keyboard
```

Verifier: `MEANING_CHANGED` — The translation adds 'the power button' as an appositive to 'Touch ID', implying Touch ID is the power button, while the quote only says 'Touch ID (power button)' — a label or identifier, not a definition. This rephrasing changes the semantic relationship and could mislead the reader into thinking Touch ID and the power button are the same physical component, which the original does not assert.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_battery_life`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_life`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation omits the critical qualifier 'up to', implying exact battery life values rather than maximum estimates, which alters the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "movie_playback_hours": 18,
  "wireless_web_hours": 15
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Up to 18 hours Apple TV app movie playback; up to 15 hours wireless web
```

Verifier: `MEANING_CHANGED` — The translation omits the critical qualifier 'up to', implying exact battery life values rather than maximum estimates, which alters the meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_box_contents`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `box_contents`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds the word 'config' after GPU and storage specifications, which is not present in the original quote and implies a configurational context not stated.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "values": [
    "13-inch MacBook Air",
    "30W USB-C Power Adapter (8-core GPU config) or 35W Dual USB-C Port Compact Power Adapter (10-core GPU + 512GB config)",
    "USB-C to MagSafe 3 Cable (2 m)"
  ]
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
13-inch MacBook Air; 30W USB-C Power Adapter (8-core GPU) or 35W Dual USB-C Port Compact Power Adapter (10-core GPU + 512GB); USB-C to MagSafe 3 Cable (2 m)
```

Verifier: `MEANING_CHANGED` — The translation adds the word 'config' after GPU and storage specifications, which is not present in the original quote and implies a configurational context not stated.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_camera`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `camera`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation drops the critical detail about the 'advanced image signal processor with computational video', reducing the specification to only the camera resolution and type, thereby omitting key technical capabilities described in the quote.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "value": "1080p FaceTime HD camera"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
1080p FaceTime HD camera; advanced image signal processor with computational video
```

Verifier: `MEANING_CHANGED` — The translation drops the critical detail about the 'advanced image signal processor with computational video', reducing the specification to only the camera resolution and type, thereby omitting key technical capabilities described in the quote.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_fast_charge`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `fast_charge_support`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds '(optional)' to the 70W USB-C Power Adapter, which is not stated in the quote; the quote implies the adapter is required for fast charging, while the translation suggests it is optional. The translation implies the device inherently supports fast charging only if the optional adapter is used, while the quote states that fast charging (up to 50% in ~30 min) is achievable with the optional adapter — not that support depends on it. The quote does not claim the feature is conditional on the adapter; it merely specifies what adapter enables that performance. The translation misrepresents the dependency.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "requires": "70W USB-C Power Adapter (optional)",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
USB-C to MagSafe 3 Cable; fast-charge capable with 70W USB-C Power Adapter
```

Verifier: `MEANING_CHANGED` — The translation adds '(optional)' to the 70W USB-C Power Adapter, which is not stated in the quote; the quote implies the adapter is required for fast charging, while the translation suggests it is optional.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
Fast charge up to 50 percent in around 30 minutes with the optional 70W USB-C Power Adapter.
```

Verifier: `MEANING_CHANGED` — The translation implies the device inherently supports fast charging only if the optional adapter is used, while the quote states that fast charging (up to 50% in ~30 min) is achievable with the optional adapter — not that support depends on it. The quote does not claim the feature is conditional on the adapter; it merely specifies what adapter enables that performance. The translation misrepresents the dependency.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_headphone_jack_impedance`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `headphone_jack_high_impedance_support`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds '3.5 mm headphone jack' and 'advanced support', which are not mentioned in the quote; the quote only states support for high-impedance headphones without specifying jack type or level of support.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "description": "3.5 mm headphone jack with advanced support for high-impedance headphones",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
3.5 mm headphone jack with advanced support for high-impedance headphones
```

Verifier: `ENTAILED` — The translation faithfully preserves the exact wording and meaning of the quote, including the specification of '3.5 mm headphone jack with advanced support for high-impedance headphones' without adding, dropping, or altering any detail.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
supports high-impedance headphones without a separate DAC or amplifier
```

Verifier: `MEANING_CHANGED` — The translation adds '3.5 mm headphone jack' and 'advanced support', which are not mentioned in the quote; the quote only states support for high-impedance headphones without specifying jack type or level of support.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_memory_options`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `memory_options`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED; Extractor flagged applicability or interpretation context
- Proposed rationale: Verifier found a meaning change: Translation omits that the 8GB base config is configurable to 16GB or 24GB, and incorrectly implies 16GB is the base with only 24GB as configurable option, altering configuration scope.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "also_listed_base_gb": 8,
  "base_gb": 16,
  "configurable_gb": [
    24
  ]
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
16GB unified memory (configurable to 24GB); 8GB base configuration also listed (configurable to 16GB or 24GB)
```

Verifier: `MEANING_CHANGED` — Translation omits that the 8GB base config is configurable to 16GB or 24GB, and incorrectly implies 16GB is the base with only 24GB as configurable option, altering configuration scope.

Extractor notes: Capture notes that the tech specs page's 16GB base reflects Apple's 2025 update; the March 2024 launch base configuration was 8GB. Reviewer should decide whether applicability.revision should split this claim.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_microphone_array`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `microphone_array`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation incorrectly implies that 'directional beamforming', 'Voice Isolation', and 'Wide Spectrum' are features of the 'three-mic array' as separate attributes, whereas the quote presents them as modes or capabilities associated with the array — not distinct features owned by it. This misattributes structure and relationship, altering meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "features": [
    "directional beamforming",
    "Voice Isolation",
    "Wide Spectrum"
  ],
  "value": "three-mic array"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Three-mic array with directional beamforming; Voice Isolation and Wide Spectrum mic modes
```

Verifier: `MEANING_CHANGED` — The translation incorrectly implies that 'directional beamforming', 'Voice Isolation', and 'Wide Spectrum' are features of the 'three-mic array' as separate attributes, whereas the quote presents them as modes or capabilities associated with the array — not distinct features owned by it. This misattributes structure and relationship, altering meaning.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_newest_compatible_os`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `newest_compatible_os`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds a specific date '2026-08-20' not present in the quote, which changes the meaning by implying a precise retrieval timestamp not stated in the original.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "as_of": "2026-08-20",
  "value": "macOS Tahoe 26"
}
```

Quote — binding 0, source `src_identify_page`, page `None`

```text
**Newest compatible operating system** (as of retrieval): macOS Tahoe 26
```

Verifier: `MEANING_CHANGED` — The translation adds a specific date '2026-08-20' not present in the quote, which changes the meaning by implying a precise retrieval timestamp not stated in the original.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_spatial_audio`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `spatial_audio_support`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'support' as a predicate and implies a boolean value 'true', which is not stated in the quote; the quote merely describes a feature context without asserting support or functionality.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "condition": "when playing music or video with Dolby Atmos on built-in speakers",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Spatial Audio when playing music/video with Dolby Atmos on built-in speakers
```

Verifier: `MEANING_CHANGED` — The translation adds 'support' as a predicate and implies a boolean value 'true', which is not stated in the quote; the quote merely describes a feature context without asserting support or functionality.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_speaker_system`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `speaker_system`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds specific speaker composition ('two tweeters, two woofers') not mentioned in the quote, which only states 'four-speaker sound system' without specifying types or configuration.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "detail": "two tweeters, two woofers",
  "value": "four-speaker sound system"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Four-speaker sound system
```

Verifier: `MEANING_CHANGED` — The translation adds specific speaker composition ('two tweeters, two woofers') not mentioned in the quote, which only states 'four-speaker sound system' without specifying types or configuration.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
the 13-inch MacBook Air has a four-speaker sound system (two tweeters, two woofers)
```

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: it specifies the four-speaker system and breaks it down into two tweeters and two woofers, matching the source without adding, dropping, or altering any detail.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_wifi_standard`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `wifi_standard`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation reverses the relationship: it treats 'Wi-Fi 6E' as the value and '802.11ax' as the standard, implying Wi-Fi 6E is a value of the standard — but the quote presents them as synonymous identifiers, not a value-standard pair. The translation reverses the relationship: it presents 'Wi-Fi 6E' as the value and '802.11ax' as the standard, implying Wi-Fi 6E is an instance or value of 802.11ax — but the quote treats them as synonymous labels for the same thing, not a value-standard pair.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "standard": "802.11ax",
  "value": "Wi-Fi 6E"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Wi-Fi 6E (802.11ax)
```

Verifier: `MEANING_CHANGED` — The translation reverses the relationship: it treats 'Wi-Fi 6E' as the value and '802.11ax' as the standard, implying Wi-Fi 6E is a value of the standard — but the quote presents them as synonymous identifiers, not a value-standard pair.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Wi-Fi 6E (802.11ax)
```

Verifier: `MEANING_CHANGED` — The translation reverses the relationship: it presents 'Wi-Fi 6E' as the value and '802.11ax' as the standard, implying Wi-Fi 6E is an instance or value of 802.11ax — but the quote treats them as synonymous labels for the same thing, not a value-standard pair.

Extractor notes: None recorded.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_step_charge_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'into the MagSafe 3 port', which is not mentioned in the original quote. The original only says 'Plug in the included USB-C Power Adapter' without specifying any port, so this addition changes the meaning by introducing an unsupported detail.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "action": "Plug the included USB-C Power Adapter into the MagSafe 3 port; the indicator light glows amber while charging is needed and green when fully charged.",
  "procedure": "charge_via_magsafe",
  "step_number": 1,
  "target_parts": [
    "magsafe_3_port",
    "usb_c_power_adapter"
  ]
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
Plug in the included USB-C Power Adapter. Indicator light glows amber when charging is needed, green when fully charged.
```

Verifier: `MEANING_CHANGED` — The translation adds 'into the MagSafe 3 port', which is not mentioned in the original quote. The original only says 'Plug in the included USB-C Power Adapter' without specifying any port, so this addition changes the meaning by introducing an unsupported detail.

Extractor notes: Single-step procedure: the guide states charging as one action.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

### `claim_mba_step_power_on_1`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The translation adds 'Touch ID (power button)' and 'laptop', which are not mentioned in the quote. The quote only says 'top-right of keyboard' without specifying the button type or device type, so adding these details changes the meaning.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "action": "Press the Touch ID (power button) at the top-right of the keyboard to turn the laptop on.",
  "procedure": "power_on",
  "step_number": 1,
  "target_parts": [
    "touch_id_power_button"
  ]
}
```

Quote — binding 0, source `src_ports_guide_tour`, page `None`

```text
top-right of keyboard; press to turn on; authenticate and Apple Pay after setup
```

Verifier: `MEANING_CHANGED` — The translation adds 'Touch ID (power button)' and 'laptop', which are not mentioned in the quote. The quote only says 'top-right of keyboard' without specifying the button type or device type, so adding these details changes the meaning.

Extractor notes: Single-step procedure: the guide states power-on as one action.

Rework path: Rewrite the procedure step to contain only details supported by its cited span, or add an authoritative binding that supports the full action; then re-run verification so the procedure can become servable for video generation.

## 2. Unresolved conflict claims (0 claims / 0 pairs)

None outside section 1 or existing human decisions.

## 3. C3 claims (0)

None.

## 4. C2 claims (0)

None.

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (1)

### `gap_bt_pairing_1`

- Kind: `SOURCE_MISSING`
- Waives: `["checklist:bt_pairing_steps"]`
- Reason: The Bluetooth pairing guide source (src_bluetooth_pairing_guide, 'Connect Bluetooth devices to your Mac', support.apple.com/guide/mac-help/blth1004/mac) has local_path null — no local capture exists. No other vault capture contains the pairing steps: ports-guide.md and videos/video-sources.md record only the guide URL, and essentials-guide-note.md is an availability note. video-sources.md also confirms Apple published no official pairing video. Writing STEP claims against a URL-only source would be unverifiable; recorded as a gap instead.
- Closes when: A verbatim capture of https://support.apple.com/guide/mac-help/blth1004/mac (or the MacBook Air guide 'Connect accessories' page) is added to source-vault/apple-macbook-air-13-m3/manuals/ and registered in manifest.json with a local_path.

## 7. Batch-eligible C0/C1 spot-audit (16)

Batch ID: `batch_apple-macbook-air-13-m3_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `16` members of `batch_apple-macbook-air-13-m3_20260826`.
- [ ] SAMPLE FAILED: do not batch-confirm; decide every member below individually.
- Owner / date: ______________________________

### `claim_mba_spec_height`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `height_closed`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 1.13,
  "unit": "in",
  "value": 0.44
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Height: 0.44 inch (1.13 cm)
```

Verifier: `ENTAILED` — The translation faithfully preserves the height values in both inches (0.44) and centimeters (1.13) with correct units and no added, dropped, or altered qualifiers.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Height (closed) | 0.44 in (1.13 cm) |
```

Verifier: `ENTAILED` — The translation faithfully preserves the exact values and units from the quote: 0.44 in and 1.13 cm for height (closed), with no added, dropped, or altered qualifiers.

Extractor notes: None recorded.

### `claim_mba_spec_width`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `width`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 30.41,
  "unit": "in",
  "value": 11.97
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Width: 11.97 inches (30.41 cm)
```

Verifier: `ENTAILED` — The translation accurately preserves the width values and units from the quote: 11.97 inches and 30.41 cm, with correct unit labels and no added or dropped qualifiers.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Width | 11.97 in (30.41 cm) |
```

Verifier: `ENTAILED` — The translation accurately preserves the width values and units (11.97 in and 30.41 cm) without adding, dropping, or altering any qualifiers, numbers, or units from the source.

Extractor notes: None recorded.

### `claim_mba_spec_depth`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `depth`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 21.5,
  "unit": "in",
  "value": 8.46
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Depth: 8.46 inches (21.5 cm)
```

Verifier: `ENTAILED` — The translation accurately preserves the depth value in both inches (8.46) and centimeters (21.5) as stated in the quote, with no added, dropped, or altered qualifiers, units, or values.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Depth | 8.46 in (21.5 cm) |
```

Verifier: `ENTAILED` — The translation faithfully preserves the depth value in both inches (8.46) and centimeters (21.5) as stated in the quote, with no added, dropped, or altered qualifiers, units, or values.

Extractor notes: None recorded.

### `claim_mba_spec_weight`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `product_weight`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "metric_unit": "kg",
  "metric_value": 1.24,
  "note": "varies by configuration",
  "unit": "lb",
  "value": 2.7
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Weight: 2.7 pounds (1.24 kg) (varies by configuration)
```

Verifier: `ENTAILED` — The translation faithfully preserves all elements: the weight values in both lb and kg, the note about variation by configuration, and the predicate 'product_weight'. No meaning is altered or added.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Weight | 2.7 lb (1.24 kg), varies by configuration |
```

Verifier: `ENTAILED` — The translation accurately preserves all elements: both imperial and metric values (2.7 lb, 1.24 kg), the note 'varies by configuration', and the predicate 'product_weight'. No meaning is added, dropped, or altered.

Extractor notes: None recorded.

### `claim_mba_spec_bluetooth_version` — SPOT-AUDIT SAMPLE

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
  "sku": null,
  "state": null
}
```

Object

```json
{
  "standard": "Bluetooth",
  "value": "5.3"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Bluetooth 5.3
```

Verifier: `ENTAILED` — The translation accurately reflects the exact quote 'Bluetooth 5.3' by encoding it as a specification with standard 'Bluetooth' and value '5.3', without adding, dropping, or altering any meaning.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Bluetooth 5.3
```

Verifier: `ENTAILED` — The translation accurately reflects the exact quote 'Bluetooth 5.3' by structuring it as a specification with standard 'Bluetooth' and value '5.3', preserving the meaning without adding or omitting any information.

Extractor notes: None recorded.

### `claim_mba_spec_colors` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `available_colors`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "values": [
    "Silver",
    "Starlight",
    "Space Gray",
    "Midnight"
  ]
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Silver, Starlight, Space Gray, Midnight
```

Verifier: `ENTAILED` — The translation accurately lists the exact color names from the quote as available colors without adding, dropping, or altering any meaning.

Quote — binding 1, source `src_identify_page`, page `None`

```text
**Colors**: Silver, Starlight, Space Gray, Midnight
```

Verifier: `ENTAILED` — The translation accurately reflects the exact colors listed in the quote without adding, dropping, or altering any details.

Extractor notes: None recorded.

### `claim_mba_spec_model_identifier` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `model_identifier`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "value": "Mac15,12"
}
```

Quote — binding 0, source `src_identify_page`, page `None`

```text
**Model Identifier**: `Mac15,12`
```

Verifier: `ENTAILED` — The translation accurately preserves the exact model identifier 'Mac15,12' and correctly labels it as a 'model_identifier' under 'SPEC' type, with no added, dropped, or altered information.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Model identifier: **Mac15,12**
```

Verifier: `ENTAILED` — The translation accurately preserves the model identifier 'Mac15,12' as the object value with the predicate 'model_identifier', matching the exact quote without adding, dropping, or altering any detail.

Extractor notes: None recorded.

### `claim_mba_spec_audio_playback_formats` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `audio_playback_formats`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "values": [
    "AAC",
    "MP3",
    "Apple Lossless",
    "FLAC",
    "Dolby Digital",
    "Dolby Digital Plus",
    "Dolby Atmos"
  ]
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
AAC, MP3, Apple Lossless, FLAC, Dolby Digital, Dolby Digital Plus, Dolby Atmos
```

Verifier: `ENTAILED` — The translation accurately lists the exact same audio formats as the quote without adding, dropping, or altering any values, qualifiers, or conditions.

Extractor notes: None recorded.

### `claim_mba_spec_display_type`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `display_type`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "backlight": "LED",
  "diagonal_in": 13.6,
  "panel": "IPS",
  "value": "Liquid Retina display"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Liquid Retina display, 13.6-inch diagonal, LED-backlit with IPS technology
```

Verifier: `ENTAILED` — The translation accurately captures all elements from the quote: 'Liquid Retina display' as the display type, '13.6-inch diagonal' as diagonal_in, 'LED-backlit' as backlight, and 'IPS technology' as panel. No meaning is added, dropped, or altered.

Extractor notes: None recorded.

### `claim_mba_spec_display_resolution`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `display_resolution`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "height_px": 1664,
  "ppi": 224,
  "width_px": 2560
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
2560-by-1664 native resolution at 224 ppi
```

Verifier: `ENTAILED` — The translation accurately preserves the exact pixel dimensions (2560x1664) and ppi (224) from the quote without adding, dropping, or altering any qualifiers or values.

Extractor notes: None recorded.

### `claim_mba_spec_battery_capacity` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_capacity`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "chemistry": "lithium-polymer",
  "unit": "Wh",
  "value": 52.6
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
52.6-watt-hour lithium-polymer battery
```

Verifier: `ENTAILED` — The translation accurately preserves the chemistry (lithium-polymer), unit (Wh), and value (52.6) from the quote, and correctly labels it as battery capacity under SPEC type without adding or omitting any meaning.

Extractor notes: None recorded.

### `claim_mba_spec_cpu`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `cpu_configuration`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "chip": "Apple M3",
  "cpu_cores": 8,
  "efficiency_cores": 4,
  "performance_cores": 4
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
8-core CPU (4 performance + 4 efficiency cores)
```

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: 8 total cores, split into 4 performance and 4 efficiency cores, with no added, dropped, or altered details.

Extractor notes: None recorded.

### `claim_mba_spec_thunderbolt_capabilities`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `thunderbolt_port_capabilities`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "capabilities": [
    "charging",
    "DisplayPort",
    "Thunderbolt 3 (up to 40Gb/s)",
    "USB 4 (up to 40Gb/s)"
  ],
  "count": 2
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Two Thunderbolt / USB 4 ports supporting: charging, DisplayPort, Thunderbolt 3 (up to 40Gb/s), USB 4 (up to 40Gb/s)
```

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: two ports with identical listed capabilities, including charging, DisplayPort, Thunderbolt 3 (up to 40Gb/s), and USB 4 (up to 40Gb/s), without adding or omitting any qualifiers or details.

Extractor notes: None recorded.

### `claim_mba_spec_storage_options`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `storage_options`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "base": "256GB SSD",
  "configurable": [
    "512GB",
    "1TB",
    "2TB"
  ]
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
256GB SSD; configurable to 512GB, 1TB, or 2TB
```

Verifier: `ENTAILED` — The translation accurately preserves the base storage (256GB SSD) and the configurable options (512GB, 1TB, 2TB) without adding, dropping, or altering any meaning.

Extractor notes: None recorded.

### `claim_mba_spec_operating_temperature`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `operating_temperature_range`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "max_c": 35,
  "max_f": 95,
  "min_c": 10,
  "min_f": 50
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Operating temperature: 50° to 95° F (10° to 35° C)
```

Verifier: `ENTAILED` — The translation accurately preserves the operating temperature range in both Fahrenheit and Celsius, with no added, dropped, or altered values or qualifiers.

Extractor notes: None recorded.

### `claim_mba_spec_launch_price`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `launch_price_us`
- Source authority: `MANUFACTURER_SPEC_PAGE`
- Queue section: `batch_eligible`
- Review focus: Standard review
- Proposed rationale: Every source binding is ENTAILED by the pinned verifier and no unresolved conflict applies; publication still requires owner confirmation.

Applicability

```json
{
  "market": "US",
  "revision": null,
  "sku": null,
  "state": null
}
```

Object

```json
{
  "availability_date": "2024-03-08",
  "orders_date": "2024-03-04",
  "unit": "USD",
  "value": 1099
}
```

Quote — binding 0, source `src_specs_summary`, page `None`

```text
Introduced: March 4, 2024 (orders), available March 8, 2024; launch price $1,099 US
```

Verifier: `ENTAILED` — The translation accurately reflects the quote: orders began March 4, 2024; availability started March 8, 2024; launch price is $1,099 USD. No meaning change.

Extractor notes: Curated spec summary cites the Newsroom launch article (src_newsroom_article, no local capture) as its origin for this fact; bound to the local summary only.
