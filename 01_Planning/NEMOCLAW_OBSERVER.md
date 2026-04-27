# NemoClaw Observer — Mission Control

The PhD stack is monitored by **NemoClaw Observer**, a five-layer
dashboard agent whose source lives in
[`mircea-constellation/nemoclaw_observer/`](../../mircea-constellation/tree/claude/setup-nemoclaw-1502q/nemoclaw_observer)
with the Telegram wrapper in
[`lobsterbot/nemoclaw_observer/`](../../lobsterbot/tree/claude/setup-nemoclaw-1502q/nemoclaw_observer).

## Why it matters for the thesis

The Triune Monism argument depends on a continuously observable field
of agents (OpenClaw, NanoClaw, Gabriel, the bot fleet). NemoClaw is the
"third-person" witness that records state to PostgreSQL and surfaces
anomalies to the operator via Telegram.

## What it watches

| Layer | Service |
|---|---|
| VPS (46.225.51.30) | n8n, PostgreSQL, Redis, Qdrant |
| Local (iMac M4)   | Ollama (phi3:14b, deepseek-r1:8b, qwen3:8b) |
| Apps              | `@Hetzy_PhD_bot` / Telegram |
| LLM spend         | Z.ai GLM-5.1 cap ($5/mo, warn at 80%) |

## Getting it running

On the Hetzy VPS (persistent background run):

```bash
git clone --branch claude/setup-nemoclaw-1502q \
    https://github.com/myedugit/mircea-constellation.git /opt/mircea-constellation
cd /opt/mircea-constellation/nemoclaw_observer
cp config.env.example .env && $EDITOR .env
./run.sh                          # one-shot verification
sudo cp nemoclaw-observer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nemoclaw-observer
```

Apply the PostgreSQL schema once:

```bash
psql -h 46.225.51.30 -U postgres amep_schema_v1 \
     -f /opt/mircea-constellation/nemoclaw_observer/schema.sql
```

## Data for the thesis

Queries that are useful when citing stack stability:

```sql
-- latest per-service state
SELECT * FROM nemoclaw_latest_status ORDER BY service;

-- last week's alerts
SELECT * FROM nemoclaw_recent_alerts;

-- uptime by service
SELECT service,
       COUNT(*) FILTER (WHERE status = 'ok')    AS ok_count,
       COUNT(*) FILTER (WHERE status = 'warn')  AS warn_count,
       COUNT(*) FILTER (WHERE status = 'error') AS error_count
FROM   nemoclaw_dashboard_log
WHERE  timestamp >= NOW() - INTERVAL '30 days'
GROUP  BY service;
```

These feed the *continuity-of-witness* chapter in
`02_Foreword_Sections/`.
