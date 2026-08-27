# Work Order: POC 7 — VACE Realism Skin over the Twin's Fold Render

**Date issued:** 2026-08-27
**For:** an autonomous agent with repository access (no prior conversation context assumed)
**Depends on:** `poc-3d-static-twin/twin/` (dressed mechanism twin, fold renders + per-frame PNG sequences), `poc-wanvace-control-video/run_vace.py` (endpoint conventions, artifact discipline), `source-vault/graco-ready2jet-2212125/` (official reference imagery), `docs/planning/digital-twin-phase-plan.md` Decision 5, `docs/pocs/vlm-verifier-poc-findings.md`
**Question this POC answers:** can WAN VACE repaint the twin's rig-verified fold render into a photoreal fold video **without altering the motion** — turning "mechanism-correct but schematic" into "mechanism-correct and real-looking"?
**Spend ceiling:** $15 provider spend, hard stop. Expected: $3–8 (2–4 VACE runs + verifier pennies).

---

## 0. Governing rules

1. **The control video is the only motion authority.** The generative model
   may change appearance only. Any run whose motion deviates from the
   control (per the gates in §4) is a FAIL for serving, regardless of how
   good it looks.
2. **Trust labeling.** Per Decision 5 these outputs are a *realism layer*
   over deterministic renders. Passing runs are labeled
   `TWIN_RENDER_VACE_SKIN`; they are never described as footage of the
   real product.
3. **INTERNAL ONLY.** Two open rights items gate shipping: the Tripo3D
   license check (the twin's scaffold ancestry) and generated-asset review.
   Watermark every produced GIF/MP4 frame like Stage T did.
4. **Person-free inputs.** Control renders and reference images must contain
   no people (program rule; also avoids provider likeness rejections).
5. **Artifact discipline** as in `run_vace.py`: every run persists
   submission.json (input SHA-256s), request id immediately on submit,
   result.json, video, extracted frames, contact sheet, under a fresh
   label directory. `FAL_KEY` via ephemeral env only.
6. **Stop-and-report:** spend ceiling; provider rejects the content;
   motion gates cannot be computed; any rule above.

## 1. Stage A — Prepare the control clip and references

1. **Control clip:** encode the mechanism twin's official-angle fold PNG
   sequence (`renders/frames-fold-official-angle/` or re-render via
   `render_twin.py` if absent) to an MP4 (`pypdfium2` is unrelated — use
   Pillow/imageio; no network). 24 fps, 1024px, neutral background as
   rendered. This is the *dressed schematic* render — clean silhouettes
   make the best control signal. Do NOT use the torn skinned-fold render.
2. **Reference images (appearance source):** person-free official imagery
   of the exact Kingston colorway from the input pack:
   `view-01-front-3q.png` primary; optionally `heldout-05-front-3q.png`
   (identity reference role) as a second reference if the endpoint accepts
   multiple. Record hashes.
3. **Prompt:** describe appearance only (product, colorway, studio
   setting); never describe motion, mechanism, or step order — motion is
   the control's job. Reuse the negative-prompt conventions from
   `run_vace.py`.

## 2. Stage B — Runs

Endpoint: `fal-ai/wan-vace-14b/depth` (verify the schema live first, as
`run_vace.py`'s header did; if a structure/pose variant of VACE is
available on fal, note it as an alternative but run depth first for
comparability with probe-01).

Run matrix (stop early if run 1 passes all gates):

| Run | Control | Resolution | Seed | Purpose |
|---|---|---|---|---|
| 1 | official-angle fold | 480p | fixed | baseline |
| 2 | official-angle fold | 720p | same | resolution sensitivity |
| 3 | novel rear-right fold | 480p | same | does the skin hold on a view with no real-footage prior? |
| 4 | reserve | — | — | one retry slot for the best configuration |

## 3. Stage C — Verification gates (all computed, all recorded)

For each run, against its control:

1. **Mask-overlap / silhouette gate:** per-frame product-silhouette IoU
   between control and output (threshold ≥ 0.80 mean, ≥ 0.65 minimum;
   record both). Simple luminance/background segmentation is acceptable on
   these clean backgrounds; commit the script.
2. **Pose-sequence gate:** the five Stage-D contact-sheet poses — output
   frames at the same timestamps must show the same fold stage (manual
   visual check recorded in the report, plus the contact sheet).
3. **Identity gate:** Kingston colorway present (gray fabric, black frame,
   tan grip); no invented controls or parts (the Higgsfield lesson);
   tri-spoke wheels not replaced with invented designs.
4. **Qwen verifier (advisory):** run the small per-question checks from the
   VLM-verifier POC (same product? fixed camera? motion direction? reaches
   folded state?) on the best run. Advisory only — Decision 4 benchmark
   still pending — but record verdicts; they seed the future benchmark
   corpus.
5. **Defect-run negative control (if budget allows within ceiling):** one
   VACE pass over a defect render (`defect_reverse_direction`) to confirm
   the skin does not accidentally "correct" wrong motion — evidence the
   pipeline preserves whatever motion it is given, which is exactly what
   makes it trustworthy.

## 4. Deliverables and definition of done

1. `poc-wanvace-control-video/out/twin-skin-<n>/` per run with full
   artifact discipline, plus watermarked internal-only GIF/MP4 copies.
2. `docs/pocs/poc7-vace-skin-findings.md`: run table (cost, gates, pass/
   fail), before/after frames, the negative-control result, and a plain-
   language verdict: does POC 7 deliver the photoreal fold, and at what
   per-video cost?
3. If a run passes all gates: register it in
   `evidence-packs/graco-ready2jet-2212125/derived-assets.json` with
   provenance chain (twin blend hash → control clip hash → run id) and
   label `TWIN_RENDER_VACE_SKIN`, internal-only, `approved_by` untouched.
4. Spend reported; ≤ $15. Repo clean; tests/validators green; protected
   files untouched; no shipping.
