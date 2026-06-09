"""v3 addition: China + Russia state institutions (institutional-only, no
named persons) plus documented influence edges from the existing v2
cohort. Per the project's anti-tinfoil rule, only Wikipedia-grade
documented engagements (program founder, board member, repeat speaker)
make it in.

Idempotent: skips records / edges that already exist.

Run from anywhere. Reads + writes the JSONL files in-place.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
INST = DATA / "institutions.jsonl"
EDGES = DATA / "edges.jsonl"

# --- China institutions (10) ----------------------------------------------
CHINA_INSTITUTIONS = [
    {"id": "PBoC", "label": "People's Bank of China", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/People%27s_Bank_of_China"},
         {"type": "official", "url": "http://www.pbc.gov.cn/en/3688006/index.html"},
     ]},
    {"id": "BoaoForum", "label": "Boao Forum for Asia", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Boao_Forum_for_Asia"},
         {"type": "official", "url": "https://english.boaoforum.org/"},
     ]},
    {"id": "CDF", "label": "China Development Forum", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/China_Development_Forum"},
     ]},
    {"id": "Tsinghua", "label": "Tsinghua University", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Tsinghua_University"},
         {"type": "official", "url": "https://www.tsinghua.edu.cn/en/"},
     ]},
    {"id": "AIIB", "label": "Asian Infrastructure Investment Bank", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Asian_Infrastructure_Investment_Bank"},
         {"type": "official", "url": "https://www.aiib.org/"},
     ]},
    {"id": "NDB", "label": "New Development Bank (BRICS)", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/New_Development_Bank"},
         {"type": "official", "url": "https://www.ndb.int/"},
     ]},
    {"id": "BRI", "label": "Belt and Road Initiative", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Belt_and_Road_Initiative"},
     ]},
    {"id": "UFWD", "label": "CCP United Front Work Department", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/United_Front_Work_Department"},
         {"type": "academic", "url": "https://www.aspi.org.au/report/party-speaks-you"},
     ]},
    {"id": "CIC", "label": "China Investment Corporation", "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/China_Investment_Corporation"},
         {"type": "official", "url": "http://www.china-inv.cn/en/"},
     ]},
    {"id": "CIDCA", "label": "China International Development Cooperation Agency",
     "sector": "china-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/China_International_Development_Cooperation_Agency"},
     ]},
]

# --- Russia institutions (6) ----------------------------------------------
RUSSIA_INSTITUTIONS = [
    {"id": "SPIEF", "label": "St. Petersburg International Economic Forum",
     "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Saint_Petersburg_International_Economic_Forum"},
         {"type": "official", "url": "https://forumspb.com/en/"},
     ]},
    {"id": "Valdai", "label": "Valdai Discussion Club", "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Valdai_Discussion_Club"},
         {"type": "official", "url": "https://valdaiclub.com/"},
     ]},
    {"id": "RDIF", "label": "Russian Direct Investment Fund", "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Russian_Direct_Investment_Fund"},
         {"type": "official", "url": "https://rdif.ru/Eng_Index/"},
     ]},
    {"id": "GRU", "label": "Russian Military Intelligence (GRU)",
     "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/GRU"},
     ]},
    {"id": "SVR", "label": "Russian Foreign Intelligence (SVR)",
     "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Foreign_Intelligence_Service_(Russia)"},
     ]},
    {"id": "FSB", "label": "Russian Federal Security Service (FSB)",
     "sector": "russia-state",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Federal_Security_Service"},
     ]},
]

# --- Documented influence edges (existing v2 cohort -> new institutions) --
# Every edge here is justifiable from publicly documented engagement.
# `influence_type` is metadata for the web viewer to dim/highlight; the MCP
# server treats edges as undirected adjacencies regardless.
EDGES_TO_ADD = [
    # Kissinger — diplomatic dean, repeat engagement
    {"source": "Kissinger", "target": "BoaoForum", "influence_type": "documented_attendance"},
    {"source": "Kissinger", "target": "Tsinghua",   "influence_type": "honorary_role"},
    {"source": "Kissinger", "target": "CDF",        "influence_type": "documented_attendance"},
    {"source": "Kissinger", "target": "Valdai",     "influence_type": "documented_attendance"},
    # Paulson — Paulson Institute partnered with Tsinghua's PBC School of Finance
    {"source": "Paulson",   "target": "Tsinghua",   "influence_type": "program_founder"},
    {"source": "Paulson",   "target": "CDF",        "influence_type": "documented_attendance"},
    {"source": "Paulson",   "target": "BoaoForum",  "influence_type": "documented_attendance"},
    # Schwarzman — Schwarzman Scholars founded at Tsinghua, 2013
    {"source": "Schwarzman", "target": "Tsinghua",  "influence_type": "program_founder"},
    {"source": "Schwarzman", "target": "BoaoForum", "influence_type": "documented_attendance"},
    # Schmidt — China AI engagement, CDF speaker
    {"source": "Schmidt",   "target": "CDF",        "influence_type": "documented_attendance"},
    # Schwab — WEF / Boao cooperation agreement; BRI praise documented
    {"source": "Schwab",    "target": "BoaoForum",  "influence_type": "partnership"},
    {"source": "Schwab",    "target": "BRI",        "influence_type": "documented_endorsement"},
    # Summers — Tsinghua advisory board, CDF speaker
    {"source": "Summers",   "target": "Tsinghua",   "influence_type": "advisory"},
    {"source": "Summers",   "target": "CDF",        "influence_type": "documented_attendance"},
    # Geithner — Warburg Pincus chairman, repeat CDF attendee
    {"source": "Geithner",  "target": "CDF",        "influence_type": "documented_attendance"},
    # Bernanke — post-Fed Boao Forum speaker
    {"source": "Bernanke",  "target": "BoaoForum",  "influence_type": "documented_attendance"},
    # Greenspan — Valdai Club speaker
    {"source": "Greenspan", "target": "Valdai",     "influence_type": "documented_attendance"},
    # Fink (BlackRock) — Asian sovereign-wealth engagement (CIC, AIIB observer status)
    {"source": "Fink",      "target": "CIC",        "influence_type": "business_relationship"},
    # Lagarde — IMF MD engagement with BRICS-aligned multilaterals
    {"source": "Lagarde",   "target": "NDB",        "influence_type": "multilateral_coordination"},
    # Fischer (Stanley) — IMF era, AIIB consultations
    {"source": "Fischer",   "target": "AIIB",       "influence_type": "multilateral_coordination"},
    # Zoellick (WB Pres) — multilateral bank diplomacy
    {"source": "Zoellick",  "target": "AIIB",       "influence_type": "multilateral_coordination"},
    {"source": "Zoellick",  "target": "CDF",        "influence_type": "documented_attendance"},
]


def read_jsonl(path: Path) -> list[dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def main() -> None:
    institutions = read_jsonl(INST)
    edges = read_jsonl(EDGES)
    existing_inst_ids = {r["id"] for r in institutions}
    existing_edges = {(e.get("source"), e.get("target")) for e in edges if isinstance(e, dict)}

    new_inst = 0
    for rec in CHINA_INSTITUTIONS + RUSSIA_INSTITUTIONS:
        if rec["id"] in existing_inst_ids:
            continue
        rec["kind"] = "institution"
        institutions.append(rec)
        new_inst += 1

    new_edges = 0
    for e in EDGES_TO_ADD:
        key = (e["source"], e["target"])
        if key in existing_edges:
            continue
        edges.append(e)
        new_edges += 1

    with INST.open("w", encoding="utf-8") as f:
        for rec in institutions:
            f.write(json.dumps(rec) + "\n")
    with EDGES.open("w", encoding="utf-8") as f:
        for e in edges:
            f.write(json.dumps(e) + "\n")

    print(f"Added {new_inst} institutions, {new_edges} edges.")
    print(f"Totals: {len(institutions)} institutions, {len(edges)} edges.")


if __name__ == "__main__":
    main()
