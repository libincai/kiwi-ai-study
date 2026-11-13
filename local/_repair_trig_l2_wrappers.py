"""Restore L3 lesson-card wrappers when section titles were flattened to bare h4."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _flatten_trig_nested_cards import ARTICLE_IN, flatten_nested_lesson_cards
from _trig_toc_20261113 import SECTIONS

H1_RE = re.compile(r"^(\s*<h1[^>]*>.*?</h1>\s*)", re.DOTALL)


def lesson_slug(href: str) -> str:
    return href.removeprefix("foundation-").removesuffix(".html")


def wrap_l3_block(slug: str, en: str, zh: str, body: str) -> str:
    body = body.strip()
    if body.startswith("<details"):
        return (
            f'<details class="lesson-card"><summary id="{slug}" '
            f'data-en="{en}" data-zh="{zh}">{en}</summary>'
            f'<div class="lesson-card-content">{body}</div></details>'
        )
    body = re.sub(
        r'^id="[^"]+"\s+data-en="[^"]*"\s+data-zh="[^"]*">[^<]*</h4>\s*',
        "",
        body,
        count=1,
    )
    body = re.sub(
        rf'^<h4 id="{re.escape(slug)}"[^>]*>.*?</h4>\s*',
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    return (
        f'<details class="lesson-card"><summary id="{slug}" '
        f'data-en="{en}" data-zh="{zh}">{en}</summary>'
        f'<div class="lesson-card-content">{body}</div></details>'
    )


def rebuild_hub_article(hub_file: str, hub_en: str, hub_zh: str, lessons: list) -> str:
    path = MATH / hub_file
    text = path.read_text(encoding="utf-8")
    m = ARTICLE_IN.search(text)
    if not m:
        raise ValueError(f"no article: {hub_file}")
    inner = m.group(2)
    h1_m = H1_RE.match(inner)
    if not h1_m:
        raise ValueError(f"no h1: {hub_file}")
    h1 = h1_m.group(1)
    rest = inner[h1_m.end() :]

    cards: list[str] = []
    for row in lessons:
        href, en, zh = row[0], row[1], row[2]
        slug = lesson_slug(href)
        # Prefer existing top-level card for this slug
        card_pat = re.compile(
            rf'<details class="lesson-card"[^>]*>\s*<summary[^>]*\bid="{re.escape(slug)}"[^>]*>',
            re.IGNORECASE,
        )
        if card_pat.search(rest):
            card_m = re.compile(
                rf'<details class="lesson-card"[^>]*>\s*<summary[^>]*\bid="{re.escape(slug)}"[^>]*>.*?</summary>\s*'
                rf'<div class="lesson-card-content">.*?</div>\s*</details>',
                re.DOTALL,
            )
            cm = card_m.search(rest)
            if cm:
                cards.append(cm.group(0))
                continue
        # Orphan section: h4/h2 title with this id, or bare id marker
        for opener in (
            rf'<h4 id="{re.escape(slug)}"',
            rf'<h2 id="{re.escape(slug)}"',
            rf'<summary id="{re.escape(slug)}"',
        ):
            idx = rest.find(opener)
            if idx != -1:
                break
        else:
            idx = rest.find(f'id="{slug}"')
        if idx == -1:
            print("warn missing section", hub_file, slug)
            continue
        next_idx = len(rest)
        for other in lessons:
            other_slug = lesson_slug(other[0])
            if other_slug == slug:
                continue
            for marker in (
                f'<h4 id="{other_slug}"',
                f'<h2 id="{other_slug}"',
                f'<details class="lesson-card"',
                f'<summary id="{other_slug}"',
            ):
                j = rest.find(marker, idx + 1)
                if j != -1:
                    next_idx = min(next_idx, j)
        body = rest[idx:next_idx]
        cards.append(wrap_l3_block(slug, en, zh, body))

    article = f"<article class=\"mf-article mf-chapter\">{h1}" + "\n".join(cards) + "</article>"
    return article


def repair_hub(hub_file: str, hub_en: str, hub_zh: str, lessons: list) -> None:
    path = MATH / hub_file
    text = path.read_text(encoding="utf-8")
    article = rebuild_hub_article(hub_file, hub_en, hub_zh, lessons)
    # flatten inner nested cards only
    inner = re.search(r"<article[^>]*>(.*)</article>", article, re.DOTALL).group(1)
    inner = flatten_nested_lesson_cards(inner)
    article = f'<article class="mf-article mf-chapter">{inner}</article>'
    if not ARTICLE_IN.search(text):
        return
    text = ARTICLE_IN.sub(lambda _m: article, text, count=1)
    path.write_text(text, encoding="utf-8")
    print("repaired", hub_file)


def main() -> None:
    targets = {
        "foundation-angles-and-trigonometric-ratios.html",
        "foundation-trigonometric-identities.html",
    }
    for hub_file, hub_en, hub_zh, *_rest, lessons in SECTIONS:
        if hub_file not in targets:
            continue
        repair_hub(hub_file, hub_en, hub_zh, lessons)


if __name__ == "__main__":
    main()
