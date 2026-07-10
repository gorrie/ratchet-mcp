# M5 run queue — full OSINT enrichment (real-network, deferred)

Heavy / real-network jobs that the analysis sandbox can't run (Maigret's sites are network-blocked here).
Run this on the **m5** (real network) when ready; it takes the Atlas from a hand-wired slice (~8 feeds,
6 lit cards) to **full enrichment** — a verified footprint + method receipts on every apparatus node.

**Discipline (unchanged):** verify every handle/feed before wiring (`--verify-handle` → OK); OSINT-restraint
floor (public professional only, no locate-kit); method-not-verdict; bounded/watched runs, not fire-and-forget.

---

## Wayback archival (durability layer) — **off-M5, do anytime**

> **Finding (2026-07):** the Wayback availability/CDX API and browser-UA liveness both work
> in the analysis sandbox — this is **not** M5-gated. Only Maigret's 500-site sweep is.
> So run archival now, off-M5; it also fixes the "dead sources with no Wayback snapshot" backlog.

Every cited URL rots. `scripts/wayback_archive.py` pins each source to a Wayback snapshot so
Atlas receipts survive link death. **Lookup-first** (a dead source predates its death, so a
capture almost always already exists); SPN2 on-demand save is best-effort only (rate-limited /
429 without S3 keys — never relied upon).

```bash
python scripts/wayback_archive.py --url <URL>                     # one-off: closest snapshot
python scripts/wayback_archive.py --dataset --dead-only           # dry-run: what would change
python scripts/wayback_archive.py --dataset --dead-only --apply   # replace truly-dead urls w/ snapshot
python scripts/wayback_archive.py --dataset --annotate --apply    # ADD a wayback companion to every source
```

**Liveness caveat baked into the tool:** raw urllib/HEAD FALSE-flags bot-blocked hosts
(justice.gov, ftc.gov, rand.org, openai.com … all 403/timeout to a library UA, 200 in a
browser). The tool uses a **browser UA** and treats ONLY `404/410` + dead-DNS as truly dead;
`403`/timeout are inconclusive and left alone. Apply the same UA fix to `check_url_liveness.py`
before trusting its report.

## Prereqs (on the m5)
```bash
# env: ~/.claude/agents/.env must have TWITTERAPI_IO_KEY + OPENROUTER_API_KEY
pip install maigret feedparser requests
```

## Step 1 — Maigret discovery (the gated step; real network)
For each verified subject in `gorrie/scripts/x/watchlist.json`, find their accounts across sites:
```bash
cd "<workspace>/gorrie/scripts/x"
for h in $(python -c "import json;print(' '.join(s['handle'] for s in json.load(open('watchlist.json'))['subjects'] if s.get('verified')))"); do
  echo "=== $h ==="; python maigret_discover.py "$h" --top-sites 500
done | tee maigret-candidates.txt
```
Output = footprint candidates (Mastodon/Bluesky/Substack/site/GitHub) + guessed RSS feeds, per subject.

## Step 2 — Verify + wire the candidates
For each candidate, confirm it's the right person, then add to the watchlist:
```bash
python x_ingest.py --verify-handle "bluesky:<handle>" --expect "<Full Name>"      # OK / MISMATCH
python x_ingest.py --verify-handle "mastodon:<user@instance>" --expect "<Full Name>"
# add verified ones: append {"rss": "...feed"} and/or {"bluesky":"...","mastodon":"..."} to the subject in watchlist.json
```
(Also fine: WebSearch-discovery — already works off-m5 — for blogs/Substacks Maigret misses.)

## Step 3 — Pull the discovered sources → texts
```bash
python x_ingest.py --timelines --platform rss      --limit 12     # all subjects with an rss field
python x_ingest.py --timelines --platform bluesky  --limit 30     # subjects with a bluesky field
python x_ingest.py --timelines --platform mastodon --limit 30
cd "<workspace>/evil-robots-series/research/ratchet-mcp"
python scripts/import_x_texts.py                                   # bridge all -> texts.jsonl
```

## Step 4 — Precompute receipts (longform → method markers)
```bash
# for each person now carrying longform texts (batch the PersonIDs):
python scripts/precompute_receipts.py --only <Id1,Id2,...> --max-texts 4   # backend=auto
```

## Step 5 — Re-export + rebuild + commit
```bash
python scripts/export_atlas.py --full        # regenerates atlas-data.json (nodes + clusters + receipts)
"<home>/tools/hugo.exe" --minify --buildFuture -s website   # verify clean
git add ... && git commit -m "OSINT enrichment batch (m5 run)" && git push   # both repos
```

## Step 6 — Calibration / tuning (once multi-platform text exists)

The deterministic cue grader (`lens-bundle.json`, run client-side or via `detect_cues`) is the
open + repeatable baseline — use it to tune:
- **Cross-platform consistency:** for a person pulled on ≥2 platforms (X + Substack + Mastodon), grade
  each separately and diff the per-lens signature. A marker that fires only on one platform is a
  *platform artifact*, not a stable signal — flag it; tune the cue/lens so the signature is medium-
  invariant (it's the person's method, not the format).
- **Repeatability lock:** snapshot the cue-grader output on a fixture set → a regression baseline, so
  any taxonomy/cue edit that shifts a score is caught. (Extends `tradecraft/eval/`.)
- **Cue-vs-LLM agreement:** where both ran, measure how often the verified LLM read agrees with the cue
  floor. Low agreement on a lens = the cues are noisy there (refine them) or the lens genuinely needs the
  context read (keep cue-floor advisory). This is how we know the verified layer is adding signal, not
  just cost.

## Optional / later (also m5, also gated)
- **twscrape** X observatory backend — needs your X account(s) added to its pool; wire as the X pull backend.
- **Auto-mapper** (`AUTO-MAPPING-DESIGN.md`) — only after its §5 gates + a measured verifier false-positive rate.
- **Lens deploy** — `lens/deploy/docker compose up` on a host; wire `content/tech/tradecraft.md` to `/grade-text`.

## What this unblocks
Full footprints + lit method-receipt cards across all ~129 profiled apparatus people, so every named
cohort in the Atlas is enriched to the Clark/Jang/Leike standard — the difference between a demo and a
tool people dig through.
