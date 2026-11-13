"""Turn nested lesson-card blocks into h4 headings inside the parent card."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _trig_toc_20261113 import SECTIONS, SIDEBAR_LEVEL2

ARTICLE_IN = re.compile(
    r"(<article class=\"mf-article mf-chapter\">)(.*?)(</article>)",
    re.DOTALL,
)
DETAILS_OPEN_RE = re.compile(r"<details class=\"lesson-card\"[^>]*>", re.IGNORECASE)
DETAILS_CLOSE = "</details>"
INNER_CARD = re.compile(
    r"<details class=\"lesson-card\"[^>]*><summary([^>]*)>(.*?)</summary>\s*"
    r"<div class=\"lesson-card-content\">(.*?)</div>\s*</details>",
    re.DOTALL,
)


def find_next_details_open(html: str, pos: int) -> re.Match[str] | None:
    return DETAILS_OPEN_RE.search(html, pos)


def is_inside_lesson_card_content(html: str, idx: int) -> bool:
    before = html[:idx]
    open_c = before.rfind('<div class="lesson-card-content">')
    if open_c == -1:
        return False
    close = before.rfind("</div></details>", open_c)
    return close == -1


def find_top_level_card_end(html: str, start: int) -> int:
    depth = 0
    i = start
    while i < len(html):
        open_m = DETAILS_OPEN_RE.match(html, i)
        if open_m:
            depth += 1
            i = open_m.end()
            continue
        if html.startswith(DETAILS_CLOSE, i):
            depth -= 1
            i += len(DETAILS_CLOSE)
            if depth == 0:
                return i
            continue
        i += 1
    raise ValueError("unclosed lesson-card")


def flatten_body(body: str) -> str:
    while True:
        m = INNER_CARD.search(body)
        if not m:
            return body
        repl = f"<h4{m.group(1)}>{m.group(2)}</h4>{m.group(3)}"
        body = body[: m.start()] + repl + body[m.end() :]
    return body


def flatten_nested_lesson_cards(inner: str) -> str:
    out: list[str] = []
    pos = 0
    while pos < len(inner):
        open_m = find_next_details_open(inner, pos)
        if not open_m:
            out.append(inner[pos:])
            break
        idx = open_m.start()
        out.append(inner[pos:idx])
        if is_inside_lesson_card_content(inner, idx):
            pos = idx + 1
            continue
        end = find_top_level_card_end(inner, idx)
        card = inner[idx:end]
        sm = re.search(r"<summary\b([^>]*)>(.*?)</summary>", card, re.DOTALL)
        cm = re.search(
            r'<div class="lesson-card-content">(.*)</div>\s*</details>\s*$',
            card,
            re.DOTALL,
        )
        if not sm or not cm:
            out.append(card)
            pos = end
            continue
        flat_body = flatten_body(cm.group(1))
        open_tag = open_m.group(0)
        out.append(
            f"{open_tag}<summary{sm.group(1)}>"
            f"{sm.group(2)}</summary>"
            f'<div class="lesson-card-content">{flat_body}</div></details>'
        )
        pos = end
    return "".join(out)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = ARTICLE_IN.search(text)
    if not m:
        return False
    inner = m.group(2)
    flat = flatten_nested_lesson_cards(inner)
    if flat == inner:
        return False
    text = ARTICLE_IN.sub(lambda mobj: mobj.group(1) + flat + mobj.group(3), text, count=1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    targets = [MATH / h for h, _, _ in SIDEBAR_LEVEL2]
    for hub, *_ in SECTIONS:
        p = MATH / hub
        if p not in targets:
            targets.append(p)
    for path in targets:
        if not path.is_file():
            print("skip", path.name)
            continue
        try:
            if process_file(path):
                print("flattened", path.name)
            else:
                print("unchanged", path.name)
        except ValueError as e:
            print("error", path.name, e)


if __name__ == "__main__":
    main()
