import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"D:\YuanSync\Mirror\MyAI\KIWI_EP15_Model_Tool_Agent_Updated.docx")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

z = zipfile.ZipFile(DOCX)
root = ET.fromstring(z.read("word/document.xml"))
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
rels_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
rid_to = {}
for rel in rels_root.findall(f"{PKG}Relationship"):
    rid = rel.get("Id")
    tgt = rel.get("Target")
    if rid and tgt:
        rid_to[rid] = tgt

ep = None
rows = []
last_para = ""
for p in root.iter(W + "p"):
    texts = [t.text for t in p.iter(W + "t") if t.text]
    para = "".join(texts).strip()
    m = re.search(r"第\s*(\d+)\s*集", para)
    if m:
        ep = int(m.group(1))
    has_img = next(p.iter(A + "blip"), None) is not None
    if para and not has_img:
        last_para = para
    for blip in p.iter(A + "blip"):
        rid = blip.get(R + "embed") or blip.get(f"{{{R}}}embed")
        if not rid and blip.attrib:
            for k, v in blip.attrib.items():
                if k.endswith("embed"):
                    rid = v
                    break
        if not rid:
            continue
        tgt = rid_to.get(rid, "?")
        rows.append((ep, Path(tgt).name, last_para[:120]))

print("rels sample", list(rid_to.items())[:3], "count", len(rid_to))

for ep_num in (12,):
    print(f"=== Episode {ep_num} ===")
    n = 0
    last_text = ""
    for e, img, txt in rows:
        if e != ep_num:
            continue
        n += 1
        if txt:
            last_text = txt
        print(f"mag-{n:02d} <= {img} | ctx: {last_text[:70]}")
