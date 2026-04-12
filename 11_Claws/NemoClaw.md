# NemoClaw

> **Status:** ✅ Active
> **Server:** 46.225.51.30 (OpenClaw VPS) — Nuremberg, DE
> **Stack:** n8n + PostgreSQL + Redis + Paperclip (Docker Compose)
> **Governed by UrantiOS v1.0**

---

## Identity

NemoClaw is the automation and orchestration layer. It runs **n8n** — a visual workflow automation engine — along with its supporting database and cache. NemoClaw is the control brain: it can SSH into servers, call APIs, trigger bots, and orchestrate everything else.

Named after Nemo — the one who navigates the deep.

## Role in the Constellation

NemoClaw is the **recommended first Claw to fix** because:
- n8n can automate the setup of all other Claws
- It already contains the **Council of Seven Master Spirits** workflow
- It can be used to build InstantlyClaw and FireClaw from within
- It connects to Obsidian, Telegram, APIs, and servers

## Access

| Method | URL / Command |
|--------|---------------|
| Web UI (after nginx fix) | http://46.225.51.30 |
| SSH Tunnel (old method) | `ssh -L 5678:127.0.0.1:5678 root@46.225.51.30` then http://127.0.0.1:5678 |
| Direct (server only) | http://127.0.0.1:5678 |

## Nginx Fix (applied 2026-04-12)

n8n was originally bound to `127.0.0.1:5678` (localhost only). Fixed by installing nginx as a reverse proxy on port 80.

Setup script: `setup/openclaw_fix.sh` in mircea-constellation repo.

```bash
# Run from iMac to fix NemoClaw
bash <(curl -fsSL https://raw.githubusercontent.com/MyEduGit/mircea-constellation/claude/count-claws-NrqRh/setup/claws_boot.sh)
```

## Docker Stack

```yaml
# Containers in the NemoClaw stack:
nemoclaw-n8n        # n8n workflow engine (n8nio/n8n:latest)
nemoclaw-bot        # Telegram bot companion
nemoclaw-postgres   # PostgreSQL 15 — n8n database
nemoclaw-redis      # Redis 7 — queue and cache
nemoclaw-paperclip  # Node 22 — file handling
```

## Key Workflows in n8n

| Workflow | Purpose | File |
|----------|---------|------|
| **Council of Seven Master Spirits v1** | 7 AI seats + Gabriel synthesizer | `council/council_of_seven_v1.n8n.json` |

Import: n8n → Workflows → New → `...` → Import from JSON → paste workflow file content.

Full docs: [[Council_of_Seven]]

## Integration Points

- **Obsidian**: via Local REST API plugin (planned)
- **Telegram**: via bot webhook
- **OpenAI / Claude**: via API credentials
- **OpenClaw bots**: via internal API calls
- **URANTiOS**: via SSH or HTTP

## Related

- [[OpenClaw]] — the server that hosts NemoClaw
- [[Session_2026-04-12]] — access fix and nginx setup
