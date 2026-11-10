#!/usr/bin/env python3
"""Convert legacy nested 'mnemonic + category' Word tables to kiwi-edu-table-with-mnemonic."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TABLE_WRAP_OLD = re.compile(
    r"<table>\s*<colgroup>\s*<col style=\"width: 100%\"/>\s*</colgroup>\s*"
    r"<thead>\s*<tr class=\"header\">\s*"
    r"<th>(?P<mnemonic>.*?)</th>\s*</tr>\s*</thead>\s*<tbody>\s*</tbody>\s*</table>",
    re.DOTALL,
)

INNER_BLOCK = re.compile(
    r"<table>\s*<colgroup>(?P<cols>.*?)</colgroup>\s*"
    r"<thead>\s*<tr class=\"header\">\s*"
    r"<th colspan=\"3\"(?P<cat_attrs>[^>]*)>(?P<cat>.*?)</th>\s*</tr>\s*</thead>\s*"
    r"<tbody>(?P<rows>.*?)</tbody>\s*</table>",
    re.DOTALL,
)

ROW_CLASS = re.compile(r'\s*class="(?:odd|even)"')


def strip_row_classes(rows: str) -> str:
    return ROW_CLASS.sub("", rows)


def mnemonic_th(mnemonic: str) -> str:
    inner = mnemonic.strip()
    # Normalize <p>...</p> mnemonic to single th content
    m = re.match(r"<p([^>]*)>(.*)</p>\s*$", inner, re.DOTALL)
    if m:
        attrs, body = m.group(1), m.group(2)
        if "data-en=" in attrs:
            return f"<th colspan=\"3\"{attrs}>{body}</th>"
    if inner.startswith("<th"):
        return inner.replace("<th", '<th colspan="3"', 1) if 'colspan=' not in inner else inner
    return f'<th colspan="3">{inner}</th>'


def convert_block(match: re.Match[str]) -> str:
    mnemonic_raw = match.group("mnemonic")
    inner_tables = list(INNER_BLOCK.finditer(mnemonic_raw))
    if not inner_tables:
        return match.group(0)
    mnemonic_part = INNER_BLOCK.sub("", mnemonic_raw, count=len(inner_tables))
    mnemonic_cell = mnemonic_th(mnemonic_part)
    cols = inner_tables[0].group("cols")
    body_parts: list[str] = []
    for it in inner_tables:
        cat_attrs = it.group("cat_attrs")
        cat = it.group("cat").strip()
        rows = strip_row_classes(it.group("rows"))
        body_parts.append(
            f"<tr>\n<th colspan=\"3\"{cat_attrs}>{cat}</th>\n</tr>\n{rows}"
        )
    tbody = "\n".join(body_parts)
    return (
        '<div class="edu-table-wrap">\n'
        '<table class="edu-table kiwi-edu-table-with-mnemonic">\n'
        f"<colgroup>{cols}</colgroup>\n"
        "<thead>\n"
        '<tr class="kiwi-edu-table-mnemonic">\n'
        f"{mnemonic_cell}\n"
        "</tr>\n"
        "</thead>\n"
        f"<tbody>\n{tbody}</tbody>\n"
        "</table>\n"
        "</div>"
    )


def convert_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    # Legacy outer wrapper: mnemonic th contains inner tables before closing </th>
    pattern = re.compile(
        r"<table>\s*<colgroup>\s*<col style=\"width: 100%\"/>\s*</colgroup>\s*"
        r"<thead>\s*<tr class=\"header\">\s*"
        r"<th>(?P<inner>.*?)</th>\s*</tr>\s*</thead>\s*<tbody>\s*</tbody>\s*</table>",
        re.DOTALL,
    )

    def repl(m: re.Match[str]) -> str:
        inner = m.group("inner")
        if inner.count("<table") < 1:
            return m.group(0)
        fake_mnemonic = re.match(
            r"(?P<lead>.*?)<table>",
            inner,
            re.DOTALL,
        )
        if not fake_mnemonic:
            return m.group(0)
        mnemonic = fake_mnemonic.group("lead").strip()
        rest = inner[fake_mnemonic.end() - len("<table>") :]  # noqa: unclear
        # Rebuild: mnemonic + all inner tables as substring
        combined = mnemonic + inner[len(mnemonic) :]
        inner_tables = list(INNER_BLOCK.finditer(combined))
        if not inner_tables:
            return m.group(0)
        cols = inner_tables[0].group("cols")
        body_parts: list[str] = []
        for it in inner_tables:
            cat_attrs = it.group("cat_attrs")
            cat = it.group("cat").strip()
            rows = strip_row_classes(it.group("rows"))
            body_parts.append(
                f"<tr>\n<th colspan=\"3\"{cat_attrs}>{cat}</th>\n</tr>\n{rows}"
            )
        tbody = "\n".join(body_parts)
        return (
            '<div class="edu-table-wrap">\n'
            '<table class="edu-table kiwi-edu-table-with-mnemonic">\n'
            f"<colgroup>{cols}</colgroup>\n"
            "<thead>\n"
            '<tr class="kiwi-edu-table-mnemonic">\n'
            f"{mnemonic_th(mnemonic)}\n"
            "</tr>\n"
            "</thead>\n"
            f"<tbody>\n{tbody}</tbody>\n"
            "</table>\n"
            "</div>"
        )

    new_html, n = pattern.subn(repl, html)
    if n:
        path.write_text(new_html, encoding="utf-8")
    return n > 0


MF_TABLE_CSS_OLD = ".mf-article table{border-collapse:collapse;width:100%;margin:14px 0;display:block;overflow-x:auto}"
MF_TABLE_CSS_NEW = (
    ".mf-article .edu-table-wrap{max-width:100%;overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}"
    ".mf-article table{border-collapse:collapse;width:100%;margin:14px 0;display:table;table-layout:fixed}"
    ".mf-article .edu-table-wrap table{margin:0}"
)


def patch_page_css(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MF_TABLE_CSS_OLD not in text:
        return False
    path.write_text(text.replace(MF_TABLE_CSS_OLD, MF_TABLE_CSS_NEW), encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    targets = argv or [
        "math/foundation-result-signs-and.html",
        "math/foundation-exponents.html",
        "math/foundation-roots.html",
    ]
    converted = []
    for rel in targets:
        path = ROOT / rel
        if not path.is_file():
            print(f"skip missing {rel}")
            continue
        if convert_file(path):
            converted.append(rel)
            print(f"converted tables in {rel}")
        patch_page_css(path)
    if not converted and not argv:
        print("no nested mnemonic tables found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
