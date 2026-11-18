"""Build data/math-topics.json topic rows from verified Ontario mappings."""
from __future__ import annotations

import json
from pathlib import Path

from _trig_toc_20261113 import SECTIONS
from kiwi_ontario_learning_order import apply_ontario_learning_sort
from kiwi_ontario_math_grades import build_ontario_topics, read_titles

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "math-topics.json"

def build_topics() -> list[dict]:
    topics: list[dict] = [
        {
            "id": "angles-trig-ratios",
            "file": "math/foundation-angles-and-trigonometric-ratios.html",
            "title_en": "Angles and Trigonometric Ratios",
            "title_zh": "角与三角比",
            "grades": [11],
            "courses": ["MCR3U"],
            "chapter_id": "foundations-trigonometry",
            "sort": 10,
            "list_on_grade_hub": True,
        },
        {
            "id": "unit-circle-six-trig",
            "file": "math/foundation-six-trigonometric-functions-unit-circle.html",
            "title_en": "Six Trigonometric Functions on the Unit Circle",
            "title_zh": "单位圆上的六种三角函数",
            "grades": [11],
            "courses": ["MCR3U"],
            "chapter_id": "foundations-trigonometry",
            "sort": 15,
            "list_on_grade_hub": True,
        },
        {
            "id": "oblique-triangles-laws",
            "file": "math/foundation-oblique-triangles-and-triangle-laws.html",
            "title_en": "Oblique Triangles and Triangle Laws",
            "title_zh": "斜三角形与三角形定理",
            "grades": [11],
            "courses": ["MCR3U"],
            "chapter_id": "foundations-trigonometry",
            "sort": 20,
            "list_on_grade_hub": True,
        },
        {
            "id": "trig-identities-hub",
            "file": "math/foundation-trigonometric-identities.html",
            "title_en": "Trigonometric Identities",
            "title_zh": "三角恒等式",
            "grades": [11],
            "courses": ["MCR3U"],
            "chapter_id": "foundations-trigonometry",
            "sort": 30,
            "list_on_grade_hub": True,
        },
    ]
    seen = {t["file"] for t in topics}
    for hub_file, _en, _zh, _le, _lz, lessons in SECTIONS:
        for i, (href, title_en, title_zh, *_rest) in enumerate(lessons):
            path = f"math/{href}"
            if path in seen:
                continue
            topics.append(
                {
                    "id": href.replace(".html", ""),
                    "file": path,
                    "title_en": title_en,
                    "title_zh": title_zh,
                    "grades": [11],
                    "courses": ["MCR3U"],
                    "chapter_id": "foundations-trigonometry",
                    "sort": 0,
                    "list_on_grade_hub": False,
                    "verified_note": f"MCR3U trig lesson under {hub_file}",
                }
            )
            seen.add(path)

    topics.append(
        {
            "id": "recovering-function-rule",
            "file": "math/thinking-recovering-function-rule.html",
            "title_en": "Recovering a Function Rule from Function Notation",
            "title_zh": "从函数记号还原函数规则",
            "grades": [11],
            "courses": ["MCR3U"],
            "chapter_id": "thinking-functions-graphs",
            "sort": 10,
            "list_on_grade_hub": True,
            "verified_note": "Page cites MCR3U Functions (Ontario 2007 curriculum)",
        }
    )
    seen.add("math/thinking-recovering-function-rule.html")

    topics.append(
        {
            "id": "discovering-pythagorean-triples",
            "file": "math/thinking-discovering-pythagorean-triples.html",
            "title_en": "Discovering Pythagorean Triples",
            "title_zh": "发现勾股数",
            "grades": [10, 11],
            "courses": ["MPM2D", "MCR3U"],
            "chapter_id": "thinking-trigonometry",
            "sort": 10,
            "list_on_grade_hub": False,
            "verified_note": "Mathematical Thinking — Pythagorean triple construction (Advanced quick reference)",
        }
    )
    seen.add("math/thinking-discovering-pythagorean-triples.html")

    # Introductory right-triangle lessons: MPM2D (G10) through MCR3U (G11).
    intro_trig = {
        "math/foundation-understanding-trigonometry.html",
        "math/foundation-the-three-sides-of-a-right-triangle.html",
        "math/foundation-the-four-basic-trigonometric-ratios.html",
    }
    for t in topics:
        if t["file"] in intro_trig:
            t["grades"] = [10, 11]
            t["courses"] = ["MPM2D", "MCR3U"]

    topics.extend(build_ontario_topics(seen_files=seen))
    apply_level2_titles(topics)
    apply_ontario_learning_sort(topics)
    return topics


