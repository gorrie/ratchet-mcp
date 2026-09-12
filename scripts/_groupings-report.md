# Ratchet Dataset — Discovered Groupings

Snapshot of 550 persons / 486 institutions / 1243 edges.

Mechanical analyses below; cross-reference against clusters.json (named human-curated clusters) and SCOPE.md (cohort definitions).


## 1. Centrality — most-connected persons and institutions

### Most-connected persons (top 25)

| Person | Edge count | Sector | Plays | Actors |
|---|---|---|---|---|
| `Kissinger` (Henry Kissinger) | 12 | gov | pulpit,cycle,cousin | embassy,eagle |
| `Summers` (Larry Summers) | 9 | gov | bretton,vault | money |
| `Paulson` (Hank Paulson) | 8 | fin | vault,acquisition,cousin | money |
| `Carney` (Mark Carney) | 8 | gov | bretton,cousin | money,priest |
| `Zoellick` (Robert Zoellick) | 7 | imf | bretton | money,embassy |
| `Schmidt` (Eric Schmidt) | 7 | tech | pipeline,cousin | algorithm,model,blueprint,flagging |
| `Rice` (Condoleezza Rice) | 6 | gov | pulpit,cousin | embassy,eagle |
| `Fischer` (Stanley Fischer) | 6 | imf | bretton,vault | money |
| `Rubin` (Robert Rubin) | 5 | fin | vault,cousin | money |
| `Geithner` (Timothy Geithner) | 5 | gov | vault | money |
| `Shultz` (George Shultz) | 5 | gov | pulpit,cousin | money,embassy |
| `Baker` (James Baker) | 5 | gov | pulpit | money,embassy |
| `Wolfowitz` (Paul Wolfowitz) | 5 | gov | bretton | embassy,eagle |
| `Petraeus` (David Petraeus) | 5 | def | backstop,cousin | tap,watchers |
| `Hayden` (Michael Hayden) | 5 | intel |  | tap,watchers,backdoor |
| `Fink` (Larry Fink) | 5 | fin | cousin | money,priest |
| `Volcker` (Paul Volcker) | 5 | gov | cycle | money |
| `Lagarde` (Christine Lagarde) | 5 | imf | bretton,cousin | money |
| `DRockefeller` (David Rockefeller) | 5 | fin | cycle,cousin | money,embassy |
| `Donilon` (Tom Donilon) | 5 | gov | vault,cousin | embassy,flagging |
| `Bolton` (John Bolton) | 5 | gov | pulpit | embassy,backdoor |
| `Haines` (Avril Haines) | 5 | intel |  | tap,watchers |
| `Hoffman` (Reid Hoffman) | 5 | tech | pipeline,cousin | algorithm,blueprint |
| `Sandberg` (Sheryl Sandberg) | 5 | tech | pipeline,vault,cousin | algorithm,flagging,papers |
| `Musk` (Elon Musk) | 5 | tech | acquisition,pipeline | algorithm,blueprint |

### Most-connected institutions (top 25)

| Institution | Person edges | Sector |
|---|---|---|
| `CFR` (CFR) | 88 | cfr |
| `WhiteHouse` (White House) | 50 | gov |
| `State` (State Dept) | 45 | gov |
| `DoD` (DoD) | 45 | def |
| `NSC` (NSC) | 31 | gov |
| `OpenAI` (OpenAI) | 27 | tech |
| `CIA` (CIA) | 24 | intel |
| `Treasury` (US Treasury) | 22 | gov |
| `Bilderberg` (Bilderberg) | 22 | cfr |
| `Google` (Google / Alphabet) | 22 | tech |
| `WEF` (WEF) | 18 | cfr |
| `Senate` (US Senate) | 16 | gov |
| `Meta` (Meta) | 16 | tech |
| `UN` (UN) | 15 | imf |
| `Anthropic` (Anthropic) | 15 | tech |
| `Goldman` (Goldman Sachs) | 13 | fin |
| `FedReserve` (Federal Reserve) | 12 | gov |
| `FederalistSociety` (Federalist Society) | 12 | tank |
| `WorldBank` (World Bank) | 11 | imf |
| `Trilateral` (Trilateral Comm.) | 11 | cfr |
| `OpenPhil` (Open Philanthropy) | 11 | tank |
| `Microsoft` (Microsoft) | 10 | tech |
| `X_Corp` (X Corp (formerly Twitter)) | 10 | tech |
| `SCOTUS` (Supreme Court of the United States) | 9 | judiciary |
| `Citigroup` (Citigroup) | 8 | fin |

