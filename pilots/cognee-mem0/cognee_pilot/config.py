"""
Cognee Pilot — Configuration
UrantiOS: Truth · Beauty · Goodness
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs" / "cognee"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LLM_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

COGNEE_DB_PATH = str(OUTPUT_DIR / "cognee_db")

DATASET_PHD = "phd_research_layers"
DATASET_LEGISLATURE = "ai_legislature_phases"
DATASET_COMMUNITY = "community_business_tiers"

SAMPLE_QUERIES = [
    "What are the deliverables for Phase 2 of the PhD research?",
    "Which PhD research steps have key findings related to physicalism?",
    "What is the status of the AI legislature governance mechanics phase?",
    "How does the AMEP community tier relate to the education mission?",
    "What are all steps with Pending status in the PhD roadmap?",
    "Which AI legislature phases depend on the UrantiOS Constitution?",
    "Show all PhD steps that contribute to Chapter 4 of the dissertation.",
    "What governance principles guide the AI legislature phases?",
    "How does the Infinite Spirit finding connect to the core thesis?",
    "What deliverables are associated with community tiers 3 and 4?",
]
