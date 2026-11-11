# Kiwi 爱AI Study — Website Design Standards

**Status:** Project-wide design rules  
**Applies to:** Every page, every language, desktop and mobile  
**Rule:** Before creating or editing a page, read this file and reuse the existing shared components and CSS tokens. Do not invent page-specific styling when a shared standard already exists.

---

## 1. Core principle

The website must look and behave like one coherent site.

- Existing approved pages are the visual reference. Do not redesign them while adding a new page.
- The shared navigation, inner-page banner, content container, typography, spacing, buttons, footer, and language switcher must remain consistent.
- A new page must inherit the shared layout and styles rather than introducing a second, competing implementation.
- If a requested change affects a global component, update the shared component once and check every page that uses it.
- Do not append repeated CSS overrides indefinitely. Find and update the original shared rule, or consolidate the rules into one canonical section.

## 2. Site structure

Use the navigation categories to organize page files:

```text
kiwi-ai-study/
├── index.html
├── README.md
├── DESIGN_STANDARDS.md
├── templates/
│   ├── level-2-primary-nav.html
│   ├── level-3-category.html
│   └── level-4-topic.html
├── about/
│   └── index.html
├── math/
│   ├── index.html
│   ├── in-class-learning.html
│   └── ...
├── ai/
│   ├── index.html
│   ├── episode-01.html
│   └── ...
├── books/
│   ├── index.html
│   └── ...
├── contact/
│   └── index.html
├── legal/
│   └── ...
└── assets/
    ├── css/
    ├── hero/
    ├── logo/
    ├── books/
    └── ...
```

- The root `index.html` is the homepage and primary entry point.
- Put each page in the folder matching its navigation section.
- Keep shared assets in `assets/`; do not duplicate the same logo, banner, or stylesheet in page folders.
- Use relative links that work from the page's folder depth.
- Keep the homepage hero separate from the inner-page banner system.

## 3. Global design tokens

The CSS `:root` block is the source of truth for reusable values. The Markdown file documents the rules; actual shared values must live in CSS custom properties, not be independently retyped on every page.

Current site-wide base values found in the stylesheet:

| Token | Current value | Use |
|---|---:|---|
| `--color-navy` | `#101747` | Main headings and primary text |
| `--color-blue` | `#0756df` | Links, active navigation, primary actions |
| `--color-body` | `#101747` | Main body text |
| `--color-soft-blue` | `#e5f2ff` | Soft blue surfaces |
| `--color-soft-lilac` | `#f0efff` | Soft lilac surfaces |
| `--font-site` | `Segoe UI, Tahoma, sans-serif` | Site-wide typography |
| `--site-content-width` | `1120px` | Main reading/content column |
| `--site-banner-width` | `1400px` | Inner-page banner and back-link frame |
| `--inner-banner-height` | `150px` | Desktop inner-page banner height |
| `--inner-banner-height-mobile` | `150px` | Mobile inner-page banner **minimum** height (banner may grow taller) |
| `--inner-banner-radius` | `22px` | Desktop inner-page banner corners |
| `--inner-banner-title-size` | `clamp(24px, 2vw, 28px)` | Inner-page banner title |
| `--inner-banner-subtitle-size` | `13.5px` | Inner-page banner subtitle |

When a new global color, font, spacing, radius, or dimension is approved:
1. Add or update one CSS custom property in `:root`.
2. Use that variable in shared components.
3. Update this table.
4. Do not create slightly different values on individual pages without a documented reason.

The canonical tokens are implemented in `assets/css/styles.css` under `:root`. Shared inner-page banner, title, subtitle, and back-link rules are consolidated in the final `GLOBAL DESIGN SYSTEM — CANONICAL SHARED COMPONENTS` section of that stylesheet.

When changing an approved global value, update the corresponding `:root` token and this table. Do not append another page-specific override.

## 4. Shared navigation

Every primary page uses the same shared header and navigation component.

- Keep logo, author mark, navigation links, language flags, spacing, and responsive behavior consistent.
- The active navigation item must have the same blue highlight treatment on every page.
- The active state must follow the current page, including the Contact page.
- Do not remove or rename navigation items on only one page.
- The current primary navigation is: Home, About, Math Education, AI Education, In-Class Learning, My Books, Contact.
- The former “Resources” item is not part of the current primary navigation unless the site owner explicitly restores it.
- Both language versions must show the equivalent navigation labels and active state.

## 5. Four-level page and banner system — mandatory for all new pages

Every page must be assigned to exactly one of the four levels below before its layout is built. The homepage is intentionally separate from the inner-page banner system.

| Level | Page type | Examples | Banner standard | Return link standard |
|---|---|---|---|---|
| 1 | Homepage | `index.html` | Homepage-only hero/banner. Keep its desktop and mobile artwork and layout independent. | No inner-page back link. |
| 2 | Primary navigation page | Math Education, AI Education, In-Class Learning, About, My Books, Contact | Use the shared primary inner-page banner. This is the standard blue-and-gold banner and its approved dimensions, typography, padding, and spacing. | One return link above the banner only when the page design calls for it; align it to the banner frame. |
| 3 | Category / landing page beneath a navigation page | Math Foundations, Math in Real Life, Visual Math & Patterns, Mathematical Thinking | **Use exactly the same banner component and visual rules as Level 2.** Do not create a separate category-banner design. | One return link above the banner. Match Level 2 in position, font, size, weight, color, and spacing. The label and destination reflect the parent page. |
| 4 | Topic / detail page | Number Families and future individual concept pages | Use the distinct topic-level banner style. The current Number Families banner is the approved visual reference: topic-specific, lighter/illustrative, and visually distinct from Levels 2–3. | One return link above the topic banner. Use the same site link typography and alignment system, with wording and destination reflecting the parent category. |

### Required rules for the return link and banner frame

- A page must show **one and only one** return link in the banner area. Never leave an old link in place when adding or replacing a shared link.
- The return link always appears above the banner, not inside the banner artwork.
- On Levels 2 and 3, the return link and banner share the same left alignment and frame width. The vertical gaps above the link and between the link and banner use the shared CSS tokens.
- On Level 4, keep the same clear hierarchy: navigation divider → one return link → topic banner → page content. Align the link and topic banner to the same topic-page content frame.
- Keep the return link live HTML text so it can be translated. Never bake it into an image.
- Do not use two different return-link implementations on the same page. Reuse the shared classes/tokens.
- When a page is created, identify its level in the implementation notes and use the matching existing component. Do not invent a fifth banner type without explicit approval.

### CSS source of truth

- Level 2 and Level 3 use the shared `--inner-banner-*` and `--inner-page-back-*` tokens and the canonical primary-banner/back-link selectors in `assets/css/styles.css`.
- Level 4 uses the `--topic-banner-*` and `--topic-page-*` tokens and the reusable `.topic-page`, `.topic-back-wrap`, and `.topic-banner` classes in the same stylesheet. Topic pages may customize their banner artwork or illustration, but not invent unrelated spacing or return-link typography.
- Level 1 remains controlled by the homepage hero rules and must not be affected by inner-page selectors.
- Markdown defines the design decisions; CSS custom properties and shared classes implement them. Update both whenever an approved shared standard changes.

## 6. Inner-page banner — mandatory shared component

All pages opened directly from the primary navigation use the same inner-page banner component and geometry.

Applies to:
- About
- Math Education
- AI Education
- In-Class Learning
- My Books
- Contact Us

Rules:
- Use the approved blue-and-gold inner-banner artwork.
- Use the same width, height, corner radius, title position, title typography, underline, subtitle position, and internal padding on every listed page.
- The Contact Us banner is the currently selected height reference. All other inner-page banners must match its rendered height, not be taller.
- Measure the actual rendered banner in the browser at the same viewport and zoom when checking equality. Do not infer height from screenshots taken at different zoom levels.
- Use one canonical CSS class and one shared height token. Do not give each page a separate banner height.
- Keep the homepage hero/banner separate; do not change it when editing inner-page banners.
- Mobile uses the approved mobile artwork and shared mobile geometry. Do not let image aspect ratio silently determine the banner height.
- **Mobile banner height must fit all visible text.** On viewports `max-width: 760px`, every inner-page banner (Levels 2–4: compact banner, topic banner, `nf-hero.topic-banner`, contact/legal/book banners, etc.) must use `height: auto`, `min-height: var(--inner-banner-height-mobile)` (150px), and `max-height: none`. Do not fix mobile banners to 150px or clip title/subtitle with `overflow: hidden`, single-line `white-space: nowrap`, or `-webkit-line-clamp`. Longer copy (especially Chinese) must wrap and the panel grows vertically. Level 4 topic banners may use content-driven height on desktop as well.
- Implement this in the shared stylesheet (`assets/css/styles.css`); do not add per-page banner heights on mobile.

### 6.1 Edu panels, formulas, and data tables (mobile)

Applies to `body.edu-page` content (Level 2–3 hubs, real-life lessons such as `math/skateboard-ramp.html`) and similar patterned pages (e.g. `body.car-page` tables).

Rules:

- **Two-column panels** (`.edu-two` / `.edu-panel`): On mobile (`max-width: 760px`), stack to one column. Grid children and panels must use `min-width: 0` and `box-sizing: border-box` so nothing forces horizontal page scroll.
- **Formula displays**: Use class `.edu-formula`, not fixed inline `font-size` (e.g. `26px`). Size with `clamp()`; padding must scale down on mobile.
- **Data tables** (`.edu-table`, `.car-table`, etc.): Do **not** set `min-width` above the viewport (legacy `min-width: 520px` is forbidden). Use `width: 100%`, `min-width: 0`, and `table-layout: fixed`. Allow header/cell text to wrap (`word-break` / `overflow-wrap`). On mobile, reduce cell padding and font size (about 12px).
- **Implementation**: Canonical rules live in `assets/css/styles.css` (`EDU / REAL-LIFE CONTENT`). Page-level `<style>` blocks may add layout-only rules but must not reintroduce fixed table widths or non-scaling formula panels. Reference markup: `math/skateboard-ramp.html`.

### 6.2 Mnemonic rule tables (sign rules, exponent parity, roots, etc.)

Use when a **single table** teaches a **short rule to memorize** plus **one or more category sections** with example rows (legacy Word nested tables must be flattened).

**Markup**

