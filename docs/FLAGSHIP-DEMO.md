# Flagship demo: the Ratchet Atlas + Tradecraft Lens

> **Decision (2026-06-29):** the public flagship is the **integrated Atlas + Lens**, built **Lens-first**.
> Everything we build from here is a component of this, not loose data. Designing backward from it.

## The shared atom: the verified receipt

`{ lens, verbatim_span, url, date, verifier_rationale }` — produced by `verified_cue_receipts` /
`texts.verified_person_receipts` (context-read, never the cues floor). **Both components render this same
object.** Get the atom right and both demos are mostly presentation. This is why the verifier was the
load-bearing build: it is the unit of public trust.

## Component A — the Tradecraft Lens (public, ships first)

Paste any text (speech / op-ed / post) → `detect(backend=auto)` → `verified_cue_receipts` → a per-lens
method reading (inevitability_framing, institutional_permeation, …) with the verbatim receipts and the
lens explainers. **Method-not-verdict, ideology-blind, grades the TEXT you paste — not a person.** That
is the maximally defensible, non-defamatory, shareable surface, and it is the books' thesis made usable:
*here is the instrument; see the method yourself.*

- Backend: a `/grade-text` endpoint on the ratchet-mcp server (it already imports tradecraft). Local
  demo needs no deploy; public needs a host (gated, like the Raziel reference-tool).
- Framing: explicit "analysis of method, not a verdict" + disclaimers (web = more obviously analytical).

## Component B — the Ratchet Atlas (the sourced network)

Extend the existing `/tech/revolving-door/` D3 graph into the full apparatus map: **417 people / 384
institutions / 926 edges**, a **finance→apparatus funding-flow view** (METR triple-funded; the labs fund
the FMF Safety Fund that grades them; the `vault`/`bretton`/`cousin` plays), and **node cards** opening
the profile + **precomputed verified receipts** + the public footprint.

- Mostly **static**: precompute the receipts offline (gated) and embed → no live backend, ships as Hugo.
- Higher defamation surface (it names real people) → every node card is receipts-first, method-not-verdict,
  and bound by the OSINT-restraint floor + the gates.

## Integration (what makes it the flagship, not two toys)

- An Atlas node → "run the Lens on this subject's texts" (live).
- A node card shows the subject's precomputed grade summary + top verified receipts.
- The receipt is the hyperlink between map and instrument: click a marker in the Lens → see who else in
  the Atlas exhibits it; click a node in the Atlas → see the marker that put them there, with the quote.

## How the current pipeline feeds it (construct backward)

| We're building… | …becomes, in the flagship |
|---|---|
| The OSINT footprint pass (64 profiles) | Atlas node-card footprints |
| `verified_person_receipts` over the graph | Lens output + precomputed Atlas node cards |
| The finance/funding buildout | the Atlas funding-flow view |
| ratchet-mcp server | the Lens `/grade-text` backend |
| OSINT tools (Maigret/twscrape… gated) | more Atlas nodes (human-approved) |

## Build order

1. **Lens local demo** — `/grade-text` endpoint + minimal UI; runs locally off the MCP server. Safest,
   backend-light, proves the core interaction.
2. **Atlas v2 (static)** — extend the D3 to the full graph + funding-flow view + node cards with
   precomputed receipts + footprints.
3. **Integrate + deploy** — cross-link the two; pick a host; unpark the public page (author-gated, like
   the reference-tool).
4. **Drift / integrity tracker** (roadmap) — see below; the most novel surface, once historical pulls exist.

## The drift tracker is an integrity / traitor detector (the novel surface)

Author insight (2026-06-29): tracking a subject's method-markers *over time* does more than show
movement — it measures **whether they have a stable principal at all**, and **whether it was altered or
substituted**. Two signals, both structural and ideology-blind (they read the *shape* of a
method-signature, never which side it argues):

- **No stable principal — the opportunist.** High variance, no attractor: the signature swings with
  audience and incentive. Someone arguing whatever the moment rewards has no coherent core, and the
  variance shows it.
- **Discontinuity — the flip / capture / substitution.** A step-change at a point in time: markers were
  stable, then abruptly re-regime. That is the fingerprint of someone bought, pressured, or captured —
  or whose public voice was *substituted* (ghostwritten, account-run, or AI-autocompleted). The date of
  the break is itself a lead.

Method: the per-lens dated timeline + `trend` that `grade_person_texts` already returns → add (a) a
coherence/variance metric (principal-stability) and (b) changepoint detection (discontinuity). It flags
*instability* and *regime-change*, never a verdict on direction — which is what makes it both novel and
defensible.

Thematic payoff: the substitution case is *Quiet Autocomplete* made measurable — the moment a human
voice shifts to a managed/autocompleted signature is a detectable changepoint. The integrity tracker
turns the series thesis into an instrument.

## Gates (unchanged, restated for a public product)

- Method-not-verdict everywhere; receipts-first; sourced.
- Web framing = explicit analysis/parody + disclaimers (legal protection).
- The auto-mapper stays INTERNAL until tuned past `AUTO-MAPPING-DESIGN.md` §5 (measured FP rate +
  adversarial review + author sign-off). Nothing auto-writes to the public Atlas.
- Deploy host + public unpark are author decisions.
