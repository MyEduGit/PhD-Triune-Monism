# `doc_auto_dashboard.sh` — Patch Status

All four originally-flagged issues are addressed in the current version
of `setup/doc_auto_dashboard.sh`. Kept here as an audit trail.

## Issue 1 — Master Mermaid invalid after first job

**Status:** PATCHED.

Old behaviour: appended `click G` / `click N` below the closing of the
diagram, reusing the same IDs, producing invalid Mermaid and
overwritten click bindings.

Fix: `master_pipeline.mmd` is now **regenerated** on every run from
`setup/master_pipeline.template.mmd` plus the `setup/jobs.json`
manifest. Each job gets a unique node ID derived from its slug
(`G_<slug_sanitized>`) and a `click` binding inside the flowchart
block. No more appends; no more ID collisions.

## Issue 2 — GitHub link pointed at wrong repo

**Status:** PATCHED.

Old default: `GITHUB_REPO=myedugit/mircea-constellation` with
`VAULT_DIR=.../PhD-Triune-Monism` — all tree URLs 404'd.

Fix: defaults are now
`GITHUB_REPO=myedugit/phd-triune-monism` and
`GITHUB_BRANCH=claude/multi-ai-obsidian-integration-jkoI9`. Both are
overridable via env. Click URLs resolve.

## Issue 3 — Notion page creation was an echo stub

**Status:** PATCHED.

Old behaviour: `echo "[✓] Notion page created ..."` — no API call.

Fix: when `NOTION_TOKEN` is set, the script now POSTs to
`https://api.notion.com/v1/pages` with the configured parent page ID
and reports the real HTTP status. When the token is absent, it prints
`NOTION_TOKEN not set — Notion page NOT created (honest skip)` and
moves on. Claim matches reality in both branches.

## Issue 4 — `canva-cli` was a phantom binary

**Status:** PATCHED.

Old behaviour: script called `canva-cli generate-design-structured`
which is not a real binary — Canva is an MCP tool, not a shell CLI.

Fix: the `canva-cli` call is removed. When `CANVA_FALLBACK=true` is
set, the script prints an honest note explaining that Canva must be
invoked from a Claude Code session via the
`generate-design-structured` MCP tool, and does nothing else. No more
false-success or confusing "CLI not available" messages.

## Concurrency (new)

- `set -euo pipefail` at the top.
- `flock -x` on `$VAULT_DIR/.doc.lock` around manifest update, master
  regen, Mermaid render, and the entire `git add/commit/push`
  sequence. Parallel runs now serialize on git and on the shared
  master file.
- `git commit` runs only if `git diff --cached` is non-empty. No empty
  commits, no accidental inclusion of unrelated staged work.
- All stdout/stderr is tee'd to
  `$VAULT_DIR/StressTestLogs/<slug>_<timestamp>.log` for audit.

## Remaining caveats (honest)

- Requires `jq` on PATH for manifest and master regen. Without it, the
  script prints a WARN and proceeds without updating the manifest.
- Requires `mmdc` for SVG/PNG. Without it, SVG/PNG are skipped with a
  log line; the scaffold still ships.
- `flock` is Linux/macOS; won't work on bare Windows shells.
- `GITHUB_BRANCH` default is this feature branch. Set
  `GITHUB_BRANCH=main` once the work is merged.
