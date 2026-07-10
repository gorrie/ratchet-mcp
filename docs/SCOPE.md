# Ratchet MCP — Scope Policy

> **What goes in the graph. What doesn't. How we decide.**

This document is the authoritative scope policy for the Ratchet MCP dataset. It governs both the curated v2 set (~117 named people, expanding toward ~350) and every future contribution. The goal is a dataset that is **defensible against a hostile reviewer** — every record has a primary-source citation, every tag is justified by documented institutional positions, and the scope criterion can be applied mechanically.

## The single criterion: 2+ sectors

A named individual is in-scope **if and only if they have held a senior position in two or more of the 9 sectors defined below.** This is the actual revolving-door predicate. It is not a popularity contest, not a fame test, and not a normative judgment of the person. It is a structural test of the network the project is documenting.

> **Senior position** means: a confirmed appointment (Senate-confirmed or equivalent), a named C-suite or partner role at the institution, a documented governing-board seat, or a documented founding role. *Junior staff, interns, fellows, and one-off advisory-board members do not satisfy the criterion unless the role is itself documented as the person's primary engagement with the institution.*

If someone famously stayed in a single sector their whole career, they are out of scope — even if they're powerful. The Ratchet is about the **rotation**, not the rank.

## The 9 sectors

| Code | Sector | What counts as a senior position |
|---|---|---|
| `gov` | US Federal Executive | Cabinet, Sub-cabinet, NSC, White House Senior Staff, Fed Chair / Governor, NY Fed President, USTR |
| `def` | Defense / Military | Service Chiefs, JCS, Combatant Commanders, Service Secretaries; defense contractor C-suite or governing-board seat |
| `intel` | Intelligence | Director or Deputy of CIA / NSA / DNI / NCTC / FBI; NSC Senior Director with Intel portfolio |
| `fin` | Finance / Wall Street | C-suite, Partner, or governing-board seat at a major bank, asset manager, private-equity, hedge-fund, or insurance firm |
| `imf` | Multilateral / Bretton Woods | IMF MD or Deputy, World Bank President or VP, ECB / BIS / UN senior leadership |
| `cfr` | CFR-cluster networks | CFR / Trilateral / Bilderberg / WEF YGL — **note**: simple membership counts as a network tag (see below), but only Chair / President / Director-level role at the network's own organization counts as a sector position |
| `tank` | Think tanks / Academia | Think-tank President or named-chair Director; university Dean or Endowed Chair where the person's policy footprint is documented |
| `tech` | Tech / AI Industry | Founder / CEO / C-suite at frontier-AI labs, major platforms, defense-adjacent tech firms, or major VC funds. **Trust & Safety leadership** (platform T&S heads, content-policy VPs, chief legal officers when their portfolio includes T&S) is `tech` sector — same revolving-door criterion applies. **Senior platform "powermods"** who hold formal company roles (CEO, COO, head of community, named moderator-on-payroll) are in. Pseudonymous-only mods are out (cannot satisfy the source-citation standard). |
| `judiciary` | SCOTUS / Federal Judiciary | SCOTUS Justice; Circuit Court Judge with later cabinet / executive role; **notable SCOTUS clerks who later staffed senior executive or major-firm partner roles** (the clerk-to-power pipeline is itself the revolving door) |

The 9 sectors are **closed** — new sectors require a written argument that the existing 9 don't accommodate the pattern. SCOTUS was added 2026-05-28 because the clerk-to-power pipeline (Roberts, Kavanaugh, Barrett etc. cycled clerk → DOJ OLC / White House Counsel → judicial appointment) is its own coherent revolving door not captured by `gov` or `tank`.

## The historical-ideologues layer (sector `historical`)

Added 2026-06-04. A **separate scoped category** that sits alongside the 9 revolving-door sectors rather than inside them. It admits the intellectual **antecedents** of the control grid — the ideologues whose programs the institutions later operationalised — who do **not** satisfy the 2-sector revolving-door predicate (most never held a sector position at all) but whose founding and authorship roles are load-bearing to the thesis.

