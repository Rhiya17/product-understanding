# POC 8 evidence map and correctness checklist

**Trust:** INTERNAL ONLY — TWIN RENDER. `approved_by: null`. Tripo3D license
review remains open; no artifact in this directory may be served externally.

## Required connection truth

| Check | Required visible state | Evidence |
|---|---|---|
| 1 | The **2.5 mm end** enters the **LEFT earcup** port. | `claim_bqcu2_step_aux_1`, `claim_bqcu2_part_aux_port_1`, owner's guide pp. 13 and 33 |
| 2 | The **3.5 mm end** enters the MacBook Air's **RIGHT-side** jack. | `claim_bqcu2_step_aux_2`, `claim_mba_part_headphone_jack`, `src_img_guide_right_side` |
| 3 | The cable is asymmetric: 2.5 mm at the headphone end and 3.5 mm at the source end. | `claim_bqcu2_aux_cable_spec_1`, owner's guide p. 33 |
| 4 | Bose and MacBook appearances remain recognizable against official images. | `src_img_black_controls`, `src_img_guide_right_side` |
| 5 | Only the active plug/cable section moves in each shot; products, desk, lighting, and camera stay fixed. | Work order Stage A/D; deterministic named actions |

## Scale evidence

### Bose QuietComfort Ultra Headphones (2nd Gen)

The official product-page quote bound to
`claim_bqcu2_spec_headphone_weight_1` is `1.772 in H × 6.299 in W × 8.071
in D`. For the observed wearing orientation this is mapped to scan axes as:

- X thickness: 0.0450088 m;
- Y width: 0.1599946 m;
- Z height: 0.2050034 m.

The mapping is interpretation of the manufacturer-labeled dimensions, not a
new measurement, and is recorded in `config.json`.

### MacBook Air 13-inch M3

- X width 0.3041 m: `claim_mba_spec_width`;
- Y depth 0.215 m: `claim_mba_spec_depth`;
- Z closed height 0.0113 m: `claim_mba_spec_height`.

The Tripo scan is open/ambiguous while Z is a closed-state claim. The work
order nevertheless requires per-axis rescaling to the claims. This mismatch
is surfaced here and in the Gate 1 report; it may cause identity failure and
must not be silently worked around.

## Scene evidence and inferences

| Scene choice | Status | Basis |
|---|---|---|
| Mac jack on right side | Evidence | `claim_mba_part_headphone_jack`; official right-side guide image |
| Bose AUX port on left earcup | Evidence | `claim_bqcu2_step_aux_1`, `claim_bqcu2_part_aux_port_1`; official wired photo |
| Black cable | Evidence | visible in `src_img_black_controls` |
| 2.5 / 3.5 mm conductive shaft diameters | Evidence | `claim_bqcu2_aux_cable_spec_1`; standard connector nominal sizes named by the claim |
| Neutral desk, studio world, light placement | **INFERRED** | presentation-only, fixed in script |
| Product separation and resting pose | **INFERRED** | presentation-only, fixed in script |
| Cable sheath diameter, slack path, plug length/grip | **INFERRED** | not specified by evidence; declared in `config.json` |
| Exact port coordinates on imperfect twins | **INFERRED** | visually registered against official views; Gate 3 must confirm side and seating |
| Camera focal lengths and framing | **INFERRED** | fixed presentation parameters; no geometry claim |

## Gate policy

1. **Gate 1:** repaired worst-axis dimension error ≤5% and VLM identity pass
   for both twins. Two failed attempts stop the POC.
2. **Gate 2:** cable-only render passes the evidence comparison; one retry.
3. **Gate 3:** sampled primary frames visibly satisfy checklist items 1–2.

No later-stage pass may override an earlier failure.

