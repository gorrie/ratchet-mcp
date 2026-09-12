#!/usr/bin/env python3
"""Infer `rel` for untyped edges from each person's own career string — and PROVE it first.

810 of 1,245 edges carry no relation type. The Gap Ledger publishes that number to readers
at /tech/record/#/gaps, which is the argument for closing it: the ledger is a promise on the
record. But 810 machine-guessed relations applied to a published dataset is exactly the
failure this project has already paid for once — a restated count that got applied.

So this does not guess. Each person record carries a career string that IS the relation:

    Rubin      "Goldman -> Treasury 1995-99 -> Citigroup -> CFR Counselor"
    Paulson    "Goldman CEO -> Treasury 2006-09 -> Paulson Institute"

An edge whose target institution is named as a step in that sequence is `employed-by`, with
two carve-outs that would otherwise be wrong:

  - MEMBERSHIP bodies (CFR, Bilderberg, Trilateral, Davos/WEF) appear in career strings as
    affiliations, not jobs. `Rubin -> CFR` is `member-of`, and the dataset already says so.
  - A body NAMED AFTER the person is `founded`, not `employed-by`. `Paulson -> PaulsonInst`
    is the giveaway; so is `Bezos -> BezosEarthFund`.

THE VALIDATION SET IS FREE. 435 edges are already typed by hand. Run the same rule over
those and compare: if it cannot reproduce relations a human already assigned, it has no
business inventing 810 new ones. That is `--validate`, and it prints precision per relation.

Nothing is written without --apply, and --apply refuses unless validation precision clears
--min-precision (default 0.95) on the relation being written.

    python scripts/infer_edge_relations.py --validate     # score against the 435 typed edges
    python scripts/infer_edge_relations.py                # dry run: what it WOULD type
    python scripts/infer_edge_relations.py --apply        # write, gated on precision
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "server" / "data"

# Bodies you belong to rather than work for. A career string lists them alongside jobs, so
# without this every CFR affiliation would be relabelled as employment.
MEMBERSHIP = {
    "CFR", "Bilderberg", "Trilateral", "WEF", "Davos", "Chatham", "AspenInstitute",
    "BohemianGrove", "PilgrimsSociety", "AtlanticCouncilMembers",
}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _surface_forms(inst, inst_id):
    """Regexes matching how this institution is written in prose.

    Two forms have to be covered: the label ("Chatham House (Royal Institute...)") and the
    CamelCase id ("WarburgPincus" -> "Warburg Pincus", "NYFed" -> "NY Fed"). Both are joined
    with `\\W*` so punctuation and spacing in the career string do not defeat the match.
    """
    out = []
    label = re.split(r"\s*\(", (inst.get("label") or ""), maxsplit=1)[0].strip()
    words = re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]+|\d+", inst_id)
    for parts in ([w for w in label.split() if w], words):
        if parts:
            out.append(re.compile(r"\W*".join(re.escape(p) for p in parts), re.I))
    return out


def load():
    def jl(name):
        return [json.loads(l) for l in open(DATA / name, encoding="utf-8") if l.strip()]
    return jl("edges.jsonl"), jl("people.jsonl"), jl("institutions.jsonl")


def infer(edge, people, insts):
    """Return (rel, why) or (None, why-not). Never guesses; declines instead."""
    sp, ti = people.get(edge["source"]), insts.get(edge["target"])
    if not sp or not ti:
        return None, "not a person->institution edge"
    role = sp.get("role") or ""
    if not role:
        return None, "person has no career string"

    keys = {norm(ti.get("label")), norm(edge["target"])} - {""}
    if not any(k and k in norm(role) for k in keys):
        # Real relation, unmatchable surface form: "Fed Chair" for FedReserve, "JCS Chair"
        # for DoD. Declining is correct -- an abbreviation table would be a guess wearing
        # a lookup's clothes.
        return None, "target not named in the career string"

    # A JOB TITLE beats the membership list. Chatham House has members, but Robin Niblett's
    # career string says "Chatham House Director and Chief Executive 2007-22" -- that is
    # employment, and calling it member-of because the body appears on a list would have
    # written three wrong relations. The validation set never contained a Chatham edge, so
    # its 100% member-of precision did not cover the case about to be written: precision is
    # only meaningful over classes the control set actually contains.
    JOB_TITLE = re.compile(
        r"\b(director|chief executive|ceo|president|chair(man|woman|person)?|"
        r"secretary[- ]general|managing director|head of|fellow|editor|counselor)\b", re.I)
    # Search the ORIGINAL role string, never a normalized copy. norm() deletes characters,
    # so an index into norm(role) does not map back onto role -- slicing a window at that
    # offset reads the wrong span and the guard silently passes. It did: Kevin Rudd is a
    # "Chatham House Distinguished Fellow", the regex covers `fellow`, and the check missed
    # it anyway. Same class as DEVELOPMENT.md section 5 (str.lower() is not length-preserving).
    for pat in _surface_forms(ti, edge["target"]):
        for m in pat.finditer(role):
            if JOB_TITLE.search(role[max(0, m.start() - 12): m.end() + 48]):
                return None, "career string gives a job title at a membership body -- ambiguous"

    if edge["target"] in MEMBERSHIP or ti.get("sector") in ("cfr",):
        return "member-of", "membership body named in an affiliation list"

    person_key = norm(sp.get("label") or edge["source"])
    tgt_key = norm(edge["target"])
    if person_key and len(person_key) > 3 and person_key in tgt_key:
        return "founded", "institution is named after the person"

    return "employed-by", "named as a step in the career sequence"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true",
                    help="score the rule against the edges a human already typed")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-precision", type=float, default=0.95)
    a = ap.parse_args()

    edges, people_l, insts_l = load()
    people = {p["id"]: p for p in people_l}
    insts = {i["id"]: i for i in insts_l}

    typed = [e for e in edges if e.get("rel")]
    untyped = [e for e in edges if not e.get("rel")]

    # ── validation against the hand-typed edges ──────────────────────────────
    # PRECISION IS PER PREDICTION, not per truth class. Scoring it per truth class answers
    # "of the edges that really are employed-by, how many did I catch" -- recall. That read
    # 100% and would have licensed writing 810 relations. The question --apply actually
    # needs is "of the edges I LABEL employed-by, how many really are", and the same run
    # answers 34%, because 62 appointed-by, 57 board memberships and 14 foundings all look
    # like a job in a career string.
    pred = collections.defaultdict(lambda: collections.Counter())
    declined = collections.Counter()
    wrong_examples = collections.defaultdict(list)
    for e in typed:
        got, _ = infer(e, people, insts)
        truth = e["rel"]
        if got is None:
            declined[truth] += 1
            continue
        pred[got][truth] += 1
        if got != truth and len(wrong_examples[got]) < 4:
            wrong_examples[got].append(f"{e['source']}->{e['target']} is {truth}")

    precision = {}
    print(f"validation against {len(typed)} hand-typed edges")
    print(f"  {'predicted':14} {'n':>5} {'correct':>8}  precision   what it actually was")
    for got in sorted(pred):
        c = pred[got]
        n, right = sum(c.values()), c[got]
        precision[got] = right / n if n else 0.0
        others = ", ".join(f"{k}x{v}" for k, v in c.most_common() if k != got)
        print(f"  {got:14} {n:>5} {right:>8}  {precision[got]:>8.0%}   {others or '-'}")
        for ex in wrong_examples[got]:
            print(f"      {ex}")
    if declined:
        print(f"  declined outright: {sum(declined.values())} "
              f"({', '.join(f'{k} x{v}' for k, v in declined.most_common(4))})")
    if a.validate:
        return 0

    # ── what it would type ───────────────────────────────────────────────────
    proposals, declines = [], collections.Counter()
    for e in untyped:
        rel, why = infer(e, people, insts)
        if rel:
            proposals.append((e, rel))
        else:
            declines[why] += 1
    by_rel = collections.Counter(r for _, r in proposals)
    print(f"\nuntyped edges: {len(untyped)}")
    print(f"  would type:  {len(proposals)}  {dict(by_rel)}")
    print(f"  declines:")
    for why, n in declines.most_common():
        print(f"      {n:>4}  {why}")

    blocked = {r for r in by_rel if precision.get(r, 0) < a.min_precision}
    if blocked:
        print(f"\n  BLOCKED (validation precision below {a.min_precision:.0%}): "
              f"{', '.join(sorted(blocked))}")
        proposals = [(e, r) for e, r in proposals if r not in blocked]
        print(f"  writable after the block: {len(proposals)}")

    if not a.apply:
        for e, r in proposals[:10]:
            print(f"      {e['source']} -> {e['target']}  ::  {r}")
        print("\n  dry run -- pass --apply to write")
        return 0

    if not proposals:
        print("\n  nothing writable. Not touching the dataset.")
        return 1

    # Rewrite in place, preserving every other field and the file's line order.
    want = {(e["source"], e["target"]): r for e, r in proposals}
    path = DATA / "edges.jsonl"
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    out, n = [], 0
    for l in lines:
        rec = json.loads(l)
        k = (rec.get("source"), rec.get("target"))
        if not rec.get("rel") and k in want:
            rec["rel"] = want[k]
            n += 1
        out.append(json.dumps(rec, ensure_ascii=False))
    assert len(out) == len(lines), "line count changed"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"\n  WROTE {n} relation(s) to {path.name}. "
          f"Re-run server/tests/audit_citations.py and tools/freshness_gate.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
