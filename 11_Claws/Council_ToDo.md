# Council of Seven — To-Do List

> **Date:** 2026-04-12 (Melbourne, Australia)
> **Status:** In progress
> **Governed by UrantiOS v1.0 — Truth · Beauty · Goodness**

All remaining tasks to finish building and operationalising the Council of Seven and related Claws. Execute in order shown. Record every proof in `11_Claws/Proofs/`.

---

## Prerequisites

- [ ] Clone repos: `phd-triune-monism`, `mircea-constellation`, `lobsterbot`
- [ ] `git pull origin claude/count-claws-NrqRh` on each repo
- [ ] Copy `12_Credentials/SECRETS.template.md` → `12_Credentials/SECRETS.md` and fill in all keys

---

## Infrastructure & Fixes

- [ ] **Heal NemoClaw** — run the one-command boot script from iMac Terminal:
  ```bash
  bash <(curl -fsSL https://raw.githubusercontent.com/MyEduGit/mircea-constellation/claude/count-claws-NrqRh/setup/claws_boot.sh)
  ```
  Script: installs nginx, reverse-proxies n8n on port 80, imports Council workflow, prompts for Z.ai key.
  After: n8n accessible at `http://46.225.51.30` without SSH tunnel.

- [ ] **Seat 4 — Ollama / Gemma**: Install Ollama and pull `gemma3` model on URANTiOS (204.168.143.98):
  ```bash
  ssh root@204.168.143.98 'ollama pull gemma3'
  ```
  Confirm it runs at `http://204.168.143.98:11434`.

---

## Credential Management

- [ ] Complete `12_Credentials/SECRETS.md` (local only, gitignored):

| Key | Where to get it | Status |
|-----|----------------|--------|
| `Z_AI_API_KEY` | chat.z.ai → Settings → API Keys | ✅ Have |
| `N8N_EMAIL` | n8n owner account email | ❓ |
| `N8N_PASSWORD` | n8n owner account password | ❓ |
| `ANTHROPIC_API_KEY` | console.anthropic.com | ✅ Have |
| `OPENAI_API_KEY` | platform.openai.com | ❓ |
| `GOOGLE_API_KEY` | console.cloud.google.com | ❓ |
| `DEEPSEEK_API_KEY` | platform.deepseek.com | ❓ |
| `XAI_API_KEY` | console.x.ai | ❓ |

- [ ] **Sync Notion** — update `🔐 CREDENTIALS MASTER` page to match SECRETS.md (keep both in sync always)

---

## Seat Configuration & Testing

Work through seats in build order. For each seat: configure → test in isolation → save proof file.

### Seat 6 — Son-Spirit / GLM (Z.ai) — FIRST
- [ ] Verify workflow imported (claws_boot.sh handles this automatically)
- [ ] If key was entered in script: test immediately in n8n
- [ ] If not: open `Seat6_SonSpirit_GLM` node → Authorization header → `Bearer <Z_AI_API_KEY>`
- [ ] Execute node in isolation, verify `choices[0].message.content` in response
- [ ] Save output: `11_Claws/Proofs/Seat6_GLM_first_run.md`
- [ ] **Proof required before proceeding to next seat**

### Seat 4 — Father-Son / Gemma (Ollama local) — SECOND
- [ ] Confirm `ollama pull gemma3` completed on URANTiOS
- [ ] Verify endpoint `http://204.168.143.98:11434/api/chat` accessible from n8n
- [ ] Execute `Seat4_FatherSon_Ollama` node in isolation, verify `message.content` in response
- [ ] Save output: `11_Claws/Proofs/Seat4_Gemma_first_run.md`

### Seat 2 — Son / Claude (Anthropic) — THIRD
- [ ] Add `ANTHROPIC_API_KEY` to `Seat2_Son_Claude` node → `x-api-key` header (no "Bearer" prefix)
- [ ] Execute in isolation, verify `content[0].text` in response
- [ ] Save output: `11_Claws/Proofs/Seat2_Claude_first_run.md`

