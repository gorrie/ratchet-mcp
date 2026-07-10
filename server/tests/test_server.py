"""Tests for the MCP tool wrappers (server.py). Calls each tool against the real dataset;
the two LittleSis tools have their network client mocked. graph() lazy-loads once.
"""
from __future__ import annotations

import asyncio

import pytest

from ratchet_mcp import server


def test_graph_lazy_loads_once():
    g1 = server.graph()
    g2 = server.graph()
    assert g1 is g2 and len(g1.people) >= 100


def test_query_cohort():
    out = server.query_cohort(sector="fin", limit=5)
    assert isinstance(out, list) and len(out) <= 5


def test_get_entity_and_missing():
    assert server.get_entity("Rubin")["id"] == "Rubin"
    assert server.get_entity("NoSuchEntity") is None


def test_who_connects():
    paths = server.who_connects("Rubin", "Treasury", max_hops=3)
    assert isinstance(paths, list)


def test_find_overlap():
    assert isinstance(server.find_overlap(actors=["tap"]), list)


def test_list_plays_for():
    assert isinstance(server.list_plays_for("Rubin"), list)


def test_list_players_for():
    assert isinstance(server.list_players_for(play="vault"), list)


def test_find_in_administration():
    assert isinstance(server.find_in_administration("clinton"), list)


def test_list_and_apply_cluster():
    clusters = server.list_clusters()
    assert isinstance(clusters, list) and clusters
    res = server.apply_cluster(clusters[0]["id"])
    assert "members" in res and "cluster" in res


def test_grade_person_texts_tool():
    out = server.grade_person_texts("Rubin", backend="cues")
    assert out["person_id"] == "Rubin" and "subject" in out


def test_profile_person_tool():
    out = server.profile_person("Rubin", backend="cues")
    assert "graph" in out and "network_brokerage" in out["graph"]
    assert "revolving_door" in out["graph"]  # unblocked on the ratchet graph


def test_enrich_from_littlesis_mocked(monkeypatch):
    async def fake_search(query, limit=10):
        return [{"id": 42, "name": query}]
    monkeypatch.setattr(server, "search_entity", fake_search)
    out = asyncio.run(server.enrich_from_littlesis("rubin"))
    assert out == [{"id": 42, "name": "rubin"}]


def test_littlesis_relationships_mocked(monkeypatch):
    async def fake_rel(eid, limit=20):
        return [{"rel": "x", "id": eid}]
    monkeypatch.setattr(server, "get_relationships", fake_rel)
    out = asyncio.run(server.littlesis_relationships(7))
    assert out == [{"rel": "x", "id": 7}]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
