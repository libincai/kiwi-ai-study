"""Assemble Level-2 trig pages: L3 topics as expandable lesson-card sections."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _trig_toc_20261113 import SECTIONS

ARTICLE_IN = re.compile(
    r"<article class=\"mf-article mf-chapter\">.*?</article>",
    re.DOTALL,
)
ARTICLE_BODY = re.compile(
    r"<article class=\"mf-article mf-chapter\">(.*?)</article>",
    re.DOTALL,
)
H1_RE = re.compile(r"<h1[^>]*>.*?</h1>\s*", re.DOTALL)
TITLE_RE = re.compile(r"<title[^>]*>.*?</title>", re.DOTALL)
SHELL = MATH / "foundation-special-right-triangles.html"
NESTED_CARD = re.compile(
    r"<details class=\"lesson-card\"><summary([^>]*)>(.*?)</summary>\s*"
    r"<div class=\"lesson-card-content\">(.*?)</div>\s*</details>",
    re.DOTALL,
)


def flatten_body(body: str) -> str:
    while True:
        m = NESTED_CARD.search(body)
        if not m:
            return body
        repl = f"<h4{m.group(1)}>{m.group(2)}</h4>{m.group(3)}"
        body = body[: m.start()] + repl + body[m.end() :]
    return body


def lesson_slug(href: str) -> str:
    return href.removeprefix("foundation-").removesuffix(".html")


def extract_article_inner(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = ARTICLE_BODY.search(text)
    if not m:
        raise ValueError(f"no article in {path.name}")
    inner = m.group(1)
    return H1_RE.sub("", inner, count=1).strip()


def l3_card(href: str, title_en: str, title_zh: str, inner: str) -> str:
    sid = lesson_slug(href)
    return (
        f'<details class="lesson-card"><summary id="{sid}" '
        f'data-en="{title_en}" data-zh="{title_zh}">{title_en}</summary>'
        f'<div class="lesson-card-content">{inner}</div></details>'
    )


def build_article(hub_en: str, hub_zh: str, lessons: list[tuple]) -> str:
    cards: list[str] = []
    for row in lessons:
        href, title_en, title_zh = row[0], row[1], row[2]
        lesson_path = MATH / href
        if not lesson_path.is_file():
            print("skip missing lesson", href)
            continue
        inner = flatten_body(extract_article_inner(lesson_path))
        cards.append(l3_card(href, title_en, title_zh, inner))
    body = "\n".join(cards)
    return (
        f'<article class="mf-article mf-chapter">'
        f'<h1 data-en="{hub_en}" data-zh="{hub_zh}">{hub_en}</h1>\n'
        f"{body}\n</article>"
    )


def write_redirect(hub: str, href: str, title_en: str) -> None:
    path = MATH / href
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    anchor = lesson_slug(href)
    target = f"{hub}#{anchor}"
    redirect_article = (
        f'<article class="mf-article mf-chapter">'
        f'<h1 data-en="{title_en}" data-zh="{title_en}">{title_en}</h1>'
        f'<p class="edu-lead">This topic is part of '
        f'<a href="{hub}">{hub.replace("foundation-", "").replace(".html", "")}</a>. '
        f'<a href="{target}">Jump to section →</a></p>'
        f"<script>location.replace({target!r});</script>"
        f"</article>"
    )
    if not ARTICLE_IN.search(text):
        return
    text = ARTICLE_IN.sub(lambda _m: redirect_article, text, count=1)
    path.write_text(text, encoding="utf-8")
    print("redirect", href, "->", target)


def write_hub(hub_file: str, hub_en: str, hub_zh: str, lessons: list[tuple]) -> None:
    hub_path = MATH / hub_file
    if hub_path.is_file():
        text = hub_path.read_text(encoding="utf-8")
    else:
        text = SHELL.read_text(encoding="utf-8")
    new_title = (
        f'<title data-en="{hub_en} | KIWI 爱AI Study" data-zh="{hub_zh} | KIWI 爱AI Study">'
        f"{hub_en} | KIWI 爱AI Study</title>"
    )
    text = TITLE_RE.sub(new_title, text, count=1)
    article = build_article(hub_en, hub_zh, lessons)
    if not ARTICLE_IN.search(text):
        raise ValueError(f"no article slot in {hub_file}")
    text = ARTICLE_IN.sub(lambda _m: article, text, count=1)
    hub_path.write_text(text, encoding="utf-8")
    print("assembled", hub_file)
    for row in lessons:
        write_redirect(hub_file, row[0], row[1])


def main() -> None:
    for hub_file, hub_en, hub_zh, _lead_en, _lead_zh, lessons in SECTIONS:
        write_hub(hub_file, hub_en, hub_zh, lessons)


if __name__ == "__main__":
    main()
