# Tesla Model Y (2025+ body) — rear cargo geometry evidence

Compiled 2026-10-07. Target: current US Model Y (2025+ refreshed body, MY2026), excluding Model Y L.

## Summary

- **Tesla does not publish trunk opening or cargo-floor dimensions** for the 2025+ Model Y in the owner's manual, on tesla.com, or in the shop. The only official linear numbers near the trunk are body-in-white datum distances in the 2025+ Collision Repair manual (row 1–3). Those are structural hole-to-hole measurements, not usable opening sizes.
- **Update 2026-10-07:** two Chinese reviews tape-measured the 2025+ trunk (§1c): opening 1190 × 1140 mm, depth 1060 mm and 108.5 cm, floor-to-top 680 mm. d1ev states the space is essentially unchanged from the legacy body. The bullets below describe the first pass.
- **The only third-party linear measurement of the 2025+ trunk found is ÖAMTC/ADAC's 68 cm load-lip height** (EU Maximum Range RWD). ADAC also measured volumes, including 105 L under the floor.
- **Every tape-measure floor/width/opening number found is either for the 2020–2024 body (Tesmanian, 2020 Performance) or from a low-authority 2026 web article that names no method (AutoEdgeView).** The legacy numbers are listed separately as a SUBSTITUTION and must not be treated as 2025+ facts.
- **Trim matters.** Tesla sells different rear-trunk floor liners for "Model Y" (Standard) and "Model Y Premium and Performance", and a third for 7-seat. The sub-trunk well liner is one part for all 5-seat cars. The cargo floor geometry or trim therefore differs between Standard and Premium/Performance in some undocumented way (see `specs/specs.md` §4).
- **Recommendation for the Blender build (not a fact):** treat the opening and floor numbers as unknown for 2025+ until someone measures a real car or buys the illumaesthetic "Interior + Trunk" scan (`3d-model-candidates.md`). Use legacy numbers only as a labeled placeholder.

## Legend

- `confidence`: H = official, exact statement; M = reputable third-party measurement of the right body; L = unknown method, or wrong/unclear body.
- `body`: which Model Y body was measured. "2025+" = refreshed ("Juniper") body. "2020–24" = legacy body (SUBSTITUTION).
- Source IDs refer to `manifest.json`.

## 1. Dimension table

