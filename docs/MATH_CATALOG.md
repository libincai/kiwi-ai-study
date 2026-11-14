# Math grade catalog

Single source of truth: **`data/math-topics.json`**.

- **Topic pages** stay under `math/` (e.g. `foundation-oblique-triangles-and-triangle-laws.html`).
- **Grade index** `math/by-grade.html` and **grade hubs** (e.g. `math/grade-11.html`) are generated — edit the JSON, not those HTML files.
- **Chapters** in the JSON use exact hub card titles (`chapters.*.title_en` / `title_zh`, e.g. Math Foundations **Trigonometry** / **三角函数**). Topics link via `chapter_id`.

## Update workflow

```powershell
# Edit data/math-topics.json, then:
python local/kiwi_math_catalog.py
python local/kiwi_search_prepare.py
python local/kiwi_inject_search_assets.py   # if needed
npx --yes pagefind --site .
```

`tools/build-search.ps1` and `tools/dev-server.ps1` run `kiwi_math_catalog.py` automatically.

## Add a Grade 11 topic

Add a row to `topics` with `"grades": [11]` and the `file` path. Re-run `kiwi_math_catalog.py`.