# Ratchet Dataset — Discovered Groupings

Snapshot of 385 persons / 319 institutions / 823 edges.

Mechanical analyses below; cross-reference against clusters.json (named human-curated clusters) and SCOPE.md (cohort definitions).


## 1. Centrality — most-connected persons and institutions

### Most-connected persons (top 25)

| Person | Edge count | Sector | Plays | Actors |
|---|---|---|---|---|
| `Kissinger` (Henry Kissinger) | 10 | gov | pulpit,cycle,cousin | embassy,eagle |
| `Summers` (Larry Summers) | 9 | gov | rumpelstiltskin,vault | money |
| `Paulson` (Hank Paulson) | 8 | fin | vault,acquisition,cousin | money |
| `Carney` (Mark Carney) | 8 | gov | rumpelstiltskin,cousin | money,priest |
| `Zoellick` (Robert Zoellick) | 7 | imf | rumpelstiltskin | money,embassy |
| `Rice` (Condoleezza Rice) | 6 | gov | pulpit,cousin | embassy,eagle |
| `Fischer` (Stanley Fischer) | 6 | imf | rumpelstiltskin,vault | money |
| `Schmidt` (Eric Schmidt) | 6 | tech | pipeline,cousin | algorithm,model,blueprint,flagging |
| `Rubin` (Robert Rubin) | 5 | fin | vault,cousin | money |
| `Geithner` (Timothy Geithner) | 5 | gov | vault | money |
| `Shultz` (George Shultz) | 5 | gov | pulpit,cousin | money,embassy |
| `Baker` (James Baker) | 5 | gov | pulpit | money,embassy |
| `Wolfowitz` (Paul Wolfowitz) | 5 | gov | rumpelstiltskin | embassy,eagle |
| `Fink` (Larry Fink) | 5 | fin | cousin | money,priest |
| `Volcker` (Paul Volcker) | 5 | gov | cycle | money |
| `Lagarde` (Christine Lagarde) | 5 | imf | rumpelstiltskin,cousin | money |
| `Donilon` (Tom Donilon) | 5 | gov | vault,cousin | embassy,flagging |
| `Bolton` (John Bolton) | 5 | gov | pulpit | embassy,backdoor |
| `Sandberg` (Sheryl Sandberg) | 5 | tech | pipeline,vault,cousin | algorithm,flagging,papers |
| `Musk` (Elon Musk) | 5 | tech | acquisition,pipeline | algorithm,blueprint |
| `Yellen` (Janet Yellen) | 4 | gov | vault | money,priest |
| `Haig` (Alexander Haig) | 4 | gov | pulpit | embassy |
| `CPowell` (Colin Powell) | 4 | gov | pulpit | embassy,eagle |
| `Blinken` (Antony Blinken) | 4 | gov | pulpit | embassy,flagging |
| `Cheney` (Dick Cheney) | 4 | gov | backstop | tap,watchers,backdoor,embassy |

### Most-connected institutions (top 25)

| Institution | Person edges | Sector |
|---|---|---|
| `CFR` (CFR) | 85 | cfr |
| `State` (State Dept) | 40 | gov |
| `WhiteHouse` (White House) | 35 | gov |
| `NSC` (NSC) | 27 | gov |
| `DoD` (DoD) | 25 | def |
| `Bilderberg` (Bilderberg) | 22 | cfr |
| `Treasury` (US Treasury) | 21 | gov |
| `WEF` (WEF) | 18 | cfr |
| `Senate` (US Senate) | 17 | gov |
| `CIA` (CIA) | 16 | intel |
| `UN` (UN) | 14 | imf |
| `Goldman` (Goldman Sachs) | 12 | fin |
| `FedReserve` (Federal Reserve) | 12 | gov |
| `FederalistSociety` (Federalist Society) | 12 | tank |
| `Trilateral` (Trilateral Comm.) | 11 | cfr |
| `WorldBank` (World Bank) | 10 | imf |
| `Google` (Google / Alphabet) | 10 | tech |
| `Meta` (Meta) | 9 | tech |
| `X_Corp` (X Corp (formerly Twitter)) | 9 | tech |
| `SCOTUS` (Supreme Court of the United States) | 9 | judiciary |
| `Citigroup` (Citigroup) | 8 | fin |
| `IMF` (IMF) | 7 | imf |
| `OpenAI` (OpenAI) | 7 | tech |
| `UKGov` (UK Government) | 7 | gov |
| `CDF` (China Development Forum) | 6 | china-state |

