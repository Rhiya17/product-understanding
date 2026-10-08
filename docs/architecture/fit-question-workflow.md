# Fit questions: from the question box to a checked video

*2026-10-07 · Implemented and tested offline; no paid generation run yet*

## Executive summary

- **A question like "Can I fit the Ready2Jet stroller in a Tesla Model Y trunk?" now goes through the normal ShowMe workflow.** Nothing is written by hand for that question.
- **The answer is calculated from verified measurements only.** If a measurement it needs is missing, the answer says "very likely, not confirmed" and names the missing measurement. If the measurements say it does not fit, it says no. It never invents a fit.
- **The same calculation automatically becomes the video brief.** The website's existing video request, the worker, Astra (which writes the Blender scene), the Claude critic, rendering and playback all run as they do for folding and headphones videos.
- **New automatic geometry checks** run inside the sandboxed Blender build. The video is rejected if the stroller passes through any part of the trunk, floats, sits too close to the closed liftgate or seatback, or if anything is drawn at the wrong size.
- **A checked video is reused** for any wording of the same fit question, until the evidence changes.

## How it works

| Stage | What happens | Code |
|---|---|---|
| 1. Recognise | The question mentions fitting and a trunk. One named product has folded-size claims (the object) and another has trunk-measurement claims (the space). | [`system/fit_answer.py`](../../system/fit_answer.py) `fit_pair` |
| 2. Gather evidence | Every claim stating each measurement is found by its wording, not hand-picked. Only claims that passed the automatic publishing checks are used ([policy](auto-publish-policy.md)). | [`system/fit_engine.py`](../../system/fit_engine.py) `build_case` |
| 3. Calculate | Every orientation is tried. Conflicting sources are combined cautiously: the largest stroller size, the smallest trunk size. Unknown measurements stay unknown; the engine reports how much each one could vary before the fit fails. | `run_case` |
| 4. Answer | Verdict, the numbers with their sources, how to place it, what is not verified, and the Tesla liftgate and loading warnings. | `fit_answer.answer` |
| 5. Brief | The calculation becomes four steps (`fit_step_fold`, `fit_step_open`, `fit_step_place`, `fit_step_close`), a scene brief (sizes, orientation, placement, evidence, what to disclose) and a geometry-check spec. A video is only briefed when the verdict is "fits" or "very likely fits". | [`app/pipeline/fit_brief.py`](../../app/pipeline/fit_brief.py) |
| 6. Generate | The normal `author` job: Astra writes the scene to the brief, and the trusted runner builds it and runs the fit checks. Failures go back to Astra to repair. The critic reviews, then the final render is made. Spend is reserved before every paid call. | [`app/pipeline/authoring.py`](../../app/pipeline/authoring.py), [`app/worker.py`](../../app/worker.py) `job_steps` |
| 7. Check geometry | Every frame: no part of the stroller passes through the floor, sides, seatback, liftgate or ceiling. Last frame: it rests on the floor with the required gap to every surface. Its size matches the evidence within 6%, and the trunk's floor depth and height match within 2%. | [`app/render/fit_checks.py`](../../app/render/fit_checks.py) |
| 8. Play and reuse | The published video plays in the answer; its chapters match the "How to place it" rows. The reuse key is the product pair plus their evidence, not the question wording. | `authoring.input_fingerprint` |

## What the current evidence gives

Ready2Jet in a 2025+ Tesla Model Y, laid flat with its long side across the car:

| Check | Needs | Has | Result |
|---|---|---|---|
| Height with the liftgate closed | 32 cm | 68 cm (12365auto tape measurement) | Pass |
| Floor depth | 57 cm | 106 cm (12365auto; d1ev measured 108.5 cm) | Pass |
| Through the open liftgate | 84 cm | 114 cm (smallest measured opening span) | Pass |
| Floor width between the wheel arches | 84 cm | No verified measurement | Unknown |

So the answer is **"very likely, not confirmed"**. A video of it shows the floor at a width labelled as illustrative, and says so.

## Tests

[`app/tests/test_fit_video_route.py`](../../app/tests/test_fit_video_route.py) drives the real server, answer engine, evidence packs, store and worker; only the paid authoring call is faked. It covers:

- a website submission queuing one `author` job;
- the brief being built from the calculation;
- playback with chapters;
- a reworded question reusing the video with no second job;
- no video being offered or made when the verdict is "does not fit" or unknown.

It also runs the trusted runner in real Blender: a correct scene passes, and the same scene pushed 20 cm too far fails on the seatback. [`system/tests/test_auto_publish.py`](../../system/tests/test_auto_publish.py) and [`system/tests/test_fit_answer.py`](../../system/tests/test_fit_answer.py) cover the policy, discovery and answers.

## Limitations

- **Not yet run with paid generation.** The acceptance test is to ask the question on the website and get a checked, playable video. It needs Astra (OpenAI), the critic (Anthropic), Blender and the video budget configured, as for any other new video.
- **The trunk is drawn by Astra from measurements and photos**, not from a 3D scan, so shapes no measurement covers (trim curvature, wheel-arch bulge) are approximations. The checks cover the dimensions that decide the fit.
- **Only rear-trunk fits of a folded object are modelled.** Other spaces (frunk, overhead bin) need their own measurement wording in `SPACE_RULES` and their own colliders.
