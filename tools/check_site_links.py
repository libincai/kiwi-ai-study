"""Verify GitHub Pages + local dev link prerequisites for public HTML."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"local", "templates", "tools", "docs", "scripts", ".cursor", ".github", "pagefind", "node_modules"}
SKIP_STUB_SLUGS = {"math", "ai", "about", "contact", "books", "legal", "assets", "data", "docs", "local", "pagefind", "templates", "tools"}

ROOT_HREF = re.compile(
    r"""href\s*=\s*["']/([a-z0-9][\w./-]*)""",
    re.I,
)
SITE_BASE = "kiwi-site-base.js"
BREADCRUMB = "drive-breadcrumb.js"


def load_slug_set() -> set[str]:
    spec = importlib.util.spec_from_file_location(
        "gen", ROOT / "tools" / "generate-serve-rewrites.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    out: set[str] = set()
    for rule in mod.collect_slug_rewrites():
        src = rule["source"]
        if src in ("/math", "/"):
            continue
        out.add(src.lstrip("/"))
    return out


def is_github_redirect_stub(path: Path, stub_slugs: set[str]) -> bool:
    if path.name != "index.html":
        return False
    try:
        rel_parts = path.relative_to(ROOT).parts
    except ValueError:
        return False
    if len(rel_parts) != 2 or rel_parts[1] != "index.html":
        return False
    if rel_parts[0] not in stub_slugs:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return "data-pagefind-ignore" in text and "http-equiv=\"refresh\"" in text


def iter_public_html(stub_slugs: set[str]) -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith("_"):
            continue
        if is_github_redirect_stub(path, stub_slugs):
            continue
        paths.append(path)
    return sorted(paths)


def needs_site_base(text: str) -> bool:
    if BREADCRUMB in text:
        return True
    for m in ROOT_HREF.finditer(text):
        first = m.group(1).split("/")[0]
        if first in ("assets", "pagefind", "legal"):
            continue
        return True
    return False


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    slugs = load_slug_set()
    manifest_path = ROOT / "tools" / "github-pages-stubs.json"
    if manifest_path.is_file():
        stub_slugs = set(json.loads(manifest_path.read_text(encoding="utf-8")))
    else:
        stub_slugs = set()
        warnings.append("missing tools/github-pages-stubs.json — run generate-serve-rewrites.py")

    need_stub = {s for s in slugs if s not in SKIP_STUB_SLUGS}
    missing_stubs = need_stub - stub_slugs
    extra_stubs = stub_slugs - need_stub
    for slug in sorted(missing_stubs):
        errors.append(f"GitHub stub missing: {slug}/index.html")
    for slug in sorted(extra_stubs):
        warnings.append(f"stale stub folder (not in slug list): {slug}")

    for slug in need_stub:
        idx = ROOT / slug / "index.html"
        if not idx.is_file():
            errors.append(f"stub file missing on disk: {slug}/index.html")
    for section in ("about", "contact", "books", "ai", "math"):
        idx = ROOT / section / "index.html"
        if section in slugs or section == "math":
            if not idx.is_file():
                errors.append(f"section index missing: {section}/index.html")

    nojekyll = ROOT / ".nojekyll"
    if not nojekyll.is_file():
        warnings.append("missing .nojekyll at repo root")

    missing_base: list[str] = []
    for path in iter_public_html(stub_slugs):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not needs_site_base(text):
            continue
        if SITE_BASE not in text:
            rel = path.relative_to(ROOT).as_posix()
            missing_base.append(rel)

    for rel in sorted(missing_base):
        errors.append(f"root-absolute links or breadcrumb but no {SITE_BASE}: {rel}")

    for line in warnings:
        print("WARN:", line)
    for line in errors:
        print("ERROR:", line)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(
        f"OK — {len(need_stub)} GitHub stubs, "
        f"{len(iter_public_html(stub_slugs))} public HTML files checked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())