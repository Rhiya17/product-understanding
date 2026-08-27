#!/usr/bin/env python3
"""Local HTTP server for published product answers."""

import argparse
import hashlib
import json
import mimetypes
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = APP_ROOT / "static"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from system import answer  # noqa: E402


_HASH_CACHE = {}
_HASH_CACHE_LOCK = threading.Lock()


def _catalog_products(vault_root):
    """Return the public subset of product catalog fields."""
    return [{
        "id": product.get("product_id"),
        "dir": product.get("dir"),
        "brand": product.get("brand"),
        "model": product.get("model"),
        "category": product.get("category"),
    } for product in answer.load_catalog(vault_root)]


def _verified_hash(path, expected_hash):
    """Verify a file against its manifest hash, caching unchanged files."""
    path = Path(path)
    stat = path.stat()
    cache_key = (str(path.resolve()), expected_hash)
    fingerprint = (stat.st_mtime_ns, stat.st_size)
    with _HASH_CACHE_LOCK:
        cached = _HASH_CACHE.get(cache_key)
    if cached and cached[:2] == fingerprint:
        return cached[2]

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    matches = digest.hexdigest() == expected_hash
    with _HASH_CACHE_LOCK:
        _HASH_CACHE[cache_key] = (*fingerprint, matches)
    return matches


def _media_url(product_dir, local_path):
    product = quote(product_dir, safe="")
    relative = quote(Path(local_path).as_posix(), safe="/")
    return f"/media/{product}/{relative}"


def _media_index(packs_root, vault_root, preview):
    """Index approved (or explicitly previewed) bindings by claim id."""
    index = {}
    for product in answer.load_catalog(vault_root):
        product_dir = product.get("dir")
        manifest = answer.load_json(
            vault_root / product_dir / "manifest.json", {})
        sources = {source.get("source_id"): source
                   for source in manifest.get("sources", [])}
        media_doc = answer.load_json(
            packs_root / product_dir / "media-bindings.json", {})
        for binding in media_doc.get("bindings", []):
            approved = bool(binding.get("approved_by"))
            if not approved and not preview:
                continue
            source = sources.get(binding.get("source_id"), {})
            kind = binding.get("kind")
            if kind == "VIDEO_URL":
                media_url = source.get("origin_url")
            else:
                local_path = source.get("local_path")
                media_url = (_media_url(product_dir, local_path)
                             if local_path else None)
            media = {
                "id": binding.get("binding_id"),
                "kind": kind,
                "url": media_url,
                "page": binding.get("page"),
                "start_seconds": binding.get("start_seconds"),
                "end_seconds": binding.get("end_seconds"),
                "rationale": binding.get("rationale"),
                "awaiting_approval": not approved,
                "rights_note": (source.get("rights_note")
                                if kind == "VIDEO_FILE" else None),
            }
            for claim_id in binding.get("claim_ids", []):
                index.setdefault(claim_id, []).append(media)
    return index


