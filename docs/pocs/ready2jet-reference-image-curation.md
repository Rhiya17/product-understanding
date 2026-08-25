# Ready2Jet reference-image collection and curation

*Written 2026-08-13. This documents how the seven-image reference library for the Graco Ready2Jet stroller was assembled for a Meshy digital-twin experiment.*

## Summary

The collection was **moderately difficult (about 6/10)**. Downloading high-resolution images from Graco was relatively straightforward once the underlying Scene7 asset URLs were identified. The difficult part was viewpoint coverage: Graco and Amazon largely reuse the same marketing gallery, and that gallery does not contain clean, orthographic rear, top-down, or fully reclined views of the exact Kingston SKU.

The result is a seven-image **reference library**, not seven equally suitable Meshy inputs:

- Four views are exact, official-product references derived from the Graco gallery.
- One is an official Graco lifestyle image that only partially satisfies the requested side/recline view.
- Two are supplemental Amazon customer-media views used because the official gallery lacks the requested angles.
- All curated deliverables are 2000 × 2000 PNG canvases, but canvas size must not be confused with source detail. The Amazon customer images do not gain real resolution when normalized to that canvas.

The working files are stored at:

```text
/Users/vbp/Documents/ChatGPT/ShowMe/Ready2Jet_Meshy_References/
```

## Product identity and source pages

The collected product is:

- **Product:** Graco Ready2Jet Stroller
- **Colorway:** Kingston
- **Graco model:** 2209064
- **Amazon ASIN:** B0D2LXK44T

Sources:

