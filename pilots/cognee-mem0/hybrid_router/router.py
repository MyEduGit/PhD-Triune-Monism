"""
Hybrid Memory Router
Classifies query intent and routes to Cognee (structural/relational)
or Mem0 (semantic/fuzzy), or both, then merges results.

UrantiOS: Truth · Beauty · Goodness
"""
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from cognee_pilot.config import LLM_API_KEY, LLM_PROVIDER, LLM_MODEL, COGNEE_DB_PATH
from mem0_pilot.config import MEM0_CONFIG, USER_ID


class Route(str, Enum):
    COGNEE = "cognee"
    MEM0 = "mem0"
    BOTH = "both"


@dataclass
class RouterResult:
    query: str
    route: Route
    cognee_results: list = field(default_factory=list)
    mem0_results: list = field(default_factory=list)
    merged: list = field(default_factory=list)
    cognee_time_s: float = 0.0
    mem0_time_s: float = 0.0
    total_time_s: float = 0.0
    reasoning: str = ""


# Structural query signals → Cognee (graph traversal)
STRUCTURAL = [
    "depends on", "dependency", "what feeds", "contributes to",
    "linked to", "trace", "chain", "path to", "chapter", "phase",
    "deliverables for", "findings from", "produces", "leads to",
    "what requires", "prerequisite", "in order to",
]

# Semantic/fuzzy query signals → Mem0 (vector similarity)
SEMANTIC = [
    "like", "related to", "similar", "about", "involving",
    "concerning", "anything", "show all", "everything about",
    "where is", "who", "find", "search",
]


def classify(query: str) -> tuple[Route, str]:
    q = query.lower()
    structural_hits = [s for s in STRUCTURAL if s in q]
    semantic_hits   = [s for s in SEMANTIC   if s in q]

    if structural_hits and not semantic_hits:
        return Route.COGNEE, f"structural signals: {structural_hits}"
    if semantic_hits and not structural_hits:
        return Route.MEM0, f"semantic signals: {semantic_hits}"
    if structural_hits and semantic_hits:
        return Route.BOTH, f"mixed — structural: {structural_hits}  semantic: {semantic_hits}"
    return Route.BOTH, "ambiguous — querying both"


async def _cognee(query: str) -> tuple[list, float]:
    import cognee
    from cognee.api.v1.search import SearchType
    cognee.config.llm_api_key = LLM_API_KEY
    cognee.config.llm_provider = LLM_PROVIDER
    cognee.config.llm_model = LLM_MODEL
    cognee.config.db_path = COGNEE_DB_PATH
    t0 = time.time()
    try:
        r = await cognee.search(SearchType.INSIGHTS, query) or []
        return [{"source": "cognee", "content": str(x), "score": None} for x in r], time.time()-t0
    except Exception as exc:
        return [{"source": "cognee", "content": f"error: {exc}", "score": None}], time.time()-t0


def _mem0(query: str) -> tuple[list, float]:
    from mem0 import Memory
    m = Memory.from_config(MEM0_CONFIG)
    t0 = time.time()
    try:
        r = m.search(query, user_id=USER_ID) or []
        return [{"source": "mem0",
                 "content": x.get("memory", str(x)),
                 "score": x.get("score"),
                 "metadata": x.get("metadata", {})}
                for x in r], time.time()-t0
    except Exception as exc:
        return [{"source": "mem0", "content": f"error: {exc}",
                 "score": None, "metadata": {}}], time.time()-t0


async def route(query: str, force: Optional[Route] = None) -> RouterResult:
    """Classify intent, query the right system(s), return merged results."""
    t_start = time.time()
    chosen, reasoning = (force, f"forced={force}") if force else classify(query)
    r = RouterResult(query=query, route=chosen, reasoning=reasoning)

    if chosen in (Route.COGNEE, Route.BOTH):
        r.cognee_results, r.cognee_time_s = await _cognee(query)
    if chosen in (Route.MEM0, Route.BOTH):
        r.mem0_results, r.mem0_time_s = _mem0(query)

    seen, merged = set(), []
    for item in r.cognee_results + r.mem0_results:
        key = item["content"][:120]
        if key not in seen:
            seen.add(key)
            merged.append(item)
    r.merged = merged
    r.total_time_s = round(time.time()-t_start, 3)
    return r