def make_handler(packs_root, vault_root):
    """Build a request handler bound to explicit content roots."""
    packs_root = Path(packs_root).resolve()
    vault_root = Path(vault_root).resolve()

    class AnswerHandler(BaseHTTPRequestHandler):
        server_version = "ShowMeAnswer/0"

        def _send_json(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _send_file(self, path, cache_control="no-cache"):
            file_size = path.stat().st_size
            content_type = mimetypes.guess_type(path.name)[0]
            if path.suffix == ".js":
                content_type = "text/javascript"
            content_type = content_type or "application/octet-stream"
            if content_type.startswith("text/"):
                content_type = f"{content_type}; charset=utf-8"

            start, end, status = 0, file_size - 1, 200
            range_header = self.headers.get("Range")
            if range_header and range_header.startswith("bytes="):
                try:
                    start_text, end_text = range_header[6:].split("-", 1)
                    start = int(start_text) if start_text else 0
                    end = int(end_text) if end_text else file_size - 1
                    if start < 0 or end < start or end >= file_size:
                        raise ValueError
                    status = 206
                except ValueError:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{file_size}")
                    self.end_headers()
                    return

            length = end - start + 1
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Accept-Ranges", "bytes")
            if status == 206:
                self.send_header("Content-Range",
                                 f"bytes {start}-{end}/{file_size}")
            self.send_header("Cache-Control", cache_control)
            self.end_headers()
            with path.open("rb") as handle:
                handle.seek(start)
                remaining = length
                try:
                    while remaining:
                        chunk = handle.read(min(1024 * 1024, remaining))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    # Browsers routinely cancel speculative media ranges.
                    return

        def _serve_static(self, request_path):
            relative = "index.html" if request_path == "/" else unquote(
                request_path.removeprefix("/static/"))
            candidate = (STATIC_ROOT / relative).resolve()
            if STATIC_ROOT not in candidate.parents or not candidate.is_file():
                self._send_json(404, {"error": "Not found"})
                return
            self._send_file(candidate)

        def _serve_products(self):
            self._send_json(200, {"products": _catalog_products(vault_root)})

        def _serve_media(self, request_path):
            relative = unquote(request_path.removeprefix("/media/"))
            parts = Path(relative).parts
            if (len(parts) < 2 or any(part in {"", ".", ".."}
                                      for part in parts)):
                self._send_json(404, {"error": "Media not found"})
                return
            product_dir = parts[0]
            local_path = Path(*parts[1:]).as_posix()
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir not in known_products:
                self._send_json(404, {"error": "Media not found"})
                return

            product_root = (vault_root / product_dir).resolve()
            candidate = (product_root / local_path).resolve()
            if product_root not in candidate.parents or not candidate.is_file():
                self._send_json(404, {"error": "Media not found"})
                return

            manifest = answer.load_json(product_root / "manifest.json", {})
            source = next((item for item in manifest.get("sources", [])
                           if item.get("local_path") == local_path), None)
            if source is None:
                self._send_json(404, {"error": "Media not found"})
                return
            if source.get("type") == "VIDEO":
                secure = (
                    source.get("authority") == "MANUFACTURER"
                    and bool(source.get("rights_note"))
                    and isinstance(source.get("sha256"), str)
                    and _verified_hash(candidate, source["sha256"])
                )
                if not secure:
                    self._send_json(500, {"error": "Media integrity check failed"})
                    return
            self._send_file(candidate, cache_control="no-store")

        def _serve_answer(self, query):
            question = query.get("q", [""])[0].strip()
            if not question:
                self._send_json(400, {"error": "Question must not be empty"})
                return

            preview_value = query.get("preview", ["0"])[0]
            if preview_value not in {"0", "1"}:
                self._send_json(400, {"error": "preview must be 0 or 1"})
                return

            product_dir = query.get("product", [""])[0].strip() or None
            known_products = {item["dir"] for item in _catalog_products(vault_root)}
            if product_dir and product_dir not in known_products:
                self._send_json(404, {"error": "Unknown product"})
                return

            try:
                top = int(query.get("top", ["3"])[0])
            except ValueError:
                self._send_json(400, {"error": "top must be an integer"})
                return
            if top < 1 or top > 100:
                self._send_json(400, {"error": "top must be between 1 and 100"})
                return

            results, not_served = answer.search(
                question,
                packs_root=packs_root,
                vault_root=vault_root,
                product_dir=product_dir,
                preview=preview_value == "1",
                top=top,
            )
            media_by_claim = _media_index(
                packs_root, vault_root, preview_value == "1")
            for result in results:
                result["media"] = media_by_claim.get(result["claim_id"], [])
            self._send_json(200, {
                "question": question,
                "results": results,
                "not_served": not_served,
            })

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            try:
                if parsed.path == "/api/answer":
                    self._serve_answer(parse_qs(parsed.query, keep_blank_values=True))
                elif parsed.path == "/api/products":
                    self._serve_products()
                elif parsed.path.startswith("/media/"):
                    self._serve_media(parsed.path)
                elif parsed.path == "/" or parsed.path.startswith("/static/"):
                    self._serve_static(parsed.path)
                else:
                    self._send_json(404, {"error": "Not found"})
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception:  # Keep internal details out of the HTTP response.
                self._send_json(500, {"error": "Internal server error"})

        def log_message(self, format_string, *args):
            sys.stderr.write(
                f"{self.address_string()} - {format_string % args}\n")

    return AnswerHandler


def create_server(port=8765, packs_root=None, vault_root=None):
    """Create the app server. Passing port 0 lets the OS choose a test port."""
    handler = make_handler(
        packs_root or REPO_ROOT / "evidence-packs",
        vault_root or REPO_ROOT / "source-vault",
    )
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Serve the local answer app")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--packs-root", type=Path,
                        default=REPO_ROOT / "evidence-packs")
    parser.add_argument("--vault-root", type=Path,
                        default=REPO_ROOT / "source-vault")
    args = parser.parse_args(argv)

    server = create_server(args.port, args.packs_root, args.vault_root)
    print(f"Answer app listening on http://localhost:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
