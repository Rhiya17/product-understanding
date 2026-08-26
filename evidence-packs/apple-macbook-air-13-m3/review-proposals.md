# Review Proposals — apple-macbook-air-13-m3

Generated: `2026-08-26`
Verification status: `COMPLETE`

This is an advisory proposal document, not a publication record. Only the product owner may mark decisions here. An unmarked item is undecided.

## Decision summary

- Claims in pack: `33`
- Existing human decisions: `0`
- Undecided claims covered here: `33`
- Existing decisions reopened by v2 alarms: `0`
- Total owner action items: `33`
- Proposed `NEEDS_RECHECK`: `5`
- Proposed `REJECTED_FOR_SERVING`: `0`
- Proposed `APPROVED_FOR_PUBLISH`: `28`
- Batch-eligible C0/C1: `28`

For C2/C3, mark every item individually. For section 7, inspect every designated sample item; then either confirm the batch statement or mark the sample as failed and decide every batch member individually.

## 1. MEANING_CHANGED alarms (5)

### `claim_mba_part_magsafe_port`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `magsafe_3_port_location`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source. The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| MagSafe 3 charging port | 1 | Left |
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'next to the two Thunderbolt / USB 4 ports,' which is not mentioned or implied in any quote; this introduces an unsupported spatial relationship and broadens the claim beyond the source.

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
- Proposed rationale: Verifier found a meaning change: The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists. The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
Fast charge up to 50 percent in around 30 minutes with the optional 70W USB-C Power Adapter.
```

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts that the 70W USB-C Power Adapter is 'optional' while also being a requirement ('requires'), which is a contradiction. The quotes state the adapter is 'optional' for fast charging, not that it is required. The projection wrongly implies a mandatory condition where none exists.

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
- Proposed rationale: Verifier found a meaning change: The projection asserts 'base_gb':16, but the quote states 16GB is the default configuration while explicitly listing 8GB as the base configuration (which is configurable to 16GB or 24GB), making 16GB not the base but an upgrade option; thus, assigning 16 as the base misrepresents the hierarchy and conditions.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection asserts 'base_gb':16, but the quote states 16GB is the default configuration while explicitly listing 8GB as the base configuration (which is configurable to 16GB or 24GB), making 16GB not the base but an upgrade option; thus, assigning 16 as the base misrepresents the hierarchy and conditions.

Extractor notes: Capture notes that the tech specs page's 16GB base reflects Apple's 2025 update; the March 2024 launch base configuration was 8GB. Reviewer should decide whether applicability.revision should split this claim.

Rework path: Correct the structured translation or add an authoritative quote that supports every stated detail, then re-run verification.

### `claim_mba_spec_newest_compatible_os`

- Proposed disposition: **`NEEDS_RECHECK`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `newest_compatible_os`
- Source authority: `MANUFACTURER_SUPPORT_PAGE`
- Queue section: `alarm`
- Review focus: HARD REVIEW — verifier MEANING_CHANGED
- Proposed rationale: Verifier found a meaning change: The quote specifies 'as of retrieval' without a date, while the projection asserts a specific date '2026-08-20', which is an unsupported addition not present in the source.

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

Verifier (claim quote union): `MEANING_CHANGED` — The quote specifies 'as of retrieval' without a date, while the projection asserts a specific date '2026-08-20', which is an unsupported addition not present in the source.

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
- Proposed rationale: Verifier found a meaning change: The projection adds 'into the MagSafe 3 port', which is not mentioned in the quote. The quote only says 'Plug in the included USB-C Power Adapter' without specifying any port, let alone the MagSafe 3 port. This is an unsupported semantic addition that narrows the scope of the action incorrectly.

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

Verifier (claim quote union): `MEANING_CHANGED` — The projection adds 'into the MagSafe 3 port', which is not mentioned in the quote. The quote only says 'Plug in the included USB-C Power Adapter' without specifying any port, let alone the MagSafe 3 port. This is an unsupported semantic addition that narrows the scope of the action incorrectly.

Extractor notes: Single-step procedure: the guide states charging as one action.

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

## 7. Batch-eligible C0/C1 spot-audit (28)

Batch ID: `batch_apple-macbook-air-13-m3_20260826`

- [ ] OWNER CONFIRMS: I reviewed all `5` designated sample claims and confirm `APPROVED_FOR_PUBLISH` for all `28` members of `batch_apple-macbook-air-13-m3_20260826`.
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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the height values and units from both quotes: 0.44 inch and 1.13 cm, with no added conditions, directions, or unsupported semantic expansions.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Height (closed) | 0.44 in (1.13 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the height values and units from both quotes: 0.44 inch and 1.13 cm, with no added conditions, directions, or unsupported semantic expansions.

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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in both quotes without adding, omitting, or altering any conditions, directions, or qualifiers.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Width | 11.97 in (30.41 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in both quotes without adding, omitting, or altering any conditions, directions, or qualifiers.

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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in the quotes: 8.46 inches and 21.5 cm, with no added conditions, directions, or unsupported semantic expansions.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Depth | 8.46 in (21.5 cm) |
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the exact values and units stated in the quotes: 8.46 inches and 21.5 cm, with no added conditions, directions, or unsupported semantic expansions.

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

Verifier (claim quote union): `ENTAILED` — Every semantic assertion in the projection is directly supported by the union of quotes: both quotes state the weight as 2.7 lb and 1.24 kg, and both include the note 'varies by configuration'. The projection faithfully extracts these values and qualifiers without adding, broadening, or omitting any governing condition.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Weight | 2.7 lb (1.24 kg), varies by configuration |
```

