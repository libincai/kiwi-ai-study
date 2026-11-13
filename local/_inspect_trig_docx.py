"""Inspect trigonometry updated docx structure."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"c:\Users\yyuan\Downloads\math-quick-ref-trigonometry-angle-C-updated.docx")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def para_text(p):
    parts = []
    for child in list(p):
        if child.tag == W + "r":
            for t in child.iter(W + "t"):
                if t.text:
                    parts.append(t.text)
            for omath in child.iter(M + "oMath"):
                parts.append(f"[{math_text(omath)}]")
        elif child.tag == M + "oMath":
            parts.append(f"[{math_text(child)}]")
    return "".join(parts).strip()


def math_text(el):
    return "".join(t.text or "" for t in el.iter(f"{M}t"))


def main():
    with zipfile.ZipFile(DOCX) as z:
        body = list(ET.fromstring(z.read("word/document.xml")).find(W + "body"))

    sections: list[tuple[str, list[str]]] = []
    current_title = "_intro"
    current_lines: list[str] = []

    for el in body:
        if el.tag == W + "p":
            line = para_text(el)
            pstyle = ""
            ppr = el.find(W + "pPr")
            if ppr is not None:
                ps = ppr.find(W + "pStyle")
                if ps is not None:
                    pstyle = ps.get(W + "val") or ""

            is_h = bool(pstyle and re.search(r"Heading|Title", pstyle, re.I))
            if not is_h and line and len(line) < 90:
                if line in (
                    "Understanding Trigonometry",
                    "The Three Sides of a Right Triangle",
                    "The Four Basic Trigonometric Ratios",
                    "Special Right Triangles",
                    "Trigonometric Ratios Beyond 90°",
                    "Law of Cosines",
                ):
                    is_h = True

            if is_h and line:
                if current_lines:
                    sections.append((current_title, current_lines))
                current_title = line
                current_lines = []
            elif line:
                current_lines.append(line)
        elif el.tag == W + "tbl":
            rows = []
            for tr in el.iter(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    ctext = []
                    for p in tc.findall(W + "p"):
                        ctext.append(para_text(p))
                    cells.append(" | ".join(x for x in ctext if x))
                rows.append(" || ".join(cells))
            current_lines.append("TABLE: " + "; ".join(rows[:6]))

    if current_lines:
        sections.append((current_title, current_lines))

    print(f"sections: {len(sections)}")
    for title, lines in sections:
        print("---", title, f"({len(lines)} lines)")
        for ln in lines[:8]:
            print(" ", ln[:120])
        if len(lines) > 8:
            print("  ...")


if __name__ == "__main__":
    main()
