"""
Mem0 Pilot — Configuration
UrantiOS: Truth · Beauty · Goodness
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs" / "mem0"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MEM0_CONFIG = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "roadmap_pilot",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 1536,
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0,
            "api_key": OPENAI_API_KEY,
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": OPENAI_API_KEY,
        },
    },
}

USER_ID = "mircea"
AGENT_PHD = "hetzy_phd"
AGENT_LEGISLATURE = "council_legislature"
AGENT_COMMUNITY = "community_tier_agent"

SAMPLE_QUERIES = [
    ("What are the deliverables for Phase 2 of the PhD research?", "phd_layers"),
    ("Which PhD steps are related to the hard problem of consciousness?", "phd_layers"),
    ("What infrastructure supports the AI legislature governance phases?", "ai_legislature"),
    ("Show all community tiers with active status.", "community_tiers"),
    ("What steps have the governance principle of Truth?", None),
    ("How is the Infinite Spirit connected to the PhD thesis?", "phd_layers"),
    ("Which AI legislature phases depend on earlier phases?", "ai_legislature"),
    ("What are the revenue models for the community tiers?", "community_tiers"),
    ("Show all items linked to Governance Mechanics.", None),
    ("What is the relationship between the Council of Seven and the UrantiOS Constitution?", None),
]
