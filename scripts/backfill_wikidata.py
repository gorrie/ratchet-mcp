"""Backfill: append a Wikidata source to every legacy person record
that currently has < 2 sources.

For each legacy single-source record, look up the Wikidata Q-ID via the
MediaWiki API by sending the existing Wikipedia URL's page title. Append
``{"type":"wikidata","url":"https://www.wikidata.org/wiki/Q<id>"}`` to the
record's ``sources`` array.

Why Wikidata: it's a primary-source structured data export, accepted by
our CITATIONS policy, and every English-Wikipedia article has a Q-ID
that's machine-derivable. URLs are deterministic and won't 404.

Rate: ~5 requests/second to en.wikipedia.org. ~110 records = ~25 seconds.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
PEOPLE = DATA / "people.jsonl"

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "ratchet-mcp-backfill/0.1 (https://github.com/gorrie/ratchet-mcp)"


def wiki_title_from_url(url: str) -> str | None:
    """Extract the article title from an en.wikipedia.org URL."""
    if "en.wikipedia.org/wiki/" not in url:
        return None
    fragment = url.split("/wiki/", 1)[1].split("#", 1)[0].split("?", 1)[0]
    return urllib.parse.unquote(fragment)


def fetch_qid(title: str) -> str | None:
    """Return the Wikidata Q-ID for the given English Wikipedia article
    title, or ``None`` if not found / API error."""
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageprops",
        "titles": title,
        "ppprop": "wikibase_item",
        "redirects": "1",
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = json.loads(r.read())
    except Exception as e:
        print(f"  ! API error for {title!r}: {e}", file=sys.stderr)
        return None
    pages = body.get("query", {}).get("pages", {})
    for page in pages.values():
        qid = (page.get("pageprops") or {}).get("wikibase_item")
        if qid:
            return qid
    return None


def main() -> int:
    records: list[dict] = []
    with PEOPLE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    needs_backfill = [
        r for r in records
        if len(r.get("sources") or []) < 2
    ]
    print(f"Records needing backfill: {len(needs_backfill)} of {len(records)}")

    added = 0
    skipped_no_wiki = 0
    skipped_no_qid = 0
    skipped_dup = 0
    for rec in needs_backfill:
        srcs = rec.get("sources") or []
        existing_types = {s.get("type") for s in srcs if isinstance(s, dict)}
        if "wikidata" in existing_types:
            skipped_dup += 1
            continue
        wiki_src = next(
            (s for s in srcs if isinstance(s, dict) and s.get("type") == "wikipedia"),
            None,
        )
        if not wiki_src:
            skipped_no_wiki += 1
            print(f"  - {rec['id']!r}: no Wikipedia source; skip")
            continue
        title = wiki_title_from_url(wiki_src["url"])
        if not title:
            skipped_no_wiki += 1
            continue
        qid = fetch_qid(title)
        if not qid:
            skipped_no_qid += 1
            print(f"  - {rec['id']!r}: no Q-ID for {title!r}")
            continue
        srcs.append({"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"})
        rec["sources"] = srcs
        added += 1
        # Polite rate limit.
        time.sleep(0.18)

    with PEOPLE.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(f"\nAdded Wikidata sources: {added}")
    print(f"Skipped (no Wikipedia URL): {skipped_no_wiki}")
    print(f"Skipped (no Q-ID found): {skipped_no_qid}")
    print(f"Skipped (already had Wikidata): {skipped_dup}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
