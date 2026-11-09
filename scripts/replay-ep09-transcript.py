#!/usr/bin/env python3
"""Replay transcript Write/StrReplace ops for ai/episode-09.html."""

from __future__ import annotations

import json
import sys
from pathlib import Path

EP = "episode-09.html"
transcript = Path(
    r"C:\Users\yyuan\.cursor\projects\d-YuanSync-Mirror-MyAI-kiwi-ai-study"
    r"\agent-transcripts\f4a37644-c102-4e14-b2a6-4eea47b63f84"
    r"\f4a37644-c102-4e14-b2a6-4eea47b63f84.jsonl"
)
out = Path(r"d:\YuanSync\Mirror\MyAI\kiwi-ai-study\ai\episode-09.html")

content: str | None = None
applied = 0

with transcript.open(encoding="utf-8") as f:
    for line in f:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("role") != "assistant":
            continue
        for part in row.get("message", {}).get("content", []):
            if part.get("type") != "tool_use":
                continue
            inp = part.get("input")
            if not isinstance(inp, dict):
                continue
            path = (inp.get("path") or "").replace("\\", "/")
            if not path.lower().endswith(EP):
                continue
            if "contents" in inp:
                content = inp["contents"]
                applied += 1
            elif content is not None and "old_string" in inp and "new_string" in inp:
                old, new = inp["old_string"], inp["new_string"]
                if old in content:
                    content = content.replace(old, new, 1)
                    applied += 1

if content is None:
    print("No content recovered", file=sys.stderr)
    sys.exit(1)

out.write_text(content, encoding="utf-8", newline="\n")
print(f"Replayed {applied} ops -> {out} ({len(content)} chars)")
