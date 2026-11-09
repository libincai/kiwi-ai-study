#!/usr/bin/env python3
"""Normalize em dashes in HTML: data-en uses spaced — ; data-zh uses spaced ——."""

from __future__ import annotations

import re
import sys
from pathlib import Path

EM = "\u2014"


def fix_en_dashes(text: str) -> str:
    if EM not in text:
        return text
    parts = text.split(EM)
    return " — ".join(p.strip() for p in parts)


def fix_zh_dashes(text: str) -> str:
    if EM not in text:
        return text
    ph = "\uE000DOUBLE\uE001"
    text = re.sub(r"(?:\s*" + re.escape(EM) + r"\s*){2,}", ph, text)
    text = re.sub(re.escape(EM) + re.escape(EM), ph, text)
    text = text.replace(ph, " —— ")
    text = text.replace(" —— ", ph)
    text = re.sub(re.escape(EM), " —— ", text)
    text = text.replace(ph, " —— ")
    text = re.sub(r" {2,}", " ", text)
    return text


ZH_ATTR = re.compile(
    r'(?P<attr>data-zh(?:-label)?)="(?P<val>(?:[^"\\]|\\.)*)"'
)
EN_ATTR = re.compile(
    r'(?P<attr>data-en(?:-label)?)="(?P<val>(?:[^"\\]|\\.)*)"'
)


def process_html(content: str) -> tuple[str, int, int]:
    zh_count = 0
    en_count = 0

    def zh_sub(m: re.Match[str]) -> str:
        nonlocal zh_count
        old = m.group("val")
        new = fix_zh_dashes(old)
        if new != old:
            zh_count += 1
        return f'{m.group("attr")}="{new}"'

    content = ZH_ATTR.sub(zh_sub, content)

    def en_sub(m: re.Match[str]) -> str:
        nonlocal en_count
        old = m.group("val")
        new = fix_en_dashes(old)
        if new != old:
            en_count += 1
        return f'{m.group("attr")}="{new}"'

    content = EN_ATTR.sub(en_sub, content)

    def meta_sub(m: re.Match[str]) -> str:
        nonlocal en_count
        old = m.group(1)
        new = fix_en_dashes(old)
        if new != old:
            en_count += 1
        return f'<meta name="description" content="{new}"'

    content = re.sub(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        meta_sub,
        content,
        flags=re.I,
    )

    def aria_sub(m: re.Match[str]) -> str:
        nonlocal en_count
        old = m.group(1)
        if re.search(r"[\u4e00-\u9fff]", old):
            return m.group(0)
        new = fix_en_dashes(old)
        if new != old:
            en_count += 1
        return f'aria-label="{new}"'

    content = re.sub(r'aria-label="([^"]*)"', aria_sub, content)

    return content, zh_count, en_count


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    paths = sorted(root.rglob("*.html"))
    total_zh = total_en = 0
    changed_files: list[str] = []

    for path in paths:
        if "node_modules" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated, zh, en = process_html(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed_files.append(str(path.relative_to(root)))
            total_zh += zh
            total_en += en

    print(f"Files updated: {len(changed_files)}")
    print(f"data-zh/* fixes: {total_zh}")
    print(f"data-en/* + meta fixes: {total_en}")
    for f in changed_files:
        print(f"  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
