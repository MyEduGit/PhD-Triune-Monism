#!/usr/bin/env bash
# Run both pilots end-to-end and then benchmark
# UrantiOS: Truth · Beauty · Goodness
set -e

cd "$(dirname "$0")"

echo "======================================"
echo "COGNEE + MEM0 PILOT — FULL RUN"
echo "======================================"

# Check .env
if [ ! -f .env ]; then
  echo "[error] .env not found. Copy .env.example and add your API keys."
  exit 1
fi

export $(grep -v '^#' .env | xargs)

# Qdrant check
echo "[check] Qdrant..."
curl -sf http://localhost:6333/health > /dev/null || {
  echo "[warn] Qdrant not running. Start with: docker run -p 6333:6333 qdrant/qdrant"
  echo "       Mem0 pilot will fail without it."
}

echo ""
echo "--- COGNEE PILOT ---"
python cognee_pilot/ingest.py

echo ""
echo "--- MEM0 PILOT ---"
python mem0_pilot/ingest.py

echo ""
echo "--- BENCHMARK ---"
python comparison/benchmark.py

echo ""
echo "All done. Results in outputs/"
