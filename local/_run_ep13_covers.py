"""Regenerate episode 013 covers from 4-metadata and export hub WebP."""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

MYAI = Path(r"D:\YuanSync\Mirror\MyAI")
STUDIO = MYAI / "ai-learning-studio"
ROOT = Path(r"G:\02-MyBackup2Drive\04 AI-Learning-Studio")
WEBSITE = Path(r"D:\YuanSync\Mirror\MyAI\kiwi-ai-study")
META = ROOT / "episodes" / "episode-013" / "4-metadata"
OUT = ROOT / "episodes" / "episode-013" / "2-cover"
ARCHIVE = OUT / "archive"
BASES = STUDIO / "assets" / "cover-bases"
SCRIPTS = MYAI / "skills" / "create-covers" / "scripts"

EP = 13
NNN = "013"
title_cn = (META / "eps013_cover_title_cn.txt").read_text(encoding="utf-8").strip()
title_en = (META / "eps013_cover_title_en.txt").read_text(encoding="utf-8").strip()
sub_cn = (META / "eps013_cover_subtitle_cn.txt").read_text(encoding="utf-8").strip()
sub_en = (META / "eps013_cover_subtitle_en.txt").read_text(encoding="utf-8").strip()

assert len(title_cn) <= 6
assert len(sub_cn) <= 20
assert len(title_en) <= 15
assert len(sub_en) <= 20

ARCHIVE.mkdir(parents=True, exist_ok=True)
for png in list(OUT.glob("ai-learning-studio-episode-013-*.png")):
    dest = ARCHIVE / f"{png.stem}_{datetime.now():%Y%m%d%H%M%S}{png.suffix}"
    shutil.move(png, dest)
    print("archived", dest.name)


def run(cmd: list[str]) -> None:
    print(">", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


jobs = [
    (
        [sys.executable, str(SCRIPTS / "compose_cn_3x4.py")],
        BASES / "ai-learning-studio-base-cn-3x4.png",
        BASES / "ai-learning-studio-base-cn-3x4.layout.json",
        title_cn,
        sub_cn,
        OUT / f"ai-learning-studio-episode-{NNN}-cn-3x4.png",
    ),
    (
        [sys.executable, str(SCRIPTS / "compose_cn_4x3.py")],
        BASES / "ai-learning-studio-base-cn-4x3.png",
        BASES / "ai-learning-studio-base-cn-4x3.layout.json",
        title_cn,
        sub_cn,
        OUT / f"ai-learning-studio-episode-{NNN}-cn-4x3.png",
    ),
]
for prefix, base, layout, title, subtitle, output in jobs:
    run(
        prefix
        + [
            "--base",
            str(base),
            "--layout",
            str(layout),
            "--episode",
            str(EP),
            "--title",
            title,
            "--subtitle",
            subtitle,
            "--output",
            str(output),
        ]
    )

for lang, title, subtitle in (
    ("en", title_en, sub_en),
    ("cn", title_cn, sub_cn),
):
    for aspect in ("3x4", "4x3", "16x9"):
        if lang == "cn" and aspect in ("3x4", "4x3"):
            continue
        base = BASES / f"ai-learning-studio-base-{lang}-{aspect}.png"
        layout = BASES / f"ai-learning-studio-base-{lang}-{aspect}.layout.json"
        output = OUT / f"ai-learning-studio-episode-{NNN}-{lang}-{aspect}.png"
        run(
            [
                sys.executable,
                str(SCRIPTS / "compose_cover.py"),
                "--base",
                str(base),
                "--layout",
                str(layout),
                "--lang",
                lang,
                "--episode",
                str(EP),
                "--title",
                title,
                "--subtitle",
                subtitle,
                "--output",
                str(output),
            ]
        )

IMG_DIR = WEBSITE / "ai" / "images"


def export_webp(lang: str) -> None:
    png = OUT / f"ai-learning-studio-episode-{NNN}-{lang}-4x3.png"
    if not png.is_file():
        print("skip webp", lang, "no png")
        return
    canonical = IMG_DIR / f"ai-learning-studio-episode-{NNN}-{lang}-4x3.webp"
    if canonical.is_file():
        n = 1
        while True:
            backup = IMG_DIR / f"ai-learning-studio-episode-{NNN}-{lang}-4x3-{n:03d}.webp"
            if not backup.is_file():
                shutil.move(canonical, backup)
                print("renamed", canonical.name, "->", backup.name)
                break
            n += 1
    im = Image.open(png).convert("RGB")
    im.save(canonical, format="WEBP", quality=82, method=6)
    print("webp", canonical, canonical.stat().st_size)


export_webp("cn")
export_webp("en")
print("done")
