# Extraction Report — Bose QuietComfort Ultra Headphones (2nd Gen)

**Product:** `prod_bose_qc_ultra_headphones` (`bose-qc-ultra-headphones`)
**Work order:** `evidence-packs/workorders/bose-qc-ultra-headphones.json` (`wo_extract_bose_v1`)
**Extractor:** `evidence-pack-agent-v2` — extracted 2026-08-24
**Result:** 59 CANDIDATE claims, 5 recorded gaps. Validator green (0 errors, 0 warnings).

## Claim counts

| Type | Count | | Ceiling | Count |
|---|---|---|---|---|
| SPEC | 16 | | C0 | 15 |
| STEP | 14 | | C1 | 28 |
| WARNING | 9 | | C2 | 7 |
| STATE | 7 | | C3 | 9 |
| PART_LOCATION | 6 | | | |
| CARE | 3 | | | |
| COMPATIBILITY | 3 | | | |
| LIMIT | 1 | | | |

All required-type floors met (SPEC ≥5, STEP ≥3, PART_LOCATION ≥2, WARNING ≥1); total 59 within the 25–60 contract band.

STEP procedures (all contiguous from 1): `bluetooth_pairing` (3), `store_headphones` (4), `clear_paired_device_list` (2), `connect_aux_cable` (2), `connect_usb_audio` (3).

## What a reviewer should look at first

### Conflicts recorded (both discovered, none mandated by the work order)

