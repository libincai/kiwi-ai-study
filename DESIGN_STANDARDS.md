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

## 7. Back-to-home row and page alignment

- The “Back to Home” link appears above the inner-page banner.
- Its left edge must align exactly with the banner's left edge.
- The back-link wrapper, banner, and main content should use the same page alignment guides where the layout calls for a shared content width.
- Keep the vertical gap between the navigation divider and the back link consistent across all inner pages.
- Keep the gap between the back link and banner consistent.
- Do not use page-specific margins to compensate for a wrong parent container width.

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
