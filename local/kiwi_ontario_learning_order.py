"""Ontario curriculum learning sequence for grade-hub topic ordering.

Ordering follows Ontario Mathematics progression (2021 elementary strands, Grade 9
MTH1W, Grade 10 MPM2D, Grade 11 MCR3U) within each Level 1 chapter — not sidebar
order. See docs/MATH_NAV_LEVELS.md.
"""
from __future__ import annotations

from _trig_toc_20261113 import SECTIONS

# Strand bands (hundreds within chapter order from math-topics.json chapters.*.order)
_BASE = {
    "number": 1_000,
    "functions": 2_000,
    "geometry": 3_000,
    "trig": 4_000,
    "data": 5_000,
    "strategies": 6_000,
}

# Foundations + Thinking tracks, curriculum-teaching order (Ontario B → …).
_NUMBER = [
    "foundation-math-operation-signs-and.html",
    "number-families.html",
    "foundation-decimal.html",
    "foundation-decimal-to-fraction.html",
    "foundation-division-rules-2-9.html",
    "foundation-result-signs-and.html",
    "foundation-greatest-common-factor-gcf.html",
    "foundation-exponents.html",
    "foundation-roots.html",
    "foundation-rational-exponents.html",
    "foundation-unit-conversions-and-rates.html",
]

_FUNCTIONS = [
    "foundation-algebra-language-and-patterns.html",
    "foundation-step-pattern-and-first-differences-y.html",
    "foundation-understanding-functions.html",
    "foundation-linear-vs-non-linear-functions.html",
    "foundation-understanding-the-placeholder-in-f-x.html",
    "foundation-function-transformations.html",
    "foundation-functions-and-their-inverses.html",
    "foundation-algebraic-strategies.html",
    "recovering-function-rule.html",
]

_GEOMETRY = [
    "foundation-basic-geometry-words.html",
    "foundation-geometric-strategies.html",
    "foundation-rotation-transformation.html",
    "foundation-special-right-triangles.html",
    "foundation-trigonometry-fundamentals.html",
]

_DATA = [
    "foundation-data-and-graphs.html",
    "foundation-measures-of-center.html",
    "foundation-chance-and-probability.html",
]

_STRATEGIES: list[str] = []


def _band_sort(files: list[str], base: int, step: int = 10) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, name in enumerate(files):
        out[f"math/{name}"] = base + i * step
    return out


def _trig_sort() -> dict[str, int]:
    out: dict[str, int] = {}
    n = _BASE["trig"]
    # MPM2D right-triangle introduction before MCR3U unit-circle / laws / identities.
    for fname, *_ in SECTIONS[0][5]:
        out[f"math/{fname}"] = n
        n += 5
    n = _BASE["trig"] + 80
    out["math/foundation-special-right-triangles.html"] = n
    n += 10
    for hub, *_rest, lessons in SECTIONS:
        out[f"math/{hub}"] = n
        n += 10
        for fname, *_ in lessons:
            if fname in {
                "foundation-understanding-trigonometry.html",
                "foundation-the-three-sides-of-a-right-triangle.html",
                "foundation-the-four-basic-trigonometric-ratios.html",
            }:
                continue
            out[f"math/{fname}"] = n
            n += 5
    return out


def build_ontario_sort_map() -> dict[str, int]:
    m: dict[str, int] = {}
    m.update(_band_sort(_NUMBER, _BASE["number"]))
    m.update(_band_sort(_FUNCTIONS, _BASE["functions"]))
    m.update(_band_sort(_GEOMETRY, _BASE["geometry"]))
    m.update(_trig_sort())
    m.update(_band_sort(_DATA, _BASE["data"]))
    m.update(_band_sort(_STRATEGIES, _BASE["strategies"]))
    return m


ONTOARIO_LEARNING_SORT: dict[str, int] = build_ontario_sort_map()


def apply_ontario_learning_sort(topics: list[dict]) -> None:
    for t in topics:
        path = t.get("file", "")
        if path in ONTOARIO_LEARNING_SORT:
            t["sort"] = ONTOARIO_LEARNING_SORT[path]