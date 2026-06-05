# Cognee vs Mem0 — Roadmap Memory Pilot

**Project:** PhD-Triune-Monism / Mircea's Constellation  
**Branch:** `claude/cognee-mem0-pilot-klDtU`  
**UrantiOS:** Truth · Beauty · Goodness  
**Date:** 2026-06-05

## Purpose

Compare two memory architectures for operationalising the three roadmap tables:

| Table | Rows | Description |
|---|---|---|
| `phd_research_layers.csv` | 24 | 6-phase × 4-step PhD research roadmap |
| `ai_legislature_phases.csv` | 6 | UrantiOS AI governance phases |
| `community_business_tiers.csv` | 6 | Constellation community/business tier structure |

**Cognee** builds a **knowledge graph** — nodes, relationships, multi-hop traversal.  
**Mem0** builds **vector memory** — semantic embeddings, similarity retrieval.

## Directory Structure

```
pilots/cognee-mem0/
├── .env.example          # copy to .env
├── run_all.sh            # convenience runner
├── data/
│   ├── phd_research_layers.csv
│   ├── ai_legislature_phases.csv
│   └── community_business_tiers.csv
├── cognee_pilot/
│   ├── requirements.txt
│   ├── config.py
│   ├── graph_schema.py
│   ├── ingest.py         # build the knowledge graph
│   └── agent.py          # interactive query agent
├── mem0_pilot/
│   ├── requirements.txt
│   ├── config.py
│   ├── ingest.py         # store vector memories
│   └── agent.py          # semantic retrieval agent
└── comparison/
    ├── benchmark.py      # side-by-side 10-query benchmark
    └── COMPARISON_REPORT.md
```

## Setup

### 1. API Keys
```bash
cd pilots/cognee-mem0
cp .env.example .env
# edit .env — add OPENAI_API_KEY
```

### 2. Qdrant (for Mem0)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Install dependencies
```bash
# Cognee pilot
pip install -r cognee_pilot/requirements.txt

# Mem0 pilot
pip install -r mem0_pilot/requirements.txt
```

## Running the Pilots

### Cognee
```bash
# Build the knowledge graph
python cognee_pilot/ingest.py

# Interactive query agent
python cognee_pilot/agent.py

# Single query
python cognee_pilot/agent.py "What are the deliverables for Phase 2?"
```

### Mem0
```bash
# Store vector memories
python mem0_pilot/ingest.py

# Interactive retrieval agent
python mem0_pilot/agent.py

# Single query
python mem0_pilot/agent.py "Show all PhD steps linked to governance"
```

### Benchmark
```bash
python comparison/benchmark.py
```

## Sample Queries

1. What are the deliverables for Phase 2 of the PhD research?
2. Which PhD steps have findings related to physicalism?
3. What is the status of the AI legislature governance mechanics?
4. How does the AMEP community tier relate to the education mission?
5. Which AI legislature phases depend on the UrantiOS Constitution?
6. Show all PhD steps that contribute to Chapter 4.
7. What governance principles guide the AI legislature phases?
8. How does the Infinite Spirit finding connect to the core thesis?
9. What deliverables serve community tiers 3 and 4?
10. Show all items with Pending status.

## Comparison Dimensions

| Dimension | Cognee (graph) | Mem0 (vector) |
|---|---|---|
| Relationship traversal | Strong — multi-hop | Weak — no explicit edges |
| Semantic fuzzy search | Moderate | Strong — cosine similarity |
| Setup complexity | Higher — LLM extracts graph | Lower — embeddings only |
| Query speed | Slower (graph traversal) | Faster (ANN search) |
| n8n integration | REST API + Cognee server | Mem0 cloud or self-hosted |
| Best for | "What depends on X?" | "Show me things like X" |

See `comparison/COMPARISON_REPORT.md` for full analysis.
