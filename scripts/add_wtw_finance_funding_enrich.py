"""Flesh out the finance/funding-layer entries: build their documented affiliations into the graph.

add_wtw_finance_funding.py seeded the funder nodes (Open Phil, Schmidt Sciences, SFF, CSET, FMF AI
Safety Fund, ROOST, Berkman Klein, etc.) but left them sparsely connected. This second pass builds them
out — adding the connective figures and parent/backer nodes their documented record requires so each new
entry is a full graph member, not a stub:

  * Jason Matheny — the missing revolving-door hinge: IARPA director -> CSET founding director ->
    White House OSTP/NSC -> RAND CEO (connects CSET to the intel/gov rotation).
  * Frontier Model Forum (parent) + the six member labs -> the FMF AI Safety Fund (the labs fund the
    fund that grades them).
  * The funder-people's own bios (Tallinn -> FLI; Karnofsky/Open Phil -> GiveWell; Moskovitz -> Asana,
    Meta), ROOST's remaining backers (Google, Discord, Roblox), and Berkman Klein's co-funders
    (Omidyar Network, Knight Foundation).

Idempotent; positions-only role text; >=2 sources each; plain-adjacency edges; institution-set only,
never an ethnic/collective-actor frame.
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
    {"id": "FMF", "label": "Frontier Model Forum", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.frontiermodelforum.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Frontier_Model_Forum"}], "kind": "institution"},
    {"id": "FLI", "label": "Future of Life Institute", "sector": "tank",
     "sources": [{"type": "official", "url": "https://futureoflife.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Future_of_Life_Institute"}], "kind": "institution"},
    {"id": "GiveWell", "label": "GiveWell", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.givewell.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/GiveWell"}], "kind": "institution"},
    {"id": "Asana", "label": "Asana", "sector": "tech",
     "sources": [{"type": "official", "url": "https://asana.com/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Asana,_Inc."}], "kind": "institution"},
    {"id": "Roblox", "label": "Roblox Corporation", "sector": "tech",
     "sources": [{"type": "official", "url": "https://corp.roblox.com/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Roblox_Corporation"}], "kind": "institution"},
    {"id": "IARPA", "label": "Intelligence Advanced Research Projects Activity", "sector": "intel",
     "sources": [{"type": "official", "url": "https://www.iarpa.gov/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Intelligence_Advanced_Research_Projects_Activity"}], "kind": "institution"},
    {"id": "OmidyarNetwork", "label": "Omidyar Network", "sector": "tank",
     "sources": [{"type": "official", "url": "https://omidyar.com/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Omidyar_Network"}], "kind": "institution"},
    {"id": "KnightFoundation", "label": "John S. and James L. Knight Foundation", "sector": "tank",
     "sources": [{"type": "official", "url": "https://knightfoundation.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Knight_Foundation"}], "kind": "institution"},
]

PEOPLE_RECS = [
    {"id": "Matheny", "label": "Jason Matheny", "kind": "person", "sector": "intel",
     "admin": ["biden"], "networks": [], "plays": [], "actors": ["watchers", "blueprint"],
     "role": "IARPA director -> CSET founding director (Georgetown) -> White House OSTP/NSC "
             "deputy assistant to the president -> RAND Corporation president & CEO",
     "sources": [{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Jason_Gaverick_Matheny"},
                 {"type": "official", "url": "https://www.rand.org/about/people/m/matheny_jason.html"}]},
]

EDGE_RECS = [
    # Matheny: the intel -> tank -> gov -> tank rotation that connects CSET to the revolving door
    ("Matheny", "IARPA"), ("Matheny", "CSET"), ("Matheny", "RAND"),
    # the six member labs fund the FMF AI Safety Fund (the fund that grades them)
    ("Microsoft", "FMF"), ("Google", "FMF"), ("OpenAI", "FMF"),
    ("Anthropic", "FMF"), ("Amazon", "FMF"), ("Meta", "FMF"), ("FMF", "FMFSafetyFund"),
    # funder-people bios
    ("Tallinn", "FLI"), ("Karnofsky", "GiveWell"), ("OpenPhil", "GiveWell"),
    ("Moskovitz", "Asana"), ("Moskovitz", "Meta"),
    # ROOST's remaining backers
    ("Google", "ROOST"), ("Discord", "ROOST"), ("Roblox", "ROOST"),
    # Berkman Klein Ethics & Governance of AI Fund co-funders
    ("OmidyarNetwork", "BerkmanKlein"), ("KnightFoundation", "BerkmanKlein"),
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
    ai = ap = ae = 0
    with INST.open("a", encoding="utf-8") as fh:
        for rec in INSTITUTIONS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); ai += 1
    with PEOPLE.open("a", encoding="utf-8") as fh:
        for rec in PEOPLE_RECS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); ap += 1
    ee = _edge_set()
    with EDGES.open("a", encoding="utf-8") as fh:
        for s, t in EDGE_RECS:
            if (s, t) not in ee and s in have and t in have:
                fh.write(json.dumps({"source": s, "target": t}, ensure_ascii=False) + "\n")
                ee.add((s, t)); ae += 1
    print(f"Added: {ai} institutions, {ap} people, {ae} edges.")


if __name__ == "__main__":
    main()
