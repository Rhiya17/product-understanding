# POC: What can Higgsfield actually do with computed geometry?

## The question this answers

The HLD assumes we can hand Higgsfield a "generation plan grounded in computed
geometry" and get back a video that respects exact dimensions and placement.
But the Higgsfield API accepts only **an image URL + a text prompt** (plus
motion preset / duration). There is no parameter for coordinates, dimensions,
or 3D constraints. So "geometry-constrained generation" can only mean one of:

- **H1 — prompt-only control:** describe the placement in words and hope.
- **H2 — render-then-animate:** *we* render the verified placement into the
  start image; Higgsfield only adds realism and camera motion on top of a
  frame that is already geometrically correct.
- **H3 — it can't be done**, and fit visualization should be a pure 3D render
  (CAD-style), with Higgsfield reserved for non-metric answers (folding
  demos, part highlights).

This POC produces the evidence to pick between H1 / H2 / H3.

## Files

| File | Role |
|---|---|
| `fit_engine.py` | Deterministic box-fit: enumerates valid stroller orientations in the trunk. Placeholder dimensions — swap in verified ones. |
| `render_placement.py` | Renders a chosen valid orientation to `out/placement_<i>.png` — the geometry-grounded start frame for H2. |
| `higgsfield_client.py` | Submit + poll the image-to-video API. Needs `HIGGSFIELD_API_KEY` (and secret if your account uses one); check the model path against your dashboard. |
| `verify_drift.py` | Extracts frames (ffmpeg) and measures drift vs frame 0 — the proxy check for "did the placement survive generation." |

## Setup

```bash
pip install matplotlib numpy requests
export HIGGSFIELD_API_KEY=...          # from your Higgsfield dashboard
# ffmpeg required for verify_drift.py
```

The API takes an image **URL**, so host `out/placement_0.png` somewhere
reachable (S3 presigned URL is fine) before Experiment 2.

## Experiments

Run each 3× (generation is stochastic and there's no documented seed on the
official API). Record results in the matrix below.

**E1 — prompt-only placement (tests H1).**
Start from a *real trunk photo* (no stroller) and prompt:
`"A folded navy stroller lying flat, diagonally, handle toward the left
taillight, in this open Tesla Model Y trunk"`.
Score: does the stroller appear at all / in the described pose / at plausible
scale? Expected: pose and scale are not reliably honored.

**E2 — render-then-animate (tests H2, the important one).**
```bash
python fit_engine.py                      # see valid orientations
python render_placement.py 0              # out/placement_0.png
python higgsfield_client.py <hosted-url> \
  "slow smooth camera orbit around the scene, objects perfectly still"
python verify_drift.py out/<result>.mp4
```
Score: does the blue box stay in position, keep its proportions, and keep its
edges across all frames? Try both a "camera only moves" prompt and a styling
prompt ("make it photorealistic, real stroller in a real trunk") — the second
is where morphing is most likely.

**E3 — stylized render-then-animate (H2 stretch).**
Same as E2, but the start frame is a *textured/realistic* render (or a
composite of real product photos placed at the computed position). Tests
whether realism can come from the start frame instead of from Higgsfield
reinterpreting the scene.

**E5 — first-last-frame interpolation (H2, strongest form).**
Probing the API revealed undocumented variants: `dop/lite/first-last-frame`,
`dop/standard/first-last-frame`, `dop/turbo/first-last-frame`. Render
orientation 0 as the first frame and orientation 1 as the last frame and let
Higgsfield interpolate — the geometry is then pinned at *both* ends by frames
we authored. This maps directly onto the "show me a different position"
follow-up. Score: does the in-between motion stay rigid and plausible?

**E4 — verifier feasibility probe.**
For the best E2/E3 output: can `verify_drift.py` + eyeballing confirm the
placement held? Then try to state a *numeric* acceptance rule ("reject if
final-frame drift > X in the object region"). If no rule survives contact with
three runs, automated verification of generated fit videos is not yet real.

## Results matrix (fill in)

| Exp | Run | Placement honored? | Proportions stable? | Morphing/artifacts | Verdict |
|---|---|---|---|---|---|
| E1 | 1 | | | | |
| E2 | 1 (dop/lite, orbit prompt) | 0–2s yes, then no | 0–2s yes | After ~2s the model reinvented the scene: trunk cavity → glass display case on a pedestal, added a dome, and the solid box morphed into an open-top tray. Drift metric: 0.02 @1s → 0.37 @5s. | Authored geometry survives ~2s, then generation takes over. Unconstrained i2v is NOT truth-preserving. |
| E3 | 1 | | | | |
| E5 | 1 (dop/lite/first-last-frame, orient 0→1) | Yes — both endpoints match the authored renders | Yes — container intact throughout, box stays a solid box | Mid-motion the box tips up on edge: a physically plausible-looking but UNVERIFIED path (the swept volume may exceed the 46 cm cavity height). Title text garbles mid-video. Drift: 0.04 peak mid-video, 0.016 at end (vs 0.37 for E2). | First-last-frame pinning works: endpoints are truth-preserved, hallucination suppressed. The in-between path is the model's invention and must not be presented as a maneuvering instruction. |

## Decision rule

- **E2/E3 mostly hold** → HLD keeps generation for fit answers, but reworded:
  *the system renders the computed placement and Higgsfield animates that
  render* — generation never originates geometry. Verifier checks drift vs the
  authored start frame, not "dimensions from pixels."
- **E2/E3 don't hold** → fit answers use the pure 3D render directly (still a
  video — camera orbit rendered by us), and Higgsfield is scoped to non-metric
  answers. Update HLD trust rule 5 and the fallback path accordingly.

Either outcome removes the unexamined assumption from the HLD.
