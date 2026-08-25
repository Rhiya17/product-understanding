# Evidence extraction system

This directory implements the four-stage evidence pipeline for Python 3.12.
Claims remain immutable `CANDIDATE` records; verifier findings live in
`verdicts.json`, and publication dispositions live in `reviews.json`.

Install the pinned runtime:

```bash
python3.12 -m pip install -r system/requirements.txt
```

## Run the stages

Stage 1 — Detective/orchestrator. A new extraction uses `--product`; an
existing pack must use append-only `--topup`. Each attempt runs in
`system/staging/`, passes the deterministic gate there, and is atomically
promoted only when green. The Claude Agent SDK uses its normal Claude
authentication (for API usage, set `ANTHROPIC_API_KEY`).

```bash
python3.12 system/extract_orchestrator.py --product <product>
python3.12 system/extract_orchestrator.py --topup <product>
```

Stage 2 — Guard Dog:

```bash
python3.12 evidence-packs/validate.py
python3.12 scripts/validate_vault.py
```

Stage 3 — Verifier. Set `FAL_KEY` in the process environment; never place it
in repository files or command arguments. The pinned independent model is
`qwen/qwen3-vl-235b-a22b-instruct` through `fal-ai/any-llm/vision`, prompt
version `v1`. No Claude/Anthropic model is permitted for this stage.

```bash
python3.12 system/verify_claims.py
python3.12 system/verify_claims.py --product <product>
python3.12 system/verify_claims.py --product <product> --conflicts
```

Exit codes are `0` complete, `10` complete with `MEANING_CHANGED` alarms,
`20` partial, `30` provider/credential failure, and `40` malformed provider
output after retry. Responses are cached under `system/cache/` using claim,
binding, quote hash, translation hash, tier, model, and prompt version. The
script reports an estimate using the documented model token prices; actual
provider billing can differ. A five-pack run is expected to stay within
single-digit dollars. Stop if projected spend would exceed that range.

Stage 4 — human queue:

```bash
python3.12 system/review_queue.py
python3.12 system/review_queue.py --product <product>
```

Queues are written as each pack's `review-queue.md`, ordered from semantic
alarms through conflicts, C3/C2, unresolved C0/C1 verification, gaps, and
auto-approval spot audits. Humans record decisions in `reviews.json`; they do
not edit claims or verdicts.

## Tests and live canary

The complete offline suite uses mocked providers and OS-temporary scratch
packs, never real pack mutation:

```bash
python3.12 -m compileall system/ evidence-packs/
python3.12 -m pytest -q system/tests
```

With `FAL_KEY` configured, the small manual canary is:

```bash
python3.12 system/tests/live_canary.py
```

Current repository note: the hardened vault validator intentionally reports
`source-vault/bose-qc-ultra-headphones/videos/video-sources.md` as an orphan
until an authorized manifest/source curation change registers or removes it.
The validator does not ignore or repair that user-owned file.
