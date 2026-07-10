"""Targeted tests closing the remaining coverage gaps in data / queries / texts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from ratchet_mcp import data, queries, texts
from ratchet_mcp.data import Graph


# ---- data.py ---------------------------------------------------------------------------------

def test_data_dir_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("RATCHET_DATA_DIR", str(tmp_path))
    assert data._data_dir() == tmp_path


def test_data_dir_not_found(monkeypatch, tmp_path):
    monkeypatch.delenv("RATCHET_DATA_DIR", raising=False)
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    monkeypatch.setattr(data, "__file__", str(pkg / "mod.py"))
    with pytest.raises(FileNotFoundError):
        data._data_dir()


def test_load_blanklines_listedge_and_helpers(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    (d / "people.jsonl").write_text("\n" + json.dumps({"id": "P", "sector": "fin", "kind": "person"}) + "\n",
                                    encoding="utf-8")
    (d / "institutions.jsonl").write_text("\n" + json.dumps({"id": "I", "sector": "gov", "kind": "institution"}) + "\n",
                                          encoding="utf-8")
    (d / "edges.jsonl").write_text('\n["P", "I"]\n', encoding="utf-8")  # blank line + list-form edge
    g = Graph.load(d)
    assert g.neighbors_of("I") == ["P"]          # target-direction branch
    assert [r["id"] for r in g.institutions_of("P")] == ["I"]
    assert [r["id"] for r in g.people_of("I")] == ["P"]
    assert g.entity("P")["id"] == "P" and g.entity("nope") is None


# ---- queries.py ------------------------------------------------------------------------------

def _toy_graph():
    g = Graph()
    g.people = {k: {"id": k, "sector": "x", "plays": ["pp"], "actors": ["aa"], "admin": ["clinton"]}
                for k in ["A", "B", "C", "D", "E", "Z"]}
    g.edges = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"},
               {"source": "C", "target": "D"}, {"source": "D", "target": "E"}]
    return g


def test_matches_person_str_want_negative():
    g = _toy_graph()
    assert queries.query_cohort(g, sector="nonexistent") == []          # str want not in have
    assert queries.query_cohort(g, network=["zzz"]) == []               # list want, no intersection
    assert len(queries.query_cohort(g, play=["pp"])) == 6               # list want intersects


def test_who_connects_branches():
    g = _toy_graph()
    assert queries.who_connects(g, "Ghost", "A") == []                  # a missing
    assert queries.who_connects(g, "A", "Ghost") == []                  # b missing
    assert queries.who_connects(g, "A", "A") == [["A"]]                 # a == b
    assert queries.who_connects(g, "A", "D", max_hops=4) == [["A", "B", "C", "D"]]
    assert queries.who_connects(g, "A", "Z", max_hops=10) == []         # no path -> frontier dries up
    assert queries.who_connects(g, "A", "E", max_hops=2) == []          # b beyond max_hops -> loop exhausts


def test_list_players_for_requires_exactly_one():
    g = _toy_graph()
    with pytest.raises(ValueError):
        queries.list_players_for(g)
    with pytest.raises(ValueError):
        queries.list_players_for(g, play="pp", actor="aa")
    assert len(queries.list_players_for(g, actor="aa")) == 6


def test_apply_cluster_paths():
    g = _toy_graph()
    g.clusters = [
        {"id": "c1", "label": "L", "query": {"tool": "query_cohort", "args": {"sector": "x"}},
         "filter_sector": "x"},
        {"id": "c2", "query": {"tool": "find_overlap", "args": {"plays": ["pp"]}}, "filter_ids": ["A"]},
        {"id": "c3", "query": {"tool": "badtool"}},
    ]
    assert queries.apply_cluster(g, "c1")["member_count"] == 6          # query_cohort + filter_sector
    r2 = queries.apply_cluster(g, "c2")
    assert [m["id"] for m in r2["members"]] == ["A"]                    # find_overlap + filter_ids
    assert "error" in queries.apply_cluster(g, "c3")                    # unsupported tool
    assert "error" in queries.apply_cluster(g, "ghost")                # unknown id


# ---- texts.py --------------------------------------------------------------------------------

def test_load_texts_missing_store(monkeypatch, tmp_path):
    monkeypatch.setenv("RATCHET_DATA_DIR", str(tmp_path))  # no texts.jsonl here
    assert texts.load_texts() == []


def test_load_texts_skips_blank_lines(monkeypatch, tmp_path):
    monkeypatch.setenv("RATCHET_DATA_DIR", str(tmp_path))
    (tmp_path / "texts.jsonl").write_text("\n" + json.dumps({"person_id": "P", "text": "x"}) + "\n",
                                          encoding="utf-8")
    assert len(texts.load_texts("P")) == 1


def test_import_tradecraft_env_path(monkeypatch):
    # Force the first import to fail (fresh) so the TRADECRAFT_PATH branch runs, then recover.
    real = str(Path(texts.__file__).resolve().parents[4] / "tradecraft")
    for m in ("tradecraft", "tradecraft.loader", "tradecraft.subject"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    monkeypatch.setattr(sys, "path", [p for p in sys.path if p != real])
    monkeypatch.setenv("TRADECRAFT_PATH", real)
    load_lenses, grade_person, text_lenses = texts._import_tradecraft()
    assert callable(load_lenses) and callable(grade_person) and callable(text_lenses)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
