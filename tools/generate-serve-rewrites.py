"""Generate serve.json — local URLs match GitHub project Pages (/kiwi-ai-study/...)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "serve.json"

# Same segment as GitHub Pages project site and assets/js/kiwi-site-base.js.
SITE_PREFIX = "kiwi-ai-study"

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


def collect_slug_rewrites() -> list[dict[str, str]]:
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

    return rewrites


def main() -> None:
    slug_rewrites = collect_slug_rewrites()
    prefix = f"/{SITE_PREFIX}"

    rewrites: list[dict[str, str]] = []

    for rule in slug_rewrites:
        rewrites.append(
            {
                "source": f"{prefix}{rule['source']}",
                "destination": rule["destination"],
            }
        )

    rewrites.append({"source": prefix, "destination": "/index.html"})
    rewrites.append({"source": f"{prefix}/", "destination": "/index.html"})
    # Static files (assets/, …) are served by stripping PREFIX in tools/kiwi_dev_server.py.

    redirects: list[dict[str, str | int]] = [
        {"source": "/", "destination": f"{prefix}/", "type": 302},
    ]
    for rule in slug_rewrites:
        redirects.append(
            {
                "source": rule["source"],
                "destination": f"{prefix}{rule['source']}",
                "type": 302,
            }
        )
        src = rule["source"]
        if src != "/":
            redirects.append(
                {
                    "source": f"{src}.html",
                    "destination": f"{prefix}{src}",
                    "type": 302,
                }
            )
            redirects.append(
                {
                    "source": f"{prefix}{src}.html",
                    "destination": f"{prefix}{src}",
                    "type": 302,
                }
            )

    # Legacy nav links use ../math/<slug>.html → /math/<slug> in the browser bar.
    for path in sorted((ROOT / "math").glob("*.html")):
        slug = path.stem
        if slug in SKIP_MATH:
            continue
        if slug == "index":
            canon = f"{prefix}/math"
            legacy_sources = ("/math/index.html",)
        else:
            canon = f"{prefix}/{slug}"
            legacy_sources = (f"/math/{slug}", f"/math/{path.name}")
        for legacy in legacy_sources:
            redirects.append({"source": legacy, "destination": canon, "type": 302})

    payload = {"rewrites": rewrites, "redirects": redirects}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "wrote",
        OUT.relative_to(ROOT),
        "—",
        len(rewrites),
        "rewrites,",
        len(redirects),
        "redirects under",
        prefix,
    )


if __name__ == "__main__":
    main()
    try:
        import importlib.util
        from pathlib import Path

        stub_py = Path(__file__).with_name("generate_github_pages_stubs.py")
        if stub_py.is_file():
            spec = importlib.util.spec_from_file_location("gh_stubs", stub_py)
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)
            mod.main()
    except Exception as err:
        print("warn: GitHub Pages stubs not updated:", err, file=__import__("sys").stderr)