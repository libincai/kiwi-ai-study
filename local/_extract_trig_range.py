"""Extract trigonometry chapter paragraphs + math from updated docx."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"c:\Users\yyuan\Downloads\math-quick-ref-trigonometry-angle-C-updated.docx")
OUT = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\local\trig-docx-extract.txt")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def math_text(el):
    return "".join(t.text or "" for t in el.iter(f"{M}t"))


def para_line(p):
    parts = []
    for child in list(p):
        if child.tag == W + "r":
            for t in child.iter(W + "t"):
                if t.text:
                    parts.append(t.text)
            for om in child.iter(M + "oMath"):
                parts.append(f"${math_text(om)}$")
        elif child.tag == M + "oMath":
            parts.append(f"${math_text(child)}$")
    return "".join(parts).strip()


def is_heading(line: str) -> bool:
    known = {
        "Understanding Trigonometry",
        "The Three Sides of a Right Triangle",
        "The Pythagorean Theorem",
        "The Four Basic Trigonometric Ratios",
        "The SOH–CAH–TOA Mnemonic",
        "Special Right Triangles",
        "The 30°–60°–90° Triangle",
        "The 45°–45°–90° Triangle",
        "Finding a Missing Side",
        "Finding a Missing Angle",
        "Applications of Trigonometry",
        "Initial Arm and Terminal Arm",
        "Primary Trigonometric Ratios on the Coordinate Plane",
        "Signs of Trigonometric Ratios in Four Quadrants",
        "Related Acute Angle (Reference Angle)",
        "Coterminal Angles",
        "Trigonometric Ratios Beyond 90°",
        "Exact Values from Special Right Triangles",
        "Common Exact-Value Table",
        "Reciprocal Trigonometric Ratios",
        "Types of Oblique Triangles",
        "The Sine Law",
        "The SSA Ambiguous Case",
        "Using the Sine Law in Applications",
        "Why Two Different Triangles May Be Possible",
        "The Four Possible Outcomes",
        "Worked Example",
        "Understanding and Remembering the Formula",
        "What Is the Law of Cosines?",
        "Choosing Between the Sine Law and the Cosine Law",
        "Working with Three Dimensions",
        "Data and Graphs",
    }
    return line in known


def main():
    with zipfile.ZipFile(DOCX) as z:
        body = list(ET.fromstring(z.read("word/document.xml")).find(W + "body"))

    lines: list[str] = []
    capture = False
    for el in body:
        if el.tag == W + "p":
            line = para_line(el)
            if line == "Understanding Trigonometry":
                capture = True
            if capture and line == "Data and Graphs":
                break
            if capture and line:
                if is_heading(line):
                    lines.append("\n## " + line + "\n")
                else:
                    lines.append(line)
        elif el.tag == W + "tbl" and capture:
            row_bits = []
            for tr in el.iter(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    c = " ".join(para_line(p) for p in tc.findall(W + "p") if para_line(p))
                    if c:
                        cells.append(c)
                if cells:
                    row_bits.append(" | ".join(cells))
            if row_bits:
                lines.append("[TABLE]\n" + "\n".join(row_bits) + "\n[/TABLE]")

    text = "\n".join(lines)
    OUT.write_text(text, encoding="utf-8")
    print("wrote", OUT, "chars", len(text))


if __name__ == "__main__":
    main()
