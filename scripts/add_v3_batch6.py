"""v3 batch 6: cluster-completing additions.

Federalist Society architects (5): Calabresi (co-founder 1982), Whelan
(EPPC), Mitchell (election law), vonSpakovsky (Heritage), Spalding (Heritage).

AI startups completing the council (3): Sutskever, Brockman, Murati.
Plus LeCun (Meta AI Chief Scientist) to round AI policy council.

Hedge fund kings (5): Dalio, Griffin, SCohen (Point72/SAC),
Singer (Elliott), Loeb (Third Point).

Private equity titans (3): LBlack (Apollo), HKravis (KKR), GRoberts
(KKR) -- distinct from Roberts (Chief Justice already in).

Media moguls (3): RMurdoch, LMurdoch, AWintour.

Big Tech remaining (3): Catz (Oracle), Sweeney (Epic), SJobs (Apple
founder, historical).

Major political donor (1): TSteyer (Farallon, climate, 2020 candidate).

Total: 23 persons + 16 supporting institutions.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def wd(qid): return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}
def off(url): return {"type": "official", "url": url}
def acad(url): return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    # Hedge funds + PE
    {"id": "Bridgewater", "label": "Bridgewater Associates", "sector": "fin",
     "sources": [w("Bridgewater_Associates"), off("https://www.bridgewater.com/")]},
    {"id": "Citadel", "label": "Citadel LLC", "sector": "fin",
     "sources": [w("Citadel_LLC"), off("https://www.citadel.com/")]},
    {"id": "Point72", "label": "Point72 Asset Management", "sector": "fin",
     "sources": [w("Point72_Asset_Management"), off("https://point72.com/")]},
    {"id": "Elliott", "label": "Elliott Investment Management", "sector": "fin",
     "sources": [w("Elliott_Investment_Management"), off("https://www.elliottmgmt.com/")]},
    {"id": "ThirdPoint", "label": "Third Point LLC", "sector": "fin",
     "sources": [w("Third_Point_Management"), off("https://www.thirdpoint.com/")]},
    {"id": "Apollo", "label": "Apollo Global Management", "sector": "fin",
     "sources": [w("Apollo_Global_Management"), off("https://www.apolloglobal.com/")]},
    {"id": "Farallon", "label": "Farallon Capital Management", "sector": "fin",
     "sources": [w("Farallon_Capital"), off("https://www.faralloncapital.com/")]},
    # Conservative legal
    {"id": "EPPC", "label": "Ethics and Public Policy Center", "sector": "tank",
     "sources": [w("Ethics_and_Public_Policy_Center"), off("https://eppc.org/")]},
    {"id": "NorthwesternLaw", "label": "Northwestern University Pritzker School of Law",
     "sector": "tank",
     "sources": [w("Northwestern_University_Pritzker_School_of_Law"),
                 off("https://www.law.northwestern.edu/")]},
    # Media
    {"id": "NewsCorp", "label": "News Corp", "sector": "tech",
     "sources": [w("News_Corp"), off("https://newscorp.com/")]},
    {"id": "FoxCorp", "label": "Fox Corporation", "sector": "tech",
     "sources": [w("Fox_Corporation"), off("https://www.foxcorporation.com/")]},
    {"id": "CondeNast", "label": "Conde Nast", "sector": "tech",
     "sources": [w("Cond%C3%A9_Nast"), off("https://www.condenast.com/")]},
    # Tech
    {"id": "Oracle", "label": "Oracle Corporation", "sector": "tech",
     "sources": [w("Oracle_Corporation"), off("https://www.oracle.com/")]},
    {"id": "EpicGames", "label": "Epic Games", "sector": "tech",
     "sources": [w("Epic_Games"), off("https://www.epicgames.com/")]},
    # AI institutions
    {"id": "ThinkingMachines", "label": "Thinking Machines (Murati lab)", "sector": "tech",
     "sources": [w("Thinking_Machines_Lab"), off("https://thinkingmachines.lab/")]},
    # Heritage Center for Renewing America connection
    {"id": "HeritageElectionLaw", "label": "Heritage Foundation Election Law Reform Initiative",
     "sector": "tank",
     "sources": [w("The_Heritage_Foundation"), off("https://www.heritage.org/election-integrity")]},
]


NEW_PERSONS = [
    # ---- Federalist Society architects + conservative legal ---------------
    {"id": "Calabresi", "label": "Steven Calabresi", "sector": "tank",
     "admin": ["reagan"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": ["blueprint"],
     "role": "Bork clerk -> Reagan White House Counsel's Office -> Federalist Society co-founder 1982 -> Northwestern Pritzker School of Law Professor",
     "sources": [w("Steven_Calabresi"), wd("Q7613015"),
                 off("https://www.law.northwestern.edu/faculty/profiles/StevenCalabresi/")]},
    {"id": "Whelan", "label": "Ed Whelan", "sector": "tank",
     "admin": ["bush2"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Scalia clerk -> DOJ Office of Legal Counsel Principal Deputy AAG (Bush2) -> Ethics and Public Policy Center President 2004-19 -> EPPC Antonin Scalia Chair in Constitutional Studies",
     "sources": [w("Ed_Whelan_(legal_commentator)"), wd("Q5337081"),
                 off("https://eppc.org/author/edward-whelan/")]},
    {"id": "CMitchell", "label": "Cleta Mitchell", "sector": "tank",
     "admin": [], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Oklahoma House of Representatives -> Foley & Lardner partner -> election-law attorney; chair of Public Interest Legal Foundation board; Conservative Partnership Institute Election Integrity Network",
     "sources": [w("Cleta_Mitchell"), wd("Q5132580"),
                 off("https://cpi.org/team/cleta-mitchell-esq/")]},
    {"id": "VonSpakovsky", "label": "Hans von Spakovsky", "sector": "tank",
     "admin": ["bush2"], "networks": ["heritage", "federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "DOJ Civil Rights Division counsel -> Federal Election Commission Commissioner 2006-07 -> Heritage Foundation Manager Election Law Reform Initiative + Senior Legal Fellow",
     "sources": [w("Hans_von_Spakovsky"), wd("Q5645940"),
                 off("https://www.heritage.org/staff/hans-von-spakovsky")]},
    {"id": "Spalding", "label": "Matthew Spalding", "sector": "tank",
     "admin": [], "networks": ["heritage"],
     "plays": [], "actors": [],
     "role": "Hillsdale College Allan P. Kirby Jr. Center for Constitutional Studies and Citizenship Dean -> Heritage Foundation Vice President for American Studies + B. Kenneth Simon Center Director",
     "sources": [w("Matthew_Spalding"), wd("Q104853898"),
                 off("https://www.heritage.org/staff/matthew-spalding")]},

    # ---- AI council completion -------------------------------------------
    {"id": "Sutskever", "label": "Ilya Sutskever", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "U Toronto AI research (Hinton lab) -> Google Brain -> OpenAI co-founder + Chief Scientist 2015-24 -> Safe Superintelligence Inc. co-founder 2024-",
     "sources": [w("Ilya_Sutskever"), wd("Q19834590"),
                 off("https://ssi.inc/")]},
    {"id": "Brockman", "label": "Greg Brockman", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "Stripe CTO 2010-15 -> OpenAI co-founder 2015 -> OpenAI CTO -> OpenAI President 2017-",
     "sources": [w("Greg_Brockman"), wd("Q104853841"),
                 off("https://openai.com/our-structure/")]},
    {"id": "Murati", "label": "Mira Murati", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "Goldman Sachs analyst -> Tesla Model X program lead -> Leap Motion VP -> OpenAI VP -> OpenAI CTO 2022-24 -> Thinking Machines founder/CEO 2024-",
     "sources": [w("Mira_Murati"), wd("Q113018917"),
                 off("https://thinkingmachines.lab/")]},
    {"id": "LeCun", "label": "Yann LeCun", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "Bell Labs AI research -> NYU professor -> Meta Vice President + Chief AI Scientist 2013- -> Turing Award 2018",
     "sources": [w("Yann_LeCun"), wd("Q1929300"),
                 off("https://about.meta.com/realitylabs/research/")]},

    # ---- Hedge fund kings ------------------------------------------------
    {"id": "Dalio", "label": "Ray Dalio", "sector": "fin",
     "admin": [], "networks": ["cfr"],
     "plays": [], "actors": [],
     "role": "Shearson Hayden Stone -> Bridgewater Associates founder 1975 -> Bridgewater CIO 1985-2022 -> Bridgewater Chairman",
     "sources": [w("Ray_Dalio"), wd("Q466596"),
                 off("https://www.principles.com/about-ray-dalio/")]},
    {"id": "Griffin", "label": "Ken Griffin", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Glenwood Capital -> Citadel LLC founder 1990 -> Citadel CEO; Citadel Securities founder/CEO",
     "sources": [w("Ken_Griffin_(financier)"), wd("Q3024570"),
                 off("https://www.citadel.com/about-us/our-leaders/ken-griffin/")]},
    {"id": "SCohen", "label": "Steven A. Cohen", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Gruntal & Co. -> SAC Capital Advisors founder 1992 (SAC pled guilty to insider trading 2013 per court record) -> Point72 Asset Management founder 2014",
     "sources": [w("Steven_A._Cohen"), wd("Q325077"),
                 off("https://point72.com/about/")]},
    {"id": "Singer", "label": "Paul Singer", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Donaldson, Lufkin & Jenrette -> Elliott Management Corporation founder 1977",
     "sources": [w("Paul_Singer_(businessman)"), wd("Q7150836"),
                 off("https://www.elliottmgmt.com/")]},
    {"id": "Loeb", "label": "Daniel S. Loeb", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Jefferies & Co. -> Citigroup distressed debt -> Third Point LLC founder 1995/CEO",
     "sources": [w("Daniel_S._Loeb"), wd("Q5217672"),
                 off("https://www.thirdpoint.com/")]},

    # ---- Private equity titans -------------------------------------------
    {"id": "LBlack", "label": "Leon Black", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Drexel Burnham Lambert M&A head -> Apollo Global Management co-founder 1990/CEO -> Apollo Chairman 2009-21 (stepped down 2021 per Apollo board statement)",
     "sources": [w("Leon_Black"), wd("Q6524022"),
                 off("https://www.apolloglobal.com/")]},
    {"id": "HKravis", "label": "Henry Kravis", "sector": "fin",
     "admin": [], "networks": ["cfr"],
     "plays": [], "actors": [],
     "role": "Bear Stearns -> KKR co-founder 1976 -> KKR Co-Chairman/Co-CEO until 2021",
     "sources": [w("Henry_Kravis"), wd("Q1276720"),
                 off("https://www.kkr.com/about/our-leadership/henry-r-kravis")]},
    {"id": "GRoberts", "label": "George R. Roberts", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Bear Stearns -> KKR co-founder 1976 -> KKR Co-Chairman/Co-CEO until 2021",
     "sources": [w("George_R._Roberts"), wd("Q5544143"),
                 off("https://www.kkr.com/about/our-leadership/george-r-roberts")]},

    # ---- Media moguls -----------------------------------------------------
    {"id": "RMurdoch", "label": "Rupert Murdoch", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "News Limited (Australia) -> News Corporation founder/Chairman/CEO 1979-2013 -> 21st Century Fox -> News Corp + Fox Corporation Chairman (stepped down 2023)",
     "sources": [w("Rupert_Murdoch"), wd("Q103476"),
                 off("https://newscorp.com/about/leadership/")]},
    {"id": "LMurdoch", "label": "Lachlan Murdoch", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "News Limited (Australia) Deputy CEO -> News Corp Co-Chair -> Fox Corporation Chair + CEO 2019-",
     "sources": [w("Lachlan_Murdoch"), wd("Q1077041"),
                 off("https://www.foxcorporation.com/about/")]},
    {"id": "AWintour", "label": "Anna Wintour", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Harper's & Queen -> New York magazine -> Vogue Editor-in-Chief 1988- -> Conde Nast Artistic Director 2013- -> Conde Nast Global Chief Content Officer 2020-",
     "sources": [w("Anna_Wintour"), wd("Q229695"),
                 off("https://www.condenast.com/leadership")]},

    # ---- Big Tech remaining ----------------------------------------------
    {"id": "Catz", "label": "Safra Catz", "sector": "tech",
     "admin": ["trump1"], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "Donaldson, Lufkin & Jenrette banker -> Oracle Executive Vice President 1999 -> Oracle Co-CEO 2014-19 -> Oracle CEO 2019- -> Trump1 Defense Innovation Board",
     "sources": [w("Safra_Catz"), wd("Q444762"),
                 off("https://www.oracle.com/corporate/board-of-directors/")]},
    {"id": "Sweeney", "label": "Tim Sweeney", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Epic Games founder 1991/CEO (Unreal Engine, Fortnite); plaintiff in Epic Games v. Apple antitrust case per court record",
     "sources": [w("Tim_Sweeney_(game_developer)"), wd("Q1788540"),
                 off("https://www.epicgames.com/site/en-US/about")]},
    {"id": "SJobs", "label": "Steve Jobs", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Apple co-founder 1976 -> Apple CEO 1977-85, 1997-2011 -> NeXT founder/CEO -> Pixar majority owner -> Disney board (post-Pixar sale)",
     "sources": [w("Steve_Jobs"), wd("Q19837"),
                 off("https://www.apple.com/leadership/")]},

    # ---- Major political donor pre-Trump2 -------------------------------
    {"id": "TSteyer", "label": "Tom Steyer", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Goldman Sachs -> Hellman & Friedman -> Farallon Capital Management founder 1986 -> Farallon Managing Partner until 2012 -> NextGen America founder -> 2020 Democratic presidential candidate",
     "sources": [w("Tom_Steyer"), wd("Q1331009"),
                 off("https://nextgenamerica.org/")]},
]


NEW_EDGES = [
    # Federalist Society architects
    ("Calabresi", "FederalistSociety"), ("Calabresi", "NorthwesternLaw"), ("Calabresi", "WhiteHouse"),
    ("Whelan", "EPPC"), ("Whelan", "DOJ_OLC"),
    ("CMitchell", "FederalistSociety"),
    ("VonSpakovsky", "Heritage"), ("VonSpakovsky", "FederalistSociety"),
    ("Spalding", "Heritage"),
    # AI council
    ("Sutskever", "OpenAI"), ("Sutskever", "Google"),
    ("Brockman", "OpenAI"),
    ("Murati", "OpenAI"), ("Murati", "ThinkingMachines"), ("Murati", "Tesla"),
    ("LeCun", "Meta"),
    # Hedge funds
    ("Dalio", "Bridgewater"),
    ("Griffin", "Citadel"),
    ("SCohen", "Point72"),
    ("Singer", "Elliott"),
    ("Loeb", "ThirdPoint"),
    # PE
    ("LBlack", "Apollo"),
    ("HKravis", "KKR"),
    ("GRoberts", "KKR"),
    # Media
    ("RMurdoch", "NewsCorp"), ("RMurdoch", "FoxCorp"),
    ("LMurdoch", "NewsCorp"), ("LMurdoch", "FoxCorp"),
    ("AWintour", "CondeNast"),
    # Tech
    ("Catz", "Oracle"),
    ("Sweeney", "EpicGames"),
    ("SJobs", "Apple"),
    # Steyer
    ("TSteyer", "Farallon"), ("TSteyer", "Goldman"),
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
