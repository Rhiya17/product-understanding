# Source Vault

The MVP's product asset repository — the "shelf" the offline factory stocks and the
online answer path reads (LLD §6.1–6.2). One directory per product, five products
in the first wave (see `catalog.json` for identities and selection rationale).

## Layout

```
source-vault/
  catalog.json                  # the 5 products, identity + tier hypothesis + pairs
  <product-dir>/
    manifest.json               # one entry per source: type, origin URL, sha256,
                                # acquisition date, authority, rights note
    manuals/                    # official manual / guide PDFs (or .md for HTML-only guides)
    images/                     # official product images, descriptive names
    videos/                     # direct-hosted official videos + video-sources.md (URL list)
    specs/                      # specs.md extracted from official spec pages, with URLs
```

## Rules (from the LLD)

1. **Originals are immutable.** Never edit a file in place; a corrected or re-fetched
   source is a new file and a new manifest entry.
2. **Every file has a manifest entry** with a real SHA-256, origin URL, acquisition
   date, and authority level. URL-only sources (YouTube videos we don't download)
   get entries with `local_path: null`.
3. **Rights discipline:** everything here is manufacturer-copyrighted, collected for
   internal research. `generate_from` is NOT cleared for any source — sending a
   source to a generation provider requires a rights review first (LLD §12.1).
   Images containing people are flagged — provider likeness filters reject them.
4. **Derivatives live outside the vault** (POC folders, evidence packs) and must
   reference their parent `source_id`.
5. **A source is not a claim.** Nothing in this vault is servable; facts become
   servable only when extracted into validated claims in the evidence pack
   (LLD §1.2 rule 1).
6. **Latest revision only** (policy decision 2026-08-24, from the Levoit
   300S/300S-P case). When a product has multiple hardware revisions sold under
   the same retail name, collect and maintain ONLY the latest revision's manual;
   do not keep multiple manuals for one listing — it is confusing and creates
   spurious conflicts. When collection discovers a same-name revision, the agent
   records the identity finding and captures the CURRENT revision's sources.
   Removals are logged in the manifest's `curation_log` with origin URLs retained
   for provenance (originals-are-immutable applies to files we keep, not to
   curation removals directed by a human). Known caveat, accepted: owners of
   older-revision units are not served revision-specific facts (e.g. the original
   300S takes filter Core 300-RF, not the served Core 300-P-RF); revisit if
   owned-device support for legacy revisions ever becomes a requirement.

## Collection status

Seeded 2026-08-20. Ready2Jet assets consolidated from POC folders; the other four
products collected from official manufacturer sources. Per-product gaps are listed
in each `manifest.json` under `collection_gaps`. The 360-spin audit column
(digital-twin plan Decision 8) is recorded per product in `spin_360`.
