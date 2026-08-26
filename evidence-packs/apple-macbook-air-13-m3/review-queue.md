# Review Queue — apple-macbook-air-13-m3

Verification status: `COMPLETE`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.
A v2 alarm reopens `0` existing human disposition(s); those decisions must be explicitly reconfirmed or amended.

## 1. MEANING_CHANGED alarms (5)

### claim_mba_part_magsafe_port

- Claim: `claim_mba_part_magsafe_port`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `magsafe_3_port_location`

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

Quote — binding 0, source `src_ports_guide_tour`

```text
1x MagSafe 3 charging port (front-most position toward hinge end of left edge)
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source.

Quote — binding 1, source `src_specs_summary`

```text
| MagSafe 3 charging port | 1 | Left |
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source.

Extractor notes: None recorded.

### claim_mba_spec_fast_charge

- Claim: `claim_mba_spec_fast_charge`
- Tier: `C0`
- Type/predicate: `SPEC` / `fast_charge_support`

Object

```json
{
  "requires": "70W USB-C Power Adapter (optional)",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
USB-C to MagSafe 3 Cable; fast-charge capable with 70W USB-C Power Adapter
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists.

Quote — binding 1, source `src_ports_guide_tour`

```text
Fast charge up to 50 percent in around 30 minutes with the optional 70W USB-C Power Adapter.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists.

Extractor notes: None recorded.

### claim_mba_spec_memory_options

- Claim: `claim_mba_spec_memory_options`
- Tier: `C0`
- Type/predicate: `SPEC` / `memory_options`

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

Quote — binding 0, source `src_tech_specs_page`

```text
16GB unified memory (configurable to 24GB); 8GB base configuration also listed (configurable to 16GB or 24GB)
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts 'base_gb':16, but the quote states 16GB is the default configuration while explicitly listing 8GB as the base configuration (which is configurable to 16GB or 24GB), making 16GB not the base but an upgrade option; thus, assigning 16 as the base misrepresents the hierarchy and conditions.

Extractor notes: Capture notes that the tech specs page's 16GB base reflects Apple's 2025 update; the March 2024 launch base configuration was 8GB. Reviewer should decide whether applicability.revision should split this claim.

### claim_mba_spec_newest_compatible_os

- Claim: `claim_mba_spec_newest_compatible_os`
- Tier: `C0`
- Type/predicate: `SPEC` / `newest_compatible_os`

Object

```json
{
  "as_of": "2026-08-20",
  "value": "macOS Tahoe 26"
}
```

Quote — binding 0, source `src_identify_page`

```text
**Newest compatible operating system** (as of retrieval): macOS Tahoe 26
```

Verifier (claim quote union): `MEANING_CHANGED` — The quote specifies 'as of retrieval' without a date, while the projection asserts a specific date '2026-08-20', which is an unsupported addition not present in the source.

Extractor notes: None recorded.

### claim_mba_step_charge_1

- Claim: `claim_mba_step_charge_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Quote — binding 0, source `src_ports_guide_tour`

