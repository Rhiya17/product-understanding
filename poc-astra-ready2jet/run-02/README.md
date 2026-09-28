# Ready2Jet — run-02 realism pass

**Partial realism improvement. INTERNAL RESEARCH.** Kingston-reference reconstruction; exact SKU applicability unresolved. The canopy now has a distinct visor, upholstery has padding/sewn divisions, the basket has visible suspended mesh and binding, and the same assembly retains the inherited fold. The crown remains too angular, upholstery/back construction is simplified, and gathered fabric is stylized. No photorealism, hidden-mechanism accuracy or physical fit is established.

## Open the deliverables

- [Editable scene](final/ready2jet.blend)
- [Source / baseline / candidate](final/open-appearance-comparison.jpg), [controlled before/after](final/before-after.jpg), [neutral geometry comparison](final/geometry-before-after.jpg)
- [Main folding MP4](final/fold-main.mp4), [GIF preview](final/fold-main-preview.gif), [synchronized rear-right MP4](final/fold-rear-right.mp4)
- [Open product still](final/open-product.jpg), [folded product still](final/folded-product.jpg), [material detail sheet](final/material-detail-sheet.jpg)
- [Open / middle / folded source comparison](final/open-mid-folded-comparison.jpg)
- [Fixed side diagnostic](final/side-diagnostic.jpg)
- [Main sampled review](final/main-sampled-animation-review.jpg), [rear sampled review](final/rear-sampled-animation-review.jpg)
- [Qualified release-control source panel](final/release-control-source-panel.png)
- [Report](report.md), [reference manifest](input-manifest.json), [part evidence](part-joint-evidence.json), [action mapping](action-event-map.json)

## Verified runtime and settings

macOS 26.6.2 arm64; Python 3.11.4; **bpy / Blender 5.0.1, Cycles CPU**. FFmpeg 8.0.1 / libx264; Pillow 12.3.0 in the bundled runtime. Isolated bpy required filesystem-sandbox escalation; no open Blender application session was used.

Both clips contain **193 frames at 24 fps**, 8.0417 seconds, rendered and encoded at **1280×720**. Main: 24 Cycles samples; rear: 20; denoising enabled. Product pixels are not upscaled onto a larger canvas. The fixed orthographic diagnostic framing spans the whole action. Clean native PNG sequences are in `final/frames-main/` and `final/frames-rear/`.

Open/folded stills: **1600×1600, 96 samples**, separate brighter photography lighting. Comparisons: 640×640, neutral baseline lights and AgX / Medium High Contrast / exposure −0.3. Details: 900×900, 48 samples. Beauty still exposure is 0.0; broad-light changes are recorded in `scripts/realism_run.py --beauty` and `records/camera-fit.md`. Presentation outputs are watermarked; clean renders are retained separately.

## Tested authoring path

Run from the project root. These exact build/render combinations were exercised into `verification/`, independently of the delivered scene. Choose a new directory if retaining every verification attempt is important.

```sh
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-02/scripts/realism_run.py build --round 3 --directory verification
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-02/scripts/realism_run.py reproduce --blend verification/ready2jet.blend --directory verification/check --frames 1,95,145 --samples 24
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-02/scripts/realism_run.py render --blend verification/ready2jet.blend --directory verification/detail --camera Camera_Material --frames 1 --size 900 --samples 48
```

Open, middle and folded verification images are pixel-identical to fresh-process renders of the delivered scene. Material close-up reproduction is recorded in `records/final-build-comparison.json`.

The authoritative build is **realism_run.py build --round 3**. It calls the copied `geometry.py` revision-3 construction, replaces soft topology, hooks the refined coordinate functions into the copied `rig.py`, regenerates every shape key and rest UV, then applies procedural materials. It requires these local scripts, **not a baseline .blend**. `blender_run.py` is retained for the original baseline reproduction; it does not implement the new realism pass. Script snapshots under the round folders preserve history and are not the supported entry points.

Recreate the full native clean sequences (these commands were exercised with these settings):

```sh
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-02/scripts/realism_run.py render --directory final/frames-main --camera Camera_Reference --frames 1:194 --width 1280 --size 720 --samples 24
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-02/scripts/realism_run.py render --directory final/frames-rear --camera Camera_RearRight --frames 1:194 --width 1280 --size 720 --samples 20
/Users/ramyamanchikanti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 poc-astra-ready2jet/run-02/scripts/deliver_media.py
```

The compositor replaces presentation outputs in `run-02/final/` and expects the delivered still/detail PNGs, reference files, source photo and local Arial fonts. The scene itself has **no external textures or simulation caches**. All shader nodes are procedural. All write arguments in the new Blender entry point are constrained to this run; .blend backups are disabled. Installed Blender may support `--background --python ... -- ...`, but that alternative executable command was **not tested** here.

## Editing and evidence

Meters; X forward, Y left, Z up. Named `RIG_*` empties carry baked transforms, not interactive stage drivers. `RIG_support` stage properties are readouts. The source-time event table and release-before-collapse order remain unchanged. Frames 1–37 prepare, 43–55 thumb slide, 58–70 lever squeeze, 73–137 continuous collapse at 2× slow motion, then final hold through 193. Secure/carry is source-backed text, not simulated activity.

`realism.py` contains soft-surface geometry, attachments, metric UVs, procedural materials and new cameras. Soft surfaces use world-space coordinates and remain unparented; hems share those functions. Topology changes require regenerating Basis, all keys and UVs together. Parts retain names; wheel inset replacements are identified in object properties and the evidence record.

`baseline/` preserves the delivered run-01 scene and exact script copies. `baseline-rebuild/` establishes pixel-identical reproduction of its current scripts. `round-1/`, `round-2/`, `round-3/` retain the bounded checkpoints. Original run-01, original prompts, source vault and application files were not edited.
