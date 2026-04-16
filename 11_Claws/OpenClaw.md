# OpenClaw

> **Status:** ✅ Active
> **Server:** 46.225.51.30 — Hetzner CPX22 — Nuremberg, DE
> **Governed by UrantiOS v1.0**

---

## Identity

OpenClaw is the primary execution node. It hosts the bot fleet and the NemoClaw automation stack. It is the main worker server in the Constellation.

## Server Specifications

| Property | Value |
|----------|-------|
| IP | 46.225.51.30 |
| Provider | Hetzner Cloud |
| Type | CPX22 |
| RAM | 8 GB |
| Storage | 80 GB SSD |
| Location | Nuremberg, Germany |
| OS | Linux (Debian/Ubuntu) |
| Disk usage | 46% |

## Ports in Use

| Port | Service | Access |
|------|---------|--------|
| 18789 | OpenClaw API | Internal |
| 18791 | OpenClaw secondary | Internal |
| 18792 | OpenClaw tertiary | Internal |
| 5678 | n8n (NemoClaw) | localhost only → port 80 via nginx |
| 5432 | PostgreSQL (NemoClaw) | localhost only |
| 6379 | Redis (NemoClaw) | localhost only |
| 80 | nginx (n8n proxy) | Public (after fix) |

## What Runs Here

- **Bot fleet**: 9–10 active Telegram bots
- **NemoClaw stack**: n8n, PostgreSQL, Redis, Paperclip (Docker)
- **nginx**: Reverse proxy for n8n (added 2026-04-12)

## Docker Containers (as of 2026-04-12)

| Container | Image | Status |
|-----------|-------|--------|
| nemoclaw-n8n | n8nio/n8n:latest | Up |
| nemoclaw-bot | nemoclaw-bot | Up |
| nemoclaw-postgres | postgres:15-alpine | Up |
| nemoclaw-redis | redis:7-alpine | Up |
| nemoclaw-paperclip | node:22-alpine | Up |

## SSH Access

```bash
ssh root@46.225.51.30
```

## Related

- [[NemoClaw]] — automation stack running on this server
- [[Infrastructure_Map]] — full network diagram
- [[Session_2026-04-12]] — nginx fix applied