## 2. Co-occurrence — which plays / actors / networks travel together

### Plays that co-occur (>= 3 persons hold both)

| Play A | Play B | Persons with both |
|---|---|---|
| acquisition | pipeline | 7 |
| cousin | vault | 5 |
| cousin | pulpit | 5 |
| cousin | pipeline | 5 |
| backstop | pulpit | 5 |
| acquisition | vault | 4 |
| cycle | pulpit | 4 |
| bretton | cousin | 4 |
| bretton | vault | 3 |

### Actors that co-occur (>= 3 persons touch both)

| Actor A | Actor B | Persons touching both |
|---|---|---|
| tap | watchers | 28 |
| eagle | embassy | 13 |
| embassy | tap | 12 |
| algorithm | flagging | 10 |
| algorithm | blueprint | 9 |
| blueprint | model | 9 |
| embassy | money | 6 |
| backdoor | tap | 6 |
| model | papers | 6 |
| embassy | flagging | 5 |
| backdoor | watchers | 5 |
| flagging | tap | 4 |
| model | watchers | 4 |
| money | priest | 3 |
| algorithm | model | 3 |
| blueprint | flagging | 3 |
| model | tap | 3 |

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
| acquisition | hospital | 3 | Slaoui, Azar, Slavitt |
| cousin | flagging | 3 | Schmidt, Donilon, Sandberg |
| cycle | eagle | 3 | Kissinger, Brzezinski, Hills |
| pulpit | money | 3 | Shultz, Baker, Froman |
| acquisition | blueprint | 4 | Andreessen, Musk, Warner, PLuckey |
| cousin | blueprint | 4 | Schmidt, Hoffman, Altman, Schwab |
| cousin | eagle | 4 | Kissinger, Rice, Clinton, Dulles |
| cycle | money | 4 | Volcker, Blumenthal, DRockefeller, Burns |
| pulpit | flagging | 4 | Blinken, JSullivan, SPower, LauraRosenberger |
| cousin | algorithm | 5 | Clinton, Schmidt, Gore, Hoffman, Sandberg |
| pulpit | tap | 5 | Pompeo, WBurns, Negroponte, Panetta, McCabe |
| pulpit | watchers | 5 | Pompeo, Negroponte, GGerstell, Panetta, McCabe |
| acquisition | money | 7 | Paulson, Mnuchin, Bessent, ORneill, Snow, Corzine, Lutnick |
| cousin | embassy | 7 | Kissinger, Shultz, Rice, Clinton, Dulles, DRockefeller, Donilon |
| pipeline | tap | 7 | Thiel, Monaco, SGordon, CInglis, DCohen, Morial, RJacobson |
| cycle | embassy | 8 | Kissinger, Vance, Christopher, Brzezinski, HBrown, AYoung, Huntington, DRockefeller |
| pipeline | papers | 8 | Sandberg, Nilekani, FCollins, Varmus, Gutmann, SeidmanBecker, BlakeHall, OWest |
| backstop | watchers | 9 | Cheney, Petraeus, KAlexander, MRogers, RJoyce, MMorell, Vickers, Panetta, Nakasone |
| pipeline | algorithm | 10 | Schmidt, Gore, Khan, Hoffman, Suleyman, Sandberg, Musk, Bickert, Walker, YRoth |
| backstop | tap | 12 | Cheney, Petraeus, Gates, KAlexander, Mueller, MRogers, RJoyce, MMorell, Deutch, Vickers, Panetta, Nakasone |
| pipeline | watchers | 14 | SGordon, CInglis, DCohen, JBash, MChertoff, SOSullivan, TraeStephens, Bratton, Sankar, Carmona, JeriWilliams, KTodt, TSzymanski, DMathews |
| pulpit | eagle | 14 | Kissinger, Albright, CPowell, Rice, Clinton, Powell, Acheson, Dulles, Rusk, Hills, Marshall, SPower, Makanju, Lehane |
| bretton | money | 15 | Summers, Fischer, Lagarde, Georgieva, Zoellick, Kim, Banga, Camdessus, Kohler, Rato, StraussKahn, Wolfensohn, Malpass, Carney, Draghi |
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
| wef-ygl | money | 7 | Dimon, Fink, Schwarzman, Georgieva, Kim, Froman, Carney |
| cfr | flagging | 8 | Blinken, Brennan, Schmidt, Donilon, JSullivan, SPower, EmersonBrooking, LauraRosenberger |
| trilateral | embassy | 8 | Kissinger, Vance, Christopher, Brzezinski, HBrown, AYoung, Huntington, DRockefeller |
| cfr | watchers | 9 | Cheney, Petraeus, Brennan, Clapper, Hayden, Tenet, Haines, Negroponte, GGerstell |
| cfr | tap | 11 | Cheney, Petraeus, Brennan, Clapper, Hayden, Gates, Tenet, WBurns, Haines, Negroponte, ADulles |
| bilderberg | money | 13 | Rubin, Paulson, Shultz, Dimon, Lagarde, DRockefeller, Camdessus, StraussKahn, Wolfensohn, Corzine, Soros, Carney, Draghi |
| cfr | eagle | 14 | Kissinger, Albright, CPowell, Rice, Clinton, Brzezinski, Wolfowitz, Powell, Acheson, Dulles, Rusk, Hills, McNamara, SPower |

