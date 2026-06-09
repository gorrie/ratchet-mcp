"""Smoke tests on the loaded dataset.

These tests run against the real ``server/data/`` JSONL files, not a
fixture — so they double as a data-integrity check (every record loads,
IDs are unique, edges reference real nodes).
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from ratchet_mcp.data import Graph

DATA = Path(os.environ.get("RATCHET_DATA_DIR") or Path(__file__).resolve().parents[2] / "server" / "data")


@pytest.fixture(scope="module")
def g() -> Graph:
    return Graph.load(DATA)


def test_load_counts(g: Graph) -> None:
    assert len(g.people) >= 100, "v2 dataset should hold ≥100 persons"
    assert len(g.institutions) >= 50
    assert len(g.edges) >= 200


def test_person_ids_unique(g: Graph) -> None:
    # Loader already keys by id; this catches duplicate IDs in the JSONL.
    with (DATA / "people.jsonl").open("r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    ids = [__import__("json").loads(line)["id"] for line in lines]
    assert len(ids) == len(set(ids)), f"Duplicate person IDs: {sorted(set(x for x in ids if ids.count(x) > 1))}"


def test_institution_ids_unique(g: Graph) -> None:
    with (DATA / "institutions.jsonl").open("r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    ids = [__import__("json").loads(line)["id"] for line in lines]
    assert len(ids) == len(set(ids))


def test_edges_reference_real_nodes(g: Graph) -> None:
    all_ids = set(g.people) | set(g.institutions)
    for e in g.edges:
        assert e["source"] in all_ids, f"Edge source not in dataset: {e}"
        assert e["target"] in all_ids, f"Edge target not in dataset: {e}"


def test_every_person_has_role(g: Graph) -> None:
    missing = [p["id"] for p in g.people.values() if not p.get("role")]
    assert not missing, f"Persons missing role: {missing}"