def apply_level2_titles(topics: list[dict]) -> None:
    """Sync catalog topic titles with sidebar Level 2 names (MATH_NAV_LEVELS)."""
    for t in topics:
        en, zh = read_titles(ROOT / t["file"])
        t["title_en"] = en
        t["title_zh"] = zh


def _grade_hubs() -> dict:
    """Grade hub pages for by-grade picker (generated)."""
    base = {
        "title_zh": "",
        "subtitle_en": "Topics from Math Foundations and Mathematical Thinking for this grade.",
        "subtitle_zh": "来自「数学基础」与「数学思维」、适合本年级的主题。",
        "courses_en": "",
        "courses_zh": "",
        "hub_file": "",
        "hub_slug": "",
    }
    specs = {
        3: ("Grade 3 Mathematics", "三年级数学"),
        4: ("Grade 4 Mathematics", "四年级数学"),
        5: ("Grade 5 Mathematics", "五年级数学"),
        6: ("Grade 6 Mathematics", "六年级数学"),
        7: ("Grade 7 Mathematics", "七年级数学"),
        8: ("Grade 8 Mathematics", "八年级数学"),
        9: ("Grade 9 Mathematics", "九年级数学", "MTH1W", "MTH1W"),
        10: ("Grade 10 Mathematics", "十年级数学", "MPM2D · Principles", "MPM2D · 原理"),
        11: (
            "Grade 11 Mathematics",
            "十一年级数学",
            "MCR3U · Functions",
            "MCR3U · 函数",
        ),
    }
    out: dict = {}
    for g, row in specs.items():
        title_en, title_zh = row[0], row[1]
        courses_en = row[2] if len(row) > 2 else ""
        courses_zh = row[3] if len(row) > 3 else courses_en
        slug = f"grade-{g}"
        out[str(g)] = {
            **base,
            "title_en": title_en,
            "title_zh": title_zh,
            "courses_en": courses_en,
            "courses_zh": courses_zh,
            "hub_file": f"math/{slug}.html",
            "hub_slug": slug,
        }
    return out


def _by_course_hub() -> dict:
    return {
        "title_en": "Ontario Course Codes",
        "title_zh": "安省课程代码",
        "subtitle_en": "Codes used on this site: a short Ontario description and links to our lessons for each course. This is not the full ministry curriculum.",
        "subtitle_zh": "本站使用的课程代码：安省课程简要说明，以及各代码下的主题链接。并非完整的教育厅课程文件。",
        "hub_file": "math/by-ontario-course.html",
        "hub_slug": "by-ontario-course",
    }