### Admin x Actor intersections (small cohorts)

| Admin | Actor | Persons | Names |
|---|---|---|---|
| biden | eagle | 3 | Powell, SPower, Makanju |
| bush1 | eagle | 3 | CPowell, Powell, Hills |
| bush1 | money | 3 | Baker, Greenspan, Zoellick |
| bush2 | eagle | 3 | CPowell, Rice, Wolfowitz |
| carter | money | 3 | Rubenstein, Volcker, Blumenthal |
| clinton | algorithm | 3 | Gore, Sandberg, Walker |
| clinton | hospital | 3 | Fauci, Woodcock, Varmus |
| clinton | tap | 3 | Tenet, Deutch, Panetta |
| kennedy | eagle | 3 | Rusk, McNamara, Westmoreland |
| lbj | eagle | 3 | Rusk, McNamara, Westmoreland |
| obama | blueprint | 3 | Schmidt, Hoffman, AratiPrabhakar |
| obama | eagle | 3 | Clinton, SPower, Makanju |
| trump1 | flagging | 3 | Wray, WBarr, ChrisKrebs |
| trump2 | model | 3 | MichaelKratsios, SriramKrishnan, Sankar |
| bush1 | tap | 4 | Cheney, Gates, WBarr, Addington |
| bush2 | flagging | 4 | Wray, JBaker, Bickert, JKaplan |
| eisenhower | embassy | 4 | Dulles, Herter, ADulles, Lodge |
| ford | embassy | 4 | Kissinger, Scowcroft, Rumsfeld, Cheney |
| nixon | money | 4 | Shultz, Burns, Martin, Connally |
| obama | algorithm | 4 | Clinton, Schmidt, Hoffman, Bickert |
| obama | model | 4 | Schmidt, AratiPrabhakar, TinoCuellar, Dugan |
| obama | papers | 4 | FCollins, Varmus, Gutmann, Bollinger |
| reagan | money | 4 | Shultz, Baker, Volcker, Greenspan |
| roosevelt | embassy | 4 | Stettinius, Marshall, Stimson, Harriman |
| trump2 | embassy | 4 | Rubio, Waltz, Hegseth, Claver-Carone |
| trump2 | money | 4 | Bessent, Lutnick, JWilliams, Claver-Carone |
| biden | blueprint | 5 | Khan, Hoffman, Matheny, AratiPrabhakar, BenBuchanan |
| clinton | flagging | 5 | Donilon, Sandberg, Holder, Garland, Walker |
| nixon | embassy | 5 | Kissinger, Haig, Shultz, Rogers, Lodge |
| trump1 | model | 5 | Thiel, MichaelKratsios, TraeStephens, Nakasone, OWest |
| reagan | embassy | 6 | Haig, Shultz, Baker, CPowell, McFarlane, Wolfowitz |
| trump1 | money | 6 | Mnuchin, Malpass, JWilliams, Mester, Rosengren, Claver-Carone |
| trump2 | blueprint | 6 | Andreessen, Musk, Sacks, Vought, MichaelKratsios, Sankar |
| biden | hospital | 7 | Gawande, Fauci, Califf, Slavitt, EFowler, Woodcock, FCollins |
| biden | model | 7 | Khan, ElizabethKelly, GinaRaimondo, AratiPrabhakar, RummanChowdhury, BenBuchanan, Nakasone |
| biden | money | 7 | Lew, Yellen, Biden, JWilliams, Mester, Rosengren, DCohen |
| biden | watchers | 7 | Haines, Matheny, CInglis, RJoyce, DCohen, Nakasone, DMathews |
| bush1 | embassy | 7 | Baker, CPowell, Scowcroft, Cheney, Gates, Powell, Zoellick |
| bush2 | money | 7 | Paulson, Greenspan, Bernanke, Zoellick, ORneill, Snow, Rosengren |
| clinton | money | 7 | Rubin, Yellen, Summers, Greenspan, Wolfensohn, Bentsen, Corzine |
| lbj | embassy | 7 | Rusk, MBundy, Rostow, Harriman, Lodge, Stevenson, Ball |
| truman | embassy | 7 | Stettinius, Acheson, Marshall, ADulles, Stimson, Harriman, Stevenson |
| biden | tap | 8 | WBurns, Haines, Wray, Monaco, CInglis, RJoyce, DCohen, Nakasone |
| bush2 | backdoor | 8 | Cheney, Hayden, Bolton, KAlexander, Wray, Yoo, Addington, Bybee |
| carter | embassy | 8 | Vance, Christopher, Brzezinski, Muskie, HBrown, AYoung, Huntington, Perry |
| kennedy | embassy | 8 | Rusk, ADulles, MBundy, Rostow, Harriman, Lodge, Stevenson, Ball |
| clinton | embassy | 9 | Christopher, Albright, Berger, Donilon, Holder, Gabriel-Edward, Flournoy, Deutch, Perry |
| trump1 | hospital | 9 | Fauci, Birx, Slaoui, Gottlieb, Hahn, Azar, Woodcock, Frazier, FCollins |
| trump1 | watchers | 9 | Pompeo, Ratcliffe, MRogers, SGordon, GGerstell, RJoyce, TraeStephens, McCabe, Nakasone |
| biden | embassy | 10 | Kerry, Blinken, Powell, JSullivan, WBurns, Austin, Biden, Harris, SPower, SRice |
| biden | flagging | 10 | Blinken, JSullivan, Wray, Monaco, Garland, SPower, NinaJankowicz, EmersonBrooking, JenEasterly, LauraRosenberger |
| bush2 | hospital | 10 | Fauci, Hatchett, Dybul, Birx, Veneman, McClellan, Gerberding, Azar, Woodcock, Zerhouni |
| trump1 | embassy | 10 | Tillerson, Powell, Bolton, Mattis, Esper, Mueller, NHaley, Kumar-Shalabh, Claver-Carone, Work |
| obama | hospital | 11 | RShah, Gawande, Fauci, Hatchett, Birx, Califf, Slavitt, EFowler, Woodcock, FCollins, Varmus |
| trump1 | tap | 12 | Pompeo, Thiel, Ratcliffe, Wray, Mueller, WBarr, Comey, MRogers, SGordon, RJoyce, McCabe, Nakasone |
| obama | money | 13 | Geithner, Lew, Yellen, Summers, Bernanke, Fischer, Froman, Biden, JWilliams, Mester, Rosengren, DCohen, Bollinger |
| bush2 | embassy | 14 | CPowell, Rice, Rumsfeld, Cheney, Wolfowitz, Gates, Zoellick, Haass, Hadley, Bolton, Negroponte, Mueller, VCha, Stavridis |
| bush2 | watchers | 14 | Cheney, Petraeus, Clapper, Hayden, Tenet, Goss, Negroponte, KAlexander, Yoo, Addington, CInglis, MChertoff, Vickers, Carmona |

