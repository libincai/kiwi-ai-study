"""Trigonometry TOC from Math_Quick_Ref_20261113.docx — L2 sidebar, L3 lesson-cards on L2 pages."""
from __future__ import annotations

# (hub_file, section_en, section_zh, lead_en, lead_zh, lessons)
# lessons: (file, title_en, title_zh, blurb_en, blurb_zh)

SECTIONS: list[
    tuple[str, str, str, str, str, list[tuple[str, str, str, str, str]]]
] = [
    (
        "foundation-trigonometry-fundamentals.html",
        "Trigonometry Fundamentals",
        "三角学基础",
        "Choose a lesson to explore right triangles and the basic trigonometric ratios.",
        "选择一课，学习直角三角形与基本三角比。",
        [
            (
                "foundation-understanding-trigonometry.html",
                "Understanding Trigonometry",
                "认识三角函数",
                "What trigonometry studies and why it matters in real life.",
                "三角学研究什么，以及它在生活中的用途。",
            ),
            (
                "foundation-the-three-sides-of-a-right-triangle.html",
                "The Three Sides of a Right Triangle",
                "直角三角形的三条边",
                "Identify the hypotenuse, opposite, and adjacent sides relative to an angle.",
                "根据一个角辨认斜边、对边与邻边。",
            ),
            (
                "foundation-the-four-basic-trigonometric-ratios.html",
                "The Four Basic Trigonometric Ratios",
                "四个基本三角比",
                "Define sine, cosine, tangent, and cotangent using side ratios.",
                "用边的比值定义 sin、cos、tan 与 cot。",
            ),
        ],
    ),
    (
        "foundation-angles-and-trigonometric-ratios.html",
        "Angles and Trigonometric Ratios",
        "角与三角比",
        "Choose a lesson on standard-position angles, special values, and reciprocal ratios.",
        "选择一课，学习标准位置角、特殊角三角比与倒数比。",
        [
            (
                "foundation-angles-in-standard-position.html",
                "Angles in Standard Position",
                "标准位置角",
                "Initial arm, terminal arm, and primary ratios on the coordinate plane.",
                "始边、终边，以及坐标平面上的基本三角比。",
            ),
            (
                "foundation-related-and-coterminal-angles.html",
                "Related and Coterminal Angles",
                "相关角与同界角",
                "Reference angles and angles that share the same terminal arm.",
                "参考角与同终边角。",
            ),
            (
                "foundation-trigonometric-ratios-beyond-90.html",
                "Trigonometric Ratios Beyond 90°",
                "超过90°的三角比",
                "Extend ratios past right triangles using signed projections.",
                "用带符号投影把三角比推广到超过 90° 的角。",
            ),
            (
                "foundation-exact-trigonometric-values.html",
                "Trigonometric Ratios of Special Angles",
                "特殊角的三角比",
                "Exact values from special triangles and common tables.",
                "由特殊三角形推导精确值并查表。",
            ),
            (
                "foundation-reciprocal-trigonometric-ratios.html",
                "Reciprocal Trigonometric Ratios",
                "倒数三角比",
                "Cosecant, secant, and cotangent as reciprocals of the basic ratios.",
                "余割、正割、余切与基本比的倒数关系。",
            ),
        ],
    ),
    (
        "foundation-oblique-triangles-and-triangle-laws.html",
        "Oblique Triangles and Triangle Laws",
        "斜三角形与三角形定理",
        "Choose a lesson on the sine law, cosine law, and when to use each.",
        "选择一课，学习正弦定理、余弦定理及选用方法。",
        [
            (
                "foundation-sine-law.html",
                "Oblique Triangles and the Sine Law",
                "斜三角形与正弦定理",
                "Types of oblique triangles and applying the sine law.",
                "斜三角形类型与正弦定理的应用。",
            ),
            (
                "foundation-ssa-ambiguous-case.html",
                "SSA Ambiguous Case (Sine Law)",
                "SSA 歧义情形（正弦定理）",
                "When SSA gives zero, one, or two possible triangles.",
                "SSA 何时无解、一解或两解。",
            ),
            (
                "foundation-law-of-cosines.html",
                "The Cosine Law",
                "余弦定理",
                "Relate three sides and an angle when the sine law is not enough.",
                "在正弦定理不便时用三边与角的关系。",
            ),
            (
                "foundation-trigonometry-3d-applications.html",
                "Applications in 3D Settings",
                "三维应用",
                "Layer triangles to solve problems in three dimensions.",
                "分层使用三角形解决三维问题。",
            ),
            (
                "foundation-choosing-trigonometry-laws.html",
                "Choosing Between the Sine Law and the Cosine Law",
                "正弦定理与余弦定理的选择",
                "Decide which law fits a given oblique triangle problem.",
                "根据题意选择正弦定理或余弦定理。",
            ),
        ],
    ),
    (
        "foundation-trigonometric-identities.html",
        "Trigonometric Identities",
        "三角恒等式",
        "Choose a lesson on core identities and strategies for proving them.",
        "选择一课，学习核心恒等式与证明策略。",
        [
            (
                "foundation-what-is-trigonometric-identity.html",
                "What Is an Identity?",
                "什么是恒等式？",
                "How an identity differs from an equation.",
                "恒等式与方程的区别。",
            ),
            (
                "foundation-pythagorean-identity.html",
                "Pythagorean Identity",
                "勾股恒等式",
                "The fundamental relationship between sine and cosine.",
                "正弦与余弦的基本关系式。",
            ),
            (
                "foundation-quotient-identities.html",
                "Quotient Identities",
                "商恒等式",
                "Tangent and cotangent in terms of sine and cosine.",
                "用 sin、cos 表示 tan、cot。",
            ),
            (
                "foundation-reciprocal-identities.html",
                "Reciprocal Identities",
                "倒数恒等式",
                "Pair each basic ratio with its reciprocal.",
                "基本比与其倒数的对应关系。",
            ),
            (
                "foundation-proving-trigonometric-identities.html",
                "Strategies for Proving Trigonometric Identities",
                "证明三角恒等式的策略",
                "Algebraic moves that simplify one side to match the other.",
                "化简一边使之与另一边一致的常用变形。",
            ),
            (
                "foundation-trigonometric-identities-quick-checks.html",
                "Quick Checks",
                "快速检验",
                "Fast ways to verify whether a statement is an identity.",
                "快速检验式子是否为恒等式。",
            ),
        ],
    ),
]

