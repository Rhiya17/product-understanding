"""Read-only playback check for the five agreed ShowMe website questions.

Does not request generation, retry jobs, or call model providers directly.
The exact question strings also serve as a repeatable browser acceptance checklist.
"""
import argparse
import json
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

CASES = [
    ("fold", "How do I fold the Ready2Jet stroller?"),
    ("trunk_fit", "Will the Ready2Jet stroller fit in my Tesla Model Y trunk?"),
    ("brakes", "How do I operate the Ready2Jet stroller brakes?"),
    ("headphones", "How do I connect QuietComfort headphones to my Mac?"),
    ("filter", "How do I replace the filter in my Levoit Core 300S?"),
]


def check(base_url, case, question):
    url = base_url.rstrip("/") + "/api/answer?" + urlencode({"q": question, "preview": "0"})
    with urlopen(url, timeout=30) as response:
        payload = json.load(response)
    document = payload.get("answer_document") or {}
    video = document.get("video") or {}
    result = {"case": case, "question": question, "answer_status": document.get("status"),
              "headline": document.get("headline"), "video_state": video.get("state"),
              "procedure": (document.get("coverage") or {}).get("procedure_id"),
              "assets": [], "playable": False}
    for asset in video.get("assets", []):
        media_url = urljoin(base_url, asset["url"])
        if urlparse(media_url).netloc != urlparse(base_url).netloc:
            raise ValueError("Refusing a playback check outside the supplied app origin")
        with urlopen(Request(media_url, headers={"Range": "bytes=0-1023"}), timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            prefix = response.read(1024)
            valid = response.status == 206 and content_type.startswith("video/mp4") and bool(prefix)
            result["assets"].append({"id": asset.get("id"), "url": media_url,
                                     "http_status": response.status, "content_type": content_type,
                                     "range_playback_ok": valid})
    result["playable"] = any(asset["range_playback_ok"] for asset in result["assets"])
    if not result["playable"]:
        result["detail"] = (document.get("gap") or {}).get("message") or document.get("direct_answer")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8766")
    parser.add_argument("--require-all", action="store_true", help="Exit nonzero if any video is missing")
    args = parser.parse_args()
    results = []
    for case, question in CASES:
        try:
            results.append(check(args.base_url, case, question))
        except Exception as error:
            results.append({"case": case, "question": question, "playable": False,
                            "error": f"{type(error).__name__}: {error}"})
    complete = all(result["playable"] for result in results)
    print(json.dumps({"all_five_playable": complete, "cases": results}, indent=2))
    return 1 if args.require_all and not complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
