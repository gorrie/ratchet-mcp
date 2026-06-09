# Ratchet — Add Person

Add a single named person to the Ratchet dataset with ≥2 primary sources,
correct closed-vocabulary tags, and audit passing before commit.

## TRIGGER when

- User asks to add a person to the Revolving Door / Ratchet dataset
- User says "add X to the map" / "include X" / "missing: X"
- v3 cohort expansion against [docs/SCOPE.md](../../docs/SCOPE.md) cohorts

## SKIP

- Wholesale cohort additions of >10 people in one shot (use the
  `ratchet-curator` agent for that — this skill is one-at-a-time)
- Institution additions (different format; manual edit for now)
- Edits to existing person records (manual; this skill is additive only)

## CRITICAL rules

1. **≥2 sources or no commit.** Hard rule. Walk the source priors in
   [docs/SCOPE.md](../../docs/SCOPE.md#source-priors) top-down until you
   have at least 2 primary sources. Wikipedia counts as secondary only —
   never the sole source.
2. **Positions only in `role`.** No "controversial," "hawkish," "alleged."
   See the defamation rules in [docs/CITATIONS.md](../../docs/CITATIONS.md#anti-defamation-discipline).
3. **Tags must be defensible.** Each `plays` and `actors` tag has to be
   justifiable from the documented institutional positions. If you can't
   justify it from the `role` text + edges, drop the tag.
4. **Anti-tinfoil rule.** Foundations as institutional actors IN.
   Bloodline-conspiracy framing OUT. If you can't cite a documented
   position (board seat, advisory role, employment), don't add the
   person.

## Steps

### 1. Research

Take the name. Walk source priors:

```
LittleSis -> Wikidata (P463 for memberships) -> Wikipedia -> Official site
-> Government records (Senate confirmation transcripts, FOIA releases)
-> Domhoff catalog (Who Rules America?) -> Bilderberg/Trilateral/WEF rosters
```

Hit at least 2 PRIMARY (non-Wikipedia) sources. Capture every URL.

### 2. Draft the record

Use the schema:

```jsonl
{"id":"ShortID","label":"Full Name","kind":"person",
 "sector":"tech|fin|gov|def|intel|cfr|tank|imf|multi|judiciary",
 "admin":["administration1","administration2"],
 "networks":["cfr","trilateral","bilderberg","wef","wef-ygl","pnac"],
 "plays":["vault","pulpit","cycle","acquisition","pipeline","backstop","cousin","rumpelstiltskin"],
 "actors":["flagging","algorithm","money","papers","embassy","eagle","tap","watchers","backdoor","model","blueprint"],
 "role":"Positions only, arrows between roles, no characterizations",
 "sources":[
   {"type":"littlesis","url":"https://littlesis.org/person/..."},
   {"type":"wikipedia","url":"https://en.wikipedia.org/wiki/..."}
 ]}
```

`id`: PascalCase, unique across people+institutions. Collisions: append
discriminator (`CPowell` for Colin Powell vs `Powell` for Jerome).

### 3. Identify institutional edges

For each documented position in `role`, find the corresponding institution
in `server/data/institutions.jsonl`. If the institution isn't in the
dataset and is load-bearing (>=2 persons will edge to it), add it first.
Otherwise drop the edge.

Append edges to `server/data/edges.jsonl`:

```jsonl
{"source":"ShortID","target":"InstitutionID"}
```

### 4. Append, audit, commit

```bash
cd "<workspace>/evil-robots-series/research/ratchet-mcp"
# Append draft record (manual edit or Python script).
/c/Python314/python.exe server/tests/audit_citations.py
```

If the audit fails on the new record: fix before commit. If the audit
fails on legacy records only: surface but don't block (legacy backfill
tracked separately).

### 5. Commit on the project repo

```bash
cd "<workspace>/evil-robots-series"
git add research/ratchet-mcp/server/data/people.jsonl \
        research/ratchet-mcp/server/data/edges.jsonl \
        research/ratchet-mcp/server/data/institutions.jsonl
git commit -m "Ratchet: add <Name> (sector/play tag rationale)"
```

(Once `github.com/gorrie/ratchet-mcp` exists, mirror commits there.)

## Closed vocabularies

- **plays**: vault, pulpit, cycle, acquisition, pipeline, backstop, cousin, rumpelstiltskin
- **actors**: flagging, algorithm, money, papers, embassy, eagle, tap, watchers, backdoor, model, blueprint
- **sectors**: gov, fin, imf, cfr, tank, intel, def, tech, multi, judiciary
- **networks**: cfr, trilateral, bilderberg, wef, wef-ygl, pnac, atlantic, rockefeller
- **admins**: truman, eisenhower, kennedy, johnson, nixon, ford, carter, reagan, bush1, clinton, bush2, obama, trump1, biden, trump2

A value outside these sets is a CI failure.

## When to propose a new vocabulary value

- A new `play` requires 3 documented exemplars + a one-paragraph
  definition. Open a PR against [docs/PLAYS.md](../../docs/PLAYS.md).
- A new `actor` mirrors one of the unmodelled Ratchet clicks
  (`killswitch`, `club`, `priest`, `car`, `office`, etc.). Same bar.
- A new `network`, `sector`, or `admin` value requires updating
  `audit_citations.py` and the docs in one PR.

Never silently introduce a new tag value — CI will block it.

## Hard rules

- No emojis in dataset records.
- IDs are PascalCase, unique, deterministic from the label.
- All `role` text is paraphrased from sources, not copied — but
  paraphrase must be factual, not editorialized.
- If the person is too obscure to cite from ≥2 primary sources, the
  person doesn't belong in the dataset yet.