## 4. Admin density — where the cohort thickens by administration

| Admin | Total persons | Top sectors |
|---|---|---|
| obama | 97 | gov:45, intel:21, tank:13, def:8 |
| bush2 | 69 | gov:32, intel:14, tank:10, judiciary:5 |
| trump1 | 67 | gov:32, intel:12, def:5, tank:5 |
| biden | 53 | gov:35, intel:10, tank:3, def:2 |
| clinton | 38 | gov:22, intel:3, tank:3, fin:2 |
| trump2 | 25 | gov:14, tech:5, intel:3, fin:2 |
| reagan | 19 | gov:13, judiciary:3, tank:3 |
| bush1 | 18 | gov:11, judiciary:3, intel:1, imf:1 |
| truman | 13 | gov:7, def:5, intel:1 |
| kennedy | 12 | gov:9, def:2, intel:1 |
| carter | 11 | gov:9, fin:1, def:1 |
| nixon | 10 | gov:9, def:1 |
| lbj | 10 | gov:8, def:2 |
| ford | 8 | gov:8 |
| roosevelt | 7 | def:4, gov:3 |
| eisenhower | 6 | gov:5, intel:1 |

## 5. Network gravity

| Network | Members | Cross-network neighbors |
|---|---|---|
| cfr | 95 | aei, bilderberg, brookings, pnac, trilateral, wef-ygl |
| bilderberg | 33 | cfr, trilateral, wef-ygl |
| federalist | 20 | aei, heritage |
| wef-ygl | 17 | bilderberg, cfr |
| trilateral | 13 | bilderberg, cfr |
| heritage | 5 | federalist |
| aei | 4 | cfr, federalist, pnac |
| pnac | 2 | aei, cfr |
| wef | 2 |  |
| brookings | 1 | cfr |
| rockefeller | 1 |  |