def _course_codes_meta() -> dict:
    return {
        "MTH1W": {
            "order": 1,
            "summary_en": "Grade 9 · MTH1W · Mathematics",
            "summary_zh": "九年级 · MTH1W · 数学",
            "course_line_en": "<strong>Grade 9 Mathematics — MTH1W</strong>",
            "course_line_zh": "<strong>九年级数学 — MTH1W</strong>",
            "leadin_en": "The Ontario curriculum for Grade 9 Mathematics (de-streamed) emphasizes algebraic thinking, relationships among representations, and problem solving across number, algebra, data, geometry, and measurement strands.",
            "leadin_zh": "安省九年级数学（不分流）课程强调代数思维、多种表征之间的联系，以及在数、代数、数据、几何与度量各领域的解题能力。",
            "quote_en": "Students develop algebraic concepts and make connections between number and algebra using different tools and representations.",
            "quote_zh": "学生发展代数概念，并通过不同工具与表征理解数与代数之间的联系。",
            "citation_en": "— Ontario Curriculum: Secondary Mathematics, Grade 9 (MTH1W), Ministry of Education.",
            "citation_zh": "——《安省课程：中学数学》，九年级（MTH1W），省教育厅。",
            "official_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/secondary-mathematics/courses/mth1w",
            "connect_en": "Topics on this site tagged MTH1W support expressions, equations, linear relations, and foundational function ideas at the Grade 9 level.",
            "connect_zh": "本站标注 MTH1W 的主题，对应九年级层面的式子、方程、线性关系与函数入门等内容。",
            "code_explainer_en": (
                "<strong>What this code means:</strong> "
                "<strong>M</strong> = Mathematics; "
                "<strong>TH</strong> = the compulsory Grade 9 course; "
                "<strong>1</strong> = Grade 9; "
                "<strong>W</strong> = de-streamed (one course for all students, not Applied vs Academic)."
            ),
            "code_explainer_zh": (
                "<strong>代码含义：</strong>"
                "<strong>M</strong> = 数学；"
                "<strong>TH</strong> = 九年级必修课；"
                "<strong>1</strong> = 九年级；"
                "<strong>W</strong> = 不分流（全体学生同一门数学课，而非应用/学术分流）。"
            ),
        },
        "MPM2D": {
            "order": 2,
            "summary_en": "Grade 10 · MPM2D · Principles of Mathematics",
            "summary_zh": "十年级 · MPM2D · 数学原理",
            "course_line_en": "<strong>Grade 10 Principles of Mathematics — MPM2D</strong>",
            "course_line_zh": "<strong>十年级数学原理 — MPM2D</strong>",
            "leadin_en": "The Ontario Grade 10 Principles course develops reasoning with quadratics, trigonometry, analytic geometry, and linear systems, with emphasis on problem solving and communication.",
            "leadin_zh": "安省十年级数学原理课程发展二次关系、三角学、解析几何与线性方程组方面的推理能力，并强调解题与表达。",
            "quote_en": "Students continue to build on their understanding of linear relations and extend their thinking to quadratic relations and trigonometry.",
            "quote_zh": "学生在线性关系的基础上，将思维拓展至二次关系与三角学。",
            "citation_en": "— The Ontario Curriculum, Grades 9 and 10: Mathematics, Ontario Ministry of Education, Principles of Mathematics, Grade 10, Academic (MPM2D).",
            "citation_zh": "——《安大略课程：9 与 10 年级数学》，安大略省教育厅，十年级数学原理学术课程（MPM2D）。",
            "official_url": "https://www.edu.gov.on.ca/eng/curriculum/secondary/math910currb.pdf",
            "connect_en": "Lessons tagged MPM2D on this site include introductory trigonometry, transformations, and quadratic patterns that align with early Principles topics.",
            "connect_zh": "本站标注 MPM2D 的课时包含与数学原理入门主题相衔接的三角学入门、变换与二次模式等内容。",
            "code_explainer_en": (
                "<strong>What this code means:</strong> "
                "<strong>M</strong> = Mathematics; "
                "<strong>PM</strong> = <em>Principles of Mathematics</em> (this course line); "
                "<strong>2</strong> = Grade 10; "
                "<strong>D</strong> = Academic (university-oriented pathway in Grades 9–10)."
            ),
            "code_explainer_zh": (
                "<strong>代码含义：</strong>"
                "<strong>M</strong> = 数学；"
                "<strong>PM</strong> = <em>数学原理</em>（Principles of Mathematics）；"
                "<strong>2</strong> = 十年级；"
                "<strong>D</strong> = 学术类（9–10 年级大学导向课程）。"
            ),
        },
        "MCR3U": {
            "order": 3,
            "summary_en": "Grade 11 · MCR3U · Functions",
            "summary_zh": "十一年级 · MCR3U · 函数",
            "course_line_en": "<strong>Grade 11 Functions — MCR3U</strong>",
            "course_line_zh": "<strong>十一年级函数 — MCR3U</strong>",
            "leadin_en": "The Ontario Ministry of Education describes the Grade 11 Functions course as follows:",
            "leadin_zh": "安大略省教育厅对十一年级函数课程说明如下：",
            "quote_en": "Students will reason mathematically and communicate their thinking as they solve multi-step problems.",
            "quote_zh": "学生将进行数学推理，并在解决多步骤问题时表达自己的想法。",
            "citation_en": "— The Ontario Curriculum, Grades 11 and 12: Mathematics, Ontario Ministry of Education, 2007, Functions, Grade 11, University Preparation (MCR3U), page 43.",
            "citation_zh": "——《安大略课程：11 与 12 年级数学》，安大略省教育厅，2007，函数，十一年级大学预备（MCR3U），第 43 页。",
            "official_url": "https://www.edu.gov.on.ca/eng/curriculum/secondary/math1112currb.pdf",
            "connect_en": "Topics tagged MCR3U extend trigonometry, identities, and function reasoning for university-preparation Functions.",
            "connect_zh": "本站标注 MCR3U 的主题，涵盖大学预备函数课程中的三角学、恒等式与函数推理等内容。",
            "code_explainer_en": (
                "<strong>What this code means:</strong> "
                "<strong>M</strong> = Mathematics; "
                "<strong>CR</strong> = <em>Functions</em> (this course); "
                "<strong>3</strong> = Grade 11; "
                "<strong>U</strong> = University preparation."
            ),
            "code_explainer_zh": (
                "<strong>代码含义：</strong>"
                "<strong>M</strong> = 数学；"
                "<strong>CR</strong> = <em>函数</em>（Functions）；"
                "<strong>3</strong> = 十一年级；"
                "<strong>U</strong> = 大学预备。"
            ),
        },
    }


