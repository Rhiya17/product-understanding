# Catalog twin scorecard — Bose QC Ultra Headphones (2nd Gen)

**Verdict: useful internal static-look probe; dimensional control FAIL; not shippable.**

- Run: Tripo H3.1 request `01a04255-9708-7e12-aafa-44a4cc2865b5`, deterministic seeds `20260827`, `auto_size`, 100k face limit, PBR. Cost recorded: **$0.60**.
- Input: exact person-free front + left exterior side, both black and in the same open/wear state. Hashes and vault verification are in `input-manifest.json` and `submission.json`.
- Mesh: 97,648 faces; **1 position-welded component; 100.0% of faces in the largest shell**. This is a fused statue, not an articulated headphone model.
- PCA OBB, sorted: **11.103 × 24.851 × 25.608 cm**. Official sorted dimensions are **4.501 × 15.999 × 20.500 cm**, published in the product-details quote bound to `claim_bqcu2_spec_headphone_weight_1`; errors are **+146.7% / +55.3% / +24.9%**. This fails the existing 5% probe threshold on every axis.
- Identity present in provider preview and orbit: full padded headband, both earcups, both cushions, yokes, exterior Bose marks, and control/port-like details.
- Missing or unreliable: hinge separability, exact control geometry, interior acoustic fabric, and unseen rear surfaces. Reflective yokes and fine controls are texture/geometry approximations.

The 24-frame 1024px turntable is `turntable-internal-only.gif`. It is visibly watermarked; the Tripo3D license check remains open.
