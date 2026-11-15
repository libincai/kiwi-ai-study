"""Find Level 4 foundation pages with empty or broken lesson-card bodies."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "math"


class Stripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        self._chunks.append(data)

    def plain(self) -> str:
        return re.sub(r"\s+", " ", "".join(self._chunks)).strip()


CARD_RE = re.compile(
    r'<details\s+class="lesson-card"[^>]*>.*?<summary[^>]*>(?P<summary>.*?)</summary>(?P<body>.*?)</details>',
    re.I | re.S,
)
TAG_RE = re.compile(r"<(p|h[2-6]|ul|ol|table|img|math|div|details)\b", re.I)


def main() -> None:
    issues: list[tuple[str, ...]] = []
    level4_files = sorted(
        p for p in ROOT.glob("foundation-*.html") if "foundation-level4" in p.read_text(encoding="utf-8")
    )

    for path in level4_files:
        html = path.read_text(encoding="utf-8")
        cards = list(CARD_RE.finditer(html))
        if not cards:
            issues.append((path.name, "NO_CARDS", "", ""))
            continue

        for m in cards:
            body = m.group("body")
            summary = re.sub(r"<[^>]+>", "", m.group("summary"))
            summary = re.sub(r"\s+", " ", summary).strip()[:80]

            if "lesson-card-content" not in body:
                issues.append((path.name, "NO_CONTENT_WRAPPER", summary, str(len(body))))
                continue

            inner_m = re.search(
                r'<div\s+class="lesson-card-content"[^>]*>([\s\S]*?)</div>',
                body,
                re.I,
            )
            inner = inner_m.group(1) if inner_m else body

            strip = Stripper()
            try:
                strip.feed(inner)
            except Exception:  # noqa: BLE001
                pass
            plain = strip.plain()
            tag_count = len(TAG_RE.findall(inner))

            if len(plain) < 20 and tag_count < 2:
                issues.append(
                    (
                        path.name,
                        "EMPTY_OR_TINY",
                        summary,
                        f"chars={len(plain)} tags={tag_count}",
                    )
                )

        art = re.search(
            r'<article class="mf-article mf-chapter">([\s\S]*?)</article>',
            html,
        )
        if not art:
            continue
        article = art.group(1)
        for h4 in re.finditer(r"<h4\b[^>]*>[\s\S]*?</h4>", article):
            pos = h4.start()
            before = article[:pos]
            in_content = before.rfind('<div class="lesson-card-content"') > before.rfind(
                "</details>"
            )
            if in_content:
                continue
            after_last_details = before.rsplit("</details>", 1)[-1]
            if "lesson-card" in after_last_details or "<h4" in after_last_details:
                title = re.sub(r"<[^>]+>", "", h4.group())
                title = re.sub(r"\s+", " ", title).strip()[:60]
                issues.append((path.name, "H4_OUTSIDE_CARD", title, ""))

    print(f"Scanned {len(level4_files)} Level 4 pages")
    print(f"=== Issues ({len(issues)}) ===")
    for row in issues:
        print(" | ".join(row))


if __name__ == "__main__":
    main()