## 6. Highest-edge institutions vs. their sector distribution

Institutions touched by the most persons, with the sector breakdown of those persons. Institutions touched by persons across many sectors are bridge nodes.

| Institution | Persons | Person-sector breakdown |
|---|---|---|
| `CFR` (CFR) | 88 | gov:57, intel:10, imf:7, fin:5, def:5, cfr:2, tank:1, tech:1 |
| `WhiteHouse` (White House) | 50 | gov:25, tank:12, tech:6, fin:2, judiciary:2, def:1, multi:1, intel:1 |
| `State` (State Dept) | 45 | gov:34, tank:3, intel:2, def:2, tech:1, imf:1, fin:1, cfr:1 |
| `DoD` (DoD) | 45 | def:21, gov:12, intel:7, tank:3, tech:2 |
| `NSC` (NSC) | 31 | gov:23, tank:4, intel:2, def:1, tech:1 |
| `OpenAI` (OpenAI) | 27 | tech:15, tank:3, gov:2, multi:1, intel:1 |
| `CIA` (CIA) | 24 | intel:19, gov:3, def:2 |
| `Treasury` (US Treasury) | 22 | gov:15, fin:4, tech:1, imf:1, intel:1 |
| `Bilderberg` (Bilderberg) | 22 | fin:6, gov:6, tech:4, imf:4, tank:1, def:1 |
| `Google` (Google / Alphabet) | 22 | tech:16, gov:1, def:1 |
| `WEF` (WEF) | 18 | gov:7, fin:3, tech:3, imf:2, tank:1, cfr:1, multi:1 |
| `Senate` (US Senate) | 16 | gov:13, fin:1, def:1, intel:1 |
| `Meta` (Meta) | 16 | tech:12, def:2, gov:1 |
| `UN` (UN) | 15 | gov:10, intel:2, multi:2, fin:1 |
| `Anthropic` (Anthropic) | 15 | tech:9, tank:2 |
| `Goldman` (Goldman Sachs) | 13 | fin:7, gov:4, multi:1, imf:1 |
| `FedReserve` (Federal Reserve) | 12 | gov:11, imf:1 |
| `FederalistSociety` (Federalist Society) | 12 | tank:5, judiciary:5, gov:2 |
| `WorldBank` (World Bank) | 11 | imf:7, gov:2, fin:1, def:1 |
| `Trilateral` (Trilateral Comm.) | 11 | gov:10, fin:1 |

