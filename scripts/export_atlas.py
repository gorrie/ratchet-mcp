"""Phase 2a — export the Atlas data bundle from the canonical graph (+ profile/footprint enrichment).

Data-driven, not hardcoded: the Atlas page loads this JSON, so it stays in sync with people/institutions/
edges.jsonl (the source of truth) instead of a hand-maintained copy like the revolving-door tool. Scopes
to the Atlas node set (scope_atlas), attaches profile_url + footprint where a profile exists, and leaves a
`receipts` slot the precompute step (Phase 1e) fills. Read-only except the JSON it writes.

Output: website/static/tech/ratchet-atlas/atlas-data.json
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PROFILES = ROOT.parents[1] / "website" / "content" / "profiles"
OUT = ROOT.parents[1] / "website" / "static" / "tech" / "ratchet-atlas" / "atlas-data.json"


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def footprint_of(md_text: str) -> str:
    m = re.search(r"\*\*Public footprint:\*\*\s*(.+)", md_text)
    return m.group(1).strip() if m else ""


def main():
    people = {r["id"]: r for r in load_jsonl(DATA / "people.jsonl")}
    insts = {r["id"]: r for r in load_jsonl(DATA / "institutions.jsonl")}
    edges = load_jsonl(DATA / "edges.jsonl")

    # precomputed method-marker receipts (Phase 1e), keyed by person_id
    receipts = {}
    rc_path = DATA / "receipts.jsonl"
    if rc_path.exists():
        for r in load_jsonl(rc_path):
            receipts.setdefault(r["person_id"], []).append(
                {"lens": r["lens"], "span": html.unescape(r["span"]), "url": r.get("url", ""), "date": r.get("date", "")})

    # profile slug -> (url, footprint)
    prof = {}
    for f in PROFILES.glob("*.md"):
        if f.stem == "_index":
            continue
        txt = f.read_text(encoding="utf-8")
        prof[f.stem] = {"url": f"/profiles/{f.stem}/", "footprint": footprint_of(txt)}
    person_slug = {pid: slug(p["label"]) for pid, p in people.items()}
    inst_slug = {iid: slug(i["label"].split("(")[0]) for iid, i in insts.items()}

    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="export the WHOLE network (all people + edge-connected institutions), not "
                         "just the profiled/finance foreground — denser, the full apparatus")
    args = ap.parse_args()

    if args.full:
        node_people = set(people)
        touched = set()
        for e in edges:
            touched.add(e["source"]); touched.add(e["target"])
        node_insts = {iid for iid in insts if iid in touched}   # drop isolated orgs only
    else:
        # scoped foreground: profiled people + finance layer + connecting institutions
        matched_people = {pid for pid, s in person_slug.items() if s in prof}
        fin_people = {pid for pid, p in people.items()
                      if "money" in p.get("actors", []) or p.get("sector") in ("fin", "imf", "cfr")}
        node_people = matched_people | fin_people
        deg = {}
        for e in edges:
            for a, b in ((e["source"], e["target"]), (e["target"], e["source"])):
                if a in node_people and b in insts:
                    deg[b] = deg.get(b, 0) + 1
        matched_insts = {iid for iid, s in inst_slug.items() if s in prof}
        node_insts = matched_insts | {iid for iid, d in deg.items() if d >= 2}
    V = node_people | node_insts

    nodes = []
    for pid in sorted(node_people):
        p = people[pid]
        pr = prof.get(person_slug[pid], {})
        nodes.append({
            "id": pid, "label": p["label"], "kind": "person", "sector": p.get("sector", "tank"),
            "plays": p.get("plays", []), "actors": p.get("actors", []),
            "role": p.get("role", ""), "sources": p.get("sources", []),
            "profile_url": pr.get("url"), "footprint": pr.get("footprint", ""),
            "receipts": receipts.get(pid, []),
        })
    # existing institutions whose profile slug != label-slug
    PROFILE_ALIAS = {"GovAI": "govai", "RAND": "rand-corporation",
                     "UKAISI": "uk-ai-safety-institute", "CAISI": "us-caisi"}
    for iid in sorted(node_insts):
        i = insts[iid]
        pr = prof.get(PROFILE_ALIAS.get(iid) or inst_slug[iid], {})
        nodes.append({
            "id": iid, "label": i["label"], "kind": "institution", "sector": i.get("sector", "tank"),
            "sources": i.get("sources", []), "profile_url": pr.get("url"),
        })

    out_edges = [{"source": e["source"], "target": e["target"]}
                 for e in edges if e["source"] in V and e["target"] in V]

    # named clusters of influence (clusters.json) — resolve each query to its members in V
    pinst = {}                                          # person -> institutions they edge to
    for e in edges:
        if e["source"] in people and e["target"] in insts:
            pinst.setdefault(e["source"], set()).add(e["target"])
        if e["target"] in people and e["source"] in insts:
            pinst.setdefault(e["target"], set()).add(e["source"])

    def resolve(c):
        a = c.get("query", {}).get("args", {})
        acts = list(a.get("actors", [])) + ([a["actor"]] if "actor" in a else [])
        nets = list(a.get("networks", [])) + ([a["network"]] if "network" in a else [])
        inst_filter = set(c.get("filter_ids_via_institutions", []))
        # a cluster with NO recognized constraint must NOT match everyone
        if not (acts or nets or a.get("admins") or "sector" in a or "play" in a or inst_filter):
            return set()
        out = set()
        for pid, p in people.items():
            if all(x in p.get("actors", []) for x in acts) \
               and all(x in p.get("networks", []) for x in nets) \
               and all(x in p.get("admin", []) for x in a.get("admins", [])) \
               and ("sector" not in a or p.get("sector") == a["sector"]) \
               and ("play" not in a or a["play"] in p.get("plays", [])) \
               and (not inst_filter or (pinst.get(pid, set()) & inst_filter)):
                out.add(pid)
        return out
    clusters_out = []
    cpath = DATA / "clusters.json"
    if cpath.exists():
        for c in json.loads(cpath.read_text(encoding="utf-8")).get("clusters", []):
            members = sorted(pid for pid in resolve(c) if pid in V)
            if 2 <= len(members) < len(node_people):   # a real cohort, never "everyone"
                clusters_out.append({"id": c["id"], "label": c["label"],
                                     "summary": c.get("summary", ""), "members": members})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"nodes": nodes, "edges": out_edges, "clusters": clusters_out},
                              ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"  {len(clusters_out)} clusters resolved (>=2 members)")
    npeople = sum(1 for n in nodes if n["kind"] == "person")
    nprof = sum(1 for n in nodes if n.get("profile_url"))
    print(f"atlas-data.json: {len(nodes)} nodes ({npeople} people, {len(nodes)-npeople} inst), "
          f"{len(out_edges)} edges, {nprof} with profiles")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
