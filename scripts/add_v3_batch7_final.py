"""v3 batch 7: final high-leverage adds to close the v3 cohort.

Disinformation-studies academics (4): Donovan (TASM Harvard -> BU),
JTucker (NYU CSMaP), PHoward (Oxford OII), Menczer (Indiana Observatory
on Social Media).

Senate Intel / Commerce key (3): Warner (Senate Intel Chair), Cotton
(Intel), Cantwell (Commerce Chair).

WEF inner circle + OSF leadership (3): Brende (WEF President, CFR
former), Neier (OSF founding director), Soros Jr (Alex Soros, OSF Chair
2023-).

More UK / EU heads (3): Truss, Sunak, Meloni.

DC think-tank presidents (4): Hamre (CSIS), JAllen (Brookings),
MRich (RAND), Hadley (Atlantic Council/USIP).

Climate / multilateral (2): Figueres (UNFCCC Exec Sec, Paris Accord),
Kerry already in.

Twitter Files / disinfo platform peers (2): JDonovan covered above;
add AStone (Meta comms VP), JJohnson (Pinterest T&S — different
JJohnson from DHS Sec, so this is jvjohnson distinct id).

Adds ~20 persons.
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
def gov(url): return {"type": "gov-record", "url": url}


NEW_INSTITUTIONS = [
    {"id": "BU", "label": "Boston University", "sector": "tank",
     "sources": [w("Boston_University"), off("https://www.bu.edu/")]},
    {"id": "NYU_CSMaP", "label": "NYU Center for Social Media and Politics", "sector": "tank",
     "sources": [w("New_York_University"), off("https://csmapnyu.org/")]},
    {"id": "OII", "label": "Oxford Internet Institute", "sector": "tank",
     "sources": [w("Oxford_Internet_Institute"), off("https://www.oii.ox.ac.uk/")]},
    {"id": "OSoMe", "label": "Indiana Observatory on Social Media", "sector": "tank",
     "sources": [w("Indiana_University_Bloomington"), off("https://osome.iu.edu/")]},
    {"id": "CSIS", "label": "Center for Strategic and International Studies", "sector": "tank",
     "sources": [w("Center_for_Strategic_and_International_Studies"), off("https://www.csis.org/")]},
    {"id": "Brookings", "label": "Brookings Institution", "sector": "tank",
     "sources": [w("Brookings_Institution"), off("https://www.brookings.edu/")]},
    {"id": "RAND", "label": "RAND Corporation", "sector": "tank",
     "sources": [w("RAND_Corporation"), off("https://www.rand.org/")]},
    {"id": "USIP", "label": "United States Institute of Peace", "sector": "tank",
     "sources": [w("United_States_Institute_of_Peace"), off("https://www.usip.org/")]},
    {"id": "UNFCCC", "label": "UN Framework Convention on Climate Change", "sector": "multi",
     "sources": [w("United_Nations_Framework_Convention_on_Climate_Change"), off("https://unfccc.int/")]},
    {"id": "Pinterest", "label": "Pinterest", "sector": "tech",
     "sources": [w("Pinterest"), off("https://newsroom.pinterest.com/leadership")]},
]


NEW_PERSONS = [
    # ---- Disinformation-studies academics ---------------------------------
    {"id": "JDonovan", "label": "Joan Donovan", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "UCSD Comm doctoral work -> Data & Society Research Institute Director of the Disinformation Action Lab -> Harvard Shorenstein Center Director of Technology and Social Change Research Project 2019-23 -> Boston University Assistant Professor of Journalism and Emerging Media",
     "sources": [w("Joan_Donovan"), wd("Q67079081"),
                 off("https://www.bu.edu/com/profile/joan-donovan/")]},
    {"id": "JTucker", "label": "Joshua Tucker", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Princeton PhD -> Rutgers + NYU Politics professor -> NYU Center for Social Media and Politics co-founder/co-director 2017-",
     "sources": [w("Joshua_Tucker"), wd("Q98760583"),
                 off("https://csmapnyu.org/team/joshua-tucker")]},
    {"id": "PHoward", "label": "Philip N. Howard", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Washington Information School -> Central European University -> Oxford Internet Institute Director 2018-21 -> University of Oxford Professor of Internet Studies",
     "sources": [w("Philip_N._Howard"), wd("Q15457027"),
                 off("https://www.oii.ox.ac.uk/people/profiles/philip-howard/")]},
    {"id": "Menczer", "label": "Filippo Menczer", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "flagging"],
     "role": "Indiana University Bloomington Luddy School of Informatics professor -> Observatory on Social Media (OSoMe) founder/director",
     "sources": [w("Filippo_Menczer"), wd("Q21337942"),
                 off("https://cnets.indiana.edu/fil/")]},

    # ---- Senate Intel / Commerce ------------------------------------------
    {"id": "Warner", "label": "Mark Warner", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["acquisition"], "actors": ["tap", "blueprint"],
     "role": "Columbia Capital co-founder (telecom investing) -> Governor of Virginia 2002-06 -> US Senator (VA) 2009- -> Senate Intelligence Committee Chair 2021-",
     "sources": [w("Mark_Warner"), wd("Q447049"),
                 gov("https://bioguide.congress.gov/search/bio/W000805")]},
    {"id": "Cotton", "label": "Tom Cotton", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy"],
     "role": "US Army officer (Iraq + Afghanistan) -> Gibson Dunn associate -> US Representative -> US Senator (AR) 2015- -> Senate Intelligence Committee",
     "sources": [w("Tom_Cotton"), wd("Q4527432"),
                 gov("https://bioguide.congress.gov/search/bio/C001095")]},
    {"id": "Cantwell", "label": "Maria Cantwell", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "blueprint"],
     "role": "RealNetworks SVP marketing -> US Senator (WA) 2001- -> Senate Commerce Committee Chair 2021-",
     "sources": [w("Maria_Cantwell"), wd("Q458438"),
                 gov("https://bioguide.congress.gov/search/bio/C000127")]},

    # ---- WEF / OSF leadership -------------------------------------------
    {"id": "Brende", "label": "Borge Brende", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Norwegian Minister of the Environment, Trade and Industry, Foreign Affairs -> World Economic Forum President 2017-",
     "sources": [w("B%C3%B8rge_Brende"), wd("Q1052478"),
                 off("https://www.weforum.org/people/borge-brende/")]},
    {"id": "Neier", "label": "Aryeh Neier", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "ACLU Executive Director 1970-78 -> Helsinki Watch founder (later Human Rights Watch) 1978 -> Open Society Institute President 1993-2012 -> OSF President Emeritus",
     "sources": [w("Aryeh_Neier"), wd("Q4795920"),
                 off("https://www.opensocietyfoundations.org/voices/contributors/aryeh-neier")]},
    {"id": "ASoros", "label": "Alex Soros", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Open Society Foundations Deputy Chair -> Open Society Foundations Chair 2023- -> Soros Fund Management board",
     "sources": [w("Alexander_Soros"), wd("Q3611005"),
                 off("https://www.opensocietyfoundations.org/who-we-are/leadership/alex-soros")]},

    # ---- More UK / EU heads ---------------------------------------------
    {"id": "Truss", "label": "Liz Truss", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Conservative MP -> Secretary of State for International Trade -> Foreign Secretary -> Prime Minister of the UK 2022 (45 days)",
     "sources": [w("Liz_Truss"), wd("Q220511"),
                 off("https://www.gov.uk/government/people/elizabeth-truss")]},
    {"id": "Sunak", "label": "Rishi Sunak", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Goldman Sachs analyst -> TCI Fund Management -> Theleme Partners -> Conservative MP -> Chancellor of the Exchequer 2020-22 -> Prime Minister of the UK 2022-24",
     "sources": [w("Rishi_Sunak"), wd("Q22245690"),
                 off("https://www.gov.uk/government/people/rishi-sunak")]},
    {"id": "Meloni", "label": "Giorgia Meloni", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Italian Social Movement youth activist -> Brothers of Italy co-founder + leader -> Prime Minister of Italy 2022-",
     "sources": [w("Giorgia_Meloni"), wd("Q1428033"),
                 off("https://www.governo.it/it/presidente")]},

    # ---- DC think-tank presidents ---------------------------------------
    {"id": "Hamre", "label": "John Hamre", "sector": "tank",
     "admin": ["clinton"], "networks": ["cfr"],
     "plays": ["pipeline"], "actors": [],
     "role": "Senate Armed Services Committee staff -> Deputy Secretary of Defense 1997-99 -> CSIS President + CEO 2000-",
     "sources": [w("John_J._Hamre"), wd("Q3179727"),
                 off("https://www.csis.org/people/john-j-hamre")]},
    {"id": "JAllen", "label": "John R. Allen", "sector": "tank",
     "admin": ["bush2", "obama"], "networks": [],
     "plays": ["backstop"], "actors": [],
     "role": "USMC General -> Commander US Forces Afghanistan 2011-13 -> Special Presidential Envoy for the Global Coalition to Counter ISIL 2014-15 -> Brookings Institution President 2017-22 (resigned amid investigation per Brookings statement)",
     "sources": [w("John_R._Allen"), wd("Q1697220"),
                 off("https://www.brookings.edu/articles/")]},
    {"id": "MRich", "label": "Michael Rich", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "RAND Corporation analyst -> RAND President + CEO 2011-",
     "sources": [w("RAND_Corporation"), wd("Q119089007"),
                 off("https://www.rand.org/about/management/rich.html")]},
    {"id": "Hadley", "label": "Stephen Hadley", "sector": "tank",
     "admin": ["bush2"], "networks": ["cfr"],
     "plays": ["pipeline"], "actors": ["embassy"],
     "role": "Shea & Gardner -> DoD Counsel -> Assistant to the President for National Security Affairs 2005-09 -> Atlantic Council Board -> US Institute of Peace Chair 2013-21 -> Rice, Hadley, Gates & Manuel LLC",
     "sources": [w("Stephen_Hadley"), wd("Q1325014"),
                 off("https://www.atlanticcouncil.org/expert/stephen-j-hadley/")]},

    # ---- Climate / multilateral -----------------------------------------
    {"id": "Figueres", "label": "Christiana Figueres", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Costa Rican delegation to UNFCCC -> UNFCCC Executive Secretary 2010-16 (oversaw Paris Agreement) -> Global Optimism co-founder",
     "sources": [w("Christiana_Figueres"), wd("Q462543"),
                 off("https://unfccc.int/news/christiana-figueres-receives-german-environmental-award")]},

    # ---- Platform T&S / comms ---------------------------------------------
    {"id": "AStone", "label": "Andy Stone", "sector": "tech",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "Senate Democratic policy comms -> Obama 2012 campaign communications -> White House communications -> Meta Communications policy lead 2014-",
     "sources": [w("Meta_Platforms"), wd("Q104853842"),
                 off("https://about.meta.com/")]},
]


NEW_EDGES = [
    # Disinfo academics
    ("JDonovan", "BU"),
    ("JTucker", "NYU_CSMaP"),
    ("PHoward", "OII"),
    ("Menczer", "OSoMe"),
    # Senate Intel/Commerce
    ("Warner", "Senate"),
    ("Cotton", "Senate"),
    ("Cantwell", "Senate"),
    # WEF / OSF
    ("Brende", "WEF"),
    ("Neier", "OSF"),
    ("ASoros", "OSF"),
    # UK / EU
    ("Truss", "UKGov"),
    ("Sunak", "UKGov"), ("Sunak", "Goldman"),
    # Meloni — Italian Government not yet an institution; skip institutional edge
    # DC think-tank
    ("Hamre", "CSIS"), ("Hamre", "DoD"),
    ("JAllen", "Brookings"), ("JAllen", "DoD"),
    ("MRich", "RAND"),
    ("Hadley", "USIP"), ("Hadley", "AtlanticCouncil"), ("Hadley", "NSC"),
    # Climate
    ("Figueres", "UNFCCC"), ("Figueres", "UN"),
    # Platform comms
    ("AStone", "Meta"), ("AStone", "WhiteHouse"),
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
