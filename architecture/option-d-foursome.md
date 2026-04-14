# Option D — The Awesome Foursome Architecture

> Vision: a job dropped into the vault wakes all four AIs automatically.
> "Reverse n8n" — the vault triggers the workflow, not the other way round.
> Each contribution signed with source AI name. All four share one Task ID.
> DRIFT → 4 working as one.

## Architecture diagram

```mermaid
flowchart TD
    %% ===== TOP: USER & VAULT =====
    User["👤 You — Mircea<br/>Create job · See all answers · Give new work"]

    Vault["📓 Obsidian Vault<br/>PhD-Triune-Monism<br/><b>Single Source of Truth</b><br/>jobs/&lt;task&gt;/input.md"]

    %% ===== GIT LAYER =====
    ObsGit["🔄 Obsidian Git plugin<br/>auto commit + push / pull"]
    GH["☁️ GitHub<br/>myedugit/PhD-Triune-Monism<br/>branch: claude/multi-ai-obsidian-integration-jkoI9"]
    Hook["🪝 Webhook<br/>push event fires"]

    %% ===== ORCHESTRATOR =====
    Orch["⚙️ Orchestrator on hetzy-openclaw<br/><b>n8n + CrewAI hybrid</b><br/>Webhook receiver · Fan-out · Shared Task ID"]

    %% ===== THE FOURSOME (with roles) =====
    GPT["🟢 ChatGPT<br/><b>Editor / Writer</b><br/>api.openai.com<br/>signs: gpt@foursome"]
    Claude["🟢 Claude Code<br/><b>Architect / Reasoner</b><br/>api.anthropic.com<br/>signs: claude@foursome"]
    Grok["🟢 Grok<br/><b>Truth-Seeker / Builder</b><br/>api.x.ai<br/>signs: grok@foursome"]
    Gemma["🟢 Gemma 4:e4b<br/><b>Local Thinker / Fact-Checker</b><br/>Ollama @ urantios-prime<br/>100.72.238.7:11434<br/>9.6 GB · ID c6eb396dbd59<br/>signs: gemma@foursome"]

    %% ===== RESPONSE COLLECTOR =====
    Resp["📥 Vault Responses<br/>jobs/&lt;task&gt;/responses/<br/>├─ gpt.md<br/>├─ claude.md<br/>├─ grok.md<br/>└─ gemma.md<br/><i>AI signature + timestamp</i>"]

    %% ===== SUPPORT =====
    TG["📱 @GabrielVault_bot<br/>alternate trigger"]
    TS(("🕸️ Tailscale mesh"))
    Paper["📎 Paperclip :3101<br/>prove / verify"]

    %% ===== HOT PATH =====
    User -->|"1. writes input.md"| Vault
    Vault -->|"2. live sync"| ObsGit
    ObsGit -->|"3. commit + push"| GH
    GH -->|"4. triggers"| Hook
    Hook -->|"5. POST /webhook"| Orch
    TG -.->|"alt trigger"| Orch

    Orch -->|"6a. fan-out · Shared Task ID"| GPT
    Orch -->|"6b. fan-out · Shared Task ID"| Claude
    Orch -->|"6c. fan-out · Shared Task ID"| Grok
    Orch -->|"6d. fan-out · Shared Task ID"| Gemma

    GPT -->|"7. signed commit"| GH
    Claude -->|"7. signed commit"| GH
    Grok -->|"7. signed commit"| GH
    Gemma -->|"7. signed commit"| GH

    GH -->|"8. pull"| ObsGit
    ObsGit --> Resp
    Resp -->|"9. Mircea reads all 4"| User

    %% ===== SUPPORT LINKS =====
    Orch -.->|"verify"| Paper
    Gemma -.-> TS
    TS -.-> Orch

    %% ===== COLOURS =====
    classDef user fill:#fef3c7,stroke:#d97706,color:#000,stroke-width:2px
    classDef vault fill:#1e3a8a,stroke:#60a5fa,color:#fff,stroke-width:2px
    classDef git fill:#7f1d1d,stroke:#ef4444,color:#fff,stroke-width:2px
    classDef orch fill:#4c1d95,stroke:#a78bfa,color:#fff,stroke-width:2px
    classDef ai fill:#14532d,stroke:#22c55e,color:#fff,stroke-width:2px
    classDef resp fill:#1e3a8a,stroke:#60a5fa,color:#fff,stroke-width:2px
    classDef support fill:#164e63,stroke:#22d3ee,color:#fff,stroke-width:1px

    class User user
    class Vault,Resp,ObsGit vault
    class GH,Hook git
    class Orch orch
    class GPT,Claude,Grok,Gemma ai
    class TG,TS,Paper support
```

