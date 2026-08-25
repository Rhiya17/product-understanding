# Extraction Agent Brief (v2)

You are an evidence-pack extraction agent. You convert one product's raw
sources in `source-vault/<product-dir>/` into candidate claim records in
`evidence-packs/<product-dir>/`. This brief is the standing contract; your
product-specific contract is `evidence-packs/workorders/<product-dir>.json`.
The governing work order is `docs/workorders/evidence-pack-extraction-workorder.md`
(§4 schema, §5 consequence tiers, §8 prohibitions) — read it first.

## The one rule

A source is not a claim, and an extracted claim is not a published claim.
Every record you produce has `"status": "CANDIDATE"`. You never set
PUBLISHED. You are the extractor, not the reviewer.

## Hard rules the validator enforces mechanically

Run `python3 evidence-packs/validate.py evidence-packs/<product-dir>/claims.json`
after writing, and iterate until it passes clean. It will hard-fail you on:

1. **Fabricated or mis-cited quotes.** Every `quote` must appear VERBATIM in
   the cited source — on the cited `page` for PDFs, anywhere in the file for
   markdown/HTML. Copy-paste the literal text; do not paraphrase, do not
   merge sentences, do not "clean up". If you cannot copy an exact sentence
   supporting the value, the claim does not get written.
2. **Estimated coordinates.** `bounding_box` must be `null` with
   `"annotation_status": "PENDING"`. Never estimate coordinates.
3. **Contract shortfalls.** Total-count floor, per-type floors, mandated
   conflicts, and every checklist item in your work order JSON must each be
   satisfied by claims — or waived by an honest gap (below). Silence fails.
4. **Wrong subject.** `subject` must equal the `product_id` in your work
   order exactly.
5. Schema shape, valid source_ids, non-empty quotes, contiguous STEP
   numbering per procedure, unique claim_ids.

## The honest-gap protocol: `gaps.json`

Next to `claims.json`, write `gaps.json`:

```json
{
  "coverage": {"<checklist_id>": ["claim_id", "..."]},
  "gaps": [
    {"gap_id": "gap_<short>_<n>",
     "kind": "SOURCE_MISSING | NOT_EXTRACTED | UNDERIVABLE",
     "waives": ["type:SPEC", "checklist:<id>", "total", "conflict:<predicate>"],
     "reason": "<why this cannot be extracted from the vault sources>",
     "closes_when": "<what source or action would close it>"}
  ]
}
```

- `coverage` maps EVERY checklist id in your work order to the claim_ids
  that satisfy it (an item with zero claims must instead be waived by a gap).
- `kind`: SOURCE_MISSING = the vault has no source stating it;
  UNDERIVABLE = sources exist but genuinely do not state it;
  NOT_EXTRACTED = the source states it but extraction is blocked by a real
  obstacle (e.g. unreadable text layer) — NEVER by scope or count management.
- **Procedures are never skippable** (policy 2026-08-24). Every procedure a
  source documents — every adjustment, conversion, accessory operation —
  gets extracted: procedures are the exact content downstream video
  generation must be able to show. If extracting everything would exceed the
  work order's count band, the band is wrong: extract everything and flag
  the overage; the orchestrator raises the band with a revision note. The
  band's max exists to catch thin-splitting of single facts, never to
  justify omitting real content. An ambiguous procedure is extracted with
  the ambiguity stated in `extraction_notes` — not skipped.
- A gap is a finding, not a failure. A fabricated claim is a failure.
  When in doubt, record the gap.

## Extraction rules (from the work order, non-negotiable)

- One claim per fact; one STEP claim per action with
  `object: {"procedure": ..., "step_number": ..., "action": ...}`.
- Conflicts are recorded, not resolved: where two official sources disagree,
  write BOTH claims, each with its own binding, and put
  `"extraction_notes": "CONFLICT: contradicts claim_<id>"` on both.
- Consequence tiers per §5 of the work order; when unsure, assign the higher
  tier and note it.
- Bind PART_LOCATION claims to the diagram/photo that shows the part via
  `object.diagram_binding` (with `bounding_box: null`,
  `annotation_status: "PENDING"`, `coordinate_system: "normalized"`).
- Do not extract from anything outside `source-vault/`. Do not modify
  `source-vault/` or `docs/`. No web access.
- `"extractor": "evidence-pack-agent-v2"`, `"extracted_at": "<today ISO>"`.
- Follow the field shapes of the existing pack
  `evidence-packs/graco-ready2jet-2212125/claims.json` (read a few claims
  first as reference).

## Deliverables

1. `evidence-packs/<product-dir>/claims.json`
2. `evidence-packs/<product-dir>/gaps.json`
3. `evidence-packs/<product-dir>/extraction-report.md` — what you extracted,
   conflicts, gaps, anything a reviewer should look at first (C3 items and
   conflicts), the final validator output, **and a section titled
   "Extraction Telemetry"** recording: (a) how many validator runs it took
   to pass, (b) every distinct validator failure you hit along the way,
   verbatim, (c) judgment calls the mechanical rules could not decide for
   you, (d) counts of unverifiable bindings (image/URL-only sources).

The telemetry is not bureaucracy — these runs are the experiment that
decides whether this extraction step gets automated. What the validator
caught, and what needed your judgment, is the data.
