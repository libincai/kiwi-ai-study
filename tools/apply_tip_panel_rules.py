#!/usr/bin/env python3
"""Apply sitewide tip-panel markup and CSS hygiene (see assets/css/styles.css)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT / "math"
CSS_V = "20261110-tip-panels"

PANEL_RE = re.compile(
    r"(<aside\s+class=\"kiwi-(?:word-info|insight)-panel\"[^>]*>)(.*?)(</aside>)",
    re.DOTALL,
)
HEADING_RE = re.compile(
    r"<div class=\"kiwi-(?:panel-heading|insight-header|word-info-header)\"[^>]*>.*?</div>",
    re.DOTALL,
)
INLINE_LAYOUT_LINES = [
    re.compile(
        r"\.kiwi-word-info-panel\s+\.kiwi-panel-heading\{display:flex[^}]+\}\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\.kiwi-topic-article\s+\.kiwi-insight-header\{display:flex[^}]+\}\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\.kiwi-(?:insight-header|word-info-header)\{display:flex[^}]+\}\s*",
        re.IGNORECASE,
    ),
]
STYLES_LINK_RE = re.compile(
    r"(href=\"\.\./assets/css/styles\.css\?v=)[^\"]+(\" )",
)


def needs_content_wrap(after: str) -> bool:
    s = after.strip()
    if not s:
        return False
    if s.startswith('<div class="kiwi-word-info-body') or s.startswith(
        '<div class="kiwi-insight-body"'
    ):
        return False
    if s.startswith("<p") or s.startswith("<ul") or s.startswith("<ol"):
        return False
    if s.startswith("<strong>") and s.endswith("</strong>") and s.count("<") <= 2:
        return False
    if "<p" in s[:80]:
        return False
    return True


def fix_panel_inner(inner: str) -> tuple[str, bool]:
    hm = HEADING_RE.search(inner)
    if not hm:
        return inner, False
    after = inner[hm.end() :]
    if not needs_content_wrap(after):
        return inner, False
    wrapped = inner[: hm.end()] + '<div class="kiwi-panel-content">' + after + "</div>"
    return wrapped, True


def process_html(text: str) -> tuple[str, dict[str, int]]:
    stats = {"panels_wrapped": 0, "dup_aside_fixed": 0, "inline_css_removed": 0}
    if "</aside></aside>" in text:
        text = text.replace("</aside></aside>", "</aside>")
        stats["dup_aside_fixed"] += text.count("</aside></aside>")  # unlikely after replace

    def sub_panel(m: re.Match[str]) -> str:
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        new_inner, changed = fix_panel_inner(inner)
        if changed:
            stats["panels_wrapped"] += 1
        return open_tag + new_inner + close

    text = PANEL_RE.sub(sub_panel, text)

    removed = 0
    for pat in INLINE_LAYOUT_LINES:
        text, n = pat.subn("", text)
        removed += n
    stats["inline_css_removed"] = removed

    if 'href="../assets/css/styles.css' in text:
        text = STYLES_LINK_RE.sub(rf"\g<1>{CSS_V}\2", text)

    return text, stats


def main() -> int:
    total = {"files": 0, "panels_wrapped": 0, "dup_aside_fixed": 0, "inline_css_removed": 0}
    for path in sorted(MATH.glob("*.html")):
        raw = path.read_text(encoding="utf-8")
        if "kiwi-word-info-panel" not in raw and "kiwi-insight-panel" not in raw:
            continue
        new, stats = process_html(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8", newline="\n")
            total["files"] += 1
            for k in stats:
                total[k] = total.get(k, 0) + stats[k]
    print(
        f"Updated {total['files']} files; "
        f"wrapped {total.get('panels_wrapped', 0)} panels; "
        f"removed {total.get('inline_css_removed', 0)} inline layout rules; "
        f"dup aside fixes {total.get('dup_aside_fixed', 0)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
