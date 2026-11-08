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
| `--inner-banner-height-mobile` | `150px` | Mobile inner-page banner height |
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
