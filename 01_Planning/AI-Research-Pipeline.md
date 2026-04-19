# AI Research Pipeline — Triune Monism PhD

## Overview

Seven AI providers, orchestrated through n8n on NemoClaw (Hetzner 46.225.51.30:5678), support the Triune Monism research pipeline.

**Endpoint**: `http://localhost:5678/webhook/ai-router` (SSH tunnel required)

---

## Provider Roles in PhD Research

| Provider | Model | task_type | Role in Research |
|----------|-------|-----------|-----------------|
| **OpenAI GPT-4o** | gpt-4o | `code` | Argument structuring, LaTeX formatting, citation tools |
| **Anthropic Claude** | claude-sonnet-4-6 | `creative` | Philosophical synthesis, long-form chapter writing |
| **Google Gemini** | gemini-2.0-flash | `research` | Literature review, cross-referencing (1M context) |
| **Mistral** | mistral-large-latest | `analysis` | Comparative analysis, structured argument validation |
| **Groq (Llama)** | llama-3.3-70b | `fast` | Quick definitions, real-time Q&A during writing |
| **Ollama** | qwen2.5:32b | `local` | Private drafts, sensitive personal notes, zero cost |
| **Cohere** | command-r-plus | `search` | RAG over Urantia Book corpus, grounded citations |

---

## Research Workflow Integration

### Daily Writing Session
```bash
# 1. Quick definition lookup (Groq — ~50ms)
curl -X POST http://localhost:5678/webhook/ai-router \
  -H "Content-Type: application/json" \
  -d '{"query": "Define morontia in Urantia cosmology", "task_type": "fast"}'

# 2. Chapter section writing (Claude)
curl -X POST http://localhost:5678/webhook/ai-router \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Develop the argument that Triune Monism resolves the mind-body problem",
    "task_type": "creative",
    "system_prompt": "You are a PhD philosophy advisor specializing in ontology and The Urantia Book."
  }'

# 3. Literature cross-reference (Gemini — 1M context)
curl -X POST http://localhost:5678/webhook/ai-router \
  -H "Content-Type: application/json" \
  -d '{"query": "Compare Triune Monism with Hegel Absolute Idealism and Spinoza Substance Monism", "task_type": "research"}'
```

### Ensemble Review (Critical Chapters)
```bash
# Get 3 perspectives in parallel — OpenAI + Anthropic + Gemini
curl -X POST http://localhost:5678/webhook/ai-ensemble \
  -H "Content-Type: application/json" \
  -d '{"query": "Critique the Triune Monism ontological framework for logical consistency"}'
```

### Private Drafts (Ollama — no API, stays local)
```bash
curl -X POST http://localhost:5678/webhook/ai-router \
  -H "Content-Type: application/json" \
  -d '{"query": "Draft personal reflection on Paper 1 of The Urantia Book", "task_type": "local"}'
```

---

## Urantia Book RAG (Cohere)

Cohere's `command-r-plus` model supports grounded retrieval. When the n8n Urantia corpus is indexed:

```bash
curl -X POST http://localhost:5678/webhook/ai-router \
  -H "Content-Type: application/json" \
  -d '{"query": "Find all references to triune reality in the Foreword", "task_type": "search"}'
```

---

## Access

SSH tunnel from iMac M4:
```bash
ssh -L 5678:localhost:5678 mircea@46.225.51.30
# Then: http://localhost:5678
```

---

*Governed by UrantiOS — Truth · Beauty · Goodness*
