"""Generate new trigonometry foundation pages from law-of-cosines shell."""
from __future__ import annotations

import re
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
TEMPLATE = MATH / "foundation-law-of-cosines.html"

EDU_TABLE_CSS = ".mf-article .edu-table-wrap{max-width:100%;overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}.mf-article table{border-collapse:collapse;width:100%;margin:14px 0;display:table;table-layout:fixed}.mf-article .edu-table-wrap table{margin:0}"

PAGES = [
    {
        "file": "foundation-exact-trigonometric-values.html",
        "title_en": "Exact Trigonometric Values | KIWI 爱AI Study",
        "title_zh": "特殊角的精确值 | KIWI 爱AI Study",
        "desc": "Exact sine, cosine, and tangent values from special triangles, extended by reference angles and quadrant signs.",
        "css_v": "20261113-trig-exact",
        "h1_en": "Exact Trigonometric Values",
        "h1_zh": "特殊角的精确值",
        "article": r'''<p data-en="A 45°–45°–90° triangle has side ratio 1 : 1 : √2. A 30°–60°–90° triangle has side ratio 1 : √3 : 2. Use reference angles and quadrant signs to extend these values beyond 90°." data-zh="45°–45°–90° 三角形边长比为 1 : 1 : √2；30°–60°–90° 为 1 : √3 : 2。结合参考角与象限符号可将精确值推广到超过 90°。">A 45°–45°–90° triangle has side ratio 1 : 1 : √2. A 30°–60°–90° triangle has side ratio 1 : √3 : 2. Use reference angles and quadrant signs to extend these values beyond 90°.</p>
<details class="lesson-card" open><summary id="exact-value-table" data-en="Common Exact-Value Table" data-zh="常用精确值表">Common Exact-Value Table</summary><div class="lesson-card-content">
<div class="edu-table-wrap"><table class="edu-table kiwi-edu-table-row-column-header">
<colgroup><col style="width:14%"/><col style="width:28%"/><col style="width:28%"/><col style="width:30%"/></colgroup>
<thead><tr class="header"><th data-en="θ" data-zh="θ">θ</th><th data-en="sin θ" data-zh="sin θ">sin θ</th><th data-en="cos θ" data-zh="cos θ">cos θ</th><th data-en="tan θ" data-zh="tan θ">tan θ</th></tr></thead>
<tbody>
<tr><td>0°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="0" data-tex-zh="0"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="1" data-tex-zh="1"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="0" data-tex-zh="0"></div></td></tr>
<tr><td>30°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{1}{2}" data-tex-zh="\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{2}" data-tex-zh="\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{3}" data-tex-zh="\frac{\sqrt{3}}{3}"></div></td></tr>
<tr><td>45°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{2}}{2}" data-tex-zh="\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{2}}{2}" data-tex-zh="\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="1" data-tex-zh="1"></div></td></tr>
<tr><td>60°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{2}" data-tex-zh="\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{1}{2}" data-tex-zh="\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\sqrt{3}" data-tex-zh="\sqrt{3}"></div></td></tr>
<tr><td>90°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="1" data-tex-zh="1"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="0" data-tex-zh="0"></div></td><td data-en="undefined" data-zh="无定义">undefined</td></tr>
<tr><td>120°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{2}" data-tex-zh="\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{1}{2}" data-tex-zh="-\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\sqrt{3}" data-tex-zh="-\sqrt{3}"></div></td></tr>
<tr><td>135°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{2}}{2}" data-tex-zh="\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{2}}{2}" data-tex-zh="-\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-1" data-tex-zh="-1"></div></td></tr>
<tr><td>150°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{1}{2}" data-tex-zh="\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{2}" data-tex-zh="-\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{3}" data-tex-zh="-\frac{\sqrt{3}}{3}"></div></td></tr>
<tr><td>210°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{1}{2}" data-tex-zh="-\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{2}" data-tex-zh="-\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{3}" data-tex-zh="\frac{\sqrt{3}}{3}"></div></td></tr>
<tr><td>225°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{2}}{2}" data-tex-zh="-\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{2}}{2}" data-tex-zh="-\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="1" data-tex-zh="1"></div></td></tr>
<tr><td>240°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{2}" data-tex-zh="-\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{1}{2}" data-tex-zh="-\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\sqrt{3}" data-tex-zh="\sqrt{3}"></div></td></tr>
<tr><td>300°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{2}" data-tex-zh="-\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{1}{2}" data-tex-zh="\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\sqrt{3}" data-tex-zh="-\sqrt{3}"></div></td></tr>
<tr><td>315°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{2}}{2}" data-tex-zh="-\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{2}}{2}" data-tex-zh="\frac{\sqrt{2}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-1" data-tex-zh="-1"></div></td></tr>
<tr><td>330°</td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{1}{2}" data-tex-zh="-\frac{1}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{\sqrt{3}}{2}" data-tex-zh="\frac{\sqrt{3}}{2}"></div></td><td><div class="kiwi-math-block kiwi-math-latex" data-tex-en="-\frac{\sqrt{3}}{3}" data-tex-zh="-\frac{\sqrt{3}}{3}"></div></td></tr>
</tbody></table></div>
</div></details>
<details class="lesson-card"><summary id="reciprocal-ratios" data-en="Reciprocal Trigonometric Ratios" data-zh="倒数三角比">Reciprocal Trigonometric Ratios</summary><div class="lesson-card-content">
<p data-en="The reciprocal of sine is cosecant (csc), the reciprocal of cosine is secant (sec), and the reciprocal of tangent is cotangent (cot)." data-zh="正弦的倒数是余割（csc），余弦的倒数是正割（sec），正切的倒数是余切（cot）。">The reciprocal of sine is cosecant (csc), the reciprocal of cosine is secant (sec), and the reciprocal of tangent is cotangent (cot).</p>
<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}" data-tex-zh="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}"></div>
<p data-en="These ratios are undefined when their denominators are zero. Do not confuse reciprocal ratios with inverse trigonometric functions (arcsin, arccos, arctan)." data-zh="分母为零时无定义。不要把倒数比与反三角函数（arcsin、arccos、arctan）混淆。">These ratios are undefined when their denominators are zero. Do not confuse reciprocal ratios with inverse trigonometric functions (arcsin, arccos, arctan).</p>
</div></details>''',
    },
    {
        "file": "foundation-sine-law.html",
        "title_en": "The Sine Law | KIWI 爱AI Study",
        "title_zh": "正弦定理 | KIWI 爱AI Study",
        "desc": "Use the Sine Law for oblique triangles, including the SSA ambiguous case.",
        "css_v": "20261113-sine-law",
        "h1_en": "The Sine Law",
        "h1_zh": "正弦定理",
        "article": r'''<p data-en="An oblique triangle is any triangle that is not a right triangle. An acute triangle has all three angles smaller than 90°. An obtuse triangle has one angle greater than 90°." data-zh="斜三角形指非直角三角形。锐角三角形三个角都小于 90°；钝角三角形有一个角大于 90°。">An oblique triangle is any triangle that is not a right triangle. An acute triangle has all three angles smaller than 90°. An obtuse triangle has one angle greater than 90°.</p>
<p data-en="For triangle ABC, side &lt;em&gt;a&lt;/em&gt; is opposite angle &lt;em&gt;A&lt;/em&gt;, side &lt;em&gt;b&lt;/em&gt; opposite &lt;em&gt;B&lt;/em&gt;, and side &lt;em&gt;c&lt;/em&gt; opposite &lt;em&gt;C&lt;/em&gt;." data-zh="在三角形 ABC 中，边 &lt;em&gt;a&lt;/em&gt; 对角 &lt;em&gt;A&lt;/em&gt;，边 &lt;em&gt;b&lt;/em&gt; 对角 &lt;em&gt;B&lt;/em&gt;，边 &lt;em&gt;c&lt;/em&gt; 对角 &lt;em&gt;C&lt;/em&gt;。">For triangle ABC, side <em>a</em> is opposite angle <em>A</em>, side <em>b</em> opposite <em>B</em>, and side <em>c</em> opposite <em>C</em>.</p>
<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}" data-tex-zh="\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}"></div>
<p data-en="Use the Sine Law when a known angle–opposite-side pair is available (ASA, AAS, or SSA). For SAS or SSS, start with the Law of Cosines." data-zh="当有「角—对边」已知对时（ASA、AAS 或 SSA）用正弦定理；SAS 或 SSS 通常从余弦定理入手。">Use the Sine Law when a known angle–opposite-side pair is available (ASA, AAS, or SSA). For SAS or SSS, start with the Law of Cosines.</p>
<details class="lesson-card" open><summary id="ssa-ambiguous" data-en="The SSA Ambiguous Case" data-zh="SSA 歧义情形">The SSA Ambiguous Case</summary><div class="lesson-card-content">
<figure class="trig-beyond-90-figure trig-beyond-90-figure--ssa"><img alt="Oblique triangle labeled with sides and opposite angles" loading="lazy" src="../assets/math/trig-image32.png"/></figure>
<p data-en="When two side lengths and a non-included angle are given (SSA), zero, one, or two distinct oblique triangles may satisfy the data." data-zh="已知两边及一对角（SSA）时，可能无解、一组解或两组解。">When two side lengths and a non-included angle are given (SSA), zero, one, or two distinct oblique triangles may satisfy the data.</p>
<p data-en="Let &lt;em&gt;A&lt;/em&gt; be the known acute angle, &lt;em&gt;a&lt;/em&gt; the side opposite &lt;em&gt;A&lt;/em&gt;, and &lt;em&gt;b&lt;/em&gt; the other known side. The height from the end of side &lt;em&gt;b&lt;/em&gt; to the base ray is:" data-zh="设已知锐角为 &lt;em&gt;A&lt;/em&gt;，其对边为 &lt;em&gt;a&lt;/em&gt;，另一边为 &lt;em&gt;b&lt;/em&gt;。从 &lt;em&gt;b&lt;/em&gt; 一端到基准射线的垂线高度为：">Let <em>A</em> be the known acute angle, <em>a</em> the side opposite <em>A</em>, and <em>b</em> the other known side. The height from the end of side <em>b</em> to the base ray is:</p>
<div class="kiwi-math-block kiwi-math-latex" data-tex-en="h=b\sin A" data-tex-zh="h=b\sin A"></div>
<ul>
<li data-en="&lt;em&gt;a &lt; h&lt;/em&gt; — no triangle" data-zh="&lt;em&gt;a &lt; h&lt;/em&gt; — 无解"><em>a &lt; h</em> — no triangle</li>
<li data-en="&lt;em&gt;a = h&lt;/em&gt; — one right triangle" data-zh="&lt;em&gt;a = h&lt;/em&gt; — 一个直角三角形"><em>a = h</em> — one right triangle</li>
<li data-en="&lt;em&gt;h &lt; a &lt; b&lt;/em&gt; — two distinct triangles" data-zh="&lt;em&gt;h &lt; a &lt; b&lt;/em&gt; — 两个三角形"><em>h &lt; a &lt; b</em> — two distinct triangles</li>
<li data-en="&lt;em&gt;a ≥ b&lt;/em&gt; — exactly one triangle" data-zh="&lt;em&gt;a ≥ b&lt;/em&gt; — 唯一解"><em>a ≥ b</em> — exactly one triangle</li>
</ul>
<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\text{Two triangles when }b\sin A&lt;a&lt;b" data-tex-zh="\text{两解条件：}b\sin A&lt;a&lt;b"></div>
</div></details>
<details class="lesson-card"><summary id="sine-applications" data-en="Using the Sine Law in Applications" data-zh="正弦定理的应用">Using the Sine Law in Applications</summary><div class="lesson-card-content">
<p data-en="Sketch the situation, label each angle and its opposite side, set the calculator to degree mode, choose the matching ratio, and solve." data-zh="画示意图，标出各角及对边，计算器用角度模式，选对比例式求解。">Sketch the situation, label each angle and its opposite side, set the calculator to degree mode, choose the matching ratio, and solve.</p>
<p data-en="If you find &lt;em&gt;sin B = k&lt;/em&gt;, a second candidate angle is &lt;em&gt;180° − B&lt;/em&gt;. Keep it only if all three angles still sum to less than 180°." data-zh="由 &lt;em&gt;sin B = k&lt;/em&gt; 得角 B 后，另一候选为 &lt;em&gt;180° − B&lt;/em&gt;；仅当三内角和仍小于 180° 时保留。">If you find <em>sin B = k</em>, a second candidate angle is <em>180° − B</em>. Keep it only if all three angles still sum to less than 180°.</p>
</div></details>
<details class="lesson-card"><summary id="ssa-example" data-en="Worked Example" data-zh="例题">Worked Example</summary><div class="lesson-card-content">
<p data-en="&lt;em&gt;A = 30°&lt;/em&gt;, &lt;em&gt;b = 10&lt;/em&gt;, &lt;em&gt;a = 8&lt;/em&gt;. First check:&lt;em&gt; h = 10 sin 30° = 5&lt;/em&gt;, and &lt;em&gt;5 &lt; 8 &lt; 10&lt;/em&gt;, so two triangles are possible." data-zh="&lt;em&gt;A = 30°&lt;/em&gt;，&lt;em&gt;b = 10&lt;/em&gt;，&lt;em&gt;a = 8&lt;/em&gt;。&lt;em&gt;h = 10 sin 30° = 5&lt;/em&gt;，且 &lt;em&gt;5 &lt; 8 &lt; 10&lt;/em&gt;，故可能有两解。"><em>A = 30°</em>, <em>b = 10</em>, <em>a = 8</em>. First check: <em>h = 10 sin 30° = 5</em>, and <em>5 &lt; 8 &lt; 10</em>, so two triangles are possible.</p>
<div class="edu-note" data-en="&lt;strong&gt;Note:&lt;/strong&gt; The two-triangle test assumes &lt;em&gt;A&lt;/em&gt; is acute. A right or obtuse given angle does not produce two distinct valid SSA triangles." data-zh="&lt;strong&gt;注意：&lt;/strong&gt; 两解判别假设已知角 &lt;em&gt;A&lt;/em&gt; 为锐角。"><strong>Note:</strong> The two-triangle test assumes <em>A</em> is acute. A right or obtuse given angle does not produce two distinct valid SSA triangles.</div>
</div></details>''',
    },
    {
        "file": "foundation-choosing-trigonometry-laws.html",
        "title_en": "Choosing Sine or Cosine Law | KIWI 爱AI Study",
        "title_zh": "正弦定理与余弦定理的选择 | KIWI 爱AI Study",
        "desc": "Decide between the Sine Law and Law of Cosines, and apply trigonometry in 3D.",
        "css_v": "20261113-choose-trig-law",
        "h1_en": "Choosing Sine or Cosine Law",
        "h1_zh": "正弦定理与余弦定理的选择",
        "article": r'''<p data-en="Once you know both laws, read what is given around the triangle before choosing a formula." data-zh="熟悉两定理后，先看清已知条件再选公式。">Once you know both laws, read what is given around the triangle before choosing a formula.</p>
<details class="lesson-card" open><summary id="choosing-laws" data-en="Which Law to Use" data-zh="选哪条定理">Which Law to Use</summary><div class="lesson-card-content">
<div class="edu-note" data-en="&lt;strong&gt;Quick tip:&lt;/strong&gt; Pair → Sine; Sandwich → Cosine. &lt;em&gt;Pair&lt;/em&gt; = a known angle and its opposite side. &lt;em&gt;Sandwich&lt;/em&gt; = the known angle lies between two known sides (SAS)." data-zh="&lt;strong&gt;口诀：&lt;/strong&gt;「对边成对」→ 正弦；「夹角夹边」→ 余弦。"><strong>Quick tip:</strong> Pair → Sine; Sandwich → Cosine. <em>Pair</em> = a known angle and its opposite side. <em>Sandwich</em> = the known angle lies between two known sides (SAS).</div>
<figure class="trig-beyond-90-figure trig-beyond-90-figure--choose"><img alt="Triangle diagrams marking angle A and opposite pair versus included angle" loading="lazy" src="../assets/math/trig-image39.png"/></figure>
<ul>
<li data-en="ASA or AAS → find the third angle (180°), then use the Sine Law." data-zh="ASA 或 AAS → 先求第三角，再用正弦定理。">ASA or AAS → find the third angle (180°), then use the Sine Law.</li>
<li data-en="SSA → Sine Law first; check the ambiguous case." data-zh="SSA → 先用正弦定理，并检验歧义情形。">SSA → Sine Law first; check the ambiguous case.</li>
<li data-en="SAS → Cosine Law to find the opposite side." data-zh="SAS → 用余弦定理求对边。">SAS → Cosine Law to find the opposite side.</li>
<li data-en="SSS → Cosine Law to find an angle." data-zh="SSS → 用余弦定理求角。">SSS → Cosine Law to find an angle.</li>
</ul>
<p data-en="To finish solving a triangle, you may switch between the two laws. The larger side is opposite the larger angle." data-zh="求完三角形时可在两定理间切换；较大边对等较大角。">To finish solving a triangle, you may switch between the two laws. The larger side is opposite the larger angle.</p>
</div></details>
<details class="lesson-card"><summary id="trig-3d" data-en="Working with Three Dimensions" data-zh="三维应用">Working with Three Dimensions</summary><div class="lesson-card-content">
<p data-en="Use SOH–CAH–TOA, the Sine Law, and the Law of Cosines in 3D by identifying the horizontal plane, vertical height, and slanted segment." data-zh="在三维问题中分清水平面、竖直高度与斜线段，再套用 SOH–CAH–TOA、正弦定理或余弦定理。">Use SOH–CAH–TOA, the Sine Law, and the Law of Cosines in 3D by identifying the horizontal plane, vertical height, and slanted segment.</p>
<p data-en="Draw a 3D sketch, isolate a right or oblique triangle in one plane, solve it, then use the result in the next triangle." data-zh="先画三维示意图，在某一平面内抽出直角或斜三角形，逐层求解。">Draw a 3D sketch, isolate a right or oblique triangle in one plane, solve it, then use the result in the next triangle.</p>
<p data-en="Typical applications include the height of a regular tetrahedron, a diagonal through a rectangular solid, and distances that combine horizontal and vertical parts." data-zh="常见应用包括正四面体的高、长方体对角线，以及水平与竖直分量组合的距离。">Typical applications include the height of a regular tetrahedron, a diagonal through a rectangular solid, and distances that combine horizontal and vertical parts.</p>
</div></details>''',
    },
]


