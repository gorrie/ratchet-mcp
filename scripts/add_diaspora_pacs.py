"""Add the diaspora-pacs cluster + its first 18 institutions, 5 named persons,
and 5 edges to the Ratchet MCP dataset.

One-shot bootstrap script for the cluster expansion documented in
`evil-robots-series/research/research-diaspora-pacs.md`. Idempotent: skips
records whose ID already exists in the target file.

Run from anywhere; uses absolute paths.
"""
from __future__ import annotations

import json
from pathlib import Path

# Portable: resolve relative to the repo, matching the other add_*.py scripts.
# RATCHET_DATA_DIR overrides (same env var the server's data.py honors).
import os
ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ["RATCHET_DATA_DIR"]) if os.environ.get("RATCHET_DATA_DIR") else ROOT / "server" / "data"

INSTITUTIONS = [
    {
        "id": "USINPAC",
        "label": "USINPAC",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.usinpac.com/"},
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00381699/"},
        ],
        "kind": "institution",
    },
    {
        "id": "OFBJP-USA",
        "label": "Overseas Friends of BJP-USA",
        "sector": "diaspora",
        "sources": [
            {"type": "news", "url": "https://theprint.in/world/overseas-friends-of-bjp-registers-under-us-foreign-agents-registration-act/500190/"},
            {"type": "news", "url": "https://scroll.in/global/973063/explainer-why-the-overseas-friends-of-bjp-has-registered-as-a-foreign-agent-in-the-us"},
        ],
        "kind": "institution",
    },
    {
        "id": "Impact-PAC",
        "label": "Indian American Impact",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://iaimpact.org/about/history/"},
        ],
        "kind": "institution",
    },
    {
        "id": "RHC",
        "label": "Republican Hindu Coalition",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://rhc-usa.org/"},
            {"type": "news", "url": "https://thehill.com/homenews/campaign/288377-hindu-american-emerges-as-trump-mega-donor/"},
        ],
        "kind": "institution",
    },
    {
        "id": "HAF",
        "label": "Hindu American Foundation",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.hinduamerican.org/our-team"},
        ],
        "kind": "institution",
    },
    {
        "id": "PAK-PAC",
        "label": "Pakistani American PAC",
        "sector": "diaspora",
        "sources": [
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00238204/"},
            {"type": "official", "url": "https://www.pakpacusa.org/about/"},
        ],
        "kind": "institution",
    },
    {
        "id": "BAPAC",
        "label": "Bangladeshi American PAC",
        "sector": "diaspora",
        "sources": [
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00400440/"},
            {"type": "official", "url": "http://www.bapac-usa.org/about.html"},
        ],
        "kind": "institution",
    },
    {
        "id": "ANCA",
        "label": "Armenian National Committee of America",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://anca.org/about-anca/"},
        ],
        "kind": "institution",
    },
    {
        "id": "AAA-Armenia",
        "label": "Armenian Assembly of America",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.armenian-assembly.org/about-us"},
        ],
        "kind": "institution",
    },
    {
        "id": "FAPA",
        "label": "Formosan Association for Public Affairs",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://fapa.org/about-us/"},
        ],
        "kind": "institution",
    },
    {
        "id": "Committee100",
        "label": "Committee of 100",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.committee100.org/about-us/"},
        ],
        "kind": "institution",
    },
    {
        "id": "CANF",
        "label": "Cuban American National Foundation",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://canf.org/"},
            {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Cuban_American_National_Foundation"},
        ],
        "kind": "institution",
    },
    {
        "id": "USCDP",
        "label": "US-Cuba Democracy PAC",
        "sector": "diaspora",
        "sources": [
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00387720/"},
            {"type": "official", "url": "https://www.opensecrets.org/political-action-committees-pacs/us-cuba-democracy-pac/C00387720/summary/2022"},
        ],
        "kind": "institution",
    },
    {
        "id": "ATFL",
        "label": "American Task Force on Lebanon",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://atfl.org/"},
        ],
        "kind": "institution",
    },
    {
        "id": "NaFFAA",
        "label": "National Federation of Filipino American Associations",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://naffaa.org/about/"},
        ],
        "kind": "institution",
    },
    {
        "id": "CARECEN",
        "label": "Central American Resource Center",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.carecen-la.org/history"},
        ],
        "kind": "institution",
    },
    {
        "id": "BPSOS",
        "label": "Boat People SOS",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://www.bpsos.org/"},
        ],
        "kind": "institution",
    },
    {
        "id": "KAGC",
        "label": "Korean American Grassroots Conference",
        "sector": "diaspora",
        "sources": [
            {"type": "official", "url": "https://kagc.us/about/"},
        ],
        "kind": "institution",
    },
]

