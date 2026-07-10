# texts.jsonl — the texts-by-person store

The graph half of this dataset profiles a person by their career/funding **topology**. This store is
the prose half: verbatim texts attributed to dataset persons, run through the Tradecraft TEXT lenses
(via the `grade_person_texts` MCP tool) to profile **how their own words operate** — per lens,
aggregated per subject, never blended, never a verdict.

## Schema (one JSON object per line)

```json
{"person_id": "Rubin", "id": "rubin-2008-oped", "text": "<verbatim text>", "url": "https://…", "date": "2008-09-15"}
```

| field       | required | meaning |
|-------------|----------|---------|
| `person_id` | yes      | must match an `id` in `people.jsonl` (e.g. `Rubin`, `Christiano`) |
| `text`      | yes      | the verbatim statement — the thing being graded |
| `id`        | no       | short text id; defaults to `person_id#N` |
| `url`       | no*      | the source (the receipt). Expected for anything load-bearing. |
| `date`      | no       | `YYYY-MM-DD`; enables the per-subject escalation timeline |

\* technically optional, but a text with no source is not evidence — include the URL.

## Rules

- **Real and sourced only.** This is an evidence store about real people. Never invent or paraphrase
  a quote into the store — verbatim text + a working source URL, or it does not belong here.
- **Attribution discipline.** The lane reports *what a text exhibits*, attributed to the text — it is
  not a finding about the person's character or motives. Keep it that way when you cite results.
- The store is empty by default; the tool returns a clear "no texts stored" note until populated.

## Engine

Grading lives in the sibling `tradecraft` package (the single source of truth for lenses + grader),
not here. The MCP tool imports it; for local dev set `TRADECRAFT_PATH` to the tradecraft repo root if
it is not pip-installed. Offline default backend is `cues` (deterministic, no key); pass `cloud` /
`local` / `auto` for the model read.
