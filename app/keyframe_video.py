"""Grounded keyframe procedure-video pipeline.

Implements docs/workorders/workorder-grounded-video-pipeline.md: a procedure
video is composed from curated evidence keyframes registered in the product's
evidence pack. A generative model (Seedance 2.0 first/last-frame) is only
allowed to interpolate motion between pinned truths; every segment is then
verified by a vision-language model against its own keyframes, and one failing
segment fails the whole job. Procedures without registered keyframes are
refused — no video beats an ungrounded one.
"""

import hashlib
import json
import os
import re
from pathlib import Path

SEEDANCE_ENDPOINTS = {
    "quality": "bytedance/seedance-2.0/image-to-video",
    "fast": "bytedance/seedance-2.0/fast/image-to-video",
}
VLM_ENDPOINT = "fal-ai/any-llm/vision"
DEFAULT_VLM_MODEL = "qwen/qwen3-vl-235b-a22b-instruct"
DEFAULT_SEED = 42001
VERIFICATION_FRAME_COUNT = 8
REGISTRY_FILENAME = "procedure-keyframes.json"

VERIFY_PROMPT = """\
You are a strict verifier for AI-generated product demonstration videos.
Judge only what is visible. Do not give the benefit of the doubt.

Image 1: the verified START keyframe for this video segment (ground truth).
Image 2: the verified END keyframe for this video segment (ground truth).
Images 3-{last}: {count} chronological frames sampled evenly from a candidate
video that must move the exact product of images 1-2 from the start state to
the end state.

Answer in JSON only, with these keys:
{{
  "same_product": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "reaches_end_state": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "invented_or_vanishing_parts": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "camera_and_object_orientation_fixed": {{"answer": "yes|no|unsure", "evidence": "..."}},
  "verdict": "pass|fail",
  "verdict_reason": "..."
}}
"same_product" means every frame keeps the exact product identity of the
keyframes: shape, colors, materials, parts, proportions, logos. Note any
drift. The verdict is "pass" only if the product identity holds, the end
state is reached, and no parts are invented or vanish.
"""


class KeyframesMissingError(RuntimeError):
    """The procedure has no registered keyframes; generation is refused."""


class SegmentVerificationError(RuntimeError):
    """A generated segment failed VLM verification against its keyframes."""


def registry_entry(packs_root, product_dir, procedure):
    """Return the registered keyframe plan for one procedure, or None."""
    path = Path(packs_root) / str(product_dir or "") / REGISTRY_FILENAME
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
        
    pack_claims_path = Path(packs_root) / str(product_dir or "") / "claims.json"
    valid_claim_ids = set()
    try:
        claims_doc = json.loads(pack_claims_path.read_text(encoding="utf-8"))
        for c in claims_doc:
            if isinstance(c, dict) and "claim_id" in c:
                valid_claim_ids.add(c["claim_id"])
    except (OSError, json.JSONDecodeError):
        pass

    for entry in document.get("procedures", []):
        if (isinstance(entry, dict) and entry.get("procedure") == procedure
                and entry.get("segments")):
            states = {s["state_id"]: s for s in entry.get("states", [])}
            is_valid = True
            
            for state_id, state in states.items():
                for claim_id in state.get("claim_ids", []):
                    if claim_id not in valid_claim_ids:
                        is_valid = False
                        break
                        
            for seg in entry["segments"]:
                for ref in ["start_state", "end_state"]:
                    if ref in seg:
                        state_id = seg[ref]
                        if state_id not in states:
                            is_valid = False
            if is_valid:
                return entry
    return None


def parse_verdict(vlm_result):
    """Extract the strict JSON verdict from a VLM response; fail closed."""
    output = vlm_result.get("output") if isinstance(vlm_result, dict) else None
    if not isinstance(output, str):
        return {"verdict": "fail", "verdict_reason": "empty VLM response"}
    text = output.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return {"verdict": "fail", "verdict_reason": "no JSON in VLM response"}
    try:
        verdict = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return {"verdict": "fail", "verdict_reason": "invalid JSON from VLM"}
    if verdict.get("verdict") not in {"pass", "fail"}:
        verdict["verdict"] = "fail"
        verdict.setdefault("verdict_reason", "missing verdict field")
    return verdict


