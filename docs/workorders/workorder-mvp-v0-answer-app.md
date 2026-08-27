# Work Order: MVP v0 — Local Answer App over Fact Cards and Manuals

**Date issued:** 2026-08-27
**For:** an autonomous agent with repository access (no prior conversation context assumed)
**Depends on:** `system/answer.py` (answer engine, committed `971b5d5`), `evidence-packs/` (claims, reviews, verdicts), `source-vault/` (manifests, manuals, images, video sources), `source-vault/catalog.json`
**Output:** a local web application ("the answer app") that answers product questions from reviewed fact cards, plays official media, and shows illustrated procedure steps rendered from the manuals — plus tests, docs, and per-phase commits
**Explicitly out of scope:** any generative model in the serving path (no Seedance, no VACE, no image generation), any cloud hosting, any change to `claims.json`, `reviews.json`, `verdicts.json`, or any file under `source-vault/` other than reading it.

---

## 0. Governing rules (read first; these override convenience)

1. **Serve only what is published.** The default serving set is claims whose
   status per `system/answer.py` is `PUBLISHED` (latest human disposition
   `APPROVED_FOR_PUBLISH`, no outstanding `MEANING_CHANGED` verdict). Reuse
   `system.answer.search()`; do not reimplement status logic.
2. **Preview is labeled, off by default, and visually unmistakable.**
   `CANDIDATE` and `SUSPENDED` content may appear only behind a UI toggle
   named "Internal preview", each card carrying its status label. `REJECTED`
   content never renders anywhere.
3. **Never invent pixels or motion.** Every image shown is either a file in
   `source-vault/` or a page rendered from a vault PDF. Every video is an
   origin URL registered in a vault manifest. Nothing else.
4. **Media requires owner approval before default serving.** A media binding
   (claim ↔ asset link) drafted by the agent serves only in preview until the
   owner approves it (§3). The agent never sets the approval field.
5. **Local-first.** Python 3.12, no cloud services, no telemetry, no network
   calls made by the server at runtime. The browser may load registered
   origin URLs (e.g., an official video embed); the server itself must not.
6. **Stop-and-report conditions:** any rule above would be violated; a needed
   fact is missing from the packs; a source file fails its manifest hash.
   Report; do not improvise.

## 1. Phase 1 — Web app over the answer engine

**Build** `app/` at the repository root:

- `app/server.py` — Python 3.12 standard library only (`http.server`). No
  new dependencies for this phase. Flags: `--port` (default `8765`),
  `--packs-root`, `--vault-root` (defaults: repo layout).
- Endpoints:
  - `GET /` → `app/static/index.html` (plus any static CSS/JS files; no CDN
    or external assets).
  - `GET /api/answer?q=<question>&preview=<0|1>&product=<dir|empty>&top=<n>`
    → JSON `{question, results, not_served}` exactly as returned by
    `system.answer.search()`.
  - `GET /api/products` → the catalog product list (id, dir, brand, model,
    category).
- UI (single page): a question input; a product dropdown ("All products" +
  the five); answer cards showing status badge, product, predicate, tier,
  the rendered answer, and each citation as the quote plus a link to
  `origin_url`; the "not served" notice with counts; the Internal-preview
  toggle per rule 2.
- Errors: empty question → HTTP 400 with a JSON error; unknown product →
  HTTP 404; all other failures → HTTP 500 with a JSON error and no stack
  trace in the response body.

**Tests** in `app/tests/test_server.py`: exercise the JSON API against a
temporary fixture pack (copy the fixture pattern from
`system/tests/test_answer.py`), covering: published-only default, preview
flag behavior, product filter, empty-question 400. Tests must not bind a
fixed port (use port 0) and must not depend on repository pack contents.

**Expected outcome (acceptance):** `python3.12 app/server.py` then opening
`http://localhost:8765` and asking "what is the max child weight for the
snugride?" renders one PUBLISHED card: 30 lb, the manual quote, a working
link to the Graco PDF. `python3.12 -m pytest -q system/tests app/tests`
passes. Commit checkpoint.

## 2. Phase 2 — Official media wired to claims

**Schema.** Create `evidence-packs/<product>/media-bindings.json`:

