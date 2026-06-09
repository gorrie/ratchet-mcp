"""Climate / ESG / Net-Zero Ratchet (Click #7: The Priest) institutional + named adds.

Per the 2026-05-29 research agent: hybrid finance-led with multilateral
enforcement wrapper. Three operational tiers: finance-led (GFANZ, asset-
manager voting bloc), regulatory/standards (TCFD->ISSB->CSRD->SEC),
central-bank coordination (NGFS). Ratchet mechanism: voluntary standards
-> mandatory disclosure -> capital allocation consequences.

Chapter recommendation: expand Click #7 (The Priest) to include the
financial-infrastructure ratchet ("Fifth Pawl: The Climate Financier"),
OR create new Click #8 (The Ledger / Balance Sheet). Editorial decision
left to author.

Persons added (4 new): Espinosa (UNFCCC Exec Sec 2016-22), Stiell
(UNFCCC Exec Sec 2022-, Grenada), HMizuno (GPIF CIO + UN PRI), BBadré
(ex-WB CFO + Blue like an Orange).

Existing persons retagged with `priest` actor: Fink (BlackRock CEO),
Carney (UN Climate Envoy + GFANZ co-founder), Bloomberg (UN Climate
Envoy + GFANZ co-founder + TCFD chair), JKerry (Biden Climate Envoy),
Figueres (UNFCCC Paris Agreement architect), Yellen (Treasury FSOC
climate authority).

Institutions added (11): GFANZ, NZAOA, ClimateAction100, ISSB, CDP,
NGFS, UN_PRI, ClimateBonds, Sustainalytics, MSCI, BLab, BlueLikeAnOrange.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def wd(qid): return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}
def off(url): return {"type": "official", "url": url}
def gov(url): return {"type": "gov-record", "url": url}


NEW_INSTITUTIONS = [
    {"id": "GFANZ", "label": "Glasgow Financial Alliance for Net Zero", "sector": "fin",
     "sources": [w("Glasgow_Financial_Alliance_for_Net_Zero"), off("https://www.gfanzero.com/")]},
    {"id": "NZAOA", "label": "Net Zero Asset Owners Alliance", "sector": "fin",
     "sources": [w("Net-Zero_Asset_Owner_Alliance"), off("https://www.unepfi.org/net-zero-alliance/")]},
    {"id": "ClimateAction100", "label": "Climate Action 100+", "sector": "fin",
     "sources": [w("Climate_Action_100%2B"), off("https://www.climateaction100.org/")]},
    {"id": "ISSB", "label": "International Sustainability Standards Board (IFRS Foundation)",
     "sector": "multi",
     "sources": [w("International_Sustainability_Standards_Board"),
                 off("https://www.ifrs.org/groups/international-sustainability-standards-board/")]},
    {"id": "CDP", "label": "CDP (formerly Carbon Disclosure Project)", "sector": "tank",
     "sources": [w("CDP_(non-profit)"), off("https://www.cdp.net/")]},
    {"id": "NGFS", "label": "Network for Greening the Financial System (central-bank network)",
     "sector": "multi",
     "sources": [w("Network_for_Greening_the_Financial_System"), off("https://www.ngfs.net/en")]},
    {"id": "UN_PRI", "label": "UN Principles for Responsible Investment", "sector": "multi",
     "sources": [w("Principles_for_Responsible_Investment"), off("https://www.unpri.org/")]},
    {"id": "ClimateBonds", "label": "Climate Bonds Initiative", "sector": "tank",
     "sources": [w("Climate_Bonds_Initiative"), off("https://www.climatebonds.net/")]},
    {"id": "Sustainalytics", "label": "Sustainalytics (Morningstar ESG ratings)", "sector": "tech",
     "sources": [w("Sustainalytics"), off("https://www.sustainalytics.com/")]},
    {"id": "MSCI", "label": "MSCI Inc. (ESG ratings + index provider)", "sector": "fin",
     "sources": [w("MSCI"), off("https://www.msci.com/")]},
    {"id": "BLab", "label": "B Lab (B Corp certification)", "sector": "tank",
     "sources": [w("B_Lab"), off("https://www.bcorporation.net/")]},
    {"id": "BlueLikeAnOrange", "label": "Blue like an Orange Sustainable Capital", "sector": "fin",
     "sources": [w("Bertrand_Badr%C3%A9"), off("https://bluelikeanorangecapital.com/")]},
    {"id": "EngineNo1", "label": "Engine No. 1 (activist investor)", "sector": "fin",
     "sources": [w("Engine_No._1"), off("https://www.engine1.com/")]},
]


NEW_PERSONS = [
    {"id": "Espinosa", "label": "Patricia Espinosa", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": ["priest", "embassy"],
     "role": "Mexican Foreign Service career diplomat -> Mexican Secretary of Foreign Affairs 2006-12 -> UNFCCC Executive Secretary 2016-22 (oversaw Paris Agreement implementation across 6 COPs)",
     "sources": [w("Patricia_Espinosa"), wd("Q466557"),
                 off("https://unfccc.int/about-us/the-executive-secretary/former-executive-secretary-patricia-espinosa")]},
    {"id": "Stiell", "label": "Simon Stiell", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": ["priest"],
     "role": "Grenadian government Minister for Climate Resilience and the Environment 2013-22 -> UNFCCC Executive Secretary 2022-",
     "sources": [w("Simon_Stiell"), wd("Q113018918"),
                 off("https://unfccc.int/about-us/the-executive-secretary")]},
    {"id": "HMizuno", "label": "Hiro Mizuno", "sector": "fin",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["priest"],
     "role": "Sumitomo Mitsui Banking Corporation -> Coller Capital partner -> Government Pension Investment Fund of Japan (GPIF) Chief Investment Officer 2015-20 -> UN PRI board director -> UN Special Envoy on Innovative Finance and Sustainable Investments 2020- -> Tesla board member 2020-",
     "sources": [w("Hiro_Mizuno"), wd("Q98072108"),
                 off("https://www.un.org/sg/en/content/sg/personnel-appointments/2020-12-30/mr-hiro-mizuno-of-japan-special-envoy-innovative-finance-and-sustainable-investments")]},
    {"id": "BBadre", "label": "Bertrand Badre", "sector": "fin",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["priest"],
     "role": "French Treasury / IMF career -> French G8/G20 Sherpa -> Societe Generale Group CFO -> Credit Agricole CFO -> World Bank Managing Director and CFO 2013-16 -> Blue like an Orange Sustainable Capital founder + Managing Partner 2017-",
     "sources": [w("Bertrand_Badr%C3%A9"), wd("Q2899858"),
                 off("https://bluelikeanorangecapital.com/bertrandbadre")]},
]


NEW_EDGES = [
    # Already-in dataset persons -> new climate institutions (documented engagement)
    ("Carney", "GFANZ"),  # GFANZ co-founder 2021
    ("Bloomberg", "GFANZ"),  # GFANZ co-founder Jan 2022
    ("Bloomberg", "ClimateAction100"),  # founding signatory documented
    ("Fink", "GFANZ"),  # BlackRock GFANZ member
    ("Fink", "NZAOA"),  # BlackRock NZAOA participation
    ("Figueres", "ClimateAction100"),  # board / advisory
    ("JKerry", "GFANZ"),  # US climate envoy interfacing with GFANZ
    ("Yellen", "NGFS"),  # Federal Reserve NGFS member during her Fed chair tenure
    # New persons -> institutions
    ("Espinosa", "UNFCCC"),
    ("Stiell", "UNFCCC"),
    ("HMizuno", "UN_PRI"), ("HMizuno", "UN"), ("HMizuno", "Tesla"),
    ("BBadre", "BlueLikeAnOrange"), ("BBadre", "WorldBank"),
    # Institutional architecture edges (institution-to-institution
    # relationships documenting the architecture itself)
    ("ISSB", "EC"),  # ISSB -> EU CSRD alignment
]


# Tag patches: add `priest` actor to existing climate/ESG figures
TAG_PATCHES = {
    "Fink": {"add_actors": ["priest"]},        # BlackRock ESG architect
    "Carney": {"add_actors": ["priest"]},      # UN Climate Envoy + GFANZ co-founder
    "Bloomberg": {"add_actors": ["priest"]},   # UN Climate Envoy + GFANZ + TCFD chair
    "Kerry": {"add_actors": ["priest"]},       # Biden Special Presidential Envoy for Climate
    "Figueres": {"add_actors": ["priest"]},    # UNFCCC Paris Agreement architect
    "Yellen": {"add_actors": ["priest"]},      # Treasury FSOC climate-financial-risk authority
    # Hospital actor on health-governance persons (per pandemic-cluster
    # research finding; structural pattern = philanthropic-funding-determinism)
    "Fauci": {"add_actors": ["hospital"]},
    "Tedros": {"add_actors": ["hospital"]},
    "MChan": {"add_actors": ["hospital"]},
    "Farrar": {"add_actors": ["hospital"]},
    "Berkley": {"add_actors": ["hospital"]},
    "Hatchett": {"add_actors": ["hospital"]},
    "Dybul": {"add_actors": ["hospital"]},
    "Birx": {"add_actors": ["hospital"]},
    "Slaoui": {"add_actors": ["hospital"]},
    "BGates": {"add_actors": ["hospital"]},
    "Suzman": {"add_actors": ["hospital"]},
    "RShah": {"add_actors": ["hospital"]},
    "Gawande": {"add_actors": ["hospital"]},
    "RFKJr": {"add_actors": ["hospital"]},
}


def read_jsonl(path):
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    institutions = read_jsonl(DATA / "institutions.jsonl")
    people = read_jsonl(DATA / "people.jsonl")
    edges = read_jsonl(DATA / "edges.jsonl")

    inst_ids = {r["id"] for r in institutions}
    person_ids = {r["id"] for r in people}
    edge_keys = {(e.get("source"), e.get("target")) for e in edges if isinstance(e, dict)}
    all_ids = inst_ids | person_ids

    new_i = 0
    for rec in NEW_INSTITUTIONS:
        if rec["id"] in inst_ids or rec["id"] in person_ids:
            continue
        rec["kind"] = "institution"
        institutions.append(rec); inst_ids.add(rec["id"]); all_ids.add(rec["id"]); new_i += 1
    new_p = 0
    for rec in NEW_PERSONS:
        if rec["id"] in person_ids or rec["id"] in inst_ids:
            continue
        rec["kind"] = "person"
        people.append(rec); person_ids.add(rec["id"]); all_ids.add(rec["id"]); new_p += 1
    new_e = 0
    skipped = []
    for src, tgt in NEW_EDGES:
        if src not in all_ids or tgt not in all_ids:
            skipped.append(f"{src}->{tgt}"); continue
        if (src, tgt) in edge_keys: continue
        edges.append({"source": src, "target": tgt})
        edge_keys.add((src, tgt)); new_e += 1

    # Apply tag patches
    patches = 0
    for p in people:
        if p["id"] in TAG_PATCHES:
            patch = TAG_PATCHES[p["id"]]
            if "add_actors" in patch:
                actors = set(p.get("actors") or [])
                want = actors | set(patch["add_actors"])
                if want != actors:
                    p["actors"] = sorted(want)
                    patches += 1

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions: f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people: f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges: f.write(json.dumps(e) + "\n")

    print(f"Added {new_i} institutions, {new_p} persons, {new_e} edges.")
    print(f"Tag patches: {patches} existing persons retagged with priest/hospital actors.")
    if skipped: print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