def sample_frames(video_path, out_dir, count=VERIFICATION_FRAME_COUNT):
    """Write `count` evenly spaced frames as PNGs and return their paths."""
    import cv2
    capture = cv2.VideoCapture(str(video_path))
    try:
        total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if total < count:
            raise RuntimeError("Segment video has too few frames to verify")
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for index in range(count):
            position = int(round(index * (total - 1) / (count - 1)))
            capture.set(cv2.CAP_PROP_POS_FRAMES, position)
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError("Could not read a verification frame")
            path = out_dir / f"verify-frame-{index + 1:02d}.png"
            cv2.imwrite(str(path), frame)
            paths.append(path)
        return paths
    finally:
        capture.release()


def stitch_segments(segment_paths, output):
    """Concatenate segment videos into one clip, resizing to the first."""
    import cv2
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = None
    size = None
    try:
        for segment_path in segment_paths:
            capture = cv2.VideoCapture(str(segment_path))
            try:
                if writer is None:
                    fps = capture.get(cv2.CAP_PROP_FPS) or 24
                    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                    writer = cv2.VideoWriter(
                        str(output), cv2.VideoWriter_fourcc(*"avc1"),
                        fps, size)
                    if not writer.isOpened():
                        raise RuntimeError(
                            "OpenCV could not open the stitch writer")
                while True:
                    ok, frame = capture.read()
                    if not ok:
                        break
                    if (frame.shape[1], frame.shape[0]) != size:
                        frame = cv2.resize(frame, size)
                    writer.write(frame)
            finally:
                capture.release()
    finally:
        if writer is not None:
            writer.release()
    if not output.is_file() or output.stat().st_size < 50_000:
        raise RuntimeError("Stitched video is missing or unexpectedly small")


def _write_poster(image_path, poster_path):
    import cv2
    frame = cv2.imread(str(image_path))
    if frame is None:
        raise RuntimeError("Could not read the poster keyframe")
    Path(poster_path).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(poster_path), frame):
        raise RuntimeError("Could not write the poster frame")


def _download(url, path):
    import urllib.request
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as response, \
            path.open("wb") as handle:
        for chunk in iter(lambda: response.read(1024 * 1024), b""):
            handle.write(chunk)
    if not path.is_file() or path.stat().st_size < 50_000:
        raise RuntimeError("Downloaded segment is missing or too small")


