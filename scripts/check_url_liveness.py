#!/usr/bin/env python3
"""Weekly watchdog: do the vault's recorded URLs still resolve?

Checks every origin_url in every manifest plus every http(s) URL found in
videos/video-sources.md files. Dead or moved URLs are the link-rot failure
mode of URL-only sources (embedded videos especially) — a failure here
should trigger the LLD §3.4 correction/invalidation flow for the affected
source, not a code fix.

Advisory: exits 1 if anything is dead so the scheduled run shows red.
"""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
VAULT = ROOT / "source-vault"
TIMEOUT = 20
# Some CDNs reject HEAD or unknown agents; these statuses still mean "alive".
ALIVE_EXTRA = {403, 405, 429}
UA = {"User-Agent": "Mozilla/5.0 (compatible; showme-freshness-check)"}


def alive(url: str) -> bool:
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=UA)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status < 400:
                    return True
        except urllib.error.HTTPError as e:
            if e.code in ALIVE_EXTRA:
                return True
        except Exception:  # noqa: BLE001
            if method == "GET":
                return False
    return False


def collect_urls():
    urls = {}
    for mp in VAULT.glob("*/manifest.json"):
        m = json.loads(mp.read_text())
        for s in m.get("sources", []):
            u = s.get("origin_url")
            if u:
                urls.setdefault(u, mp.parent.name)
    for vs in VAULT.glob("*/videos/video-sources.md"):
        for u in re.findall(r"https?://[^\s)\">\]]+", vs.read_text()):
            urls.setdefault(u, vs.parent.parent.name)
    return urls


def main() -> int:
    urls = collect_urls()
    dead = []
    for url, product in sorted(urls.items()):
        ok = alive(url)
        print(f"{'ok  ' if ok else 'DEAD'} [{product}] {url}")
        if not ok:
            dead.append((product, url))
    print(f"\n{len(urls)} URLs checked, {len(dead)} dead")
    if dead:
        print("Dead URLs mean a recorded source moved or was removed — "
              "route through the source-correction flow (LLD §3.4).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
