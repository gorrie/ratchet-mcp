"""Add the remaining Watching-the-Watchers lab/policy-wing people to the Ratchet graph.

Seven subjects carry web profiles on evilrobots.lol but were missing from people.jsonl, so
grade_person_texts could not run on them. This adds them (>=2 sources, closed-vocab tags,
positions-only role text) + the institutions and edges they need. Idempotent; defamation-disciplined
(no characterizations in role/tags).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PEOPLE = DATA / "people.jsonl"
INST = DATA / "institutions.jsonl"
EDGES = DATA / "edges.jsonl"

INSTITUTIONS = [
    {"id": "UKAISI", "label": "UK AI Security Institute", "sector": "gov",
     "sources": [{"type": "official", "url": "https://www.aisi.gov.uk/about"}], "kind": "institution"},
    {"id": "GovAI", "label": "Centre for the Governance of AI", "sector": "tank",
     "sources": [{"type": "official", "url": "https://www.governance.ai/"}], "kind": "institution"},
    {"id": "CAIS", "label": "Center for AI Safety", "sector": "tank",
     "sources": [{"type": "official", "url": "https://safe.ai/"}], "kind": "institution"},
    {"id": "Scale", "label": "Scale AI", "sector": "tech",
     "sources": [{"type": "official", "url": "https://scale.com/"}], "kind": "institution"},
    {"id": "CAISI", "label": "Center for AI Standards and Innovation (NIST)", "sector": "gov",
     "sources": [{"type": "official", "url": "https://www.nist.gov/caisi"}], "kind": "institution"},
    {"id": "NIST", "label": "National Institute of Standards and Technology", "sector": "gov",
     "sources": [{"type": "official", "url": "https://www.nist.gov/"}], "kind": "institution"},
    {"id": "Coinbase", "label": "Coinbase", "sector": "fin",
     "sources": [{"type": "official", "url": "https://www.coinbase.com/"}], "kind": "institution"},
]

PEOPLE_RECS = [
    {"id": "JClark", "label": "Jack Clark", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": ["pulpit"], "actors": [],
     "role": "Bloomberg / The Register AI journalist -> OpenAI Policy Director -> "
             "Anthropic co-founder & Head of Public Benefit; US National AI Advisory Committee",
     "sources": [
         {"type": "official", "url": "https://www.anthropic.com/news/the-anthropic-institute"},
         {"type": "gov", "url": "https://docs.house.gov/meetings/ZS/ZS00/20250625/118428/HHRG-119-ZS00-Wstate-ClarkJ-20250625.pdf"}]},
    {"id": "Jang", "label": "Joanne Jang", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Google Assistant -> OpenAI Model Behavior founder & Model Spec -> OAI Labs founder 2025",
     "sources": [
         {"type": "official", "url": "https://reservoirsamples.substack.com/p/thoughts-on-setting-policy-for-new"},
         {"type": "official", "url": "https://model-spec.openai.com/2025-12-18.html"}]},
    {"id": "JLeung", "label": "Jade Leung", "kind": "person", "sector": "multi",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Oxford GovAI Head of Research -> OpenAI Governance Lead -> UK AI Security Institute CTO; "
             "AI adviser to the British Prime Minister",
     "sources": [
         {"type": "official", "url": "https://www.governance.ai/team/jade-leung"},
         {"type": "official", "url": "https://www.aisi.gov.uk/about"}]},
    {"id": "Hendrycks", "label": "Dan Hendrycks", "kind": "person", "sector": "tank",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Center for AI Safety director -> xAI safety adviser -> Scale AI adviser",
     "sources": [
         {"type": "official", "url": "https://safe.ai/"},
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Dan_Hendrycks"}]},
    {"id": "Christiano", "label": "Paul Christiano", "kind": "person", "sector": "tank",
     "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "OpenAI RLHF co-author -> Alignment Research Center founder -> "
             "Head of AI Safety, CAISI (NIST) 2024-",
     "sources": [
         {"type": "official", "url": "https://www.nist.gov/people/paul-christiano"},
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Paul_Christiano_(researcher)"}]},
    {"id": "DWillner", "label": "Dave Willner", "kind": "person", "sector": "tech",
     "admin": [], "networks": [], "plays": [], "actors": ["flagging"],
     "role": "Facebook first content-policy rulebook -> Airbnb Head of Community Policy -> "
             "OpenAI first Head of Trust & Safety 2022-23 -> safety advisor",
     "sources": [
         {"type": "press", "url": "https://techcrunch.com/2023/07/21/openais-head-of-trust-and-safety-dave-willner-steps-down/"},
         {"type": "official", "url": "https://law.yale.edu/yls-today/yale-law-school-events/david-willner-head-community-policing-airbnb-former-head-content-policy-facebook"}]},
    {"id": "Lehane", "label": "Chris Lehane", "kind": "person", "sector": "gov",
     "admin": ["clinton"], "networks": [], "plays": ["pulpit"], "actors": ["eagle"],
     "role": "Clinton White House counsel's office -> Gore 2000 press secretary -> "
             "Airbnb Head of Global Policy 2015-22 -> OpenAI Chief Global Affairs Officer",
     "sources": [
         {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Chris_Lehane"},
         {"type": "official", "url": "https://cdn.openai.com/global-affairs/ostp-rfi/ec680b75-d539-4653-b297-8bcf6e5f7686/openai-response-ostp-nsf-rfi-notice-request-for-information-on-the-development-of-an-artificial-intelligence-ai-action-plan.pdf"}]},
]

EDGE_RECS = [
    ("JClark", "Anthropic"), ("JClark", "OpenAI"),
    ("Jang", "OpenAI"), ("Jang", "Google"),
    ("JLeung", "GovAI"), ("JLeung", "OpenAI"), ("JLeung", "UKAISI"),
    ("Hendrycks", "CAIS"), ("Hendrycks", "xAI"), ("Hendrycks", "Scale"),
    ("Christiano", "OpenAI"), ("Christiano", "ARC"), ("Christiano", "METR"),
    ("Christiano", "CAISI"), ("Christiano", "NIST"),
    ("DWillner", "Meta"), ("DWillner", "Airbnb"), ("DWillner", "OpenAI"),
    ("Lehane", "OpenAI"), ("Lehane", "Airbnb"), ("Lehane", "Coinbase"),
]


def _ids(path):
    out = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.add(json.loads(line)["id"])
    return out


def _edge_set():
    out = set()
    if EDGES.exists():
        for line in EDGES.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                e = json.loads(line)
                out.add((e["source"], e["target"]))
    return out


def main():
    have = _ids(PEOPLE) | _ids(INST)
    ai = ap = ae = 0
    with INST.open("a", encoding="utf-8") as fh:
        for rec in INSTITUTIONS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); ai += 1
    with PEOPLE.open("a", encoding="utf-8") as fh:
        for rec in PEOPLE_RECS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); ap += 1
    ee = _edge_set()
    with EDGES.open("a", encoding="utf-8") as fh:
        for s, t in EDGE_RECS:
            if (s, t) not in ee and s in have and t in have:
                fh.write(json.dumps({"source": s, "target": t}, ensure_ascii=False) + "\n")
                ee.add((s, t)); ae += 1
    print(f"Added: {ai} institutions, {ap} people, {ae} edges.")


if __name__ == "__main__":
    main()
