#!/usr/bin/env python3
"""Flag ol.kiwi-example-steps that look like parallel variants, not solution steps."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "math"
STEP_MARKERS = re.compile(
    r"[=÷×/+\-]|remainder|因此|所以|→|∴|because|multiply|divide|simplify|substitute|cancel|convert|GCF|LCM",
    re.I,
)


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[^;]+;", " ", s)
    return " ".join(s.split())


PARALLEL_CTX = re.compile(
    r"also said as|也可说|right triangle has:|三角形：|Examples:\s*</p>\s*<ol",
    re.I,
)


def main() -> None:
    if "--all" in __import__("sys").argv:
        for path in sorted(ROOT.glob("*.html")):
            t = path.read_text(encoding="utf-8")
            for om in re.finditer(r'<ol class="kiwi-example-steps[^"]*">([\s\S]*?)</ol>', t):
                inner = om.group(1)
                lis = re.findall(r"<li[^>]*>([\s\S]*?)</li>", inner)
                if len(lis) < 2:
                    continue
                plain = [strip_tags(li)[:100] for li in lis]
                ctx = strip_tags(t[max(0, om.start() - 200) : om.start()])[-70:]
                line = t[: om.start()].count("\n") + 1
                print(f"\n{path.name}:{line}  ctx=...{ctx}")
                for i, p in enumerate(plain, 1):
                    print(f"  {i}. {p}")
        return

    for path in sorted(ROOT.glob("*.html")):
        t = path.read_text(encoding="utf-8")
        for om in re.finditer(r'<ol class="kiwi-example-steps[^"]*">([\s\S]*?)</ol>', t):
            inner = om.group(1)
            lis = re.findall(r"<li[^>]*>([\s\S]*?)</li>", inner)
            if not lis:
                continue
            plain = [strip_tags(li)[:160] for li in lis]
            ctx = t[max(0, om.start() - 500) : om.start()]
            has_parallel_ctx = bool(PARALLEL_CTX.search(ctx))
            has_also = "also said as" in ctx.lower() or "也可说" in ctx
            non_step = sum(1 for p in plain if not STEP_MARKERS.search(p))
            # Parallel factor listings: "15 →" and "25 →" with no sequential check
            parallel_factors = (
                len(lis) == 2
                and all("→" in p for p in plain)
                and not any("?" in p for p in plain)
                and "Factors of" not in plain[0]
            )
            if (
                has_also
                or has_parallel_ctx
                or parallel_factors
                or (non_step == len(lis) and len(lis) >= 2)
            ):
                line = t[: om.start()].count("\n") + 1
                print(f"\n{path.name}:{line} (also={has_also}, non_step={non_step}/{len(lis)}, fac={parallel_factors})")
                print("  CTX:", strip_tags(ctx)[-120:])
                for i, p in enumerate(plain, 1):
                    print(f"  {i}. {p}")


if __name__ == "__main__":
    main()
