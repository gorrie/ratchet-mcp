"""v3 batch 4: Big Tech CEOs, defense contractor C-suite, and the
foundation cohort (Gates Foundation, Open Society Foundations,
Bloomberg LP). The anti-tinfoil rule from SCOPE.md applies hardest
here: foundations are documented institutional actors (their trustees
and grants are public) — IN. Bloodline-conspiracy framing — OUT.

Big Tech CEOs (6): Pichai (Alphabet), Nadella (Microsoft), Dorsey
(Twitter/Square/Bluesky), Spiegel (Snap), Wojcicki (YouTube), BGates
(Microsoft founder + Gates Foundation co-chair).

Defense contractor C-suite (6): Calhoun (Boeing), Taiclet (Lockheed),
Warden (Northrop), Hayes (RTX), Kubasik (L3Harris), Novakovic (GD).

Foundation / NGO leaders (4): Suzman (Gates Foundation), Gaspard
(OSF), MalloochBrown (OSF), Bloomberg (Bloomberg LP + Mayor NYC).

Plus Munger (Berkshire Hathaway VC, Buffett partner).

Idempotent.
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
    {"id": "Alphabet", "label": "Alphabet Inc.", "sector": "tech",
     "sources": [w("Alphabet_Inc."), off("https://abc.xyz/")]},
    {"id": "Snap", "label": "Snap Inc.", "sector": "tech",
     "sources": [w("Snap_Inc."), off("https://snap.com/")]},
    {"id": "YouTube", "label": "YouTube", "sector": "tech",
     "sources": [w("YouTube"), off("https://www.youtube.com/about/")]},
    {"id": "Bluesky", "label": "Bluesky", "sector": "tech",
     "sources": [w("Bluesky_Social"), off("https://bsky.social/about")]},
    {"id": "Boeing", "label": "Boeing", "sector": "def",
     "sources": [w("Boeing"), off("https://www.boeing.com/")]},
    {"id": "Lockheed", "label": "Lockheed Martin", "sector": "def",
     "sources": [w("Lockheed_Martin"), off("https://www.lockheedmartin.com/")]},
    {"id": "Northrop", "label": "Northrop Grumman", "sector": "def",
     "sources": [w("Northrop_Grumman"), off("https://www.northropgrumman.com/")]},
    {"id": "RTX", "label": "RTX Corporation (Raytheon)", "sector": "def",
     "sources": [w("RTX_Corporation"), off("https://www.rtx.com/")]},
    {"id": "L3Harris", "label": "L3Harris Technologies", "sector": "def",
     "sources": [w("L3Harris_Technologies"), off("https://www.l3harris.com/")]},
    {"id": "GD", "label": "General Dynamics", "sector": "def",
     "sources": [w("General_Dynamics"), off("https://www.gd.com/")]},
    {"id": "BerkshireHathaway", "label": "Berkshire Hathaway", "sector": "fin",
     "sources": [w("Berkshire_Hathaway"), off("https://www.berkshirehathaway.com/")]},
    {"id": "GatesFoundation", "label": "Bill & Melinda Gates Foundation",
     "sector": "tank",
     "sources": [w("Bill_%26_Melinda_Gates_Foundation"), off("https://www.gatesfoundation.org/")]},
    {"id": "OSF", "label": "Open Society Foundations", "sector": "tank",
     "sources": [w("Open_Society_Foundations"), off("https://www.opensocietyfoundations.org/")]},
    {"id": "BloombergLP", "label": "Bloomberg L.P.", "sector": "tech",
     "sources": [w("Bloomberg_L.P."), off("https://www.bloomberg.com/company/")]},
    {"id": "FordFoundation", "label": "Ford Foundation", "sector": "tank",
     "sources": [w("Ford_Foundation"), off("https://www.fordfoundation.org/")]},
    {"id": "RockefellerFoundation", "label": "Rockefeller Foundation", "sector": "tank",
     "sources": [w("Rockefeller_Foundation"), off("https://www.rockefellerfoundation.org/")]},
    {"id": "CarnegieEndowment", "label": "Carnegie Endowment for International Peace",
     "sector": "tank",
     "sources": [w("Carnegie_Endowment_for_International_Peace"), off("https://carnegieendowment.org/")]},
]

NEW_PERSONS = [
    # ---- Big Tech CEOs ---------------------------------------------------
    {"id": "Pichai", "label": "Sundar Pichai", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "blueprint"],
     "role": "Applied Materials -> McKinsey -> Google Chrome/Apps lead -> Google CEO 2015- -> Alphabet CEO 2019-",
     "sources": [w("Sundar_Pichai"), wd("Q1336262"),
                 off("https://abc.xyz/investor/founders-letters/")]},
    {"id": "Nadella", "label": "Satya Nadella", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["blueprint"],
     "role": "Sun Microsystems -> Microsoft Server and Tools / Bing / Cloud + Enterprise -> Microsoft CEO 2014- -> Microsoft Chairman 2021-",
     "sources": [w("Satya_Nadella"), wd("Q3110505"),
                 off("https://news.microsoft.com/exec/satya-nadella/")]},
    {"id": "Dorsey", "label": "Jack Dorsey", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "flagging"],
     "role": "Twitter co-founder 2006 -> Twitter CEO 2006-08, 2015-21 -> Square (later Block) co-founder/CEO 2009- -> Bluesky board",
     "sources": [w("Jack_Dorsey"), wd("Q313060"),
                 off("https://block.xyz/")]},
    {"id": "Spiegel", "label": "Evan Spiegel", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Snap Inc. co-founder 2011 -> Snap CEO 2011-",
     "sources": [w("Evan_Spiegel"), wd("Q15869"),
                 off("https://snap.com/en-US/team")]},
    {"id": "Wojcicki", "label": "Susan Wojcicki", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm"],
     "role": "Intel -> Google employee #16 -> Senior VP Advertising and Commerce -> YouTube CEO 2014-23",
     "sources": [w("Susan_Wojcicki"), wd("Q469940"),
                 off("https://about.youtube/")]},
    {"id": "BGates", "label": "Bill Gates", "sector": "tech",
     "admin": [], "networks": ["bilderberg"],
     "plays": [], "actors": [],
     "role": "Microsoft co-founder 1975 -> Microsoft CEO 1975-2000 -> Microsoft Chairman 1981-2014 -> Bill & Melinda Gates Foundation co-founder/co-chair 2000-",
     "sources": [w("Bill_Gates"), wd("Q5284"),
                 off("https://www.gatesnotes.com/")]},

    # ---- Defense contractor C-suite -------------------------------------
    {"id": "Calhoun", "label": "David L. Calhoun", "sector": "def",
     "admin": [], "networks": [],
     "plays": ["acquisition"], "actors": [],
     "role": "GE Vice Chairman -> Nielsen Holdings CEO -> Blackstone Senior Managing Director -> Boeing Chairman 2019-20 -> Boeing CEO 2020-24",
     "sources": [w("David_L._Calhoun"), wd("Q5235068"),
                 off("https://www.boeing.com/company/leadership/")]},
    {"id": "Taiclet", "label": "James Taiclet", "sector": "def",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Air Force officer -> Pratt & Whitney -> McKinsey -> Honeywell -> American Tower Corporation CEO 2003-20 -> Lockheed Martin CEO 2020-",
     "sources": [w("James_Taiclet"), wd("Q105827611"),
                 off("https://www.lockheedmartin.com/en-us/who-we-are/leadership-governance/")]},
    {"id": "Warden", "label": "Kathy J. Warden", "sector": "def",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "General Dynamics IT -> Northrop Grumman President -> Northrop Grumman CEO 2019- -> Chair 2020-",
     "sources": [w("Kathy_Warden"), wd("Q60734070"),
                 off("https://www.northropgrumman.com/who-we-are/leadership/")]},
    {"id": "GHayes", "label": "Greg Hayes", "sector": "def",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "United Technologies CFO -> United Technologies CEO 2014-20 -> Raytheon Technologies (now RTX) CEO 2020-24 -> RTX Chairman 2024-",
     "sources": [w("Gregory_J._Hayes"), wd("Q42178010"),
                 off("https://www.rtx.com/who-we-are/leadership")]},
    {"id": "Kubasik", "label": "Chris Kubasik", "sector": "def",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Lockheed Martin COO -> L3 Technologies CEO -> L3Harris Technologies CEO 2021-",
     "sources": [w("L3Harris_Technologies"), wd("Q104107693"),
                 off("https://www.l3harris.com/company/leadership")]},
    {"id": "Novakovic", "label": "Phebe Novakovic", "sector": "def",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "CIA officer -> OMB -> General Dynamics SVP Planning -> General Dynamics CEO 2013-",
     "sources": [w("Phebe_Novakovic"), wd("Q7180059"),
                 off("https://www.gd.com/leadership")]},

    # ---- Foundation / NGO leaders + others ------------------------------
    {"id": "Suzman", "label": "Mark Suzman", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "South African journalist -> Financial Times -> UN Development Programme -> Gates Foundation various roles 2007-19 -> Gates Foundation CEO 2020-",
     "sources": [w("Mark_Suzman"), wd("Q86683010"),
                 off("https://www.gatesfoundation.org/about/leadership/mark-suzman")]},
    {"id": "Gaspard", "label": "Patrick Gaspard", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Obama campaign National Political Director -> White House Political Director -> Democratic National Committee Executive Director -> US Ambassador to South Africa 2013-16 -> Open Society Foundations President 2018-20 -> Center for American Progress President + CEO 2021-",
     "sources": [w("Patrick_Gaspard"), wd("Q7144987"),
                 off("https://americanprogress.org/about/our-leadership/")]},
    {"id": "MalloochBrown", "label": "Mark Malloch Brown", "sector": "multi",
     "admin": [], "networks": [],
     "plays": ["bretton"], "actors": [],
     "role": "UNDP Administrator -> UN Deputy Secretary-General 2006 -> UK Minister of State for Africa, Asia and the UN 2007-09 (Lord Malloch-Brown) -> Smartmatic Chair -> Open Society Foundations President 2021-",
     "sources": [w("Mark_Malloch_Brown,_Baron_Malloch-Brown"), wd("Q1899020"),
                 off("https://www.opensocietyfoundations.org/who-we-are/leadership/mark-malloch-brown")]},
    {"id": "Bloomberg", "label": "Michael Bloomberg", "sector": "tech",
     "admin": [], "networks": ["cfr", "bilderberg"],
     "plays": ["acquisition"], "actors": [],
     "role": "Salomon Brothers -> Bloomberg L.P. founder 1981 -> Mayor of New York City 2002-13 -> Bloomberg Philanthropies founder -> Democratic presidential candidate 2020",
     "sources": [w("Michael_Bloomberg"), wd("Q607"),
                 off("https://www.bloomberg.com/company/values/founder/")]},
    {"id": "Munger", "label": "Charlie Munger", "sector": "fin",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Munger Tolles & Olson co-founder -> Wesco Financial Chairman -> Berkshire Hathaway Vice Chairman 1978-2023",
     "sources": [w("Charlie_Munger"), wd("Q484125"),
                 off("https://www.berkshirehathaway.com/")]},
]

NEW_EDGES = [
    # Tech CEOs
    ("Pichai", "Google"), ("Pichai", "Alphabet"),
    ("Nadella", "Microsoft"),
    ("Dorsey", "X_Corp"), ("Dorsey", "Bluesky"),
    ("Spiegel", "Snap"),
    ("Wojcicki", "YouTube"), ("Wojcicki", "Google"),
    ("BGates", "Microsoft"), ("BGates", "GatesFoundation"),
    # Defense contractor C-suite
    ("Calhoun", "Boeing"), ("Calhoun", "Blackstone"),
    ("Taiclet", "Lockheed"),
    ("Warden", "Northrop"),
    ("GHayes", "RTX"),
    ("Kubasik", "L3Harris"), ("Kubasik", "Lockheed"),
    ("Novakovic", "GD"), ("Novakovic", "CIA"), ("Novakovic", "OMB"),
    # Foundation / NGO
    ("Suzman", "GatesFoundation"),
    ("Gaspard", "OSF"), ("Gaspard", "WhiteHouse"),
    ("MalloochBrown", "OSF"), ("MalloochBrown", "UN"),
    ("Bloomberg", "BloombergLP"),
    ("Munger", "BerkshireHathaway"), ("Munger", "MungerTolles"),
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
