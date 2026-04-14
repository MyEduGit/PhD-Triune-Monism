---
name: doc
description: Creates a /doc job in the PhD-Triune-Monism Obsidian vault. Scaffolds the date/slug folder, writes job.md with YAML frontmatter, generates a Mermaid diagram, regenerates master_pipeline.mmd from template + jobs.json, commits to the active feature branch. Optionally invokes the Canva MCP tool to render a branded PNG, and the Notion MCP tool to create a page under the Sovereign Dashboard. Invoke as `/doc <job-slug>`.
---

# /doc skill — hybrid shell + MCP

## When to run

User types `/doc <slug>` (e.g. `/doc telegram-bot-redesign`). Slug must
match `[a-z0-9-]+`.

## Steps

1. **Shell phase (filesystem + git + REST).**
   Run from the vault root:
   ```
   bash setup/doc_auto_dashboard.sh <slug>
   ```
   This creates the job folder, updates `setup/jobs.json`, regenerates
   `master_pipeline.mmd`, commits, pushes. If `NOTION_TOKEN` is set,
   it also POSTs to the Notion REST API. If `ZAPIER_HOOK_URL` is set,
   it fires the webhook.

   Report the tail of `StressTestLogs/<slug>_<ts>.log`. Do not claim
   success for any step the log does not verify.

2. **Canva MCP phase (optional).**
   If the user asked for a Canva diagram or `CANVA_FALLBACK=true` is
   in the environment, invoke the Canva MCP tool
   `generate-design-structured` with the job's Mermaid source as
   input. Save the output to
   `<today>/<slug>/assets/<slug>-canva.png` in the vault. Git-add
   and commit the PNG as a follow-up.

3. **Notion MCP phase (optional, only if NOTION_TOKEN was not used).**
   If step 1 honest-skipped Notion (`NOTION_TOKEN not set`) but the
   user wants a page, use the Notion MCP tool `notion-create-pages`
   to create a child page under parent
   `3328525a-b5a0-815d-886c-d5488593aa3d`. Title: `<slug> — <date>`.
   Body: contents of `job.md`. Record the page URL.

4. **Completion.**
   Update the job's `job.md` frontmatter `status: active` →
   `status: complete`. Commit and push. Report to the user:
   - vault job path
   - github commit SHA
   - notion page URL (if created)
   - canva png path (if created)
   - zapier result (if fired)
   Anything not verified from a tool result stays unreported.

## Honesty rules (UrantiOS Lucifer Test)

- Do not echo `[✓]` for a step that did not produce evidence.
- If a tool errors, include the error in the user-facing summary.
- If the user asks for Canva but the MCP server is disconnected,
  say so and stop — do not fall back to a shell `canva-cli` (no
  such binary exists).
