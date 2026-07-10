"""Phase 1e — precompute method-marker receipts for the Atlas node cards.

Grades a person's LONGFORM texts (source=rss; tweets yield ~0 per the verifier finding) with the
context-reading backend and keeps the strongest firing markers as receipts (lens + verbatim span + the
source URL + rationale). These are detect(auto) hits — already an LLM context read, the trustworthy
receipt — written to server/data/receipts.jsonl for export_atlas.py to attach to nodes.

Cost is O(longform_texts x text_lenses) model calls, so it grades only longform and caps per person.

Run:  python scripts/precompute_receipts.py --only JClark,Jang [--max-texts 6]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


def is_longform(t):
    """Longform if the URL is not a microblog post (tweet/bsky/mastodon status). The bridge drops the
    'source' field, so classify by URL shape; also honor an explicit source==rss if present."""
    if t.get("source") == "rss":
        return True
    u = t.get("url", "") or ""
    if not u:
        return False
    micro = ("/status/" in u) or ("bsky.app" in u) or bool(re.search(r"/@[^/]+/\d+/?$", u))
    return not micro

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
RECEIPTS = ROOT / "server" / "data" / "receipts.jsonl"
TEXTS = ROOT / "server" / "data" / "texts.jsonl"

ENV = os.path.expanduser("~/.claude/agents/.env")
if os.path.exists(ENV):
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_receipts():
    out = {}
    if RECEIPTS.exists():
        for line in RECEIPTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out.setdefault(r["person_id"], []).append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated person_ids", required=True)
    ap.add_argument("--max-texts", type=int, default=6, help="cap longform texts graded per person")
    ap.add_argument("--per-person", type=int, default=6, help="max receipts kept per person")
    ap.add_argument("--backend", default="auto")
    args = ap.parse_args()

    from ratchet_mcp.texts import _import_tradecraft, _tradecraft_detectors_dir
    load_lenses, _, text_lenses = _import_tradecraft()
    from tradecraft.detect import detect
    from tradecraft.grader import grade_document_for_lens
    lenses = text_lenses(load_lenses(_tradecraft_detectors_dir()))

    texts = [json.loads(l) for l in TEXTS.read_text(encoding="utf-8").splitlines() if l.strip()]
    store = load_receipts()
    pids = [p.strip() for p in args.only.split(",") if p.strip()]

    for pid in pids:
        longform = [t for t in texts if t.get("person_id") == pid and is_longform(t)]
        longform = sorted(longform, key=lambda t: len(t.get("text", "")), reverse=True)[:args.max_texts]
        found = []
        for t in longform:
            tok = max(1, len(t.get("text", "").split()))
            for lid, tax in lenses.items():
                try:
                    hits = detect(t["text"][:8000], tax, backend=args.backend)
                except Exception:
                    continue
                r = grade_document_for_lens(tax, hits, token_count=tok)
                if r.index <= 0 or not hits:
                    continue
                h = hits[0]
                found.append({"person_id": pid, "lens": lid, "detection_id": h.detection_id,
                              "span": h.span, "url": t.get("url", ""), "date": t.get("date", ""),
                              "rationale": h.rationale, "index": round(float(r.index), 1)})
        found.sort(key=lambda x: x["index"], reverse=True)
        # one receipt per lens (strongest), capped
        seen, kept = set(), []
        for rc in found:
            if rc["lens"] in seen:
                continue
            seen.add(rc["lens"]); kept.append(rc)
            if len(kept) >= args.per_person:
                break
        store[pid] = kept
        print(f"{pid}: {len(kept)} receipts from {len(longform)} longform texts -> "
              + ", ".join(f"{r['lens']}({r['index']})" for r in kept))

    with RECEIPTS.open("w", encoding="utf-8") as fh:
        for pid in sorted(store):
            for rc in store[pid]:
                fh.write(json.dumps(rc, ensure_ascii=False) + "\n")
    print(f"wrote {RECEIPTS.relative_to(ROOT)} ({sum(len(v) for v in store.values())} receipts)")


if __name__ == "__main__":
    main()
