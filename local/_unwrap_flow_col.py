"""Remove full-section .ep-flow-col wrappers so prose wraps floated figures (Level 4 magazine)."""
import re
from pathlib import Path

ROOT = Path(r"D:\YuanSync\Mirror\MyAI\kiwi-ai-study\ai")


def unwrap_flow_cols(html: str) -> str:
    html = html.replace('        <div class="ep-flow-col">\n', "")
    html = re.sub(r"\n        </div>\n(      </div>)", r"\n\1", html)
    return html


def main() -> None:
    for path in sorted(ROOT.glob("episode-*.html")):
        stem = path.stem
        if stem == "episode-special-learning":
            continue
        try:
            num = int(stem.split("-")[1])
        except (IndexError, ValueError):
            continue
        if num < 9 or num >= 10:
            continue  # 10–15: keep hand-maintained .ep-flow-col for .nf-note only
        text = path.read_text(encoding="utf-8")
        before = text.count('<div class="ep-flow-col">')
        text = unwrap_flow_cols(text)
        text = text.replace(
            ".ep-flow-col{overflow:hidden;min-width:0}",
            ".ep-flow-col{overflow:visible;min-width:0}",
        )
        path.write_text(text, encoding="utf-8")
        after = text.count('<div class="ep-flow-col">')
        print(f"{path.name}: flow-col {before} -> {after}")


if __name__ == "__main__":
    main()
