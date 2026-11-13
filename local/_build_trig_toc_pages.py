"""Create/split trigonometry pages for book TOC structure."""
from __future__ import annotations

import re
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
SHELL = MATH / "foundation-understanding-trigonometry.html"


def shell_page(
    filename: str,
    title_en: str,
    title_zh: str,
    desc: str,
    css_v: str,
    article: str,
) -> None:
    text = SHELL.read_text(encoding="utf-8")
    text = re.sub(
        r'<title[^>]*>[^<]*</title>',
        f'<title data-en="{title_en} | KIWI 爱AI Study" data-zh="{title_zh} | KIWI 爱AI Study">'
        f"{title_en.split('|')[0].strip()}</title>",
        text,
        count=1,
    )
    text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{desc}" name="description"/>',
        text,
        count=1,
    )
    text = re.sub(
        r'href="../assets/css/styles\.css\?v=[^"]*"',
        f'href="../assets/css/styles.css?v={css_v}"',
        text,
        count=1,
    )
    art = (
        f'<article class="mf-article mf-chapter"><h1 data-en="{title_en}" data-zh="{title_zh}">'
        f"{title_en}</h1>\n{article}</article>"
    )
    text = re.sub(
        r'<article class="mf-article mf-chapter">.*?</article>',
        lambda _m: art,
        text,
        count=1,
        flags=re.DOTALL,
    )
    (MATH / filename).write_text(text, encoding="utf-8")
    print("wrote", filename)


def extract_between(html: str, start_marker: str, end_marker: str | None) -> str:
    i = html.find(start_marker)
    if i < 0:
        return ""
    j = html.find(end_marker, i) if end_marker else len(html)
    return html[i : j]