def make_generator(packs_root):
    """Bind the pipeline to a packs root; returns a job-manager generator."""
    packs_root = Path(packs_root).resolve()
    repo_root = packs_root.parent

    def resolve(relative):
        candidate = (repo_root / relative).resolve()
        if repo_root not in candidate.parents or not candidate.is_file():
            raise KeyframesMissingError(
                f"Registered keyframe not found: {relative}")
        return candidate

    def generate(product_label, procedure, steps, output, poster,
                 reference_image=None, product_dir=None):
        if not os.environ.get("FAL_KEY") and os.environ.get("FAL_API_KEY"):
            os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]
        import fal_client

        entry = registry_entry(packs_root, product_dir, procedure)
        if entry is None:
            raise KeyframesMissingError(
                f"No registered keyframes for {product_dir}:{procedure}")
        tier = os.environ.get("SHOWME_VIDEO_SEEDANCE_TIER", "quality")
        endpoint = SEEDANCE_ENDPOINTS.get(tier, SEEDANCE_ENDPOINTS["quality"])
        vlm_model = os.environ.get("SHOWME_VIDEO_VLM_MODEL", DEFAULT_VLM_MODEL)
        seed = int(os.environ.get("SHOWME_VIDEO_SEED", DEFAULT_SEED))

        upload_cache = {}

        def upload(path):
            digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            if digest not in upload_cache:
                upload_cache[digest] = fal_client.upload_file(str(path))
            return upload_cache[digest]

        output = Path(output)
        work_dir = output.parent / f".{output.stem}-work"
        segment_paths, provenance_segments, request_ids = [], [], []
        first_start = None
        try:
            states_by_id = {s["state_id"]: s for s in entry.get("states", [])}
            
            def resolve_endpoint(seg_endpoint, is_start=True):
                if is_start and "start_path" in seg_endpoint:
                    return resolve(seg_endpoint["start_path"])
                elif not is_start and "end_path" in seg_endpoint:
                    return resolve(seg_endpoint["end_path"])
                elif is_start and "start_state" in seg_endpoint:
                    from app.keyframe_synthesis import resolve_state
                    return resolve_state(states_by_id[seg_endpoint["start_state"]], procedure, packs_root, product_dir, fal_client, upload_cache)
                elif not is_start and "end_state" in seg_endpoint:
                    from app.keyframe_synthesis import resolve_state
                    return resolve_state(states_by_id[seg_endpoint["end_state"]], procedure, packs_root, product_dir, fal_client, upload_cache)
                raise KeyframesMissingError("Segment missing start/end path or state")

            for segment in entry["segments"]:
                segment_id = segment.get("segment_id") or (
                    f"seg{len(segment_paths) + 1}")
                start = resolve_endpoint(segment, is_start=True)
                end = resolve_endpoint(segment, is_start=False)
                if first_start is None:
                    first_start = start
                arguments = {
                    "prompt": segment["motion_prompt"],
                    "resolution": entry.get("resolution", "720p"),
                    "duration": str(segment.get("duration_seconds", 4)),
                    "aspect_ratio": entry.get("aspect_ratio", "16:9"),
                    "generate_audio": False,
                    "seed": seed,
                    "image_url": upload(start),
                    "end_image_url": upload(end),
                }
                handle = fal_client.submit(endpoint, arguments=arguments)
                request_id = getattr(handle, "request_id", None)
                result = handle.get()
                video_url = ((result or {}).get("video") or {}).get("url")
                if not video_url:
                    raise RuntimeError(
                        f"Segment {segment_id}: no video URL in response")
                segment_path = work_dir / f"{segment_id}.mp4"
                _download(video_url, segment_path)

                frames = sample_frames(
                    segment_path, work_dir / f"{segment_id}-frames")
                prompt = VERIFY_PROMPT.format(
                    count=VERIFICATION_FRAME_COUNT,
                    last=VERIFICATION_FRAME_COUNT + 2)
                verify_handle = fal_client.submit(VLM_ENDPOINT, arguments={
                    "model": vlm_model,
                    "prompt": prompt,
                    "image_urls": [upload(start), upload(end)]
                                  + [upload(frame) for frame in frames],
                    "temperature": 0,
                    "max_tokens": 2000,
                })
                verdict = parse_verdict(verify_handle.get())
                provenance_segments.append({
                    "segment_id": segment_id,
                    "endpoint": endpoint,
                    "request_id": request_id,
                    "seed": seed,
                    "start_path": segment.get("start_path"),
                    "end_path": segment.get("end_path"),
                    "start_state": segment.get("start_state"),
                    "end_state": segment.get("end_state"),
                    "verification_model": vlm_model,
                    "verdict": verdict,
                })
                request_ids.append(request_id)
                if verdict.get("verdict") != "pass":
                    raise SegmentVerificationError(
                        f"Segment {segment_id} failed verification: "
                        f"{verdict.get('verdict_reason')}")
                segment_paths.append(segment_path)

            stitch_segments(segment_paths, output)
            _write_poster(first_start, poster)
        finally:
            verification_path = output.with_name(
                f"{output.stem}-verification.json")
            if provenance_segments:
                verification_path.parent.mkdir(parents=True, exist_ok=True)
                verification_path.write_text(json.dumps({
                    "procedure": procedure,
                    "product_dir": product_dir,
                    "pipeline": "keyframe-pinned segments, per-segment VLM "
                                "verification, stitched on all-pass",
                    "segments": provenance_segments,
                }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            import shutil
            shutil.rmtree(work_dir, ignore_errors=True)

        return {
            "provider": (f"fal.ai / {endpoint} (keyframe-pinned) + "
                         f"{vlm_model} verification"),
            "generator": "app/keyframe_video.py",
            "request_id": ", ".join(str(r) for r in request_ids if r) or None,
            "license_status": "GROUNDED_GENERATED_PENDING_REVIEW",
            "rights_note": (
                "Generated by interpolating between registered evidence "
                "keyframes only; every segment VLM-verified against its "
                "keyframes. Pending owner review — do not publish "
                "externally."),
            "verification_local_path": str(
                verification_path.relative_to(repo_root)
                if repo_root in verification_path.parents
                else verification_path),
            "keyframe_provenance": entry.get("keyframe_provenance"),
            "external_spend_usd": None,
        }

    return generate
