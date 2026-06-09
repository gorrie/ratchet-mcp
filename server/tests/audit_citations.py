"""CI audit: enforce dataset citation discipline per docs/CITATIONS.md.

Runs in GitHub Actions on every push/PR. Non-zero exit if anything fails.

Checks:
  1. Every person record has >=2 source URLs.
  2. Every institution record has >=1 source URL.
  3. No record has Wikipedia as its sole source.
  4. Source ``type`` values are from the accepted vocabulary.
  5. Source URLs are well-formed.
  6. Defamation lint — forbidden patterns in ``role`` text:
       - Adjectival characterizations ("controversial," "hawkish,"
         "neoliberal," "shady," "infamous")
       - Unsourced allegation language ("alleged," "rumored,"
         "reportedly")
       - Family / health / financial-trouble references in role text
  7. ID uniqueness across people + institutions.
  8. Tag values from the closed vocabularies (plays, actors, sectors).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

DATA = Path(os.environ.get("RATCHET_DATA_DIR") or Path(__file__).resolve().parents[2] / "server" / "data")

ACCEPTED_SOURCE_TYPES = {
    "littlesis", "wikipedia", "wikidata", "official", "gov-record",
    "wayback", "academic", "news",
}

# Closed vocabularies — see docs/PLAYS.md, docs/ACTORS.md.
PLAYS = {
    "vault", "pulpit", "cycle", "acquisition", "pipeline", "backstop",
    "cousin", "rumpelstiltskin",
}
ACTORS = {
    "flagging", "algorithm", "money", "papers", "embassy", "eagle",
    "tap", "watchers", "backdoor", "model", "blueprint",
    # Added 2026-05-29 via research-driven cluster expansion:
    "priest",    # Click #7 — ESG/DEI/Net-Zero compliance as control mechanism
    "hospital",  # Click #13 — health surveillance + governance architecture
}
SECTORS = {
    "gov", "fin", "imf", "cfr", "tank", "intel", "def", "tech",
    "multi", "judiciary",
    # Foreign-state institutional cluster (institutional-only — no named
    # persons; influence shown via documented engagement edges from the
    # primary cohort). See docs/SCOPE.md Cohort F.
    "china-state", "russia-state",
    # Added 2026-05-29 via diaspora-pacs cluster expansion.
    # Country-of-origin diaspora-political-action committees and
    # advocacy orgs operating in US politics. Mix of Embassy-aligned
    # (foreign-state-adjacent positioning) and reverse-aligned
    # (counter-home-state positioning).
    "diaspora",
    # Added 2026-06-04 via the historical-ideologues layer (add_v4_ideologues).
    # Intellectual ANTECEDENTS of the control grid (Galton, the Fabians,
    # Rhodes/Milner, Quigley, Mises/Hayek, LaRouche) and the movement
    # institutions they founded. Exempt from the 2-sector revolving-door
    # predicate; admitted on documented founding/authorship roles with the
    # same >=2-source + defamation discipline. See docs/SCOPE.md ->
    # "Historical-ideologues layer". No plays/actors tags on these persons.
    "historical",
}
NETWORKS = {
    "cfr", "trilateral", "bilderberg", "wef", "wef-ygl", "pnac",
    "atlantic", "rockefeller",
    # Think-tank affiliations tracked as networks
    "aei", "brookings", "heritage", "csis", "rand", "hoover",
    # Legal-network affiliations
    "federalist", "americanbar",
}
ADMINS = {
    "roosevelt", "truman", "eisenhower", "kennedy", "lbj", "nixon",
    "ford", "carter", "reagan", "bush1", "clinton", "bush2", "obama",
    "trump1", "biden", "trump2",
}

DEFAMATION_ADJECTIVES = re.compile(
    r"\b(controversial|hawkish|neoliberal|shady|infamous|corrupt|disgraced|"
    r"discredited|notorious|crooked|sleazy|odious)\b",
    re.IGNORECASE,
)
UNSOURCED_ALLEGATION = re.compile(
    r"\b(rumored to|allegedly|reportedly|purportedly|supposedly)\b",
    re.IGNORECASE,
)
PRIVATE_LIFE = re.compile(
    r"\b(divorced|widowed|estranged|mistress|affair with|battling cancer|"
    r"bankruptcy|gambling debts|alcoholic)\b",
    re.IGNORECASE,
)


def read_jsonl(path: Path) -> list[dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path.name}:{i} invalid JSON: {e}")
    return out


def main() -> int:
    fails: list[str] = []
    people = read_jsonl(DATA / "people.jsonl")
    institutions = read_jsonl(DATA / "institutions.jsonl")
    edges = read_jsonl(DATA / "edges.jsonl")

    # 1. Source count + 2. Institution count
    for p in people:
        srcs = p.get("sources", []) or []
        if len(srcs) < 2:
            fails.append(f"person {p['id']!r} has {len(srcs)} sources (need >=2)")
    for inst in institutions:
        srcs = inst.get("sources", []) or []
        if len(srcs) < 1:
            fails.append(f"institution {inst['id']!r} has 0 sources (need >=1)")

    # 3. Wikipedia-only
    for p in people:
        srcs = p.get("sources", []) or []
        types = {s.get("type") for s in srcs if isinstance(s, dict)}
        if types and types <= {"wikipedia"}:
            fails.append(f"person {p['id']!r} has only Wikipedia sources")

    # 4. Source type vocabulary + 5. URL well-formedness
    for rec in people + institutions:
        for src in rec.get("sources", []) or []:
            if not isinstance(src, dict):
                fails.append(f"{rec['id']!r} has non-dict source: {src!r}")
                continue
            t = src.get("type")
            if t not in ACCEPTED_SOURCE_TYPES:
                fails.append(f"{rec['id']!r} unknown source type {t!r}")
            url = src.get("url", "")
            if not url:
                fails.append(f"{rec['id']!r} source missing url")
                continue
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                fails.append(f"{rec['id']!r} malformed url: {url!r}")

    # 6. Defamation lint
    for p in people:
        role = p.get("role", "") or ""
        for pat, label in (
            (DEFAMATION_ADJECTIVES, "characterization"),
            (UNSOURCED_ALLEGATION, "unsourced allegation"),
            (PRIVATE_LIFE, "private-life detail"),
        ):
            m = pat.search(role)
            if m:
                fails.append(f"person {p['id']!r} role contains {label} ({m.group(0)!r})")

    # 7. ID uniqueness across both tables
    seen: dict[str, str] = {}
    for kind, rows in (("person", people), ("institution", institutions)):
        for r in rows:
            if r["id"] in seen:
                fails.append(f"duplicate id {r['id']!r} ({seen[r['id']]} and {kind})")
            else:
                seen[r["id"]] = kind

    # 8. Closed-vocabulary tag values
    def _check_set(rec, field, accepted, label):
        for v in rec.get(field, []) or []:
            if v not in accepted:
                fails.append(f"person {rec['id']!r} has unknown {label} tag {v!r}")

    for p in people:
        _check_set(p, "plays", PLAYS, "play")
        _check_set(p, "actors", ACTORS, "actor")
        _check_set(p, "networks", NETWORKS, "network")
        _check_set(p, "admin", ADMINS, "admin")
        sector = p.get("sector")
        if sector and sector not in SECTORS:
            fails.append(f"person {p['id']!r} has unknown sector {sector!r}")
    for inst in institutions:
        sector = inst.get("sector")
        if sector and sector not in SECTORS:
            fails.append(f"institution {inst['id']!r} has unknown sector {sector!r}")

    # Edges reference real nodes
    all_ids = {p["id"] for p in people} | {i["id"] for i in institutions}
    for e in edges:
        if isinstance(e, list):
            src, tgt = e[0], e[1]
        else:
            src, tgt = e.get("source"), e.get("target")
        if src not in all_ids:
            fails.append(f"edge source not in dataset: {src!r}")
        if tgt not in all_ids:
            fails.append(f"edge target not in dataset: {tgt!r}")

    print(f"Audited {len(people)} people, {len(institutions)} institutions, {len(edges)} edges.")
    if fails:
        # Summarize by first-word category, then list each.
        from collections import Counter
        cats = Counter(f.split(" has ")[0].split(" ", 1)[0] for f in fails)
        print(f"\n{len(fails)} FAILURE(S). Top categories:")
        for cat, n in cats.most_common(10):
            print(f"  {n:>4}  {cat}")
        print()
        for f in fails:
            try:
                print(f"  - {f}")
            except UnicodeEncodeError:
                print(f"  - {f.encode('ascii', 'replace').decode('ascii')}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
