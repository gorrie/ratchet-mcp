"""One-time fix: split the duplicated `Powell` id into CPowell (Colin)
and Powell (Jerome). Updates people.jsonl + edges.jsonl in place.

Colin's institutional edges (DoD, State, CFR-first, NSC) → CPowell.
Jerome's edges (Treasury, Carlyle, FedReserve, CFR-second) → Powell.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PEOPLE = DATA / "people.jsonl"
EDGES = DATA / "edges.jsonl"

# People: rename the FIRST Powell (Colin) to CPowell; keep the second (Jerome).
out_people = []
seen_powell = False
with PEOPLE.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec["id"] == "Powell":
            if not seen_powell:
                seen_powell = True
                # First Powell encountered = Colin (per inspection order).
                if rec.get("label", "").startswith("Colin"):
                    rec["id"] = "CPowell"
                # else Jerome came first — keep as Powell, mark seen.
            # second occurrence: keep as Powell (Jerome) if Colin was renamed,
            # otherwise we have a problem.
        out_people.append(rec)

with PEOPLE.open("w", encoding="utf-8") as f:
    for rec in out_people:
        f.write(json.dumps(rec) + "\n")

# Edges: edges 1-4 listed in extraction order belong to Colin.
# (DoD, State, CFR, NSC) → CPowell. Remaining Powell edges keep Powell.
colin_targets = {"DoD", "State", "NSC"}  # CFR is shared; we resolve by edge index.
out_edges = []
cfr_seen = 0
with EDGES.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if isinstance(e, list):
            src, tgt = e[0], e[1]
            e = {"source": src, "target": tgt}
        if e.get("source") == "Powell":
            if e["target"] in colin_targets:
                e["source"] = "CPowell"
            elif e["target"] == "CFR":
                cfr_seen += 1
                if cfr_seen == 1:
                    e["source"] = "CPowell"
                # second CFR edge stays Powell (Jerome)
        out_edges.append(e)

with EDGES.open("w", encoding="utf-8") as f:
    for e in out_edges:
        f.write(json.dumps(e) + "\n")

print(f"Renamed Colin Powell -> CPowell, redirected {1 + len(colin_targets)} edges.")
