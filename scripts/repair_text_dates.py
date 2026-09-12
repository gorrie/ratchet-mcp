#!/usr/bin/env python3
"""Repair dates truncated by the old `created_at[:10]` ingest bug.

`import_x_texts.py` stored `(created_at or "")[:10]`. That is correct for ISO
feeds and destructive for RFC-822 ones (X, and every Substack RSS `pubDate`):
"Mon, 06 Apr 2026 09:00:00 GMT" became "Mon, 06 Ap" -- weekday, day, and half a
month, with the year gone. 58 of 328 texts and all 24 derived receipts carry it.

Recovery policy, deliberately conservative:
  - A truncated date is recoverable only if weekday + day + month resolve to
    exactly ONE past date. Ambiguous month stems ("Ma" = Mar|May, "Ju" = Jun|Jul)
    usually do not, and future dates are never candidates.
  - Anything not uniquely determined gets `date: null`. We do not guess a date on
    a sourced record. The original string is preserved in `date_corrupt` so the
    damage stays visible and a later re-fetch can target exactly those rows.

Idempotent. Run with --apply to write; default is a dry run.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TRUNC = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\d{2}) ([A-Z][a-z])$")
WD = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
STEM = {"Ja": [1], "Fe": [2], "Ma": [3, 5], "Ap": [4], "Ju": [6, 7],
        "Au": [8], "Se": [9], "Oc": [10], "No": [11], "De": [12]}


def recover(s, today):
    """Return an ISO date iff weekday+day+month-stem pin exactly one past date."""
    m = TRUNC.match(str(s))
    if not m:
        return None
    wd, day, stem = WD[m.group(1)], int(m.group(2)), m.group(3)
    hits = []
    for year in range(today.year - 6, today.year + 1):
        for month in STEM.get(stem, []):
            try:
                d = datetime.date(year, month, day)
            except ValueError:
                continue
            if d.weekday() == wd and d <= today:
                hits.append(d)
    return hits[0].isoformat() if len(hits) == 1 else None


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def write(p, rows):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--today", help="ISO date to treat as today (testing)")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()

    stats = {"recovered": 0, "nulled": 0, "already_ok": 0}
    fixed_by_url = {}

    for name in ("texts.jsonl", "receipts.jsonl"):
        path = DATA / name
        rows = load(path)
        for r in rows:
            d = r.get("date")
            if not d or ISO.match(str(d)):
                if d:
                    stats["already_ok"] += 1
                continue
            # A receipt inherits its text's date -- prefer the repaired value.
            got = fixed_by_url.get(r.get("url")) or recover(d, today)
            if got:
                r["date_corrupt"] = d
                r["date"] = got
                if r.get("url"):
                    fixed_by_url[r["url"]] = got
                stats["recovered"] += 1
            else:
                r["date_corrupt"] = d
                r["date"] = None
                stats["nulled"] += 1
        if a.apply:
            shutil.copy(path, str(path) + ".prerepair")
            write(path, rows)

    print(f"already ISO : {stats['already_ok']}")
    print(f"recovered   : {stats['recovered']}  (weekday+day+month pinned one past date)")
    print(f"nulled      : {stats['nulled']}  (ambiguous -- original kept in `date_corrupt`)")
    print("APPLIED" if a.apply else "dry run -- pass --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