1. **Connected status-light duration — 5 s vs 10 s (same document).**
   `claim_bqcu2_state_connected_light_5s_1` (owner's guide p37 status table: "Solid blue (5 seconds) Connected") vs `claim_bqcu2_state_connected_light_10s_1` (p28 pairing procedure: "Once connected, the status light glows solid blue for 10 seconds."). Both carry CONFLICT extraction_notes.
2. **Quick-charge playback — 3 h body copy vs 2.5 h in its own test footnote (owner's guide p36).**
   `claim_bqcu2_quick_charge_playback_1` ("a 15-minute charge powers the headphones for up to 3 hours") vs `claim_bqcu2_quick_charge_playback_2` (footnote 1: the April 2025 quick-charge test "resulting in up to 2.5 hours playback time before battery depletion"; 2 h with Immersive Audio on). Both carry CONFLICT extraction_notes.

A third *potential* conflict was noted but not claim-paired: Bluetooth range is 30 ft / 9 m in the owner's guide (claimed), while the manifest notes for the uncaptured support specifications article record "33 ft". Since the 33 ft side has no local source text, it is noted in `claim_bqcu2_bluetooth_range_1.extraction_notes` instead of being written as an unverifiable conflicting claim.

### C3 items
All 9 WARNING claims (hearing damage, vehicle operation, situational awareness, hinge pinch, not-for-children, choking/small parts, magnetic material vs implants, battery-removal prohibition, loud unusual noise). Assigned C3 per the work order §5 row "all safety warnings from the manuals" — see judgment call (c) below.

### The one unverifiable binding
`claim_bqcu2_bluetooth_version_1` (Bluetooth 5.4) is bound to `src_specifications_article`, which has **no local capture** — the quote cannot be mechanically verified. The fact is recorded in the source-vault manifest's own notes for that source ("Bluetooth 5.4"). Flagged in extraction_notes; must be verified against the live article before publish.

## Gaps (gaps.json)

| gap_id | kind | waives | summary |
|---|---|---|---|
| gap_macbook_1 | UNDERIVABLE | checklist:macbook_compatibility | No collected source on either side states MacBook pairing/wired compatibility. The owner's guide only says "a computer" as a USB-C power source. **This is the expected, important finding.** |
| gap_weight_1 | SOURCE_MISSING | — | Product weight appears in no local source; spec pages uncaptured, manifest notes record no numeric weight. |
| gap_codecs_1 | UNDERIVABLE | — | Codec list beyond aptX Adaptive (SBC/AAC) not enumerated anywhere collected; manifest collection_gaps confirms. |
| gap_usb_lossless_1 | SOURCE_MISSING | — | USB-C lossless bit depth / sample rates only on the uncaptured product page; owner's guide states USB-C audio support without figures. |
| gap_included_cable_lengths_1 | SOURCE_MISSING | — | Cable lengths (e.g. 39-in USB-C) not in any local source. |

Checklist coverage: `specs_core` (14 claims), `pairing_procedure` (3), `bt_device_name` (1), `controls_layout` (5), `macbook_compatibility` (waived by gap_macbook_1).

## Source usage

- `src_owners_guide_en` (50-page PDF): 49 of 50 bindings — the workhorse.
- `src_safety_instructions_ml` (PDF): 6 WARNING bindings (page 1, English section — cleaner text extraction than the owner's guide safety pages for several warnings).
- `src_specifications_article` (no local file): 1 binding (Bluetooth 5.4), unverifiable, flagged.
- `src_power_user_gestures` (carton insert PDF): **zero bindings** — its extractable text is only "1x 2x 3x support.Bose.com/QCU2"; no verbatim quote could support any claim. Controls diagram bindings went to owner's guide p13 instead.
- Image and video sources: not bound (no PART_LOCATION needed them; owner's guide diagrams are better annotation targets).

## Extraction Telemetry

**(a) Validator runs to green: 1.** The pack passed on the first run (0 errors, 0 warnings). A per-page text dump of the owner's guide was made first and all quotes were copy-pasted from that dump (the same pypdf extraction the validator uses), which is what made a first-run pass possible.

**(b) Distinct validator failures hit along the way, verbatim: none.** No FAIL or WARNING lines were ever emitted for this pack.

**(c) Judgment calls the mechanical rules could not decide:**
1. **Warning tier in a consumer-electronics domain.** The §5 table's C3 row is child-restraint themed but ends with "all safety warnings from the manuals". Applied that literally: all 9 warnings are C3 even though the product's consequence domain is C0/C1 consumer electronics. Higher-tier-when-unsure rule applied.
2. **Binding to a no-local-file source.** Wrote exactly one claim (Bluetooth 5.4) against `src_specifications_article`, per the instruction that such bindings are allowed only for facts the manifest itself records. The quote is the value as the manifest records it, not a verified article sentence — flagged for review. Every other spec-page-only fact (weight, 33 ft range, lossless figures, cable lengths, price) became a gap or a note instead of a claim.
3. **Quick-charge footnote treated as a conflict.** The p36 footnote describes the very test behind the "up to 3 hours" headline and reports 2.5 hours; recorded as two conflicting claims rather than silently preferring either figure.
4. **PDF extraction artifacts preserved.** pypdf renders some ligated text as "T o", "T urn", etc. Quotes were copied with artifacts intact (e.g. "T o use Fast Pair…") because the validator matches against the same extraction; claims carrying artifacts note this in extraction_notes.
5. **Serial-number location assigned C2** (not C1 like other PART_LOCATIONs) because viewing it requires removing the ear cushion and peeling inner fabric, which the guide cautions can damage the headphones.
6. **Gestures carton unusable for quotes** (text-free); decided against forcing a binding to it.
7. **Bluetooth range 30 ft vs 33 ft** handled as an extraction note, not a conflict pair, because one side has no citable local text.
8. **COMPATIBILITY claims at C2** per §5 ("third-party compatibility"), including the Bose-to-Bose SimpleSync claim for consistency.

**(d) Unverifiable-binding counts:** 1 binding unverifiable for lack of a local file (`src_specifications_article` / Bluetooth 5.4); 0 bindings to image/video (binary) sources. 58 of 59 quote-bearing bindings were mechanically verified against local PDFs.

## Final validator output

```
--- Validating evidence-packs/bose-qc-ultra-headphones/claims.json ---
SUMMARY_JSON: {"ceilings": {"C0": 15, "C1": 28, "C2": 7, "C3": 9}, "claims": 59, "errors": 0, "gaps_recorded": 5, "product": "bose-qc-ultra-headphones", "quotes_verified": 58, "types": {"CARE": 3, "COMPATIBILITY": 3, "LIMIT": 1, "PART_LOCATION": 6, "SPEC": 16, "STATE": 7, "STEP": 14, "WARNING": 9}, "unverifiable_binary_source": 0, "unverifiable_no_local_file": 1, "warnings": 0, "workorder_enforced": true}
Validation successful for evidence-packs/bose-qc-ultra-headphones/claims.json
```

## Gap-closure top-up (2026-08-24, human-directed)

Directed by review (vijayp.cmu@gmail.com): capture the missing spec sources
and close the spec gaps. What happened:

- **Discovery:** `specs/specs.md` existed on disk since collection day with
  the missing facts (Bluetooth 5.4, weight, USB-C lossless, cable length) but
  was never registered in the vault manifest — which is why extraction
  correctly refused to bind to it. Registered as `src_specs_curated_v1`
  (secondary authority: curated transcription). NOTE: `validate_vault.py`
  did not catch the orphan file — validator gap, see findings doc.
- **Fresh capture:** the official product page was captured as static HTML
  (`src_product_page_capture_v1`); it carries weight/dimensions and the
  USB-C 16-bit/44.1-48 kHz audio statement in static markup. The support
  specifications article could NOT be captured over HTTP (JS application
  shell) — recorded as `gap_spec_article_raw_capture_1`.
- **5 new claims** (all C0 SPEC, quotes machine-verified):
  `claim_bqcu2_bluetooth_version_2` (supersedes the rejected v1),
  `headphone_weight` 0.583 lb / 264 g, `usb_audio_format` 16-bit 44.1/48 kHz,
  `included_usbc_cable_length` 39 in, and `bluetooth_range` 33 ft — the last
  recorded as a NEW CONFLICT with the owner's-guide 30 ft claim (likely
  9 m vs 10 m rounding; reviewer to disposition).
- **Gaps:** closed gap_bluetooth_version_1, gap_weight_1, gap_usb_lossless_1;
  narrowed gap_included_cable_lengths_1 to the aux cable only; added
  gap_spec_article_raw_capture_1. gap_codecs_1 stands (specs.md confirms
  SBC/AAC are not enumerated anywhere official).
- Validator: 0 errors; 65 quotes verified; work-order max raised 60→70 with
  a revision note.
