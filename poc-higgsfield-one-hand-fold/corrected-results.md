# Corrected three-run result: 0/3 pass

## Verdict

The clean experiment confirms the core failure. With prompt enhancement disabled,
the motion preset neutralized to strength `0.0`, the live API's non-Turbo
`dop-preview` tier, the same official Graco source image, the exact same prompt,
and three predeclared seeds, **none of the three videos folded the stroller**.

All three runs passed the parameter audit before generation. The server echoed
the prompt unchanged, `enhance_prompt: false`, the requested seed, and the
explicit motion entry at strength `0.0`. The result can therefore be attributed
to this model and controlled configuration, not the hidden defaults that
invalidated the first run.

## Results at a glance

| Run | Seed | API controls | Visual verdict | Elapsed |
|---|---:|---|---|---:|
| 1 | 41001 | Exact match | Fail | 394 s |
| 2 | 41002 | Exact match | Fail | 391 s |
| 3 | 41003 | Exact match | Fail | 392 s |

Every output is a 5.37-second video. Each took about 6 minutes 32 seconds from
submission to the saved file.

## Repeated failure across all three seeds

Each run begins with the exact compact Ready2Jet side view. Instead of showing
the documented slide-and-squeeze action followed by an automatic fold, the
model gradually rotates or reframes the scene and transforms the stroller into
a larger, front-facing, fully open stroller. The canopy opens, the seat and
handle geometry change, and the final stroller does not match Graco's folded
reference.

- No run visibly demonstrates the real thumb-switch action.
- No run visibly demonstrates the underside handle-lever squeeze.
- No run shows a mechanically plausible fold.
- No run ends with a compact, folded, self-standing Ready2Jet.
- Every run changes the product's identity or parts.

The controlled experiment therefore supports this architecture rule:
**prompt-only generative video must not be used for product-operation
instructions.** A polished, plausible-looking clip is not evidence that the
shown mechanism is real.

## Evidence

Each run directory contains the exact request, request ID, effective-parameter
validation, final server response, video, extracted frames, and contact sheet:

- `out/corrected-preview-run-01/`
- `out/corrected-preview-run-02/`
- `out/corrected-preview-run-03/`

The original uncontrolled run remains in `out/` and is excluded from the 0/3
verdict.
