# Extraction Report — Levoit Core 300S (`prod_levoit_core_300s`)

Extractor: `evidence-pack-agent-v2` · Extracted: 2026-08-24 · Work order: `wo_extract_levoit_v1`

## Summary

57 CANDIDATE claims (contract window 25–60), all validating clean.

| Type | Count | | Ceiling | Count |
|---|---|---|---|---|
| SPEC | 20 | | C0 | 16 |
| STEP | 18 | | C1 | 20 |
| WARNING | 6 | | C2 | 15 |
| CARE | 5 | | C3 | 6 |
| PART_LOCATION | 3 |
| LIMIT | 2 |
| COMPATIBILITY | 1 | POLICY | 1 |
| STATE | 1 |

Procedures (all contiguous from 1): `replace_filter` (6 steps, C2), `reset_check_filter_indicator` (4 steps, C1), `vesync_app_setup` (3 steps, C1), `initial_setup_unwrap_filter` (4 steps, C2/C1), `disconnect_wifi_restore_defaults` (1 step, C1).

## The central finding: the primary source has no text layer

Both vault copies of the original Core 300S manual (`src_manual_core300s_us`,
`src_manual_core300s_vesync`) extract **zero characters** on all 24 pages via
pypdf and pdfminer.six (CID-encoded fonts, no usable ToUnicode maps — already
flagged in the vault manifest's collection_gaps). Any quote bound to those
source_ids would mechanically fail the validator's anti-fabrication gate,
regardless of being verbatim on the printed page.

Resolution taken (documented as `gap_300s_manual_binding_1`):

- The 300S manual was **read visually** — all relevant pages rendered to
  images via pypdfium2 and inspected — so it remains the authority against
  which every extracted fact was checked, and the source of the four revision
  conflicts below.
- Bindings cite the two mechanically verifiable sources instead:
  `src_manual_core300sp_us` (its cover states "Product Series: Core 300S
  series, Core 300S-P Series" — it is the official manual for *both* series)
  and `src_spec_page_core300s` (specs.md transcription, which carries the
  original-300S values). 300S-manual page numbers are preserved in
  `extraction_notes` on every claim where they matter.

## Revision conflicts recorded (300S vs 300S-P) — reviewers start here

Four conflicting pairs, per the §6.5 revision protocol (both claims written,
CONFLICT cross-references in `extraction_notes`, `applicability.revision` set):

| Predicate | Core 300S (manual p2/p12 + spec page) | Core 300S-P (manual rev A2-240918, p2/p12) |
|---|---|---|
| `product_weight` | 5.95 lb / 2.7 kg | **7.48 lb / 3.393 kg** |
| `rated_power` | 23 W | **39 W** |
| `noise_level` | 22–50 dB | **22–54.5 dB** |
| `replacement_filter_model` | Core 300-RF (True HEPA 3-Stage Original) | **Core 300-P-RF** (3-Stage Original) |

Spot-check notes on facts that did **not** conflict: dimensions, power supply
(AC 120V 60Hz), standby power (<2W), operating conditions, 219 ft² room size,
6–8 month filter interval, all extracted procedures (filter install/replace,
reset, app setup), and the warranty term are the same in both manuals. The
300S-P manual *omits* the CADR row and Ideal Room Size row from its spec table
and drops all "True HEPA"/H13/99.97% language — recorded as absences/notes, not
conflicts. Package contents differ only in the filter's printed name (noted on
`claim_c300s_spec_package_contents`).

Additional reviewer flags:

- **C3 items**: the six WARNING claims (fire, shock, oxygen-proximity,
  combustible-environment, dimmer-switch, unplug-before-maintenance), assigned
  C3 per the "all safety warnings from the manuals" rule.
- `claim_c300s_spec_coverage`: spec page says "219 ft² at 4.8 ACH", 300S manual
  p11 says ACH of 5 — marketing-page vs manual tension, noted, not a revision
  conflict.
- `claim_c300s_warning_unplug_before_maintenance`: quote is verbatim from the
  300S-P PDF's *garbled* text layer ("air purifierbefore servicing ,cleaning…");
  the note carries the clean 300S-manual wording.
- `claim_c300s_part_filter_reset_button`: there is no dedicated reset button —
  the Sleep Mode (moon) button carries the "RESET FILTER (3S)" secondary
  function; bound to the top-control-panel image with `bounding_box: null`,
  `annotation_status: PENDING` (C1, per work order).

## Gaps (3, none waiving a contract expectation)

1. `gap_300s_manual_binding_1` (NOT_EXTRACTED) — 300S manual unbindable (above).
2. `gap_hepa_efficiency_1` (UNDERIVABLE) — the 99.97% @ 0.3 µm H13 figure exists
   only in the unbindable 300S manual (p11); 300S-P manual dropped it; spec page
   lacks the number. No claim written.
3. `gap_support_page_capture_1` (SOURCE_MISSING) — VeSync filter store page has
   no local capture (`local_path: null`); filter compatibility/lifespan bind to
   the specs.md transcription instead.

## Extraction Telemetry

**(a) Validator runs to green: 1.** The pack passed with 0 errors / 0 warnings
on the first run. This was not luck: before writing a single claim I probed the
validator's normalization behavior (read `validate.py`), dumped the 300S-P
manual's full per-page extracted text to the scratchpad, and composed every
quote directly from that extracted text rather than from the visually rendered
page. All 64 text-bound quotes verified.

**(b) Distinct validator failures hit, verbatim: none.** (Zero failed runs.)
The failure that *would* have dominated was identified pre-emptively by probing:
any binding to `src_manual_core300s_us` yields
`quote not found on cited page N of levoit-core-300s-user-manual-us.pdf — possible fabricated or mis-cited quote`
because both 300S PDF copies extract as empty text. This was designed around
(see central finding) rather than hit.

**(c) Judgment calls the mechanical rules could not decide:**

1. **Primary source unbindable.** The work order names the 300S manual as the
   extraction primary, but its quotes can never pass the quote gate. Chose:
   visual reading for truth + verifiable bindings to the 300S-P series manual
   (which officially covers the 300S series) and the spec page, with the gap
   recorded, over either (i) writing bindings guaranteed to fail or (ii)
   silently extracting only from the 300S-P manual.
2. **Quote fidelity vs text-layer artifacts.** The 300S-P PDF's text layer
   contains kerning/garbling artifacts ("Y ou", "air purifierbefore servicing
   ,cleaning"). The verbatim-in-source rule was read as "verbatim in the text
   layer the validator checks"; artifacts were kept in quotes and explained in
   `extraction_notes` rather than "cleaned up" (which the brief prohibits).
3. **Icon-glyph steps.** Reset steps 3–4 print button icons that vanish in
   extraction ("Press and hold  for 3 seconds"); paired each with a second
   binding (manual p6) that names the Sleep Mode button in prose.
4. **Conflict vs absence.** CADR, Ideal Room Size, and the True HEPA/99.97%
   language are *missing* from the 300S-P manual, not contradicted — recorded
   as notes/gaps, not CONFLICT pairs. The 4.8 vs 5 ACH tension (spec page vs
   manual) likewise noted, not conflicted, since §6.5 scopes conflicts to
   300S-vs-300S-P differences.
5. **Tier calls.** Filter-model SPECs → C2 (drives replacement purchases);
   initial-setup steps 1–3 → C2 (filter-compartment access), step 4 → C1;
   housing wipe-down → C1 (everyday reversible), pre-filter/sensor
   cleaning → C2. Ambiguous ones carry `extraction_notes`.
6. **Package-contents wording.** Filter named differently across manuals but
   contents identical — treated as wording variance (note), not a value
   conflict; a stricter reading could split it into a fifth conflict pair.

**(d) Unverifiable-binding counts:** 2 bindings on image sources
(`src_img_top_panel_2048` on the reset-button PART_LOCATION;
`src_img_aq_indicator_table` on the AQ-indicator SPEC) — counted by the
validator as `unverifiable_binary_source: 2`. 0 bindings to no-local-file
sources (the VeSync support page was deliberately *not* bound; see gap 3).
The two PART_LOCATION `diagram_binding`s to manual page 5 are on a verifiable
PDF and carry `bounding_box: null` + `PENDING`.

## Final validator output

```
--- Validating evidence-packs/levoit-core-300s/claims.json ---
SUMMARY_JSON: {"ceilings": {"C0": 16, "C1": 20, "C2": 15, "C3": 6}, "claims": 57, "errors": 0, "gaps_recorded": 3, "product": "levoit-core-300s", "quotes_verified": 64, "types": {"CARE": 5, "COMPATIBILITY": 1, "LIMIT": 2, "PART_LOCATION": 3, "POLICY": 1, "SPEC": 20, "STATE": 1, "STEP": 18, "WARNING": 6}, "unverifiable_binary_source": 2, "unverifiable_no_local_file": 0, "warnings": 0, "workorder_enforced": true}
Validation successful for evidence-packs/levoit-core-300s/claims.json
```

## Revision policy decision (2026-08-24, human review)

Latest-revision-only policy adopted (reviewer: vijayp.cmu@gmail.com): the
Core 300S-P is the current retail revision and is canonical. Actions taken:

- The two original Core 300S manual PDFs (`src_manual_core300s_us`,
  `src_manual_core300s_vesync`) were REMOVED from the vault (zero claims ever
  bound to them — no text layer). Logged in the manifest `curation_log`;
  origin URLs retained for provenance.
- The four revision-conflict pairs were dispositioned in `reviews.json`:
  all four 300S-P claims APPROVED_FOR_PUBLISH, all four original-300S claims
  REJECTED_FOR_SERVING (kept as CANDIDATE records — their source, Levoit's
  live spec page, still carries original-revision values).
- The `revision_conflict_300sp` checklist item was retired from the work
  order; this report's "Revision conflicts" section above stands as the
  historical record of what the comparison found.
- Caveat recorded on the filter decision: original-300S owners need
  Core 300-RF, not the served Core 300-P-RF.

## Human verification of image bindings (2026-08-24)

Both mechanically-unverifiable image bindings were verified by human review
(reviewer: vijayp.cmu@gmail.com, with rendered images inspected):

- `claim_c300s_part_filter_reset_button` / `src_img_top_panel_2048`:
  VERIFIED — the moon (Sleep Mode) button sits left of the ring around the
  central power button with the label "RESET FILTER (3S)" beneath it,
  exactly as described.
- `claim_c300s_spec_aq_indicator` / `src_img_aq_indicator_table`:
  VERIFIED WITH A NOTE — the primary binding (300S-P manual p9 chart) is
  machine-verified and carries the full mapping; the image corroborates the
  four indicator colors and the fan-speed dot progression, but its
  air-quality text labels are illegible (single-frame PNG with faint text,
  despite the .webp extension). The binding description slightly overstates
  what the graphic legibly shows; the claim's data is manual-backed and
  stands.
