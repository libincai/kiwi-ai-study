#!/usr/bin/env python3
"""Insert Basic ↔ Advanced skill cross-link panels (see DESIGN_STANDARDS.md)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MATH = Path(__file__).resolve().parents[1] / "math"

HEADING = (
    '<div class="kiwi-panel-heading" data-en="&lt;span aria-hidden=&quot;true&quot; class=&quot;kiwi-panel-icon&quot;&gt;🔗&lt;/span&gt;" '
    'data-zh="&lt;span aria-hidden=&quot;true&quot; class=&quot;kiwi-panel-icon&quot;&gt;🔗&lt;/span&gt;">'
    '<span aria-hidden="true" class="kiwi-panel-icon">🔗</span></div>'
)


def esc_attr(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_panel(p1_en: str, p1_zh: str, p2_en: str, p2_zh: str) -> str:
    return (
        '<aside class="kiwi-word-info-panel kiwi-skill-crosslink-panel" role="note">'
        + HEADING
        + f'<p data-en="{esc_attr(p1_en)}" data-zh="{esc_attr(p1_zh)}">{p1_en}</p>'
        + f'<p data-en="{esc_attr(p2_en)}" data-zh="{esc_attr(p2_zh)}">{p2_en}</p>'
        + "</aside>"
    )


# Manually scoped copy per paired topic (foundation ↔ mathematical-thinking slug).
PAIRS = [
    {
        "foundation": "foundation-unit-conversions-and-rates.html",
        "advanced": "unit-conversions-and-rates.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> ratios, rates, unit rates, and introductory unit conversions with conversion factors.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 比、比率、单位率，以及用换算因数的入门单位换算。",
        "basic_also_en": "<strong>Also see:</strong> Multi-step <strong>dimensional analysis</strong> and advanced conversion chains in <a href=\"unit-conversions-and-rates.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>多步<strong>量纲分析</strong>与进阶换算链见数学思维中的 <a href=\"unit-conversions-and-rates.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> unit work — dimensional analysis and multi-step conversion chains.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 单位换算——量纲分析与多步换算链。",
        "adv_also_en": "<strong>Also see:</strong> Ratios, rates, and unit-rate conversions in <a href=\"foundation-unit-conversions-and-rates.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>比、比率与单位率换算见数学基础中的 <a href=\"foundation-unit-conversions-and-rates.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-special-right-triangles.html",
        "advanced": "special-right-triangles.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> 30°–60°–90° and 45°–45°–90° triangles, missing sides and angles, and introductory applications.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 30°–60°–90° 与 45°–45°–90° 三角形、求边求角及入门应用。",
        "basic_also_en": "<strong>Also see:</strong> Deriving special-angle values and quick pattern tricks in <a href=\"special-right-triangles.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>特殊角的推导与快速规律见数学思维中的 <a href=\"special-right-triangles.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> special angles — derive values instead of memorizing, plus quick pattern methods.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 特殊角——推导而少背，以及快速规律法。",
        "adv_also_en": "<strong>Also see:</strong> Core 30°–60°–90° and 45°–45°–90° triangle lessons in <a href=\"foundation-special-right-triangles.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>30°–60°–90° 与 45°–45°–90° 核心内容见数学基础中的 <a href=\"foundation-special-right-triangles.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-number-strategies.html",
        "advanced": "number-strategies.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> number strategies — properties of operations, factoring, friendly multiples, and pairing tricks.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 数字策略——运算性质、因式分解、凑整与配对窍门。",
        "basic_also_en": "<strong>Also see:</strong> Factor grouping, friendly-middle, and compensation strategies in <a href=\"number-strategies.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>因数分组、友好中间数与补偿法见数学思维中的 <a href=\"number-strategies.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> mental math — factor grouping, friendly-middle splits, and compensation.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 心算——因数分组、友好中间数与补偿法。",
        "adv_also_en": "<strong>Also see:</strong> Operation properties and starter tricks in <a href=\"foundation-number-strategies.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>运算性质与入门窍门见数学基础中的 <a href=\"foundation-number-strategies.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-algebraic-strategies.html",
        "advanced": "algebraic-strategies.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> algebraic strategies — simplifying expressions, substitutions, and factoring identities.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 代数策略——化简式子、代入与因式分解恒等式。",
        "basic_also_en": "<strong>Also see:</strong> Infinity limits, square-root estimation, and iterative correction in <a href=\"algebraic-strategies.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>无穷极限、平方根估计与迭代修正见数学思维中的 <a href=\"algebraic-strategies.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> algebraic strategies — tail tricks, estimation formulas, and repeated correction.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 代数策略——尾项技巧、估计公式与反复修正。",
        "adv_also_en": "<strong>Also see:</strong> Expression simplification and factoring basics in <a href=\"foundation-algebraic-strategies.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>式子化简与因式分解基础见数学基础中的 <a href=\"foundation-algebraic-strategies.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-geometric-strategies.html",
        "advanced": "geometric-strategies.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> geometric thinking — area ideas and visual problem-solving building blocks (Math Foundations track).",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 几何思维——面积观念与数形入门（数学基础路线）。",
        "basic_also_en": "<strong>Also see:</strong> Triangle-counting and polygon-area strategies in <a href=\"geometric-strategies.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>数三角形与多边形面积策略见数学思维中的 <a href=\"geometric-strategies.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> geometric strategies — the letter strategy for counting triangles and polygon area methods.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 几何策略——字母标号数三角形与多边形面积法。",
        "adv_also_en": "<strong>Also see:</strong> Foundational geometric reasoning in <a href=\"foundation-geometric-strategies.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>几何思维入门见数学基础中的 <a href=\"foundation-geometric-strategies.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-why-simplified-calculation.html",
        "advanced": "why-simplified-calculation.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> introduction to simplified calculation — reordering numbers using operation properties, with a starter example.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 简化计算入门——用运算性质重新组合数字，含入门例题。",
        "basic_also_en": "<strong>Also see:</strong> The same conceptual overview with links to strategy lessons in <a href=\"why-simplified-calculation.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>同一概念导读及后续策略专题见数学思维中的 <a href=\"why-simplified-calculation.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> overview — why simplified calculation works (commutative property and choosing an easier path).",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 导读——简化计算为何成立（交换律与选更省事的路径）。",
        "adv_also_en": "<strong>Also see:</strong> The Math Foundations introduction and worked starter example in <a href=\"foundation-why-simplified-calculation.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>数学基础导读与例题见 <a href=\"foundation-why-simplified-calculation.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-word-problems.html",
        "advanced": "word-problems.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> word problems — a structured read–plan–solve–verify approach.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 应用题——读题、计划、求解、检验的结构化方法。",
        "basic_also_en": "<strong>Also see:</strong> Extended examples and strategy depth in <a href=\"word-problems.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>更多例题与策略拓展见数学思维中的 <a href=\"word-problems.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> word problems — full structured approach with extended examples and reasoning conventions (∵ / ∴).",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 应用题——完整结构化方法与拓展例题（含 ∵ / ∴ 推理习惯）。",
        "adv_also_en": "<strong>Also see:</strong> The foundational structured method in <a href=\"foundation-word-problems.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>入门结构化方法见数学基础中的 <a href=\"foundation-word-problems.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-data-and-graphs.html",
        "advanced": "data-and-graphs.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> data and graphs — data, frequency, range, outliers, and bar, line, and histogram graphs.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 数据与图表——数据、频数、极差、异常值及条形图、折线图、直方图。",
        "basic_also_en": "<strong>Also see:</strong> Mathematical Thinking extensions on the same topic in <a href=\"data-and-graphs.html\">Advanced Skills</a>.",
        "basic_also_zh": "<strong>延伸学习：</strong>同一主题的数学思维拓展见 <a href=\"data-and-graphs.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> data and graphs — deeper analysis and reasoning on the same core graph types.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 数据与图表——在相同图表类型上做更深的分析与推理。",
        "adv_also_en": "<strong>Also see:</strong> Core vocabulary and graph basics in <a href=\"foundation-data-and-graphs.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>核心术语与图表基础见数学基础中的 <a href=\"foundation-data-and-graphs.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-measures-of-center.html",
        "advanced": "measures-of-center.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> measures of center — mean, median, and mode.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 集中趋势——平均数、中位数与众数。",
        "basic_also_en": "<strong>Also see:</strong> Extended reasoning and examples in <a href=\"measures-of-center.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>拓展推理与例题见数学思维中的 <a href=\"measures-of-center.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> measures of center — when to use mean, median, or mode and extended applications.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 集中趋势——何时用平均数、中位数或众数及拓展应用。",
        "adv_also_en": "<strong>Also see:</strong> Definitions and starter examples in <a href=\"foundation-measures-of-center.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>定义与入门例题见数学基础中的 <a href=\"foundation-measures-of-center.html\">基本方法</a>。",
    },
    {
        "foundation": "foundation-chance-and-probability.html",
        "advanced": "chance-and-probability.html",
        "basic_scope_en": "<strong>Lesson scope:</strong> <strong>Basic</strong> probability — outcomes, events, sample space, theoretical and experimental probability.",
        "basic_scope_zh": "<strong>本课范围：</strong><strong>基本</strong> 概率——结果、事件、样本空间、理论概率与实验概率。",
        "basic_also_en": "<strong>Also see:</strong> Independent and dependent events and extended reasoning in <a href=\"chance-and-probability.html\">Advanced Skills</a> (Mathematical Thinking).",
        "basic_also_zh": "<strong>延伸学习：</strong>独立与相关事件及拓展推理见数学思维中的 <a href=\"chance-and-probability.html\">进阶技巧</a>。",
        "adv_scope_en": "<strong>Lesson scope:</strong> <strong>Advanced</strong> probability — independence, dependence, and richer chance reasoning.",
        "adv_scope_zh": "<strong>本课范围：</strong><strong>进阶</strong> 概率——独立性、相关性与更丰富的概率推理。",
        "adv_also_en": "<strong>Also see:</strong> Core probability vocabulary in <a href=\"foundation-chance-and-probability.html\">Basic Skills</a> (Math Foundations).",
        "adv_also_zh": "<strong>亦可参阅：</strong>概率核心术语见数学基础中的 <a href=\"foundation-chance-and-probability.html\">基本方法</a>。",
    },
]

INSERT_BEFORE_CARD = re.compile(r"<details class=\"lesson-card\"", re.I)
AFTER_MT_TOPIC_H2 = re.compile(
    r'(<h2 class="kiwi-current-topic"[^>]*>.*?</h2>)',
    re.I | re.DOTALL,
)
AFTER_FOUNDATION_H1 = re.compile(
    r"(<article[^>]+>\s*<h1[^>]*>.*?</h1>)",
    re.I | re.DOTALL,
)
BEFORE_ARTICLE_CLOSE = re.compile(
    r"</article>\s*</div>\s*(?:<!--[^>]*-->\s*)?</main>",
    re.I,
)


def insert_panel(html: str, panel: str) -> tuple[str, bool]:
    if "kiwi-skill-crosslink-panel" in html:
        return html, False
    m = INSERT_BEFORE_CARD.search(html)
    if m:
        return html[: m.start()] + panel + html[m.start() :], True
    m = AFTER_MT_TOPIC_H2.search(html)
    if m:
        return html[: m.end()] + panel + html[m.end() :], True
    m = AFTER_FOUNDATION_H1.search(html)
    if m:
        return html[: m.end()] + panel + html[m.end() :], True
    anchor = BEFORE_ARTICLE_CLOSE.search(html)
    if anchor:
        return html[: anchor.start()] + panel + html[anchor.start() :], True
    return html, False


def main() -> int:
    changed = []
    for pair in PAIRS:
        f_path = MATH / pair["foundation"]
        a_path = MATH / pair["advanced"]
        basic_panel = build_panel(
            pair["basic_scope_en"],
            pair["basic_scope_zh"],
            pair["basic_also_en"],
            pair["basic_also_zh"],
        )
        adv_panel = build_panel(
            pair["adv_scope_en"],
            pair["adv_scope_zh"],
            pair["adv_also_en"],
            pair["adv_also_zh"],
        )
        for path, panel in ((f_path, basic_panel), (a_path, adv_panel)):
            if not path.is_file():
                print(f"MISSING {path.name}", file=sys.stderr)
                continue
            text = path.read_text(encoding="utf-8")
            new_text, ok = insert_panel(text, panel)
            if ok:
                path.write_text(new_text, encoding="utf-8")
                changed.append(path.name)
    print(f"Updated {len(changed)} files:")
    for name in sorted(set(changed)):
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
