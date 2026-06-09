"""UK + European institutional architecture drain.

The dataset already has UK persons (Carney, Blair, Cameron, BJohnson,
Sunak, Truss, Fleming, RMoore) and UK govt orgs (UKGov, BoE, BoC, GCHQ,
MI6, NATO) — but no UK think-tank brain trust (Chatham House / RIIA,
IISS, RUSI, etc.). Same for EU beyond EC/ECB.

UK think tanks (7): Chatham House, IISS, RUSI, KingsWarStudies, Wilton
Park, Ditchley, ReutersInstitute, HenryJackson, PolicyExchange.

EU think tanks (3): ECFR (European Council on Foreign Relations),
Bruegel (Brussels economics), CER (Centre for European Reform).

UK gov institutions (2): FCDO (Foreign Commonwealth & Development
Office), MI5 (Security Service).

UK persons (5): Niblett (Chatham House Director 2007-22), BMaddox
(Chatham House Director 2022-), Sawers (MI6 Chief 2009-14), AParker
(MI5 DG 2013-20), McCallum (MI5 DG 2020-), Starmer (UK PM 2024-).

EU persons (1): JBorrell (EU High Representative for Foreign Affairs
2019-24).

Plus US-side person: Reeves (Rachel Reeves, UK Chancellor 2024-).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def wd(qid): return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}
def off(url): return {"type": "official", "url": url}


NEW_INSTITUTIONS = [
    # UK think tanks
    {"id": "Chatham", "label": "Chatham House (Royal Institute of International Affairs)",
     "sector": "tank",
     "sources": [w("Chatham_House"), off("https://www.chathamhouse.org/")]},
    {"id": "IISS", "label": "International Institute for Strategic Studies", "sector": "tank",
     "sources": [w("International_Institute_for_Strategic_Studies"), off("https://www.iiss.org/")]},
    {"id": "RUSI", "label": "Royal United Services Institute", "sector": "tank",
     "sources": [w("Royal_United_Services_Institute"), off("https://www.rusi.org/")]},
    {"id": "KingsWarStudies", "label": "King's College London Department of War Studies",
     "sector": "tank",
     "sources": [w("Department_of_War_Studies,_King%27s_College_London"),
                 off("https://www.kcl.ac.uk/warstudies")]},
    {"id": "WiltonPark", "label": "Wilton Park (FCDO conferences)", "sector": "tank",
     "sources": [w("Wilton_Park"), off("https://www.wiltonpark.org.uk/")]},
    {"id": "Ditchley", "label": "Ditchley Foundation", "sector": "tank",
     "sources": [w("Ditchley_Foundation"), off("https://www.ditchley.com/")]},
    {"id": "ReutersInstitute", "label": "Reuters Institute for the Study of Journalism (Oxford)",
     "sector": "tank",
     "sources": [w("Reuters_Institute_for_the_Study_of_Journalism"),
                 off("https://reutersinstitute.politics.ox.ac.uk/")]},
    {"id": "HenryJackson", "label": "Henry Jackson Society", "sector": "tank",
     "sources": [w("Henry_Jackson_Society"), off("https://henryjacksonsociety.org/")]},
    {"id": "PolicyExchange", "label": "Policy Exchange (UK)", "sector": "tank",
     "sources": [w("Policy_Exchange"), off("https://policyexchange.org.uk/")]},
    # EU think tanks
    {"id": "ECFR", "label": "European Council on Foreign Relations", "sector": "tank",
     "sources": [w("European_Council_on_Foreign_Relations"), off("https://ecfr.eu/")]},
    {"id": "Bruegel", "label": "Bruegel (Brussels economics think tank)", "sector": "tank",
     "sources": [w("Bruegel_(institution)"), off("https://www.bruegel.org/")]},
    {"id": "CER", "label": "Centre for European Reform", "sector": "tank",
     "sources": [w("Centre_for_European_Reform"), off("https://www.cer.eu/")]},
    # UK gov institutions
    {"id": "FCDO", "label": "Foreign, Commonwealth & Development Office (UK)", "sector": "gov",
     "sources": [w("Foreign,_Commonwealth_and_Development_Office"),
                 off("https://www.gov.uk/government/organisations/foreign-commonwealth-development-office")]},
    {"id": "MI5", "label": "MI5 (UK Security Service)", "sector": "intel",
     "sources": [w("MI5"), off("https://www.mi5.gov.uk/")]},
]


NEW_PERSONS = [
    {"id": "Niblett", "label": "Robin Niblett", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "CSIS Vice President -> Chatham House Director and Chief Executive 2007-22 -> Hakluyt & Co. distinguished fellow",
     "sources": [w("Robin_Niblett"), wd("Q7350547"),
                 off("https://www.chathamhouse.org/about-us/our-people/robin-niblett")]},
    {"id": "BMaddox", "label": "Bronwen Maddox", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Financial Times foreign editor -> The Times chief foreign commentator -> Prospect magazine Editor 2010-16 -> Institute for Government Director 2016-22 -> Chatham House Director and Chief Executive 2022-",
     "sources": [w("Bronwen_Maddox"), wd("Q4974823"),
                 off("https://www.chathamhouse.org/about-us/our-people/bronwen-maddox")]},
    {"id": "Sawers", "label": "John Sawers", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy", "tap"],
     "role": "FCO career diplomat -> Tony Blair's foreign affairs adviser -> UK Ambassador to UN 2007-09 -> Chief of the Secret Intelligence Service (MI6) 2009-14 -> Macro Advisory Partners founder -> BP non-executive Director",
     "sources": [w("John_Sawers"), wd("Q3179727"),
                 off("https://www.sis.gov.uk/our-history.html")]},
    {"id": "AParker", "label": "Andrew Parker", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["tap", "watchers"],
     "role": "MI5 career officer -> MI5 Director General 2013-20 -> Lord Parker of Minsmere (peer 2021)",
     "sources": [w("Andrew_Parker_(MI5)"), wd("Q4757432"),
                 off("https://www.mi5.gov.uk/director-general")]},
    {"id": "McCallum", "label": "Ken McCallum", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["tap", "watchers"],
     "role": "MI5 career officer -> Director of Intelligence Coordination -> MI5 Director General 2020-",
     "sources": [w("Ken_McCallum"), wd("Q98044870"),
                 off("https://www.mi5.gov.uk/director-general")]},
    {"id": "Starmer", "label": "Keir Starmer", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Doughty Street Chambers barrister + QC -> Director of Public Prosecutions 2008-13 -> UK Labour MP 2015- -> Leader of the Opposition 2020-24 -> Prime Minister of the UK 2024-",
     "sources": [w("Keir_Starmer"), wd("Q333553"),
                 off("https://www.gov.uk/government/people/keir-starmer")]},
    {"id": "Reeves", "label": "Rachel Reeves", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Bank of England economist -> HBOS economist -> UK Labour MP 2010- -> Shadow Chancellor of the Exchequer 2021-24 -> Chancellor of the Exchequer 2024-",
     "sources": [w("Rachel_Reeves"), wd("Q4203919"),
                 off("https://www.gov.uk/government/people/rachel-reeves")]},
    {"id": "JBorrell", "label": "Josep Borrell", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy"],
     "role": "Spanish PSOE politician -> President of the European Parliament 2004-07 -> Spanish Minister of Foreign Affairs 2018-19 -> EU High Representative for Foreign Affairs and Security Policy + Vice-President of the European Commission 2019-24",
     "sources": [w("Josep_Borrell"), wd("Q193710"),
                 off("https://www.eeas.europa.eu/eeas/josep-borrell-fontelles_en")]},
]


NEW_EDGES = [
    # Chatham House persons
    ("Niblett", "Chatham"), ("Niblett", "CSIS"), ("Niblett", "Hakluyt"),
    ("BMaddox", "Chatham"),
    # MI6 / MI5 / FCO
    ("Sawers", "MI6"), ("Sawers", "FCDO"), ("Sawers", "UN"),
    ("AParker", "MI5"),
    ("McCallum", "MI5"),
    # UK PM/Chancellor
    ("Starmer", "UKGov"),
    ("Reeves", "UKGov"), ("Reeves", "BoE"),
    # EU
    ("JBorrell", "EC"),
    # Already-in-dataset UK persons -> new UK institutions
    ("Cameron", "Chatham"),  # documented Chatham House engagement
    ("Blair", "Chatham"),    # documented Chatham House engagement
    ("Carney", "Chatham"),
    ("Carney", "BoE"),       # already present? add if not
    ("Fleming", "RUSI"),     # MI5/GCHQ-RUSI nexus
    # Hakluyt + Niblett already wired
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
