# Ratchet MCP — Staffing Plays Index

> **The named patterns.** Each "play" is a recurring personnel pattern across the dataset. The book's thesis is that these plays are operational, not coincidental — the same cohort runs each pattern repeatedly.

To add a new play, see [CONTRIBUTING.md](CONTRIBUTING.md#how-to-add-a-new-play). Minimum 3 documented exemplars per new play.

## The 8 plays (v2 dataset)

| Code | Name | Definition | Example exemplars |
|---|---|---|---|
| `vault` | The Vault | Wall Street → US Treasury → back to Wall Street. The financial-services revolver. | Rubin (Goldman→Treas→Citi), Paulson (Goldman→Treas→Paulson Institute), Geithner (NY Fed→Treas→Warburg Pincus), Mnuchin (Goldman/OneWest→Treas→Liberty Strategic), Bessent (Soros Fund→Treas) |
| `pulpit` | The Pulpit | CFR member → State Department → CFR President / think-tank seat. The foreign-policy revolver. | Kissinger (CFR→State→Kissinger Associates), Albright (CFR→State→Albright Stonebridge), Rice (CFR→State→Hoover), Clinton (CFR→State→speaking circuit), Haass (State Policy Planning→CFR Pres), Froman (USTR→Mastercard→CFR Pres) |
| `cycle` | The Cycle | Trilateral Commission membership → senior admin role → think-tank seat. The Trilateral Carter-era pattern named at its peak. | Brzezinski (Trilateral co-founder→NSA→CSIS), Vance (Trilateral→State→law firm), HBrown (Trilateral→Defense→Caltech), Blumenthal (Trilateral→Treasury→Burroughs), Volcker (Trilateral→Fed→Wolfensohn & Co) |
| `acquisition` | The Acquisition | Corporate CEO buys themselves a cabinet seat via campaign donation + advisory role. The "purchase a chair" pattern. | Paulson (Goldman CEO→Treas), Mnuchin (OneWest→Treas), Tillerson (ExxonMobil→State), Corzine (Goldman→Senate→NJ Gov), Bessent (Key Square→Treas), Andreessen (a16z→Trump tech advisor) |
| `pipeline` | The Pipeline | Tech executive → policy / regulator → tech executive. The Silicon Valley revolver. | Schmidt (Google→DoD NSCAI→Schmidt Futures), Sandberg (Treasury→Google→Meta), Hoffman (LinkedIn→OpenAI/Inflection investor→AI policy), Khan (Columbia→FTC→Columbia), Thiel (Palantir→Trump transition→Palantir), Altman (Y Combinator→OpenAI / Senate testimony) |
| `backstop` | The Backstop | Defense / military → defense contractor C-suite or governing-board → Defense. The "rule about not lobbying the agency you just left" worked-around. | Cheney (Defense→Halliburton CEO→VP), Mattis (CENTCOM→General Dynamics board→Defense), Austin (CENTCOM→Raytheon board→Defense), Esper (Raytheon VP→Defense), Petraeus (CENTCOM→CIA→KKR), Gates (Defense→boards→Texas A&M) |
| `cousin` | The Cousin | Sustained Bilderberg / WEF / Trilateral attendance while holding a senior US position. The supranational coordination pattern named for the genteel "we're all family" tone of those forums. | Kissinger, Rubin, Paulson, Rice, Clinton, Petraeus, Donilon, Dimon, Sandberg, Fink, Schmidt, Hoffman, Schwarzman, Soros, Schwab, Lagarde |
| `rumpelstiltskin` | The Rumpelstiltskin | IMF / World Bank pipeline → finance or regulator role. Named for the trick of taking value from the multilateral institutions and re-installing it in private capital. | Fischer (IMF→Citi→BoI→Fed→BlackRock), Lagarde (France Fin→IMF→ECB), Zoellick (USTR→State→WB→Goldman), Summers (WB→Treasury→D.E. Shaw), Banga (Citi→Mastercard→WB), Wolfensohn (Salomon→WB→consulting), Malpass (Treasury→Bear Stearns→WB) |

## When to use which tag

A person can carry multiple play tags — many of the 117 do. The dataset's filter dimensions are designed to make this useful:

- `query_cohort(play="vault", admin="clinton")` → who ran the Vault under Clinton? (Rubin, Summers, possibly others)
- `query_cohort(play="cousin", network="bilderberg")` → who's a Cousin via Bilderberg specifically? (overlap question)
- `find_overlap(plays=["vault","pulpit"])` → who runs both the financial AND foreign-policy revolvers? (cross-sector titans)

## The closed set rationale

These 8 plays were named to cover the patterns most visible in the dataset's v2 cohort. They are **descriptive**, not normative — naming a pattern doesn't claim the people executing it are bad actors. It claims the pattern is recurring and worth tracking.

A reader who looks at our dataset and sees a pattern we don't name should [propose a new play](CONTRIBUTING.md#how-to-add-a-new-play). Three exemplars + a one-paragraph definition is the entry cost.

## What we explicitly did NOT name as plays

- **"The Israel Lobby"** — exists as a published thesis (Mearsheimer & Walt) but doesn't translate cleanly into a staffing pattern across our criterion. People who fit lateral the pattern fit the existing tags (Trilateral / Bilderberg / CFR / WEF).
- **"Family dynasties"** (Bush, Clinton, Kennedy) — these are nepotism patterns, not staffing-play patterns. Out of scope for this project.
- **"The Deep State"** — too vague to operationalize. Specific plays subsume the useful parts (`tap`, `watchers`, `backdoor` on the actor side; `backstop`, `cousin` on the play side).
- **"The Tech Right"** — too recent and too small to fit our criterion. Maybe a v4 play if the pattern keeps repeating.

We name plays we can demonstrate. Patterns we can't demonstrate stay out.
