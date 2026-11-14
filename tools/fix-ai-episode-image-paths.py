"""Use root-relative /ai/images/ so clean URLs (/episode-02) still load figures."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "ai"


def main() -> None:
    for path in sorted(ROOT.glob("episode*.html")):
        text = path.read_text(encoding="utf-8")
        new = text.replace('src="images/', 'src="/ai/images/').replace(
            'href="images/', 'href="/ai/images/'
        )
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()