- Wrapper: `<div class="edu-table-wrap">`
- Table: `<table class="edu-table kiwi-edu-table-with-mnemonic">` with `table-layout: fixed`, full width (`display: table` on `.mf-article` pages — not `display: block` on `<table>`).
- Row 1 (memorize): `<thead><tr class="kiwi-edu-table-mnemonic"><th colspan="3">…</th></tr></thead>` — one cell, centered rule text (often `<strong>…</strong>`), EN/ZH on `th` via `data-en` / `data-zh`.
- Categories: in `<tbody>`, each section starts with `<tr><th colspan="3">Category title</th></tr>` followed by normal `<tr><td>…</td>…</tr>` data rows.
- Do **not** nest `<table>` inside `<th>`. Do **not** use a single-cell outer `width: 100%` colgroup wrapper.

**Visual (canonical CSS in `styles.css`)**

- Mnemonic row: background `#fff8e8`, border `#f0dfad`, top corners `12px` rounded; **memorize text** `#b85f0c`. Tip panel titles (Learning Insight) use the same `#b85f0c` (global CSS in `styles.css`).
- Category title rows: background `#f1f5fa`, title color `#174a82`, centered.
- Data rows: default `.mf-article` / `.edu-table` cell borders.

**Reference pages:** `math/foundation-math-operation-signs-and.html`, `math/foundation-result-signs-and.html`, `math/foundation-exponents.html`, `math/foundation-roots.html`.

**Batch tool:** `python tools/apply_mnemonic_table.py` (converts legacy nested mnemonic tables on foundation pages).

### 6.3 Row-column header tables (property × category comparisons)

Use when the **first column lists row properties** (Form, Degree, Δy, …) and the **header row names categories** (Linear, Quadratic, Constant). This is not a mnemonic rule table (§6.2).

**Markup**

- Wrapper: `<div class="edu-table-wrap">`
- Table: `<table class="edu-table kiwi-edu-table-row-column-header">` — add `table-layout: fixed` and `<colgroup>` as needed.
- `<thead>`: one row of column titles; first cell is the corner label (e.g. Property).
- `<tbody>`: first cell in each row is the row label (`<td>` or `<th scope="row">`); remaining cells are values.

**Visual (canonical CSS in `styles.css`)**

- Header row **and** first column (including corner): background `#f3f8fe`, **bold** (`700`).
- Body value cells: default white background, normal weight.
- All cells: **left-aligned** (same as default data tables on `.mf-article`).

**Reference pages:** `math/foundation-linear-vs-non-linear-functions.html` (Comparison Table), `math/foundation-rational-exponents.html` (Laws of Exponents), `math/car-journey.html` (model comparison uses `car-table` + same class).

**Batch tool:** `python tools/apply_row_column_header_table.py` (adds the class to non–data-grid tables with `<thead>`; skips mnemonic tables and numeric first-column grids such as `t (s)` / `x` value tables).

### Banner text

- Title typography must be identical across pages and languages at equivalent responsive breakpoints.
- Subtitle typography must be identical across pages: font family, size, weight, color, letter spacing, line height, and text treatment.
- Keep subtitles short enough to preserve generous empty space. Prefer a concise phrase over a long sentence.
- Do not add decorative kicker labels such as “QVS Study”, “Mastery”, or other extra headings unless explicitly requested.
- Preserve the approved title underline and text contrast treatment.
- Do not put text into the banner background image itself; title and subtitle remain live HTML text so they can be translated and resized.

## 7. Breadcrumb trail and page alignment

Primary wayfinding above the Level 2 banner is the **breadcrumb** (`Home › Section name › …`), not a permanent visible “← Back” line.

- Load `assets/js/drive-breadcrumb.js` on every inner page that participates in the site hierarchy.
- The script removes `.page-back-wrap` (and legacy `.edu-back` / `.ai-back`) and inserts `.drive-breadcrumb` as the first child of `<main>`.
- Register each new page in the `pages` object inside `drive-breadcrumb.js` with `en`, `zh`, and `parent` (use `parent: ""` for direct primary-nav landings such as About, Math Education, AI Education, My Books, and Contact).
- Keep a `.page-back-wrap` link in the HTML as a no-JavaScript fallback; it is replaced when the script runs.
- The breadcrumb, banner, and main content should share the same horizontal alignment and content width tokens.
- Do not use page-specific margins to compensate for a wrong parent container width.

### Level 2 page template (copy source)

File: `templates/level-2-primary-nav.html`

Use this file when creating or rebuilding a **Level 2 primary navigation** landing page (see §5). It is **not** served directly; copy it into the target folder (for example `math/index.html`).

| Shell (fixed in template) | Per page |
|---|---|
| `site-header`, `site-nav`, language flags | One `class="active"` on the matching `data-nav` link |
| Fallback `.page-back-wrap` + `drive-breadcrumb.js` | Breadcrumb registry entry |
| `.compact-page-banner.about-compact-banner` | Banner `h1` + `.compact-banner-subtitle` (`data-en` / `data-zh`) |
| `site-footer` + shared language script | `<title>`, meta description |
| | All sections between `LEVEL-2 BODY` markers |

Approved `body` / `<main>` pairs:

- `about-page` → `<main>` (no extra class) — About
- `edu-page` + `edu-main` — Math Education, My Books (and shared edu section styles when needed)
- `ai-page` + `ai-main` — AI Education hub
- `contact-page` + `contact-main` — Contact (banner may add `contact-banner` when required)

**In-Class Learning** is a top-nav destination but lives at `math/in-class-learning.html`; clone that page or set breadcrumb `parent` to `math/index.html`, not the Level 2 shell alone.

Reference implementations: `about/index.html`, `math/index.html`, `ai/index.html` (Level 2 shell applied), `books/index.html`, `contact/index.html`.

### Level 3 page template (copy source)

File: `templates/level-3-category.html`

Use for category hubs beneath a Level 2 nav page (Level 3 in §5): same compact blue-gold banner as Level 2, not the Level 4 topic banner.

| Shell (fixed in template) | Per page |
|---|---|
| `body.edu-page` + `main.edu-main` | Breadcrumb `parent` = Level 2 hub (e.g. `math/index.html`) |
| Fallback `.page-back-wrap` + `drive-breadcrumb.js` | No active primary nav |
| `.compact-page-banner.about-compact-banner` | Short `.compact-banner-subtitle`; longer intro in body `.edu-lead` |
| `site-footer` + shared language script | `<title>`, meta description |
| | Sections between `LEVEL-3 BODY` markers |

Page CSS is content-only (grids, topic lists, callouts). Do not override `.edu-main` width or banner geometry in `styles.css`.

Reference implementations: `math/math-foundations.html`, `math/math-real-life.html`, `math/visual-math-patterns.html`, `math/mathematical-thinking.html`.

### Level 4 page template (copy source)

File: `templates/level-4-topic.html`

Reference implementation: **`math/number-families.html`**. Use for topic/detail/leaf pages (Level 4 in §5): gradient topic banner, not the Level 2 blue-gold compact banner.

| Shell (fixed in template) | Per page |
|---|---|
| `body.topic-page` + `main.topic-main` | Breadcrumb `parent` = Level 3 category (or hub) |
| Fallback `.page-back-wrap` + `drive-breadcrumb.js` | No active primary nav |
| `.nf-hero.topic-banner` with kicker, `h1`, `.topic-banner-subtitle` | Kicker, title, short subtitle (`data-en` / `data-zh`) |
| `site-footer` + shared language script | `<title>`, meta description |
| | Sections between `LEVEL-4 BODY` markers |

Do not add page-specific CSS that changes banner height, padding, gradient, or title scale; use the shared rules in `assets/css/styles.css` (`.nf-hero.topic-banner`).

## 8. Main content layout

- The main content should align with the banner's left and right edges unless a page has an explicitly approved alternate layout.
- Use the shared maximum content width (`1120px` in the current design) and center it.
- Cards in the same row should have consistent heights, gaps, corner radii, borders, and shadows.
- Use responsive grids that collapse cleanly on smaller screens.
- Do not let content overflow the banner or page container.
- The homepage's introductory section and mascot/character illustration are important content and must not be removed as a side effect of changing the homepage navigation cards.

## 9. Typography and color

### Body H2 standard

- Every H2 heading in the main page content uses the same typography as the inner-page Banner Title.
- The shared CSS token is `--body-h2-size`, linked directly to `--inner-banner-title-size`.
- All body H2 headings use the same navy color, Segoe UI font, 700 weight, and 1.2 line height.
- No body H2 may be larger than the Banner Title.
- Individual page styles must not override H2 size, color, font weight, or line height.
- H3 and lower headings remain subordinate to H2 and must not be styled larger than H2.


- Use the site-wide Segoe UI font stack.
- Main headings use the approved navy color.
- Links and active navigation use the approved blue.
- Body text uses the approved body color and consistent readable line height.
- Equivalent heading levels must have consistent sizes and weights across pages.
- Do not set arbitrary local font sizes if a shared heading or body class already exists.
- English and Chinese versions should have equivalent hierarchy and visual weight; adjust text length or line breaks where needed without changing the shared component dimensions.

## 10. Language switching

- Every bilingual page must support the same English/Chinese language switcher.
- Use the same flag controls, selected-language treatment, and persistence behavior.
- All visible page text, navigation labels, buttons, form labels, validation messages, and page metadata intended for visitors must switch correctly.
- A page is not complete until both languages have been tested.
- Do not change the homepage mobile banner or other language-specific hero assets when fixing an unrelated page.

## 11. Forms and interactions

- Contact form submissions must continue to use the approved Formspree endpoint configured for the project.
- Keep the visitor's reply email field, subject/topic selection, message field, and spam-trap honeypot.
- Do not expose the honeypot visually or remove it during styling changes.
- Keep success and error feedback understandable in both languages.
- Never replace a working form endpoint with a placeholder.

## 12. Images and assets

- Reuse approved assets from `assets/` rather than recreating or duplicating them.
- Do not stretch logos, book covers, mascot artwork, or illustrations.
- Preserve the homepage mascot/character illustration and homepage introduction unless the owner explicitly requests a change.
- Keep homepage hero images independent from inner-page banner images.
- Optimize image file sizes without changing the approved visual composition.

## 12. Change-control rules

Before editing:
1. Read this file.
2. Inspect the existing page and shared CSS.
3. Identify the shared component or token responsible for the requested change.
4. Confirm which pages could be affected.
5. Preserve all unrelated approved content and assets.

After editing:
1. Check the edited page in English and Chinese.
2. Check desktop and mobile layouts.
3. Check the navigation active state and all links.
4. Compare banner dimensions, title/subtitle typography, back-link alignment, and body spacing against the approved reference.
5. Check the homepage separately if shared CSS was changed.
6. Search for duplicate or conflicting CSS rules introduced by the change.
7. Package the complete site in a ZIP and verify the ZIP contents before sharing it.

## 13. Approval and exceptions

