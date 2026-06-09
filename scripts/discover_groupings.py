"""Discover interesting groupings in the Ratchet dataset.

Goes beyond the 15 predefined clusters in clusters.json by running
mechanical analyses that surface patterns the dataset embeds whether
or not anyone named them yet:

1. Centrality — who/what is most-connected in the graph
2. Co-occurrence — which plays / actors / networks co-occur most
3. Surprise overlaps — 2- and 3-attribute combinations yielding small
   (3-15 person) cohorts; small = thesis-sharp, non-empty = real
4. Admin density — per-administration person counts (where the cohort
   was thickest under whom)
5. Network gravity — which networks have most cross-network members
6. Connector personalities — persons who bridge otherwise-disconnected
   institutional clusters (high betweenness-like indicator)
7. Concentrated edges — institutions with disproportionate edge counts

Writes Markdown report to scripts/_groupings-report.md.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
OUT = ROOT / "scripts" / "_groupings-report.md"


def read_jsonl(path):
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main() -> int:
    people = read_jsonl(DATA / "people.jsonl")
    institutions = read_jsonl(DATA / "institutions.jsonl")
    edges = read_jsonl(DATA / "edges.jsonl")

    persons_by_id = {p["id"]: p for p in people}
    institutions_by_id = {i["id"]: i for i in institutions}

    # Build adjacency
    adj = defaultdict(set)
    for e in edges:
        src, tgt = e.get("source"), e.get("target")
        adj[src].add(tgt)
        adj[tgt].add(src)

    lines = ["# Ratchet Dataset — Discovered Groupings\n"]
    lines.append(f"Snapshot of {len(people)} persons / {len(institutions)} institutions / {len(edges)} edges.\n")
    lines.append("Mechanical analyses below; cross-reference against clusters.json (named human-curated clusters) and SCOPE.md (cohort definitions).\n")

    # ============================================================ Centrality
    lines.append("\n## 1. Centrality — most-connected persons and institutions\n")
    person_degree = Counter()
    inst_degree = Counter()
    for nid, neighbors in adj.items():
        if nid in persons_by_id:
            person_degree[nid] = len(neighbors)
        elif nid in institutions_by_id:
            inst_degree[nid] = len(neighbors)

    lines.append("### Most-connected persons (top 25)\n")
    lines.append("| Person | Edge count | Sector | Plays | Actors |")
    lines.append("|---|---|---|---|---|")
    for pid, deg in person_degree.most_common(25):
        p = persons_by_id[pid]
        plays = ",".join(p.get("plays") or [])
        actors = ",".join(p.get("actors") or [])
        lines.append(f"| `{pid}` ({p.get('label','')}) | {deg} | {p.get('sector','')} | {plays} | {actors} |")

    lines.append("\n### Most-connected institutions (top 25)\n")
    lines.append("| Institution | Person edges | Sector |")
    lines.append("|---|---|---|")
    for iid, deg in inst_degree.most_common(25):
        inst = institutions_by_id[iid]
        lines.append(f"| `{iid}` ({inst.get('label','')}) | {deg} | {inst.get('sector','')} |")

    # ============================================================ Co-occurrence
    lines.append("\n## 2. Co-occurrence — which plays / actors / networks travel together\n")

    def cooccur(field: str, min_count: int = 3):
        pairs = Counter()
        for p in people:
            vals = p.get(field, []) or []
            for a, b in combinations(sorted(set(vals)), 2):
                pairs[(a, b)] += 1
        out = []
        for (a, b), n in pairs.most_common():
            if n >= min_count:
                out.append((a, b, n))
        return out

    lines.append("### Plays that co-occur (>= 3 persons hold both)\n")
    lines.append("| Play A | Play B | Persons with both |")
    lines.append("|---|---|---|")
    for a, b, n in cooccur("plays", 3):
        lines.append(f"| {a} | {b} | {n} |")

    lines.append("\n### Actors that co-occur (>= 3 persons touch both)\n")
    lines.append("| Actor A | Actor B | Persons touching both |")
    lines.append("|---|---|---|")
    for a, b, n in cooccur("actors", 3):
        lines.append(f"| {a} | {b} | {n} |")

    lines.append("\n### Networks that co-occur (>= 3 persons hold both memberships)\n")
    lines.append("| Network A | Network B | Members of both |")
    lines.append("|---|---|---|")
    for a, b, n in cooccur("networks", 3):
        lines.append(f"| {a} | {b} | {n} |")

    # ============================================================ Surprise overlaps
    lines.append("\n## 3. Surprise overlaps — 2-attribute combinations yielding 3-15 person cohorts\n")
    lines.append("Small cohorts are thesis-sharp. These are the unexpected ones — small named-pattern intersections that suggest an unnamed cluster worth investigating.\n")
    lines.append("### Play x Actor intersections\n")
    lines.append("| Play | Actor | Persons | Names |")
    lines.append("|---|---|---|---|")
    pa_pairs = []
    for play_val in {p for pp in people for p in (pp.get("plays") or [])}:
        for actor_val in {a for pp in people for a in (pp.get("actors") or [])}:
            members = [p for p in people
                       if play_val in (p.get("plays") or []) and actor_val in (p.get("actors") or [])]
            if 3 <= len(members) <= 15:
                pa_pairs.append((play_val, actor_val, members))
    for play_val, actor_val, members in sorted(pa_pairs, key=lambda x: (len(x[2]), x[0], x[1])):
        names = ", ".join(m["id"] for m in members)
        lines.append(f"| {play_val} | {actor_val} | {len(members)} | {names} |")

    lines.append("\n### Network x Actor intersections\n")
    lines.append("| Network | Actor | Persons | Names |")
    lines.append("|---|---|---|---|")
    na_pairs = []
    for network_val in {n for pp in people for n in (pp.get("networks") or [])}:
        for actor_val in {a for pp in people for a in (pp.get("actors") or [])}:
            members = [p for p in people
                       if network_val in (p.get("networks") or []) and actor_val in (p.get("actors") or [])]
            if 3 <= len(members) <= 15:
                na_pairs.append((network_val, actor_val, members))
    for network_val, actor_val, members in sorted(na_pairs, key=lambda x: (len(x[2]), x[0], x[1])):
        names = ", ".join(m["id"] for m in members)
        lines.append(f"| {network_val} | {actor_val} | {len(members)} | {names} |")

    lines.append("\n### Admin x Actor intersections (small cohorts)\n")
    lines.append("| Admin | Actor | Persons | Names |")
    lines.append("|---|---|---|---|")
    aa_pairs = []
    for admin_val in {a for pp in people for a in (pp.get("admin") or [])}:
        for actor_val in {a for pp in people for a in (pp.get("actors") or [])}:
            members = [p for p in people
                       if admin_val in (p.get("admin") or []) and actor_val in (p.get("actors") or [])]
            if 3 <= len(members) <= 15:
                aa_pairs.append((admin_val, actor_val, members))
    for admin_val, actor_val, members in sorted(aa_pairs, key=lambda x: (len(x[2]), x[0], x[1])):
        names = ", ".join(m["id"] for m in members)
        lines.append(f"| {admin_val} | {actor_val} | {len(members)} | {names} |")

    # ============================================================ Admin density
    lines.append("\n## 4. Admin density — where the cohort thickens by administration\n")
    admin_count = Counter()
    admin_sector = defaultdict(Counter)
    for p in people:
        for a in (p.get("admin") or []):
            admin_count[a] += 1
            admin_sector[a][p.get("sector", "?")] += 1
    lines.append("| Admin | Total persons | Top sectors |")
    lines.append("|---|---|---|")
    for adm, n in admin_count.most_common():
        top = ", ".join(f"{s}:{c}" for s, c in admin_sector[adm].most_common(4))
        lines.append(f"| {adm} | {n} | {top} |")

    # ============================================================ Network membership
    lines.append("\n## 5. Network gravity\n")
    net_count = Counter()
    net_cross = defaultdict(set)
    for p in people:
        nets = p.get("networks") or []
        for n in nets:
            net_count[n] += 1
            for other in nets:
                if other != n:
                    net_cross[n].add(other)
    lines.append("| Network | Members | Cross-network neighbors |")
    lines.append("|---|---|---|")
    for net, n in net_count.most_common():
        cross = ", ".join(sorted(net_cross[net]))
        lines.append(f"| {net} | {n} | {cross} |")

    # ============================================================ Concentrated edges
    lines.append("\n## 6. Highest-edge institutions vs. their sector distribution\n")
    lines.append("Institutions touched by the most persons, with the sector breakdown of those persons. Institutions touched by persons across many sectors are bridge nodes.\n")
    lines.append("| Institution | Persons | Person-sector breakdown |")
    lines.append("|---|---|---|")
    for iid, deg in inst_degree.most_common(20):
        sector_dist = Counter(persons_by_id[n].get("sector") for n in adj[iid] if n in persons_by_id)
        breakdown = ", ".join(f"{s}:{c}" for s, c in sector_dist.most_common())
        inst = institutions_by_id[iid]
        lines.append(f"| `{iid}` ({inst.get('label','')}) | {deg} | {breakdown} |")

    # ============================================================ Connector personalities
    lines.append("\n## 7. Connector personalities — persons whose edges span the most distinct sectors\n")
    lines.append("People connected to institutions across many distinct sectors. Higher = bridges between worlds (the Ratchet thesis's most thesis-defining shape).\n")
    person_sector_breadth = []
    for pid, p in persons_by_id.items():
        edge_sectors = set()
        for nbr in adj[pid]:
            if nbr in institutions_by_id:
                edge_sectors.add(institutions_by_id[nbr].get("sector"))
        if edge_sectors:
            person_sector_breadth.append((pid, len(edge_sectors), sorted(edge_sectors)))
    person_sector_breadth.sort(key=lambda x: (-x[1], x[0]))
    lines.append("| Person | Sectors spanned | Sector list |")
    lines.append("|---|---|---|")
    for pid, breadth, sectors in person_sector_breadth[:25]:
        p = persons_by_id[pid]
        lines.append(f"| `{pid}` ({p.get('label','')}) | {breadth} | {', '.join(sectors)} |")

    # ============================================================ Empty / unrepresented values
    lines.append("\n## 8. Vocabulary coverage check\n")
    PLAYS = {"vault","pulpit","cycle","acquisition","pipeline","backstop","cousin","rumpelstiltskin"}
    ACTORS = {"flagging","algorithm","money","papers","embassy","eagle","tap","watchers","backdoor","model","blueprint"}
    NETWORKS = {"cfr","trilateral","bilderberg","wef","wef-ygl","pnac","atlantic","rockefeller",
                "aei","brookings","heritage","csis","rand","hoover","federalist","americanbar"}

    play_counts = Counter()
    actor_counts = Counter()
    network_counts = Counter()
    for p in people:
        for pl in p.get("plays") or []: play_counts[pl] += 1
        for ac in p.get("actors") or []: actor_counts[ac] += 1
        for nt in p.get("networks") or []: network_counts[nt] += 1

    lines.append("### Plays usage\n")
    lines.append("| Play | Count |\n|---|---|")
    for pl in sorted(PLAYS): lines.append(f"| {pl} | {play_counts.get(pl, 0)} |")
    underused_plays = [p for p in PLAYS if play_counts.get(p, 0) < 5]
    if underused_plays:
        lines.append(f"\n*Underused (<5): {', '.join(sorted(underused_plays))}*")

    lines.append("\n### Actors usage\n")
    lines.append("| Actor | Count |\n|---|---|")
    for ac in sorted(ACTORS): lines.append(f"| {ac} | {actor_counts.get(ac, 0)} |")
    underused_actors = [a for a in ACTORS if actor_counts.get(a, 0) < 5]
    if underused_actors:
        lines.append(f"\n*Underused (<5): {', '.join(sorted(underused_actors))}*")

    lines.append("\n### Networks usage\n")
    lines.append("| Network | Count |\n|---|---|")
    for nt in sorted(NETWORKS):
        c = network_counts.get(nt, 0)
        lines.append(f"| {nt} | {c} |")
    underused_networks = [n for n in NETWORKS if network_counts.get(n, 0) < 3]
    if underused_networks:
        lines.append(f"\n*Underused (<3): {', '.join(sorted(underused_networks))}*")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {OUT}")
    print(f"  {len(people)} persons, {len(institutions)} institutions, {len(edges)} edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
