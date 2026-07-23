"""Run one controlled Ready2Jet one-hand-fold Higgsfield POC attempt.

The request uses a public crop of Graco's official fold-sequence image as the
source frame. Credentials are read from environment variables and are never
written to disk. Each attempt has a unique output directory so prior evidence
cannot be overwritten.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import time

import requests


BASE_URL = "https://platform.higgsfield.ai"
ENDPOINT_PATH = "/v1/image2video/dop"
DEFAULT_MODEL = "dop-preview"
DEFAULT_MOTION_ID = "31177282-bde3-4870-b283-1135ca0a201a"
DEFAULT_IMAGE_URL = (
    "https://newellbrands.imgix.net/"
    "13f546fb-a043-300c-82ce-43db1392fe58/"
    "13f546fb-a043-300c-82ce-43db1392fe58.jpg"
    "?auto=format,compress&rect=0,350,1120,1900&w=720"
)
POLL_SECONDS = 10
TIMEOUT_SECONDS = 900


def auth_headers() -> dict[str, str]:
    key = os.environ.get("HIGGSFIELD_API_KEY")
    secret = os.environ.get("HIGGSFIELD_API_SECRET")
    if not key or not secret:
        raise SystemExit(
            "Set HIGGSFIELD_API_KEY and HIGGSFIELD_API_SECRET before submitting."
        )
    return {
        "Content-Type": "application/json",
        "Authorization": f"Key {key}:{secret}",
    }


def find_video_url(result: dict) -> str | None:
    video = result.get("video")
    if isinstance(video, dict) and isinstance(video.get("url"), str):
        return video["url"]
    for field in ("video_url", "url", "output_url"):
        value = result.get(field)
        if isinstance(value, str) and value.startswith("http"):
            return value
    return None


def validate_effective_params(
    submitted: dict,
    expected_params: dict,
) -> list[str]:
    """Return differences between requested and server-effective controls."""
    effective = submitted.get("input_params")
    if not isinstance(effective, dict):
        return ["Initial response did not include input_params for auditing."]

    mismatches: list[str] = []
    for field in (
        "model",
        "prompt",
        "input_images",
        "seed",
        "enhance_prompt",
        "motions",
    ):
        expected = expected_params.get(field)
        actual = effective.get(field)
        if actual != expected:
            mismatches.append(
                f"{field}: requested {expected!r}, server applied {actual!r}"
            )
    return mismatches


def cancel_invalid_job(submitted: dict, headers: dict[str, str]) -> dict:
    cancel_url = submitted.get("cancel_url")
    if not isinstance(cancel_url, str) or not cancel_url.startswith("http"):
        return {"attempted": False, "reason": "No cancel URL was returned."}
    try:
        response = requests.post(cancel_url, headers=headers, timeout=60)
        return {
            "attempted": True,
            "status_code": response.status_code,
            "body": response.text[:2000],
        }
    except requests.RequestException as exc:
        return {"attempted": True, "error": str(exc)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-label", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument(
        "--model",
        default=os.environ.get("HIGGSFIELD_MODEL", DEFAULT_MODEL),
    )
    parser.add_argument("--image-url", default=DEFAULT_IMAGE_URL)
    parser.add_argument("--prompt-file", default="prompt-corrected.txt")
    parser.add_argument("--motion-id", default=DEFAULT_MOTION_ID)
    parser.add_argument("--motion-strength", type=float, default=0.0)
    args = parser.parse_args()

    if not 0 <= args.seed <= 1_000_000:
        raise SystemExit("--seed must be between 0 and 1,000,000")
    if not args.run_label.replace("-", "").replace("_", "").isalnum():
        raise SystemExit("--run-label may contain only letters, numbers, - and _")
    if not 0.0 <= args.motion_strength <= 1.0:
        raise SystemExit("--motion-strength must be between 0.0 and 1.0")

    root = Path(__file__).resolve().parent
    prompt = (root / args.prompt_file).read_text(encoding="utf-8").strip()
    output_dir = root / "out" / args.run_label
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"Refusing to overwrite existing run: {output_dir}")

    endpoint = f"{BASE_URL}{ENDPOINT_PATH}"
    params = {
        "model": args.model,
        "prompt": prompt,
        "input_images": [
            {
                "type": "image_url",
                "image_url": args.image_url,
            }
        ],
        "seed": args.seed,
        "enhance_prompt": False,
        # The live API rejects an empty list. Supplying the previously injected
        # motion explicitly at zero strength satisfies the schema while
        # neutralizing its camera movement.
        "motions": [{"id": args.motion_id, "strength": args.motion_strength}],
    }
    request_body = {"params": params}

    if args.dry_run:
        print(json.dumps({"endpoint": endpoint, "body": request_body}, indent=2))
        return

    output_dir.mkdir(parents=True, exist_ok=False)
    headers = auth_headers()

    response = requests.post(
        endpoint,
        headers=headers,
        json=request_body,
        timeout=60,
    )
    if not response.ok:
        (output_dir / "rejection.json").write_text(
            json.dumps(
                {
                    "submitted_at_unix": int(time.time()),
                    "endpoint": endpoint,
                    "body": request_body,
                    "status_code": response.status_code,
                    "response_text": response.text[:4000],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        raise RuntimeError(
            f"Higgsfield rejected the request ({response.status_code}): "
            f"{response.text[:4000]}"
        )
    submitted = response.json()
    request_id = submitted.get("request_id") or submitted.get("id")
    if not request_id:
        raise RuntimeError(f"Higgsfield response did not contain a request ID: {submitted}")

    submission_record = {
        "submitted_at_unix": int(time.time()),
        "endpoint": endpoint,
        "body": request_body,
        "request_id": request_id,
        "initial_response": submitted,
    }
    (output_dir / "submission.json").write_text(
        json.dumps(submission_record, indent=2), encoding="utf-8"
    )
    print(f"Submitted {request_id}")

    mismatches = validate_effective_params(submitted, params)
    validation_record = {
        "valid": not mismatches,
        "mismatches": mismatches,
        "requested": params,
        "effective": submitted.get("input_params"),
    }
    if mismatches:
        validation_record["cancellation"] = cancel_invalid_job(submitted, headers)
    (output_dir / "effective-params-validation.json").write_text(
        json.dumps(validation_record, indent=2), encoding="utf-8"
    )
    if mismatches:
        raise RuntimeError(
            "Server-effective parameters did not match the controlled request: "
            + "; ".join(mismatches)
        )
    print(
        "Effective controls verified: prompt unchanged, enhancement off, "
        f"motion strength {args.motion_strength}"
    )

    status_url = submitted.get("status_url") or (
        f"{BASE_URL}/requests/{request_id}/status"
    )
    deadline = time.time() + TIMEOUT_SECONDS

    while time.time() < deadline:
        status_response = requests.get(
            status_url,
            headers=headers,
            timeout=60,
        )
        status_response.raise_for_status()
        result = status_response.json()
        state = str(result.get("status", "")).lower()
        print(f"Status: {state or 'unknown'}")

        if state in {"completed", "failed", "nsfw", "cancelled", "canceled"}:
            (output_dir / "result.json").write_text(
                json.dumps(result, indent=2), encoding="utf-8"
            )
            if state != "completed":
                raise RuntimeError(f"Generation ended with status {state}")

            video_url = find_video_url(result)
            if not video_url:
                raise RuntimeError("Completed response did not contain a video URL")
            video_response = requests.get(video_url, timeout=180)
            video_response.raise_for_status()
            (output_dir / "video.mp4").write_bytes(video_response.content)
            print(f"Saved {output_dir / 'video.mp4'}")
            return

        time.sleep(POLL_SECONDS)

    raise TimeoutError(f"Generation did not finish within {TIMEOUT_SECONDS} seconds")


if __name__ == "__main__":
    main()
