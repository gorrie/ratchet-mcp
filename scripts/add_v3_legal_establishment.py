"""v3 legal establishment drain: ~23 named persons across the US legal
infrastructure that operates the control grid's legal substrate.

Conservative legal architecture: Meese (founder of conservative legal
movement), Leo (Federalist Society Co-Chair / Marble Freedom Trust),
EScalia, Yoo + Addington (Bush2 OLC torture / surveillance memo
authors — documented institutional positions only, no motive imputation).

Obama / Biden legal apparatus: Monaco (DAG x2), Yates, Garland,
McCord (DOJ NSD -> Georgetown ICAP).

Prosecutor / special counsel circuit: Durham, Comey, Weissmann, JSmith.

Solicitors General: TOlson, Verrilli, NFrancisco, Prelogar.

Tech general counsels: BSmith (Microsoft President), Walker (Google GC).

Other: MHorowitz (DOJ IG), Bauer (Obama WH Counsel + Perkins Coie),
McGahn (Trump1 WH Counsel + Jones Day).

Idempotent. Adds supporting institutions (Heritage, DOJ NSD, OSG,
Marble Freedom Trust, JonesDay, GibsonDunn, MungerTolles, KingSpalding,
ICAP, BerkeleyLaw, NYULaw).
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
def acad(url): return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    {"id": "Heritage", "label": "Heritage Foundation", "sector": "tank",
     "sources": [w("The_Heritage_Foundation"), off("https://www.heritage.org/")]},
    {"id": "DOJ_NSD", "label": "DOJ National Security Division", "sector": "intel",
     "sources": [w("National_Security_Division"), off("https://www.justice.gov/nsd")]},
    {"id": "DOJ_OLC", "label": "DOJ Office of Legal Counsel", "sector": "gov",
     "sources": [w("Office_of_Legal_Counsel"), off("https://www.justice.gov/olc")]},
    {"id": "OSG", "label": "Office of the Solicitor General", "sector": "gov",
     "sources": [w("United_States_Solicitor_General"), off("https://www.justice.gov/osg")]},
    {"id": "MarbleFreedomTrust", "label": "Marble Freedom Trust", "sector": "tank",
     "sources": [w("Marble_Freedom_Trust"),
                 gov("https://efile.fara.gov/docs/7136-Exhibit-AB-20211101-22.pdf")]},
    {"id": "JonesDay", "label": "Jones Day", "sector": "tank",
     "sources": [w("Jones_Day"), off("https://www.jonesday.com/")]},
    {"id": "GibsonDunn", "label": "Gibson, Dunn & Crutcher", "sector": "tank",
     "sources": [w("Gibson,_Dunn_%26_Crutcher"), off("https://www.gibsondunn.com/")]},
    {"id": "MungerTolles", "label": "Munger, Tolles & Olson", "sector": "tank",
     "sources": [w("Munger,_Tolles_%26_Olson"), off("https://www.mto.com/")]},
    {"id": "KingSpalding", "label": "King & Spalding", "sector": "tank",
     "sources": [w("King_%26_Spalding"), off("https://www.kslaw.com/")]},
    {"id": "ICAP", "label": "Georgetown Institute for Constitutional Advocacy and Protection",
     "sector": "tank",
     "sources": [w("Mary_McCord"), off("https://www.law.georgetown.edu/icap/")]},
    {"id": "BerkeleyLaw", "label": "UC Berkeley School of Law", "sector": "tank",
     "sources": [w("UC_Berkeley_School_of_Law"), off("https://www.law.berkeley.edu/")]},
    {"id": "NYULaw", "label": "NYU School of Law", "sector": "tank",
     "sources": [w("New_York_University_School_of_Law"), off("https://www.law.nyu.edu/")]},
    {"id": "FBI", "label": "Federal Bureau of Investigation", "sector": "intel",
     "sources": [w("Federal_Bureau_of_Investigation"), off("https://www.fbi.gov/")]},
]

NEW_PERSONS = [
    # ---- Conservative legal architecture ---------------------------------
    {"id": "Meese", "label": "Edwin Meese III", "sector": "gov",
     "admin": ["reagan"], "networks": ["heritage", "federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Reagan California Chief of Staff -> White House Counselor 1981-85 -> US Attorney General 1985-88 -> Heritage Foundation Ronald Reagan Distinguished Fellow",
     "sources": [w("Edwin_Meese"), wd("Q314378"),
                 gov("https://www.justice.gov/ag/bio/meese-edwin-iii")]},
    {"id": "Leo", "label": "Leonard Leo", "sector": "tank",
     "admin": [], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": ["blueprint"],
     "role": "Federalist Society Executive Vice President 1991-2020 -> Federalist Society Co-Chairman 2020- -> Marble Freedom Trust Trustee (~$1.6B donor-advised vehicle per IRS filings)",
     "sources": [w("Leonard_Leo"), wd("Q6526009"),
                 gov("https://efile.fara.gov/docs/7136-Exhibit-AB-20211101-22.pdf")]},
    {"id": "EScalia", "label": "Eugene Scalia", "sector": "gov",
     "admin": ["bush2", "trump1"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Gibson Dunn partner -> Department of Labor Solicitor 2002-03 -> Gibson Dunn -> Secretary of Labor 2019-21 -> Gibson Dunn",
     "sources": [w("Eugene_Scalia"), wd("Q5407249"),
                 gov("https://www.dol.gov/agencies/oasam/secretarys-office")]},
    {"id": "Yoo", "label": "John Yoo", "sector": "gov",
     "admin": ["bush2"], "networks": ["aei", "federalist"],
     "plays": [], "actors": ["tap", "watchers", "backdoor"],
     "role": "DOJ Office of Legal Counsel Deputy Assistant Attorney General 2001-03 (authored interrogation + surveillance memos, public per court FOIA releases) -> UC Berkeley School of Law Professor -> AEI Visiting Scholar",
     "sources": [w("John_Yoo"), wd("Q1701418"),
                 gov("https://www.justice.gov/d9/olc/legacy/2009/08/24/memo-warrantlessurveillance.pdf")]},
    {"id": "Addington", "label": "David Addington", "sector": "gov",
     "admin": ["reagan", "bush1", "bush2"], "networks": ["heritage"],
     "plays": [], "actors": ["tap", "watchers", "backdoor"],
     "role": "CIA Assistant General Counsel -> DoD General Counsel staff -> Vice President's Chief Counsel + Chief of Staff 2001-09 -> Heritage Foundation Vice President",
     "sources": [w("David_Addington"), wd("Q1175064"),
                 gov("https://www.justice.gov/d9/olc/legacy/2009/08/24/memo-warrantlessurveillance.pdf")]},

    # ---- Obama / Biden legal apparatus ----------------------------------
    {"id": "Monaco", "label": "Lisa Monaco", "sector": "gov",
     "admin": ["obama", "biden"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging", "tap"],
     "role": "DOJ National Security Division Assistant AG -> White House Homeland Security and Counterterrorism Advisor 2013-17 -> NYU Law -> Deputy AG 2021-25",
     "sources": [w("Lisa_Monaco"), wd("Q22059249"),
                 gov("https://www.justice.gov/dag/staff-profile/former-deputy-attorney-general-lisa-monaco")]},
    {"id": "Yates", "label": "Sally Yates", "sector": "gov",
     "admin": ["obama", "trump1"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Attorney for ND Georgia -> Deputy Attorney General 2015-17 -> Acting Attorney General Jan 2017 (fired by Trump) -> King & Spalding partner",
     "sources": [w("Sally_Yates"), wd("Q21158036"),
                 gov("https://www.justice.gov/dag/staff-profile/former-deputy-attorney-general-sally-quillian-yates")]},
    {"id": "Garland", "label": "Merrick Garland", "sector": "gov",
     "admin": ["clinton", "obama", "biden"], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "DOJ Criminal Division -> Principal Associate Deputy AG -> DC Circuit 1997-2021 (Chief Judge 2013-20) -> US Attorney General 2021-25",
     "sources": [w("Merrick_Garland"), wd("Q22687"),
                 gov("https://www.justice.gov/ag/bio/garland-merrick-b")]},
    {"id": "McCord", "label": "Mary McCord", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "DOJ National Security Division Principal Deputy AAG -> Acting AAG for National Security 2016-17 -> Georgetown Law ICAP Executive Director 2017-",
     "sources": [w("Mary_McCord"), wd("Q66053411"),
                 off("https://www.law.georgetown.edu/faculty/mary-b-mccord/")]},

    # ---- Prosecutor / special counsel circuit ---------------------------
    {"id": "Durham", "label": "John Durham", "sector": "intel",
     "admin": ["bush2", "obama", "trump1", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Attorney for Connecticut 2017-21 -> Special Counsel investigating Crossfire Hurricane 2020-23 (final report May 2023)",
     "sources": [w("John_Durham_(lawyer)"), wd("Q47011998"),
                 gov("https://www.justice.gov/storage/durhamreport.pdf")]},
    {"id": "Comey", "label": "James Comey", "sector": "intel",
     "admin": ["bush2", "obama", "trump1"], "networks": [],
     "plays": [], "actors": ["tap"],
     "role": "Lockheed Martin General Counsel -> Bridgewater Associates General Counsel -> Deputy Attorney General 2003-05 -> FBI Director 2013-17 (terminated) -> Howard University faculty",
     "sources": [w("James_Comey"), wd("Q322512"),
                 gov("https://www.fbi.gov/history/directors/james-b-comey")]},
    {"id": "Weissmann", "label": "Andrew Weissmann", "sector": "tank",
     "admin": ["obama", "trump1"], "networks": [],
     "plays": [], "actors": [],
     "role": "DOJ Criminal Division Fraud Section Chief 2015-17 -> Mueller Special Counsel team Lead Prosecutor 2017-19 -> NYU School of Law Distinguished Senior Fellow",
     "sources": [w("Andrew_Weissmann"), wd("Q4757672"),
                 off("https://its.law.nyu.edu/facultyprofiles/index.cfm?fuseaction=profile.overview&personid=42155")]},
    {"id": "JSmith", "label": "Jack Smith", "sector": "intel",
     "admin": ["obama", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "DOJ Public Integrity Section Chief 2010-15 -> International Criminal Court Specialist Prosecutor (Kosovo) 2018-22 -> US Special Counsel 2022-25 (Trump prosecutions)",
     "sources": [w("Jack_Smith_(lawyer)"), wd("Q115286906"),
                 gov("https://www.justice.gov/sco-smith")]},

    # ---- Solicitors General --------------------------------------------
    {"id": "TOlson", "label": "Theodore Olson", "sector": "tank",
     "admin": ["reagan", "bush2"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "DOJ Office of Legal Counsel AAG 1981-84 -> Gibson Dunn partner -> US Solicitor General 2001-04 (argued Bush v. Gore) -> Gibson Dunn",
     "sources": [w("Theodore_Olson"), wd("Q317672"),
                 gov("https://www.justice.gov/osg/solicitors-general-united-states")]},
    {"id": "Verrilli", "label": "Donald Verrilli Jr.", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Jenner & Block partner -> Associate Deputy AG -> White House Deputy Counsel -> US Solicitor General 2011-16 (defended ACA + same-sex marriage) -> Munger Tolles partner",
     "sources": [w("Donald_Verrilli_Jr."), wd("Q3035116"),
                 gov("https://www.justice.gov/osg/solicitors-general-united-states")]},
    {"id": "NFrancisco", "label": "Noel Francisco", "sector": "tank",
     "admin": ["bush2", "trump1"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Scalia clerk -> White House Counsel's Office (Bush2) -> Jones Day partner -> US Solicitor General 2017-20 -> Jones Day partner / Government Regulation Practice chair",
     "sources": [w("Noel_Francisco"), wd("Q43181595"),
                 gov("https://www.justice.gov/osg/solicitors-general-united-states")]},
    {"id": "Prelogar", "label": "Elizabeth Prelogar", "sector": "gov",
     "admin": ["biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "Kagan + Ginsburg clerks -> Hogan Lovells -> Office of the Solicitor General career attorney -> Principal Deputy SG -> US Solicitor General 2021-25",
     "sources": [w("Elizabeth_Prelogar"), wd("Q105906180"),
                 gov("https://www.justice.gov/osg/solicitors-general-united-states")]},

    # ---- Tech general counsels (the Big Tech legal apparatus) -----------
    {"id": "BSmith", "label": "Brad Smith", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint", "flagging"],
     "role": "Covington & Burling -> Microsoft General Counsel 2002-15 -> Microsoft President 2015-",
     "sources": [w("Brad_Smith_(American_lawyer)"), wd("Q4956218"),
                 off("https://blogs.microsoft.com/on-the-issues/author/bradsmith/")]},
    {"id": "Walker", "label": "Kent Walker", "sector": "tech",
     "admin": ["clinton"], "networks": [],
     "plays": ["pipeline"], "actors": ["algorithm", "flagging"],
     "role": "DOJ Cybercrime -> AOL Senior Counsel -> eBay -> Google General Counsel 2006-18 -> Google President of Global Affairs / Chief Legal Officer 2018-",
     "sources": [w("Kent_Walker"), wd("Q56275559"),
                 off("https://www.google.com/about/leadership/")]},

    # ---- Other key legal players ----------------------------------------
    {"id": "MHorowitz", "label": "Michael Horowitz", "sector": "gov",
     "admin": ["bush2", "obama", "trump1", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "DOJ Criminal Division -> US Sentencing Commission Commissioner -> DOJ Inspector General 2012- (Crossfire Hurricane + Clinton email investigation reports)",
     "sources": [w("Michael_E._Horowitz"), wd("Q15140867"),
                 gov("https://oig.justice.gov/")]},
    {"id": "Bauer", "label": "Robert Bauer", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": [], "actors": [],
     "role": "Perkins Coie partner -> Obama campaign counsel -> White House Counsel 2010-11 -> Perkins Coie -> NYU School of Law professor",
     "sources": [w("Robert_F._Bauer"), wd("Q7344139"),
                 off("https://www.law.nyu.edu/faculty/robert-f-bauer")]},
    {"id": "McGahn", "label": "Don McGahn", "sector": "tank",
     "admin": ["trump1"], "networks": ["federalist"],
     "plays": ["pipeline"], "actors": [],
     "role": "Jones Day partner -> FEC Commissioner 2008-13 -> Jones Day -> White House Counsel 2017-18 (judicial-nomination coordination with Federalist Society documented) -> Jones Day partner",
     "sources": [w("Don_McGahn"), wd("Q5292069"),
                 gov("https://www.fec.gov/about/leadership-and-structure/commissioners/")]},
]

NEW_EDGES = [
    # Meese
    ("Meese", "WhiteHouse"), ("Meese", "Heritage"), ("Meese", "FederalistSociety"),
    # Leo
    ("Leo", "FederalistSociety"), ("Leo", "MarbleFreedomTrust"),
    # EScalia
    ("EScalia", "GibsonDunn"), ("EScalia", "FederalistSociety"),
    # Yoo
    ("Yoo", "DOJ_OLC"), ("Yoo", "BerkeleyLaw"),
    # Addington
    ("Addington", "WhiteHouse"), ("Addington", "Heritage"), ("Addington", "CIA"),
    # Monaco
    ("Monaco", "DOJ_NSD"), ("Monaco", "WhiteHouse"), ("Monaco", "NYULaw"),
    # Yates
    ("Yates", "KingSpalding"),
    # Garland
    ("Garland", "FBI"),
    # McCord
    ("McCord", "DOJ_NSD"), ("McCord", "ICAP"),
    # Durham
    ("Durham", "FBI"),
    # Comey
    ("Comey", "FBI"),
    # Weissmann
    ("Weissmann", "NYULaw"),
    # JSmith
    # (no edges to add — institutions covered by general DOJ)
    # TOlson
    ("TOlson", "GibsonDunn"), ("TOlson", "OSG"), ("TOlson", "DOJ_OLC"),
    # Verrilli
    ("Verrilli", "MungerTolles"), ("Verrilli", "OSG"), ("Verrilli", "WhiteHouse"),
    # NFrancisco
    ("NFrancisco", "JonesDay"), ("NFrancisco", "OSG"), ("NFrancisco", "WhiteHouse"),
    # Prelogar
    ("Prelogar", "OSG"),
    # BSmith
    ("BSmith", "Microsoft"), ("BSmith", "Covington"),
    # Walker
    ("Walker", "Google"),
    # MHorowitz
    # (DOJ IG — institution covered by general DOJ; no specific edge)
    # Bauer
    ("Bauer", "PerkinsCoie"), ("Bauer", "WhiteHouse"), ("Bauer", "NYULaw"),
    # McGahn
    ("McGahn", "JonesDay"), ("McGahn", "WhiteHouse"), ("McGahn", "FederalistSociety"),
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
    for rec in NEW_PERSONS:
        if rec["id"] in person_ids or rec["id"] in inst_ids:
            continue
        rec["kind"] = "person"
        people.append(rec)
        person_ids.add(rec["id"])
        all_ids.add(rec["id"])
        new_persons += 1

    new_edges = 0
    skipped = []
    for src, tgt in NEW_EDGES:
        if src not in all_ids or tgt not in all_ids:
            skipped.append(f"{src}->{tgt}")
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
    if skipped:
        print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
