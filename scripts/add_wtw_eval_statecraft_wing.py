"""Add the Watching-the-Watchers eval/statecraft-wing people to the Ratchet graph.

Five subjects already carry web profiles on evilrobots.lol but were not in people.jsonl, so
grade_person_texts could not run on them. This adds them (with >=2 sources, closed-vocab tags,
positions-only role text) plus the institutions and edges they need. Idempotent: skips any id that
already exists. No characterizations in role/tags (defamation discipline, docs/CITATIONS.md).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PEOPLE = DATA / "people.jsonl"
INST = DATA / "institutions.jsonl"
EDGES = DATA / "edges.jsonl"

INSTITUTIONS = [
    {"id": "GraySwan", "label": "Gray Swan AI", "sector": "tech",
     "sources": [{"type": "official", "url": "https://www.grayswan.ai/about"}], "kind": "institution"},
    {"id": "METR", "label": "METR (Model Evaluation & Threat Research)", "sector": "tank",
     "sources": [{"type": "official", "url": "https://metr.org/about"}], "kind": "institution"},
    {"id": "ARC", "label": "Alignment Research Center", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.alignment.org/"}], "kind": "institution"},
    {"id": "RethinkPriorities", "label": "Rethink Priorities", "sector": "tank",
     "sources": [{"type": "official", "url": "https://rethinkpriorities.org/"}], "kind": "institution"},
    {"id": "CMU", "label": "Carnegie Mellon University", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.cmu.edu/"}], "kind": "institution"},
    {"id": "Airbnb", "label": "Airbnb", "sector": "tech",
     "sources": [{"type": "official", "url": "https://news.airbnb.com/"}], "kind": "institution"},
    {"id": "ACLU", "label": "American Civil Liberties Union", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.aclu.org/"}], "kind": "institution"},
    {"id": "StateDept", "label": "U.S. Department of State", "sector": "gov",
     "sources": [{"type": "official", "url": "https://www.state.gov/"}], "kind": "institution"},
]

PEOPLE_RECS = [
    {"id": "Kolter", "label": "Zico Kolter", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Carnegie Mellon ML Department head -> Gray Swan AI co-founder & Chief Scientist -> "
             "OpenAI Board of Directors & Safety and Security Committee chair 2024-",
     "sources": [
         {"type": "official", "url": "https://openai.com/index/zico-kolter-joins-openais-board-of-directors/"},
         {"type": "official", "url": "https://www.grayswan.ai/about"},
         {"type": "paper", "url": "https://arxiv.org/abs/2307.15043"}]},
    {"id": "BBarnes", "label": "Beth Barnes", "kind": "person", "sector": "tank",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "OpenAI alignment research -> ARC Evals lead -> METR founder & CEO 2023-",
     "sources": [
         {"type": "official", "url": "https://metr.org/about"},
         {"type": "official", "url": "https://metr.org/blog/2023-09-19-spin-out-announcement/"}]},
    {"id": "Hobbhahn", "label": "Marius Hobbhahn", "kind": "person", "sector": "tank",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "University of Tubingen ML PhD -> Apollo Research co-founder & CEO 2023-",
     "sources": [
         {"type": "official", "url": "https://www.apolloresearch.ai/team"},
         {"type": "announcement", "url": "https://forum.effectivealtruism.org/posts/ysC6crBKhDBGZfob3/announcing-apollo-research"}]},
    {"id": "Makanju", "label": "Anna Makanju", "kind": "person", "sector": "gov",
     "admin": ["obama", "biden"], "networks": [], "plays": ["pulpit"], "actors": ["eagle"],
     "role": "US Department of Defense -> State Department -> NSC Director for Russia -> "
             "special adviser to VP Biden -> Facebook global elections policy 2018 -> "
             "OpenAI VP Global Affairs -> VP Global Impact 2024-",
     "sources": [
         {"type": "press", "url": "https://www.fastcompany.com/90948225/how-anna-makanju-orchestrated-openais-political-charm-offensive"},
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Anna_Makanju"}]},
    {"id": "Downs", "label": "Juniper Downs", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["flagging"],
     "role": "ACLU of Northern California attorney -> Google content policy 2012 -> "
             "YouTube Director of Public Policy -> Google Global Director of Policy -> "
             "Airbnb Global Head of Community Policy 2021-",
     "sources": [
         {"type": "official", "url": "https://fosi.org/people/juniper-downs/"},
         {"type": "official", "url": "https://news.airbnb.com/juniper-downs-joins-airbnb-as-global-head-of-community-policy-partnership/"},
         {"type": "gov", "url": "https://docs.house.gov/meetings/JU/JU00/20180717/108546/HHRG-115-JU00-Wstate-DownsJ-20180717.pdf"}]},
]

EDGE_RECS = [
    ("Kolter", "OpenAI"), ("Kolter", "GraySwan"), ("Kolter", "CMU"),
    ("BBarnes", "METR"), ("BBarnes", "OpenAI"), ("BBarnes", "ARC"),
    ("Hobbhahn", "Apollo"), ("Hobbhahn", "RethinkPriorities"),
    ("Makanju", "OpenAI"), ("Makanju", "Meta"), ("Makanju", "NSC"),
    ("Makanju", "StateDept"), ("Makanju", "DoD"),
    ("Downs", "Google"), ("Downs", "YouTube"), ("Downs", "Airbnb"), ("Downs", "ACLU"),
]


def _ids(path):
    out = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.add(json.loads(line)["id"])
    return out


def _edge_set():
    out = set()
    if EDGES.exists():
        for line in EDGES.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                e = json.loads(line)
                out.add((e["source"], e["target"]))
    return out


def main():
    have = _ids(PEOPLE) | _ids(INST)
    added_i = added_p = added_e = 0
    with INST.open("a", encoding="utf-8") as fh:
        for rec in INSTITUTIONS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); added_i += 1
    with PEOPLE.open("a", encoding="utf-8") as fh:
        for rec in PEOPLE_RECS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); added_p += 1
    existing_edges = _edge_set()
    with EDGES.open("a", encoding="utf-8") as fh:
        for s, t in EDGE_RECS:
            if (s, t) not in existing_edges and s in have and t in have:
                fh.write(json.dumps({"source": s, "target": t}, ensure_ascii=False) + "\n")
                existing_edges.add((s, t)); added_e += 1
    print(f"Added: {added_i} institutions, {added_p} people, {added_e} edges.")


if __name__ == "__main__":
    main()
