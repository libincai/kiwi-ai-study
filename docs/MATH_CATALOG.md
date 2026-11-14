# Math grade catalog

Single source of truth: **`data/math-topics.json`**.

- **Topic pages** stay under `math/` (e.g. `foundation-oblique-triangles-and-triangle-laws.html`).
- **Grade hubs** are generated — do not hand-edit `math/grade-11.html`.

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