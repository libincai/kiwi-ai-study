#!/usr/bin/env python3
"""Apply DESIGN_STANDARDS H4/H5 CSS to foundation-* and thinking-* math pages."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT / "math"

OLD_ARTICLE = (
    ".mf-article h4,.mf-article h5{font-size:16px;color:#173e70;margin:17px 0 7px}"
)
NEW_ARTICLE = (
    ".mf-article h4{font-size:16px;font-weight:750;color:#173e70;margin:20px 0 8px}"
    ".mf-article h5{font-size:15px;font-weight:650;color:#1768b2;"
    "margin:12px 0 6px 3ch;line-height:1.5}"
)

OLD_LESSON = (
    ".mf-article .lesson-card-content h4,.mf-article .lesson-card-content h5"
    "{color:#153d70;font-size:16px;margin:17px 0 7px}"
)
NEW_LESSON = (
    ".mf-article .lesson-card-content h4{color:#153d70;font-size:16px;font-weight:750;"
    "margin:20px 0 8px}"
    ".mf-article .lesson-card-content h5{font-size:15px;font-weight:650;color:#1768b2;"
    "margin:12px 0 6px 3ch;line-height:1.5}"
)

NUMBER_FAMILIES_ANCHOR = (
    ".foundation-level4 .mf-article h1{font-size:clamp(23px,2.6vw,30px);"
    "color:#153d70;border-bottom:2px solid #e5f2ff;padding-bottom:12px;margin:0 0 22px}"
)
NUMBER_FAMILIES_HEADINGS = (
    ".foundation-level4 .mf-article h4{font-size:16px;font-weight:750;color:#173e70;"
    "margin:20px 0 8px}"
    ".foundation-level4 .mf-article h5{font-size:15px;font-weight:650;color:#1768b2;"
    "margin:12px 0 6px 3ch;line-height:1.5}"
)

THINKING_LESSON_H3 = (
    ".lesson-card-content h3{color:#153d70;font-size:17px;margin:20px 0 8px}"
)
THINKING_LESSON_H3_H4_H5 = (
    THINKING_LESSON_H3
    + ".lesson-card-content h4{color:#153d70;font-size:16px;font-weight:750;margin:20px 0 8px}"
    + ".lesson-card-content h5{font-size:15px;font-weight:650;color:#1768b2;"
    "margin:12px 0 6px 3ch;line-height:1.5}"
)


def patch_foundation_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    if OLD_ARTICLE in text:
        text = text.replace(OLD_ARTICLE, NEW_ARTICLE, 1)
        notes.append("article h4/h5 split")
    elif ".mf-article h5{font-size:15px;font-weight:650" in text:
        notes.append("article already split")
    else:
        notes.append("article: no bundled rule")

    count = text.count(OLD_LESSON)
    if count:
        text = text.replace(OLD_LESSON, NEW_LESSON)
        notes.append(f"lesson-card h4/h5 split ({count})")
    elif ".lesson-card-content h5{font-size:15px;font-weight:650" in text:
        notes.append("lesson-card already split")

    if path.name == "foundation-number-families.html":
        if NUMBER_FAMILIES_ANCHOR in text and NUMBER_FAMILIES_HEADINGS not in text:
            text = text.replace(
                NUMBER_FAMILIES_ANCHOR,
                NUMBER_FAMILIES_ANCHOR + NUMBER_FAMILIES_HEADINGS,
                1,
            )
            notes.append("number-families h4/h5 added")

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
    return notes


def patch_thinking_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    if THINKING_LESSON_H3_H4_H5 in text:
        notes.append("word-topic lesson h4/h5 already")
    elif THINKING_LESSON_H3 in text:
        text = text.replace(THINKING_LESSON_H3, THINKING_LESSON_H3_H4_H5, 1)
        notes.append("word-topic lesson h4/h5 added")

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
    return notes


def main() -> int:
    foundation_paths = sorted(MATH.glob("foundation-*.html"))
    f_updated = 0
    for path in foundation_paths:
        notes = patch_foundation_file(path)
        changed = any("split" in n or "added" in n for n in notes)
        if changed:
            f_updated += 1
            print(f"OK {path.name}: {', '.join(notes)}")
        elif "already" in " ".join(notes):
            print(f"-- {path.name}: {', '.join(notes)}")

    thinking_paths = sorted(MATH.glob("thinking-*.html"))
    t_updated = 0
    for path in thinking_paths:
        notes = patch_thinking_file(path)
        if any("added" in n for n in notes):
            t_updated += 1
            print(f"OK {path.name}: {', '.join(notes)}")
        elif notes:
            print(f"-- {path.name}: {', '.join(notes)}")

    print(
        f"\nFoundation: {f_updated} updated of {len(foundation_paths)}. "
        f"Thinking (advanced): {t_updated} updated of {len(thinking_paths)}. "
        "Global rules also in assets/css/styles.css."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())