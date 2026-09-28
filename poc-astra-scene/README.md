# Astra → Python → Blender proof of concept

The problem: create a persistent, editable 3D set from a text description,
then obtain different shots without regenerating the building for every image.
Higgsfield is not used. Blender's Python module constructs and saves the scene;
Cycles renders it locally on the CPU.

## Scope

An Opera House–inspired stylized set with seven separate roof shells, a stepped
plaza, a ferry, a fictional interior, 96 individual seats, three cameras, and
day/sunset lighting. This is a workflow experiment, **not a faithful replica**.
The shell formula is an artistic approximation. Actual Opera House shells use
spherical geometry: https://www.sydneyoperahouse.com/our-story/the-spherical-solution
Neither the interior nor the proportions have been validated against plans.

## Run

Requires Python 3.11 and `bpy==5.0.1` (the runtime used for this experiment).

```sh
python3.11 -m venv /tmp/astra-blender-venv
/tmp/astra-blender-venv/bin/pip install bpy==5.0.1
/tmp/astra-blender-venv/bin/python build_scene.py
```

Or run the script with an installed compatible Blender:

```sh
blender --background --python build_scene.py
```

Outputs in `output/`: editable `.blend`, four PNG images, and `validation.json`.
The script compares hashes of mesh vertices, faces, and object transforms
across the camera/lighting changes. It also moves and restores a named wall.
These checks test static geometry continuity and editability; they do not
measure landmark fidelity, image quality, interior connectivity, or performance
on arbitrary prompts. The script is authored for this scene, not a general
text-to-3D application.

## What the next POC should measure

1. Reference fidelity: agree on exterior and interior reference views, model
   from them, then compare unseen camera views against independent references.
2. Edit locality: render an intentional wall/prop edit and check that only
   the intended object and its physical lighting effects change.
3. Connected space: animate one camera from plaza through a modeled doorway
   into the hall, checking collisions and revealing missing geometry.
4. Production quality: improve roof geometry, materials, glazing, detail,
   lighting, and render samples before judging cinematic suitability.

The reusable architecture is prompt → structured scene specification → Blender
builder → saved `.blend` → camera/lighting/edit commands → renders + validation.
A GPU or render farm can accelerate rendering; it does not establish accuracy
of generated geometry.

## Executed result

Ran on this Mac using Blender 5.0.1 / Cycles CPU, 16 samples, 960×640.
All four renders completed; 225 mesh objects retained identical geometry
hashes across camera and lighting changes. The named-wall mutation and restore
checks passed. Exterior, interior, and sunset outputs were visually inspected.
The result is a basic blockout with visibly simplified roof forms, sparse
materials, and an unfinished interior, not cinematic or architecturally accurate.
The Python runtime required execution outside the filesystem sandbox.
