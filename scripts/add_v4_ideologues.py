"""v4 historical-ideologues layer.

A separate scoped category for the intellectual *antecedents* of the control
grid -- the ideologues whose programs the institutions later operationalised.
These figures are NOT in the dataset on the 2-sector revolving-door predicate
(most never held a sector position at all). They are admitted under a distinct
layer, tagged `sector: "historical"`, carrying:

  - a one-line `brief` (what they are the antecedent of),
  - a `role` paraphrase of documented public positions only,
  - >=2 primary sources (Wikipedia + one official/academic; never Wikipedia-only),
  - edges to the institutions they founded or led,
  - NO `plays` / `actors` tags (they predate the control-grid actors; the
    institutions carry the operational edges, not the people).

See docs/SCOPE.md -> "Historical-ideologues layer" for the policy.

Idempotent. Adds the two missing supporting institutions (RhodesTrust, LSE);
the others (EugenicsSociety, FabianSociety, MontPelerin, RoundTable,
SchillerInstitute, Georgetown) already exist and are reused.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name):
    return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}


def off(url):
    return {"type": "official", "url": url}


def acad(url):
    return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    {"id": "RhodesTrust", "label": "Rhodes Trust", "sector": "historical",
     "sources": [w("Rhodes_Trust"), off("https://www.rhodeshouse.ox.ac.uk/")],
     "brief": "Rhodes Trust, established 1902 under Cecil Rhodes's will to fund the Rhodes Scholarships at Oxford; the endowment that bankrolled the Milner / Round Table imperial-federation network."},
    {"id": "LSE", "label": "London School of Economics", "sector": "tank",
     "sources": [w("London_School_of_Economics"), off("https://www.lse.ac.uk/")],
     "brief": "London School of Economics, founded 1895 by Fabian Society members Sidney and Beatrice Webb to train an administrative and policy class."},
]

NEW_PERSONS = [
    # ---- Hereditarian / eugenics antecedent --------------------------------
    {"id": "Galton", "label": "Francis Galton", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Originator of 'eugenics'; hereditarian antecedent of 20th-century population-control policy.",
     "role": "Victorian polymath and statistician; coined 'eugenics' (1883); endowed the first eugenics fellowship and chair at University College London; the Eugenics Education Society (1907) institutionalised his program",
     "sources": [w("Francis_Galton"), acad("https://galton.org/")]},

    # ---- Fabian / gradualist-socialist antecedents -------------------------
    {"id": "Shaw", "label": "George Bernard Shaw", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Fabian gradualist who popularised socialist policy through theatre and tracts.",
     "role": "Playwright and essayist; founding member of the Fabian Society (1884); long-serving Fabian pamphleteer and lecturer; Nobel laureate in Literature 1925",
     "sources": [w("George_Bernard_Shaw"),
                 off("https://www.nobelprize.org/prizes/literature/1925/shaw/facts/")]},
    {"id": "SidneyWebb", "label": "Sidney Webb", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Co-architect of Fabian gradualism and the LSE.",
     "role": "Fabian Society leader; co-founder of the London School of Economics (1895); principal drafter of the Labour Party's 1918 constitution; President of the Board of Trade (1924) and Secretary of State for the Colonies (1929-31)",
     "sources": [w("Sidney_Webb,_1st_Baron_Passfield"),
                 off("https://www.lse.ac.uk/about-lse/our-history")]},
    {"id": "BeatriceWebb", "label": "Beatrice Webb", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Co-architect, with Sidney Webb, of Fabian social policy and the LSE.",
     "role": "Social researcher and Fabian Society leader; co-founder of the London School of Economics; author of the 1909 Minority Report of the Royal Commission on the Poor Laws",
     "sources": [w("Beatrice_Webb"),
                 acad("https://www.britannica.com/biography/Beatrice-Webb")]},
    {"id": "Wells", "label": "H. G. Wells", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Popularised technocratic world-order ideas in fiction and essays.",
     "role": "Novelist and essayist; Fabian Society member (1903-08); author of 'The Open Conspiracy' (1928) and 'The Shape of Things to Come' (1933), advocating a planned world order",
     "sources": [w("H._G._Wells"),
                 acad("https://www.britannica.com/biography/H-G-Wells")]},

    # ---- Rhodes / Milner imperial-network antecedents ----------------------
    {"id": "Rhodes", "label": "Cecil Rhodes", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Imperial financier whose bequest funded the Rhodes-Milner network.",
     "role": "Mining financier; founder of De Beers and the British South Africa Company; Prime Minister of the Cape Colony (1890-96); his will (1902) created the Rhodes Trust, the Rhodes Scholarships, and called for a society to extend British influence",
     "sources": [w("Cecil_Rhodes"), off("https://www.rhodeshouse.ox.ac.uk/")]},
    {"id": "Milner", "label": "Alfred Milner", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Built the Round Table imperial-federation network from the Rhodes bequest.",
     "role": "British High Commissioner for Southern Africa (1897-1905); member of Lloyd George's War Cabinet (1916-18); Secretary of State for the Colonies (1919-21); Rhodes Trust trustee and organiser of the Round Table movement",
     "sources": [w("Alfred_Milner,_1st_Viscount_Milner"),
                 acad("https://www.britannica.com/biography/Alfred-Milner-Viscount-Milner")]},
    {"id": "Quigley", "label": "Carroll Quigley", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Documented the Anglo-American establishment from inside the academy.",
     "role": "Historian; professor at Georgetown University's School of Foreign Service (1941-76); author of 'Tragedy and Hope' (1966) and 'The Anglo-American Establishment' (1981), which documented the Rhodes-Milner Round Table network",
     "sources": [w("Carroll_Quigley"), acad("https://www.carrollquigley.net/")]},

    # ---- Austrian School / free-market antecedents -------------------------
    {"id": "Mises", "label": "Ludwig von Mises", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Austrian School antecedent of the postwar free-market movement.",
     "role": "Austrian School economist; founding member of the Mont Pelerin Society (1947); visiting professor at New York University (1945-69); author of 'Human Action' (1949)",
     "sources": [w("Ludwig_von_Mises"),
                 off("https://mises.org/profile/ludwig-von-mises")]},
    {"id": "Hayek", "label": "Friedrich Hayek", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Principal organiser of the postwar free-market intellectual network.",
     "role": "Austrian School economist; professor at the London School of Economics and the University of Chicago; founder and first president of the Mont Pelerin Society (1947); Nobel laureate in Economic Sciences 1974; author of 'The Road to Serfdom' (1944)",
     "sources": [w("Friedrich_Hayek"),
                 off("https://www.nobelprize.org/prizes/economic-sciences/1974/hayek/facts/")]},

    # ---- Idiosyncratic political-network antecedent ------------------------
    {"id": "LaRouche", "label": "Lyndon LaRouche", "sector": "historical",
     "admin": [], "networks": [], "plays": [], "actors": [],
     "brief": "Founder of an idiosyncratic political-ideological network.",
     "role": "Political organiser; founder of the LaRouche political movement and co-founder of the Schiller Institute (1984); eight-time US presidential candidate (1976-2004)",
     "sources": [w("Lyndon_LaRouche"),
                 acad("https://www.britannica.com/biography/Lyndon-LaRouche")]},
]

NEW_EDGES = [
    ("Galton", "EugenicsSociety"),
    ("Shaw", "FabianSociety"),
    ("SidneyWebb", "FabianSociety"), ("SidneyWebb", "LSE"),
    ("BeatriceWebb", "FabianSociety"), ("BeatriceWebb", "LSE"),
    ("Wells", "FabianSociety"),
    ("Rhodes", "RhodesTrust"), ("Rhodes", "RoundTable"),
    ("Milner", "RoundTable"), ("Milner", "RhodesTrust"),
    ("Quigley", "Georgetown"),
    ("Mises", "MontPelerin"),
    ("Hayek", "MontPelerin"), ("Hayek", "LSE"),
    ("LaRouche", "SchillerInstitute"),
]


def read_jsonl(path):
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
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

    new_inst = 0
    for rec in NEW_INSTITUTIONS:
        if rec["id"] in inst_ids or rec["id"] in person_ids:
            continue
        rec["kind"] = "institution"
        institutions.append(rec)
        inst_ids.add(rec["id"])
        all_ids.add(rec["id"])
        new_inst += 1

    new_persons = 0
    skipped_dup = []
    for rec in NEW_PERSONS:
        if rec["id"] in person_ids or rec["id"] in inst_ids:
            skipped_dup.append(rec["id"])
            continue
        rec["kind"] = "person"
        people.append(rec)
        person_ids.add(rec["id"])
        all_ids.add(rec["id"])
        new_persons += 1

    new_edges = 0
    skipped_edges = []
    for src, tgt in NEW_EDGES:
        if src not in all_ids or tgt not in all_ids:
            skipped_edges.append(f"{src}->{tgt}")
            continue
        if (src, tgt) in edge_keys:
            continue
        edges.append({"source": src, "target": tgt})
        edge_keys.add((src, tgt))
        new_edges += 1

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions:
            f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people:
            f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges:
            f.write(json.dumps(e) + "\n")

    print(f"Added {new_inst} institutions, {new_persons} persons, {new_edges} edges.")
    if skipped_dup:
        print(f"Skipped {len(skipped_dup)} dup IDs: {skipped_dup}")
    if skipped_edges:
        print(f"Skipped edges (missing node): {skipped_edges}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
