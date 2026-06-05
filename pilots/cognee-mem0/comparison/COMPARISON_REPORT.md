# Cognee vs Mem0 — Comparison Report

**Project:** PhD-Triune-Monism / Mircea's Constellation  
**Data:** 3 roadmap tables (36 entities: 24 PhD layers + 6 legislature phases + 6 community tiers)  
**UrantiOS:** Truth · Beauty · Goodness  
**Date:** 2026-06-05

---

## 1. Architecture Summary

### Cognee — Graph Memory

Cognee ingests text and uses an LLM to extract **entities and relationships**, building a
knowledge graph (NetworkX/Neo4j). Queries traverse the graph via `SearchType.INSIGHTS`
(multi-hop reasoning) or `SearchType.SUMMARIES` (overview retrieval).

```
CSV rows → text documents → cognee.add() → cognee.cognify() [LLM extraction]
         → knowledge graph (nodes + edges) → cognee.search(INSIGHTS, query)
```

**Node types extracted (expected):**
- `PhDPhase`, `PhDStep`, `KeyFinding`, `Deliverable`
- `LegislaturePhase`, `GovernancePrinciple`, `Agent`
- `CommunityTier`, `Infrastructure`, `RevenueModel`

**Relationships extracted (expected):**
- `PART_OF`, `HAS_FINDING`, `HAS_DELIVERABLE`, `DEPENDS_ON`
- `GOVERNED_BY`, `USES`, `SERVES`

### Mem0 — Vector Memory

Mem0 converts each row to a natural-language string, embeds it with
`text-embedding-3-small`, and stores it in Qdrant. Retrieval is cosine-similarity
search with optional metadata filtering.

```
CSV rows → natural-language strings → mem0.add() → vector embeddings → Qdrant
         → mem0.search(query) → ANN cosine search → ranked results + scores
```

**Metadata stored per memory:**
- `table`: phd_layers | ai_legislature | community_tiers
- `phase_id` / `step_id` / `tier_id`
- `status`, `phd_chapter`, `governance_principle`

---

## 2. Benchmark Results

> Fill in after running `python comparison/benchmark.py`

| # | Query | Cognee results | Cognee time | Mem0 results | Mem0 time | Mem0 score |
|---|---|---|---|---|---|---|
| 1 | Phase 2 deliverables? | — | — | — | — | — |
| 2 | Steps linked to physicalism? | — | — | — | — | — |
| 3 | Governance mechanics status? | — | — | — | — | — |
| 4 | AMEP & education mission? | — | — | — | — | — |
| 5 | All Pending items? | — | — | — | — | — |
| 6 | Phases depending on UrantiOS? | — | — | — | — | — |
| 7 | PhD steps for Chapter 4? | — | — | — | — | — |
| 8 | Governance principles? | — | — | — | — | — |
| 9 | Infinite Spirit → core thesis? | — | — | — | — | — |
| 10 | Tiers 3 & 4 deliverables? | — | — | — | — | — |
| **Avg** | | | | | | |

---

## 3. Dimension Comparison

| Dimension | Cognee (graph) | Mem0 (vector) | Winner |
|---|---|---|---|
| **Relationship traversal** | Strong — explicit edges enable multi-hop | None — no traversal | Cognee |
| **Semantic fuzzy search** | Moderate — LLM-extracted concepts | Strong — cosine similarity on full text | Mem0 |
| **Setup time** | Slower — LLM must extract graph from text | Faster — embeddings only | Mem0 |
| **Query speed** | Slower — graph traversal + LLM | Faster — ANN vector search | Mem0 |
| **Result explainability** | High — shows entity path | Medium — shows score only | Cognee |
| **Metadata filtering** | Limited | Strong — filter by table/phase/status | Mem0 |
| **Extensibility** | High — add node types and relationships | High — add metadata fields | Tie |
| **n8n integration** | Via Cognee REST server | Via Mem0 cloud or self-hosted API | Tie |
| **Cost per query** | Higher — LLM tokens for traversal | Lower — embedding + ANN only | Mem0 |
| **PhD research queries** | Better for structured “what depends on X” | Better for “show me things like X” | Context-dependent |

---

## 4. Query Type Analysis

### Cognee is better for:
- Structural queries: *"Which phases depend on Phase 3?"*
- Multi-hop: *"What findings in steps linked to Chapter 4 relate to physicalism?"*
- Graph traversal: *"Trace the argument from Step 1.2 to the core thesis"*
- Explicit relationship queries: *"Show all deliverables that serve the Legislature phase"*

### Mem0 is better for:
- Semantic similarity: *"Show me things related to governance mechanics"*
- Fuzzy concept search: *"Find steps about consciousness and mind"*
- Fast retrieval at scale: sub-100ms queries once indexed
- Cross-table semantic links the graph didn’t explicitly encode

---

## 5. Integration Fit

### n8n / OpenClaw

| System | Integration Path | Latency | Notes |
|---|---|---|---|
| Cognee | `POST /api/v1/search` on Cognee server | 1–5s | Requires Cognee server running |
| Mem0 | `mem0ai` SDK or Mem0 cloud REST API | 0.1–0.5s | Simpler; Qdrant is the only dependency |

### UrantiOS Agent Compatibility

Both systems can be wrapped into a UrantiOS-compliant agent following the Spawn Mandate:
```
NAME: RoadmapMemoryAgent
FUNCTION: Answer queries about PhD layers / AI legislature / community tiers
MANDATE: Retrieve and reason over roadmap data only
AUTHORITY: Read-only
URANTIOS_CORE: Truth · Beauty · Goodness
LUCIFER_TEST: Transparent, honest, in-mandate, mission-first
```

---

## 6. Recommendation

### For PhD Research Queries → **Cognee**
The PhD roadmap has deep dependency relationships (steps → phases → chapters →
findings → thesis). Cognee’s graph traversal is the natural fit for queries like
*"What contributes to the core argument in Chapter 4?"*

### For Community / Semantic Discovery → **Mem0**
Community tiers and legislature phases benefit more from semantic search —
users are likely to ask fuzzy questions like *"show me tiers related to education”*
rather than precise structural queries.

### Recommended Architecture → **Hybrid**

```
User query
    │
    ├── Structural / relational? ──► Cognee (graph traversal)
    └── Semantic / fuzzy?       ──► Mem0  (vector similarity)
```

Route by query intent detection (simple keyword heuristic or LLM classifier).
Results from both can be merged for comprehensive answers.

### For Proof Logging (Phase 5 of AI Legislature)
Mem0’s metadata layer is ideal for **milestone tagging**; Cognee’s graph is ideal
for **dependency proof chains** ("this milestone was reached because steps X, Y, Z
were completed"). Use both.

---

## 7. Next Steps

- [ ] Run `run_all.sh` and fill in benchmark table in Section 2
- [ ] Test Cognee `SearchType.SUMMARIES` vs `INSIGHTS` for overview queries
- [ ] Add Mem0 metadata filter queries (`table=phd_layers AND status=Pending`)
- [ ] Prototype n8n webhook that calls Mem0 on new PhD diary entries
- [ ] Evaluate Cognee + Neo4j backend for production (vs NetworkX dev backend)
- [ ] Extend pilot to include Obsidian vault content (full PhD diary as memory)
- [ ] Build proof-logging layer on top of Mem0 for AI Legislature Phase 5
