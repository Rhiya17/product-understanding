# Evidence Packs

This directory contains the output of the offline Claim Extraction pipeline. 

The purpose of these packs is to convert raw, unstructured product manuals and specifications from the `source-vault` into typed, verifiable JSON claims. These candidate claims seed the Evidence Graph for the ShowMe system.

## Data Model & Guiding Principles
- **Candidate Status Only:** All claims are generated with `status: "CANDIDATE"`. They must pass human review or strict programmatic policy verification before entering production.
- **Consequence Tiers:** Claims are assigned a consequence ceiling (`C0` through `C3`) to determine the level of strictness required for validation and serving. Safety limits and warnings are generally `C3`.
- **Hybrid RAG:** These structured claims work alongside raw manual RAG. They provide verified answers to exact limit questions, step-by-step procedures, and compatibility, while vector search handles contextual inquiries.
- **Source Preservation:** Every single claim contains a `source_bindings` array with exact quotation and page numbers pointing to the authoritative `source_id` in the vault manifest. The validator verifies every quote literally appears in the cited local source (PDF page, or whole file for markdown/HTML) — a claim whose quote cannot be found fails validation as possibly fabricated.
- **Honest gaps, not silent holes:** Each pack carries a `gaps.json` with a `coverage` map (work-order checklist item → claim_ids) and typed gap records (`SOURCE_MISSING` / `UNDERIVABLE` / `NOT_EXTRACTED`) that explicitly waive any contract expectation the sources cannot support.

## Work orders
`workorders/<product-dir>.json` is the machine-readable extraction contract per product (claim-type floors, total-count band, mandated conflict pairs, checklist). `workorders/extraction-agent-brief.md` is the standing brief given to every extraction agent. The validator enforces the contract: unmet expectations are hard failures unless waived by a recorded gap.

## Usage
To validate structure, source bindings (including quote existence), and work-order contract compliance:
```bash
python validate.py <product-directory>/claims.json
```
If called with no arguments, it validates all packs. Requires `pypdf` for the quote gate (CI installs it; without it PDF quote checks are skipped with a warning). Each run prints one `SUMMARY_JSON` line per pack for telemetry.

## Review status
All five products extracted (2026-08-24, `evidence-pack-agent-v2`; Ready2Jet v1 base 2026-08-20). All claims remain `CANDIDATE` — claims are immutable extraction artifacts; human review decisions are recorded separately in each pack's `reviews.json` (`APPROVED_FOR_PUBLISH` / `REJECTED_FOR_SERVING` / `NEEDS_RECHECK`, validated by `validate.py`). First decision recorded 2026-08-24: SnugRide max child weight — the manual's 30 lb approved, the legacy 35 lb gallery-image figure rejected for serving. Reviewers should start with the C3 claims and the recorded CONFLICT pairs (see each pack's `extraction-report.md`).