1. [Graco Baby official product page](https://www.gracobaby.com/shop/strollers/compact-lightweight-strollers/ready2jet-stroller/SAP_2209064.html?actionPoint=Show)
2. [Amazon product listing](https://www.amazon.com/dp/B0D2LXK44T)

This identity check matters because the repository's current [POC 5 runbook](./poc5-digital-twin-runbook.md) names Ready2Jet **2212125, Splatter Art**. Kingston 2209064 and Splatter Art 2212125 must not be silently combined in one exact-SKU evaluation. The images described here can support a Kingston run, or the same collection process can be repeated for Splatter Art.

## What made the task easy or difficult

| Part | Difficulty | What happened |
|---|---:|---|
| Finding the exact official PDP | Easy | Graco exposes the model number in the product-page URL, which made SKU verification direct. |
| Getting high-resolution Graco assets | Easy–moderate | The visible gallery is backed by Scene7. Once the asset identifiers were found, it was possible to request 2000 × 2000 PNG output directly. |
| Getting Amazon's main gallery | Moderate | The Amazon page is dynamic, and the large images use separate media-host URLs. The main gallery also duplicated most of Graco's images rather than adding new angles. |
| Finding rear and top-down coverage | Hard | Neither official gallery supplied these views. Customer photos and a review-video thumbnail were the only usable coverage of the exact Kingston stroller. |
| Finding a true full-recline profile | Hard / unresolved | The official lifestyle photo shows a reclined seat, but not a clean side profile or proven maximum recline. No source was found that justified labeling it “full recline.” |
| Finding the folded, self-standing state | Easy | Graco publishes a clear, high-resolution self-standing fold image, although it uses a cyan background panel instead of white. |
| Avoiding wrong variants | Moderate | Amazon exposed other colorways and travel-system imagery. Those assets were inspected but excluded to avoid mixing sibling products or variants. |

The main lesson is that **download resolution was not the bottleneck; source coverage was**. A large image cannot recover a viewpoint the manufacturer never photographed.

## Collection procedure

### 1. Verify the exact product before downloading

I first matched the Graco model and Amazon listing to the same Ready2Jet Kingston product. Images belonging to other colorways, travel systems, or nearby Ready2Jet variants were not accepted merely because the chassis looked similar.

This prevents a common digital-twin failure: combining plausible-looking images from different SKUs and asking the model to reconcile conflicting geometry, materials, or accessories.

### 2. Inspect the official Graco gallery

I opened the Graco PDP and inspected its gallery/media references. The product images are served by Newell Brands' Scene7 image service. Six relevant official gallery assets were retained in `raw_official/`.

Representative retrieval form:

```text
https://s7d1.scene7.com/is/image/NewellBrands/<asset-id>?wid=2000&hei=2000&fmt=png-alpha&qlt=100
```

Relevant Scene7 asset identifiers found on the page included:

```text
baby0465_gr_2209064_ready2jet_stroller_atf_1
baby_2209064_glbl99_6eq00_ready2jet_atf_6
baby0465_gr_2209064_ready2jet_stroller_atf_3
baby0465_gr_2209064_ready2jet_stroller_atf_4
baby0465_gr_2209064_ready2jet_stroller_atf_5
baby0465_gr_2209064_ready2jet_stroller_atf_6
```

The `wid`, `hei`, `fmt`, and `qlt` parameters requested a large PNG response and preserved alpha when the source supported it. These downloads provided the cleanest overall view and the best material/color evidence.

### 3. Inspect Amazon's main image gallery

I then inspected the Amazon listing to look for angles absent from Graco. Amazon's main product images are hosted on `m.media-amazon.com`; the large-image form used in the collection was:

```text
https://m.media-amazon.com/images/I/<image-id>._SL2000_.jpg
```

The relevant main-gallery images were saved in `raw_amazon/`. This step confirmed that Amazon mostly republishes the same marketing set as Graco. It did not solve the rear, top-down, or true full-recline gaps.

### 4. Inspect Amazon customer photos and review media

Because the main galleries lacked several requested viewpoints, I reviewed the listing's customer media. Two supplemental views were retained:

- A rear/operator-angle frame showing the handle, chassis, and rear wheels.
- A top-down-ish customer photo showing the empty seat, canopy, belly bar, and wheel layout.

I also downloaded the official Amazon product video and extracted frames for inspection. The video contributed useful fold-sequence and suspension references, but most frames were motion/lifestyle shots rather than clean still inputs. The video and extracted frames are retained under `official_amazon_product_video.*` and `video_frames/` so later reviewers can inspect the evidence without repeating the extraction.

The customer-media step solved coverage, but with a quality tradeoff: the rear view contains a child and outdoor scene, and the top-down view has pavement/background. They are therefore **geometry-inspection references**, not preferred appearance inputs.

### 5. Normalize files without inventing missing views

The selected images were converted or derived into 2000 × 2000 PNG canvases. Operations were limited to:

- format conversion;
- cropping to emphasize the requested part or state;
- proportional resizing; and
- white padding where needed to preserve a square canvas.

No generative fill or synthesized camera angle was used. In particular, missing rear and full-recline geometry was not hallucinated from the front view.

The normalized files live in `curated_7/`; originals remain in the `raw_official/`, `raw_amazon/`, and `raw_amazon_customer/` folders. Keeping both is important because a normalized 2000 × 2000 PNG may contain padding or may originate from a smaller JPEG.

### 6. Build and visually inspect a contact sheet

I generated `curated_contact_sheet.jpg` and inspected the seven choices together. The contact sheet made duplicate coverage, background contamination, state changes, and missing geometry easier to spot than reviewing files individually.

### 7. Package provenance and limitations with the images

The collection includes:

```text
curated_7/                 seven selected PNG references
raw_official/              original Graco gallery downloads
raw_amazon/                Amazon main-gallery downloads
raw_amazon_customer/       selected customer-media originals
video_frames/              frames extracted from Amazon product video
manifest.csv               per-image source and confidence notes
README.md                  short usage guidance
curated_contact_sheet.jpg  visual index
```

A ZIP containing the seven curated images, manifest, README, and contact sheet was also created at:

```text
/Users/vbp/Documents/ChatGPT/ShowMe/Ready2Jet_Meshy_Reference_Kit.zip
```

## How the seven images were selected

Selection used five criteria, in this order:

1. **Exact SKU/colorway:** Kingston 2209064 was required; lookalike variants were rejected.
2. **Requested viewpoint coverage:** each image needed to contribute a distinct requested angle, component, or functional state.
3. **Authoritative source:** official Graco media was preferred over Amazon main-gallery media, which was preferred over customer media.
4. **Geometric usefulness:** the stroller or target component needed to be large enough and sufficiently visible to constrain shape.
5. **Low scene contamination:** white or simple backgrounds were preferred; images with people/backgrounds were accepted only when no clean source covered the angle, and were marked as partial or approximate.

| # | Curated file | Why it was chosen | Limitation |
|---:|---|---|---|
| 1 | `01_front_3q_unfolded_canopy_open.png` | Best exact-product overview; official Graco image; canopy open; clean white background. This is the strongest open-state seed. | A three-quarter view cannot prove hidden rear geometry. |
| 2 | `02_side_profile_recline_reference.png` | Best official evidence of the seat in a reclined configuration and the chassis from the side. | Lifestyle composition, people/background, not orthographic, and not proof of maximum recline. |
| 3 | `03_rear_handle_and_wheels.png` | Best found rear/operator perspective of the exact product; adds otherwise missing handle and rear-wheel relationships. | Customer-review frame with a child and pavement; inspection-only unless carefully masked. |
| 4 | `04_top_down_seat_and_canopy.png` | Best found top-down-ish view; clearly shows seat shape, canopy interior, belly bar, foot area, and wheel placement. | Customer image with outdoor background; not a true camera-normal top view. |
| 5 | `05_belly_bar_carry_handle_closeup.png` | Official Graco-derived crop showing the belly bar, harness, seat edges, and adjacent frame. The belly bar doubles as the carry handle when folded. | It is a crop, not an independent camera view. |
| 6 | `06_wheels_suspension_basket_closeup.png` | Official Graco-derived crop with the clearest product-only evidence for wheel design, lower chassis, basket, and suspension area. | Does not isolate every suspension component; the video frames are useful secondary evidence. |
| 7 | `07_folded_self_standing_crucial.png` | Exact official evidence of the self-standing folded configuration; essential for modeling the product's second functional state. | Cyan background panel; folded state must not be mixed into an open-state static reconstruction job. |

## Recommended use in Meshy

The seven images should **not** all be uploaded into one static image-to-3D request.

### Open-state run

- Use `01` as the primary open-state image.
- Add only compatible open-state, person-free views after preprocessing.
- Use `05` and `06` mainly as detail-validation evidence; because they are crops, verify that Meshy's multi-image mode interprets them correctly rather than treating each crop as the whole object.
- Keep `02`, `03`, and `04` as inspection references unless the people and backgrounds are removed without altering product pixels.
- Hold out at least one independent view for validation, as required by the POC 5 runbook.

### Folded-state run

- Run `07` separately as the primary folded-state reference.
- Use fold-sequence video frames only if they show a compatible, fully folded state and pass exact-SKU checks.
- Do not mix open and folded states in one static reconstruction. A single static generator will otherwise try to average incompatible geometry.

If the final goal is an articulated twin that can fold, the correct workflow is two verified static state references plus downstream part segmentation/rigging—not asking one static Meshy job to infer articulation from contradictory states.

## Gaps and next steps

The library is sufficient for an exploratory Meshy run, but not ideal for production-grade reconstruction. The highest-value improvement would be to obtain or shoot three exact-product photos:

1. Rear orthographic view on white, empty stroller, handle fully visible.
2. True top view on white, camera normal to the ground plane.
3. True side view at the documented maximum recline, empty stroller.

For best geometric consistency, shoot all three with a long focal length, matched camera distance/height, fixed stroller state, even lighting, and visible scale reference. A Graco press/CAD asset pack or a manufacturer 360 spin would be preferable if available.

Before this collection is used as formal POC 5 input, copy the chosen state-specific images into the experiment's `inputs/` directory and create the runbook-required `source-manifest.json` with retrieval date, SHA-256, viewpoint, state, role, parent asset, and every crop/padding operation. Also confirm source-media usage rights before redistribution or commercial publication.
