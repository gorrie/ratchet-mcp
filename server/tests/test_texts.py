"""Tests for the texts-by-person lane (ratchet_mcp.texts).

The store + bridge half lives here; the grading engine lives in the sibling ``tradecraft`` package,
imported via the dev-layout fallback. These run OFFLINE (backend="cues", no key, no model) against a
throwaway data dir, so they assert the lane's contracts without touching the real store:

  * unknown / empty subjects return clear, non-crashing notes,
  * a populated subject is graded PER LENS and aggregated PER SUBJECT,
  * graph lenses never appear on a text-lane profile, and nothing is blended.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ratchet_mcp.data import Graph
from ratchet_mcp import texts as T

INEV = ("There is no alternative. We are on the right side of history and the future is already here; "
        "those who refuse to adapt or die will be left behind.")


def _write_data_dir(root: Path) -> Path:
    """Build a minimal but valid ratchet data dir with a texts store."""
    d = root / "data"
    d.mkdir()
    (d / "people.jsonl").write_text(
        json.dumps({"id": "TestSubj", "label": "Test Subject", "kind": "person"}) + "\n",
        encoding="utf-8")
    (d / "institutions.jsonl").write_text(
        json.dumps({"id": "Inst", "label": "An Institution", "kind": "institution"}) + "\n",
        encoding="utf-8")
    (d / "edges.jsonl").write_text("", encoding="utf-8")
    (d / "texts.jsonl").write_text(
        json.dumps({"person_id": "TestSubj", "id": "t1", "text": INEV, "date": "2020-01-01"}) + "\n"
        + json.dumps({"person_id": "TestSubj", "id": "t2", "text": INEV, "date": "2024-01-01"}) + "\n"
        + json.dumps({"person_id": "Other", "id": "z", "text": "unrelated", "date": "2021-01-01"}) + "\n",
        encoding="utf-8")
    return d


@pytest.fixture()
def data_dir(tmp_path, monkeypatch):
    d = _write_data_dir(tmp_path)
    monkeypatch.setenv("RATCHET_DATA_DIR", str(d))
    return d


def test_load_texts_filters_by_person(data_dir):
    assert len(T.load_texts()) == 3
    assert [r["id"] for r in T.load_texts("TestSubj")] == ["t1", "t2"]


def test_unknown_person_returns_error(data_dir):
    g = Graph.load(data_dir)
    out = T.grade_person_texts(g, "NobodyHere")
    assert out["error"] == "unknown person_id"


def test_person_with_no_texts_returns_note(data_dir):
    # 'Inst' is an institution, not in people — but a real person with zero stored texts:
    g = Graph.load(data_dir)
    g.people["Empty"] = {"id": "Empty", "label": "Empty Person", "kind": "person"}
    out = T.grade_person_texts(g, "Empty")
    assert out["n_texts"] == 0 and "no texts stored" in out["note"]


def test_populated_subject_graded_per_lens(data_dir):
    g = Graph.load(data_dir)
    out = T.grade_person_texts(g, "TestSubj", backend="cues")
    assert out["n_texts"] == 2
    assert out["label"] == "Test Subject"
    per_lens = out["subject"]["per_lens"]
    # the inevitability lens registers; nothing is collapsed into one score.
    assert per_lens["inevitability_framing"]["max"] > 0.0
    assert "revolving_door" not in per_lens and "network_brokerage" not in per_lens
    # per-document receipts are preserved for adjudication.
    assert len(out["documents"]) == 2
    assert out["documents"][0]["lenses"]["inevitability_framing"]["receipts"]


def test_profile_person_combined_two_lanes(data_dir):
    # The synthetic dir has no edges, so the graph lane will be quiet; assert the SHAPE: both lanes
    # present, per-lens, never blended. (Graph firing on real topology is covered in tradecraft.)
    g = Graph.load(data_dir)
    # give TestSubj some topology so the graph lane has something to read
    g.institutions["Bank"] = {"id": "Bank", "label": "Bank", "sector": "fin", "kind": "institution"}
    out = T.profile_person(g, "TestSubj", backend="cues")
    assert out["label"] == "Test Subject"
    assert "graph" in out and "text" in out and "score" not in out  # two axes, never one number
    # text lane ran on the 2 stored TestSubj texts
    assert out["n_texts"] == 2


def test_profile_person_unknown(data_dir):
    g = Graph.load(data_dir)
    assert T.profile_person(g, "Ghost")["error"] == "unknown person_id"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
