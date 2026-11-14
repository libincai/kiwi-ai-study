"""Annotate public HTML for Pagefind (section, breadcrumbs, zh mirror, redirects)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    "local",
    "templates",
    "tools",
    "docs",
    "scripts",
    ".cursor",
    ".github",
    "pagefind",
    "node_modules",
    "assets",
}

SECTION_MAP = [
    ("math/", "math"),
    ("ai/", "ai"),
    ("books/", "books"),
    ("about/", "about"),
    ("legal/", "legal"),
    ("contact/", "contact"),
]

MARKER_ZH = "<!-- kiwi-search-zh-index -->"
MARKER_PREP = "<!-- kiwi-search-prepared -->"


def section_for(rel: str) -> str:
    if rel in ("index.html",):
        return "home"
    for prefix, name in SECTION_MAP:
        if rel.startswith(prefix):
            return name
    return "site"


def breadcrumb_en(rel: str, title: str) -> str:
    parts = []
    if rel == "index.html":
        return "Home"
    if rel.startswith("math/"):
        parts.append("Math")
        if rel == "math/index.html":
            return "Math Education"
        if rel == "math/math-foundations.html":
            return "Math › Math Foundations"
        stem = Path(rel).stem
        if stem.startswith("foundation-"):
            parts.append("Foundations")
        parts.append(title or stem.replace("-", " ").title())
        return " › ".join(parts[:3])
    if rel.startswith("ai/"):
        if rel == "ai/index.html":
            return "AI Education"
        if rel.startswith("ai/episode-"):
            return f"AI › {title or 'Episode'}"
        return f"AI › {title or Path(rel).stem}"
    if rel.startswith("books/"):
        return f"Books › {title or Path(rel).stem}"
    return title or "Kiwi 爱AI Study"


def extract_title(text: str) -> str:
    m = re.search(r"<title[^>]*>([^<]+)</title>", text, re.I)
    if not m:
        return ""
    t = re.sub(r"\s*\|\s*KIWI.*$", "", m.group(1), flags=re.I)
    return html.unescape(t.strip())


def extract_h1_en(text: str) -> str:
    m = re.search(
        r"<h1[^>]*\bdata-en=\"([^\"]+)\"",
        text,
        re.I,
    )
    if m:
        return html.unescape(m.group(1))
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", text, re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def extract_h1_zh(text: str) -> str:
    m = re.search(r"<h1[^>]*\bdata-zh=\"([^\"]+)\"", text, re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def extract_title_zh(text: str) -> str:
    m = re.search(r"<title[^>]*\bdata-zh=\"([^\"]+)\"", text, re.I)
    if m:
        return html.unescape(m.group(1).strip())
    m = re.search(r"<title[^>]*>([^<]+)</title>", text, re.I)
    if not m:
        return ""
    raw = html.unescape(m.group(1).strip())
    return re.sub(r"\s*\|\s*KIWI.*$", "", raw, flags=re.I).strip()


def breadcrumb_zh(rel: str, title: str) -> str:
    if rel == "index.html":
        return "首页"
    if rel.startswith("math/"):
        if rel == "math/index.html":
            return "数学教育"
        if rel == "math/math-foundations.html":
            return "数学 › 数学基础"
        stem = Path(rel).stem
        if stem.startswith("foundation-"):
            return f"数学 › 三角学 › {title}" if "trig" in stem else f"数学 › 数学基础 › {title}"
        if "trig" in rel or "foundation-" in rel:
            return f"数学 › 三角学 › {title}"
        return f"数学 › {title or Path(rel).stem}"
    if rel.startswith("ai/"):
        if rel == "ai/index.html":
            return "人工智能教育"
        if rel.startswith("ai/episode-"):
            return f"人工智能 › {title or '课程'}"
        return f"人工智能 › {title or Path(rel).stem}"
    if rel.startswith("books/"):
        return f"书籍 › {title or Path(rel).stem}"
    return title or "Kiwi 爱AI Study"


def main_html_scope(text: str) -> str:
    m = re.search(r"<main\b[^>]*>.*?</main>", text, re.I | re.DOTALL)
    if m:
        return m.group(0)
    m = re.search(r'class="[^"]*mf-article[^"]*"', text, re.I)
    if m:
        start = text.rfind("<", 0, m.start())
        end = text.find("</article>", m.start())
        if start != -1 and end != -1:
            return text[start : end + len("</article>")]
    return text


def plain_text_for_index(raw: str) -> str:
    plain = html.unescape(raw)
    for _ in range(2):
        plain = re.sub(r"<math\b[^>]*>.*?</math>", " ", plain, flags=re.I | re.DOTALL)
    plain = re.sub(r"&lt;math\b[^&]*&gt;.*?&lt;/math&gt;", " ", plain, flags=re.I | re.DOTALL)
    plain = re.sub(
        r'<annotation[^>]*encoding="application/x-tex"[^>]*>([^<]*)</annotation>',
        r" \1 ",
        plain,
        flags=re.I,
    )
    plain = re.sub(r"&lt;annotation[^&]*&gt;([^&]*)&lt;/annotation&gt;", r" \1 ", plain, flags=re.I)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = re.sub(r"&lt;[^&]+&gt;", " ", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    return plain


def collect_data_zh(text: str) -> str:
    bits: list[str] = []
    scope = main_html_scope(text)

    def add(raw: str | None) -> None:
        if not raw:
            return
        plain = plain_text_for_index(raw)
        if plain and plain not in bits:
            bits.append(plain)

    for m in re.finditer(r"\bdata-zh=\"([^\"]*)\"", scope):
        add(m.group(1))
    acronyms = sorted(
        {m.group(0).upper() for m in re.finditer(r"\b(?:ASA|AAS|SSA|SAS|SSS)\b", scope, re.I)},
    )
    if acronyms:
        bits.append(" ".join(acronyms))
    return " ".join(bits[:400])


def make_zh_excerpt(zh_text: str, max_len: int = 220) -> str:
    plain = re.sub(r"\s+", " ", zh_text).strip()
    for marker in (
        "← 返回数学基础目录",
        "← 返回数学思维目录",
        "← 返回数学教育",
        "← 返回首页",
    ):
        if marker in plain:
            plain = plain.split(marker, 1)[-1].strip()
            break
    hub_leads = ("探索核心数学概念", "探索数的关系", "选择一个数学", "从校园、兴趣爱好")
    for lead in hub_leads:
        idx = plain.find(lead)
        if 0 <= idx < 100:
            end = plain.find("。", idx)
            if end > idx:
                plain = plain[end + 1 :].strip()
            break
    if len(plain) > max_len:
        plain = plain[: max_len - 1].rstrip("，、； ") + "…"
    return plain


def is_redirect_stub(text: str) -> bool:
    return "location.replace(" in text and 'class="edu-lead">This topic is part of' in text


def strip_old_blocks(text: str) -> str:
    text = re.sub(
        r"<!-- kiwi-search-zh-index -->.*?<!-- /kiwi-search-zh-index -->",
        "",
        text,
        flags=re.DOTALL,
    )
    return text


def prepare_file(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    if "<html" not in text.lower():
        return False

    changed = False
    title = extract_h1_en(text) or extract_title(text)
    section = section_for(rel)
    crumb_en = breadcrumb_en(rel, title)

    if is_redirect_stub(text):
        if 'data-pagefind-ignore="all"' not in text:
            text = re.sub(
                r"<body([^>]*)>",
                r'<body\1 data-pagefind-ignore="all">',
                text,
                count=1,
                flags=re.I,
            )
            changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
        return changed

    if MARKER_PREP not in text:
        text = text.replace("<head>", f"<head>\n{MARKER_PREP}", 1)
        changed = True

    filter_attr = f"section:{section}"
    meta_crumb = html.escape(crumb_en, quote=True)
    if "data-pagefind-filter=" not in text:
        text = re.sub(
            r"<html([^>]*)>",
            f'<html\\1 data-pagefind-filter="{filter_attr}" data-pagefind-meta="breadcrumb:{meta_crumb}">',
            text,
            count=1,
            flags=re.I,
        )
        changed = True

    meta_block = (
        f'<meta name="pagefind:section" content="{section}" />\n'
        f'<meta name="pagefind:title_en" content="{html.escape(title)}" />\n'
        f'<meta name="pagefind:breadcrumb" content="{html.escape(crumb_en)}" />\n'
    )
    if 'name="pagefind:section"' not in text:
        text = text.replace(MARKER_PREP, f"{MARKER_PREP}\n{meta_block}", 1)
        changed = True
    if 'name="pagefind:title_en"' not in text and 'name="pagefind:section"' in text:
        text = text.replace(
            '<meta name="pagefind:section"',
            f'<meta name="pagefind:title_en" content="{html.escape(title)}" />\n<meta name="pagefind:section"',
            1,
        )
        changed = True

    if "<main" in text:
        if "data-pagefind-body" not in text:
            text = re.sub(
                r"<main(\s)",
                r'<main data-pagefind-body="" data-pagefind-filter="lang:en" \1',
                text,
                count=1,
                flags=re.I,
            )
            changed = True
        elif 'data-pagefind-filter="lang:en"' not in text:
            text2, n = re.subn(
                r"(<main[^>]*\bdata-pagefind-body=\"\")",
                r'\1 data-pagefind-filter="lang:en"',
                text,
                count=1,
                flags=re.I,
            )
            if n:
                text = text2
                changed = True

    zh_text = collect_data_zh(text)
    title_zh = extract_h1_zh(text) or extract_title_zh(text) or title
    crumb_zh = breadcrumb_zh(rel, title_zh)
    excerpt_zh = make_zh_excerpt(zh_text)
    zh_block = (
        f"{MARKER_ZH}\n"
        f'<div class="kiwi-pagefind-zh" hidden aria-hidden="true" data-pagefind-lang="zh" '
        f'data-pagefind-body="" data-pagefind-filter="lang:zh">'
        f'<span hidden data-pagefind-meta="title_zh">{html.escape(title_zh)}</span>'
        f'<span hidden data-pagefind-meta="breadcrumb_zh">{html.escape(crumb_zh)}</span>'
        f'<span hidden data-pagefind-meta="excerpt_zh">{html.escape(excerpt_zh)}</span>'
        f"{html.escape(zh_text)}"
        f"</div>\n<!-- /kiwi-search-zh-index -->"
    )
    text = strip_old_blocks(text)
    if zh_text:
        idx = text.lower().rfind("</body>")
        if idx != -1:
            text = text[:idx] + zh_block + "\n" + text[idx:]
            changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    n = 0
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if prepare_file(path):
            n += 1
            print("prepared", path.relative_to(ROOT))
    print("done,", n, "files updated")


if __name__ == "__main__":
    main()