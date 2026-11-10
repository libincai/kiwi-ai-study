#!/usr/bin/env python3
"""Remove trailing Word-export `\\ ` from x-tex annotations in one HTML file."""
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "math/foundation-algebra-language-and-patterns.html")
t = path.read_text(encoding="utf-8")
t2 = re.sub(r"\\ +(?=&lt;/annotation)", "", t)
t2 = re.sub(r"\\ +(?=</annotation>)", "", t2)
t2 = t2.replace("</math>is", "</math> is")
t2 = t2.replace("&lt;/math&gt;is", "&lt;/math&gt; is")
t2 = t2.replace('<mspace width="0.222em"></mspace></mrow>', "</mrow>")
t2 = t2.replace(
    "&lt;mspace width=&quot;0.222em&quot;&gt;&lt;/mspace&gt;&lt;/mrow&gt;",
    "&lt;/mrow&gt;",
)
if t2 != t:
    path.write_text(t2, encoding="utf-8")
    print("fixed", path)
else:
  print("no changes", path)
