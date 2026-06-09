"""Health-Governance Ratchet (Click #14: The Hospital) institutional + named adds.

Per the 2026-05-29 research agent: structurally DISTINCT from US/UK
revolving-door Ratchet. Pattern is philanthropic-funding-determinism +
institutional embedding (Gates Foundation funds Gavi/CEPI -> shapes
their priorities -> WHO + multilateral coordination). Personnel rotate
(Farrar Wellcome->WHO, Dybul PEPFAR->Global Fund, Hatchett BARDA->CEPI),
but the structural lock is funding, not employment.

Per author anti-defamation rule: role text is POSITIONS-ONLY. No
characterizations like "epistemic monopoly" / "Follow the science" /
"WHO-China dynamics" — those are pundit shorthand. Document the
publicly-documented institutional positions only.

Institutions (7): Gavi, CEPI, Wellcome, PEPFAR, GISAID, GlobalFund,
BARDA, plus NIAID if missing.

Persons (7): Fauci (NIAID), MChan (WHO DG predecessor to Tedros),
Farrar (Wellcome -> WHO), Berkley (Gavi), Hatchett (BARDA -> CEPI),
Dybul (PEPFAR -> Global Fund), Birx (Trump COVID coordinator),
Slaoui (Operation Warp Speed).
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
    {"id": "Gavi", "label": "Gavi, the Vaccine Alliance", "sector": "tank",
     "sources": [w("GAVI"), off("https://www.gavi.org/")]},
    {"id": "CEPI", "label": "Coalition for Epidemic Preparedness Innovations", "sector": "tank",
     "sources": [w("Coalition_for_Epidemic_Preparedness_Innovations"), off("https://cepi.net/")]},
    {"id": "Wellcome", "label": "Wellcome Trust", "sector": "tank",
     "sources": [w("Wellcome_Trust"), off("https://wellcome.org/")]},
    {"id": "PEPFAR", "label": "US President's Emergency Plan for AIDS Relief", "sector": "gov",
     "sources": [w("President%27s_Emergency_Plan_for_AIDS_Relief"), off("https://www.state.gov/pepfar/")]},
    {"id": "GISAID", "label": "GISAID (Global Initiative on Sharing All Influenza Data)",
     "sector": "tank",
     "sources": [w("GISAID"), off("https://www.gisaid.org/")]},
    {"id": "GlobalFund", "label": "Global Fund to Fight AIDS, Tuberculosis and Malaria",
     "sector": "multi",
     "sources": [w("Global_Fund_to_Fight_AIDS,_Tuberculosis_and_Malaria"),
                 off("https://www.theglobalfund.org/")]},
    {"id": "BARDA", "label": "Biomedical Advanced Research and Development Authority (HHS)",
     "sector": "gov",
     "sources": [w("Biomedical_Advanced_Research_and_Development_Authority"),
                 off("https://aspr.hhs.gov/AboutASPR/ProgramOffices/BARDA/")]},
    {"id": "NIAID", "label": "National Institute of Allergy and Infectious Diseases (NIH)",
     "sector": "gov",
     "sources": [w("National_Institute_of_Allergy_and_Infectious_Diseases"),
                 off("https://www.niaid.nih.gov/")]},
    {"id": "WHO_HEP", "label": "WHO Health Emergencies Programme", "sector": "multi",
     "sources": [w("World_Health_Organization"),
                 off("https://www.who.int/our-work/health-emergencies/")]},
]


NEW_PERSONS = [
    {"id": "Fauci", "label": "Anthony Fauci", "sector": "gov",
     "admin": ["reagan", "bush1", "clinton", "bush2", "obama", "trump1", "biden"], "networks": [],
     "plays": [], "actors": [],
     "role": "NIH career researcher -> Director of the National Institute of Allergy and Infectious Diseases 1984-2022 -> Chief Medical Advisor to the President 2021-22 -> Georgetown University Distinguished University Professor 2023-",
     "sources": [w("Anthony_Fauci"), wd("Q573665"),
                 gov("https://www.niaid.nih.gov/about/anthony-s-fauci-md-bio")]},
    {"id": "MChan", "label": "Margaret Chan", "sector": "multi",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Hong Kong Department of Health Director -> WHO Western Pacific Regional Director -> WHO Director-General 2006-17 (predecessor of Tedros) -> Boao Forum Vision Foundation Chair",
     "sources": [w("Margaret_Chan"), wd("Q298232"),
                 off("https://www.who.int/director-general/former-directors-general")]},
    {"id": "Farrar", "label": "Jeremy Farrar", "sector": "multi",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Oxford University researcher (infectious diseases) -> Director of Wellcome Trust 2013-23 (Wellcome co-funded CEPI launch $460M 2017; additional $300M 2022 commitment with Gates Foundation) -> WHO Chief Scientist 2023-",
     "sources": [w("Jeremy_Farrar"), wd("Q6182905"),
                 off("https://www.who.int/news/item/13-12-2022-world-health-organization-names-sir-jeremy-farrar-as-chief-scientist")]},
    {"id": "Berkley", "label": "Seth Berkley", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Rockefeller Foundation health programs -> International AIDS Vaccine Initiative founding President + CEO 1996-2011 -> Gavi CEO 2011-23",
     "sources": [w("Seth_Berkley"), wd("Q7457087"),
                 off("https://www.gavi.org/")]},
    {"id": "Hatchett", "label": "Richard Hatchett", "sector": "tank",
     "admin": ["bush2", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Bush2 White House Homeland Security Council biodefense policy -> Obama Office of Science and Technology Policy -> BARDA (HHS) Director -> CEPI CEO 2017-",
     "sources": [w("Coalition_for_Epidemic_Preparedness_Innovations"), wd("Q56402290"),
                 off("https://cepi.net/about/leadership/")]},
    {"id": "Dybul", "label": "Mark Dybul", "sector": "multi",
     "admin": ["bush2"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "NIH researcher -> Director of PEPFAR (US Global AIDS Coordinator) 2006-09 -> Georgetown Global Health -> Executive Director of the Global Fund to Fight AIDS, Tuberculosis and Malaria 2012-17 -> Georgetown Global Health Institute Co-Director",
     "sources": [w("Mark_R._Dybul"), wd("Q6770062"),
                 off("https://globalhealth.georgetown.edu/people/mark-dybul")]},
    {"id": "Birx", "label": "Deborah Birx", "sector": "gov",
     "admin": ["bush2", "obama", "trump1"], "networks": [],
     "plays": [], "actors": [],
     "role": "US Army Medical Corps physician -> CDC HIV/AIDS Division -> Director of CDC Global AIDS Program -> US Global AIDS Coordinator (Ambassador-at-Large) 2014-21 -> White House Coronavirus Response Coordinator 2020-21 -> ActivePure Technologies Chief Medical and Scientific Advisor",
     "sources": [w("Deborah_Birx"), wd("Q22247843"),
                 gov("https://coronavirus.house.gov/news/press-releases/former-white-house-coronavirus-task-force-coordinator-dr-deborah-birx-testify")]},
    {"id": "Slaoui", "label": "Moncef Slaoui", "sector": "tech",
     "admin": ["trump1"], "networks": [],
     "plays": ["acquisition", "pipeline"], "actors": [],
     "role": "GSK Chief Scientific Officer + Chairman of Global Vaccines (29 years) -> Moderna board -> Operation Warp Speed Chief Scientific Adviser May 2020-Jan 2021 -> Centessa Pharmaceuticals Chairman -> resigned roles March 2021 after GSK investigation finding",
     "sources": [w("Moncef_Slaoui"), wd("Q88498032"),
                 off("https://www.hhs.gov/coronavirus/explaining-operation-warp-speed/index.html")]},
]


NEW_EDGES = [
    # Gates ecosystem
    ("BGates", "Gavi"), ("BGates", "CEPI"),
    ("GatesFoundation", "Gavi"), ("GatesFoundation", "CEPI"),
    # Wellcome co-funded CEPI
    ("Wellcome", "CEPI"),
    # Farrar pipeline
    ("Farrar", "Wellcome"), ("Farrar", "WHO"),
    # Berkley
    ("Berkley", "Gavi"),
    # Hatchett
    ("Hatchett", "BARDA"), ("Hatchett", "CEPI"), ("Hatchett", "WhiteHouse"),
    # Dybul
    ("Dybul", "PEPFAR"), ("Dybul", "GlobalFund"), ("Dybul", "Georgetown"),
    # Fauci
    ("Fauci", "NIAID"), ("Fauci", "WhiteHouse"), ("Fauci", "Georgetown"),
    # Birx
    ("Birx", "WhiteHouse"), ("Birx", "PEPFAR"),
    # Slaoui
    ("Slaoui", "WhiteHouse"),
    # WHO leadership continuity
    ("MChan", "WHO"),
    ("Tedros", "WHO_HEP"),  # already linked to WHO; add HEP-specific
    # Gates Foundation -> WHO funding flow is the structural lock
    ("GatesFoundation", "WHO"),
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
