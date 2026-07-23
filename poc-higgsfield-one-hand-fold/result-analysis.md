# Run 1 result: FAIL under uncontrolled defaults

## Generation

- Model: `dop-turbo`
- Request ID: `dbdc598f-ac1b-47e5-b933-4ef41a311faf`
- Output: `out/ready2jet-one-hand-fold.mp4`
- Duration: 5.37 seconds
- Resolution: 736 x 1248
- Contact sheet: `out/contact-sheet.png`

The exact submitted body is stored in `out/submission.json`; the final API
response is stored in `out/result.json`.

## What actually happened

The video did not show a one-hand fold. The stroller stayed open for the entire
clip. As the camera moved from a side view toward the front, Higgsfield gradually
changed the source Ready2Jet into a different, larger stroller.

Visible failures:

- The adult used both hands around the handle/canopy area.
- No clear thumb-switch slide or underside-lever squeeze was shown.
- A large red control appeared in the center of the handle even though it was
  not present in the source frame.
- Other red controls appeared near the seat and rear wheel.
- The seat, canopy, belly bar, front assembly, frame, wheel geometry, and fabric
  changed over time.
- The stroller grew into a full-size open stroller instead of collapsing.
- The product logo became unreadable/invented.
- The camera moved to a front view despite the locked-camera instruction.
- The final frame did not resemble Graco's compact, self-standing folded
  reference.

## Scorecard

| Required check | Result |
|---|---|
| Same Ready2Jet identity and parts throughout | No |
| Exactly one hand activates the fold | No |
| Correct thumb-switch location is visible | No |
| Same hand squeezes the underside lever | No |
| Other hand stays away | No |
| Automatic fold is mechanically plausible | No - no fold occurred |
| Wheels and frame remain stable | No |
| Final shape matches official folded reference | No |
| Final stroller is self-standing and folded | No |
| No child or infant car seat is present | Yes |
| No hand/part intersections or mutations | No |
| No invented controls, parts, or logo mutation | No |

## Attribution caveat

This run is an operational failure, but it is **not** a clean prompt-adherence
experiment. The server echoed `enhance_prompt: true` even though the client did
not request prompt enhancement, so the submitted prompt may have been rewritten.
It also injected a camera-motion preset at strength `1.0` even though the client
sent no motion setting. Those uncontrolled defaults plausibly contributed to
the camera swing and scene reinvention.

Therefore, Run 1 cannot support a claim about what DOP does with the exact prompt
under static-camera settings. It remains useful evidence that Higgsfield's
defaults are unsafe for instructional generation. The corrected experiment uses
the live endpoint's `dop-preview` tier, `enhance_prompt: false`, a required motion
entry at strength `0.0`, fixed seeds, and verifies the server-effective
parameters before accepting each run. (`dop-standard` and an empty motion list
were both rejected by the live endpoint before any generation began.)
