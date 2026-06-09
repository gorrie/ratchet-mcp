# Ratchet MCP — Control-Grid Actors Index

> **The mechanisms.** Each "actor" is a piece of the control-grid infrastructure — one of the 20 Ratchet clicks from the book, encoded as a queryable tag.

The actor set is a subset of the 20 Ratchet clicks (see [evilrobots.lol/tech/ratchet-clicks/](https://evilrobots.lol/tech/ratchet-clicks/)). We tag people with the actors their documented institutional positions touched.

To propose a new actor, see [CONTRIBUTING.md](CONTRIBUTING.md#how-to-add-a-new-actor).

## The 11 actors (v2 dataset)

| Code | Name | Ratchet click | Definition | Example person-touches |
|---|---|---|---|---|
| `flagging` | The Flagging Machine | Click 1 | Government-funded or coordinated content flagging that pressures platform takedowns. | Brennan (CIA-EIP era), Sullivan (NSC disinfo apparatus), Schmidt (DoD content-moderation working groups) |
| `algorithm` | The Algorithm | Click 2 | Engagement-optimizing platform algorithms that amplify outrage; AI-curation policy. | Schmidt (Google), Sandberg (Meta/Google), Hoffman (LinkedIn/Inflection), Suleyman (DeepMind→Microsoft AI), Khan (FTC algorithmic-amplification rulemaking), Gore (Apple board / Google) |
| `money` | The Money | Click 4 | Payment-system control: CBDC, sanctions, account freezing, programmable money infrastructure. | Mnuchin, Yellen, Lew, Geithner, Rubin, Paulson, Powell (Fed), Lagarde, Banga (Mastercard→WB), Fink (BlackRock), Dimon (JPMorgan) — most cabinet Treasury Secs and Fed Chairs |
| `papers` | The Papers | Click 5 | Digital identity systems, biometric enrollment, identity verification mandates. | Schmidt (NSCAI/digital ID), Banga (Mastercard/India Stack), Khan (FTC privacy), Sandberg (Meta ID systems), Schwab (WEF digital-ID advocacy) |
| `embassy` | The Embassy | Click 8 | Foreign government operations in US territory; US diplomatic / intel posture abroad. | Most State Dept and CIA chiefs (Kissinger, Albright, Powell, Rice, Clinton, Brennan, Hayden, Pompeo, Blinken, Rubio, etc.) |
| `eagle` | The Eagle | Click 9 | US extraterritorial enforcement — sanctions, military bases, USAID-conditioned programs. | Kissinger, Acheson, Dulles, Rusk, Rice, Albright, Powell, Clinton, Wolfowitz |
| `tap` | The Tap | Click 14 | SIGINT mass collection — NSA, GCHQ, Five Eyes, mass-metadata regimes. | Hayden, Brennan, Clapper, Tenet, Negroponte, William Burns (CIA), Gates, Cheney, Pompeo, Petraeus |
| `watchers` | The Watchers | Click 15 | Mass-metadata collection programs as distinct from targeted SIGINT — Section 215, Section 702, PRISM, Stellar Wind. | Cheney (architect), Hayden (operator), Clapper, Brennan, Petraeus, Karp (Palantir as contractor) |
| `backdoor` | The Backdoor | Click 16 | Encryption mandates, lawful-intercept requirements, client-side scanning. | Hayden (NSA, CALEA expansion), Cheney (PATRIOT Section 215), Bolton (encryption-backdoor advocacy as NSA) |
| `model` | The Model | Click 17 | Facial recognition deployment, biometric surveillance, identity-resolution products. | Karp (Palantir), Thiel (Palantir investor / founder), Schmidt (NSCAI on AI surveillance), Khan (FTC facial-rec rulemaking), Pompeo (CIA→State surveillance posture), Hassabis (DeepMind→Google Vision) |
| `blueprint` | The Blueprint | Click 18 | AI governance — registration requirements, compute thresholds, content watermarking mandates. | Schmidt (NSCAI chair), Khan (FTC AI rules), Andreessen (anti-regulation lobbying), Altman (Senate testimony / safety institute participation), Hassabis (DeepMind safety), Suleyman (Microsoft AI policy), Amodei (Anthropic safety-frontier policy), Hoffman, Schwab (WEF AI Action), Karp (Palantir / defense AI) |

## Multi-actor people (where the thesis lives)

The book's central observation is that control-grid mechanisms aren't operated by different people — they're operated by the *same* cohort, often touching multiple actors in one career. The MCP makes this checkable. From the v2 dataset:

- **Cheney**: `tap`, `watchers`, `backdoor`, `embassy` — 4 actors (the densest).
- **Hayden**: `tap`, `watchers`, `backdoor` — the SIGINT-and-mandate trifecta.
- **Schmidt**: `algorithm`, `model`, `blueprint`, `flagging` — the AI-policy quadrant.
- **Brennan**: `tap`, `watchers`, `flagging` — intel-to-platform-coordination bridge.
- **Khan**: `algorithm`, `blueprint`, `model` — the regulator side of the AI quadrant.
- **Sandberg**: `algorithm`, `flagging`, `papers` — the platform-side digital-ID trifecta.

`find_overlap(actors=["tap","backdoor"])` → Hayden, Cheney, Bolton (3 of 117). The headline prompt.

## What we explicitly chose to NOT model (yet)

The 20 Ratchet clicks include several that don't yet have a clean person-touches mapping in our dataset:

- `killswitch` (Click 3, infrastructure-level deplatforming): names like AWS leadership during the Parler decision are corporate-decision-level; would need separate sourcing.
- `club` (Click 6, elite invitation forums): partially covered by the `networks` dimension already.
- `priest` (Click 7, ESG / DEI compliance): names exist in our cohort (Fink → BlackRock ESG); not yet tagged.
- `car` / `office` / `school` / `hospital` (Clicks 10-13): vehicle / workplace / school / health surveillance. Industry-leader-level mapping needed.
- `counter` (Click 19) / `cat` (Click 20): structural / counter-argument clicks; not personnel-mapped.

v3 may add some of these. Each requires the same "≥2 exemplars" standard as new plays.

## How CI enforces consistent actor tagging

The tag-justification check in `tests/audit_citations.py`:

For each `actor` tag on each person:

1. Look at the person's edges (institutions they're documented at).
2. Look at the actor's documented institutions (the agencies / firms / programs known to operate that actor — e.g., `tap` → NSA, CIA, NCTC).
3. If the person's institutional edges don't include any of the actor's institutions AND the actor isn't justifiable from the role text, flag the tag.

The check is fuzzy at v2; tightens as the institution-to-actor lookup table grows.

## Cross-reference

- Plays are *patterns of person movement*. Actors are *mechanisms the people operate*. A person can execute a play (career pattern) without touching an actor (mechanism), and vice versa.
- The most informative `find_overlap` queries cross plays and actors: "who runs the Vault play AND touches the Money actor?" — the answer is almost every Treasury Secretary in the dataset, which is the point.
- Filter compositions: `query_cohort(play="pulpit", actor="embassy")` is nearly tautological (Pulpit people are by definition State-Dept people touching the embassy actor). The interesting queries are the *non*-tautologies: `play="pipeline", actor="model"` → which tech-pipeliners touch facial recognition? Returns Karp, Thiel, Schmidt, Hassabis.
