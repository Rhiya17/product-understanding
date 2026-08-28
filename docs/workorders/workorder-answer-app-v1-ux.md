# Work Order: Answer App v1 — From Fact Browser to Product

**Date issued:** 2026-08-28
**For:** an autonomous agent with repository access (no prior conversation context assumed)
**Depends on:** `app/` (server, static UI, tests), `system/answer.py` (search + procedure composition), `evidence-packs/` (claims, reviews, gaps, media-bindings, derived-assets), expert review of 2026-08-28 (recorded in this document's problem statements)
**Format:** each item states the PROBLEM, FIX OPTIONS (pick one — you decide, and record the choice + reason in the final report), and the EXPECTED OUTCOME, which is the acceptance test. Outcomes are binding; implementations are yours.
**Spend:** $0 external. No generative model calls in the serving path. All 55 existing tests stay green; each item adds at least one test pinning its outcome.

---

## 0. Global rules

1. Serving policy is unchanged: REJECTED never serves; the MVP exception
   (labeled pending facts by default) stays until the owner review pass.
2. Every displayed answer keeps a visible path to its evidence (quote +
   source). No item below may weaken traceability while improving looks.
3. `claims.json` and `verdicts.json` stay read-only. Item 2 writes
   `reviews.json` through the existing record shape only.
4. Commit per item or per coherent group; stop-and-report if an outcome
   cannot be met within its effort band.

## 1. Answers should read like answers (UI-1) — MUST

**Problem.** Cards lead with storage internals: `value: 30 | unit: lb`,
headings like "procedure step", meta rows like `Tier C3 ·
claim_srl_limit_max_weight_current`. The user reads a database row, not an
answer.

**Fix options (choose):**
- (a) A deterministic renderer per claim `type`/predicate family (SPEC,
  LIMIT, WARNING, STEP, COMPATIBILITY…) producing one lead sentence from
  the object fields — template-based, no model calls; unknown shapes fall
  back to the current rendering.
- (b) Add a precomputed `display_text` to search results in
  `system/answer.py` with the same template logic, so CLI and app share it.
- (c) Either of the above plus a "Details" disclosure that hides tier,
  claim id, and raw fields until expanded.

**Expected outcome.** The SnugRide weight question leads with a bold
human sentence (e.g. "Maximum child weight: 30 lb (13.6 kg)"); no raw
`key: value` strings, claim ids, or tier codes visible on a collapsed
card; quote + human source name remain visible. Test: rendered payload/DOM
for at least SPEC, LIMIT, WARNING, and STEP claims.

## 2. Owner review mode (PM-2) — MUST

**Problem.** The 338-decision review backlog lives in markdown files far
from where the facts are seen. Reviewing has stalled; the whole serving
policy waits on it.

**Fix options (choose):**
- (a) An "Owner review" toggle in the app: pending cards gain
  Approve-for-publish / Reject-for-serving / Needs-rework buttons posting
  to a new endpoint that appends well-formed records to that pack's
  `reviews.json` (reviewer = the owner email from a `--reviewer` server
  flag; refuse to write when unset).
- (b) A dedicated `/review` page that walks the existing review-proposals
  order queue-style, same write path.
- (c) Either, plus a progress indicator (decided / total per pack).

**Guardrails (not optional):** writes are append-only and atomic; each
record matches the existing schema (`review_id`, `date`, `reviewer`,
`scope`, `claim_id`, `disposition`, `rationale` — rationale optional free
text from a small input, defaulting to "approved via app review mode");
C2/C3 claims require an explicit per-claim click (no bulk approve at those
tiers); a bulk action is allowed only for C0/C1. The UI must state that
decisions are recorded to the pack.

**Expected outcome.** The owner can open the app, flip to review mode, and
decide claims where they see them; decisions appear in `reviews.json`,
survive server restart, immediately change serving status, and the
evidence-pack validator stays green. Test: end-to-end approve + reject on
a fixture pack via the API, including the C3 no-bulk rule.

## 3. Search-first layout (UI-3) — MUST

**Problem.** The hero headline occupies most of the first viewport; after a
search, answers land below the fold and the page must be scrolled every
time.

**Fix options:** collapse the hero to a slim bar after the first query
(CSS class swap), or pin a compact search header and move the hero to an
empty-state only. Either way, no layout jump that loses the user's scroll
position on subsequent searches.

**Expected outcome.** After any search, the first answer card is visible
without scrolling at 1280×720; the search box remains reachable at top.

## 4. One honesty banner, quieter chips (UI-4) — SHOULD

**Problem.** "Pending review" appears as a page banner, a full-width badge
per card, a chip per step, and a media banner — four repetitions of one
fact, drowning the content.

**Fix options:** keep the single page-level banner; reduce card badges to a
compact dot+word chip; per-step chips only when a step's status differs
from the card's; media banner folded into the media caption line.

**Expected outcome.** The fold answer shows the pending state exactly once
at page level and once per card at most; steps with the same status as the
card carry no individual chip. Traceability text (quote, source) untouched.

## 5. No orphan fragments (UI-5) — SHOULD

**Problem.** Non-composed step cards render as "procedure step" with no
procedure name (e.g. the car-seat prep step under a fold question), and
sibling context is invisible.

**Fix options:** title such cards "Step N of <readable procedure name>"
with a link/button that opens the procedure player at that procedure; or
compose even single-step matches into a collapsed procedure card showing
the matched step expanded.

**Expected outcome.** No card titled bare "procedure step"; every step
shown names its procedure and one click reaches the full ordered view.

## 6. Media and dropdown polish (UI-6) — SHOULD

**Problem.** The fold video renders as a black rectangle until played (no
poster); every procedure option carries "· not fully published" — pure
noise while the whole catalog is pending.

**Fix.** Poster frame for `VIDEO_FILE` players (first frame extracted
server-side and cached, or `preload="metadata"` if it renders a frame);
suffix the dropdown only when publication state is mixed, otherwise rely on
the page banner.

**Expected outcome.** The video area shows an image before play; the
procedure dropdown reads clean; suffix returns automatically for partially
published procedures (test with a fixture where one step is approved).

## 7. Honest misses and guided starts (UI-7 + PM-3) — SHOULD

**Problem.** A miss renders a bare "No answers matched." — although
`gaps.json` often knows *why* ("source missing", "not documented"), and the
empty state gives no examples to try.

**Fix options:** on zero results, query the matched product's `gaps.json`
for token overlap and render "We don't have a verified answer for this —
recorded gap: <reason>" when one matches, else the plain miss line plus
2–3 clickable example questions (drawn from a small static list per
product, or generated from top predicates).

**Expected outcome.** A question that hits a recorded gap says so with the
gap's reason; the landing empty state offers clickable example questions
that run a search when clicked.

## 8. Serve the derived visuals (PM-5) — SHOULD

**Problem.** The Levoit and MacBook photo-projected turntables and the twin
fold renders are registered in `derived-assets.json` but the media schema
has no lane for derived assets, so the app cannot show them.

**Fix options:** extend `validate_media.py` + serving with a
`DERIVED_ASSET` binding kind that references a `derived-assets.json` entry
(provenance id, watermark required, label from the asset's `label` field);
or serve directly from `derived-assets.json` entries carrying a
`claim_ids` list added there. Either path: unapproved derived assets serve
only under the MVP-exception labeling, `approved_by` stays owner-only, and
the internal-only watermark must remain visible.

**Expected outcome.** "What does the Levoit look like?" (or its product
page in the app) shows the watermarked turntable with its label and
provenance-backed caption; validators cover the new lane; nothing serves
without either owner approval or the pending label.

## 9. Feedback intake (PM-6) — NICE

**Problem.** No way to flag a wrong answer; the architecture's correction
pipeline has no intake from the UI, and no record exists of asked-but-
missed questions.

**Fix options:** a "Report an issue" control per card appending to a local
`app/feedback.jsonl` (question, claim_id, timestamp, optional note); plus
an opt-in local log of zero-result questions to the same file. No network,
no PII beyond what the user types.

**Expected outcome.** Reports and misses accumulate in one local file the
owner can read; a test covers the endpoint.

## 10. Ambiguity guard (PM-4) — NICE

**Problem.** With one product per category the matcher cannot be ambiguous,
but the failure mode (two strollers → interleaved wrong-product steps) is
already known and cheap to prevent.

**Fix.** When top-scoring products tie and the question names no specific
product, return a `clarify` payload listing candidates; UI renders "Which
product did you mean?" buttons that re-run the query filtered.

**Expected outcome.** A fixture catalog with two same-category products
yields the clarification response instead of mixed results; today's
catalog behavior is unchanged (test both).

## 11. Definition of done

1. MUST items 1–3 complete; SHOULD items complete or individually
   reported with a concrete blocker; NICE items as time allows.
2. Every item's expected outcome has a passing test; full suite green;
   validators green; repo clean.
3. Final report `docs/workorders/report-answer-app-v1.md`: per-item chosen
   option + why, screenshots (before/after for items 1, 3, 4), and the
   remaining known gaps.
4. The demo script: fold question, SnugRide weight question, a gap-hitting
   question, and an owner-review approve → the approved card serving
   unlabeled — all working on a fresh `python3 app/server.py`.
