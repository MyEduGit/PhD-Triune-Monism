# NemoClaw Observer — Mission Control Dashboard Agent

**Agent type:** Open Claw (Monitoring + Reporting)  
**Operated by:** Jabbok River Productions  
**Eternal Automation Directive:** Active — functions without operator presence

---

## What It Does

NemoClaw Observer is an automated monitoring agent that checks every layer of the
Mircea/JRP mission stack every 6 hours and produces a plain-language dashboard.
It sends the dashboard to Telegram, stores each snapshot in PostgreSQL, and fires
alerts if anything goes wrong.

Designed so a 70-year-old reader can understand every line without jargon.

---

## Stack Layers Monitored

| # | Layer | What is checked |
|---|---|---|
| 1 | VPS (Hetzy 46.225.51.30) | n8n, PostgreSQL (amep_schema_v1), Redis, Qdrant (havona_records_v2) |
| 2 | Local (iMac M4 / NemoClaw) | Ollama models: phi3:14b, deepseek-r1:8b, qwen3:8b |
| 3 | Agents | OpenClaw agents + n8n active workflows |
| 4 | LLMs in use | Z.ai GLM-5.1 spend guard ($5/month hard cap) |
| 5 | Connected apps | Telegram bot (@hetzy_phd), Qdrant API, PostgreSQL port |

---

## Dashboard Output (sample)

```
## NemoClaw Mission Dashboard
**Generated:** 2026-04-13 11:47:00 AEDT

### HEALTHY | WARNING | ERROR

| Layer | Service     | Status | Note                              |
|-------|-------------|--------|-----------------------------------|
| VPS   | n8n         | ✅      | n8n reachable                     |
| VPS   | PostgreSQL  | ✅      | amep_schema_v1 connected          |
| VPS   | Redis       | ✅      | 42.3 MB used                      |
| VPS   | Qdrant      | ✅      | 18421 vectors — havona_records_v2 |
| Local | Ollama      | ⚠️      | Missing: deepseek-r1:8b           |
| App   | Telegram Bot| ✅      | @hetzy_phd_bot online             |
| LLM   | Z.ai GLM-5.1| ✅      | $1.20 / $5.00 — SAFE             |

### SPEND SUMMARY
- Z.ai GLM-5.1: $1.20 / $5.00 — SAFE
- Gemini 2.5 Flash: $0.00 (free API)
- Groq (NanoClaw): $0.00 (free tier)
- Ollama (local iMac M4): $0.00
```

---

## Files

| Repo | File | Purpose |
|---|---|---|
| mircea-constellation | `nemoclaw_observer/observer.py` | Core monitoring agent |
| mircea-constellation | `nemoclaw_observer/schema.sql` | PostgreSQL table + views |
| mircea-constellation | `nemoclaw_observer/n8n_cron_workflow.json` | n8n scheduled run |
| mircea-constellation | `nemoclaw_observer/config.env.example` | All env vars documented |
| lobsterbot | `nemoclaw_observer/telegram_handler.py` | `/dashboard` Telegram command |
| lobsterbot | `nemoclaw_observer/observer.py` | Standalone copy for VPS deploy |

---

## Deployment Steps (Hetzy VPS)

**Step 1 — Install**
```bash
cd /opt
git clone https://github.com/MyEduGit/mircea-constellation.git nemoclaw
pip3 install -r /opt/nemoclaw/nemoclaw_observer/requirements.txt
```

**Step 2 — Configure**
```bash
cp /opt/nemoclaw/nemoclaw_observer/config.env.example /opt/nemoclaw/.env
nano /opt/nemoclaw/.env   # fill in PG_DSN, TELEGRAM_TOKEN, TELEGRAM_CHAT
```

**Step 3 — Create database table**
```bash
psql -h 46.225.51.30 -U postgres amep_schema_v1 \
  -f /opt/nemoclaw/nemoclaw_observer/schema.sql
```

**Step 4 — Test run**
```bash
cd /opt/nemoclaw && python3 nemoclaw_observer/observer.py
```

**Step 5 — Import n8n workflow**
1. Open n8n at `http://46.225.51.30:5678`
2. Settings → Import Workflow
3. Upload `nemoclaw_observer/n8n_cron_workflow.json`
4. Activate the workflow

**Step 6 — Wire Telegram /dashboard command** (in hetzy_phd.py)
```python
from nemoclaw_observer.telegram_handler import handle_dashboard_command
application.add_handler(CommandHandler("dashboard", handle_dashboard_command))
```

---

## Alert Rules

| Condition | Status | Action |
|---|---|---|
| Z.ai spend >= $4.00 | WARNING | Telegram alert |
| Z.ai spend >= $5.00 | HALT | Telegram alert + stop Z.ai calls |
| Any agent idle > 24 hours | WARNING | Flagged in dashboard |
| Any service unreachable | ERROR | Alert with suggested fix command |

---

## Trigger Options

- **Every 6 hours** — n8n cron (automatic, unattended)
- **Manual** — `python3 observer.py` on the VPS terminal
- **Telegram** — send `/dashboard` to @hetzy_phd_bot
- **n8n webhook** — GET `http://46.225.51.30:5678/webhook/nemoclaw-dashboard`

---

## Integration with UrantiOS / Mission Stack

This agent is one node in the NemoClaw constellation:

```
iPhone 16 Pro
    └─ iMac M4 (NemoClaw) ────────── Ollama (phi3, deepseek, qwen3)
         └─ Hetzy VPS (46.225.51.30)
              ├─ n8n (▶ NemoClaw Observer cron)
              ├─ PostgreSQL (amep_schema_v1 + nemoclaw_dashboard_log)
              ├─ Redis
              ├─ Qdrant (havona_records_v2)
              └─ Telegram bots (▶ /dashboard command → this agent)
```

Governed by **UrantiOS v1.0** — Truth, Beauty, Goodness.

---

*Agent specification committed to branch `claude/nemoclaw-observer-dashboard-sfT8m`*  
*All code lives in mircea-constellation and lobsterbot repos.*
