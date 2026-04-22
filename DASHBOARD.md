# PhD-Triune-Monism — Live Status Dashboard

**Generated:** 2026-04-14 by Claude Code (GitHub MCP + terminal verification)  
**Principle:** every row below is backed by a commit, a log line, a file, or a verifiable absence. Nothing on this page is narrated.

---

## 1. Vault

| Item | Value |
|---|---|
| Repo | `MyEduGit/PhD-Triune-Monism` |
| Active branch | `claude/multi-ai-obsidian-integration-jkoI9` |
| Installer-authored tip | `cb1ef55` |
| Latest commit | `8167ff3` (hand-authored, not installer-produced) |

---

## 2. Phase A Dry-Run — FAILED (7 attempts)

All seven runs are recorded in `StressTestLogs/`. Nothing here is interpretation — quotes are from the log files in commit `8167ff3`.

### Open bug A — `flock` broken on macOS
- First run: `setup/doc_auto_dashboard.sh: line 86: flock: command not found`
- Last run (after a Homebrew attempt): `/usr/local/bin/flock: line 2: exec: gflock: not found`
- Impact: the locked region dies under `set -e`, so the manifest update and master-pipeline regen never run to completion.

### Open bug B — Mermaid source is malformed
- Log `phase-a-dryrun-01_20260414_132043.log`:  
  `Error: Lexical error on line 2. Unrecognized text. ...oc phase-a-dryrun-01] --> B[Create job f`
- Cause: `A[/doc $JOB_SLUG]` — Mermaid reads `[/` as the start of a trapezoid shape.
- Impact: `mmdc` fails on every run; no SVG, no PNG.

### Open bug C — repo hygiene
- `.doc.lock` is committed (it is a runtime flock file; should be in `.gitignore`).
- A file literally named `Auto-updating` is committed at repo root.
- The installer never adds either; both came from a manual `git add .`.

### What landed
- `2026-04-14/phase-a-dryrun-01/job.md` (391 B)
- `2026-04-14/phase-a-dryrun-01/assets/phase-a-dryrun-01.mmd` (163 B, but malformed per bug B)
- 7 StressTestLogs files

### What did NOT land
- `setup/jobs.json` is still `[]` — the manifest-update path never completed.
- `master_pipeline.mmd` has the jobs-section header comment but zero job entries.
- `master_pipeline.svg` / `.png` were never produced.

---

## 3. Hetzner Claw Fleet — UNVERIFIED

No ground truth has been produced for the claw fleet, inside this repo or in any terminal output I have seen. Specifically missing:

- [ ] Hetzner VPS hostname / IP / project ID
- [ ] `tailscale status` output showing claw hosts
- [ ] `docker ps` from any claimed host
- [ ] Log lines authored BY a claw (not ABOUT one)
- [ ] Commits authored by any claw service account

Until one of the above lands, all claw-dependent operations are unsubstantiated. No dashboard row for them can be filled in honestly.

**Minimum check (5 min in a browser):** log into [console.hetzner.com](https://console.hetzner.com), list the servers in the project, and paste: server names, IPs, running state, monthly cost.

---

## 4. Peer repos

| Repo | Branch tip | Scaffold | PR |
|---|---|---|---|
| `mircea-constellation` | `0dc3813b` | pushed | #3 open |
| `lobsterbot` | `b87cade2` | pushed | #3 open |
| `URANTiOS` | `095c44c2` | pushed | #3 open |
| `phd-triune-monism` | `8167ff3` | Phase A failed 7x | #3 open |

---

## 5. What can happen in the next hour (copy-paste ready)

Three independent, actionable steps. Run any or all.

### Step 1 — Gemma 3 locally on iMac_M4 (no Hetzner needed)

```bash
# install once
brew install ollama
brew services start ollama

# pull a real model (Gemma 3 4B, ~3 GB)
ollama pull gemma3:4b

# talk to it
ollama run gemma3:4b
```

> Note: `gemma4` is not a real Ollama model. `gemma3` is.

### Step 2 — Patch the installer bugs

Reply `patch` in Claude Code and a single commit with Fix A + Fix B + Fix C will land on this branch. Then re-run `bash setup/doc_auto_dashboard.sh phase-a-dryrun-02` on iMac_M4 and paste the raw log. If `jobs.json` grows from `[]` to one entry and the master gets a job node, Phase A is genuinely verified — no narrative, just diff.

### Step 3 — Hetzner ground truth

Open [console.hetzner.com](https://console.hetzner.com), list servers, paste here. If there are none, we stop paying. If there are some, we wire them up properly with real hostnames and a tested SSH path.

---

## 6. What this dashboard is NOT

This page does not claim the claw fleet works.  
It does not claim Phase A succeeded.  
It does not claim dashboards exist elsewhere.  
When any of those become verifiable, this page updates.

*Rebuilt from live GitHub state. Change it by changing reality, not by editing prose.*
