"""Gulf states + Egypt customer-cohort institutional adds.

Per the 2026-05-29 research agent verdict: Saudi Arabia, UAE, Egypt,
Bahrain are all documented CUSTOMERS of NSO Pegasus / Cellebrite /
Predator / Hacking Team. Qatar is non-player (defensive only;
targeted BY operators). None warrant full Ratchet cluster modeling
— they belong as institutional nodes in the customer-cohort sub-graph.

Per author 2026-05-29 anti-defamation rule for foreign nationals:
INSTITUTIONAL-ONLY for these states. No named heads-of-state even
where documented (MBS, MbZ) — same posture as Cohort F (China/Russia).

Institutions added:
- Saudi: GIP, KFCRIS, PIF, SaudiGov
- UAE: SSA_UAE, ADIA, DarkMatter, UAEGov
- Egypt: GIS_Egypt, EgyptGov
- Bahrain: BahrainGov
- Qatar: QIA, NCSA_Qatar, AlJazeera, QatarGov
- Vendor: Cytrox (Predator spyware), HackingTeam (legacy)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def off(url): return {"type": "official", "url": url}
def acad(url): return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    # Saudi Arabia
    {"id": "GIP_Saudi", "label": "General Intelligence Presidency (Saudi Arabia)", "sector": "intel",
     "sources": [w("General_Intelligence_Presidency"),
                 acad("https://citizenlab.ca/research/hide-and-seek-tracking-nso-groups-pegasus-spyware-to-operations-in-45-countries/")]},
    {"id": "KFCRIS", "label": "King Faisal Center for Research and Islamic Studies", "sector": "tank",
     "sources": [w("King_Faisal_Center_for_Research_and_Islamic_Studies"), off("https://kfcris.com/en/")]},
    {"id": "PIF", "label": "Saudi Public Investment Fund", "sector": "fin",
     "sources": [w("Public_Investment_Fund"), off("https://www.pif.gov.sa/en/")]},
    {"id": "SaudiGov", "label": "Government of Saudi Arabia", "sector": "gov",
     "sources": [w("Politics_of_Saudi_Arabia"), off("https://www.saudiembassy.net/")]},
    # UAE
    {"id": "SSA_UAE", "label": "State Security Department (UAE)", "sector": "intel",
     "sources": [w("State_Security_(United_Arab_Emirates)"),
                 acad("https://citizenlab.ca/research/")]},
    {"id": "ADIA", "label": "Abu Dhabi Investment Authority", "sector": "fin",
     "sources": [w("Abu_Dhabi_Investment_Authority"), off("https://www.adia.ae/")]},
    {"id": "DarkMatter", "label": "DarkMatter Group (UAE)", "sector": "intel",
     "sources": [w("DarkMatter_(Emirati_company)"),
                 acad("https://www.reuters.com/article/usa-spying-raven-idUSL2N1ZN1AT/")]},
    {"id": "UAEGov", "label": "Government of the United Arab Emirates", "sector": "gov",
     "sources": [w("Politics_of_the_United_Arab_Emirates"), off("https://u.ae/")]},
    # Egypt
    {"id": "GIS_Egypt", "label": "General Intelligence Service (Egypt) — Technical Research Division",
     "sector": "intel",
     "sources": [w("General_Intelligence_Service_(Egypt)"),
                 acad("https://www.privacyinternational.org/sites/default/files/2018-02/egypt_reportEnglish_0.pdf")]},
    {"id": "EgyptGov", "label": "Government of Egypt", "sector": "gov",
     "sources": [w("Politics_of_Egypt"), off("https://www.cabinet.gov.eg/")]},
    # Bahrain
    {"id": "BahrainGov", "label": "Government of Bahrain", "sector": "gov",
     "sources": [w("Politics_of_Bahrain"), off("https://www.bahrain.bh/")]},
    {"id": "NSA_Bahrain", "label": "National Security Agency (Bahrain)", "sector": "intel",
     "sources": [w("National_Security_Agency_(Bahrain)"),
                 acad("https://citizenlab.ca/2021/08/bahrain-hacks-activists-with-nso-group-zero-click-iphone-exploits/")]},
    # Qatar
    {"id": "QIA", "label": "Qatar Investment Authority", "sector": "fin",
     "sources": [w("Qatar_Investment_Authority"), off("https://www.qia.qa/")]},
    {"id": "NCSA_Qatar", "label": "National Cyber Security Agency (Qatar)", "sector": "intel",
     "sources": [w("National_Cyber_Security_Agency_(Qatar)"), off("https://www.ncsa.gov.qa/en")]},
    {"id": "AlJazeera", "label": "Al Jazeera Media Network", "sector": "tech",
     "sources": [w("Al_Jazeera"), off("https://www.aljazeera.com/")]},
    {"id": "QatarGov", "label": "Government of Qatar", "sector": "gov",
     "sources": [w("Politics_of_Qatar"), off("https://www.gco.gov.qa/en/")]},
    # Vendors (commercial surveillance ecosystem)
    {"id": "Cytrox", "label": "Cytrox / Intellexa (Predator spyware)", "sector": "tech",
     "sources": [w("Intellexa"),
                 acad("https://citizenlab.ca/research/pegasus-vs-predator-dissidents-doubly-infected-iphone-reveals-cytrox-mercenary-spyware/")]},
    {"id": "HackingTeam", "label": "Hacking Team / Memento Labs", "sector": "tech",
     "sources": [w("Hacking_Team"), off("https://memento-labs.com/")]},
    {"id": "FinFisher", "label": "FinFisher / Gamma Group (legacy)", "sector": "tech",
     "sources": [w("FinFisher")]},
]


# Edges document the CUSTOMER relationship: vendor -> customer state.
# Per the agent verdict, these are flow directions worth modeling:
NEW_EDGES = [
    # NSO Pegasus customer relationships (already added NSO institution earlier)
    ("NSO", "GIP_Saudi"),     # documented Saudi GIP NSO contract per Citizen Lab
    ("NSO", "SSA_UAE"),       # documented UAE Pegasus operator per Citizen Lab
    ("NSO", "GIS_Egypt"),     # documented Egypt Pegasus targeting per Citizen Lab
    ("NSO", "NSA_Bahrain"),   # LULU operator per Citizen Lab
    # Cellebrite customer (Cellebrite already in dataset)
    ("Cellebrite", "SSA_UAE"),  # documented $3M Abu Dhabi deal per Citizen Lab
    ("Cellebrite", "GIS_Egypt"),  # documented Egyptian deployment
    # Cytrox / Predator customer
    ("Cytrox", "GIS_Egypt"),  # documented Eltantawy targeting May-Sept 2023 per Citizen Lab
    # Hacking Team legacy customer
    ("HackingTeam", "GIS_Egypt"),  # documented per Privacy International leaked-document 2016 report
    # DarkMatter as UAE-hosted contractor (uses ex-NSA + Unit 8200)
    # Already noted in role text; no edge from NSA/Unit8200 to DarkMatter (would imply employment which is more nuanced)
    # PIF -> sovereign wealth investment vehicles; QIA same
    ("PIF", "SaudiGov"),
    ("ADIA", "UAEGov"),
    ("QIA", "QatarGov"),
    # KFCRIS academic node under Saudi
    ("KFCRIS", "SaudiGov"),
    # Al Jazeera under Qatar govt
    ("AlJazeera", "QatarGov"),
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
    edges = read_jsonl(DATA / "edges.jsonl")

    inst_ids = {r["id"] for r in institutions}
    people_set = set()
    for line in (DATA / "people.jsonl").open("r", encoding="utf-8"):
        line = line.strip()
        if line: people_set.add(json.loads(line)["id"])
    edge_keys = {(e.get("source"), e.get("target")) for e in edges if isinstance(e, dict)}
    all_ids = inst_ids | people_set

    new_i = 0
    for rec in NEW_INSTITUTIONS:
        if rec["id"] in inst_ids or rec["id"] in people_set:
            continue
        rec["kind"] = "institution"
        institutions.append(rec); inst_ids.add(rec["id"]); all_ids.add(rec["id"]); new_i += 1
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
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges: f.write(json.dumps(e) + "\n")

    print(f"Added {new_i} institutions, {new_e} edges (institutional-only batch).")
    if skipped: print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people_set)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
