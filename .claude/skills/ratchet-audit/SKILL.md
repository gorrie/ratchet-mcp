# Ratchet — Audit

Run the dataset audit (citation / defamation / vocabulary / structure)
and return a categorized report. Wrapper around
`server/tests/audit_citations.py` with a one-line invocation.

## TRIGGER when

- User asks to "audit," "check," "validate," or "lint" the Ratchet dataset
- Before any commit that modifies `server/data/*.jsonl`
- After bulk additions (cohort expansions, batch imports)

## SKIP

- General code linting (use repo's normal tooling)
- Bias study audits (different system, `bias-study-prep` skill)

## Steps

### Run the audit

```bash
cd "<workspace>/evil-robots-series/research/ratchet-mcp"
/c/Python314/python.exe server/tests/audit_citations.py
```

Exit 0 = pass, exit 1 = failures.

### Categorize the output

The script prints a "Top categories" header. Map each category to FIX or
FLAG:

| Category | Action |
|---|---|
| `person ... source(s)` (count <2) | FIX — backfill with primary source from priors |
| `person ... only Wikipedia` | FIX — add a non-Wikipedia source |
| `person ... characterization` (defamation) | FIX — rewrite role text to positions only |
| `person ... unsourced allegation` | FIX — rewrite role text or drop claim |
| `person ... private-life detail` | FIX — drop the detail |
| `person ... unknown <play\|actor\|sector\|admin> tag` | FIX — use a closed-vocab value or propose new |
| `edge ... not in dataset` | FIX — add the missing node or remove edge |
| `duplicate id` | FIX — rename with discriminator (e.g., `CPowell`) |
| `... malformed url` | FIX — repair URL |

Every category here is a FIX, not a FLAG. The audit catches things that
have unambiguous corrections.

### Backfill workflow (legacy single-source records)

The v2 import left most records with 1 source. Backfilling is per-record:

1. Pick the record. Read its current source URL.
2. Walk source priors to find a second primary source.
3. Append to `sources` array via the Edit tool (touching only the
   record's line in the JSONL).
4. Re-run audit. Verify that record no longer flags.
5. Commit batch-by-batch (10-20 records per commit) with a message like:
   `Ratchet: backfill 12 cabinet-Secretary records with LittleSis+gov-record sources`

### Pre-commit check

Add to local pre-commit, or run manually before every commit that
touches `server/data/`:

```bash
/c/Python314/python.exe server/tests/audit_citations.py || exit 1
```

CI will block on the same script.

## Hard rules

- Never relax the ≥2-source rule per record. The audit can be put in
  "legacy mode" for backfill scheduling, but the rule itself is fixed.
- Never silently introduce a new tag value to make the audit pass. Add
  it to the vocabulary in `audit_citations.py` + docs first, then add
  the record.
- The audit is run in CI on every PR. Local-pass and CI-fail means the
  data files diverged — confirm with `git status` before debugging.
