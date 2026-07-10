"""Add the finance/funding layer behind the Watching-the-Watchers apparatus to the Ratchet graph.

The graph already holds the apparatus people/orgs and the finance-principal people (vault/bretton/cousin
plays). What was missing is the FUNDING adjacency that makes "finance -> apparatus" queryable rather than
prose: the grantmakers (Open Philanthropy / Good Ventures, Schmidt Sciences, Survival and Flourishing
Fund, Berkman Klein's funders) that bankroll the evaluators and governance shops (CSET, METR, GovAI, the
FMF AI Safety Fund, ROOST), plus Kissinger's documented finance patronage (Rockefeller Brothers Fund,
Kissinger Associates).

Idempotent; defamation-disciplined (positions-only role text, >=2 sources each, no characterizations).
Edges are plain adjacency. This is research scaffolding — a documented funding/affiliation map, never a
verdict, and strictly an institution-set (never an ethnic/collective-actor frame).
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
    {"id": "OpenPhil", "label": "Open Philanthropy", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.openphilanthropy.org/"},
                 {"type": "official", "url": "https://www.openphilanthropy.org/grants/"}], "kind": "institution"},
    {"id": "GoodVentures", "label": "Good Ventures", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.goodventures.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Dustin_Moskovitz"}], "kind": "institution"},
    {"id": "SchmidtSciences", "label": "Schmidt Sciences (formerly Schmidt Futures)", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.schmidtsciences.org/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Schmidt_Futures"}], "kind": "institution"},
    {"id": "SFF", "label": "Survival and Flourishing Fund", "sector": "tank",
     "sources": [{"type": "official", "url": "https://survivalandflourishing.fund/"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Jaan_Tallinn"}], "kind": "institution"},
    {"id": "RBF", "label": "Rockefeller Brothers Fund", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.rbf.org/"},
                 {"type": "official", "url": "https://www.rbf.org/about/our-history/timeline/special-studies-project"}], "kind": "institution"},
    {"id": "CSET", "label": "Center for Security and Emerging Technology (Georgetown)", "sector": "tank",
     "sources": [{"type": "official", "url": "https://cset.georgetown.edu/"},
                 {"type": "official", "url": "https://www.openphilanthropy.org/grants/georgetown-university-center-for-security-and-emerging-technology/"}], "kind": "institution"},
    {"id": "FMFSafetyFund", "label": "Frontier Model Forum AI Safety Fund", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.frontiermodelforum.org/"},
                 {"type": "press", "url": "https://www.frontiermodelforum.org/updates/ai-safety-fund/"}], "kind": "institution"},
    {"id": "ROOST", "label": "ROOST (Robust Open Online Safety Tools)", "sector": "tank",
     "sources": [{"type": "official", "url": "https://roost.tools/"},
                 {"type": "press", "url": "https://www.weforum.org/press/2025/02/roost-launch-online-safety-tools/"}], "kind": "institution"},
    {"id": "BerkmanKlein", "label": "Berkman Klein Center for Internet & Society (Harvard)", "sector": "tank",
     "sources": [{"type": "official", "url": "https://cyber.harvard.edu/"},
                 {"type": "official", "url": "https://cyber.harvard.edu/story/2017-01/ethics-and-governance-artificial-intelligence-fund"}], "kind": "institution"},
    {"id": "KissingerAssociates", "label": "Kissinger Associates", "sector": "fin",
     "sources": [{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Kissinger_Associates"},
                 {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Henry_Kissinger"}], "kind": "institution"},
]

PEOPLE_RECS = [
    {"id": "Moskovitz", "label": "Dustin Moskovitz", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["money"],
     "role": "Facebook co-founder -> Asana co-founder/CEO -> Good Ventures / Open Philanthropy funder",
     "sources": [{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Dustin_Moskovitz"},
                 {"type": "official", "url": "https://www.goodventures.org/about-us/"}]},
    {"id": "Karnofsky", "label": "Holden Karnofsky", "kind": "person", "sector": "tank",
     "admin": [], "networks": [], "plays": [], "actors": ["money", "model"],
     "role": "GiveWell co-founder -> Open Philanthropy co-founder/co-CEO -> OpenAI board (2017) -> Anthropic",
     "sources": [{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Holden_Karnofsky"},
                 {"type": "official", "url": "https://www.openphilanthropy.org/about/team/holden-karnofsky/"}]},
    {"id": "Tallinn", "label": "Jaan Tallinn", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["money"],
     "role": "Skype/Kazaa co-founder -> CSER & Future of Life Institute co-founder -> Survival and Flourishing Fund",
     "sources": [{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Jaan_Tallinn"},
                 {"type": "official", "url": "https://futureoflife.org/person/jaan-tallinn/"}]},
]

EDGE_RECS = [
    # grantmaker structure
    ("Moskovitz", "GoodVentures"), ("Moskovitz", "OpenPhil"), ("GoodVentures", "OpenPhil"),
    ("Karnofsky", "OpenPhil"), ("Karnofsky", "OpenAI"), ("Karnofsky", "Anthropic"),
    ("Tallinn", "SFF"), ("Schmidt", "SchmidtSciences"),
    # Open Philanthropy -> apparatus
    ("OpenPhil", "CSET"), ("OpenPhil", "OpenAI"), ("OpenPhil", "GovAI"),
    ("OpenPhil", "METR"), ("OpenPhil", "ARC"),
    # Schmidt -> apparatus
    ("SchmidtSciences", "CSET"), ("SchmidtSciences", "METR"),
    ("SchmidtSciences", "FMFSafetyFund"), ("SchmidtSciences", "ROOST"),
    # SFF -> apparatus
    ("SFF", "METR"), ("SFF", "FMFSafetyFund"),
    # Berkman Klein funding + ROOST backers
    ("Hoffman", "BerkmanKlein"), ("OpenAI", "ROOST"),
    # Kissinger finance patronage (CFR edge already exists)
    ("Kissinger", "RBF"), ("Kissinger", "KissingerAssociates"), ("DRockefeller", "RBF"),
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