The layer's discipline is stricter, not looser:

- `sector: "historical"` is a **layer marker, not a 10th revolving-door sector.** It does not assert that the person rotated between sectors.
- A `brief` naming what the figure is the antecedent of, plus a `role` paraphrase of **documented public positions only** — same defamation lint as every other record.
- **≥2 primary sources, never Wikipedia-only** (Wikipedia + one official or academic source).
- **No `plays` / `actors` tags.** These figures predate the 20 control-grid actors; the *institutions* they founded carry the operational edges, not the people. This keeps the layer out of motive-imputation: we record that Galton coined "eugenics," not that he "caused" any later policy.
- Edges run person → the institution they founded or led.

Initial set (11 persons): **Francis Galton** (Eugenics Society); **George Bernard Shaw, Sidney Webb, Beatrice Webb, H. G. Wells** (Fabian Society / LSE); **Cecil Rhodes, Alfred Milner** (Rhodes Trust / Round Table); **Carroll Quigley** (Georgetown — the historian who documented the Rhodes–Milner network from inside the academy); **Ludwig von Mises, Friedrich Hayek** (Mont Pelerin Society); **Lyndon LaRouche** (Schiller Institute).

The anti-tinfoil rule (below) still governs: institutions are the artifact, bloodlines are not, and no edge asserts a *direction* of influence. The layer documents who founded what and who wrote what — nothing more. The CI audit (`server/tests/audit_citations.py`) accepts `historical` as a valid sector value as of 2026-06-04.

## The 5 dimensions

Each person record carries five dimension arrays. **The dimensions are closed; the values are open** (new values land via PR — see CONTRIBUTING.md).

| Dim | Field | Example values |
|---|---|---|
| Sector | `sector` (single) | one of the 9 above |
| Administration(s) served | `admin` (array) | `roosevelt`, `truman`, ..., `trump2`. Any admin in which the person held a sector-relevant position. |
| Network membership | `networks` (array) | `cfr` (CFR member), `trilateral`, `bilderberg`, `wef-ygl`, `aei`, `pnac`, etc. |
| Staffing play | `plays` (array) | `vault`, `pulpit`, `cycle`, `acquisition`, `pipeline`, `backstop`, `cousin`, `bretton` (see PROMPTS.md for definitions) |
| Control-grid actor touched | `actors` (array) | `flagging`, `algorithm`, `money`, `papers`, `tap`, `watchers`, `backdoor`, `model`, `blueprint`, `embassy`, `eagle` (subset of the 20 ratchet clicks) |

## Source priors (where the data comes from)

In priority order — when curating a new record, walk this list top-down and stop when you have ≥2 primary sources.

