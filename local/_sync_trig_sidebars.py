"""Sync trigonometry sidebar: Level 2 only (Math Quick Ref 20261113.docx)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _trig_toc_20261113 import SIDEBAR_LEVEL2, all_sync_pages

TOC_CSS = """<style id="trig-toc-sidebar">
.mf-sidebar .mf-trig-toc-title{margin:0 0 10px;padding:4px 8px 10px;font-size:15px;font-weight:800;color:#153d70;border-bottom:1px solid #dce7f3}
.mf-sidebar .mf-trig-toc-parent{padding:6px 0;border-top:1px solid #e1e9f4}
.mf-sidebar .mf-trig-toc-parent:first-of-type{border-top:0}
.mf-sidebar .mf-trig-toc-parent a{display:block;font-size:13px;font-weight:700;color:#173e70;padding:8px 6px;line-height:1.35;border-radius:9px}
.mf-sidebar .mf-trig-toc-parent a.mf-current{background:#deecff;color:#073e83;font-weight:700;border-left:3px solid #0865c9;padding-left:10px}
.mf-sidebar .mf-trig-toc-parent a:hover{background:#e8f2ff;color:#0756ba}
</style>"""

BACK = (
    '<a class="kiwi-sidebar-back" data-en="← All Math Foundations" '
    'data-zh="← 返回数学基础目录" href="math-foundations.html">← All Math Foundations</a>'
)


def link_html(href: str, en: str, zh: str, *, current: bool) -> str:
    if current:
        return (
            f'<a aria-current="page" class="mf-current" href="{href}" '
            f'data-en="{en}" data-zh="{zh}">{en}</a>'
        )
    return f'<a href="{href}" data-en="{en}" data-zh="{zh}">{en}</a>'


def build_nav(current: str) -> str:
    active = current
    parts = [
        '<nav class="mf-side-links mf-trig-toc">',
        '<p class="mf-trig-toc-title" data-en="Trigonometry" data-zh="三角学">Trigonometry</p>',
    ]
    for href, en, zh in SIDEBAR_LEVEL2:
        is_current = href == active or href == current
        parts.append(
            f'<div class="mf-trig-toc-parent">{link_html(href, en, zh, current=is_current)}</div>'
        )
    parts.append(BACK)
    parts.append("</nav>")
    return "".join(parts)


def inject_css(text: str) -> str:
    if 'id="trig-toc-sidebar"' in text:
        text = re.sub(
            r'<style id="trig-toc-sidebar">.*?</style>',
            TOC_CSS.strip(),
            text,
            count=1,
            flags=re.DOTALL,
        )
        return text
    return text.replace("</head>", TOC_CSS + "\n</head>", 1)


def main() -> None:
    aside_pat = re.compile(
        r'<aside aria-label="Topic navigation" class="mf-sidebar">.*?</aside>',
        re.DOTALL,
    )
    for href in all_sync_pages():
        path = MATH / href
        if not path.is_file():
            print("skip missing", href)
            continue
        text = path.read_text(encoding="utf-8")
        text = inject_css(text)
        new_aside = f'<aside aria-label="Topic navigation" class="mf-sidebar">{build_nav(href)}</aside>'
        if not aside_pat.search(text):
            print("no sidebar", href)
            continue
        text = aside_pat.sub(new_aside, text, count=1)
        path.write_text(text, encoding="utf-8")
        print("updated", href)


if __name__ == "__main__":
    main()