| # | Dimension | Value | Unit | source_id | Exact quote / location | Body / trim measured | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | Rear body aperture, upper datum hole to datum hole (left↔right across the rear opening; hole locations are defined only by the figure) | 1217 - 1223 | mm | src_brm2025_rear_body_capture | Label "1217 - 1223 mm" on Figure 4 "Rear Body Measurements", 2025+ Collision Repair Procedures → Dimensional Specifications. Page states "All measurements are in millimeters", "measured center-to-center", "for reference only" | 2025+ body-in-white (no trim) | H for the datum distance. **Not** a trimmed opening width; the trimmed opening is narrower by an unknown amount |
| 2 | Rear body lower datum, diagonal (upper-left lower hole ↔ lower-right hole, as drawn) | 916 - 926 | mm | src_brm2025_rear_body_capture | Label "916 - 926 mm", same figure | 2025+ BIW | H (datum only) |
| 3 | Rear body lower datum, other diagonal | 795 - 805 | mm | src_brm2025_rear_body_capture | Label printed "795 - 805 mm" on figure | 2025+ BIW | H (datum only). The two diagonals differ by about 120 mm, so the four holes are not a symmetric pattern (or the arrows join different-height holes). Read with care and check against the figure |
| 4 | Load-lip height above road (Ladekante) | 68 | cm | src_oeamtc_adac_autotest_2025 | p.5 "Kofferraum-Nutzbarkeit": "Die Ladekante liegt mit 68 cm auf einer passablen Höhe über der Fahrbahn." | 2025+ EU "Model Y Maximum Range" RWD (ADAC Autotest, PDF dated 2026-05-20) | M |
| 5 | Load lip vs cargo floor step | flush (no step) | — | src_oeamtc_adac_autotest_2025 | p.5: "Ladekante und -boden befinden sich auf einer Ebene" | same | M |
| 6 | Floor with second row folded | "nahezu ebene Ladefläche ohne störende Stufe" (nearly flat, no step) | — | src_oeamtc_adac_autotest_2025 | p.5 | same (power-fold rear seats) | M |
| 7 | Liftgate head clearance | people up to about 1.95 m need not worry about their head | m | src_oeamtc_adac_autotest_2025 | p.5: "Personen bis rund 1,95 m Körpergröße müssen sich um ihren Kopf keine Sorgen machen" | same | M (qualitative; at default max opening) |
| 8 | Liftgate max opening height (top of open liftgate above ground) | ≈8 ft / 2.4 m **vs** ≈7.5 ft / 2.3 m | ft / m | src_manual_live_html; src_manual_pdf_2025_12 | Dimensions page: "can open up to approximately 8 feet (2.4 meters) high"; Rear Trunk page: "up to approximately 7.5 feet (2.3 meters) high". Both statements appear in the live HTML and the Dec-2025 PDF (pp.221 / 32) | 2025+, "depending on configuration (such as suspension height or wheel selection)" | H, but **CONFLICT** (see §2) |
| 9 | Liftgate opening height is user-adjustable | yes, saved per location | — | src_manual_live_html | "Adjusting Liftgate Opening Height" section | 2025+ all | H |
| 10 | Rear cargo volume, behind 2nd row, seats up | Standard 29.5 cu ft / 835 L; Premium 5-seat & Performance 29.0 / 822 | cu ft / L | src_manual_live_html | Dimensions → Cargo Volume | 2025+ | H (SAE-style volume; method not stated) |
| 11 | Rear cargo volume, 2nd row folded | Standard 70.8 / 2004; Premium 5 & Perf 71.4 / 2022; Premium 7-seat (2nd+3rd folded) 69.4 / 1966 | cu ft / L | src_manual_live_html | same | 2025+ | H |
| 12 | Cargo behind 2nd row, 7-seat, 3rd row folded flat | 27.1 / 766 | cu ft / L | src_manual_live_html | same | 2025+ Premium 7-seat | H |
| 13 | Cargo behind 3rd row (7-seat) | 13.1 / 370 | cu ft / L | src_manual_live_html | same | 2025+ Premium 7-seat | H |
| 14 | Frunk volume | Standard 4.0 / 114; Premium/Perf 4.1 / 116 | cu ft / L | src_manual_live_html | same | 2025+ | H |
| 15 | Rear cargo volume (VDA-style, ADAC measured): normal / to roof (seats up) / seats folded to window line / folded to roof | 420 / 540 / 850 / 1380 | L | src_oeamtc_adac_autotest_2025 | p.4 "Kofferraum-Volumen": "Das Standardvolumen beträgt 420 l … bis zum Dach hoch … 540 l … bis 850 l … bis zu 1.380 l" | 2025+ EU Maximum Range RWD | M (different method from Tesla's figures, so not comparable to rows 10–11) |
| 16 | Under-floor (sub-trunk) volume | 105 | L | src_oeamtc_adac_autotest_2025 | p.4: "weitere 105 l Stauraum unter dem Ladeboden" | same | M |
| 17 | Frunk volume (ADAC) | ≈80 | L | src_oeamtc_adac_autotest_2025 | p.4: "rund 80 l im Frunk" | same | M (vs Tesla 114–116 L, a method difference) |
| 18 | Under-floor layout | two large compartments under a transversely split floor, plus two side storage bins (left and right) | — | src_oeamtc_adac_autotest_2025 | p.5: "zwei große Fächer unter dem quer geteilten Ladeboden sowie zwei Ablagefächer links und rechts" | same | M (qualitative) |
| 19 | Lower-compartment load limit / upper floor load limit | 88 lbs (40 kg) / 198 lbs (90 kg) | lb / kg | src_manual_live_html | Rear Trunk → Rear Trunk Load Limits | 2025+ | H |
| 20 | Frunk load limit | 110 lb (50 kg) if tow eye on frunk side wall; 65 lb (30 kg) if tow eye on frunk bottom | lb / kg | src_manual_live_html | Front Trunk → Storage and Load Limits | 2025+ (two frunk variants exist) | H |
| 21 | Rear seat recline (strap-release seats) | "one of the four recline positions" (no angles given) | — | src_manual_live_html | Seats → Using Release Straps | 2025+ trims with release straps (Standard) | H (no angle published) |
| 22 | Trunk carry-on test | 7 carry-ons in the cargo area; 19 with 2nd row folded; frunk fit 1 | count | src_caranddriver_2026_url | caranddriver.com/tesla/model-y-2026, "Interior, Comfort, and Cargo" (paraphrased) | 2026 Model Y (trim not stated in the passage read) | M (count, not dimensions) |
| 23 | Trunk width between wheel wells / depth seatback-to-hatch / height at lowest hatch-glass point | "approximately 37 inches wide between the wheel wells, 31 inches deep (seatback to hatch), and 27 inches tall" | in | src_autoedgeview_2026_url | autoedgeview.com/ev-reviews/tesla-model-y-trunk-cargo-review-2026 (2026-07-30), no author, no method | Claims "2026 Juniper"; the same article quotes legacy volumes (30.2 / 72.1 cu ft), so the body is uncertain | **L** |

### 1b. SUBSTITUTION — legacy 2020–2024 body measurements (do not use as 2025+ facts)

Source: Tesmanian, "Tesla Model Y Interior, Trunk, Trunk Well, Frunk and Other Measurements", 2020-04-11, by Vincent Y, measured on a **Model Y Performance (2020, legacy body)**. Labels A–E refer to the arrows on the saved diagrams `geometry/LEGACY-2020-tesmanian-*.jpg`. The mapping from letter to dimension below is read from the arrows in those images.

| # | Dimension (arrow) | Value | Diagram file | Notes |
|---|---|---|---|---|
| L1 | Floor width across the mid-floor between the side trims (trunk01 "A") | 94 cm / 37 in | LEGACY-2020-tesmanian-trunk01-measurement-diagram.jpg | Arrow spans side trim to side trim at about the wheel-arch zone |
| L2 | Floor length, rear seatback base to load lip, seats up (trunk01 "B") | 108 cm / 42.5 in | same | |
| L3 | Floor length, load lip to front-seat backs, 2nd row folded (trunk02 "A") | 200 cm / 78.7 in | LEGACY-2020-tesmanian-trunk02-measurement-diagram.jpg | Depends on front-seat position |
| L4 | Opening height, cargo floor to top of liftgate aperture (trunk02 "B") | 70 cm / 27.6 in | same | |
| L5 | Load-lip height above ground (back "A") | 60 cm / 23.6 in | LEGACY-2020-tesmanian-back-measurement-diagram.jpg | Performance trim (lower ride). **Conflicts with ADAC 68 cm** for 2025+ RWD; different body and trim |
| L6 | Sub-trunk well: lower basin fore-aft (A) / lower basin width (B) / upper well width (C) / upper well fore-aft (D) / step from rim to lower basin (E) | 35 / 60 / 80 / 47 / 35 cm (13.8 / 23.6 / 31.5 / 18.5 / 13.8 in) | LEGACY-2020-tesmanian-trunkwell-measurement-diagram.jpg | E is drawn in plan view, so it may be a fore-aft distance rather than a depth. **No clear well depth was published** |
| L7 | Frunk: tray fore-aft (A) / tray width (B) / opening fore-aft (C) / opening width (D) / rim to tray (E) | 35 / 70 / 43 / 91 / 35 cm | LEGACY-2020-tesmanian-frunk-measurement-diagram.jpg | Legacy frunk; the 2025+ frunk is 4.0–4.1 cu ft (same as legacy per Tesla), but its shape is not verified |

### 1c. Tape measurements of the 2025+ body (added 2026-10-07 by the orchestrator, after the first pass)

Two Chinese test reviews measured the refreshed (焕新版) body with a tape. They were found by searching in Chinese, which the first collection pass did not do.

| # | Dimension | Value | Unit | source_id | Exact quote | Body measured | Confidence |
|---|---|---|---|---|---|---|---|
| N1 | Trunk opening, "开口长度" (opening length) | 1190 | mm | src_12365auto_2025_practicality_test | "开口长度为1190mm" | 2025款 Model Y 长续航全轮驱动 首发版 (China, 2025+ body) | M. The axis is undefined on the page. Most likely the horizontal opening width, which is consistent with the 1217–1223 mm body-in-white datum (row 1) |
| N2 | Trunk opening, "开口宽度" (opening width) | 1140 | mm | same | "开口宽度为1140mm" | same | M. The axis is undefined. If N1 is the width, this is the opening's height along the sloped aperture (lip to top), not a vertical height |
| N3 | Trunk depth (进深), seats up | 1060 | mm | same | "后备厢进深为1060mm" | same | M |
| N4 | Cargo floor to top, vertical (地台与顶部的垂直高度) | 680 | mm | same | "后备厢地台与顶部的垂直高度为680mm" | same | M. The top is probably the parcel shelf or headliner at the measuring point; this is not stated |
| N5 | Trunk depth (纵深), seats up, "normal state" | 108.5 | cm | src_d1ev_2025_model_y_review | "根据实际的测量，焕新版 Model Y 与老款的空间基本相同，常规状态下纵深能够达到 108.5cm，与老款基本没有变化。" | 焕新版 (2025+ body, China) | M. The reviewer states the space is essentially unchanged from the legacy body |

Reading these together: depth is 1060 mm (12365auto) vs 1085 mm (d1ev) vs legacy 1080 mm (Tesmanian L2). The 25 mm spread is plausibly from different measuring points. d1ev's "same as legacy" statement makes the legacy width figure (L1, 94 cm between the side trims) a reasonable stand-in for the 2025+ body. This is an inference, not a measurement.

Unsourced figures from an AI assistant (Gemini, supplied by the owner 2026-10-07) are **not evidence** and are not recorded as a source. They largely reproduce the legacy Tesmanian numbers (94 cm, 109 cm, 200 cm, 60 cm well). Their "opening height ~66 cm" and "opening width ~109 cm" disagree with N1/N2.

Basenor (accessory maker, 2026 pages) says the "Juniper rear bench is slightly deeper than Legacy — cargo mats and trunk liners cut for pre-Juniper Model Y will leave a gap at the rear seat base". This suggests the 2025+ seats-up floor length (L2) is **shorter** than legacy. It is unquantified and low authority (src_basenor_juniper_pages_url).

## 2. Conflicts (recorded, not resolved)

1. **Liftgate max opening height:** manual Dimensions page "≈8 ft (2.4 m)" vs manual Rear Trunk page "≈7.5 ft (2.3 m)". Both appear in the live HTML (2026-10-07) and the Dec-2025 PDF.
2. **Load-lip height:** ADAC 68 cm (2025+ EU Max Range RWD) vs Tesmanian 60 cm (2020 Performance legacy). Different body and ride height; not a like-for-like conflict.
3. **Rear cargo volume method:** Tesla 822–835 L behind row 2 vs ADAC 420 L (to the cover line) / 540 L (to roof). These are different measurement methods; do not compare directly.
4. **Frunk:** Tesla 114–116 L vs ADAC ≈80 L (method).
5. **tesla.com "Cargo" headline:** Standard RWD "74 cu ft" vs Standard AWD "74.8 cu ft" vs manual 70.8 cu ft (rear, seats folded). The 74.8 equals rear-folded plus frunk.
6. **Premium laden ground clearance** (affects load-lip height laden): Dec-2025 PDF 5.4 in / 138 mm vs live HTML 4.8 in / 122 mm.
7. **AutoEdgeView "31 in deep" (2026)** vs Tesmanian legacy 42.5 in seats-up floor length. These differ by more than 11 in, so they probably measure different things (e.g. at the top vs the floor). Unresolvable without method.

## 3. Shape references saved in this folder (no numbers, but outlines)

| File | What it shows | Use |
|---|---|---|
| `trunk-floor-liner-5seat-outline-topdown.png` | Tesla shop product shot: 5-seat rear trunk floor liner (trapezoid: wider at the seatback, notch at the latch end) plus 3-piece seatback liners, top-down | Floor plan-view outline (unscaled). Tesla's gallery shows the same image for both Standard and Premium/Performance styles, so it is unclear which style it depicts |
| `trunk-floor-liner-7seat-outline-topdown.png` | 7-seat floor liner plus 2-piece seatback liners | 7-seat outline |
| `sub-trunk-well-liner-outline.png` | Rear well (sub-trunk) liner, 5-seat style per page default | Well plan shape (unscaled) |
| `collision-manual-2025-rear-body-measurements-capture.png` | Screen capture (1392×783, zoomed browser render) of the 1600×900 official figure | Rows 1–3 |
| `LEGACY-2020-tesmanian-*.jpg` (5 files) | Legacy-body measurement photos with arrows | §1b only |

Official owner's manual illustrations in the vault PDF (`manuals/model-y-2025plus-owners-manual-na-sw2025.44.pdf`), by PDF page index: p.32 open liftgate with adjust button; p.33 lower-compartment cover lifted (shows the two-level floor); p.40 power-fold seat switch and trunk view; p.41 trunk-side seat-fold switches (left trunk wall); p.220 exterior dimension drawing (A–H letters).

## 4. Gaps: dimensions nobody publishes for the 2025+ body (as of 2026-10-07)

- Liftgate opening width at the top and at the bottom (trimmed aperture)
- Opening height (floor/lip to top of aperture)
- Cargo floor length, seats up and seats folded (at the floor and at the top of the seatback)
- Floor width between the wheel arches, and maximum width behind the arches
- Interior height floor → parcel shelf, and floor → headliner
- Sub-trunk L × W × depth (only ADAC's 105 L volume and Tesla's 88 lb limit exist)
- Second-row seatback angle (upright and the four strap positions)
- Frunk L × W × depth for the 2025+ body
- Difference between Standard and Premium/Performance floors (only the separate liner SKUs show that one exists)
- Load-lip height for US-spec trims (ADAC measured an EU RWD car only)

Closing these needs a physical measurement (tape and photos on a 2026 US Model Y and a Premium) or a purchased 3D scan.
