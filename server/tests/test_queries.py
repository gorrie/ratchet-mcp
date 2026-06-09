"""Unit tests for the query primitives.

Use the real dataset (not a synthetic fixture) so the assertions also
catch dataset regressions.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from ratchet_mcp import queries
from ratchet_mcp.data import Graph

DATA = Path(os.environ.get("RATCHET_DATA_DIR") or Path(__file__).resolve().parents[2] / "server" / "data")


@pytest.fixture(scope="module")
def g() -> Graph:
    return Graph.load(DATA)


def test_query_cohort_no_filters_returns_all(g: Graph) -> None:
    assert len(queries.query_cohort(g, limit=1000)) == len(g.people)


def test_query_cohort_filters_intersect(g: Graph) -> None:
    treasury = queries.query_cohort(g, sector="fin", play="vault")
    assert all("vault" in p["plays"] for p in treasury)
    assert all(p["sector"] == "fin" for p in treasury)


def test_get_entity_returns_person_with_edges(g: Graph) -> None:
    rec = queries.get_entity(g, "Rubin")
    if rec is None:
        pytest.skip("Rubin not in current dataset")
    assert rec["id"] == "Rubin"
    assert "edges" in rec
    assert isinstance(rec["edges"], list)


def test_get_entity_missing_returns_none(g: Graph) -> None:
    assert queries.get_entity(g, "NotAReal_PersonID") is None


def test_who_connects_finds_path(g: Graph) -> None:
    # Rubin should connect to Treasury via a 1-hop edge.
    paths = queries.who_connects(g, "Rubin", "Treasury", max_hops=2)
    if not paths:
        pytest.skip("Rubin or Treasury missing")
    assert any(len(p) <= 2 for p in paths)


def test_find_overlap_tap_backdoor(g: Graph) -> None:
    """The headline thesis prompt: same persons touch tap AND backdoor."""
    hits = queries.find_overlap(g, actors=["tap", "backdoor"])
    # The book argues this returns a small concentrated set (Hayden,
    # Cheney, Bolton level). Allow flexibility but verify it's not empty
    # if those actors exist in the dataset.
    has_tap = any("tap" in (p.get("actors") or []) for p in g.people.values())
    has_backdoor = any("backdoor" in (p.get("actors") or []) for p in g.people.values())
    if has_tap and has_backdoor:
        assert hits, "Expected overlap of tap and backdoor to be non-empty"


def test_list_plays_for_returns_list(g: Graph) -> None:
    sample = next(iter(g.people.values()))
    plays = queries.list_plays_for(g, sample["id"])
    assert isinstance(plays, list)


def test_list_players_for_requires_one_arg(g: Graph) -> None:
    with pytest.raises(ValueError):
        queries.list_players_for(g, play="vault", actor="money")
    with pytest.raises(ValueError):
        queries.list_players_for(g)


def test_find_in_administration_filter(g: Graph) -> None:
    rec = queries.find_in_administration(g, "clinton")
    assert all("clinton" in (p.get("admin") or []) for p in rec)


def test_list_clusters(g: Graph) -> None:
    clusters = queries.list_clusters(g)
    assert isinstance(clusters, list)
    if clusters:
        for c in clusters:
            assert "id" in c and "label" in c and "summary" in c


def test_apply_cluster_unknown(g: Graph) -> None:
    out = queries.apply_cluster(g, "not-a-real-cluster")
    assert "error" in out


def test_apply_cluster_known(g: Graph) -> None:
    """If clusters exist, apply_cluster should return members for at least one."""
    if not g.clusters:
        pytest.skip("No clusters defined")
    cid = g.clusters[0]["id"]
    out = queries.apply_cluster(g, cid)
    assert "cluster" in out
    assert "members" in out
    assert isinstance(out["members"], list)
    assert out["member_count"] == len(out["members"])
