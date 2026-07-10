# OSINT restraint — the public-footprint standard

This project maps an apparatus of **public figures acting in public roles**. It is a restrained
Maltego, not a target package. The point is the *method and the record* — what someone said, where
they worked, who they are connected to, all addressable and sourced.

**The line is PURPOSE and CONTENT TYPE, not access difficulty.** Content that is addressable — it has
a URL, it is a known published artifact — is published content, fetched however it must be (an open
API, or an authenticated read of login-walled public content). That is documentation. What we do not
*assemble* is a **locate-and-harass kit**: home, kids, private contact, real-time movements — not
because that data is hard to get, but because publishing it serves targeting, not the record.

This is the **default floor**, not an absolute. Genuinely newsworthy non-public material is an
editorial call made in context, with sourcing — the way investigative outlets (Bellingcat, 404 Media,
Unicorn Riot) routinely go far further, publishing leaked data and identifying individuals. We sit
well short of that, by choice; the floor below just says where the default sits and why.

## What may be recorded

- **The subject's own addressable accounts and statements** — any X / Bluesky / Mastodon / LinkedIn /
  personal-site / Substack content the subject themselves authored (professional or
  personal-but-published), **after the correctness gate confirms the account is theirs**
  (`x_ingest.py --verify` / `--verify-handle`: a wrong handle attributes a stranger — a correctness bug
  and a smear). Login-walled or authenticated-read content counts — it is still their published word.
- **Official affiliations** — employer, org, lab, board seat, the bio link on their own profile, a
  faculty/company page, congressional testimony, filings.
- **On-the-record statements + documented connections** — speeches, posts, op-eds, testimony, funding
  ties, edges, each with a source URL receipt.

## The floor (what we don't assemble — the locate-and-harass kit)

These serve targeting, not documentation, so they stay out by default:

- **Family.** Spouse's name/workplace, partner, children, children's school — unless that family member
  is independently a public actor in the matter.
- **Home / real-time location.** Home address, neighborhood, daily schedule, routes, "where they'll be."
- **Private contact + correspondence.** Personal phone, personal email, DMs / private messages.
- **Derived-to-locate data.** Anything whose purpose is to find or physically reach the person.
- **Relatives-of framing.** A person is in scope for *their own* role, not as someone's relative.

The distinction from access, made concrete: a *locked account's* public-professional posts are the
subject's published word (in — gate first); a person's *home address* is a locate kit (out) — even if
both happened to take a login to see.

## Test before adding anything

1. **Is it the subject's own addressable content or a documented connection?** (URL / source receipt.)
   If it's private personal/family/locating data, that's the floor — stop, unless there's a documented
   public-interest reason taken as a deliberate editorial call.
2. **Did the correctness gate pass?** Account confirmed to the right person? If not, stop.
3. **Does it serve the record, or targeting?** If its purpose is to help someone locate, reach, or
   harass them or their family, it's out — regardless of how public it technically is.

## Access mechanism: observatory accounts

Walled gardens (Instagram, Facebook, LinkedIn, X-behind-login) gate published content behind a login.
The access path is a **logged-in viewing identity** — the author's **personal account where the
platform's ToS permits** logged-in reading, or a dedicated isolated **observatory account** where it
does not — used to *observe* public figures' walled-but-published content. Standard OSINT/journalism
tradecraft, and inside the standard: the account only views what it is permitted to view; the
**content-type floor still governs what we RECORD** (a walled post is the subject's published word —
in; their home address is a locate kit — out, whatever the account can see).

- **Accounts.** Personal account where ToS-compliant; a dedicated isolated observatory account where it
  is not (or where separation is preferred). Either way, credentials live off-repo (env / secrets
  store), never committed. (Public Bluesky/Mastodon/RSS need no account at all.)
- **ToS reality.** Authenticated observation breaks several platforms' ToS — an accepted, deliberate
  research risk, the author's call, not a technical question.
- **The one line that stays:** viewing a public figure's public-but-walled posts is *observation*;
  using an observatory account to *deceive a private individual into granting access* to their
  followers-only circle is *infiltration* — that's the floor, not the default.
