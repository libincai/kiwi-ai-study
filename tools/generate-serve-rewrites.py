"""Generate serve.json — map clean local URLs (/math-foundations) to real HTML paths."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "serve.json"

SKIP_MATH = {"math-foundations-content"}


def main() -> None:
    rewrites: list[dict[str, str]] = []

    seen_slugs: set[str] = set()
    for path in sorted((ROOT / "math").glob("*.html")):
        slug = path.stem
        if slug in SKIP_MATH or slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        if slug == "index":
            rewrites.append({"source": "/math", "destination": "/math/index.html"})
        else:
            rewrites.append({"source": f"/{slug}", "destination": f"/math/{path.name}"})

    for path in sorted((ROOT / "ai").glob("episode-*.html")):
        rewrites.append({"source": f"/{path.stem}", "destination": f"/ai/{path.name}"})
    if (ROOT / "ai" / "index.html").is_file():
        rewrites.append({"source": "/ai", "destination": "/ai/index.html"})

    for section in ("about", "contact", "books"):
        if (ROOT / section / "index.html").is_file():
            rewrites.append({"source": f"/{section}", "destination": f"/{section}/index.html"})

    payload = {"rewrites": rewrites}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "with", len(rewrites), "rewrites")


if __name__ == "__main__":
    main()