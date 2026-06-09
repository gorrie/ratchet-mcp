"""Five Eyes completion + Japan + South Korea Ratchet institutional + named adds.

Per the 2026-05-29 research agent verdict:
- Canada, Australia, Japan, South Korea all have coherent Ratchet patterns
  worth full cluster modeling.
- New Zealand is too thin for independent cluster; satellite of Australia.

CA institutions (5): CIGI, CSIS_Can, CSE, CGAI, MunkSchool.
CA persons (2): Johnston (former Governor General), Barton (McKinsey
Canada Managing Partner -> Trudeau Growth Council Chair -> Ambassador
to China).

AU institutions (6): ASIO, ASIS, ASD, ONI, ASPI, Lowy.
AU persons (4): Rudd (PM, Chatham House, Asia Society, CSIS, IPI Chair),
Turnbull (PM), Payne (FM/Defence -> Hoover Distinguished Fellow),
Abbott (PM).

NZ institutions (1): NZIIA. Persons: already have Ardern + Luxon.

JP institutions (5): JIIA, PSIA, CIRO, JMOD, OkazakiInst.
JP persons (3): Abe (long PM, JIIA founder, NSC architect), Motegi
(FM continuity 2019-21, 2021-), OkazakiHisahiko (Abe foreign policy
adviser, Okazaki Institute founder).

SK institutions (4): AsanInstitute, NIS_SK, KIDA, MND_SK.
SK persons (4): Yoon (PM 2022-25, prosecutor-to-presidency), VCha
(CSIS Korea Chair + Georgetown + Asan affiliate), CKang (Asan President,
ex-NSC Senior Director for Policy Planning), Park (PM 2013-17,
impeached 2017).
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
    # Canada
    {"id": "CIGI", "label": "Centre for International Governance Innovation", "sector": "tank",
     "sources": [w("Centre_for_International_Governance_Innovation"), off("https://www.cigionline.org/")]},
    {"id": "CSIS_Can", "label": "Canadian Security Intelligence Service", "sector": "intel",
     "sources": [w("Canadian_Security_Intelligence_Service"), off("https://www.canada.ca/en/security-intelligence-service.html")]},
    {"id": "CSE_Can", "label": "Communications Security Establishment (Canada)", "sector": "intel",
     "sources": [w("Communications_Security_Establishment"), off("https://www.cse-cst.gc.ca/")]},
    {"id": "CGAI", "label": "Canadian Global Affairs Institute", "sector": "tank",
     "sources": [w("Canadian_Global_Affairs_Institute"), off("https://www.cgai.ca/")]},
    {"id": "MunkSchool", "label": "Munk School of Global Affairs and Public Policy (Toronto)",
     "sector": "tank",
     "sources": [w("Munk_School_of_Global_Affairs"), off("https://munkschool.utoronto.ca/")]},
    # Australia
    {"id": "ASIO", "label": "Australian Security Intelligence Organisation", "sector": "intel",
     "sources": [w("Australian_Security_Intelligence_Organisation"), off("https://www.asio.gov.au/")]},
    {"id": "ASIS", "label": "Australian Secret Intelligence Service", "sector": "intel",
     "sources": [w("Australian_Secret_Intelligence_Service"), off("https://www.asis.gov.au/")]},
    {"id": "ASD", "label": "Australian Signals Directorate", "sector": "intel",
     "sources": [w("Australian_Signals_Directorate"), off("https://www.asd.gov.au/")]},
    {"id": "ONI_AU", "label": "Office of National Intelligence (Australia)", "sector": "intel",
     "sources": [w("Office_of_National_Intelligence_(Australia)"), off("https://www.oni.gov.au/")]},
    {"id": "ASPI", "label": "Australian Strategic Policy Institute", "sector": "tank",
     "sources": [w("Australian_Strategic_Policy_Institute"), off("https://www.aspi.org.au/")]},
    {"id": "Lowy", "label": "Lowy Institute", "sector": "tank",
     "sources": [w("Lowy_Institute"), off("https://www.lowyinstitute.org/")]},
    # New Zealand (single addition)
    {"id": "NZIIA", "label": "New Zealand Institute of International Affairs", "sector": "tank",
     "sources": [w("New_Zealand_Institute_of_International_Affairs"), off("https://www.nziia.org.nz/")]},
    # Japan
    {"id": "JIIA", "label": "Japan Institute of International Affairs", "sector": "tank",
     "sources": [w("Japan_Institute_of_International_Affairs"), off("https://www.jiia.or.jp/en/")]},
    {"id": "PSIA", "label": "Public Security Intelligence Agency (Japan)", "sector": "intel",
     "sources": [w("Public_Security_Intelligence_Agency"), off("https://www.moj.go.jp/psia/")]},
    {"id": "CIRO", "label": "Cabinet Intelligence and Research Office (Japan)", "sector": "intel",
     "sources": [w("Cabinet_Intelligence_and_Research_Office"), off("https://www.cas.go.jp/jp/seisaku/")]},
    {"id": "JMOD", "label": "Japan Ministry of Defense", "sector": "def",
     "sources": [w("Ministry_of_Defense_(Japan)"), off("https://www.mod.go.jp/en/")]},
    {"id": "OkazakiInst", "label": "Okazaki Institute (Japan)", "sector": "tank",
     "sources": [w("Hisahiko_Okazaki"), off("https://www.okazaki-inst.jp/")]},
    # South Korea
    {"id": "Asan", "label": "Asan Institute for Policy Studies", "sector": "tank",
     "sources": [w("Asan_Institute_for_Policy_Studies"), off("https://en.asaninst.org/")]},
    {"id": "NIS_SK", "label": "National Intelligence Service (South Korea)", "sector": "intel",
     "sources": [w("National_Intelligence_Service_(South_Korea)"), off("https://eng.nis.go.kr/")]},
    {"id": "KIDA", "label": "Korea Institute for Defense Analyses", "sector": "tank",
     "sources": [w("Korea_Institute_for_Defense_Analyses"), off("https://www.kida.re.kr/eng/")]},
    {"id": "MND_SK", "label": "Ministry of National Defense (South Korea)", "sector": "def",
     "sources": [w("Ministry_of_National_Defense_(South_Korea)"), off("https://www.mnd.go.kr/user/mndEN/")]},
]


NEW_PERSONS = [
    # ---- Canada ----------------------------------------------------------
    {"id": "DJohnston", "label": "David Johnston", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["pulpit"], "actors": [],
     "role": "Harvard + Cambridge + Queen's law academic -> Principal of McGill 1979-94 -> President of University of Waterloo -> Governor General of Canada 2010-17 -> Rideau Hall Foundation Chair -> various corporate boards",
     "sources": [w("David_Johnston"), wd("Q333418"),
                 off("https://www.gg.ca/en/governor-general/former-governors-general/david-johnston")]},
    {"id": "Barton", "label": "Dominic Barton", "sector": "tank",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "McKinsey & Company Canada -> McKinsey Asia Chairman -> McKinsey Global Managing Partner 2009-18 -> Trudeau Advisory Council on Economic Growth Chair 2016-17 -> Canada's Ambassador to China 2019-21 -> Rio Tinto Chair 2021-",
     "sources": [w("Dominic_Barton"), wd("Q4234810"),
                 off("https://www.riotinto.com/en/about/governance-and-leadership")]},

    # ---- Australia -------------------------------------------------------
    {"id": "Rudd", "label": "Kevin Rudd", "sector": "gov",
     "admin": [], "networks": ["wef"],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Australian Labor MP -> Foreign Minister -> Prime Minister of Australia 2007-10, 2013 -> Asia Society Policy Institute President + CEO 2015-22 -> Australian Ambassador to the US 2023- -> Chatham House Distinguished Fellow + CSIS senior associate + International Peace Institute Chair",
     "sources": [w("Kevin_Rudd"), wd("Q156761"),
                 off("https://www.chathamhouse.org/about-us/our-people/dr-kevin-rudd")]},
    {"id": "Turnbull", "label": "Malcolm Turnbull", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["acquisition", "pulpit"], "actors": [],
     "role": "Goldman Sachs Australia Managing Director -> Communications Minister 2013-15 -> Liberal Party leader 2015-18 -> Prime Minister of Australia 2015-18",
     "sources": [w("Malcolm_Turnbull"), wd("Q44464"),
                 off("https://www.malcolmturnbull.com.au/")]},
    {"id": "MPayne", "label": "Marise Payne", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["pulpit", "backstop"], "actors": ["embassy"],
     "role": "Australian Liberal Senator (NSW) -> Minister for Human Services -> Minister for Defence 2015-18 -> Minister for Foreign Affairs 2018-22 -> Hoover Institution Distinguished Visiting Fellow",
     "sources": [w("Marise_Payne"), wd("Q1568"),
                 off("https://www.hoover.org/profiles/marise-payne")]},
    {"id": "TAbbott", "label": "Tony Abbott", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Australian journalist -> Liberal MP -> Minister for Health 2003-07 -> Prime Minister of Australia 2013-15 -> UK Board of Trade adviser 2020-",
     "sources": [w("Tony_Abbott"), wd("Q133682"),
                 off("https://www.gov.uk/government/people/tony-abbott")]},

    # ---- Japan ----------------------------------------------------------
    {"id": "Abe", "label": "Shinzo Abe", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy"],
     "role": "LDP MP -> Chief Cabinet Secretary 2005-06 -> Prime Minister of Japan 2006-07, 2012-20 (longest-serving PM in Japanese history) -> founded Japan's National Security Council 2013 -> assassinated July 2022",
     "sources": [w("Shinzo_Abe"), wd("Q132345"),
                 off("https://japan.kantei.go.jp/96_abe/profile.html")]},
    {"id": "Motegi", "label": "Toshimitsu Motegi", "sector": "gov",
     "admin": [], "networks": [],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Marubeni Corporation -> Liberal Democratic Party MP -> Minister of Economy, Trade and Industry 2012-14 -> Minister for Foreign Affairs 2019-21 -> LDP Secretary-General 2021-23",
     "sources": [w("Toshimitsu_Motegi"), wd("Q559089"),
                 off("https://www.mofa.go.jp/about/hq/profile/index.html")]},
    {"id": "Okazaki", "label": "Hisahiko Okazaki", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy"],
     "role": "Japanese Foreign Ministry career diplomat -> Director-General of Information Analysis Bureau -> Ambassador to Saudi Arabia, Thailand -> Okazaki Institute founder; foreign-policy adviser to PMs Nakasone, Hashimoto, Abe",
     "sources": [w("Hisahiko_Okazaki"), wd("Q5872428"),
                 off("https://www.okazaki-inst.jp/")]},

    # ---- South Korea ----------------------------------------------------
    {"id": "Yoon", "label": "Yoon Suk-yeol", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Korean prosecutor 1991- -> Prosecutor General 2019-21 -> President of South Korea 2022-25 (impeached and removed April 2025 per Constitutional Court)",
     "sources": [w("Yoon_Suk_Yeol"), wd("Q16264101"),
                 off("https://english.president.go.kr/")]},
    {"id": "VCha", "label": "Victor Cha", "sector": "tank",
     "admin": ["bush2"], "networks": [],
     "plays": ["pulpit"], "actors": ["embassy"],
     "role": "Georgetown University Department of Government professor -> Bush2 NSC Director for Asian Affairs 2004-07 (Six-Party Talks deputy chair) -> CSIS Korea Chair + Senior VP for Asia -> Asan Institute affiliate",
     "sources": [w("Victor_Cha"), wd("Q7926011"),
                 off("https://www.csis.org/people/victor-cha")]},
    {"id": "CKang", "label": "Choi Kang", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "KIDA Senior Research Fellow -> NSC Senior Director for Policy Planning -> Asan Institute Vice President -> Asan Institute President 2021-",
     "sources": [w("Asan_Institute_for_Policy_Studies"), wd("Q117101451"),
                 off("https://en.asaninst.org/contents/choi-kang/")]},
    {"id": "Park", "label": "Park Geun-hye", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Daughter of Park Chung-hee -> Saenuri Party leader -> President of South Korea 2013-17 (impeached December 2016, removed March 2017, convicted 2018, pardoned 2021)",
     "sources": [w("Park_Geun-hye"), wd("Q138048"),
                 off("https://www.britannica.com/biography/Park-Geun-Hye")]},
]


NEW_EDGES = [
    # Canada
    ("DJohnston", "CanadaGov"),
    ("Barton", "CanadaGov"),
    ("Carney", "CIGI"),  # documented CIGI engagement
    ("Trudeau", "CanadaGov"),  # already linked, add if missing
    # Australia
    ("Rudd", "AUGov"), ("Rudd", "Chatham"), ("Rudd", "CSIS"),
    ("Turnbull", "AUGov"), ("Turnbull", "Goldman"),
    ("MPayne", "AUGov"),
    ("TAbbott", "AUGov"),
    ("Albanese", "ASIO"),  # PM oversight
    # Japan
    ("Abe", "JPGov"), ("Abe", "JIIA"),
    ("Motegi", "JPGov"),
    ("Okazaki", "OkazakiInst"), ("Okazaki", "JIIA"),
    ("Kishida", "JIIA"),
    # South Korea
    ("Yoon", "NIS_SK"),
    ("VCha", "Asan"), ("VCha", "CSIS"), ("VCha", "Georgetown"), ("VCha", "NSC"),
    ("CKang", "Asan"), ("CKang", "KIDA"), ("CKang", "NSC"),
    ("Park", "NIS_SK"),
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
