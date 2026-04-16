# Infrastructure Map — Mircea's Constellation

> **Governed by UrantiOS v1.0 — Truth · Beauty · Goodness**
> **Updated:** 2026-04-12

---

## Servers

### OpenClaw VPS (Primary Worker)

```
IP:       46.225.51.30
SSH:      ssh root@46.225.51.30
Provider: Hetzner Cloud
Type:     CPX22
RAM:      8 GB
Disk:     80 GB SSD (46% used)
Location: Nuremberg, Germany
OS:       Linux
```

**Hosts:**
- NemoClaw stack (n8n + PostgreSQL + Redis + Paperclip)
- OpenClaw bot fleet (9–10 Telegram bots)
- nginx reverse proxy (added 2026-04-12)

### URANTiOS Prime (AI + Publishing)

```
IP:       204.168.143.98
SSH:      ssh root@204.168.143.98
Provider: Hetzner Cloud
Type:     CCX23
RAM:      16 GB
Disk:     160 GB SSD (38% used)
Location: Helsinki, Finland
OS:       Linux
```

**Hosts:**
- NanoClaw v1.2.17 (Claude SDK Telegram agent)
- Gabriel Brain (:18900) — Bright and Morning Star
- Ollama (qwen2.5:32b) — local AI
- UrantiPedia (.org + .com) — 196 papers, 477 personalities

### iMac M4 (Controller)

```
User:      mircea8me.com
Tailscale: 100.75.177.36
Role:      Controller, Obsidian vault, AMEP Hub
```

**Hosts:**
- Obsidian knowledge vault (this repo)
- AMEP Hub (:18802) — 21 students
- Fleet dashboard (:18801)
- Local Claude Code sessions

---

## Telegram Bots

| Bot | Handle | Role | Server |
|-----|--------|------|--------|
| Hetzy PhD | @Hetzy_PhD_bot | Fleet Commander — autonomous 30min cycles | OpenClaw |
| NanoClaw | @nanoclaw_openclaw_bot | Claude SDK agent | URANTiOS |
| UrantiPedia Agent | @UrantiPedia_Agent_01_bot | Gateway to UrantiPedia | OpenClaw |
| Bot Fleet (8 more) | various | Mission agents | OpenClaw |

Total bots: **11** (10/11 active as of 2026-04-12)

---

## Network Topology

```
 iPhone 16 Pro Max
        │
        ├──────────────────┐
        ▼                  ▼
   iMac M4            Bot Fleet (Telegram)
  (Controller)              │
     │   │                 │
     │   └─────────────────┤
     ▼                     ▼
 OpenClaw (46.225.51.30) ◄─── URANTiOS (204.168.143.98)
  ├── NemoClaw (n8n)          ├── NanoClaw
  ├── Bot Fleet               ├── Gabriel
  └── nginx :80               ├── Ollama
                              └── UrantiPedia
```

---

## Key Internal Ports

| Server | Port | Service |
|--------|------|---------|
| OpenClaw | 18789 | OpenClaw API |
| OpenClaw | 18791 | OpenClaw secondary |
| OpenClaw | 18792 | OpenClaw tertiary |
| OpenClaw | 5678 | n8n (localhost → port 80 via nginx) |
| OpenClaw | 5432 | PostgreSQL (localhost) |
| OpenClaw | 6379 | Redis (localhost) |
| OpenClaw | 80 | nginx → n8n |
| URANTiOS | 18900 | Gabriel Brain |
| iMac | 18800 | Main dashboard |
| iMac | 18801 | Fleet Bus |
| iMac | 18802 | AMEP Hub |

---

## Setup Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| claws_boot.sh | mircea-constellation/setup/ | Full boot from iMac — fixes all Claws |
| openclaw_fix.sh | mircea-constellation/setup/ | nginx fix for NemoClaw n8n |
| m1_terminal.sh | mircea-constellation/setup/ | iMac dev environment setup |
| m1_terminal.sh | lobsterbot/setup/ | LobsterBot dev setup |

### One-Command Boot

```bash
# Run from iMac Terminal to fix and verify all Claws:
bash <(curl -fsSL https://raw.githubusercontent.com/MyEduGit/mircea-constellation/claude/count-claws-NrqRh/setup/claws_boot.sh)
```

---

## Related

- [[00_CLAWS_MASTER]] — Claws overview
- [[OpenClaw]] — primary worker server
- [[NemoClaw]] — n8n automation
- [[NanoClaw]] — Claude SDK agent
- [[Session_2026-04-12]] — today's work log
