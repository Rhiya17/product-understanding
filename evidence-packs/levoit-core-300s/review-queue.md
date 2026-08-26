# Review Queue — levoit-core-300s

Verification status: `COMPLETE`

Work top-to-bottom. Record human dispositions in `reviews.json`; do not edit claims or verifier verdicts.

## 1. MEANING_CHANGED alarms (43)

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

Verifier: `MEANING_CHANGED` — The translation adds specific signals (increased noise, decreased airflow, etc.) that trigger filter replacement, which are not mentioned in the original quote. The original only states replacement depends on usage frequency, not diagnostic symptoms.

Quote — binding 1, source `src_spec_page_core300s`

```text
Filter lifespan: 6–8 months; filter life tracked in the VeSync app
```

Verifier: `MEANING_CHANGED` — The translation adds unmentioned replacement signals (increased noise, decreased airflow, etc.) and implies a conditional trigger for replacement, while the quote only states a fixed lifespan tracked via app, with no mention of symptoms or user-triggered replacement.

Extractor notes: The 'Y ou' spacing in the first quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

### claim_c300s_care_housing_cleaning

- Claim: `claim_c300s_care_housing_cleaning`
- Tier: `C1`
- Type/predicate: `CARE` / `housing_cleaning`

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

Verifier: `MEANING_CHANGED` — The translation adds 'unplug first' and 'vacuum the inside', which are not mentioned in the quote. It also adds restrictions about abrasive chemicals and flammable agents, which the quote does not state. These are unauthorized additions that change the meaning.

Extractor notes: C1 assigned: everyday reversible wipe-down, not disassembly-level care.

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

Verifier: `MEANING_CHANGED` — Translation adds restrictions not in the quote: 'Do not clean the filter with water or other liquids' and 'Main filter: do not clean' — these are prohibitions absent in the source text.

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

Verifier: `MEANING_CHANGED` — The translation adds specific cleaning instructions (unplug, vacuum for 10 seconds) not present in the quote, which only states 'Clean the sensor every 3 months' without method details.

Extractor notes: None recorded.

### claim_c300s_care_storage

- Claim: `claim_c300s_care_storage`
- Tier: `C1`
- Type/predicate: `CARE` / `storage_procedure`

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

Verifier: `MEANING_CHANGED` — The translation omits the conditional 'If not using the air purifier for an extended period of time,' which is a critical condition in the original. Removing this condition makes the instruction appear mandatory rather than situational, altering the meaning.

Extractor notes: None recorded.

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

Verifier: `MEANING_CHANGED` — The translation adds 'counterpart':'Levoit Core 300 Series Original Filter (Core 300-RF)', which is not mentioned in the source quote and introduces an unverified product association.

Extractor notes: Underlying source is the official VeSync store filter page (src_support_vesync_filter_page), which has no local capture; the binding cites the vault's spec transcription that records it (see gaps.json gap_support_page_capture_1).

### claim_c300s_limit_room_size

- Claim: `claim_c300s_limit_room_size`
- Tier: `C1`
- Type/predicate: `LIMIT` / `effective_room_size`

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

Verifier: `MEANING_CHANGED` — The translation presents the room size limit as a single value (219 ft² / 20 m²) without indicating it is an upper bound ('smaller than'), and omits the conditional warning that effectiveness may decrease in larger rooms. This removes the cautionary context and implies the device is designed for exactly that size, altering the meaning.

Extractor notes: None recorded.

### claim_c300s_part_airsight_sensor

- Claim: `claim_c300s_part_airsight_sensor`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `dust_sensor_location`

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

Verifier: `MEANING_CHANGED` — The quote only labels a part as 'P. AirSight™ Plus Laser Dust Sensor' without specifying its location, while the translation adds detailed spatial information (behind slotted openings on the back, upper section, labeled P in diagram) not present in the quote.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified).

### claim_c300s_part_filter_cover

- Claim: `claim_c300s_part_filter_cover`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `filter_cover_location`

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