## 2. Co-occurrence — which plays / actors / networks travel together

### Plays that co-occur (>= 3 persons hold both)

| Play A | Play B | Persons with both |
|---|---|---|
| cousin | vault | 5 |
| cousin | pulpit | 5 |
| cousin | pipeline | 5 |
| acquisition | pipeline | 5 |
| acquisition | vault | 4 |
| cycle | pulpit | 4 |
| cousin | rumpelstiltskin | 4 |
| rumpelstiltskin | vault | 3 |
| backstop | pulpit | 3 |

### Actors that co-occur (>= 3 persons touch both)

| Actor A | Actor B | Persons touching both |
|---|---|---|
| tap | watchers | 18 |
| eagle | embassy | 13 |
| embassy | tap | 11 |
| algorithm | flagging | 10 |
| algorithm | blueprint | 9 |
| backdoor | tap | 6 |
| embassy | money | 5 |
| embassy | flagging | 5 |
| backdoor | watchers | 5 |
| blueprint | model | 5 |
| flagging | tap | 4 |
| money | priest | 3 |
| algorithm | model | 3 |
| blueprint | flagging | 3 |
| model | papers | 3 |

### Networks that co-occur (>= 3 persons hold both memberships)

| Network A | Network B | Members of both |
|---|---|---|
| bilderberg | cfr | 12 |
| cfr | trilateral | 10 |
| bilderberg | wef-ygl | 5 |
| cfr | wef-ygl | 4 |
| bilderberg | trilateral | 3 |
| aei | cfr | 3 |

## 3. Surprise overlaps — 2-attribute combinations yielding 3-15 person cohorts

Small cohorts are thesis-sharp. These are the unexpected ones — small named-pattern intersections that suggest an unnamed cluster worth investigating.

### Play x Actor intersections

| Play | Actor | Persons | Names |
|---|---|---|---|
| backstop | watchers | 3 | Cheney, Petraeus, KAlexander |
| cousin | flagging | 3 | Schmidt, Donilon, Sandberg |
| cycle | eagle | 3 | Kissinger, Brzezinski, Hills |
| pulpit | flagging | 3 | Blinken, JSullivan, SPower |
| pulpit | money | 3 | Shultz, Baker, Froman |
| pulpit | tap | 3 | Pompeo, WBurns, Negroponte |
| acquisition | blueprint | 4 | Andreessen, Musk, Warner, PLuckey |
| cousin | blueprint | 4 | Schmidt, Hoffman, Altman, Schwab |
| cousin | eagle | 4 | Kissinger, Rice, Clinton, Dulles |
| cycle | money | 4 | Volcker, Blumenthal, DRockefeller, Burns |
| backstop | tap | 5 | Cheney, Petraeus, Gates, KAlexander, Mueller |
| cousin | algorithm | 5 | Clinton, Schmidt, Gore, Hoffman, Sandberg |
| pipeline | hospital | 5 | RShah, Farrar, Hatchett, Dybul, Slaoui |
| acquisition | money | 7 | Paulson, Mnuchin, Bessent, ORneill, Snow, Corzine, Lutnick |
| cousin | embassy | 7 | Kissinger, Shultz, Rice, Clinton, Dulles, DRockefeller, Donilon |
| pipeline | model | 7 | Schmidt, Thiel, Khan, Hassabis, Lonsdale, Nilekani, PLuckey |
| cycle | embassy | 8 | Kissinger, Vance, Christopher, Brzezinski, HBrown, AYoung, Huntington, DRockefeller |
| pipeline | algorithm | 10 | Schmidt, Gore, Khan, Hoffman, Suleyman, Sandberg, Musk, Bickert, Walker, YRoth |
| pulpit | eagle | 12 | Kissinger, Albright, CPowell, Rice, Clinton, Powell, Acheson, Dulles, Rusk, Hills, Marshall, SPower |
| backstop | embassy | 13 | Rumsfeld, Cheney, Gates, HBrown, JJones, Hagel, Mattis, Esper, Austin, Mueller, Marshall, Stimson, MPayne |
| pipeline | blueprint | 14 | Schmidt, Khan, Andreessen, Hoffman, Altman, Hassabis, Suleyman, Amodei, Musk, Sacks, Leo, Vought, Calabresi, PLuckey |
| pipeline | flagging | 15 | Schmidt, Sandberg, Stamos, JBaker, Bickert, JKaplan, Greenblatt, Monaco, McCord, Walker, Brookie, YRoth, AStone, SPower, Badalich |
| rumpelstiltskin | money | 15 | Summers, Fischer, Lagarde, Georgieva, Zoellick, Kim, Banga, Camdessus, Kohler, Rato, StraussKahn, Wolfensohn, Malpass, Carney, Draghi |
| vault | money | 15 | Rubin, Paulson, Geithner, Lew, Mnuchin, Yellen, Summers, Bessent, Fischer, Blumenthal, Corzine, Weill, Pandit, Lewis, Draghi |

