# Ratchet MCP

> Open-source Model Context Protocol server for a curated, source-cited
> dataset of named persons and institutions across the US legal /
> regulatory / financial / multilateral control grid — tagged with
> recurring staffing plays and control-grid mechanisms.

Companion to *The Ratchet: How Safety Infrastructure Became the Control
Grid* (Evil Robots Series Book 2, 4LULZ). The book argues that a small
recurring cohort runs identifiable, repeating personnel patterns across
US administrations. This MCP server makes those patterns directly
queryable.

## What's in it

- **454 named persons** — every record carries ≥2 primary sources and
  tags from the closed [plays](docs/PLAYS.md) and
  [actors](docs/ACTORS.md) vocabularies.
- **388 institutions** — every record carries ≥1 source.
- **948 edges** — person → institution adjacencies.
- **MCP server** in Python with 10 tools: `query_cohort`, `get_entity`,
  `who_connects`, `find_overlap`, `list_plays_for`, `list_players_for`,
  `find_in_administration`, `grade_person_texts`, `enrich_from_littlesis`,
  `littlesis_relationships`.
- **Texts-by-person lane** — `grade_person_texts` runs the
  [Tradecraft](https://github.com/gorrie/tradecraft) TEXT lenses over a dataset person's stored
  statements (`server/data/texts.jsonl`; see its `texts.README.md`), profiling
  *how their own words operate* per lens, aggregated per subject, never blended,
  never a verdict. The graph half profiles topology; this is the prose half.
- **Optional web viewer** — D3 force-directed graph at `http://localhost:8088`.

## Quickstart

```bash
git clone https://github.com/gorrie/ratchet-mcp
cd ratchet-mcp
docker compose up --build
# Web viewer (optional):
docker compose --profile web up --build
```

Wire to Claude Desktop by adding to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ratchet": {
      "command": "docker",
      "args": ["compose", "-f", "/absolute/path/to/ratchet-mcp/docker-compose.yml",
               "run", "--rm", "-T", "mcp"]
    }
  }
}
```

Three example prompts to demo the surface — see
[docs/PROMPTS.md](docs/PROMPTS.md) for the full set:

- **Trump II Vault**: *"Who ran the Vault play under the Trump II
  administration?"* → 4-5 named Treasury revolvers with sourced positions.
- **Anthropic → State**: *"What connects Anthropic to the State
  Department?"* → multi-hop path through senior policy staff with
  documented cross-affiliations.
- **Two Cranks Same Hand**: *"Find people who touched both `tap` and
  `backdoor` actors."* → Hayden, Cheney, Bolton.

## Scope and discipline

This is an **open dataset** held to publication standards:

- **Every record has ≥2 primary sources.** No record makes it past CI
  with Wikipedia as its only source. See [docs/CITATIONS.md](docs/CITATIONS.md).
- **No motive imputation, no characterizations, no private-life
  references, no unproven allegations.** The `role` field is positions
  only. See the anti-defamation policy in
  [docs/CITATIONS.md](docs/CITATIONS.md#anti-defamation-discipline).
- **Foundations are in, bloodline conspiracy framing is out.** This is a
  dataset about documented institutional positions. See
  [docs/SCOPE.md](docs/SCOPE.md#what-we-deliberately-exclude).

To propose additions or corrections, read
[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) first. PRs that don't meet
the citation and tag-justification standards get blocked at CI.

## Related projects

Part of a three-repo toolkit for measuring institutional capture — the graph
layer here, the prose grader, and the model-layer audit:

- **[tradecraft](https://github.com/gorrie/tradecraft)** — detect-the-method
  capture grader. The `grade_person_texts` tool here calls Tradecraft's TEXT
  lenses to profile *how a dataset person's own words operate*; this repo is the
  graph half, Tradecraft is the prose half.
- **[bias-study](https://github.com/gorrie/bias-study)** — a reproducible audit
  of institutional-skepticism framing across 36+ LLMs, including *The Wash*, the
  abliterated low-flinch judge that Tradecraft's verify step can run as its
  `local` context-reading backend.
- **[evilrobots.lol](https://evilrobots.lol)** — the same argument in narrative
  form; companion to *The Ratchet* (Evil Robots Series Book 2, 4LULZ).

## Licensing

MIT for everything — code and dataset. See [LICENSE](LICENSE). Use it,
fork it, ship it. Citations within each dataset record point at the
underlying primary sources independently of how this repo is licensed.

LittleSis (linked from `enrich_from_littlesis`) is a runtime API, not
an upstream we copy from. Records in `server/data/` are independently
sourced from gov records / Wikidata / official org bios / academic
papers / archived press releases — LittleSis appears as one citation
among several, not as the dataset's origin.

## Layout

```
ratchet-mcp/
├── docs/                        # SCOPE, PLAYS, ACTORS, PROMPTS,
│                                # CITATIONS, CONTRIBUTING
├── server/
│   ├── ratchet_mcp/             # Python package
│   │   ├── data.py              # JSONL loader / Graph
│   │   ├── queries.py           # Query primitives
│   │   ├── littlesis.py         # LittleSis API client
│   │   └── server.py            # MCP tool surface
│   ├── data/                    # JSONL data (single source of truth)
│   ├── tests/                   # pytest suite
│   ├── pyproject.toml
│   └── Dockerfile
├── web/                         # Optional D3 viewer
│   ├── Dockerfile
│   ├── index.html
│   ├── viewer.js
│   ├── viewer.css
│   └── nginx.conf
├── scripts/
│   └── extract_from_graphjs.js  # one-time extraction from upstream graph.js
├── docker-compose.yml
├── LICENSE                      # MIT (code + data)
└── README.md
```

## Status

`v0.2` — 2026-07-10. Dataset at 454 persons / 388 institutions / 948 edges.
New since v0.1: the Watching-the-Watchers eval/statecraft and lab/policy
wings, the finance/funding layer behind the apparatus (grantmakers →
evaluators queryable as data), full apparatus reconciliation (all 46
book/website profiles are now graph nodes), and the `rumpelstiltskin →
bretton` play rename. v0.1 (2026-06-09) was the initial public release at
401 / 351 / 844, covering SCOPE.md cohorts A–F plus the foreign-influence /
Five Eyes / UK-EU / USAID-DRG / Gulf customer / climate-ESG /
health-governance / nation-state comparative clusters and the
historical-ideologues layer. The book *The Ratchet* ships shortly; this
dataset is the queryable form of its institutional infrastructure argument,
and the release time-series is itself the bias-drift instrument.

**Longitudinal cadence.** Re-sampled periodically. Each cut is tagged
(`vX.Y.Z`) so peer experimenters can pin a specific version and
reproduce; the time-series of cuts is the bias-drift instrument.

Server tool surface stable. CI gates citation, source-count, and
tag-justification rules (see `.github/workflows/ci.yml`).