Verifier: `MEANING_CHANGED` — The quote only states 'R. Filter Cover' — a label or identifier — while the translation adds detailed location, orientation, removal/locking instructions, and diagram context not present in the original.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Flip the air purifier over. Twist the filter cover counterclockwise and remove it.
```

Verifier: `MEANING_CHANGED` — The translation adds that the filter cover 'twists clockwise to lock' and specifies it is 'labeled R in the parts diagram' — neither stated in the quote. Also, it implies the cover is always on the bottom (requiring flipping), while the quote only instructs to flip it for access, not that it’s permanently located there.

Extractor notes: Same diagram appears on 300S manual page 4 (visually verified). Official photo src_img_three_quarter_elevated_3000 shows the dark bottom cover edge.

### claim_c300s_part_filter_reset_button

- Claim: `claim_c300s_part_filter_reset_button`
- Tier: `C1`
- Type/predicate: `PART_LOCATION` / `filter_reset_control_location`

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

Verifier: `MEANING_CHANGED` — The translation falsely labels the Sleep Mode button as a 'filter reset control' with a dedicated 'RESET FILTER (3S)' label, while the quote only states that pressing and holding the Sleep Mode button for 3 seconds resets the Check Filter Indicator — no separate label or dedicated function is mentioned.

Quote — binding 1, source `src_spec_page_core300s`

```text
label under the moon icon reads "RESET FILTER (3S)"
```

Verifier: `MEANING_CHANGED` — The translation adds specific operational instructions ('Press and hold 3 seconds to reset the Check Filter Indicator') and locates the button relative to other controls ('left side of the ring around the central On/Off button'), which are not present in the exact quote and alter the meaning by introducing unverified context.

Quote — binding 2, source `src_img_top_panel_2048`

```text
Top-down control panel photo showing the moon icon button with the 'RESET FILTER (3S)' label beneath it.
```

Verifier: `CANNOT_JUDGE` — Visual binding; text-only verification is unavailable.

Extractor notes: There is no dedicated reset button; the Sleep Mode button carries the secondary reset function (300S manual page 5 control diagram shows 'RESET FILTER (3S)' under the moon icon, visually verified). If the filter was changed before the indicator lit, press and hold for 3 seconds twice per manual page 13 case B. Third binding is an image (visual, mechanically unverifiable). Bounding box left null PENDING per anti-hallucination rule.

### claim_c300s_policy_warranty

- Claim: `claim_c300s_policy_warranty`
- Tier: `C0`
- Type/predicate: `POLICY` / `warranty_period`

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

Verifier: `MEANING_CHANGED` — The translation adds 'provider: Arovast Corporation' which is not mentioned in the quote; also, it structures the warranty as a 'POLICY' with a specific object format, which introduces unquoted metadata and reifies the warranty beyond the original statement's scope.

Extractor notes: 300S manual page 19 states the same 2-year term ('for a period of 2 years from the date of original purchase', visually verified).

### claim_c300s_spec_aq_indicator

- Claim: `claim_c300s_spec_aq_indicator`
- Tier: `C1`
- Type/predicate: `SPEC` / `air_quality_indicator_mapping`

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

Verifier: `MEANING_CHANGED` — The translation incorrectly maps 'Sleep Mode' as the fan speed for 'Very Good' air quality, whereas the quote lists 'Sleep Mode' under 'Auto Mode' as a separate column — implying it is not a fan speed but a mode setting, making the mapping semantically inaccurate.

Quote — binding 1, source `src_img_aq_indicator_table`

```text
Official 'Air Quality Indicator Color Table' graphic showing the same color-to-quality-to-fan-speed mapping.
```

Verifier: `CANNOT_JUDGE` — Visual binding; text-only verification is unavailable.

Extractor notes: First quote is the manual's chart flattened to reading order by text extraction. Second binding is an image (visual, mechanically unverifiable).

### claim_c300s_spec_cadr

- Claim: `claim_c300s_spec_cadr`
- Tier: `C0`
- Type/predicate: `SPEC` / `clean_air_delivery_rate`

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

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 'CFM' as the unit for the metric value 240 m³/h, while the quote clearly pairs 141 with CFM and 240 with m³/h — swapping units misrepresents the specification.

Extractor notes: Also stated on pages 2 and 11 of src_manual_core300s_us ('CADR (CFM) 141 CFM / 240 m³/h'; 'Clean Air Delivery Rate of 141 cubic feet per minute (CFM), or 240 m³/h'), visually verified. The 300S-P manual spec table omits CADR; not treated as a conflict (absence, not disagreement).

### claim_c300s_spec_coverage

- Claim: `claim_c300s_spec_coverage`
- Tier: `C0`
- Type/predicate: `SPEC` / `room_coverage`

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

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 219 ft² as the 'ideal_room_size_ft2', but the quote specifies 219 ft² only at 4.8 ACH — not as the general ideal room size. It also adds 'ideal_room_size_m2':20, which is not mentioned or implied in the quote. The quote presents two distinct coverage scenarios, not a single ideal size.

Extractor notes: 300S manual page 2 states 'Ideal Room Size 219 ft² / 20 m²' and page 11 states 'an air change per hour of 5' (visually verified) — slight tension with the spec page's '4.8 ACH'; flagged for reviewer, not a 300S vs 300S-P revision conflict. See also claim_c300s_limit_room_size.

### claim_c300s_spec_dimensions

- Claim: `claim_c300s_spec_dimensions`
- Tier: `C0`
- Type/predicate: `SPEC` / `product_dimensions`

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

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 'unit':'in' to the entire object while also including metric values, implying inches are the primary unit — but the quote presents both units as equivalent alternatives, not a hierarchy. Also, the translation imposes structured fields (depth_in, height_in, width_in) not present in the quote, which is unstructured and does not specify which dimension corresponds to depth, height, or width.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Dimensions 8.7 × 8.7 × 14.2 in / 22 × 22 × 36 cm
```

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 'unit':'in' while also including metric values in the object, implying the unit applies to the entire object; the quote presents both units as parallel, not hierarchical, and the translation falsely suggests the metric values are secondary or derived from inches.

