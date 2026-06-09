"""Data loader for the Ratchet MCP server.

Loads three JSONL files (``people.jsonl``, ``institutions.jsonl``,
``edges.jsonl``) at startup. Exposes a small ``Graph`` value-object the
query layer queries against. Read-only; no mutation after load.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _data_dir() -> Path:
    """Resolve the data directory.

    Order: ``RATCHET_DATA_DIR`` env var → ``./data`` next to this package
    → ``../data`` relative to the package (the repo layout).
    """
    env = os.environ.get("RATCHET_DATA_DIR")
    if env:
        return Path(env)
    here = Path(__file__).resolve().parent
    for candidate in (here.parent / "data", here.parent.parent / "data"):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not locate Ratchet MCP data directory. "
        "Set RATCHET_DATA_DIR or place JSONL files at server/data/."
    )


@dataclass
class Graph:
    people: dict[str, dict[str, Any]] = field(default_factory=dict)
    institutions: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[dict[str, str]] = field(default_factory=list)
    clusters: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def load(cls, data_dir: Path | None = None) -> "Graph":
        d = Path(data_dir) if data_dir else _data_dir()
        g = cls()
        clusters_path = d / "clusters.json"
        if clusters_path.exists():
            with clusters_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
            g.clusters = payload.get("clusters", [])
        with (d / "people.jsonl").open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                g.people[rec["id"]] = rec
        with (d / "institutions.jsonl").open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                g.institutions[rec["id"]] = rec
        with (d / "edges.jsonl").open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                e = json.loads(line)
                if isinstance(e, list):
                    e = {"source": e[0], "target": e[1]}
                g.edges.append(e)
        return g

    def neighbors_of(self, node_id: str) -> list[str]:
        """All node IDs adjacent to ``node_id`` (undirected)."""
        out: list[str] = []
        for e in self.edges:
            if e["source"] == node_id:
                out.append(e["target"])
            elif e["target"] == node_id:
                out.append(e["source"])
        return out

    def institutions_of(self, person_id: str) -> list[dict[str, Any]]:
        """Institutions the person is edged to (as full records)."""
        return [
            self.institutions[nid]
            for nid in self.neighbors_of(person_id)
            if nid in self.institutions
        ]

    def people_of(self, institution_id: str) -> list[dict[str, Any]]:
        """People edged to this institution."""
        return [
            self.people[nid]
            for nid in self.neighbors_of(institution_id)
            if nid in self.people
        ]

    def entity(self, entity_id: str) -> dict[str, Any] | None:
        return self.people.get(entity_id) or self.institutions.get(entity_id)