def patch_shell(spec: dict) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    if EDU_TABLE_CSS not in text:
        text = text.replace(
            ".mf-article img{display:block;max-width:100%",
            EDU_TABLE_CSS + ".mf-article img{display:block;max-width:100%",
            1,
        )
    text = re.sub(
        r'<title data-en="[^"]*" data-zh="[^"]*">[^<]*</title>',
        f'<title data-en="{spec["title_en"]}" data-zh="{spec["title_zh"]}">{spec["title_en"].split("|")[0].strip()}</title>',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{spec["desc"]}" name="description"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'href="../assets/css/styles\.css\?v=[^"]*"',
        f'href="../assets/css/styles.css?v={spec["css_v"]}"',
        text,
        count=1,
    )
    article = (
        f'<article class="mf-article mf-chapter"><h1 data-en="{spec["h1_en"]}" data-zh="{spec["h1_zh"]}">{spec["h1_en"]}</h1>\n'
        + spec["article"]
        + "</article>"
    )
    text = re.sub(
        r'<article class="mf-article mf-chapter">.*?</article>',
        lambda _m: article,
        text,
        count=1,
        flags=re.DOTALL,
    )
    # figure scale like beyond-90
    if "trig-beyond-90-figures" not in text:
        fig_css = """<style id="trig-beyond-90-figures">
.mf-article .lesson-card-content .trig-beyond-90-figure{margin:14px 0 6px;text-align:center}
.mf-article .lesson-card-content .trig-beyond-90-figure img{width:100%;height:auto;display:block;margin:0 auto;border:0;border-radius:0;object-fit:contain;box-shadow:none}
.mf-article .lesson-card-content .trig-beyond-90-figure--ssa img{max-width:min(100%,780px)}
.mf-article .lesson-card-content .trig-beyond-90-figure--choose img{max-width:min(100%,720px)}
</style>"""
        text = text.replace("</head>", fig_css + "\n</head>", 1)
    return text


def main():
    for spec in PAGES:
        path = MATH / spec["file"]
        path.write_text(patch_shell(spec), encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
