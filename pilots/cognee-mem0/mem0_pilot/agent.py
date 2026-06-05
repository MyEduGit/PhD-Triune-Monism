#!/usr/bin/env python3
"""
Mem0 Pilot — Interactive Semantic Retrieval Agent
Run after ingest.py has stored memories.

Usage:
    python agent.py                       # interactive REPL
    python agent.py "your question here"  # single query

UrantiOS: Truth · Beauty · Goodness
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import MEM0_CONFIG, USER_ID, SAMPLE_QUERIES


def get_memory():
    from mem0 import Memory
    return Memory.from_config(MEM0_CONFIG)


def search(m, query: str, top_k: int = 5) -> list:
    return m.search(query, user_id=USER_ID, limit=top_k) or []


def run_single(question: str):
    m = get_memory()
    t0 = time.time()
    results = search(m, question)
    elapsed = time.time() - t0
    print(f"\nQuery : {question}")
    print(f"Time  : {elapsed:.2f}s  |  Results: {len(results)}")
    print("-" * 60)
    for i, r in enumerate(results, 1):
        score  = r.get("score", "?")
        memory = r.get("memory", str(r))
        table  = r.get("metadata", {}).get("table", "?")
        print(f"[{i}] [{table}] score={score:.3f}")
        print(f"     {memory}")


def repl():
    m = get_memory()
    total = len(m.get_all(user_id=USER_ID) or [])
    print("=" * 60)
    print(f"MEM0 AGENT — {total} memories loaded")
    print("Commands: 'demo' | 'all' — list memories | 'exit'")
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
        if text.lower() == "all":
            memories = m.get_all(user_id=USER_ID) or []
            print(f"{len(memories)} stored memories:")
            for mem in memories[:20]:
                print(f"  • {mem.get('memory', str(mem))[:120]}")
            if len(memories) > 20:
                print(f"  … ({len(memories)-20} more)")
            continue
        if text.lower() == "demo":
            for q, _ in SAMPLE_QUERIES:
                t0 = time.time()
                res = m.search(q, user_id=USER_ID) or []
                elapsed = time.time() - t0
                print(f"\n>> {q}")
                print(f"   {len(res)} result(s) in {elapsed:.2f}s")
                for r in res[:2]:
                    score = r.get("score", "?")
                    mem   = r.get("memory", "")[:160]
                    print(f"   [{score:.3f}] {mem}")
            continue

        t0 = time.time()
        results = search(m, text)
        print(f"{len(results)} result(s)  {time.time()-t0:.2f}s")
        for i, r in enumerate(results, 1):
            score  = r.get("score", "?")
            memory = r.get("memory", str(r))
            table  = r.get("metadata", {}).get("table", "?")
            print(f"  [{i}] [{table}] score={score:.3f}")
            print(f"       {memory[:280]}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_single(" ".join(sys.argv[1:]))
    else:
        repl()
