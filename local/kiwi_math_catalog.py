"""Math topic catalog: grade labels on pages + generated grade hub TOCs."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "math-topics.json"
MARKER_START = "<!-- kiwi-math-catalog:start -->"
MARKER_END = "<!-- kiwi-math-catalog:end -->"
META_START = "<!-- kiwi-math-catalog-meta -->"
META_END = "<!-- /kiwi-math-catalog-meta -->"


def load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def strip_catalog_blocks(text: str) -> str:
    text = re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\s*",
        "",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        re.escape(META_START) + r".*?" + re.escape(META_END) + r"\s*",
        "",
        text,
        flags=re.DOTALL,
    )
    return text


def grade_pills_block(grades: list[int], courses: list[str], hub_href: str) -> str:
    g = grades[0] if grades else ""
    grade_en = f"Grade {g}" if g else ""
    grade_zh = {9: "九年级", 10: "十年级", 11: "十一年级", 12: "十二年级"}.get(g, f"{g} 年级")
    course_pills = ""
    for c in courses:
        course_pills += (
            f'<span class="kiwi-grade-pill kiwi-grade-pill--course" '
            f'data-en="{html.escape(c)}" data-zh="{html.escape(c)}">{html.escape(c)}</span> '
        )
    hub_link = ""
    if hub_href:
        hub_link = (
            f'<a class="kiwi-grade-hub-link" href="{html.escape(hub_href, quote=True)}" '
            f'data-en="All Grade {g} topics →" data-zh="{html.escape(grade_zh)}全部主题 →">'
            f"All Grade {g} topics →</a>"
        )
    filters = " ".join(f"grade:{x}" for x in grades)
    return (
        f"{MARKER_START}\n"
        f'<div class="kiwi-grade-strip-wrap" data-pagefind-filter="{html.escape(filters)}">\n'
        f'  <p class="kiwi-grade-strip">\n'
        f'    <span class="kiwi-grade-pill" data-en="{html.escape(grade_en)}" '
        f'data-zh="{html.escape(grade_zh)}">{html.escape(grade_en)}</span>\n'
        f"    {course_pills}\n"
        f"    {hub_link}\n"
        f"  </p>\n"
        f"</div>\n"
        f"{MARKER_END}"
    )


def meta_block(grades: list[int]) -> str:
    gs = ",".join(str(x) for x in sorted(set(grades)))
    return (
        f"{META_START}\n"
        f'<meta name="pagefind:grades" content="{html.escape(gs)}" />\n'
        f"{META_END}"
    )


def inject_topic(path: Path, topic: dict, hub_href: str) -> bool:
    if not path.is_file():
        print("missing", path.relative_to(ROOT))
        return False
    text = path.read_text(encoding="utf-8")
    text = strip_catalog_blocks(text)
    block = grade_pills_block(topic.get("grades", []), topic.get("courses", []), hub_href)
    banner = re.search(
        r'<section[^>]*\bfoundation-topic-banner\b[^>]*>.*?</section>',
        text,
        flags=re.DOTALL | re.I,
    )
    if not banner:
        print("no banner", path.relative_to(ROOT))
        return False
    insert_at = banner.end()
    text = text[:insert_at] + "\n" + block + text[insert_at:]
    if META_START not in text:
        text = text.replace("<!-- kiwi-search-prepared -->", f"<!-- kiwi-search-prepared -->\n{meta_block(topic['grades'])}", 1)
    else:
        text = re.sub(
            re.escape(META_START) + r".*?" + re.escape(META_END),
            meta_block(topic["grades"]).strip(),
            text,
            flags=re.DOTALL,
        )
    path.write_text(text, encoding="utf-8")
    return True


def topic_href(slug: str) -> str:
    return f"{slug}.html"


GRADE_ZH = {9: "九年级", 10: "十年级", 11: "十一年级", 12: "十二年级"}


def grades_with_topics(catalog: dict) -> list[int]:
    found: set[int] = set()
    for t in catalog.get("topics", []):
        for g in t.get("grades", []):
            found.add(int(g))
    return sorted(found)


def chapters_for_grade(grade: int, catalog: dict) -> list[tuple[dict, list[dict]]]:
    topics = [t for t in catalog["topics"] if grade in t.get("grades", [])]
    chapters_dict = catalog.get("chapters", {})
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for t in topics:
        by_chapter[t.get("chapter_id", "misc")].append(t)
    ordered: list[tuple[int, dict, list[dict]]] = []
    for cid, items in by_chapter.items():
        items.sort(key=lambda x: x.get("sort", 0))
        ch = chapters_dict.get(
            cid,
            {"title_en": cid, "title_zh": cid, "order": 999},
        )
        ordered.append((ch.get("order", 999), ch, items))
    ordered.sort(key=lambda x: (x[0], x[1].get("title_en", "")))
    return [(ch, items) for _, ch, items in ordered]


def book_toc_html(grade: int, catalog: dict) -> str:
    parts = ['<nav class="kiwi-book-toc" aria-label="Table of contents">']
    for ch, items in chapters_for_grade(grade, catalog):
        te, tz = ch["title_en"], ch["title_zh"]
        parts.append('<section class="kiwi-book-chapter">')
        parts.append(
            f'<h2 class="kiwi-book-chapter-title" data-en="{html.escape(te)}" '
            f'data-zh="{html.escape(tz)}">{html.escape(te)}</h2>'
        )
        parts.append('<ol class="kiwi-book-topic-list">')
        for t in items:
            slug = Path(t["file"]).stem
            href = topic_href(slug)
            parts.append(
                f'<li><a href="{html.escape(href, quote=True)}" '
                f'data-en="{html.escape(t["title_en"])}" '
                f'data-zh="{html.escape(t["title_zh"])}">{html.escape(t["title_en"])}</a></li>'
            )
        parts.append("</ol></section>")
    parts.append("</nav>")
    return "\n".join(parts)


LANG_SCRIPT = r"""
<script>
(() => {
  const nav = { en: ['Home','About','Math Education','AI Education','In-Class Learning','My Books','Contact'], zh: ['首页','关于我们','数学教育','人工智能教育','课堂学习','我的书籍','联系我们'] };
  const legal = { en: ['Privacy Policy','Terms of Service','Home'], zh: ['隐私政策','服务条款','首页'] };
  const btns = document.querySelectorAll('.flag[data-language]');
  function setLanguage(lang) {
    const l = lang === 'zh' ? 'zh' : 'en';
    document.documentElement.lang = l === 'zh' ? 'zh-CN' : 'en-CA';
    document.querySelectorAll('[data-en][data-zh]').forEach(el => {
      el.innerHTML = el.getAttribute(l === 'zh' ? 'data-zh' : 'data-en');
    });
    document.querySelectorAll('.site-nav [data-nav]').forEach((el, i) => { el.textContent = nav[l][i]; });
    document.querySelectorAll('.site-footer [data-legal]').forEach((el, i) => { el.textContent = legal[l][i]; });
    btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.language === l)));
    try { localStorage.setItem('kiwi-site-language', l); } catch (e) {}
  }
  btns.forEach(b => b.addEventListener('click', () => setLanguage(b.dataset.language)));
  let saved = 'en';
  try { saved = localStorage.getItem('kiwi-site-language') || 'en'; } catch (e) {}
  setLanguage(saved);
  window.addEventListener('pageshow', () => {
    let l = 'en';
    try { l = localStorage.getItem('kiwi-site-language') || 'en'; } catch (e) {}
    setLanguage(l);
  });
})();
</script>
<script defer src="../assets/js/drive-breadcrumb.js?v=20261114-bcrumb2"></script>
<link href="../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer src="../assets/js/kiwi-site-search.js?v=20261114-search20"></script>
"""


def math_page_header(
    title_en: str,
    title_zh: str,
    description: str,
    pagefind_filter: str,
    pagefind_meta: str,
    pagefind_grades: str | None = None,
) -> str:
    grades_meta = ""
    if pagefind_grades:
        grades_meta = f'<meta name="pagefind:grades" content="{html.escape(pagefind_grades)}" />\n'
    return f"""<!DOCTYPE html>
