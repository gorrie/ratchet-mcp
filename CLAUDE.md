# CLAUDE.md — ratchet-mcp

## Git identity — CRITICAL
This project publishes to **github.com/gorrie/ratchet-mcp** (PUBLIC author account).
ALL commits MUST be **gorrie**. Never use a machine-default identity and never any non-gorrie
identity on this repo.

In EVERY clone, set LOCAL config (never `--global`) before committing:
```
git config user.name  "gorrie"
git config user.email "4443401+gorrie@users.noreply.github.com"
gh auth switch --user gorrie
```

## Recurrence guard
Install a pre-commit hook that aborts the commit if `user.email` is not
`4443401+gorrie@users.noreply.github.com` — mirror the GitLab identity hook
(`eureka projects/install-identity-hook.sh`), swapping in the gorrie identity.
