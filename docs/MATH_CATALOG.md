# Math grade catalog

Single source of truth: **`data/math-topics.json`** (regenerated from **`local/kiwi_math_topics_data.py`**).

- **Topic pages** stay under `math/` (e.g. `foundation-oblique-triangles-and-triangle-laws.html`).
- **Grade index** `math/by-grade.html` and **grade hubs** (e.g. `math/grade-11.html`) are generated — edit the topics data module, not those HTML files.
- **Chapters** in the JSON use exact hub card titles (`chapters.*.title_en` / `title_zh`, e.g. Math Foundations **Trigonometry** / **三角函数**). Topics link via `chapter_id`.
- **Level 1 vs Level 2 naming** (chapter vs sidebar hub on grade pages): see **`docs/MATH_NAV_LEVELS.md`**. Course **requirement pills** on grade hub rows come from `topics[].courses`.
- **Grade strip** on a lesson page (Grade pill, course pill, link to `grade-11.html`) is injected only for topics listed in the catalog. Pages **not** in the catalog are intentionally unlabeled.

## Ontario labeling policy

**Full rules:** **`docs/ONTARIO_GRADE_LABELS.md`**

Summary: no **Grade** / course pills and no **grade hub** listing unless Ontario’s curriculum **requires or clearly expects** that content at that grade. **Mathematical Thinking** leaf pages and enrichment topics stay unlabeled.

Verified topics live in **`local/kiwi_math_topics_data.py`**, **`local/kiwi_ontario_math_grades.py`** (`ONTARIO_MAPPINGS`), and the MCR3U trig toc. Re-run the catalog after edits; removed topics are stripped automatically.

## Update workflow

```powershell
# Edit local/kiwi_math_topics_data.py (writes data/math-topics.json), then:
python local/kiwi_math_catalog.py
python local/kiwi_search_prepare.py
python local/kiwi_inject_search_assets.py   # if needed
npx --yes pagefind --site .
```

`tools/build-search.ps1` and `tools/dev-server.ps1` run `kiwi_math_catalog.py` automatically.

## Add a Grade 11 topic

Add a verified row in `kiwi_math_topics_data.build_topics()` with `"grades": [11]`, `"courses": ["MCR3U"]` (or another Ontario course code), and the `file` path. Re-run `kiwi_math_catalog.py`.