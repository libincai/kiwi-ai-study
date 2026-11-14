# Site search (Pagefind)

Kiwi uses **build-time Pagefind** plus a **header modal** (`assets/js/kiwi-site-search.js`). Re-run indexing after adding or editing public HTML.

## Build (repo root)

```powershell
cd D:\YuanSync\Mirror\MyAI\kiwi-ai-study
python local/kiwi_search_prepare.py
python local/kiwi_inject_search_assets.py
npx --yes pagefind --site .
```

Commit `pagefind/` output with the site. GitHub Pages serves it at `/pagefind/`.

Local dev (clean URLs like `http://localhost:3000/math-foundations`):

```powershell
.\tools\dev-server.ps1
```

This runs `tools/generate-serve-rewrites.py` (writes `serve.json`) and `npx serve . -l 3000`. GitHub Pages keeps folder paths (`/math/math-foundations.html`). Search links follow your environment: clean slugs on localhost, `.html` paths on GitHub.

## Index contract (every new public page)

1. **Main content** — wrap teachable content in `<main>` (already standard). Optional: `data-pagefind-body` on `main` or `.mf-article` (prepare script adds this).
2. **Bilingual** — keep `data-en` / `data-zh` on copy. Prepare injects hidden `div.kiwi-pagefind-zh` (`lang:zh` filter, Chinese title/breadcrumb meta) and tags `<main>` with `lang:en`. Search uses the active UI language (`html lang`) to filter results.
3. **Section filter** — prepare sets `data-pagefind-filter="section:math|ai|books|about|legal|home"` from URL path for hub-scoped search.
4. **Breadcrumb meta** — prepare sets `data-pagefind-meta="breadcrumb:Math › Trigonometry"` (EN) and `breadcrumb_zh:…` when detectable from title/h1.
5. **Exclude** — redirect-only stubs get `data-pagefind-ignore="all"` on `<body>`. Do not index `templates/`, `local/`, etc. (see `pagefind.yml`).
## UI

- **Global:** search icon in header (before language flags), **Ctrl/Cmd+K** and **/**.

## Do not

- Hand-maintain a separate URL list.
- Rely on hub-only filters as the only search (AI episode filter may remain for the card grid).