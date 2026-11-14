"""Restore worked-example layout on mental-squaring (pre mistaken git checkout)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "math" / "thinking-mental-squaring-and-square-rooting.html"


def answers_to_follows(html: str) -> str:
    html = html.replace(
        '<blockquote class="kiwi-example-answer">',
        '<div class="kiwi-example-follow">',
    )
    # Close example-answer blocks (no other blockquotes use this wrapper chain).
    html = re.sub(
        r"(</ol>)(\s*)(</blockquote>)(\s*)(?=<div class=\"kiwi-example-follow\">)",
        r"\1\2</div>\3",
        html,
    )
    html = re.sub(
        r"</ol>\s*</blockquote>\s*</div>\s*</details>",
        "</ol></div></div></details>",
        html,
        count=1,
    )
    html = re.sub(
        r"</ol>\s*</ul>",
        "</ol></div>",
        html,
        count=1,
    )
    return html


def merge_append_steps(html: str) -> str:
    pat = re.compile(
        r"(<li[^>]*>(?:Append|接上)"
        r"[\s\S]*?"
        r'<math display="inline"[\s\S]*?</math>'
        r"[:：]</li>\s*)"
        r'<li[^>]*><p class="kiwi-formula-row">=([^<]+)</p></li>',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        head, val = m.group(1), m.group(2).strip()
        if ":</li>" in head:
            return head.replace(":</li>", f": {val}</li>")
        return head.replace("：</li>", f"：{val}</li>")

    return pat.sub(repl, html)


def mark_questions(html: str) -> str:
    html = re.sub(
        r'<div class="kiwi-example-block kiwi-example-standard">\s*<p><strong>',
        '<div class="kiwi-example-block kiwi-example-standard">\n<p class="kiwi-example-question"><strong>',
        html,
    )
    html = re.sub(
        r'<div class="kiwi-example-block kiwi-example-standard">\s*<p>(\d+)<sup>2</sup></p>',
        r'<div class="kiwi-example-block kiwi-example-standard">\n<p class="kiwi-example-question"><strong>\1<sup>2</sup></strong></p>',
        html,
    )
    html = re.sub(
        r'<div class="kiwi-example-follow">\s*<p>(\d+)<sup>2</sup></p>',
        r'<div class="kiwi-example-follow">\n<p class="kiwi-example-question"><strong>\1<sup>2</sup></strong></p>',
        html,
    )
    html = re.sub(
        r'<div class="kiwi-example-follow">\s*\n<p>(\d+)<sup>2</sup></p>',
        r'<div class="kiwi-example-follow">\n<p class="kiwi-example-question"><strong>\1<sup>2</sup></strong></p>',
        html,
    )
    return html


def simplify_step_items(html: str) -> str:
    html = html.replace('class="kiwi-equation-list-item"', "")
    html = re.sub(
        r'(<li[^>]*>)\s*<div class="kiwi-formula-row kiwi-math-block"\s+((?:data-en="[^"]*"\s+)?(?:data-zh="[^"]*"\s+)?)>',
        r"\1 \2>",
        html,
    )
    html = html.replace("<li >data-en=", "<li data-en=")
    html = re.sub(r"</div>\s*</li>", "</li>", html)
    within_steps = re.compile(
        r'(<ol class="kiwi-example-steps[^"]*"[^>]*>)([\s\S]*?)(</ol>)',
    )

    def fix_math(block: re.Match[str]) -> str:
        body = block.group(2)
        body = body.replace('display="block"', 'display="inline"')
        body = body.replace("display=&quot;block&quot;", "display=&quot;inline&quot;")
        return block.group(1) + body + block.group(3)

    return within_steps.sub(fix_math, html)


def flatten_follows(html: str) -> str:
    start = '<div class="kiwi-example-block kiwi-example-standard">'
    split = re.compile(r"</ol>\s*<div class=\"kiwi-example-follow\">", re.I)
    parts = html.split(start)
    out = [parts[0]]
    for chunk in parts[1:]:
        close_idx = chunk.find("</div>")
        if close_idx == -1:
            out.append(start + chunk)
            continue
        inner, tail = chunk[:close_idx], chunk[close_idx:]
        seen = False

        def repl(_: re.Match[str]) -> str:
            nonlocal seen
            if not seen:
                seen = True
                return '</ol>\n<div class="kiwi-example-follow">'
            return '</ol>\n</div>\n<div class="kiwi-example-follow">'

        inner = split.sub(repl, inner)
        out.append(start + inner + tail)
    return "".join(out)


def patch_styles(html: str) -> str:
    html = re.sub(
        r"\.kiwi-topic-article li\.kiwi-equation-list-item\{[^}]+\}\n"
        r"\.kiwi-topic-article li\.kiwi-equation-list-item::marker\{[^}]+\}\n"
        r"\.kiwi-topic-article li\.kiwi-equation-list-item::before\{[^}]+\}\n"
        r"\.kiwi-topic-article li\.kiwi-equation-list-item>p\{[^}]+\}\n"
        r"\.kiwi-topic-article li\.kiwi-equation-list-item>p math\{[^}]+\}\n",
        ".kiwi-topic-article .kiwi-example-steps > li{list-style:decimal inside!important;display:list-item!important;}\n",
        html,
    )
    html = html.replace(
        ".kiwi-topic-article .kiwi-example-standard > ol.kiwi-example-steps {",
        ".kiwi-topic-article .kiwi-example-standard ol.kiwi-example-steps {",
    )
    html = html.replace(
        ".kiwi-topic-article .kiwi-example-standard > ol.kiwi-example-steps > li {",
        ".kiwi-topic-article .kiwi-example-standard ol.kiwi-example-steps > li {",
    )
    html = html.replace(
        ".kiwi-topic-article .kiwi-example-standard > ol.kiwi-example-steps > li::marker {",
        ".kiwi-topic-article .kiwi-example-standard ol.kiwi-example-steps > li::marker {",
    )
    html = html.replace(
        ".kiwi-topic-article .kiwi-example-standard > ol.kiwi-example-steps > li > p {",
        ".kiwi-topic-article .kiwi-example-standard ol.kiwi-example-steps > li > p {",
    )
    if ".kiwi-example-standard .kiwi-example-follow{margin:.75rem 0 .35rem 0" not in html:
        html = html.replace(
            ".kiwi-topic-article .kiwi-example-follow{margin:.75rem 0 .35rem 3ch;",
            ".kiwi-topic-article .kiwi-example-standard .kiwi-example-follow{margin:.75rem 0 .35rem 0!important;",
        )
    extra = """