### Network x Actor intersections

| Network | Actor | Persons | Names |
|---|---|---|---|
| aei | backdoor | 3 | Cheney, Bolton, Yoo |
| aei | embassy | 3 | Cheney, Wolfowitz, Bolton |
| bilderberg | blueprint | 3 | Schmidt, Hoffman, Schwab |
| bilderberg | eagle | 3 | Kissinger, Rice, Clinton |
| bilderberg | flagging | 3 | Schmidt, Donilon, Sandberg |
| cfr | backdoor | 3 | Cheney, Hayden, Bolton |
| cfr | priest | 3 | Yellen, Kerry, Bloomberg |
| trilateral | eagle | 3 | Kissinger, Brzezinski, Hills |
| trilateral | money | 4 | Volcker, Blumenthal, DRockefeller, Draghi |
| bilderberg | algorithm | 5 | Clinton, Schmidt, Gore, Hoffman, Sandberg |
| wef-ygl | flagging | 5 | Blinken, Schmidt, JSullivan, Sandberg, Ardern |
| bilderberg | embassy | 6 | Kissinger, Shultz, Rice, Clinton, DRockefeller, Donilon |
| cfr | flagging | 6 | Blinken, Brennan, Schmidt, Donilon, JSullivan, SPower |
| wef-ygl | money | 7 | Dimon, Fink, Schwarzman, Georgieva, Kim, Froman, Carney |
| cfr | watchers | 8 | Cheney, Petraeus, Brennan, Clapper, Hayden, Tenet, Haines, Negroponte |
| trilateral | embassy | 8 | Kissinger, Vance, Christopher, Brzezinski, HBrown, AYoung, Huntington, DRockefeller |
| cfr | tap | 11 | Cheney, Petraeus, Brennan, Clapper, Hayden, Gates, Tenet, WBurns, Haines, Negroponte, ADulles |
| bilderberg | money | 13 | Rubin, Paulson, Shultz, Dimon, Lagarde, DRockefeller, Camdessus, StraussKahn, Wolfensohn, Corzine, Soros, Carney, Draghi |
| cfr | eagle | 14 | Kissinger, Albright, CPowell, Rice, Clinton, Brzezinski, Wolfowitz, Powell, Acheson, Dulles, Rusk, Hills, McNamara, SPower |

### Admin x Actor intersections (small cohorts)

