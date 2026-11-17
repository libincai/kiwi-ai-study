"""Build standard favicon assets at repo root from brand PNG."""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image
except ImportError as err:
    raise SystemExit("Pillow required: pip install Pillow") from err

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path(r"D:\YuanSync\Mirror\MyAI\assets\brand\logo\favicon-loveAI-180.png")
# Largest heart-only fit in the tab square (no circle, no clipping).
TAB_INSET_FILL = 0.99
TAB_PAD_PX = 1
APPLE_FILL = 0.9


def trim_opaque(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    bbox = im.split()[3].getbbox()
    return im.crop(bbox) if bbox else im


def pad_artwork(art: Image.Image, px: int) -> Image.Image:
    if px <= 0:
        return art
    cw, ch = art.size
    out = Image.new("RGBA", (cw + 2 * px, ch + 2 * px), (0, 0, 0, 0))
    out.paste(art, (px, px))
    return out


def render_tab_icon(art: Image.Image, size: int) -> Image.Image:
    """Heart only on transparent ground — max size, centered, no edge clip."""
    art = pad_artwork(art, TAB_PAD_PX)
    cw, ch = art.size
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    limit = size * TAB_INSET_FILL
    scale = min(limit / cw, limit / ch)
    new_w = max(1, int(round(cw * scale)))
    new_h = max(1, int(round(ch * scale)))
    scaled = art.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x = (size - new_w) // 2
    y = (size - new_h) // 2
    canvas.paste(scaled, (x, y), scaled)
    return canvas


def render_contained(art: Image.Image, size: int, fill: float) -> Image.Image:
    cw, ch = art.size
    side = max(cw, ch)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(art, ((side - cw) // 2, (side - ch) // 2))
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = max(1, int(round(size * fill)))
    scaled = square.resize((inner, inner), Image.Resampling.LANCZOS)
    offset = (size - inner) // 2
    canvas.paste(scaled, (offset, offset), scaled)
    return canvas


def main() -> None:
    src = DEFAULT_SRC if DEFAULT_SRC.is_file() else ROOT / "apple-touch-icon.png"
    if not src.is_file():
        raise SystemExit(f"source not found: {src}")
    art = trim_opaque(Image.open(src))

    for size in (16, 32):
        render_tab_icon(art, size).save(
            ROOT / f"favicon-{size}x{size}.png",
            format="PNG",
            optimize=True,
        )

    render_contained(art, 180, APPLE_FILL).save(
        ROOT / "apple-touch-icon.png",
        format="PNG",
        optimize=True,
    )

    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    ico_images = [render_tab_icon(art, s[0]) for s in ico_sizes]
    ico_images[0].save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=ico_sizes,
        append_images=ico_images[1:],
    )
    print(
        "wrote favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png",
        "(heart only)",
    )


if __name__ == "__main__":
    main()