Extractor notes: Same value confirmed visually on page 2 of src_manual_core300s_us (no machine-readable text layer; see gaps.json gap_300s_manual_binding_1).

### claim_c300s_spec_filtration_stages

- Claim: `claim_c300s_spec_filtration_stages`
- Tier: `C0`
- Type/predicate: `SPEC` / `filtration_stages`

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

Verifier: `MEANING_CHANGED` — The translation omits 'ultra-fine' describing the nylon pre-filter, which is a material specification that affects performance; dropping this qualifier changes the meaning.

Extractor notes: 300S manual page 11 additionally states the H13 True HEPA filter 'Captures at least 99.97% of airborne particles 0.3 microns (μm) in size' — visually verified but not extractable as a bindable quote (see gaps.json gap_hepa_efficiency_1). The 300S-P manual drops the 'True HEPA'/H13 wording.

### claim_c300s_spec_model_name

- Claim: `claim_c300s_spec_model_name`
- Tier: `C0`
- Type/predicate: `SPEC` / `model_name`

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

Verifier: `MEANING_CHANGED` — The translation drops 'Product Name Smart Air Purifier' and only retains 'Core 300S' as the model name, omitting the full product identification and implying 'Core 300S' alone is the model name without context, which alters the original meaning.

Extractor notes: Even the current 300S-P manual's warranty table lists Model: Core 300S (spec table on its page 2 says 'Model Core 300S series'). Original 300S manual page 19 identically lists Model: Core 300S (visually verified).

### claim_c300s_spec_operating_conditions

- Claim: `claim_c300s_spec_operating_conditions`
- Tier: `C0`
- Type/predicate: `SPEC` / `operating_temperature_range`

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

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns '°F' as the unit for the metric value '-10 to 40 °C', creating a false association between the metric temperature and the imperial unit, which distorts the original meaning.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_spec_standby_power

- Claim: `claim_c300s_spec_standby_power`
- Tier: `C0`
- Type/predicate: `SPEC` / `standby_power`

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

Verifier: `MEANING_CHANGED` — The translation drops the 'Standby Power' label and converts it into a structured predicate 'standby_power', which may imply a different semantic framing; also, the value '< 2' is separated from its unit 'W' in structure, risking misinterpretation if parsed independently.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_spec_voice_control

