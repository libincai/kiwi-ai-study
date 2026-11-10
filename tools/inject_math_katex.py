#!/usr/bin/env python3
"""Add KaTeX + kiwi-math-katex.js to HTML files that contain <math>, and hook language toggle."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KATEX_CSS = '<link href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" rel="stylesheet"/>'
KATEX_JS = '<script defer crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>'
KIWI_JS = '<script defer src="{prefix}assets/js/kiwi-math-katex.js?v=2"></script>'
HOOK = "if (window.kiwiRenderAllMath) window.kiwiRenderAllMath();"

MARKER_CSS = "katex.min.css"
MARKER_JS = "kiwi-math-katex.js"


def asset_prefix(html_path: Path) -> str:
    rel = html_path.parent.relative_to(ROOT)
    depth = len(rel.parts)
    return "../" * depth if depth else "./"


def has_math(text: str) -> bool:
    return "<math" in text.lower()


def inject_css(text: str) -> str:
    if MARKER_CSS in text:
        return text
    m = re.search(r"<link[^>]+styles\.css[^>]*>", text, re.I)
    if m:
        insert = m.end()
        return text[:insert] + "\n" + KATEX_CSS + text[insert:]
    m = re.search(r"</head>", text, re.I)
    if m:
        return text[: m.start()] + KATEX_CSS + "\n" + text[m.start() :]
    return text


def inject_js(text: str, prefix: str) -> str:
    kiwi = KIWI_JS.format(prefix=prefix)
    has_katex = "katex.min.js" in text
    has_kiwi = MARKER_JS in text
    parts = []
    if not has_katex:
        parts.append(KATEX_JS)
    if not has_kiwi:
        parts.append(kiwi)
    if not parts:
        return text
    bundle = "\n".join(parts)
    if "drive-breadcrumb.js" in text:
        return text.replace(
            '<script defer="" src="',
            bundle + "\n" + '<script defer="" src="',
            1,
        ).replace(
            '<script defer src="',
            bundle + "\n" + '<script defer src="',
            1,
        )
    m = re.search(r"</body>", text, re.I)
    if m:
        return text[: m.start()] + bundle + "\n" + text[m.start() :]
    return text + bundle


def hook_language(text: str) -> str:
    if HOOK in text:
        return text
    patterns = [
        r"(try\s*\{\s*localStorage\.setItem\('kiwi-site-language',\s*l\);\s*\}\s*catch\s*\(e\)\s*\{\s*\})",
        r'(try\s*\{\s*localStorage\.setItem\("kiwi-site-language",\s*l\);\s*\}\s*catch\s*\(e\)\s*\{\s*\})',
    ]
    for pat in patterns:
        if re.search(pat, text):

            def repl(m: re.Match[str]) -> str:
                return m.group(1) + "\n    " + HOOK

            return re.sub(pat, repl, text, count=1)
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not has_math(text):
        return False
    original = text
    prefix = asset_prefix(path)
    text = inject_css(text)
    text = inject_js(text, prefix)
    text = hook_language(text)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if process_file(path):
            changed.append(path.relative_to(ROOT))
    print(f"Updated {len(changed)} HTML file(s)")
    for p in changed:
        print(f"  {p}")


if __name__ == "__main__":
    main()