## The Foursome — roles and endpoints

| AI | Role | Endpoint | Signature |
|---|---|---|---|
| **ChatGPT** | Editor / Writer | `api.openai.com` | `gpt@foursome` |
| **Claude Code** | Architect / Reasoner | `api.anthropic.com` | `claude@foursome` |
| **Grok** | Truth-Seeker / Builder | `api.x.ai` | `grok@foursome` |
| **Gemma 4:e4b** | Local Thinker / Fact-Checker | Ollama @ `urantios-prime` (`100.72.238.7:11434`) | `gemma@foursome` |

**Gemma 4 model selection.** Verified via `ollama list` on iMac_M4:

| Tag | Model ID | Size | Notes |
|---|---|---|---|
| `gemma4:e2b` | `7fbdbf8f5e45` | 7.2 GB | Smaller, faster |
| `gemma4:e4b` | `c6eb396dbd59` | 9.6 GB | **Foursome default** — balanced speed/capability |
| `gemma4:latest` | `c6eb396dbd59` | 9.6 GB | Alias of `e4b` |
| `gemma4:31b` | `6316f0629137` | 19 GB | Heavyweight — use for deep reasoning jobs only |

`gemma4:e4b` is the Foursome's Local Thinker. For jobs requiring deeper reasoning, the orchestrator can route to `gemma4:31b` instead via a job-level flag in `input.md` frontmatter (`gemma_model: gemma4:31b`).

## Vault convention

```
PhD-Triune-Monism/
└── jobs/
    └── <task-name>/
        ├── input.md                    # the job spec — Mircea writes this
        └── responses/
            ├── gpt.md                  # ChatGPT's signed reply
            ├── claude.md               # Claude's signed reply
            ├── grok.md                 # Grok's signed reply
            └── gemma.md                # Gemma 4:e4b's signed reply
```

Each response file carries AI signature + ISO timestamp in its frontmatter.

## The 9-step hot path

1. **You write** `jobs/<task>/input.md` in Obsidian
2. **Obsidian Git** live-syncs the change
3. **Commit + push** to GitHub
4. GitHub **webhook** fires on push
5. **n8n** receives `POST /webhook` on `hetzy-openclaw:5678`
6. n8n **fans out** with a Shared Task ID → (a) GPT, (b) Claude, (c) Grok, (d) Gemma in parallel
7. Each AI writes its reply as a **signed commit** back to GitHub
8. Obsidian Git **pulls** the four new files
9. **You read** all four answers side-by-side in Obsidian

## Support layer (not on the hot path, but essential)

- **Tailscale mesh** — how n8n reaches Gemma on `urantios-prime`
- **Paperclip** (`:3101/paperclip/prove`) — receipt / verification service
- **@GabrielVault_bot** — Telegram alternate trigger for jobs from mobile

## Cost

Real verified spend: **$33.29/mo** to Hetzner Online GmbH (PayPal, 14 Apr 2026).
Plus per-call API usage for OpenAI / Anthropic / xAI. Gemma is free (local).

## Render this diagram

- **Obsidian**: renders natively in Preview mode
- **Web**: paste into https://mermaid.live → export PNG/SVG
- **CLI**: `npm i -g @mermaid-js/mermaid-cli && mmdc -i option-d-foursome.md -o option-d-foursome.svg`
