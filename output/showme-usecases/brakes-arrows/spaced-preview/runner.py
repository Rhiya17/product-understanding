"""Trusted Blender runner, copied into a per-build OS sandbox.

Generated scene.py creates objects only. This runner owns persistence, frame
sampling and rendering. The OS sandbox (not Python filtering) enforces isolation.
"""
import json
import math
import resource
from pathlib import Path

import bpy

ROOT = Path.cwd()
# Bound crashes, memory and runaway writes independently of the host timeout.
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
resource.setrlimit(resource.RLIMIT_FSIZE, (2 * 1024**3, 2 * 1024**3))
contract = json.loads((ROOT / "contract.json").read_text())
# CPU time sums all render threads. The old 1,500 CPU-second limit could
# kill a healthy render after roughly six minutes despite its wall-clock limit.
cpu_seconds = 8 * 3600 if contract["mode"] == "final" else 4 * 480
resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))


def normalize(scene, width, height, samples):
    scene.camera = bpy.data.objects[contract["camera"]]
    scene.frame_start, scene.frame_end = 1, contract["last_frame"]
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x, scene.render.resolution_y = width, height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_border = False
    scene.render.use_sequencer = False
    scene.render.use_compositing = False
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.seed = 0
    scene.cycles.use_denoising = True


def sample_frames():
    last = contract["last_frame"]
    frames = {1, last}
    for step in contract["coverage"]:
        frames.update((step["start_frame"], (step["start_frame"] + step["end_frame"]) // 2,
                       step["end_frame"]))
    frames.update(round(1 + (last - 1) * i / 7) for i in range(8))
    return sorted(frames)


if contract["mode"] == "preview":
    default_handlers = {name: list(getattr(bpy.app.handlers, name))
                        for name in dir(bpy.app.handlers)
                        if isinstance(getattr(bpy.app.handlers, name), list)}
    code = (ROOT / "scene.py").read_text()
    exec(compile(code, "scene.py", "exec"), {"__name__": "__main__"})
    problems = []
    camera = bpy.data.objects.get(contract["camera"])
    if not camera or camera.type != "CAMERA":
        problems.append("named camera does not exist")
    for name in contract["parts"]:
        obj = bpy.data.objects.get(name)
        if not obj or obj.type not in ("MESH", "CURVE"):
            problems.append(f"missing visible part {name}")
    if len(bpy.data.objects) > 1000:
        problems.append("scene exceeds 1000-object limit")
    for obj in bpy.data.objects:
        if obj.animation_data and obj.animation_data.drivers:
            problems.append(f"drivers are not allowed: {obj.name}")
    if bpy.data.libraries or bpy.data.texts:
        problems.append("external libraries and executable text blocks are not allowed")
    for name in dir(bpy.app.handlers):
        handlers = getattr(bpy.app.handlers, name)
        if isinstance(handlers, list) and handlers != default_handlers.get(name, []):
            problems.append(f"runtime handler is not allowed: {name}")
    scene = bpy.context.scene
    observations = {}
    initial_scales = {}
    if not problems:
        # Check every frame, not only the critic's sampled images. Dimensions are
        # recorded for diagnosis; we do not claim they establish physical truth.
        for frame in range(1, contract["last_frame"] + 1):
            scene.frame_set(frame)
            for name in contract["parts"]:
                obj = bpy.data.objects[name]
                scale = tuple(obj.matrix_world.to_scale())
                if frame == 1:
                    initial_scales[name] = scale
                elif any(abs(a - b) > 1e-4 for a, b in zip(scale, initial_scales[name])):
                    problems.append(f"part changes scale: {name} at frame {frame}")
                values = [*obj.matrix_world.translation, *obj.dimensions]
                if not all(math.isfinite(v) for v in values) or any(v > 100 for v in obj.dimensions):
                    problems.append(f"invalid geometry: {name} at frame {frame}")
                if obj.hide_render or obj.hide_get() or max(obj.dimensions) <= 1e-6:
                    problems.append(f"part disappears: {name} at frame {frame}")
            if frame in sample_frames():
                observations[str(frame)] = {name: {"position": list(bpy.data.objects[name].matrix_world.translation),
                                                   "dimensions": list(bpy.data.objects[name].dimensions)}
                                           for name in contract["parts"]}
    fit_spec = contract.get("fit_checks")
    fit_report = None
    if fit_spec and not problems:
        # Cargo-fit scenes: trusted geometry checks from the fit brief (fit_checks.py
        # is copied beside this runner). Failures go back to the author as problems.
        import sys
        sys.path.insert(0, str(ROOT))
        import fit_checks
        measured = fit_checks.measure(bpy, fit_spec, contract["last_frame"])
        if measured.get("missing"):
            problems.extend(f"fit: missing required object {n}" for n in measured["missing"])
        else:
            problems.extend(fit_checks.compare(fit_spec, measured))
        fit_report = measured
    report = {"problems": sorted(set(problems)), "observations": observations, "previews": [],
              "fit": fit_report}
    if not problems:
        normalize(scene, 1280, 720, 24)
        scene.frame_set(1)
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "scene.blend"))
        normalize(scene, 640, 360, 8)
        for frame in sample_frames():
            scene.frame_set(frame)
            filename = f"preview-{frame:04d}.png"
            scene.render.filepath = str(ROOT / filename)
            bpy.ops.render.render(write_still=True)
            report["previews"].append({"seconds": (frame - 1) / 24, "path": filename})
    (ROOT / "checks.json").write_text(json.dumps(report, indent=2))
else:
    # Explicit, per-job owner preview hold; ordinary jobs remain automatic.
    # This is also a backstop for workers already running when a hold is requested.
    hold = ROOT / "preview-approval-required"
    if hold.exists():
        import time
        print("SHOWME_PREVIEW_APPROVAL_REQUIRED", flush=True)
        (ROOT / "awaiting-preview-approval").write_text("Final frames have not started.")
        while not (ROOT / "preview-approved").exists():
            time.sleep(1)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scene.blend"), use_scripts=False)
    scene = bpy.context.scene
    normalize(scene, 1280, 720, 24)
    frames = ROOT / "frames"
    frames.mkdir(exist_ok=True)
    for frame in range(1, contract["last_frame"] + 1):
        scene.frame_set(frame)
        scene.render.filepath = str(frames / f"frame-{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"SHOWME_PROGRESS {frame}/{contract['last_frame']}", flush=True)
