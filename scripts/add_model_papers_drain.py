"""Drain underused `model` and `papers` actor tags by adding named
biometric / digital-ID deployment leaders + retagging existing records.

Per the discovered-groupings narrative: `model` (facial recognition,
biometric surveillance) is at 5 persons, `papers` (digital ID, biometric
enrollment) is at 4. Both undercount the actual cohort.

New persons (4): Hoan Ton-That + Richard Schwartz (Clearview AI),
Palmer Luckey (Anduril founder), Alex Blania (Tools for Humanity /
Worldcoin CEO).

Tag patches:
- Nilekani: add `papers` to actors (he's the Aadhaar architect; already
  documented in role text)
- Pichai: add `model` to actors (Google deploys Vision face/object
  recognition broadly)
- Karp: already has `model`; no change
- Schmidt: already has `model`; no change

New institutions (3): Clearview AI, Anduril Industries, Tools for Humanity.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name): return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}
def wd(qid): return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}
def off(url): return {"type": "official", "url": url}
def news(url): return {"type": "news", "url": url}


NEW_INSTITUTIONS = [
    {"id": "Clearview", "label": "Clearview AI", "sector": "tech",
     "sources": [w("Clearview_AI"), off("https://www.clearview.ai/")]},
    {"id": "Anduril", "label": "Anduril Industries", "sector": "def",
     "sources": [w("Anduril_Industries"), off("https://www.anduril.com/")]},
    {"id": "ToolsForHumanity", "label": "Tools for Humanity (Worldcoin)", "sector": "tech",
     "sources": [w("Worldcoin"), off("https://www.toolsforhumanity.com/")]},
]


NEW_PERSONS = [
    {"id": "TonThat", "label": "Hoan Ton-That", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["model", "papers"],
     "role": "iOS app developer (Trumpet, ViddyHo) -> Clearview AI co-founder + CEO 2017-",
     "sources": [w("Hoan_Ton-That"), wd("Q104923539"),
                 news("https://www.nytimes.com/2020/01/18/technology/clearview-privacy-facial-recognition.html")]},
    {"id": "RSchwartz", "label": "Richard Schwartz", "sector": "tech",
     "admin": ["bush1"], "networks": [],
     "plays": [], "actors": ["model"],
     "role": "Rudy Giuliani senior adviser (NYC mayoralty) -> Manhattan Institute Senior Fellow -> Smart Cards LLC -> Clearview AI co-founder 2017-",
     "sources": [w("Clearview_AI"), wd("Q104923538"),
                 news("https://www.nytimes.com/2020/01/18/technology/clearview-privacy-facial-recognition.html")]},
    {"id": "PLuckey", "label": "Palmer Luckey", "sector": "def",
     "admin": [], "networks": [],
     "plays": ["acquisition", "pipeline"], "actors": ["model", "blueprint"],
     "role": "Oculus VR founder 2012 -> sold to Facebook 2014 ($2.3B) -> departed Facebook 2017 -> Anduril Industries co-founder + Chairman 2017-",
     "sources": [w("Palmer_Luckey"), wd("Q19360027"),
                 off("https://www.anduril.com/")]},
    {"id": "Blania", "label": "Alex Blania", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["papers", "model"],
     "role": "Caltech physics PhD -> Worldcoin co-founder (with Sam Altman, Max Novendstern) 2020 -> Tools for Humanity CEO",
     "sources": [w("Worldcoin"), wd("Q108812428"),
                 off("https://www.toolsforhumanity.com/")]},
]


NEW_EDGES = [
    ("TonThat", "Clearview"),
    ("RSchwartz", "Clearview"),
    ("PLuckey", "Anduril"), ("PLuckey", "Meta"),
    ("Blania", "ToolsForHumanity"), ("Blania", "OpenAI"),  # Worldcoin/Altman link
]


# Tag patches: append to existing records' actors[] without overwriting other fields
TAG_PATCHES = {
    "Nilekani": {"add_actors": ["papers"]},
    "Pichai": {"add_actors": ["model"]},
}


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

    # Apply tag patches to existing records
    patches_applied = 0
    for p in people:
        if p["id"] in TAG_PATCHES:
            patch = TAG_PATCHES[p["id"]]
            if "add_actors" in patch:
                actors = set(p.get("actors") or [])
                new_actors = actors | set(patch["add_actors"])
                if new_actors != actors:
                    p["actors"] = sorted(new_actors)
                    patches_applied += 1

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions: f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people: f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges: f.write(json.dumps(e) + "\n")

    print(f"Added {new_i} institutions, {new_p} persons, {new_e} edges.")
    print(f"Patched {patches_applied} existing records with new tags.")
    if skipped: print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
