"""Generate serve.json — map clean local URLs (/math-foundations) to real HTML paths."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "serve.json"

SKIP_MATH = {"math-foundations-content"}

# Old clean URLs that should keep working after a file rename.
LEGACY_SLUG_ALIASES: dict[str, str] = {
    "number-families": "foundation-number-families",
    # Mathematical Thinking track (unprefixed slugs before thinking-* rename)
    "gcf": "thinking-greatest-common-factor-gcf",
    "unit-conversions-and-rates": "thinking-unit-conversions-and-rates",
    "mental-squaring-and-square-rooting": "thinking-mental-squaring-and-square-rooting",
    "recovering-function-rule": "thinking-recovering-function-rule",
    "car-journey-advanced": "thinking-car-journey-advanced",
    "rotation-transformation": "thinking-rotation-transformation",
    "special-right-triangles": "thinking-special-right-triangles",
    "data-and-graphs": "thinking-data-and-graphs",
    "measures-of-center": "thinking-measures-of-center",
    "chance-and-probability": "thinking-chance-and-probability",
    "why-simplified-calculation": "thinking-why-simplified-calculation",
    "number-strategies": "thinking-number-strategies",
    "algebraic-strategies": "thinking-algebraic-strategies",
    "geometric-strategies": "thinking-geometric-strategies",
    "number-shape-thinking": "thinking-number-shape-thinking",
    "word-problems": "thinking-word-problems",
}


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

    for legacy_slug, target_slug in LEGACY_SLUG_ALIASES.items():
        target = ROOT / "math" / f"{target_slug}.html"
        if target.is_file():
            rewrites.append(
                {
                    "source": f"/{legacy_slug}",
                    "destination": f"/math/{target.name}",
                }
            )

    payload = {"rewrites": rewrites}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "with", len(rewrites), "rewrites")


if __name__ == "__main__":
    main()