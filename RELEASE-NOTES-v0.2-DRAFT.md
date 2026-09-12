# Ratchet MCP — v0.2 release notes (DRAFT — stage for publish)

> **Status: DRAFT.** Accumulate here until the v0.2 cut publishes via the `ratchet-mcp-publish`
> skill (`gh auth switch -u gorrie`, audit passing, tag + GitHub Release). Per author: the
> tooling-improvement writeup ships *with* the v0.2 update — keep this current as tooling lands.

## Dataset

- **+12 people, +15 institutions, +38 edges** — two Watching-the-Watchers wings:
  - **eval/statecraft wing** (+5): Zico Kolter (Gray Swan / OpenAI board), Beth Barnes (METR),
    Marius Hobbhahn (Apollo), Anna Makanju (OpenAI global affairs / ex-NSC), Juniper Downs
    (Google–YouTube → Airbnb content policy). (`scripts/add_wtw_eval_statecraft_wing.py`.)
  - **lab/policy wing** (+7): Jack Clark (Anthropic), Joanne Jang (OpenAI Model Spec), Jade Leung
    (GovAI → UK AISI CTO), Dan Hendrycks (CAIS), Paul Christiano (CAISI/NIST), Dave Willner
    (OpenAI first T&S), Chris Lehane (OpenAI global affairs). (`scripts/add_wtw_lab_policy_wing.py`.)
  Closed-vocab tags, positions-only role text, ≥2 sources each, both idempotent. Graph: 401→413 people,
  351→366 institutions, 844→882 edges.
- **+3 people, +10 institutions, +24 edges** — the **finance/funding layer** behind the apparatus
  (`scripts/add_wtw_finance_funding.py`). Adds the grantmakers (Open Philanthropy / Good Ventures,
  Schmidt Sciences, Survival and Flourishing Fund, Berkman Klein funders) and the funded evaluators/
  governance shops (CSET, FMF AI Safety Fund, ROOST), plus Kissinger's documented finance patronage
  (Rockefeller Brothers Fund, Kissinger Associates). This makes **finance → apparatus queryable as data,
  not prose**: e.g. METR (the frontier evaluator) is now visibly funded by Open Philanthropy, Schmidt
  Sciences, and SFF at once. Graph: 413→416 people, 366→376 institutions, 882→906 edges.
- **Full apparatus reconciliation** — every one of the 46 book/website apparatus profiles is now a
  graph node (not just the named wings), plus the AI-apparatus cohorts (OpenAI / Anthropic /
  Evaluators / Governance Shops). This is what closes the gap between the profiles and the graph.
- **Play rename `rumpelstiltskin` → `bretton`** (the IMF/World Bank → private-capital pipeline) for
  legibility and credibility — atomic across data, docs, web graph, tests.

**Final v0.2 dataset (verified 2026-07-04): 454 people · 388 institutions · 948 edges — every person
carries ≥2 sources (0 thin; CI source-gate green), 54/54 tests pass.**

## Tooling

- **`scripts/import_x_texts.py` — the x_ingest → texts-by-person bridge.** Reads the X-ingest output
  (gorrie `x_ingest.py`, twitterapi.io pay-per-use read backend), name-matches each subject to a
  `people.jsonl` label to resolve `person_id`, **drops retweets** (an `RT @…` is not the subject's own
  speech), dedupes by id, and only bridges people already in the graph. This is the missing PRODUCER
  for the texts-by-person lane: pulled speech in → `texts.jsonl` → `grade_person_texts` out.
- **Correctness gate (`x_ingest.py --verify`).** Before any post is attributed (or any handle
  published), a `user/info` call confirms the account's real name matches the expected subject —
  nickname-aware (`names_match`: Beth↔Elizabeth, Chris↔Christopher; surname must match). A wrong
  handle (a stranger's posts → the subject) is caught as both a correctness bug and a dox. 6/6
  apparatus handles verified OK.
- **Receipt verifier — the publish gate (`tradecraft/detect.verified_cue_receipts`,
  `texts.verified_person_receipts`).** Grading subjects' own posts on the offline `cues` floor produced
  per-document "method markers" that were mostly context-blind false positives — and some that fired on
  the *opposite* of the text's meaning (a subject *accusing others* of a "narrative"; an *anti*-
  centralization argument). Those are not publishable on named real people. The fix is a find→verify
  pipeline: `cues` finds candidates (recall), then a context-reading backend judges each
  **genuine / incidental / opposite** and keeps only `genuine`, defaulting to rejection. Live
  calibration (`tradecraft/eval/verify_eval.py`): **1 control kept, 7 documented real false positives
  dropped, 0 leaked**; 7 offline mocked-transport tests; full suite 108 passing. **Finding:** zero
  publishable in-context markers came out of the short-tweet sample — even the one that looked clean was
  a nuanced juxtaposition the verifier correctly dropped. Genuine markers live in **longform**, which is
  the empirical case for the monitoring backlog's RSS-first priority. (`eval/RESULTS-verify-2026-06-29.md`.)
