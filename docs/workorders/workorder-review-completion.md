# Work Order: Review Completion — CANDIDATE to Servable

**Date issued:** 2026-08-25
**For:** an autonomous agent with repository access (no prior conversation context assumed), working with the product owner (vijayp.cmu@gmail.com), who is the only party allowed to make publish decisions
**Depends on:** `evidence-packs/` (5 products, 356 CANDIDATE claims), `system/` (orchestrator, verifier, review-queue tooling — all built and tested), `system/README.md` (stage commands and exit codes)
**Output:** every claim carries a human disposition in its pack's `reviews.json`; per-pack completion report; the packs become the servable Evidence Graph for the answer layer

---

## Execution status (2026-08-26)

- Preflight audit completed. A bundled Python 3.12.13 runtime was used because
  `python3.12` is not installed on the host PATH.
- Offline suite: **22 passed**. Evidence-pack and source-vault validators both
  exit 0.
- The verifier was changed to advisory-only for this pass. It cannot write
  `reviews.json`; the queue derives batch eligibility from complete all-ENTAILED
  verdict sets and chooses a reproducible five-claim spot-audit sample.
- Pre-call projection: **$0.0429** for 389 text-binding requests plus 8
  conflict-triage requests, before any malformed-output retries. This is below
  the $9.99 ceiling.
- `FAL_KEY` was supplied for an ephemeral process environment. The preflight
  found that fal retired the configured `fal-ai/any-llm/vision` route (HTTP
  422); the current documented `openrouter/router/vision` route passed a live
  schema check. The pinned Qwen model and prompt remain unchanged.
- Phase A completed: all **392 bindings** now have verdicts — 86 `ENTAILED`,
  303 `MEANING_CHANGED`, and 3 expected visual `CANNOT_JUDGE`. Eight conflict
  pairs were triaged (5 `GENUINE_CONFLICT`, 3 `DIFFERENT_SCOPE_OR_EVENT`).
  Regenerated queues contain 268 alarm claims and 38 batch-eligible C0/C1
  claims. This measured result supersedes the pre-run workload estimate below.

---

## 1. Objective and the one governing rule

Take all 356 claims from `CANDIDATE` to a decided state so the answer layer
can serve from them. The governing rule is unchanged from the LLD:
**the agent never decides publication.** This completion pass intentionally
tightens the older verifier auto-approval policy: the agent runs machinery, drafts
recommendations, and transcribes confirmed decisions; the human makes every
disposition. Any `reviews.json` entry must trace to an explicit human
confirmation. C2/C3 claims (child-safety limits, installation procedures)
are never batch-confirmed — the human sees each one.

## 2. Current state (measured 2026-08-25)

| Pack | Claims | C0 | C1 | C2 | C3 | Human decisions so far |
|---|---|---|---|---|---|---|
| graco-snugride-35-lite-lx | 108 | 4 | 0 | 1 | 103 | 2 |
| graco-ready2jet-2212125 | 94 | 9 | 30 | 6 | 49 | 1 |
| bose-qc-ultra-headphones | 64 | 20 | 28 | 7 | 9 | 7 |
| levoit-core-300s | 57 | 16 | 20 | 15 | 6 | 8 |
| apple-macbook-air-13-m3 | 33 | 27 | 6 | 0 | 0 | 0 |
| **Total** | **356** | **76** | **84** | **29** | **167** | **18** |

Stage 3 verification is essentially unrun: 3 verdicts exist repo-wide
(all `CANNOT_JUDGE` on visual bindings). Queues therefore currently route
all C0/C1 claims to section 5 ("Unresolved verifier") instead of section 7
("Batch-eligible C0/C1 spot-audit"). Running the verifier first is what makes
the human workload tractable: up to 160 C0/C1 claims move from "human must
read" to "spot-audit a sample, then explicitly confirm the clean batch."

## 3. Phases

### Phase A — Run the verifier fleet (agent, ~1 hour, < $10)

1. Preconditions: `FAL_KEY` in the process environment (never in files or
   argv); `python3.12 -m pytest -q system/tests` green before spending.
