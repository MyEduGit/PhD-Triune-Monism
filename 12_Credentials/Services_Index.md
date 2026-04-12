# Services Index — All Credentials

> **Updated:** 2026-04-12
> Actual values live in `SECRETS.md` (local only, gitignored)

---

## AI / LLM Services — Council of Seven

| Seat | Service | URL | Key Name | Used By | Build Order | Status |
|------|---------|-----|----------|---------|-------------|--------|
| 6 | **Z.ai / ZhipuAI GLM** | https://chat.z.ai | `Z_AI_API_KEY` | Seat6_SonSpirit_GLM | **1st — WIRE NOW** | ✅ Have key |
| 4 | **Ollama / Gemma** | 204.168.143.98:11434 | none — local | Seat4_FatherSon_Ollama | 2nd — no key | ✅ No key needed |
| 2 | **Anthropic / Claude** | https://api.anthropic.com | `ANTHROPIC_API_KEY` | Seat2_Son_Claude, NanoClaw | 3rd | ✅ Have key |
| 3 | **Google Gemini** | https://generativelanguage.googleapis.com | `GOOGLE_API_KEY` | Seat3_Spirit_Gemini | 4th | ❓ Need key |
| 1 | **OpenAI** | https://api.openai.com | `OPENAI_API_KEY` | Seat1_Father_GPT, Gabriel | 5th | ❓ Need key |
| 5 | **DeepSeek** | https://api.deepseek.com | `DEEPSEEK_API_KEY` | Seat5_FatherSpirit_DeepSeek | 6th | ❓ Need key |
| 7 | **xAI / Grok** | https://api.x.ai | `XAI_API_KEY` | Seat7_Trinity_Grok | 7th | ❓ Need key |

## Telegram

| Service | Handle | Key Name in SECRETS.md | Used By | Status |
|---------|--------|------------------------|---------|--------|
| **Main bot token** | @UrantiPedia_Agent_01_bot | `TELEGRAM_BOT_TOKEN` | OpenClaw fleet | ✅ Have |
| **NanoClaw bot** | @nanoclaw_openclaw_bot | `NANOCLAW_BOT_TOKEN` | NanoClaw | ✅ Have |
| **Hetzy PhD bot** | @Hetzy_PhD_bot | `HETZY_BOT_TOKEN` | Fleet Commander | ✅ Have |
| **Mircea Telegram ID** | — | `TELEGRAM_USER_ID` | All bots | 828807562 |

## Infrastructure

| Service | Details | Key Name in SECRETS.md | Status |
|---------|---------|------------------------|--------|
| **OpenClaw SSH** | root@46.225.51.30 | SSH key (not a token) | ✅ Configured |
| **URANTiOS SSH** | root@204.168.143.98 | SSH key (not a token) | ✅ Configured |
| **Hetzner Cloud** | hetzner.com | `HETZNER_API_TOKEN` | Server management | ❓ Check |
| **n8n (NemoClaw)** | http://46.225.51.30 | `N8N_EMAIL` + `N8N_PASSWORD` | Browser login | ❓ Check |

## Web Services

| Service | URL | Key Name in SECRETS.md | Status |
|---------|-----|------------------------|--------|
| **Z.ai chat login** | https://chat.z.ai | `Z_AI_EMAIL` + `Z_AI_PASSWORD` | Browser | ✅ Have |
| **GitHub** | github.com/myedugit | `GITHUB_PAT` | Repos, CI | ✅ Have |
| **Tailscale** | tailscale.com | `TAILSCALE_AUTH_KEY` | VPN | ✅ Active |

---

## Missing / To Verify

- [ ] OpenAI API key — do we have one?
- [ ] Hetzner API token — needed for automated provisioning
- [ ] n8n owner account email+password — needed to log in
- [ ] Any other bot tokens not listed above?

---

## Related

- [[00_CREDENTIALS_POLICY]] — how this system works
- [[SECRETS.template]] — copy to SECRETS.md and fill in values