- **OSINT-restraint standard (`docs/OSINT-RESTRAINT.md`).** A restrained Maltego: public,
  professional, verified social/affiliation only; a hard line against family, home, children/school,
  private contact, physical patterns, relatives-of. Governs every social-contact field. Profiles now
  carry a restrained "Public footprint" line (verified handle + the subject's own public bio link).
- **Grade loop proven + scaled — and it corroborates the profiles.** The x_ingest → bridge → grade
  loop now runs across the apparatus on subjects' **own posts** (RTs dropped). `texts.jsonl` 6 → **262**,
  **11 subjects graded**. Results match the hand-written archetypes, independently: Jack Clark (the
  "House Framer") → inevitability_framing **39.1** + institutional_permeation 32.9; Chris Lehane (the
  operative) → adept_speech; Dan Hendrycks → distributed_accountability 31.9; Joanne Jang →
  institutional_permeation; Alex Stamos → institutional_permeation / legibility. Per-lens, per-document,
  receipts only (each `doc_id` a real URL) — never blended, never a verdict.

## Calibration / methods

- **Tradecraft eval +2 high-confidence known-faction fixtures** (real, public, sourced): Marc Andreessen's
  Techno-Optimist Manifesto (accelerationist → inevitability_framing) and Sidney Webb's 1923 "inevitable
  gradualness" (Fabian → institutional_permeation). Both fire correctly at the offline `cues` floor.
  Suite: 19→21 fixtures, **11/11 positives fire, 5/5 negatives quiet, 11/11 marker coverage.** The lenses
  generalize from gold cue-probes to named known-faction text. (See `tradecraft/eval/RESULTS-2026-06-29.md`.)

## Provenance / discipline (unchanged, restated for the release)

- Texts are REAL and SOURCED (every entry carries a URL receipt); no invented quotes.
- Grading is per-lens with receipts, **never blended, never a verdict** — flag-and-show-the-receipt.
- Closed-vocab tags; positions-only `role`; no characterizations (anti-defamation discipline).

## Open / known gaps (carry forward)

- Local (Ollama abliterate) backend under-fires on varied prose; `cloud`/`auto` or the `cues` floor are
  the dependable paths. Two-pass local detection remains open.
- Newer subjects beyond the 5 above (and the rest of the verified X watchlist) still need pull → bridge →
  grade to populate their texts.
- Curated **search → top/controversial → capture** layer (text + screenshot card) is spec'd, not yet built.
- **Multi-platform read-only monitoring** is spec'd, not yet built (`gorrie/scripts/x/MONITORING-BACKLOG.md`).
  Priority RSS/Atom (longform → highest lens signal) → Mastodon → Bluesky → IG/FB on demand; each is a new
  ingest backend emitting the common record schema into the same bridge, with a per-platform handle gate.
  (Bluesky = monitoring subjects only, not our presence.)
- **Longitudinal political/method drift** (roadmap — HELD, author-confirmed 2026-06-29): the
  longitudinal extension of the per-profile **graded method-marker receipts** now landing on the
  evilrobots.lol profiles (top firing lens + verbatim quoted post + URL). Today each profile shows a
  *snapshot* of a subject's method markers; the drift report shows the same markers **moving over time**.
  `grade_person_texts` already returns a dated per-document timeline + per-lens `trend` — the same
  machinery as the AI bias-drift study, applied to a person. Pulling a subject's texts across a longer
  time span (the monitoring backlog's RSS/Mastodon/Bluesky backends supply the history) turns the flat
  `trend` into a measured drift (e.g. rising institutional_permeation across years). Sequence: per-profile
  snapshot markers (now) → historical multi-platform pulls (monitoring backlog) → drift report. Scaffolding
  is in place; build after the snapshot markers and the monitoring backends.
