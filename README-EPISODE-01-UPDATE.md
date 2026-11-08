# Episode 1 layout update

- Reworked `ai/episode-01.html` to match the approved reference: existing site navigation, illustrated episode banner, a compact bilingual episode-introduction panel, and 15 story cards in a 5 × 3 desktop grid.
- Tablet and mobile breakpoints reflow the cards without stretching or CSS-cropping their images.
- Each of the 15 picture assets is stored separately as a WebP file. The illustration crops are derived from the approved visual reference; the card headings and explanations remain live bilingual HTML.
- Other site pages, shared navigation, logo, footer, and global stylesheet were left intact.
\n\n## Language-specific hero and introduction label\n- The introduction pill now reads “Introduction” in English and “本集简介” in Chinese (removed “Episode”).\n- Added a dedicated English Episode 1 hero image (`ai/images/comics/episode01-hero-en.webp`). The page language switch now selects the English or Chinese hero image automatically.\n