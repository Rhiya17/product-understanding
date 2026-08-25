# POC 5: Static Digital Twin from Curated Images

Execution follows [docs/pocs/poc5-digital-twin-runbook.md](../docs/pocs/poc5-digital-twin-runbook.md);
decisions behind it are in
[docs/planning/digital-twin-phase-plan.md](../docs/planning/digital-twin-phase-plan.md).

**Question:** can multi-image image-to-3D services produce a usable static
mesh of the Graco Ready2Jet (gray/tan colorway) from 4 curated views — and
how badly are the moving parts fused (the POC 6 cost driver)?

## Inputs

4 input views + 1 held-out validation image + 1 folded-state image for a
separate future job. Full provenance, hashes, roles, and accepted risks:
[`inputs/source-manifest.json`](inputs/source-manifest.json).

Known accepted risks: three canopy configurations across inputs, no true
rear view, one close-up input, view-02 SKU confirmation pending.

## Running

```bash
pip3 install fal-client requests
echo 'FAL_KEY=key_id:key_secret' > .env     # never commit; .gitignore covers it
set -a; source .env; set +a

python3 run_meshy.py --label meshy-run-01 --dry-run   # inspect exact request
python3 run_meshy.py --label meshy-run-01             # ~5-10 min per Meshy run
```

Endpoint: `fal-ai/meshy/v6/multi-image-to-3d` (schema verified live
2026-08-13; **no seed parameter** — runs are stochastic, do 3).
`symmetry_mode` is `off` because the cup holder is one-sided; auto/on risks
mirroring it into invented geometry (hard-fail check 4d).

Rodin and Hunyuan 3D runners follow after the Meshy probe validates the
artifact flow (verify their fal endpoint schemas first, same as Stage 0).

## Scoring

Runbook Stages 3–5: normalize scale against verified dimensions (record them
in the manifest first — currently missing), silhouette/landmark checks
against the held-out image, invented-geometry inspection, fusion grade
F0–F3, scorecards in `evaluation/`.
