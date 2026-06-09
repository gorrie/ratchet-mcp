# Ratchet MCP — Citation Policy

> **Every record. Every claim. Two URLs minimum.** No exceptions.

This is the project's anti-defamation backbone. It's why the dataset is publishable, why the MCP's responses are defensible, and why the maintainer can hand the repo to a reviewer without flinching.

## Required per record

| Record type | Minimum sources | Required types |
|---|---|---|
| **Person** | 2 URLs | At least one of: LittleSis page, official biography (org or government), Wikidata entry. Wikipedia counts as a secondary — not as the primary. |
| **Institution** | 1 URL | Official site (preferred) OR Wikipedia (acceptable). |
| **Edge (person → institution)** | Inherited from the person's sources — if the institutional position is in the person's `role` text and at least one source corroborates it, the edge is sourced. |
| **Play tag on a person** | Implicitly justified by the person's sourced institutional positions. If the play would only be justified by an unsourced position, the tag is invalid. |
| **Actor tag on a person** | Same rule. Tag must be defensible from the documented positions. |

## Accepted source types

| Type | Code | Notes |
|---|---|---|
| LittleSis | `littlesis` | Public Accountability Initiative's curated influence-network database. Primary. |
| Wikipedia | `wikipedia` | Crowdsourced encyclopedia. Secondary — must pair with another type. |
| Wikidata | `wikidata` | Structured data export of Wikipedia. Primary for membership records (`P463`). |
| Official site | `official` | Institution's own bio / press release / annual report. Primary. |
| Government record | `gov-record` | Senate confirmation hearing transcript, FOIA-released document, Federal Register notice, court filing. Primary. |
| Wayback Machine | `wayback` | Use when the original URL is dead. Note the snapshot date. |
| Academic | `academic` | Peer-reviewed paper, scholarly book (e.g., Domhoff). Primary. |
| News (contemporary) | `news` | Only for confirmation of a specific event, not as a sole source for inclusion. |

## Rejected source types

- Tabloids
- Anonymous blog posts
- Conspiracy aggregators
- Tweets without a corroborating source
- Reddit / forum posts
- Author's own prior work (this is a sourced dataset, not a citation network for *The Ratchet*'s claims)

## Source format in `people.jsonl`

```jsonl
{"id":"Rubin","label":"Robert Rubin",...,"sources":[
  {"type":"littlesis","url":"https://littlesis.org/person/3-Robert_E_Rubin"},
  {"type":"wikipedia","url":"https://en.wikipedia.org/wiki/Robert_Rubin"}
]}
```

Fields per source:
- `type` — one of the accepted source types above
- `url` — full URL
- `note` (optional) — when a citation needs context (e.g., page number, archive snapshot date)
- `accessed` (optional, ISO date) — for sources that may change

## Anti-defamation discipline

Beyond the citation requirement, the `role` text of each person record follows these rules:

1. **No motive imputation.** "X served on Y's board" is OK. "X was paid by Y to advocate for Z" requires a court filing or admitted-conflict-of-interest filing as the citation.
2. **No private-life references.** Marriage, family, health, financial troubles — out unless the role's documentation is directly affected (e.g., "resigned after [public court matter]").
3. **No criminal allegations without conviction or settlement.** "Indicted but not convicted" → out. "Settled SEC charges in 2009" → in, with the SEC citation.
4. **No characterizations.** Adjectives like "controversial," "hawkish," "neoliberal" go in the book; the dataset's `role` text is positions only.

## How CI enforces this

The CI script `tests/audit_citations.py` runs on every PR:

1. **Source count check.** Every person record has ≥2 sources, every institution has ≥1. Exit non-zero if any record fails.
2. **Source type check.** No record has Wikipedia as its only source.
3. **Tag-justification check.** For each `plays` and `actors` tag, the script grep's the person's edges and `role` text for the institutional anchor. If the tag would require an unsourced position to justify, flag it.
4. **Defamation lint** (heuristic). Scans `role` text for forbidden patterns:
   - Adjectival characterizations near a name
   - Phrases like "rumored to," "alleged," "reportedly" (without a citation)
   - Family / health / financial-trouble references
   The heuristic is fuzzy — maintainer can override with explicit reasoning in the PR description.
5. **URL liveness** (optional, run weekly not per-PR). HEAD-requests every source URL; flags 404s for archival via the Wayback Machine.

## Licensing

This repository (code and dataset) is MIT. See [../LICENSE](../LICENSE).

Records here are not bulk-copied from any single upstream — each record
is independently sourced from primary materials (government records,
official org bios, Wikidata, academic papers) plus secondary corroboration
(Wikipedia, archived news). LittleSis is consulted as one citation among
several via the `enrich_from_littlesis` MCP tool at runtime; we are not a
downstream of their dataset.

If you build on this dataset, MIT-style attribution (preserving the
LICENSE notice in derivatives) is all that's required. Each record's
own `sources` array points at the primary URLs you should cite for the
underlying claims.

## Worked example: a record's source provenance

Record: Robert Rubin.

```jsonl
{"id":"Rubin","label":"Robert Rubin","sector":"fin","admin":["clinton"],
 "networks":["cfr","bilderberg"],"plays":["vault","cousin"],"actors":["money"],
 "role":"Goldman → Treasury 1995-99 → Citigroup → CFR Counselor",
 "sources":[
   {"type":"wikipedia","url":"https://en.wikipedia.org/wiki/Robert_Rubin"},
   {"type":"littlesis","url":"https://littlesis.org/person/3-Robert_E_Rubin"}
 ]}
```

- The `role` paraphrases publicly documented positions (Treasury record, Citigroup SEC filings, CFR's own published roster).
- The `vault` play tag is justified by the Goldman → Treasury → Citigroup arc — both endpoints documented in both sources.
- The `cousin` play tag is justified by Bilderberg attendance — published by [bilderbergmeetings.org](https://bilderbergmeetings.org/meetings.html).
- The `money` actor tag is justified by Treasury Secretary role + Citigroup vice-chair role — both touch payment-system / sanctions infrastructure.
- Two sources. One primary (LittleSis), one secondary (Wikipedia). Meets the minimum.

Every record in the dataset should pass this same walkthrough.

## What to do when a source goes dead

1. Find the URL in the Wayback Machine ([web.archive.org](https://web.archive.org/)).
2. Submit a PR updating the source entry to:
   ```jsonl
   {"type":"wayback","url":"https://web.archive.org/web/YYYYMMDDHHMMSS/<original-url>","note":"original 404 as of YYYY-MM-DD"}
   ```
3. Leave the original-URL note so the record remains traceable.

If no archive snapshot exists and the record has only one source after the death:
- If the record has 2+ other live sources, drop the dead one.
- If the dead source brought the record down to 1, the record is at-risk — open a discussion issue, do not silently violate the 2-source minimum.

## Crediting LittleSis

Where a record cites a LittleSis URL in its `sources` array, that's the
attribution at the record level. No additional repo-wide credit is
required — LittleSis is one source type among several. The web viewer's
footer mentions LittleSis as a useful adjacent project, not as an
upstream we depend on.

The staffing-plays and control-grid-actors framing is original to
*The Ratchet* and is what the MCP server exposes on top of the dataset.
