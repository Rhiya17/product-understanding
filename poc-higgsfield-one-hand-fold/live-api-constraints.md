# Live API controls discovered during the corrected POC

Checked July 22, 2026 against `POST /v1/image2video/dop`.

The first corrected batch was rejected before generation, so it spent no video
credits. The live validation response established two constraints:

1. `model: "dop-standard"` is rejected. The accepted values reported by the
   endpoint are `dop-lite`, `dop-preview`, and `dop-turbo`.
2. `motions: []` is rejected because the list must contain at least one item.

This conflicts with the official JavaScript SDK helper, which exposes
`dop-standard` as its highest-quality option. For this POC, `dop-preview` is the
fairest live non-Lite, non-Turbo option rather than silently falling back to the
speed-optimized `dop-turbo` model.

The SDK permits motion strengths from `0.0` through `1.0`. The corrected request
therefore explicitly sends the motion ID that the server had previously
injected, but at strength `0.0`. Every run is accepted only if the server echoes
that exact zero-strength motion and `enhance_prompt: false` in `input_params`.
