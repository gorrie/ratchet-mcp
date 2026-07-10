"""Wayback archival for Ratchet MCP sources — durability layer for citations.

Every cited URL rots eventually; this makes each source recoverable by pinning a
Wayback snapshot. Lookup-first (existing snapshots — dead sources predate their
death, so a capture almost always exists); SPN2 save is a best-effort fallback
(it is rate-limited / often 429 without S3 keys, so never relied upon).

KEY FINDING baked in (2026-07): raw urllib/HEAD liveness FALSE-flags bot-blocked
hosts (justice.gov, ftc.gov, rand.org, openai.com ... all 403/timeout to a library
UA but 200 in a browser). So liveness here uses a browser User-Agent and treats
ONLY 404/410 and dead-DNS as truly dead; 403/timeout are inconclusive => left alone.

Usage:
  python scripts/wayback_archive.py --url <URL>              # one-off: closest snapshot
  python scripts/wayback_archive.py --dataset --dead-only    # dry-run: what would change
  python scripts/wayback_archive.py --dataset --dead-only --apply   # replace dead urls with snapshots
  python scripts/wayback_archive.py --dataset --annotate --apply    # ADD a wayback companion to every live source (full archival)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
FILES = [DATA / "people.jsonl", DATA / "institutions.jsonl"]

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
AVAIL = "https://archive.org/wayback/available?url="
SAVE = "https://web.archive.org/save/"

# Wikimedia bot-blocks library clients even in a browser UA sometimes; but a real
# 404 on a wiki page usually means the article was renamed. We still archive those
# (the snapshot of the cited title is legitimate provenance), but we never treat a
# wiki host as "dead" purely on a 403.
INCONCLUSIVE = {403, 429, 500, 502, 503, 999}


def _req(url: str, method: str = "GET", timeout: int = 25):
    r = urllib.request.Request(url, method=method, headers={"User-Agent": BROWSER_UA})
    return urllib.request.urlopen(r, timeout=timeout)


def liveness(url: str) -> str:
    """Return 'live' | 'dead' | 'inconclusive' using a browser UA."""
    try:
        with _req(url, method="GET") as resp:
            return "live" if 200 <= resp.status < 400 else "inconclusive"
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return "dead"
        return "inconclusive"
    except (urllib.error.URLError, TimeoutError) as e:
        reason = str(getattr(e, "reason", e)).lower()
        # DNS failure / domain gone => dead; connection/SSL noise => inconclusive.
        if "getaddrinfo" in reason or "name or service" in reason or "nodename" in reason:
            return "dead"
        return "inconclusive"
    except Exception:
        return "inconclusive"


def wayback_lookup(url: str) -> str | None:
    """Closest existing Wayback snapshot URL (https-normalized), or None."""
    try:
        with _req(AVAIL + urllib.parse.quote(url, safe=""), timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None
    snap = (data.get("archived_snapshots") or {}).get("closest") or {}
    if snap.get("available") and str(snap.get("status", "")).startswith("2"):
        return (snap.get("url") or "").replace("http://web.archive.org", "https://web.archive.org")
    return None


def wayback_save(url: str) -> str | None:
    """Best-effort SPN2 save; returns snapshot URL or None (often 429 without keys)."""
    try:
        with _req(SAVE + url, timeout=40) as resp:
            final = resp.geturl()
            return final if "web.archive.org/web/" in final else None
    except Exception:
        return None


def ensure(url: str) -> str | None:
    return wayback_lookup(url) or wayback_save(url)


def iter_records():
    for f in FILES:
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines()):
            if line.strip():
                yield f, i, json.loads(line)


def load(f: Path):
    return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump(f: Path, recs):
    f.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")


def is_wayback(u: str) -> bool:
    return "web.archive.org/web/" in (u or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="one-off: print closest snapshot for URL")
    ap.add_argument("--dataset", action="store_true", help="operate over people+institutions sources")
    ap.add_argument("--dead-only", action="store_true", help="only act on truly-dead (404/410/dead-DNS) urls")
    ap.add_argument("--annotate", action="store_true", help="ADD a wayback companion to every non-wayback source")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--rate", type=float, default=0.5, help="seconds between network calls")
    args = ap.parse_args()

    if args.url:
        print(ensure(args.url) or "NO SNAPSHOT")
        return

    if not args.dataset:
        ap.error("need --url or --dataset")

    changed_total = 0
    for f in FILES:
        recs = load(f)
        fchanged = 0
        for r in recs:
            new_sources = []
            for s in r.get("sources", []):
                url = s.get("url", "")
                if is_wayback(url):
                    new_sources.append(s)
                    continue
                if args.dead_only:
                    live = liveness(url); time.sleep(args.rate)
                    if live != "dead":
                        new_sources.append(s)
                        continue
                    snap = ensure(url); time.sleep(args.rate)
                    if snap and liveness(snap) == "live":
                        print(f"  DEAD  {r['id']:<18} {url}\n   -> WAYBACK {snap}")
                        new_sources.append({"type": "wayback", "url": snap})
                        fchanged += 1
                    else:
                        print(f"  DEAD  {r['id']:<18} {url}\n   -> NO SNAPSHOT (leave for manual)")
                        new_sources.append(s)
                elif args.annotate:
                    new_sources.append(s)
                    snap = wayback_lookup(url); time.sleep(args.rate)
                    if snap and not any(x.get("url") == snap for x in r.get("sources", [])):
                        new_sources.append({"type": "wayback", "url": snap})
                        fchanged += 1
                else:
                    new_sources.append(s)
            r["sources"] = new_sources
        if args.apply and fchanged:
            dump(f, recs)
        print(f"{f.name}: {fchanged} change(s){' [APPLIED]' if (args.apply and fchanged) else ' [dry-run]' if fchanged else ''}")
        changed_total += fchanged
    print(f"TOTAL: {changed_total} change(s)")


if __name__ == "__main__":
    main()
