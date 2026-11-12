import re
import zipfile
from pathlib import Path

DOCX = Path(r"D:\YuanSync\Mirror\MyAI\KIWI_EP15_Model_Tool_Agent_Updated.docx")
z = zipfile.ZipFile(DOCX)
xml = z.read("word/document.xml").decode("utf-8", errors="replace")
rels = z.read("word/_rels/document.xml.rels").decode("utf-8")

s = xml.find("第 12 集")
e = xml.find("第 13 集")
if s < 0:
    raise SystemExit("Episode 12 marker not found")
chunk = xml[s:e] if e > s else xml[s:]

def target_for_rid(rid: str) -> str:
    m = re.search(rf'Id="{re.escape(rid)}"[^>]*Target="([^"]+)"', rels)
    return Path(m.group(1)).name if m else "?"

parts = re.split(r"<w:p[^>]*>", chunk)
n = 0
for p in parts:
    m = re.search(r'r:embed="(rId\d+)"', p)
    if not m:
        continue
    n += 1
    texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)
    text = "".join(texts).strip()[:100]
    print(f"{n:02d} {target_for_rid(m.group(1))} | {text}")