Verifier (claim quote union): `ENTAILED` — Every semantic assertion in the projection is directly supported by the union of quotes: both quotes state the weight as 2.7 lb and 1.24 kg, and both include the note 'varies by configuration'. The projection faithfully extracts these values and qualifiers without adding, broadening, or omitting any governing condition.

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

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Bluetooth 5.3' twice, which fully supports the projection's assertion of standard 'Bluetooth' and value '5.3' without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Bluetooth 5.3
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Bluetooth 5.3' twice, which fully supports the projection's assertion of standard 'Bluetooth' and value '5.3' without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: None recorded.

### `claim_mba_spec_wifi_standard`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `wifi_standard`
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
  "standard": "802.11ax",
  "value": "Wi-Fi 6E"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Wi-Fi 6E (802.11ax)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Wi-Fi 6E (802.11ax)', which directly supports both the standard '802.11ax' and the value 'Wi-Fi 6E' in the projection without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Wi-Fi 6E (802.11ax)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes explicitly states 'Wi-Fi 6E (802.11ax)', which directly supports both the standard '802.11ax' and the value 'Wi-Fi 6E' in the projection without adding, omitting, or altering any semantic condition or qualifier.

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

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the four colors stated in both quotes, with no added conditions, directions, or qualifiers; the union of quotes fully supports the semantic content of the projection.

Quote — binding 1, source `src_identify_page`, page `None`

```text
**Colors**: Silver, Starlight, Space Gray, Midnight
```

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the four colors stated in both quotes, with no added conditions, directions, or qualifiers; the union of quotes fully supports the semantic content of the projection.

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

Verifier (claim quote union): `ENTAILED` — Both quotes explicitly state the model identifier as 'Mac15,12', and the projection faithfully extracts this exact value without adding, omitting, or altering any semantic condition or qualifier.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
Model identifier: **Mac15,12**
```

Verifier (claim quote union): `ENTAILED` — Both quotes explicitly state the model identifier as 'Mac15,12', and the projection faithfully extracts this exact value without adding, omitting, or altering any semantic condition or qualifier.

Extractor notes: None recorded.

### `claim_mba_spec_speaker_system` — SPOT-AUDIT SAMPLE

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `speaker_system`
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
  "detail": "two tweeters, two woofers",
  "value": "four-speaker sound system"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Four-speaker sound system
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports both assertions: 'four-speaker sound system' is directly stated in both, and 'two tweeters, two woofers' is explicitly provided in the second quote as the composition of that system. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
the 13-inch MacBook Air has a four-speaker sound system (two tweeters, two woofers)
```

