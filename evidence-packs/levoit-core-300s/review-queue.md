# Review Queue — levoit-core-300s

Verification status: `PARTIAL`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.

## 1. MEANING_CHANGED alarms (0)

None.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (6)

### claim_c300s_warning_plastic_wrap

- Claim: `claim_c300s_warning_plastic_wrap`
- Tier: `C3`
- Type/predicate: `WARNING` / `remove_filter_wrap_before_use`

Object

```json
{
  "description": "Do not use without removing the plastic wrap from the filter; the purifier will not filter air and may overheat, causing a fire hazard.",
  "hazard_type": "fire"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Do not use without removing the plastic wrap from the filter. The air purifier will not filter air, and may overheat, causing a fire hazard.
```

Verifier: no verdict recorded.

Extractor notes: C3 assigned per work order rule: all safety warnings from the manuals.

### claim_c300s_warning_water

- Claim: `claim_c300s_warning_water`
- Tier: `C3`
- Type/predicate: `WARNING` / `keep_away_from_water`

Object

```json
{
  "description": "Keep the air purifier away from water and wet or damp areas; never place in water or liquid.",
  "hazard_type": "electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Keep the air purifier away from water, and wet or damp areas. Never place in water or liquid.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_warning_oxygen

- Claim: `claim_c300s_warning_oxygen`
- Tier: `C3`
- Type/predicate: `WARNING` / `oxygen_administration_distance`

Object

```json
{
  "description": "Keep 5 ft / 1.5 m away from where oxygen is being administered.",
  "hazard_type": "fire"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Keep 5 ft / 1.5 m away from where oxygen is being administered.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_warning_combustible

- Claim: `claim_c300s_warning_combustible`
- Tier: `C3`
- Type/predicate: `WARNING` / `no_combustible_environments`

Object

```json
{
  "description": "Do not use where combustible gases, vapors, metallic dust, aerosol products, or fumes from industrial oil are present.",
  "hazard_type": "fire_explosion"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Do not use where combustible gases, vapors, metallic dust, aerosol (spray) products, or fumes from industrial oil are present.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_warning_dimmer

- Claim: `claim_c300s_warning_dimmer`
- Tier: `C3`
- Type/predicate: `WARNING` / `no_solid_state_speed_controls`

Object

```json
{
  "description": "Do not use this air purifier with any solid-state speed controls such as a dimmer switch.",
  "hazard_type": "fire_electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
WARNING: To reduce the risk of fire or electric shock, do not use this air purifier with any solid-state speed controls (such as a dimmer switch).
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_warning_unplug_before_maintenance

- Claim: `claim_c300s_warning_unplug_before_maintenance`
- Tier: `C3`
- Type/predicate: `WARNING` / `unplug_before_maintenance`

Object

```json
{
  "description": "Always unplug the air purifier before servicing, cleaning, or other maintenance such as changing the filter.",
  "hazard_type": "electric_shock"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Always unplug the air purifierbefore servicing ,cleaning or other maintenances(such aschanging the filter).
```

Verifier: no verdict recorded.

Extractor notes: Quote is verbatim from the 300S-P manual's embedded text layer, including its missing/misplaced spaces (text-layer artifact of that PDF). The original 300S manual page 3 reads cleanly: 'Always unplug the air purifier before servicing (such as changing the filter).' (visually verified).

## 4. C2 claims (13)

### claim_c300s_step_replace_filter_1

- Claim: `claim_c300s_step_replace_filter_1`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Unplug the air purifier. Flip the air purifier over and remove the filter cover.",
  "procedure": "replace_filter",
  "step_number": 1,
  "target_parts": [
    "power_cord",
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
1. Unplug the air purifier. Flip the air purifier over and remove the filter cover (see Getting Started, page 7).
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_replace_filter_2

- Claim: `claim_c300s_step_replace_filter_2`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Remove the old filter.",
  "procedure": "replace_filter",
  "step_number": 2,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
2. Remove the old filter.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_replace_filter_3

- Claim: `claim_c300s_step_replace_filter_3`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Clean out any remaining dust or hair inside the air purifier using a vacuum hose. Do not use water or liquids.",
  "procedure": "replace_filter",
  "step_number": 3,
  "target_parts": [
    "filter_compartment"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
3. Clean out any remaining dust or hair inside the air purifier using a vacuum hose. Do not use water or liquids to clean the air purifier. [Figure 3.2]
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_replace_filter_4

- Claim: `claim_c300s_step_replace_filter_4`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Unwrap the new filter and place it into the housing.",
  "procedure": "replace_filter",
  "step_number": 4,
  "target_parts": [
    "filter_cartridge",
    "housing"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
4. Unwrap the new filter and place it into the housing (see Getting Started, page 7).
```

Verifier: no verdict recorded.

Extractor notes: Orientation detail from Getting Started: filter goes in with the handle facing up (see claim_c300s_step_initial_setup_2).

### claim_c300s_step_replace_filter_5

- Claim: `claim_c300s_step_replace_filter_5`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Replace the cover. Plug in the air purifier.",
  "procedure": "replace_filter",
  "step_number": 5,
  "target_parts": [
    "filter_cover",
    "power_cord"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
5. Replace the cover. Plug in the air purifier.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_replace_filter_6

- Claim: `claim_c300s_step_replace_filter_6`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Reset the Check Filter Indicator.",
  "procedure": "replace_filter",
  "step_number": 6,
  "target_parts": [
    "sleep_mode_button",
    "check_filter_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
6. Reset the Check Filter Indicator (see page 13).
```

Verifier: no verdict recorded.

Extractor notes: Reset detail is the reset_check_filter_indicator procedure (claims claim_c300s_step_reset_filter_1..4).

### claim_c300s_step_initial_setup_1

- Claim: `claim_c300s_step_initial_setup_1`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Flip the air purifier over. Twist the filter cover counterclockwise and remove it.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 1,
  "target_parts": [
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
1. Flip the air purifier over. Twist the filter cover counterclockwise and remove it. [Figure 1.1]
```

Verifier: no verdict recorded.

Extractor notes: C2 assigned (higher of C1/C2) because the step opens the filter compartment.

### claim_c300s_step_initial_setup_2

- Claim: `claim_c300s_step_initial_setup_2`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Remove the filter from its plastic packaging and place it back into the air purifier with the handle facing up.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 2,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
2. Remove the filter from its plastic packaging and place the filter back into the air purifier with the handle facing up. [Figure 1.2]
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_initial_setup_3

- Claim: `claim_c300s_step_initial_setup_3`
- Tier: `C2`
- Type/predicate: `STEP` / `procedure_step`

Object

```json
{
  "action": "Replace the filter cover and twist clockwise to lock (cover should snap shut).",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 3,
  "target_parts": [
    "filter_cover"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
3. Replace the filter cover and twist clockwise to lock. [Figure 1.3]
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_care_prefilter_cleaning

- Claim: `claim_c300s_care_prefilter_cleaning`
- Tier: `C2`
- Type/predicate: `CARE` / `prefilter_cleaning`

Object

```json
{
  "interval": "every 2-4 weeks",
  "method": "soft brush or vacuum hose",
  "restrictions": [
    "Do not clean the filter with water or other liquids",
    "Main filter: do not clean"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
The outer pre-filter should be cleaned every 2–4 weeks to increase efficiency and extend the life of your filter. Clean the pre-filter using a soft brush or vacuum hose to remove hair, dust, and large particles.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_care_sensor_cleaning

- Claim: `claim_c300s_care_sensor_cleaning`
- Tier: `C2`
- Type/predicate: `CARE` / `dust_sensor_cleaning`

Object

```json
{
  "interval": "every 3 months",
  "method": "unplug; place a vacuum cleaner over the sensor openings; run the vacuum for at least 10 seconds"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
The AirSight Plus Laser Dust Sensor can be blocked by dust, which affects the sensor’s accuracy. Clean the sensor every 3 months.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_care_filter_lifespan

- Claim: `claim_c300s_care_filter_lifespan`
- Tier: `C2`
- Type/predicate: `CARE` / `filter_replacement_interval`

Object

```json
{
  "interval": "every 6-8 months",
  "signals": [
    "increased noise",
    "decreased airflow",
    "unusual odors",
    "visibly clogged filter"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
The filter should be replaced every 6–8 months. Y ou may need to replace your filter earlier or later depending on how often you use your air purifier.
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_spec_page_core300s`

```text
Filter lifespan: 6–8 months; filter life tracked in the VeSync app
```

Verifier: no verdict recorded.

Extractor notes: The 'Y ou' spacing in the first quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

### claim_c300s_compat_filter_models

- Claim: `claim_c300s_compat_filter_models`
- Tier: `C2`
- Type/predicate: `COMPATIBILITY` / `replacement_filter_compatible_models`

Object

```json
{
  "compatible_with": [
    "Core 300",
    "Core 300-P",
    "Core 300S",
    "Core 300S-P",
    "Core P350",
    "Core P350-P"
  ],
  "counterpart": "Levoit Core 300 Series Original Filter (Core 300-RF)"
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
Compatible models per VeSync store: Core 300, Core 300-P, Core 300S, Core 300S-P, Core P350, Core P350-P
```

Verifier: no verdict recorded.

Extractor notes: Underlying source is the official VeSync store filter page (src_support_vesync_filter_page), which has no local capture; the binding cites the vault's spec transcription that records it (see gaps.json gap_support_page_capture_1).

## 5. Unresolved verifier — C0/C1 (30)

### claim_c300s_spec_dimensions

- Claim: `claim_c300s_spec_dimensions`
- Tier: `C0`
- Type/predicate: `SPEC` / `product_dimensions`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric": "22 x 22 x 36 cm",
  "unit": "in",
  "value": {
    "depth_in": 8.7,
    "height_in": 14.2,
    "width_in": 8.7
  }
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
Dimensions: 8.7 x 8.7 x 14.2 in / 22 x 22 x 36 cm
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Dimensions 8.7 × 8.7 × 14.2 in / 22 × 22 × 36 cm
```

Verifier: no verdict recorded.

Extractor notes: Same value confirmed visually on page 2 of src_manual_core300s_us (no machine-readable text layer; see gaps.json gap_300s_manual_binding_1).

### claim_c300s_spec_cadr

- Claim: `claim_c300s_spec_cadr`
- Tier: `C0`
- Type/predicate: `SPEC` / `clean_air_delivery_rate`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric": "240 m³/h",
  "unit": "CFM",
  "value": 141
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
CADR: 141 CFM / 240 m³/h
```

Verifier: no verdict recorded.

Extractor notes: Also stated on pages 2 and 11 of src_manual_core300s_us ('CADR (CFM) 141 CFM / 240 m³/h'; 'Clean Air Delivery Rate of 141 cubic feet per minute (CFM), or 240 m³/h'), visually verified. The 300S-P manual spec table omits CADR; not treated as a conflict (absence, not disagreement).

### claim_c300s_spec_coverage

- Claim: `claim_c300s_spec_coverage`
- Tier: `C0`
- Type/predicate: `SPEC` / `room_coverage`
- Verifier state: document status is PARTIAL

Object

```json
{
  "extended_coverage_ft2_at_1ach": 1051,
  "ideal_room_size_ft2": 219,
  "ideal_room_size_m2": 20
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
Ideal room size (coverage): 1,051 ft² at 1 air change per hour; 219 ft² at 4.8 ACH
```

Verifier: no verdict recorded.

Extractor notes: 300S manual page 2 states 'Ideal Room Size 219 ft² / 20 m²' and page 11 states 'an air change per hour of 5' (visually verified) — slight tension with the spec page's '4.8 ACH'; flagged for reviewer, not a 300S vs 300S-P revision conflict. See also claim_c300s_limit_room_size.

### claim_c300s_spec_power_supply

- Claim: `claim_c300s_spec_power_supply`
- Tier: `C0`
- Type/predicate: `SPEC` / `power_supply`
- Verifier state: document status is PARTIAL

Object

```json
{
  "frequency": "60Hz",
  "voltage": "AC 120V"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Power Supply AC 120V, 60Hz
```

Verifier: no verdict recorded.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_spec_standby_power

- Claim: `claim_c300s_spec_standby_power`
- Tier: `C0`
- Type/predicate: `SPEC` / `standby_power`
- Verifier state: document status is PARTIAL

Object

```json
{
  "unit": "W",
  "value": "< 2"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Standby Power < 2W
```

Verifier: no verdict recorded.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_spec_operating_conditions

- Claim: `claim_c300s_spec_operating_conditions`
- Tier: `C0`
- Type/predicate: `SPEC` / `operating_temperature_range`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric": "-10 to 40 °C",
  "unit": "°F",
  "value": "14 to 104"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Temperature: 14°–104°F / -10°–40°C
```

Verifier: no verdict recorded.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_spec_wifi_band

- Claim: `claim_c300s_spec_wifi_band`
- Tier: `C1`
- Type/predicate: `SPEC` / `wireless_connectivity`
- Verifier state: document status is PARTIAL

Object

```json
{
  "app": "VeSync",
  "wifi_band": "2.4 GHz"
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
WiFi (2.4 GHz) + VeSync app: remote control, schedules, timers, filter life %, PM2.5 history, Auto/Sleep modes
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_manual_core300sp_us`

```text
During the setup process, you must be on a secure 2.4GHz WiFi network.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_spec_voice_control

- Claim: `claim_c300s_spec_voice_control`
- Tier: `C1`
- Type/predicate: `SPEC` / `voice_assistant_support`
- Verifier state: document status is PARTIAL

Object

```json
{
  "assistants": [
    "Amazon Alexa",
    "Google Assistant"
  ],
  "requires": "VeSync account"
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
Voice control: Amazon Alexa and Google Assistant
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Note: Y ou must create your own VeSync account to access voice assistants.
```

Verifier: no verdict recorded.

Extractor notes: The 'Y ou' spacing in the second quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

### claim_c300s_spec_package_contents

- Claim: `claim_c300s_spec_package_contents`
- Tier: `C0`
- Type/predicate: `SPEC` / `package_contents`
- Verifier state: document status is PARTIAL

Object

```json
{
  "items": [
    "1 x Smart Air Purifier",
    "1 x Pre-installed 3-Stage Original Filter",
    "1 x User Manual",
    "1 x Quick Start Guide"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
1 × Smart Air Purifier 1 × Pre-installed 3-Stage Original Filter 1 × User Manual 1 × Quick Start Guide
```

Verifier: no verdict recorded.

Extractor notes: Original 300S manual page 2 lists the same four items but names the filter 'True HEPA 3-Stage Original Filter (Pre-Installed)' (visually verified). Wording difference only; item count identical, so not recorded as a value conflict.

### claim_c300s_spec_model_name

- Claim: `claim_c300s_spec_model_name`
- Tier: `C0`
- Type/predicate: `SPEC` / `model_name`
- Verifier state: document status is PARTIAL

Object

```json
{
  "value": "Core 300S"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Product Name Smart Air Purifier Model Core 300S
```

Verifier: no verdict recorded.

Extractor notes: Even the current 300S-P manual's warranty table lists Model: Core 300S (spec table on its page 2 says 'Model Core 300S series'). Original 300S manual page 19 identically lists Model: Core 300S (visually verified).

### claim_c300s_spec_filtration_stages

- Claim: `claim_c300s_spec_filtration_stages`
- Tier: `C0`
- Type/predicate: `SPEC` / `filtration_stages`
- Verifier state: document status is PARTIAL

Object

```json
{
  "form": "single cylindrical cartridge",
  "stages": [
    "nylon pre-filter",
    "True HEPA main filter",
    "high-efficiency activated carbon filter"
  ]
}
```

Quote — binding 0, source `src_spec_page_core300s`

```text
3-stage filter cartridge (single cylindrical unit): ultra-fine nylon pre-filter + True HEPA main filter + high-efficiency activated carbon filter
```

Verifier: no verdict recorded.

Extractor notes: 300S manual page 11 additionally states the H13 True HEPA filter 'Captures at least 99.97% of airborne particles 0.3 microns (μm) in size' — visually verified but not extractable as a bindable quote (see gaps.json gap_hepa_efficiency_1). The 300S-P manual drops the 'True HEPA'/H13 wording.

### claim_c300s_spec_aq_indicator

- Claim: `claim_c300s_spec_aq_indicator`
- Tier: `C1`
- Type/predicate: `SPEC` / `air_quality_indicator_mapping`
- Verifier state: document status is PARTIAL

Object

```json
{
  "mapping": [
    {
      "air_quality": "Very Good",
      "auto_mode_fan_speed": "Sleep Mode",
      "color": "Blue"
    },
    {
      "air_quality": "Good",
      "auto_mode_fan_speed": "Low",
      "color": "Green"
    },
    {
      "air_quality": "Moderate",
      "auto_mode_fan_speed": "Medium",
      "color": "Orange"
    },
    {
      "air_quality": "Bad",
      "auto_mode_fan_speed": "High",
      "color": "Red"
    }
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Indicator Color Air Quality Auto Mode Fan Speed Blue Very Good Sleep Mode Green Good Low Orange Moderate Medium Red Bad High
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_img_aq_indicator_table`

```text
Official 'Air Quality Indicator Color Table' graphic showing the same color-to-quality-to-fan-speed mapping.
```

Verifier: `CANNOT_JUDGE` — Visual binding; text-only verification is unavailable.

Extractor notes: First quote is the manual's chart flattened to reading order by text extraction. Second binding is an image (visual, mechanically unverifiable).

### claim_c300s_limit_humidity

- Claim: `claim_c300s_limit_humidity`
- Tier: `C1`
- Type/predicate: `LIMIT` / `maximum_operating_humidity`
- Verifier state: document status is PARTIAL

Object

```json
{
  "unit": "% RH",
  "value": "< 85"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Humidity: < 85% RH
```

Verifier: no verdict recorded.

Extractor notes: 300S manual page 11 (Humidity section) adds that above this level 'the surface of the filter may become moldy' (visually verified).

### claim_c300s_limit_room_size

- Claim: `claim_c300s_limit_room_size`
- Tier: `C1`
- Type/predicate: `LIMIT` / `effective_room_size`
- Verifier state: document status is PARTIAL

Object

```json
{
  "metric": "20 m²",
  "unit": "ft²",
  "value": 219
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Make sure the room is smaller than 219 ft² / 20 m². The air purifier may not be as effective in larger rooms.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_reset_filter_1

- Claim: `claim_c300s_step_reset_filter_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Replace the filter.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 1,
  "target_parts": [
    "filter_cartridge"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
1. Replace the filter (see page 14).
```

Verifier: no verdict recorded.

Extractor notes: Case A of the manual's reset instructions (indicator lit red). Case B (filter changed before the indicator lit) is press-and-hold only; recorded in the PART_LOCATION claim's notes.

### claim_c300s_step_reset_filter_2

- Claim: `claim_c300s_step_reset_filter_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Turn on the air purifier.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 2,
  "target_parts": [
    "on_off_button"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
2. Turn on the air purifier.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_reset_filter_3

- Claim: `claim_c300s_step_reset_filter_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Press and hold the Sleep Mode button for 3 seconds.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 3,
  "target_parts": [
    "sleep_mode_button"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
3. Press and hold for 3 seconds.
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Reset the Check Filter Indicator by pressing and holding the Sleep Mode button for 3 seconds.
```

Verifier: no verdict recorded.

Extractor notes: The page 13 step shows the Sleep Mode moon icon between 'hold' and 'for'; the icon glyph does not survive text extraction. Page 6 quote names the button explicitly.

### claim_c300s_step_reset_filter_4

- Claim: `claim_c300s_step_reset_filter_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Confirm the Check Filter Indicator turns off, indicating a successful reset.",
  "procedure": "reset_check_filter_indicator",
  "step_number": 4,
  "target_parts": [
    "check_filter_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
4. will turn off when successfully reset.
```

Verifier: no verdict recorded.

Extractor notes: The Check Filter icon precedes 'will turn off' on the printed page; the icon glyph does not survive text extraction.

### claim_c300s_step_app_setup_1

- Claim: `claim_c300s_step_app_setup_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Download the VeSync app by scanning the QR code or searching \"VeSync\" in the Apple App Store or Google Play Store.",
  "procedure": "vesync_app_setup",
  "step_number": 1
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
1. To download the VeSync app, scan the QR code or search “VeSync” in the Apple App Store® or Google Play Store.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_app_setup_2

- Claim: `claim_c300s_step_app_setup_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Open the VeSync app and Log In or Sign Up.",
  "procedure": "vesync_app_setup",
  "step_number": 2
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
2. Open the VeSync app. Log In or Sign Up.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_app_setup_3

- Claim: `claim_c300s_step_app_setup_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Follow the in-app instructions to set up the smart air purifier.",
  "procedure": "vesync_app_setup",
  "step_number": 3
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
3. Follow the in-app instructions to set up your smart air purifier.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_initial_setup_4

- Claim: `claim_c300s_step_initial_setup_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Place the purifier on a flat, stable surface with the display facing up, allowing at least 15 in / 38 cm of clearance on all sides, away from anything that would block airflow.",
  "procedure": "initial_setup_unwrap_filter",
  "step_number": 4,
  "target_parts": [
    "housing"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
4. Place the purifier on a flat, stable surface with the display facing up. Allow at least 15 inches / 38 cm of clearance on all sides.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_step_wifi_reset_1

- Claim: `claim_c300s_step_wifi_reset_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`
- Verifier state: document status is PARTIAL

Object

```json
{
  "action": "Press and hold the On/Off button for 15 seconds until the Wi-Fi indicator turns off. This restores default settings and disconnects the purifier from the VeSync app.",
  "procedure": "disconnect_wifi_restore_defaults",
  "step_number": 1,
  "target_parts": [
    "on_off_button",
    "wifi_indicator"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
To disconnect Wi-Fi, press and hold the On/Off button for 15 seconds until the Wi-Fi indicator turns off. This will restore the smart air purifier’s default settings and disconnect it from the VeSync app.
```

Verifier: no verdict recorded.

Extractor notes: Single-step procedure; to reconnect, the manual defers to the VeSync app's add-a-device instructions.

### claim_c300s_part_filter_reset_button

- Claim: `claim_c300s_part_filter_reset_button`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `filter_reset_control_location`
- Verifier state: document status is PARTIAL

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": null,
    "source_id": "src_img_top_panel_2048"
  },
  "location_description": "The filter reset control is the Sleep Mode (moon icon) touch button on the top control panel, left side of the ring around the central On/Off button; the label under the moon icon reads 'RESET FILTER (3S)'. Press and hold 3 seconds to reset the Check Filter Indicator.",
  "part": "sleep_mode_button_filter_reset"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Sleep Mode Button • Turns Sleep Mode on (see page 9). • Press and hold for 3 seconds to reset the Check Filter Indicator.
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_spec_page_core300s`

```text
label under the moon icon reads "RESET FILTER (3S)"
```

Verifier: no verdict recorded.

Quote — binding 2, source `src_img_top_panel_2048`

```text
Top-down control panel photo showing the moon icon button with the 'RESET FILTER (3S)' label beneath it.
```

Verifier: `CANNOT_JUDGE` — Visual binding; text-only verification is unavailable.

Extractor notes: There is no dedicated reset button; the Sleep Mode button carries the secondary reset function (300S manual page 5 control diagram shows 'RESET FILTER (3S)' under the moon icon, visually verified). If the filter was changed before the indicator lit, press and hold for 3 seconds twice per manual page 13 case B. Third binding is an image (visual, mechanically unverifiable). Bounding box left null PENDING per anti-hallucination rule.

### claim_c300s_part_filter_cover

- Claim: `claim_c300s_part_filter_cover`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `filter_cover_location`
- Verifier state: document status is PARTIAL

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 5,
    "source_id": "src_manual_core300sp_us"
  },
  "location_description": "The filter cover is on the bottom of the unit (the unit is flipped over to access it); it twists counterclockwise to remove and clockwise to lock. Labeled R in the parts diagram.",
  "part": "filter_cover"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
R. Filter Cover
```

Verifier: no verdict recorded.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Flip the air purifier over. Twist the filter cover counterclockwise and remove it.
```

Verifier: no verdict recorded.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified). Official photo src_img_three_quarter_elevated_3000 shows the dark bottom cover edge.

### claim_c300s_part_airsight_sensor

- Claim: `claim_c300s_part_airsight_sensor`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `dust_sensor_location`
- Verifier state: document status is PARTIAL

Object

```json
{
  "diagram_binding": {
    "annotation_status": "PENDING",
    "bounding_box": null,
    "coordinate_system": "normalized",
    "page": 5,
    "source_id": "src_manual_core300sp_us"
  },
  "location_description": "The AirSight Plus Laser Dust Sensor sits behind slotted openings on the back of the housing, upper section (labeled P in the parts diagram, shown on the 'Back' view).",
  "part": "airsight_plus_laser_dust_sensor"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
P. AirSight™ Plus Laser Dust Sensor
```

Verifier: no verdict recorded.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified).

### claim_c300s_care_housing_cleaning

- Claim: `claim_c300s_care_housing_cleaning`
- Tier: `C1`
- Type/predicate: `CARE` / `housing_cleaning`
- Verifier state: document status is PARTIAL

Object

```json
{
  "method": "wipe with a soft, dry cloth; damp cloth if necessary, then immediately dry; unplug first; vacuum the inside",
  "restrictions": [
    "Do not clean with abrasive chemicals or flammable cleaning agents"
  ]
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
Wipe the outside of the air purifier with a soft, dry cloth. If necessary, wipe the housing with a damp cloth, then immediately dry.
```

Verifier: no verdict recorded.

Extractor notes: C1 assigned: everyday reversible wipe-down, not disassembly-level care.

### claim_c300s_care_storage

- Claim: `claim_c300s_care_storage`
- Tier: `C1`
- Type/predicate: `CARE` / `storage_procedure`
- Verifier state: document status is PARTIAL

Object

```json
{
  "method": "wrap both the air purifier and the filter in plastic packaging; store in a dry place",
  "reason": "avoid moisture damage"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
If not using the air purifier for an extended period of time, wrap both the air purifier and the filter in plastic packaging and store in a dry place to avoid moisture damage.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

### claim_c300s_policy_warranty

- Claim: `claim_c300s_policy_warranty`
- Tier: `C0`
- Type/predicate: `POLICY` / `warranty_period`
- Verifier state: document status is PARTIAL

Object

```json
{
  "provider": "Arovast Corporation",
  "unit": "years",
  "value": 2
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
the product shall be free from defects in material and workmanship for a period of 2 years from the date of original purchase
```

Verifier: no verdict recorded.

Extractor notes: 300S manual page 19 states the same 2-year term ('for a period of 2 years from the date of original purchase', visually verified).

### claim_c300s_state_standby

- Claim: `claim_c300s_state_standby`
- Tier: `C1`
- Type/predicate: `STATE` / `standby_mode_definition`
- Verifier state: document status is PARTIAL

Object

```json
{
  "description": "Turned off but plugged in; the laser dust sensor still detects surrounding air quality and reports to the VeSync app.",
  "state": "STANDBY"
}
```

Quote — binding 0, source `src_manual_core300sp_us`

```text
The air purifier is in Standby Mode when it is turned off, but plugged in.
```

Verifier: no verdict recorded.

Extractor notes: None recorded.

## 6. Open gaps (3)

### gap_300s_manual_binding_1

- Kind: `NOT_EXTRACTED`
- Waives: `[]`

Reason: The primary source src_manual_core300s_us (and its byte-near-identical copy src_manual_core300s_vesync) has no machine-readable text layer: pypdf and pdfminer.six both extract zero characters from all 24 pages (CID-encoded fonts without usable ToUnicode maps). Every fact was read visually from rendered page images and cross-checked, but a quote bound to these source_ids can never pass the validator's mechanical anti-fabrication gate. Claims are therefore bound to src_manual_core300sp_us (whose cover states 'Product Series: Core 300S series, Core 300S-P Series' — it is the official manual for both series) and to src_spec_page_core300s, with the corresponding src_manual_core300s_us page numbers preserved in extraction_notes. No checklist item or floor is left unmet by this substitution, so nothing is waived; this gap documents why the nominal primary source carries no bindings.

Closes when: An OCR text layer is added to the vault copy of the 300S manual (without altering the original artifact's hash record), or the validator gains a mode for verifying quotes against rendered page images.

### gap_hepa_efficiency_1

- Kind: `UNDERIVABLE`
- Waives: `[]`

Reason: The HEPA efficiency figure ('H13 True HEPA Filter ... Captures at least 99.97% of airborne particles 0.3 microns (um) in size', 300S manual page 11, visually verified) appears only in src_manual_core300s_us, which has no bindable text layer. The 300S-P manual drops the True HEPA/H13 wording entirely, and specs.md says only 'True HEPA main filter' with no efficiency number. No mechanically verifiable source in the vault states the 99.97% / 0.3 micron figure, so no claim was written for it.

Closes when: OCR text layer for the 300S manual, or a captured official spec page stating the filtration efficiency.

### gap_support_page_capture_1

- Kind: `SOURCE_MISSING`
- Waives: `[]`

Reason: src_support_vesync_filter_page (official VeSync store filter page confirming Core 300-RF compatibility and 6-8 month lifespan) has local_path null - no captured file exists in the vault. Claims that rely on its facts (claim_c300s_compat_filter_models, part of claim_c300s_care_filter_lifespan) bind instead to the specs.md transcription, which attributes those facts to the VeSync store.

Closes when: An HTML or text capture of the VeSync filter page is added to the vault with a local_path.

## 7. Auto-approved spot-audit (0)

None.
