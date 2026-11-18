"""Rebuild thinking-imaginary-complex-numbers.html from Advanced docx content."""
from __future__ import annotations

import html
import io
import re
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DOCX = Path(r"D:\YuanSync\Mirror\MyAI\math-quick-ref-chatGPT\math-quick-ref_advanced.docx")
PAGE = ROOT / "math" / "thinking-imaginary-complex-numbers.html"
ASSETS = ROOT / "assets"

FIG_MAP = [
    ("media/image2.jpg", "complex-argand-4plus3i.webp", "Argand plane showing 4 + 3i"),
    ("media/image3.png", "complex-multiply-by-i.webp", "Multiplying 2 + i by i"),
    ("media/image4.jpeg", "complex-four-i-rotations.webp", "Four multiplications by i"),
    ("media/image5.jpeg", "complex-distance-modulus.webp", "Distance between complex numbers"),
    ("media/image6.jpeg", "complex-sine-projection.webp", "Rotating vector and sine projection"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def mb(tex: str) -> str:
    t = esc(tex)
    return (
        f'<div class="kiwi-math-block kiwi-math-latex" data-tex-en="{t}" '
        f'data-tex-zh="{t}"></div>'
    )


def mi(tex: str) -> str:
    t = esc(tex)
    return (
        f'<span class="kiwi-math-latex kiwi-katex-inline" data-tex-en="{t}" '
        f'data-tex-zh="{t}"></span>'
    )


def p(en: str, zh: str) -> str:
    return (
        f'<p data-en="{esc(en)}" data-zh="{esc(zh)}">{en}</p>'
    )


def li(en: str, zh: str) -> str:
    return f'<li data-en="{esc(en)}" data-zh="{esc(zh)}">{en}</li>'


def fig(
    src: str,
    alt_en: str,
    alt_zh: str,
    cap_en: str,
    cap_zh: str,
    *,
    width: int = 520,
    scale_class: str = "",
) -> str:
    cls = "nf-figure word-figure kiwi-figure-centered"
    if scale_class:
        cls += f" {scale_class}"
    return (
        f'<figure class="{cls}">'
        f'<img alt="{esc(alt_en)}" src="../assets/{src}" width="{width}" loading="lazy"/>'
        f'<figcaption data-en="{esc(cap_en)}" data-zh="{esc(cap_zh)}">{cap_en}</figcaption>'
        f"</figure>"
    )


def card(title_en: str, title_zh: str, inner: str, open_first: bool = False) -> str:
    o = ' open=""' if open_first else ""
    return (
        f'<details class="lesson-card"{o}>'
        f'<summary data-en="{esc(title_en)}" data-zh="{esc(title_zh)}">{title_en}</summary>'
        f'<div class="lesson-card-content">{inner}</div></details>'
    )


def extract_figures() -> None:
    with zipfile.ZipFile(DOCX) as z:
        for media, out_name, _alt in FIG_MAP:
            data = z.read(f"word/{media}")
            im = Image.open(io.BytesIO(data))
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            out = ASSETS / out_name
            im.save(out, "WEBP", quality=88)
            print("wrote", out.relative_to(ROOT))


def build_body() -> str:
    # abbreviated zh mirrors EN; formulas identical in both languages
    intro_en = (
        "Advanced extension on number families: how complex numbers arise from algebra, "
        "gain geometric meaning on a plane, and describe rotation, waves, and physical motion."
    )
    intro_zh = (
        "数族的进阶延伸：复数如何从代数中产生、在复平面上获得几何意义，并描述旋转、波动与物理运动。"
    )

    s1 = ""
    s1 += p(
        "Number systems expanded whenever familiar numbers could not solve a problem. "
        "This progression leads naturally to complex numbers.",
        "每当现有数系无法解决问题，数学家便扩展数系；这一历程自然引向复数。",
    )
    s1 += "<ul>"
    s1 += li(
        f"<strong>Natural numbers</strong> — counting with {mi('1,2,3,\\ldots')}.",
        f"<strong>自然数</strong>——用于计数 {mi('1,2,3,\\ldots')}。",
    )
    s1 += li(
        f"<strong>Fractions</strong> — sharing: three oranges for four children gives "
        f"{mi('3 \\div 4 = \\dfrac{3}{4}')}.",
        f"<strong>分数</strong>——分配：3 个橘子分给 4 个孩子，每人得 {mi('3 \\div 4 = \\dfrac{3}{4}')}。",
    )
    s1 += li(
        f"<strong>Negative numbers</strong> — net balance: {mi('2-6=-4')}.",
        f"<strong>负数</strong>——净余额：{mi('2-6=-4')}。",
    )
    s1 += li(
        f"<strong>Rational numbers</strong> — ratios {mi('\\dfrac{a}{b}')}, "
        f"{mi('a,b\\in\\mathbb{Z},\\ b\\neq 0')} (e.g. {mi('-4')}, {mi('0')}, "
        f"{mi('\\dfrac{3}{4}')}, {mi('\\dfrac{5}{2}')}).",
        f"<strong>有理数</strong>——整数之比 {mi('\\dfrac{a}{b}')}，{mi('a,b\\in\\mathbb{Z},\\ b\\neq 0')}。",
    )
    s1 += li(
        f"<strong>Irrational numbers</strong> — a square of side {mi('2')} has diagonal "
        f"{mi('d=\\sqrt{2^2+2^2}=2\\sqrt{2}')}; {mi('\\sqrt{2}')} is irrational.",
        f"<strong>无理数</strong>——边长为 {mi('2')} 的正方形对角线为 {mi('2\\sqrt{2}')}，{mi('\\sqrt{2}')} 无理。",
    )
    s1 += li(
        f"<strong>Real numbers</strong> {mi('\\mathbb{R}')} — rationals and irrationals on one line, "
        "yet still not enough for every polynomial.",
        f"<strong>实数</strong> {mi('\\mathbb{R}')}——有理数与无理数填满数轴，但仍不能解所有多项式方程。",
    )
    s1 += "</ul>"

    s2 = p("Consider the equation that has no real solution:", "考虑下面在实数范围内无解的方程：")
    s2 += mb("x^2=-1")
    s2 += p(
        f"For every real {mi('x')}, we have {mi('x^2\\ge 0')}. Define the imaginary unit "
        f"{mi('i')} by {mi('i^2=-1')}.",
        f"对任意实数 {mi('x')}，有 {mi('x^2\\ge 0')}。定义虚数单位 {mi('i')}：{mi('i^2=-1')}。",
    )
    s2 += mb("x^2+25=0 \\quad\\Rightarrow\\quad x=\\pm 5i")
    s2 += p(
        f"{mi('i')} is not a point on the real line; it belongs to an enlarged number system.",
        f"{mi('i')} 不在实轴上，而属于扩展后的数系。",
    )

    s3 = p(
        "In the 16th century, cubics could produce complex intermediate steps even when the "
        "final roots are real (<em>casus irreducibilis</em>).",
        "16 世纪解三次方程时，即使最终根为实数，中间步骤也会出现复数（不可约情形）。",
    )
    s3 += mb("x^3-15x+22=0")
    s3 += p(f"Check {mi('x=2')}: {mi('2^3-15\\cdot 2+22=0')}.", f"验证 {mi('x=2')}：{mi('2^3-15\\cdot 2+22=0')}。")
    s3 += p("Cardano’s formula can involve negative square roots:", "卡尔达诺公式中可出现负数的平方根：")
    s3 += mb(
        "x=\\sqrt[3]{-11+2i}+\\sqrt[3]{-11-2i}"
    )
    s3 += p(f"Since {mi('\\sqrt{-4}=2i')}:", f"因为 {mi('\\sqrt{-4}=2i')}：")
    s3 += mb("x=\\sqrt[3]{-11+2i}+\\sqrt[3]{-11-2i}")
    s3 += mb("(1+2i)^3=-11-2i,\\qquad (1-2i)^3=-11+2i")
    s3 += mb("x=(1+2i)+(1-2i)=2")
    s3 += p(
        "Imaginary parts cancel; complex numbers are essential intermediates for a real answer.",
        "虚部相消；复数是得到实数解的必要中间步骤。",
    )

    s4 = mb("z=a+bi,\\qquad a,b\\in\\mathbb{R}")
    s4 += p(
        f"Real part {mi('\\operatorname{Re}z=a')}, imaginary part {mi('\\operatorname{Im}z=b')}. "
        f"Example: {mi('z=4+3i')} → point {mi('(4,3)')} (Argand plane).",
        f"实部 {mi('\\operatorname{Re}z=a')}，虚部 {mi('\\operatorname{Im}z=b')}。例如 {mi('z=4+3i')} 对应点 {mi('(4,3)')}（Argand 平面）。",
    )
    s4 += fig(
        "complex-argand-4plus3i.webp",
        "The complex number 4 + 3i in the Argand plane",
        "复平面上 4 + 3i",
        "Figure 1. The complex number 4 + 3i in the Argand plane.",
        "图 1. Argand 平面上复数 4 + 3i。",
    )

    s5 = p("Successive multiplication by i:", "连续乘以 i：")
    s5 += mb("1 \\xrightarrow{\\times i} i \\xrightarrow{\\times i} -1 \\xrightarrow{\\times i} -i \\xrightarrow{\\times i} 1")
    s5 += p(
        f"Each multiplication by {mi('i')} rotates a point {mi('90^\\circ')} counterclockwise about the origin.",
        f"每次乘以 {mi('i')} 使点绕原点逆时针旋转 {mi('90^\\circ')}。",
    )
    s5 += p(f"For {mi('z=a+bi')}:", f"设 {mi('z=a+bi')}：")
    s5 += mb("iz=-b+ai")
    s5 += p(
        f"Point {mi('(a,b)')} maps to {mi('(-b,a)')} — the rule for a {mi('90^\\circ')} turn.",
        f"点 {mi('(a,b)')} 变为 {mi('(-b,a)')}，即逆时针转 {mi('90^\\circ')} 的坐标法则。",
    )
    s5 += fig(
        "complex-multiply-by-i.webp",
        "Multiplying 2 + i by i",
        "2 + i 乘以 i",
        "Figure 2. Multiplying z = 2 + i by i gives −1 + 2i.",
        "图 2. z = 2 + i 乘以 i 得 −1 + 2i。",
    )
    s5 += fig(
        "complex-four-i-rotations.webp",
        "Four multiplications by i",
        "连续四次乘以 i",
        "Figure 2A. Four multiplications by i complete one full rotation.",
        "图 2A. 四次乘以 i 完成一整圈旋转。",
    )

    s6 = p("Modulus (length) and argument (direction from the positive real axis):", "模（长度）与辐角（自正实轴起算的方向）：")
    s6 += mb("|z|=\\sqrt{a^2+b^2}")
    s6 += p(f"Example: {mi('z=5+12i')} gives {mi('|z|=13')}.", f"例：{mi('z=5+12i')} 时 {mi('|z|=13')}。")
    s6 += mb("z=r(\\cos\\theta+i\\sin\\theta),\\qquad \\tan\\theta=\\dfrac{b}{a}\\ \\text{(Q I)}")
    s6 += p("Distance between two complex numbers:", "两复数对应点之间的距离：")
    s6 += mb("d=|z_2-z_1|")
    s6 += p(f"Example: {mi('z_1=1+2i')}, {mi('z_2=4+6i')} → {mi('d=|3+4i|=5')}.", f"例：{mi('z_1=1+2i')}, {mi('z_2=4+6i')} → {mi('d=5')}。")
    s6 += fig(
        "complex-distance-modulus.webp",
        "Distance between complex numbers",
        "两复数之间的距离",
        "Figure 3. Distance uses the Pythagorean theorem.",
        "图 3. 距离满足勾股定理。",
    )

    s7 = p(
        "A vector of length A at angular speed ω with initial phase φ has projections:",
        "长度为 A、角速度 ω、初相 φ 的旋转向量的投影为：",
    )
    s7 += mb("y(t)=A\\sin(\\omega t+\\phi)")
    s7 += mb("x(t)=A\\cos(\\omega t+\\phi)")
    s7 += p(
        "Circular motion projected onto an axis produces sinusoidal motion. "
        f"Frequency {mi('f=\\dfrac{\\omega}{2\\pi}')}, period {mi('T=\\dfrac{2\\pi}{\\omega}')}.",
        f"圆周运动在轴上的投影为正弦运动；频率 {mi('f=\\omega/(2\\pi)')}，周期 {mi('T=2\\pi/\\omega')}。",
    )
    s7 += fig(
        "complex-sine-projection.webp",
        "Sine wave from a rotating vector",
        "旋转向量产生正弦波",
        "Figure 4. A rotating vector produces a sinusoidal vertical projection.",
        "图 4. 旋转向量的竖直投影为正弦曲线。",
        width=676,
        scale_class="kiwi-figure-scale-130",
    )

    s8 = "<ul>"
    s8 += li(
        "<strong>Spring–mass</strong> (undamped): simple harmonic motion.",
        "<strong>弹簧—质量</strong>（无阻尼）：简谐运动。",
    )
    s8 += li(
        "<strong>Pendulum</strong> (small angle): approximately sinusoidal.",
        "<strong>单摆</strong>（小角）：近似正弦运动。",
    )
    s8 += li(
        f"<strong>AC voltage</strong> — e.g. {mi('V=V_0\\sin(\\omega t)')}.",
        f"<strong>交流电压</strong>——如 {mi('V=V_0\\sin(\\omega t)')}。",
    )
    s8 += li(
        "Waves and signals: a complex amplitude encodes size and phase; "
        f"{mi('e^{i\\omega t}')} tracks phase in time.",
        "波与信号：复振幅同时编码大小与相位；时间演化常用指数相位因子表示。",
    )
    s8 += "</ul>"

    s9 = mb("e^{i\\theta}=\\cos\\theta+i\\sin\\theta")
    s9 += mb("z=r e^{i\\theta}=r(\\cos\\theta+i\\sin\\theta)")
    s9 += mb("(r_1 e^{i\\theta_1})(r_2 e^{i\\theta_2})=r_1 r_2\\, e^{i(\\theta_1+\\theta_2)}")
    s9 += p(
        "Multiplication scales magnitudes and adds angles — ideal for rotation, phase, and periodic signals.",
        "乘法放大模长、相加辐角——非常适合描述旋转、相位与周期信号。",
    )

    s10 = p(
        "In quantum mechanics the wavefunction ψ is complex-valued. The time-dependent Schrödinger equation uses i:",
        "量子力学中波函数 ψ 一般为复值；含时薛定谔方程中出现 i：",
    )
    s10 += mb("i\\hbar\\frac{\\partial\\psi}{\\partial t}=\\hat{H}\\psi")
    s10 += p(
        "A full treatment is beyond this lesson; the form shows why complex numbers remain central in modern physics.",
        "完整理论超出本课范围；此式说明复数在现代物理中的核心地位。",
    )

    s11 = "<ul>"
    takeaways = [
        (f"{mi('i^2=-1')} extends the reals.", f"{mi('i^2=-1')} 扩展实数系。"),
        ("Complex numbers live on a plane with real and imaginary parts.", "复数由实部、虚部组成，对应平面上的点。"),
        (f"Multiplying by {mi('i')} is a {mi('90^\\circ')} counterclockwise rotation.", f"乘以 {mi('i')} 等价于逆时针 {mi('90^\\circ')} 旋转。"),
        ("Modulus and argument give magnitude and direction.", "模与辐角描述大小与方向。"),
        ("Uniform circular motion links to sine and cosine.", "匀速圆周运动与正弦、余弦紧密相联。"),
        ("Complex numbers unify oscillations, phases, and waves.", "复数统一了振动、相位与波动。"),
    ]
    for en, zh in takeaways:
        s11 += li(en, zh)
    s11 += "</ul>"
    s11 += p(
        "<strong>Mathematical insight:</strong> Mathematics reveals structures shared by algebra, geometry, and physical motion.",
        "<strong>数学感悟：</strong>数学揭示代数、几何与物理运动之间的共同结构。",
    )

    s12 = '<ol class="kiwi-numbered-steps">'
    s12 += li(f"Solve {mi('x^2+4=0')} in ℂ.", f"在复数范围内解 {mi('x^2+4=0')}。")
    s12 += li(f"Plot {mi('3+4i')} and find {mi('|z|')}.", f"作图 {mi('3+4i')} 并求模。")
    s12 += li(f"For {mi('z=2+3i')}, compute {mi('iz')} and interpret geometrically.", f"对 {mi('z=2+3i')} 计算 {mi('iz')} 并解释几何意义。")
    s12 += li(f"Starting at {mi('1')}, find {mi('i')}, {mi('i^2')}, {mi('i^3')}, {mi('i^4')} under repeated multiplication.", f"从 {mi('1')} 出发，连续乘以 {mi('i')} 得 {mi('i,i^2,i^3,i^4')}。")
    s12 += li(
        f"A vector has {mi('A=2')}, {mi('\\omega=3\\ \\text{rad/s}')}, {mi('\\phi=\\pi/4')}. Write {mi('y(t)')}.",
        f"向量 {mi('A=2')}, {mi('\\omega=3\\ \\text{rad/s}')}, {mi('\\phi=\\pi/4')}，写出 {mi('y(t)')}。",
    )
    s12 += li(
        "Explain why complex intermediates can appear when a real solution is sought.",
        "说明为何求实数解时仍会出现复数中间量。",
    )
    s12 += "</ol>"
    s12 += p("<strong>Answers (check)</strong>", "<strong>核对答案</strong>")
    s12 += mb("x=\\pm 2i")
    s12 += mb("|3+4i|=5")
    s12 += mb("iz=-3+2i\\quad\\text{(90}^\\circ\\text{ rotation)}")
    s12 += mb("i,\\ -1,\\ -i,\\ 1")
    s12 += mb("y(t)=2\\sin\\left(3t+\\dfrac{\\pi}{4}\\right)")
    s12 += p(
        "Algebraic methods may pass through complex values before returning real roots (see the cubic example).",
        "代数方法可能在得到实根之前经过复数中间步骤（见三次方程例）。",
    )

    inner = (
        f'<p class="topic-intro" data-en="{esc(intro_en)}" data-zh="{esc(intro_zh)}">{intro_en}</p>'
        '<aside class="kiwi-word-info-panel kiwi-skill-crosslink-panel" role="note">'
        '<div class="kiwi-panel-heading"><span aria-hidden="true" class="kiwi-panel-icon">🔗</span></div>'
        + p(
            "<strong>Lesson scope:</strong> <strong>Advanced</strong> — from number-family motivation through "
            "the complex plane, rotation, waves, Euler’s formula, and physical models (Math Quick Reference Advanced).",
            "<strong>本课范围：</strong><strong>进阶</strong>——从数族动机到复平面、旋转、波动、欧拉公式与物理模型（进阶版数学速查）。",
        )
        + p(
            '<strong>Also see:</strong> Number family definitions and basic complex-plane picture in '
            '<a href="/foundation-number-families">Number Families</a> (Math Foundations).',
            '<strong>亦可参阅：</strong>数族定义与复平面初图见数学基础中的 '
            '<a href="/foundation-number-families">数的家族</a>。',
        )
        + "</aside>"
        + card("When familiar numbers are not enough", "熟悉数不够用的时候", s1, True)
        + card("The equation that challenges the reals", "挑战实数的方程", s2)
        + card("A surprising cubic equation", "出人意料的三次方程", s3)
        + card("Giving numbers a second dimension", "给数第二个维度", s4)
        + card("Multiplication by i: a quarter-turn", "乘以 i：四分之一圈", s5)
        + card("Magnitude and direction", "大小与方向", s6)
        + card("From circular motion to sine waves", "从圆周运动到正弦波", s7)
        + card("Physical phenomena", "物理现象", s8)
        + card("Euler’s formula and multiplication", "欧拉公式与乘法", s9)
        + card("A glimpse of quantum mechanics", "量子力学一瞥", s10)
        + card("Key takeaways", "要点回顾", s11)
        + card("Practice problems", "练习题", s12)
    )

    sidebar = (
        '<aside aria-label="Topic navigation" class="kiwi-topic-sidebar">'
        '<a data-en="Greatest Common Factor (GCF)" data-zh="最大公因数" href="/thinking-greatest-common-factor-gcf">'
        "Greatest Common Factor (GCF)</a>"
        '<a data-en="Unit Conversions and Rates" data-zh="单位换算与比率" href="/thinking-unit-conversions-and-rates">'
        "Unit Conversions and Rates</a>"
        '<a data-en="Mental Squaring and Square Rooting" data-zh="心算平方与平方根" '
        'href="/thinking-mental-squaring-and-square-rooting">Mental Squaring and Square Rooting</a>'
        '<a aria-current="page" data-en="Imaginary &amp; Complex Numbers" data-zh="虚数与复数" '
        'href="/thinking-imaginary-complex-numbers">Imaginary &amp; Complex Numbers</a>'
        '<a class="kiwi-sidebar-back" data-en="← All Mathematical Thinking" data-zh="← 返回数学思维目录" '
        'href="/mathematical-thinking">← All Mathematical Thinking</a></aside>'
    )

    h1_en = "Imaginary and Complex Numbers — From Algebra to the Physical World"
    h1_zh = "虚数与复数——从代数到物理世界"

    return (
        f'<div class="kiwi-learning-layout">{sidebar}'
        f'<article class="kiwi-topic-article">'
        f'<h1 class="kiwi-current-topic" data-en="{esc(h1_en)}" data-zh="{esc(h1_zh)}">{h1_en}</h1>'
        f'<section class="nf-section word-topic kiwi-generated-content">{inner}</section>'
        f"</article></div>"
    )


def patch_page(body: str) -> None:
    text = PAGE.read_text(encoding="utf-8")
    text = re.sub(
        r'<meta name="pagefind:title_en" content="[^"]*" />',
        '<meta name="pagefind:title_en" content="Imaginary and Complex Numbers" />',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        '<meta content="From number families to i, the Argand plane, rotation, waves, Euler’s formula, and physical models — Advanced Mathematical Thinking." name="description"/>',
        text,
        count=1,
    )
    text = re.sub(
        r"<title data-en=\"[^\"]*\"[^>]*>[^<]*</title>",
        '<title data-en="Imaginary &amp; Complex Numbers | KIWI 爱AI Study" '
        'data-zh="虚数与复数 | KIWI 爱AI Study">Imaginary &amp; Complex Numbers | KIWI 爱AI Study</title>',
        text,
        count=1,
    )
    m = re.search(r"<!-- LEVEL-4 BODY START -->.*?<!-- LEVEL-4 BODY END -->", text, re.S)
    if not m:
        raise SystemExit("body markers missing")
    text = text[: m.start()] + "<!-- LEVEL-4 BODY START -->\n" + body + "\n<!-- LEVEL-4 BODY END -->" + text[m.end() :]
    PAGE.write_text(text, encoding="utf-8")
    print("patched", PAGE.name)


def main() -> None:
    extract_figures()
    body = build_body()
    patch_page(body)


if __name__ == "__main__":
    main()