Verifier (claim quote union): `ENTAILED` — The union of quotes supports both assertions: 'four-speaker sound system' is directly stated in both, and 'two tweeters, two woofers' is explicitly provided in the second quote as the composition of that system. No condition, direction, or qualifier is omitted that would broaden or alter the meaning.

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

Verifier (claim quote union): `ENTAILED` — The projection lists exactly the audio formats quoted, with no added conditions, directions, or semantic expansions; the union of quotes fully supports the asserted values.

Extractor notes: None recorded.

### `claim_mba_spec_headphone_jack_impedance`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `headphone_jack_high_impedance_support`
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
  "description": "3.5 mm headphone jack with advanced support for high-impedance headphones",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
3.5 mm headphone jack with advanced support for high-impedance headphones
```

Verifier (claim quote union): `ENTAILED` — The projection's description exactly matches the first quote, and the value 'true' is semantically supported by both quotes asserting the feature exists and functions without additional hardware — no unsupported addition, contradiction, or lost condition.

Quote — binding 1, source `src_ports_guide_tour`, page `None`

```text
supports high-impedance headphones without a separate DAC or amplifier
```

Verifier (claim quote union): `ENTAILED` — The projection's description exactly matches the first quote, and the value 'true' is semantically supported by both quotes asserting the feature exists and functions without additional hardware — no unsupported addition, contradiction, or lost condition.

Extractor notes: None recorded.

### `claim_mba_spec_microphone_array`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `microphone_array`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately extracts 'directional beamforming', 'Voice Isolation', and 'Wide Spectrum' as features from the quote, and correctly assigns 'three-mic array' as the value. All assertions are directly supported by the single quote without adding, omitting, or misrepresenting conditions, directions, or scope.

Extractor notes: None recorded.

### `claim_mba_spec_spatial_audio`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `spatial_audio_support`
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
  "condition": "when playing music or video with Dolby Atmos on built-in speakers",
  "value": true
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Spatial Audio when playing music/video with Dolby Atmos on built-in speakers
```

Verifier (claim quote union): `ENTAILED` — The projection's condition exactly matches the quote's context, and the value 'true' is a faithful semantic assertion of the feature being enabled under that condition; no unsupported addition or contradiction exists.

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

Verifier (claim quote union): `ENTAILED` — Every assertion in the projection — LED backlight, 13.6-inch diagonal, IPS panel, and Liquid Retina display — is directly and unambiguously stated in the quote; no condition, direction, or qualifier is omitted that would broaden or alter the meaning.

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

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '2560-by-1664 native resolution at 224 ppi', which directly supports the width_px (2560), height_px (1664), and ppi (224) values in the projection without adding, omitting, or altering any conditions or directions.

Extractor notes: None recorded.

### `claim_mba_spec_battery_capacity`

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

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '52.6-watt-hour lithium-polymer battery', which directly supports the chemistry, unit, and value in the projection without adding or omitting any governing conditions or semantic qualifiers.

Extractor notes: None recorded.

### `claim_mba_spec_battery_life`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `battery_life`
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
  "movie_playback_hours": 18,
  "wireless_web_hours": 15
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
Up to 18 hours Apple TV app movie playback; up to 15 hours wireless web
```

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the maximum durations stated in the quote: 18 hours for movie playback and 15 hours for wireless web, with no unsupported additions or dropped conditions.

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

Verifier (claim quote union): `ENTAILED` — The quote explicitly states '8-core CPU (4 performance + 4 efficiency cores)', which directly supports the projection's assertions of 8 total cores, 4 performance cores, and 4 efficiency cores.

Extractor notes: None recorded.

### `claim_mba_spec_camera`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `camera`
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
  "value": "1080p FaceTime HD camera"
}
```

Quote — binding 0, source `src_tech_specs_page`, page `None`

```text
1080p FaceTime HD camera; advanced image signal processor with computational video
```

