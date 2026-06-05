#!/usr/bin/env python3
"""
Mem0 Pilot — Ingestion Script
Loads the three roadmap tables into Mem0 vector memory with structured metadata.

Usage:
    python ingest.py

UrantiOS: Truth · Beauty · Goodness
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    DATA_DIR, OUTPUT_DIR, MEM0_CONFIG,
    USER_ID, AGENT_PHD, AGENT_LEGISLATURE, AGENT_COMMUNITY,
    SAMPLE_QUERIES,
)


# ── Row → memory text ────────────────────────────────────────────────────────

def row_to_text(row: dict, table: str) -> str:
    if table == "phd_layers":
        return (
            f"PhD research step {row['step_id']} ({row['step_name']}) "
            f"is part of Phase {row['phase_id']} ({row['phase_name']}). "
            f"{row['description']} "
            f"Key finding: {row['key_finding']} "
            f"Deliverables: {row['deliverables']} "
            f"Status: {row['status']}. Chapter: {row['phd_chapter']}. "
            f"Timeline: {row['timeline']}. Principle: {row['governance_principle']}."
        )
    if table == "ai_legislature":
        return (
            f"AI Legislature Phase {row['phase_id']} is called {row['phase_name']}: {row['title']}. "
            f"{row['description']} "
            f"Deliverables: {row['deliverables']} "
            f"Status: {row['status']}. Infrastructure: {row['infrastructure']}. "
            f"Depends on: {row['dependencies']}. Principle: {row['governance_principle']}. "
            f"Timeline: {row['timeline']}. Agents: {row['agents_involved']}."
        )
    if table == "community_tiers":
        return (
            f"Community Tier {row['tier_id']} ({row['tier_name']}) role: {row['role']}. "
            f"{row['description']} "
            f"Members: {row['members_estimate']}. Access: {row['access_level']}. "
            f"Infrastructure: {row['infrastructure']}. Revenue: {row['revenue_model']}. "
            f"Status: {row['current_status']}. UrantiOS: {row['urantios_relation']}. "
            f"Serves: {row['deliverables_served']}."
        )
    return str(row)


def meta(row: dict, table: str) -> dict:
    base = {"table": table}
    if table == "phd_layers":
        base.update({"phase_id": row.get("phase_id", ""),
                     "step_id": row.get("step_id", ""),
                     "status": row.get("status", ""),
                     "phd_chapter": row.get("phd_chapter", ""),
                     "governance_principle": row.get("governance_principle", "")})
    elif table == "ai_legislature":
        base.update({"phase_id": row.get("phase_id", ""),
                     "status": row.get("status", ""),
                     "governance_principle": row.get("governance_principle", "")})
    elif table == "community_tiers":
        base.update({"tier_id": row.get("tier_id", ""),
                     "current_status": row.get("current_status", "")})
    return base


# ── Ingestion ───────────────────────────────────────────────────────────────────

def ingest_table(m, csv_path: Path, table: str, agent_id: str):
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"\n[mem0] Ingesting {len(rows)} rows → '{table}'...")
    added = 0
    for row in rows:
        text = row_to_text(row, table)
        try:
            m.add(
                [{"role": "user", "content": text}],
                user_id=USER_ID,
                agent_id=agent_id,
                metadata=meta(row, table),
            )
            added += 1
            label = row.get("step_id") or row.get("phase_id") or row.get("tier_id", "?")
            print(f"  + row {label}")
        except Exception as exc:
            print(f"  [warn] {exc}")
    print(f"[mem0] {added}/{len(rows)} memories stored for '{table}'")
    return added


def run_sample_queries(m) -> list:
    print("\n" + "="*60)
    print("MEM0 — SAMPLE QUERY VALIDATION")
    print("="*60)
    log = []
    for i, (query, _table) in enumerate(SAMPLE_QUERIES, 1):
        print(f"\nQ{i}: {query}")
        t0 = time.time()
        try:
            results = m.search(query, user_id=USER_ID) or []
            elapsed = time.time() - t0
            for j, r in enumerate(results[:3], 1):
                score  = r.get("score", "?")
                memory = r.get("memory", str(r))[:180]
                print(f"  [{j}] score={score:.3f}  {memory}")
            log.append({"query": query, "result_count": len(results),
                        "elapsed_s": round(elapsed, 3), "status": "ok"})
            print(f"  → {len(results)} result(s)  {elapsed:.2f}s")
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"  [ERROR] {exc}")
            log.append({"query": query, "result_count": 0,
                        "elapsed_s": round(elapsed, 3), "status": str(exc)})

    out = OUTPUT_DIR / "mem0_query_results.json"
    out.write_text(json.dumps(log, indent=2))
    print(f"\n[mem0] results → {out}")
    return log


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("MEM0 PILOT — Roadmap Vector Memory Ingestion")
    print("UrantiOS: Truth · Beauty · Goodness")
    print("=" * 60)

    from mem0 import Memory
    m = Memory.from_config(MEM0_CONFIG)
    print("[mem0] Memory initialised.")

    ingest_table(m, DATA_DIR / "phd_research_layers.csv",    "phd_layers",     AGENT_PHD)
    ingest_table(m, DATA_DIR / "ai_legislature_phases.csv",  "ai_legislature",  AGENT_LEGISLATURE)
    ingest_table(m, DATA_DIR / "community_business_tiers.csv", "community_tiers", AGENT_COMMUNITY)

    total = len(m.get_all(user_id=USER_ID) or [])
    print(f"\n[mem0] Total memories stored: {total}")

    results = run_sample_queries(m)
    ok  = sum(1 for r in results if r["status"] == "ok")
    avg = sum(r["elapsed_s"] for r in results) / max(len(results), 1)
    print(f"\n[mem0] DONE  {ok}/{len(results)} queries OK  avg {avg:.2f}s")


if __name__ == "__main__":
    main()
