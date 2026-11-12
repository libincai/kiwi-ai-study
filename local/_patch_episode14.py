from pathlib import Path

html_path = Path(r"D:\YuanSync\Mirror\MyAI\kiwi-ai-study\ai\episode-14.html")
body_path = Path(r"D:\YuanSync\Mirror\MyAI\kiwi-ai-study\local\_episode14_body.html")
html = html_path.read_text(encoding="utf-8")
body = body_path.read_text(encoding="utf-8")
marker = '<article class="nf-section ep-article"'
start = html.index(marker)
end = html.index("</article>", start) + len("</article>")
new = (
    html[:start]
    + '<article class="nf-section ep-article" aria-label="Episode article">\n'
    + body.strip()
    + "\n    </article>"
    + html[end:]
)
html_path.write_text(new, encoding="utf-8")
print("ok", new.count("ep14-mag-"))