- The site owner’s latest explicit visual approval takes precedence over older drafts.
- A page-specific exception must be explicitly approved and documented here.
- Never silently change a global standard to solve a local page issue.
- When two screenshots appear different, compare them at the same browser viewport, zoom, and device scale before changing dimensions.
- If the exact measurement is uncertain, inspect the rendered page and shared CSS first; do not guess a new value.


## Heading hierarchy

Use semantic heading levels consistently across inner pages:

- H1: the inner-page banner title (one page-level H1).
- H2: each major content section in the page body. Multiple sibling H2 headings are appropriate when sections are parallel.
- H3: subsections or cards grouped under an H2.
- H4: only when a genuine fourth level of content nesting is needed.
- Eyebrow labels, taglines, captions, diagram labels, and flow-step labels are not headings. Use paragraph, span, or strong text instead.

All body H2 headings use the shared deep-blue heading color `#123B73` and the shared H2 size token. Do not create oversized body H1 headings. Preserve established layout and spacing when correcting semantic heading tags.


### First content heading spacing
- On inner pages, keep the vertical distance from the bottom of the banner to the first main content heading visually consistent.
- The Math Education page is the reference for this spacing.
- On the About page, the mascot grid vertically centers the intro copy; compensate for this without moving the mascot or changing other sections.


### Math Education card images
- Keep the four Math Education card images fully visible; do not crop book covers or instructional diagrams.
- Use a consistent image-frame height, centered contain behavior, and a soft neutral-blue background with balanced internal padding.


### Math Education card artwork
- The four Math Education cards use dedicated landscape artwork designed for the card image frame.
- Keep a consistent 1200 × 448 px source size and use a full-width cover crop.
- The original book covers and learning diagrams remain in the asset library and are not overwritten.


### Math in Real Life graph accuracy
- The card illustration for y = a t² uses a = 1, 3, and 5.
- Time runs from 0 to 5 seconds; the vertical scale runs from 0 to 140.
- At t = 5, the three plotted values are 25, 75, and 125 respectively.


### Math in Real Life quadratic graph
- Use y = a t² with a = 6, 8, and 10.
- Time axis: 0 to 3 seconds.
- Speed axis: 0 to 90 km/h.
- At t = 3, the values are 54, 72, and 90 respectively.
- Blend the car/road illustration into the graph background without a visible dividing line.


### Math Education card image sizing
- All four Math Education cards use the same image-frame height: 205px.
- Keep the image frames visually consistent; do not enlarge an individual card image independently.

## 13. New-page implementation checklist

Before publishing a new page:

1. Assign Level 1, 2, 3, or 4.
2. Reuse the matching shared banner class and CSS tokens.
3. Add no more than one parent/back link; verify the old link was removed if replacing it.
4. Check the banner and return-link alignment, spacing, and typography at desktop and mobile widths.
5. Test English and Chinese text, including the return-link label.
6. Confirm the homepage hero is unchanged when editing any inner-page banner.

## Image optimization and asset size — mandatory

All new images and replacement images must be optimized before they are added to the website. The goal is the smallest practical file size that still looks clear and works correctly at the actual size displayed on the website. Do not use unnecessarily high-resolution or oversized image files.

- **Preferred format:** WebP for photographs, banners, book covers, cards, illustrations, and other raster images. Use SVG for suitable vector artwork and icons.
- **Fallbacks / exceptions:** Keep PNG when lossless quality or transparency is essential and WebP does not meet the visual requirement. Keep JPEG when it is already smaller or WebP would make the file larger without a visible quality improvement.
- **Right-size every image:** Resize to the maximum dimensions actually needed by the website, allowing for high-density screens where appropriate. Do not upload a 3000–4000 px image when a much smaller image will display just as clearly.
- **Quality target:** Use a sensible WebP quality setting (normally around 80–90) and visually inspect the result. Adjust quality only as needed to avoid visible artifacts, blurry text, jagged edges, or damaged fine details.
- **Preserve transparency:** Logos and illustrations that require transparent backgrounds must retain transparency after conversion.
- **Do not sacrifice usability:** Text in graphics, mathematical symbols, diagrams, labels, and fine lines must remain readable at the intended display size. If compression makes them unclear, use a higher quality setting or a more suitable format.
- **Update references:** When changing an image's filename or format, update every HTML, CSS, JavaScript, and other reference to it. Remove obsolete copies from the active website folder after verifying that no page uses them.
- **Verify before publishing:** Check the image on desktop and mobile, confirm that it loads without errors, and inspect important pages such as the homepage, books, math, and AI sections. Check the browser console/network panel for missing asset requests.
- **Keep source artwork separately when needed:** If an editable or lossless master is important, store it outside the deployed website assets or in the project's source/archive location. The deployed website should contain only the optimized assets it actually uses.

**Default rule:** Use the lowest file size that preserves a clear, professional appearance on the website. Maximum resolution is not the goal; sufficient visual quality with efficient loading is.

## Body text color — mandatory site-wide standard

All main body text across the website must use one consistent near-black color for comfortable reading.

- **Body text color:** `#222222`.
- Apply this consistently to paragraphs, list items, explanations, examples, captions, table text, and instructional copy across all non-legal pages.
- Keep headings in the approved navy/blue heading colors.
- Keep links, navigation states, buttons, badges, and brand accents in their existing approved colors.
- Legal pages under `legal/` are excluded from this global body-text rule and may retain their own typography and color treatment.
- Do not introduce page-specific muted blue-gray body text colors. If a new component needs body copy, use `#222222`.

When updating shared typography or colors, implement the rule in `assets/css/styles.css` and keep this document as the source of design guidance.

## Bilingual body typography — mandatory site-wide standard

All non-legal website body text must follow one consistent typography system in both English and Chinese. The homepage feature cards (Math Education, AI Education, and In-Class Learning) must match the body text in Latest Books and all other content pages.

- **Body font size:** 15 px on desktop and mobile.
- **Body font weight:** 400 (regular).
- **Body line height:** 1.55.
- **Body text color:** `#222222`.
- Apply consistently to paragraphs, list items, table text, explanations, examples, captions, and instructional copy across Homepage, Math, AI, Books, About, Contact, and other non-legal pages.
- English body text keeps the existing site font stack (`Segoe UI`, then fallbacks).
- Chinese body text uses `Microsoft YaHei`, with `PingFang SC` and `Noto Sans SC` fallbacks.
- Headings retain their existing size hierarchy, weights, and navy/blue colors.
- Navigation, links, buttons, badges, labels, and decorative/brand text retain their existing styles.
- Legal pages are excluded and keep their independent typography.
- Do not introduce page-specific body font sizes, weights, or line heights. New body copy must inherit this shared standard.

The shared rule is implemented in `assets/css/styles.css`. If a page-specific selector overrides body typography, remove that override or update it to comply with this standard.

## Math Foundations topic-page banner alignment

The Number Families page is a child topic page of Math Foundations. Its page container, breadcrumb, vertical spacing, and banner typography must match the Math Foundations page template. Only the banner background treatment and page-specific wording may differ. Keep the kicker uppercase, omit decorative separator dots, and preserve readable text contrast against each page's own background.


### Number Families banner typography correction

- The Number Families subtitle remains sentence case, regular weight, and normal letter spacing. Do not force it to uppercase or bold.
- Its main title must use the same restrained size scale as the Math Foundations banner, not the oversized 50px topic-heading scale.
- The Back link must use the shared inner-page back-link style and color.


### Banner height consistency

All banners within the same page-template family must share the same height. The Number Families banner uses the same fixed 150px height as the other inner-page banners on desktop and mobile.


## Inner-page banner height — mandatory standard

All inner-page banners use a consistent fixed height of **150px** on desktop and mobile. This includes section and topic banners, book banners, AI banners, Contact, About, and legal banners. The homepage hero is explicitly excluded: preserve its original responsive aspect ratio and artwork proportions; do not force it to a fixed height or stretch its image. Keep inner-page banner content within 150px by adjusting internal spacing or text sizing rather than changing the shared height.


## Image asset optimization (mandatory)

Every image newly added to the website, and every replacement image, must be optimized for web display before it is committed to the site. The goal is **clear appearance at the actual on-screen display size**, not maximum source resolution or print quality.

### Required workflow

1. Check where and how the image will appear (hero/banner, card, content illustration, logo, or portrait) and determine its largest rendered size on desktop and mobile.
2. Resize the image to a sensible pixel dimension for that use. Do not upload a 3000–6000 px source when the page displays it at a few hundred pixels. Do not upscale small originals.
3. Prefer **WebP** for photographic and illustrated raster images. Use AVIF only when the existing build/deployment workflow supports it reliably. Keep SVG for clean vector logos/icons when available.
4. Compress the resized image and visually inspect the result at its real website display size. Text, fine lines, faces, and mathematical labels must remain legible; if artifacts are visible, increase quality slightly rather than keeping an unnecessarily huge file.
5. Use descriptive, lowercase, hyphen-separated filenames. Store the image in the existing appropriate `assets/` or section-specific image folder. Reuse an existing image instead of creating another copy when possible.
6. Update every affected HTML reference and check that the image loads correctly on desktop and mobile. Do not leave unused high-resolution originals in the deployed website folder.

### Practical export targets

These are guidelines, not rigid limits. A visually clear image may exceed a target when its detail genuinely requires it; do not sacrifice legibility just to hit a number.

| Image use | Suggested maximum dimensions | Preferred target file size |
|---|---:|---:|
| Small icon / logo | Use SVG when possible; otherwise 300–600 px | 10–60 KB |
| Card / thumbnail | 600–900 px on the longest edge | 40–120 KB |
| Standard content image / illustration | 900–1200 px on the longest edge | 80–180 KB |
| Portrait / 3:4 or 4:3 feature image | About 1000–1200 px on the longest edge | 100–200 KB |
| Wide hero / banner | About 1600 px wide, or the actual required banner dimensions | 150–300 KB; up to 400 KB if needed |

### Format and quality guidance

- For WebP, start around **quality 78–85** and adjust after visual inspection.
- For JPEG, start around **quality 75–82** when WebP is not suitable.
- Strip unnecessary metadata such as camera, editing, and location metadata from public website images.
- Keep transparency when it is required for logos or overlays; use lossless WebP or optimized PNG only when necessary.
- Avoid saving multiple language/size variants unless the page actually uses them. Before generating variants such as `16x9`, `4x3`, and `3x4`, confirm each variant has a real placement in the site.
- Do not replace a crisp image containing important text or math notation with a version that makes the text blurry. Optimize dimensions first, then compression.
- Do not commit large source files, duplicate exports, or unused alternatives to the production website.

**Default rule:** if an image is larger than approximately **250 KB**, review whether its dimensions or compression can be reduced before adding it. Images above **400 KB** require a clear reason to remain that large. These are review thresholds, not automatic rejection limits.