```text
Plug in the included USB-C Power Adapter. Indicator light glows amber when charging is needed, green when fully charged.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'into the MagSafe 3 port', which is not mentioned in the quote. The quote only says 'Plug in the included USB-C Power Adapter' without specifying any port, let alone the MagSafe 3 port. This is an unsupported semantic addition that narrows the scope of the action incorrectly.

Extractor notes: Single-step procedure: the guide states charging as one action.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (0)

None.

## 4. C2 claims (0)

None.

## 5. Unresolved verifier — C0/C1 (0)

None.

## 6. Open gaps (1)

### gap_bt_pairing_1

- Kind: `SOURCE_MISSING`
- Waives: `["checklist:bt_pairing_steps"]`

Reason: The Bluetooth pairing guide source (src_bluetooth_pairing_guide, 'Connect Bluetooth devices to your Mac', support.apple.com/guide/mac-help/blth1004/mac) has local_path null — no local capture exists. No other vault capture contains the pairing steps: ports-guide.md and videos/video-sources.md record only the guide URL, and essentials-guide-note.md is an availability note. video-sources.md also confirms Apple published no official pairing video. Writing STEP claims against a URL-only source would be unverifiable; recorded as a gap instead.

Closes when: A verbatim capture of https://support.apple.com/guide/mac-help/blth1004/mac (or the MacBook Air guide 'Connect accessories' page) is added to source-vault/apple-macbook-air-13-m3/manuals/ and registered in manifest.json with a local_path.

## 7. Batch-eligible C0/C1 spot-audit (28)

Spot-audit sample: `5` of `28` eligible claims. The sample is the five lowest SHA-256 ranks of `review-completion-v1\0<product>\0<claim_id>`, so it is stable and reproducible.

A clean sample may be confirmed as one explicit human batch decision. A failed sample removes batch eligibility; review every batch member individually.

Batch members

- `claim_mba_spec_height`
- `claim_mba_spec_width`
- `claim_mba_spec_depth`
- `claim_mba_spec_weight`
- `claim_mba_spec_bluetooth_version`
- `claim_mba_spec_wifi_standard`
- `claim_mba_spec_colors`
- `claim_mba_spec_model_identifier`
- `claim_mba_spec_speaker_system`
- `claim_mba_spec_audio_playback_formats`
- `claim_mba_spec_headphone_jack_impedance`
- `claim_mba_spec_microphone_array`
- `claim_mba_spec_spatial_audio`
- `claim_mba_spec_display_type`
- `claim_mba_spec_display_resolution`
- `claim_mba_spec_battery_capacity`
- `claim_mba_spec_battery_life`
- `claim_mba_spec_cpu`
- `claim_mba_spec_camera`
- `claim_mba_spec_thunderbolt_capabilities`
- `claim_mba_spec_storage_options`
- `claim_mba_spec_box_contents`
- `claim_mba_spec_operating_temperature`
- `claim_mba_spec_launch_price`
- `claim_mba_part_thunderbolt_ports`
- `claim_mba_part_headphone_jack`
- `claim_mba_part_touch_id`
- `claim_mba_step_power_on_1`

Sample details

### claim_mba_spec_model_identifier

- Claim: `claim_mba_spec_model_identifier`
- Tier: `C0`
- Type/predicate: `SPEC` / `model_identifier`

Object

```json
{
  "value": "Mac15,12"
}
```

Quote — binding 0, source `src_identify_page`

```text
**Model Identifier**: `Mac15,12`
```

Verifier (claim quote union): `ENTAILED` — Both quotes explicitly state the model identifier as 'Mac15,12', and the projection faithfully extracts this exact value without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`

```text
Model identifier: **Mac15,12**
```

Verifier (claim quote union): `ENTAILED` — Both quotes explicitly state the model identifier as 'Mac15,12', and the projection faithfully extracts this exact value without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: None recorded.

### claim_mba_spec_audio_playback_formats

- Claim: `claim_mba_spec_audio_playback_formats`
- Tier: `C0`
- Type/predicate: `SPEC` / `audio_playback_formats`

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

Quote — binding 0, source `src_tech_specs_page`

```text
AAC, MP3, Apple Lossless, FLAC, Dolby Digital, Dolby Digital Plus, Dolby Atmos
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the audio formats quoted, with no added conditions, directions, or semantic expansions; the union of quotes fully supports the asserted values.

Extractor notes: None recorded.

### claim_mba_spec_bluetooth_version

- Claim: `claim_mba_spec_bluetooth_version`
- Tier: `C0`
- Type/predicate: `SPEC` / `bluetooth_version`

Object

```json
{
  "standard": "Bluetooth",
  "value": "5.3"
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Bluetooth 5.3
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Bluetooth 5.3' twice, which fully supports the projection's assertion of standard 'Bluetooth' and value '5.3' without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`

```text
Bluetooth 5.3
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Bluetooth 5.3' twice, which fully supports the projection's assertion of standard 'Bluetooth' and value '5.3' without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: None recorded.

### claim_mba_spec_speaker_system

- Claim: `claim_mba_spec_speaker_system`
- Tier: `C0`
- Type/predicate: `SPEC` / `speaker_system`

Object

```json
{
  "detail": "two tweeters, two woofers",
  "value": "four-speaker sound system"
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Four-speaker sound system
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports both assertions: 'four-speaker sound system' is directly stated in both, and 'two tweeters, two woofers' is explicitly provided in the second quote as the composition of that system. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Quote — binding 1, source `src_ports_guide_tour`

```text
the 13-inch MacBook Air has a four-speaker sound system (two tweeters, two woofers)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports both assertions: 'four-speaker sound system' is directly stated in both, and 'two tweeters, two woofers' is explicitly provided in the second quote as the composition of that system. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### claim_mba_spec_colors

- Claim: `claim_mba_spec_colors`
- Tier: `C0`
- Type/predicate: `SPEC` / `available_colors`

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

Quote — binding 0, source `src_tech_specs_page`

```text
Silver, Starlight, Space Gray, Midnight
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the four colors stated in both quotes, with no added conditions, directions, or qualifiers; the union of quotes fully supports the semantic content of the projection.

Quote — binding 1, source `src_identify_page`

```text
**Colors**: Silver, Starlight, Space Gray, Midnight
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the four colors stated in both quotes, with no added conditions, directions, or qualifiers; the union of quotes fully supports the semantic content of the projection.

Extractor notes: None recorded.
