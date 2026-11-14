"""Episode figures: use ../ai/images/ (not /ai/images/) for GitHub project Pages + local clean URLs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "ai"
PREFIX = "../ai/images/"


def main() -> None:
    for path in sorted(ROOT.glob("episode*.html")):
        text = path.read_text(encoding="utf-8")
        new = text.replace('src="/ai/images/', f'src="{PREFIX}')
        new = new.replace('href="/ai/images/', f'href="{PREFIX}')
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()