## Inner-page banner standard (mandatory)

All inner-page banners must use the same shared banner component and dimensions as the existing inner pages (`.compact-page-banner.about-compact-banner`). Do not create a taller, wider, or page-specific hero banner for an inner page.

- Keep the banner height consistent across all inner pages: use the shared CSS height rule in `assets/css/styles.css` (desktop `clamp(140px, 9.24vw, 177px)`; mobile `150px`).
- Keep the banner text-only: title and short subtitle only.
- **Do not place images, illustrations, icons, emoji, SVGs, or decorative graphics inside an inner-page banner.**
- Do not add a second visual column or increase banner height to accommodate artwork.
- Keep page-specific diagrams, images, icons, and illustrations in the content sections below the banner.
- Reuse the existing shared CSS component; do not override its height on individual pages.


## Card icon and emoji placement (mandatory)

Inside content cards, small icons and emoji must not occupy a separate row above the heading or description. Place the icon at the left side of the card and let the heading and body text flow beside it, then continue naturally below it when the text is longer (float/wrap treatment). Keep the icon compact and vertically aligned near the start of the text. This rule applies to all new and existing learning/content cards. Do not apply this rule to page banners, where icons and emoji are prohibited entirely.


## Content-card icon column (mandatory)

For cards containing an icon or emoji, use a dedicated narrow left column for the icon and a separate right text column for the heading and description. The heading and description must both remain in the right column; text must never flow or wrap underneath the icon. It is acceptable for the area below a short icon to remain empty. Do not use float-based text wrapping for these cards. This applies to all content and learning cards. Banners remain text-only and must not contain icons or imagery.


## Primary navigation active highlight (mandatory)

Only pages that are direct destinations of the main navigation may show the active/highlighted navigation state. On deeper inner pages, lesson pages, episode pages, and individual book/detail pages, do not highlight the parent navigation item merely because the page belongs to that section. The About page is the explicit exception and keeps its About highlight. Keep active states on the main landing pages for Home, Math Education, AI Education, In-Class Learning, My Books, Contact, and About.


## Supplied lesson scripts are the source of truth

When the user provides a complete lesson/video script, the corresponding episode page must be built from that supplied script. Do not replace it with a shortened generic summary or independently invented lesson copy. Preserve the supplied structure, examples, sequence, key wording and next-episode preview. English may be translated faithfully for the bilingual site, but the supplied Chinese script remains the source of truth.


## Lesson-page editorial layout

A supplied video script is the source for the lesson content, but the website page is a learning article, not a screenplay or teleprompter transcript. Preserve the full ideas, examples and teaching sequence while combining related sentences into coherent paragraphs and organizing them under clear section headings. Do not put every spoken sentence on a separate line unless the content is genuinely a list or emphasis. Do not add a large decorative next-episode banner at the end of a lesson. A brief next-lesson link or compact text note is sufficient.

**AI Knowledge Class episode magazine pages:** follow **`docs/AI_EPISODE_MAGAZINE.md`** (image–text pairing, student tone, `.ep-pair` layout). Reference: `ai/episode-01.html`.


## Learning article density and navigation (mandatory)

Learning pages must read like polished textbook/web articles, not line-by-line scripts. Use a restrained heading hierarchy: group related ideas under a small number of meaningful section headings, and use bold inline lead-ins for subtopics instead of creating a separate large heading for every point. Develop each paragraph enough to explain the idea with context and an example; avoid one-sentence fragments and excessive highlighted heading text. Do not add a separate next-lesson promo card when the page's bottom navigation already links to the next lesson. Keep only one clear next-lesson navigation destination.


## Canonical inner leaf-page banner standard — Number Families

The **Number Families** banner (`math/number-families.html`) is the single visual source of truth for every deepest-level / last-page banner across the website. New or revised leaf pages must reuse the shared `.topic-banner` component in `assets/css/styles.css`; do not invent page-specific banner dimensions or typography.

Required shared structure:
- One text-only banner with a category kicker, one H1 title, and one short subtitle.
- No images, illustrations, icons, emoji, SVGs, or decorative artwork inside or behind the banner.
- Reuse the shared background gradient, border, radius, spacing, typography, colors, and responsive rules exactly.
- The kicker uses the shared blue bold uppercase style; the H1 and subtitle use the Number Families font scale, color and spacing.
- Do not set a fixed page-specific height. Let the shared padding and content determine the banner height.
- Use the same shared `.topic-banner` class and child classes: `.topic-banner-kicker`, `h1`, and `.topic-banner-subtitle`.
- Keep the page container width and horizontal gutters aligned with the Number Families topic-page layout.
- Before adding a new last-level page, reuse this component rather than copying or modifying its CSS locally.

This standard applies to all new and existing deepest-level pages, including AI lessons, episode detail pages, math topic pages, and individual detail pages. The Number Families page itself must continue using the same shared component so it remains the reference implementation.


Correction: the shared last-level banner must reuse the exact `.nf-hero.topic-banner` implementation from Number Families, including its existing font sizes, spacing, gradient and responsive behavior. Do not approximate it with a separately styled `.topic-banner` rule.

When applying or updating a banner, change only the banner markup/classes and shared banner CSS. Preserve the existing article layout, image placement, body content, breadcrumbs, and navigation. In Episode 1, the cover image belongs in the article flow at the right on desktop and must not become a full-width image immediately below the banner.


Correction based on the final Number Families implementation: desktop leaf-page banner is exactly 150px high, padding 24px 46px, margin 14px 0 34px, 24px radius, kicker 12px/800/#2676b7, H1 clamp(29px, 3.2vw, 38px), subtitle 16px/#405875. Mobile uses auto height, min-height 150px, padding 24px 23px and 29px H1. Never use a larger generic 50px topic-banner heading on these pages.

Episode detail navigation must retain the existing flex layout: left-side All AI Episodes link and right-side episode link, with divider, top padding and spacing. Banner changes must not alter navigation or article layout.


## Canonical deepest-level banner — Version 1.3
All deepest-level/detail pages reuse the exact Number Families banner: 150px desktop height, 24px 46px padding, 14px 0 34px margin, 24px radius, gradient `linear-gradient(112deg,#dff3ff,#eaf0ff 58%,#fff1d8)`, 12px kicker, 38px maximum title scale and 16px regular subtitle. On mobile use auto height, 150px minimum height, 24px 23px padding and 29px title. Use `nf-hero topic-banner` and `topic-banner-kicker` classes.

Do not alter page breadcrumbs, article content, images, image positions, bottom navigation or footer when changing a banner. Top-level and category/overview pages retain their hierarchy-specific banner design.


## Canonical deepest-level page banner standard

**Source of truth:** `math/number-families.html` — the approved Number Families banner. Every deepest-level/detail page must reuse this exact shared component. Do not create a page-specific variation.

### Required HTML structure

```html
<section class="nf-hero topic-banner" aria-label="Page introduction">
  <p class="topic-banner-kicker">SECTION LABEL</p>
  <h1>Page Title</h1>
  <p class="topic-banner-subtitle">Short page introduction.</p>
</section>
```

### Exact desktop styling

- Height, min-height and max-height: `150px`.
- Padding: `24px 46px`.
- Margin: `14px 0 34px`.
- Border: `1px solid #d8e8f8`.
- Corner radius: `24px`.
- Background: `linear-gradient(112deg, #dff3ff, #eaf0ff 58%, #fff1d8)`.
- Layout: flex column, vertically centered.
- Kicker: `12px`, weight `800`, color `#2676b7`, letter spacing `.14em`, bottom margin `12px`.
- H1: `clamp(29px, 3.2vw, 38px)`, weight `700`, color `#123d75`, line-height `1.12`, bottom margin `14px`.
- Subtitle: `16px`, regular weight, color `#405875`, line-height `1.6`, max-width `850px`.

### Mobile styling

- Height: `auto`; min-height: `150px`; max-height: `none`.
- Padding: `24px 23px`.
- H1: `29px`.
- Preserve the same gradient, border, radius and text hierarchy.

### Content and change boundaries

- The banner contains text only: no images, illustrations, icons, emoji, SVGs or decorative artwork.
- Replace only the kicker, H1 and subtitle text for each page.
- Do not change breadcrumbs, article content, page width, image placement, bottom navigation or footer when standardizing a banner.
- Do not add page-specific banner heights, typography, gradients, padding or corner radii.
- Homepage, primary navigation pages and category/overview pages keep their own hierarchy-specific banner designs; this rule applies only to deepest-level/detail pages.

### Required workflow for new deepest-level pages

1. Identify the page as a deepest-level/detail page.
2. Reuse the shared `nf-hero topic-banner` markup and the canonical CSS in `assets/css/styles.css`.
3. Replace only the category kicker, page title and short subtitle.
4. Keep all existing page content, images, breadcrumbs and navigation intact.
5. Check desktop and mobile rendering against `math/number-families.html` before publishing.

The canonical CSS is maintained once in `assets/css/styles.css`. This Markdown section is the durable project rule for future edits; do not create a separate Word specification.


### Banner text-length limits (mandatory)

- The category kicker must remain on one line.
- The main page title must remain on one line. If necessary, reduce its responsive font size; do not allow it to wrap onto a second line.
- The subtitle must display no more than **two lines** on desktop or mobile. Keep it concise and summarize the page rather than placing a full paragraph in the banner.
- Use the shared CSS line clamp for two lines. Prefer editing overly long subtitle copy so the complete key message fits within those two lines; do not rely on clipping to hide essential information.
- The banner must grow naturally to fit the kicker, one-line title and up to two subtitle lines. Do not use a fixed height that cuts off any text.


## Final canonical leaf-page banner specification — v2

**This is the single source of truth for every deepest-level / last-page banner.**
The approved visual reference is `math/number-families.html`. Every leaf page must use
`<section class="nf-hero topic-banner">` and the shared CSS block named
`FINAL CANONICAL LEAF-PAGE BANNER STANDARD — v2` in `assets/css/styles.css`.
Do not create page-specific banner CSS.

### Desktop measurements and typography

| Part | Required value |
|---|---|
| Banner background | `linear-gradient(112deg, #dff3ff, #eaf0ff 58%, #fff1d8)` |
| Border | `1px solid #d8e8f8` |
| Corner radius | `24px` |
| Width | `100%` of the page content container |
| Height | Natural/content-driven; `min-height: 150px`; no fixed or maximum height |
| Padding | `24px 46px` |
| Margin | `14px 0 34px` |
| Layout | Flex column, vertically centered |
| Kicker font | Segoe UI, `12px`, weight `800`, line-height `1.2`, letter spacing `.14em`, color `#2676b7` |
| Kicker spacing | `12px` below |
| Main title font | **Segoe UI**, `38px`, weight `700`, line-height `1.12`, letter spacing `-.025em`, color `#123d75` |
| Title spacing | `14px` below |
| Subtitle font | Segoe UI, `16px`, weight `400`, line-height `1.6`, color `#405875`, max-width `850px` |
| Subtitle length | Maximum **2 lines** |

