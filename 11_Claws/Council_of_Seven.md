# Council of Seven Master Spirits

## Overview

The Council of Seven is a multi-AI deliberation system built in n8n. Seven AI seats respond in parallel to any question; Gabriel (the Synthesizer) collects all responses and issues a unified judgment.

Built on: **NemoClaw** (n8n at OpenClaw, port 80 via nginx)

---

## Seats

| # | Name | Role | Provider | Model ID | Status |
|---|------|------|----------|----------|--------|
| 1 | Father | Final Judge | OpenAI | gpt-4o | NOT_CONFIGURED |
| 2 | Son | Builder / Coder | Anthropic | claude-opus-4-5-20251001 | NOT_CONFIGURED |
| 3 | Spirit | Multimodal / Long Context | Google | gemini-2.5-pro | NOT_CONFIGURED |
| 4 | Father-Son | Local Sovereign | Ollama (local) | gemma3 | NOT_CONFIGURED |
| 5 | Father-Spirit | Low-Cost Frontier | DeepSeek | deepseek-chat | NOT_CONFIGURED |
| 6 | Son-Spirit | Engineering Specialist | Z.ai (ZhipuAI) | glm-4-flash | **PENDING_KEY** |
| 7 | Trinity | Live Context / Web | xAI | grok-3 | NOT_CONFIGURED |
| G | Gabriel | Synthesizer — Bright & Morning Star | OpenAI | gpt-4o | NOT_CONFIGURED |

---

## Architecture

```
Manual Trigger
    └─► Set Question  ──────────────────────────────────────────┐
                      │                                          │
            ┌─────────┴──────────────────────────────────────┐  │
            │  7 Parallel HTTP Request nodes                 │  │
            │  (all: continueOnFail = true)                  │  │
            │                                                │  │
            │  Seat1_Father_GPT          → OpenAI            │  │
            │  Seat2_Son_Claude          → Anthropic         │  │
            │  Seat3_Spirit_Gemini       → Google            │  │
            │  Seat4_FatherSon_Ollama    → 204.168.143.98    │  │
            │  Seat5_FatherSpirit_DeepSeek → DeepSeek        │  │
            │  Seat6_SonSpirit_GLM       → open.bigmodel.cn  │  │
            │  Seat7_Trinity_Grok        → xAI               │  │
            └─────────┬──────────────────────────────────────┘  │
                      │                                          │
                 Merge Responses (append mode)                   │
                      │                                          │
                 Build Synthesis Prompt (Code node) ◄───────────┘
                      │  (re-reads question from Set Question)
                      │
                 Gabriel_Synthesizer (OpenAI, gpt-4o)
                      │
                 Council Output (Set node)
```

**Governance rule:** No claim without proof. Continue on fail. Gabriel synthesizes from available seats only.

---

## Files (GitHub)

| File | Location |
|------|----------|
| Schema (source of truth) | `mircea-constellation/council/COUNCIL_SCHEMA_v1.json` |
| n8n workflow (importable) | `mircea-constellation/council/council_of_seven_v1.n8n.json` |
| Import guide | `mircea-constellation/council/README.md` |

Branch: `claude/count-claws-NrqRh`

---

## Credentials Required

| Seat | Key Name | Notes |
|------|----------|-------|
| Father (1) | `OPENAI_API_KEY` | also used by Gabriel |
| Son (2) | `ANTHROPIC_API_KEY` | header: `x-api-key` (no Bearer prefix) |
| Spirit (3) | `GOOGLE_API_KEY` | header: `x-goog-api-key` |
| Father-Son (4) | (none) | Ollama local, pull: `ollama pull gemma3` |
| Father-Spirit (5) | `DEEPSEEK_API_KEY` | |
| Son-Spirit (6) | `Z_AI_API_KEY` | **key exists** — paste into GLM node |
| Trinity (7) | `XAI_API_KEY` | |

All keys must be in: `12_Credentials/SECRETS.md` (local only, gitignored)

---

## Build Order

```
Step 1  →  Seat 6 (Son-Spirit / GLM / Z.ai)     KEY EXISTS — wire NOW
Step 2  →  Seat 4 (Father-Son / Gemma / Ollama)  no key, just: ollama pull gemma3
Step 3  →  Seat 2 (Son / Claude / Anthropic)
Step 4  →  Seat 3 (Spirit / Gemini / Google)
Step 5  →  Seat 1 (Father / GPT / OpenAI)        also activates Gabriel
Step 6  →  Seat 5 (Father-Spirit / DeepSeek)
Step 7  →  Seat 7 (Trinity / Grok / xAI)
```

**Rule:** Prove each seat stable (10+ runs or 3-7 days) before adding next.

---

## Access

- **n8n UI:** `http://46.225.51.30` (OpenClaw, after nginx fix)
- **SSH tunnel fallback:** `ssh -L 5678:127.0.0.1:5678 root@46.225.51.30` then `http://localhost:5678`
- **nginx fix:** Run `claws_boot.sh` from iMac, or `openclaw_fix.sh` on server directly

---

## Session Log

- Created: 2026-04-12
- Session: [[Session_2026-04-12]]
- Related Claws: [[NemoClaw]], [[OpenClaw]]
- Related files: [[00_CLAWS_MASTER]]