<!-- Generated by local/kiwi_math_catalog.py — edit data/math-topics.json, not this file by hand. -->
<html lang="en-CA" {pagefind_filter} {pagefind_meta}>
<head>
<!-- kiwi-search-prepared -->
<meta name="pagefind:title_en" content="{html.escape(title_en)}" />
<meta name="pagefind:section" content="math" />
{grades_meta}<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{html.escape(description)}"/>
<title data-en="{html.escape(title_en)} | Kiwi 爱AI Study" data-zh="{html.escape(title_zh)} | Kiwi 爱AI Study">{html.escape(title_en)} | Kiwi 爱AI Study</title>
<link rel="stylesheet" href="../assets/css/styles.css?v=20261114-grade-nav"/>
</head>
<body class="edu-page topic-page">
<header class="site-header">
<div class="brand-lockup">
<a aria-label="Kiwi 爱AI Study home" class="logo-link" href="../index.html">
<img alt="Kiwi 爱AI Study logo" class="logo" src="../assets/logo/kiwi-ai-study-logo.webp"/>
</a>
<span aria-hidden="true" class="divider"></span>
<div class="author-wrap">
<a aria-label="Sherry Cai" class="author-image-link" href="../index.html">
<img alt="Sherry Cai" class="author-signature-image" src="../assets/logo/sherry-cai-signature.webp"/>
</a>
</div>
</div>
<nav aria-label="Primary" class="site-nav">
<a data-en="Home" data-nav="home" data-zh="首页" href="../index.html">Home</a>
<a data-en="About" data-nav="about" data-zh="关于我们" href="../about/index.html">About</a>
<a data-en="Math Education" data-nav="math" data-zh="数学教育" href="index.html">Math Education</a>
<a data-en="AI Education" data-nav="ai" data-zh="人工智能教育" href="../ai/index.html">AI Education</a>
<a data-en="In-Class Learning" data-nav="class" data-zh="课堂学习" href="in-class-learning.html">In-Class Learning</a>
<a data-en="My Books" data-nav="books" data-zh="我的书籍" href="../books/index.html">My Books</a>
<a data-en="Contact" data-nav="contact" data-zh="联系我们" href="../contact/index.html">Contact</a>
<button type="button" class="kiwi-search-open" data-kiwi-search-trigger aria-label="Search site"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
<span aria-label="Languages" class="flags">
<button aria-label="Switch to English" aria-pressed="true" class="flag" data-language="en" title="English" type="button">
<img alt="English" src="https://flagcdn.com/w160/ca.png"/>
</button>
<button aria-label="切换到中文" aria-pressed="false" class="flag" data-language="zh" title="中文" type="button">
<img alt="中文" src="https://flagcdn.com/w160/cn.png"/>
</button>
</span>
</nav>
</header>
"""


def math_page_footer() -> str:
    return f"""<footer class="site-footer">
