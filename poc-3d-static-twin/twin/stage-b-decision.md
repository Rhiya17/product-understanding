# Stage B geometry decision

## Verdict

**B2 parametric rebuild wins.** The work-order expectation is confirmed.
The Tripo mesh remains a hidden, hash-pinned dimensional scaffold; it is not
cut into production rig parts.

## Handle spike

Both branches ran headlessly in Blender 5.2.0 LTS against
`tripo-probe-01`, pack hash
`da454173c3733e0227d90f869925145897669e96df8f7c593f0f45be94d8a83f`.
Detailed machine metrics and renders are in `stage-b-spike/`.

| Branch | Agent time | Result | Rig readiness |
|---|---:|---|---|
| B1 surgery | 0.1 h | Spatial handle-envelope cut: 15,982 faces, 40 connected components, 2,208 boundary edges. Hole fill still left 155 boundary and 964 non-manifold edges, and the result visibly includes canopy/soft goods. | FAIL |
| B2 rebuild | 0.1 h | Ten named manifold objects: lower/upper tubes, patent-118 pivots, grip, housing, thumb switch, and squeeze lever. Aggregate boundary edges: 0. | PASS |

Surgery cannot expose patent pivot 118 without arbitrary topology decisions;
closing its cut loops creates surfaces absent from evidence. Rebuild exposes the
joint as an object boundary and keeps simplified geometry visibly labeled.

## Full Stage B build

`build_twin_geometry.py` creates `ready2jet-stage-b.blend` with:

- front and rear frame members around patent hub 112;
- split handle assembly, pivot 118, thumb switch, and squeeze lever;
- seat/backrest unit and fold-relevant canopy;
- four tri-spoke wheel assemblies;
- simplified basket, belly bar, and cup holder;
- a hidden `REFERENCE_SCAFFOLD_INTERNAL_ONLY` collection carrying Tripo run,
  pack, asset-hash, and open-license metadata.

The rebuilt open envelope is 0.6902 x 0.5340 x 1.0935 m D x W x H versus
the official 0.6858 x 0.5207 x 1.0922 m: +0.64%, +2.55%, and +0.11%.

## INFERRED geometry after Stage B

- seat/backrest linkage and soft-goods thickness;
- canopy fabric deformation and rib linkage;
- basket rear/unseen surfaces;
- cup-holder mount/wall details;
- rear axle surface and rear-facing wheel details;
- all hidden cables, locks, slider, spring, and hub-linkage surfaces (their
  behavior is patent-documented, but they are intentionally not exposed).

The rebuild is an internal mechanism visualization, not a manufacturing CAD
model. Nothing in this stage changes the open Tripo3D license status.
