#!/usr/bin/env python3
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "math" / "unit-conversions-and-rates.html"
t = p.read_text(encoding="utf-8")
pat = (
    r"</ul><div class=\"kiwi-formula-row kiwi-math-block\" "
    r"data-en=\"[^\"]*Value[^\"]*\" data-zh=\"[^\"]*\"[^>]*>.*?</div><ul>"
)
rep = (
    "</ul><div class=\"kiwi-formula-row kiwi-math-block kiwi-math-latex\" "
    "data-tex-en=\"\\text{Value} = \\text{Rate} \\times "
    "\\text{Conversion}\\,\\text{Factor} \\times \\text{Quantity}\" "
    "data-tex-zh=\"\\text{数值} = \\text{比率} \\times \\text{换算因数} \\times \\text{数量}\">"
    "</div><ul>"
)
t2, n = re.subn(pat, rep, t, count=1, flags=re.DOTALL)
print("replacements", n)
if n:
    p.write_text(t2, encoding="utf-8")