<nav aria-label="Legal">
<a data-legal="privacy" href="../legal/privacy.html">Privacy Policy</a>
<a data-legal="terms" href="../legal/terms.html">Copyright &amp; Content Usage Policy</a>
<a data-legal="home" href="../index.html">Home</a>
<a data-en="Business &amp; Collaboration" data-zh="商业与合作" href="../about/index.html#business-collaboration">Business &amp; Collaboration</a>
</nav>
<p data-en="© 2026 Kiwi 爱AI Study. All rights reserved." data-zh="© 2026 Kiwi 爱AI Study。保留所有权利。">© 2026 Kiwi 爱AI Study. All rights reserved.</p>
</footer>
{LANG_SCRIPT}
</body>
</html>
"""


def render_by_grade(catalog: dict) -> None:
    meta = catalog["by_grade"]
    title_en = meta["title_en"]
    title_zh = meta["title_zh"]
    sub_en = meta["subtitle_en"]
    sub_zh = meta["subtitle_zh"]
    picks: list[str] = []
    for g in grades_with_topics(catalog):
        gmeta = catalog["grades"][str(g)]
        gzh = GRADE_ZH.get(g, f"{g} 年级")
        slug = html.escape(gmeta["hub_slug"], quote=True)
        courses_en = gmeta.get("courses_en", "")
        courses_zh = gmeta.get("courses_zh", courses_en)
        course_line = ""
        if courses_en:
            course_line = (
                f'<span class="kiwi-grade-pick-meta" data-en="{html.escape(courses_en)}" '
                f'data-zh="{html.escape(courses_zh)}">{html.escape(courses_en)}</span>'
            )
        picks.append(
            f'<a class="kiwi-grade-pick" href="{slug}.html">'
            f'<span class="kiwi-grade-pick-main">'
            f'<span class="kiwi-grade-pick-label" data-en="Grade {g}" data-zh="{html.escape(gzh)}">'
            f"Grade {g}</span>"
            f"{course_line}</span>"
            f'<span class="kiwi-grade-pick-cta" data-en="View topics →" data-zh="查看主题 →">'
            f"View topics →</span></a>"
        )
    pick_body = "\n".join(picks)
    page = (
        math_page_header(
            title_en,
            title_zh,
            sub_en,
            'data-pagefind-filter="section:math"',
            f'data-pagefind-meta="breadcrumb:Math › {html.escape(title_en, quote=True)}"',
        )
        + f"""<main data-pagefind-body="" data-pagefind-filter="lang:en" class="edu-main topic-main">
