# MVP v0 Final Report — Local Answer App

**Date:** 2026-08-27  
**Status:** complete; owner claim and media approvals remain intentionally external

## What was built

- A Python 3.12 standard-library HTTP app on `127.0.0.1:8765` over
  `system.answer.search()`, serving only `PUBLISHED` facts by default.
- A single-page question UI with product filtering, cited fact cards, serving
  status badges, hidden-match counts, and an unmistakable off-by-default
  **Internal preview** mode. `REJECTED` facts never render.
- Twenty-six conservative official-media bindings across all five products,
  with an offline validator and owner-controlled approval gate.
- Read-only, manifest-registered local media serving with traversal protection.
  The Ready2Jet manufacturer video is served locally only after its SHA-256 is
  rechecked against the manifest; its internal-research rights note is displayed
  beside the native player.
- A “Show me” procedure player that discovers real `STEP` claim groups, orders
  them by `object.step_number`, applies serving policy per step, and provides
  Previous/Next controls.
- Whole authentic manual-page rendering at 144 DPI from explicit `PDF_PAGE`
  bindings only. Pages are cached under ignored `app/cache/`; no page is guessed,
  cropped, annotated, or synthesized.
- Offline tests for answer serving, approval behavior, media integrity, path
  safety, procedure grouping/order, unpublished-step filtering, text-only
  fallback, and PDF rendering. CI runs the app tests and media validator.

## Run locally

Use Python 3.12 and install the pinned dependencies once:

```bash
python3.12 -m pip install -r system/requirements.txt
python3.12 app/server.py
```

Then open `http://localhost:8765`.

## Exact demo script

1. Leave **Internal preview** off and **Product** set to **All products**.
   Ask: `what is the max child weight for the snugride?`
   - Exactly one PUBLISHED card appears for Graco SnugRide Lite LX.
   - The answer is `value: 30 | unit: lb`.
   - The card includes the manual quote beginning “This child restraint must
     only be used…” and an **Open source** link to the official Graco PDF.
   - No draft media appears.
2. Turn **Internal preview** on. Ask:
   `how does the stroller fold?`
   - Labeled CANDIDATE fold-related cards appear.
   - The official Ready2Jet fold-sequence image and native fold-video player
     appear once, each labeled **MEDIA AWAITING OWNER APPROVAL**.
   - The video displays the manifest notice: “Manufacturer copyright; internal
     research use; generate_from NOT cleared.”
3. Keep preview on and select **Graco Ready2Jet** in Product.
   - In **Show me a procedure**, select **Fold Stroller · not fully published**
     and press **Show me**.
   - The banner reads: **This procedure is not fully published.**
   - Previous/Next walks seven real steps in order.
   - Steps 1–3 show whole manual page 33, steps 4–5 show page 34, and steps 6–7
     show page 35, all rendered at 144 DPI with no crop or annotation.
4. Still on Ready2Jet, select **Unfold Stroller · not fully published**.
   - The real ordered step text appears.
   - Because this small binding batch has no page binding for that procedure,
     the page side explicitly says: **No approved page binding for this step.
     Showing verified step text only.**
5. Turn **Internal preview** off again.
   - Candidate procedure content and all 26 unapproved media bindings disappear.
   - After the owner supplies approval emails, approved media will appear in
     default mode without a code change, subject to its claim also being
     PUBLISHED.

## Binding counts

| Product | Bindings |
|---|---:|
| Apple MacBook Air 13-inch M3 | 3 |
| Bose QuietComfort Ultra Headphones (2nd Gen) | 8 |
| Graco Ready2Jet | 5 |
| Graco SnugRide Lite LX | 5 |
| Levoit Core 300S | 5 |
| **Total** | **26** |

By kind: 10 IMAGE, 6 VIDEO_URL, 1 VIDEO_FILE, and 9 PDF_PAGE. Every
`approved_by` remains `null`. The complete owner queue and conservative omission
list are in `docs/workorders/report-mvp-v0-phase2.md`.

## Omissions and known gaps

- Default serving remains intentionally sparse until the owner completes the
  claim review pass. Preview is not publication.
- All media is pending the owner's separate approval pass and therefore appears
  only in Internal preview today.
- PDF page coverage is deliberately narrow: Ready2Jet folding, Bose pairing and
  storage, and Levoit filter replacement/reset. Other procedures use explicit
  text-only fallback rather than guessed pages.
- The Ready2Jet manual and selected local manufacturer assets have no recorded
  origin URL. They remain hash-pinned vault files; the local video is restricted
  to internal research use and requires rights re-clearance before any non-local
  deployment.
- Lexical answer retrieval can surface another fold-related action before the
  main fold procedure. The procedure selector is deterministic and presents the
  complete grouped sequence.
- Highlighting, cropping, animation, generated frames, and motion synthesis are
  intentionally absent from v0.

## Grounding and safety result

The served experience contains zero generated imagery or motion. Every displayed
image is a registered vault file or a whole page rendered from a hash-registered
vault PDF; every video is a registered origin URL or the narrowly amended,
hash-verified local manufacturer file. The server makes no runtime network calls.
