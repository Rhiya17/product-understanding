"""Minimal Higgsfield API client (POC).

The public API surface (docs.higgsfield.ai) is image-to-video:
    POST https://platform.higgsfield.ai/<model-path>   {image_url, prompt, ...}
    -> request_id, then poll until COMPLETED/FAILED.

Exact auth header names and model paths come from your Higgsfield dashboard —
adjust MODEL_PATH and headers below to match. Set:
    export HIGGSFIELD_API_KEY=...
    export HIGGSFIELD_API_SECRET=...   # if your account uses key+secret

Note: the API takes an image *URL*, not an upload, so the rendered start frame
must be hosted somewhere reachable (S3 presigned URL, etc.).
"""

import os
import sys
import time

import requests

BASE = "https://platform.higgsfield.ai"
# Valid slugs (from API validation): lite, standard, turbo, and
# {lite,standard,turbo}/first-last-frame
MODEL_PATH = "higgsfield-ai/dop/lite"
POLL_SECONDS = 10
TIMEOUT_SECONDS = 600


def _headers():
    # Discovered by probing platform.higgsfield.ai: it validates an
    # `hf-api-key` header as a UUID (the key ID from the dashboard) and takes
    # the 64-hex secret separately.
    key = os.environ.get("HIGGSFIELD_API_KEY")      # UUID key ID
    secret = os.environ.get("HIGGSFIELD_API_SECRET")  # 64-hex secret
    if not key or not secret:
        raise SystemExit("Set HIGGSFIELD_API_KEY (UUID) and HIGGSFIELD_API_SECRET (64-hex).")
    return {"Content-Type": "application/json", "hf-api-key": key, "hf-secret": secret}


def generate(image_url: str, prompt: str, duration: int = 5) -> dict:
    """Submit a job, poll to completion, return the final job payload."""
    r = requests.post(f"{BASE}/{MODEL_PATH}", headers=_headers(), json={
        "image_url": image_url,
        "prompt": prompt,
        "duration": duration,
    })
    r.raise_for_status()
    job = r.json()
    request_id = job.get("request_id") or job.get("id")
    print(f"submitted: {request_id}")

    deadline = time.time() + TIMEOUT_SECONDS
    while time.time() < deadline:
        s = requests.get(f"{BASE}/requests/{request_id}", headers=_headers())
        s.raise_for_status()
        status = s.json()
        state = status.get("status", "").upper()
        print(f"  status: {state}")
        if state in ("COMPLETED", "FAILED"):
            return status
        time.sleep(POLL_SECONDS)
    raise TimeoutError(f"job {request_id} did not finish in {TIMEOUT_SECONDS}s")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("usage: python higgsfield_client.py <image_url> <prompt>")
    result = generate(sys.argv[1], " ".join(sys.argv[2:]))
    print(result)
