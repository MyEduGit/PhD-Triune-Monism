#!/usr/bin/env python3
"""
Cognee Pilot — Ingestion & Knowledge Graph Builder

Loads the three roadmap CSV tables, ingests into Cognee,
builds the knowledge graph, and runs sample queries to validate.

Usage:
    python ingest.py

UrantiOS: Truth · Beauty · Goodness
"""
import asyncio
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    DATA_DIR, OUTPUT_DIR,
    LLM_API_KEY, LLM_PROVIDER, LLM_MODEL,
    DATASET_PHD, DATASET_LEGISLATURE, DATASET_COMMUNITY,
    SAMPLE_QUERIES, COGNEE_DB_PATH,
)
from graph_schema import PhDLayer, AILegislaturePhase, CommunityTier


# ── Data loaders ─────────────────────────────────────────────────────────────────────

def _coerce(row: dict) -> dict:
    for field in ("phase_id", "tier_id"):
        if field in row:
            try:
                row[field] = int(row[field])
            except (ValueError, TypeError):
                pass
    return row


def load_phd_layers() -> list[PhDLayer]:
    rows = []
    with open(DATA_DIR / "phd_research_layers.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = _coerce(row)
            rows.append(PhDLayer(
                step_id=r["step_id"],
                step_name=r["step_name"],
                phase_id=r["phase_id"],
                phase_name=r["phase_name"],
                description=r["description"],
                key_finding=r["key_finding"],
                deliverables=r["deliverables"],
                status=r["status"],
                phd_chapter=r["phd_chapter"],
                timeline=r["timeline"],
                governance_principle=r["governance_principle"],
            ))
    return rows


def load_legislature_phases() -> list[AILegislaturePhase]:
    rows = []
    with open(DATA_DIR / "ai_legislature_phases.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = _coerce(row)
            rows.append(AILegislaturePhase(
                phase_id=r["phase_id"],
                phase_name=r["phase_name"],
                title=r["title"],
                description=r["description"],
                deliverables=r["deliverables"],
                status=r["status"],
                infrastructure=r["infrastructure"],
                dependencies=r["dependencies"],
                governance_principle=r["governance_principle"],
                timeline=r["timeline"],
                agents_involved=r["agents_involved"],
            ))
    return rows


def load_community_tiers() -> list[CommunityTier]:
    rows = []
    with open(DATA_DIR / "community_business_tiers.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = _coerce(row)
            rows.append(CommunityTier(
                tier_id=r["tier_id"],
                tier_name=r["tier_name"],
                role=r["role"],
                description=r["description"],
                members_estimate=r["members_estimate"],
                access_level=r["access_level"],
                infrastructure=r["infrastructure"],
                revenue_model=r["revenue_model"],
                current_status=r["current_status"],
                urantios_relation=r["urantios_relation"],
                deliverables_served=r["deliverables_served"],
            ))
    return rows


def build_document(title: str, records) -> str:
    return title + "\n\n" + "\n\n".join(r.to_text() for r in records)


# ── Cognee helpers ──────────────────────────────────────────────────────────────

async def configure():
    import cognee
    if not LLM_API_KEY:
        raise EnvironmentError("Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
    cognee.config.llm_api_key = LLM_API_KEY
    cognee.config.llm_provider = LLM_PROVIDER
    cognee.config.llm_model = LLM_MODEL
    cognee.config.db_path = COGNEE_DB_PATH
    print(f"[cognee] provider={LLM_PROVIDER}  model={LLM_MODEL}")


async def reset():
    import cognee
    try:
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)
        print("[cognee] cleared previous graph.")
    except Exception as exc:
        print(f"[cognee] reset (non-fatal): {exc}")


async def ingest(doc: str, dataset: str):
    import cognee
    t0 = datetime.now()
    await cognee.add(doc, dataset_name=dataset)
    print(f"[cognee] dataset '{dataset}' added  ({(datetime.now()-t0).total_seconds():.1f}s)")


async def cognify():
    import cognee
    print("[cognee] building knowledge graph…")
    t0 = datetime.now()
    await cognee.cognify()
    print(f"[cognee] graph built in {(datetime.now()-t0).total_seconds():.1f}s")


# ── Query validation ───────────────────────────────────────────────────────────

async def run_sample_queries() -> list[dict]:
    import cognee
    from cognee.api.v1.search import SearchType

    print("\n" + "="*60)
    print("COGNEE — SAMPLE QUERY VALIDATION")
    print("="*60)
    log = []
    for i, q in enumerate(SAMPLE_QUERIES, 1):
        print(f"\nQ{i}: {q}")
        t0 = datetime.now()
        try:
            results = await cognee.search(SearchType.INSIGHTS, q)
            elapsed = (datetime.now()-t0).total_seconds()
            count = len(results) if results else 0
            for j, r in enumerate(results[:3], 1):
                print(f"  [{j}] {str(r)[:200]}")
            log.append({"query": q, "result_count": count,
                        "elapsed_s": round(elapsed, 3), "status": "ok"})
            print(f"  → {count} result(s)  {elapsed:.2f}s")
        except Exception as exc:
            elapsed = (datetime.now()-t0).total_seconds()
            print(f"  [ERROR] {exc}")
            log.append({"query": q, "result_count": 0,
                        "elapsed_s": round(elapsed, 3), "status": str(exc)})

    out = OUTPUT_DIR / "cognee_query_results.json"
    out.write_text(json.dumps(log, indent=2))
    print(f"\n[cognee] results → {out}")
    return log


# ── Main ────────────────────────────────────────────────────────────────────────

async def main():
    print("=" * 60)
    print("COGNEE PILOT — Roadmap Knowledge Graph Ingestion")
    print("UrantiOS: Truth · Beauty · Goodness")
    print("=" * 60)

    await configure()
    await reset()

    phd  = load_phd_layers()
    leg  = load_legislature_phases()
    comm = load_community_tiers()
    print(f"\n[data] {len(phd)} PhD layers | {len(leg)} legislature phases | {len(comm)} community tiers")

    await ingest(build_document("# PhD Research Layers — Triune Monism", phd),         DATASET_PHD)
    await ingest(build_document("# AI Legislature Phases — UrantiOS Governance", leg),  DATASET_LEGISLATURE)
    await ingest(build_document("# Community & Business Tiers — Constellation", comm),  DATASET_COMMUNITY)

    await cognify()

    results = await run_sample_queries()
    ok  = sum(1 for r in results if r["status"] == "ok")
    avg = sum(r["elapsed_s"] for r in results) / max(len(results), 1)
    print(f"\n[cognee] DONE  {ok}/{len(results)} queries OK  avg {avg:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
