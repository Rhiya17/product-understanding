# Work Order: Ready2Jet Vault Gap Closure

**Date issued:** 2026-08-20
**For:** an autonomous agent with repository access and web access (no prior conversation context assumed)
**Scope:** ONLY the Graco Ready2Jet — `source-vault/graco-ready2jet-2212125/` and `evidence-packs/graco-ready2jet-2212125/`. Do not touch any other product.
**Governing rules:** `source-vault/README.md` (vault rules), `docs/workorders/evidence-pack-extraction-workorder.md` §4–§5 (claim schema and consequence tiers).

---

## Why

The Ready2Jet was seeded from local POC files rather than fresh collection, so it
has three recorded gaps the other four products don't have (see
`collection_gaps` in its `manifest.json`):

1. Its `specs/` directory is **empty** — no official spec source was ever
   collected, which is why the evidence pack has zero SPEC claims (empty
   weight, dimensions, box contents are absent from the manual).
2. Every manifest entry has `origin_url: null`.
3. `spin_360` is unchecked (digital-twin plan Decision 8, task D8a).

Close all three, then carry the new spec facts into the evidence pack.

## Task 1 — Collect the official spec source (the main event)

1. Find the Ready2Jet product page on **gracobaby.com** (model 2212125; URL
   shape is like `https://www.gracobaby.com/shop/.../SAP_2212125.html`).
   Known access quirk from prior collection: **gracobaby.com blocks curl and
   plain fetches — use browser tools for the page itself.** Graco's asset
   CDNs (`s7d1.scene7.com` for images, `newellbrands.imgix.net` for PDFs)
   allow direct `curl` download.
2. Write `source-vault/graco-ready2jet-2212125/specs/specs.md` with the full
   spec transcription: **product (empty) weight, open dimensions, folded
   dimensions**, child weight/height capacity as stated on the page, box
   contents, car-seat compatibility statement, price, colorway. Header must
   carry the source URL and retrieval date.
3. If the PDP links any spec/instruction PDFs not already in the vault,
   download them into `specs/` or `manuals/` (verify with `file`; delete
   HTML masquerades).
4. Add one manifest entry per new file/page with real SHA-256
   (`shasum -a 256`), `origin_url`, `acquired_at` (today), `authority:
   "MANUFACTURER_SPEC_PAGE"`, and the standard rights note used by the other
   entries. Follow the existing entries' exact JSON shape.
5. If the current PDP turns out to be a different revision/model-year than
   2212125, do NOT silently substitute: collect it anyway, record the exact
   identity found, and describe the discrepancy prominently in
   `collection_gaps` and your report (precedent: the SnugRide rename found
   during first-wave collection).

## Task 2 — Origin-URL backfill

The Ready2Jet's existing sources were acquired during July POCs. Recover
their origin URLs where the repo records them:

- Search `poc-higgsfield-one-hand-fold/` (README, result docs),
  `docs/pocs/ready2jet-reference-image-curation.md`,
  `poc-3d-static-twin/inputs/` (any source manifest), and
  `poc-wanvace-control-video/references/` for recorded acquisition URLs.
- For each vault entry you can match, set `origin_url`.
- Where no URL is recorded anywhere, set
  `"origin_url": "unknown:local-poc-acquisition"` and note it — an explicit
  unknown beats a silent null.
- Do not change any `sha256`, `local_path`, or `source_id`.

## Task 3 — D8a: 360-spin audit

Check BOTH the gracobaby.com PDP and the Amazon listing for the Ready2Jet:

- Is there a 360°/spin viewer? (Look for spin UI, viewer scripts, or a
  multi-frame rotation asset set — a flat image carousel is "absent".)
- If present: photographic or CGI?
- Update `spin_360` in the manifest: `present` (true/false), `type`
  (`"photo"`, `"cgi"`, or null), `checked_at` (the URLs you inspected), and
  a one-line note. Remove the spin item from `collection_gaps`.

## Task 4 — Carry the specs into the evidence pack

1. Extract SPEC claims from the new `specs.md` into
   `evidence-packs/graco-ready2jet-2212125/claims.json`: product weight,
   open dimensions, folded dimensions, box contents, and any other directly
   stated facts. Schema per the extraction work order §4; these are C0
   unless safety-adjacent; `authority: "MANUFACTURER_SPEC_PAGE"`;
   `source_bindings` cite the new manifest `source_id` with the exact quote
   (page may be null for a web page — quote is still mandatory).
2. **Conflict protocol:** if a spec value disagrees with anything already
   claimed from the manual (e.g., child weight capacity), record BOTH claims
   with `extraction_notes: "CONFLICT: ..."` cross-references. Never
   reconcile.
3. Update `extraction-report.md`: the "Missing Specifications" gap is now
   closed (or narrowed) — say what was added and what remains; note the D8a
   result.

## Verification before you finish (mandatory)

Run from the repo root; all three must pass:

```
python3 scripts/validate_vault.py        # manifest/hash integrity incl. your new entries
python3 evidence-packs/validate.py       # claim schema + anti-fabrication quote gate
python3 scripts/check_docs_sync.py       # must remain untouched-green
```

Note: the evidence-pack validator verifies quotes against cited PDF pages
mechanically. For web-page-sourced claims it cannot, so your quotes from
`specs.md` must be copy-paste exact — a human will spot-check them.

## What NOT to do

- No changes outside the two Ready2Jet directories.
- No new claims without a source binding and exact quote; no inferred values.
- No YouTube/retailer media downloads (URL records only, per vault rules).
- Do not modify existing claims except to add conflict cross-references.
- Do not touch `docs/` or any other product.

## Definition of done

- `specs/specs.md` exists with the facts listed in Task 1.2, manifested with
  real hashes and origin URLs.
- Zero `origin_url: null` entries remain (real URL or explicit
  `unknown:local-poc-acquisition`).
- `spin_360` resolved with evidence; `collection_gaps` updated to reflect
  all three closures.
- New SPEC claims in the evidence pack; report updated.
- All three validators pass from the repo root.
- Final report: what was found (including the spin answer and any identity
  discrepancy), claims added, URLs backfilled vs. marked unknown, anything
  left open.
