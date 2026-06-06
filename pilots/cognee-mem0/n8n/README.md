# n8n Integration — Roadmap Memory Router

**UrantiOS: Truth · Beauty · Goodness**

## Workflows

| File | Trigger | Calls | Purpose |
|---|---|---|---|
| `workflow_roadmap_query.json` | `POST /roadmap-query` | `POST :8765/query` | Route query to Cognee or Mem0 |
| `workflow_proof_logger.json` | `POST /log-milestone` | `POST :8765/proof/log/milestone` | Log PhD milestone as proof |

## Import into n8n

1. Open n8n → Workflows → Import
2. Paste or upload the JSON file
3. Activate the workflow
4. Test with a POST request

## Example Requests

### Query
```bash
curl -X POST http://your-n8n/webhook/roadmap-query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the deliverables for Phase 2?"}'
```

### Log Milestone
```bash
curl -X POST http://your-n8n/webhook/log-milestone \
  -H "Content-Type: application/json" \
  -d '{
    "milestone_id": "PhD-1.2",
    "title": "Seven Absolutes Analysis Complete",
    "description": "Mapped all 7 Absolutes with gravity circuits",
    "evidence": ["02-SEVEN-ABSOLUTES.md created", "F3 finding logged"],
    "phd_phase": "1",
    "legislature_phase": ""
  }'
```

## Direct API (no n8n)

The FastAPI server runs on port **8765**:

```bash
# Start server
uvicorn hybrid_router.server:app --host 0.0.0.0 --port 8765

# Health check
curl http://localhost:8765/health

# Query
curl -X POST http://localhost:8765/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show governance mechanics status"}'

# Audit trail
curl http://localhost:8765/proof/audit
```
