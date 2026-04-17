---
job: multi-ai-obsidian-integration-dryrun
date: 2026-04-14
ai_sources: [ChatGPT, Claude Code, Grok, Gemma4]
status: draft
github_commit: pending
notion_url: pending
zapier_fanout: skipped
---

# Multi-AI Obsidian Integration — Dry-Run Job

## Goal

Validate the DOC pipeline end-to-end using Claude Code as the first
AI source. Prove the scaffold, not the full integration.

## What this commit actually did

- [x] Created the canonical folder layout under `2026-04-14/<job-slug>/`.
- [x] Dropped Mermaid source at `assets/multi-ai-obsidian-integration-dryrun.mmd`.
- [x] Seeded `scripts/install.sh`, `scripts/validate.sh`,
      `hooks/doc-reminder.sh`, `hooks/doc-verify.sh`.
- [x] Pushed branch `claude/multi-ai-obsidian-integration-jkoI9` to
      `myedugit/phd-triune-monism`.
- [x] Added root `master_pipeline.mmd` with live GitHub / Notion links.

## What this commit did NOT do (Truth Report)

- [ ] Render SVG or PNG from the Mermaid source. Requires `mmdc`
      installed on the host; `validate.sh` will do it when run locally.
- [ ] Create a Canva diagram. Canva MCP is available but not invoked
      until a brand-kit target is confirmed.
- [ ] Create the Notion page. Deferred until the Sovereign Dashboard
      parent ID is written into secrets.
- [ ] Fire the Zapier webhook. `ZAPIER_WEBHOOK_URL` is unset.
- [ ] Replicate to the other three repos (mircea-constellation,
      lobsterbot, URANTiOS). Deferred until this dry-run validates.

## Diagram

Source: `assets/multi-ai-obsidian-integration-dryrun.mmd`

Rendered outputs (run `scripts/validate.sh` to produce):

- `assets/multi-ai-obsidian-integration-dryrun.svg`
- `assets/multi-ai-obsidian-integration-dryrun.png`
- `assets/multi-ai-obsidian-integration-dryrun-canva.png` (optional)

## Links

- Master pipeline: `../../master_pipeline.mmd`
- Architecture: `../../ARCHITECTURE.md`
- Branch: `claude/multi-ai-obsidian-integration-jkoI9`

## Next actions (in order)

1. On iMac M4: `cd <vault> && bash 2026-04-14/multi-ai-obsidian-integration-dryrun/scripts/install.sh`
2. Then: `bash 2026-04-14/multi-ai-obsidian-integration-dryrun/scripts/validate.sh`
3. Confirm SVG + PNG exist, commit them.
4. Wire Notion page creation; paste live URL into `notion_url` frontmatter.
5. Replicate layout to the other three repos on the same branch.
