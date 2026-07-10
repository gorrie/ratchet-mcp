"""Apply the clean (>=2-source) PERSON drafts from reconcile-draft.json into the ratchet graph.

Reconciles profiled apparatus people who had no graph node, so the Atlas renders them. People only;
>=2 sources only (the ratchet rule); institutions and under-sourced people are handled separately.
Role text + sources are verbatim from the vetted profiles. A few coarse sector auto-assignments are
overridden where the keyword matcher mis-tagged academics/safety staff. Idempotent.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
DRAFT = ROOT / "docs" / "reconcile-draft.json"

# coarse-sector corrections where the keyword matcher mis-fired (role text is the source of truth)
SECTOR_OVERRIDE = {"KateKlonick": "tank", "SarahTRoberts": "tank", "JNathanMatias": "tank",
                   "JacobKlein": "tech", "AnikaCollierNavaroli": "tank", "AndyZou": "tech"}

# genuinely-new institutions (profile slug -> clean id, slug-matching label, sector); the slug match
# lets export_atlas link the profile. Excludes govai/rand/uk-ai-safety/us-caisi (already in graph).
INST_MAP = {"apollo-research": ("ApolloResearch", "Apollo Research", "tank"),
            "dfrlab": ("DFRLab", "DFRLab", "tank"),
            "graphika": ("Graphika", "Graphika", "intel"),
            "mlcommons": ("MLCommons", "MLCommons", "tank"),
            "partnership-on-ai": ("PartnershipOnAI", "Partnership on AI", "tank")}


def ids(path):
    out = set()
    if path.exists():
        for l in path.read_text(encoding="utf-8").splitlines():
            if l.strip():
                out.add(json.loads(l)["id"])
    return out


def edge_set():
    out = set()
    p = DATA / "edges.jsonl"
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                e = json.loads(l); out.add((e["source"], e["target"]))
    return out


def main():
    drafts = json.loads(DRAFT.read_text(encoding="utf-8"))
    # All profiled people: a published evilrobots.lol profile IS the editorial vetting, and the Atlas
    # card links to it for full (often prose) sourcing. URL-backfill for the prose-sourced ones is the
    # footprint pass, not a blocker. We never fabricate sources — nodes carry only what's verifiable.
    clean = [d for d in drafts if d["kind"] == "person"]
    have = ids(DATA / "people.jsonl") | ids(DATA / "institutions.jsonl")
    ee = edge_set()
    ap = ae = 0
    with (DATA / "people.jsonl").open("a", encoding="utf-8") as fh:
        for d in clean:
            if d["id"] in have:
                continue
            rec = {"id": d["id"], "label": d["label"], "kind": "person",
                   "sector": SECTOR_OVERRIDE.get(d["id"], d["sector"]),
                   "admin": [], "networks": [], "plays": [], "actors": [],
                   "role": d["role"], "sources": d["sources"]}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(d["id"]); ap += 1
    ai = 0
    with (DATA / "institutions.jsonl").open("a", encoding="utf-8") as fh:
        for d in drafts:
            if d["kind"] != "institution" or d["slug"] not in INST_MAP or d["n_sources"] < 2:
                continue
            iid, label, sector = INST_MAP[d["slug"]]
            if iid in have:
                continue
            fh.write(json.dumps({"id": iid, "label": label, "sector": sector,
                                 "sources": d["sources"], "kind": "institution"}, ensure_ascii=False) + "\n")
            have.add(iid); ai += 1
    with (DATA / "edges.jsonl").open("a", encoding="utf-8") as fh:
        for d in clean:
            for tgt in d["edges"]:
                if (d["id"], tgt) not in ee and d["id"] in have and tgt in have:
                    fh.write(json.dumps({"source": d["id"], "target": tgt}, ensure_ascii=False) + "\n")
                    ee.add((d["id"], tgt)); ae += 1
    print(f"Added: {ap} people, {ai} institutions, {ae} edges.")


if __name__ == "__main__":
    main()