### Mobile measurements and typography

- Horizontal/vertical padding: `24px 23px`.
- Banner height remains content-driven, with `150px` minimum and no maximum.
- Main title: Segoe UI, `29px`, weight `700`, line-height `1.12`.
- Subtitle: Segoe UI, `15px`, line-height `1.55`, maximum 2 lines.
- Keep the same gradient, border, radius, colours and text hierarchy.

### Text and layout rules

1. The kicker stays on one line.
2. The main title stays on one line. Keep the specified font family, weight and size; do not enlarge it or replace it with a different heading style.
3. The subtitle is a concise page summary and must not exceed two lines. Shorten the wording when necessary; do not hide important information through clipping.
4. The banner height must grow naturally to fit its contents. Never force a fixed `150px` height or crop the title/subtitle.
5. No images, icons, emoji, SVGs or decorative artwork inside the banner.
6. Only the kicker, title and subtitle text vary from page to page.

### Implementation rule

All deepest-level pages must reuse the same `.nf-hero.topic-banner` component and the one
canonical CSS block in `assets/css/styles.css`. The Markdown file is the permanent project
standard. When changing the standard, update this section and the shared CSS together.
Never create a separate Word specification.

When applying the banner, do not modify breadcrumbs, page content, images, image placement,
bottom navigation, footer or page width. Homepage, navigation landing pages and category/
overview pages retain their separate hierarchy-specific banner designs.


## Final canonical leaf-page banner specification — v3 (supersedes v2)

This is the single source of truth for every deepest-level / last-page banner.
All pages reuse `.nf-hero.topic-banner` and the shared CSS block
`FINAL CANONICAL LEAF-PAGE BANNER STANDARD — v3` in `assets/css/styles.css`.
Do not create page-specific banner CSS.

### Desktop specification

| Part | Required value |
|---|---|
| Background | `linear-gradient(112deg, #dff3ff, #eaf0ff 58%, #fff1d8)` |
| Border / radius | `1px solid #d8e8f8` / `24px` |
| Height | Content-driven; minimum `150px`; no fixed or maximum height |
| Padding / margin | `24px 46px` / `14px 0 34px` |
| Kicker | Segoe UI, `12px`, weight `800`, line-height `1.2`, letter spacing `.14em`, color `#2676b7` |
| Main title | **Segoe UI, `36px`, weight `700`, line-height `1.25`, letter spacing `-.025em`, color `#123d75`** |
| Title spacing | `12px` below; `2px` top and `3px` bottom internal padding |
| Subtitle | Segoe UI, `16px`, weight `400`, line-height `1.6`, color `#405875`, max-width `850px` |
| Subtitle length | Maximum **2 lines** |

### Mobile specification

- Padding: `24px 23px`.
- Content-driven height, minimum `150px`.
- Main title: Segoe UI, `28px`, weight `700`, line-height `1.25`.
- Subtitle: Segoe UI, `15px`, line-height `1.55`, maximum 2 lines.

### Mandatory text and layout rules

1. Kicker remains on one line.
2. Title remains on one line and uses the exact font family, size, weight and line-height above.
3. Do not apply `overflow: hidden` to the H1. Preserve its line box and vertical padding so letters with descenders, such as `y` and `g`, are never clipped.
4. Subtitle is a concise summary of no more than two lines. Shorten wording when needed instead of hiding essential content.
5. Banner height grows naturally; never crop its text.
6. No images, icons, emoji, SVGs or decorative artwork inside the banner.
7. Only kicker, title and subtitle text vary between pages.

All deepest-level pages must use the shared component and CSS. Keep this rule in Markdown;
do not create a separate Word specification. Do not alter breadcrumbs, body content,
images, bottom navigation or footer when applying the banner. Homepage, navigation landing
pages and category/overview pages retain their separate hierarchy-specific banner designs.


## AI Knowledge Classroom — student-friendly lesson page standard

For lesson pages aimed at middle-school and high-school learners, avoid long uninterrupted
text blocks. Preserve the teaching content, but break explanations up with compact visual
learning aids: simple diagrams, illustrated real-world examples, comparison cards and short
capability summaries. Use the site's light backgrounds, navy/blue typography, rounded cards,
clear spacing and restrained decoration. Keep visuals bilingual through `data-en` / `data-zh`
when the page supports language switching. Use lightweight inline SVG or optimized local
illustrations; do not turn the whole page into a poster or place text inside decorative images.
For Episode 1, the visuals explain: app → AI model → response; the car-brand analogy; AI in
cars, medical imaging and factory robots; recognition/prediction versus generation; human
judgement and checking; and the five broad AI abilities. Keep the original explanations and
episode navigation intact.


## Episode learning pages — bilingual comic format (approved for Episode 1)

- The episode introduction appears before all comic illustrations and is localized independently in Chinese and English.
- Use a lively, age-appropriate introduction of approximately 200–250 Chinese characters; provide a natural English equivalent.
- Present 6–8 separate comic illustrations as individual responsive cards, not one long composite poster.
- Each card has a concise scene title and a short explanatory caption.
- Keep the existing shared header, topic banner, language switcher, footer, and next/previous episode navigation unchanged.
- Character artwork should follow the established Episode 1 girl and white-blue robot references; do not redraw or alter the site-wide mascot or unrelated page art.


## Word-to-Web Conversion & Mathematical Content Standards (Approved)

### Scope and source hierarchy

- Apply these rules to converting **Math Quick Reference Library – Advanced** Word content into KIWI 爱AI Study topic pages. The Word book supplies content, but the website is **not** a synchronized companion edition: never embed book page numbers or require identical chapter order.
- Preserve all teaching content, examples, formula meaning, figures and pedagogical sequencing unless the user explicitly requests restructuring. Do not include Worksheet or Answer Key sections when excluded by the task.
- Use existing site templates and CSS; do not rebuild global header, footer, breadcrumbs or language switching. Check existing topic URLs before creating new ones.
- Level 3 **Mathematical Thinking** is a compact, single-column directory of top-level subject categories, not nested topic cards.
- Level 4 pages use the shared Level 4 banner. Put the **category** (for example, *Number Skills & Operations*) in the banner; the current topic title belongs in the content column. Desktop layout: narrow left navigation listing sibling topics **without** a “TOPICS” heading; main reading column on the right. Long navigation titles wrap naturally. Mobile navigation moves above the content.
- Heading 2 normally defines a Level 4 topic/page; Heading 3 normally defines a collapsible teaching card; Heading 4 is an internal subheading. **Pedagogical structure overrides mechanical heading mapping**: a section such as “Advanced Skills” may be introductory text outside cards, while its Subtraction Method and Division Method become separate cards.

### Accordion / teaching cards

- Use semantic `<details>` / `<summary>` or an accessible equivalent with keyboard support and an accurate expanded state.
- The **first teaching card is expanded by default**, all subsequent cards collapsed. Users may close the first and open others.
- Card headings use the established pale-blue header, navy text and right-aligned plus/minus affordance. Avoid a large “card inside card” hierarchy unless required by the actual learning structure.
- In GCF, keep the Advanced Skills overview outside the cards, then create independent **Subtraction Method** and **Division Method (Euclidean Algorithm)** cards.

### Math rendering: classify before converting

1. **Display formulas** (rules, identities, derivations): one line/paragraph, centered within the reading column; examples include `\gcd(a,b)=\gcd(a-b,b)` and `\gcd(a,b)=\gcd(b,r)`. Use semantic MathML or a consistently configured MathJax/KaTeX renderer. Do not convert LaTeX commands to raw visible text.
2. **Inline math** (variables or expressions within a sentence): remain inline and do not center the surrounding prose.
3. **Worked calculation steps** inside an example: normal **left-aligned** text in a numbered list, not display-math blocks. Keep the number close to the calculation.
4. **Short multiple examples** may be bullet items; one example question must **not** receive a decorative bullet merely because it came from Word list formatting.
5. Operators and notation: preserve `÷`, `×`, `−`, `=`, `→`, fractions, superscripts, roots and parentheses. Write `gcd`/`GCF` as an upright operator name (not three italic variables). Check rendered math visually and against the Word source; never trust successful HTML conversion alone.
6. No vertical scrollbars, up/down spinner arrows, clipped formulas, or formula containers with accidental `overflow-y: auto`. On narrow screens allow **horizontal overflow only if truly needed**, without distorting the math.

### Examples, lists and indentation

- Use semantic `<ul>` for genuine bullet lists and `<ol>` for sequential methods. Preserve bullets for several distinct examples, but do not insert bullets before a single question.
- A list is indented **one level (approximately three character spaces)** relative to its introducing text. Avoid literal repeated spaces or tab characters; implement indentation with CSS `margin-inline-start` and `padding-inline-start`.
- **Vertical spacing between list items:** use a **half-line** gap between siblings (`margin-top: 0.5lh` on `li + li`) in `.mf-article`, `.kiwi-topic-article`, and tip/insight panels. Do not tighten plain instructional bullet lists to a single line height. Numbered **`ol.kiwi-example-steps`** and parallel **`ul.kiwi-example-variants`** inside **`.kiwi-example-standard`** keep their own step spacing.
- Example hierarchy: `Example:` (base indent) → `Find GCF(84, 30).` (one indent) → `1. 84 ÷ 30 = 2 remainder 24` etc. (a **second** indent). Place the example question **before** its steps.
- Keep the entire example together: the explanatory sentence **“When the remainder is 0, the last divisor is the GCF.”** follows step 3 **at the same text indent as the numbered calculation**, within the example block. The final result `∴ GCF(84, 30) = 6` belongs to the same example, not an unrelated top-level paragraph.
- Do not render steps as centered formulas; do not use a layout that puts numbers at the far left and calculations at the far right.
- For GCF division example the correct step text is exactly:
  1. `84 ÷ 30 = 2 remainder 24`
  2. `30 ÷ 24 = 1 remainder 6`
  3. `24 ÷ 6 = 4 remainder 0`
- Do **not** allow escaped TeX to leak into text (e.g. `\div` appearing literally or `84 \div 30 = 2\ remainder 24` concatenated with raw MathML). If the source expression is mixed prose and math, render the arithmetic and “remainder” separately or as verified plain Unicode text.

### Learning Insight / Info Panel

