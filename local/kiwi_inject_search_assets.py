"""Inject kiwi-site-search.js before </body> on all public HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"local", "templates", "tools", "docs", "scripts", ".cursor", ".github", "pagefind", "node_modules"}
MARKER = "kiwi-site-search.js"
VERSION = "20261114-search20"
BACK_TO_TOP_MARKER = "kiwi-back-to-top.js"
BACK_TO_TOP_VERSION = "20261115d"
SEARCH_BTN = (
    '<button type="button" class="kiwi-search-open" data-kiwi-search-trigger '
    'aria-label="Search site">'
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>'
    '<path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    "</svg></button>"
)


def depth(rel: str) -> int:
    return rel.count("/")


def script_tag(depth: int) -> str:
    prefix = "../" * depth if depth else ""
    return (
        f'<link href="{prefix}pagefind/pagefind-ui.css" rel="stylesheet"/>\n'
        f'<script defer src="{prefix}assets/js/kiwi-site-search.js?v={VERSION}"></script>'
    )


def inject_header_button(text: str) -> str:
    if "data-kiwi-search-trigger" in text:
        return text
    needle = '<span aria-label="Languages" class="flags">'
    alt = '<span class="flags" aria-label="Languages">'
    if needle in text:
        return text.replace(needle, SEARCH_BTN + "\n" + needle, 1)
    if alt in text:
        return text.replace(alt, SEARCH_BTN + "\n" + alt, 1)
    return text


def back_to_top_tag(_depth: int) -> str:
    return (
        f'<script defer src="/assets/js/{BACK_TO_TOP_MARKER}?v={BACK_TO_TOP_VERSION}"></script>'
    )


def inject_back_to_top(text: str, depth: int) -> tuple[str, bool]:
    if "foundation-level4" not in text:
        return text, False
    tag = back_to_top_tag(depth)
    if BACK_TO_TOP_MARKER in text:
        new = text
        new = re.sub(
            rf'src="(?:/|(?:\.\./)*)?assets/js/{re.escape(BACK_TO_TOP_MARKER)}\?v=[^"]+"',
            f'src="/assets/js/{BACK_TO_TOP_MARKER}?v={BACK_TO_TOP_VERSION}"',
            new,
            count=1,
        )
        return new, new != text
    if not re.search(r"</body>", text, re.I):
        return text, False
    new = re.sub(r"</body>", tag + "\n</body>", text, count=1, flags=re.I)
    return new, True


def inject(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    changed = False
    new_text = inject_header_button(text)
    if new_text != text:
        text = new_text
        changed = True
    text, btt_changed = inject_back_to_top(text, depth(rel))
    if btt_changed:
        changed = True
    if MARKER in text:
        text = re.sub(
            r'<script type="module" src="([^"]*kiwi-site-search\.js[^"]*)"',
            rf'<script defer src="\1"',
            text,
            count=1,
        )
        text = re.sub(
            r"kiwi-site-search\.js\?v=[^\"']+",
            f"kiwi-site-search.js?v={VERSION}",
            text,
            count=1,
        )
        if changed or text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
            return True
        return False
    if "<html" not in text.lower():
        return False
    tag = script_tag(depth(rel))
    if not re.search(r"</body>", text, re.I):
        return False
    text = re.sub(r"</body>", tag + "\n</body>", text, count=1, flags=re.I)
    text, _ = inject_back_to_top(text, depth(rel))
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if inject(path):
            n += 1
    print("injected search assets on", n, "files")


if __name__ == "__main__":
    main()