| Admin | Actor | Persons | Names |
|---|---|---|---|
| bush1 | eagle | 3 | CPowell, Powell, Hills |
| bush1 | money | 3 | Baker, Greenspan, Zoellick |
| bush2 | eagle | 3 | CPowell, Rice, Wolfowitz |
| carter | money | 3 | Rubenstein, Volcker, Blumenthal |
| clinton | algorithm | 3 | Gore, Sandberg, Walker |
| kennedy | eagle | 3 | Rusk, McNamara, Westmoreland |
| lbj | eagle | 3 | Rusk, McNamara, Westmoreland |
| trump1 | hospital | 3 | Fauci, Birx, Slaoui |
| trump2 | embassy | 3 | Rubio, Waltz, Hegseth |
| trump2 | money | 3 | Bessent, Lutnick, JWilliams |
| biden | tap | 4 | WBurns, Haines, Wray, Monaco |
| bush1 | tap | 4 | Cheney, Gates, WBarr, Addington |
| bush2 | flagging | 4 | Wray, JBaker, Bickert, JKaplan |
| bush2 | hospital | 4 | Fauci, Hatchett, Dybul, Birx |
| eisenhower | embassy | 4 | Dulles, Herter, ADulles, Lodge |
| ford | embassy | 4 | Kissinger, Scowcroft, Rumsfeld, Cheney |
| nixon | money | 4 | Shultz, Burns, Martin, Connally |
| obama | algorithm | 4 | Clinton, Schmidt, Hoffman, Bickert |
| reagan | money | 4 | Shultz, Baker, Volcker, Greenspan |
| roosevelt | embassy | 4 | Stettinius, Marshall, Stimson, Harriman |
| trump2 | blueprint | 4 | Andreessen, Musk, Sacks, Vought |
| clinton | embassy | 5 | Christopher, Albright, Berger, Donilon, Holder |
| clinton | flagging | 5 | Donilon, Sandberg, Holder, Garland, Walker |
| nixon | embassy | 5 | Kissinger, Haig, Shultz, Rogers, Lodge |
| obama | hospital | 5 | RShah, Gawande, Fauci, Hatchett, Birx |
| obama | watchers | 5 | Petraeus, Brennan, Clapper, Haines, KAlexander |
| trump1 | money | 5 | Mnuchin, Malpass, JWilliams, Mester, Rosengren |
| biden | flagging | 6 | Blinken, JSullivan, Wray, Monaco, Garland, SPower |
| biden | money | 6 | Lew, Yellen, Biden, JWilliams, Mester, Rosengren |
| reagan | embassy | 6 | Haig, Shultz, Baker, CPowell, McFarlane, Wolfowitz |
| bush1 | embassy | 7 | Baker, CPowell, Scowcroft, Cheney, Gates, Powell, Zoellick |
| bush2 | money | 7 | Paulson, Greenspan, Bernanke, Zoellick, ORneill, Snow, Rosengren |
| carter | embassy | 7 | Vance, Christopher, Brzezinski, Muskie, HBrown, AYoung, Huntington |
| clinton | money | 7 | Rubin, Yellen, Summers, Greenspan, Wolfensohn, Bentsen, Corzine |
| lbj | embassy | 7 | Rusk, MBundy, Rostow, Harriman, Lodge, Stevenson, Ball |
| truman | embassy | 7 | Stettinius, Acheson, Marshall, ADulles, Stimson, Harriman, Stevenson |
| trump1 | embassy | 7 | Tillerson, Powell, Bolton, Mattis, Esper, Mueller, NHaley |
| trump1 | tap | 7 | Pompeo, Thiel, Ratcliffe, Wray, Mueller, WBarr, Comey |
| bush2 | backdoor | 8 | Cheney, Hayden, Bolton, KAlexander, Wray, Yoo, Addington, Bybee |
| kennedy | embassy | 8 | Rusk, ADulles, MBundy, Rostow, Harriman, Lodge, Stevenson, Ball |
| biden | embassy | 9 | Kerry, Blinken, Powell, JSullivan, WBurns, Austin, Biden, Harris, SPower |
| obama | tap | 9 | Petraeus, Brennan, Clapper, Gates, Haines, KAlexander, Mueller, Monaco, Comey |
| bush2 | watchers | 10 | Cheney, Petraeus, Clapper, Hayden, Tenet, Goss, Negroponte, KAlexander, Yoo, Addington |
| obama | money | 11 | Geithner, Lew, Yellen, Summers, Bernanke, Fischer, Froman, Biden, JWilliams, Mester, Rosengren |
| obama | embassy | 12 | Clinton, Kerry, Blinken, Gates, Donilon, JJones, JSullivan, Hagel, Biden, Mueller, Holder, SPower |
| bush2 | embassy | 13 | CPowell, Rice, Rumsfeld, Cheney, Wolfowitz, Gates, Zoellick, Haass, Hadley, Bolton, Negroponte, Mueller, VCha |
| bush2 | tap | 14 | Cheney, Petraeus, Clapper, Hayden, Gates, Tenet, Goss, Negroponte, KAlexander, Wray, Mueller, Yoo, Addington, Comey |
| obama | flagging | 15 | Blinken, Brennan, Schmidt, Donilon, JSullivan, Holder, JBaker, Bickert, Greenblatt, Monaco, Garland, McCord, Brookie, AStone, SPower |

