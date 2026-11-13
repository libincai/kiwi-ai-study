from pathlib import Path

page = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\math\foundation-trigonometric-ratios-beyond-90.html")
article = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\local\_trig_beyond90_article.html")
text = page.read_text(encoding="utf-8")
chunk = article.read_text(encoding="utf-8")
marker = '<div class="mf-layout foundation-level4">'
start = text.index(marker)
end = text.index("</main>", start)
page.write_text(text[:start] + chunk + text[end:], encoding="utf-8")
print("patched", page)
