from pathlib import Path

MATH = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math")
FIG = """<style id="trig-beyond-90-figures">
.mf-article .lesson-card-content .trig-beyond-90-figure{margin:14px 0 6px;text-align:center}
.mf-article .lesson-card-content .trig-beyond-90-figure img{width:100%;height:auto;display:block;margin:0 auto;border:0;border-radius:0;object-fit:contain;box-shadow:none}
.mf-article .trig-beyond-90-figure img{max-width:min(100%,780px)}
</style>"""
KATEX_CSS = '<link href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" rel="stylesheet"/>'
KATEX_JS = """<script defer crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="../assets/js/kiwi-math-katex.js?v=6"></script>"""

for p in MATH.glob("foundation-*.html"):
    t = p.read_text(encoding="utf-8")
    changed = False
    if ("kiwi-math-latex" in t or "kiwi-math-block" in t) and "katex.min.js" not in t:
        if "katex.min.css" not in t:
            t = t.replace("</head>", KATEX_CSS + "\n</head>", 1)
        t = t.replace("</footer>", KATEX_JS + "\n</footer>", 1)
        changed = True
    if "trig-beyond-90-figure" in t and "trig-beyond-90-figures" not in t:
        t = t.replace("</head>", FIG + "\n</head>", 1)
        changed = True
    if changed:
        p.write_text(t, encoding="utf-8")
        print("patched", p.name)