Verifier (claim quote union): `ENTAILED` — The projection '1080p FaceTime HD camera' is a direct subset of the quoted text, which includes that exact phrase. No condition, direction, or qualifier is omitted that would broaden or alter the meaning. The additional text in the quote ('advanced image signal processor with computational video') is irrelevant to the projection and its omission does not change the semantic assertion.

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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the capabilities and count stated in the quote: two ports supporting charging, DisplayPort, Thunderbolt 3 (up to 40Gb/s), and USB 4 (up to 40Gb/s), with no unsupported additions or dropped conditions.

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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the base storage (256GB SSD) and the configurable options (512GB, 1TB, 2TB) as stated in the quote; no unsupported addition or contradiction exists.

Extractor notes: None recorded.

### `claim_mba_spec_box_contents`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C0`
- Type / predicate: `SPEC` / `box_contents`
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

Verifier (claim quote union): `ENTAILED` — The projection faithfully lists the exact components and their configurations as quoted, without adding, omitting, or altering any conditions, units, or qualifiers.

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

Verifier (claim quote union): `ENTAILED` — The projection's temperature bounds exactly match the quoted operating range, with no added conditions or directions; the union supports all asserted values.

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

Verifier (claim quote union): `ENTAILED` — The projection accurately reflects the dates and price from the quote: orders began March 4, 2024; availability started March 8, 2024; and the launch price was $1,099 US, which maps to value 1099 and unit USD. No unsupported additions, contradictions, or lost conditions.

Extractor notes: Curated spec summary cites the Newsroom launch article (src_newsroom_article, no local capture) as its origin for this fact; bound to the local summary only.

### `claim_mba_part_thunderbolt_ports`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `thunderbolt_ports_location`
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

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms both Thunderbolt/USB 4 ports are on the left side, and one quote explicitly places them next to MagSafe; the projection accurately reflects this without adding unsupported conditions or broadening scope.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| Thunderbolt / USB 4 (Thunderbolt 3 40Gb/s, USB 4 40Gb/s, DisplayPort, charging) | 2 | Left |
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms both Thunderbolt/USB 4 ports are on the left side, and one quote explicitly places them next to MagSafe; the projection accurately reflects this without adding unsupported conditions or broadening scope.

Extractor notes: None recorded.

### `claim_mba_part_headphone_jack`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `headphone_jack_location`
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

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms the 3.5 mm headphone jack is on the right side and is the only port on that side; the projection faithfully restates this without adding unsupported conditions, directions, or scope.

Quote — binding 1, source `src_specs_summary`, page `None`

```text
| 3.5 mm headphone jack (high-impedance headphone support) | 1 | Right |
```

Verifier (claim quote union): `ENTAILED` — The union of quotes confirms the 3.5 mm headphone jack is on the right side and is the only port on that side; the projection faithfully restates this without adding unsupported conditions, directions, or scope.

Extractor notes: None recorded.

### `claim_mba_part_touch_id`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `PART_LOCATION` / `touch_id_location`
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

Verifier (claim quote union): `ENTAILED` — The projection accurately restates the quote’s assertion: 'Touch ID (power button)' is located at the 'top-right of keyboard.' The rephrasing 'Touch ID (the power button)' is semantically equivalent to '(power button)' as a descriptor, and no conditions, directions, or qualifiers are omitted or added that alter meaning.

Extractor notes: None recorded.

### `claim_mba_step_power_on_1`

- Proposed disposition: **`APPROVED_FOR_PUBLISH`**
- Owner decision: [ ] confirm recommendation  [ ] override: __________
- Claim tier: `C1`
- Type / predicate: `STEP` / `procedure_step`
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

Verifier (claim quote union): `ENTAILED` — The quote states 'top-right of keyboard; press to turn on', which directly supports pressing the button at that location to turn on the device. The projection adds 'Touch ID (power button)' as a descriptor, which is a plausible functional label consistent with common device design and does not contradict the quote. No condition, direction, or scope is wrongly broadened or omitted.

Extractor notes: Single-step procedure: the guide states power-on as one action.