- Convert Word hint/history/insight boxes to a native semantic `<aside role="note">`, **not** an HTML table or blockquote.
- Match the site's existing **warm pale-cream/yellow** callout: light cream background, subtle warm-yellow border, rounded corners, a small lightbulb beside the title.
- Title and prose are **left-aligned**; standalone math inside the panel remains centered. Preserve the original content, including history notes and actual bullet lists.
- Do not substitute a blue panel or center all the text; do not leave empty icon columns or Word table borders.

### Required QA and acceptance checks

- Inspect the actual source DOCX structure, including equations (OMML), drawings, tables, heading levels and text in images. Convert in logical reading order; do not silently drop content.
- Validate generated HTML, CSS, anchor destinations, accessible accordion behavior, first-card-open default and mobile layout.
- Render the actual page in a browser and visually inspect **all formula blocks**, especially division signs, upright `gcd`, line alignment, clipping and scroll arrows.
- Check every example's nesting and sequence: question → numbered steps → explanation → answer; verify bullets appear only where intended.
- Check the site's English/Chinese language behavior without fabricating translations or breaking existing language flags.
- Do not claim a ZIP integrity test alone proves the website or math is correct. Compare representative rendered pages to the Word original before final delivery.

### Minimal HTML pattern for a nested example

```html
<p>Example:</p>
<div class="kiwi-example-block">
  <p class="kiwi-example-question">Find GCF(84, 30).</p>
  <ol class="kiwi-example-steps">
    <li>84 ÷ 30 = 2 remainder 24</li>
    <li>30 ÷ 24 = 1 remainder 6</li>
    <li>24 ÷ 6 = 4 remainder 0</li>
  </ol>
  <p class="kiwi-example-explanation">When the remainder is 0, the last divisor is the GCF.</p>
  <p class="kiwi-example-answer">∴ GCF(84, 30) = 6.</p>
</div>
```

Indent the question once and the numbered steps/explanation twice with CSS; do not use literal spaces. The explanation aligns with the **step text**, not with the leftmost number marker.


### Example numbered-list indentation (refined)

- Within a single-example block, place the numbered steps **one tab (approximately three character spaces)** to the right of the example question, not two tabs.
- Keep the step number adjacent to the left-aligned step text. Avoid legacy broad `padding-left: 4.7rem` rules overriding example-specific indentation.
- Keep the explanation and final answer in the same example block, visually aligned with the step text.
- Use scoped CSS for `.kiwi-example-block ol.kiwi-example-steps` and verify both desktop and mobile rendering.


### Numbered List Marker Color

For mathematical worked examples, numbered list markers (1., 2., 3., etc.) must use near-black (`#111111`), not the site accent blue. Preserve the approved single-tab indentation and left-aligned calculation text. Use `li::marker { color: #111111; }` on both `.kiwi-numbered-steps` and `.kiwi-example-steps`.


## Word-to-Web Conversion: Approved Math Lesson Formatting (2026-11-09)

These rules apply to the KIWI Mathematical Thinking Level 4 teaching pages and future Word-to-Web conversions. Preserve the original source's mathematical meaning, examples and teaching order; do not blindly turn every Word paragraph into a display equation.

### Page hierarchy and navigation

- Level 3 Mathematical Thinking: a clean single-column list of primary categories, without nested cards.
- Level 4: each actual topic is a separate page with the category (e.g., Number Skills & Operations) in its banner. The topic title is in the article body. A compact left-side topic navigation has no `TOPICS` heading, supports long wrapping labels, and moves above content on small screens.
- Heading 3 is generally a collapsible teaching card; Heading 4 is an internal subsection. Editorial teaching logic overrides automatic mapping: for example, put the Advanced Skills introduction outside the cards, and give Subtraction Method and Division Method separate cards.
- First accordion card starts open; all other cards start closed. Cards remain independently collapsible.
- Do not display Advanced book page numbers or claim the site is a companion book. Exclude worksheets and answer keys when requested.

### Numbered and bulleted lists

- **Number markers must be normal-weight BLACK (`font-weight: 400; color: #111`)**, not blue and not bold. Do not inherit accent colors or bold styling from general list/card rules.
- Text of numbered steps is normal-weight unless a specific mathematical term needs emphasis.
- Real multi-item examples and conceptual bullet lists use bullet markers. A *single* example question (e.g., `Find GCF(48, 18).`) has no bullet.
- Example question: indent one tab (~3 character widths) relative to the `Example:` label. Numbered steps: indent one further tab (~3 character widths) relative to the question, not two. Keep the numeral near its step text; both are left-aligned. Use real `<ol><li>` markup, not centered display equations.
- The explanation and final answer belonging to an example remain within the example block, aligned to its step text, not reset to the page's outer margin.
- A computation sequence may be an ordered list; standalone mathematical identities/rules are display equations instead. Do not introduce unwanted bullet markers on formulas.

Example markup:

```html
<p>Example:</p>
<div class="kiwi-example-block">
  <p class="kiwi-example-question">Find GCF(84, 30).</p>
  <ol class="kiwi-example-steps">
    <li>84 ÷ 30 = 2 remainder 24</li>
    <li>30 ÷ 24 = 1 remainder 6</li>
    <li>24 ÷ 6 = 4 remainder 0</li>
  </ol>
  <p class="kiwi-example-explanation">When the remainder is 0, the last divisor is the GCF.</p>
  <p class="kiwi-example-answer">∴ GCF(84, 30) = 6.</p>
</div>
```

```css
.kiwi-topic-article ol li::marker {
  color: #111 !important;
  font-weight: 400 !important;
  font-style: normal !important;
}
```

### Mathematics formulas

- Independent formulas and identities are separate, horizontally centered display blocks. Inline variables and short expressions remain inline. Keep numbered calculation steps left-aligned as text, with inline math only where necessary.
- Use semantically correct MathML or a consistently configured math renderer; do not flatten Word equation objects into broken plain text. Preserve `÷`, fractions, superscripts, roots, parentheses, equality and `\operatorname{GCF}` / `\gcd` notation.
- Display `gcd` as a proper upright mathematical operator: `gcd(a,b) = gcd(a-b,b)` and `gcd(a,b) = gcd(b,r)`. Do not split `gcd` into italic individual letters.
- Never show vertical scroll arrows/scrollbars on math containers. For unusually wide formulas on narrow screens, allow only an intentional horizontal overflow treatment.
- Verify all formulas visually in a real browser, especially division and dimensional analysis; a valid ZIP or syntactically valid HTML is not enough.

### Info panels

- Use the site's established warm cream/yellow panel with a soft gold border and a small lightbulb icon beside the heading. Keep prose left-aligned, formulas centered only when they are standalone. Avoid importing Word table cells and centered table text as the website's info panel layout.

### QA checklist

- Compare page text and teaching sequence against the source Word document.
- Check every Heading 3 accordion, including the first-open default, and all Level 4 links.
- Check ordinary black, nonbold ordered-list markers; single-example indentation; ordered steps and their explanations.
- Check display-vs-inline math, correct symbols, formula alignment, and no vertical math scroll arrows.
- Check cream info panels, desktop/mobile layout, language toggle, and preservation of existing site pages.


### Canonical example layout (approved)

- **Label wording:** Use **`Example:`** (singular) when the block presents **one** worked problem with steps and an answer. Use **`Examples:`** (plural) when listing **multiple separate short items** (typically a bulleted list of facts or mini-results) with no shared step-by-step solution. Match Chinese: **示例：** vs **例如：**.
- **Worked steps:** Use **`<ol class="kiwi-example-steps">`** (decimal **1., 2., 3.**) only for **sequential solution steps** (calculations or working in order). Use **two or more** `<li>` items when numbering; a single calculation line uses **`kiwi-example-list-step`** or **`.kiwi-math-block`** instead (see below). Do **not** number **parallel alternatives**—equivalent names, wording variants after **also said as:**, or other non-step lists.
- **Wording variants inside `Example:`:** When one worked example lists **equivalent phrasings** (not steps), use **`<ul class="kiwi-example-variants">`** inside **`.kiwi-example-standard`**, indented at **6ch** like numbered steps. Reference: square/cube root “also said as” lists in `math/foundation-roots.html`.
- **Separate `Examples:` bullets:** Use **`ul.kiwi-example-list`** only under the plural **`Examples:`** label for multiple independent short items outside a single step-by-step block.
- **Single step (no `1.`):** When a worked **`Example:`** has only **one** calculation or working line after the question, do **not** use a numbered list. Use an unnumbered step line: **`<p class="kiwi-example-list-part kiwi-example-list-step">`** at **6ch** with **inline** math (reference: `459 ÷ 9` in `math/foundation-division-rules-2-9.html`), **or** **`<div class="kiwi-math-block">`** with **`display="block"`** math when the working line is a **standalone display formula** (centered on its own line). **Display-formula rules override example step alignment** for that line only (reference: apple-rate example in `math/foundation-unit-conversions-and-rates.html`).
- **Multi-line bullets under `Examples:`:** When one bullet item needs **several stacked lines** (setup → working → conclusion), split each visual line with **`<span class="kiwi-example-list-part">`**: first line = setup (no extra class), middle line(s) = **`.kiwi-example-list-step`** (+3ch inside the bullet), final line = **`.kiwi-example-list-answer`** (pale left rule; aligns with the first line of that bullet, not the bullet marker). Reference: divisible-by-7 list in `math/foundation-division-rules-2-9.html`.
- **Conclusion inside `Example:` (Since / So / Therefore):** After working lines, the conclusion may use **`<p class="kiwi-example-list-part kiwi-example-list-answer">`** at **3ch** (aligned with **`kiwi-single-example`**) **or** **`blockquote.kiwi-example-answer`** when the page already uses that pattern for **`∴`**. Do not indent the conclusion with the step column at 6ch. Prefer **`kiwi-example-list-answer`** when the conclusion is a full sentence starting with *Since*, *So*, or *Therefore* and must line up with the problem line.
- Do **not** wrap the problem statement or working steps in generic `<blockquote>` panels (no dark-blue left rule or pale-blue fill on the question). Only the final **`∴` answer** uses the subtle pale-blue left border via `.kiwi-example-answer`.
- The `Example:` label remains at the normal paragraph left margin.
- A single problem statement is **not** a bullet. Indent it by **3ch** (approximately three spaces / one tab) relative to the label.
- Ordered solution steps are indented by one more **3ch** relative to the problem. The list marker is black, normal-weight, not bold. Keep markers adjacent to their step text and left-align the whole list; do not center each step as a display formula.
- Any concluding explanation belongs to the same example, immediately after the numbered steps, aligned with the step text (not the list number). Use **`<p class="kiwi-example-explanation">`** at **6ch** for reasoning lines (including **`∵`** and **`∴`** when they **explain** why the math works, not when they state the final result). **No pale vertical rule** on explanations.
- The **final answer** (numeric result or explicit “the answer is …”) uses **`∴`** with **`.kiwi-example-list-answer`**, **`.kiwi-example-answer`**, or **`blockquote.kiwi-example-answer`** and the subtle pale-blue left border at **3ch**. Do not use the answer classes for post-formula unit-cancellation prose (reference: apple-rate **`∴`** line in `math/foundation-unit-conversions-and-rates.html`). Do not turn the answer into an extra numbered step.
- **Answer typography:** The `∴` conclusion line (`.kiwi-example-answer`) is **normal body weight** throughout—do not bold the numeric result or wrap it in `<strong>`. The pale left rule alone marks the answer; emphasis belongs in the problem or explanation, not the solution.
- Preserve the teaching order: Example → problem → steps → explanation (when needed) → answer.
- For subtraction and division methods, use the same markup and CSS rather than per-example indentation hacks.

