"""URL liveness sweep on the Ratchet MCP dataset.

HEAD-request every source URL across people.jsonl + institutions.jsonl,
report 404s / timeouts / redirects to Wayback. Rate-limited (~5 req/s)
so we don't trip any DDoS detector.

Output: scripts/_url-liveness-report.md (markdown, sorted by status code)
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
OUT = ROOT / "scripts" / "_url-liveness-report.md"

# Browser UA: a library UA gets FALSE 403/timeout from bot-blocked-but-live hosts
# (justice.gov, ftc.gov, rand.org, openai.com ...). Confirmed 2026-07: those return
# 200 in a browser. Without this the report is drowned in false-positive 403s that
# would wrongly trigger Wayback swaps. Treat 403/timeout as INCONCLUSIVE, not dead.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

# Wikimedia bot-blocks raw HEAD/GET — it serves 404/403 to automated clients even
# for live pages (confirmed: live Wikidata items like Q22245690/Q333792 return 404
# to urllib). Raw-fetch liveness is therefore meaningless for these; verify titles
# via the MediaWiki API and QIDs via the Wikidata API instead. Skip them here so the
# report isn't drowned in false-positives that would wrongly trigger Wayback swaps.
SKIP_DOMAINS = ("wikipedia.org", "wikidata.org")


def collect_urls() -> list[tuple[str, str, str, str]]:
    """Return list of (record_id, kind, source_type, url)."""
    urls = []
    for fname, kind in (("people.jsonl", "person"), ("institutions.jsonl", "institution")):
        path = DATA / fname
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                for s in rec.get("sources", []) or []:
                    if isinstance(s, dict) and s.get("url"):
                        if any(d in s["url"] for d in SKIP_DOMAINS):
                            continue  # Wikimedia bot-blocks raw fetch — verify via API, not here
                        urls.append((rec["id"], kind, s.get("type", ""), s["url"]))
    return urls


def check_url(url: str) -> tuple[int, str]:
    """Return (status_code, note). status_code -1 means network error."""
    for method in ("HEAD", "GET"):  # some hosts 403/405 HEAD but 200 GET
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.status, r.headers.get("Location", "")
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # retry with GET
            return e.code, str(e)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            return -1, type(e).__name__ + ": " + str(e)[:80]
        except Exception as e:
            return -2, type(e).__name__ + ": " + str(e)[:80]
    return 403, "HEAD+GET both 403/405"


def main() -> int:
    urls = collect_urls()
    total = len(urls)
    print(f"Checking {total} URLs...", file=sys.stderr)

    results = []
    by_status = defaultdict(int)
    by_domain = defaultdict(lambda: {"ok": 0, "fail": 0})

    for i, (rid, kind, stype, url) in enumerate(urls, 1):
        status, note = check_url(url)
        results.append((rid, kind, stype, url, status, note))
        by_status[status] += 1
        domain = urllib.parse.urlparse(url).netloc
        if status == 200 or 200 <= status < 400:
            by_domain[domain]["ok"] += 1
        else:
            by_domain[domain]["fail"] += 1
        if i % 25 == 0:
            print(f"  [{i}/{total}] {by_status}", file=sys.stderr)
        time.sleep(0.2)  # 5 req/s

    # Markdown report
    lines = ["# URL Liveness Report\n"]
    lines.append(f"Total URLs: **{total}**\n")
    lines.append("## Status code distribution\n\n| Code | Count |\n|---|---|")
    for code in sorted(by_status.keys()):
        label = "200 OK" if code == 200 else ("Network error" if code == -1 else f"HTTP {code}")
        lines.append(f"| {label} | {by_status[code]} |")
    lines.append("")

    failures = [r for r in results if r[4] != 200 and not (200 <= r[4] < 400)]
    if failures:
        lines.append(f"\n## Failures ({len(failures)})\n")
        lines.append("| Record | Type | URL | Status | Note |")
        lines.append("|---|---|---|---|---|")
        for rid, kind, stype, url, status, note in failures:
            note_clean = note.replace("|", "/").replace("\n", " ")[:80]
            lines.append(f"| `{rid}` ({kind}) | {stype} | {url} | {status} | {note_clean} |")
    else:
        lines.append("\n## All clear\n\nNo failures.")

    lines.append("\n## By domain\n\n| Domain | OK | Fail |\n|---|---|---|")
    for dom, c in sorted(by_domain.items(), key=lambda x: (-x[1]["fail"], -x[1]["ok"])):
        lines.append(f"| {dom} | {c['ok']} | {c['fail']} |")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {OUT}")
    print(f"Failures: {len(failures)} / {total}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
