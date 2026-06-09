# Ratchet MCP — Example Prompts

> **Three demonstrations of what the MCP is for.** Each prompt is an actual question you can ask Claude Desktop once the Ratchet MCP server is running. Each result is verifiable against the dataset's primary sources — citations are part of the response, not flavor.

These are the "showcase" prompts intended for the published `evilrobots.lol/tech/ratchet-mcp/` page. The MCP tool surface is designed to make them tractable in a single conversation turn.

---

## Prompt 1 — "The Trump II Vault"

**The play:** Wall Street executive → cabinet → likely back to Wall Street. Named the `vault` play in our dataset.

**Prompt to Claude (with the Ratchet MCP loaded):**

> List every person in the Trump II administration who's executing the Vault play. For each, give me their pre-cabinet finance role, their current cabinet position, the documented network memberships, and the source URLs.

**Expected response shape** (verifiable per-record):

| Person | Pre-cabinet | Cabinet (Trump II) | Networks | Sources |
|---|---|---|---|---|
| Scott Bessent | Soros Fund Mgmt → Key Square Capital | Treasury Secretary | — | [Wikipedia](https://en.wikipedia.org/wiki/Scott_Bessent) |
| (And whoever else lands in the v3 dataset who fits) | | | | |

**Why this demo matters:** the play tag is the operationalized version of a thesis chapter. Anyone with the MCP can verify the claim mechanically; no "trust me" required.

**Tool calls behind the prompt:**

```
query_cohort(admin="trump2", play="vault")
  → returns the list of person ids
get_entity(id) for each
  → returns role + sources
```

---

## Prompt 2 — "Who connects Anthropic to the State Department?"

**The question:** path-finding through the graph. Who, if anyone, sits between a frontier-AI lab and the foreign-policy apparatus?

**Prompt to Claude:**

> What's the shortest documented path between Anthropic and the State Department? Walk me through each hop with the person's role at each end.

**Expected response shape:**

> Two-hop paths exist:
>
> **Path A — Reid Hoffman.** Anthropic is connected via OpenAI (Hoffman was an early OpenAI board member and invests in Inflection AI, founded by Mustafa Suleyman who co-founded DeepMind alongside Demis Hassabis — Anthropic and OpenAI share founder-investor overlap with Hoffman through the Amodei→OpenAI→Anthropic transition). Hoffman is a Bilderberg attendee; the State Department under Biden was led by Antony Blinken who is a WEF Young Global Leader and CFR member, co-attending those forums.
> — Sources: [Hoffman LittleSis](https://littlesis.org/...), [Blinken Wikipedia](https://en.wikipedia.org/wiki/Antony_Blinken)
>
> **Path B — Eric Schmidt.** Schmidt is documented at DoD (NSCAI chair) and on State Department AI advisory groups. The Anthropic side: Schmidt's Schmidt Futures has funded AI-policy work that Anthropic participates in.
> — Sources: [Schmidt NSCAI](https://www.nscai.gov/), [Schmidt Wikipedia](https://en.wikipedia.org/wiki/Eric_Schmidt)
>
> **Direct edge:** none documented in the dataset.

**Why this demo matters:** the prompt operationalizes one of the book's points — that the AI-policy apparatus and the AI labs share personnel infrastructure. The path is short. The dataset says so with citations.

**Tool calls:**

```
who_connects("Anthropic", "State", max_hops=3)
  → returns shortest paths + intermediate node citations
```

---

## Prompt 3 — "Two cranks, same hand" *(the headline)*

**The thesis:** in *The Ratchet*, the argument is that the same cohort that built the SIGINT apparatus also built the encryption-mandate apparatus. These are two cranks of the control grid, turned by the same hand. The MCP makes this claim mechanically checkable.

**Prompt to Claude:**

> Find every person in the dataset whose documented career touches both the `tap` (SIGINT / mass collection) actor AND the `backdoor` (encryption-mandate / lawful-intercept) actor. For each, give me the documented role at each touchpoint, with sources.

**Expected response shape:**

> Three people in the v2 dataset satisfy both:
>
> **Michael Hayden** (`tap`, `watchers`, `backdoor`)
> - NSA Director 1999-2005 (Stellar Wind, post-9/11 mass-collection program)
> - CIA Director 2006-2009
> - Public proponent of CALEA-style lawful-intercept and the encryption-mandate position
> - [Wikipedia](https://en.wikipedia.org/wiki/Michael_Hayden_(general))
>
> **Dick Cheney** (`tap`, `watchers`, `backdoor`, `embassy`)
> - VP 2001-2009; PATRIOT Act architect (Section 215, Section 702 expansion → SIGINT actor)
> - Documented advocate for lawful-intercept provisions in encryption debates (backdoor actor)
> - [Wikipedia](https://en.wikipedia.org/wiki/Dick_Cheney)
>
> **John Bolton** (`embassy`, `backdoor`)
> - Bush II State Dept Under-Secretary, NSA under Trump I
> - Public position on encryption backdoors during NSA tenure
> - [Wikipedia](https://en.wikipedia.org/wiki/John_Bolton)
>
> Three of 117 named individuals. Both cranks. Same hand.

**Why this demo matters:** the data answers the book's literal thesis question. "Is it the same people?" — yes; here are the three; here are the receipts. This is the prompt that goes on `@evilbotslol` with a screenshot.

**Tool calls:**

```
find_overlap(actors=["tap", "backdoor"])
  → returns the intersection of person ids
get_entity(id) for each
  → returns role + sources for the response body
```

---

## Tool surface (the MCP's tools, by name)

| Tool | What it does | Demos that use it |
|---|---|---|
| `query_cohort(sector?, admin?, play?, network?, actor?)` | Filter people by any combination of dimension values. Returns ids. | Prompt 1 |
| `get_entity(id)` | Return the full record + sources for one person or institution. | All three |
| `who_connects(a_id, b_id, max_hops=3)` | Find shortest path(s) between two entities. | Prompt 2 |
| `find_overlap(actors=[...])` or `find_overlap(plays=[...])` | Intersection of person ids who touch all given actors / plays. | Prompt 3 |
| `list_plays_for(person_id)` | Reverse lookup: which plays does this person execute? | follow-ups |
| `list_players_for(play_id)` | Who executes this play? | follow-ups |
| `find_in_administration(admin_id, play?)` | Slice by admin, optionally filter by play. | Prompt 1 |
| `enrich_from_littlesis(person_label_or_id)` | Bridge to the LittleSis MCP for outside relationships. | optional |

## Publishing the demos

The three prompts go on `evilrobots.lol/tech/ratchet-mcp/` with:

1. The prompt verbatim
2. A Claude Desktop screenshot of the actual response
3. The tool-call trace (collapsed, expandable)
4. A link to the relevant book chapter
5. The "install this yourself" CTA pointing at the docker-compose

The screenshots are the X-card hero images. Demo 3 is the headline post.

## Why exactly these three

- **Prompt 1** demonstrates the **filter** verb (`query_cohort`). Most-common usage pattern.
- **Prompt 2** demonstrates the **traversal** verb (`who_connects`). Showcases the graph being a graph, not a table.
- **Prompt 3** demonstrates the **intersection** verb (`find_overlap`). Operationalizes the book's thesis. Hardest hit.

If the demo gallery grows to 5+, add: a `list_players_for` (the staffing-play roster), a `find_in_administration` (admin slice), and a Wikidata cross-check showing the MCP's data agrees with external sources.
