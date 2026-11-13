"""Create foundation-trigonometry-fundamentals.html hub from an existing trig shell."""
from __future__ import annotations

import re
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
SRC = MATH / "foundation-understanding-trigonometry.html"
DST = MATH / "foundation-trigonometry-fundamentals.html"

CTA_CSS = (
    ".edu-topic-cta{grid-column:1 / -1;grid-row:2;justify-self:end;align-self:center;"
    "white-space:nowrap;max-width:100%;font-size:inherit;font-weight:inherit;"
    "color:inherit;text-align:right;line-height:1.4}"
)

ARTICLE = """<article class="mf-article mf-chapter"><h1 data-en="Trigonometry Fundamentals" data-zh="三角学基础">Trigonometry Fundamentals</h1>
<p class="edu-lead" data-en="Choose a lesson to explore right triangles and the basic trigonometric ratios." data-zh="选择一课，学习直角三角形与基本三角比。">Choose a lesson to explore right triangles and the basic trigonometric ratios.</p>
<div class="edu-topic-list">
<a class="edu-topic edu-topic-link edu-topic-active" href="foundation-understanding-trigonometry.html"><span class="edu-topic-number">1</span><div><h3 data-en="Understanding Trigonometry" data-zh="认识三角函数">Understanding Trigonometry</h3><p data-en="What trigonometry studies and why it matters in real life." data-zh="三角学研究什么，以及它在生活中的用途。">What trigonometry studies and why it matters in real life.</p></div><span class="edu-topic-cta" data-en="Open lesson →" data-zh="打开课程 →">Open lesson →</span></a>
<a class="edu-topic edu-topic-link edu-topic-active" href="foundation-the-three-sides-of-a-right-triangle.html"><span class="edu-topic-number">2</span><div><h3 data-en="The Three Sides of a Right Triangle" data-zh="直角三角形的三条边">The Three Sides of a Right Triangle</h3><p data-en="Identify the hypotenuse, opposite, and adjacent sides relative to an angle." data-zh="根据一个角辨认斜边、对边与邻边。">Identify the hypotenuse, opposite, and adjacent sides relative to an angle.</p></div><span class="edu-topic-cta" data-en="Open lesson →" data-zh="打开课程 →">Open lesson →</span></a>
<a class="edu-topic edu-topic-link edu-topic-active" href="foundation-the-four-basic-trigonometric-ratios.html"><span class="edu-topic-number">3</span><div><h3 data-en="The Four Basic Trigonometric Ratios" data-zh="四个基本三角比">The Four Basic Trigonometric Ratios</h3><p data-en="Define sine, cosine, tangent, and cotangent using side ratios." data-zh="用边的比值定义 sin、cos、tan 与 cot。">Define sine, cosine, tangent, and cotangent using side ratios.</p></div><span class="edu-topic-cta" data-en="Open lesson →" data-zh="打开课程 →">Open lesson →</span></a>
</div>
</article>"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = re.sub(
        r"<title[^>]*>.*?</title>",
        '<title data-en="Trigonometry Fundamentals | KIWI 爱AI Study" data-zh="三角学基础 | KIWI 爱AI Study">'
        "Trigonometry Fundamentals | KIWI 爱AI Study</title>",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if CTA_CSS not in text:
        text = text.replace(
            "@media(max-width:760px){.edu-topic{",
            CTA_CSS + "@media(max-width:760px){.edu-topic{",
        )
    text = re.sub(
        r"<article class=\"mf-article mf-chapter\">.*?</article>",
        ARTICLE,
        text,
        count=1,
        flags=re.DOTALL,
    )
    DST.write_text(text, encoding="utf-8")
    print("wrote", DST.name)


if __name__ == "__main__":
    main()
