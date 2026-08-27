# MVP v0 Phase 2 Report — Owner Media Approval Queue

**Date:** 2026-08-27  
**Status:** implementation complete; every proposed binding is preview-only pending owner approval

## Summary

The five evidence packs contain 26 conservative claim-to-media bindings: 10
images, 6 official video URLs, 1 hash-gated local manufacturer video, and 9
authentic PDF pages. Every `approved_by` value is `null`. To publish a binding,
the owner writes their email into that binding's `approved_by` field; no code
change is required.

The local Ready2Jet video is limited to internal research use. The server
rechecks its manifest SHA-256 before every uncached serve, exposes it only under
the read-only `/media/` route, and displays the manifest rights note beside the
player. Any non-local deployment requires rights re-clearance.

## Bindings for approval

| Product | Binding | Kind | Source | Claim coverage |
|---|---|---|---|---|
| MacBook Air M3 | `mb_mba_left_ports` | IMAGE | `src_img_guide_left_side` | MagSafe/Thunderbolt locations and MagSafe charging |
| MacBook Air M3 | `mb_mba_right_headphone_jack` | IMAGE | `src_img_guide_right_side` | Headphone-jack location and capability |
| MacBook Air M3 | `mb_mba_top_controls` | IMAGE | `src_img_guide_top_open` | Touch ID/power and camera |
| Bose QC Ultra 2 | `mb_bqcu2_controls_image` | IMAGE | `src_img_black_controls` | Controls, auxiliary port, cable connection, clear-list controls |
| Bose QC Ultra 2 | `mb_bqcu2_folded_image` | IMAGE | `src_img_black_folded` | Storage steps 2–4 |
| Bose QC Ultra 2 | `mb_bqcu2_pairing_video` | VIDEO_URL | `src_video_unboxing_setup` | Bluetooth-pairing steps 1–3 |
| Bose QC Ultra 2 | `mb_bqcu2_controls_video` | VIDEO_URL | `src_video_controls_overview` | Controls location/operation |
| Bose QC Ultra 2 | `mb_bqcu2_pairing_page_27` | PDF_PAGE | `src_owners_guide_en`, p.27 | Pairing step 1 |
| Bose QC Ultra 2 | `mb_bqcu2_pairing_page_28` | PDF_PAGE | `src_owners_guide_en`, p.28 | Pairing steps 2–3 |
| Bose QC Ultra 2 | `mb_bqcu2_storage_page_42` | PDF_PAGE | `src_owners_guide_en`, p.42 | Storage steps 1–2 |
| Bose QC Ultra 2 | `mb_bqcu2_storage_page_43` | PDF_PAGE | `src_owners_guide_en`, p.43 | Storage steps 3–4 |
| Ready2Jet | `mb_r2j_fold_sequence` | IMAGE | `src_r2j_fold_sequence_v1` | Fold steps 1–7 |
| Ready2Jet | `mb_r2j_fold_video` | VIDEO_FILE | `src_r2j_fold_video_v1` | Fold steps 1–7 |
| Ready2Jet | `mb_r2j_fold_page_33` | PDF_PAGE | `src_r2j_manual_v1`, p.33 | Fold steps 1–3 |
| Ready2Jet | `mb_r2j_fold_page_34` | PDF_PAGE | `src_r2j_manual_v1`, p.34 | Fold steps 4–5 and both compact-fold tips |
| Ready2Jet | `mb_r2j_fold_page_35` | PDF_PAGE | `src_r2j_manual_v1`, p.35 | Fold steps 6–7 |
| SnugRide Lite LX | `mb_srl_latch_install_video` | VIDEO_URL | `src_video_install_latch` | LATCH base-install steps 1–10 |
| SnugRide Lite LX | `mb_srl_baseless_install_video` | VIDEO_URL | `src_video_install_seatbelt` | Baseless seat-belt-install steps 1–6 |
| SnugRide Lite LX | `mb_srl_harness_position_video` | VIDEO_URL | `src_video_harness_position` | Secure-child steps 1–7 |
| SnugRide Lite LX | `mb_srl_base_context_image` | IMAGE | `src_img_base_alone` | Base features, placement, and level check |
| SnugRide Lite LX | `mb_srl_harness_context_image` | IMAGE | `src_img_harness_support_detail` | Secure-child steps 1–6 |
| Levoit Core 300S | `mb_c300s_reset_control_image` | IMAGE | `src_img_top_panel_2048` | Reset-control location and reset actions |
| Levoit Core 300S | `mb_c300s_filter_context_image` | IMAGE | `src_img_filter_beside_unit` | Filter-replacement steps 1–5 |
| Levoit Core 300S | `mb_c300s_vesync_video` | VIDEO_URL | `src_video_vesync_app_flow` | VeSync setup and filter-reset handoff |
| Levoit Core 300S | `mb_c300s_replace_filter_page_14` | PDF_PAGE | `src_manual_core300sp_us`, p.14 | Filter-replacement steps 1–6 |
| Levoit Core 300S | `mb_c300s_reset_filter_page_13` | PDF_PAGE | `src_manual_core300sp_us`, p.13 | Filter-indicator reset steps 1–4 |

## Conservative omissions

- **MacBook Air M3:** general newsroom, color, display, keyboard, and closed-lid
  images were omitted because they add appearance rather than answer a bound
  fact. `src_video_list` was omitted because its videos are generic Mac
  tutorials; the curation log explicitly records that no official generic
  Bluetooth-pairing video for Mac exists. The environmental PDF is unrelated
  to the two procedures in this pack.
- **Bose QC Ultra 2:** general product/color/lifestyle views and the closed case
  were omitted because they do not demonstrate a fact or action more directly
  than the selected assets. `src_video_voice_prompts_switching` was omitted
  because the curation log records an unresolved CMS reference ID. Remaining
  manual procedures intentionally use text-only fallback until pages are bound
  in a later approval batch.
- **Ready2Jet:** the open/folded inset and folded-side image were omitted as
  redundant with the stronger fold-sequence image. Lifestyle and POC gallery
  views do not directly explain a bound fact. Procedures other than folding
  intentionally use text-only fallback; their pages were not guessed or
  bulk-bound.
- **SnugRide Lite LX:** the installed-seat image carrying the legacy 4–35 lb
  overlay was omitted because it conflicts with the current published 30 lb
  limit. Other gallery images are general product context or duplicate the two
  selected close views. The curation log records no official click-in video.
  Manual procedure pages remain text-only in this small binding batch.
- **Levoit Core 300S:** general hero, lifestyle, revision-comparison, filter
  detail, and air-quality-table images were omitted where they did not show an
  exact action. The voice-control and Sleep Mode videos do not demonstrate a
  bound procedure. Initial-setup and Wi-Fi-reset manual pages remain text-only.
- **All products:** manifest entries that are documents, support pages, spec
  captures, source indexes, or curation notes are evidence sources rather than
  renderable media and were not converted into media bindings.

These omissions are deliberate. No unregistered, third-party, generated,
cropped, or synthesized media was substituted.
