# Extraction Systematization: Findings from the Five-Product Run

**Date:** 2026-08-24
**Status:** Findings from a completed experiment; input to the build decision
**Companion:** `docs/workorders/evidence-pack-extraction-workorder.md` (the work executed),
`docs/planning/agentic-source-collection.md` (the sibling system this parallels),
`evidence-packs/workorders/` (the machine-readable contracts this run produced)

## 1. The question and the answer

The question: **is claim extraction predictable enough to automate?** The v1
Ready2Jet pilot said no — it took human-style iteration to catch a fabricated
step, and the deterministic validator at the time verified shape, not truth.

The answer after this run: **yes — build the automated extraction
orchestrator.** Five extractions ran against a hardened deterministic gate
(one per product, in parallel, plus a Ready2Jet top-up). All five converged,
the gate's traps demonstrably fire on the failure modes that burned v1, and
the judgment calls that remain are now enumerated and fall into categories a
system can route rather than resolve.

## 2. What was built for the run (and is now standing infrastructure)

1. **Machine-readable work orders** — `evidence-packs/workorders/<product>.json`:
   per-type claim floors, total-count band, mandated conflict pairs, and a
   checklist where every item must end as claims or a recorded gap.
2. **The hardened gate** — `evidence-packs/validate.py`:
   - *Anti-fabrication:* every quote must literally appear in the cited local
     source (PDF page; whole file for markdown/HTML; whole-PDF fallback when
     no page is cited).
   - *Anti-hallucination:* non-null bounding boxes hard-fail unless
     `annotation_status: "MEASURED"`.
   - *Contract enforcement:* floors, bands, conflicts, checklist coverage.
   - *Honest-gap protocol:* `gaps.json` waivers typed as `SOURCE_MISSING` /
     `UNDERIVABLE` / `NOT_EXTRACTED`, each with reason and `closes_when`.
   - One `SUMMARY_JSON` telemetry line per pack.
3. **The standing agent brief** — `workorders/extraction-agent-brief.md`: the
   prompt contract an orchestrator sends with each work order.

**Trap verification before trusting the gate:** three synthetic bad claims
were injected into a scratch copy of the v1 pack — a fabricated quote (the
exact "push frame downward" failure mode from v1), an estimated bounding box,
and a real quote cited to the wrong page. All three hard-failed; all 26
legitimate claims passed. The baseline run also confirmed the contract layer:
the v1 pack, which passed the old validator, failed the new gate with 11
errors for precisely its known shortfalls (26 < 40 claims, zero SPEC, no
coverage map).

## 3. Results

| Product | Claims | Ceilings (C3/C2/C1/C0) | Gaps | Quotes verified | Unverifiable | Runs to green |
|---|---:|---|---:|---:|---:|---:|
| Graco Ready2Jet (79 = 26 v1 + 53 v2) | 79 | 39/6/25/9 | 3 | 80 | 0 | 1 |
| Graco SnugRide Lite LX | 90 | 85/1/0/4 | 5 | 99 | 1 (image) | 1 |
| Bose QC Ultra 2nd Gen | 59 | 9/7/28/15 | 5 | 58 | 1 (URL-only) | 1 |
| Apple MacBook Air 13 M3 | 33 | 0/0/6/27 | 1 | 47 | 0 | 1 |
| Levoit Core 300S | 57 | 6/15/20/16 | 3 | 64 | 2 (image) | 1 |
| **Total** | **318** | | **17** | **348** | **4** | |

All five packs pass the full gate with 0 errors. Two benign warnings remain
(legitimately shared quotes). Everything is `CANDIDATE`; nothing is promoted.

**Conflicts recorded (the protocol working on real data):**
- SnugRide: the mandated 30 lb / 35 lb child-weight conflict (current manual
  vs legacy gallery-image overlay) — recorded, unresolved, per contract.
- Bose: two conflicts nobody planted, inside Bose's own owner's guide —
  status-light duration (5 s vs 10 s across pages) and quick-charge playback
  (3 h body text vs 2.5 h test footnote on the same page).
- Levoit: four 300S vs 300S-P revision conflicts — product weight
  (5.95 → 7.48 lb), rated power (23 → 39 W), noise (50 → 54.5 dB max),
  filter model (Core 300-RF → Core 300-P-RF).

**Notable single finding:** the SnugRide manual PDF's text layer contains a
leftover editor's note ("I hope marketing doesn't point out the fact that the
base is facing the wrong way here…") — flagged in that pack's report, not
extracted.

