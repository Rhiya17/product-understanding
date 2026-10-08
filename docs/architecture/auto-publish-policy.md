# Automatic publishing policy and evidence rules

*2026-10-07 · In effect for the packs it is run on (currently `tesla-model-y` and `graco-ready2jet-2212125`)*

## Executive summary

- **No person has to approve a claim before ShowMe can show it.** A program, [`system/auto_publish.py`](../../system/auto_publish.py), decides instead, using four checks anyone can re-run.
- **A claim is shown only if all four checks pass:** its quote is really in the source, it is about the exact product, a second, independent AI model agreed the claim says what the quote says, and no other source contradicts it without a rule settling the disagreement.
- **Every decision is written down** in `evidence-packs/<product>/auto-publish-decisions.jsonl`. It names the checks, the verifier receipt, and the rule used. It is labelled as an automated decision, never as a human review.
- **A human decision still wins.** If anyone records a review in `reviews.json` (approve, reject, recheck), that decision overrides the automatic one.
- **Safety warnings go through the same checks** and are attached to answers as before; the policy cannot hide a warning that passes.

## Why this exists

Before this change, a claim could only be shown after a person marked it `APPROVED_FOR_PUBLISH`. The owner does not review claims by hand, so new products (the Tesla Model Y) could never be answered. The checks a reviewer would do can all be done by programs, so they are now a pipeline step.

## The four checks

| Check | What passes | How it is checked |
|---|---|---|
| Source support | Every quote in the claim is found, word for word, in the hash-pinned source file (on the cited page for PDFs) | `PackEvidence.authenticate_binding` in [`system/evidence_status.py`](../../system/evidence_status.py). Image-only sources do not pass. |
| Product match | The claim is about the pack's product. A named SKU must be the product's model number. A superseded body (for example the 2020–24 Model Y) fails. A different market passes only for physical measurements, and only when the vault records a body equivalence (below). | `_product_match` in `auto_publish.py` |
| Independent verification | The latest semantic receipt for this exact claim version says `ENTAILED`, from a `qwen/*` model (never Claude, which wrote the claims), and no meaning-changed alarm is open | Receipts in `evidence-packs/<product>/verification-receipts.jsonl`, written by [`scripts/run_verifier_receipts.py`](../../scripts/run_verifier_receipts.py) under a spend cap |
| No unresolved contradiction | If extraction marked the claim as conflicting with another, an evidence rule below must say this claim may be shown | Conflict groups and their resolutions, in the same decisions file |

A changed claim gets a new digest, so an old approval no longer applies until the checks pass again.

## Evidence rules for conflicting sources

Conflicts are found from the `CONFLICT: contradicts claim_…` notes that extraction must write. They are settled in this order:

| Rule | When it applies | Outcome |
|---|---|---|
| R2 Scope | Each claim describes a different market, body, trim or configuration | Not a contradiction. Each is shown only for its own scope. |
| R3 Unusable | A value cannot be applied: axes not labelled, or only a bound ("less than") | Excluded from answers and from fit calculations |
| R1 Authority | One statement comes from a stronger author. Order: manufacturer documents, then the brand's own account on another site, then independent test measurements, then retailer data, then community posts. The real author (recorded in the claim's `authority_note`) counts, not the website it appeared on. | The strongest is shown; the others are marked superseded |
| R4 Range | Equally strong statements disagree (for example, Tesla's manual says the liftgate opens to about 8 ft on one page and about 7.5 ft on another) | Both are shown together as a range; warnings use the safer value |
| R5 Conservative fit | Any deterministic fit calculation | Uses every non-excluded, verified value: the largest for the object, the smallest for the space |

**Body equivalence (cross-market measurements).** A physical measurement from another market (for example a Chinese tape measurement of a Model Y trunk) applies to the US product only when that market's stated wheelbase, width and height agree with the US manual within 0.5%. For the Model Y this is recorded in `source-vault/tesla-model-y/manifest.json` under `identity.body_equivalence`, citing the claims that state those dimensions.

**Legacy stand-ins are never evidence.** A measurement of a superseded body can be used to draw a 3D scene, labelled as a stand-in, but cannot pass the product-match check or support a confirmed answer.

## How to run it

```sh
.venv/bin/python scripts/run_verifier_receipts.py plan --run-id RUN --cap 0.50 --product tesla-model-y --candidates
# record the run approval (owner, or delegated decision recorded as such), then:
.venv/bin/python scripts/run_verifier_receipts.py execute --run-id RUN --approval-id APPR
.venv/bin/python -m system.auto_publish --product tesla-model-y
```

`--dry-run` prints decisions without writing them.

## Limitations

- **The verifier checks wording, not truth.** A claim that faithfully repeats a wrong number in a source still passes. Conflict rules and fit margins exist to limit the damage.
- **Authority comes from extraction notes.** If the extractor mislabels who wrote a statement, rule R1 can rank it wrongly. The `authority_note` text is checked by the verifier as part of the claim.
- **Only packs it is run on are affected.** Other products still depend on their human reviews.
