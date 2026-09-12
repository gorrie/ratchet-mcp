#!/usr/bin/env python3
"""Generate README.md's dataset counts from server/data/*.jsonl. Never hand-maintained.

Two copies of a fact -> generate one. README.md said 454 persons / 388 institutions / 948
edges (the v0.2 cut, 2026-07-10) while server/data held 550 / 486 / 1,245, and nothing
compared them: the counts were prose, the data was data, and the public mirror advertised
a dataset a fifth smaller than the one it shipped. This rewrites the block between the
`<!-- counts:begin -->` / `<!-- counts:end -->` markers from the files themselves, and
`--check` exits 1 when the block on disk differs from a fresh render. CI runs --check.

The `## Status` history lines (v0.2 at 454 / 388 / 948, v0.1 at 401 / 351 / 844) are NOT
touched: those are what earlier releases contained, and a historical count is a fact about
the past, not a stale copy of the present.

    python scripts/gen_readme_counts.py            # rewrite the block in README.md
    python scripts/gen_readme_counts.py --check    # exit 1 if README.md is stale
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]           # research/ratchet-mcp/
DATA = ROOT / "server" / "data"
README = ROOT / "README.md"
BEGIN, END = "<!-- counts:begin -->", "<!-- counts:end -->"


def count(name: str) -> int:
    p = DATA / f"{name}.jsonl"
    if not p.is_file():
        sys.exit(f"missing {p}")
    return sum(1 for line in io.open(p, encoding="utf-8") if line.strip())


def render() -> str:
    people, insts, edges = count("people"), count("institutions"), count("edges")
    texts, receipts = count("texts"), count("receipts")
    # Preserve the README's own phrasing; only the numbers are generated.
    return "\n".join([
        f"- **{people:,} named persons** — every record carries ≥2 primary sources and",
        "  tags from the closed [plays](docs/PLAYS.md) and",
        "  [actors](docs/ACTORS.md) vocabularies.",
        f"- **{insts:,} institutions** — every record carries ≥1 source.",
        f"- **{edges:,} edges** — person → institution adjacencies.",
        f"- **{texts:,} stored statements** in the texts-by-person lane (`server/data/texts.jsonl`)",
        f"  and **{receipts:,} receipts** (`server/data/receipts.jsonl`), each a sourced, dated act.",
    ])


def splice(text: str, block: str) -> str:
    pat = re.compile(re.escape(BEGIN) + r"\n.*?\n" + re.escape(END), re.S)
    if not pat.search(text):
        sys.exit(f"README.md has no {BEGIN} ... {END} block")
    return pat.sub(lambda _m: f"{BEGIN}\n{block}\n{END}", text, count=1)


#: Every file that carries the counts block. The release notes for the pending cut carry the
#: same block, so the two cannot disagree -- one generator, two targets, one --check.
TARGETS = [README, ROOT / "RELEASE-NOTES-v0.3.md"]


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    block = render()
    stale = []
    for target in TARGETS:
        if not target.is_file():
            continue
        raw = io.open(target, encoding="utf-8", newline="").read()   # keep the file's own line endings
        nl = "\r\n" if "\r\n" in raw else "\n"
        text = raw.replace("\r\n", "\n")
        want = splice(text, block)
        if want == text:
            continue
        stale.append(target.name)
        if "--check" not in argv:
            io.open(target, "w", encoding="utf-8", newline="").write(want.replace("\n", nl))
    if "--check" in argv:
        if stale:
            print("dataset counts are stale in %s. Run: python scripts/gen_readme_counts.py" % ", ".join(stale))
            return 1
        print("dataset counts match server/data in %s" % ", ".join(t.name for t in TARGETS if t.is_file()))
        return 0
    if stale:
        # ASCII only: a Windows console at cp1252 cannot print the block's own ">=".
        print("wrote counts to %s: %d persons / %d institutions / %d edges / %d texts / %d receipts"
              % (", ".join(stale), count("people"), count("institutions"), count("edges"),
                 count("texts"), count("receipts")))
    else:
        print("counts already current in %s" % ", ".join(t.name for t in TARGETS if t.is_file()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
