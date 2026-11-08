# AI Knowledge Class — magazine episode pages (agent guide)

**Golden reference:** `ai/episode-01.html`  
**Also read:** `DESIGN_STANDARDS.md` (Level 4 shell, topic banner, script source of truth, breadcrumbs)  
**When to use:** Level 4 AI episode detail pages with **text-first magazine layout** + **6–8 spot illustrations** (not comic strips, not full-width image grids).

---

## Agent workflow (new episode)

1. **Script:** Use `episodes/episode-NNN/1-script/` (or user-supplied script). Preserve sequence, examples, and teaching beats; write an **article**, not line-by-line transcript.
2. **Copy shell:** Duplicate `ai/episode-01.html` → `ai/episode-NN.html` (match site naming). Keep header, footer, language script, `ai-bottom-nav`, `body.topic-page`, `main.topic-main`, topic banner pattern.
3. **Breadcrumb:** Register in `assets/js/drive-breadcrumb.js` (parent → `ai/index.html`).
4. **Images:** Put WebP/JPG in `ai/images/episode-NNN/magazine/` as `epNN-mag-01-….webp` (see [Images](#images)).
5. **Body:** Replace content between `<!-- LEVEL-4 BODY START -->` / `END` using patterns below. **Keep the page `<style>` block** from episode 01 unless adding episode-specific tokens only.
6. **Balance pass (required):** Walk every `.ep-pair` and apply [Balance & density](#balance--density). Do not skip this step — thin pairs and white gaps beside floats are blocking defects, not polish.
7. **Checklist:** [Publish checklist](#publish-checklist).

---

## Audience & tone

- **Who:** Middle / high school (grades ~6–12), bilingual EN + 中文 (`data-en` / `data-zh` on the same element; update both together).
- **Voice:** Curious, capable, a little warm — analogies from school, phones, games, daily life. Accurate to script; no hype, no “AI is human.”

| Do | Avoid |
|----|--------|
| Paragraphs + a few section `h2`s | An `h3` per beat or comic-panel grid |
| `.ep-myth` for “Mix-up N: …” | Blue button-style UI |
| Short figure captions; lesson in HTML | Long text baked into images |
| One orange `.nf-note` when a habit tip helps | Full-width note beside wrong column |

---

## Page structure

```
topic banner (kicker · EPISODE N, h1, subtitle)
article.nf-section.ep-article
  div.ep-pair          → intro + welcome figure
  h2                   → section (3–4 per episode typical)
  p                    → optional one-line bridge under h2
  div.ep-pair          → myth + figure + prose (repeat)
  ...
  h2                   → closing section (e.g. definition)
  div.ep-pair          → figure + closing prose
  [div.ep-abilities]   → optional keyword row (ep01 pattern)
nav.ai-bottom-nav      → prev / all episodes / next
p.ai-footer-note
```

- **Width:** `.ep-article { width: 100% }` inside `.topic-main` — **same width as topic banner** (1240px frame).
- **Headings:** Section titles = **`h2` only**, `text-align: left`, `clear: both` (see episode 01 CSS). Mix-ups = **`.ep-myth` `<p>`**, not `h3`.

---

## CSS classes (copy from episode 01)

| Class | Role |
|--------|------|
| `.ep-article` | Main magazine column; full topic width |
| `.ep-pair` | One illustration + related copy; clearfix after floats |
| `.ep-figure` / `--right` / `--left` | Floated spot illustration — **same on-page size as Ep1** (`width: min(34%, 300px)`); alternate sides. **Do not** add wider variants (e.g. no `.ep-figure--landscape`). |
| `.ep-myth` | Mix-up or mistaken belief label (semibold blue) |
| `.nf-lead` | Opening lead paragraph |
| `.nf-note` | Orange tip panel (use sparingly, ~1 per page) |
| `.ep-flow-col` | **Paragraph + `.nf-note` beside same float** — shared width as text column (ep01 “Use your judgment” block) |
| `.ep-abilities` | **Keyword strip** — not pills/buttons; `识别 · 学习 · …` with left bar |
| `.ai-bottom-nav` | Episode prev/next; do not duplicate with a second promo banner |

Mobile (`max-width: 720px`): figures unfloat, centered at `width: min(72vw, 280px)` — copy **exactly** from `episode-01.html` (do not use wider mobile widths).

---

## Illustration pairing rules

1. Each `<figure class="ep-figure">` lives inside the **same** `.ep-pair` as the text it explains.
2. **DOM order:** `p.ep-myth` (if any) → `figure` (float) → explaining `p` block(s).
3. Place figure on the **first paragraph** that matches the art (e.g. car analogy → car image next to that paragraph, not under mix-up label only).
4. Alternate **right / left** floats for rhythm.
5. See [Balance & density](#balance--density) — expand copy when a float looks taller than its text or leaves visible gaps.

### Balance & density

Tall **9:16** spot figures need enough **paired prose** in the same `.ep-pair`. **Do not ship lopsided blocks.**

- **Rule (gaps):** If you see **more than one empty row** of unused space beside an illustration (or a large gap before the next `h2`), **add real copy** until the block looks balanced.
- **Rule (short copy):** If the text beside a figure is **too short** for that image (e.g. one light sentence next to a full-height spot, or the float clearly outlasts the paragraph), **add script-backed detail** until the pair reads and looks balanced — even when there is no obvious white band yet.
- **What to add:** Extra sentences from the episode **script** — school-life examples, a second analogy, a bridge line under the next `h2`, or a short recap. Match Ep1’s student tone.
- **What not to add:** Padding, repeated slogans, or lorem. Do **not** fix imbalance only by shrinking margins (unless the user asks).
- **When drafting a new episode:** After placing figures, scan each `.ep-pair` in the browser; thicken thin copy and fill gaps before publish.

### Orange info panel (`.nf-note`)

- **When:** One actionable habit (e.g. “verify before you trust”).
- **Width:** If beside a left/right figure, wrap body + note in **`.ep-flow-col`** so the note matches the **same column width** as the paragraph above — **not** full article width unless there is no adjacent float.
- **Placement:** Directly **under** the paragraph it extends (episode 01: under the “models can be wrong …” paragraph).

---

## Images

- **Path:** `ai/images/episode-NNN/magazine/`
- **Naming:** `epNN-mag-01-welcome.webp`, `epNN-mag-02-….webp`, … (semantic slug)
- **On-page display size (standard):** Always match **`ai/episode-01.html`** — floated figures use `.ep-figure { width: min(34%, 300px); }` only. Source files may be 9:16, 16:9, or other aspects; the browser scales them inside the **same max ~300px column width**. Never widen floats for landscape art (no `52%` / `480px` rules).
- **`<img>` dimensions:** Set `width` and `height` to the **file’s true pixel size** (e.g. Ep1 spots `360`×`640`; 1280×720 WebP → `1280`×`720`) so aspect ratio is correct while CSS controls display width.
- **`loading="lazy"`** · Decorative spots → `alt=""` when caption + body carry the lesson
- **Source:** User-generated / storyboard pipeline — do not copy reference JPGs into the repo without instruction

---

## Content source

- Video **script** = source of truth for ideas, order, examples, mix-ups.
- Web page = merged paragraphs, **3–4 `h2` sections**, mix-ups as `.ep-myth`.
- Episode 1 pattern: six mix-ups grouped into sections (apps/brands, beyond chat, judgment, definition) — other episodes may group differently but keep **few section titles**.

---

## Files & metadata

| Item | Pattern |
|------|---------|
| HTML | `ai/episode-NN.html` |
| Title | `… \| AI Knowledge Class · Episode N \| Kiwi 爱AI Study` |
| Banner kicker | `AI EDUCATION · EPISODE N` / `人工智能教育 · 第 N 集` |
| Figure src | `images/episode-NNN/magazine/epNN-mag-….webp` |

---

## Publish checklist

- [ ] Shell matches ep01 (header, banner, bottom nav, language JS).
- [ ] Breadcrumb entry in `drive-breadcrumb.js`.
- [ ] Every magazine image in an `.ep-pair` with matching copy.
- [ ] ≤4 section `h2`s; left-aligned; mix-ups only as `.ep-myth`.
- [ ] EN + 中文 in sync on all new/edited nodes.
- [ ] `.ep-abilities` (if used) is keyword strip, not button pills.
- [ ] At most one `.nf-note`; width via `.ep-flow-col` when floated beside art.
- [ ] No copied reference assets; WebP in `magazine/` folder.
- [ ] Script beats preserved; student tone; no giant next-episode graphic (nav link is enough).
- [ ] Each figure’s paired text is substantial enough to balance the spot; no multi-row gaps; expand from script where copy is thin.
- [ ] Figure CSS matches Ep1 float width (`min(34%, 300px)`); no extra landscape/wide figure classes.

---

## Future: shared CSS

Episode magazine styles still live in **episode 01’s `<style>` block**. When a second episode ships, consider moving the `.ep-*` rules to `assets/css/` and linking once — until then, **clone the block from `episode-01.html`** when creating `episode-02.html`.
