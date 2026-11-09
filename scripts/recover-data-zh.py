#!/usr/bin/env python3
"""Restore data-zh / data-zh-label from git HEAD when placeholder corruption occurred."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

Z_ATTR = re.compile(r'(data-zh(?:-label)?)="([^"]*)"')
CORRUPT = re.compile(
    r"^(首页|关于我们|数学教育|人工智能教育|课堂学习|我的书籍|联系我们)\d+$"
)


def head_text(root: Path, rel: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "show", f"HEAD:{rel}"],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError:
        return None


def is_corrupt(val: str) -> bool:
    return bool(CORRUPT.match(val.strip()))


def restore_file(root: Path, path: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    head = head_text(root, rel)
    if head is None:
        return False
    original = path.read_text(encoding="utf-8")
    head_vals = [m.group(2) for m in Z_ATTR.finditer(head)]
    if not head_vals:
        return False

    idx = 0
    changed = False

    def repl(m: re.Match[str]) -> str:
        nonlocal idx, changed
        attr, val = m.group(1), m.group(2)
        if idx < len(head_vals) and is_corrupt(val):
            val = head_vals[idx]
            changed = True
        idx += 1
        return f'{attr}="{val}"'

    updated = Z_ATTR.sub(repl, original)
    if changed:
        path.write_text(updated, encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    fixed = 0
    for path in sorted(root.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if restore_file(root, path):
            fixed += 1
            print(path.relative_to(root))
    print(f"Restored: {fixed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
