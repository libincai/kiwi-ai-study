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


def course_hub_slug(catalog: dict) -> str:
    return catalog.get("by_course", {}).get("hub_slug", "by-ontario-course")


def course_hub_anchor(code: str) -> str:
    return code.lower()


def course_hub_href(code: str, catalog: dict) -> str:
    return f"/{course_hub_slug(catalog)}#{course_hub_anchor(code)}"


def grade_pills_block(grades: list[int], courses: list[str], catalog: dict) -> str:
    unique = sorted(set(grades))
    grade_meta = catalog.get("grades", {})
    grade_pill_lines = []
    for g in unique:
        grade_en = f"Grade {g}"
        grade_zh = GRADE_ZH.get(g, f"{g} 年级")
        hub = grade_meta.get(str(g), {}).get("hub_slug", f"grade-{g}")
        grade_pill_lines.append(
            f'    <a class="kiwi-grade-pill kiwi-grade-pill--link" href="/{html.escape(hub, quote=True)}" '
            f'data-en="{html.escape(grade_en)}" data-zh="{html.escape(grade_zh)}">'
            f"{html.escape(grade_en)}</a>"
        )
    grade_pills_body = "\n".join(grade_pill_lines)
    course_pills = ""
    seen_courses: set[str] = set()
    for c in courses:
        if c in seen_courses:
            continue
        seen_courses.add(c)
        href = course_hub_href(c, catalog)
        course_pills += (
            f'<a class="kiwi-grade-pill kiwi-grade-pill--course kiwi-grade-pill--link" '
            f'href="{html.escape(href, quote=True)}" '
            f'data-en="{html.escape(c)}" data-zh="{html.escape(c)}">{html.escape(c)}</a> '
        )
    filters = " ".join(f"grade:{x}" for x in unique)
    return (
        f"{MARKER_START}\n"
        f'<div class="kiwi-grade-strip-wrap" data-pagefind-filter="{html.escape(filters)}">\n'
        f'  <p class="kiwi-grade-strip">\n'
        f"{grade_pills_body}\n"
        f"    {course_pills}\n"
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


def inject_topic(path: Path, topic: dict, catalog: dict) -> bool:
    if not path.is_file():
        print("missing", path.relative_to(ROOT))
        return False
    text = path.read_text(encoding="utf-8")
    text = strip_catalog_blocks(text)
    block = grade_pills_block(topic.get("grades", []), topic.get("courses", []), catalog)
    banner = re.search(
        r'<section[^>]*\b(?:foundation-topic-banner|nf-hero\s+topic-banner)\b[^>]*>.*?</section>',
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
    return f"/{slug}"


COURSE_PRIMARY_GRADE: dict[str, int] = {
    "MTH1W": 9,
    "MPM2D": 10,
    "MCR3U": 11,
}


GRADE_ZH = {
    3: "三年级",
    4: "四年级",
    5: "五年级",
    6: "六年级",
    7: "七年级",
    8: "八年级",
    9: "九年级",
    10: "十年级",
    11: "十一年级",
    12: "十二年级",
}


def hub_href_for_topic(topic: dict, catalog: dict) -> str:
    grades = sorted(set(topic.get("grades", [])))
    grade_meta = catalog.get("grades", {})
    if len(grades) == 1:
        g = str(grades[0])
        if g in grade_meta:
            return f"{grade_meta[g]['hub_slug']}.html"
    if 11 in grades and "11" in grade_meta:
        return "grade-11.html"
    slug = catalog.get("by_grade", {}).get("hub_slug", "by-grade")
    return f"{slug}.html"


def grades_with_topics(catalog: dict) -> list[int]:
    found: set[int] = set()
    for t in catalog.get("topics", []):
        for g in t.get("grades", []):
            found.add(int(g))
    return sorted(found)


def _dedupe_level2_in_chapter(items: list[dict]) -> list[dict]:
    """One grade-hub link per Level 2 title within a chapter."""
    seen: set[str] = set()
    out: list[dict] = []
    for t in items:
        key = (t.get("title_en") or "").strip().casefold()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(t)
    return out


def chapters_for_grade(grade: int, catalog: dict) -> list[tuple[dict, list[dict]]]:
    if grade == 11:
        topics = [
            t
            for t in catalog["topics"]
            if grade in t.get("grades", []) and t.get("list_on_grade_hub", True)
        ]
    else:
        topics = [t for t in catalog["topics"] if grade in t.get("grades", [])]
    chapters_dict = catalog.get("chapters", {})
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for t in topics:
        by_chapter[t.get("chapter_id", "misc")].append(t)
    ordered: list[tuple[int, dict, list[dict]]] = []
    for cid, items in by_chapter.items():
        items.sort(key=lambda x: x.get("sort", 0))
        items = _dedupe_level2_in_chapter(items)
        ch = chapters_dict.get(
            cid,
            {"title_en": cid, "title_zh": cid, "order": 999},
        )
        ordered.append((ch.get("order", 999), ch, items))
    ordered.sort(key=lambda x: (x[0], x[1].get("title_en", "")))
    return _merge_level1_chapters([(ch, items) for _, ch, items in ordered])


def _merge_level1_chapters(
    sections: list[tuple[dict, list[dict]]],
) -> list[tuple[dict, list[dict]]]:
    """One grade-hub chapter per Level 1 title (foundations + thinking)."""
    buckets: dict[tuple[str, str], dict] = {}
    for ch, items in sections:
        key = (ch.get("title_en", ""), ch.get("title_zh", ch.get("title_en", "")))
        if key not in buckets:
            buckets[key] = {"order": ch.get("order", 999), "ch": ch, "items": []}
        else:
            buckets[key]["order"] = min(buckets[key]["order"], ch.get("order", 999))
        buckets[key]["items"].extend(items)
    merged: list[tuple[int, dict, list[dict]]] = []
    for data in buckets.values():
        items = _dedupe_level2_in_chapter(data["items"])
        items.sort(key=lambda x: x.get("sort", 0))
        if not items:
            continue
        merged.append((data["order"], data["ch"], items))
    merged.sort(key=lambda x: (x[0], x[1].get("title_en", "")))
    return [(ch, items) for _, ch, items in merged]


def topic_course_pills(courses: list[str]) -> str:
    pills = ""
    seen: set[str] = set()
    for c in courses:
        if not c or c in seen:
            continue
        seen.add(c)
        pills += (
            f'<span class="kiwi-grade-pill kiwi-grade-pill--course" '
            f'data-en="{html.escape(c)}" data-zh="{html.escape(c)}">{html.escape(c)}</span> '
        )
    if not pills:
        return ""
    return f'<span class="kiwi-book-topic-courses">{pills.strip()}</span>'


def book_toc_html(grade: int, catalog: dict) -> str:
    parts = ['<nav class="kiwi-book-toc" aria-label="Table of contents">']
    for seq, (ch, items) in enumerate(chapters_for_grade(grade, catalog), start=1):
        te, tz = ch["title_en"], ch["title_zh"]
        num = f"{seq:02d}"
        parts.append('<section class="kiwi-book-chapter">')
        parts.append('<div class="kiwi-book-chapter-head">')
        parts.append(
            f'<span class="kiwi-book-chapter-number" aria-hidden="true">{num}</span>'
        )
        parts.append(
            f'<p class="kiwi-book-chapter-title"><strong data-en="{html.escape(te)}" '
            f'data-zh="{html.escape(tz)}">{html.escape(te)}</strong></p>'
        )
        parts.append("</div>")
        parts.append('<ol class="kiwi-book-topic-list">')
        for t in items:
            slug = Path(t["file"]).stem
            href = topic_href(slug)
            req = topic_course_pills(t.get("courses") or [])
            parts.append(
                f'<li class="kiwi-book-topic-row">'
                f'<a href="{html.escape(href, quote=True)}" '
                f'data-en="{html.escape(t["title_en"])}" '
                f'data-zh="{html.escape(t["title_zh"])}">{html.escape(t["title_en"])}</a>'
                f"{req}</li>"
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
<script defer src="../assets/js/drive-breadcrumb.js?v=20261115-bcrumb4"></script>
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
    body_class: str = "edu-page topic-page",
    css_v: str = "20261115-course-hub-toc",
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
<link rel="stylesheet" href="../assets/css/styles.css?v={css_v}"/>
</head>
<body class="{body_class}">
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
<a data-en="Math Education" data-nav="math" data-zh="数学教育" href="/math">Math Education</a>
<a data-en="AI Education" data-nav="ai" data-zh="人工智能教育" href="../ai/index.html">AI Education</a>
<a data-en="In-Class Learning" data-nav="class" data-zh="课堂学习" href="/in-class-learning">In-Class Learning</a>
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


def courses_used(catalog: dict) -> list[str]:
    found: set[str] = set()
    for t in catalog.get("topics", []):
        for c in t.get("courses") or []:
            found.add(c)
    codes = catalog.get("course_codes", {})
    ordered = sorted(found, key=lambda c: (codes.get(c, {}).get("order", 999), c))
    return ordered


def _level2_for_course_hub(topic: dict) -> bool:
    """Sidebar / Level 2 links only — not nested lesson pages under a hub."""
    if topic.get("list_on_grade_hub", True):
        return True
    note = topic.get("verified_note") or ""
    if note.startswith("Ontario curriculum expectation alignment"):
        return True
    return False


def topics_for_course(code: str, catalog: dict) -> list[dict]:
    """Level 2 sidebar hubs only (see docs/MATH_NAV_LEVELS.md)."""
    chapters = catalog.get("chapters", {})
    items = [
        t
        for t in catalog.get("topics", [])
        if code in (t.get("courses") or []) and _level2_for_course_hub(t)
    ]

    def sort_key(t: dict) -> tuple:
        ch = chapters.get(t.get("chapter_id", ""), {})
        return (ch.get("order", 999), t.get("sort", 0), t.get("title_en", ""))

    items.sort(key=sort_key)
    return items


def grades_for_course(code: str, catalog: dict) -> list[int]:
    found: set[int] = set()
    for t in topics_for_course(code, catalog):
        for g in t.get("grades", []):
            found.add(int(g))
    return sorted(found)


def chapters_for_course(code: str, catalog: dict) -> list[tuple[dict, list[dict]]]:
    topics = topics_for_course(code, catalog)
    if not topics:
        return []
    chapters_dict = catalog.get("chapters", {})
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for t in topics:
        by_chapter[t.get("chapter_id", "misc")].append(t)
    ordered: list[tuple[int, dict, list[dict]]] = []
    for cid, items in by_chapter.items():
        items.sort(key=lambda x: x.get("sort", 0))
        items = _dedupe_level2_in_chapter(items)
        ch = chapters_dict.get(
            cid,
            {"title_en": cid, "title_zh": cid, "order": 999},
        )
        ordered.append((ch.get("order", 999), ch, items))
    ordered.sort(key=lambda x: (x[0], x[1].get("title_en", "")))
    return _merge_level1_chapters([(ch, items) for _, ch, items in ordered])


def course_grade_hub_links_html(code: str, catalog: dict) -> str:
    grade_set = set(grades_for_course(code, catalog))
    if not grade_set:
        return ""
    primary = COURSE_PRIMARY_GRADE.get(code)
    ordered: list[int] = []
    if primary is not None and primary in grade_set:
        ordered.append(primary)
        if code == "MPM2D" and 11 in grade_set:
            ordered.append(11)
        elif code == "MCR3U" and 10 in grade_set:
            ordered.append(10)
    else:
        ordered = sorted(grade_set)
    grade_meta = catalog.get("grades", {})
    links: list[str] = []
    for g in ordered:
        gm = grade_meta.get(str(g))
        if not gm:
            continue
        slug = html.escape(gm.get("hub_slug", f"grade-{g}"), quote=True)
        title_en = gm.get("title_en", f"Grade {g} Mathematics")
        title_zh = gm.get("title_zh", GRADE_ZH.get(g, str(g)))
        links.append(
            f'<a href="/{slug}" data-en="{html.escape(title_en)}" '
            f'data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</a>'
        )
    if not links:
        return ""
    joined = " · ".join(links)
    en = f"Browse the same lessons by grade: {joined}"
    zh = f"按年级浏览相关主题：{joined}"
    return (
        f'<p class="kiwi-course-grade-hub-links" data-en="{html.escape(en)}" '
        f'data-zh="{html.escape(zh)}">{en}</p>'
    )


def _bilingual_p(en: str, zh: str) -> str:
    return (
        f'<p data-en="{html.escape(en)}" data-zh="{html.escape(zh)}">{en}</p>'
    )


def curriculum_panel_html(meta: dict, code: str, catalog: dict) -> str:
    url = html.escape(meta.get("official_url", ""), quote=True)
    official_en = (
        f'Official source: <a href="{url}">{html.escape(meta.get("official_url", ""))}</a>'
    )
    official_zh = (
        f'官方来源：<a href="{url}">{html.escape(meta.get("official_url", ""))}</a>'
    )
    parts = [
        '<aside aria-label="Ontario Curriculum Connection" class="kiwi-curriculum-panel">',
        '<div class="kiwi-curriculum-heading" data-en="Ontario Curriculum Connection" '
        'data-zh="安大略课程衔接">Ontario Curriculum Connection</div>',
    ]
    if meta.get("code_explainer_en"):
        parts.append(
            f'<p class="kiwi-course-code-explainer" '
            f'data-en="{html.escape(meta["code_explainer_en"])}" '
            f'data-zh="{html.escape(meta.get("code_explainer_zh", meta["code_explainer_en"]))}">'
            f'{meta["code_explainer_en"]}</p>'
        )
    parts.append(_bilingual_p(meta["leadin_en"], meta["leadin_zh"]))
    if meta.get("quote_en"):
        q_en = f'“{meta["quote_en"]}”'
        q_zh = f'“{meta["quote_zh"]}”'
        parts.append(_bilingual_p(q_en, q_zh))
    parts.append(_bilingual_p(meta["citation_en"], meta["citation_zh"]))
    parts.append(
        f'<p data-en="{html.escape(official_en)}" data-zh="{html.escape(official_zh)}">'
        f"{official_en}</p>"
    )
    parts.append(
        '<p data-en="<strong>How topics on this site connect</strong>" '
        'data-zh="<strong>本站主题如何衔接</strong>">'
        "<strong>How topics on this site connect</strong></p>"
    )
    parts.append(_bilingual_p(meta["connect_en"], meta["connect_zh"]))
    parts.append(course_grade_hub_links_html(code, catalog))
    parts.append("</aside>")
    return "\n".join(parts)


def course_toc_html(code: str, catalog: dict) -> str:
    sections = chapters_for_course(code, catalog)
    if not sections:
        return (
            '<p data-en="No lessons are tagged with this course code yet." '
            'data-zh="尚无标注此课程代码的课时。">'
            "No lessons are tagged with this course code yet.</p>"
        )
    parts = ['<nav class="kiwi-book-toc" aria-label="Lessons for this course">']
    for seq, (ch, items) in enumerate(sections, start=1):
        te, tz = ch["title_en"], ch["title_zh"]
        num = f"{seq:02d}"
        parts.append('<section class="kiwi-book-chapter">')
        parts.append('<div class="kiwi-book-chapter-head">')
        parts.append(
            f'<span class="kiwi-book-chapter-number" aria-hidden="true">{num}</span>'
        )
        parts.append(
            f'<p class="kiwi-book-chapter-title"><strong data-en="{html.escape(te)}" '
            f'data-zh="{html.escape(tz)}">{html.escape(te)}</strong></p>'
        )
        parts.append("</div>")
        parts.append('<ol class="kiwi-book-topic-list">')
        for t in items:
            slug = Path(t["file"]).stem
            href = topic_href(slug)
            parts.append(
                f'<li class="kiwi-book-topic-row">'
                f'<a href="{html.escape(href, quote=True)}" '
                f'data-en="{html.escape(t["title_en"])}" '
                f'data-zh="{html.escape(t["title_zh"])}">{html.escape(t["title_en"])}</a>'
                f"</li>"
            )
        parts.append("</ol></section>")
    parts.append("</nav>")
    return "\n".join(parts)


def course_hub_cards_html(catalog: dict) -> str:
    codes = courses_used(catalog)
    code_meta = catalog.get("course_codes", {})
    cards: list[str] = []
    for i, code in enumerate(codes):
        meta = code_meta.get(code, {})
        anchor = course_hub_anchor(code)
        summary_en = meta.get("summary_en", code)
        summary_zh = meta.get("summary_zh", code)
        open_attr = ' open=""' if i == 0 else ""
        cards.append(
            f'<details class="lesson-card" id="{html.escape(anchor)}"{open_attr}>'
            f'<summary data-en="{html.escape(summary_en)}" data-zh="{html.escape(summary_zh)}">'
            f"{html.escape(summary_en)}</summary>"
            f'<div class="lesson-card-content">'
            f"{curriculum_panel_html(meta, code, catalog)}"
            f"{course_toc_html(code, catalog)}"
            f"</div></details>"
        )
    return "\n".join(cards)


COURSE_HUB_ACCORDION = r"""
<style id="kiwi-ontario-course-hub-style">
.kiwi-ontario-course-main .lesson-card{background:#fff;border:1px solid #dce7f3;border-radius:14px;margin:12px 0;overflow:hidden}
.kiwi-ontario-course-main .lesson-card summary{padding:19px 23px;cursor:pointer;font-weight:750;color:#173e70;font-size:18px;list-style:none;display:flex;justify-content:space-between;align-items:center}
.kiwi-ontario-course-main .lesson-card summary::-webkit-details-marker{display:none}
.kiwi-ontario-course-main .lesson-card summary::after{content:'+';font-size:25px;color:#1768b2;flex-shrink:0;margin-left:12px}
.kiwi-ontario-course-main .lesson-card[open] summary::after{content:'−'}
.kiwi-ontario-course-main .lesson-card[open] summary{background:#eef6ff;border-bottom:1px solid #dce7f3}
.kiwi-ontario-course-main .lesson-card-content{padding:14px 24px 24px;line-height:1.8;overflow-wrap:anywhere}
.kiwi-ontario-course-main .lesson-card[id]{scroll-margin-top:22px}
.kiwi-ontario-course-main .kiwi-curriculum-panel .kiwi-course-grade-hub-links{margin-top:10px}
@media(max-width:600px){.kiwi-ontario-course-main .lesson-card summary{padding:15px;font-size:16px}.kiwi-ontario-course-main .lesson-card-content{padding:12px 16px}}
.kiwi-accordion-controls{display:flex;justify-content:flex-end;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0 12px}
.kiwi-accordion-controls button{font:inherit;font-size:13px;font-weight:600;color:#155d9d;background:#fff;border:1px solid #cddff2;border-radius:8px;padding:8px 13px;cursor:pointer}
.kiwi-accordion-controls button:hover,.kiwi-accordion-controls button:focus-visible{background:#eaf3fd;outline-offset:2px}
</style>
<script id="kiwi-ontario-course-accordion">
(function(){
  function openFromHash(){
    var id=location.hash?location.hash.slice(1):'';
    if(!id)return;
    var card=document.getElementById(id);
    if(card&&card.tagName==='DETAILS')card.open=true;
  }
  function init(){
    document.querySelectorAll('.kiwi-ontario-course-main').forEach(function(main){
      var cards=Array.from(main.querySelectorAll('details.lesson-card'));
      if(!cards.length)return;
      openFromHash();
      if(cards.length<2)return;
      if(main.querySelector('.kiwi-accordion-controls'))return;
      var first=cards[0];
      var controls=document.createElement('div');
      controls.className='kiwi-accordion-controls';
      controls.setAttribute('role','group');
      controls.setAttribute('aria-label','Course sections');
      controls.innerHTML='<button type="button" data-accordion-action="expand" data-en="Expand All" data-zh="全部展开">Expand All</button><button type="button" data-accordion-action="collapse" data-en="Collapse All" data-zh="全部收起">Collapse All</button>';
      first.parentNode.insertBefore(controls,first);
      controls.addEventListener('click',function(event){
        var button=event.target.closest('button[data-accordion-action]');
        if(!button)return;
        var expand=button.getAttribute('data-accordion-action')==='expand';
        cards.forEach(function(card){card.open=expand;});
      });
      function syncLanguage(){
        var zh=(document.documentElement.lang||'').toLowerCase().startsWith('zh');
        controls.querySelectorAll('button').forEach(function(b){b.textContent=b.getAttribute(zh?'data-zh':'data-en');});
      }
      syncLanguage();
      new MutationObserver(syncLanguage).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
    });
    window.addEventListener('hashchange',openFromHash);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
"""


def render_ontario_course_hub(catalog: dict) -> None:
    meta = catalog.get("by_course", {})
    if not meta or not courses_used(catalog):
        return
    title_en = meta["title_en"]
    title_zh = meta["title_zh"]
    sub_en = meta["subtitle_en"]
    sub_zh = meta["subtitle_zh"]
    cards = course_hub_cards_html(catalog)
    page = (
        math_page_header(
            title_en,
            title_zh,
            sub_en,
            'data-pagefind-filter="section:math"',
            f'data-pagefind-meta="breadcrumb:Math › {html.escape(title_en, quote=True)}"',
            body_class="edu-page topic-page kiwi-ontario-course-hub",
        )
        + COURSE_HUB_ACCORDION
        + f"""<main data-pagefind-body="" data-pagefind-filter="lang:en" class="edu-main topic-main kiwi-ontario-course-main">
<div class="page-back-wrap">
<a class="page-back-link" data-en="← Back to Math Education" data-page-back="" data-zh="← 返回数学教育" href="/math">← Back to Math Education</a>
</div>
<section class="nf-hero topic-banner" aria-label="Ontario course codes">
<p class="topic-banner-kicker" data-en="MATH · ONTARIO" data-zh="数学 · 安省">MATH · ONTARIO</p>
<h1 data-en="{html.escape(title_en)}" data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</h1>
<p class="topic-banner-subtitle" data-en="{html.escape(sub_en)}" data-zh="{html.escape(sub_zh)}">{html.escape(sub_en)}</p>
</section>
<section class="edu-section" aria-labelledby="course-hub-heading">
<h2 id="course-hub-heading" class="visually-hidden" data-en="Course codes" data-zh="课程代码">Course codes</h2>
{cards}
</section>
</main>
"""
        + math_page_footer()
    )
    out = ROOT / meta["hub_file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


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
            f'<a class="kiwi-grade-pick" href="/{slug}">'
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
<a class="page-back-link" data-en="← Back to Math Education" data-page-back="" data-zh="← 返回数学教育" href="/math">← Back to Math Education</a>
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
    gzh = GRADE_ZH.get(grade, f"{grade} 年级")
    page = (
        math_page_header(
            title_en,
            title_zh,
            sub_en,
            f'data-pagefind-filter="section:math grade:{grade}"',
            f'data-pagefind-meta="breadcrumb:Math › {html.escape(title_en, quote=True)}"',
            str(grade),
            body_class="edu-page topic-page kiwi-grade-hub",
        )
        + f"""<main data-pagefind-body="" data-pagefind-filter="lang:en" class="edu-main topic-main kiwi-grade-hub-main">
<div class="page-back-wrap">
<a class="page-back-link" data-en="← Back to Math by Grade" data-page-back="" data-zh="← 返回按年级浏览" href="/by-grade">← Back to Math by Grade</a>
</div>
<section class="nf-hero topic-banner" aria-label="Grade hub">
<p class="topic-banner-kicker" data-en="ONTARIO · GRADE {grade}" data-zh="安省 · {html.escape(gzh)}">ONTARIO · GRADE {grade}</p>
<h1 data-en="{html.escape(title_en)}" data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</h1>
<p class="topic-banner-subtitle" data-en="{html.escape(sub_en)}" data-zh="{html.escape(sub_zh)}">{html.escape(sub_en)}</p>
</section>
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


SKIP_STRIP = frozenset(
    {
        "by-grade.html",
        "by-ontario-course.html",
        "index.html",
        "in-class-learning.html",
        "math-foundations.html",
        "mathematical-thinking.html",
    }
)


def strip_labels_not_in_catalog(catalog: dict) -> None:
    """Remove injected grade strips from pages dropped from math-topics.json."""
    topic_files = {t["file"] for t in catalog.get("topics", [])}
    math_dir = ROOT / "math"
    for path in sorted(math_dir.glob("*.html")):
        if path.name.startswith("grade-") or path.name in SKIP_STRIP:
            continue
        rel = f"math/{path.name}"
        text = path.read_text(encoding="utf-8")
        if META_START not in text and MARKER_START not in text:
            continue
        if rel in topic_files:
            continue
        new_text = strip_catalog_blocks(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print("unlabeled", rel)


def main() -> None:
    from kiwi_math_topics_data import write_catalog

    write_catalog()
    catalog = load_catalog()
    injected: set[str] = set()
    for topic in catalog.get("topics", []):
        rel = topic["file"]
        if rel in injected:
            continue
        injected.add(rel)
        path = ROOT / rel
        if inject_topic(path, topic, catalog):
            print("labeled", path.relative_to(ROOT))
    strip_labels_not_in_catalog(catalog)
    render_by_grade(catalog)
    render_ontario_course_hub(catalog)
    for g in grades_with_topics(catalog):
        render_grade_hub(g, catalog)


if __name__ == "__main__":
    main()