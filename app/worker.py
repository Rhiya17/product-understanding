"""The single render worker: python -m app.worker

Claims queued render jobs from the SQLite store, renders frames in Blender
from the saved scene, encodes an MP4 + poster with ffmpeg, checks the result,
then publishes the asset and resolves waiting requests in one transaction.
Only one worker may run per data directory (file lock).
"""
import fcntl
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.pipeline import scenes  # noqa: E402
from app.pipeline.store import Store, file_sha256  # noqa: E402

RENDER_SCRIPT = REPO_ROOT / "app" / "render" / "blender_render.py"
RENDER_TIMEOUT_SECONDS = 60 * 60
POLL_SECONDS = 2


def pipeline_code_version():
    """Detect deployed code changes before accepting another queued job."""
    import hashlib
    paths = [Path(__file__), *sorted((REPO_ROOT / "app" / "pipeline").glob("*.py")),
             *sorted((REPO_ROOT / "app" / "render").glob("*.py"))]
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


class RenderError(Exception):
    def __init__(self, message, transient=False):
        super().__init__(message)
        self.transient = transient


def blender_executable():
    candidates = [os.environ.get("SHOWME_BLENDER"), shutil.which("blender"),
                  "/Applications/Blender.app/Contents/MacOS/Blender"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def run_blender(job, scene, view, frames_dir, on_progress):
    blender = blender_executable()
    if not blender:
        raise RenderError("Blender is not installed (set SHOWME_BLENDER)")
    first, last = scene["frames"]
    width, height = scene["size"]
    command = [blender, "--background", "--factory-startup", "--python", str(RENDER_SCRIPT),
               "--", "--blend", str(REPO_ROOT / scene["blend"]), "--camera", view["camera"],
               "--frames", f"{first}:{last}", "--out", str(frames_dir),
               "--width", str(width), "--height", str(height),
               "--samples", str(view["samples"]), "--shift-x", str(view["shift_x"])]
    log_path = frames_dir.parent / "blender.log"
    deadline = time.time() + RENDER_TIMEOUT_SECONDS
    with open(log_path, "w") as log:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, start_new_session=True)
        try:
            for line in process.stdout:
                log.write(line)
                if line.startswith("SHOWME_PROGRESS"):
                    done, total = line.split()[1].split("/")
                    on_progress(int(done) / int(total))
                if time.time() > deadline:
                    raise RenderError("render timed out")
            process.wait(timeout=60)
        except BaseException:
            os.killpg(process.pid, signal.SIGTERM)
            raise
    if process.returncode != 0:
        raise RenderError(f"Blender exited with {process.returncode}; see {log_path}",
                          transient=True)
    expected = last - first + 1
    written = len(list(frames_dir.glob("frame-*.png")))
    if written != expected:
        raise RenderError(f"expected {expected} frames, found {written}")


def encode(frames_dir, scene, out_dir):
    first, last = scene["frames"]
    video = out_dir / "video.mp4"
    poster = out_dir / "poster.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(scene["fps"]),
                    "-start_number", str(first), "-i", str(frames_dir / "frame-%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-movflags", "+faststart", str(video)], check=True, timeout=600)
    middle = frames_dir / f"frame-{(first + last) // 2:04d}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(middle),
                    "-q:v", "3", str(poster)], check=True, timeout=120)
    return video, poster


