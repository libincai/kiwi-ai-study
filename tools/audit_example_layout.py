#!/usr/bin/env python3
"""Audit worked-example layout against DESIGN_STANDARDS."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit_file(path: Path) -> list[tuple[str, str]]:
    t = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    issues: list[tuple[str, str]] = []

    for om in re.finditer(r'<ol class="kiwi-example-steps[^"]*">([\s\S]*?)</ol>', t):
        inner = om.group(1)
        lis = len(re.findall(r"<li[\s>]", inner))
        if lis == 1:
            ctx = t[max(0, om.start() - 120) : om.start()]
            in_standard = "kiwi-example-standard" in ctx
            tag = "single-li-ol"
            if in_standard:
                tag += " (in kiwi-example-standard)"
            issues.append(
                (
                    rel,
                    f"{tag}: replace with "
                    f"<p class=\"kiwi-example-list-part kiwi-example-list-step\">",
                )
            )

    for um in re.finditer(r'<ul class="kiwi-example-list">([\s\S]*?)</ul>', t):
        ul = um.group(1)
        for lm in re.finditer(r"<li>([\s\S]*?)</li>", ul):
            li = lm.group(1)
            if "kiwi-example-list-part" not in li:
                continue
            parts = li.count("kiwi-example-list-part")
            if parts < 2:
                continue
            has_ans = "kiwi-example-list-answer" in li
            has_step = "kiwi-example-list-step" in li
            middle = parts - 1 - (1 if has_ans else 0)
            if not has_ans:
                issues.append((rel, "multi-line kiwi-example-list: missing kiwi-example-list-answer"))
            if middle >= 1 and not has_step:
                issues.append((rel, "multi-line kiwi-example-list: missing kiwi-example-list-step"))

    if re.search(
        r'<ol class="kiwi-example-steps[^"]*">(?:(?!</ol>).)*?</ul>',
        t,
    ):
        issues.append((rel, "malformed: kiwi-example-steps closed with </ul> (use </ol>)"))

    return issues


def main() -> int:
    all_issues: list[tuple[str, str]] = []
    for path in sorted((ROOT / "math").glob("*.html")):
        all_issues.extend(audit_file(path))

    if not all_issues:
        print("No layout issues found.")
        return 0

    by_file: dict[str, list[str]] = {}
    for rel, msg in all_issues:
        by_file.setdefault(rel, []).append(msg)

    for rel in sorted(by_file):
        print(rel)
        for msg in by_file[rel]:
            print(f"  - {msg}")
    print(f"\nTotal: {len(all_issues)} issue(s) in {len(by_file)} file(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
