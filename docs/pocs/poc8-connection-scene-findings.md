# POC 8 — rigid-body connection scene findings

**Verdict after three runs: Gate 1: FAIL — Tripo H3.1 cannot deliver a
MacBook Air twin with port-level detail.** The Bose twin passes; the
deterministic connection scene must not be built from a scan-based MacBook
twin. See "Run 2–3: owner-approved re-scan" below for the decisive evidence.

**Trust:** INTERNAL ONLY — TWIN RENDER. `approved_by: null`. Tripo3D license
review remains open. No artifact was registered or exposed to the app.

## Direct finding

Per-axis repair removed the known scale errors from both GLBs, but scale repair
cannot create missing geometry. The repaired Bose twin remained recognizable
and passed its first VLM identity check. The MacBook twin still lacks a visible
right-side 3.5 mm jack, contains invented/debris-like structures, and does not
read as a credible MacBook Air profile. It failed both permitted VLM attempts.

The governing stop-and-report rule therefore ended the POC at Stage B. No
cable, animated scene, CG connection video, VACE skin, or Seedance comparison
was produced.

![Gate 1 comparison contact sheet](../../poc8/out/gate1/contact-sheet.png)

## Stage outcomes

| Stage | Outcome | Evidence / reason |
|---|---|---|
| A — ground truth | PASS | Checklist and claim/source mapping in `poc8/evidence-map.md` |
| B — twin scale repair | PASS | Both post-repair worst-axis errors below 0.00001%; see per-product `scale-repair.json` |
| Gate 1 — identity | **FAIL** | Bose PASS first attempt; MacBook FAIL twice |
| C — cable | NOT RUN | Prohibited after Gate 1 failure |
| D — scene and named actions | NOT RUN | Prohibited after Gate 1 failure |
| E — deterministic primary render | NOT RUN | Prohibited after Gate 1 failure |
| F — VACE skin arm | NOT RUN | No passing deterministic control input |
| G — Seedance comparison | NOT RUN | No passing deterministic first/last frames |
| H — report/registration | COMPLETE / NO REGISTRATION | Failure recorded; no pack binding created |

## Scale repair

Fresh headless imports reproduced the committed axis-aligned mesh extents with
0% discrepancy on every axis.

| Product | Raw AABB (m, XYZ) | Evidence target (m, XYZ) | Scale factors (XYZ) | Post-repair worst error |
|---|---|---|---|---:|
| Bose QC Ultra | 0.110640 × 0.251158 × 0.250000 | 0.045009 × 0.159995 × 0.205003 | 0.406806 × 0.637028 × 0.820014 | 0.0000083% |
| MacBook Air 13 M3 | 6.243679 × 2.433347 × 1.000000 | 0.304100 × 0.215000 × 0.011300 | 0.048705 × 0.088356 × 0.011300 | 0.0000082% |

The MacBook Z target is the manufacturer **closed-height** claim applied to an
open/ambiguous scan because the work order explicitly requires per-axis repair
to the committed dimension claims. That known state mismatch was disclosed
before rendering. It does not explain away the missing jack or invented scan
artifacts, and the strict identity gate still controls downstream use.

## Gate 1 identity results

Verifier: `qwen/qwen3-vl-235b-a22b-instruct` through
`fal-ai/any-llm/vision`, temperature 0, parsed with the application's
fail-closed `parse_verdict`.

| Product / attempt | Verdict | Request ID | Visible basis |
|---|---|---|---|
| Bose / 1 | PASS | `01a0503f-08f6-79f3-bddd-bbb973f6549b` | Recognizable product, plausible proportions, no missing major structure |
| MacBook / 1 | FAIL | `01a0503f-3192-75e3-8f43-5294798062bd` | Missing jack, implausibly flat profile, invented undercarriage/fin |
| MacBook / 2 | FAIL | `01a0503f-4baf-7a10-b1ef-51e5a1a6bb98` | Missing jack and casing; exposed/invented structures persist from reverse side |

Full JSON verdicts are stored under `poc8/out/gate1/attempt-*/<product>/`.

## Correctness checklist and arm verdicts

| Requirement | Primary deterministic arm | VACE arm | Seedance arm |
|---|---|---|---|
| 2.5 mm end into LEFT earcup | NOT RUN | NOT RUN | NOT RUN |
| 3.5 mm end into Mac RIGHT-side jack | NOT RUN | NOT RUN | NOT RUN |
| Both products match official photos | **FAIL at Mac Gate 1** | NOT RUN | NOT RUN |
| No other scene object moves/appears | NOT RUN | NOT RUN | NOT RUN |
| Overall arm verdict | **FAIL CLOSED / NO VIDEO** | NOT RUN | NOT RUN |

## INFERRED list

