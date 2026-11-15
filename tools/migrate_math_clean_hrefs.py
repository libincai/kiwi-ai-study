"""Rewrite math links: *.html -> /clean-slug (Level 4 + hubs; GitHub /kiwi-ai-study parity)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT / "math"
SKIP_STEMS = {"math-foundations-content"}
HUB_BACK = re.compile(r'href="index\.html"')
HUB_BACK_REPL = 'href="/math"'
IN_CLASS_OLD = re.compile(r'href="\.\./math/in-class-learning\.html"')
IN_CLASS_NEW = 'href="/in-class-learning"'
EMBED_HREF = re.compile(r'href=&quot;([a-z0-9][\w-]*?)(?:\.html)?&quot;', re.I)
EMBED_HASH = re.compile(r'href=&quot;([a-z0-9][\w-]*?)\.html(#[^&]+?)&quot;', re.I)
HASH_LINK = re.compile(r'href="([a-z0-9][\w-]*)\.html(#[^"]+)"', re.I)
LEGACY_TO_THINKING = {
    "unit-conversions-and-rates": "thinking-unit-conversions-and-rates",
    "special-right-triangles": "thinking-special-right-triangles",
    "number-strategies": "thinking-number-strategies",
    "algebraic-strategies": "thinking-algebraic-strategies",
    "geometric-strategies": "thinking-geometric-strategies",
    "why-simplified-calculation": "thinking-why-simplified-calculation",
    "word-problems": "thinking-word-problems",
    "data-and-graphs": "thinking-data-and-graphs",
    "measures-of-center": "thinking-measures-of-center",
    "chance-and-probability": "thinking-chance-and-probability",
}


def collect_slugs() -> set[str]:
    return {
        p.stem
        for p in MATH.glob("*.html")
        if p.stem not in SKIP_STEMS
    }


def slug_to_clean(slug: str) -> str:
    slug = slug.replace(".html", "").strip("/")
    if slug in LEGACY_TO_THINKING:
        slug = LEGACY_TO_THINKING[slug]
    return f"/{slug}" if slug else "/"


def migrate_file(path: Path, slugs: set[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    slug_alt = "|".join(re.escape(s) for s in sorted(slugs, key=len, reverse=True))
    pattern = re.compile(rf'href="({slug_alt})\.html"')

    def repl(match: re.Match[str]) -> str:
        return f'href="/{match.group(1)}"'

    text = pattern.sub(repl, text)
    if path.name != "index.html":
        text = HUB_BACK.sub(HUB_BACK_REPL, text)
    text = IN_CLASS_OLD.sub(IN_CLASS_NEW, text)

    def embed_repl(match: re.Match[str]) -> str:
        clean = slug_to_clean(match.group(1))
        return f'href=&quot;{clean}&quot;'

    text = EMBED_HREF.sub(embed_repl, text)

    def embed_hash_repl(match: re.Match[str]) -> str:
        clean = slug_to_clean(match.group(1))
        return f'href=&quot;{clean}{match.group(2)}&quot;'

    text = EMBED_HASH.sub(embed_hash_repl, text)
    text = HASH_LINK.sub(
        lambda m: f'href="{slug_to_clean(m.group(1) + ".html")}{m.group(2)}"', text
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    slugs = collect_slugs()
    n = sum(1 for p in MATH.glob("*.html") if migrate_file(p, slugs))
    print("updated", n, "math html files (clean href slugs + crosslink data)")


if __name__ == "__main__":
    main()