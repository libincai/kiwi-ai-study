"""Generate responsive WebP variants for homepage images (masters unchanged)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

VARIANTS: dict[str, list[int]] = {
    "assets/hero/banner-en.webp": [800],
    "assets/hero/banner-zh.webp": [800],
    "assets/hero/mobile-banner-en.webp": [640, 800],
    "assets/hero/mobile-banner-zh.webp": [640, 800],
    "assets/logo/kiwi-ai-study-logo.webp": [215, 430],
    "assets/logo/sherry-cai-signature.webp": [110, 220],
    "assets/books/speedy-playful-math-magic.webp": [200, 400],
    "assets/books/math-quick-reference-library.webp": [200, 400],
    "assets/books/math-quick-reference-library-advanced.webp": [200, 400],
}

WEBP_OPTS = {"quality": 86, "method": 6}


def resize_to_width(src: Path, width: int) -> Image.Image:
    with Image.open(src) as im:
        im = im.convert("RGBA") if im.mode in ("RGBA", "P") else im.convert("RGB")
        w, h = im.size
        if w <= width:
            return im.copy()
        new_h = max(1, round(h * width / w))
        return im.resize((width, new_h), Image.Resampling.LANCZOS)


def main() -> None:
    for rel, widths in VARIANTS.items():
        src = ROOT / rel
        if not src.is_file():
            raise SystemExit(f"Missing source: {src}")
        stem = src.stem
        for w in widths:
            out = src.with_name(f"{stem}-{w}w.webp")
            img = resize_to_width(src, w)
            img.save(out, format="WEBP", **WEBP_OPTS)
            print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()