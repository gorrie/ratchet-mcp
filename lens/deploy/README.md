# Tradecraft Lens — local self-host

One command, no public host, no cloud account required.

```bash
cd research/ratchet-mcp/lens/deploy
docker compose up --build           # starts ollama + the lens backend
# one-time, in another terminal — pull a local model for the grading backend:
docker compose exec ollama ollama pull qwen2.5:14b
# then open:
open http://localhost:8770          # paste text -> method reading + receipts
```

## Backends (pick one)

- **Local (no key):** the `ollama` service grades offline. After `ollama pull qwen2.5:14b`, the Lens'
  `backend=auto` falls through to it. Fully self-contained.
- **Cloud (sharper reads):** set `OPENROUTER_API_KEY` (env or a `.env` beside the compose file). `auto`
  prefers it. This is the same channel the bias study uses.

The deterministic **`cues`** floor needs no model at all (offline) — useful for a smoke test, but it is
a detector, not a publishable grader (see the verifier note in the build plan).

## What it serves

- `GET  /`            — the Lens UI (`lens.html`)
- `POST /grade-text`  — `{ "text": "...", "backend": "auto|cloud|local|cues" }` → per-lens index/tier + receipts
- `GET  /healthz`

## Going public

This bundle is the deploy vehicle. For a public endpoint, run it behind a reverse proxy (TLS +
`ALLOWED_ORIGIN`/CORS already permissive for demo), point `website/content/tech/tradecraft.md` at the
`/grade-text` URL, and unpark the page. Host + secrets are the only author decisions; the container is
the rest.
