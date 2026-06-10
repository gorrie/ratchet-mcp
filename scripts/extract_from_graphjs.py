#!/usr/bin/env python3
"""Extract people / institutions / edges from website/static/tech/revolving-door/graph.js
into JSONL files under research/ratchet-mcp/server/data/.

The graph.js file is the Alpine.js Revolving Door component. It carries the
canonical dataset inline. We parse it via a lenient JS-to-Python conversion
(strip JS-specific syntax, eval as Python) — works because the dataset is
all literals (strings, arrays, dicts).

Run from anywhere; paths are absolute.
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path

# Website-bridge script: needs the evil-robots-series working copy (the public
# standalone ratchet-mcp repo has no website/ tree). Resolve the series root
# from EUREKA_WORKSPACE, else from this script's location — ratchet-mcp lives at
# <series>/research/ratchet-mcp/, so parents[2] is the series dir. No hard-coded
# user paths; runs on any host that has the working copy.
_here = Path(__file__).resolve()
SERIES = Path(os.environ["EUREKA_WORKSPACE"]) if os.environ.get("EUREKA_WORKSPACE") else _here.parents[2]
GRAPH_JS = SERIES / "website" / "static" / "tech" / "revolving-door" / "graph.js"
OUT_DIR = _here.parents[1] / "server" / "data"


def js_array_to_py(text: str, marker: str) -> list:
    """Find an array literal after `<marker>:` and return it as Python.

    Looks for the pattern `<marker>:\\s*\\[` then balanced-bracket-matches
    until the closing bracket. Then JS→Python translation:
      - `'foo'` → `"foo"` (use json-compatible double quotes)
      - bare keys like `id:` → `"id":`
      - trailing commas before `]` or `}` → remove
    """
    m = re.search(rf"\b{re.escape(marker)}\s*:\s*\[", text)
    if not m:
        raise RuntimeError(f"marker {marker!r} not found")
    start = m.end() - 1  # the opening '['
    depth = 0
    end = None
    in_str = None
    i = start
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_str = ch
            i += 1
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    if end is None:
        raise RuntimeError(f"unterminated array for {marker!r}")
    js_lit = text[start:end]

    # Convert JS literal to Python literal.
    # 1) JS single-quoted strings → Python double-quoted (preserve embedded chars
    #    safely by walking the string).
    py = []
    j = 0
    in_str = None
    while j < len(js_lit):
        c = js_lit[j]
        if in_str:
            if c == "\\":
                py.append(c)
                py.append(js_lit[j + 1])
                j += 2
                continue
            if c == in_str:
                py.append('"')
                in_str = None
                j += 1
                continue
            if c == '"':
                py.append('\\"')
                j += 1
                continue
            py.append(c)
            j += 1
            continue
        if c == "'":
            py.append('"')
            in_str = "'"
            j += 1
            continue
        if c == '"':
            py.append(c)
            in_str = '"'
            j += 1
            continue
        py.append(c)
        j += 1
    py_text = "".join(py)

    # 2) Bare keys: `id:` → `"id":`. Match identifier followed by colon
    #    that isn't already preceded by a quote.
    py_text = re.sub(r"(?<![\"\w])([A-Za-z_][A-Za-z0-9_]*)\s*:", r'"\1":', py_text)

    # 3) Trailing commas before `]` or `}`.
    py_text = re.sub(r",(\s*[}\]])", r"\1", py_text)

    # 4) Comments (// ...) — strip whole-line comments.
    py_text = re.sub(r"//[^\n]*", "", py_text)

    decoder = json.JSONDecoder(strict=False)
    obj, end = decoder.raw_decode(py_text)
    return obj


def extract_edges(text: str) -> list[list[str]]:
    """Edges are an array of [source, target] arrays."""
    return js_array_to_py(text, "links")


def main() -> int:
    text = GRAPH_JS.read_text(encoding="utf-8")
    institutions = js_array_to_py(text, "institutions")
    people = js_array_to_py(text, "people")
    edges = extract_edges(text)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write JSONL: one record per line, deterministic key order.
    with (OUT_DIR / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions:
            rec["kind"] = "institution"
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    with (OUT_DIR / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people:
            rec["kind"] = "person"
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    with (OUT_DIR / "edges.jsonl").open("w", encoding="utf-8") as f:
        for edge in edges:
            f.write(json.dumps(edge) + "\n")

    print(f"Wrote {len(institutions)} institutions, {len(people)} people, {len(edges)} edges")
    print(f"to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
