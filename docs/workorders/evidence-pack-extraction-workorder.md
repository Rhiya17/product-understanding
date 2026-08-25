# Work Order: Evidence Pack Extraction

**Date issued:** 2026-08-20
**For:** an autonomous agent with repository access (no prior conversation context assumed)
**Depends on:** `source-vault/` (complete, 5 products), `docs/architecture/low-level-design.md` v0.7 (the LLD — §6.5, §6.6, §9.2 govern this work)
**Output:** `evidence-packs/` — one directory of structured candidate claims per product

---

## 1. Objective

Convert the raw sources in `source-vault/` into **candidate claim records** —
small, typed, individually-cited fact cards — for all five catalog products.
These packs seed the Evidence Graph: they are what the answer system will
serve from, what clarification options are enumerated from, and what video
generation specs bind to.

**The one rule that governs everything: a source is not a claim, and an
extracted claim is not a published claim.** Every record you produce has
`"status": "CANDIDATE"`. You never set `PUBLISHED` — a human review pass
does that later. You are the extractor, not the validator.

## 2. Inputs

- `source-vault/catalog.json` — the five products, identities, compatibility pairs.
- `source-vault/<product-dir>/manifest.json` — every source with its `source_id`,
  local path, and origin URL. **Cite claims against these `source_id`s only.**
- The source files themselves: manual PDFs, `specs/specs.md`, images,
  `videos/video-sources.md`.
- Schema reference: LLD §6.6 (claim record), §6.5 (validation context),
  consequence tiers C0–C3 in `docs/architecture/system-architecture.md` §9.

## 3. Output layout

```
evidence-packs/
  README.md                      # brief: what these are, CANDIDATE-only rule, review status
  <product-dir>/                 # same dir names as source-vault/
    claims.json                  # all candidate claims for the product
    extraction-report.md         # what you extracted, what you skipped, conflicts, gaps
```

## 4. Claim record schema

Follow LLD §6.6 exactly. Template:

```json
{
  "claim_id": "claim_<product_short>_<predicate>_<seq>",
  "version": 1,
  "type": "SPEC | LIMIT | STEP | PART_LOCATION | COMPATIBILITY | WARNING | CARE | POLICY | STATE",
  "subject": "<product_id from catalog.json>",
  "predicate": "<snake_case fact name, e.g. maximum_child_weight>",
  "object": {"value": 30, "unit": "lb"},
  "applicability": {"sku": "...", "revision": null, "market": "US", "state": null},
  "source_bindings": [
    {"source_id": "<from the product manifest>", "page": 5, "region": null,
     "quote": "<the exact sentence or table cell the value came from>"}
  ],
  "authority": "MANUFACTURER_MANUAL | MANUFACTURER_SPEC_PAGE | MANUFACTURER_SUPPORT_PAGE",
  "consequence_ceiling": "C0 | C1 | C2 | C3",
  "status": "CANDIDATE",
  "extractor": "evidence-pack-agent-v1",
  "extracted_at": "<ISO date>",
  "extraction_notes": "<only if something needs a reviewer's attention>"
}
```

Rules on fields:

- **`source_bindings` is mandatory and must be real.** Page number for PDFs,
  the section for markdown specs, and always the `quote` — the literal text
  you extracted from. A claim you cannot bind to a source **does not get
  written**. Never fill a value from general knowledge, another product, or
  inference.
- **Ordered steps**: one claim per step, `type: "STEP"`, with
  `object: {"procedure": "fold", "step_number": 2, "action": "...", "part": "..."}`.
  The procedure's step numbering must be complete and gap-free.
- **Part locations**: `object: {"part": "thumb_switch", "location_description": "...",
  "diagram_binding": {"source_id": "...", "page": 34}}` — bind to the manual
  diagram or photo that shows it.
- **Compatibility**: one claim per (product, counterpart) pair with exact
  identities both sides, e.g. SnugRide ↔ each stroller row of the official
  compatibility chart PDF.
- **Conflicts are recorded, not resolved.** Where two official sources
  disagree, write BOTH claims, give each its own binding, and add
  `"extraction_notes": "CONFLICT: contradicts claim_<id>"` on both. (Known
  live example: the SnugRide weight limit — current manual/page says 4–30 lb,
  one official gallery image still says 4–35 lb. Both must appear.)

## 5. Consequence assignment (deterministic, don't improvise)

| Tier | Assign to |
|---|---|
| C0 | Colors, dimensions, weights of the product itself, box contents, warranty length, battery life |
| C1 | Everyday reversible operation: fold/unfold, recline, canopy, pairing, app setup, filter reset button location |
| C2 | Care and disassembly that can damage the product: fabric washing, wheel/filter removal and replacement, firmware; third-party compatibility |
| C3 | Anything touching child restraint: car seat installation, harness steps, child weight/height limits, stroller↔car-seat attachment; all safety warnings from the manuals |

