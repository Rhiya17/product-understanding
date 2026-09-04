# Review Queue — apple-macbook-air-13-m3

Verification status: `PARTIAL`

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

## 5. Unresolved verifier — C0/C1 (34)

### claim_mba_spec_height

- Claim: `claim_mba_spec_height`
- Tier: `C0`
- Type/predicate: `SPEC` / `height_closed`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 1.13,
  "unit": "in",
  "value": 0.44
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Height: 0.44 inch (1.13 cm)
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the height values and units from both quotes: 0.44 inch and 1.13 cm, with no added conditions, directions, or unsupported semantic expansions.

Quote — binding 1, source `src_specs_summary`

```text
| Height (closed) | 0.44 in (1.13 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the height values and units from both quotes: 0.44 inch and 1.13 cm, with no added conditions, directions, or unsupported semantic expansions.

Extractor notes: None recorded.

### claim_mba_spec_width

- Claim: `claim_mba_spec_width`
- Tier: `C0`
- Type/predicate: `SPEC` / `width`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 30.41,
  "unit": "in",
  "value": 11.97
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Width: 11.97 inches (30.41 cm)
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in both quotes without adding, omitting, or altering any conditions, directions, or qualifiers.

Quote — binding 1, source `src_specs_summary`

```text
| Width | 11.97 in (30.41 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in both quotes without adding, omitting, or altering any conditions, directions, or qualifiers.

Extractor notes: None recorded.

### claim_mba_spec_depth

- Claim: `claim_mba_spec_depth`
- Tier: `C0`
- Type/predicate: `SPEC` / `depth`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric_unit": "cm",
  "metric_value": 21.5,
  "unit": "in",
  "value": 8.46
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Depth: 8.46 inches (21.5 cm)
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in the quotes: 8.46 inches and 21.5 cm, with no added conditions, directions, or unsupported semantic expansions.

Quote — binding 1, source `src_specs_summary`

```text
| Depth | 8.46 in (21.5 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in the quotes: 8.46 inches and 21.5 cm, with no added conditions, directions, or unsupported semantic expansions.

Extractor notes: None recorded.

### claim_mba_spec_weight

- Claim: `claim_mba_spec_weight`
- Tier: `C0`
- Type/predicate: `SPEC` / `product_weight`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_tech_specs_page`

```text
Weight: 2.7 pounds (1.24 kg) (varies by configuration)
```

Verifier (claim quote union): `ENTAILED` — Every semantic assertion in the projection is directly supported by the union of quotes: both quotes state the weight as 2.7 lb and 1.24 kg, and both include the note 'varies by configuration'. The projection faithfully extracts these values and qualifiers without adding, broadening, or omitting any governing condition.

Quote — binding 1, source `src_specs_summary`

```text
| Weight | 2.7 lb (1.24 kg), varies by configuration |
```

Verifier (claim quote union): `ENTAILED` — Every semantic assertion in the projection is directly supported by the union of quotes: both quotes state the weight as 2.7 lb and 1.24 kg, and both include the note 'varies by configuration'. The projection faithfully extracts these values and qualifiers without adding, broadening, or omitting any governing condition.

Extractor notes: None recorded.

### claim_mba_spec_bluetooth_version

- Claim: `claim_mba_spec_bluetooth_version`
- Tier: `C0`
- Type/predicate: `SPEC` / `bluetooth_version`
- Verifier state: document status is PARTIAL

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

### claim_mba_spec_wifi_standard

- Claim: `claim_mba_spec_wifi_standard`
- Tier: `C0`
- Type/predicate: `SPEC` / `wifi_standard`
- Verifier state: document status is PARTIAL

Object

```json
{
  "standard": "802.11ax",
  "value": "Wi-Fi 6E"
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Wi-Fi 6E (802.11ax)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Wi-Fi 6E (802.11ax)', which directly supports both the standard '802.11ax' and the value 'Wi-Fi 6E' in the projection without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`

```text
Wi-Fi 6E (802.11ax)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Wi-Fi 6E (802.11ax)', which directly supports both the standard '802.11ax' and the value 'Wi-Fi 6E' in the projection without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: None recorded.

### claim_mba_spec_colors

- Claim: `claim_mba_spec_colors`
- Tier: `C0`
- Type/predicate: `SPEC` / `available_colors`
- Verifier state: document status is PARTIAL

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

### claim_mba_spec_model_identifier

- Claim: `claim_mba_spec_model_identifier`
- Tier: `C0`
- Type/predicate: `SPEC` / `model_identifier`
- Verifier state: document status is PARTIAL

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

### claim_mba_spec_speaker_system

- Claim: `claim_mba_spec_speaker_system`
- Tier: `C0`
- Type/predicate: `SPEC` / `speaker_system`
- Verifier state: document status is PARTIAL

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

### claim_mba_spec_audio_playback_formats

- Claim: `claim_mba_spec_audio_playback_formats`
- Tier: `C0`
- Type/predicate: `SPEC` / `audio_playback_formats`
- Verifier state: document status is PARTIAL

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

### claim_mba_spec_headphone_jack_impedance

- Claim: `claim_mba_spec_headphone_jack_impedance`
- Tier: `C0`
- Type/predicate: `SPEC` / `headphone_jack_high_impedance_support`
- Verifier state: document status is PARTIAL

Object

```json
{
  "description": "3.5 mm headphone jack with advanced support for high-impedance headphones",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
3.5 mm headphone jack with advanced support for high-impedance headphones
```

Verifier (claim quote union): `ENTAILED` — The projection's description exactly matches the first quote, and the value 'true' is semantically supported by both quotes asserting the feature exists and functions without additional hardware — no unsupported addition, contradiction, or lost condition.

Quote — binding 1, source `src_ports_guide_tour`

```text
supports high-impedance headphones without a separate DAC or amplifier
```

Verifier (claim quote union): `ENTAILED` — The projection's description exactly matches the first quote, and the value 'true' is semantically supported by both quotes asserting the feature exists and functions without additional hardware — no unsupported addition, contradiction, or lost condition.

Extractor notes: None recorded.

### claim_mba_spec_microphone_array

- Claim: `claim_mba_spec_microphone_array`
- Tier: `C0`
- Type/predicate: `SPEC` / `microphone_array`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_tech_specs_page`

```text
Three-mic array with directional beamforming; Voice Isolation and Wide Spectrum mic modes
```

Verifier (claim quote union): `ENTAILED` — The projection accurately extracts 'directional beamforming', 'Voice Isolation', and 'Wide Spectrum' as features from the quote, and correctly assigns 'three-mic array' as the value. All assertions are directly supported by the single quote without adding, omitting, or misrepresenting conditions, directions, or scope.

Extractor notes: None recorded.

### claim_mba_spec_spatial_audio

- Claim: `claim_mba_spec_spatial_audio`
- Tier: `C0`
- Type/predicate: `SPEC` / `spatial_audio_support`
- Verifier state: document status is PARTIAL

Object

```json
{
  "condition": "when playing music or video with Dolby Atmos on built-in speakers",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Spatial Audio when playing music/video with Dolby Atmos on built-in speakers
```

Verifier (claim quote union): `ENTAILED` — The projection's condition exactly matches the quote's context, and the value 'true' is a faithful semantic assertion of the feature being enabled under that condition; no unsupported addition or contradiction exists.

Extractor notes: None recorded.

### claim_mba_spec_display_type

- Claim: `claim_mba_spec_display_type`
- Tier: `C0`
- Type/predicate: `SPEC` / `display_type`
- Verifier state: document status is PARTIAL

Object

```json
{
  "backlight": "LED",
  "diagonal_in": 13.6,
  "panel": "IPS",
  "value": "Liquid Retina display"
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Liquid Retina display, 13.6-inch diagonal, LED-backlit with IPS technology
```

Verifier (claim quote union): `ENTAILED` — Every assertion in the projection — LED backlight, 13.6-inch diagonal, IPS panel, and Liquid Retina display — is directly and unambiguously stated in the quote; no condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Extractor notes: None recorded.

### claim_mba_spec_display_resolution

- Claim: `claim_mba_spec_display_resolution`
- Tier: `C0`
- Type/predicate: `SPEC` / `display_resolution`
- Verifier state: document status is PARTIAL

Object

```json
{
  "height_px": 1664,
  "ppi": 224,
  "width_px": 2560
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
2560-by-1664 native resolution at 224 ppi
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '2560-by-1664 native resolution at 224 ppi', which directly supports the width_px (2560), height_px (1664), and ppi (224) values in the projection without adding, omitting, or altering any conditions or directions.

Extractor notes: None recorded.

### claim_mba_spec_battery_capacity

- Claim: `claim_mba_spec_battery_capacity`
- Tier: `C0`
- Type/predicate: `SPEC` / `battery_capacity`
- Verifier state: document status is PARTIAL

Object

```json
{
  "chemistry": "lithium-polymer",
  "unit": "Wh",
  "value": 52.6
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
52.6-watt-hour lithium-polymer battery
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '52.6-watt-hour lithium-polymer battery', which directly supports the chemistry, unit, and value in the projection without adding or omitting any governing conditions or semantic qualifiers.

Extractor notes: None recorded.

### claim_mba_spec_battery_life

- Claim: `claim_mba_spec_battery_life`
- Tier: `C0`
- Type/predicate: `SPEC` / `battery_life`
- Verifier state: document status is PARTIAL

Object

```json
{
  "movie_playback_hours": 18,
  "wireless_web_hours": 15
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Up to 18 hours Apple TV app movie playback; up to 15 hours wireless web
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the maximum durations stated in the quote: 18 hours for movie playback and 15 hours for wireless web, with no unsupported additions or dropped conditions.

Extractor notes: None recorded.

### claim_mba_spec_cpu

- Claim: `claim_mba_spec_cpu`
- Tier: `C0`
- Type/predicate: `SPEC` / `cpu_configuration`
- Verifier state: document status is PARTIAL

Object

```json
{
  "chip": "Apple M3",
  "cpu_cores": 8,
  "efficiency_cores": 4,
  "performance_cores": 4
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
8-core CPU (4 performance + 4 efficiency cores)
```

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '8-core CPU (4 performance + 4 efficiency cores)', which directly supports the projection's assertions of 8 total cores, 4 performance cores, and 4 efficiency cores.

Extractor notes: None recorded.

### claim_mba_spec_camera

- Claim: `claim_mba_spec_camera`
- Tier: `C0`
- Type/predicate: `SPEC` / `camera`
- Verifier state: document status is PARTIAL

Object

```json
{
  "value": "1080p FaceTime HD camera"
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
1080p FaceTime HD camera; advanced image signal processor with computational video
```

Verifier (claim quote union): `ENTAILED` — The projection '1080p FaceTime HD camera' is a direct subset of the quoted text, which includes that exact phrase. No condition, direction, or qualifier is omitted that would broaden or alter the meaning. The additional text in the quote ('advanced image signal processor with computational video') is irrelevant to the projection and its omission does not change the semantic assertion.

Extractor notes: None recorded.

### claim_mba_spec_thunderbolt_capabilities

- Claim: `claim_mba_spec_thunderbolt_capabilities`
- Tier: `C0`
- Type/predicate: `SPEC` / `thunderbolt_port_capabilities`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_tech_specs_page`

```text
Two Thunderbolt / USB 4 ports supporting: charging, DisplayPort, Thunderbolt 3 (up to 40Gb/s), USB 4 (up to 40Gb/s)
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the capabilities and count stated in the quote: two ports supporting charging, DisplayPort, Thunderbolt 3 (up to 40Gb/s), and USB 4 (up to 40Gb/s), with no unsupported additions or dropped conditions.

Extractor notes: None recorded.

### claim_mba_spec_storage_options

- Claim: `claim_mba_spec_storage_options`
- Tier: `C0`
- Type/predicate: `SPEC` / `storage_options`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_tech_specs_page`

```text
256GB SSD; configurable to 512GB, 1TB, or 2TB
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the base storage (256GB SSD) and the configurable options (512GB, 1TB, 2TB) as stated in the quote; no unsupported addition or contradiction exists.

Extractor notes: None recorded.

### claim_mba_spec_box_contents

- Claim: `claim_mba_spec_box_contents`
- Tier: `C0`
- Type/predicate: `SPEC` / `box_contents`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_tech_specs_page`

```text
13-inch MacBook Air; 30W USB-C Power Adapter (8-core GPU) or 35W Dual USB-C Port Compact Power Adapter (10-core GPU + 512GB); USB-C to MagSafe 3 Cable (2 m)
```

Verifier (claim quote union): `ENTAILED` — The projection faithfully lists the exact components and their configurations as quoted, without adding, omitting, or altering any conditions, units, or qualifiers.

Extractor notes: None recorded.

### claim_mba_spec_operating_temperature

- Claim: `claim_mba_spec_operating_temperature`
- Tier: `C0`
- Type/predicate: `SPEC` / `operating_temperature_range`
- Verifier state: document status is PARTIAL

Object

```json
{
  "max_c": 35,
  "max_f": 95,
  "min_c": 10,
  "min_f": 50
}
```

Quote — binding 0, source `src_tech_specs_page`

```text
Operating temperature: 50° to 95° F (10° to 35° C)
```

Verifier (claim quote union): `ENTAILED` — The projection's temperature bounds exactly match the quoted operating range, with no added conditions or directions; the union supports all asserted values.

Extractor notes: None recorded.

### claim_mba_spec_launch_price

- Claim: `claim_mba_spec_launch_price`
- Tier: `C0`
- Type/predicate: `SPEC` / `launch_price_us`
- Verifier state: document status is PARTIAL

Object

```json
{
  "availability_date": "2024-03-08",
  "orders_date": "2024-03-04",
  "unit": "USD",
  "value": 1099
}
```

Quote — binding 0, source `src_specs_summary`

```text
Introduced: March 4, 2024 (orders), available March 8, 2024; launch price $1,099 US
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the dates and price from the quote: orders began March 4, 2024; availability started March 8, 2024; and the launch price was $1,099 US, which maps to value 1099 and unit USD. No unsupported additions, contradictions, or lost conditions.

Extractor notes: Curated spec summary cites the Newsroom launch article (src_newsroom_article, no local capture) as its origin for this fact; bound to the local summary only.

### claim_mba_part_thunderbolt_ports

- Claim: `claim_mba_part_thunderbolt_ports`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `thunderbolt_ports_location`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_ports_guide_tour`

```text
2x Thunderbolt / USB 4 ports (both on the left side, next to MagSafe)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms both Thunderbolt/USB 4 ports are on the left side, and one quote explicitly places them next to MagSafe; the projection accurately reflects this without adding unsupported conditions or broadening scope.

Quote — binding 1, source `src_specs_summary`

```text
| Thunderbolt / USB 4 (Thunderbolt 3 40Gb/s, USB 4 40Gb/s, DisplayPort, charging) | 2 | Left |
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms both Thunderbolt/USB 4 ports are on the left side, and one quote explicitly places them next to MagSafe; the projection accurately reflects this without adding unsupported conditions or broadening scope.

Extractor notes: None recorded.

### claim_mba_part_headphone_jack

- Claim: `claim_mba_part_headphone_jack`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `headphone_jack_location`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_ports_guide_tour`

```text
1x 3.5 mm headphone jack (the only port on the right side)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms the 3.5 mm headphone jack is on the right side and is the only port on that side; the projection faithfully restates this without adding unsupported conditions, directions, or scope.

Quote — binding 1, source `src_specs_summary`

```text
| 3.5 mm headphone jack (high-impedance headphone support) | 1 | Right |
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms the 3.5 mm headphone jack is on the right side and is the only port on that side; the projection faithfully restates this without adding unsupported conditions, directions, or scope.

Extractor notes: None recorded.

### claim_mba_part_touch_id

- Claim: `claim_mba_part_touch_id`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `touch_id_location`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_ports_guide_tour`

```text
**Touch ID (power button)**: top-right of keyboard
```

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the quote’s assertion: 'Touch ID (power button)' is located at the 'top-right of keyboard.' The rephrasing 'Touch ID (the power button)' is semantically equivalent to '(power button)' as a descriptor, and no conditions, directions, or qualifiers are omitted or added that alter meaning.

Extractor notes: None recorded.

### claim_mba_step_power_on_1

- Claim: `claim_mba_step_power_on_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

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

Quote — binding 0, source `src_ports_guide_tour`

```text
top-right of keyboard; press to turn on; authenticate and Apple Pay after setup
```

Verifier (claim quote union): `ENTAILED` — The quote states 'top-right of keyboard; press to turn on', which directly supports pressing the button at that location to turn on the device. The projection adds 'Touch ID (power button)' as a descriptor, which is a plausible functional label consistent with common device design and does not contradict the quote. No condition, direction, or scope is wrongly broadened or omitted.

Extractor notes: Single-step procedure: the guide states power-on as one action.

### claim_mba_step_bluetooth_pairing_1

- Claim: `claim_mba_step_bluetooth_pairing_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Turn on the Bluetooth device and make it discoverable, following the device manufacturer's instructions.",
  "procedure": "pair_bluetooth_device",
  "step_number": 1,
  "target_parts": [
    "bluetooth_accessory"
  ]
}
```

Quote — binding 0, source `src_bluetooth_pairing_guide`

```text
Make sure the device is turned on and discoverable (see the device's documentation for details).
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_mba_step_bluetooth_pairing_2

- Claim: `claim_mba_step_bluetooth_pairing_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "On the Mac, choose Apple menu > System Settings, then click Bluetooth in the sidebar.",
  "procedure": "pair_bluetooth_device",
  "step_number": 2,
  "target_parts": [
    "apple_menu",
    "system_settings",
    "bluetooth_sidebar"
  ]
}
```

Quote — binding 0, source `src_bluetooth_pairing_guide`

```text
On your Mac, choose Apple menu > System Settings, then click Bluetooth in the sidebar.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_mba_step_bluetooth_pairing_3

- Claim: `claim_mba_step_bluetooth_pairing_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Hold the pointer over the device, click Connect, then click Accept or enter the displayed numbers if prompted.",
  "procedure": "pair_bluetooth_device",
  "step_number": 3,
  "target_parts": [
    "bluetooth_device_list",
    "connect_button"
  ]
}
```

Quote — binding 0, source `src_bluetooth_pairing_guide`

```text
Hold the pointer over the device in the list, then click Connect. If asked, click Accept (or enter a series of numbers, then press Enter).
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_mba_step_connection_method_1

- Claim: `claim_mba_step_connection_method_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Choose one connection path: use a compatible cable and physical port for a wired device, or use Bluetooth pairing for a wireless device.",
  "procedure": "connect_wired_or_bluetooth_device",
  "step_number": 1,
  "target_parts": [
    "physical_port",
    "bluetooth_settings"
  ]
}
```

Quote — binding 0, source `src_ports_guide_tour`

```text
Stereo headphones or external speakers; supports high-impedance headphones without a separate DAC or amplifier.
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_ports_guide_tour`

```text
To pair Bluetooth accessories, Apple documents the process in the macOS User Guide
```

Verifier: no verdict recorded.

Extractor notes: Routing synthesis: the source separately documents physical-port connections and Bluetooth pairing; the step makes the mutually exclusive path choice explicit.

### claim_mba_step_connection_method_2

- Claim: `claim_mba_step_connection_method_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "For 3.5 mm headphones or speakers, use the headphone jack on the right; for a compatible USB-C or Thunderbolt accessory, use either Thunderbolt / USB 4 port on the left and follow the device documentation.",
  "procedure": "connect_wired_or_bluetooth_device",
  "step_number": 2,
  "target_parts": [
    "headphone_jack_3_5mm",
    "thunderbolt_usb4_ports"
  ]
}
```

Quote — binding 0, source `src_ports_guide_tour`

```text
The left side view of a MacBook Air with callouts to the MagSafe 3 and Thunderbolt / USB 4 ports
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_ports_guide_tour`

```text
The right side view of a MacBook Air with a callout to the 3.5 mm headphone jack
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_mba_step_connection_method_3

- Claim: `claim_mba_step_connection_method_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "If there is no cable and the intended path is wireless, open System Settings > Bluetooth, choose the discoverable device, and click Connect.",
  "procedure": "connect_wired_or_bluetooth_device",
  "step_number": 3,
  "target_parts": [
    "bluetooth_settings",
    "connect_button"
  ]
}
```

Quote — binding 0, source `src_bluetooth_pairing_guide`

```text
On your Mac, choose Apple menu > System Settings, then click Bluetooth in the sidebar. Hold the pointer over the device in the list, then click Connect.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

## 6. Open gaps (0)

None.

## 7. Batch-eligible C0/C1 spot-audit (0)

None.