The intended later scene declared these presentation-only inferences before the
gate ran: neutral desk and studio lighting; product separation/resting pose;
cable sheath diameter; cable slack path and bend radius; plug barrel/grip
length and finish; exact port coordinates on imperfect twins; camera focal
lengths and framing. None became a Stage C–G artifact because those stages were
not run.

## Spend ledger

| Use | Requests | Spend |
|---|---:|---:|
| Local Blender 5.2.0 repair + renders | local | $0.00 |
| Qwen Gate 1 checks | 3 × $0.01 | $0.03 |
| VACE | 0 | $0.00 |
| Seedance | 0 | $0.00 |
| **Total** | **3 external requests** | **$0.03 / $10.00 ceiling** |

The authoritative request ledger is `poc8/out/spend-ledger.json`.

## Registration and routing decision

**No registration.** Gates 1–3 did not all pass, so no derived asset or media
binding was added to the Bose evidence pack. The rigid-body route is recorded
as `POC8: FAIL at Gate 1 — new Mac twin required`; it must not be selected for
serving.

## Required next input

Re-scan the MacBook from compatible, annotation-free open-state views including
a true right-side view where the sole 3.5 mm jack is visible. The replacement
must pass dimension and identity gates and its license must be cleared before
this POC resumes at Stage C. Rescanning is explicitly outside POC 8's budget and
scope.

## Run 2–3: owner-approved re-scan (2026-08-29)

After run 1's fail, the owner approved a Tripo H3.1 **re-scan** of the
MacBook with high-quality inputs. Root cause of the original scan was
identified first: its input set mixed an OPEN front view with a CLOSED-state
guide diagram containing callout graphics.

**New inputs (all official Apple, consistent OPEN state, midnight):**
newly captured vault source `src_img_store_open_side_profiles` (2400px store
gallery asset `mba13-m3-midnight-gallery3-202402`, both true side profiles,
jack visible) split into derivation-recorded left/right crops
(`poc8/inputs/`), plus the existing `src_img_store_midnight` front view.
`src_img_store_closed_side_ports` (gallery6, port close-ups) was also
captured as future verification evidence. Submission:
`poc8/twins/macbook-rescan/` (request `01a0…`, $0.60).

**Result: geometry recovered, ports did not.** The re-scanned twin has a
credible open-laptop silhouette, correct claim-derived proportions after
per-axis repair (depth/width claims; open height INFERRED from scan
proportions — no claim documents it), a readable keyboard deck and screen.
But at port level the scan is wrong: the right side carries **invented
rectangular slots mirrored from the left side** where the real machine has a
single 3.5 mm jack near the front, and no distinct jack exists anywhere.
Two render-pipeline defects found during verification were fixed and
documented in `repair_twins.py` (HASHED alpha → translucent look; area-light
overexposure washing dark PBR textures) — presentation-only corrections that
did not change the verdict.

An intermediate verification round (3 VLM checks, ledger ids 01a05051/2-*) ran before the render fixes and failed on the translucent-material look; its verdict artifacts were overwritten by the Stage B rerun because `repair_twins.py` deleted its output directory on rerun — that destructive behavior is now fixed (reruns archive to `gate1-archived-<ts>/`), and the round's reasons survive in the spend ledger and session record.

**Formal Gate 1 (run 3): Bose PASS (first attempt), MacBook FAIL (both
attempts).** Run 1's artifacts are preserved in `poc8/out/gate1-run1-fail/`.

**Provenance correction:** run 1 cited the Bose *weight* claim as the source
of its dimension targets. The targets themselves matched the vault spec
source; the citation now correctly reads `src_specs_curated_v1`
(specs/specs.md: "Headphones: 1.772\" H x 6.299\" W x 8.071\" D"), with the
axis mapping recorded INFERRED.

## Conclusion for the routing table

Two independent scans, correct inputs on the second, same failure class:
photogrammetry-style generation does not reproduce **port-level detail** on
thin, feature-sparse electronics — and a connection video's money shot is
exactly a port. For the rigid-body route this leaves the parametric
evidence-modeled path (base prism from `claim_mba_spec_width/depth/height`,
jack placed per `claim_mba_part_headphone_jack` and the captured
`src_img_store_closed_side_ports` close-up, surfaces via the repo's proven
photo-projection method) as the recommended Stage B-alt. The Bose twin
(passed) and the modeled cable plan are unaffected.

## Updated spend ledger (all runs)

| Entry | Cost |
|---|---|
| Run 1: 3 VLM identity checks | $0.03 |
| Run 2: Tripo H3.1 re-scan | $0.60 |
| Run 3: 3 VLM identity checks | $0.06 |
| **Total ($10.00 ceiling)** | **$0.69** |