### Seat 3 — Spirit / Gemini (Google) — FOURTH
- [ ] Add `GOOGLE_API_KEY` to `Seat3_Spirit_Gemini` node → `x-goog-api-key` header
- [ ] Execute in isolation, verify `candidates[0].content.parts[0].text` in response
- [ ] Save output: `11_Claws/Proofs/Seat3_Gemini_first_run.md`

### Seat 1 — Father / GPT (OpenAI) — FIFTH
- [ ] Add `OPENAI_API_KEY` to `Seat1_Father_GPT` node → `Authorization: Bearer` header
- [ ] Also add same key to `Gabriel_Synthesizer` node (same OpenAI key)
- [ ] Execute in isolation, verify `choices[0].message.content`
- [ ] Save output: `11_Claws/Proofs/Seat1_GPT_first_run.md`

### Seat 5 — Father-Spirit / DeepSeek — SIXTH
- [ ] Add `DEEPSEEK_API_KEY` to `Seat5_FatherSpirit_DeepSeek` node → `Authorization: Bearer` header
- [ ] Execute in isolation
- [ ] Save output: `11_Claws/Proofs/Seat5_DeepSeek_first_run.md`

### Seat 7 — Trinity / Grok (xAI) — SEVENTH
- [ ] Add `XAI_API_KEY` to `Seat7_Trinity_Grok` node → `Authorization: Bearer` header
- [ ] Execute in isolation
- [ ] Save output: `11_Claws/Proofs/Seat7_Grok_first_run.md`

---

## Gabriel Synthesiser

- [ ] Once at least Seat 6 is live: run full workflow → Gabriel synthesises from available seats
- [ ] Verify Gabriel output in `Council Output` node contains meaningful synthesis
- [ ] Save: `11_Claws/Proofs/Gabriel_first_synthesis.md`

---

## Full Council Run

- [ ] All 7 seats configured and individually proven (each has a proof file)
- [ ] Run full execution — record: time taken, token usage, which seats responded
- [ ] Save: `11_Claws/Proofs/Council_First_Full_Run.md`
- [ ] Update `00_CLAWS_MASTER.md` with completion note

---

## Backups (after each seat stable for 10+ runs or 3–7 days)

| Primary | Backup | Status |
|---------|--------|--------|
| Seat 1 Father (GPT) | Seat 2 Son (Claude) | ⏳ After stable |
| Seat 2 Son (Claude) | Seat 1 Father (GPT) | ⏳ After stable |
| Seat 3 Spirit (Gemini) | Seat 7 Trinity (Grok) | ⏳ After stable |
| Seat 5 Father-Spirit (DeepSeek) | Seat 4 Ollama | ⏳ After stable |
| Gabriel | Seat 2 Son (Claude) | ⏳ After stable |

Update `COUNCIL_SCHEMA_v1.json` `backup_model` field for each seat when assigned.

---

## Documentation & Communication

- [ ] After each task: add a line to `00_CLAWS_MASTER.md` with what was done + link to proof
- [ ] Each session: create `11_Claws/Proofs/Session_<date>.md` (commands, issues, resolutions)
- [ ] Share this to-do with collaborators via Notion or Telegram

---

## Related Files

- [[00_CLAWS_MASTER]] — master index
- [[Council_of_Seven]] — architecture and seat specs
- [[NemoClaw]] — n8n stack details
- [[Infrastructure_Map]] — server topology
- [[12_Credentials/Services_Index]] — all API keys and status
- `mircea-constellation/council/COUNCIL_SCHEMA_v1.json` — source of truth
- `mircea-constellation/council/council_of_seven_v1.n8n.json` — n8n workflow

---

*Governed by UrantiOS v1.0 — Truth · Beauty · Goodness*
*Last updated: 2026-04-12*
