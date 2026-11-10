#!/usr/bin/env python3
"""Normalize application/x-tex in foundation-rational-exponents.html for KaTeX."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "math" / "foundation-rational-exponents.html"

SUPER_CHARS = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿᵐᵖ")
SUPER_MAP = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁺": "+",
    "⁻": "-",
    "ⁿ": "n",
    "ᵐ": "m",
    "ᵖ": "p",
}


def unicode_supers_to_tex(tex: str) -> str:
    def repl(m: re.Match[str]) -> str:
        inner = "".join(SUPER_MAP.get(c, c) for c in m.group(0))
        return "^{" + inner + "}"

    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿᵐᵖ]+", repl, tex)


def normalize_tex_string(tex: str) -> str:
    t = unicode_supers_to_tex(tex)
    t = t.replace("\\sqrt{\\phantom{x}}", "\\sqrt{\\vphantom{1}}")
    t = t.replace("( - ", "(-")
    t = re.sub(r"\\frac\{a\^{m}\}\{a\^{n\}\}", r"\\frac{a^{m}}{a^{n}}", t)
    return t


def fix_annotation_block(match: re.Match[str]) -> str:
    inner = match.group(1)
    fixed = normalize_tex_string(inner)
    if fixed == inner:
        return match.group(0)
    return match.group(0).replace(inner, fixed, 1)


def wrap_display_paragraphs(html: str) -> str:
    """<p> with only <math display=\"block\"> → div.kiwi-math-block."""

    def repl(m: re.Match[str]) -> str:
        math = m.group(1)
        return f'<div class="kiwi-math-block">{math}</div>'

    return re.sub(
        r'<p(?:\s[^>]*)?>\s*(<math\s+display="block"[^>]*>[\s\S]*?</math>)\s*</p>',
        repl,
        html,
        flags=re.I,
    )


def table_display_to_inline(html: str) -> str:
    """Exponent laws table: compact inline KaTeX in cells."""
    start = html.find('<h3 id="laws-of-exponents"')
    end = html.find('<h3 id="concepts-roots-and-radicals"')
    if start < 0 or end < 0:
        return html
    chunk = html[start:end]
    chunk = chunk.replace('display="block"', 'display="inline"', 1)
    while 'display="block"' in chunk:
        chunk = chunk.replace('display="block"', 'display="inline"', 1)
    chunk = chunk.replace("&quot;block&quot;", "&quot;inline&quot;")
    return html[:start] + chunk + html[end:]


def fix_escaped_annotations(text: str) -> str:
    """data-en/data-zh contain escaped &lt;annotation ...&gt; blocks."""

    def repl(m: re.Match[str]) -> str:
        body = m.group(1)
        return (
            "&lt;annotation encoding=&quot;application/x-tex&quot;&gt;"
            + normalize_tex_string(body)
            + "&lt;/annotation&gt;"
        )

    return re.sub(
        r"&lt;annotation encoding=&quot;application/x-tex&quot;&gt;([\s\S]*?)&lt;/annotation&gt;",
        repl,
        text,
    )


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    text = re.sub(
        r'(<annotation\s+encoding="application/x-tex">)([\s\S]*?)(</annotation>)',
        lambda m: m.group(1) + normalize_tex_string(m.group(2)) + m.group(3),
        text,
    )
    text = fix_escaped_annotations(text)
    text = wrap_display_paragraphs(text)
    text = table_display_to_inline(text)
    text = text.replace("kiwi-math-katex.js?v=4", "kiwi-math-katex.js?v=8")
    PATH.write_text(text, encoding="utf-8")
    print(f"Updated {PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
