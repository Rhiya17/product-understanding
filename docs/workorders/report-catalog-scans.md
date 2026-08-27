# Completion report — skinned fold and catalog static twins

**Completed:** 2026-08-27  
**Provider spend:** **$1.20 / $10.00 ceiling**  
**Rights status:** **INTERNAL ONLY — Tripo3D license check OPEN — do not ship**

## Stage S — what a viewer sees now

There is now a skinned fold video from both requested cameras:

- `poc-3d-static-twin/twin/renders/skinned-fold-official-angle.gif`
- `poc-3d-static-twin/twin/renders/skinned-fold-novel-rear-right.gif`

The open stroller inherits the photographic scan appearance. The motion is not guessed: the armature mirrors the existing evidence-mapped object rig, and the scripted 96-frame comparison reports **0 rad maximum joint-angle error** (threshold `1e-4`), zero translation/scale error, exact latch-state agreement, zero unweighted vertices, and normalized weights. No rig joint, axis, range, order, or action was changed.

The articulated interval is **not fully photorealistic**. Tripo reconstructed 97.2% of the stroller as one fused shell, so hinge crossings stretch and visibly tear as the verified parts fold. Eight measured joint bands exceed the 1.6× visible-artifact threshold. The worst whole-mesh edge ratio is **192.556× at frame 84**; the largest scored band maximum is the seat at **71.874× at frame 84**. The complete joint table and binding/alignment disclosure are in `poc-3d-static-twin/twin/stage-s-report.md` and `stretch-qa-stage-s.json`. No invented geometry was used to hide those defects.

**POC 7 status:** VACE skinning has **not been run**. It remains the recommended next step if the target is a genuinely photoreal fold: use these rig-verified, person-free renders as the motion/control sequence, synthesize only the appearance, then re-run the fixed-camera, identity, part-persistence, and fold-pose checks. Until that follow-up passes, the current videos should be described as photographic-at-rest, mechanism-correct, and visibly deformation-limited during the fold.

## Stage T — catalog results

Levoit was audited first as required. Every product has either a completed probe or a hash-backed skip record.

| Product | Result | Probe-level score | Cost |
|---|---|---|---:|
| Levoit Core 300S | **Skipped** — clean front/three-quarter and top imagery exists, but no true left/back/right view can fill H3.1's second positional slot. The top was not mislabeled. | No request submitted; `input-manifest.json` records candidates and hashes. | $0.00 |
| Graco SnugRide 35 Lite LX | **Skipped** — only one clean front slot. The useful side view contains a human arm/hand; remaining views are people, detail/lifestyle, or not true semantic sides. | No person image submitted; no request created. | $0.00 |
| Bose QC Ultra Headphones (2nd Gen) | **Useful internal static-look probe; scale FAIL.** Request `01a04255-9708-7e12-aafa-44a4cc2865b5`. | 97,648 faces; 1 welded component; largest-shell face share 100%. OBB 11.103/24.851/25.608 cm vs official 4.501/15.999/20.500 cm (`claim_bqcu2_spec_headphone_weight_1` quote): +146.7%/+55.3%/+24.9%. Headband, earcups, cushions, yokes, marks, and control-like details are present; exact controls, hinges, inner fabric, and unseen rear are unreliable. | $0.60 |
| Apple MacBook Air 13-inch M3 | **FAIL — not a recognizable twin.** Request `01a04258-a4b7-7fb1-9196-b018747c7742`. | 62,758 faces; 6 welded components; largest-shell face share 81.4%. OBB 99.562/243.909/625.555 cm vs official closed 1.13/21.5/30.41 cm (`claim_mba_spec_height`, `claim_mba_spec_depth`, `claim_mba_spec_width`). The callout/state mismatch produced a slab, vertical fin, and detached debris; display, keyboard, trackpad, hinge, and lid identity are missing. | $0.60 |

Both completed runs persist their submission, request ID, provider result, all downloads, input hashes, deterministic seeds, mesh analysis, 24-frame 1024px watermarked turntable, scorecard, and internal-only artifact manifest under `poc-3d-static-twin/catalog-scans/<product>/`.

## App registration and blockers

The MVP media schema has **not** been extended for derived/generated assets; its `VIDEO_FILE` binding still requires source-vault manufacturer video. The two generated turntables are therefore registered only in:

- `evidence-packs/bose-qc-ultra-headphones/derived-assets.json`
- `evidence-packs/apple-macbook-air-13-m3/derived-assets.json`

No app media binding was added. App wiring remains a follow-up after a derived-asset schema is designed and the license check closes.

The **single ship blocker for these Tripo-derived assets remains the open Tripo3D license check**. Every generated GLB/render has an internal-only rights record, every GIF/frame is visibly watermarked, and every approval field is null. Source-vault files and protected `claims.json`, `reviews.json`, and `verdicts.json` were not modified.

## Validation

- Stage S artifact validator: PASS.
- Stage S motion trace: PASS at 0 rad maximum joint error across correct + three defect scenarios.
- Catalog scan validator: PASS; two honest skips, two completed scans, $1.20 total spend.
- Source-vault, evidence-pack, media-binding, docs-sync, compile, lint, and test results are recorded in the final execution checkpoint.
