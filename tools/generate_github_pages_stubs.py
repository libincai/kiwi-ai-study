"""Generate clean-URL index stubs at repo root for GitHub project Pages.

Local dev uses serve.json; GitHub Pages needs ``{slug}/index.html`` stubs that
redirect to the real HTML under math/, ai/, etc.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
import importlib.util

_TOOLS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "generate_serve_rewrites",
    _TOOLS / "generate-serve-rewrites.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
SKIP_MATH = _mod.SKIP_MATH
collect_slug_rewrites = _mod.collect_slug_rewrites

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "github-pages-stubs.json"
SITE_BASE_JS = ROOT / "assets" / "js" / "kiwi-site-base.js"
DEST_BEGIN = "/* KIWI_GITHUB_SLUG_DEST_BEGIN */"
DEST_END = "/* KIWI_GITHUB_SLUG_DEST_END */"

SKIP_STUB_DIRS = {
    "math",
    "ai",
    "about",
    "contact",
    "books",
    "legal",
    "assets",
    "data",
    "docs",
    "local",
    "pagefind",
    "templates",
    "tools",
}

STUB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>
(function(){{
  var p={dest_json};
  if((location.hostname||"").toLowerCase().slice(-12)===".github.io") p="/{site_prefix}"+p;
  location.replace(p);
}})();
</script>
<meta http-equiv="refresh" content="0;url={dest}">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Redirecting…</title>
<style>body{{margin:0;background:#fff}}</style>
</head>
<body data-pagefind-ignore="all">
<noscript><p><a href="{dest}">Continue</a></p></noscript>
</body>
</html>
"""

SITE_PREFIX = "kiwi-ai-study"

_SLUG_RE = re.compile(r"^/([a-z0-9][\w-]*)$", re.I)


def slug_from_source(source: str) -> str | None:
    if source == "/math":
        return None
    m = _SLUG_RE.match(source)
    return m.group(1) if m else None


def collect_stub_targets() -> dict[str, str]:
    """Map slug -> repo-root path (e.g. /math/foo.html) for stubs + site-base."""
    out: dict[str, str] = {}
    for rule in collect_slug_rewrites():
        slug = slug_from_source(rule["source"])
        if not slug or slug in SKIP_MATH or slug in SKIP_STUB_DIRS:
            continue
        dest = rule["destination"]
        if not dest.startswith("/"):
            continue
        out[slug] = dest
    return out


def write_slug_map_into_site_base(targets: dict[str, str]) -> None:
    """Embed slug -> .html map for in-site links on GitHub Pages (skip stub hop)."""
    if not SITE_BASE_JS.is_file():
        return
    text = SITE_BASE_JS.read_text(encoding="utf-8")
    payload = "window.KIWI_GITHUB_SLUG_DEST=" + json.dumps(
        targets, ensure_ascii=True, sort_keys=True
    ) + ";"
    block = f"{DEST_BEGIN}\n  {payload}\n  {DEST_END}"
    if DEST_BEGIN not in text or DEST_END not in text:
        print("warn: kiwi-site-base.js missing slug dest markers", file=__import__("sys").stderr)
        return
    text = re.sub(
        rf"{re.escape(DEST_BEGIN)}.*?{re.escape(DEST_END)}",
        block,
        text,
        count=1,
        flags=re.S,
    )
    SITE_BASE_JS.write_text(text, encoding="utf-8", newline="\n")


def write_stub(slug: str, dest: str) -> None:
    folder = ROOT / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(
        STUB_TEMPLATE.format(
            dest=dest,
            dest_json=json.dumps(dest),
            site_prefix=SITE_PREFIX,
        ),
        encoding="utf-8",
        newline="\n",
    )


def remove_obsolete_stubs(keep: set[str]) -> None:
    if not MANIFEST.is_file():
        return
    prev = set(json.loads(MANIFEST.read_text(encoding="utf-8")))
    for slug in prev - keep:
        if slug in SKIP_STUB_DIRS:
            continue
        folder = ROOT / slug
        if folder.is_dir() and (folder / "index.html").is_file():
            try:
                only_stub = all(
                    p.name == "index.html" or p.is_dir() for p in folder.iterdir()
                )
            except OSError:
                only_stub = False
            if only_stub:
                shutil.rmtree(folder)


def main() -> None:
    targets = collect_stub_targets()
    for slug, dest in sorted(targets.items()):
        write_stub(slug, dest)
    write_slug_map_into_site_base(targets)
    remove_obsolete_stubs(set(targets))
    MANIFEST.write_text(
        json.dumps(sorted(targets), indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / ".nojekyll").touch(exist_ok=True)
    print(
        "wrote",
        len(targets),
        "GitHub Pages stubs (slug/index.html); manifest",
        MANIFEST.relative_to(ROOT),
    )


if __name__ == "__main__":
    main()