- Claim: `claim_c300s_spec_voice_control`
- Tier: `C1`
- Type/predicate: `SPEC` / `voice_assistant_support`

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

Verifier: `MEANING_CHANGED` — The translation adds 'requires VeSync account', which is not mentioned in the quote. The quote only lists supported voice assistants without any condition or requirement.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Note: Y ou must create your own VeSync account to access voice assistants.
```

Verifier: `MEANING_CHANGED` — The quote states a general requirement to create a VeSync account to access voice assistants, without naming any specific assistants. The translation explicitly lists 'Amazon Alexa' and 'Google Assistant' as the supported assistants, which adds specific information not present in the original quote, thereby changing the meaning.

Extractor notes: The 'Y ou' spacing in the second quote is verbatim from the 300S-P manual's embedded text layer (font kerning artifact); the printed page reads 'You'.

### claim_c300s_spec_wifi_band

- Claim: `claim_c300s_spec_wifi_band`
- Tier: `C1`
- Type/predicate: `SPEC` / `wireless_connectivity`

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

Verifier: `MEANING_CHANGED` — The translation reduces the rich functionality list (remote control, schedules, timers, etc.) to only 'wireless_connectivity', omitting all features and implying a mere connectivity spec rather than feature set.

Quote — binding 1, source `src_manual_core300sp_us`

```text
During the setup process, you must be on a secure 2.4GHz WiFi network.
```

Verifier: `MEANING_CHANGED` — The translation omits the requirement that the user 'must be on a secure' network, which is a critical condition in the original quote. It also drops the context of 'during the setup process', changing the scope and timing of the requirement. The translation presents a static specification rather than a procedural constraint.

Extractor notes: None recorded.

### claim_c300s_state_standby

- Claim: `claim_c300s_state_standby`
- Tier: `C1`
- Type/predicate: `STATE` / `standby_mode_definition`

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

Verifier: `MEANING_CHANGED` — The translation adds that the laser dust sensor still detects air quality and reports to the VeSync app, which is not mentioned in the original quote and introduces new functional behavior not stated.

Extractor notes: None recorded.

### claim_c300s_step_app_setup_2

- Claim: `claim_c300s_step_app_setup_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation combines two distinct actions ('Open the VeSync app' and 'Log In or Sign Up') into a single compound action with 'and', implying they must be performed together as one step, whereas the original quote presents them as sequential or optional steps. This alters the procedural meaning.

Extractor notes: None recorded.

### claim_c300s_step_app_setup_3

- Claim: `claim_c300s_step_app_setup_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure: 'vesync_app_setup', step_number: 3) not present in the original quote, which only states a generic instruction without specifying any app name or step number. This constitutes an addition of information that alters the meaning by implying a specific procedure and context not stated in the source.

Extractor notes: None recorded.

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote, which alters meaning by implying system-specific categorization and targeting that the original does not state.

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

Verifier: `MEANING_CHANGED` — The translation adds 'target_parts':['filter_cartridge']', which is not mentioned in the quote. The original only refers to 'the filter' without specifying it as a 'filter_cartridge'. This addition introduces new information not present in the source, altering the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds '(cover should snap shut)', which is not present in the original quote and introduces a new condition not stated in the source.

Extractor notes: None recorded.

### claim_c300s_step_initial_setup_4

- Claim: `claim_c300s_step_initial_setup_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation adds 'away from anything that would block airflow,' which is not stated in the original quote. This introduces a new condition not present in the source, altering the meaning.

Extractor notes: None recorded.

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

Verifier: `MEANING_CHANGED` — The translation adds 'procedure: replace_filter' and 'target_parts: [power_cord, filter_cover]', which are not stated in the quote. The quote only describes actions without specifying the procedure name or target parts, thus introducing new information that changes the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds 'target_parts':['filter_cartridge']', which is not mentioned in the original quote. The original only says 'old filter' without specifying it is a 'filter_cartridge', thus introducing new, unsupported information.

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

