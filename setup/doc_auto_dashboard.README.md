# `doc_auto_dashboard.sh` — Truth Report

Shipped verbatim from the user-supplied snippet (2026-04-14 16:38 AEDT).
The script works as a scaffold, but three behaviours will bite on first
real run. Documenting here so they get fixed deliberately, not silently.

## Issue 1 — Master Mermaid becomes invalid after first job

The installer appends:

```text
%% Job: <slug> added ...
    click G href "..." "Open GitHub folder for <slug>"
    click N href "..." "Open Notion page for <slug>"
```

after the last line of `master_pipeline.mmd`. Two problems:

1. `click` statements must live **inside** the `flowchart TD` block that
   declared the node IDs they reference. Appending below the closing of
   the diagram leaves them outside the parse scope in strict renderers.
2. Every job reuses the same node IDs `G` and `N`, so the Mermaid
   renderer will overwrite the click binding on each append — only the
   most recent job will be clickable.

**Fix options:**

- Insert clicks before the last line of the diagram using `sed -i` with
  a marker comment like `%% CLICKS_BELOW`.
- Use unique node IDs per job: `G_<slug>` and `N_<slug>`, and add the
  actual nodes (not just clicks) to the diagram.
- Or regenerate `master_pipeline.mmd` from a template + a `jobs.json`
  manifest on every run instead of appending.

## Issue 2 — GitHub link points at the wrong repo

```bash
VAULT_DIR=~/Documents/Obsidian/PhD-Triune-Monism
GITHUB_REPO="myedugit/mircea-constellation"
```

The script commits inside the PhD-Triune-Monism vault but generates
click URLs pointing at `mircea-constellation` — the tree path will
404. Set `GITHUB_REPO="myedugit/phd-triune-monism"` unless there is an
intentional reason to link users to a different repo.

## Issue 3 — Notion page creation is an echo, not an API call

```bash
echo "[✓] Notion page created for $JOB_SLUG under parent $NOTION_PAGE_ID"
```

No page is actually created. Every job's Notion click link points at
the same parent page until a real MCP call (or `curl` to the Notion
API) replaces this line. The claim in the script output is louder than
the truth on the wire — fix before the script is wired to anything
visible.

## Minor

- `git commit` will fail if there is nothing staged; script does not
  check `--allow-empty` or branch status. On the first run with
  pre-existing changes it may commit more than just the job folder.
- `GITHUB_BRANCH="claude/claude-usage-guide-mtE8j"` is hard-coded; this
  branch is `claude/multi-ai-obsidian-integration-jkoI9`. Confirm which
  branch should be the live dashboard target.
- No `set -euo pipefail` — a failure mid-script is silent.

## When these are fixed, delete this file.
