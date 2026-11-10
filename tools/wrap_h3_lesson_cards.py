#!/usr/bin/env python3
"""Wrap mf-article h3 sections in details.lesson-card (Level 4 accordion pattern)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "math" / "foundation-rational-exponents.html"

H3_RE = re.compile(
    r'<h3\s+id="(?P<id>[^"]+)"\s+data-en="(?P<en>[^"]*)"\s+data-zh="(?P<zh>[^"]*)"[^>]*>(?P<label>[\s\S]*?)</h3>',
    re.I,
)


def wrap_h3_sections(html: str) -> str:
    start = html.find('<article class="mf-article mf-chapter">')
    if start < 0:
        raise SystemExit("article not found")
    end = html.find("</article>", start)
    if end < 0:
        raise SystemExit("article end not found")
    article = html[start:end]

    matches = list(H3_RE.finditer(article))
    if not matches:
        raise SystemExit("no h3 sections found")

    h1_m = re.search(
        r'<h1[^>]*data-en="Rational Exponents"[^>]*>[\s\S]*?</h1>',
        article,
        re.I,
    )
    if not h1_m:
        raise SystemExit("h1 not found")
    intro = article[h1_m.end() : matches[0].start()]

    cards: list[str] = []
    for i, m in enumerate(matches):
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(article)
        body = article[m.end() : body_end].strip()
        label = m.group("label").strip()
        sid = m.group("id")
        en = m.group("en")
        zh = m.group("zh")
        cards.append(
            f'<details class="lesson-card"><summary id="{sid}" data-en="{en}" data-zh="{zh}">{label}</summary>'
            f'<div class="lesson-card-content">{body}</div></details>'
        )

    new_article = article[: h1_m.end()] + intro + "".join(cards)
    return html[:start] + new_article + html[end:]


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else PATH
    text = path.read_text(encoding="utf-8")
    text = wrap_h3_sections(text)
    path.write_text(text, encoding="utf-8")
    print(f"Wrapped h3 sections in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
