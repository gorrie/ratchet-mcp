"""Sharpening pass: add persons surfaced by the 4 T&S research agents.

Discord T&S leadership (2): Redgrave (Sentropy founder -> Discord VP T&S
2021-, per Semafor + Discord blog), Badalich (Columbia HRTech ->
Breakthrough -> Twitter Sr Product Trust -> Discord Senior Director
Policy -- the academic-NGO-to-platform pipeline exemplar).

Internews institutional anchor (1): DHoffman (David M. Hoffman,
Internews founder 1982) -- documents the institutional through-line
that the agent finding established (Internews's pre-2014 media-
development mission absorbed post-2016 counter-disinfo funding without
abandoning its prior portfolio).

Plus institution: Discord (long overdue -- already cited via T&S
persons but not in graph).
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
def acad(url): return {"type": "academic", "url": url}


NEW_INSTITUTIONS = [
    {"id": "Discord", "label": "Discord Inc.", "sector": "tech",
     "sources": [w("Discord"), off("https://discord.com/company")]},
]


NEW_PERSONS = [
    {"id": "Redgrave", "label": "John Redgrave", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["acquisition"], "actors": ["flagging"],
     "role": "Sentropy founder (harassment-detection ML startup) -> Sentropy acquired by Discord 2021 -> Discord Vice President of Trust and Safety 2021-",
     "sources": [w("Discord"), wd("Q119027021"),
                 news("https://www.semafor.com/article/10/27/2023/how-advances-in-ai-can-make-content-moderation-harder-and-easier")]},
    {"id": "Badalich", "label": "Savannah Badalich", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "Columbia University Human Rights and Technology MA -> Breakthrough US program manager (gender-based-violence prevention) -> Twitter Senior Product Trust Partner -> Discord Senior Director Policy 2021-",
     "sources": [w("Discord"), wd("Q119027022"),
                 off("https://fosi.org/people/savannah-badalich/")]},
    {"id": "DHoffman", "label": "David M. Hoffman", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Internews Network co-founder 1982 -> Internews President for 30+ years (oversaw 1982-2013 media-development era including AMDEP Afghanistan, Local Voices Kenya/Nigeria, Earth Journalism Network)",
     "sources": [w("David_M._Hoffman"), wd("Q103997830"),
                 off("https://internews.org/about/our-history/")]},
]


NEW_EDGES = [
    ("Redgrave", "Discord"),
    ("Badalich", "Discord"), ("Badalich", "X_Corp"),
    ("DHoffman", "Internews"),
]


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

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions: f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people: f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges: f.write(json.dumps(e) + "\n")

    print(f"Added {new_i} institutions, {new_p} persons, {new_e} edges.")
    if skipped: print(f"Skipped edges: {skipped}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
