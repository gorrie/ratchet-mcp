#!/usr/bin/env python3
"""Every Wikidata QID in the dataset must be the entity it is attached to.

WHY THIS EXISTS
---------------
On 2026-09-26 an audit found 255 of the dataset's 404 Wikidata IDs pointing at unrelated items:
Larry Page's was Steve Wozniak's, Clarence Thomas's Jane Fonda's, Peter Fritsch's "Washington
pie". Every test was green over all of it, because nothing compared an ID to the thing it named.

This keeps `server/data/wikidata-verified.json`: one row per QID in the data, recording the
record it belongs to and what Wikidata says it is. `--refresh` builds it from the Wikidata API
and REFUSES to record a QID whose English label / English Wikipedia title does not match the
record's label (or, for a person, whose instance-of is not human). `--check` is offline: every
QID in the data must be in the file, attached to the same record. The test suite runs --check,
so a new or changed QID cannot land without a --refresh that looked at it.

    python scripts/verify_qids.py --check            # offline gate (tests run this)
    python scripts/verify_qids.py --refresh          # query Wikidata, rewrite the file
    python scripts/verify_qids.py --refresh --cache <wd_cache.json>   # seed from a saved API cache

Wikidata API: batched 50 ids per request, one request at a time, descriptive UA.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"
OUT = DATA / "wikidata-verified.json"
UA = "ratchet-mcp-qidcheck/1.0 (+https://github.com/gorrie/ratchet-mcp)"
QID_RE = re.compile(r"wikidata\.org/wiki/(Q\d+)")


# Letters NFKD does not decompose, and the given-name forms records use for people whom
# Wikidata lists formally ('Tom Donilon' / 'Thomas E. Donilon').
_TRANSLIT = str.maketrans({"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "ß": "ss", "đ": "d",
                           "ł": "l", "Ł": "l", "ı": "i"})
_NICK = {"tom": "thomas", "jim": "james", "jimmy": "james", "ed": "edward", "ted": "edward",
         "bill": "william", "will": "william", "bob": "robert", "rob": "robert", "mike": "michael",
         "dick": "richard", "rick": "richard", "chuck": "charles", "chris": "christopher",
         "dan": "daniel", "dave": "david", "joe": "joseph", "tony": "anthony", "nick": "nicholas",
         "steve": "steven", "ben": "benjamin", "sam": "samuel", "pete": "peter", "andy": "andrew",
         "matt": "matthew", "jeff": "jeffrey", "alex": "alexander", "liz": "elizabeth",
         "kate": "katherine", "sue": "susan", "jon": "jonathan", "ken": "kenneth", "larry": "lawrence"}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "").translate(_TRANSLIT)).encode("ascii", "ignore").decode()
    words = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()
    return " ".join(_NICK.get(w, w) for w in words)


def records():
    """(file, record id, label, kind, [qids]) for every record that cites a Wikidata QID."""
    for name, kind in (("people.jsonl", "person"), ("institutions.jsonl", "institution")):
        for line in (DATA / name).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            qids = sorted(set(QID_RE.findall(line)))
            if qids:
                yield name, r.get("id"), r.get("label") or r.get("name") or "", kind, qids


def names_match(label: str, wd: dict) -> bool:
    a = _norm(label)
    for cand in (wd.get("label"), wd.get("enwiki")):
        b = _norm(cand or "")
        if not a or not b:
            continue
        if a == b or a in b or b in a:
            return True
        aw, bw = set(a.split()), set(b.split())
        # same surname and at least one other shared token ("Ken Lewis" / "Kenneth D. Lewis")
        if aw and bw and a.split()[-1] == b.split()[-1] and (len(aw & bw) >= 2 or
                                                          a.split()[0][:3] == b.split()[0][:3]):
            return True
    return False


def fetch(qids: list[str]) -> dict:
    out = {}
    for i in range(0, len(qids), 50):
        chunk = qids[i:i + 50]
        q = urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(chunk),
                                    "props": "labels|descriptions|claims|sitelinks",
                                    "languages": "en", "sitefilter": "enwiki", "format": "json"})
        req = urllib.request.Request("https://www.wikidata.org/w/api.php?" + q, headers={"User-Agent": UA})
        for attempt in range(5):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 4:
                    raise
                time.sleep(10 * (attempt + 1))
        for k, e in d.get("entities", {}).items():
            claims = e.get("claims", {})
            out[k] = {"label": e.get("labels", {}).get("en", {}).get("value"),
                      "desc": e.get("descriptions", {}).get("en", {}).get("value"),
                      "P31": [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                              for c in claims.get("P31", [])],
                      "enwiki": e.get("sitelinks", {}).get("enwiki", {}).get("title"),
                      "missing": "missing" in e}
        time.sleep(2)
    return out


def refresh(cache_path: str | None) -> int:
    recs = list(records())
    qids = sorted({q for *_, qs in recs for q in qs}, key=lambda q: int(q[1:]))
    wd = json.loads(Path(cache_path).read_text(encoding="utf-8")) if cache_path else {}
    todo = [q for q in qids if q not in wd]
    if todo:
        wd.update(fetch(todo))
    rows, bad = {}, []
    for fname, rid, label, kind, qs in recs:
        for q in qs:
            e = wd.get(q) or {}
            problem = None
            if not e or e.get("missing"):
                problem = "no such item"
            elif not names_match(label, e):
                problem = "names %r / %r, not %r" % (e.get("label"), e.get("enwiki"), label)
            elif kind == "person" and "Q5" not in (e.get("P31") or []):
                problem = "instance-of %s, not human" % (e.get("P31"),)
            if problem:
                bad.append("%s %s (%s): %s" % (q, rid, fname, problem))
                continue
            rows[q] = {"record": rid, "file": fname, "record_label": label,
                       "wikidata_label": e.get("label"), "enwiki": e.get("enwiki"),
                       "desc": e.get("desc")}
    if bad:
        print("REFUSED %d QID(s) -- fix the record, then re-run:" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    OUT.write_text(json.dumps(dict(sorted(rows.items(), key=lambda kv: int(kv[0][1:]))),
                              indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s: %d verified QIDs" % (OUT.name, len(rows)))
    return 0


def check() -> int:
    if not OUT.exists():
        print("FAIL: %s missing -- run --refresh" % OUT.name)
        return 1
    have = json.loads(OUT.read_text(encoding="utf-8"))
    bad, n = [], 0
    for fname, rid, label, kind, qs in records():
        for q in qs:
            n += 1
            row = have.get(q)
            if row is None:
                bad.append("%s on %s (%s) was never verified" % (q, rid, fname))
            elif row["record"] != rid:
                bad.append("%s is on %s but was verified as %s" % (q, rid, row["record"]))
    if n == 0:
        print("FAIL: found no QIDs at all -- a gate that checked nothing must not pass")
        return 1
    if bad:
        print("FAIL: %d QID(s) not verified -- run scripts/verify_qids.py --refresh" % len(bad))
        for b in bad[:30]:
            print("  " + b)
        return 1
    print("%d QID citations, all verified against Wikidata (%s)" % (n, OUT.name))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--refresh", action="store_true")
    ap.add_argument("--cache", help="saved wbgetentities cache to seed --refresh")
    a = ap.parse_args(argv)
    return check() if a.check else refresh(a.cache)


if __name__ == "__main__":
    raise SystemExit(main())
