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


## Episode 1 picture-story learning page

Episode 1 uses a 250-character Chinese introduction (with an equivalent English version), followed by 15 numbered picture-story panels. Each panel has one shared illustration and bilingual live-text captions beneath it. Desktop uses a three-column grid, tablet two columns, and mobile a single vertical reading column. The illustrations are optimized WebP files stored in `ai/images/comics/episode01-panels/`. Only `ai/episode-01.html` and its new Episode 1 illustration assets were changed.