def check_video(video, scene):
    """The clip must decode with the expected frame count, size and duration."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames,width,height", "-show_entries",
         "format=duration", "-of", "json", str(video)],
        capture_output=True, text=True, timeout=300, check=True)
    info = json.loads(probe.stdout)
    stream = info["streams"][0]
    first, last = scene["frames"]
    expected_frames = last - first + 1
    problems = []
    if int(stream["nb_read_frames"]) != expected_frames:
        problems.append(f"frames {stream['nb_read_frames']} != {expected_frames}")
    if [stream["width"], stream["height"]] != list(scene["size"]):
        problems.append(f"size {stream['width']}x{stream['height']}")
    duration = float(info["format"]["duration"])
    if abs(duration - expected_frames / scene["fps"]) > 0.2:
        problems.append(f"duration {duration:.2f}s")
    if problems:
        raise RenderError("video check failed: " + "; ".join(problems))
    return duration


def procedure_steps(product_dir, procedure_id):
    """Verified steps (text + claim id) and product name, from the answer engine."""
    from system.answer_engine import AnswerEngine
    engine = AnswerEngine(REPO_ROOT / "evidence-packs", REPO_ROOT / "source-vault")
    product = engine.products().get(product_dir)
    procedure = product.procedures.get(procedure_id) if product else None
    if procedure is None:
        raise RenderError("procedure no longer exists")
    if not all(product.eligible(step["claim_id"]) for step in procedure["steps"]):
        raise RenderError("procedure is no longer fully verified")
    # Manual pages cited for each part. Only the page image (the hash-checked source
    # itself) is passed on, never an unverified claim's text, so eligibility is not needed.
    part_pages = {}
    for claim in product.claims.values():
        obj = claim.get("object") or {}
        if obj.get("part"):
            pages = [(b.get("source_id"), b.get("page")) for b in claim.get("source_bindings", [])]
            if (obj.get("diagram_binding") or {}).get("page"):
                pages.append((obj["diagram_binding"]["source_id"], obj["diagram_binding"]["page"]))
            part_pages.setdefault(obj["part"], []).extend(p for p in pages if p[0] and p[1])
    steps = []
    for step in procedure["steps"]:
        obj = step.get("object") or {}
        parts = obj.get("target_parts") or []
        pages = [(b.get("source_id"), b.get("page")) for b in step.get("source_bindings", [])
                 if b.get("page")]
        for part in parts:
            pages += part_pages.get(part, [])
        steps.append({"claim_id": step["claim_id"], "text": obj.get("action", ""),
                      "parts": parts,
                      "quote": next((b.get("quote") for b in step.get("source_bindings", [])
                                     if b.get("quote")), ""),
                      "manual_pages": sorted(set(pages), key=lambda p: (p[0], p[1]))})
    return steps, product.name


def process_generation(store, job, generate=None):
    from app.pipeline import generative
    generate = generate or generative.generate
    out_dir = store.root / "assets" / job["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        steps, product_name = procedure_steps(job["product_dir"], job["procedure_id"])
        store.update_job_stage(job["id"], "rendering", 0.1)
        chain, previous = [], job.get("resume_from")
        while previous and previous not in chain and len(chain) < 10:
            chain.append(previous)
            previous = (store.job(previous) or {}).get("resume_from")
        video, poster, chapters, provenance = generate(
            store, job, out_dir, REPO_ROOT / "evidence-packs", steps, product_name,
            question=store.question_for_job(job["id"]),
            resume_dir=[store.root / "assets" / j for j in reversed(chain)],
            progress=lambda stage, fraction: store.update_job_stage(job["id"], stage, fraction))
        store.update_job_stage(job["id"], "checking")
        duration = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
             "default=nw=1:nk=1", str(video)], capture_output=True, text=True,
            timeout=120, check=True).stdout.strip())
    except Exception as exc:  # noqa: BLE001 - every failure ends the paid job; no auto-retry
        return store.fail_job(job["id"], f"{type(exc).__name__}: {exc}"[:500], retry=False)
    (out_dir / "provenance.json").write_text(json.dumps(provenance, indent=1, default=str))
    store.complete_job(job["id"], {
        "product_dir": job["product_dir"], "procedure_id": job["procedure_id"],
        "view": job["view"], "scene_version": job["scene_version"],
        "path": str(video), "poster": str(poster) if Path(poster).is_file() else None,
        "sha256": file_sha256(video), "audience": "research",
        "label": f"{product_name} · AI-generated (FAL Seedance, 720p)",
        "caveat": ("AI-generated from official photos and the manual's steps; planned and "
                   "reviewed by Claude against your question, not yet human-reviewed."
                   + (" Not shown in the video: " + "; ".join(provenance["not_shown"]) + "."
                      if provenance.get("not_shown") else "")),
        "chapters": chapters, "duration": duration})
    return "succeeded"


def process_job(store, job, renderer=run_blender):
    if job.get("kind") == "author":
        return process_authoring(store, job)
    if job.get("kind") == "generate":
        return process_generation(store, job)
    scene = scenes.scene_for(job["product_dir"], job["procedure_id"])
    if not scene or job["view"] not in scene["views"] \
            or scene["scene_version"] != job["scene_version"]:
        store.fail_job(job["id"], "scene or view is no longer available", retry=False)
        return "failed"
    view = scene["views"][job["view"]]
    work = store.root / "work" / job["id"] / f"attempt-{job['attempts']}"
    frames_dir = work / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    try:
        store.update_job_stage(job["id"], "rendering", 0.0)
        renderer(job, scene, view, frames_dir,
                 lambda fraction: store.update_job_stage(job["id"], "rendering",
                                                         round(fraction, 3)))
        store.update_job_stage(job["id"], "encoding")
        out_dir = store.root / "assets" / job["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        video, poster = encode(frames_dir, scene, out_dir)
        store.update_job_stage(job["id"], "checking")
        duration = check_video(video, scene)
    except RenderError as exc:
        return store.fail_job(job["id"], str(exc), retry=exc.transient)
    except (subprocess.SubprocessError, OSError, ValueError, KeyError) as exc:
        return store.fail_job(job["id"], f"{type(exc).__name__}: {exc}", retry=True)
    store.complete_job(job["id"], {
        "product_dir": job["product_dir"], "procedure_id": job["procedure_id"],
        "view": job["view"], "scene_version": scene["scene_version"],
        "path": str(video), "poster": str(poster), "sha256": file_sha256(video),
        "audience": scene["audience"], "label": scene["label"], "caveat": scene["caveat"],
        "chapters": scene["chapters"], "duration": duration})
    shutil.rmtree(frames_dir, ignore_errors=True)
    return "succeeded"


def process_authoring(store, job, generate=None):
    from app.pipeline import authoring
    generate = generate or authoring.generate
    try:
        steps, product_name = procedure_steps(job["product_dir"], job["procedure_id"])
        asset = generate(store, job, steps, product_name,
                         progress=lambda stage, fraction: store.update_job_stage(
                             job["id"], stage, fraction))
        store.complete_job(job["id"], asset)
        return "succeeded"
    except Exception as exc:  # A paid job is never automatically replayed.
        message = str(exc) if isinstance(exc, authoring.AuthoringError) else (
            "Video creation stopped. The written instructions are still available.")
        import openai
        if isinstance(exc, openai.APIStatusError) and getattr(exc, "code", None) in (
                "credit_balance_exhausted", "insufficient_quota"):
            message = ("Video creation is unavailable because the OpenAI API account has "
                       "no available credits or quota. Add API credits or resolve the account's "
                       "billing limit, then retry. The written instructions are still available.")
        return store.fail_job(job["id"], f"{type(exc).__name__}: {exc}"[:500],
                              retry=False, message=message)


def acquire_lock(store):
    handle = open(store.root / "worker.lock", "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    handle.write(str(os.getpid()))
    handle.flush()
    return handle


def main():
    loaded_code = pipeline_code_version()
    from app.pipeline.config import load_local_settings
    load_local_settings()
    store = Store()
    lock = acquire_lock(store)
    if lock is None:
        print("Another ShowMe worker is already running for", store.root)
        return 0
    store.import_scene_assets()
    from app.pipeline import generative
    generative.load_provider_key()
    recovered = store.recover_jobs()
    print(f"ShowMe worker ready ({store.root}); Blender: {blender_executable() or 'MISSING'}; "
          f"recovered {recovered} interrupted job(s)", flush=True)
    stop = {"now": False}
    signal.signal(signal.SIGTERM, lambda *_: stop.update(now=True))
    while not stop["now"]:
        if pipeline_code_version() != loaded_code:
            # Finish any current job first, then replace this process. The lock is
            # non-inheritable, so the fresh worker can acquire it after exec.
            print("Video pipeline changed; reloading worker before the next job", flush=True)
            os.execv(sys.executable, [sys.executable, "-m", "app.worker"])
        job = store.claim_job()
        if job is None:
            time.sleep(POLL_SECONDS)
            continue
        print(f"rendering {job['id']} {job['product_dir']}/{job['procedure_id']}/{job['view']}",
              flush=True)
        result = process_job(store, job)
        print(f"{job['id']}: {result}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
