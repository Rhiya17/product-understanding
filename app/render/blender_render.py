"""Render frames from a saved ShowMe scene. Runs inside Blender:

    Blender --background --factory-startup --python app/render/blender_render.py -- \
        --blend SCENE.blend --camera Camera_Side --frames 1:193 --out DIR \
        --width 1280 --height 720 --samples 24

Opens the scene read-only (nothing is saved back) and writes numbered PNGs
plus render.json. Mirrors the run-02 video settings: Cycles, seed 0,
denoising, fixed vertical framing for orthographic cameras.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--camera", required=True)
    parser.add_argument("--frames", required=True, help="first:last inclusive")
    parser.add_argument("--out", required=True)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--samples", type=int, default=24)
    parser.add_argument("--device", choices=["CPU", "GPU"], default="GPU")
    parser.add_argument("--shift-x", type=float, default=0.0)
    return parser.parse_args(argv)


def use_gpu():
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        enabled = False
        for device in prefs.devices:
            device.use = device.type == "METAL"
            enabled = enabled or device.use
        return enabled
    except Exception:  # noqa: BLE001 - fall back to CPU on any device problem
        return False


def main():
    args = parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(Path(args.blend).resolve()))
    scene = bpy.context.scene
    if args.camera not in bpy.data.objects or bpy.data.objects[args.camera].type != "CAMERA":
        raise SystemExit(f"camera {args.camera!r} is not in the scene")
    scene.camera = bpy.data.objects[args.camera]
    render = scene.render
    render.resolution_x, render.resolution_y = args.width, args.height
    render.resolution_percentage = 100
    render.image_settings.file_format = "PNG"
    scene.cycles.samples = args.samples
    scene.cycles.seed = 0
    scene.cycles.use_denoising = True
    device = "CPU"
    if args.device == "GPU" and use_gpu():
        scene.cycles.device = "GPU"
        device = "GPU"
    camera = scene.camera.data
    if camera.type == "ORTHO":
        camera.ortho_scale = 1.35 * args.width / args.height
    camera.shift_x = args.shift_x

    first, last = (int(v) for v in args.frames.split(":"))
    started = time.time()
    for frame in range(first, last + 1):
        scene.frame_set(frame)
        render.filepath = str(out / f"frame-{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"SHOWME_PROGRESS {frame - first + 1}/{last - first + 1}", flush=True)
    record = {"blender": bpy.app.version_string, "camera": args.camera,
              "frames": [first, last], "fps": render.fps, "size": [args.width, args.height],
              "samples": args.samples, "device": device, "seconds": time.time() - started}
    (out / "render.json").write_text(json.dumps(record, indent=2))
    print("SHOWME_DONE " + json.dumps(record), flush=True)


main()