def write_catalog() -> None:
    payload = {
        "by_grade": {
            "title_en": "Math by Grade",
            "title_zh": "按年级浏览",
            "subtitle_en": "Open your grade to see lesson links from Math Foundations and Mathematical Thinking.",
            "subtitle_zh": "选择年级，查看「数学基础」与「数学思维」中为你准备的主题链接。",
            "hub_file": "math/by-grade.html",
            "hub_slug": "by-grade",
        },
        "by_course": _by_course_hub(),
        "course_codes": _course_codes_meta(),
        "chapters": {
            "foundations-number": {
                "title_en": "Number Skills & Operations",
                "title_zh": "数的技能与运算",
                "hub": "foundations",
                "order": 10,
            },
            "foundations-functions-graphs": {
                "title_en": "Functions & Graphs",
                "title_zh": "函数与图像",
                "hub": "foundations",
                "order": 20,
            },
            "foundations-geometry": {
                "title_en": "Geometry & Space",
                "title_zh": "几何与空间",
                "hub": "foundations",
                "order": 30,
            },
            "foundations-trigonometry": {
                "title_en": "Trigonometry",
                "title_zh": "三角函数",
                "hub": "foundations",
                "order": 40,
            },
            "foundations-data-chance": {
                "title_en": "Data & Chance",
                "title_zh": "数据与概率",
                "hub": "foundations",
                "order": 50,
            },
            "foundations-strategies": {
                "title_en": "Strategies & Word Problems",
                "title_zh": "策略与应用题",
                "hub": "foundations",
                "order": 60,
            },
            "thinking-number": {
                "title_en": "Number Skills & Operations",
                "title_zh": "数的技能与运算",
                "hub": "thinking",
                "order": 10,
            },
            "thinking-functions-graphs": {
                "title_en": "Functions & Graphs",
                "title_zh": "函数与图像",
                "hub": "thinking",
                "order": 20,
            },
            "thinking-geometry": {
                "title_en": "Geometry & Space",
                "title_zh": "几何与空间",
                "hub": "thinking",
                "order": 30,
            },
            "thinking-trigonometry": {
                "title_en": "Trigonometry",
                "title_zh": "三角函数",
                "hub": "thinking",
                "order": 40,
            },
            "thinking-data-chance": {
                "title_en": "Data & Chance",
                "title_zh": "数据与概率",
                "hub": "thinking",
                "order": 50,
            },
            "thinking-strategies": {
                "title_en": "Strategies & Word Problems",
                "title_zh": "策略与应用题",
                "hub": "thinking",
                "order": 60,
            },
        },
        "grades": _grade_hubs(),
        "topics": build_topics(),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "with", len(payload["topics"]), "topics")


if __name__ == "__main__":
    write_catalog()