# Ready2Jet / Kingston-reference reconstruction

**Partial illustrative result. INTERNAL RESEARCH. Exact SKU applicability unresolved.**

This run constructs a fresh editable stroller exterior and tests its visible folding motion. Folded compactness improves substantially over the archived twin, but the canopy, upholstery, rear detail, and intermediate motion fit remain approximate. No hidden production mechanism or physical fit is validated.

## Open these

- [Editable Blender scene](final/ready2jet.blend)
- [Main folding clip](final/fold-main.mp4) and [GIF preview](final/fold-main-preview.gif)
- [Synchronized rear-right diagnostic](final/fold-rear-right.mp4)
- [Release-control source panel](final/release-control-source-panel.png) and [3-second panel clip](final/release-control-source-panel.mp4)
- [Open/middle/folded comparison](final/open-mid-folded-comparison.jpg)
- [All five source stages](final/five-stage-comparison.jpg)
- [Extended-canopy appearance comparison](final/open-appearance-comparison.jpg)
- [Report](report.md), [input manifest](input-manifest.json), [part/joint evidence](part-joint-evidence.json), [action mapping](action-event-map.json)
- [Early editable scene](early/ready2jet.blend) and [early articulation milestone](early/open-mid-folded-clay.jpg)

## Actual runtime

macOS 26.6.2, arm64; Python 3.11.4; Blender Python module **5.0.1**; **Cycles CPU**. FFmpeg **8.0.1**, libx264. Pillow **12.3.0** in the bundled Python runtime. The isolated bpy runtime required normal permission escalation because importing it inside the filesystem sandbox exited with signal 11. It never touched an open Blender session.

Blender geometry and rig use only bpy, mathutils, and Python's standard library. Materials are procedural; there are no external textures to resolve or pack. The scene itself is portable. Reference/media composition expects the archived source files in this repository and the local Arial fonts used by this Mac.

## Reproduce without replacing the delivered scene

Run from the project root. These commands save a new `rebuild/` subdirectory within this run.

```sh
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-01/scripts/blender_run.py build --revision 3 --directory rebuild
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-01/scripts/blender_run.py reproduce --blend rebuild/ready2jet.blend --directory rebuild/check --frames 1,73,95,145 --size 640 --samples 16
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-01/scripts/blender_run.py render --blend rebuild/ready2jet.blend --directory rebuild/frames-main --frames 1:194 --size 720 --samples 16
/private/tmp/astra-blender-venv/bin/python -u poc-astra-ready2jet/run-01/scripts/blender_run.py render --blend rebuild/ready2jet.blend --directory rebuild/frames-rear --camera Camera_RearRight --frames 1:194 --size 720 --samples 12
```

An installed compatible Blender may instead run the same entry point as `blender --background --python /absolute/path/to/scripts/blender_run.py -- build --revision 3 --directory rebuild`. Only the bpy command above was actually exercised here.

To recreate the **delivered presentation media**, with the delivered clean PNG sequences already present:

```sh
/Users/ramyamanchikanti/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 poc-astra-ready2jet/run-01/scripts/compose_media.py
```

That command replaces only presentation outputs under this run's `final/`. Full clean sequences are in `final/frames-main/` and `final/frames-rear/`; they have no watermark. Composed media carry INTERNAL RESEARCH. The main and rear clips each contain all 193 frames, 24 fps, 1280×720, without audio.

Reference curation can be replayed with the bundled Python and `scripts/curate_references.py`. It reads and hashes the archived sources, extracts the five chosen video frames with FFmpeg, and writes local reference sheets. It does not modify sources. The original manual's printed/PDF pages 33–35 were checked with local Poppler; page 34 was independently rasterized under `references/`.

## Edit the scene

Meters: X forward, Y left, Z up. Named `RIG_*` empties carry baked, editable transform keys. Geometry remains separate under stable `part_id` names. Curved frame/grip parts stay curves; fabric remains custom subdivided meshes with editable shape keys.

`scripts/geometry.py` contains the exterior geometry and camera definitions. `scripts/rig.py` contains the source-time event table, joint rotations and fabric envelope functions. `RIG_support` stage properties are animated readouts, not a validated mechanical solver or interactive driver controls. Change the event table and rebuild to coordinate a new action.

Frames 1–37 prepare, 43–55 slide the thumb switch, 58–70 squeeze the lever, 73–137 show the continuous fold at **2× slow motion**, and 138–193 hold the settled result. Preparation/release timing is illustrative because the source uses separate shots. The secure/carry sequence is communicated in panels, not physically executed.

Earlier `early/`, `revision-1/`, `revision-2/`, and `revision-3/` scenes retain useful partial work. Revision 3's final review corrected seat timing and softened a rear-lining artifact; the delivered implementation is `scripts/` plus `final/ready2jet.blend`. Earlier snapshots intentionally show the preceding stages and should not be run against historical output directories.
