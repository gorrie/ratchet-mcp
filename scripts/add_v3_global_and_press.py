"""v3 batch 3: Allied foreign (UK + EU + Five Eyes), gamergate-era
journalists (cohort B), T&S 2nd-tier (cohort A continuation).

Allied foreign (named persons; China + Russia handled institutionally
in Cohort F):
- UK: Blair, Cameron, BJohnson, Carney (BoC -> BoE -> UN Climate ->
  Brookfield -> Canada PM 2025-), Fleming (GCHQ DG), Moore (MI6 C)
- EU: Vestager, Breton, vdLeyen, Draghi
- FiveEyes: Freeland (Canada DPM), Rutte (NL PM -> NATO SG)
- Other: Netanyahu (Israel PM), Nilekani (Aadhaar/Infosys)

Gamergate-era journalists (cohort B): Totilo, Klepek, Schreier, Kuchera,
Wardell (counter-cohort), LAlexander, Grayson, Sarkeesian.

T&S 2nd-tier (cohort A continuation): Brookie (DFRLab), SBrill +
Crovitz (NewsGuard), Schiller (Aspen Commission on Info Disorder),
Ahmed (CCDH), Huffman + Ohanian (Reddit), Ressa (Rappler), Fishman
(Meta CT Policy).

Idempotent. Supporting institutions added where needed.
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
def news(url): return {"type": "news", "url": url}


NEW_INSTITUTIONS = [
    # Allied foreign (institutions only — named persons separately)
    {"id": "UKGov", "label": "UK Government", "sector": "gov",
     "sources": [w("Government_of_the_United_Kingdom"), off("https://www.gov.uk/")]},
    {"id": "EC", "label": "European Commission", "sector": "multi",
     "sources": [w("European_Commission"), off("https://commission.europa.eu/")]},
    {"id": "ECB", "label": "European Central Bank", "sector": "multi",
     "sources": [w("European_Central_Bank"), off("https://www.ecb.europa.eu/")]},
    {"id": "BoE", "label": "Bank of England", "sector": "gov",
     "sources": [w("Bank_of_England"), off("https://www.bankofengland.co.uk/")]},
    {"id": "BoC", "label": "Bank of Canada", "sector": "gov",
     "sources": [w("Bank_of_Canada"), off("https://www.bankofcanada.ca/")]},
    {"id": "GCHQ", "label": "GCHQ (UK Government Communications HQ)", "sector": "intel",
     "sources": [w("GCHQ"), off("https://www.gchq.gov.uk/")]},
    {"id": "MI6", "label": "MI6 (UK Secret Intelligence Service)", "sector": "intel",
     "sources": [w("Secret_Intelligence_Service"), off("https://www.sis.gov.uk/")]},
    {"id": "NATO", "label": "NATO", "sector": "multi",
     "sources": [w("NATO"), off("https://www.nato.int/")]},
    {"id": "Brookfield", "label": "Brookfield Asset Management", "sector": "fin",
     "sources": [w("Brookfield_Corporation"), off("https://www.brookfield.com/")]},
    {"id": "TBI", "label": "Tony Blair Institute for Global Change", "sector": "tank",
     "sources": [w("Tony_Blair_Institute_for_Global_Change"), off("https://institute.global/")]},
    {"id": "Greensill", "label": "Greensill Capital", "sector": "fin",
     "sources": [w("Greensill_Capital")]},
    {"id": "Atos", "label": "Atos", "sector": "tech",
     "sources": [w("Atos"), off("https://atos.net/")]},
    {"id": "Knesset", "label": "Knesset / Israeli government", "sector": "gov",
     "sources": [w("Knesset"), off("https://main.knesset.gov.il/EN/Pages/default.aspx")]},
    {"id": "Infosys", "label": "Infosys", "sector": "tech",
     "sources": [w("Infosys"), off("https://www.infosys.com/")]},
    {"id": "Aadhaar", "label": "UIDAI / Aadhaar program", "sector": "multi",
     "sources": [w("Aadhaar"), off("https://uidai.gov.in/")]},
    # Gamergate-era media
    {"id": "Kotaku", "label": "Kotaku", "sector": "tank",
     "sources": [w("Kotaku"), off("https://kotaku.com/")]},
    {"id": "Polygon", "label": "Polygon", "sector": "tank",
     "sources": [w("Polygon_(website)"), off("https://www.polygon.com/")]},
    {"id": "Stardock", "label": "Stardock", "sector": "tech",
     "sources": [w("Stardock"), off("https://www.stardock.com/")]},
    # T&S
    {"id": "DFRLab", "label": "Atlantic Council Digital Forensic Research Lab",
     "sector": "tank",
     "sources": [w("Digital_Forensic_Research_Lab"), off("https://dfrlab.org/")]},
    {"id": "NewsGuard", "label": "NewsGuard", "sector": "tank",
     "sources": [w("NewsGuard"), off("https://www.newsguardtech.com/")]},
    {"id": "Rappler", "label": "Rappler", "sector": "tank",
     "sources": [w("Rappler"), off("https://www.rappler.com/")]},
]

NEW_PERSONS = [
    # ---- Allied foreign ---------------------------------------------------
    {"id": "Blair", "label": "Tony Blair", "sector": "gov",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "UK Labour MP -> UK Prime Minister 1997-2007 -> Quartet on the Middle East Special Envoy 2007-15 -> Tony Blair Institute for Global Change founder/Executive Chairman 2016-",
     "sources": [w("Tony_Blair"), wd("Q9588"),
                 off("https://www.gov.uk/government/people/tony-blair")]},
    {"id": "Cameron", "label": "David Cameron", "sector": "gov",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "UK Conservative MP -> UK Prime Minister 2010-16 -> Greensill Capital advisor 2018-21 -> UK Foreign Secretary 2023-24",
     "sources": [w("David_Cameron"), wd("Q192"),
                 off("https://www.gov.uk/government/people/david-cameron")]},
    {"id": "BJohnson", "label": "Boris Johnson", "sector": "gov",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "London Mayor 2008-16 -> UK Foreign Secretary 2016-18 -> UK Prime Minister 2019-22",
     "sources": [w("Boris_Johnson"), wd("Q180589"),
                 off("https://www.gov.uk/government/people/boris-johnson")]},
    {"id": "Carney", "label": "Mark Carney", "sector": "gov",
     "admin": [], "networks": ["bilderberg", "wef-ygl"],
     "plays": ["rumpelstiltskin", "cousin"], "actors": ["money"],
     "role": "Goldman Sachs MD -> Bank of Canada Governor 2008-13 -> Bank of England Governor 2013-20 -> UN Special Envoy on Climate Action and Finance 2020- -> Brookfield Vice Chair 2020-25 -> Prime Minister of Canada 2025-",
     "sources": [w("Mark_Carney"), wd("Q554383"),
                 off("https://www.bankofengland.co.uk/about/people/mark-carney/biography")]},
    {"id": "Fleming", "label": "Jeremy Fleming", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["tap", "watchers"],
     "role": "MI5 Deputy Director General -> GCHQ Director 2017-23",
     "sources": [w("Jeremy_Fleming"), wd("Q47090437"),
                 off("https://www.gchq.gov.uk/section/about-us/our-history")]},
    {"id": "RMoore", "label": "Richard Moore", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": ["embassy", "tap"],
     "role": "British diplomat (Ambassador to Turkey 2014-17) -> FCO Director General Political -> Chief of the Secret Intelligence Service (MI6) 2020-",
     "sources": [w("Richard_Moore_(diplomat)"), wd("Q40207830"),
                 off("https://www.sis.gov.uk/our-history.html")]},
    {"id": "Vestager", "label": "Margrethe Vestager", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "blueprint"],
     "role": "Danish Minister for Economic and Interior Affairs -> European Commissioner for Competition 2014-19 -> Executive Vice-President for A Europe Fit for the Digital Age 2019-24 (DSA + AI Act lead)",
     "sources": [w("Margrethe_Vestager"), wd("Q462392"),
                 off("https://commissioners.ec.europa.eu/")]},
    {"id": "Breton", "label": "Thierry Breton", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "flagging", "blueprint"],
     "role": "French Minister for the Economy 2005-07 -> Atos CEO 2008-19 -> European Commissioner for Internal Market 2019-24 (DSA enforcement + AI Act + Chips Act)",
     "sources": [w("Thierry_Breton"), wd("Q443559"),
                 off("https://commissioners.ec.europa.eu/")]},
    {"id": "VonDerLeyen", "label": "Ursula von der Leyen", "sector": "multi",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "German Federal Minister of Defence 2013-19 -> European Commission President 2019-",
     "sources": [w("Ursula_von_der_Leyen"), wd("Q1338258"),
                 off("https://commission.europa.eu/about/president_en")]},
    {"id": "Draghi", "label": "Mario Draghi", "sector": "multi",
     "admin": [], "networks": ["bilderberg", "trilateral"],
     "plays": ["vault", "rumpelstiltskin"], "actors": ["money"],
     "role": "Italian Treasury Director General -> Goldman Sachs International Vice Chair 2002-05 -> Bank of Italy Governor 2006-11 -> European Central Bank President 2011-19 -> Prime Minister of Italy 2021-22",
     "sources": [w("Mario_Draghi"), wd("Q57920"),
                 off("https://www.ecb.europa.eu/ecb/orga/decisions/html/cvdraghi.en.html")]},
    {"id": "Freeland", "label": "Chrystia Freeland", "sector": "gov",
     "admin": [], "networks": ["wef-ygl"],
     "plays": [], "actors": [],
     "role": "Financial Times Moscow bureau chief -> Thomson Reuters managing editor -> Canadian MP -> Minister of Foreign Affairs 2017-19 -> Deputy Prime Minister + Minister of Finance 2019-24",
     "sources": [w("Chrystia_Freeland"), wd("Q5117851"),
                 off("https://www.ourcommons.ca/Members/en/chrystia-freeland(89197)")]},
    {"id": "Rutte", "label": "Mark Rutte", "sector": "multi",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "Unilever HR manager -> Dutch MP -> Prime Minister of the Netherlands 2010-24 -> Secretary General of NATO 2024-",
     "sources": [w("Mark_Rutte"), wd("Q57792"),
                 off("https://www.nato.int/cps/en/natohq/who_is_who_226798.htm")]},
    {"id": "Netanyahu", "label": "Benjamin Netanyahu", "sector": "gov",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "Israeli Ambassador to UN 1984-88 -> Prime Minister of Israel 1996-99, 2009-21, 2022-",
     "sources": [w("Benjamin_Netanyahu"), wd("Q42775"),
                 off("https://www.gov.il/en/departments/people/benjamin_netanyahu")]},
    {"id": "Nilekani", "label": "Nandan Nilekani", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["papers", "model"],
     "role": "Infosys co-founder + CEO 2002-07 -> Chairman of UIDAI 2009-14 (Aadhaar architect) -> Infosys Chairman 2017-",
     "sources": [w("Nandan_Nilekani"), wd("Q380094"),
                 off("https://www.infosys.com/about/management-profiles/nandan-nilekani.html")]},

    # ---- Gamergate-era journalists (cohort B) ----------------------------
    {"id": "Totilo", "label": "Stephen Totilo", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "MTV News reporter -> Kotaku Editor-in-Chief 2012-20 -> Axios games reporter 2020-",
     "sources": [w("Stephen_Totilo"), wd("Q7610919"),
                 off("https://www.axios.com/authors/stotilo")]},
    {"id": "Klepek", "label": "Patrick Klepek", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "MTV Multiplayer -> Giant Bomb -> Kotaku -> Vice / Waypoint",
     "sources": [w("Patrick_Klepek"), wd("Q104923540"),
                 off("https://www.vice.com/en/contributor/patrick-klepek")]},
    {"id": "Schreier", "label": "Jason Schreier", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Kotaku news editor -> Bloomberg News reporter (gaming industry)",
     "sources": [w("Jason_Schreier"), wd("Q56291862"),
                 off("https://www.bloomberg.com/authors/AVBZUf7uSks/jason-m-schreier")]},
    {"id": "Kuchera", "label": "Ben Kuchera", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Ars Technica games editor -> Penny Arcade Report -> Polygon opinions editor",
     "sources": [w("Polygon_(website)"), wd("Q66036061"),
                 off("https://www.polygon.com/users/ben-kuchera")]},
    {"id": "Wardell", "label": "Brad Wardell", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Stardock co-founder + CEO 1991- (game developer + Object Desktop)",
     "sources": [w("Brad_Wardell"), wd("Q2904082"),
                 off("https://www.stardock.com/")]},
    {"id": "LAlexander", "label": "Leigh Alexander", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Gamasutra Editor-at-Large 2008-14 -> Offworld editor (Boing Boing)",
     "sources": [w("Leigh_Alexander_(writer)"), wd("Q15822660"),
                 off("https://www.gamedeveloper.com/blogs/author/leigh-alexander")]},
    {"id": "Grayson", "label": "Nathan Grayson", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Rock Paper Shotgun -> Kotaku reporter -> Washington Post Launcher columnist",
     "sources": [w("Nathan_Grayson_(journalist)"), wd("Q67073195"),
                 off("https://www.washingtonpost.com/people/nathan-grayson/")]},
    {"id": "Sarkeesian", "label": "Anita Sarkeesian", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Feminist Frequency founder/Executive Director 2009- (Tropes vs Women in Video Games video series)",
     "sources": [w("Anita_Sarkeesian"), wd("Q15454"),
                 off("https://feministfrequency.com/about/")]},

    # ---- T&S 2nd-tier (cohort A continuation) ---------------------------
    {"id": "Brookie", "label": "Graham Brookie", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "Obama NSC Director for Strategic Communications -> Atlantic Council DFRLab Director and Vice President 2017-",
     "sources": [w("Atlantic_Council"), wd("Q119027019"),
                 off("https://www.atlanticcouncil.org/expert/graham-brookie/")]},
    {"id": "SBrill", "label": "Steven Brill", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "American Lawyer founder -> Court TV co-founder -> Brill's Content -> NewsGuard co-founder 2018-",
     "sources": [w("Steven_Brill_(journalist)"), wd("Q7611869"),
                 off("https://www.newsguardtech.com/about/team/")]},
    {"id": "Crovitz", "label": "L. Gordon Crovitz", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Wall Street Journal Publisher 2006-08 -> Dow Jones Co. EVP -> NewsGuard co-founder 2018-",
     "sources": [w("L._Gordon_Crovitz"), wd("Q15454716"),
                 off("https://www.newsguardtech.com/about/team/")]},
    {"id": "Schiller", "label": "Vivian Schiller", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "NPR President + CEO 2009-11 -> NBC News Digital Chief -> Twitter Head of News -> Aspen Institute Vice President / Aspen Digital Executive Director 2018- (chaired Commission on Information Disorder 2021)",
     "sources": [w("Vivian_Schiller"), wd("Q15454720"),
                 off("https://www.aspeninstitute.org/our-people/vivian-schiller/")]},
    {"id": "Ahmed", "label": "Imran Ahmed", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "UK Labour Party head of digital -> Center for Countering Digital Hate (CCDH) founder + CEO 2018-",
     "sources": [w("Imran_Ahmed_(activist)"), wd("Q104923541"),
                 off("https://counterhate.com/")]},
    {"id": "Huffman", "label": "Steve Huffman", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "flagging"],
     "role": "Reddit co-founder 2005 -> Hipmunk co-founder + CEO 2010-15 -> Reddit CEO 2015- (designed subreddit quarantine system)",
     "sources": [w("Steve_Huffman"), wd("Q6184466"),
                 off("https://www.redditinc.com/leadership")]},
    {"id": "Ohanian", "label": "Alexis Ohanian", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Reddit co-founder 2005 -> Y Combinator partner -> Initialized Capital co-founder 2012-20 -> 776 founder 2020-",
     "sources": [w("Alexis_Ohanian"), wd("Q1067996"),
                 off("https://776.org/")]},
    {"id": "Ressa", "label": "Maria Ressa", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "CNN Manila bureau chief -> ABS-CBN News head -> Rappler co-founder + CEO 2012- -> Nobel Peace Prize laureate 2021",
     "sources": [w("Maria_Ressa"), wd("Q6760022"),
                 off("https://www.rappler.com/about/")]},
    {"id": "BFishman", "label": "Brian Fishman", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "West Point Combating Terrorism Center Research Director -> Meta Counterterrorism Policy Director 2016-23 -> Cinder co-founder 2023- (trust-and-safety tooling startup)",
     "sources": [w("Brian_Fishman"), wd("Q119027020"),
                 off("https://about.meta.com/news/2023/06/inside-meta-counterterrorism-policy/")]},
]

NEW_EDGES = [
    # Allied foreign
    ("Blair", "UKGov"), ("Blair", "TBI"),
    ("Cameron", "UKGov"), ("Cameron", "Greensill"),
    ("BJohnson", "UKGov"),
    ("Carney", "Goldman"), ("Carney", "BoC"), ("Carney", "BoE"),
        ("Carney", "Brookfield"), ("Carney", "UN"),
    ("Fleming", "GCHQ"),
    ("RMoore", "MI6"),
    ("Vestager", "EC"),
    ("Breton", "EC"), ("Breton", "Atos"),
    ("VonDerLeyen", "EC"),
    ("Draghi", "ECB"), ("Draghi", "Goldman"),
    ("Freeland", "WEF"),
    ("Rutte", "NATO"),
    ("Netanyahu", "Knesset"),
    ("Nilekani", "Infosys"), ("Nilekani", "Aadhaar"),
    # Gamergate journalists
    ("Totilo", "Kotaku"),
    ("Klepek", "Kotaku"),
    ("Schreier", "Kotaku"),
    ("Kuchera", "Polygon"),
    ("Wardell", "Stardock"),
    ("LAlexander", "Kotaku"),  # Gamasutra not in dataset; use Kotaku as games-press anchor
    ("Grayson", "Kotaku"),
    # Sarkeesian — no firm institutional anchor in our dataset; documented org is Feminist Frequency
    # T&S 2nd-tier
    ("Brookie", "AtlanticCouncil"), ("Brookie", "DFRLab"), ("Brookie", "NSC"),
    ("SBrill", "NewsGuard"),
    ("Crovitz", "NewsGuard"),
    ("Schiller", "Aspen"),
    ("Ahmed", "CCDH"),
    ("Huffman", "Reddit"),
    ("Ohanian", "Reddit"),
    ("Ressa", "Rappler"),
    ("BFishman", "Meta"),
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
