# 3D model candidates — Tesla Model Y 2025+ (refreshed body)

Compiled 2026-10-07. **Nothing here was downloaded.** This list feeds a later build-vs-buy decision. Metadata for Sketchfab comes from the public API (`api.sketchfab.com/v3/models/{uid}`); other listings were read in a browser.

## Summary

- **No official Tesla 3D asset is available.** tesla.com uses server-rendered 2D images (configurator "compositor"), not a downloadable mesh.
- **No free model found has a verified interior trunk.** The free downloadable Sketchfab models are exterior-focused; whether their cargo area is modeled is unknown.
- **The only geometry-faithful trunk source found is a paid 3D scan**: illumaesthetic, "Interior + Trunk" dataset, Artec Leo, ~0.4 mm accuracy, .stl/.blend, $700. Its license allows commercial development inside the buyer's organization and restricts public/marketing display.

## Candidates

| # | Name / URL | Body | License | Price | Faces / polys | Interior / trunk modeled? | Notes |
|---|---|---|---|---|---|---|---|
| 1 | illumaesthetic "Tesla Model Y (Juniper) 3D Scan (2025+)" — https://www.illumaesthetic.com/products/tesla-model-y-juniper-3d-scan-2025 | 2025+ "Model Y Juniper Long Range" (scanned vehicle) | Commercial development allowed "exclusively to the purchasee's home organization"; no redistribution; "use in certain marketing and public display is restricted" (trademarks) | $700 (dataset selector: Exterior Only / Exterior + Underbody / Interior + Trunk / Frunk; price shown for default selection) | ~23 M polygons vehicle; ~24 M other scans (decimated sizes on request) | **Yes: "Interior + Trunk" and "Frunk" datasets listed** | Artec Leo, ~0.4 mm accuracy, .stl/.blend (1.2 GB), pre-aligned XYZ, Blender scene. Long Range = Premium trim, so the Standard trunk may differ (see specs.md §4). Rights review needed before rendering for a public answer video |
| 2 | Sketchfab "2025 Tesla Model Y" by BloxBloger — https://sketchfab.com/3d-models/2025-tesla-model-y-619601e7800d418da5922c4fa7833f74 | 2025+ (light bar visible in thumbnail) | CC Attribution-NonCommercial | free, downloadable | 307,399 faces / 173,736 verts | Seats visible through the glass; trunk unknown | Published 2025-09-19. NonCommercial may block product use |
| 3 | Sketchfab "2026 Tesla Model Y Performance" by BloxBloger — https://sketchfab.com/3d-models/2026-tesla-model-y-performance-8a0bc252f9da4015a02a7bd99efd4847 | 2025+ Performance | CC Attribution-NonCommercial | free, downloadable | 346,321 faces | unknown | Same author as #2 |
| 4 | Sketchfab "Tesla Model Y 2025" by joyemeng — https://sketchfab.com/3d-models/tesla-model-y-2025-a66f7673a09d4fcb84d37111433f05a9 | claims 2025 (no thumbnail rendered via API; unverified) | CC Attribution | free, downloadable | 1,426,441 faces; 1 animation | unknown (the animation may be doors or liftgate; unverified) | Most permissive license found. Needs a visual check: it may be a re-upload of #5 (same face count ±) |
| 5 | Sketchfab "Tesla Model Y 2025-1" by chenxiangntu — https://sketchfab.com/3d-models/tesla-model-y-2025-1-1ba23c1aa3bc41569cce6caf26bd739b | claims 2025 | none listed (view only) | not downloadable | 1,426,175 faces | unknown | Near-identical face count to #4, so provenance of #4 is unclear |
| 6 | Sketchfab "Tesla Model Y Performance" by patricars — https://sketchfab.com/3d-models/tesla-model-y-performance-cb4a14ffbb554f45bdeff70b6f957e57 | 2025+ Performance (2026-06-23) | none (view only) | not downloadable | 344,958 faces | unknown | |
| 7 | Sketchfab "Tesla Model Y Standard" by averageperson1124 — https://sketchfab.com/3d-models/tesla-model-y-standard-58b487f5c1c34fefa6ec0095b0ed18dc | 2025+ Standard (2026-07-10) | none (view only) | not downloadable | 83,012 faces | unknown | Same author has "Project Juniper (Long Range)" 87,730 faces and "(Performance)" 89,488 faces, also view-only. The "(Performance)" model's description says the model shown "is of internal testing vehicle" |
| 8 | TurboSquid "3D 2025 Tesla Model Y Juniper" (#2379526) — https://www.turbosquid.com/3d-models/3d-2025-tesla-model-y-juniper-2379526 | 2025+ | TurboSquid Standard License, marked "Editorial Uses Only" | $149 | 125,218 polys / 140,739 verts | Listing text mentions an interior; trunk not stated | Publisher 3d_molier International. Variants exist (#2379648 blue, #2379544 black, #2379324 white "Simplified") |
| 9 | Sketchfab "Low Poly Car - Tesla Model Y 2025" by roh3d — https://sketchfab.com/3d-models/low-poly-car-tesla-model-y-2025-21156495b5b54dbf94fb270303a40de8 | 2025 | none (view only) | not downloadable | 11,746 faces | no | Low poly only |
| 10 | Sketchfab "Tesla Model Y White with interior" by dragosburian — https://sketchfab.com/3d-models/tesla-model-y-white-with-interior-b083d9e8def44d878db35299160f2556 | **legacy 2020–24** (published 2022) | Editorial, Sketchfab Store | $99 | 124,866 faces | interior yes; trunk unknown | Wrong body; listed only for completeness |
| 11 | 3dmodels.org "Tesla Model Y with HQ interior" — https://3dmodels.org/3d-models/tesla-model-y-with-hq-interior-2022/ | URL says 2022; search snippet says 2025; not verified (site returned 403 to fetch) | commercial (site terms) | paid | unknown | "HQ interior" claimed | Unverified |

## Not candidates

- MakerWorld / Printables / Cults3D items are partial parts (console trays, decals, console scans), not vehicles.
- tesla.com configurator images are 2D renders served by `static-assets.tesla.com/configurator/compositor` (returns 403 to scripts). There is no mesh.

## Suggested next step (for the decision, not done)

Check #4 visually in the Sketchfab viewer for an openable liftgate and a modeled cargo area. If neither free model has a real trunk, the choice is between buying the illumaesthetic Interior+Trunk scan and taking physical measurements, then modeling the cargo box by hand on top of a free exterior.