<div class="page-back-wrap">
<a class="page-back-link" data-en="← Back to Math Education" data-page-back="" data-zh="← 返回数学教育" href="index.html">← Back to Math Education</a>
</div>
<section class="nf-hero topic-banner" aria-label="Math by grade">
<p class="topic-banner-kicker" data-en="MATH · BY GRADE" data-zh="数学 · 按年级">MATH · BY GRADE</p>
<h1 data-en="{html.escape(title_en)}" data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</h1>
<p class="topic-banner-subtitle" data-en="{html.escape(sub_en)}" data-zh="{html.escape(sub_zh)}">{html.escape(sub_en)}</p>
</section>
<section class="edu-section kiwi-grade-picker-section">
<h2 class="visually-hidden" data-en="Choose a grade" data-zh="选择年级">Choose a grade</h2>
<div class="kiwi-grade-picker">{pick_body}</div>
</section>
</main>
"""
        + math_page_footer()
    )
    out = ROOT / meta["hub_file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def render_grade_hub(grade: int, catalog: dict) -> None:
    gmeta = catalog["grades"][str(grade)]
    body = book_toc_html(grade, catalog)
    title_en = gmeta["title_en"]
    title_zh = gmeta["title_zh"]
    sub_en = gmeta["subtitle_en"]
    sub_zh = gmeta["subtitle_zh"]
    courses_en = gmeta.get("courses_en", "")
    courses_zh = gmeta.get("courses_zh", "")

    gzh = GRADE_ZH.get(grade, f"{grade} 年级")
    page = (
        math_page_header(
            title_en,
            title_zh,
            sub_en,
            f'data-pagefind-filter="section:math grade:{grade}"',
            f'data-pagefind-meta="breadcrumb:Math › {html.escape(title_en, quote=True)}"',
            str(grade),
        )
        + f"""<main data-pagefind-body="" data-pagefind-filter="lang:en" class="edu-main topic-main">
<div class="page-back-wrap">
<a class="page-back-link" data-en="← Back to Math by Grade" data-page-back="" data-zh="← 返回按年级浏览" href="by-grade.html">← Back to Math by Grade</a>
</div>
<section class="nf-hero topic-banner" aria-label="Grade hub">
<p class="topic-banner-kicker" data-en="ONTARIO · GRADE {grade}" data-zh="安省 · {html.escape(gzh)}">ONTARIO · GRADE {grade}</p>
<h1 data-en="{html.escape(title_en)}" data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</h1>
<p class="topic-banner-subtitle" data-en="{html.escape(sub_en)}" data-zh="{html.escape(sub_zh)}">{html.escape(sub_en)}</p>
</section>
<p class="kiwi-grade-strip kiwi-grade-strip--hub">
<span class="kiwi-grade-pill" data-en="Grade {grade}" data-zh="{html.escape(gzh)}">Grade {grade}</span>
<span class="kiwi-grade-pill kiwi-grade-pill--course" data-en="{html.escape(courses_en)}" data-zh="{html.escape(courses_zh)}">{html.escape(courses_en)}</span>
</p>
<section class="edu-section kiwi-book-toc-section" aria-labelledby="grade-toc-heading">
<h2 id="grade-toc-heading" class="visually-hidden" data-en="Contents" data-zh="目录">Contents</h2>
{body}
</section>
</main>
"""
        + math_page_footer()
    )
    out = ROOT / gmeta["hub_file"]
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def main() -> None:
    catalog = load_catalog()
    for g in grades_with_topics(catalog):
        hub_slug = catalog["grades"][str(g)]["hub_slug"]
        hub_href = f"{hub_slug}.html"
        topics = [t for t in catalog["topics"] if g in t.get("grades", [])]
        for topic in topics:
            path = ROOT / topic["file"]
            if inject_topic(path, topic, hub_href):
                print("labeled", path.relative_to(ROOT))
    render_by_grade(catalog)
    for g in grades_with_topics(catalog):
        render_grade_hub(g, catalog)


if __name__ == "__main__":
    main()