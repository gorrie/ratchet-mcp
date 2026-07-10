"""Phase 1a — scope the Atlas node set (the enrichment worklist).

The flagship Atlas foregrounds the curated set, not all 417 graph nodes. The curated set is operationally
defined as: the people who already have an evilrobots.lol profile, PLUS the finance/funding layer, PLUS
the institutions that connect them. This script computes that subgraph from the data and reports the
enrichment gaps (who lacks a footprint, who lacks texts, who lacks precomputed receipts) so enrichment is
scoped to exactly what the demo renders.

Read-only. Prints a summary and writes docs/atlas-worklist.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PROFILES = ROOT.parents[1] / "website" / "content" / "profiles"
OUT = ROOT / "docs" / "atlas-worklist.json"


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    people = {r["id"]: r for r in load_jsonl(DATA / "people.jsonl")}
    insts = {r["id"]: r for r in load_jsonl(DATA / "institutions.jsonl")}
    edges = load_jsonl(DATA / "edges.jsonl")
    texts_ids = {json.loads(l)["person_id"] for l in (DATA / "texts.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}

    # profile slugs (exclude the section index) + which already carry a footprint
    prof = {}
    for f in PROFILES.glob("*.md"):
        if f.stem == "_index":
            continue
        prof[f.stem] = "Public footprint" in f.read_text(encoding="utf-8")

    # match profiles -> graph people / institutions by normalized label
    person_by_slug = {slug(p["label"]): pid for pid, p in people.items()}
    inst_by_slug = {slug(i["label"]): iid for iid, i in insts.items()}
    # institution labels are messy ("METR (Model Evaluation...)"); also index by leading token
    for iid, i in insts.items():
        inst_by_slug.setdefault(slug(i["label"].split("(")[0]), iid)

    matched_people, matched_insts, unmatched_profiles = {}, {}, []
    for s, has_fp in prof.items():
        if s in person_by_slug:
            matched_people[person_by_slug[s]] = has_fp
        elif s in inst_by_slug:
            matched_insts[inst_by_slug[s]] = has_fp
        else:
            unmatched_profiles.append(s)

    # finance/funding layer: people with the money actor or fin/imf/cfr sector; their funder institutions
    fin_people = {pid for pid, p in people.items()
                  if "money" in p.get("actors", []) or p.get("sector") in ("fin", "imf", "cfr")}
    node_people = set(matched_people) | fin_people
    # institutions in scope: profiled institutions + any institution touching >=2 in-scope people
    deg = {}
    for e in edges:
        s, t = e["source"], e["target"]
        if s in node_people and t in insts:
            deg[t] = deg.get(t, 0) + 1
        if t in node_people and s in insts:
            deg[s] = deg.get(s, 0) + 1
    node_insts = set(matched_insts) | {iid for iid, d in deg.items() if d >= 2}
    V = node_people | node_insts
    E = [e for e in edges if e["source"] in V and e["target"] in V]

    # enrichment gaps among in-scope PEOPLE
    need_footprint = sorted(pid for pid in node_people
                            if pid in matched_people and not matched_people[pid])
    no_profile = sorted(pid for pid in node_people if pid not in matched_people)
    need_texts = sorted(pid for pid in node_people if pid not in texts_ids)
    has_texts = sorted(pid for pid in node_people if pid in texts_ids)

    worklist = {
        "node_people": sorted(node_people), "node_insts": sorted(node_insts),
        "n_people": len(node_people), "n_insts": len(node_insts), "n_edges": len(E),
        "gaps": {
            "profiled_people_missing_footprint": need_footprint,
            "in_scope_people_without_profile": no_profile,
            "people_without_texts": need_texts,
            "people_with_texts (receipts-ready)": has_texts,
        },
        "unmatched_profiles": sorted(unmatched_profiles),
    }
    OUT.write_text(json.dumps(worklist, indent=2), encoding="utf-8")

    print(f"ATLAS NODE SET: {len(node_people)} people + {len(node_insts)} institutions, {len(E)} edges")
    print(f"  (of {len(people)} people / {len(insts)} insts total — foregrounding ~{round(100*len(V)/(len(people)+len(insts)))}%)")
    print(f"\nENRICHMENT GAPS (scoped to the node set):")
    print(f"  profiled people missing a footprint : {len(need_footprint)}")
    print(f"  in-scope people with NO profile yet  : {len(no_profile)}")
    print(f"  in-scope people with NO texts        : {len(need_texts)}")
    print(f"  in-scope people texts-ready (receipts): {len(has_texts)}  -> {', '.join(has_texts)}")
    if unmatched_profiles:
        print(f"\n  profiles not matched to a graph node ({len(unmatched_profiles)}): {', '.join(unmatched_profiles[:12])}{'…' if len(unmatched_profiles)>12 else ''}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
