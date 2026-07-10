# Auto-mapping ratchet frameworks from detections — design (R&D-GATED, not live)

> **Status: DESIGN.** This describes a capability, not a running system. It is **internal R&D, human-in-
> the-loop, never public until tuned past the bar in §5.** Auto-expanding a network of real people and
> auto-attributing "ratchet method" is guilt-by-association + false-positive defamation *at scale*. The
> whole point of writing it down is to make the dangers and the gates explicit before any of it runs.

## 1. The idea

Given a seed (a person, institution, or handle), automatically expand the surrounding network and keep
the nodes that **exhibit the tradecraft method-markers** — producing a candidate ratchet framework
(people + institutions + edges) for human review, rather than hand-building each node. "Mapped by
detection," not by assertion.

## 2. The tools (evaluated 2026-06-29 — all MIT, all importable Python libs, all current)

| Tool | Role in the pipeline | Auth tier | Output | Notes |
|---|---|---|---|---|
| **Maigret** (`soxoj/maigret`) | Footprint discovery + **recursive identity expansion** (handle → linked accounts → recurse) | none (enumeration) | JSON / CSV / **Neo4j Cypher** / D3 graph | 3000+ sites; async lib import; the safe, high-value starting primitive |
| **twscrape** (`vladkens/twscrape`) | X reads + **followers/following** (social edges) + texts | tier-2 (account pool) | tweets/users/edges | observatory-account model for X; could replace paid twitterapi.io |
| **snscrape** (`JustAnotherArchivist/snscrape`) | Multi-net texts (Reddit / Telegram / Mastodon) | none–tier-2 | posts | X support degraded; use for the other nets |
| **SpiderFoot** (`smicallef/spiderfoot`) | **Correlation engine** (37 YAML rules) over person/username/email/domain | varies | **GEXF graph** / JSON | headless CLI; the heaviest auto-mapper; correlation rules = candidate edges |

Each is a *primitive*. None is the product — the product is the gated pipeline below.

## 3. The pipeline

```
seed(person|inst|handle)
  → EXPAND   (Maigret recursive identity ∪ twscrape follows ∪ SpiderFoot correlation)  → candidate nodes+edges
  → GATE     (correctness gate: every handle --verify'd to a real named person)         → confirmed identities
  → COLLECT  (pull the subject's OWN published texts, per OSINT-RESTRAINT content floor) → texts
  → DETECT   (tradecraft text lenses, backend=auto)                                      → per-node method scores
  → VERIFY   (verified_cue_receipts: keep only genuine, in-context markers)              → publishable receipts
  → REVIEW   (human: confirm node, edge, and that the receipt is real)                   → approved
  → WRITE    (idempotent add to people/institutions/edges; ≥2 sources, positions-only)   → ratchet graph
```

Two filters carry the weight: the **correctness gate** (a node is a *confirmed* named person, never a
guessed handle) and the **verified-receipt** step (a node is "ratchet" only on a context-confirmed
marker, never a raw cue hit — the floor we already proved kills tweet-level false positives).

## 4. Why it is dangerous (the failure modes to design against)

- **Guilt-by-association.** A follows/correlation edge is not complicity. Auto-expansion makes "is near
  the network" look like "is in the apparatus." A follower is not a member.
- **False-positive method attribution at scale.** The cues floor false-fires on short text (proven); an
  auto-mapper that skips the verifier would brand thousands of people on word-matches.
- **Snowball drift.** Recursive expansion drifts from the seed's relevance — N hops out you are mapping
  strangers. Relevance decays; the map doesn't know that.
- **Bycatch of private people.** Expansion sweeps in non-public individuals (a researcher's friends,
  family). The OSINT-restraint floor must hold per-node, automatically.
- **Laundering inference as data.** A graph *looks* authoritative. An auto-generated edge with no human
  check reads as established fact. That is the exact defect the project critiques in others.

## 5. The gates (what must be true before it runs — and the higher bar for public)

**To run INTERNALLY (R&D):**
- **Human-in-the-loop is mandatory.** Nothing is written to the graph without per-node/per-edge human
  approval. The tools *propose*; a person *commits*. No auto-write.
- **Verifier-gated detections only.** A node is tagged "ratchet method" solely on a `verified_cue_receipts`
  genuine hit (context-read), never a cues-floor or raw-score hit.
- **Correctness-gated nodes only.** No node without a `--verify`'d handle → named person.
- **Bounded expansion.** Hop limit (≤2 from seed) + a relevance threshold; log everything dropped (no
  silent truncation).
- **Restraint floor per node, automatic.** Private individuals and locate-kit data filtered before review.
- **Edges are typed and sourced.** "follows" / "co-affiliated" / "funded-by" are different claims; an edge
  carries its kind + receipt, never a bare line implying complicity.

**Before ANYTHING is public (the higher bar):**
- Measured false-positive rate on a labeled set, below an agreed threshold (calibrate like the verifier
  eval: known-faction positives fire, known-clean negatives stay quiet).
- Adversarial review of a sample map for guilt-by-association and bycatch (the `adversarial-reviewer` lens).
- Author sign-off that every published node/edge would survive a defamation read on its own receipts.
- Web framing as analysis-of-method with sourcing, never a verdict (per the parody/seriousness split).

## 6. Phased plan

1. **Maigret first** (safe, non-ToS, immediate value): wire footprint discovery into the OSINT pass —
   Maigret finds candidate handles → `--verify-handle` confirms → human records. No expansion yet.
2. **twscrape** as the X observatory backend (tier-2 accounts) for texts + follow-edges, behind review.
3. **Detection-filter loop**: detector + verifier over collected texts → proposed method tags, human-approved.
4. **SpiderFoot correlation** as the expansion engine — last, and only with §5's gates wired, because it
   is the one that most readily manufactures unearned edges.

Build order is deliberately "safest-first." The auto-expander (4) does not get built until the gates (5)
are real and the verifier false-positive rate is measured. Until then this stays a hand-driven OSINT
pass with power tools, not an autonomous mapper.
