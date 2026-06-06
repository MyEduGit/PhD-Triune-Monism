#!/usr/bin/env python3
"""
Hybrid Memory Router — FastAPI Server
Exposes /query endpoint for n8n, OpenClaw, and Telegram bot integration.

Usage:
    uvicorn server:app --host 0.0.0.0 --port 8765 --reload

Endpoints:
    GET  /health          — liveness check
    POST /query           — route a query to Cognee/Mem0/both
    GET  /sample          — run 3 canonical queries
    POST /proof/log       — log a PhD milestone (Phase 5)
    GET  /proof/audit     — retrieve full audit trail

UrantiOS: Truth · Beauty · Goodness
"""
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
from router import route, Route
from proof_logger.logger import log_milestone, log_agent_action, get_audit_trail

app = FastAPI(
    title="Roadmap Memory Router",
    description="Hybrid Cognee (graph) + Mem0 (vector) router. UrantiOS-governed.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


# ── Schemas ─────────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str
    force_route: Optional[str] = None  # cognee | mem0 | both

class MilestoneRequest(BaseModel):
    milestone_id: str
    title: str
    description: str
    evidence: list[str]
    phd_phase: Optional[str] = ""
    legislature_phase: Optional[str] = ""
    agent_id: Optional[str] = "mircea"

class AgentActionRequest(BaseModel):
    agent_id: str
    action: str
    result: str
    passed_lucifer_test: bool
    mandate: Optional[str] = ""


# ── Routes ─────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "governed_by": "UrantiOS v1.0",
            "values": ["Truth", "Beauty", "Goodness"]}


@app.post("/query")
async def query_endpoint(body: QueryRequest):
    force = Route(body.force_route) if body.force_route else None
    r = await route(body.query, force=force)
    return {
        "query":         r.query,
        "route":         r.route,
        "reasoning":     r.reasoning,
        "result_count":  len(r.merged),
        "results":       r.merged,
        "cognee_time_s": round(r.cognee_time_s, 3),
        "mem0_time_s":   round(r.mem0_time_s, 3),
        "total_time_s":  r.total_time_s,
    }


@app.get("/sample")
async def sample():
    queries = [
        "What are the deliverables for Phase 2 of the PhD research?",
        "Show everything related to governance mechanics.",
        "Which PhD steps contribute to Chapter 4?",
    ]
    out = []
    for q in queries:
        r = await route(q)
        out.append({"query": q, "route": r.route,
                    "count": len(r.merged), "time_s": r.total_time_s})
    return out


@app.post("/proof/log/milestone")
def proof_milestone(body: MilestoneRequest):
    record = log_milestone(
        milestone_id=body.milestone_id,
        title=body.title,
        description=body.description,
        evidence=body.evidence,
        phd_phase=body.phd_phase,
        legislature_phase=body.legislature_phase,
        agent_id=body.agent_id,
    )
    return {"status": "logged", "hash": record["hash"]}


@app.post("/proof/log/action")
def proof_action(body: AgentActionRequest):
    record = log_agent_action(
        agent_id=body.agent_id,
        action=body.action,
        result=body.result,
        passed_lucifer_test=body.passed_lucifer_test,
        mandate=body.mandate,
    )
    return {"status": "logged", "hash": record["hash"],
            "lucifer_test": "PASS" if body.passed_lucifer_test else "FAIL"}


@app.get("/proof/audit")
def proof_audit(filter_type: Optional[str] = None, agent_id: Optional[str] = None):
    records = get_audit_trail(filter_type=filter_type, agent_id=agent_id)
    return {"count": len(records), "records": records}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
