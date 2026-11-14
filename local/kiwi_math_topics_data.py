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
            "thinking-data-chance": {
                "title_en": "Data & Chance",
                "title_zh": "数据与概率",
                "hub": "thinking",
                "order": 40,
            },
            "thinking-strategies": {
                "title_en": "Strategies & Word Problems",
                "title_zh": "策略与应用题",
                "hub": "thinking",
                "order": 50,
            },
        },
        "grades": _grade_hubs(),
        "topics": build_topics(),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "with", len(payload["topics"]), "topics")


if __name__ == "__main__":
    write_catalog()