```html
<p>Example:</p>
<div class="kiwi-example-block kiwi-example-standard">
  <p class="kiwi-example-question">Find GCF(84, 30).</p>
  <ol class="kiwi-example-steps">
    <li>84 ÷ 30 = 2 remainder 24</li>
    <li>30 ÷ 24 = 1 remainder 6</li>
    <li>24 ÷ 6 = 4 remainder 0</li>
  </ol>
  <p class="kiwi-example-explanation">When the remainder is 0, the last divisor is the GCF.</p>
  <p class="kiwi-example-answer">∴ GCF(84, 30) = 6.</p>
</div>
```

Global layout CSS lives in **`assets/css/styles.css`** (`.kiwi-example-standard`, `ol.kiwi-example-steps`, `ul.kiwi-example-variants`, `ul.kiwi-example-list`, `.kiwi-example-list-step`, `.kiwi-example-list-answer`). Page-specific overrides in `math/gcf.html` remain the accordion reference for **kiwi-topic-article**; foundation pages use **`.mf-article`** with the same global rules.

**QA tool:** run `python tools/audit_example_layout.py` on `math/*.html` to flag single-item `<ol class="kiwi-example-steps">` lists and multi-line `kiwi-example-list` bullets missing step/answer classes.

On mobile, keep indentation relative and avoid horizontal overflow.


### Example ordered-list alignment correction

- `Example:` is at the normal text margin.
- Problem line starts at `3ch` from the example margin.
- The **visible numbered marker** (1., 2., 3.) must start about another `3ch` to the right of the problem line, never to its left. Account for the browser's list-marker gutter: do not equate `ol` margin with the marker's visible position.
- In the current `math/gcf.html` reference CSS, use `ol.kiwi-example-steps { margin-left: 9ch; padding-left: 2.1ch; }` with marker outside, and align the subsequent explanation with the step text. Test visually in a browser and adjust the marker gutter if fonts change.
- Apply the same alignment to Subtraction Method and Division Method; markers remain normal-weight black.


### Example step indentation: CSS conflict prevention

The `Example:` label is at the base text margin. The problem begins at `3ch`. The **visible number marker** (1., 2., 3.) begins at `6ch` from the base, not `9ch`; the marker and text remain adjacent. Use `list-style-position: inside` and `margin-left: 6ch; padding-left: 0` for the numbered list, and use normal-weight black numerals. Do not combine a `9ch` margin with extra `padding-left` or legacy `4.7rem` overrides. Verify actual browser rendering, not just ZIP validity.


### Example indentation: final alignment rule

- Example label starts at 0ch. The single problem statement begins at 3ch.
- The **visible number** (not just its content) of each numbered step begins at 6ch, three characters farther right than the problem statement.
- Number markers are normal-weight black; working text follows the number immediately. Use `list-style-position: inside` with zero list padding to avoid browser default marker offsets.
- The blue vertical rule for the conclusion aligns with the problem statement at 3ch; conclusion text is padded inside the rule.
- Never stack conflicting `ol` padding and margin overrides. Verify the final rendered marker position on desktop and mobile.


## Shared Mathematics Formula and Example Quality Rules (2026-11-09)

Applies to `math/gcf.html`, `math/unit-conversions-and-rates.html`, and `math/mental-squaring-and-square-rooting.html`.

- **Display equations:** one row, horizontally centered; MathML remains structurally intact; do not put a display equation in a scrolling vertical container. Only permit horizontal overflow on narrow screens. Inline math stays inline. Verify rendering in a real browser.
- **Examples:** `Example:` remains at the body margin; a single problem begins 3ch to the right. An ordered working list begins at 6ch relative to `Example:` (one additional 3ch indent). The *visible number*, not just the text, must align at 6ch. Numbers are black and normal weight. Do not center numbered steps.
- **Example conclusion:** after all working and explanation, use a `∴` answer line with a subtle pale-blue left border aligned with the problem at 3ch. Explanatory prose associated with a worked example stays within that example.
- **True multiple examples:** preserve an ordinary bullet list; do not confuse a list of independent examples with a numbered solution.
- **Content fidelity:** never silently repair ambiguous Word mathematics; compare the source Word equation and verify the correct `÷`, `−`, exponents, radicals, units, parentheses and GCF/gcd notation. MathML may be mathematically incorrect even when visually centered.
- **QA:** check all three Level 4 pages, including expanded accordion cards, at desktop and mobile widths. Check computed CSS, not only ZIP validity.


### Display Formula Alignment — Sitewide Enforcement

- Only standalone mathematical equations are centered. Inline math remains inline, and numbered calculation steps stay left aligned.
- Wrap a standalone MathML equation in **`.kiwi-math-block`** with **`display="block"`** on the `<math>` element. Global CSS uses **`display: flex; justify-content: center`** on the wrapper so the formula sits on its **own line** and is **horizontally centered** in the content column, including inside **`.kiwi-example-standard`** (this overrides example step left-align for that line only).
- **Sitewide renderer:** All teaching HTML with `<math>` loads **KaTeX** + **`assets/js/kiwi-math-katex.js`** (see `tools/inject_math_katex.py`). On load and after language toggle, **`kiwiRenderAllMath()`** renders (1) **`.kiwi-math-latex`** from `data-tex-en` / `data-tex-zh`, and (2) every **`<math>`** that has a **`application/x-tex`** annotation (replaces fragile MathML). **`normalizeTex()`** uses **`\dfrac`**, **`\text{…}`** for common unit abbreviations, and maps **`\boxed{\text{unit}}` → `\cancel{\text{unit}}`**.
- **Unit cancellation:** Author explicit cancel lines as **`\cancel{\text{lb}}`** in `data-tex-*` or in the tex annotation. Do **not** rely on **`<menclose notation="updiagonalstrike">`** or Word boxed units.
- **Upright units:** In LaTeX use **`\text{lb}`**, **`\text{km/h}`**, etc.—never bare italic `lb` in math mode.
- Use horizontal overflow only when an equation cannot fit a narrow viewport; do not allow vertical scrollbars or spinner-like scroll indicators.
- Keep actual examples and numbered lists left aligned, with normal-weight black numbering and established indentation.
- Never turn a multi-sentence paragraph or a curriculum panel into a centered math block.
- Validate the mathematics against the source Word file separately from CSS/layout checks.

### Formula followed by “where …” (variable gloss)

Do **not** put **`display="block"`** math and a **where** clause in the same `<p>` (Word export spreads them across the line: formula left, gloss far right).

- Wrap the rule in **`.kiwi-math-block`** with centered display math.
- Put the gloss in the **next** left-aligned `<p>` inside **`.kiwi-math-where`**: *where* `<math display="inline">n</math>` *is the term number.* (Chinese: *其中* … with the same inline math for the symbol).
- After a **`ul.kiwi-example-list`** (e.g. “Rule (expression):”), indent the whole **`.kiwi-math-where`** block **3ch** (`ul.kiwi-example-list + .kiwi-math-where` in global CSS).
- Use **spaced ` — `** in English and **spaced ` —— `** in Chinese only when the gloss is rhetorical prose in `data-en` / `data-zh`; keep *where* / *其中* as normal sentence openers.
- Short rules that read as one sentence may stay **fully inline** (inline math only, no `.kiwi-math-block`).


## Level 4 Accordion: Expand All / Collapse All (2026-11-09)

- When a Level 4 teaching article has at least two `.lesson-card` accordion sections, display compact **Expand All** and **Collapse All** buttons immediately above the first card, right aligned in the content column (not in the banner or topic sidebar).
- On initial page load, open the first lesson card and close the remaining cards. Each card remains independently toggleable via its native `<summary>`.
- Expand All opens all lesson cards in the current article; Collapse All closes all lesson cards. Do not affect unrelated site navigation, nested disclosure widgets outside the lesson-card collection, or other pages.
- For a single lesson card, omit both controls. Use real `<button type="button">` controls, responsive wrapping, accessible group labels, and English/Chinese text via the site's language setting.
- Implement in the shared Level 4 template for future pages, and apply to existing Level 4 pages. Keep the existing math formula, Example, list, and Info Panel standards unchanged.


### Readability-first sizing for educational diagrams

- Do not apply repeated percentage reductions to already resized image widths. Base any new size on the original image and its legibility.
- For composite images containing two side-by-side charts, use a readable desktop display width (typically 700–800px, constrained by `max-width:100%`), not the single-figure 50% rule.
- Preserve aspect ratio and center diagrams. Inspect labels, axis ticks and annotations at the actual rendered size.
- For narrow mobile viewports, use responsive sizing and consider a dedicated stacked layout when annotations become unreadable.


## Teaching Image Readability and Sizing (Level 4)

**Do not repeatedly scale an already scaled image.** Always determine display size from the original asset dimensions and content, never from the previous CSS width. Imported mathematical diagrams must remain readable at normal browser zoom.

- Small symbols or simple icons: retain their natural size; do not enlarge unnecessarily.
- Single coordinate graphs, geometric diagrams, and formula diagrams: typically 500–680 CSS px depending on density and aspect ratio.
- Wide, side-by-side comparisons with axes, legends, or text: typically 680–760 CSS px (or the available content width).
- Portrait diagrams: generally up to 500 CSS px, keeping their aspect ratio.
- Preserve original source image resolution and aspect ratio; never crop, stretch, blur-pad, or resize the raster asset merely to adjust on-page presentation.
- Use `max-width: 100%; height: auto; display: block; margin: 1rem auto` for responsive centered display.
- Do not change logos, flags, banners, or decorative site images when adjusting Word-imported teaching illustrations.
- Visually inspect labels, tick marks, equations, and comparison graphs at 100% browser zoom on desktop and mobile. If they are illegible, increase display width or offer a full-size view rather than blindly applying a 50% reduction.


