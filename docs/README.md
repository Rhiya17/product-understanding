# Docs

| Folder | Contents |
|---|---|
| `architecture/` | The system's design: `system-architecture.md` (v3.6 blueprint), `showme-system-architecture.md` (v3.1 sibling), `high-level-design.md`, `low-level-design.md`/`.html` (v0.7 normative contracts; kept in sync by `scripts/check_docs_sync.py`), `lld-visual-guide.html`, `aws-evidence-extraction-architecture.md` (deferred cloud posture — the MVP is local-first) |
| `workorders/` | Executable contracts handed to agents or people: evidence-pack extraction (§6 per-product checklists), Ready2Jet gap closure, and the extraction-system build spec (the four-stage Detective/Guard-Dog/Verifier/Judge pipeline) |
| `pocs/` | Probe findings and runbooks: Higgsfield (fold FAIL 0/3), Seedance + keyframe chain, VLM verifier (Qwen 6/6 vs Claude 5/6), RLDX-1 evaluation (rejected), POC 5 digital-twin runbook, reference-image curation, video-generation alternatives |
| `planning/` | Strategy and cross-cutting findings: the digital-twin phase plan (9 decisions), the agentic source-collection design note, the extraction-systematization findings (go/no-go experiment for the automated system), and open questions for Koustubh |

Machine-facing contracts that agents consume live outside `docs/`, next to
their data: `evidence-packs/workorders/*.json` (per-product extraction
contracts + the standing agent brief) and each pack's
`gaps.json` / `reviews.json` / `verdicts.json`.
