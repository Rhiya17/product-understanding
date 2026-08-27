#!/usr/bin/env python3
"""Local HTTP server for published product answers."""

import argparse
import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = APP_ROOT / "static"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from system import answer  # noqa: E402


def _catalog_products(vault_root):
    """Return the public subset of product catalog fields."""
    return [{
        "id": product.get("product_id"),
        "dir": product.get("dir"),
        "brand": product.get("brand"),
        "model": product.get("model"),
        "category": product.get("category"),
    } for product in answer.load_catalog(vault_root)]


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

        def _send_file(self, path):
            body = path.read_bytes()
            content_type = mimetypes.guess_type(path.name)[0]
            if path.suffix == ".js":
                content_type = "text/javascript"
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type or 'application/octet-stream'}; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)

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
                elif parsed.path == "/" or parsed.path.startswith("/static/"):
                    self._serve_static(parsed.path)
                else:
                    self._send_json(404, {"error": "Not found"})
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
