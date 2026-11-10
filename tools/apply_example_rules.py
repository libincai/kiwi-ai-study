#!/usr/bin/env python3
"""Apply DESIGN_STANDARDS worked-example markup to HTML pages.

After bulk edits, run ``python tools/audit_example_layout.py`` to catch
single-item ``kiwi-example-steps`` lists and multi-line ``kiwi-example-list``
bullets missing step/answer classes (see DESIGN_STANDARDS.md).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCKQUOTE_SEL_OLD = ".mf-article blockquote{border-left:4px solid #1768b2"
BLOCKQUOTE_SEL_NEW = ".mf-article blockquote:not(.kiwi-example-answer){border-left:4px solid #1768b2"


def strip_strong(s: str) -> str:
    return re.sub(r"</?strong>", "", s, flags=re.I)


def add_class_to_p(tag: str, class_name: str) -> str:
    if re.search(r'\bclass="', tag):
        return re.sub(r'\bclass="([^"]*)"', rf'class="{class_name} \1"', tag, count=1)
    return tag.replace("<p ", f'<p class="{class_name}" ', 1)


def unbold_answer_blockquotes(html: str) -> str:
    def fix(m: re.Match[str]) -> str:
        body = strip_strong(m.group(1))
        cls = m.group(0)
        if 'class="kiwi-example-answer"' not in cls:
            return f'<blockquote class="kiwi-example-answer">{body}</blockquote>'
        return f'<blockquote class="kiwi-example-answer">{body}</blockquote>'

    html = re.sub(
        r'<blockquote class="kiwi-example-answer">\s*(.*?)\s*</blockquote>',
        fix,
        html,
        flags=re.DOTALL,
    )
    # Conclusion blockquotes in example blocks (Therefore / ∴)
    html = re.sub(
        r'(<div class="kiwi-example-block kiwi-example-standard">[\s\S]*?)<blockquote>\s*(<p[^>]*>(?:\s*(?:Therefore|∴)[\s\S]*?)</p>)\s*</blockquote>',
        lambda m: m.group(1)
        + '<blockquote class="kiwi-example-answer">'
        + strip_strong(m.group(2))
        + "</blockquote>",
        html,
    )
    return html


def convert_example_blocks(html: str) -> str:
    """Convert legacy Example blockquote + ul patterns."""
    if "kiwi-example-block kiwi-example-standard" in html and html.count(
        '<p data-en="Example:"'
    ) == html.count('<div class="kiwi-example-block kiwi-example-standard">'):
        # May still need ul conversions inside partial files
        pass

    # Examples: + blockquote + optional ul (single worked example)
    html = re.sub(
        r'<p data-en="Examples:"([^>]*)>Examples:</p>\s*<blockquote>\s*(<p[\s\S]*?</p>)\s*</blockquote>\s*<ul>',
        lambda m: (
            f'<p data-en="Example:"{m.group(1)}>Example:</p>\n'
            f'<div class="kiwi-example-block kiwi-example-standard">\n'
            f"{add_class_to_p(m.group(2), 'kiwi-single-example')}\n"
            f'<ol class="kiwi-example-steps kiwi-numbered-steps">'
        ),
        html,
        count=0,
    )

    # Example: + blockquote + ul (worked)
    def worked_open(m: re.Match[str]) -> str:
        p_tag = m.group(2)
        return (
            f"{m.group(1)}<div class=\"kiwi-example-block kiwi-example-standard\">\n"
            f"{add_class_to_p(p_tag, 'kiwi-single-example')}"
        )

    html = re.sub(
        r'(<p data-en="Example:"[^>]*>Example:</p>\s*)<blockquote>\s*(<p[^>]*>)',
        worked_open,
        html,
    )

    html = re.sub(
        r"</p>\s*</blockquote>\s*<ul>",
        "</p>\n<ol class=\"kiwi-example-steps kiwi-numbered-steps\">",
        html,
    )
    html = re.sub(r"</ul>\s*<blockquote>", "</ol>\n<blockquote class=\"kiwi-example-answer\">", html)

    # Example: + lone blockquote (no list)
    def simple_open(m: re.Match[str]) -> str:
        return (
            f"{m.group(1)}<div class=\"kiwi-example-block kiwi-example-standard\">\n"
            f"{add_class_to_p(m.group(2), 'kiwi-single-example')}"
        )

    html = re.sub(
        r'(<p data-en="Example:"[^>]*>Example:</p>\s*)<blockquote>\s*(<p[^>]*>)',
        simple_open,
        html,
    )
    html = re.sub(
        r"(<p class=\"kiwi-single-example\"[^>]*>[\s\S]*?</p>)\s*</blockquote>(\s*<h[1-6])",
        r"\1</div>\2",
        html,
    )

    # Close div after answer blockquote
    html = re.sub(
        r"(<blockquote class=\"kiwi-example-answer\">[\s\S]*?</blockquote>)(\s*<h[1-6])",
        r"\1\n</div>\2",
        html,
    )
    html = re.sub(
        r"(<blockquote class=\"kiwi-example-answer\">[\s\S]*?</blockquote>)(\s*</article>)",
        r"\1\n</div>\2",
        html,
    )

    # Examples: single blockquote, no ul
    html = re.sub(
        r'<p data-en="Examples:"([^>]*)>Examples:</p>\s*<blockquote>\s*(<p[\s\S]*?</p>)\s*</blockquote>',
        lambda m: (
            f'<p data-en="Example:"{m.group(1)}>Example:</p>\n'
            f'<div class="kiwi-example-block kiwi-example-standard">\n'
            f"{add_class_to_p(m.group(2), 'kiwi-single-example')}\n</div>"
        ),
        html,
    )

    # Bullet list under Examples: (short items)
    html = re.sub(
        r'(<p data-en="Examples:"[^>]*>Examples:</p>\s*)<ul>',
        r'\1<ul class="kiwi-example-list">',
        html,
    )

    # ol steps: flatten li>p to li when trivial
    html = re.sub(
        r"<li>\s*<p([^>]*)>([\s\S]*?)</p>\s*</li>",
        r"<li\1>\2</li>",
        html,
    )

    return unbold_answer_blockquotes(html)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    if BLOCKQUOTE_SEL_OLD in text and ":not(.kiwi-example-answer)" not in text:
        text = text.replace(BLOCKQUOTE_SEL_OLD, BLOCKQUOTE_SEL_NEW)

    if "mf-article" in text or "kiwi-topic-article" in text:
        text = convert_example_blocks(text)

    # Topic pages: Example blockquote without mf-article blockquote selector
    text = re.sub(
        r'(<p data-en="Examples:"[^>]*>Examples:</p>\s*)<blockquote>\s*<p ',
        r'<p data-en="Example:" data-zh="示例：">Example:</p>\n<div class="kiwi-example-block kiwi-example-standard"><p class="kiwi-single-example" ',
        text,
    )
    text = re.sub(
        r'(<p data-en="Example:"[^>]*>Example:</p>\s*)<blockquote>\s*<p ',
        r'\1<div class="kiwi-example-block kiwi-example-standard"><p class="kiwi-single-example" ',
        text,
    )
    text = re.sub(
        r'(<p class="kiwi-single-example"[^>]*>[\s\S]*?</p>)\s*</blockquote>(\s*<h)',
        r"\1</div>\2",
        text,
        flags=re.DOTALL,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    math = ROOT / "math"
    files = sorted({f.resolve() for f in math.glob("*.html") if f.is_file()})

    changed = []
    for f in files:
        if process_file(f):
            changed.append(f.relative_to(ROOT))

    # patch kiwi-example-answer font-weight in embedded styles
    fw_old = "> blockquote.kiwi-example-answer p {margin:0!important;}"
    fw_new = "> blockquote.kiwi-example-answer p,.kiwi-topic-article .kiwi-example-standard > blockquote.kiwi-example-answer strong {margin:0!important;font-weight:400!important;}"
    for f in files:
        t = f.read_text(encoding="utf-8")
        if fw_old in t and fw_new not in t:
            f.write_text(t.replace(fw_old, fw_new), encoding="utf-8")
            if f.relative_to(ROOT) not in changed:
                changed.append(f.relative_to(ROOT))

    print(f"Updated {len(changed)} files")
    for c in changed:
        print(c)
    return 0


def fix_missing_answer_close() -> int:
    pat = re.compile(
        r'(<blockquote class="kiwi-example-answer">.*?<p[^>]*>.*?</p>)\s*</div>',
        re.DOTALL,
    )
    n = 0
    for f in (ROOT / "math").glob("*.html"):
        t = f.read_text(encoding="utf-8")
        if "kiwi-example-answer" not in t:
            continue
        u = pat.sub(r"\1</blockquote></div>", t)
        if u != t:
            f.write_text(u, encoding="utf-8")
            n += 1
    print(f"fixed missing </blockquote> in {n} files")
    return n


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fix-close":
        sys.exit(0 if fix_missing_answer_close() >= 0 else 1)
    sys.exit(main())
