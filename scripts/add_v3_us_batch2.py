"""v3 US batch 2: Trump2 cabinet + OLC/DOJ remainders from the dossier
'gaps to add next' list.

Trump2 cabinet (8): Bondi (AG), KPatel (FBI), Gabbard (DNI), Hegseth
(Defense), RFKJr (HHS), Burgum (Interior), Vought (OMB - Project 2025
architect), McMahon (Education).

OLC/DOJ remainders (10): Bybee + Bradbury (OLC surveillance memo
lineage), Rosenstein (Bush2 -> Trump1 DAG), Breuer (Covington rotation),
JJohnson (Obama DHS), LLynch (Obama AG), Sessions (Trump1 AG),
Cipollone (Trump1 WH Counsel), JBClark (Trump1 DOJ Civil), Whitaker
(Trump1 acting AG).

Idempotent. Adds supporting institutions as needed (DHS, HHS, OMB,
Interior, PaulWeiss, IRS).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def wd(qid): return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}
def gov(url): return {"type": "gov-record", "url": url}
def off(url): return {"type": "official", "url": url}


NEW_INSTITUTIONS = [
    {"id": "DHS", "label": "US Department of Homeland Security", "sector": "gov",
     "sources": [w("United_States_Department_of_Homeland_Security"), off("https://www.dhs.gov/")]},
    {"id": "HHS", "label": "US Department of Health and Human Services", "sector": "gov",
     "sources": [w("United_States_Department_of_Health_and_Human_Services"), off("https://www.hhs.gov/")]},
    {"id": "Interior", "label": "US Department of the Interior", "sector": "gov",
     "sources": [w("United_States_Department_of_the_Interior"), off("https://www.doi.gov/")]},
    {"id": "Education", "label": "US Department of Education", "sector": "gov",
     "sources": [w("United_States_Department_of_Education"), off("https://www.ed.gov/")]},
    {"id": "PaulWeiss", "label": "Paul, Weiss, Rifkind, Wharton & Garrison", "sector": "tank",
     "sources": [w("Paul,_Weiss,_Rifkind,_Wharton_%26_Garrison"), off("https://www.paulweiss.com/")]},
    {"id": "USDA", "label": "US Department of Agriculture", "sector": "gov",
     "sources": [w("United_States_Department_of_Agriculture"), off("https://www.usda.gov/")]},
    {"id": "WWE", "label": "World Wrestling Entertainment", "sector": "tech",
     "sources": [w("WWE"), off("https://corporate.wwe.com/")]},
]

NEW_PERSONS = [
    # ---- Trump2 cabinet (just installed) -------------------------------
    {"id": "Bondi", "label": "Pam Bondi", "sector": "gov",
     "admin": ["trump1", "trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "Hillsborough County prosecutor -> Florida Attorney General 2011-19 -> Trump1 impeachment defense team -> America First Policy Institute -> US Attorney General 2025-",
     "sources": [w("Pam_Bondi"), wd("Q4126953"),
                 gov("https://www.justice.gov/ag/staff-profile/meet-attorney-general")]},
    {"id": "KPatel", "label": "Kash Patel", "sector": "intel",
     "admin": ["trump1", "trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "DOJ National Security Division -> House Intelligence Committee staff (Nunes investigation lead) -> NSC senior counterterrorism director -> DoD Chief of Staff (acting) -> FBI Director 2025-",
     "sources": [w("Kash_Patel"), wd("Q88497067"),
                 gov("https://www.fbi.gov/history/directors")]},
    {"id": "Gabbard", "label": "Tulsi Gabbard", "sector": "gov",
     "admin": ["trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "Hawaii state legislator -> Iraq War veteran -> US Representative HI-02 2013-21 -> Democratic presidential candidate 2020 -> Director of National Intelligence 2025-",
     "sources": [w("Tulsi_Gabbard"), wd("Q3543874"),
                 gov("https://www.dni.gov/index.php/who-we-are/leadership/director-of-national-intelligence")]},
    {"id": "Hegseth", "label": "Pete Hegseth", "sector": "def",
     "admin": ["trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "Princeton + Harvard Kennedy School -> Army National Guard officer (Iraq + Afghanistan) -> Concerned Veterans for America CEO -> Fox News weekend co-host -> US Secretary of Defense 2025-",
     "sources": [w("Pete_Hegseth"), wd("Q7174832"),
                 gov("https://www.defense.gov/About/Biographies/Biography/Article/4014657/")]},
    {"id": "RFKJr", "label": "Robert F. Kennedy Jr.", "sector": "gov",
     "admin": ["trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "Natural Resources Defense Council attorney -> Riverkeeper / Waterkeeper Alliance founder -> Children's Health Defense founder/chair -> presidential candidate 2024 -> US Secretary of Health and Human Services 2025-",
     "sources": [w("Robert_F._Kennedy_Jr."), wd("Q446196"),
                 gov("https://www.hhs.gov/about/leadership/index.html")]},
    {"id": "Burgum", "label": "Doug Burgum", "sector": "gov",
     "admin": ["trump2"], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "Great Plains Software CEO (sold to Microsoft 2001) -> Microsoft SVP -> SilverSquare investor -> Governor of North Dakota 2016-24 -> US Secretary of the Interior 2025-",
     "sources": [w("Doug_Burgum"), wd("Q5304148"),
                 gov("https://www.doi.gov/whoweare/secretary-doug-burgum")]},
    {"id": "Vought", "label": "Russell Vought", "sector": "gov",
     "admin": ["trump1", "trump2"], "networks": ["heritage"],
     "plays": ["pipeline"], "actors": ["blueprint"],
     "role": "Republican Study Committee policy director -> Heritage Action VP -> OMB Deputy Director -> OMB Director 2020-21 -> Center for Renewing America founder (Project 2025 contributor) -> OMB Director 2025-",
     "sources": [w("Russell_Vought"), wd("Q60713253"),
                 gov("https://www.whitehouse.gov/omb/")]},
    {"id": "McMahon", "label": "Linda McMahon", "sector": "gov",
     "admin": ["trump1", "trump2"], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "WWE co-founder + CEO 1980-2009 -> US Senate candidate (CT) -> Small Business Administration Administrator (Trump1) -> America First Policy Institute board -> US Secretary of Education 2025-",
     "sources": [w("Linda_McMahon"), wd("Q545876"),
                 gov("https://www.ed.gov/about/ed-overview/biographies-of-leadership/linda-mcmahon")]},

    # ---- OLC + DOJ remainders -------------------------------------------
    {"id": "Bybee", "label": "Jay Bybee", "sector": "judiciary",
     "admin": ["bush2"], "networks": ["federalist"],
     "plays": [], "actors": ["backdoor"],
     "role": "DOJ Office of Legal Counsel AAG 2001-03 (signed interrogation memos, public per FOIA) -> Ninth Circuit Court of Appeals 2003-",
     "sources": [w("Jay_Bybee"), wd("Q1685898"),
                 gov("https://www.justice.gov/d9/olc/legacy/2010/06/04/memo-bybee2002.pdf")]},
    {"id": "Bradbury", "label": "Steven Bradbury", "sector": "gov",
     "admin": ["bush2", "trump1", "trump2"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Kirkland & Ellis -> DOJ OLC Acting AAG 2005-09 -> Dechert partner -> Department of Transportation General Counsel (Trump1) -> Acting Deputy Secretary of Transportation 2025-",
     "sources": [w("Steven_G._Bradbury"), wd("Q3493957"),
                 gov("https://www.transportation.gov/meet-deputy")]},
    {"id": "Rosenstein", "label": "Rod Rosenstein", "sector": "gov",
     "admin": ["bush2", "trump1"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "DOJ Public Integrity Section -> US Attorney for Maryland 2005-17 -> Deputy Attorney General 2017-19 (appointed Mueller as Special Counsel) -> King & Spalding partner",
     "sources": [w("Rod_Rosenstein"), wd("Q22245090"),
                 gov("https://www.justice.gov/dag/staff-profile/former-deputy-attorney-general-rod-j-rosenstein")]},
    {"id": "Breuer", "label": "Lanny Breuer", "sector": "tank",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Covington & Burling -> Clinton White House Special Counsel -> Covington -> DOJ Criminal Division AAG 2009-13 -> Covington Vice Chair",
     "sources": [w("Lanny_Breuer"), wd("Q15047127"),
                 off("https://www.cov.com/en/professionals/b/lanny-breuer")]},
    {"id": "JJohnson", "label": "Jeh Johnson", "sector": "gov",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Paul Weiss partner -> Air Force General Counsel (Clinton) -> Paul Weiss -> DoD General Counsel (Obama) -> Secretary of Homeland Security 2013-17 -> Paul Weiss partner",
     "sources": [w("Jeh_Johnson"), wd("Q373517"),
                 gov("https://www.dhs.gov/person/jeh-charles-johnson")]},
    {"id": "LLynch", "label": "Loretta Lynch", "sector": "gov",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "US Attorney for EDNY -> Hogan Lovells partner -> US Attorney for EDNY (second term) -> US Attorney General 2015-17 -> Paul Weiss partner",
     "sources": [w("Loretta_Lynch"), wd("Q444899"),
                 gov("https://www.justice.gov/ag/bio/lynch-loretta-e")]},
    {"id": "Sessions", "label": "Jeff Sessions", "sector": "gov",
     "admin": ["trump1"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Attorney for SD Alabama -> Alabama AG -> US Senator (AL) 1997-2017 -> US Attorney General 2017-18 (recused from Russia investigation)",
     "sources": [w("Jeff_Sessions"), wd("Q170581"),
                 gov("https://www.justice.gov/ag/bio/sessions-jefferson-b-iii")]},
    {"id": "Whitaker", "label": "Matthew Whitaker", "sector": "gov",
     "admin": ["trump1", "trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Attorney for SD Iowa -> Foundation for Accountability and Civic Trust -> DOJ Chief of Staff -> Acting US Attorney General 2018-19 -> US Ambassador to NATO 2025-",
     "sources": [w("Matthew_Whitaker"), wd("Q31886011"),
                 gov("https://www.state.gov/biographies/matthew-whitaker/")]},
    {"id": "Cipollone", "label": "Pat Cipollone", "sector": "tank",
     "admin": ["bush1", "trump1"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Stigler clerk -> DOJ Office of the Solicitor General -> Kirkland & Ellis partner -> White House Counsel (Trump1) 2018-21 -> Ellis George Cipollone partner",
     "sources": [w("Pat_Cipollone"), wd("Q60803013"),
                 gov("https://trumpwhitehouse.archives.gov/people/pat-cipollone/")]},
    {"id": "JBClark", "label": "Jeffrey Bossert Clark", "sector": "tank",
     "admin": ["bush2", "trump1"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Kirkland & Ellis partner -> DOJ Environmental Division AAG (Bush2) -> Kirkland & Ellis -> DOJ Environment & Natural Resources Division AAG -> Acting DOJ Civil Division AAG 2020-21 (Trump1 final weeks)",
     "sources": [w("Jeffrey_Clark"), wd("Q104810636"),
                 gov("https://oig.justice.gov/sites/default/files/reports/24-009.pdf")]},
    {"id": "Bongino", "label": "Dan Bongino", "sector": "intel",
     "admin": ["trump2"], "networks": [],
     "plays": [], "actors": [],
     "role": "NYPD officer -> US Secret Service agent 1999-2011 -> conservative talk-radio host (The Dan Bongino Show) -> Fox News contributor -> FBI Deputy Director 2025-",
     "sources": [w("Dan_Bongino"), wd("Q5215207"),
                 gov("https://www.fbi.gov/history/directors")]},
]

NEW_EDGES = [
    # Trump2
    ("Bondi", "WhiteHouse"),
    ("KPatel", "FBI"), ("KPatel", "NSC"), ("KPatel", "DOJ_NSD"),
    ("Gabbard", "DNI"), ("Gabbard", "Senate"),
    ("Hegseth", "DoD"),
    ("RFKJr", "HHS"),
    ("Burgum", "Interior"), ("Burgum", "Microsoft"),
    ("Vought", "OMB"), ("Vought", "Heritage"),
    ("McMahon", "Education"), ("McMahon", "WWE"),
    # OLC/DOJ remainders
    ("Bybee", "DOJ_OLC"),
    ("Bradbury", "DOJ_OLC"), ("Bradbury", "KirklandEllis"),
    ("Rosenstein", "KingSpalding"),
    ("Breuer", "Covington"), ("Breuer", "WhiteHouse"),
    ("JJohnson", "PaulWeiss"), ("JJohnson", "DHS"), ("JJohnson", "DoD"),
    ("LLynch", "PaulWeiss"),
    ("Sessions", "Senate"),
    ("Whitaker", "State"),
    ("Cipollone", "WhiteHouse"), ("Cipollone", "KirklandEllis"), ("Cipollone", "OSG"),
    ("JBClark", "KirklandEllis"),
    ("Bongino", "FBI"),
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