## Word-to-Web Info Panel Conversion — Final Standard (2026-11-09)

- Convert **Word two-column tables containing a lightbulb icon** into semantic `<aside class="kiwi-word-info-panel" role="note">`, not HTML tables. Preserve all original prose, mathematics, and real lists.
- Convert **Ontario Curriculum Connection** one-cell Word tables into `<aside class="kiwi-curriculum-panel" role="note">`, with no lightbulb. Preserve curriculum title, grade, citations, source links, and paragraphs in original order.
- Convert standalone **historical/learning notes** (e.g. A Short History) into the same warm-cream insight panel; include a small lightbulb for insight/history, but not for curriculum panels.
- Style panels consistently in `assets/css/styles.css`: pale cream `#fff8e9`, subtle gold frame `#f0d58d`, **3px right accent** `#e4b54e` (canonical reference: original `math/gcf.html` tip panels), 12px radius, left-aligned prose and heading. Do not redefine panel background or outer border in page `<style>` blocks — sitewide chrome only. Standalone display mathematics inside panels remains centered; inline math stays inline.
- **Tip panel row 1 (global CSS in `assets/css/styles.css`):** The lightbulb sits in column 1, row 1. Column 2, row 1 is either the panel **title** (when a title span is present) or the **first line of body content** when the header is icon-only. All following body blocks stay in column 2 only, left-aligned with that first text column (not with the bulb). Markup: `kiwi-panel-heading` / `kiwi-word-info-header` / `kiwi-insight-header` plus optional `kiwi-word-info-body`, `kiwi-insight-body`, or `kiwi-panel-content` for mixed loose text/math. **Do not** duplicate heading `display:flex` layout in page `<style>` blocks — run `python tools/apply_tip_panel_rules.py` after bulk panel edits.
- Never center all the text in an imported table or keep empty Word icon columns. Do not convert actual data tables (multi-row numerical tables, comparisons, formula tables) into panels.
- QA: review panel types and links across every imported Level 4 page, including mobile, while preserving the existing example, math and image readability standards.


## Math Foundations Level 3 → Level 4 Navigation

- The six Math Foundations category cards are Level 3 index cards, matching Mathematical Thinking. Clicking one must open an actual Level 4 lesson directly, not a book-wide intermediate page.
- Each Level 4 lesson has a left sidebar listing the sibling lessons of its category. Number Families is the FIRST item of Number Skills & Operations; do not edit its existing lesson content.
- The imported Word Heading 2 topics become individual Level 4 lesson pages. Word Worksheet and Answer Key are not published, per prior web conversion rules.
- Use breadcrumb navigation instead of legacy Back to buttons; preserve existing banner, website header and footer.


## Math Foundations Level 4 Banner (2026-11-09)
- All Math Foundations topic pages use the **Level 4 Topic Banner**, following the existing Number Families leaf-page style (light background), not the blue Level 3 compact banner.
- Banner heading names the **parent category**, e.g. Number Skills & Operations; the lesson heading in the main content names the specific topic (Number Families, Decimal, etc.).
- Preserve the six-card Level 3 Math Foundations index and the category-specific Level 4 left sidebar. Avoid duplicate breadcrumbs.


## Math Foundations Level 4 Banner Consistency (2026-11-09)
All imported `math/foundation-*.html` lesson banners must use `class="nf-hero topic-banner foundation-topic-banner"`, matching the existing Number Families reference page. Never use `topic-banner` alone on these pages: its generic 50px title rule causes oversized, vertically clipped text. Keep the Level 4 category heading and separate lesson title in the article. Do not change the Number Families original content.


### Math Foundations Level 4 Breadcrumbs
- Use only the shared `assets/js/drive-breadcrumb.js` breadcrumb, consistent with the existing Number Families page.
- Do not insert a second hard-coded breadcrumb (`nf-lesson-crumb` or `foundation-crumb`) into lesson HTML.
- Register every new Level 4 lesson in the shared breadcrumb page registry, parented to `math/math-foundations.html`.
- Keep the Google Drive-style clickable ancestors and dropdowns; no Back to Math Education button.


## Level 4 Breadcrumb category labels (2026-11-09)

For all Level 4 pages under Math Foundations and Mathematical Thinking, the final Breadcrumb item displays the **category shown in the Level 4 topic banner**, not the individual lesson title. Example: `Home › Math Education › Mathematical Thinking › Number Skills & Operations`. The individual lesson name (e.g. Greatest Common Factor (GCF), Decimal, Number Families) appears as the article title and active left-navigation item. Preserve the existing parent path, dropdown behavior, bilingual labels, banner, and lesson content. Maintain the per-page registration in `assets/js/drive-breadcrumb.js` accordingly.


### Level 4 page body width consistency (2026-11-09)
- All Level 4 topic pages must align their breadcrumb, banner, sidebar and main lesson with the Math Foundations Decimal page frame.
- Desktop outer main: `width:100%; max-width:1240px; margin-inline:auto; padding-inline:34px; box-sizing:border-box` (usable content width 1172px at wide viewports).
- Mobile <=700px: `width:100%; padding-inline:18px; box-sizing:border-box`.
- Both `.topic-main` (Number Families and Mathematical Thinking) and `.edu-main` (imported Math Foundations) must use the same effective frame; do not combine `calc(100% - 64px)` with additional horizontal padding.
- Keep existing Level 4 banner, sidebar, breadcrumb and lesson content intact.


### Level 4 full-width alignment (corrected)
Match the `edu-main` Decimal reference exactly. For `.topic-page .topic-main`, use the same responsive outer width as `.edu-page .edu-main` and **zero horizontal padding**. Do not add 34px gutters inside `topic-main`: this makes Number Families and Mathematical Thinking pages narrower. Desktop width: `min(1240px, calc(100% - 64px))`, between 701px and 1303px: `calc(100% - 48px)`; mobile: `calc(100% - 36px)`.


## Math Foundations panel audit (2026-11-09)
- One-row two-cell Word learning-note tables are semantic warm-cream `aside.kiwi-word-info-panel` with lightbulb; genuine multi-row data tables remain tables.
- Ontario Curriculum Connection is a warm-cream `aside.kiwi-curriculum-panel` without lightbulb; original curriculum descriptions and links remain.
- Both panels use left-aligned prose and centered standalone equations.


### Level 4 body and banner alignment
The lesson layout (sidebar plus article) must align exactly with the left and right edges of the Level 4 banner. Never cap `.kiwi-learning-layout` at 1160px inside a 1240px `.topic-main`; override it to `width:100%; max-width:none; margin-inline:0`. Apply the same rule to `.nf-lesson-layout`. The outer `topic-main` controls the shared width and mobile gutters.


## Level 4 left navigation — canonical GCF sidebar

All Math Foundations and Mathematical Thinking Level 4 pages must use the **GCF (`math/gcf.html`) sidebar visual style**: pale blue-white `#f7faff` background, `1px #dce7f3` border, 14px rounded corners, 18px/12px padding, 14px navy link text, 12px/13px link padding, 6px vertical spacing, and 9px link radius. The current lesson has a pale blue `#deecff` fill, bold dark blue text and a 3px blue left accent. Hover uses `#e8f2ff`. Keep sidebar topics scoped to their category; preserve lesson links and order. Apply the same CSS to `.kiwi-topic-sidebar`, `.mf-sidebar .mf-side-links`, and `.nf-lesson-sidebar nav`, rather than inventing a different sidebar for imported pages. Sidebar and main content remain in the same Level 4 grid. On narrow screens sidebar becomes non-sticky and full-width.


### Level 4 Sidebar Alignment (Math Foundations and Mathematical Thinking)
Use the GCF / Number Families sidebar as the visual reference. All topic links start at the same left edge. The legacy `.mf-side-links { padding: 5px 0 9px 26px; }` must NOT shift Foundation links to the right. Use `padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px` for the link container, and consistent 12px/13px link padding. The active link uses a light-blue background and a 3px blue left border, compensated in its left padding.


## Level 4 sidebar return link

Every Math Foundations Level 4 sidebar must end with a separate, visually divided return link: `← All Math Foundations` (Chinese: `← 返回数学基础目录`) linking to `math-foundations.html`. Match the GCF Mathematical Thinking sidebar return-link spacing, border, font size, and styling. Keep this return link after the topic links and outside the active-topic state.


### Math Foundations classification: Trigonometry
- Trigonometry is an independent Level 3 category, separate from Geometry & Space.
- Geometry & Space Level 4 sidebars must not contain Trigonometry.
- Trigonometry Level 4 sidebars contain its own lessons (Understanding Trigonometry, Three Sides, Four Ratios, Special Right Triangles).
- The Level 3 category card links directly to the first Trigonometry Level 4 lesson.


### Level 4 topic banner overflow fix (desktop and mobile)

- Use min-height: 150px and height: auto; never fixed height or maximum height.
- Do not clip title or subtitle with overflow:hidden, max-height, or line-clamp.
- On narrow screens, allow the title to wrap rather than cropping it.
- Keep subtitle copy concise (prefer two lines), but never truncate text via CSS.
- Apply the shared .nf-hero.topic-banner rule to both Math Foundations and Mathematical Thinking.


### Level 4 Banner — Mobile Text Containment (2026-11-09)
- Applies to Math Foundations and Mathematical Thinking Level 4 topic pages.
- Keep the kicker, category heading, and category-level subtitle **inside** the gradient banner and its rounded border at every viewport size.
- Use content-driven height (`height:auto; min-height:150px`) with adequate padding, never clipping text or placing it outside the banner.
- On mobile, allow kicker and heading to wrap naturally, and do not line-clamp the subtitle.
- The kicker identifies the Level 3 parent (e.g., `MATH FOUNDATIONS`), not a lesson-specific name.
- The subtitle describes the Level 4 **category**, not the first lesson (e.g., Number Families).


### Level 3 category cards — mobile CTA alignment (2026-11-09)
For both Math Foundations and Mathematical Thinking category indexes, preserve the desktop horizontal card layout. On screens at or below 760px, use a two-column first row (number badge at left, heading and description at right) and a second full-width row with the “Explore topics →” CTA right-aligned. The CTA must remain on one line; never allow it to collapse into a narrow first column or wrap into stacked words. Apply identically in English and Chinese.


### Level 3 Mobile Category CTA Typography
On mobile, place the Explore topics CTA at the bottom right of each category card, but retain the same inherited font, weight, and text color as the desktop version. Do not add mobile-only blue coloring or bold emphasis. Applies to Math Foundations and Mathematical Thinking.
