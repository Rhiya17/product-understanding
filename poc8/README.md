# POC 8 — deterministic rigid-body connection scene

This directory implements `docs/workorders/workorder-poc8-connection-scene.md`.
It is intentionally isolated from the application and evidence-pack runtime.

All outputs are **INTERNAL ONLY**. The two Tripo3D inputs have an open license
review and may not be published or served.

## Reproducible entry points

```bash
BLENDER=/Users/vbp/Applications/Blender.app/Contents/MacOS/Blender

# Stage B: import, measure, repair scale, and render the two Gate 1 attempts.
"$BLENDER" --background --python poc8/repair_twins.py

# Gate 1 identity verification (requires FAL_KEY; hard spend guard is $10).
set -a; source ~/.config/showme/fal.env; set +a
export FAL_KEY="${FAL_API_KEY:-$FAL_KEY}"
python3 poc8/verify_gate1.py

# Validate artifacts and trust controls.
python3 poc8/validate_poc8.py
```

`repair_twins.py` is safe to rerun: it replaces only generated Stage B files
under `poc8/out/gate1/`. A rerun also removes the live Gate 1 verdict, so the
verifier cannot accidentally reuse a result for changed pixels.

## Current terminal state

Gate 1 is **FAIL**: Bose identity passed on attempt 1; MacBook identity failed
both permitted attempts. In accordance with governing rule 4, Stages C–G were
not authored or run, and no `scene.blend` or connection video exists. Replace
the MacBook GLB with a recognizable, right-jack-preserving scan, update its
hash/path in `config.json`, and rerun Stage B before implementing later stages.

## Important modeling constraint

The catalog MacBook mesh is an open/ambiguous scan, while the only authoritative
height claim is the **closed** height. The work order explicitly requires
per-axis scaling to that claim. The repair therefore records this state mismatch
instead of hiding it; a recognizable identity verdict is still required before
the repaired mesh can be used downstream.
