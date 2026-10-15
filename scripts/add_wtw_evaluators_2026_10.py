"""Add the AI-evaluator layer (October 2026) to the Ratchet graph: the contract evaluators the labs
name, the people who run them, and the funder/lab/board edges between them.

inventory-checked: add_wtw_eval_statecraft_wing.py -- same idempotent append pattern; that batch added METR, Gray Swan and
their founders; this one adds the evaluators it did not (Trail of Bits, Irregular, Redwood, Epoch, Palisade, SecureBio,
Mechanize) and their leaders, with typed edges and per-edge sources where the relation needs one.

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

METR_HF = "https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/"


def _o(url):
    return {"type": "official", "url": url}


def _p(url):
    return {"type": "press", "url": url}


INSTITUTIONS = [
    {"id": "TrailOfBits", "label": "Trail of Bits", "sector": "tech", "kind": "institution",
     "sources": [_o("https://trailofbits.com/about/")],
     "brief": "Security research firm founded 2012; lists AI/ML evaluation among its practice areas; in preliminary acquisition talks with OpenAI per The Information, Oct 13 2026."},
    {"id": "Irregular", "label": "Irregular (formerly Pattern Labs)", "sector": "tech", "kind": "institution",
     "sources": [_p("https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models/"),
                 _o("https://www.irregular.com/research/addressing-recent-incidents-ongoing-findings-and-path-forward")],
     "brief": "Frontier-AI security evaluation lab, Tel Aviv; its ranges were the setting of 2026 evaluation-escape incidents disclosed by Anthropic and Google."},
    {"id": "RedwoodResearch", "label": "Redwood Research", "sector": "tank", "kind": "institution",
     "sources": [_o("https://www.redwoodresearch.org/"), _o("https://www.redwoodresearch.org/team")],
     "brief": "AI safety and security nonprofit; originated 'AI control'; co-investigated the OpenAI / Hugging Face incident with METR."},
    {"id": "EpochAI", "label": "Epoch AI", "sector": "tank", "kind": "institution",
     "sources": [_o("https://epoch.ai/about/team"),
                 _p("https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/")],
     "brief": "AI trends and benchmarking nonprofit; FrontierMath benchmark, funded by OpenAI (disclosed Dec 20 2024)."},
    {"id": "PalisadeResearch", "label": "Palisade Research", "sector": "tank", "kind": "institution",
     "sources": [_o("https://palisaderesearch.org/about/")],
     "brief": "AI capabilities and risk nonprofit; shutdown-resistance and specification-gaming demonstrations."},
    {"id": "SecureBio", "label": "SecureBio", "sector": "tank", "kind": "institution",
     "sources": [_o("https://securebio.org/")],
     "brief": "Pandemic-security nonprofit; Virology Capabilities Test; member of the NIST US AI Safety Consortium."},
    {"id": "Mechanize", "label": "Mechanize", "sector": "tech", "kind": "institution",
     "sources": [_o("https://www.mechanize.work/"), _o("https://x.com/tamaybes/status/1912905467376124240")],
     "brief": "Company founded April 2025 by Epoch AI alumni to build work environments, benchmarks and training data for automating work."},
]

PEOPLE_RECS = [
    {"id": "DGuido", "label": "Dan Guido", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Trail of Bits co-founder & CEO",
     "sources": [_o("https://trailofbits.com/about/"),
                 _p("https://www.pymnts.com/cybersecurity/2026/openai-weighs-deal-one-time-security-partner-trail-of-bits/")]},
    {"id": "DLahav", "label": "Dan Lahav", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Irregular (formerly Pattern Labs) co-founder",
     "sources": [_p("https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models/"),
                 _p("https://en.globes.co.il/en/article-israeli-ai-security-lab-irregular-raises-80m-1001522079")]},
    {"id": "ONevo", "label": "Omer Nevo", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Irregular (formerly Pattern Labs) co-founder",
     "sources": [_p("https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models/"),
                 _p("https://en.globes.co.il/en/article-israeli-ai-security-lab-irregular-raises-80m-1001522079")]},
    {"id": "Shlegeris", "label": "Buck Shlegeris", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Redwood Research CEO and board member",
     "sources": [_o("https://www.redwoodresearch.org/team"), _o("https://www.alignmentforum.org/users/buck")]},
    {"id": "RGreenblatt", "label": "Ryan Greenblatt", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Redwood Research Chief Scientist; lead author, Alignment Faking in LLMs (with Anthropic, 2024); METR contractor on the 2026 Hugging Face investigation -> joined METR Sept 2026",
     "sources": [_o("https://www.redwoodresearch.org/"), {"type": "paper", "url": "https://arxiv.org/abs/2412.14093"}, _o(METR_HF),
                 _o("https://x.com/RyanGreenblatt/status/2104268596553957477")]},
    {"id": "ACotra", "label": "Ajeya Cotra", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Coefficient Giving (Open Philanthropy), led technical AI safety program 2024 -> METR Technical Staff; Epoch AI board",
     "sources": [_o("https://metr.org/team/ajeya-cotra/"), _o("https://epoch.ai/about/team")]},
    {"id": "Besiroglu", "label": "Tamay Besiroglu", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Epoch AI co-founder & associate director -> Mechanize co-founder 2025-",
     "sources": [_p("https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/"),
                 _o("https://x.com/tamaybes/status/1912905467376124240")]},
    {"id": "JSevilla", "label": "Jaime Sevilla", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Epoch AI CEO and board member",
     "sources": [_o("https://epoch.ai/about/team"), {"type": "paper", "url": "https://arxiv.org/abs/2202.05924"}]},
    {"id": "Ladish", "label": "Jeffrey Ladish", "kind": "person", "sector": "tank", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Anthropic information security program -> Palisade Research Executive Director; adviser to the White House, DoD and congressional offices",
     "sources": [_o("https://palisaderesearch.org/about/"), {"type": "paper", "url": "https://arxiv.org/abs/2509.14260"}]},
    {"id": "MFredrikson", "label": "Matt Fredrikson", "kind": "person", "sector": "tech", "admin": [], "networks": [], "plays": [], "actors": ["model"],
     "role": "Gray Swan AI co-founder & CEO",
     "sources": [_o("https://www.grayswan.ai/about"), _o("https://csd.cmu.edu/people/faculty/matt-fredrikson")]},
]

# (source, target, rel or None, sources or None)
EDGE_RECS = [
    ("DGuido", "TrailOfBits", "founded", None),
    ("TrailOfBits", "OpenAI", "acquisition-talks", [_p("https://www.pymnts.com/cybersecurity/2026/openai-weighs-deal-one-time-security-partner-trail-of-bits/")]),
    ("DLahav", "Irregular", "founded", None), ("ONevo", "Irregular", "founded", None),
    ("Irregular", "Sequoia", "funded-by", [_p("https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models/")]),
    ("Irregular", "Anthropic", "evaluator-for", [_o("https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents")]),
    ("Irregular", "Google", "evaluator-for", [_p("https://www.foxbusiness.com/technology/google-gemini-accessed-3-companies-systems-during-ai-cybersecurity-test")]),
    ("Shlegeris", "RedwoodResearch", "employed-by", None),
    ("RGreenblatt", "RedwoodResearch", "employed-by", None),
    ("RGreenblatt", "METR", "employed-by", [_o(METR_HF), _o("https://x.com/RyanGreenblatt/status/2104268596553957477")]),
    ("RGreenblatt", "Anthropic", "co-author", [{"type": "paper", "url": "https://arxiv.org/abs/2412.14093"}]),
    ("RGreenblatt", "BBarnes", "disclosed-relationship", [_o(METR_HF)]),
    ("RedwoodResearch", "UKAISI", "advisory", [_o("https://www.redwoodresearch.org/")]),
    ("RedwoodResearch", "Anthropic", "advisory", [_o("https://www.redwoodresearch.org/")]),
    ("RedwoodResearch", "DeepMind", "advisory", [_o("https://www.redwoodresearch.org/")]),
    ("RedwoodResearch", "METR", "joint-investigation", [_o(METR_HF)]),
    ("ACotra", "METR", "employed-by", None),
    ("ACotra", "OpenPhil", "employed-by", [_o("https://metr.org/team/ajeya-cotra/")]),
    ("ACotra", "EpochAI", "member-of", [_o("https://epoch.ai/about/team")]),
    ("ACotra", "Christiano", "disclosed-relationship", [_o(METR_HF)]),
    ("Besiroglu", "EpochAI", "founded", None),
    ("Besiroglu", "Mechanize", "founded", None),
    ("JSevilla", "EpochAI", "employed-by", None),
    ("EpochAI", "OpenAI", "funded-by", [_p("https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/")]),
    ("EpochAI", "OpenPhil", "funded-by", [_p("https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai/")]),
    ("Ladish", "PalisadeResearch", "founded", None),
    ("Ladish", "Anthropic", "employed-by", [_o("https://palisaderesearch.org/about/")]),
    ("MFredrikson", "GraySwan", "founded", None),
    ("MFredrikson", "CMU", "employed-by", [_o("https://www.grayswan.ai/about")]),
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