PEOPLE = [
    {
        "id": "Puri-Sanjay",
        "label": "Sanjay Puri",
        "sector": "diaspora",
        "admin": [],
        "networks": [],
        "plays": [],
        "actors": ["embassy"],
        "sources": [
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00381699/"},
            {"type": "official", "url": "https://www.usinpac.com/"},
        ],
        "role": "USINPAC founder + chairman from 2002; treasurer per recent FEC filings",
        "kind": "person",
    },
    {
        "id": "Makhija-Neil",
        "label": "Neil Makhija",
        "sector": "diaspora",
        "admin": [],
        "networks": [],
        "plays": [],
        "actors": ["embassy"],
        "sources": [
            {"type": "official", "url": "https://iaimpact.org/team/neil-makhija/"},
            {"type": "academic", "url": "https://www.law.upenn.edu/cf/faculty/nmakhija/"},
        ],
        "role": "Indian American Impact Executive Director; lecturer, Penn Carey Law",
        "kind": "person",
    },
    {
        "id": "Kumar-Shalabh",
        "label": "Shalabh Kumar",
        "sector": "diaspora",
        "admin": ["trump1"],
        "networks": [],
        "plays": [],
        "actors": ["embassy"],
        "sources": [
            {"type": "official", "url": "https://rhc-usa.org/"},
            {"type": "news", "url": "https://thehill.com/homenews/campaign/288377-hindu-american-emerges-as-trump-mega-donor/"},
        ],
        "role": "RHC founder 2015; AVG Advanced Technologies founder; Trump 2016 major donor",
        "kind": "person",
    },
    {
        "id": "Claver-Carone",
        "label": "Mauricio Claver-Carone",
        "sector": "diaspora",
        "admin": ["trump1", "trump2"],
        "networks": [],
        "plays": [],
        "actors": ["embassy", "money"],
        "sources": [
            {"type": "gov-record", "url": "https://www.fec.gov/data/committee/C00387720/"},
            {"type": "gov-record", "url": "https://www.iadb.org/en/about-us/governance/president"},
        ],
        "role": "US-Cuba Democracy PAC founder 2003; NSC Senior Director Western Hemisphere 2017-2019; IDB President 2020-2022",
        "kind": "person",
    },
    {
        "id": "Gabriel-Edward",
        "label": "Edward M. Gabriel",
        "sector": "diaspora",
        "admin": ["clinton"],
        "networks": [],
        "plays": [],
        "actors": ["embassy"],
        "sources": [
            {"type": "official", "url": "https://atfl.org/the-hon-edward-m-gabriel/"},
            {"type": "gov-record", "url": "https://history.state.gov/departmenthistory/people/gabriel-edward-m"},
        ],
        "role": "US Ambassador to Morocco 1997-2001; ATFL President/CEO",
        "kind": "person",
    },
]

EDGES = [
    {"source": "Puri-Sanjay", "target": "USINPAC"},
    {"source": "Makhija-Neil", "target": "Impact-PAC"},
    {"source": "Kumar-Shalabh", "target": "RHC"},
    {"source": "Claver-Carone", "target": "USCDP"},
    {"source": "Gabriel-Edward", "target": "ATFL"},
]


