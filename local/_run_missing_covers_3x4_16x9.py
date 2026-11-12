"""Generate missing cn/en 3x4 and 16x9 covers for episodes 010–015 (keep existing 4x3)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MYAI = Path(r"D:\YuanSync\Mirror\MyAI")
STUDIO = MYAI / "ai-learning-studio"
ROOT = Path(r"G:\02-MyBackup2Drive\04 AI-Learning-Studio")
BASES = STUDIO / "assets" / "cover-bases"
SCRIPTS = MYAI / "skills" / "create-covers" / "scripts"

EPISODES = (10, 11, 12, 14, 15)
MISSING_ASPECTS = ("cn-3x4", "en-3x4", "cn-16x9", "en-16x9")


def run(cmd: list[str]) -> None:
    print(">", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def read_meta(ep: int, key: str) -> str:
    p = ROOT / f"episodes/episode-{ep:03d}/4-metadata/eps{ep:03d}_{key}.txt"
    return p.read_text(encoding="utf-8").strip()


for ep in EPISODES:
    nnn = f"{ep:03d}"
    out_dir = ROOT / f"episodes/episode-{nnn}/2-cover"
    title_cn = read_meta(ep, "cover_title_cn")
    title_en = read_meta(ep, "cover_title_en")
    sub_cn = read_meta(ep, "cover_subtitle_cn")
    sub_en = read_meta(ep, "cover_subtitle_en")

    jobs: list[tuple[str, str, str, str, Path]] = []

    for aspect in MISSING_ASPECTS:
        lang, asp = aspect.split("-", 1)
        output = out_dir / f"ai-learning-studio-episode-{nnn}-{lang}-{asp}.png"
        if output.is_file():
            print("skip exists", output.name)
            continue
        title = title_cn if lang == "cn" else title_en
        subtitle = sub_cn if lang == "cn" else sub_en
        base = BASES / f"ai-learning-studio-base-{lang}-{asp}.png"
        layout = BASES / f"ai-learning-studio-base-{lang}-{asp}.layout.json"
        jobs.append((lang, asp, title, subtitle, output))

    for lang, asp, title, subtitle, output in jobs:
        if lang == "cn" and asp == "3x4":
            run(
                [
                    sys.executable,
                    str(SCRIPTS / "compose_cn_3x4.py"),
                    "--base",
                    str(base := BASES / f"ai-learning-studio-base-cn-3x4.png"),
                    "--layout",
                    str(BASES / "ai-learning-studio-base-cn-3x4.layout.json"),
                    "--episode",
                    str(ep),
                    "--title",
                    title,
                    "--subtitle",
                    subtitle,
                    "--output",
                    str(output),
                ]
            )
        else:
            run(
                [
                    sys.executable,
                    str(SCRIPTS / "compose_cover.py"),
                    "--base",
                    str(BASES / f"ai-learning-studio-base-{lang}-{asp}.png"),
                    "--layout",
                    str(BASES / f"ai-learning-studio-base-{lang}-{asp}.layout.json"),
                    "--lang",
                    lang,
                    "--episode",
                    str(ep),
                    "--title",
                    title,
                    "--subtitle",
                    subtitle,
                    "--output",
                    str(output),
                ]
            )

print("all done")
