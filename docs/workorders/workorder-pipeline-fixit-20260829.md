# Work Order: Fix-it pass on the question→video pipeline build

**Date issued:** 2026-08-29
**For:** the agent that implemented
`workorder-question-to-video-pipeline.md` (review found one critical defect
and four gaps). Work through the tasks **in order**; Task 1 blocks everything
else. Do not start the live acceptance run (Task 8) until Tasks 1–7 are done
and the full test suite passes.

**Standing rule (new, applies forever):** a mocked or stubbed run must NEVER
write to the real `evidence-packs/`, `generated-assets/`, or
`source-vault/` trees. All tests and mock runs operate on `tmp_path`
fixture copies only. Fabricated provenance in the trust store is the single
worst failure this system can have.

---

## Task 1 — CRITICAL: purge the mock artifacts from the real pack

The mocked "acceptance run" registered fake artifacts with fabricated
provenance (`request_id: "mock_req_123"`, verdicts reading "Looks good").
Remove every trace:

1. In `evidence-packs/bose-qc-ultra-headphones/derived-assets.json`: delete
   the asset `derived_generated_connect_aux_cable_walkthrough`.
2. In `evidence-packs/bose-qc-ultra-headphones/media-bindings.json`: delete
   the binding `mb_generated_connect_aux_cable_walkthrough`.
3. Delete the directory `generated-assets/bose-qc-ultra-headphones/`
   entirely (dummy mp4s, mock keyframes, mock provenance, mock
   verification JSON — all of it).
4. Delete the repo-root clutter: `run_bose_aux.py`, `run_bose_aux_mock.py`,
   `run_bose_aux_mock2.py`, `run_bose_aux_mock3.py`, `tmp_dummy.png`, and
   the `tmp/` directory.
5. Verify: `python3 evidence-packs/validate_media.py` passes, and
   `grep -r "mock_req" evidence-packs/ generated-assets/` returns nothing.

## Task 2 — add a tripwire so this cannot happen again

Extend `evidence-packs/validate_media.py` with a derived-asset provenance
check that FAILS validation when, for any registered `DERIVED_ASSET`:

- `request_id` is present and matches `(?i)mock|fake|test|dummy`, or
- the asset names a `verification_local_path` that does not exist on disk.

Add a unit test for both conditions in `app/tests/test_validate_media.py`
(fixture pack in `tmp_path`, per the standing rule).

## Task 3 — remove the stale-cache short-circuit in synthesis

`app/keyframe_synthesis.py` returns early when the keyframe PNG already
exists (`if output_path.is_file(): return output_path`). That would have
silently reused the mock PNGs forever. Replace with: reuse the file ONLY if
its sibling `*.provenance.json` exists, parses, has
`verdict.verdict == "pass"`, and has a non-empty `request_id` that does not
match the mock pattern from Task 2. Otherwise delete the stale file and
regenerate. Test both branches.

## Task 4 — implement the D2 "retrieve first" ladder

`resolve_state()` currently jumps straight to paid synthesis unless a
`curated_path` is set. Implement the preference order from the parent work
order, per state:

1. **`curated_path`** in the registry (existing behavior — keep).
2. **`evidence_source_id`** (new optional registry field): the state is
   directly shown by an existing vault image; resolve it via the manifest
   and use the file as the keyframe with zero generation. Provenance JSON
   records `{"retrieved_from": source_id}`.
3. **Manual figure**: new optional `manual_page` field → render via the
   PDF path already used in `system/image_retrieval.py`.
4. **Synthesis** (existing D3/D4) — last resort only.

Then fix the Bose registry
(`evidence-packs/bose-qc-ultra-headphones/procedure-keyframes.json`):
state `s1` ("2.5 mm end seated in LEFT earcup") is already shown by the
official photo — set
`"evidence_source_id": "src_img_black_controls"` so s1 costs nothing and
cannot hallucinate. Only s0 and s2 remain synthesis candidates.

## Task 5 — pin a real composition endpoint

