"""v3 USAID + democracy-promotion orbit drain.

Named persons (5): SPower (USAID Admin Obama UN -> USAID Biden),
RShah (USAID Admin Obama -> Rockefeller Foundation), Gawande (USAID
Global Health Biden), Gershman (NED President 1984-2021), DWilson
(NED President 2021- ex-Atlantic Council COO).

USAID-orbit institutions (5): NED (National Endowment for
Democracy), IFES (International Foundation for Electoral Systems),
NDI (National Democratic Institute), IRI (International Republican
Institute), Internews.

These complete the documented USAID -> democracy-promotion ->
disinformation-research pipeline that the Twitter Files / DOJ NSD
research has been mapping. Adjacent to but not identical with the
T&S analytical surface (which catalogs the pseudonymous-mod ecosystem
separately).
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
    {"id": "NED", "label": "National Endowment for Democracy", "sector": "tank",
     "sources": [w("National_Endowment_for_Democracy"), off("https://www.ned.org/")]},
    {"id": "IFES", "label": "International Foundation for Electoral Systems", "sector": "tank",
     "sources": [w("International_Foundation_for_Electoral_Systems"), off("https://www.ifes.org/")]},
    {"id": "NDI", "label": "National Democratic Institute", "sector": "tank",
     "sources": [w("National_Democratic_Institute"), off("https://www.ndi.org/")]},
    {"id": "IRI", "label": "International Republican Institute", "sector": "tank",
     "sources": [w("International_Republican_Institute"), off("https://www.iri.org/")]},
    {"id": "Internews", "label": "Internews Network", "sector": "tank",
     "sources": [w("Internews"), off("https://internews.org/")]},
]


NEW_PERSONS = [
    {"id": "SPower", "label": "Samantha Power", "sector": "gov",
     "admin": ["obama", "biden"], "networks": ["cfr"],
     "plays": ["pulpit", "pipeline"], "actors": ["embassy", "eagle", "flagging"],
     "role": "Carr Center for Human Rights Policy founding executive director -> NSC Senior Director for Multilateral Affairs and Human Rights -> US Ambassador to the UN 2013-17 -> Harvard Kennedy School professor -> USAID Administrator 2021-25",
     "sources": [w("Samantha_Power"), wd("Q272421"),
                 gov("https://www.usaid.gov/who-we-are/organization/administrator/samantha-power")]},
    {"id": "RShah", "label": "Rajiv Shah", "sector": "gov",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline", "rumpelstiltskin"], "actors": [],
     "role": "Gates Foundation Director of Agricultural Development -> USDA Under Secretary for Research, Education and Economics -> USAID Administrator 2010-15 -> Rockefeller Foundation President 2017-",
     "sources": [w("Rajiv_Shah_(Indian-American)"), wd("Q3416275"),
                 gov("https://www.usaid.gov/who-we-are/organization/administrator/dr-rajiv-shah")]},
    {"id": "Gawande", "label": "Atul Gawande", "sector": "gov",
     "admin": ["obama", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "Harvard Medical School + Brigham and Women's surgeon -> The New Yorker staff writer -> Ariadne Labs founder -> Haven Healthcare CEO 2018-20 -> USAID Assistant Administrator for Global Health 2022-25",
     "sources": [w("Atul_Gawande"), wd("Q4818825"),
                 gov("https://www.usaid.gov/who-we-are/organization/bureaus/bureau-global-health/assistant-administrator")]},
    {"id": "Gershman", "label": "Carl Gershman", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Social Democrats USA Executive Director -> Senior counselor to US Ambassador to UN -> National Endowment for Democracy founding President 1984-2021",
     "sources": [w("Carl_Gershman"), wd("Q5043900"),
                 off("https://www.ned.org/about/board/meet-our-staff/carl-gershman/")]},
    {"id": "DWilson", "label": "Damon Wilson", "sector": "tank",
     "admin": ["bush2"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "NSC Senior Director for European Affairs (Bush2) -> Atlantic Council Executive Vice President -> National Endowment for Democracy President 2021-",
     "sources": [w("Damon_Wilson_(political_scientist)"), wd("Q105906179"),
                 off("https://www.ned.org/about/board/meet-our-staff/")]},
]


NEW_EDGES = [
    ("SPower", "USAID"), ("SPower", "UN"), ("SPower", "NSC"), ("SPower", "CFR"),
    ("RShah", "USAID"), ("RShah", "RockefellerFoundation"), ("RShah", "GatesFoundation"),
    ("Gawande", "USAID"),
    ("Gershman", "NED"),
    ("DWilson", "NED"), ("DWilson", "AtlanticCouncil"), ("DWilson", "NSC"),
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
    if skipped:
        print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