## 4. Admin density — where the cohort thickens by administration

| Admin | Total persons | Top sectors |
|---|---|---|
| obama | 58 | gov:27, intel:10, tank:10, tech:4 |
| bush2 | 54 | gov:20, intel:12, tank:10, judiciary:5 |
| trump1 | 44 | gov:23, intel:6, tank:5, tech:3 |
| biden | 27 | gov:19, intel:5, def:1, tech:1 |
| clinton | 24 | gov:14, fin:2, tech:2, judiciary:2 |
| trump2 | 22 | gov:14, intel:3, tech:3, fin:2 |
| bush1 | 18 | gov:11, judiciary:3, intel:1, imf:1 |
| reagan | 17 | gov:11, judiciary:3, tank:3 |
| truman | 13 | gov:7, def:5, intel:1 |
| kennedy | 12 | gov:9, def:2, intel:1 |
| nixon | 10 | gov:9, def:1 |
| carter | 10 | gov:9, fin:1 |
| lbj | 10 | gov:8, def:2 |
| ford | 8 | gov:8 |
| roosevelt | 7 | def:4, gov:3 |
| eisenhower | 6 | gov:5, intel:1 |

## 5. Network gravity

| Network | Members | Cross-network neighbors |
|---|---|---|
| cfr | 90 | aei, bilderberg, brookings, pnac, trilateral, wef-ygl |
| bilderberg | 33 | cfr, trilateral, wef-ygl |
| federalist | 20 | aei, heritage |
| wef-ygl | 17 | bilderberg, cfr |
| trilateral | 12 | bilderberg, cfr |
| heritage | 5 | federalist |
| aei | 4 | cfr, federalist, pnac |
| pnac | 2 | aei, cfr |
| wef | 2 |  |
| brookings | 1 | cfr |

## 6. Highest-edge institutions vs. their sector distribution

Institutions touched by the most persons, with the sector breakdown of those persons. Institutions touched by persons across many sectors are bridge nodes.

| Institution | Persons | Person-sector breakdown |
|---|---|---|
| `CFR` (CFR) | 85 | gov:56, intel:9, imf:7, def:5, fin:5, cfr:2, tech:1 |
| `State` (State Dept) | 40 | gov:31, tank:2, def:2, intel:2, imf:1, fin:1, cfr:1 |
| `WhiteHouse` (White House) | 35 | gov:16, tank:10, tech:5, fin:2, judiciary:2 |
| `NSC` (NSC) | 27 | gov:20, tank:4, intel:2, def:1 |
| `DoD` (DoD) | 25 | gov:11, def:10, tank:2, tech:1, intel:1 |
| `Bilderberg` (Bilderberg) | 22 | gov:6, fin:6, tech:4, imf:4, tank:1, def:1 |
| `Treasury` (US Treasury) | 21 | gov:15, fin:4, tech:1, imf:1 |
| `WEF` (WEF) | 18 | gov:7, tech:3, fin:3, imf:2, tank:1, multi:1, cfr:1 |
| `Senate` (US Senate) | 17 | gov:14, fin:1, intel:1, def:1 |
| `CIA` (CIA) | 16 | intel:11, gov:3, def:2 |
| `UN` (UN) | 14 | gov:9, multi:2, intel:2, fin:1 |
| `Goldman` (Goldman Sachs) | 12 | fin:7, gov:3, multi:1, imf:1 |
| `FedReserve` (Federal Reserve) | 12 | gov:11, imf:1 |
| `FederalistSociety` (Federalist Society) | 12 | tank:5, judiciary:5, gov:2 |
| `Trilateral` (Trilateral Comm.) | 11 | gov:10, fin:1 |
| `WorldBank` (World Bank) | 10 | imf:6, gov:2, fin:1, def:1 |
| `Google` (Google / Alphabet) | 10 | tech:9, gov:1 |
| `Meta` (Meta) | 9 | tech:8, def:1 |
| `X_Corp` (X Corp (formerly Twitter)) | 9 | tech:7, tank:1, intel:1 |
| `SCOTUS` (Supreme Court of the United States) | 9 | judiciary:9 |

