"""Append the two Q-IDs the backfill missed (O'Neill: Q456921, Lewis: Q1700630)."""
import json
from pathlib import Path

PEOPLE = Path(__file__).resolve().parents[1] / "server" / "data" / "people.jsonl"
PATCHES = {"ORneill": "Q456921", "Lewis": "Q1700630"}

records = []
for line in PEOPLE.open("r", encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    rec = json.loads(line)
    if rec["id"] in PATCHES:
        srcs = rec.get("sources") or []
        if not any(s.get("type") == "wikidata" for s in srcs if isinstance(s, dict)):
            srcs.append({"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{PATCHES[rec['id']]}"})
            rec["sources"] = srcs
    records.append(rec)

with PEOPLE.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")
print("Patched.")