def main():
    beyond = (MATH / "foundation-trigonometric-ratios-beyond-90.html").read_text(encoding="utf-8")

    m_std = re.search(
        r'<h2 id="angles-standard-position".*?'
        r'(<details class="lesson-card"><summary id="initial-terminal-arm".*?'
        r'</details>\s*<details class="lesson-card"><summary id="primary-on-plane".*?'
        r'</details>\s*<details class="lesson-card"><summary id="signs-four-quadrants".*?'
        r"</details>)",
        beyond,
        re.DOTALL,
    )
    std_block = m_std.group(1) if m_std else ""
    related_block = extract_between(
        beyond,
        '<details class="lesson-card"><summary id="related-acute-angle"',
        '<h2 id="ratios-beyond-90"',
    )
    # related block should not include std h2 - fix: take from related through coterminal closing only
    m_rel = re.search(
        r'(<details class="lesson-card"><summary id="related-acute-angle".*?</details>\s*'
        r'<details class="lesson-card"><summary id="coterminal-angles".*?</details>)',
        beyond,
        re.DOTALL,
    )
    related_only = m_rel.group(1) if m_rel else ""

    beyond_body = extract_between(beyond, '<h2 id="ratios-beyond-90"', "</article>")

    shell_page(
        "foundation-angles-in-standard-position.html",
        "Angles in Standard Position",
        "标准位置角",
        "Initial and terminal arms, primary ratios on the coordinate plane, and quadrant signs.",
        "20261113-trig-std-pos",
        std_block,
    )

    shell_page(
        "foundation-related-and-coterminal-angles.html",
        "Related and Coterminal Angles",
        "相关角与同界角",
        "Reference angles and coterminal angles on the coordinate plane.",
        "20261113-trig-related",
        related_only,
    )

    # Trim beyond-90 page article
    beyond_new = (
        '<article class="mf-article mf-chapter"><h1 data-en="Trigonometric Ratios Beyond 90°" '
        'data-zh="超过90°的三角比">Trigonometric Ratios Beyond 90°</h1>\n'
        + beyond_body
        + "</article>"
    )
    beyond = re.sub(
        r'<article class="mf-article mf-chapter">.*?</article>',
        lambda _m: beyond_new,
        beyond,
        count=1,
        flags=re.DOTALL,
    )
    (MATH / "foundation-trigonometric-ratios-beyond-90.html").write_text(beyond, encoding="utf-8")
    print("trimmed foundation-trigonometric-ratios-beyond-90.html")

    exact = (MATH / "foundation-exact-trigonometric-values.html").read_text(encoding="utf-8")
    exact = re.sub(
        r'<details class="lesson-card"><summary id="reciprocal-ratios".*?</details>\s*',
        "",
        exact,
        count=1,
        flags=re.DOTALL,
    )
    (MATH / "foundation-exact-trigonometric-values.html").write_text(exact, encoding="utf-8")
    print("trimmed exact values page")

    reciprocal_art = r'''<p data-en="The reciprocal of sine is cosecant (csc), the reciprocal of cosine is secant (sec), and the reciprocal of tangent is cotangent (cot)." data-zh="正弦的倒数是余割（csc），余弦的倒数是正割（sec），正切的倒数是余切（cot）。">The reciprocal of sine is cosecant (csc), the reciprocal of cosine is secant (sec), and the reciprocal of tangent is cotangent (cot).</p>
<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}" data-tex-zh="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}"></div>
<p data-en="These ratios are undefined when their denominators are zero. Do not confuse reciprocal ratios with inverse trigonometric functions (arcsin, arccos, arctan)." data-zh="分母为零时无定义。不要把倒数比与反三角函数（arcsin、arccos、arctan）混淆。">These ratios are undefined when their denominators are zero. Do not confuse reciprocal ratios with inverse trigonometric functions (arcsin, arccos, arctan).</p>'''
    shell_page(
        "foundation-reciprocal-trigonometric-ratios.html",
        "Reciprocal Trigonometric Ratios",
        "倒数三角比",
        "Cosecant, secant, and cotangent as reciprocals of sine, cosine, and tangent.",
        "20261113-trig-recip-ratio",
        reciprocal_art,
    )

    sine = (MATH / "foundation-sine-law.html").read_text(encoding="utf-8")
    m_ssa = re.search(
        r'(<h2 id="ssa-ambiguous-case".*?</details>\s*</article>)',
        sine,
        re.DOTALL,
    )
    ssa_block = ""
    if m_ssa:
        ssa_block = m_ssa.group(1).replace("</article>", "").replace(
            '<h2 id="ssa-ambiguous-case" data-en="SSA Ambiguous Case (Sine Law)" data-zh="SSA 歧义情形（正弦定理）">SSA Ambiguous Case (Sine Law)</h2>',
            "",
        )
        sine = sine[: m_ssa.start()] + "</article>" + sine[m_ssa.end() :]

    shell_page(
        "foundation-ssa-ambiguous-case.html",
        "SSA Ambiguous Case (Sine Law)",
        "SSA 歧义情形（正弦定理）",
        "Height test, compass construction, and when two oblique triangles are possible.",
        "20261113-trig-ssa",
        ssa_block,
    )
    (MATH / "foundation-sine-law.html").write_text(sine, encoding="utf-8")
    print("split sine / ssa pages")

    choose = (MATH / "foundation-choosing-trigonometry-laws.html").read_text(encoding="utf-8")
    m_3d = re.search(
        r'<h2 id="trig-3d-heading".*?</details>\s*<h2 id="choosing-laws-heading"',
        choose,
        re.DOTALL,
    )
    if m_3d:
        d3 = m_3d.group(0)
        d3_inner = re.sub(r"<h2[^>]*>.*?</h2>", "", d3, count=1)
        d3_inner = d3_inner.replace('<h2 id="choosing-laws-heading"', "").split("<h2")[0]
        shell_page(
            "foundation-trigonometry-3d-applications.html",
            "Applications in 3D Settings",
            "三维应用",
            "Use trigonometry laws in three dimensions with layered triangles.",
            "20261113-trig-3d",
            d3_inner,
        )
        choose = choose.replace(m_3d.group(0), '<h2 id="choosing-laws-heading"', 1)

    (MATH / "foundation-choosing-trigonometry-laws.html").write_text(choose, encoding="utf-8")
    print("split 3d / choosing pages")

    identity_pages = [
        (
            "foundation-what-is-trigonometric-identity.html",
            "What Is an Identity?",
            "什么是恒等式？",
            "A trigonometric identity is true for every angle where both sides are defined.",
            r'''<p data-en="A trigonometric identity is an equation that is true for every angle for which both sides are defined. Identities can be used to simplify expressions and prove two forms are equivalent." data-zh="三角恒等式是在两边均有定义的每个角上都成立的等式，可用于化简式子或证明两种形式等价。">A trigonometric identity is an equation that is true for every angle for which both sides are defined. Identities can be used to simplify expressions and prove two forms are equivalent.</p>''',
        ),
        (
            "foundation-pythagorean-identity.html",
            "Pythagorean Identity",
            "勾股恒等式",
            "The fundamental relationship between sine and cosine.",
            r'''<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\sin^2\theta+\cos^2\theta=1" data-tex-zh="\sin^2\theta+\cos^2\theta=1"></div>
<p data-en="This follows from the unit circle and the Pythagorean theorem on the right triangle formed by &lt;em&gt;x&lt;/em&gt;, &lt;em&gt;y&lt;/em&gt;, and &lt;em&gt;r = 1&lt;/em&gt;." data-zh="由单位圆及由 &lt;em&gt;x&lt;/em&gt;、&lt;em&gt;y&lt;/em&gt;、&lt;em&gt;r = 1&lt;/em&gt; 构成的直角三角形与勾股定理可得。">This follows from the unit circle and the Pythagorean theorem on the right triangle formed by <em>x</em>, <em>y</em>, and <em>r = 1</em>.</p>''',
        ),
        (
            "foundation-quotient-identities.html",
            "Quotient Identities",
            "商恒等式",
            "Tangent and cotangent in terms of sine and cosine.",
            r'''<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\tan\theta=\frac{\sin\theta}{\cos\theta},\quad \cot\theta=\frac{\cos\theta}{\sin\theta}" data-tex-zh="\tan\theta=\frac{\sin\theta}{\cos\theta},\quad \cot\theta=\frac{\cos\theta}{\sin\theta}"></div>
<p data-en="These hold wherever the denominators are nonzero." data-zh="在分母不为零时成立。">These hold wherever the denominators are nonzero.</p>''',
        ),
        (
            "foundation-reciprocal-identities.html",
            "Reciprocal Identities",
            "倒数恒等式",
            "Relate csc, sec, and cot to sin, cos, and tan.",
            r'''<div class="kiwi-math-block kiwi-math-latex" data-tex-en="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}" data-tex-zh="\csc\theta=\frac{1}{\sin\theta},\quad \sec\theta=\frac{1}{\cos\theta},\quad \cot\theta=\frac{1}{\tan\theta}"></div>''',
        ),
        (
            "foundation-proving-trigonometric-identities.html",
            "Strategies for Proving Trigonometric Identities",
            "证明三角恒等式的策略",
            "Work from the complicated side and convert to sine and cosine.",
            r'''<p data-en="Begin with the more complicated side. Convert sec, csc, cot, and tan to sine and cosine when useful. Look for common denominators, factoring, expansion, and the Pythagorean identity. Work on one side until it matches the other; do not assume the identity is already true." data-zh="从较复杂的一边入手。必要时把 sec、csc、cot、tan 化为 sin 与 cos。寻找通分、因式分解、展开与勾股恒等式。只化简一边直到与另一边相同；不要默认恒等式已成立。">Begin with the more complicated side. Convert sec, csc, cot, and tan to sine and cosine when useful. Look for common denominators, factoring, expansion, and the Pythagorean identity. Work on one side until it matches the other; do not assume the identity is already true.</p>
<p data-en="Useful algebra: factor expressions, combine fractions, multiply numerator and denominator by the same nonzero expression, and use conjugates where appropriate. State domain restrictions if a denominator could be zero." data-zh="可用代数：因式分解、合并分式、分子分母同乘非零式、必要时用共轭。若分母可能为零，应说明定义域限制。">Useful algebra: factor expressions, combine fractions, multiply numerator and denominator by the same nonzero expression, and use conjugates where appropriate. State domain restrictions if a denominator could be zero.</p>''',
        ),
        (
            "foundation-trigonometric-identities-quick-checks.html",
            "Quick Checks",
            "快速检验",
            "Short practice items for trigonometric identities.",
            r'''<ol>
<li data-en="Simplify cos(135°) × tan(135°)." data-zh="化简 cos(135°) × tan(135°)。">Simplify cos(135°) × tan(135°).</li>
<li data-en="Show that tan θ × cos θ = sin θ whenever defined." data-zh="证明在定义域内 tan θ × cos θ = sin θ。">Show that tan θ × cos θ = sin θ whenever defined.</li>
<li data-en="Explain why csc θ is undefined when sin θ = 0." data-zh="说明为何 sin θ = 0 时 csc θ 无定义。">Explain why csc θ is undefined when sin θ = 0.</li>
</ol>''',
        ),
    ]
    for fname, en, zh, desc, body in identity_pages:
        body_fix = body.replace("klpi-math-latex", "kiwi-math-latex")
        shell_page(fname, en, zh, desc, "20261113-trig-id", body_fix)


if __name__ == "__main__":
    main()
