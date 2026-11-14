# Ontario grade and course labels on math pages

**Rule:** A math lesson page gets **Grade** pills, **course** pills (MTH1W, MPM2D, MCR3U, …), and inclusion on **grade hub** pages only when Ontario’s published mathematics curriculum **requires or clearly expects** that content at that grade — not when a topic is enrichment, a duplicate track, or a general thinking demo.

If a page is **not** tied to a specific Ontario expectation or approved secondary course outcome, it must have **no** grade/course labeling and must **not** appear on `grade-N.html` hubs.

## What qualifies

| Qualifies | Does not qualify |
|-----------|------------------|
| **Math Foundations** L3 hubs and their lesson sequences that mirror Ontario strands (e.g. decimals, exponents, data literacy) with defensible grade bands | **Mathematical Thinking** leaf pages (`gcf.html`, `mental-squaring-and-square-rooting.html`, `car-journey.html`, etc.) |
| **MCR3U / MPM2D** lessons listed in `local/_trig_toc_20261113.py` or with an on-page Ontario course citation | Cross-grade “strategies” or mental-math enrichment (`number-strategies`, `why-simplified-calculation`, …) |
| `recovering-function-rule.html` (explicit MCR3U functions alignment) | Pages that only “support” a course informally (e.g. mental squaring beside square roots) |

## Sources of truth

1. **`local/kiwi_math_topics_data.py`** — Verified Grade 11 trig, `recovering-function-rule`, MPM2D intro trig grades.
2. **`local/kiwi_ontario_math_grades.py`** — `ONTARIO_MAPPINGS` only for **Foundations** files that pass this policy.
3. **`data/math-topics.json`** — Generated; do not hand-edit.

Each catalog row should include a short `verified_note` (or implicit trig/MCR3U source) explaining *why* grades are assigned.

## Adding or changing labels

1. Confirm the Ontario grade/course (elementary 2021 strands, MTH1W, MPM2D, MCR3U) and the specific expectation or course outcome — not just “related ideas.”
2. Add or update a row in `ONTARIO_MAPPINGS` or `build_topics()` in `kiwi_math_topics_data.py`.
3. Run `python local/kiwi_math_catalog.py` (strips labels from pages removed from the catalog).

## Removing labels

Delete the topic row from `ONTARIO_MAPPINGS` / `build_topics()`. Re-run the catalog. Pages no longer in `math-topics.json` have catalog injection blocks removed automatically.

See also **`docs/MATH_CATALOG.md`** and **`docs/MATH_NAV_LEVELS.md`** (Level 2 pills on grade hubs).