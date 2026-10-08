# Tesla Model Y (2025+ body, US model year 2026) — official specs

- **Source URLs:**
  - https://www.tesla.com/modely (section "Model Y Specs", one panel per trim and drive)
  - https://www.tesla.com/modely/design#overview (configurator)
  - https://www.tesla.com/ownersmanual/modely/en_us/GUID-1E76B638-7B12-4D9A-8767-94B7F1E92A0E.html (owner's manual "Dimensions", software 2026.32)
  - https://shop.tesla.com/product/model-y-all-weather-rear-trunk-_-seatback-liner, https://shop.tesla.com/product/model-y-all-weather-rear-well-liner, https://shop.tesla.com/product/model-y-parcel-shelf (fitment notes)
- **Retrieved:** 2026-10-07, read in a browser session (tesla.com returns 403 to scripted clients). Values below are copied exactly as displayed.
- **Market:** US (en_US pages).

## 1. Identity: what is sold now (US)

The tesla.com/modely page and configurator (2026-10-07) list four choices:

| Tile on tesla.com | Drive shown | Notes shown on page |
|---|---|---|
| Model Y | Rear-Wheel Drive; All-Wheel Drive (specs panel has both tabs) | Configurator default: "Rear-Wheel Drive · Stealth Grey · 18" Aperture Wheels · All Black · Five Seat Layout" |
| Model Y Premium | "Rear-Wheel & All-Wheel Drive" | specs: "Up to 7 seats" (AWD panel), "5 seats" (RWD panel) |
| Model Y L Premium | "Long Wheelbase, All-Wheel Drive", "LAUNCH" badge | **Excluded from this vault** per work order (6-seat long-wheelbase body). Note that it **is** sold in the US now, not only in China. |
| Model Y Performance | All-Wheel Drive | specs panel not captured (see gaps) |

The owner's manual calls the base trim "Model Y" (the Dec-2025 PDF calls it "Standard"). Third parties (ADAC, Edmunds, accessory makers) also call it "Model Y Standard".

## 2. tesla.com/modely spec panels (verbatim values)

| Field | Model Y RWD | Model Y AWD | Model Y Premium RWD | Model Y Premium AWD |
|---|---|---|---|---|
| Range (EPA est.) | 321 mi | 294 mi | 355 mi | 327 mi |
| Acceleration | 6.8 s 0-60 mph | 4.3 s 0-60 mph (as displayed; see caveat) | 5.4 s 0-60 mph | 4.3 s 0-60 mph |
| Drive | Rear-Wheel Drive | All-Wheel Drive | Rear-Wheel Drive | Dual Motor All-Wheel Drive |
| Weight (Curb Mass) | 4,061 lbs | 4,246 lbs | 4,184 lbs | 4,473 lbs |
| Cargo | 74 cu ft | 74.8 cu ft | 76 cu ft | 76 cu ft |
| Wheels | 18" or 19" | 18" or 19" | 19" or 20" | 19" or 20" |
| Seating | 5 seats | 5 seats | 5 seats | Up to 7 seats |
| Displays | 16" Center Touchscreen | 16" Center Touchscreen | 16" Center Touchscreen; 8" Rear Touchscreen | 16" Center Touchscreen; 8" Rear Touchscreen |
| Ground Clearance | 6.4" | 6.4" | 6.6" | 6.6" |
| Overall Width | Folded mirrors: 78"; Extended mirrors: 83.8" | same | Folded mirrors: 78.0"; Extended mirrors: 83.8" | same |
| Overall Height | 63.8" | 63.8" | 63.9" | 63.9" |
| Overall Length | 188.7" | 188.7" | 188.6" | 188.6" |

Caveats:
- The two "4.3 s" values were read from hidden/visible tab panels in the page DOM. The Model Y AWD value was confirmed on screen after clicking the AWD tab. These figures are not needed for cargo work and were not checked further.
- The "Cargo" headline values (74 / 74.8 / 76 cu ft) do not match the manual's "Behind first row, second row seats folded" figures (70.8 / 71.4). They match "Maximum total cargo volume with driver and front passenger" (74.8 / 75.5), which **includes the frunk**. The Standard RWD "74" and AWD "74.8" disagree with each other. Do not use the headline "Cargo" number as rear-trunk volume.
- Page footnote: "Based on available 2026 model year EPA MPGe as of March 25, 2026, for 2026 Model Y RWD with 18-inch wheels." This confirms that MY2026 is the current US model year.

## 3. Owner's manual dimensions (software 2026.32, live HTML)

Verbatim tables are in `manuals/owners-manual-live-sections-2026-10-07.md` §1. Key values:

