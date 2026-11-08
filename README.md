# Kiwi 爱AI Study — Website Structure

- `index.html`: Home page
- `math/`: Math Education pages and learning examples
- `ai/`: AI Education hub and episode pages
- `books/`: Books overview and individual book pages
- `about/`: About page
- `legal/`: Privacy and Terms pages
- `assets/`: Shared CSS, images, logos, banners, and fonts
- `tiktokMrPWsgOh6TmiyXI0MfJttPkSMBpIrQ0v.txt`: Domain/platform verification file; intentionally kept at the site root.

The folder structure follows the main website navigation. Shared visual assets remain centralized in `assets/`.

- `DESIGN_STANDARDS.md`: Project-wide design and implementation rules. Read it before changing pages or adding assets.
- `templates/level-2-primary-nav.html`: Copy source for primary navigation landing pages (header, breadcrumb script, banner, body placeholder, footer). See DESIGN_STANDARDS.md §7.
- `templates/level-3-category.html`: Copy source for category hubs under Math/AI (same compact banner as Level 2; short subtitle + `.edu-lead` in body). Reference: `math/math-foundations.html`.
- `templates/level-4-topic.html`: Copy source for Level 4 topic/detail pages (gradient `nf-hero topic-banner`, breadcrumbs, body placeholder). Reference: `math/number-families.html`.
- **Image rule:** Before adding or replacing any website image, resize and compress it for its actual display size. Prefer WebP, aim for a clear image rather than maximum resolution, review images over 250 KB, and avoid adding images over 400 KB without a specific reason. See `DESIGN_STANDARDS.md` for dimensions, quality guidance, and exceptions.

- **Inner-page banners:** all inner pages must use the same-height, text-only shared banner. No images, icons, emoji, SVGs, or illustrations inside banners. See `DESIGN_STANDARDS.md`.

- **Card icons:** icons and emoji in content cards must sit on the left, with heading and description text flowing beside them; never place them alone on a separate top row. Page banners remain text-only.

- **Content-card icons:** use a dedicated left icon column and a separate right text column; descriptions must not wrap below the icon. Banner remains text-only.

- **Navigation highlight:** only direct main-navigation destination pages show an active nav highlight. Deeper lesson, episode, and detail pages do not; About remains highlighted as an explicit exception.

- **Learning article layout:** use fewer section headings, fuller explanatory paragraphs, restrained emphasis, and only one next-lesson link (do not duplicate the bottom navigation with another promo card).

- **Last-level page banner:** reuse the exact shared `.topic-banner` component based on the Number Families banner. Text-only; no images/icons; no page-specific sizing. See `DESIGN_STANDARDS.md`.

- **Banner design standard:** the canonical deepest-level page banner rules are documented in `DESIGN_STANDARDS.md`. Keep the standard in Markdown; do not create a separate Word specification.

- **Banner text length:** category kicker and title stay on one line; subtitle is limited to a maximum of two lines. See `DESIGN_STANDARDS.md`.

- **Canonical last-page banner:** follow the final v2 specification in `DESIGN_STANDARDS.md` and the shared CSS block `FINAL CANONICAL LEAF-PAGE BANNER STANDARD — v2` in `assets/css/styles.css`. Do not add page-specific banner styles.

- **Canonical last-page banner:** follow v3 in `DESIGN_STANDARDS.md` and the shared CSS block `FINAL CANONICAL LEAF-PAGE BANNER STANDARD — v3` in `assets/css/styles.css`. Do not add page-specific banner styles.


## AI episode pages (magazine layout)

AI Knowledge Class episodes use a **text-first magazine article** with floated spot illustrations. **Agent guide:** `docs/AI_EPISODE_MAGAZINE.md`. **Reference:** `ai/episode-01.html`; images in `ai/images/episode-001/magazine/`.