## 4. Why "all first-run green" is the result, not the absence of one

No agent ever saw a FAIL line — every agent read the validator first, dumped
source text with the validator's own extractor (pypdf), and composed quotes
from that dump. The gate did its work *upstream*, by being cheap, local, and
exactly reproducible: it converted "be careful about quotes" from advice into
a mechanical procedure agents self-apply. That is the property an automated
system needs — convergence without a human in the retry loop. (The traps
themselves are proven by the synthetic injection test, §2.)

## 5. The judgment surface (what still needed a mind)

Telemetry across the five runs shows the judgment calls cluster into five
categories. This list is the automation frontier — the orchestrator routes
these; it does not resolve them:

1. **Source pathology.** The Levoit 300S manual has *no usable text layer*
   (CID fonts; zero extractable characters from both vault copies) — the
   agent read it visually and bound claims to the mechanically verifiable
   300S-P series manual + spec page, recording the situation as a gap.
   Related: pypdf ligature/kerning artifacts kept verbatim in quotes (Bose,
   Levoit, SnugRide), icon glyphs vanishing from step text, graphical
   chart semantics (SnugRide's ✓/– columns) not derivable from text alone.
2. **Binding policy edges.** URL-only sources with no local capture (Bose
   Bluetooth 5.4 — one deliberate exception, flagged; everything else became
   a gap, not a claim), quotes transcribed from images (SnugRide's legacy
   35 lb overlay — mechanically unverifiable by design), authority mapping
   when no classic manual exists (MacBook).
3. **Conflict vs absence vs wording variance.** A dropped spec row is an
   absence, not a conflict (Levoit CADR); a footnote disagreeing with body
   text is a conflict (Bose); a renamed filter with identical contents is
   wording variance (Levoit).
4. **Consequence-tier escalations.** When-unsure-go-higher applied
   repeatedly (SnugRide buckle CARE → C3; Bose serial-number location → C2);
   each escalation is noted on the claim for the reviewer.
5. **Scope discipline.** Staying inside the count band by recording
   NOT_EXTRACTED gaps instead of thinning facts (SnugRide harness-height
   sections; Ready2Jet 3-point-conversion).

## 6. Residual risks the gate cannot catch

- **Value–quote mismatch:** a real quote paired with a misread
  `object.value`. A 10-claim cross-pack spot audit found 0 mismatches, but
  the gate is structurally blind to this. Mitigation for the system: a
  cheap second-agent verifier that checks `object` against `quote` per claim
  (mechanizable; this is the extraction analog of the POC-verifier work).
- **Quote-supports-claim semantics:** the quote exists but doesn't actually
  entail the claim. Same mitigation; also what human review is for.
- **Image-bound quotes** (4 across 318 claims) are counted and flagged but
  unverifiable until visual annotation/OCR exists.
- **False conflicts.** Human review (2026-08-24) resolved all 7 recorded
  conflict pairs; one proved to be no conflict at all — the Bose
  connected-light "5 s vs 10 s" pair describes two different trigger events
  (status-check display vs connection event), visible only in the cited
  pages' surrounding context, not in the quotes themselves. Implication for
  the system: conflict triage needs page-context, not just quote comparison —
  a natural job for the value–quote verifier stage. Recording it as a
  conflict was still correct extractor behavior (record, don't resolve).
- **Promotion is human by design.** Nothing here touches CANDIDATE→PUBLISHED.

## 7. What the automated system looks like (build spec)

**Decided 2026-08-24 (with the project owner): the system is a four-stage
pipeline, and the cross-family verifier is a first-class stage, not an
add-on.** The stages, in the owner's framing:

| # | Stage | Actor | Catches |
|---|---|---|---|
| 1 | **The Detective** — extraction | Claude agent (brief + work order JSON) | reads sources, writes CANDIDATE claims + honest gaps |
| 2 | **The Guard Dog** — deterministic gate | `validate.py` | fabricated/mis-cited quotes, estimated bboxes, contract shortfalls, schema |
| 3 | **The Verifier** — cross-examination | **Qwen3** (different model family, deliberately) | meaning drift: quote is real but the translation (object/step) changed what it says |
| 4 | **The Judge** — human review | reviewer via `reviews.json` | conflicts, C2/C3 promotion, policy decisions |

**Stage 3 design (decided):**
- **Model: Qwen3.** Rationale on record: (a) independence — the extractor is
  Claude-family, and correlated blind spots defeat the purpose; (b) the
  vlm-verifier POC already showed Qwen3-VL catching a meaning-level error
  (wrong-way fold) that Claude missed, 6/6 vs 5/6; (c) it is already the
  project's designated verifier ("continue as first review step") with
  working integration code (`poc-seedance-keyframe-fold/verify_with_vlm.py`),
  giving one verifier stack for claims and video; (d) the Koustubh
  fine-tuning question (25–100 labels) then applies to both uses; (e) open
  weights, trivial per-sweep cost at this volume.
- **Blind and adversarial.** The verifier receives ONLY (quote, translated
  object/step, claim type) — no extractor notes, no rationale — and is
  prompted to refute: "assume the translation changed the meaning; prove it."
- **Output is a machine-checkable artifact**: `verdicts.json` per pack, one
  verdict per source binding — `{claim_id, binding_index, verdict:
  ENTAILED | MEANING_CHANGED | CANNOT_JUDGE, note}` — validated by the gate
  like gaps.json and reviews.json.
- **Routing respects consequence tiers**: C0/C1 + ENTAILED →
  auto-approvable; ANY MEANING_CHANGED → loud alarm, straight to the human
  queue regardless of tier; C2/C3 + ENTAILED → still human-reviewed, but the
  verifier's verdicts order and annotate the queue (the read-through becomes
  "read the flagged ones first"). Promotion stays human for C2/C3 by design.
- **Second job, same stage:** conflict triage with page context (§6's false-
  conflict finding) — hand the verifier both quotes plus their surrounding
  page text and ask whether they genuinely contradict.

The orchestrator (Claude Agent SDK or equivalent) is small and deterministic:

```
for product in catalog:
    workorder = evidence-packs/workorders/{product}.json
    loop (max N):
        agent(brief + workorder)          # 1 Detective: claims.json, gaps.json
        result = run(validate.py, pack)   # 2 Guard Dog: deterministic gate
        if result.errors == 0: break      # feed FAIL lines back otherwise
    verdicts = qwen_verify(pack)          # 3 Verifier: blind entailment per binding
    alarm on MEANING_CHANGED              #   any tier -> human, loudly
    queue = order(C3+conflicts first, verifier-annotated)   # 4 Judge: human
    collect SUMMARY_JSON + verdict stats  # telemetry
```

Additions worth building with it, in order:
1. **Text-layer health check + orphan-file check at collection time**
   (`validate_vault.py`): the Levoit no-text-layer pathology and the Bose
   unregistered-specs.md pathology should both be caught when a source
   enters the vault, not discovered at extraction. Requirements flowing
   *back* into the source-collection system design.
2. **Stage 3 verifier** as specced above — buildable and useful immediately,
   standalone, against the five existing packs (before the orchestrator
   exists): it collapses the pending C3 read-through into a flagged-first
   queue.
3. **Reviewer queue ordering:** C3 + conflicts first, verifier-annotated
   (make it an artifact, not a sentence).

## 8. Housekeeping surfaced by the run (needs human decision)

- ~~catalog `compatibility_pairs` and the SnugRide manifest carried the old
  `prod_graco_snugride_35_lite_lx` id~~ FIXED 2026-08-24 (human-approved):
  both renamed to `prod_graco_snugride_lite_lx`, logged in the manifest
  `curation_log`; zero dangling identifiers remain. The extraction report's
  judgment-call note about the mismatch stands as history.
- Ready2Jet still has no spec source (`gap_specs_1`); closes with
  `docs/workorders/workorder-ready2jet-gap-closure.md` Task 1 (`specs/specs.md`), after
  which SPEC claims can be topped up and the type floor raised.
- ~~The uncaptured Bose spec pages block several SPEC facts~~ CLOSED
  2026-08-24: `specs/specs.md` turned out to exist on disk unregistered;
  registering it + a fresh product-page HTML capture closed the
  bluetooth/weight/lossless gaps (5 new claims). Remaining: the support
  specifications article serves only a JS shell over HTTP — raw capture
  needs a browser session (`gap_spec_article_raw_capture_1`); SBC/AAC codec
  list is genuinely unpublished (`gap_codecs_1` stands).
- **Validator gap found during closure:** `validate_vault.py` verifies every
  manifest entry has a correctly-hashed file, but NOT the reverse — an
  on-disk file with no manifest entry (the Bose `specs/specs.md` case) passes
  silently, and unregistered sources are invisible to extraction. Add an
  orphan-file check (fits the text-layer health check already queued for the
  collection system, §7 item 1).
