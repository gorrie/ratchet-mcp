"""Integrity tests on the SYNC OUTPUT (website graph.js), not just the JSONL.

``test_data.py`` proves the source JSONL is well-formed. This file proves the
generated ``website/static/tech/revolving-door/graph.js`` still faithfully
reflects it after ``sync_jsonl_to_graphjs.py`` runs — the guard that was
missing when a re-sync silently rewrote the node arrays.

The failure mode these tests catch:
  * a JSONL node dropped from graph.js on re-sync (node DROP),
  * an edge whose endpoint no longer resolves to any node (ORPHAN),
  * edge-count drift between the dataset and the rendered graph.

The runtime already filters unresolvable edges at draw time
(``links.filter(([s,t]) => nodeIds.has(s) && nodeIds.has(t))``), so an orphan
is a silent data loss, not a crash — exactly the kind of thing a test, not a
render, has to catch.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

# .../research/ratchet-mcp/server/tests/test_graph_sync.py
#   parents[2] = ratchet-mcp   parents[4] = series-workspace
_HERE = Path(__file__).resolve()
DATA = Path(os.environ.get("RATCHET_DATA_DIR") or _HERE.parents[2] / "server" / "data")
SERIES = Path(os.environ.get("SERIES_ROOT") or _HERE.parents[4])
GRAPH_JS = SERIES / "website" / "static" / "tech" / "revolving-door" / "graph.js"
OVERLAY = SERIES / "website" / "data" / "research-entities.json"


def _jsonl_ids(name: str) -> set[str]:
    path = DATA / name
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            ids.add(json.loads(line)["id"])
    return ids


def _jsonl_edge_count() -> int:
    return sum(
        1 for line in (DATA / "edges.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
    )


@pytest.fixture(scope="module")
def gj() -> str:
    if not GRAPH_JS.exists():
        pytest.skip(f"graph.js not found at {GRAPH_JS}")
    return GRAPH_JS.read_text(encoding="utf-8")


def _base_node_ids(gj: str) -> set[str]:
    return set(re.findall(r'\bid:\s*"([^"]+)"', gj))


def _links(gj: str) -> list[tuple[str, str]]:
    # isolate ONLY the `links: [ ... ]` array, not every 2-string array
    start = gj.index("links: [") + len("links: ")
    depth = 0
    for j in range(start, len(gj)):
        if gj[j] == "[":
            depth += 1
        elif gj[j] == "]":
            depth -= 1
            if depth == 0:
                break
    block = gj[start : j + 1]
    return re.findall(r'\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', block)


def _overlay_ids() -> set[str]:
    if not OVERLAY.exists():
        return set()
    data = json.loads(OVERLAY.read_text(encoding="utf-8"))
    ents = data if isinstance(data, list) else data.get("entities") or data.get("nodes") or []
    ids: set[str] = set()
    for e in ents:
        if isinstance(e, dict):
            for k in ("id", "slug", "name"):
                if e.get(k):
                    ids.add(e[k])
    return ids


def test_no_jsonl_node_dropped(gj: str) -> None:
    """Every dataset node must appear in the synced graph.js (anti-DROP guard)."""
    dataset = _jsonl_ids("people.jsonl") | _jsonl_ids("institutions.jsonl")
    base = _base_node_ids(gj)
    dropped = sorted(dataset - base)
    assert not dropped, f"{len(dropped)} JSONL nodes missing from graph.js: {dropped[:20]}"


def test_edge_count_parity(gj: str) -> None:
    """The rendered links array should carry every dataset edge."""
    assert len(_links(gj)) == _jsonl_edge_count()


def test_no_orphaned_edges(gj: str) -> None:
    """Every edge endpoint must resolve to a base node or an overlay node."""
    universe = _base_node_ids(gj) | _overlay_ids()
    orphans = [(a, b) for a, b in _links(gj) if a not in universe or b not in universe]
    assert not orphans, f"{len(orphans)} orphaned edges, e.g. {orphans[:10]}"
