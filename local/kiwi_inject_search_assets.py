"""Inject kiwi-site-search.js before </body> on all public HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"local", "templates", "tools", "docs", "scripts", ".cursor", ".github", "pagefind", "node_modules"}
MARKER = "kiwi-site-search.js"
VERSION = "20261114-search20"
BASE_MARKER = "kiwi-site-base.js"
BASE_VERSION = "20261116-customdomain"
BACK_TO_TOP_MARKER = "kiwi-back-to-top.js"
BACK_TO_TOP_VERSION = "20261118-thinking"
CF_BEACON_MARKER = "static.cloudflareinsights.com/beacon.min.js"
CLOUDFLARE_ANALYTICS = """<!-- Cloudflare Web Analytics -->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "1e1bdfca980f4ec293ede3cb0483adfc"}'></script>
<!-- End Cloudflare Web Analytics -->"""

SEARCH_BTN = (
    '<button type="button" class="kiwi-search-open" data-kiwi-search-trigger '
    'aria-label="Search site">'
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>'
    '<path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '</svg></button>'
)


def depth(rel: str) -> int:
    return rel.count("/")


def asset_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def script_tag(depth: int) -> str:
    prefix = asset_prefix(depth)
    return (
        f'<link href="{prefix}pagefind/pagefind-ui.css" rel="stylesheet"/>\n'
        f'<script defer src="{prefix}assets/js/kiwi-site-search.js?v={VERSION}"></script>'
    )


def base_script_tag(depth: int) -> str:
    prefix = asset_prefix(depth)
    return f'<script src="{prefix}assets/js/{BASE_MARKER}?v={BASE_VERSION}"></script>'


def favicon_tags(depth: int) -> str:
    prefix = asset_prefix(depth)
    return (
        f'<link rel="icon" href="{prefix}favicon.ico" sizes="any">\n'
        f'<link rel="icon" type="image/png" sizes="32x32" '
        f'href="{prefix}favicon-32x32.png">\n'
        f'<link rel="icon" type="image/png" sizes="16x16" '
        f'href="{prefix}favicon-16x16.png">\n'
        f'<link rel="apple-touch-icon" sizes="180x180" '
        f'href="{prefix}apple-touch-icon.png">'
    )


def inject_favicon(text: str, depth: int) -> tuple[str, bool]:
    tags = favicon_tags(depth)
    text = re.sub(
        r'<link[^>]+\brel=["\'](?:shortcut )?icon["\'][^>]*>\s*',
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'<link[^>]+\brel=["\']apple-touch-icon["\'][^>]*>\s*',
        "",
        text,
        flags=re.I,
    )
    if "favicon-32x32.png" in text and "apple-touch-icon.png" in text:
        return text, False
    quoted = r'(<meta\s+charset\s*=\s*["\'][^"\']+["\']\s*/?>)'
    m = re.search(quoted, text, re.I)
    if not m:
        m = re.search(r"(<meta\s+charset[^>]*>)", text, re.I)
    if not m:
        return text, False
    anchor = m.group(1)
    new = text.replace(anchor, anchor + "\n" + tags, 1)
    return new, new != text


def inject_cloudflare_analytics(text: str) -> tuple[str, bool]:
    if CF_BEACON_MARKER in text:
        return text, False
    if not re.search(r"</head>", text, re.I):
        return text, False
    new = re.sub(
        r"</head>",
        CLOUDFLARE_ANALYTICS + "\n</head>",
        text,
        count=1,
        flags=re.I,
    )
    return new, new != text


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


def back_to_top_tag(depth: int) -> str:
    prefix = asset_prefix(depth)
    return (
        f'<script defer src="{prefix}assets/js/{BACK_TO_TOP_MARKER}?v={BACK_TO_TOP_VERSION}"></script>'
    )


def inject_site_base(text: str, depth: int) -> tuple[str, bool]:
    tag = base_script_tag(depth)
    if BASE_MARKER in text:
        new = re.sub(
            rf'<script src="(?:/|(?:\.\./)*)?assets/js/{re.escape(BASE_MARKER)}\?v=[^"]+"></script>',
            tag,
            text,
            count=1,
        )
        return new, new != text
    if not re.search(r"</head>", text, re.I):
        return text, False
    new = re.sub(r"</head>", tag + "\n</head>", text, count=1, flags=re.I)
    return new, True


def page_uses_back_to_top(text: str) -> bool:
    if "foundation-level4" in text:
        return True
    return "kiwi-learning-layout" in text and "kiwi-topic-article" in text


def inject_back_to_top(text: str, depth: int) -> tuple[str, bool]:
    if not page_uses_back_to_top(text):
        return text, False
    tag = back_to_top_tag(depth)
    rel_src = f'{asset_prefix(depth)}assets/js/{BACK_TO_TOP_MARKER}?v={BACK_TO_TOP_VERSION}'
    if BACK_TO_TOP_MARKER in text:
        new = text
        new = re.sub(
            rf'src="(?:/|(?:\.\./)*)?assets/js/{re.escape(BACK_TO_TOP_MARKER)}\?v=[^"]+"',
            f'src="{rel_src}"',
            new,
            count=1,
        )
        return new, new != text
    if not re.search(r"</body>", text, re.I):
        return text, False
    new = re.sub(r"</body>", tag + "\n</body>", text, count=1, flags=re.I)
    return new, True


def is_github_redirect_stub(path: Path, text: str) -> bool:
    if path.name != "index.html":
        return False
    try:
        rel_parts = path.relative_to(ROOT).parts
    except ValueError:
        return False
    if len(rel_parts) != 2:
        return False
    return "data-pagefind-ignore" in text and 'http-equiv="refresh"' in text


def inject(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    d = depth(rel)
    text = path.read_text(encoding="utf-8")
    if is_github_redirect_stub(path, text):
        return False
    if "<html" not in text.lower():
        return False
    original = text

    text = inject_header_button(text)
    text, _ = inject_favicon(text, d)
    text, _ = inject_cloudflare_analytics(text)
    text, _ = inject_site_base(text, d)
    text, _ = inject_back_to_top(text, d)

    if MARKER in text:
        text = re.sub(
            r'<script type="module" src="([^"]*kiwi-site-search\.js[^"]*)"',
            r'<script defer src="\1"',
            text,
            count=1,
        )
        text = re.sub(
            r"kiwi-site-search\.js\?v=[^\"']+",
            f"kiwi-site-search.js?v={VERSION}",
            text,
            count=1,
        )
    else:
        if not re.search(r"</body>", text, re.I):
            return False
        text = re.sub(r"</body>", script_tag(d) + "\n</body>", text, count=1, flags=re.I)
        text, _ = inject_back_to_top(text, d)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    cf = 0
    skip_stub = 0
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if is_github_redirect_stub(path, text):
            skip_stub += 1
            continue
        if "<html" not in text.lower():
            continue
        had_cf = CF_BEACON_MARKER in text
        if inject(path):
            n += 1
        after = path.read_text(encoding="utf-8")
        if CF_BEACON_MARKER in after and not had_cf:
            cf += 1
    print(
        "updated",
        n,
        "html files; cloudflare analytics added to",
        cf,
        "pages;",
        skip_stub,
        "redirect stubs skipped",
    )


if __name__ == "__main__":
    main()