"""Quick analysis: for each candidate nation-state, how many persons /
institutions are already in the dataset that would form the seed of a
Ratchet cluster? Higher density = lower-effort full cluster; lower
density = needs research before deciding.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"

# Nation candidates + the institution IDs / role-text-keywords that identify them
CANDIDATES = {
    "Canada": ["CanadaGov", "BoC", "Carney", "Trudeau", "Freeland"],
    "Australia": ["AUGov", "Albanese"],
    "New Zealand": ["NZGov", "Ardern", "Luxon"],
    "Japan": ["JPGov", "Kishida"],
    "South Korea": [],
    "Saudi Arabia": [],
    "UAE": [],
    "Brazil": [],
    "Mexico": [],
    "South Africa": [],
    "Turkey": [],
    "Iran": [],
}

people = []
with (DATA / "people.jsonl").open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line: people.append(json.loads(line))
institutions = []
with (DATA / "institutions.jsonl").open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line: institutions.append(json.loads(line))
edges = []
with (DATA / "edges.jsonl").open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line: edges.append(json.loads(line))

inst_by_id = {i["id"]: i for i in institutions}
people_by_id = {p["id"]: p for p in people}

print("=" * 80)
print(f"Nation-Ratchet density check — {len(people)} persons / {len(institutions)} institutions / {len(edges)} edges")
print("=" * 80)
print()
for nation, ids in CANDIDATES.items():
    inst_count = sum(1 for x in ids if x in inst_by_id)
    person_count = sum(1 for x in ids if x in people_by_id)
    edges_to = sum(1 for e in edges if (e.get("source") in ids or e.get("target") in ids))
    # Also count role-text keyword matches as proxy for any-nation mentions
    keyword_role_hits = sum(1 for p in people if nation.lower() in (p.get("role","").lower()))
    print(f"{nation:18}  inst:{inst_count:2}  persons:{person_count:2}  edges:{edges_to:3}  role-text-mentions:{keyword_role_hits:3}")

print()
print("Interpretation:")
print("- High density (5+ existing nodes + 10+ edges): minor batch tops it off as a real cluster")
print("- Medium density (2-4 nodes + 5-10 edges): research-batch to find next-tier persons + institutions")
print("- Low density (<2 nodes): research first to determine if there's a coherent Ratchet pattern worth modeling")
