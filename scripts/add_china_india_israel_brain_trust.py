"""China + India + Israel institutional brain trust + selected named
ex-officials.

China brain trust (institutional-only per Cohort F anti-tinfoil rule):
CICIR, CASS, CCG, CIIS, SIIS, IDCPC (CPC International Department).

India brain trust (institutions + named ex-officials per existing rule):
ORF, MP-IDSA, CSEP, GatewayHouse, VIF, ICWA, CarnegieIndia.

Israel brain trust + commercial-surveillance vendors (institutions
+ named ex-officials only -- current operators and active operations
stay institutional-only):
INSS, Unit8200, NSO, Pegasus-affected institutions are out (too
specific); Cellebrite already in.

Indian named officials (3): Jaishankar (current EAM), SMenon (ex-NSA),
NJaishankar context.
Israeli named ex-officials (3): Barak (ex-PM), Olmert (ex-PM), Livni
(ex-FM).

Documented engagement edges from existing UK/US cohort to these
institutions (e.g., Kissinger -> Boao already in; add Kissinger ->
Tsinghua already in; new: Niblett -> Chatham-China dialogue if
documented).
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
    # ---- China state-run think tanks (institutional-only per Cohort F) ----
    {"id": "CICIR", "label": "China Institutes of Contemporary International Relations (MSS-affiliated)",
     "sector": "china-state",
     "sources": [w("China_Institutes_of_Contemporary_International_Relations"),
                 acad("https://www.aspi.org.au/report/party-speaks-you")]},
    {"id": "CASS", "label": "Chinese Academy of Social Sciences", "sector": "china-state",
     "sources": [w("Chinese_Academy_of_Social_Sciences"), off("http://english.cssn.cn/")]},
    {"id": "CCG", "label": "Center for China and Globalization", "sector": "china-state",
     "sources": [w("Center_for_China_and_Globalization"), off("http://en.ccg.org.cn/")]},
    {"id": "CIIS", "label": "China Institute of International Studies (MFA-affiliated)",
     "sector": "china-state",
     "sources": [w("China_Institute_of_International_Studies"), off("https://www.ciis.org.cn/english/")]},
    {"id": "SIIS", "label": "Shanghai Institutes for International Studies", "sector": "china-state",
     "sources": [w("Shanghai_Institutes_for_International_Studies"), off("http://www.siis.org.cn/english/")]},
    {"id": "IDCPC", "label": "International Department of the Chinese Communist Party",
     "sector": "china-state",
     "sources": [w("International_Department_of_the_Chinese_Communist_Party"),
                 off("http://www.idcpc.gov.cn/english/")]},

    # ---- India think tanks (US/UK-style — named persons OK) ---------------
    {"id": "ORF", "label": "Observer Research Foundation (Reliance-backed)", "sector": "tank",
     "sources": [w("Observer_Research_Foundation"), off("https://www.orfonline.org/")]},
    {"id": "MP_IDSA", "label": "Manohar Parrikar Institute for Defence Studies and Analyses (MoD-affiliated)",
     "sector": "tank",
     "sources": [w("Manohar_Parrikar_Institute_for_Defence_Studies_and_Analyses"),
                 off("https://www.idsa.in/")]},
    {"id": "CSEP", "label": "Centre for Social and Economic Progress (formerly Brookings India)",
     "sector": "tank",
     "sources": [w("Centre_for_Social_and_Economic_Progress"), off("https://csep.org/")]},
    {"id": "GatewayHouse", "label": "Gateway House (India)", "sector": "tank",
     "sources": [w("Gateway_House"), off("https://www.gatewayhouse.in/")]},
    {"id": "VIF", "label": "Vivekananda International Foundation (India)", "sector": "tank",
     "sources": [w("Vivekananda_International_Foundation"), off("https://www.vifindia.org/")]},
    {"id": "ICWA", "label": "Indian Council of World Affairs (MEA-affiliated)", "sector": "tank",
     "sources": [w("Indian_Council_of_World_Affairs"), off("https://www.icwa.in/")]},
    {"id": "CarnegieIndia", "label": "Carnegie India", "sector": "tank",
     "sources": [w("Carnegie_Endowment_for_International_Peace"), off("https://carnegieindia.org/")]},
    {"id": "MEA_India", "label": "Ministry of External Affairs (India)", "sector": "gov",
     "sources": [w("Ministry_of_External_Affairs_(India)"), off("https://www.mea.gov.in/")]},

    # ---- Israel institutional brain trust + alumni network ----------------
    {"id": "INSS", "label": "Institute for National Security Studies (Tel Aviv)", "sector": "tank",
     "sources": [w("Institute_for_National_Security_Studies"), off("https://www.inss.org.il/")]},
    {"id": "Unit8200", "label": "Unit 8200 (IDF Intelligence Corps)", "sector": "intel",
     "sources": [w("Unit_8200"),
                 acad("https://www.haaretz.com/israel-news/2018-04-24/ty-article/.premium/from-aman-to-the-startup-cluster-how-unit-8200-became-israels-tech-startup-incubator/")]},
    {"id": "NSO", "label": "NSO Group (Pegasus spyware)", "sector": "tech",
     "sources": [w("NSO_Group"),
                 off("https://www.nsogroup.com/")]},
    {"id": "BlackCube", "label": "Black Cube (Israeli private intelligence)", "sector": "intel",
     "sources": [w("Black_Cube"), off("https://www.blackcube.com/")]},
    {"id": "IsraelGov", "label": "Israeli Government", "sector": "gov",
     "sources": [w("Cabinet_of_Israel"), off("https://www.gov.il/en")]},
]


NEW_PERSONS = [
    # ---- Indian named officials (eligible per same rule as US/UK) ----------
    {"id": "Jaishankar", "label": "Subrahmanyam Jaishankar", "sector": "gov",
     "admin": [], "networks": ["wef"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Indian Foreign Service career diplomat -> Ambassador to Czech Republic, Singapore, China 2009-13 -> Ambassador to US 2013-15 -> Foreign Secretary 2015-18 -> External Affairs Minister of India 2019- -> Rajya Sabha MP",
     "sources": [w("Subrahmanyam_Jaishankar"), wd("Q15461081"),
                 off("https://www.mea.gov.in/about-mea.htm")]},
    {"id": "SMenon", "label": "Shivshankar Menon", "sector": "tank",
     "admin": [], "networks": [],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Indian Foreign Service -> Ambassador to Israel, Sri Lanka, China, Pakistan -> Foreign Secretary 2006-09 -> National Security Adviser 2010-14 -> Brookings India Distinguished Fellow -> Ashoka University professor",
     "sources": [w("Shivshankar_Menon"), wd("Q7501095"),
                 off("https://csep.org/people/shivshankar-menon/")]},
    {"id": "Doval", "label": "Ajit Doval", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["tap", "embassy"],
     "role": "Indian Police Service / Intelligence Bureau operative -> Director of IB 2004-05 -> Vivekananda International Foundation founding Director 2009 -> National Security Adviser of India 2014-",
     "sources": [w("Ajit_Doval"), wd("Q1018571"),
                 off("https://www.pmindia.gov.in/en/profile-committee/national-security-adviser/")]},

    # ---- Israeli named ex-officials ---------------------------------------
    {"id": "Barak", "label": "Ehud Barak", "sector": "def",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "IDF career officer -> IDF Chief of the General Staff 1991-95 -> Israeli Foreign Minister 1995-96 -> Prime Minister of Israel 1999-2001 -> Minister of Defense 2007-13 -> Carbyne911 chair (Israeli emergency-comms startup)",
     "sources": [w("Ehud_Barak"), wd("Q170388"),
                 off("https://www.gov.il/he/departments/people/")]},
    {"id": "Olmert", "label": "Ehud Olmert", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Israeli Likud / Kadima MK -> Mayor of Jerusalem 1993-2003 -> Minister of Trade and Industry -> acting PM following Sharon's stroke -> Prime Minister of Israel 2006-09",
     "sources": [w("Ehud_Olmert"), wd("Q170581_"),
                 off("https://www.gov.il/he/departments/people/")]},
    {"id": "Livni", "label": "Tzipi Livni", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Mossad officer (1980s) -> Likud / Kadima / Hatnuah Knesset member -> Foreign Minister of Israel 2006-09 -> Minister of Justice 2013-14",
     "sources": [w("Tzipi_Livni"), wd("Q161571"),
                 off("https://main.knesset.gov.il/EN/MK/Pages/MKPersonalDetails.aspx?MKID=683")]},
    {"id": "Bennett", "label": "Naftali Bennett", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "IDF Sayeret Matkal special-forces -> Cyota CEO (sold to RSA Security $145M 2005) -> Soluto founder/CEO (sold to Asurion 2013) -> Knesset MK -> Minister of Education, Defense -> Prime Minister of Israel 2021-22",
     "sources": [w("Naftali_Bennett"), wd("Q241176"),
                 off("https://main.knesset.gov.il/EN/MK/")]},
]


NEW_EDGES = [
    # India persons -> Indian institutions
    ("Jaishankar", "MEA_India"),
    ("SMenon", "MEA_India"), ("SMenon", "CSEP"),
    ("Doval", "VIF"),
    # Already-in-dataset US/allied cohort -> India institutions
    ("Nilekani", "ORF"),  # documented ORF engagement
    # Israeli persons -> Israeli institutions
    ("Barak", "IsraelGov"), ("Barak", "Knesset"),
    ("Olmert", "IsraelGov"), ("Olmert", "Knesset"),
    ("Livni", "Mossad"), ("Livni", "IsraelGov"), ("Livni", "Knesset"),
    ("Bennett", "IsraelGov"), ("Bennett", "Knesset"),
    # Existing Israeli dataset -> new institutions
    # YCohen / Barnea already have Mossad edges; add Mossad to Knesset relation? No, those are different sectors
    # Already-in US cohort -> Chinese institutions (additional documented engagement)
    ("Schwarzman", "Tsinghua"),  # already added; redundant skip
    ("Kissinger", "CASS"),  # documented Kissinger Associates engagement with CASS
    ("Paulson", "CASS"),
    ("Summers", "ORF"),  # documented ORF engagement at conferences
    # Document the Israeli alumni-network pattern via existing dataset edges
    # (no new edges needed; Mossad already linked from YCohen + Barnea)
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
