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
            f'data-en="Grade {g} topic index →" data-zh="{html.escape(grade_zh)}主题目录 →">'
            f"Grade {g} topic index →</a>"
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


def render_grade_hub(grade: int, catalog: dict) -> None:
    gmeta = catalog["grades"][str(grade)]
    topics = [t for t in catalog["topics"] if grade in t.get("grades", [])]
    topics.sort(key=lambda t: (t.get("strand_en", ""), t.get("sort", 0), t["title_en"]))
    by_strand: dict[str, list[dict]] = defaultdict(list)
    for t in topics:
        by_strand[t.get("strand_en", "Topics")].append(t)

    rows: list[str] = []
    n = 0
    for strand, items in sorted(by_strand.items()):
        strand_zh = items[0].get("strand_zh", strand) if items else strand
        rows.append(
            f'<h3 class="kiwi-grade-strand" data-en="{html.escape(strand)}" '
            f'data-zh="{html.escape(strand_zh)}">{html.escape(strand)}</h3>'
        )
        rows.append('<div class="edu-topic-list">')
        for t in items:
            n += 1
            slug = Path(t["file"]).stem
            href = topic_href(slug)
            rows.append(
                f'<a class="edu-topic edu-topic-link" href="{html.escape(href, quote=True)}">'
                f'<span class="edu-topic-number">{n:02d}</span>'
                f"<div><h3 data-en=\"{html.escape(t['title_en'])}\" "
                f"data-zh=\"{html.escape(t['title_zh'])}\">{html.escape(t['title_en'])}</h3>"
                f"<p data-en=\"{html.escape(t.get('desc_en', ''))}\" "
                f"data-zh=\"{html.escape(t.get('desc_zh', ''))}\">{html.escape(t.get('desc_en', ''))}</p></div>"
                f'<span class="edu-link" data-en="Open lesson →" data-zh="打开课程 →">Open lesson →</span></a>'
            )
        rows.append("</div>")

    body = "\n".join(rows)
    title_en = gmeta["title_en"]
    title_zh = gmeta["title_zh"]
    sub_en = gmeta["subtitle_en"]
    sub_zh = gmeta["subtitle_zh"]
    courses_en = gmeta.get("courses_en", "")
    courses_zh = gmeta.get("courses_zh", "")

    page = f"""<!DOCTYPE html>
<!-- Generated by local/kiwi_math_catalog.py — edit data/math-topics.json, not this file by hand. -->
<html lang="en-CA" data-pagefind-filter="section:math grade:{grade}" data-pagefind-meta="breadcrumb:Math › {html.escape(title_en, quote=True)}">
<head>
<!-- kiwi-search-prepared -->
<meta name="pagefind:title_en" content="{html.escape(title_en)}" />
<meta name="pagefind:section" content="math" />
<meta name="pagefind:breadcrumb" content="Math › {html.escape(title_en)}" />
<meta name="pagefind:grades" content="{grade}" />
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title data-en="{html.escape(title_en)} | Kiwi 爱AI Study" data-zh="{html.escape(title_zh)} | Kiwi 爱AI Study">{html.escape(title_en)} | Kiwi 爱AI Study</title>
<meta name="description" content="{html.escape(sub_en)}"/>
<link rel="stylesheet" href="../assets/css/styles.css?v=20261108-level2-width"/>
<style>
.edu-page{{--ink:#14264d;--blue:#1768b2;--muted:#5e6f88;--line:#dce6f1;color:var(--ink)}}
.edu-section{{margin:42px 0}}
.edu-section h2{{font-size:clamp(24px,2.7vw,32px);line-height:1.2;color:#153d70;margin:0 0 12px}}
.edu-lead{{color:var(--muted);font-size:16px;line-height:1.75;max-width:900px;margin:0 0 22px}}
.edu-topic-list{{display:grid;gap:12px;margin-bottom:28px}}
.edu-topic{{display:grid;grid-template-columns:74px minmax(0,1fr) auto;gap:16px;align-items:center;padding:17px 19px;border:1px solid var(--line);border-radius:15px;background:#fff;text-decoration:none;color:inherit}}
.edu-topic-link{{transition:transform .16s ease,box-shadow .16s ease}}
.edu-topic-link:hover{{transform:translateY(-2px);box-shadow:0 8px 20px rgba(24,55,95,.09)}}
.edu-topic-number{{width:54px;height:54px;display:grid;place-items:center;border-radius:14px;background:#eaf4ff;color:#1768b2;font-weight:900;font-size:19px}}
.edu-topic h3{{margin:0 0 5px;font-size:18px;color:#173e70}}
.edu-topic p{{margin:0;color:#62738a;font-size:13px;line-height:1.5}}
.edu-topic .edu-link{{white-space:nowrap;color:#1768b2;font-weight:800;font-size:14px}}
.kiwi-grade-strand{{margin:28px 0 12px;font-size:20px;color:#153d70}}
@media(max-width:760px){{.edu-topic{{grid-template-columns:52px minmax(0,1fr);gap:12px}}.edu-topic .edu-link{{grid-column:2}}}}
</style>
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
<main data-pagefind-body="" data-pagefind-filter="lang:en" class="edu-main topic-main">
<div class="page-back-wrap">
<a class="page-back-link" data-en="← Back to Math Education" data-page-back="" data-zh="← 返回数学教育" href="index.html">← Back to Math Education</a>
</div>
<section class="nf-hero topic-banner" aria-label="Grade hub">
<p class="topic-banner-kicker" data-en="BY GRADE · ONTARIO" data-zh="按年级 · 安省">BY GRADE · ONTARIO</p>
<h1 data-en="{html.escape(title_en)}" data-zh="{html.escape(title_zh)}">{html.escape(title_en)}</h1>
<p class="topic-banner-subtitle" data-en="{html.escape(sub_en)}" data-zh="{html.escape(sub_zh)}">{html.escape(sub_en)}</p>
</section>
<p class="kiwi-grade-strip kiwi-grade-strip--hub">
<span class="kiwi-grade-pill" data-en="Grade {grade}" data-zh="{html.escape({'9':'九年级','10':'十年级','11':'十一年级','12':'十二年级'}.get(str(grade), f'{grade} 年级'))}">Grade {grade}</span>
<span class="kiwi-grade-pill kiwi-grade-pill--course" data-en="{html.escape(courses_en)}" data-zh="{html.escape(courses_zh)}">{html.escape(courses_en)}</span>
</p>
<section class="edu-section">
<h2 data-en="Topic index" data-zh="主题目录">Topic index</h2>
<p class="edu-lead" data-en="These links open the same lesson pages used in Math Foundations — update content once." data-zh="以下链接与「数学基础」共用同一页面 —— 内容只需维护一处。">These links open the same lesson pages used in Math Foundations — update content once.</p>
{body}
<p class="edu-lead"><a data-en="Math Foundations hub →" data-zh="数学基础目录 →" href="math-foundations.html">Math Foundations hub →</a></p>
</section>
</main>
<footer class="site-footer">
<nav aria-label="Legal">
<a data-legal="privacy" href="../legal/privacy.html">Privacy Policy</a>
<a data-legal="terms" href="../legal/terms.html">Copyright &amp; Content Usage Policy</a>
<a data-legal="home" href="../index.html">Home</a>
<a data-en="Business &amp; Collaboration" data-zh="商业与合作" href="../about/index.html#business-collaboration">Business &amp; Collaboration</a>
</nav>
<p data-en="© 2026 Kiwi 爱AI Study. All rights reserved." data-zh="© 2026 Kiwi 爱AI Study。保留所有权利。">© 2026 Kiwi 爱AI Study. All rights reserved.</p>
</footer>
<script>
(() => {{
  const nav = {{ en: ['Home','About','Math Education','AI Education','In-Class Learning','My Books','Contact'], zh: ['首页','关于我们','数学教育','人工智能教育','课堂学习','我的书籍','联系我们'] }};
  const legal = {{ en: ['Privacy Policy','Terms of Service','Home'], zh: ['隐私政策','服务条款','首页'] }};
  const btns = document.querySelectorAll('.flag[data-language]');
  function setLanguage(lang) {{
    const l = lang === 'zh' ? 'zh' : 'en';
    document.documentElement.lang = l === 'zh' ? 'zh-CN' : 'en-CA';
    document.querySelectorAll('[data-en][data-zh]').forEach(el => {{
      el.innerHTML = el.getAttribute(l === 'zh' ? 'data-zh' : 'data-en');
    }});
    document.querySelectorAll('.site-nav [data-nav]').forEach((el, i) => {{ el.textContent = nav[l][i]; }});
    document.querySelectorAll('.site-footer [data-legal]').forEach((el, i) => {{ el.textContent = legal[l][i]; }});
    btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.language === l)));
    try {{ localStorage.setItem('kiwi-site-language', l); }} catch (e) {{}}
  }}
  btns.forEach(b => b.addEventListener('click', () => setLanguage(b.dataset.language)));
  let saved = 'en';
  try {{ saved = localStorage.getItem('kiwi-site-language') || 'en'; }} catch (e) {{}}
  setLanguage(saved);
  window.addEventListener('pageshow', () => {{
    let l = 'en';
    try {{ l = localStorage.getItem('kiwi-site-language') || 'en'; }} catch (e) {{}}
    setLanguage(l);
  }});
}})();
</script>
<script defer src="../assets/js/drive-breadcrumb.js?v=20261114-bcrumb1"></script>
<link href="../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer src="../assets/js/kiwi-site-search.js?v=20261114-search20"></script>
</body>
</html>
"""
    out = ROOT / gmeta["hub_file"]
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def main() -> None:
    catalog = load_catalog()
    hub_slug = catalog["grades"]["11"]["hub_slug"]
    hub_href = f"{hub_slug}.html"
    for topic in catalog["topics"]:
        path = ROOT / topic["file"]
        if inject_topic(path, topic, hub_href):
            print("labeled", path.relative_to(ROOT))
    render_grade_hub(11, catalog)


if __name__ == "__main__":
    main()