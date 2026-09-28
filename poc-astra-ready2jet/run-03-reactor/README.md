# Reactor realism trial

Status: input prepared; generation has not started. Waiting for Reactor sign-in.

The user requested a short Reactor realism experiment using the existing Blender animation. This is a separate internal research trial. Earlier runs and source records are unchanged.

## Prepared input

- `input/fold-clean-720.mp4`: all 193 frames from run-02's main raw render, 24 fps, approximately 8.04 seconds, cropped to 720 × 720 without rescaling.
- Source: `../run-02/final/frames-main/Camera_Reference-%04d.png`, frames 1–193.
- Crop: x=114, y=0, width=720, height=720, matching the existing diagnostic crop.
- The presentation MP4 was not used: it contains a manufacturer reference-image inset. The new clip contains only the procedural Blender render, without reference photographs, manual panels, presentation labels, or audio.
- Source geometry remains an inferred Kingston-reference reconstruction; exact SKU applicability and mechanical accuracy are unresolved. This preparation does not grant or change source rights or asset approval.

## Intended first trial

Playground: https://www.reactor.inc/models/sana-streaming

Select Video clip, choose the prepared MP4, and use `prompt.txt`. Attempt one short edit and capture the complete output before disconnecting. Preserve the captured original and record the model, prompt, settings exposed by the playground, actual session duration, and any displayed credit consumption. Prompt constraints are requests, not guarantees of preservation.

Compare open, prepared, mid-fold, and folded frames against the input. Check fabric and lighting realism separately from changes to component count, controls, belly-bar color, silhouette, attachments, fold direction/timing, and continuity across frames. Record missing frames or timing changes rather than treating them as a complete matched comparison.

## Access check

The current shell has no configured REACTOR_API_KEY. The Reactor playground is signed out. Its login screen offers Google, GitHub, or email and states that continuing accepts its Terms of Service and Privacy Notice. The browser tab is left at sign-in for the user. No file has been uploaded and no generation session has been started. Actual generation cost and output quality are unknown.

## Re-create the input

Run from the repository root, choosing a new output path if the file already exists:

```sh
ffmpeg -v error -framerate 24 -start_number 1 -i poc-astra-ready2jet/run-02/final/frames-main/Camera_Reference-%04d.png -frames:v 193 -vf crop=720:720:114:0 -an -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart -n poc-astra-ready2jet/run-03-reactor/input/fold-clean-720.mp4
```
