---
name: ratchet-mcp-publish
description: Release a new version of the Ratchet MCP dataset + server to the public github.com/gorrie/ratchet-mcp repository. Codifies the canonical longitudinal release flow — the user re-samples the dataset periodically to measure bias drift in institutional staffing patterns, and each cut is published as a tagged release for peer-experiment reproducibility. Use this when the dataset has new persons / institutions / edges since the last public tag, or when a tooling change is ready to ship.
---

# ratchet-mcp-publish

The Ratchet MCP repo is **two trees that need to stay in sync**:

| Tree | Role |
|---|---|
| `evil-robots-series/research/ratchet-mcp/` (private GitLab, in the book repo) | Where the author works. Where `ratchet-add-person` and `ratchet-audit` skills run. Canonical source for all updates. |
| `github.com/gorrie/ratchet-mcp` (public GitHub) | Where peer experimenters and external readers go. Discrete tagged releases (v0.1, v0.2, …). Each tag pins a cut of the dataset for reproducibility. |

This skill is the bridge: it propagates a clean, secret-scrubbed, audit-passing
snapshot from the private tree to the public tree, tags it, and creates a
GitHub Release with the right release notes.

## TRIGGER when
- A meaningful number of additions to `server/data/*.jsonl` have landed since
  the last tagged release (a new cohort, batch addition, or v3+ cluster).
- The dataset has been re-sampled to extend the longitudinal time-series for
  measuring bias drift.
- A tooling change to `server/` or `web/` is ready to ship (new MCP tool,
  bug fix, license update).
- The book *The Ratchet* is about to publish and the README needs a
  matching reference revision.

## SKIP
- Mid-cycle drafts: only published when the citation audit passes locally
  AND on CI. Use the `ratchet-audit` skill first.
- Single-record fixes that don't move the dataset materially (those land in
  the private tree and get rolled into the next release).
- Forks / contributor branches: those go through PRs in the public repo,
  not through this skill.

## Preconditions
1. **`gh` CLI authenticated as `gorrie`**. The default account on this
   machine is `REDACTED`; switch with `gh auth switch -u gorrie`
   before running. Verify with `gh auth status --active`. After the
   release, switch back with `gh auth switch -u REDACTED`.
2. **Citation audit passes locally**: from `server/`, run
   `python tests/audit_citations.py`. Should print "All checks passed."
   If it fails, DO NOT proceed — fix the dataset first, that's the
   whole point of the discipline.
3. **No uncommitted changes** in the private tree's ratchet-mcp subdir
   (`git status -s research/ratchet-mcp/` from the book repo root). The
   private tree is the source of truth; if it has unstaged work the
   release will lose it.
4. **Current dataset counts known**: run the inline counts probe in
   step 1 so the release notes are accurate, not aspirational.

## Procedure (verified before the next — no walk-away)

### 1. Audit + count

```bash
SRC=/path/to/evil-robots-series/research/ratchet-mcp
cd "$SRC/server"
python tests/audit_citations.py
# Expected: "Audited N people, M institutions, K edges. All checks passed."
# If anything else: fix it, don't bypass it.

python -c "
import json
n_p = sum(1 for _ in open('data/people.jsonl'))
n_i = sum(1 for _ in open('data/institutions.jsonl'))
n_e = sum(1 for _ in open('data/edges.jsonl'))
print(f'persons={n_p} institutions={n_i} edges={n_e}')
"
```

Record these numbers — they go in the README, the release notes, and the
"What's in it" section. The README counts MUST match the data files;
stale counts in the README are the kind of trust-eroding drift this
skill exists to prevent.

### 2. Refresh README + Status block

If counts changed since the last release, edit `README.md`:

- Top "What's in it" bullets: update persons / institutions / edges.
- "Status" block: bump version, set release date, note what's new.

### 3. Stage a clean public-release tree

```bash
PUB=/tmp/ratchet-mcp-public
rm -rf "$PUB" && mkdir -p "$PUB"
rsync -a \
  --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='.pytest_cache' --exclude='.DS_Store' \
  "$SRC/" "$PUB/"
```

Then secret-scan:

```bash
grep -rE "sk-or-v1-|sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AIza[a-zA-Z0-9]{20,}|hf_[a-zA-Z0-9]{20,}" "$PUB" 2>/dev/null \
  && { echo "FOUND SECRET-SHAPED STRING — DO NOT PUSH"; exit 1; } \
  || echo "clean"
```

If ever a secret-shaped string appears, **stop and investigate**. The skill
does not auto-redact.

### 4. Sync to the public clone

For a **first release** (no public repo yet):

```bash
gh auth switch -u gorrie
cd "$PUB"
git init -b main
git config user.name "gorrie"
git config user.email "4443401+gorrie@users.noreply.github.com"
git add . && git commit -m "v0.1: initial public release ..."
gh repo create gorrie/ratchet-mcp --public --description "..." --source . --remote origin --push
gh auth setup-git  # so subsequent git push uses gorrie's token, not REDACTED
```

For **subsequent releases** (repo exists):