Verifier: `MEANING_CHANGED` — The translation adds 'replace_filter' as the procedure and 'filter_compartment' as the target part, neither of which is mentioned in the original quote. The original only instructs to clean dust/hair with a vacuum hose and forbids liquids — it does not specify any filter replacement or target compartment, thus altering the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds structured metadata (procedure, step_number, target_parts) not present in the quote. The quote is a simple imperative instruction; the translation implies a formalized procedure with categorized parts and step numbering, which alters the meaning by introducing unmentioned structure and classification.

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

Verifier: `MEANING_CHANGED` — The translation adds unmentioned details: 'procedure: replace_filter', 'target_parts: [filter_cover, power_cord]'. The original quote does not specify replacing a filter or identify target parts; it only says to replace the cover and plug in the device. These additions change the meaning by implying specific components and a procedure not stated.

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

Verifier: `MEANING_CHANGED` — The translation adds 'procedure: replace_filter' and 'target_parts: [sleep_mode_button, check_filter_indicator]', which are not mentioned in the quote; the quote only states to reset the indicator without specifying a filter replacement or involving a sleep mode button.

Extractor notes: Reset detail is the reset_check_filter_indicator procedure (claims claim_c300s_step_reset_filter_1..4).

### claim_c300s_step_reset_filter_1

- Claim: `claim_c300s_step_reset_filter_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation adds 'reset_check_filter_indicator' and 'target_parts':['filter_cartridge'] which are not mentioned in the quote. The original only says to replace the filter and refers to page 14; it does not specify any indicator reset or part type.

Extractor notes: Case A of the manual's reset instructions (indicator lit red). Case B (filter changed before the indicator lit) is press-and-hold only; recorded in the PART_LOCATION claim's notes.

### claim_c300s_step_reset_filter_2

- Claim: `claim_c300s_step_reset_filter_2`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation adds procedural metadata (procedure: 'reset_check_filter_indicator', target_parts: ['on_off_button']) not present in the original quote, which only states 'Turn on the air purifier.' without specifying context, purpose, or physical controls.

Extractor notes: None recorded.

### claim_c300s_step_reset_filter_3

- Claim: `claim_c300s_step_reset_filter_3`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The translation adds 'the Sleep Mode button' as the target, which is not specified in the original quote; the original only says 'Press and hold for 3 seconds' without identifying any button or part.

Quote — binding 1, source `src_manual_core300sp_us`

```text
Reset the Check Filter Indicator by pressing and holding the Sleep Mode button for 3 seconds.
```

Verifier: `MEANING_CHANGED` — The translation incorrectly assigns 'step_number': 3, implying this is the third step in a sequence, which is not stated or implied in the original quote. The original only describes a single action without any step numbering or procedural context.

Extractor notes: The page 13 step shows the Sleep Mode moon icon between 'hold' and 'for'; the icon glyph does not survive text extraction. Page 6 quote names the button explicitly.

### claim_c300s_step_reset_filter_4

- Claim: `claim_c300s_step_reset_filter_4`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `MEANING_CHANGED` — The quote states the device 'will turn off when successfully reset' without specifying what turns off or confirming any indicator; the translation adds 'Confirm the Check Filter Indicator turns off', which introduces a specific component and an action (confirmation) not present in the original.

Extractor notes: The Check Filter icon precedes 'will turn off' on the printed page; the icon glyph does not survive text extraction.

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

Verifier: `MEANING_CHANGED` — The translation drops 'spray' from 'aerosol (spray) products', altering the specificity of the hazard and potentially excluding a subset of aerosol products that are spray-based, which the original explicitly includes.

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

Verifier: `MEANING_CHANGED` — The translation omits the causal phrase 'To reduce the risk of fire or electric shock,' which is critical context for the warning. Removing this changes the meaning by stripping the rationale for the restriction, making the warning appear arbitrary rather than safety-motivated.

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

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type: fire' which is not stated or implied in the exact quote. The original only specifies a distance requirement without attributing it to fire hazard, thus introducing new information that changes the meaning.

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

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type': 'electric_shock', which is not mentioned or implied in the original quote; this introduces new safety information not present in the source.

Extractor notes: Quote is verbatim from the 300S-P manual's embedded text layer, including its missing/misplaced spaces (text-layer artifact of that PDF). The original 300S manual page 3 reads cleanly: 'Always unplug the air purifier before servicing (such as changing the filter).' (visually verified).

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

Verifier: `MEANING_CHANGED` — The translation adds 'hazard_type':'electric_shock', which is not stated or implied in the original quote. The original only gives a safety instruction without specifying the hazard type, so this addition changes the meaning by introducing unmentioned information.

Extractor notes: None recorded.

## 2. Unresolved conflict pairs (0)

None.

## 3. C3 claims (1)

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

Verifier: `ENTAILED` — The translation accurately preserves the core warning: do not use without removing the plastic wrap, as it prevents air filtering and may cause overheating and fire hazard. The structured format does not alter meaning; 'hazard_type': 'fire' is a faithful extraction of 'causing a fire hazard'. No added, dropped, or altered qualifiers, numbers, units, or conditions.

Extractor notes: C3 assigned per work order rule: all safety warnings from the manuals.

## 4. C2 claims (0)

None.

## 5. Unresolved verifier — C0/C1 (0)

None.

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

## 7. Batch-eligible C0/C1 spot-audit (5)

Spot-audit sample: `5` of `5` eligible claims. The sample is the five lowest SHA-256 ranks of `review-completion-v1\0<product>\0<claim_id>`, so it is stable and reproducible.

A clean sample may be confirmed as one explicit human batch decision. A failed sample removes batch eligibility; review every batch member individually.

Batch members

- `claim_c300s_spec_power_supply`
- `claim_c300s_spec_package_contents`
- `claim_c300s_limit_humidity`
- `claim_c300s_step_app_setup_1`
- `claim_c300s_step_wifi_reset_1`

Sample details

### claim_c300s_spec_power_supply

- Claim: `claim_c300s_spec_power_supply`
- Tier: `C0`
- Type/predicate: `SPEC` / `power_supply`

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

Verifier: `ENTAILED` — The translation accurately preserves the voltage (AC 120V) and frequency (60Hz) from the quote, with no added, dropped, or altered qualifiers, numbers, or units.

Extractor notes: Identical value visually verified on page 2 of src_manual_core300s_us.

### claim_c300s_step_app_setup_1

- Claim: `claim_c300s_step_app_setup_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `ENTAILED` — The translation accurately preserves the original instruction: downloading the VeSync app via QR code or app store search, with no added, dropped, or altered qualifiers, numbers, units, or actors.

