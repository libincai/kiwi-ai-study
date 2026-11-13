"""Copy trigonometry media from updated docx into site assets."""
from __future__ import annotations

import zipfile
from pathlib import Path

DOCX = Path(r"c:\Users\yyuan\Downloads\math-quick-ref-trigonometry-angle-C-updated.docx")
OUT = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\assets\math")
NAMES = [
    "image25.webp",
    "image26.webp",
    "image27.webp",
    "image28.webp",
    "image29.webp",
    "image30.webp",
    "image31.webp",
    "image32.png",
    "image39.png",
]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DOCX) as z:
        for name in NAMES:
            src = f"word/media/{name}"
            dest = OUT / f"trig-{name.rsplit('.', 1)[0]}.{name.rsplit('.', 1)[1]}"
            dest.write_bytes(z.read(src))
            print(dest, dest.stat().st_size)

if __name__ == "__main__":
    main()