## 7. Connector personalities — persons whose edges span the most distinct sectors

People connected to institutions across many distinct sectors. Higher = bridges between worlds (the Ratchet thesis's most thesis-defining shape).

| Person | Sectors spanned | Sector list |
|---|---|---|
| `Summers` (Larry Summers) | 6 | cfr, china-state, fin, gov, imf, tank |
| `Fischer` (Stanley Fischer) | 5 | cfr, china-state, fin, gov, imf |
| `Paulson` (Hank Paulson) | 5 | cfr, china-state, fin, gov, tank |
| `Wolfowitz` (Paul Wolfowitz) | 5 | cfr, def, gov, imf, tank |
| `Zoellick` (Robert Zoellick) | 5 | cfr, china-state, fin, gov, imf |
| `Bernanke` (Ben Bernanke) | 4 | cfr, china-state, gov, tank |
| `Bolton` (John Bolton) | 4 | cfr, gov, imf, tank |
| `Carney` (Mark Carney) | 4 | fin, gov, imf, tank |
| `Cheney` (Dick Cheney) | 4 | cfr, def, gov, tank |
| `Geithner` (Timothy Geithner) | 4 | cfr, china-state, fin, gov |
| `Kissinger` (Henry Kissinger) | 4 | cfr, china-state, gov, russia-state |
| `Negroponte` (John Negroponte) | 4 | cfr, gov, imf, intel |
| `Rubenstein` (David Rubenstein) | 4 | cfr, fin, gov, tank |
| `Schmidt` (Eric Schmidt) | 4 | cfr, china-state, def, tech |
| `Addington` (David Addington) | 3 | gov, intel, tank |
| `Baker` (James Baker) | 3 | cfr, fin, gov |
| `Ball` (George Ball) | 3 | cfr, gov, imf |
| `Banga` (Ajay Banga) | 3 | cfr, fin, imf |
| `CPowell` (Colin Powell) | 3 | cfr, def, gov |
| `Cameron` (David Cameron) | 3 | fin, gov, tank |
| `Corzine` (Jon Corzine) | 3 | cfr, fin, gov |
| `Donilon` (Tom Donilon) | 3 | cfr, fin, gov |
| `Dybul` (Mark Dybul) | 3 | gov, multi, tank |
| `Figueres` (Christiana Figueres) | 3 | fin, imf, multi |
| `Fink` (Larry Fink) | 3 | cfr, china-state, fin |

## 8. Vocabulary coverage check

### Plays usage

| Play | Count |
|---|---|
| acquisition | 25 |
| backstop | 20 |
| cousin | 29 |
| cycle | 12 |
| pipeline | 61 |
| pulpit | 50 |
| rumpelstiltskin | 19 |
| vault | 18 |

### Actors usage

| Actor | Count |
|---|---|
| algorithm | 23 |
| backdoor | 8 |
| blueprint | 27 |
| eagle | 16 |
| embassy | 80 |
| flagging | 42 |
| model | 12 |
| money | 53 |
| papers | 6 |
| tap | 33 |
| watchers | 18 |

### Networks usage

| Network | Count |
|---|---|
| aei | 4 |
| americanbar | 0 |
| atlantic | 0 |
| bilderberg | 33 |
| brookings | 1 |
| cfr | 90 |
| csis | 0 |
| federalist | 20 |
| heritage | 5 |
| hoover | 0 |
| pnac | 2 |
| rand | 0 |
| rockefeller | 0 |
| trilateral | 12 |
| wef | 2 |
| wef-ygl | 17 |

*Underused (<3): americanbar, atlantic, brookings, csis, hoover, pnac, rand, rockefeller, wef*