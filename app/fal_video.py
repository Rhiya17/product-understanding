"""fal.ai-backed procedure video generation.

Produces a real generated video for a procedure. When the procedure's claims
have a bound evidence image, that image seeds an image-to-video model so the
clip shows the actual product; otherwise a text-to-video model is used. The
prompt forbids on-screen text so the result is a demonstration, not slides.

Returns provenance metadata (model, request id, prompt) that the job manager
registers alongside the asset for owner review.
"""

import os
import urllib.request
from pathlib import Path

DEFAULT_IMAGE_MODEL = "alibaba/wan-3.0/image-to-video"
DEFAULT_TEXT_MODEL = "alibaba/wan-3.0/text-to-video"
MAX_PROMPT_STEPS = 6


def build_prompt(product_label, procedure, steps):
    readable = str(procedure or "").replace("_", " ").strip()
    actions = " Then ".join(
        str(step.get("action") or "").strip().rstrip(".") + "."
        for step in steps[:MAX_PROMPT_STEPS] if step.get("action"))
    return (
        f"Realistic product demonstration video of {product_label}: "
        f"{readable}. A person's hands demonstrate each step in order: "
        f"{actions} Clean neutral studio setting, close-up on the product, "
        "smooth camera motion, photorealistic. Strictly no on-screen text, "
        "no captions, no subtitles, no title cards.")


def _download(url, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as response, \
            output.open("wb") as handle:
        for chunk in iter(lambda: response.read(1024 * 1024), b""):
            handle.write(chunk)
    if not output.is_file() or output.stat().st_size < 50_000:
        raise RuntimeError("Downloaded fal.ai video is missing or too small")


def _write_poster(video_path, poster_path):
    import cv2
    capture = cv2.VideoCapture(str(video_path))
    try:
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError("Could not read a poster frame from the video")
        Path(poster_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(poster_path), frame):
            raise RuntimeError("Could not write the poster frame")
    finally:
        capture.release()


def generate(product_label, procedure, steps, output, poster,
             reference_image=None, product_dir=None):
    # fal-client reads FAL_KEY; accept the FAL_API_KEY spelling too.
    if not os.environ.get("FAL_KEY") and os.environ.get("FAL_API_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]
    import fal_client

    prompt = build_prompt(product_label, procedure, steps)
    arguments = {
        "prompt": prompt,
        "duration": int(os.environ.get(
            "SHOWME_VIDEO_DURATION_SECONDS", "5")),
        "resolution": os.environ.get("SHOWME_VIDEO_RESOLUTION", "720p"),
        "aspect_ratio": "16:9",
        "audio": False,
        "enable_safety_checker": True,
    }
    if reference_image is not None:
        model = os.environ.get("SHOWME_VIDEO_MODEL", DEFAULT_IMAGE_MODEL)
        arguments["start_image_url"] = fal_client.upload_file(
            str(reference_image))
    else:
        model = os.environ.get("SHOWME_VIDEO_TEXT_MODEL", DEFAULT_TEXT_MODEL)
    handle = fal_client.submit(model, arguments=arguments)
    result = handle.get()
    video_url = ((result or {}).get("video") or {}).get("url")
    if not video_url:
        raise RuntimeError("fal.ai response did not contain a video URL")
    _download(video_url, output)
    _write_poster(output, poster)
    return {
        "provider": f"fal.ai / {model}",
        "request_id": getattr(handle, "request_id", None),
        "generation_prompt": prompt,
        "reference_image": (str(reference_image)
                            if reference_image is not None else None),
        "license_status": "AI_GENERATED_PENDING_REVIEW",
        "rights_note": (
            f"AI-generated illustrative video (fal.ai {model}), prompted "
            "from the documented steps"
            + (" and seeded with the bound evidence image"
               if reference_image is not None else "")
            + ". Pending owner review — do not publish externally."),
        "external_spend_usd": None,
        "generator": "app/fal_video.py",
    }
