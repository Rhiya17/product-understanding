#!/usr/bin/env python3
"""Append corrected replacements for the 2026-08-29 unpublished-claim pass.

Claims are immutable in this repository.  This script therefore appends new
claim IDs, records a machine-readable replacement manifest, and remaps media
references for procedures that must be replaced as complete contiguous sets.
It never edits or removes an existing claim.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "evidence-packs"
RUN_PATH = ROOT / "system" / "runs" / "unpublished-repair-20260829.json"
STAMP = "20260829"
REPAIR_EXTRACTOR = "codex-expert-repair-v1"


def binding(source_id: str, page: int | None, quote: str) -> dict:
    return {"source_id": source_id, "page": page, "quote": quote}


def load(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def repaired_id(claim_id: str) -> str:
    return f"{claim_id}_repair_{STAMP}"


def clone_claim(
    source: dict,
    *,
    object_value: dict | None = None,
    bindings: list[dict] | None = None,
    procedure: str | None = None,
) -> dict:
    claim = copy.deepcopy(source)
    old_id = claim["claim_id"]
    claim["claim_id"] = repaired_id(old_id)
    claim["version"] = 1
    claim["status"] = "CANDIDATE"
    claim["object"] = copy.deepcopy(object_value if object_value is not None else source["object"])
    if procedure is not None:
        claim["object"]["procedure"] = procedure
    claim["source_bindings"] = copy.deepcopy(bindings if bindings is not None else source["source_bindings"])
    claim["extractor"] = REPAIR_EXTRACTOR
    claim["extracted_at"] = "2026-08-29"
    claim["extraction_notes"] = (
        f"Append-only repair superseding {old_id}. Corrected after owner-directed "
        "expert review of the complete authoritative source context; the protected "
        "original claim remains immutable."
    )
    return claim


def append_binding(bindings: list[dict], *items: dict) -> list[dict]:
    result = copy.deepcopy(bindings)
    for item in items:
        if item not in result:
            result.append(item)
    return result


def apple_rules(by_id: dict[str, dict]) -> list[dict]:
    repairs = []
    repairs.append(clone_claim(
        by_id["claim_mba_spec_fast_charge"],
        object_value={
            "capability": "Fast charge up to 50 percent in around 30 minutes",
            "adapter": "optional 70W USB-C Power Adapter",
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_mba_spec_memory_options"],
        object_value={
            "configurations": [
                {"memory_gb": 16, "configurable_to_gb": [24]},
                {"memory_gb": 8, "configurable_to_gb": [16, 24]},
            ]
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_mba_spec_newest_compatible_os"],
        object_value={"value": "macOS Tahoe 26"},
    ))
    magsafe = copy.deepcopy(by_id["claim_mba_part_magsafe_port"]["object"])
    magsafe["location_description"] = (
        "One MagSafe 3 charging port on the left side of the laptop, in the "
        "front-most position toward the hinge end of the left edge."
    )
    repairs.append(clone_claim(by_id["claim_mba_part_magsafe_port"], object_value=magsafe))

    charge_proc = f"charge_via_magsafe_verified_{STAMP}"
    charge = copy.deepcopy(by_id["claim_mba_step_charge_1"]["object"])
    charge["action"] = (
        "Plug in the included USB-C Power Adapter; the indicator light glows amber "
        "when charging is needed and green when fully charged."
    )
    repairs.append(clone_claim(
        by_id["claim_mba_step_charge_1"], object_value=charge, procedure=charge_proc
    ))

    connect_proc = f"connect_wired_or_bluetooth_device_verified_{STAMP}"
    for number in (1, 2, 3):
        old = by_id[f"claim_mba_step_connection_method_{number}"]
        obj = copy.deepcopy(old["object"])
        bindings = old["source_bindings"]
        if number == 2:
            obj["action"] = (
                "Connect stereo headphones or external speakers to the 3.5 mm "
                "headphone jack on the right side; use either Thunderbolt / USB 4 "
                "port on the left for compatible USB-C or Thunderbolt accessories."
            )
            bindings = [
                binding(
                    "src_ports_guide_tour",
                    None,
                    "1x 3.5 mm headphone jack (the only port on the right side)",
                ),
                binding(
                    "src_ports_guide_tour",
                    None,
                    "2x Thunderbolt / USB 4 ports (both on the left side, next to MagSafe)",
                ),
                binding(
                    "src_ports_guide_tour",
                    None,
                    "**Thunderbolt / USB 4 ports**: Charge the computer, transfer data at Thunderbolt 3 or USB 4 speeds (up to 40 Gbit/s), charge devices, connect a display or projector.",
                ),
                binding(
                    "src_ports_guide_tour",
                    None,
                    "**3.5 mm headphone jack**: Stereo headphones or external speakers; supports high-impedance headphones without a separate DAC or amplifier.",
                ),
            ]
        repairs.append(clone_claim(old, object_value=obj, bindings=bindings, procedure=connect_proc))
    return repairs


def bose_rules(by_id: dict[str, dict]) -> list[dict]:
    repairs = []
    additions = {
        "claim_bqcu2_full_charge_time_1": [
            binding("src_owners_guide_en", 36, "NOTE: Charging is slower when the headphones are in use.")
        ],
        "claim_bqcu2_bluetooth_device_name_1": [
            binding("src_owners_guide_en", 28, "NOTE: Look for the name you entered for your headphones in the Bose app.")
        ],
        "claim_bqcu2_aptx_adaptive_codec_1": [
            binding("src_owners_guide_en", 32, "T o experience Snapdragon Sound, you need a Snapdragon Sound-certified device, such as a compatible Android device.")
        ],
        "claim_bqcu2_part_serial_number_1": [
            binding("src_owners_guide_en", 45, "The serial number and regulatory markings are located inside the earcups under the inner fabric."),
            binding("src_owners_guide_en", 45, "On the earcup, gently pull one area of the cushion away from the earcup until all tabs around the inside rim of the earcup release."),
            binding("src_owners_guide_en", 45, "Grab the upper edge of the fabric and gently peel it away until the information is displayed."),
        ],
        "claim_bqcu2_warning_vehicle_1": [
            binding("src_safety_instructions_ml", 1, "Stop using your headphones immediately if they interfere with your ability to remain attentive or if they interfere with your ability to hear surrounding sounds, including alarms and warning signals, while operating a vehicle.")
        ],
        "claim_bqcu2_care_firmware_update_1": [
            binding("src_owners_guide_en", 44, "You can also update the headphones using the Bose updater website. On your computer, visit: btu.Bose.com and follow the on-screen instructions.")
        ],
        "claim_bqcu2_state_default_power_on_mode_1": [
            binding("src_owners_guide_en", 22, "NOTE: The headphones power on with the last settings used.")
        ],
        "claim_bqcu2_state_lay_flat_disconnect_1": [
            binding("src_owners_guide_en", 16, "If they are removed from your head and left in any other orientation, they disconnect from your devices after 10 minutes.")
        ],
        "claim_bqcu2_state_auto_sleep_1": [
            binding("src_owners_guide_en", 16, "T o wake the headphones, place them on your head or press and release the Bluetooth/Power button.")
        ],
        "claim_bqcu2_compat_fast_pair_android_1": [
            binding("src_owners_guide_en", 31, "Your Android device must have the Bluetooth and Location features enabled.")
        ],
        "claim_bqcu2_compat_bose_speakers_1": [
            binding("src_owners_guide_en", 39, "Using SimpleSync technology, you can connect the headphones to a Bose Smart Soundbar or Bose Smart Speaker for a personal listening experience."),
            binding("src_owners_guide_en", 39, "Popular compatible products include:"),
            binding("src_owners_guide_en", 39, "Bose Smart Ultra Soundbar"),
            binding("src_owners_guide_en", 39, "Bose Smart Soundbar"),
            binding("src_owners_guide_en", 39, "Bose Portable Smart Speaker/Bose Portable Home Speaker"),
        ],
    }
    for claim_id in (
        "claim_bqcu2_full_charge_time_1",
        "claim_bqcu2_bluetooth_device_name_1",
        "claim_bqcu2_aptx_adaptive_codec_1",
        "claim_bqcu2_part_serial_number_1",
        "claim_bqcu2_warning_vehicle_1",
        "claim_bqcu2_care_firmware_update_1",
        "claim_bqcu2_state_default_power_on_mode_1",
        "claim_bqcu2_state_lay_flat_disconnect_1",
        "claim_bqcu2_state_auto_sleep_1",
        "claim_bqcu2_compat_fast_pair_android_1",
        "claim_bqcu2_compat_bose_speakers_1",
    ):
        old = by_id[claim_id]
        repairs.append(clone_claim(
            old,
            bindings=append_binding(old["source_bindings"], *additions[claim_id]),
        ))

    range_obj = copy.deepcopy(by_id["claim_bqcu2_bluetooth_range_1"]["object"])
    range_obj["condition"] = "devices are within range and powered on"
    repairs.append(clone_claim(by_id["claim_bqcu2_bluetooth_range_1"], object_value=range_obj))

    aux = copy.deepcopy(by_id["claim_bqcu2_part_aux_port_1"]["object"])
    aux["location_description"] = (
        "The 2.5 mm AUX audio port is shown in the page 13 controls diagram on "
        "the earcup with the USB-C port and status light."
    )
    repairs.append(clone_claim(
        by_id["claim_bqcu2_part_aux_port_1"],
        object_value=aux,
        bindings=[
            binding("src_owners_guide_en", 13, "2.5 mm AUX audio port"),
            binding("src_owners_guide_en", 13, "USB-C® port"),
            binding("src_owners_guide_en", 13, "Status light"),
        ],
    ))

    pairing_proc = f"bluetooth_pairing_verified_{STAMP}"
    for number in (1, 2, 3):
        old = by_id[f"claim_bqcu2_step_pairing_{number}"]
        bindings = old["source_bindings"]
        if number == 3:
            bindings = append_binding(
                bindings,
                binding("src_owners_guide_en", 28, "NOTE: Look for the name you entered for your headphones in the Bose app. If you didn’t name your headphones, the default name appears."),
                binding("src_owners_guide_en", 28, "BOSE QC ULTRA 2 HP"),
            )
        repairs.append(clone_claim(old, bindings=bindings, procedure=pairing_proc))
    return repairs


def ready2jet_rules(by_id: dict[str, dict]) -> list[dict]:
    repairs = []
    belly = copy.deepcopy(by_id["claim_r2j_part_belly_bar"]["object"])
    belly["location_description"] = "Attaches to the belly bar mounts."
    repairs.append(clone_claim(by_id["claim_r2j_part_belly_bar"], object_value=belly))

    thumb = copy.deepcopy(by_id["claim_r2j_part_thumb_switch"]["object"])
    thumb["location_description"] = (
        "Shown as control (a) in the stroller folding diagram and slid before "
        "the handle lever is squeezed."
    )
    repairs.append(clone_claim(
        by_id["claim_r2j_part_thumb_switch"],
        object_value=thumb,
        bindings=[binding("src_r2j_manual_v1", 34, "To fold stroller: (a) slide thumb switch; (b) squeeze handle lever")],
    ))

    lever = copy.deepcopy(by_id["claim_r2j_part_handle_lever"]["object"])
    lever["location_description"] = (
        "Shown as control (b) in the stroller folding diagram and squeezed after "
        "the thumb switch is slid."
    )
    repairs.append(clone_claim(
        by_id["claim_r2j_part_handle_lever"],
        object_value=lever,
        bindings=[binding("src_r2j_manual_v1", 34, "To fold stroller: (a) slide thumb switch; (b) squeeze handle lever")],
    ))

    cup = {
        "applies_to": "cup holder",
        "rule": "Do not place more than 1 lb (0.45 kg) in the cup holder.",
        "value": 1,
        "unit": "lb",
    }
    repairs.append(clone_claim(by_id["claim_r2j_limit_cup_holder_weight"], object_value=cup))

    zip_obj = copy.deepcopy(by_id["claim_r2j_warning_zip_tie"]["object"])
    zip_obj["description"] = "Remove and immediately discard the zip tie."
    repairs.append(clone_claim(by_id["claim_r2j_warning_zip_tie"], object_value=zip_obj))

    compat = by_id["claim_r2j_compat_graco_infant_car_seats"]
    repairs.append(clone_claim(
        compat,
        bindings=append_binding(
            compat["source_bindings"],
            binding("src_r2j_manual_v1", 5, "For additional questions or for more information on compatibility please call Graco’s customer service number: 1-800-345-4109 or scan for compatibility."),
        ),
    ))

    wet = {
        "condition": "if the stroller becomes wet",
        "method": "open the canopy and allow the stroller to dry thoroughly before storing",
    }
    repairs.append(clone_claim(by_id["claim_r2j_care_wet_drying"], object_value=wet))
    return repairs


def snugride_compatibility_claim(old: dict) -> dict:
    obj = copy.deepcopy(old["object"])
    obj.pop("relationship", None)
    if old["claim_id"] == "claim_srl_compat_click_connect_requirement":
        obj = {
            "compatible": True,
            "counterpart": "strollers in the Graco Click Connect travel system",
            "counterpart_type": "stroller_system",
            "restriction": (
                "Use only with strollers that are part of the Graco Click Connect "
                "travel system; never use with another manufacturer's stroller."
            ),
        }
        bindings = [
            binding("src_snugride_manual_en_v1", 60, "USE ONLY WITH STROLLERS THAT ARE PART OF THE GRACO CLICK CONNECT TRAVEL SYSTEM."),
            binding("src_snugride_manual_en_v1", 60, "NEVER use a Graco infant carrier with any other manufacturer’s strollers. This can result in serious injury or death."),
        ]
        return clone_claim(old, object_value=obj, bindings=bindings)

    is_base = old["claim_id"].startswith("claim_srl_compat_base_")
    header = (
        binding("src_compatibility_chart_apr2026", 3, "Graco® Infant Car Seats & Base Compatibility List")
        if is_base
        else binding("src_compatibility_chart_apr2026", 1, "Graco® Strollers & Infant Car Seats Compatibility List")
    )
    family = (
        binding("src_compatibility_chart_apr2026", 3, "SnugRide® Infant Car Seats (includes SnugRide® Lite family, SnugRide® Snugfit® & SnugRide® Snuglock® families)")
        if is_base
        else binding("src_compatibility_chart_apr2026", 1, "SnugRide® Infant Car Seats (includes SnugRide® Lite family, SnugRide® Snugfit® & SnugRide® Snuglock® families)")
    )
    return clone_claim(
        old,
        object_value=obj,
        bindings=[header, family, *copy.deepcopy(old["source_bindings"])],
    )


def snugride_rules(by_id: dict[str, dict]) -> list[dict]:
    repairs = []
    max_height = {
        "rule": "For rear-facing use, child height must be 32 in (81 cm) or less.",
        "value": 32,
        "unit": "in",
    }
    repairs.append(clone_claim(by_id["claim_srl_limit_max_height"], object_value=max_height))

    body = {
        "rule": "The body support can only be used for infants 12 lb (5 kg) or less.",
        "value": 12,
        "unit": "lb",
    }
    repairs.append(clone_claim(by_id["claim_srl_limit_body_support_max_weight"], object_value=body))

    expiration = by_id["claim_srl_limit_expiration_7yr"]
    repairs.append(clone_claim(
        expiration,
        bindings=append_binding(
            expiration["source_bindings"],
            binding("src_snugride_manual_en_v1", 10, "Look for date of manufacture label on back of the car seat."),
        ),
    ))

    conflict = {
        "status": "source_conflict",
        "specification_table_lb": 7.5,
        "marketing_copy_lb": 7.2,
        "rule": "The current Graco product page conflicts internally; do not present a single carrier-only weight without qualification.",
    }
    repairs.append(clone_claim(
        by_id["claim_srl_spec_carrier_weight"],
        object_value=conflict,
        bindings=[
            binding("src_pdp_specs_page", None, "| Carrier weight without base | 7.5 lb (spec table); marketing copy says \"weighs just 7.2 lb\" |"),
        ],
    ))

    aircraft = by_id["claim_srl_spec_aircraft_certified"]
    repairs.append(clone_claim(
        aircraft,
        bindings=append_binding(
            aircraft["source_bindings"],
            binding("src_snugride_manual_en_v1", 10, "Follow the instructions for vehicle installation. See sections 3-C, 3-D and 6-D Lap Belt Installation."),
        ),
    ))

    harness_part = copy.deepcopy(by_id["claim_srl_part_harness_release_lever"]["object"])
    harness_part["location_description"] = "Under the seat pad."
    repairs.append(clone_claim(
        by_id["claim_srl_part_harness_release_lever"], object_value=harness_part
    ))
    belt_part = copy.deepcopy(by_id["claim_srl_part_rearfacing_belt_path"]["object"])
    belt_part["location_description"] = (
        "Rear-facing belt path on the carrier when it is used without the base."
    )
    repairs.append(clone_claim(
        by_id["claim_srl_part_rearfacing_belt_path"], object_value=belt_part
    ))

    for old in by_id.values():
        if old["claim_id"].startswith("claim_srl_compat_"):
            repairs.append(snugride_compatibility_claim(old))

    procedure_specs = {
        "install_base_lower_anchor": {
            6: [binding("src_snugride_manual_en_v1", 28, "Do not attach the hook upside down.")],
            8: [binding("src_snugride_manual_en_v1", 29, "If the base moves less than 1” (2.5 cm), it is tight enough.")],
            9: [binding("src_snugride_manual_en_v1", 30, "Test to make sure the car seat is attached by pulling up on the front corners of car seat.")],
        },
        "install_base_seat_belt": {
            5: [binding("src_snugride_manual_en_v1", 37, "Slowly pull out on the belt and it should be locked. If not, review your car’s owner manual and section 6-D.")],
            7: [binding("src_snugride_manual_en_v1", 38, "If the base moves less than 1” (2.5 cm), it is tight enough.")],
            8: [binding("src_snugride_manual_en_v1", 38, "Test to make sure the car seat is attached by pulling up on the front corners of car seat.")],
        },
        "install_carrier_seat_belt": {
            3: [binding("src_snugride_manual_en_v1", 42, "Slowly pull out on the belt and it should be locked. If not, review your car’s owner manual and section 6-D.")],
            5: [binding("src_snugride_manual_en_v1", 43, "If the car seat moves less than 1” (2.5 cm), it is tight enough.")],
            6: [binding("src_snugride_manual_en_v1", 44, "Check the level line with child in the child restraint when making sure the line is level with the ground.")],
        },
    }
    for procedure, additions in procedure_specs.items():
        members = sorted(
            (c for c in by_id.values() if c.get("type") == "STEP" and c.get("object", {}).get("procedure") == procedure),
            key=lambda c: c["object"]["step_number"],
        )
        new_procedure = f"{procedure}_verified_{STAMP}"
        for old in members:
            number = old["object"]["step_number"]
            bindings = append_binding(old["source_bindings"], *additions.get(number, []))
            repairs.append(clone_claim(old, bindings=bindings, procedure=new_procedure))

    warning_additions = {
        "claim_srl_warning_airbag": binding("src_snugride_manual_en_v1", 11, "If an air bag inflates, it can hit the child and car seat with great force and cause serious injury or death to your child."),
        "claim_srl_warning_bulky_clothing": binding("src_snugride_manual_en_v1", 47, "To keep child warm, buckle your child in the car seat and place a blanket around the child or place the child’s coat on backwards after buckling in."),
        "claim_srl_warning_strings_cords": binding("src_snugride_manual_en_v1", 59, "DO NOT hang strings on or over the carrier. DO NOT attach strings to toys."),
    }
    for claim_id, extra in warning_additions.items():
        old = by_id[claim_id]
        repairs.append(clone_claim(old, bindings=append_binding(old["source_bindings"], extra)))

    buckle = by_id["claim_srl_care_buckle"]
    repairs.append(clone_claim(
        buckle,
        bindings=append_binding(
            buckle["source_bindings"],
            binding("src_snugride_manual_en_v1", 78, "Shake out excess water and allow to air dry. Repeat steps as needed until it fastens with a click."),
        ),
    ))

    harness_limit = copy.deepcopy(by_id["claim_srl_limit_harness_strap_height"]["object"])
    harness_limit["rule"] = "Harness straps must be at or just below the child’s shoulders."
    repairs.append(clone_claim(
        by_id["claim_srl_limit_harness_strap_height"], object_value=harness_limit
    ))
    return repairs


def levoit_rules(by_id: dict[str, dict]) -> tuple[list[dict], list[str]]:
    repairs = []
    obsolete = ["claim_c300s_spec_weight_300s"]
    repairs.append(clone_claim(
        by_id["claim_c300s_spec_dimensions"],
        object_value={
            "imperial": {"width": 8.7, "depth": 8.7, "height": 14.2, "unit": "in"},
            "metric": {"width": 22, "depth": 22, "height": 36, "unit": "cm"},
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_c300s_spec_weight_300sp"],
        object_value={
            "imperial": {"value": 7.48, "unit": "lb"},
            "metric": {"value": 3.393, "unit": "kg"},
            "revision": "Core 300S-P",
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_c300s_spec_coverage"],
        object_value={
            "coverage": [
                {"area_ft2": 1051, "air_changes_per_hour": 1},
                {"area_ft2": 219, "air_changes_per_hour": 4.8},
            ]
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_c300s_spec_operating_conditions"],
        object_value={
            "imperial": {"minimum": 14, "maximum": 104, "unit": "°F"},
            "metric": {"minimum": -10, "maximum": 40, "unit": "°C"},
        },
    ))
    repairs.append(clone_claim(
        by_id["claim_c300s_limit_room_size"],
        object_value={
            "rule": "For poor air-purification troubleshooting, make sure the room is smaller than 219 ft² / 20 m²; the purifier may be less effective in larger rooms.",
            "imperial_upper_bound": {"value": 219, "unit": "ft²"},
            "metric_upper_bound": {"value": 20, "unit": "m²"},
        },
    ))

    init_proc = f"initial_setup_unwrap_filter_verified_{STAMP}"
    for number in (1, 2, 3, 4):
        old = by_id[f"claim_c300s_step_initial_setup_{number}"]
        bindings = old["source_bindings"]
        if number == 3:
            bindings = append_binding(bindings, binding("src_manual_core300sp_us", 7, "cover should snap shut"))
        if number == 4:
            bindings = append_binding(bindings, binding("src_manual_core300sp_us", 7, "Keep away from anything that would block airflow, such as curtains."))
        repairs.append(clone_claim(old, bindings=bindings, procedure=init_proc))

    cover = by_id["claim_c300s_part_filter_cover"]
    repairs.append(clone_claim(
        cover,
        bindings=append_binding(
            cover["source_bindings"],
            binding("src_manual_core300sp_us", 7, "Replace the filter cover and twist clockwise to lock."),
        ),
    ))
    sensor_obj = copy.deepcopy(by_id["claim_c300s_part_airsight_sensor"]["object"])
    sensor_obj["location_description"] = (
        "Labeled P in the parts diagram and shown on the Back view of the purifier."
    )
    repairs.append(clone_claim(
        by_id["claim_c300s_part_airsight_sensor"],
        object_value=sensor_obj,
        bindings=[
            binding("src_manual_core300sp_us", 5, "P. AirSight™ Plus Laser Dust Sensor"),
            binding("src_manual_core300sp_us", 5, "Front, upside downBack"),
        ],
    ))

    prefilter = by_id["claim_c300s_care_prefilter_cleaning"]
    repairs.append(clone_claim(
        prefilter,
        bindings=append_binding(
            prefilter["source_bindings"],
            binding("src_manual_core300sp_us", 13, "Do not clean the filter with water or other liquids."),
            binding("src_manual_core300sp_us", 13, "Main Filter Do not clean"),
        ),
    ))
    housing = by_id["claim_c300s_care_housing_cleaning"]
    repairs.append(clone_claim(
        housing,
        bindings=append_binding(
            housing["source_bindings"],
            binding("src_manual_core300sp_us", 13, "Unplug before cleaning."),
            binding("src_manual_core300sp_us", 13, "Vacuum the inside of the air purifier."),
            binding("src_manual_core300sp_us", 13, "Do not clean with abrasive chemicals or flammable cleaning agents."),
        ),
    ))
    sensor = by_id["claim_c300s_care_sensor_cleaning"]
    repairs.append(clone_claim(
        sensor,
        bindings=append_binding(
            sensor["source_bindings"],
            binding("src_manual_core300sp_us", 14, "1. Unplug the air purifier."),
            binding("src_manual_core300sp_us", 14, "2. Place the end of a vacuum cleaner over the sensor openings."),
            binding("src_manual_core300sp_us", 14, "3. Turn the vacuum on for at least 10 seconds to clean out dust."),
        ),
    ))
    lifespan = by_id["claim_c300s_care_filter_lifespan"]
    repairs.append(clone_claim(
        lifespan,
        bindings=append_binding(
            lifespan["source_bindings"],
            binding("src_manual_core300sp_us", 14, "Y ou may need to replace your filter if you notice:"),
            binding("src_manual_core300sp_us", 14, "Increased noise when the air purifier is on"),
            binding("src_manual_core300sp_us", 14, "Decreased airflow"),
            binding("src_manual_core300sp_us", 14, "Unusual odors"),
            binding("src_manual_core300sp_us", 14, "A visibly clogged filter"),
        ),
    ))
    standby = by_id["claim_c300s_state_standby"]
    repairs.append(clone_claim(
        standby,
        bindings=append_binding(
            standby["source_bindings"],
            binding("src_manual_core300sp_us", 9, "The laser dust sensor will still detect the surrounding air quality and give you updates in the VeSync app."),
        ),
    ))
    return repairs, obsolete


def replace_ids(value, mapping: dict[str, str]):
    if isinstance(value, dict):
        return {key: replace_ids(item, mapping) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_ids(item, mapping) for item in value]
    if isinstance(value, str):
        return mapping.get(value, value)
    return value


def main() -> None:
    all_repairs: list[dict] = []
    old_to_new: dict[str, str] = {}
    obsolete: list[dict] = []

    builders = {
        "apple-macbook-air-13-m3": apple_rules,
        "bose-qc-ultra-headphones": bose_rules,
        "graco-ready2jet-2212125": ready2jet_rules,
        "graco-snugride-35-lite-lx": snugride_rules,
    }

    pack_repairs: dict[str, list[dict]] = {}
    for pack_name, builder in builders.items():
        claims = load(PACKS / pack_name / "claims.json")
        by_id = {
            claim["claim_id"]: claim
            for claim in claims
            if claim.get("extractor") != REPAIR_EXTRACTOR
        }
        pack_repairs[pack_name] = builder(by_id)

    levoit_name = "levoit-core-300s"
    levoit_claims = load(PACKS / levoit_name / "claims.json")
    levoit_by_id = {
        claim["claim_id"]: claim
        for claim in levoit_claims
        if claim.get("extractor") != REPAIR_EXTRACTOR
    }
    levoit_repairs, levoit_obsolete = levoit_rules(levoit_by_id)
    pack_repairs[levoit_name] = levoit_repairs
    obsolete.extend({"product": levoit_name, "claim_id": cid} for cid in levoit_obsolete)

    for pack_name, repairs in pack_repairs.items():
        path = PACKS / pack_name / "claims.json"
        claims = load(path)
        existing = {claim["claim_id"] for claim in claims}
        positions = {claim["claim_id"]: index for index, claim in enumerate(claims)}
        for claim in repairs:
            if claim["claim_id"] in existing:
                current = claims[positions[claim["claim_id"]]]
                if current.get("extractor") != REPAIR_EXTRACTOR:
                    raise ValueError(
                        f"Refusing to overwrite non-repair claim {claim['claim_id']}"
                    )
                claims[positions[claim["claim_id"]]] = claim
            else:
                claims.append(claim)
                existing.add(claim["claim_id"])
                positions[claim["claim_id"]] = len(claims) - 1
            old_id = claim["extraction_notes"].split("superseding ", 1)[1].split(".", 1)[0]
            old_to_new[old_id] = claim["claim_id"]
            all_repairs.append({
                "product": pack_name,
                "old_claim_id": old_id,
                "new_claim_id": claim["claim_id"],
            })
        write(path, claims)

        # The prior verifier run cannot truthfully remain COMPLETE after new
        # claim/binding pairs are appended. Preserve every recorded verdict,
        # but mark its document coverage PARTIAL until an independent rerun is
        # possible.
        verdicts_path = PACKS / pack_name / "verdicts.json"
        if verdicts_path.exists():
            verdicts = load(verdicts_path)
            coverage_reason = (
                "Claims appended by the 2026-08-29 unpublished repair pass "
                "have complete exact-source and human review but no new "
                "independent verifier verdict because FAL_KEY is unavailable; "
                "all earlier verifier verdict entries remain unchanged."
            )
            if coverage_reason not in verdicts.get("reason", ""):
                previous_reason = verdicts.get("reason", "").strip()
                verdicts["reason"] = " ".join(
                    part for part in (previous_reason, coverage_reason) if part
                )
            verdicts["status"] = "PARTIAL"
            write(verdicts_path, verdicts)

    # Preserve media/derived-asset coverage when an entire procedure is replaced.
    for path in sorted(PACKS.glob("*/media-bindings.json")) + sorted(PACKS.glob("*/derived-assets.json")):
        value = load(path)
        repaired = replace_ids(value, old_to_new)
        if repaired != value:
            write(path, repaired)

    run = {
        "date": "2026-08-29",
        "policy": "append-only repaired replacements; protected originals unchanged",
        "independent_verifier": "not_rerun_fal_key_unavailable",
        "replacement_count": len(all_repairs),
        "replacements": all_repairs,
        "obsolete_without_replacement": obsolete,
    }
    write(RUN_PATH, run)
    print(json.dumps({
        "replacement_count": len(all_repairs),
        "obsolete_without_replacement": len(obsolete),
        "run_manifest": str(RUN_PATH.relative_to(ROOT)),
    }))


if __name__ == "__main__":
    main()
