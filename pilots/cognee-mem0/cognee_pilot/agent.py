#!/usr/bin/env python3
"""
Cognee Pilot — Interactive Query Agent
Run after ingest.py has built the knowledge graph.

Usage:
    python agent.py                       # interactive REPL
    python agent.py "your question here"  # single query

UrantiOS: Truth · Beauty · Goodness
"""
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import LLM_API_KEY, LLM_PROVIDER, LLM_MODEL, COGNEE_DB_PATH, SAMPLE_QUERIES


async def setup():
    import cognee
    if not LLM_API_KEY:
        raise EnvironmentError("Set OPENAI_API_KEY in .env")
    cognee.config.llm_api_key = LLM_API_KEY
    cognee.config.llm_provider = LLM_PROVIDER
    cognee.config.llm_model = LLM_MODEL
    cognee.config.db_path = COGNEE_DB_PATH


async def query_graph(text: str) -> list:
    import cognee
    from cognee.api.v1.search import SearchType
    return await cognee.search(SearchType.INSIGHTS, text) or []


async def run_single(question: str):
    await setup()
    t0 = time.time()
    results = await query_graph(question)
    elapsed = time.time() - t0
    print(f"\nQuery : {question}")
    print(f"Time  : {elapsed:.2f}s  |  Results: {len(results)}")
    print("-" * 60)
    if results:
        for i, r in enumerate(results, 1):
            print(f"[{i}] {str(r)[:300]}")
    else:
        print("(no results — run ingest.py first)")


async def repl():
    await setup()
    print("=" * 60)
    print("COGNEE AGENT — Knowledge Graph Query")
    print("Commands: 'demo' — run all sample queries | 'exit' — quit")
    print("=" * 60)

    while True:
        try:
            text = input("\nQuery> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not text:
            continue
        if text.lower() == "exit":
            break
        if text.lower() == "demo":
            for q in SAMPLE_QUERIES:
                print(f"\n>> {q}")
                t0 = time.time()
                results = await query_graph(q)
                elapsed = time.time() - t0
                print(f"   {len(results)} result(s) in {elapsed:.2f}s")
                for r in results[:2]:
                    print(f"   • {str(r)[:180]}")
            continue

        t0 = time.time()
        results = await query_graph(text)
        print(f"{len(results)} result(s) in {time.time()-t0:.2f}s")
        for i, r in enumerate(results, 1):
            print(f"  [{i}] {str(r)[:300]}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(run_single(" ".join(sys.argv[1:])))
    else:
        asyncio.run(repl())