`"fal-ai/seedream"` is a guess and will fail at runtime. Do this properly:

1. Look up fal's current model catalog and select a multi-image
   composition/edit endpoint (Seedream or nano-banana class) that accepts
   **multiple reference images**. Record the exact endpoint id and its
   input schema (field names for prompt + image list) in a short note at
   the top of `app/keyframe_synthesis.py`.
2. Make it the default for `SHOWME_IMAGE_COMPOSE_MODEL` and adapt
   `attempt()` to the real schema (the current
   `image_url`/`reference_images` guess must be replaced by the documented
   fields).
3. Prove it with ONE cheap live smoke call (a single image edit, expected
   cost cents; `~/.config/showme/fal.env` exports `FAL_API_KEY` — map to
   `FAL_KEY` before importing `fal_client`). Save the smoke result under
   your scratch area, NOT under `generated-assets/`.

## Task 6 — strengthen the D4 verification prompt with claim facts

The current prompt checks only the free-text state description. Build the
checklist from the claims: for each `claim_id` on the state, include the
claim's quoted text (from `source_bindings[].quote`) in the verification
prompt as numbered ground-truth assertions, and require the verifier to
judge each one (`"assertion_checks": [{"assertion": "...", "answer":
"yes|no|unsure", "evidence": "..."}]`) in addition to the existing keys.
For Bose aux this means the verifier explicitly confirms: 2.5 mm end, LEFT
earcup, 3.5 mm end at the source device. The overall verdict passes only if
every assertion check is "yes".

## Task 7 — tests and hygiene

1. Add pytest coverage (all on `tmp_path` fixtures):
   - `system/image_retrieval.py`: bound image resolution; PDF-figure
     rendering path; missing-manifest tolerance.
   - `app/keyframe_synthesis.py`: stubbed `fal_client` — pass path,
     retry-then-pass, retry-then-fail (raises, no file written); the Task 3
     cache rules; the Task 4 ladder order (evidence beats synthesis).
   - registry v2 validation: dangling state ref and unknown claim id both
     yield refusal (`can_generate` false).
2. Move the PDF render cache from repo-root `tmp/pdf_cache` to
   `app/cache/pdf-figures/`.
3. Replace `print()` error reporting in `system/image_retrieval.py` with
   `sys.stderr.write`, and delete temp files on failed synthesis attempts.
4. Full suite green: `python3 -m pytest app/tests system/tests -q`.

## Task 8 — the LIVE acceptance run (only after 1–7)

Budget ceiling **$5** for this run. With `FAL_API_KEY` loaded and
`SHOWME_VIDEO_RENDERER` unset (grounded default):

1. Start the server, ask exactly: *"Show me a video of how to connect Bose
   QuietComfort Ultra headphones to a MacBook Air using the audio cable."*
2. Expected: immediate text+steps answer, "Video generating…" placeholder,
   then either a verified video or an honest failure.
3. Record in `docs/pocs/pipeline-live-acceptance-20260829.md`: per-state
   resolution source (retrieved vs synthesized), every request id, every
   verdict verbatim, total spend, and wall-clock time.
4. **Do not tune verdicts to pass.** If keyframe synthesis fails identity
   (POC 7 failed exactly there), that is a finding, not a bug: report it
   and stop. The deterministic fallback for this procedure is POC 8
   (`workorder-poc8-connection-scene.md`), which is queued separately.
5. If the run passes: leave the artifacts registered as pending
   (`approved_by: null`) for the owner's review — approve nothing.

## Acceptance criteria for this work order

- No mock-provenance artifacts anywhere under `evidence-packs/` or
  `generated-assets/` (Task 2 tripwire enforces it in validation).
- Bose s1 resolves from the official photo with zero generation.
- A real, schema-verified composition endpoint is pinned and smoke-tested.
- D4 verifies claim-derived assertions, not just a description.
- New tests cover retrieval, synthesis, cache rules, ladder order, and
  registry validation; full suite green.
- The live acceptance report exists with honest verdicts and an itemized
  spend ≤ $5.