2. Run per pack, checking exit codes (`0` complete, `10` semantic alarms,
   `20` partial, `30` credentials, `40` malformed output):

   ```bash
   python3.12 system/verify_claims.py --product <product>
   python3.12 system/verify_claims.py --product <product> --conflicts
   ```

3. Budget stop: the README expects single-digit dollars for a five-pack
   run. Before the first provider call, calculate the projection from all
   uncached prompts with `verify_claims.estimated_cost`; if it exceeds $9.99,
   stop and report. Also stop if the running estimate exceeds that ceiling —
   do not proceed.
4. `CANNOT_JUDGE` on visual bindings is an expected outcome, not an error;
   those claims fall to the human queue.
5. Regenerate all queues: `python3.12 system/review_queue.py`.
6. Commit verdicts + regenerated queues as one checkpoint.

### Phase B — Draft review proposals (agent, one session)

Produce `evidence-packs/<product>/review-proposals.md` — a **proposal
document, never `reviews.json`** — mirroring the queue's order. For each
claim needing a decision:

- the claim, its quote, source, tier, and verifier verdict;
- a recommended disposition (`APPROVED_FOR_PUBLISH` / `REJECTED_FOR_SERVING`
  / `NEEDS_RECHECK`) with a one-sentence rationale;
- apply standing policies when drafting: latest-revision-only (older
  hardware revisions → `REJECTED_FOR_SERVING`, kept as CANDIDATE records —
  precedent: `rev_c300s_revision_policy_*` in the Levoit pack); every
  documented procedure must end up servable in some form (procedures feed
  video generation — a rejected procedure claim needs a rework path, not
  silence);
- flag anything the human must look at hard: verifier FAIL or
  `MEANING_CHANGED`, quote/object mismatches, applicability doubts
  (SKU/market/revision), and every C3.

Also draft the section-7 five-item deterministic spot-audit sample (the queue
tooling defines it by stable SHA-256 rank)
for batch-eligible C0/C1 claims.

### Phase C — Human decision pass (product owner, ~half a day)

Owner works through each pack's proposals top-to-bottom:

- **Undecided C3/C2 (191 claims):** confirm or override each recommendation
  individually. With drafted rationales this is ~1 minute per claim;
  the two Graco packs are the bulk (156 of the 191).
- **Conflicts / alarms / CANNOT_JUDGE:** decide each.
- **C0/C1 that passed verification:** review only the spot-audit sample;
  if the sample is clean, confirm the batch in one statement; if any sample
  item fails, the batch loses batch eligibility and is reviewed individually.
- Confirmation format: the owner marks each item (or batch statement) in
  the proposals file or in conversation; anything unmarked is undecided,
  not approved.

### Phase D — Transcribe, validate, close (agent, ~1 hour)

1. Write confirmed decisions into each pack's `reviews.json`, matching the
   existing record shape (`review_id`, `date`, `reviewer` =
   `vijayp.cmu@gmail.com`, `scope`, `claim_id`, `disposition`,
   `rationale`). Never edit `claims.json` or `verdicts.json`.
2. Re-run the gates: `python3.12 evidence-packs/validate.py`,
   `python3.12 scripts/validate_vault.py`, `python3.12 -m pytest -q
   system/tests`; regenerate queues (sections should drain to zero except
   documented leftovers).
3. Write `evidence-packs/<product>/review-completion-report.md`: counts by
   disposition, rejected-with-reason list, open `NEEDS_RECHECK` items, and
   the resulting servable-claim count.
4. Commit.

## 4. Acceptance criteria

- Every one of the 356 claims has exactly one current disposition or an
  explicit `NEEDS_RECHECK` follow-up; no claim silently undecided.
- No disposition exists without a traceable human confirmation; no
  batch-confirmed C2/C3.
- All validators and offline tests green; queues regenerate clean.
- Reports exist per pack; total servable count stated.

## 5. Schedule and cost

| Phase | Who | Effort | Cost |
|---|---|---|---|
| A — verifier fleet | agent | ~1 h wall clock | < $10 (hard stop) |
| B — proposals | agent | one session | model usage only |
| C — decisions | human | ~3–5 h focused | — |
| D — transcribe + close | agent | ~1 h | — |

Elapsed: comfortably **2–3 days**; a single focused day if Phase C is done
in one sitting. The critical path is the owner's Phase C time.
