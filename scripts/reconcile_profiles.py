"""Phase enrich — draft graph nodes for profiled apparatus people not yet in the ratchet graph.

The Atlas renders the graph; 46 evilrobots.lol profiles have no graph node, so they don't appear. The
profiles already cleared the sourcing bar, so this extracts the load-bearing fields VERBATIM (label,
positions-only role from `status`, the Sources-line URLs) and PROPOSES sector + institutional edges by
keyword. It writes a review draft — it does NOT mutate the graph — and flags institution-profiles that
likely already exist under a different id (e.g. govai->GovAI) so we don't duplicate or collide
(apollo-research must not become the existing Apollo = Apollo Global Management).

Output: docs/reconcile-draft.json  (review, then apply the clean ones).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PROFILES = ROOT.parents[1] / "website" / "content" / "profiles"
OUT = ROOT / "docs" / "reconcile-draft.json"

SECTOR_KW = [
    ("intel", ["CIA", "NSA", "intelligence", "IARPA", "DNI"]),
    ("gov", ["NIST", "CAISI", "White House", "OSTP", "government", "UK AI", "AISI", "Senate", "congress", "federal"]),
    ("tech", ["OpenAI", "Anthropic", "Google", "DeepMind", "Meta", "Microsoft", "xAI", "a16z", "Andreessen",
              "Scale AI", "startup", "Roblox", "Discord", "Mistral", "Hugging Face"]),
    ("tank", ["CSET", "Georgetown", "GovAI", "Oxford", "Berkeley", "Stanford", "MIT", "institute", "center",
              "centre", "RAND", "Brookings", "think tank", "foundation", "academic", "professor", "fellow",
              "MIRI", "FLI", "CAIS", "Partnership on AI", "MLCommons"]),
]
ALIAS = {  # role-text mention -> existing graph institution id
    "openai": "OpenAI", "anthropic": "Anthropic", "google": "Google", "deepmind": "Google",
    "meta": "Meta", "microsoft": "Microsoft", "cset": "CSET", "georgetown": "CSET", "govai": "GovAI",
    "metr": "METR", "rand": "RAND", "nist": "NIST", "caisi": "CAISI", "uk ai security": "UKAISI",
    "scale ai": "Scale", "a16z": "a16z", "discord": "Discord",
    "apollo research": "ApolloResearch", "graphika": "Graphika", "dfrlab": "DFRLab",
    "mlcommons": "MLCommons", "partnership on ai": "PartnershipOnAI", "roost": "ROOST",
    "gray swan": "GraySwan", "xai": "xAI", "cmu": "CMU", "carnegie mellon": "CMU",
}


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def pascal(s):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return "".join(w.capitalize() for w in re.split(r"[^a-z0-9]+", s.lower()) if w)


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    people = load_jsonl(DATA / "people.jsonl")
    insts = load_jsonl(DATA / "institutions.jsonl")
    have_ids = {r["id"] for r in people} | {r["id"] for r in insts}
    inst_slugs = {slug(i["label"].split("(")[0]): i["id"] for i in insts}
    worklist = json.loads((ROOT / "docs" / "atlas-worklist.json").read_text(encoding="utf-8"))

    drafts = []
    for s in worklist["unmatched_profiles"]:
        f = PROFILES / f"{s}.md"
        if not f.exists():
            continue
        txt = f.read_text(encoding="utf-8")
        label = (re.search(r'subject_name:\s*"([^"]+)"', txt) or [None, s])[1]
        if label.isupper():
            label = label.title()   # profiles store SHOUTY subject_name; graph uses Title Case
        register = (re.search(r'register:\s*"([^"]+)"', txt) or [None, ""])[1]
        status = (re.search(r'status:\s*"([^"]+)"', txt) or [None, ""])[1]
        role = re.sub(r"^(ACTIVE|FORMER|INACTIVE)\s*[—-]\s*", "", status).strip()
        kind = "institution" if register == "institutions" else "person"
        sline = (re.search(r"^\*Sources:(.+)", txt, re.M) or [None, ""])[1]
        fline = (re.search(r"\*\*Public footprint:\*\*(.+)", txt) or [None, ""])[1]
        urls = []
        for _t, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", sline + " " + fline):
            if u not in urls:
                urls.append(u)
        for u in re.findall(r"(?<!\()https?://[^\s)\];]+", sline):   # bare URLs (prose-style source lists)
            u = u.rstrip(".,")
            if u not in urls:
                urls.append(u)
        srcs = [{"type": ("wikipedia" if "wikipedia.org" in u else "official"), "url": u} for u in urls]
        sector = "tank"
        for sec, kws in SECTOR_KW:
            if any(k.lower() in role.lower() for k in kws):
                sector = sec; break
        edges = sorted({iid for key, iid in ALIAS.items() if key in role.lower() and iid in have_ids})
        INST_ALIAS = {"govai": "GovAI", "rand-corporation": "RAND", "uk-ai-safety-institute": "UKAISI",
                      "us-caisi": "CAISI", "metr": "METR", "apollo-research": None}  # None = distinct from Apollo PE
        dup = None
        if kind == "institution":
            dup = INST_ALIAS[s] if s in INST_ALIAS else inst_slugs.get(slug(label.split("(")[0]))
        pid = pascal(label)
        drafts.append({"slug": s, "id": pid, "label": label, "kind": kind, "sector": sector,
                       "role": role, "n_sources": len(srcs), "sources": srcs, "edges": edges,
                       "id_collision": pid in have_ids, "likely_existing_inst": dup})

    OUT.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    people_d = [d for d in drafts if d["kind"] == "person"]
    inst_d = [d for d in drafts if d["kind"] == "institution"]
    print(f"{len(drafts)} drafts: {len(people_d)} people, {len(inst_d)} institutions")
    print(f"  people with <2 sources: {sum(1 for d in people_d if d['n_sources'] < 2)}")
    print(f"  id collisions (id already in graph): {[d['id'] for d in drafts if d['id_collision']]}")
    print(f"  institution-profiles likely ALREADY in graph (map, don't add):")
    for d in inst_d:
        print(f"    {d['slug']:28} -> {d['likely_existing_inst'] or 'NEW: ' + d['id']}")
    print(f"\n  sample person drafts:")
    for d in people_d[:6]:
        print(f"    {d['id']:18} [{d['sector']}] src={d['n_sources']} edges={d['edges']}  {d['role'][:55]}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
