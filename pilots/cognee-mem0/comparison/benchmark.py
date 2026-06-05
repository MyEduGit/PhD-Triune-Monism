#!/usr/bin/env python3
"""
Cognee vs Mem0 — Side-by-Side Benchmark
Runs the same 10 queries on both systems and compares speed and result counts.

Prerequisites:
    - cognee_pilot/ingest.py must have been run
    - mem0_pilot/ingest.py must have been run

Usage:
    python benchmark.py

UrantiOS: Truth · Beauty · Goodness
"""
import asyncio
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from cognee_pilot.config import (
    LLM_API_KEY, LLM_PROVIDER, LLM_MODEL, COGNEE_DB_PATH,
)
from mem0_pilot.config import MEM0_CONFIG, USER_ID

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "comparison"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK_QUERIES = [
    "What are the deliverables for Phase 2 of the PhD research?",
    "Which PhD research steps are related to physicalism and the hard problem?",
    "What is the status of the AI legislature governance mechanics phase?",
    "How does the AMEP community tier relate to the education mission?",
    "What are all Pending items in the PhD roadmap?",
    "Which AI legislature phases depend on the UrantiOS Constitution?",
    "Show all PhD steps contributing to Chapter 4 of the dissertation.",
    "What governance principles guide the AI legislature phases?",
    "How does the Infinite Spirit finding connect to the core thesis?",
    "What deliverables serve community tiers 3 and 4?",
]


async def run_cognee(queries: list) -> list:
    import cognee
    from cognee.api.v1.search import SearchType
    cognee.config.llm_api_key = LLM_API_KEY
    cognee.config.llm_provider = LLM_PROVIDER
    cognee.config.llm_model = LLM_MODEL
    cognee.config.db_path = COGNEE_DB_PATH

    results = []
    for q in queries:
        t0 = time.time()
        try:
            r = await cognee.search(SearchType.INSIGHTS, q) or []
            elapsed = time.time() - t0
            results.append({"query": q, "system": "cognee",
                            "result_count": len(r), "elapsed_s": round(elapsed, 3),
                            "top_result": str(r[0])[:200] if r else "",
                            "status": "ok"})
        except Exception as exc:
            results.append({"query": q, "system": "cognee",
                            "result_count": 0, "elapsed_s": round(time.time()-t0, 3),
                            "top_result": "", "status": str(exc)})
    return results


def run_mem0(queries: list) -> list:
    from mem0 import Memory
    m = Memory.from_config(MEM0_CONFIG)
    results = []
    for q in queries:
        t0 = time.time()
        try:
            r = m.search(q, user_id=USER_ID) or []
            elapsed = time.time() - t0
            top = r[0] if r else {}
            results.append({"query": q, "system": "mem0",
                            "result_count": len(r), "elapsed_s": round(elapsed, 3),
                            "top_result": top.get("memory", "")[:200],
                            "top_score": round(top.get("score", 0), 4) if r else 0,
                            "status": "ok"})
        except Exception as exc:
            results.append({"query": q, "system": "mem0",
                            "result_count": 0, "elapsed_s": round(time.time()-t0, 3),
                            "top_result": "", "top_score": 0, "status": str(exc)})
    return results


def print_table(cognee_res: list, mem0_res: list):
    print("\n" + "="*82)
    print("COGNEE (graph) vs MEM0 (vector) — BENCHMARK")
    print("="*82)
    print(f"{'#':<3} {'Query':<50} {'Cognee':>14} {'Mem0':>14}")
    print("-"*82)
    ct, mt = [], []
    for i, (c, m0) in enumerate(zip(cognee_res, mem0_res), 1):
        cl = f"{c['result_count']}r / {c['elapsed_s']}s" if c["status"]=="ok" else "ERR"
        ml = f"{m0['result_count']}r / {m0['elapsed_s']}s" if m0["status"]=="ok" else "ERR"
        qs = (c["query"][:48] + ".." if len(c["query"]) > 48 else c["query"])
        print(f"{i:<3} {qs:<50} {cl:>14} {ml:>14}")
        if c["status"]=="ok":  ct.append(c["elapsed_s"])
        if m0["status"]=="ok": mt.append(m0["elapsed_s"])
    print("-"*82)
    avg_c = sum(ct)/max(len(ct),1)
    avg_m = sum(mt)/max(len(mt),1)
    faster = "Mem0" if avg_m < avg_c else "Cognee"
    print(f"{'Avg response time':<53} {avg_c:>14.3f}s {avg_m:>14.3f}s")
    print(f"{'Queries OK':<53} {len(ct):>14} {len(mt):>14}")
    print(f"\nFaster system: {faster} ({min(avg_c,avg_m):.3f}s vs {max(avg_c,avg_m):.3f}s)")
    print("="*82)


async def main():
    print("=" * 60)
    print("BENCHMARK — Cognee (graph) vs Mem0 (vector)")
    print("UrantiOS: Truth · Beauty · Goodness")
    print("=" * 60)

    print("\n[1/2] Running Cognee queries...")
    cognee_results = await run_cognee(BENCHMARK_QUERIES)

    print("\n[2/2] Running Mem0 queries...")
    mem0_results = run_mem0(BENCHMARK_QUERIES)

    print_table(cognee_results, mem0_results)

    out = OUTPUT_DIR / "benchmark_results.json"
    out.write_text(json.dumps({"cognee": cognee_results, "mem0": mem0_results}, indent=2))
    print(f"\nFull results → {out}")


if __name__ == "__main__":
    asyncio.run(main())
