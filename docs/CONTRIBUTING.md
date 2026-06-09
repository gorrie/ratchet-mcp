# Contributing to Ratchet MCP

The dataset grows via pull requests. **The framework is closed. The values are open.**

- The 9 sectors and the 5 dimensions (sector / admin / network / plays / actors) are fixed structural choices — proposing a new sector or a new dimension requires a substantive design argument, not just a record to add.
- The values within those dimensions — specific plays, specific actors, specific networks, specific people — grow as contributors submit them. Every value requires the same source-and-justification standard the maintainer uses.

Read [SCOPE.md](SCOPE.md) before opening anything. The 2-sector criterion is non-negotiable.

## How to add a new person

1. **Confirm the 2-sector test.** The person must have held a senior position in two or more of the 9 sectors. If they're famous in one sector only, they're out of scope — no matter who they are.
2. **Gather sources.** Minimum two URLs from the [source priors list in SCOPE.md](SCOPE.md#source-priors-where-the-data-comes-from). LittleSis + Wikipedia is the typical pair. CI rejects PRs with fewer than 2 sources.
3. **Write the record.** JSONL format, one record per line:
   ```jsonl
   {"id":"Slug","label":"Full Name","kind":"person","sector":"gov","admin":["bush2","trump1"],"networks":["cfr","bilderberg"],"plays":["pulpit","cousin"],"actors":["embassy","tap"],"role":"Paraphrase of documented positions only.","sources":[{"type":"littlesis","url":"https://littlesis.org/person/N-Name"},{"type":"wikipedia","url":"https://en.wikipedia.org/wiki/Name"}]}
   ```
4. **Justify every tag.** Each `plays` tag and each `actors` tag must be supportable by the documented positions in the role text. If you'd need to assume the person's motivation to apply a tag, drop the tag.
5. **Add edges.** Each documented institutional position becomes an edge in `edges.jsonl`. Format: `["PersonId","InstitutionId"]`.
6. **Open the PR.** CI runs the citation audit + tag justification check + duplicate-id scan. Land or fix.

## How to add a new play

A "play" is a named recurring personnel pattern. Examples already in the dataset: `vault` (Wall Street → Treasury → back to Wall Street), `pulpit` (CFR → State → CFR President), `cycle` (Trilateral → senior admin → think tank).

To propose a new play:

1. **Name it.** One word, lowercase, evocative.
2. **Define it.** One paragraph in `docs/PLAYS.md`. The definition must be operational: "X person executes Play Y if they did Z."
3. **Demonstrate it.** List ≥3 people already in the dataset who satisfy your definition, with citations. If only 1-2 people fit, the pattern isn't recurring enough to name.
4. **Update existing records.** Add the play tag to those ≥3 people in `people.jsonl`. Tag justification rules from "How to add a new person" apply.
5. **Open the PR with all three changes in one commit.** Definition + tagged records + ≥3 example citations.

## How to add a new actor

An "actor" is a control-grid mechanism — one of the 20 Ratchet clicks from *The Ratchet* book (or a clearly-defined extension). Examples already in the dataset: `tap` (SIGINT), `money` (payment freezing / CBDC), `blueprint` (AI governance).

To propose a new actor:

1. **Map it to a Ratchet click.** If your proposed actor doesn't map to one of the 20, it's probably already covered by an existing actor — re-read [the click index](https://evilrobots.lol/tech/ratchet-clicks/) before opening the PR.
2. **Add to `docs/ACTORS.md`** with: name, 1-paragraph definition, the Ratchet click it maps to, and ≥2 example person→actor linkages from the existing dataset.
3. **Update existing records.** Add the actor tag to qualifying people, with tag-justification rules applied.

## How to add a new sector

**Rare.** The 9 sectors were chosen to be exhaustive for US-centric power rotation; new ones should be a real surprise. If you're proposing one:

1. **Demonstrate the gap.** Show ≥5 in-scope people whose primary institutional pattern doesn't fit any of the existing 9 sectors.
2. **Define the boundary.** What's the sector's "senior position" test? (See SCOPE.md table for the existing tests.)
3. **Color it.** Pick a hex color that contrasts with the existing 8. The visualization assigns colors per sector.
4. **Open a discussion issue first.** Sector additions are discussed before PR.

## Required citation standard

- Minimum 2 sources per person record.
- One of: LittleSis OR a primary-source URL (official bio, Senate-confirmation record, court filing, official org page).
- Wikipedia counts as a secondary citation, not a primary. A record with Wikipedia + Wikipedia is rejected; Wikipedia + LittleSis is accepted; Wikipedia + official bio is accepted.
- For dead URLs: archive.org snapshot acceptable as the primary citation. Note `"type": "wayback"` in the source entry.
- **No citation = no record.** No exceptions for famous people. If you can't find sources for a famous person, the problem is your search, not the person's fame.

## What CI checks

Every PR runs:

1. **Citation audit** — each new person has ≥2 `sources`. Each new institution has ≥1.
2. **Duplicate-id scan** — ids are unique across people and institutions.
3. **Tag legality** — every `play`, `actor`, `network`, `admin`, `sector` value matches a name in the closed taxonomy (or, for the open values, an existing entry in `docs/PLAYS.md` / `docs/ACTORS.md` / etc.).
4. **Edge validity** — every edge endpoint exists as either a person or an institution id.
5. **Defamation policy lint** — `role` field is scanned for forbidden phrasing patterns (motive imputation, private-life reference, criminal-allegation language without citation). Heuristic, can be overridden with a maintainer review.

CI is fast (< 30 seconds). PRs that don't pass CI are not reviewed.

## What we do NOT accept

- Records based on tabloid reporting, conspiracy-blog speculation, or unverified social-media claims.
- Tag justifications that require unprovable motivation (e.g., "tagged with the `tap` actor because they probably knew about Stellar Wind").
- "Public figure, public consequences" arguments for removing the defamation policy. The policy is what makes the dataset citable; we keep it.
- Drive-by deletions. Removing a person requires the same documentation rigor as adding one.

## How to challenge an existing record

Open an issue with: the record id, the specific claim you dispute, and the primary-source URL that contradicts our current sourcing. The maintainer reviews and either: (a) updates the record with a new source, (b) removes the disputed claim, or (c) explains why the current sourcing stands. Issue resolution is public.

## License

MIT for the whole repo — code and data. See [LICENSE](../LICENSE).

By contributing, you agree your additions are submitted under MIT.
