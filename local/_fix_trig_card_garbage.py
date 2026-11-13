"""Remove broken duplicate title fragments inside lesson-card-content."""
from __future__ import annotations

import re
from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
BEYOND_SNIPPET = Path(__file__).resolve().parent / "_trig_beyond90_article.html"

GARBAGE = re.compile(
    r'(<div class="lesson-card-content">)id="[^"]+"\s+'
    r'data-en="[^"]*"\s+data-zh="[^"]*">[^<]*</h4>\s*',
    re.DOTALL,
)
INNER_CARD = re.compile(
    r"<details class=\"lesson-card\"[^>]*><summary([^>]*)>(.*?)</summary>\s*"
    r"<div class=\"lesson-card-content\">(.*?)</div>\s*</details>",
    re.DOTALL,
)
BEYOND_CARD = re.compile(
    r'(<details class="lesson-card"><summary id="trigonometric-ratios-beyond-90"[^>]*>'
    r".*?</summary><div class=\"lesson-card-content\">)(.*?)(</div></details>)",
    re.DOTALL,
)


def flatten_body(body: str) -> str:
    while True:
        m = INNER_CARD.search(body)
        if not m:
            return body
        body = (
            body[: m.start()]
            + f"<h4{m.group(1)}>{m.group(2)}</h4>{m.group(3)}"
            + body[m.end() :]
        )
    return body


def beyond_90_body() -> str:
    raw = BEYOND_SNIPPET.read_text(encoding="utf-8")
    m = re.search(
        r"<h1[^>]*>.*?</h1>\s*(.*)</article>",
        raw,
        re.DOTALL,
    )
    if not m:
        raise ValueError("beyond90 snippet missing article body")
    inner = m.group(1).strip()
    inner = re.sub(
        r"<h2 id=\"ratios-beyond-90\"[^>]*>.*?</h2>\s*",
        "",
        inner,
        count=1,
        flags=re.DOTALL,
    )
    return flatten_body(inner)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = GARBAGE.sub(r"\1", text)
    if path.name == "foundation-angles-and-trigonometric-ratios.html":
        text = BEYOND_CARD.sub(
            lambda m: m.group(1) + beyond_90_body() + m.group(3),
            text,
            count=1,
        )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    for path in sorted(MATH.glob("foundation-*.html")):
        if fix_file(path):
            print("fixed", path.name)


if __name__ == "__main__":
    main()
