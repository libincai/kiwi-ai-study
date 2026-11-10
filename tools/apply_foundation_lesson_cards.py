#!/usr/bin/env python3
"""Wrap mf-chapter h3 sections in lesson-card accordions; inject shared CSS/JS."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT / "math"

H3_RE = re.compile(
    r'<h3\s+id="(?P<id>[^"]+)"\s+data-en="(?P<en>[^"]*)"\s+data-zh="(?P<zh>[^"]*)"[^>]*>(?P<label>[\s\S]*?)</h3>',
    re.I,
)

LESSON_CARD_CSS = """<style id="foundation-lesson-cards">
/* Level 4 accordion sections (match unit-conversions-and-rates.html) */
.mf-article .lesson-card{background:#fff;border:1px solid #dce7f3;border-radius:14px;margin:12px 0;overflow:hidden}
.mf-article .lesson-card summary{padding:19px 23px;cursor:pointer;font-weight:750;color:#173e70;font-size:18px;list-style:none;display:flex;justify-content:space-between;align-items:center}
.mf-article .lesson-card summary::-webkit-details-marker{display:none}
.mf-article .lesson-card summary::after{content:'+';font-size:25px;color:#1768b2;flex-shrink:0;margin-left:12px}
.mf-article .lesson-card[open] summary::after{content:'−'}
.mf-article .lesson-card[open] summary{background:#eef6ff;border-bottom:1px solid #dce7f3}
.mf-article .lesson-card-content{padding:14px 24px 24px;line-height:1.8;overflow-wrap:anywhere}
.mf-article .lesson-card-content h4,.mf-article .lesson-card-content h5{color:#153d70;font-size:16px;margin:17px 0 7px}
.mf-article .lesson-card-content table{margin-top:0}
.mf-article .lesson-card p{margin:10px 0}
@media(max-width:600px){.mf-article .lesson-card summary{padding:15px;font-size:16px}.mf-article .lesson-card-content{padding:12px 16px}}
</style>"""

ACCORDION_CSS = """<style id="kiwi-accordion-controls-style">
.kiwi-accordion-controls{display:flex;justify-content:flex-end;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0 12px}
.kiwi-accordion-controls button{font:inherit;font-size:13px;font-weight:600;color:#155d9d;background:#fff;border:1px solid #cddff2;border-radius:8px;padding:8px 13px;cursor:pointer}
.kiwi-accordion-controls button:hover,.kiwi-accordion-controls button:focus-visible{background:#eaf3fd;outline-offset:2px}
@media(max-width:560px){.kiwi-accordion-controls{gap:7px}.kiwi-accordion-controls button{padding:7px 10px;font-size:12px}}
</style>"""

ACCORDION_SCRIPT = """<script id="kiwi-accordion-controls-script">
(function(){
  function init(){
    document.querySelectorAll('.kiwi-topic-article, .mf-article.mf-chapter').forEach(function(article){
      var cards=Array.from(article.querySelectorAll('details.lesson-card'));
      if(cards.length<2 || article.querySelector('.kiwi-accordion-controls'))return;
      var first=cards[0];
      var controls=document.createElement('div');
      controls.className='kiwi-accordion-controls';
      controls.setAttribute('role','group');
      controls.setAttribute('aria-label','Lesson sections');
      controls.innerHTML='<button type="button" data-accordion-action="expand" data-en="Expand All" data-zh="全部展开">Expand All</button><button type="button" data-accordion-action="collapse" data-en="Collapse All" data-zh="全部收起">Collapse All</button>';
      first.parentNode.insertBefore(controls,first);
      controls.addEventListener('click',function(event){
        var button=event.target.closest('button[data-accordion-action]');
        if(!button)return;
        var expand=button.getAttribute('data-accordion-action')==='expand';
        cards.forEach(function(card){card.open=expand;});
      });
      cards.forEach(function(card,i){card.open=i===0;});
      function syncLanguage(){
        var zh=(document.documentElement.lang||'').toLowerCase().startsWith('zh');
        controls.querySelectorAll('button').forEach(function(b){b.textContent=b.getAttribute(zh?'data-zh':'data-en');});
      }
      syncLanguage();
      new MutationObserver(syncLanguage).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>"""

OLD_ACCORDION_ONLY_KIWI = re.compile(
    r"<script id=\"kiwi-accordion-controls-script\">[\s\S]*?"
    r"document\.querySelectorAll\('\.kiwi-topic-article'\)"
    r"[\s\S]*?</script>",
    re.I,
)


def wrap_h3_sections(html: str) -> str:
    start = html.find('<article class="mf-article mf-chapter">')
    if start < 0:
        return html
    end = html.find("</article>", start)
    if end < 0:
        return html
    article = html[start:end]
    matches = list(H3_RE.finditer(article))
    if not matches:
        return html

    h1_m = re.search(r"<h1\b[^>]*>[\s\S]*?</h1>", article, re.I)
    if not h1_m:
        return html
    intro = article[h1_m.end() : matches[0].start()]

    cards: list[str] = []
    for i, m in enumerate(matches):
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(article)
        body = article[m.end() : body_end].strip()
        label = m.group("label").strip()
        cards.append(
            f'<details class="lesson-card"><summary id="{m.group("id")}" data-en="{m.group("en")}" data-zh="{m.group("zh")}">{label}</summary>'
            f'<div class="lesson-card-content">{body}</div></details>'
        )

    new_article = article[: h1_m.end()] + intro + "".join(cards)
    return html[:start] + new_article + html[end:]


def inject_assets(html: str) -> str:
    if 'id="foundation-lesson-cards"' not in html:
        html = html.replace("</head>", LESSON_CARD_CSS + ACCORDION_CSS + "\n</head>", 1)
    elif 'id="kiwi-accordion-controls-style"' not in html:
        html = html.replace("</head>", ACCORDION_CSS + "\n</head>", 1)

    if OLD_ACCORDION_ONLY_KIWI.search(html):
        html = OLD_ACCORDION_ONLY_KIWI.sub(ACCORDION_SCRIPT, html)
    elif 'id="kiwi-accordion-controls-script"' not in html:
        html = html.replace("</body>", ACCORDION_SCRIPT + "\n</body>", 1)
    elif ".mf-article.mf-chapter" not in html.split("kiwi-accordion-controls-script")[1].split("</script>")[0]:
        html = html.replace(
            "document.querySelectorAll('.kiwi-topic-article')",
            "document.querySelectorAll('.kiwi-topic-article, .mf-article.mf-chapter')",
        )
    return html


def process_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    if '<article class="mf-article mf-chapter">' not in text:
        return "skip:no-article"
    had_h3 = bool(H3_RE.search(text))
    if had_h3:
        text = wrap_h3_sections(text)
    text = inject_assets(text)
    if dry_run:
        return f"dry-run:h3={had_h3}"
    path.write_text(text, encoding="utf-8")
    if had_h3:
        n = len(re.findall(r'details class="lesson-card"', text))
        return f"wrapped:{n}-cards"
    if 'id="foundation-lesson-cards"' in text:
        return "assets-only"
    return "unchanged"


def main() -> None:
    dry = "--dry-run" in sys.argv
    paths = sorted(MATH.glob("foundation-*.html"))
    for path in paths:
        try:
            status = process_file(path, dry_run=dry)
            print(f"{path.name}: {status}")
        except Exception as exc:  # noqa: BLE001
            print(f"{path.name}: ERROR {exc}")


if __name__ == "__main__":
    main()
