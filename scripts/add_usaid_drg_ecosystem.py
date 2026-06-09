"""USAID DRG ecosystem expansion — pre-2014 democracy-promotion-NGO
ecosystem named figures + supporting institutions.

The 2026-05-29 research finding: USAID's democracy-promotion ecosystem
was already MATURE pre-2014 (~$103M NED appropriation FY13, ~1,200
grants/year across ~100 countries, peak US gov media spending $135M
FY08, then 43.5% contraction to $76M by FY12). No "counter-
disinformation" language pre-2014; programs were institutional/
development-framed. The 2014 Ukraine crisis was the pivot to defensive
"information warfare" framing. Ecosystem pre-built; discourse changed.

Persons (3): Carothers (Carnegie Endowment DRG-strategy author),
LDiamond (Stanford CDDRL director, "Liberation Technology" editor),
DKramer (Freedom House President 2010-14, Bush2 State Dept).

Institutions (6): CEPPS (Consortium for Elections and Political Process
Strengthening, est. 1995), CIMA (Center for International Media
Assistance, est. 2006 at NED), Counterpart International, IREX, OTF
(Open Technology Fund), Stanford CDDRL.
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
def acad(url): return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    {"id": "CEPPS", "label": "Consortium for Elections and Political Process Strengthening",
     "sector": "tank",
     "sources": [w("Consortium_for_Elections_and_Political_Process_Strengthening"),
                 off("https://www.cepps.org/")]},
    {"id": "CIMA", "label": "Center for International Media Assistance", "sector": "tank",
     "sources": [off("https://www.cima.ned.org/"),
                 acad("https://www.cima.ned.org/wp-content/uploads/2015/01/U.S.-Government-Funding-for-Media_Trends-and-Strategies.pdf")]},
    {"id": "FreedomHouse", "label": "Freedom House", "sector": "tank",
     "sources": [w("Freedom_House"), off("https://freedomhouse.org/")]},
    {"id": "IREX", "label": "IREX (International Research and Exchanges Board)", "sector": "tank",
     "sources": [w("IREX"), off("https://www.irex.org/")]},
    {"id": "Counterpart", "label": "Counterpart International", "sector": "tank",
     "sources": [w("Counterpart_International"), off("https://www.counterpart.org/")]},
    {"id": "OTF", "label": "Open Technology Fund", "sector": "tank",
     "sources": [w("Open_Technology_Fund"), off("https://www.opentech.fund/")]},
    {"id": "StanfordCDDRL", "label": "Stanford Center on Democracy, Development, and the Rule of Law",
     "sector": "tank",
     "sources": [w("Stanford_Center_on_Democracy,_Development,_and_the_Rule_of_Law"),
                 off("https://cddrl.fsi.stanford.edu/")]},
    {"id": "Carnegie", "label": "Carnegie Endowment for International Peace", "sector": "tank",
     "sources": [w("Carnegie_Endowment_for_International_Peace"), off("https://carnegieendowment.org/")]},
]


NEW_PERSONS = [
    {"id": "Carothers", "label": "Thomas Carothers", "sector": "tank",
     "admin": ["reagan"], "networks": [],
     "plays": [], "actors": [],
     "role": "State Department Office of the Legal Adviser (Reagan) -> Carnegie Endowment for International Peace Vice President for Studies and Senior Fellow 1994- (authored canonical DRG strategy analyses 1999-2014)",
     "sources": [w("Thomas_Carothers"), wd("Q7793013"),
                 off("https://carnegieendowment.org/2020/09/15/guide-to-publications-by-thomas-carothers-pub-46576")]},
    {"id": "LDiamond", "label": "Larry Diamond", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Stanford Center on Democracy, Development, and the Rule of Law Director 2009-15 -> Hoover Institution Senior Fellow -> Journal of Democracy founding co-editor; Liberation Technology editor 2012-",
     "sources": [w("Larry_Diamond"), wd("Q1810081"),
                 off("https://diamond-democracy.stanford.edu/")]},
    {"id": "DKramer", "label": "David J. Kramer", "sector": "tank",
     "admin": ["bush2"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "State Department European/Eurasian Affairs Deputy Assistant Secretary (Bush2) -> Assistant Secretary for Democracy, Human Rights, and Labor 2008-09 -> German Marshall Fund Senior Fellow -> Freedom House President 2010-14 -> McCain Institute Senior Director",
     "sources": [w("David_J._Kramer"), wd("Q5239478"),
                 off("https://www.mccaininstitute.org/people/david-j-kramer/")]},
]


NEW_EDGES = [
    # Carothers -> Carnegie + State
    ("Carothers", "Carnegie"), ("Carothers", "State"),
    # LDiamond -> Stanford CDDRL + Hoover
    ("LDiamond", "StanfordCDDRL"),
    # DKramer -> Freedom House + State + GMF (not yet inst)
    ("DKramer", "FreedomHouse"), ("DKramer", "State"),
    # Gershman -> CIMA + NED (NED already linked, CIMA new)
    ("Gershman", "CIMA"),
    # NDI / IRI / IFES are already institutions; link to CEPPS
    # (only the institutions, no person edges added here)
]


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

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions: f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people: f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges: f.write(json.dumps(e) + "\n")

    print(f"Added {new_i} institutions, {new_p} persons, {new_e} edges.")
    if skipped: print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
