#!/usr/bin/env python3
"""Recover a file's latest Write payload from agent transcript jsonl."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: extract-file-from-transcript.py <transcript.jsonl> <relative-path>")
        return 1
    transcript = Path(sys.argv[1])
    target_suffix = sys.argv[2].replace("\\", "/").lower()
    content: str | None = None
    with transcript.open(encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("role") != "assistant":
                continue
            msg = row.get("message", {})
            for part in msg.get("content", []):
                if part.get("type") != "tool_use":
                    continue
                inp = part.get("input") or {}
                path = (inp.get("path") or "").replace("\\", "/").lower()
                if target_suffix not in path:
                    continue
                if "contents" in inp:
                    content = inp["contents"]
                elif "new_string" in inp and inp.get("path", "").lower().endswith(
                    target_suffix.split("/")[-1]
                ):
                    pass  # patches only; keep last full write
    if content is None:
        print("No Write found", file=sys.stderr)
        return 2
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    if out:
        out.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {len(content)} chars to {out}")
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