When unsure between two tiers, assign the higher and note it in `extraction_notes`.

## 6. Per-product extraction checklist

Work products in this order (fastest feedback first). "Complete" means every
listed item is either a claim or a recorded gap in the extraction report.

### 6.1 Graco Ready2Jet (`graco-ready2jet-2212125`)
- All specs and limits: product weight, child weight/height limits, folded and
  open dimensions, box contents, warranty (manual + any spec source).
- **The complete fold procedure** from manual pages 33–35, one STEP claim per
  action, with the thumb switch and handle lever as PART_LOCATION claims bound
  to the manual diagrams. This is the pilot procedure the whole product demos —
  it must be airtight.
- Unfold procedure, recline, canopy, brake, wheel removal, fabric care.
- All safety warnings in the manual (each a WARNING claim, C3).

### 6.2 Graco SnugRide Lite LX (`graco-snugride-35-lite-lx`)
- Specs + limits **including the 30 lb / 35 lb conflict recorded as two
  conflicting claims** (see §4).
- Every row of the official compatibility chart PDF as a COMPATIBILITY claim —
  note the chart's "(2025+)" qualifier on Ready2Jet in `applicability.revision`.
- Harness and installation steps: extract as STEP claims, all C3.
- 7-year expiration, base/LATCH facts, care rules.

### 6.3 Bose QC Ultra 2nd Gen (`bose-qc-ultra-headphones`)
- Specs: battery, Bluetooth version/codecs, multipoint, weight, wired options
  (3.5mm aux, USB-C lossless), included cables.
- Pairing procedure (from the owner's guide) as STEP claims; the Bluetooth
  device name ("BOSE QC ULTRA 2 HP") as a SPEC claim.
- Controls layout as PART_LOCATION claims.
- COMPATIBILITY claims for the MacBook pairing (wired via 3.5mm; Bluetooth) —
  **only if a source on either side states it**; otherwise record as a gap
  (cross-product compatibility may be underivable from these sources — that
  is an acceptable, important finding).

### 6.4 Apple MacBook Air 13" M3 (`apple-macbook-air-13-m3`)
- Port inventory as PART_LOCATION claims with sides: MagSafe 3 + 2× Thunderbolt
  on the LEFT, 3.5mm headphone jack on the RIGHT (bound to the port-guide
  captures in `manuals/`).
- Specs: dimensions, weight, Bluetooth 5.3, Wi-Fi 6E, audio capabilities,
  colors, model identifier Mac15,12.
- Bluetooth pairing procedure from the captured Apple guide as STEP claims
  (digital/on-screen procedure — note OS applicability if the guide states it).

### 6.5 Levoit Core 300S (`levoit-core-300s`)
- Specs: dimensions, weight, CADR, coverage, noise, filter model (Core 300-RF).
- Filter replacement procedure as STEP claims (manual diagrams as bindings), C2.
- Filter reset button as PART_LOCATION (bound to the control-panel image), C1.
- App/WiFi setup steps, C1.
- **Manual revision note:** the vault holds both the 300S and 300S-P manuals.
  Extract from the 300S manual; where the 300S-P manual differs on a fact you
  extract, record both with applicability noting the revision, same conflict
  protocol as §4.

## 7. Self-verification before you finish (mandatory)

Write and run a validation script (keep it at `evidence-packs/validate.py`):

1. Every `claims.json` parses; every claim conforms to the §4 template
   (required fields present, `status == "CANDIDATE"`, consequence in C0–C3).
2. Every `source_id` referenced exists in that product's
   `source-vault/<dir>/manifest.json`.
3. Every STEP procedure has contiguous step numbers starting at 1.
4. Every claim's `quote` is non-empty.
5. No duplicate `claim_id`.
6. Print per-product counts by type and consequence.

The run's output goes at the bottom of each `extraction-report.md`.

## 8. What NOT to do

- Do not set any status other than `CANDIDATE`.
- Do not resolve conflicts, "correct" sources, or normalize disagreeing values.
- Do not write a claim without a source binding — no matter how obvious the
  fact is.
- Do not extract from anything outside `source-vault/` (no web access needed;
  if you believe a needed source is missing, record it as a gap).
- Do not modify anything in `source-vault/` or `docs/`.

## 9. Definition of done

- `evidence-packs/` exists with all five products, `claims.json` +
  `extraction-report.md` each, plus `README.md` and `validate.py`.
- `validate.py` passes clean on all five packs.
- Every §6 checklist item is a claim or a reported gap.
- The final report (your closing message) states: claims per product by
  type/consequence, all conflicts recorded, all gaps, and anything a human
  reviewer should look at first (the C3 items and the conflicts).

Rough expected scale, as a sanity check, not a quota: 40–80 claims for the
Ready2Jet and SnugRide, 25–50 each for the others. Far fewer means the
manuals weren't read; far more means facts are being split too thin.
