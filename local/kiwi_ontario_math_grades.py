"""Ontario Mathematics curriculum grade/course tags for Kiwi math lesson pages.

Only pages that match docs/ONTARIO_GRADE_LABELS.md belong here (Foundations +
verified secondary outcomes). Mathematical Thinking duplicates are excluded.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file under math/, grades, courses, chapter_id)
# courses empty = elementary grade-only label on the lesson page.
ONTARIO_MAPPINGS: list[tuple[str, list[int], list[str], str]] = [
    # —— Number skills (Ontario B strand / number) ——
    ("foundation-decimal.html", [4, 5, 6], [], "foundations-number"),
    ("foundation-decimal-to-fraction.html", [4, 5, 6], [], "foundations-number"),
    ("foundation-division-rules-2-9.html", [4, 5], [], "foundations-number"),
    ("foundation-math-operation-signs-and.html", [3, 4], [], "foundations-number"),
    ("foundation-result-signs-and.html", [6, 7], [], "foundations-number"),
    ("foundation-exponents.html", [7, 8, 9], ["MTH1W"], "foundations-number"),
    ("foundation-roots.html", [8, 9], ["MTH1W"], "foundations-number"),
    ("foundation-rational-exponents.html", [9, 11], ["MTH1W", "MCR3U"], "foundations-number"),
    ("foundation-greatest-common-factor-gcf.html", [6], [], "foundations-number"),
    ("foundation-number-families.html", [4, 5, 6], [], "foundations-number"),
    ("foundation-unit-conversions-and-rates.html", [6, 9], ["MTH1W"], "foundations-number"),
    # —— Functions & graphs ——
    ("foundation-algebra-language-and-patterns.html", [4, 5, 6, 9], ["MTH1W"], "foundations-functions-graphs"),
    ("foundation-understanding-functions.html", [9, 11], ["MTH1W", "MCR3U"], "foundations-functions-graphs"),
    ("foundation-linear-vs-non-linear-functions.html", [9, 10], ["MTH1W", "MPM2D"], "foundations-functions-graphs"),
    ("foundation-function-transformations.html", [11], ["MCR3U"], "foundations-functions-graphs"),
    ("foundation-functions-and-their-inverses.html", [11], ["MCR3U"], "foundations-functions-graphs"),
    ("foundation-step-pattern-and-first-differences-y.html", [9], ["MTH1W"], "foundations-functions-graphs"),
    ("foundation-understanding-the-placeholder-in-f-x.html", [11], ["MCR3U"], "foundations-functions-graphs"),
    ("foundation-algebraic-strategies.html", [6, 9], ["MTH1W"], "foundations-functions-graphs"),
    # —— Geometry & space ——
    ("foundation-basic-geometry-words.html", [4, 5, 6], [], "foundations-geometry"),
    ("foundation-rotation-transformation.html", [6, 10], ["MPM2D"], "foundations-geometry"),
    ("foundation-special-right-triangles.html", [10], ["MPM2D"], "foundations-geometry"),
    ("foundation-geometric-strategies.html", [4, 9], ["MTH1W"], "foundations-geometry"),
    ("foundation-trigonometry-fundamentals.html", [10, 11], ["MPM2D", "MCR3U"], "foundations-trigonometry"),
    # —— Data & chance ——
    ("foundation-data-and-graphs.html", [4, 5, 6], [], "foundations-data-chance"),
    ("foundation-measures-of-center.html", [6, 7, 8], [], "foundations-data-chance"),
    ("foundation-chance-and-probability.html", [7, 8], [], "foundations-data-chance"),
]

TITLE_META_EN = re.compile(
    r'<meta name="pagefind:title_en" content="([^"]+)"',
    re.I,
)
TITLE_META_ZH = re.compile(
    r'<meta name="pagefind:title_zh" content="([^"]+)"',
    re.I,
)


def _attr_pair(attrs: str) -> tuple[str, str] | None:
    en_m = re.search(r'data-en="([^"]*)"', attrs, re.I)
    if not en_m:
        return None
    zh_m = re.search(r'data-zh="([^"]*)"', attrs, re.I)
    en = html.unescape(en_m.group(1)).strip()
    zh = html.unescape(zh_m.group(1)).strip() if zh_m else en
    if not en:
        return None
    return en, zh or en


def _sidebar_title_for_page(text: str, fname: str) -> tuple[str, str] | None:
    """Level 2: active sidebar link for this file (see docs/MATH_NAV_LEVELS.md)."""
    for m in re.finditer(r"<a\s+([^>]+)>", text, re.I):
        attrs = m.group(1)
        if f'href="{fname}"' not in attrs:
            continue
        if not any(
            needle in attrs
            for needle in ('mf-current', "active", 'aria-current="page"', "aria-current='page'")
        ):
            continue
        pair = _attr_pair(attrs)
        if pair:
            return pair
    return None


def _article_title(text: str) -> tuple[str, str] | None:
    m = re.search(
        r'<article[^>]*class="[^"]*mf-article[^"]*"[^>]*>\s*<h1[^>]*data-en="([^"]+)"[^>]*data-zh="([^"]+)"',
        text,
        re.I | re.DOTALL,
    )
    if m:
        return html.unescape(m.group(1)).strip(), html.unescape(m.group(2)).strip()
    m = re.search(
        r'<article[^>]*class="[^"]*mf-article[^"]*"[^>]*>\s*<h1[^>]*data-en="([^"]+)"',
        text,
        re.I | re.DOTALL,
    )
    if m:
        en = html.unescape(m.group(1)).strip()
        return en, en
    m = re.search(r'class="kiwi-current-topic"[^>]*data-en="([^"]+)"', text, re.I)
    if m:
        en = html.unescape(m.group(1)).strip()
        zh_m = re.search(r'class="kiwi-current-topic"[^>]*data-zh="([^"]+)"', text, re.I)
        zh = html.unescape(zh_m.group(1)).strip() if zh_m else en
        return en, zh
    return None


def read_titles(path: Path) -> tuple[str, str]:
    """Grade-hub Level 2 titles: sidebar label, then article heading, then meta."""
    if not path.is_file():
        stem = path.stem.replace("-", " ").title()
        return stem, stem
    text = path.read_text(encoding="utf-8")
    fname = path.name

    pair = _sidebar_title_for_page(text, fname) or _article_title(text)
    if pair:
        return pair

    en = zh = ""
    m = TITLE_META_EN.search(text)
    if m:
        en = html.unescape(m.group(1)).strip()
    m = TITLE_META_ZH.search(text)
    if m:
        zh = html.unescape(m.group(1)).strip()
    if not en:
        m = re.search(
            r'class="[^"]*topic-banner[^"]*"[^>]*>.*?<h1[^>]*data-en="([^"]+)"',
            text,
            re.I | re.DOTALL,
        )
        if m:
            en = html.unescape(m.group(1)).strip()
    if not zh:
        m = re.search(
            r'class="[^"]*topic-banner[^"]*"[^>]*>.*?<h1[^>]*data-zh="([^"]+)"',
            text,
            re.I | re.DOTALL,
        )
        if m:
            zh = html.unescape(m.group(1)).strip()
    if not zh:
        zh = en
    if not en:
        en = zh or path.stem.replace("-", " ").title()
    return en, zh


def build_ontario_topics(*, seen_files: set[str]) -> list[dict]:
    topics: list[dict] = []
    for fname, grades, courses, chapter_id in ONTARIO_MAPPINGS:
        path = f"math/{fname}"
        if path in seen_files:
            continue
        title_en, title_zh = read_titles(ROOT / path)
        topics.append(
            {
                "id": fname.replace(".html", ""),
                "file": path,
                "title_en": title_en,
                "title_zh": title_zh,
                "grades": grades,
                "courses": courses,
                "chapter_id": chapter_id,
                "sort": 0,
                "list_on_grade_hub": False,
                "verified_note": "Ontario curriculum expectation alignment (see docs/ONTARIO_GRADE_LABELS.md)",
            }
        )
        seen_files.add(path)
    return topics