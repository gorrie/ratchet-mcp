"""Regenerate the inline data arrays inside the website's graph.js from
the JSONL source of truth at server/data/.

The website's Revolving Door page (evilrobots.lol/tech/revolving-door/)
serves a single graph.js file that declares an Alpine.js component:

    function revolvingDoorGraph() {
      return {
        institutions: [ ... ],
        people:       [ ... ],
        links:        [ ... ],
        // ...interactive component methods follow...
      };
    }

We rewrite those three array literals only. The surrounding component
methods are preserved.

After running, preview with hugo (any platform):
    cd evil-robots-series/website
    hugo server --buildFuture
to visually verify the foreign-cluster nodes appear in the right color
group and that no existing nodes were lost.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Website-bridge script: needs the evil-robots-series working copy (the public
# standalone ratchet-mcp repo has no website/ tree). SERIES_ROOT overrides;
# otherwise resolve the series root from this script's location (ratchet-mcp is
# at <series>/research/ratchet-mcp/, so parents[2] is the series dir).
_here = Path(__file__).resolve()
SERIES = Path(os.environ["SERIES_ROOT"]) if os.environ.get("SERIES_ROOT") else _here.parents[2]
GRAPH_JS = SERIES / "website" / "static" / "tech" / "revolving-door" / "graph.js"
DATA = _here.parents[1] / "server" / "data"

# Fields we emit inline. Other fields (kind, accessed dates, etc.) are
# carried in the JSONL but not needed by the web viewer.
INST_FIELDS = ("id", "label", "sector", "sources")
PERSON_FIELDS = (
    "id", "label", "sector", "admin", "networks", "plays", "actors",
    "role", "sources",
)


def js_literal(value) -> str:
    """Emit a JSON-compatible-but-readable JS literal."""
    return json.dumps(value, ensure_ascii=False)


def emit_array(records: list[dict], fields: tuple[str, ...], indent: int = 6) -> str:
    """Render a JS array of object literals, one record per line."""
    pad = " " * indent
    lines = ["["]
    for rec in records:
        parts = []
        for f in fields:
            if f not in rec or rec[f] is None:
                continue
            v = rec[f]
            # Skip empty arrays — keeps the inline literal compact.
            if isinstance(v, list) and not v:
                continue
            parts.append(f"{f}:{js_literal(v)}")
        lines.append(f"{pad}{{{', '.join(parts)}}},")
    lines.append(f"{' ' * (indent - 4)}]")
    return "\n".join(lines)


def emit_links(edges: list[dict], indent: int = 6) -> str:
    """Links are emitted as [source, target] tuples — the form the
    website's D3 code destructures. ``influence_type`` metadata stays in
    JSONL for downstream consumers (MCP server, docker viewer) but is
    not surfaced in the legacy inline form.
    """
    pad = " " * indent
    lines = ["["]
    for e in edges:
        if isinstance(e, list):
            src, tgt = e[0], e[1]
        else:
            src = e.get("source")
            tgt = e.get("target")
        lines.append(f"{pad}[{js_literal(src)}, {js_literal(tgt)}],")
    lines.append(f"{' ' * (indent - 4)}]")
    return "\n".join(lines)


def replace_array(text: str, marker: str, new_value: str) -> str:
    """Find ``<marker>: [...]`` in text and replace the array literal.

    Uses balanced-bracket matching so nested arrays/objects don't break it.
    """
    m = re.search(rf"\b{re.escape(marker)}\s*:\s*\[", text)
    if not m:
        raise RuntimeError(f"marker {marker!r} not found in graph.js")
    start = m.end() - 1  # position of opening '['
    depth = 0
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
                return text[:start] + new_value + text[end:]
        i += 1
    raise RuntimeError(f"unterminated array for {marker!r}")


def read_jsonl(path: Path) -> list[dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def main() -> int:
    institutions = read_jsonl(DATA / "institutions.jsonl")
    people = read_jsonl(DATA / "people.jsonl")
    edges = read_jsonl(DATA / "edges.jsonl")

    text = GRAPH_JS.read_text(encoding="utf-8")
    text = replace_array(text, "institutions", emit_array(institutions, INST_FIELDS))
    text = replace_array(text, "people", emit_array(people, PERSON_FIELDS))
    text = replace_array(text, "links", emit_links(edges))

    GRAPH_JS.write_text(text, encoding="utf-8")
    print(f"Updated {GRAPH_JS.relative_to(WORKSPACE)}")
    print(f"  {len(institutions)} institutions, {len(people)} people, {len(edges)} edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