.kiwi-topic-article .kiwi-example-question{margin:.35rem 0 .4rem 3ch!important;padding:0!important;text-align:left!important;font-weight:700!important;}
.kiwi-topic-article .kiwi-example-standard .kiwi-example-follow .kiwi-example-question{margin-left:3ch!important;}
.kiwi-topic-article .kiwi-example-standard .kiwi-example-follow > p:not(.kiwi-example-question){margin-left:6ch!important;text-align:left!important;}
.kiwi-topic-article .kiwi-example-steps .kiwi-math-block,
.kiwi-topic-article .kiwi-example-steps .kiwi-formula-row{display:inline!important;width:auto!important;margin:0!important;padding:0!important;text-align:left!important;justify-content:flex-start!important;}
.kiwi-topic-article .kiwi-example-steps math[display="inline"]{display:inline!important;text-align:left!important;margin:0!important;}
.kiwi-topic-article .kiwi-example-steps li{margin:.35rem 0!important;text-align:left!important;}
"""
    if "kiwi-example-standard .kiwi-example-follow .kiwi-example-question" not in html:
        anchor = ".kiwi-topic-article .kiwi-standalone-example > ol.kiwi-example-steps {margin-left:6ch!important;}"
        html = html.replace(anchor, anchor + extra)
    return html


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    text = answers_to_follows(text)
    text = mark_questions(text)
    text = merge_append_steps(text)
    text = simplify_step_items(text)
    text = flatten_follows(text)
    text = patch_styles(text)
    PAGE.write_text(text, encoding="utf-8")
    print("restored", PAGE.relative_to(ROOT))


if __name__ == "__main__":
    main()