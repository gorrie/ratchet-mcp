"""Add the second evaluator batch (October 2026) to the Ratchet graph: Scale AI's government-evaluator
and Meta edges, Transluce, FAR.AI, Andon Labs, and the people who run or govern them.

inventory-checked: add_wtw_evaluators_2026_10.py -- same idempotent append pattern; that batch added Trail of
Bits, Irregular, Redwood, Epoch, Palisade, SecureBio and Mechanize; this one adds the evaluators it did not
(Transluce, FAR.AI, Andon Labs, Sequent Research), Alexandr Wang, Geoffrey Irving, Adam Gleave and Jacob
Steinhardt, and the Scale / Meta / CAISI edges.

Every record carries the fetched source behind it; role text is positions only (defamation discipline,
docs/CITATIONS.md). Edges to an id that does not exist are skipped, never invented. Idempotent.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PEOPLE = DATA / "people.jsonl"
INST = DATA / "institutions.jsonl"
EDGES = DATA / "edges.jsonl"

SCALE_META = "https://scale.com/blog/scale-ai-announces-next-phase-of-company-evolution"
SCALE_AISI = "https://scale.com/blog/first-independent-model-evaluator-for-the-USAISI"
MSL_MEMO = "https://www.nbcnewyork.com/news/business/money-report/mark-zuckerberg-announces-creation-of-meta-superintelligence-labs-read-the-memo/6320911/"
AP_META = "https://www.news4jax.com/business/2025/06/13/meta-invests-in-ai-firm-scale-and-recruits-its-ceo-for-superintelligence-team/"
HLE = "https://arxiv.org/abs/2501.14249"
IRVING_SEQ = "https://x.com/geoffreyirving/status/2064733320827568231"
IRVING_AISI = "https://www.aisi.gov.uk/blog/why-i-joined-aisi---geoffrey-irving"
METR_ABOUT = "https://metr.org/about"


def _o(url):
    return {"type": "official", "url": url}


def _p(url):
    return {"type": "press", "url": url}


def _paper(url):
    return {"type": "paper", "url": url}


INSTITUTIONS = [
    {"id": "Transluce", "label": "Transluce", "sector": "tank", "kind": "institution",
     "sources": [_o("https://transluce.org/about"), _o("https://transluce.org/investigating-o3-truthfulness")],
     "brief": "Nonprofit AI oversight lab; pre-release o3 audit (Apr 2025) found the model fabricated actions it took."},
    {"id": "FARAI", "label": "FAR.AI", "sector": "tank", "kind": "institution",
     "sources": [_o("https://www.far.ai/about"), _paper("https://proceedings.mlr.press/v202/wang23g.html")],
     "brief": "AI security research nonprofit; pre-deployment testing for frontier developers; runs the Alignment Workshop series."},
    {"id": "AndonLabs", "label": "Andon Labs", "sector": "tech", "kind": "institution",
     "sources": [_o("https://andonlabs.com/"), _o("https://www.anthropic.com/research/project-vend-1")],
     "brief": "AI safety evaluation company (Y Combinator); Vending-Bench; ran Anthropic's Project Vend; runs AI-operated businesses."},
    {"id": "SequentResearch", "label": "Sequent Research", "sector": "tank", "kind": "institution",
     "sources": [_o(IRVING_SEQ), _o("https://x.com/geoffreyirving/status/2055241785564176552")],
     "brief": "Nonprofit alignment organization founded June 2026 by Geoffrey Irving with researchers from UK AISI's Alignment Team and Timaeus."},
]

PEOPLE_RECS = [
    {"id": "AWang", "label": "Alexandr Wang", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Scale AI founder & CEO -> Meta Chief AI Officer, Meta Superintelligence Labs (June 2025); Scale director",
     "sources": [_o(SCALE_META), _p(MSL_MEMO)]},
    {"id": "GIrving", "label": "Geoffrey Irving", "kind": "person", "sector": "multi", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "OpenAI Reflection Team lead -> DeepMind Scalable Alignment lead -> UK AISI Research Director / Chief Scientist (2024-26) -> Sequent Research co-founder (2026)",
     "sources": [_o(IRVING_AISI), _o(IRVING_SEQ)]},
    {"id": "AGleave", "label": "Adam Gleave", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "FAR.AI co-founder & CEO; METR advisor and board member; formerly Google DeepMind",
     "sources": [_o("https://www.gleave.me/"), _o(METR_ABOUT)]},
    {"id": "JSteinhardt", "label": "Jacob Steinhardt", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "UC Berkeley Associate Professor; Transluce co-founder & CEO; post-doc year at OpenAI and Open Philanthropy",
     "sources": [_o("https://jsteinhardt.stat.berkeley.edu/"), _o("https://transluce.org/about")]},
]

# (source, target, rel or None, sources or None)
EDGE_RECS = [
    ("AWang", "Scale", "founded", None),
    ("AWang", "Meta", "employed-by", [_p(MSL_MEMO)]),
    ("Scale", "Meta", "funded-by", [_o(SCALE_META), _p(AP_META)]),
    ("Scale", "CAISI", "evaluator-for", [_o(SCALE_AISI)]),
    ("Scale", "CAIS", "co-author", [_paper(HLE)]),
    ("GIrving", "UKAISI", "employed-by", [_o(IRVING_AISI)]),
    ("GIrving", "OpenAI", "employed-by", [_o(IRVING_AISI)]),
    ("GIrving", "DeepMind", "employed-by", [_o(IRVING_AISI)]),
    ("GIrving", "SequentResearch", "founded", [_o(IRVING_SEQ)]),
    ("AGleave", "FARAI", "founded", None),
    ("AGleave", "METR", "member-of", [_o(METR_ABOUT)]),
    ("AGleave", "DeepMind", "employed-by", [_o("https://www.gleave.me/")]),
    ("JSteinhardt", "Transluce", "founded", None),
    ("JSteinhardt", "OpenAI", "employed-by", [_o("https://jsteinhardt.stat.berkeley.edu/")]),
    ("JSteinhardt", "OpenPhil", "employed-by", [_o("https://jsteinhardt.stat.berkeley.edu/")]),
    ("Transluce", "OpenAI", "evaluator-for", [_o("https://transluce.org/investigating-o3-truthfulness")]),
    ("AndonLabs", "Anthropic", "evaluator-for", [_o("https://www.anthropic.com/research/project-vend-1")]),
    ("Shlegeris", "Anthropic", "co-author", [_paper("https://arxiv.org/abs/2412.14093")]),
    ("MFredrikson", "Kolter", "co-author", [_paper("https://arxiv.org/abs/2307.15043")]),
]


def _ids(path):
    out = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.add(json.loads(line)["id"])
    return out


def _edge_set():
    out = set()
    if EDGES.exists():
        for line in EDGES.read_text(encoding="utf-8").splitlines():
            if line.strip():
                e = json.loads(line)
                out.add((e["source"], e["target"]))
    return out


def main():
    have = _ids(PEOPLE) | _ids(INST)
    added_i = added_p = added_e = 0
    skipped = []
    with INST.open("a", encoding="utf-8", newline="\n") as fh:
        for rec in INSTITUTIONS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); added_i += 1
    with PEOPLE.open("a", encoding="utf-8", newline="\n") as fh:
        for rec in PEOPLE_RECS:
            if rec["id"] not in have:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); have.add(rec["id"]); added_p += 1
    existing = _edge_set()
    with EDGES.open("a", encoding="utf-8", newline="\n") as fh:
        for s, t, rel, src in EDGE_RECS:
            if (s, t) in existing:
                continue
            if s not in have or t not in have:
                skipped.append((s, t)); continue
            e = {"source": s, "target": t}
            if rel:
                e["rel"] = rel
            if src:
                e["sources"] = src
            fh.write(json.dumps(e, ensure_ascii=False) + "\n"); existing.add((s, t)); added_e += 1
    print(f"Added: {added_i} institutions, {added_p} people, {added_e} edges.")
    if skipped:
        print("Skipped (unknown id):", skipped)


if __name__ == "__main__":
    main()
