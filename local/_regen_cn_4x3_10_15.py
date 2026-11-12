"""Regenerate CN 4x3 covers eps 10-15 after compose_cn_4x3 layout fix."""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

MYAI = Path(r"D:\YuanSync\Mirror\MyAI")
ROOT = Path(r"G:\02-MyBackup2Drive\04 AI-Learning-Studio")
WEBSITE = Path(r"D:\YuanSync\Mirror\MyAI\kiwi-ai-study")
BASES = MYAI / "ai-learning-studio" / "assets" / "cover-bases"
SCRIPT = MYAI / "skills" / "create-covers" / "scripts" / "compose_cn_4x3.py"

for ep in range(10, 16):
    nnn = f"{ep:03d}"
    meta = ROOT / f"episodes/episode-{nnn}/4-metadata"
    out_dir = ROOT / f"episodes/episode-{nnn}/2-cover"
    arch = out_dir / "archive"
    arch.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"ai-learning-studio-episode-{nnn}-cn-4x3.png"
    if out.is_file():
        dest = arch / f"{out.stem}_compose-fix_{datetime.now():%Y%m%d%H%M%S}.png"
        shutil.move(out, dest)
        print("archived", dest.name)
    title = (meta / f"eps{nnn}_cover_title_cn.txt").read_text(encoding="utf-8").strip()
    subtitle = (meta / f"eps{nnn}_cover_subtitle_cn.txt").read_text(encoding="utf-8").strip()
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--base",
            str(BASES / "ai-learning-studio-base-cn-4x3.png"),
            "--layout",
            str(BASES / "ai-learning-studio-base-cn-4x3.layout.json"),
            "--episode",
            str(ep),
            "--title",
            title,
            "--subtitle",
            subtitle,
            "--output",
            str(out),
        ],
        check=True,
    )
    canonical = WEBSITE / "ai" / "images" / f"ai-learning-studio-episode-{nnn}-cn-4x3.webp"
    if canonical.is_file():
        n = 1
        while True:
            bak = WEBSITE / "ai" / "images" / f"ai-learning-studio-episode-{nnn}-cn-4x3-{n:03d}.webp"
            if not bak.is_file():
                shutil.move(canonical, bak)
                print("webp backup", bak.name)
                break
            n += 1
    Image.open(out).convert("RGB").save(canonical, format="WEBP", quality=82, method=6)
    print("webp", canonical, canonical.stat().st_size)

print("done")
