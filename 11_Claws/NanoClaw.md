# NanoClaw

> **Status:** ✅ Active — v1.2.17
> **Server:** 204.168.143.98 — URANTiOS Prime — Helsinki, FI
> **Interface:** Telegram bot @nanoclaw_openclaw_bot
> **API:** Claude SDK
> **Governed by UrantiOS v1.0**

---

## Identity

NanoClaw is the intelligent conversational agent — a Telegram bot powered by Anthropic's Claude SDK. It is deployed as a Docker container on URANTiOS Prime. Users interact with it by mentioning **@NanoClaw** in Telegram.

Nano = small, precise, targeted. NanoClaw delivers surgical AI responses.

## Access

| Method | Value |
|--------|-------|
| Telegram trigger | @NanoClaw (mention in chat) |
| Bot handle | @nanoclaw_openclaw_bot |
| Version | 1.2.17 |
| Container | Docker isolated on URANTiOS |

## Server

| Property | Value |
|----------|-------|
| IP | 204.168.143.98 |
| Provider | Hetzner Cloud |
| Type | CCX23 |
| RAM | 16 GB |
| Storage | 160 GB SSD |
| Location | Helsinki, Finland |
| Disk usage | 38% |

## Other Services on URANTiOS Prime

| Service | Port / URL | Purpose |
|---------|-----------|--------|
| Gabriel Brain | :18900 | Bright and Morning Star — website chatbot |
| Ollama | local | qwen2.5:32b — local AI reasoning |
| UrantiPedia | urantipedia.org / .com | 196 papers + Foreword, 477 personalities |

## SSH Access

```bash
ssh root@204.168.143.98
```

## Related

- [[OpenClaw]] — sister server
- [[Infrastructure_Map]] — full network
