# Catalog twin scorecard — Apple MacBook Air 13-inch M3

**Verdict: FAIL — the provider did not reconstruct a recognizable MacBook twin.**

- Run: Tripo H3.1 request `01a04258-a4b7-7fb1-9196-b018747c7742`, deterministic seeds `20260827`, `auto_size`, 100k face limit, PBR. Cost recorded: **$0.60**.
- Input: exact person-free open front + true left profile. The left profile is a closed-state official guide image with callouts. The state/annotation conflict was disclosed before submission. The true right profile was omitted because, without a back image, a third positional URL would falsely occupy H3.1's `back` slot.
- Mesh: 62,758 faces; **6 position-welded components; 81.4% of faces in the largest shell**.
- PCA OBB, sorted: **99.562 × 243.909 × 625.555 cm**. Official closed dimensions are **1.13 × 21.5 × 30.41 cm** from `claim_mba_spec_height`, `claim_mba_spec_depth`, and `claim_mba_spec_width`; errors are **+8710.8% / +1034.5% / +1957.1%**. Closed height is not directly comparable to an intended open reconstruction, but the multi-meter scale failure makes that caveat immaterial.
- Identity weakly present: two thin aluminum-colored slabs and a few port-like surface details.
- Identity missing/incorrect in provider preview and orbit: no credible open display, keyboard, trackpad, hinge, or Apple lid mark; a callout became a vertical fin; several detached callout/debris components were invented beneath the slab.

The 24-frame 1024px failure turntable is retained as `turntable-internal-only.gif` for audit. It is visibly watermarked; the Tripo3D license check remains open.