## 7. Connector personalities — persons whose edges span the most distinct sectors

People connected to institutions across many distinct sectors. Higher = bridges between worlds (the Ratchet thesis's most thesis-defining shape).

| Person | Sectors spanned | Sector list |
|---|---|---|
| `Kissinger` (Henry Kissinger) | 6 | cfr, china-state, fin, gov, russia-state, tank |
| `Summers` (Larry Summers) | 6 | cfr, china-state, fin, gov, imf, tank |
| `Fischer` (Stanley Fischer) | 5 | cfr, china-state, fin, gov, imf |
| `JBash` (Jeremy Bash) | 5 | def, fin, intel, multi, tank |
| `Paulson` (Hank Paulson) | 5 | cfr, china-state, fin, gov, tank |
| `Schmidt` (Eric Schmidt) | 5 | cfr, china-state, def, tank, tech |
| `Wolfowitz` (Paul Wolfowitz) | 5 | cfr, def, gov, imf, tank |
| `Zoellick` (Robert Zoellick) | 5 | cfr, china-state, fin, gov, imf |
| `Bernanke` (Ben Bernanke) | 4 | cfr, china-state, gov, tank |
| `Bolton` (John Bolton) | 4 | cfr, gov, imf, tank |
| `Carney` (Mark Carney) | 4 | fin, gov, imf, tank |
| `Cheney` (Dick Cheney) | 4 | cfr, def, gov, tank |
| `ClintWatts` (Clint Watts) | 4 | intel, multi, tank, tech |
| `Comey` (James Comey) | 4 | def, fin, gov, intel |
| `Geithner` (Timothy Geithner) | 4 | cfr, china-state, fin, gov |
| `Haines` (Avril Haines) | 4 | cfr, gov, intel, tank |
| `Hayden` (Michael Hayden) | 4 | cfr, intel, multi, tank |
| `McClellan` (Mark McClellan) | 4 | fin, gov, multi, tank |
| `McMaster` (H.R. McMaster) | 4 | def, gov, tank, tech |
| `Negroponte` (John Negroponte) | 4 | cfr, gov, imf, intel |
| `Panetta` (Leon Panetta) | 4 | def, gov, intel, tank |
| `Petraeus` (David Petraeus) | 4 | cfr, def, fin, intel |
| `Rubenstein` (David Rubenstein) | 4 | cfr, fin, gov, tank |
| `Stavridis` (James Stavridis) | 4 | def, fin, multi, tank |
| `VDinh` (Viet Dinh) | 4 | gov, judiciary, tank, tech |

## 8. Vocabulary coverage check

### Plays usage

| Play | Count |
|---|---|
| acquisition | 27 |
| backstop | 36 |
| bretton | 20 |
| cousin | 29 |
| cycle | 12 |
| pipeline | 116 |
| pulpit | 58 |
| vault | 18 |

### Actors usage

| Actor | Count |
|---|---|
| algorithm | 23 |
| backdoor | 8 |
| blueprint | 32 |
| eagle | 18 |
| embassy | 92 |
| flagging | 53 |
| model | 37 |
| money | 59 |
| papers | 15 |
| tap | 46 |
| watchers | 41 |

### Networks usage

| Network | Count |
|---|---|
| aei | 4 |
| americanbar | 0 |
| atlantic | 0 |
| bilderberg | 33 |
| brookings | 1 |
| cfr | 95 |
| csis | 0 |
| federalist | 20 |
| heritage | 5 |
| hoover | 0 |
| pnac | 2 |
| rand | 0 |
| rockefeller | 1 |
| trilateral | 13 |
| wef | 2 |
| wef-ygl | 17 |

*Underused (<3): americanbar, atlantic, brookings, csis, hoover, pnac, rand, rockefeller, wef*