def existing_ids(path: Path, key: str) -> set[str]:
    if not path.exists():
        return set()
    return {json.loads(line)[key] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def append_jsonl(path: Path, records: list[dict], key: str, kind_label: str) -> int:
    have = existing_ids(path, key)
    added = 0
    with path.open("a", encoding="utf-8", newline="") as f:
        for rec in records:
            if rec[key] in have:
                print(f"  skip {kind_label} {rec[key]!r} (already present)")
                continue
            f.write(json.dumps(rec, ensure_ascii=False) + "\r\n")
            added += 1
            print(f"  add  {kind_label} {rec[key]!r}")
    return added


def existing_edges(path: Path) -> set[tuple[str, str]]:
    return {(e["source"], e["target"]) for e in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())}


def append_edges(path: Path, edges: list[dict]) -> int:
    have = existing_edges(path)
    added = 0
    with path.open("a", encoding="utf-8", newline="") as f:
        for e in edges:
            key = (e["source"], e["target"])
            if key in have:
                print(f"  skip edge {key} (already present)")
                continue
            f.write(json.dumps(e, ensure_ascii=False) + "\r\n")
            added += 1
            print(f"  add  edge {key}")
    return added


def add_cluster(path: Path) -> bool:
    blob = json.loads(path.read_text(encoding="utf-8"))
    have = {c["id"] for c in blob["clusters"]}
    if "diaspora-pacs" in have:
        print("  skip cluster 'diaspora-pacs' (already present)")
        return False
    cluster = {
        "id": "diaspora-pacs",
        "label": "Diaspora PACs",
        "summary": (
            "Horizontal cluster: country-of-origin diaspora political-action committees "
            "and advocacy orgs operating in US politics. Template-replication pattern: "
            "USINPAC's founders explicitly modeled it on AIPAC; subsequent formations "
            "across multiple country-of-origin communities followed similar templates "
            "(501(c)(3) education arm + 501(c)(4) lobbying arm + FEC PAC + congressional "
            "caucus liaison). Includes both embassy-aligned vehicles (USINPAC, OFBJP-USA, "
            "Impact-PAC, RHC, HAF, PAK-PAC, BAPAC, ANCA, AAA, ATFL, NaFFAA, CARECEN, KAGC) "
            "and reverse-aligned counter-home-state vehicles (US-Cuba Democracy PAC, CANF, "
            "FAPA, BPSOS). OFBJP-USA is the single documented FARA-registered foreign-agent "
            "presence (Aug 2020). Eritrea is an edge case that bypasses the PAC pattern "
            "entirely via embassy 2% Recovery Tax collection."
        ),
        "query": {
            "tool": "query_cohort",
            "args": {"sector": "diaspora"},
            "filter_ids_via_institutions": [
                "USINPAC", "OFBJP-USA", "Impact-PAC", "RHC", "HAF",
                "PAK-PAC", "BAPAC", "ANCA", "AAA-Armenia", "FAPA",
                "Committee100", "CANF", "USCDP", "ATFL", "NaFFAA",
                "CARECEN", "BPSOS", "KAGC",
            ],
        },
        "ratchet_clicks": [8],
        "book_chapter": "the-ratchet:08-the-embassy",
    }
    blob["clusters"].append(cluster)
    path.write_text(json.dumps(blob, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  add  cluster 'diaspora-pacs'")
    return True


def main() -> None:
    print("Institutions:")
    n_inst = append_jsonl(DATA / "institutions.jsonl", INSTITUTIONS, "id", "institution")
    print("People:")
    n_ppl = append_jsonl(DATA / "people.jsonl", PEOPLE, "id", "person")
    print("Edges:")
    n_edge = append_edges(DATA / "edges.jsonl", EDGES)
    print("Cluster:")
    add_cluster(DATA / "clusters.json")
    print(f"\nDone. +{n_inst} institutions, +{n_ppl} people, +{n_edge} edges.")


if __name__ == "__main__":
    main()
