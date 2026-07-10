# Flagship build plan — Ratchet Atlas + Tradecraft Lens

Master execution plan. Goal (locked 2026-06-29): ship the integrated flagship. **Discipline: enrich only
what the Atlas renders.** Books = fixed mission; OSS v0.2 = credibility byproduct. Design: `FLAGSHIP-DEMO.md`.

> **STATUS (2026-06-29):** Phase 0 ✅. Phase 1 ✅ mostly — node set scoped, RSS/Bluesky/Mastodon ingest
> built, **all 46 profiled apparatus people/orgs reconciled into the graph** (now 454 people / 388 inst
> / 948 edges), receipts lit on the framers (Clark, Jang, Leike, Toner, Bengio, Carlini, Krakovna). Phase
> 2 ✅ — **Atlas v2 shipped** (parked, 178 nodes, node cards + funding flows + receipts). Maigret wired
> (`maigret_discover.py`) but its **live crawl is network-gated** → runs on a real-network box, not the
> sandbox. Remaining: more feeds→cards (incremental), 14→~8 footprints, twscrape/SpiderFoot (gated),
> Phase 3 cross-link + deploy (author-gated), Phase 4 drift.

## Phase 0 — Foundations (DONE this session)

- ✅ **Receipt verifier** (`detect.verified_cue_receipts` / `texts.verified_person_receipts`) — the
  shared atom; kills cues-floor false positives.
- ✅ **Finance/funding graph buildout** — 417 people / 384 inst / 926 edges; finance→apparatus queryable.
- ✅ **Bluesky + Mastodon public-API ingest** + cross-platform correctness gate (`--verify-handle`).
- ✅ **Prompt-injection defense** (`sanitize_untrusted`) — load-bearing for the public Lens.
- ✅ **ratchet-osint-pass skill** + recalibrated **OSINT-RESTRAINT** (content-type-not-access) + observatory accounts.
- ✅ **Lens local demo** (component A) — `/grade-text` + UI, tested, live-verified.

## Phase 1 — Scope + the data the Atlas needs (the SCOPED enrichment)

> This is where "enrich only what the demo renders" bites: the Atlas node set IS the enrichment worklist.

- **1a. Scope the Atlas node set.** Not all 417 — foreground the WtW apparatus + finance principals +
  their edges (the "power ranking" set). Output: an explicit node worklist. *Unblocks everything.*
- **1b. RSS/Atom ingest backend** (`x_ingest`/`import_texts`). The missing high-yield source: the
  verifier finding proved short posts yield ~0 publishable markers; **longform (Substack/blogs/org
  newsrooms) is where markers live.** Without RSS the Atlas node cards are thin. *Critical-path.*
- **1c. Pull texts for the worklist** — X (twitterapi) + Bluesky/Mastodon (built) + RSS (1b) → bridge to
  `texts.jsonl` (drop reposts, dedupe, injection-flag).
- **1d. Footprint pass on the worklist** (task #26, Maigret-accelerated #27): Maigret discovers candidate
  handles → `--verify-handle` gates → record verified footprint. Parallel to 1b/1c.
- **1e. Precompute verified receipts** for the worklist (`verified_person_receipts`, backend=auto) →
  static JSON the Atlas embeds. Depends on 1c (texts) + the verifier.

## Phase 2 — Atlas v2 (static; component B)

- **2a. Data export.** graph (people/inst/edges) + precomputed receipts (1e) + footprints (1d) → one
  static JSON bundle (no live backend).
- **2b. Graph view.** Extend the `/tech/revolving-door/` D3: full worklist graph, filter by
  sector/play/actor, the **finance→apparatus funding-flow** view (METR triple-funded; labs→FMF Safety Fund).
- **2c. Node cards.** profile + receipts (receipts-first, method-not-verdict) + footprint.
- **2d. Hugo page** (`/tech/ratchet-atlas/`), parked (`date: 2099`) until review.

## Phase 3 — Integrate + deploy

- **3a. Cross-link** Atlas↔Lens via the receipt: node → "run the Lens on their texts"; Lens marker →
  who else in the Atlas exhibits it.
- **3b. Deploy the Lens backend.** `/grade-text` container (reuse the Raziel reference-tool docker
  model: backend key / local model, CORS, healthz). **Author-gated host.**
- **3c. Go-public gate.** Disclaimers/parody framing; adversarial review of a sample map
  (guilt-by-association, bycatch); author sign-off; unpark.

## Phase 4 — Drift / integrity tracker (the differentiator)

- **4a. Historical pulls** — extend ingest over time per worklist node (RSS makes this rich).
- **4b. Analysis** — per-lens timeline → variance (no-stable-principal / opportunist) + changepoint
  (flip / capture / substitution; *Quiet Autocomplete* voice-substitution made measurable).
- **4c. Atlas view** — integrity overlay on the node cards.

## Parallel / byproduct

- **ratchet-mcp v0.2 OSS** (task #24) — ship to github.com/gorrie once tooling stable; the
  tooling-improvement writeup (`RELEASE-NOTES-v0.2-DRAFT.md`) is staged and current.

## Critical path

`1a scope → 1b RSS → 1c pulls → 1e receipts → 2 Atlas → 3 deploy`. 1d footprints runs parallel; Phase 4
follows public launch.

## Gates (cross-cutting, non-negotiable)

- **Method-not-verdict** everywhere; receipts-first; sourced; ≥2 sources per node.
- **Enrich only worklist nodes** — no open-ended accumulation.
- **Auto-mapper stays INTERNAL** until tuned past `AUTO-MAPPING-DESIGN.md` §5; nothing auto-writes to the
  public Atlas (human-in-the-loop).
- **Deploy host + public unpark are author decisions.**
- **OSINT-restraint floor** per node (content-type, not access; locate-kit stays out).