1. **LittleSis** ([littlesis.org](https://littlesis.org/)) — Public Accountability Initiative's open influence-network database. Hand-curated. Use it to cross-check relationship-level claims (X served on Y's board) and cite the specific record URL.
2. **Wikidata SPARQL** — `P463` (member of) queries against Q-IDs for CFR / Trilateral / Bilderberg / WEF YGL produce bulk roster pulls. Free, no auth.
3. **Domhoff,** *Who Rules America?* — UC Santa Cruz academic catalog of CFR / government / corporate-board personnel overlaps. Decades of citation depth.
4. **Bilderberg meetings** — annual attendee lists published by [bilderbergmeetings.org](https://bilderbergmeetings.org/meetings.html).
5. **Trilateral Commission** — annual rosters at [trilateral.org](https://trilateral.org/).
6. **WEF Young Global Leaders** alumni directory — [younggloballeaders.org/community](https://www.younggloballeaders.org/community).
7. **Official cabinet rosters** — White House archive, State Dept historian, Treasury historian, etc.
8. **OpenSecrets Revolving Door** ([opensecrets.org/revolving-door](https://www.opensecrets.org/revolving-door)) — for Congress-to-lobbying patterns.
9. **Contemporary news** — only for confirmation of a specific transition; never as the sole source for a person's inclusion.

## Cohorts the v2 dataset under-covers (v3 expansion targets)

The author flagged these specifically because they're under-represented in v2 and have outsized real-world impact. **They are in-scope**; v3 should bring them in at parity with the existing cohorts.

Author framing 2026-05-28/29: the trust-and-safety / platform-moderation / "powermod" world is best understood as **an offshoot of the legal-control grid** — not a parallel cohort. So Cohort A below is the umbrella; T&S leadership (A.1), the T&S industrial complex (A.2), and platform powermods (A.3) are sub-patterns under it.

### A. The legal control grid + its offshoots

The advocacy, academic, NGO, and platform-side infrastructure that operates content-moderation, takedown demands, and regulatory framing — and the personnel that rotates between them and government. Touches the `flagging`, `algorithm`, `model`, `blueprint` actors heavily.

#### A.1 — Trust & Safety leadership (`tech` sector)

Platform employees who run T&S directly. Documented revolving-door pattern: government / intel → platform T&S → academic content-moderation tank → consulting → back to platform.

v3 candidates (named senior roles only):

- **Yoel Roth** — Twitter Head of Trust & Safety 2020-22 → UPenn / academic.
- **Vijaya Gadde** — Twitter Chief Legal Officer 2011-22 (T&S portfolio).
- **Del Harvey** — Twitter VP Trust & Safety 2008-21.
- **Monika Bickert** — Meta VP Content Policy. Previously DOJ federal prosecutor (`gov` → `tech` Vault-shaped move).
- **Joel Kaplan** — Meta VP Global Public Policy. Previously Bush II Deputy Chief of Staff (`gov` → `tech` pipeline).
- **Brian Fishman** — Meta Counter-Terrorism Policy lead. Previously Combating Terrorism Center at West Point.
- **Susan Wojcicki** — YouTube CEO 2014-23.
- **Neal Mohan** — YouTube CEO 2023-.
- **Adam Mosseri** — Instagram Head.

#### A.2 — Trust-and-safety industrial complex (`tank` sector)

NGOs, academic institutes, and quasi-governmental coordination bodies that operate the content-flagging infrastructure between government and platforms. Touches `flagging` heavily.

v3 candidate institutions:

- **Stanford Internet Observatory** (SIO) — founded 2019; folded its content-moderation program 2024 under political pressure.
- **Election Integrity Partnership** (EIP) — Stanford SIO + UW CIP + Atlantic Council DFRLab + Graphika.
- **Atlantic Council DFRLab** — disinformation tracking, gov-funded.
- **Global Disinformation Index** (GDI).
- **NewsGuard**.
- **Graphika** — network-analysis firm; documented NDA work with government clients.
- **University of Washington Center for an Informed Public** (CIP).
- **Aspen Institute Commission on Information Disorder**.
- **Trusted News Initiative** (BBC-coordinated).
- **ADL Center for Technology and Society**.
- **Center for Countering Digital Hate** (CCDH).

v3 candidate persons:

- **Alex Stamos** — Facebook Chief Security Officer → SIO founder → Krebs Stamos Group.
- **Renée DiResta** — SIO Research Manager → New America Fellow.
- **Kate Starbird** — UW CIP director, EIP co-author.
- **Graham Brookie** — Atlantic Council DFRLab.
- **Steven Brill** + **Gordon Crovitz** — NewsGuard co-founders.
- **Vivian Schiller** — Aspen Digital director.
- **Jonathan Greenblatt** — ADL CEO, ex-Obama administration.
- **Imran Ahmed** — CCDH founder.

#### A.3 — Platform powermods (`tech` sector, named-only)

Per author 2026-05-29: "the powermod types have been a real problem." This sub-cohort is included as a specifically-flagged offshoot of the legal control grid.

**The rule**: pseudonymous-only moderators are OUT (the source-citation standard cannot be satisfied for an anonymous account; we cannot publish "we suspect X is /u/Y"). **Named persons who hold formal company roles** — CEO, Head of Community, Head of Moderation, named paid-moderator-on-payroll, product-team lead with moderation portfolio — are IN.

v3 candidate persons:

- **Steve Huffman** (Reddit CEO; designer of subreddit-quarantine system).
- **Alexis Ohanian** (Reddit co-founder, board).
- Discord T&S leadership (named officers per their corporate disclosures).
- Twitch Community team (named officers).
- **Maria Ressa** (Rappler founder; co-author of academic content-mod papers).

Pseudonymous mod accounts that have been reported on in journalism (the various "supermod" Reddit accounts repeatedly named in 2020-2023 coverage of Reddit moderation concentration) are **deliberately not listed by handle** in this dataset. If an account is identified by mainstream reporting as belonging to a named person who holds a formal role, that person enters under their real name with the role-relevant citations.

### B. Gamergate-era journalists + entertainment-gatekeeper apparatus (`tank` sector, `tech`-adjacent)

Author flagged 2026-05-29: this cohort is in-scope. They sit at the intersection of legacy game-industry journalism, content-policy advocacy, and the academic-content-mod NGO world — and their 2014-era coverage of online communities is a documented input into the platform-side moderation policies that crystallized 2015-2020. Companion to the `Lurk More` book (Fires Series Book 3, already published with full sourcing).

**Discipline note**: the same defamation rules in CITATIONS.md apply. We record **published editorial positions and documented institutional affiliations only** — never characterizations, never private-life material, never speculation about motive. The role text says what someone wrote and where they worked; nothing else.

v3 candidate persons (named with public editorial roles; sourcing per the standard):

- **Anita Sarkeesian** — Feminist Frequency founder; ConnectSafely board member; Crash Override Network co-founder; UN consultations.
- **Zoe Quinn** — Crash Override Network co-founder; UN consultant on online harassment.
- **Brianna Wu** — Giant Spacekat founder; 2018/2020 House candidate (MA-08); Spacekat / Rebellion PAC roles.
- **Leigh Alexander** — Gamasutra editor; Hyperallergic; Tribeca Film Institute roles.
- **Stephen Totilo** — Kotaku editor-in-chief 2012-20 → Axios games reporter.
- **Patrick Klepek** — Kotaku → Vice → Waypoint.
- **Jason Schreier** — Kotaku → Bloomberg.
- **Ben Kuchera** — Polygon; Ars Technica.
- **Brad Wardell** (Stardock CEO; counter-cohort, included because the sector-crossing is symmetric — he held tech founder + game-industry editorial-target positions).

Each record will paraphrase published bylines + documented institutional roles only. The book *Lurk More* handles the contextual framing; the dataset's job is to document the positions, not the disputes.

### C. Hollywood / entertainment-industry gatekeepers (`tank` sector) — **MAYBE / soft inclusion**

Author flagged 2026-05-29 with explicit "maybe anyway" caveat. Soft inclusion: candidates listed below but v3 work prioritizes A and B first.

The pattern of interest: studio executives + MPAA / industry-trade-org leadership + agencies who control casting / distribution / streaming-curation — i.e., the cultural-narrative gatekeeping layer that runs parallel to the content-moderation gatekeeping layer.

Tentative v3 candidates (named, formal positions only):

- Major studio CEOs (Bob Iger / Disney, David Zaslav / WBD, Ted Sarandos / Netflix, Tim Cook / Apple TV+ portfolio).
- MPAA chair lineage (Chris Dodd, Charles Rivkin — both `gov` → `tank` revolving-door cases).
- WGA / DGA / SAG-AFTRA leadership where they crossed into government or platform-policy roles.
- Spotify / streaming-curation leads (Daniel Ek and direct reports).

The sector-crossing is real for some of these (Dodd: Senator → MPAA; Rivkin: ambassador → MPAA; Sarandos: tech-adjacent). Others are pure entertainment-only and would fail the 2-sector test. Curation needed.

---

Combined A + B + C expansion would add ~50-60 named persons to v3. The 2-sector criterion does most of the filtering automatically; the citation-and-tag-justification discipline does the rest.

### D. BigLaw + private-intel firms (`tank` sector + `intel`/`gov` overlap)

Author flagged 2026-05-29: "the perkins coie with the uk spies stuff was pretty wild as well. that should likely be covered too unless too low level."

It's not too low level. The DOJ-to-BigLaw rotation (Justice Dept attorneys → law-firm partner → back to senior gov role) is a sustained documented pattern, and the law firms themselves serve as the operational substrate for elite political-legal coordination. The Perkins Coie / Fusion GPS / Steele dossier matter is in the public record (Sussmann indictment + acquittal court records, Durham Report); it's appropriate dataset material under the same standard as everything else: positions and documented court facts only, never characterizations.

v3 candidate institutions:

- **Sullivan & Cromwell** — the firm that produced John Foster Dulles, Allen Dulles (CIA), and a continuous Wall Street ↔ State pipeline since the 1920s.
- **Perkins Coie** — Democratic Party general counsel firm; documented role in 2016 cycle (Fusion GPS engagement) per court records.
- **Skadden, Arps** — Greg Craig (Obama WH Counsel) tenure documented; subject to Mueller-era foreign-lobbying scrutiny.
- **Covington & Burling** — Eric Holder, Lanny Breuer, Loretta Lynch all rotated through; "Project Chickenshit" memo coverage documented.
- **Williams & Connolly** — DC trial-bar establishment; multiple administration counsel roles.
- **Kirkland & Ellis** — Rod Rosenstein, William Barr revolving rotations.
- **Baker Botts / Baker Hostetler** — Bush-family-adjacent rotation.
- **WilmerHale** — Robert Mueller post-FBI; Jamie Gorelick.

v3 candidate persons:

- **Marc Elias** — Perkins Coie partner (Democratic campaigns counsel) → Democracy Docket founder. Touches `flagging`-adjacent + `gov` campaign-counsel.
- **Michael Sussmann** — Perkins Coie partner; ex-DOJ Computer Crime Section. Indicted 2021 (acquitted 2022) per public court record.
- **Robert Mueller** — DOJ → WilmerHale → FBI Director → WilmerHale → Special Counsel. Multi-rotation. Touches `tap`, `embassy`.
- **Greg Craig** — Skadden → Obama WH Counsel → Skadden. Foreign-lobbying scrutiny documented.
- **Eric Holder** — Covington → DOJ AG → Covington. Touches `embassy`, `flagging`.
- **William Barr** — Kirkland & Ellis → AG (Bush I) → Kirkland → AG (Trump I) → Kirkland.

#### D.1 — Private-intel firms (UK-spies + Crossfire Hurricane orbit)

Western-allied private intelligence firms staffed by former MI6 / FBI / NSA / CIA officers. The "former spy" → "private intelligence consultancy" → "DC law firm client" pipeline is documented. Touches `tap`-adjacent.

v3 candidate institutions:

- **Orbis Business Intelligence** — Christopher Steele's firm. Subject of UK court proceedings (Gubarev v. Steele, Trump v. Steele) which are public record.
- **Hakluyt & Co.** — UK private-intel boutique, ex-MI6 staffed.
- **Fusion GPS** — Glenn Simpson + Peter Fritsch's opposition-research firm. Sussmann trial + Senate Judiciary materials documented their commercial engagements.
- **Black Cube** — Israeli private-intel firm (relevant where US-cabinet engagements have been documented in court).
- **GS Investigative Group**, **Kroll**, **Mintz Group**, **K2 Intelligence** — major US private-intel firms with named ex-government partners.

v3 candidate persons (named ex-officials with private-intel firm leadership):

- **Christopher Steele** — UK MI6 (retired) → Orbis founder. UK court record makes the institutional positions citable.
- **Glenn Simpson** — WSJ reporter → Fusion GPS co-founder.
- **Peter Fritsch** — WSJ reporter → Fusion GPS co-founder.
- **Daniel Jones** — Senate Intelligence Committee staff → Penn Quarter Group (private-intel firm contracted by Fusion GPS per court filings).

Inclusion criterion is the same as all other cohorts: 2-sector test (most pass via gov/intel → tank/private-intel pipeline) + ≥2 primary-source URLs per record. UK-court records and US Senate hearing transcripts are primary sources of the highest quality.

---

## What we explicitly do NOT cover (anti-tinfoil)

Author 2026-05-29: "do we want to get into tinfoil areas like the rothchilds? when we talk about the foundations, and institutions, that's likely close enough."

**The institutions are the artifact. The bloodlines are not.**

- **Foundations + institutions as documented actors**: IN. Rockefeller Foundation, Carnegie Endowment, Ford Foundation, Open Society Foundations, Gates Foundation — these have published trustees, published grants, published positions. Track them as institutions; track their CEOs / presidents / chairs as people; cite their public records.
- **Bloodline / family-conspiracy framing as a thesis**: OUT. "The Rothschilds control X" is not a citable institutional claim; it's a familial designation that has no operational meaning at the dataset level. Even if individual members of historically prominent families hold sector positions (and some do — David Rockefeller is already in the v2 dataset for his **documented** roles at Chase, Trilateral, CFR), they're recorded **as individuals** with their documented positions, not as "members of family X."

This rule keeps us out of three failure modes:

1. **Defamation** — naming "the Rothschild family" as a malign actor risks libel against living family members who hold no operational positions. Naming Lord Jacob Rothschild as RIT Capital chair (his actual documented role) is fine.
2. **Anti-Semitic shorthand** — historically the bloodline-conspiracy frame was the carrier wave for anti-Jewish defamation; the institutional frame is operational, not ethnic, and is the only one we publish under.
3. **Credibility decay** — the dataset's defensibility depends on never crossing into unfalsifiable territory. The "institutions" frame is falsifiable (cite a position or remove the claim); the "bloodlines" frame is not.

Same rule applies to other family-named conspiracy frames: **DuPont**, **Bush**, **Clinton**, **Kennedy**, **Saud**, **Wallenberg**, etc. Individual family members enter on their documented positions if they pass the 2-sector test (multiple Bushes do; some DuPonts do); the family-as-actor framing is rejected.

## Cohort F — Foreign-aligned institutional influence (institutional-only)

**Author 2026-05-29**: "we can't do china and russia [named persons], but maybe we can have some ability to show their influence."

The Ratchet is global; an exclusively US-personnel dataset is provincial. But naming Chinese or Russian individuals invites two equally bad failure modes: (a) defamation against private foreign citizens with no recourse to US courts, and (b) drift into bloodline / regime / generic "they-control-X" conspiracy framing that destroys the dataset's defensibility.

**The solution: institutional-only for high-risk jurisdictions, influence shown via documented-engagement edges from the existing primary cohort.**

In scope as **institutions** (no person edges originating inside these jurisdictions):

- **China-state** (sector `china-state`): PBoC, Boao Forum for Asia, China Development Forum, Tsinghua University, AIIB, NDB (BRICS Bank), Belt and Road Initiative, CCP United Front Work Department, China Investment Corporation, CIDCA.
- **Russia-state** (sector `russia-state`): St. Petersburg International Economic Forum (SPIEF), Valdai Discussion Club, Russian Direct Investment Fund (RDIF), GRU, SVR, FSB.

Edges into these institutions come **only from the existing US/allied cohort** and must be backed by Wikipedia-grade documentation (program founder, repeat keynote speaker, multilateral-coordination role, named advisory board member). Examples that pass the bar:

- Schwarzman → Tsinghua (founded Schwarzman Scholars at Tsinghua, 2013 — NYT, Schwarzman Scholars official site).
- Paulson → Tsinghua (Paulson Institute partnered with Tsinghua's PBC School of Finance — Paulson Institute publications).
- Kissinger → Boao Forum / Valdai (repeat documented keynote attendance — multiple news primary sources).
- Schwab → BRI (WEF-published endorsements of Belt and Road cooperation).

Edges into Cohort F record the **engagement, not allegiance**. Tagged with optional `influence_type` metadata (`program_founder`, `documented_attendance`, `advisory`, `multilateral_coordination`, `business_relationship`) so the web viewer can dim or highlight by edge category. The MCP server treats them as ordinary adjacencies.

**What this gives the dataset**: when a user filters by `sector: china-state`, a cluster of foreign-state institutional nodes lights up, with edges fanning back into Wall Street, the White House, and Western academia. The thesis is visible without us naming a single foreign citizen.

**What stays out under this cohort**:

- Named Chinese / Russian persons. No Xi, no Putin, no Zhou Xiaochuan, no Igor Shuvalov, no Jack Ma. Period. Even ones with WEF or Bilderberg attendance — the defamation exposure isn't worth it, and the institutional cluster carries the influence claim better than any named person would.
- Edges asserting *direction* of influence ("X is a CCP asset," "Y is FSB-linked"). All edges are documented engagement only; readers can interpret directionality from the totality.
- Speculative or pseudonymous foreign actors (named "former intelligence officers" without an attached firm + court-record or news-record citation).

This cohort can be expanded to **other allied-foreign individuals** (UK, EU, Five Eyes, Israel, India, Switzerland) where the same defamation calculus is more favorable — those persons can be **named** because (a) they hold publicly-documented positions per the same rules as US cohort, (b) they have full recourse to courts under their own legal system, and (c) the political-conspiracy-framing risk is lower. The China/Russia bifurcation applies specifically to the two jurisdictions where the named-individual approach would invite both defamation and conspiracy-shorthand failure modes simultaneously.

## Out of scope

- **Foreign heads of state without US cabinet / multilateral crossover.** This is a US-centric revolving-door dataset by design. A French politician who attended Davos but never held a sector position outside France: out.
- **Pure media figures.** Network television hosts, newspaper editors, columnists. Their influence is real but it doesn't satisfy the 2-sector test. Exception: media executives who serve on think-tank or corporate boards (then they're `tech` or `tank`).
- **Junior staff / fellows / interns / one-off advisors.** Even if they later became famous. The record starts when they hit a senior position.
- **Private-life claims, motivation imputations, unindicted-allegation reporting.** This is a documented-positions dataset. The 117 entries are public-record. Nothing about who someone slept with, owed, or feared.
- **Living vs deceased makes no difference** — defamation safety is the test, not biological status. Same standard applies.

## Defamation safety

The whole dataset is published with the assumption that **every named person can sue and we should welcome it.** The discipline that protects against that:

1. Every record's `role` field is **a paraphrase of publicly-documented institutional positions only.** No characterizations of motive, integrity, loyalty, or private behavior. The record describes *what role they held*, not *who they are*.
2. Every record carries `sources: [...]` with ≥1 primary-source URL. CI rejects PRs missing this.
3. Tag justification: each `plays` or `actors` tag must be supportable by the documented positions. If a tag would only make sense given an unproven motivation, drop the tag.
4. **No criminal allegations cited** unless they are documented convictions or settled civil matters with a court reference. Pending allegations: out.
5. **Audit log:** each contribution lands as its own commit with its source-checks visible in the diff. If a claim is wrong, the commit can be reverted; the source-of-truth blame is mechanical.

## Target dataset size

v2 (current): 117 people, 61 institutions, 338 transitions.

v3 (next pass, "reasonable enough" per author): **~350 people** across all 9 sectors. Per the criterion + source priors, this is achievable from:

- Full Bilderberg attendee history (~1,600 unique attendees since 1954; ~300 satisfy 2-sector test)
- Full Trilateral Commission roster (~400 historical; ~150 satisfy)
- WEF Young Global Leaders cumulative (~1,400; ~80 satisfy)
- Cabinet members Truman → present (~500; nearly all satisfy)
- SCOTUS Justices + notable clerk-pipeline alumni (~120; ~60 satisfy)
- Federal Reserve Board Governors (~80; ~40 satisfy)
- IMF MDs + World Bank Presidents + senior leadership (~60; ~30 satisfy)

The 350 target is reached by the union of these source pulls, deduplicated. No single source dominates; coverage is checked against the others.

v4 and beyond: **community-driven via PR** (CONTRIBUTING.md). The maintainer's job becomes review, not curation.
