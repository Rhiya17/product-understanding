# Website video generation with Astra and Blender

Implemented 2026-09-27 at the owner's request. This supersedes the earlier
research-only/manual-review proposal for this local website integration.

The default v2 website route now uses:

1. Reuse a matching video, or render an already registered saved scene.
2. Otherwise persist an `author` job in SQLite and return immediately.
3. Snapshot verified procedure steps, authenticated official product photos and
   cited manual pages, including a named second device.
4. OpenAI `gpt-6-astra` returns structured Blender Python and a coverage timeline.
5. Execute that Python in a restricted macOS Blender subprocess, without keys,
   network access, a shell, or access to personal files. Render previews.
6. Astra sees those previews and fixes build or visible quality problems.
7. Claude checks the candidate against the references. Only a defect naming a
   provided reference, claim, preview timestamp, observation and concrete repair
   can request changes. Cosmetic feedback does not cause a rewrite.
8. At most one Claude-directed repair, followed by one Claude recheck. An
   unresolved defect, action-blocking evidence gap or unsupported finding stops the job.
   Harmless exterior simplifications belong in `visual_limitations`, are shown to
   the critic, and remain disclosed in the published video's caveat. They cannot
   excuse unknown compatibility, fit, socket location, product identity or action.
9. Render the accepted scene at 1280×720/24fps, encode MP4, verify duration,
   frame count and dimensions, recheck evidence eligibility/version, then
   atomically publish to My Videos. No human approval step is required.

## Limits and recovery

- Six Astra calls, four Blender builds, two Claude review passes, one critic repair.
  Each review pass allows at most two metered responses: 8,000 output tokens,
  then 16,000 only if the first response is incomplete. Refusals, evidence gaps
  and supported defects do not trigger that response retry. Both raw responses
  are saved before validation; another incomplete response fails visibly.
- Astra owns its self-check loop; Claude never plans shots or directs aesthetics.
- Each Astra call has a ten-minute timeout; preview builds eight minutes;
  final rendering sixty minutes. CPU limits account for all render threads
  (four for previews, eight for final renders), rather than treating cumulative
  CPU seconds as wall-clock seconds. The authoring loop checks a one-hour
  elapsed limit before starting another iteration.
- Provider retries are disabled. Interrupted paid jobs fail visibly; the worker
  never silently replays them. The user can explicitly start a new attempt.
- Before claiming another job, the worker checks the pipeline code's fingerprint
  and replaces its process when code changes, avoiding stale loaded versions.
  An active job finishes before this reload.
- Explicit retries reuse a saved candidate only if its evidence identity and
  scene, code, checks and preview hashes match. An unfinished review resumes
  at review; a passed review resumes at rendering. Completed rejected candidates
  cannot use this shortcut. No failed job is automatically replayed.
- The existing $5 per-video and $50 total runaway guards remain in effect.
  Input tokens are counted before reserving each call, and reservations settle
  to reported token usage. Unknown outcomes retain their reservation.
- API key lives in the ignored, owner-readable `.env`, beside existing keys.
- `SHOWME_VIDEO_PIPELINE=seedance` explicitly selects the older comparison path;
  there is no silent provider fallback.

## Artifacts and reuse

Each job retains its evidence snapshot, original/revised code, model usage,
preview frames, critic reports, Blender diagnostics, and final `.blend`/MP4.
Assets are versioned by pipeline version, question, named products and source /
review / verification file contents. A different question or changed evidence
cannot reuse a previous generated video. The exact requested camera is checked;
other views require their own request. The original stroller scene remains a
separate registered research artifact, with its existing caveat and serving policy.

## What the checks establish

The runner checks every frame for missing parts, nonfinite geometry, disappearing
parts and changes in object scale. It checks ordered, complete step metadata.
Claude and Astra inspect sampled frames spanning the timeline and step boundaries.
These are illustration-quality checks, not physical validation or a proof that
all interactions are correct. An unsupported physical action cannot be replaced
silently with a text slide. Declared nonvisual steps appear in the video caveat.

## Running locally

Use the repository Python environment:

```sh
.venv/bin/python app/server.py --port 8765
```

The server starts one worker. The ignored `.env` must contain `OPENAI_API_KEY`
and `ANTHROPIC_API_KEY`; Blender, FFmpeg and macOS `sandbox-exec` must be installed.
The startup message reports missing configuration. Open http://localhost:8765,
ask a procedure question and choose **Make a video**. Progress and completion
appear in **My Videos**.

Regression tests:

```sh
.venv/bin/python -m pytest app/tests/test_astra_authoring.py app/tests/test_video_pipeline.py app/tests/test_server.py app/tests/test_ui_contract.py -q
```

The provider boundaries are mocked in automated tests. A separate offline Blender
smoke run verified a real preview → saved scene → MP4 → playback-validation cycle.
A live provider test is a separate check; do not describe fixture results as a
successful Astra-generated product video.

API references used: [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
[structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
[pricing](https://developers.openai.com/api/docs/pricing?tab=suite).