| Item | Model Y (Standard) | Premium 5-seat / 7-seat | Performance |
|---|---|---|---|
| Overall length (excl. plate bracket) | 188.7 in / 4794 mm | 188.6 in / 4790 mm | 188.8 in / 4796 mm |
| Width excl. mirrors / folded / incl. mirrors | 75.6 / 78.0 / 83.8 in (1920 / 1982 / 2129 mm) | same | same |
| Overall height | 63.8 in / 1621 mm | 64.0 in / 1624 mm | 63.4 in / 1611 mm |
| Wheelbase | 113.8 in / 2890 mm | same | same |
| Rear overhang | 39.8 in / 1011 mm | same | same |
| Ground clearance laden / unladen | 4.7 / 6.4 in (119 / 164 mm) | 4.8 / 6.6 in (122 / 167 mm) | 4.6 / 6.0 in (117 / 151 mm) |
| Track | 65.2 in / 1655 mm | 64.4 in / 1636 mm | F 64.4 / R 63.9 in (1636 / 1622 mm) |
| Front trunk | 4.0 cu ft / 114 L | 4.1 cu ft / 116 L | 4.1 cu ft / 116 L |
| Behind 2nd row, seats up | 29.5 cu ft / 835 L | 29.0 cu ft / 822 L (7-seat, 3rd row folded: 27.1 / 766) | 29.0 / 822 |
| Behind 1st row, 2nd row folded | 70.8 cu ft / 2004 L | 71.4 cu ft / 2022 L (7-seat: 69.4 / 1966) | 71.4 / 2022 |
| Behind 3rd row (7-seat) | — | 13.1 cu ft / 370 L | — |
| Liftgate max opening height | "up to approximately 8 feet (2.4 meters)" (Dimensions page) vs "up to approximately 7.5 feet (2.3 meters)" (Rear Trunk page). **The manual contradicts itself; not resolved.** | | |
| Rear trunk load limit | lower compartment 88 lbs (40 kg); upper compartment 198 lbs (90 kg) | same | same |
| Front trunk load limit | 110 lbs (50 kg) if tow eye on frunk side wall; 65 lbs (30 kg) if tow eye on frunk bottom (unsealed frunk) | | |

Conflict with the vault PDF (Dec-2025 edition, software 2025.44, p.218): Premium (5-Seater) "Ground Clearance Laden 5.4 / 138" vs live **4.8 / 122**. Unladen agrees (6.6 / 167). ADAC's catalog also lists 138 mm for Premium AWD. Recorded, not resolved.

## 4. Trim-dependent cargo hardware (official statements)

| Feature | Model Y (Standard) | Premium / Performance | Source |
|---|---|---|---|
| Second-row fold mechanism | Manual "Release Straps (If Equipped)", "one of the four recline positions" | "Power Switches (If Equipped)": side switches, touchscreens, and "switch located on the left side of the rear trunk" | Owner's manual seats page (live) |
| Parcel shelf | Not included; sold as $135 accessory (listed under Accessories in the Model Y configurator) | "Included with Model Y Premium and Model Y Performance" | shop.tesla.com/product/model-y-parcel-shelf; configurator |
| Rear trunk floor liner | Separate style "Model Y", $195 | Separate style "Model Y Premium and Performance", $220; separate "Model Y 7 Seat Interior" style | shop.tesla.com rear trunk + seatback liner |
| Rear well (sub-trunk) liner | Style "Model Y 5 Seat Interior" | Same 5-seat style for Premium/Performance 5-seat; separate "7 Seat Interior" style | shop.tesla.com rear well liner |
| Rear touchscreen | none | 8" | tesla.com/modely specs |

What this means: Tesla sells different rear-trunk floor liners for Standard and for Premium/Performance (different price and style), but the same sub-trunk well liner for every 5-seat car. So the **upper cargo floor or trim differs between Standard and Premium/Performance in some way, and the lower well appears shared across 5-seat trims**. The cause is not documented; candidates are seatback/fold geometry, side-trim pockets, or the trunk-mounted seat-fold switch. The aftermarket maker Tesloid also marks its Premium/Performance cargo mat "Not compatible with standard models". The 7-seat cargo area differs from the 5-seat (third row, different liner).

All shop liner pages say "Compatible with Model Y vehicles produced in 2025+, excluding Model Y L."

## 5. Weights / payload

- Curb mass: see §2 (tesla.com). GVWR/GAWR are not published on tesla.com or in the manual text; the manual says they are on the door-pillar Vehicle Certification label.
- ADAC/ÖAMTC test car (EU "Maximum Range" RWD, 2025): manufacturer "Leergewicht/Zuladung 1.976/472 kg"; ADAC-measured "Leergewicht / Zuladung 1888 / 533 kg" (`specs/oeamtc-adac-autotest-model-y-maximum-range-2025.pdf`, p.15). EU market; not US.