Extractor notes: None recorded.

### claim_c300s_step_wifi_reset_1

- Claim: `claim_c300s_step_wifi_reset_1`
- Tier: `C1`
- Type/predicate: `STEP` / `procedure_step`

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: it preserves the action (press and hold for 15 seconds until Wi-Fi indicator turns off), the consequence (restores default settings and disconnects from VeSync app), and the target parts (On/Off button, Wi-Fi indicator). No meaning-altering changes in number, unit, direction, actor, condition, or qualifiers are present.

Extractor notes: Single-step procedure; to reconnect, the manual defers to the VeSync app's add-a-device instructions.

### claim_c300s_limit_humidity

- Claim: `claim_c300s_limit_humidity`
- Tier: `C1`
- Type/predicate: `LIMIT` / `maximum_operating_humidity`

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

Verifier: `ENTAILED` — The translation accurately reflects the exact quote: 'Humidity: < 85% RH' is correctly parsed as a maximum operating humidity limit with value '< 85' and unit '% RH'. No meaning is altered, added, or dropped.

Extractor notes: 300S manual page 11 (Humidity section) adds that above this level 'the surface of the filter may become moldy' (visually verified).

### claim_c300s_spec_package_contents

- Claim: `claim_c300s_spec_package_contents`
- Tier: `C0`
- Type/predicate: `SPEC` / `package_contents`

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

Verifier: `ENTAILED` — The translation accurately lists the exact same items with identical quantities and descriptions as the quote; no meaning is altered.

Extractor notes: Original 300S manual page 2 lists the same four items but names the filter 'True HEPA 3-Stage Original Filter (Pre-Installed)' (visually verified). Wording difference only; item count identical, so not recorded as a value conflict.