# Level-2 sidebar (book Heading 2). Special Right Triangles has no L3 hub — direct lesson page.
SIDEBAR_LEVEL2: list[tuple[str, str, str]] = [
    ("foundation-trigonometry-fundamentals.html", "Trigonometry Fundamentals", "三角学基础"),
    ("foundation-special-right-triangles.html", "Special Right Triangles", "特殊直角三角形"),
    ("foundation-angles-and-trigonometric-ratios.html", "Angles and Trigonometric Ratios", "角与三角比"),
    (
        "foundation-oblique-triangles-and-triangle-laws.html",
        "Oblique Triangles and Triangle Laws",
        "斜三角形与三角形定理",
    ),
    ("foundation-trigonometric-identities.html", "Trigonometric Identities", "三角恒等式"),
]


def hub_for_lesson(lesson_href: str) -> str | None:
    for hub, *_rest, lessons in SECTIONS:
        if any(h == lesson_href for h, *_ in lessons):
            return hub
    return None


def all_lesson_pages() -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for *_head, lessons in SECTIONS:
        for href, en, zh, *_ in lessons:
            out.append((href, en, zh))
    return out


def all_hub_pages() -> list[tuple[str, str, str]]:
    return [(h, en, zh) for h, en, zh, *_ in [(s[0], s[1], s[2], *s[3:]) for s in SECTIONS]]


def all_sync_pages() -> list[str]:
    """Pages that carry the trigonometry sidebar (Level 2 section pages only)."""
    return [h for h, _, _ in SIDEBAR_LEVEL2]
