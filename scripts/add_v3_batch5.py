"""v3 batch 5: Twitter Files cohort + tech investors + WEF YGL alumni +
Asia-Pacific allied + Mossad leadership + cabinet remainders.

Twitter Files cohort (4): Yoel Roth (Twitter Head of T&S),
Vijaya Gadde (Twitter CLO), Parag Agrawal (Twitter CEO 2021-22),
Anika Collier Navaroli (Twitter Senior Policy).

Tech investors not yet in (4): Khosla, JDoerr (Kleiner), MMoritz
(Sequoia), RonConway (SV Angel).

WEF YGL alumni (4): JTrudeau (Canada PM), Ardern (NZ PM), Macron (FR
Pres), Kurz (Austria Chancellor).

Asia-Pacific allied (3): Albanese (AU PM), Luxon (NZ PM), Kishida (JP PM).

Mossad (2, Israel allied — Cohort E framework): Cohen + Barnea.

Liberal legal academy (2): Tribe (Harvard), Sullivan (Harvard Law).

Trump cabinet remainders (3): NHaley (UN), Pence (VP), WRoss (Commerce).
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
    {"id": "Kleiner", "label": "Kleiner Perkins", "sector": "fin",
     "sources": [w("Kleiner_Perkins"), off("https://www.kleinerperkins.com/")]},
    {"id": "Sequoia", "label": "Sequoia Capital", "sector": "fin",
     "sources": [w("Sequoia_Capital"), off("https://www.sequoiacap.com/")]},
    {"id": "SVAngel", "label": "SV Angel", "sector": "fin",
     "sources": [w("SV_Angel"), off("https://svangel.com/")]},
    {"id": "AUGov", "label": "Australian Government", "sector": "gov",
     "sources": [w("Government_of_Australia"), off("https://www.australia.gov.au/")]},
    {"id": "NZGov", "label": "New Zealand Government", "sector": "gov",
     "sources": [w("Government_of_New_Zealand"), off("https://www.govt.nz/")]},
    {"id": "JPGov", "label": "Japanese Government", "sector": "gov",
     "sources": [w("Government_of_Japan"), off("https://japan.kantei.go.jp/")]},
    {"id": "Mossad", "label": "Mossad (Israeli Foreign Intelligence)", "sector": "intel",
     "sources": [w("Mossad"), off("https://www.gov.il/he/departments/the_institute_for_intelligence_and_special_operations")]},
    {"id": "Match", "label": "Match Group", "sector": "tech",
     "sources": [w("Match_Group"), off("https://mtch.com/")]},
    {"id": "TBlock", "label": "Block, Inc. (formerly Square)", "sector": "fin",
     "sources": [w("Block,_Inc."), off("https://block.xyz/")]},
    {"id": "CanadaGov", "label": "Canadian Government", "sector": "gov",
     "sources": [w("Government_of_Canada"), off("https://www.canada.ca/")]},
    {"id": "FranceGov", "label": "French Government", "sector": "gov",
     "sources": [w("Government_of_France"), off("https://www.gouvernement.fr/")]},
]

NEW_PERSONS = [
    # ---- Twitter Files cohort -------------------------------------------
    {"id": "YRoth", "label": "Yoel Roth", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging", "algorithm"],
     "role": "Twitter Trust and Safety policy 2015-22 (Head of Trust and Safety in final months) -> University of Pennsylvania visiting scholar -> Match Group Head of Trust and Safety 2022-",
     "sources": [w("Yoel_Roth"), wd("Q113018919"),
                 gov("https://oversight.house.gov/hearing/the-twitter-files-part-ii/")]},
    {"id": "Gadde", "label": "Vijaya Gadde", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Wilson Sonsini -> Juniper Networks corporate counsel -> Twitter General Counsel 2011-13 -> Twitter Chief Legal Officer 2013-22",
     "sources": [w("Vijaya_Gadde"), wd("Q19362192"),
                 gov("https://oversight.house.gov/hearing/the-twitter-files-part-ii/")]},
    {"id": "Agrawal", "label": "Parag Agrawal", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm"],
     "role": "Stanford PhD -> Microsoft Research -> Twitter ML and revenue engineering -> Twitter CTO 2017-21 -> Twitter CEO 2021-22",
     "sources": [w("Parag_Agrawal"), wd("Q4351850"),
                 off("https://about.twitter.com/en/who-we-are/our-leadership")]},
    {"id": "Navaroli", "label": "Anika Collier Navaroli", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Stanford Internet Observatory researcher -> Twitter Senior Policy Official 2019-21 -> Stanford Cyber Policy Center -> McGraw Center for Business Journalism Senior Fellow",
     "sources": [w("Anika_Collier_Navaroli"), wd("Q116700681"),
                 gov("https://www.congress.gov/event/117th-congress/house-event/115204")]},

    # ---- Tech investors -------------------------------------------------
    {"id": "Khosla", "label": "Vinod Khosla", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "Sun Microsystems co-founder 1982 -> Kleiner Perkins partner -> Khosla Ventures founder 2004-",
     "sources": [w("Vinod_Khosla"), wd("Q3568049"),
                 off("https://www.khoslaventures.com/team/vinod-khosla/")]},
    {"id": "JDoerr", "label": "John Doerr", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Intel -> Kleiner Perkins partner 1980 -> Kleiner Perkins Chairman",
     "sources": [w("John_Doerr"), wd("Q1701167"),
                 off("https://www.kleinerperkins.com/people/john-doerr/")]},
    {"id": "MMoritz", "label": "Michael Moritz", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Time magazine journalist -> Sequoia Capital partner 1986 -> Sequoia Capital Chair 2012-23 -> Sequoia Heritage co-founder",
     "sources": [w("Michael_Moritz"), wd("Q314489"),
                 off("https://www.sequoiacap.com/people/michael-moritz/")]},
    {"id": "RonConway", "label": "Ron Conway", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Altos Computer Systems -> Personal Training Systems -> SV Angel founder 1994 (early investor in Google, Facebook, Twitter, Square, Airbnb, etc.)",
     "sources": [w("Ron_Conway"), wd("Q1597946"),
                 off("https://svangel.com/")]},

    # ---- WEF Young Global Leaders alumni in office ----------------------
    {"id": "JTrudeau", "label": "Justin Trudeau", "sector": "gov",
     "admin": [], "networks": ["wef-ygl"],
     "plays": [], "actors": [],
     "role": "Canadian Liberal MP -> Prime Minister of Canada 2015-25 -> WEF Young Global Leader alumni",
     "sources": [w("Justin_Trudeau"), wd("Q3099714"),
                 off("https://www.weforum.org/people/justin-trudeau/")]},
    {"id": "Ardern", "label": "Jacinda Ardern", "sector": "gov",
     "admin": [], "networks": ["wef-ygl"],
     "plays": [], "actors": ["flagging"],
     "role": "New Zealand Labour MP -> Prime Minister of New Zealand 2017-23 (initiated Christchurch Call multilateral content-moderation framework 2019) -> WEF YGL",
     "sources": [w("Jacinda_Ardern"), wd("Q333792"),
                 off("https://www.weforum.org/people/jacinda-ardern/")]},
    {"id": "Macron", "label": "Emmanuel Macron", "sector": "gov",
     "admin": [], "networks": ["wef-ygl", "bilderberg"],
     "plays": [], "actors": [],
     "role": "Rothschild & Co investment banker -> Hollande administration Deputy Secretary General -> French Minister of the Economy 2014-16 -> President of France 2017- -> WEF YGL",
     "sources": [w("Emmanuel_Macron"), wd("Q3052772"),
                 off("https://www.elysee.fr/emmanuel-macron")]},
    {"id": "Kurz", "label": "Sebastian Kurz", "sector": "gov",
     "admin": [], "networks": ["wef-ygl"],
     "plays": [], "actors": [],
     "role": "Austrian People's Party -> Foreign Minister of Austria -> Chancellor of Austria 2017-19, 2020-21 -> Thiel Capital senior advisor (per public Thiel Capital announcement) -> WEF YGL alumnus",
     "sources": [w("Sebastian_Kurz"), wd("Q2167053"),
                 off("https://www.weforum.org/people/sebastian-kurz/")]},

    # ---- Asia-Pacific allied --------------------------------------------
    {"id": "Albanese", "label": "Anthony Albanese", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Australian Labor MP -> Deputy Prime Minister (Rudd second term) -> Leader of the Opposition 2019-22 -> Prime Minister of Australia 2022-",
     "sources": [w("Anthony_Albanese"), wd("Q706142"),
                 off("https://www.pm.gov.au/")]},
    {"id": "Luxon", "label": "Christopher Luxon", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "Unilever marketing executive -> Air New Zealand CEO 2012-19 -> National Party MP -> Prime Minister of New Zealand 2023-",
     "sources": [w("Christopher_Luxon"), wd("Q105570404"),
                 off("https://www.beehive.govt.nz/minister/hon-christopher-luxon")]},
    {"id": "Kishida", "label": "Fumio Kishida", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Liberal Democratic Party MP -> Minister of Foreign Affairs 2012-17 -> LDP Policy Research Council Chair -> Prime Minister of Japan 2021-24",
     "sources": [w("Fumio_Kishida"), wd("Q1373317"),
                 off("https://japan.kantei.go.jp/101_kishida/profile.html")]},

    # ---- Mossad (Israel, Cohort E framework) ----------------------------
    {"id": "YCohen", "label": "Yossi Cohen", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy", "tap"],
     "role": "Mossad operative 1982-2011 -> Israeli National Security Council Head -> Mossad Director 2016-21 -> SoftBank Group Israel head 2022-",
     "sources": [w("Yossi_Cohen"), wd("Q26829987"),
                 off("https://www.gov.il/he/departments/the_institute_for_intelligence_and_special_operations")]},
    {"id": "Barnea", "label": "David Barnea", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy", "tap"],
     "role": "Mossad operative 1996- -> Mossad Deputy Director -> Mossad Director 2021-",
     "sources": [w("David_Barnea"), wd("Q107251330"),
                 off("https://www.gov.il/he/departments/the_institute_for_intelligence_and_special_operations")]},

    # ---- Liberal legal academy ------------------------------------------
    {"id": "Tribe", "label": "Laurence Tribe", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Harvard Law School Professor 1968- (Ralph S. Tyler Jr. Professor of Constitutional Law) -> ACS founding member -> argued Bush v. Gore (Gore side)",
     "sources": [w("Laurence_Tribe"), wd("Q1378395"),
                 off("https://hls.harvard.edu/faculty/laurence-h-tribe/")]},
    {"id": "KSullivan", "label": "Kathleen Sullivan", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Harvard Law professor -> Stanford Law School Dean 1999-2004 -> Quinn Emanuel partner",
     "sources": [w("Kathleen_Sullivan_(lawyer)"), wd("Q6376949"),
                 off("https://www.quinnemanuel.com/attorneys/sullivan-kathleen-m/")]},

    # ---- Trump cabinet remainders ---------------------------------------
    {"id": "NHaley", "label": "Nikki Haley", "sector": "gov",
     "admin": ["trump1"], "networks": [],
     "plays": [], "actors": ["embassy"],
     "role": "South Carolina State House -> Governor of South Carolina 2011-17 -> US Ambassador to the UN 2017-18 -> Boeing board (resigned 2024) -> 2024 Republican presidential candidate",
     "sources": [w("Nikki_Haley"), wd("Q455859"),
                 off("https://2017-2021.state.gov/biographies/nikki-r-haley/")]},
    {"id": "Pence", "label": "Mike Pence", "sector": "gov",
     "admin": ["trump1"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Representative (IN) -> Governor of Indiana 2013-17 -> Vice President of the United States 2017-21 -> Advancing American Freedom founder",
     "sources": [w("Mike_Pence"), wd("Q24313"),
                 off("https://trumpwhitehouse.archives.gov/people/mike-pence/")]},
    {"id": "WRoss", "label": "Wilbur Ross", "sector": "gov",
     "admin": ["trump1"], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "Rothschild Inc. private equity head -> WL Ross & Co. founder/Chairman -> US Secretary of Commerce 2017-21 -> WL Ross & Co.",
     "sources": [w("Wilbur_Ross"), wd("Q1418381"),
                 off("https://www.commerce.gov/news/blog/2021/01/farewell-message-secretary-wilbur-l-ross")]},
]

NEW_EDGES = [
    # Twitter Files
    ("YRoth", "X_Corp"), ("YRoth", "Match"),
    ("Gadde", "X_Corp"),
    ("Agrawal", "X_Corp"),
    ("Navaroli", "X_Corp"), ("Navaroli", "SIO"), ("Navaroli", "Stanford"),
    # Tech investors
    ("Khosla", "KhoslaVentures"),
    ("JDoerr", "Kleiner"),
    ("MMoritz", "Sequoia"),
    ("RonConway", "SVAngel"),
    # WEF YGL
    ("JTrudeau", "CanadaGov"), ("JTrudeau", "WEF"),
    ("Ardern", "NZGov"), ("Ardern", "WEF"),
    ("Macron", "FranceGov"), ("Macron", "WEF"),
    ("Kurz", "WEF"),
    # Asia-Pacific
    ("Albanese", "AUGov"),
    ("Luxon", "NZGov"),
    ("Kishida", "JPGov"),
    # Mossad
    ("YCohen", "Mossad"),
    ("Barnea", "Mossad"),
    # Liberal legal academy
    ("Tribe", "HarvardLaw"),
    ("KSullivan", "HarvardLaw"),
    # Trump cabinet
    ("NHaley", "UN"), ("NHaley", "Boeing"),
    ("Pence", "WhiteHouse"),
    ("WRoss", "WhiteHouse"),
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
