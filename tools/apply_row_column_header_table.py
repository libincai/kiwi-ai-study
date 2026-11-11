"""Add kiwi-edu-table-row-column-header to matching tables (DESIGN_STANDARDS §6.3)."""
from __future__ import annotations

import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TABLE_RE = re.compile(r"<table\b([^>]*)>(.*?)</table>", re.I | re.S)
ROW_COL = "kiwi-edu-table-row-column-header"
SKIP_CLASS = (
    "kiwi-edu-table-with-mnemonic",
    "kiwi-edu-table-visual-compare",
    "kiwi-edu-table-explain",
)


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("\xa0", " ").strip()


def is_data_grid(body: str) -> bool:
    thead = re.search(r"<thead\b[^>]*>(.*?)</thead>", body, re.I | re.S)
    if not thead:
        return True
    ths = re.findall(r"<th[^>]*>(.*?)</th>", thead.group(1), re.I | re.S)
    if len(ths) < 2:
        return True
    h0 = strip_html(ths[0]).lower()
    if h0 in {"x", "t", "t (s)", "time (s)"}:
        return True
    if h0.startswith("time") and "(" in h0:
        return True
    tbody = re.search(r"<tbody\b[^>]*>(.*?)</tbody>", body, re.I | re.S)
    if not tbody:
        return False
    row = re.search(r"<tr[^>]*>(.*?)</tr>", tbody.group(1), re.I | re.S)
    if not row:
        return False
    cell = re.search(r"<t[hd][^>]*>(.*?)</t[hd]>", row.group(1), re.I | re.S)
    if not cell:
        return False
    t0 = strip_html(cell.group(1))
    if re.fullmatch(r"[\d.+\-—–\s]+", t0):
        return True
    return False


def add_classes(attrs: str) -> str:
    if ROW_COL in attrs:
        return attrs
    m = re.search(r'\bclass="([^"]*)"', attrs)
    if m:
        classes = m.group(1).split()
        if "edu-table" not in classes and "car-table" not in classes:
            classes = ["edu-table", *classes]
        if ROW_COL not in classes:
            classes.append(ROW_COL)
        return attrs[: m.start(1)] + " ".join(classes) + attrs[m.end(1) :]
    base = "edu-table" if "car-table" not in attrs else "car-table"
    extra = f' class="{base} {ROW_COL}"'
    return attrs.rstrip() + extra


def process_file(path: pathlib.Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        attrs, body = m.group(1), m.group(2)
        if any(s in attrs for s in SKIP_CLASS):
            return m.group(0)
        if ROW_COL in attrs:
            return m.group(0)
        if not re.search(r"<thead\b", body, re.I):
            return m.group(0)
        if is_data_grid(body):
            return m.group(0)
        n += 1
        return "<table" + add_classes(attrs) + ">" + body + "</table>"

    new_text = TABLE_RE.sub(repl, text)
    if n and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> None:
    total = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in str(path):
            continue
        c = process_file(path)
        if c:
            rel = path.relative_to(ROOT)
            print(f"{rel}: {c} table(s)")
            total += c
    print(f"Done. Updated {total} table(s).")


if __name__ == "__main__":
    main()
