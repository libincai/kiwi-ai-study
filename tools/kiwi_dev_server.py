"""Serve the repo at http://localhost:3000/kiwi-ai-study/ (GitHub project Pages parity)."""
from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/kiwi-ai-study"
SERVE_JSON = ROOT / "serve.json"
DEFAULT_PORT = 3000


def load_serve_config() -> tuple[dict[str, str], dict[str, str]]:
    data = json.loads(SERVE_JSON.read_text(encoding="utf-8"))
    rewrites: dict[str, str] = {}
    for rule in data.get("rewrites", []):
        src = rule.get("source", "")
        dest = rule.get("destination", "")
        if not src.startswith(PREFIX) or src in (PREFIX, f"{PREFIX}/"):
            continue
        if src.endswith("/**") or ":path" in src:
            continue
        key = src[len(PREFIX) :] or "/"
        rewrites[key] = dest
        if not key.endswith("/") and key != "/":
            rewrites[key + "/"] = dest
    redirects = {
        r["source"]: r["destination"] for r in data.get("redirects", []) if "source" in r
    }
    return rewrites, redirects


REWRITES, REDIRECTS = load_serve_config()


class KiwiDevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _pathname(self) -> str:
        return unquote(urlsplit(self.path).path)

    def _redirect(self, location: str) -> None:
        query = urlsplit(self.path).query
        if query:
            location = f"{location}?{query}"
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _map_path(self, path: str) -> str:
        if path.startswith(PREFIX):
            path = path[len(PREFIX) :] or "/"
        key = path.rstrip("/") if path != "/" else "/"
        if key in REWRITES:
            path = REWRITES[key]
        elif path in REWRITES:
            path = REWRITES[path]
        if path.endswith("/") and path != "/":
            path = path + "index.html"
        if path == "/":
            path = "/index.html"
        return path

    def translate_path(self, path: str) -> str:
        path = self._map_path(unquote(urlsplit(path).path))
        return super().translate_path(path)

    def do_GET(self) -> None:
        pathname = self._pathname()
        if pathname in REDIRECTS:
            self._redirect(REDIRECTS[pathname])
            return
        super().do_GET()

    def do_HEAD(self) -> None:
        pathname = self._pathname()
        if pathname in REDIRECTS:
            self._redirect(REDIRECTS[pathname])
            return
        super().do_HEAD()


def main() -> None:
    os.chdir(ROOT)
    if not SERVE_JSON.is_file():
        print("Missing serve.json — run tools/generate-serve-rewrites.py first", file=sys.stderr)
        sys.exit(1)
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    host = "127.0.0.1"
    try:
        httpd = ThreadingHTTPServer((host, port), KiwiDevHandler)
    except OSError as err:
        if err.errno in (98, 10048, 48):  # address already in use
            print(
                f"Port {port} is in use (often an old `npx serve`).\n"
                f"Run .\\tools\\dev-server.ps1 to stop it and start the KIWI dev server.",
                file=sys.stderr,
            )
        else:
            print(err, file=sys.stderr)
        sys.exit(1)
    with httpd:
        url = f"http://{host}:{port}{PREFIX}/"
        print(f"KIWI dev server at {url} (matches GitHub Pages)")
        print(f"  {len(REWRITES)} clean-url rewrites, {len(REDIRECTS)} redirects")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()