```bash
gh auth switch -u gorrie
cd /tmp
rm -rf ratchet-mcp-public-clone
gh repo clone gorrie/ratchet-mcp ratchet-mcp-public-clone
cd ratchet-mcp-public-clone

# Mirror the new tree onto the existing clone. --delete keeps it a clean
# mirror so files removed from the source go away in the public repo too.
rsync -a --delete \
  --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
  --exclude='.pytest_cache' --exclude='.DS_Store' \
  "$SRC/" "./"

git add -A
git status --short  # surface what's changing
git commit -m "vX.Y.Z: <release headline>"
git push origin main
```

### 5. Tag + release

```bash
git tag -a vX.Y.Z -m "vX.Y.Z release. <counts> persons / <counts> institutions / <counts> edges."
git push origin vX.Y.Z

gh release create vX.Y.Z \
  --title "vX.Y.Z — <headline>" \
  --notes "$(cat <<'EOF'
<headline>.

Dataset: N persons / M institutions / K edges.
Changes since vX.Y.Z-1:
  - new cohort: ...
  - new institution cluster: ...
  - tooling: ...

Every record cites >= 2 primary sources; CI gates the discipline.

Reproducibility note: this is a longitudinal release. Pin this tag to
reproduce a specific cut. The time-series of cuts is itself the
bias-drift instrument.
EOF
)"
```

### 6. Verify CI runs green

```bash
sleep 10
gh run list --repo gorrie/ratchet-mcp --limit 1
# Expect: completed success on the just-pushed commit + tag.
# If failure, read the logs and fix in the private tree, then re-run from step 1.
```

### 7. Switch gh back + commit the private-tree changes

```bash
gh auth switch -u REDACTED

cd "$SRC/../.."  # the book repo root
git add research/ratchet-mcp/README.md research/ratchet-mcp/server/pyproject.toml
git commit -m "ratchet-mcp: vX.Y.Z release prep (README counts, ...)"
git push origin master
```

The private-tree changes are what made the public release possible; keep
them committed so the next release starts from a consistent base.

## Recovery from failure

| Symptom | Cause | Fix |
|---|---|---|
| `gh repo create` says "X cannot create a repository for gorrie" | gh is authenticated as the wrong account | `gh auth switch -u gorrie` and retry. After the release, switch back. |
| `git push origin v0.1` returns "Permission to gorrie/ratchet-mcp.git denied to REDACTED" | git's credential helper has the wrong account stored for github.com | `gh auth setup-git` while authenticated as `gorrie` rewrites the helper to use the gorrie token. |
| CI fails on `setuptools.errors.DistutilsOptionError: Cannot access '/home/runner/work/.../server/../README.md'` | `server/pyproject.toml` references `../README.md` which setuptools won't read outside the package root | Inline the description in pyproject.toml (`description = "..."`) and remove the `readme = "../README.md"` line. |
| Audit fails locally with `Citation count < 2 for person X` | a new record was added without the discipline | Add the second primary source to that record before publishing. Never bypass the audit. |
| Secret scan finds a hit | almost always a false-positive on a URL (the `task-force-coordinator-dr-deborah-birx-testify` URL hits the `sk-` pattern in `task-force`) | Read the context; if it's a URL, the scan can be tightened to require word boundaries on the prefix. If it's actually a key, **do not push** — rotate the key and remove the file. |

## Hard lessons (do not relearn)
- **The two trees diverge unless the publish skill runs them together.** The
  README in the private tree was stale by 20+ commits (still claiming 117
  persons when the data was at 401) because release was a one-shot, not a
  repeatable workflow. The skill is the workflow.
- **gh authenticates as `REDACTED` by default on this machine.** Every
  release sequence must include the auth-switch dance and switch back at
  the end. Leaving the active account on gorrie pollutes subsequent
  REDACTED / REDACTED work with the wrong identity.
- **`server/pyproject.toml` cannot reference parent-of-package README.md.**
  Setuptools blocks it for security. Inline the description there; the
  full README ships in the repo root unchanged.
- **The release is the experiment artifact.** Peer experimenters cite
  `v0.1` to reproduce; if a record changes silently between cuts the
  time-series isn't a measurement anymore. Tag every release. Never
  rewrite history on a tagged commit.

## Cross-references
- Sibling skills in this repo: `ratchet-add-person` (single-record addition
  with audit) and `ratchet-audit` (run the citation + defamation gates
  locally). This skill is what fires AFTER both pass and a meaningful
  amount of new data has accumulated.
- Public destination: `https://github.com/gorrie/ratchet-mcp` —
  releases page at `/releases`.
- Book companion: *The Ratchet: How Safety Infrastructure Became the
  Control Grid* (Evil Robots Series Book 2, 4LULZ). The book ships with
  a specific version reference; the dataset continues past book publish
  as the longitudinal bias-drift instrument.
- Related operator agent: `convergence-updater` in the book repo at
  `evil-robots-series/.claude/agents/` is the periodic-update side of
  the longitudinal cadence — it runs on schedule to refresh data; this
  skill is what publishes the result.
