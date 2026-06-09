"""Fix dead URLs in the Ratchet MCP dataset.

Strategy:
1. Re-check each failing URL with a GET request (not HEAD) — many gov
   sites block HEAD but respond to GET. Treat those as alive.
2. For URLs that still 404, query the Wayback Machine for a snapshot.
3. Replace the source entry: change type to "wayback", set url to the
   archive URL, add note: "original 404 as of YYYY-MM-DD"
4. If no Wayback snapshot exists, leave the entry but log it for manual
   handling.

Idempotent: only touches sources whose CURRENT URL still 404s.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"

USER_AGENT = "ratchet-mcp-fix/0.1 (https://github.com/gorrie/ratchet-mcp)"


def get_check(url: str) -> int:
    """GET-request the URL and return status code. -1 = network error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1


def wayback_lookup(url: str) -> str | None:
    """Query Wayback Machine for the most recent snapshot of `url`.

    Returns the archive URL, or None if no snapshot exists.
    """
    api = "https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")
    req = urllib.request.Request(api, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            payload = json.loads(r.read())
    except Exception as e:
        print(f"  wayback API error for {url}: {e}", file=sys.stderr)
        return None
    snapshot = (payload.get("archived_snapshots") or {}).get("closest")
    if snapshot and snapshot.get("available") and snapshot.get("url"):
        return snapshot["url"]
    return None


def process_records(path: Path) -> tuple[int, int, int]:
    """Return (fixed, still_dead, get_alive)."""
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    fixed = 0
    still_dead = 0
    get_alive = 0
    today = date.today().isoformat()

    for rec in records:
        srcs = rec.get("sources") or []
        for i, s in enumerate(srcs):
            if not isinstance(s, dict):
                continue
            url = s.get("url", "")
            if not url:
                continue
            # Only check ones with current type that might be dead.
            if s.get("type") == "wayback":
                continue  # already a Wayback URL
            # Try GET first.
            status = get_check(url)
            time.sleep(0.15)
            if status == 200 or (200 <= status < 400):
                if status != 200:
                    # 3xx redirect — accept
                    pass
                # GET succeeded — alive (was a HEAD-blocked false positive)
                if status >= 300 and status < 400:
                    get_alive += 1
                continue
            # 404 or worse — try Wayback fallback
            wb = wayback_lookup(url)
            time.sleep(0.3)
            if wb:
                srcs[i] = {
                    "type": "wayback",
                    "url": wb,
                    "note": f"original 404 as of {today}: {url}",
                }
                fixed += 1
                print(f"  FIXED {rec['id']!r} -> {wb}")
            else:
                still_dead += 1
                print(f"  DEAD  {rec['id']!r} ({s.get('type')}): {url}")
        rec["sources"] = srcs

    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    return fixed, still_dead, get_alive


def main() -> int:
    print("=== people.jsonl ===")
    f1, d1, g1 = process_records(DATA / "people.jsonl")
    print("=== institutions.jsonl ===")
    f2, d2, g2 = process_records(DATA / "institutions.jsonl")
    print(f"\nFixed (Wayback fallback): {f1 + f2}")
    print(f"Still dead (no snapshot): {d1 + d2}")
    print(f"GET-alive (was HEAD-blocked): {g1 + g2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