```json
{
  "bindings": [
    {
      "binding_id": "mb_<product_short>_<slug>",
      "claim_ids": ["claim_..."],
      "source_id": "src_...",
      "kind": "IMAGE" | "VIDEO_URL" | "PDF_PAGE",
      "page": null,
      "start_seconds": null,
      "end_seconds": null,
      "rationale": "one sentence: why this asset answers these claims",
      "proposed_by": "agent",
      "approved_by": null
    }
  ]
}
```

Rules: `source_id` must exist in that product's vault manifest;
`claim_ids` must exist in that product's `claims.json`; `page` is required
and 1-based when `kind` is `PDF_PAGE`; `start_seconds`/`end_seconds` are
optional integers for `VIDEO_URL`. `approved_by` is written only by the
owner (their email), never by the agent.

**Draft the bindings** for all five products from the vault manifests and
`videos/video-sources.md` files. Bind conservatively: only assets whose
manifest entry or curation log identifies the exact product; when unsure,
omit and list the omission in the phase report. Expected volume is small
(roughly 10–30 bindings total).

**Validator.** Add `evidence-packs/validate_media.py` enforcing every rule
above, wired into CI next to the existing validators, with offline tests.

**Serving.** Extend `/api/answer`: each result gains a `media` array of its
approved bindings (id, kind, local file path or origin URL, page,
start/end). The UI renders images inline (served read-only from
`source-vault/` via a `GET /media/...` route that refuses paths outside the
vault), and renders video bindings as an embedded player or link using the
origin URL and start time. Unapproved bindings appear only when Internal
preview is on, labeled "media awaiting owner approval".

**Expected outcome (acceptance):** with preview on, "how does the stroller
fold?" shows the fold-step cards plus the official Graco fold-sequence
image and fold video reference, each labeled awaiting approval; validators
and all tests pass. After the owner writes `approved_by`, the same media
serves by default with no code change. Commit checkpoint, plus a short
`docs/workorders/report-mvp-v0-phase2.md` listing every binding and every
omission for the owner's approval pass.

## 3. Phase 3 — Illustrated procedure player (manual pages, real steps)

**Goal:** for any procedure in the packs (claims of type `STEP`, grouped by
`object.procedure`, ordered by `object.step_number`), a "Show me" view:
step text on one side, the manual page that step cites on the other,
Previous/Next controls.

- **Page images:** render pages from vault manual PDFs with `pypdfium2`
  (add to `system/requirements.txt`, pinned). Cache renders under
  `app/cache/` (add to `.gitignore`). Render at 144 DPI. The page number
  comes only from the step's `PDF_PAGE` media binding (Phase 2 schema); if
  a step has no page binding, show the step text alone — never guess a
  page.
- **No cropping, no annotation, no synthesized frames.** v0 shows whole
  authentic pages. Highlighting and motion come later.
- **Endpoint:** `GET /api/procedure?product=<dir>&procedure=<name>` →
  ordered steps `{step_number, action, claim_id, status, page_image_url}`.
  Procedure discovery: `GET /api/procedures?product=<dir>`.
- Serving policy applies per step (rule 1): unpublished steps render only
  in preview, labeled. If any step of a procedure is unpublished, the
  procedure view shows a banner: "This procedure is not fully published."

**Tests:** step grouping/ordering, the no-page fallback, path safety on the
page-image route, and one PDF render smoke test against a fixture PDF
committed under `app/tests/fixtures/` (a small generated PDF, not a vault
file).

**Expected outcome (acceptance):** with preview on, selecting the stroller's
fold procedure walks the real fold steps in manual order beside the true
manual pages. All validators, all tests (`system/tests` + `app/tests`), and
CI pass. Commit checkpoint and a final report
`docs/workorders/report-mvp-v0.md` with: what was built, the demo script
(exact questions to type and what appears), binding counts, omissions, and
known gaps.

## 4. Definition of done

1. Three phase commits plus reports as specified; repository clean;
   `python3.12 -m compileall`, both validators, media validator, and the
   full test suite green.
2. The demo script in the final report works exactly as written on a fresh
   checkout with `python3.12 app/server.py`.
3. No file under `source-vault/` modified; `claims.json`, `reviews.json`,
   `verdicts.json` untouched; no `approved_by` field set by the agent.
4. The served experience contains zero generated imagery or motion.
