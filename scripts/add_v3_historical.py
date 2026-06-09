"""v3 historical drain: cabinet (Truman-Nixon era), SCOTUS sitting + recent,
Fed officials. ~29 named persons, all well-documented public figures with
Wikipedia + Wikidata + a third primary source (history.state.gov for State,
supremecourt.gov for SCOTUS, federalreserve.gov for Fed).

Idempotent. Adds supporting institutions (SCOTUS, FederalistSociety,
War_Dept, USAID) as needed.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name):
    return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}


def wd(qid):
    return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}


def gov(url):
    return {"type": "gov-record", "url": url}


def off(url):
    return {"type": "official", "url": url}


NEW_INSTITUTIONS = [
    {"id": "SCOTUS", "label": "Supreme Court of the United States", "sector": "judiciary",
     "sources": [w("Supreme_Court_of_the_United_States"), off("https://www.supremecourt.gov/")]},
    {"id": "FederalistSociety", "label": "Federalist Society", "sector": "tank",
     "sources": [w("Federalist_Society"), off("https://fedsoc.org/")]},
    {"id": "WarDept", "label": "US War Department (1789-1947)", "sector": "def",
     "sources": [w("United_States_Department_of_War")]},
    {"id": "USAID", "label": "USAID", "sector": "gov",
     "sources": [w("United_States_Agency_for_International_Development"), off("https://www.usaid.gov/")]},
    {"id": "NYFedBank", "label": "Federal Reserve Bank of New York (regional)", "sector": "gov",
     "sources": [w("Federal_Reserve_Bank_of_New_York"), off("https://www.newyorkfed.org/aboutthefed")]},
    {"id": "HarvardLaw", "label": "Harvard Law School", "sector": "tank",
     "sources": [w("Harvard_Law_School"), off("https://hls.harvard.edu/")]},
    {"id": "YaleLaw", "label": "Yale Law School", "sector": "tank",
     "sources": [w("Yale_Law_School"), off("https://law.yale.edu/")]},
]

NEW_PERSONS = [
    # ---- Cabinet historical (Truman / Eisenhower / JFK / LBJ / Nixon) -----
    {"id": "Marshall", "label": "George Marshall", "sector": "def",
     "admin": ["roosevelt", "truman"], "networks": [],
     "plays": ["pulpit", "backstop"], "actors": ["embassy", "eagle"],
     "role": "Army Chief of Staff 1939-45 -> Special Envoy to China -> Secretary of State 1947-49 (Marshall Plan) -> Secretary of Defense 1950-51",
     "sources": [w("George_C._Marshall"), wd("Q156815"),
                 gov("https://history.state.gov/departmenthistory/people/marshall-george-catlett")]},
    {"id": "ADulles", "label": "Allen Dulles", "sector": "intel",
     "admin": ["truman", "eisenhower", "kennedy"], "networks": ["cfr"],
     "plays": [], "actors": ["embassy", "tap"],
     "role": "OSS station chief Bern -> CFR Director -> CIA Deputy Director 1951-53 -> CIA Director 1953-61",
     "sources": [w("Allen_Dulles"), wd("Q190148"),
                 off("https://www.cia.gov/legacy/headquarters/allen-w-dulles/")]},
    {"id": "McNamara", "label": "Robert McNamara", "sector": "def",
     "admin": ["kennedy", "lbj"], "networks": ["cfr"],
     "plays": ["backstop", "rumpelstiltskin"], "actors": ["eagle"],
     "role": "Ford Motor Co. President -> Secretary of Defense 1961-68 -> World Bank President 1968-81",
     "sources": [w("Robert_McNamara"), wd("Q133439"),
                 off("https://history.defense.gov/Multimedia/Biographies/Article-View/Article/571272/robert-strange-mcnamara/")]},
    {"id": "Stimson", "label": "Henry Stimson", "sector": "def",
     "admin": ["roosevelt", "truman"], "networks": ["cfr"],
     "plays": ["pulpit", "backstop"], "actors": ["embassy"],
     "role": "Secretary of War (Taft 1911-13; FDR/Truman 1940-45) -> Secretary of State (Hoover 1929-33)",
     "sources": [w("Henry_L._Stimson"), wd("Q318460"),
                 gov("https://history.state.gov/departmenthistory/people/stimson-henry-lewis")]},
    {"id": "Forrestal", "label": "James Forrestal", "sector": "def",
     "admin": ["roosevelt", "truman"], "networks": [],
     "plays": ["backstop"], "actors": [],
     "role": "Dillon Read partner -> Secretary of the Navy 1944-47 -> first US Secretary of Defense 1947-49",
     "sources": [w("James_Forrestal"), wd("Q313781"),
                 off("https://history.defense.gov/Multimedia/Biographies/Article-View/Article/571268/james-vincent-forrestal/")]},
    {"id": "MBundy", "label": "McGeorge Bundy", "sector": "gov",
     "admin": ["kennedy", "lbj"], "networks": ["cfr"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Harvard Dean of Faculty of Arts and Sciences -> National Security Advisor 1961-66 -> Ford Foundation President 1966-79",
     "sources": [w("McGeorge_Bundy"), wd("Q468797"),
                 gov("https://history.state.gov/departmenthistory/people/bundy-mcgeorge")]},
    {"id": "Rostow", "label": "Walt Rostow", "sector": "gov",
     "admin": ["kennedy", "lbj"], "networks": ["cfr"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "MIT economist -> Deputy National Security Advisor 1961-66 -> National Security Advisor 1966-69",
     "sources": [w("Walt_Whitman_Rostow"), wd("Q949063"),
                 gov("https://history.state.gov/departmenthistory/people/rostow-walt-whitman")]},
    {"id": "Harriman", "label": "W. Averell Harriman", "sector": "gov",
     "admin": ["roosevelt", "truman", "kennedy", "lbj"], "networks": ["cfr"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Brown Brothers Harriman partner -> Ambassador to USSR 1943-46 -> Commerce Secretary 1946-48 -> Governor of New York 1955-58 -> Ambassador-at-Large",
     "sources": [w("W._Averell_Harriman"), wd("Q379943"),
                 gov("https://history.state.gov/departmenthistory/people/harriman-william-averell")]},
    {"id": "Lovett", "label": "Robert Lovett", "sector": "def",
     "admin": ["roosevelt", "truman"], "networks": ["cfr"],
     "plays": ["backstop", "vault"], "actors": [],
     "role": "Brown Brothers Harriman partner -> Assistant Secretary of War for Air 1941-45 -> Under Secretary of State 1947-49 -> Secretary of Defense 1951-53",
     "sources": [w("Robert_A._Lovett"), wd("Q316957"),
                 gov("https://history.state.gov/departmenthistory/people/lovett-robert-abercrombie")]},
    {"id": "Lodge", "label": "Henry Cabot Lodge Jr.", "sector": "gov",
     "admin": ["eisenhower", "kennedy", "lbj", "nixon"], "networks": [],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "US Senator (MA) -> Ambassador to UN 1953-60 -> Ambassador to South Vietnam 1963-64, 1965-67 -> Ambassador to West Germany 1968-69",
     "sources": [w("Henry_Cabot_Lodge_Jr."), wd("Q438473"),
                 gov("https://history.state.gov/departmenthistory/people/lodge-henry-cabot")]},
    {"id": "Stevenson", "label": "Adlai Stevenson II", "sector": "gov",
     "admin": ["truman", "kennedy", "lbj"], "networks": [],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Governor of Illinois 1949-53 -> Democratic presidential nominee 1952, 1956 -> Ambassador to UN 1961-65",
     "sources": [w("Adlai_Stevenson_II"), wd("Q352227"),
                 gov("https://history.state.gov/departmenthistory/people/stevenson-adlai-ewing")]},
    {"id": "Richardson", "label": "Elliot Richardson", "sector": "gov",
     "admin": ["eisenhower", "nixon", "ford"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Attorney for Massachusetts -> Under Secretary of State -> Secretary of HEW 1970-73 -> Secretary of Defense 1973 -> US Attorney General 1973 (resigned Saturday Night Massacre) -> Secretary of Commerce 1976-77",
     "sources": [w("Elliot_Richardson"), wd("Q319175"),
                 gov("https://history.state.gov/departmenthistory/people/richardson-elliot-lee")]},
    {"id": "Westmoreland", "label": "William Westmoreland", "sector": "def",
     "admin": ["kennedy", "lbj", "nixon"], "networks": [],
     "plays": [], "actors": ["eagle"],
     "role": "MACV Commander 1964-68 (Vietnam) -> Army Chief of Staff 1968-72",
     "sources": [w("William_Westmoreland"), wd("Q374750"),
                 off("https://history.army.mil/biographies/general-william-c-westmoreland/")]},
    {"id": "PHoffman", "label": "Paul G. Hoffman", "sector": "gov",
     "admin": ["truman", "kennedy"], "networks": [],
     "plays": [], "actors": [],
     "role": "Studebaker President -> Economic Cooperation Administration Administrator 1948-50 (Marshall Plan implementation) -> Ford Foundation President 1951-53 -> UN Special Fund Managing Director 1959-65",
     "sources": [w("Paul_G._Hoffman"), wd("Q1397793"),
                 w("Marshall_Plan")]},
    {"id": "Ball", "label": "George Ball", "sector": "gov",
     "admin": ["kennedy", "lbj"], "networks": ["cfr"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Under Secretary of State for Economic and Agricultural Affairs -> Under Secretary of State 1961-66 -> Ambassador to UN 1968",
     "sources": [w("George_Ball_(diplomat)"), wd("Q5535956"),
                 gov("https://history.state.gov/departmenthistory/people/ball-george-wildman")]},
    {"id": "Symington", "label": "Stuart Symington", "sector": "def",
     "admin": ["truman"], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "Emerson Electric President -> first Secretary of the Air Force 1947-50 -> US Senator (MO) 1953-76",
     "sources": [w("Stuart_Symington"), wd("Q1257263"),
                 gov("https://www.afhra.af.mil/About-Us/Fact-Sheets/Display/Article/433880/")]},

    # ---- SCOTUS sitting + recent --------------------------------------------
    {"id": "Roberts", "label": "John Roberts", "sector": "judiciary",
     "admin": ["reagan", "bush1", "bush2"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Rehnquist clerk -> Hogan & Hartson partner -> DOJ Office of the Solicitor General -> White House Counsel -> DC Circuit -> Chief Justice 2005-",
     "sources": [w("John_Roberts"), wd("Q19009"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Thomas", "label": "Clarence Thomas", "sector": "judiciary",
     "admin": ["reagan", "bush1"], "networks": [],
     "plays": [], "actors": [],
     "role": "Education Department Office for Civil Rights -> EEOC Chair 1982-90 -> DC Circuit -> Associate Justice 1991-",
     "sources": [w("Clarence_Thomas"), wd("Q41142"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Alito", "label": "Samuel Alito", "sector": "judiciary",
     "admin": ["reagan", "bush1", "bush2"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "DOJ Office of the Solicitor General -> US Attorney for NJ -> Third Circuit 1990-2006 -> Associate Justice 2006-",
     "sources": [w("Samuel_Alito"), wd("Q83287"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Kavanaugh", "label": "Brett Kavanaugh", "sector": "judiciary",
     "admin": ["bush2", "trump1"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Kennedy clerk -> Office of Independent Counsel (Starr) -> White House Staff Secretary (Bush II) -> DC Circuit 2006-18 -> Associate Justice 2018-",
     "sources": [w("Brett_Kavanaugh"), wd("Q887775"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Barrett", "label": "Amy Coney Barrett", "sector": "judiciary",
     "admin": ["trump1"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Scalia clerk -> Notre Dame Law professor -> Seventh Circuit 2017-20 -> Associate Justice 2020-",
     "sources": [w("Amy_Coney_Barrett"), wd("Q26257"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Sotomayor", "label": "Sonia Sotomayor", "sector": "judiciary",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": [], "actors": [],
     "role": "Manhattan DA -> SDNY District Court 1992-98 -> Second Circuit 1998-2009 -> Associate Justice 2009-",
     "sources": [w("Sonia_Sotomayor"), wd("Q174658"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Kagan", "label": "Elena Kagan", "sector": "judiciary",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": [], "actors": [],
     "role": "Marshall clerk -> Clinton WH Deputy Assistant for Domestic Policy -> Harvard Law School Dean 2003-09 -> US Solicitor General 2009-10 -> Associate Justice 2010-",
     "sources": [w("Elena_Kagan"), wd("Q44473"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "Gorsuch", "label": "Neil Gorsuch", "sector": "judiciary",
     "admin": ["bush2", "trump1"], "networks": ["federalist"],
     "plays": [], "actors": [],
     "role": "Kennedy + White clerks -> Kellogg Huber partner -> DOJ Principal Deputy Associate AG -> Tenth Circuit 2006-17 -> Associate Justice 2017-",
     "sources": [w("Neil_Gorsuch"), wd("Q526765"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},
    {"id": "KJackson", "label": "Ketanji Brown Jackson", "sector": "judiciary",
     "admin": ["obama", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "Breyer clerk -> US Sentencing Commission Vice Chair -> DC District 2013-21 -> DC Circuit 2021-22 -> Associate Justice 2022-",
     "sources": [w("Ketanji_Brown_Jackson"), wd("Q5747251"),
                 off("https://www.supremecourt.gov/about/biographies.aspx")]},

    # ---- Fed Reserve historical + recent regional ---------------------------
    {"id": "Eccles", "label": "Marriner Eccles", "sector": "gov",
     "admin": ["roosevelt", "truman"], "networks": [],
     "plays": [], "actors": ["money"],
     "role": "First Security Corporation -> Fed Chair 1934-48 (Banking Act of 1935 architect)",
     "sources": [w("Marriner_S._Eccles"), wd("Q713049"),
                 off("https://www.federalreservehistory.org/people/marriner_s_eccles")]},
    {"id": "JWilliams", "label": "John C. Williams", "sector": "gov",
     "admin": ["obama", "trump1", "biden", "trump2"], "networks": [],
     "plays": [], "actors": ["money"],
     "role": "SF Fed Research Director -> SF Fed President 2011-18 -> NY Fed President 2018-",
     "sources": [w("John_C._Williams_(economist)"), wd("Q15076232"),
                 off("https://www.newyorkfed.org/aboutthefed/orgchart/williams")]},
    {"id": "Mester", "label": "Loretta Mester", "sector": "gov",
     "admin": ["obama", "trump1", "biden"], "networks": [],
     "plays": [], "actors": ["money"],
     "role": "Philly Fed Research Director -> Cleveland Fed President 2014-24",
     "sources": [w("Loretta_Mester"), wd("Q17570080"),
                 off("https://www.clevelandfed.org/our-research/loretta-mester")]},
    {"id": "Rosengren", "label": "Eric Rosengren", "sector": "gov",
     "admin": ["bush2", "obama", "trump1", "biden"], "networks": [],
     "plays": [], "actors": ["money"],
     "role": "Boston Fed Research -> Boston Fed President 2007-21",
     "sources": [w("Eric_Rosengren"), wd("Q1351196"),
                 off("https://www.bostonfed.org/people/bank/eric-rosengren")]},
]

NEW_EDGES = [
    # Cabinet historical
    ("Marshall", "State"), ("Marshall", "DoD"), ("Marshall", "WarDept"),
    ("ADulles", "CIA"), ("ADulles", "CFR"),
    ("McNamara", "DoD"), ("McNamara", "WB"),
    ("Stimson", "WarDept"), ("Stimson", "CFR"),
    ("Forrestal", "DoD"),
    ("MBundy", "NSC"), ("MBundy", "CFR"),
    ("Rostow", "NSC"), ("Rostow", "CFR"),
    ("Harriman", "State"), ("Harriman", "CFR"),
    ("Lovett", "DoD"), ("Lovett", "State"), ("Lovett", "CFR"),
    ("Lodge", "UN"), ("Lodge", "State"),
    ("Stevenson", "UN"), ("Stevenson", "State"),
    ("Richardson", "DoD"), ("Richardson", "State"),
    ("Westmoreland", "DoD"),
    ("PHoffman", "USAID"),
    ("Ball", "State"), ("Ball", "UN"), ("Ball", "CFR"),
    ("Symington", "DoD"), ("Symington", "Senate"),
    # SCOTUS
    ("Roberts", "SCOTUS"), ("Roberts", "FederalistSociety"),
    ("Thomas", "SCOTUS"),
    ("Alito", "SCOTUS"), ("Alito", "FederalistSociety"),
    ("Kavanaugh", "SCOTUS"), ("Kavanaugh", "FederalistSociety"), ("Kavanaugh", "WhiteHouse"),
    ("Barrett", "SCOTUS"), ("Barrett", "FederalistSociety"),
    ("Sotomayor", "SCOTUS"),
    ("Kagan", "SCOTUS"), ("Kagan", "HarvardLaw"), ("Kagan", "WhiteHouse"),
    ("Gorsuch", "SCOTUS"), ("Gorsuch", "FederalistSociety"),
    ("KJackson", "SCOTUS"),
    # Fed
    ("Eccles", "FedReserve"),
    ("JWilliams", "NYFedBank"), ("JWilliams", "FedReserve"),
    ("Mester", "FedReserve"),
    ("Rosengren", "FedReserve"),
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
        print(f"Skipped edges: {skipped_edges}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
