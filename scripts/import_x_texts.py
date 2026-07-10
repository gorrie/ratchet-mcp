#!/usr/bin/env python
"""Bridge: x_ingest timelines -> ratchet-mcp texts.jsonl (the texts-by-person lane).

Reads the x_ingest output (gorrie/scripts/x/data/timelines/<handle>.jsonl) + the watchlist
(handle -> name), matches each subject's NAME to a person LABEL in people.jsonl to resolve the
ratchet person_id, DROPS retweets (an "RT @..." is not the subject's own speech), and appends the
subject's own posts to texts.jsonl as {person_id, id, text, url, date}, deduped by id.

Only subjects already present in people.jsonl are bridged — you cannot grade a person the graph
does not know. This is the PRODUCER for grade_person_texts / profile_person: pulled speech in,
tradecraft grading out.

Usage (from ratchet-mcp/):
  python scripts/import_x_texts.py --dry-run
  python scripts/import_x_texts.py --only alexstamos
  python scripts/import_x_texts.py            # bridge every verified subject with a people.jsonl match
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RATCHET = HERE.parent
DATA = RATCHET / "server" / "data"
PEOPLE = DATA / "people.jsonl"
TEXTS = DATA / "texts.jsonl"
# gorrie is a workspace sibling: ratchet-mcp -> research -> evil-robots-series -> <workspace>
DEFAULT_X = RATCHET.parents[2] / "gorrie" / "scripts" / "x"


def load_name_to_id() -> dict:
    m = {}
    for line in PEOPLE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        lbl = (r.get("label") or "").strip().lower()
        if lbl:
            m[lbl] = r["id"]
    return m


def existing_ids() -> set:
    ids = set()
    if TEXTS.exists():
        for line in TEXTS.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    ids.add(json.loads(line)["id"])
                except Exception:   # noqa: BLE001
                    pass
    return ids


def main():
    ap = argparse.ArgumentParser(description="Bridge x_ingest timelines into ratchet-mcp texts.jsonl.")
    ap.add_argument("--x-dir", default=str(DEFAULT_X), help="x_ingest dir (holds watchlist.json + data/)")
    ap.add_argument("--only", help="comma-separated handles to restrict to")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    a = ap.parse_args()

    xdir = Path(a.x_dir)
    wl = json.loads((xdir / "watchlist.json").read_text(encoding="utf-8"))
    handle_to_name = {s["handle"].lower(): s.get("name", "") for s in wl.get("subjects", [])}
    name_to_id = load_name_to_id()
    only = {h.strip().lstrip("@").lower() for h in a.only.split(",")} if a.only else None
    seen = existing_ids()

    new_rows, report = [], []
    tl = xdir / "data" / "timelines"
    for f in sorted(tl.glob("*.jsonl")):
        handle = f.stem.lower()
        if only and handle not in only:
            continue
        name = handle_to_name.get(handle)
        pid = name_to_id.get((name or "").lower()) if name else None
        if not pid:
            report.append(f"  skip @{handle}: '{name}' not in people.jsonl (add via ratchet-add-person)")
            continue
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        own = [r for r in rows if not (r.get("text") or "").startswith("RT @")]
        added = 0
        for r in own:
            tid = str(r.get("id"))
            txtid = f"x-{tid}"
            txt = (r.get("text") or "").strip()
            if not txt or txtid in seen:
                continue
            new_rows.append({
                "person_id": pid,
                "id": txtid,
                "text": txt,
                "url": r.get("url") or f"https://x.com/{handle}/status/{tid}",
                "date": (r.get("created_at") or "")[:10],
            })
            seen.add(txtid)
            added += 1
        report.append(f"  + @{handle} -> {pid}: {len(own)} own posts, {added} new")

    print("\n".join(report) or "  (no matching timelines)")
    if a.dry_run:
        print(f"DRY RUN: {len(new_rows)} texts would be appended to {TEXTS}")
        return
    with TEXTS.open("a", encoding="utf-8") as fh:
        for r in new_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Appended {len(new_rows)} texts to {TEXTS}. Now: grade_person_texts(<person_id>).")


if __name__ == "__main__":
    main()
