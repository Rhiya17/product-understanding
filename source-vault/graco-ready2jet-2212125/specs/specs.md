# Graco Ready2Jet Stroller (model 2212125, Splatter Art) — Spec Transcription

- Primary source (MANUFACTURER_SPEC_PAGE): https://www.gracobaby.com/shop/strollers/compact-lightweight-strollers/ready2jet-stroller/SAP_2212125.html
- Retrieved: 2026-10-07 (read in a browser session; gracobaby.com blocks curl)
- Page title: "Ready2Jet™ Stroller | Graco Baby"; page shows a "NEW" badge.
- Quotes below are copied exactly as the page displays them, including the page's own typos.

## Identity

| Field | Value as written on the PDP |
|---|---|
| Product name | Ready2Jet™ Stroller |
| Color | Splatter Art |
| Model# | 2212125 |
| Colorways offered on the PDP (swatch assets) | Geo Pop, Splatter Art, Lilac Mod, Kingston |
| Price | $189.99 |
| Sibling listing on same PDP | "Ready2Jet™ Travel System +SnugRide® Lite Infant Car Seat, SnugRide® Lite Base $319.99" |

Colorway model numbers (identity finding, same product name and chassis, differing fabric):
- 2212125 = Splatter Art (this page)
- 2209064 = Kingston (https://www.gracobaby.com/shop/strollers/compact-lightweight-strollers/ready2jet-stroller/SAP_2209064.html; the master URL `.../ready2jet-stroller/SP_3648103.html` redirects to it). Its Specifications block shows the same weight and dimension values as 2212125.
- 2212123 = Lilac Mod, 2212124 = Geo Pop (from search-result titles/URLs only; pages not opened).

## Specifications block (PDP, verbatim)

```
Color:
Splatter Art
Model#:
2212125
Stroller Weight:
13.2 lb
Product Width:
20.5 in
Product Height:
43 in
Product Depth:
27 in
Product Weight:
13.2 in lb
```

Notes:
- "Product Weight: 13.2 in lb" is the page's own text (stray "in"); the Kingston (2209064) page shows "Product Weight: 13.2 lb".
- These Width/Height/Depth values are the stroller's **open** (unfolded) dimensions. The PDP does not label them "open", but they match the open dimensions Graco Consumer Care gives on Target (see below: "20.5" W x 43" H x 27" D").
- **The PDP does not state folded dimensions.** No dimension graphic exists in the PDP image gallery (checked 2026-10-07: six gallery images on 2212125, six on 2209064; none carry dimension arrows or numbers other than "13.2 lb").

## Weight (PDP description and features, verbatim)

- "Weighing just 13.2 lb—less than two gallons of milk—this compact stroller is fully-featured and ultra lightweight!"
- "Self-standing compact fold and ultra-lightweight at 13.2 lb, making this fully featured stroller easy to store and transport"

## Child limits

- PDP "Recommended Use" (verbatim): "Stroller holds child up to 50 lb for years of comfortable strolling"
- PDP gives no child height limit. The instruction manual (src_r2j_manual_v1, document NWL0001636434D 12/24, page 4 of the PDF, warnings) says, verbatim from its text layer: "child weighing more than 50 lb (22.5 kg) or taller than 45 in. (114 cm) will cause excessive" [sentence continues in the manual].

## Box contents

- The PDP has no "In the box" / box-contents list.
- Features that describe included items (PDP, verbatim): "Removable belly bar doubles as a carry handle"; "Parents will love the included parent cup holder and stylish leatherette stroller handle."
- The manual's parts list is on PDF page 10 ("2-A Parts List"); it is pictorial (text layer only reads "Parts shipped in basket", "2X", "2X", "No tools required.").
- Retailer statements (RETAILER authority, verbatim):
  - Target: "Includes: Removable belly bar that doubles as a carry handle, leatherette handle, UV 50 canopy, storage basket, parent cup holder"
  - Amazon (Kingston, 2209064): "Included Components Stroller with removable belly bar, parent cup holder, and UV 50 canopy"

## Car-seat compatibility

- PDP feature (verbatim): "Accepts all Graco® SnugRide® infant car seats to become a travel system"
- PDP-linked PDF "Stroller, Infant Car Seat and Base Compatibility (APR 2026)" (https://s7d1.scene7.com/is/content/NewellBrands/graco_stroller_ics_and_base_compatability_chart_apr_2026pdf). Its row for "Ready2Jet®" has a check in the "SnugRide® Infant Car Seats (includes SnugRide® Lite family, SnugRide® Snugfit® & SnugRide® Snuglock® families)" column and a check in the "GoMax Infant Car Seat" column, annotated "(Only with models produced in 2025 & later)". This PDF was NOT stored here: it is text-identical (same creation date, Apr 3 2026) to `source-vault/graco-snugride-35-lite-lx/specs/graco-stroller-carseat-base-compatibility-apr2026.pdf`, which the SnugRide vault already holds (different CDN delivery, so different bytes).

## Instruction manual linked from the PDP

- Link: https://s7d1.scene7.com/is/content/NewellBrands/ready2jet_6eq_nwl0001636434d_napdf
- Same document as the vault's `manuals/graco-ready2jet-manual.pdf` (NWL0001636434D 12/24; identical text layer and PDF creation timestamp, Dec 17 2024). The Scene7 delivery has different bytes (sha256 a4b3c428...), so it was not stored a second time. The vault file's bytes match the imgix URL recorded in the July POC (see manifest).

## FOLDED dimensions — every source recorded separately (NOT reconciled)

No gracobaby.com page states folded dimensions. The sources below disagree; they are listed as found.

### A. Graco Consumer Care answers on Target Q&A (authored by the brand account, hosted on a retailer page)

Page: https://www.target.com/p/graco-ready2jet-compact-stroller-splatter-art/-/A-92331730 (Splatter Art, TCIN 92331730). Answers read via Target's Q&A feed on 2026-10-07. Answer author shown as "Graco Consumer Care".

1. Answered 2025-03-21, to "Will this fit in overhead cabinet in airplane?":
   > "The folded dimensions of this stroller are height 30in depth 11.5in and width 20.5in."
2. Answered 2025-11-24, to "What are the dimensions folded up without the belly bar?":
   > "The Ready2Jet Compact Stroller folded dimensions are 30 in H x 11.5 in D x 20.5 in W."
   (The answer does not say whether the belly bar is on or off for these numbers.)
3. Answered 2026-08-12, to "Is this stroller compact enough to fit in an overhead bin on an airplane?":
   > "The Ready2Jet Stroller measures 30" H x 11.5" D x 20.5" W when folded"

Related Graco Consumer Care answers on the same page:
- 2025-07-28: "the stroller’s dimensions are: 20.5" W x 43" H x 27" D." (open dimensions; matches the PDP)
- 2026-04-06: "The height of the handle is 39""
- 2026-08-12: "The belly bar for the Ready2Jet stroller is used to carry the stroller when folded. It can be removed when storing."

### B. Target specifications table (RETAILER)

Same Target page, "Specifications" section, verbatim:
- "Dimensions (Collapsed): 30.98 Inches (H) x 19.52 Inches (W) x 11.06 Inches (D)"
- "Dimensions (Overall): 23.9 Inches (H) x 18 Inches (W) x 11.9 Inches (D)" (smaller than the collapsed figures and than the PDP open dimensions; meaning unclear — possibly packaging. Recorded as written.)
- "Weight: 13.2 Pounds"; "Holds up to: 50 Pounds"; "Front Wheel Diameter: 6.5 Inches"; "Rear Wheel Diameter: 7.5 Inches"; "UPC: 047406189564"
- Note: the same table also says "Product Configuration: Double", which is wrong for this single stroller — a sign the retailer table is not fully reliable.

### C. Amazon product details (RETAILER; Kingston colorway, model 2209064)

Page: https://www.amazon.com/dp/B0D2LXK44T (Kingston selected), verbatim:
- "Folded Size Less than 43.5*12.0*8.0 Inches"
- "Item Dimensions L x W x H 27"L x 20.5"W x 43"H"
- "Item Weight 13.2 pounds"; "Maximum Height 43 inches"; "Model Number 2209064"

### D. Walmart (RETAILER)

Page: https://www.walmart.com/ip/12512574204 (Splatter Art Grey). No folded dimensions found in the page data (only "Weight 13.2 lb", "Max Weight 50 lb", "Height 43 in").

### Conflict summary (not resolved)

| Source | Authority | H | W | D | Units |
|---|---|---|---|---|---|
| Graco Consumer Care on Target Q&A (3 answers, 2025-03 to 2026-08) | brand-authored, retailer-hosted | 30 | 20.5 | 11.5 | in |
| Target spec table "Dimensions (Collapsed)" | RETAILER | 30.98 | 19.52 | 11.06 | in |
| Amazon "Folded Size" | RETAILER | "Less than 43.5*12.0*8.0" (axes not labelled) | | | in |
| gracobaby.com PDP | MANUFACTURER_SPEC_PAGE | not stated | | | |

## Other official sources checked for folded dimensions

- gracobaby.com PDPs for 2212125 and 2209064 (Specifications block, gallery, linked PDFs): none.
- Instruction manual NWL0001636434D 12/24 text layer: no product dimensions.
- Graco Salsify syndication catalog pages (sites.salsify.com, SAP_2214052 Kingston and SAP_2212124 Geo Pop, found in search results): both return HTTP 404.
- well.ca (Canadian retailer, Kingston): open dimensions only ("20.5"W x 43"H x 27"D"), 13.2 lb; it states "up to 20.4 kg (45 lb)" child weight, which conflicts with the US 50 lb figure (Canadian listing, not resolved here).

## 360 / spin audit

- gracobaby.com PDP (2212125 and 2209064): flat image carousel plus one Scene7 video (`100_v5_final__ready2jet_stroller`). No spin/360 viewer; the only "spin"/"360" strings in the DOM are CSS loading-spinner keyframes.
- Amazon B0D2LXK44T: no spin/360 markers in the page HTML.
