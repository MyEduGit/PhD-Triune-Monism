#!/usr/bin/env bash
# install.sh — wire DOC skill hooks into this job folder.
# Idempotent. Safe to rerun.
set -euo pipefail

JOB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[install] job dir: $JOB_DIR"

# Ensure required subdirs exist
mkdir -p "$JOB_DIR/assets/raw" "$JOB_DIR/assets/transcripts"

# Make hooks executable
chmod +x "$JOB_DIR/hooks/"*.sh "$JOB_DIR/scripts/"*.sh 2>/dev/null || true

# Check for mmdc
if ! command -v mmdc >/dev/null 2>&1; then
  echo "[install] WARN: mmdc not found. Install: npm i -g @mermaid-js/mermaid-cli"
fi

# Check for optional env vars; report honestly, do not fail
: "${ZAPIER_WEBHOOK_URL:=}"
: "${NOTION_PARENT_PAGE_ID:=}"
[ -z "$ZAPIER_WEBHOOK_URL" ]      && echo "[install] info: ZAPIER_WEBHOOK_URL not set — fan-out disabled"
[ -z "$NOTION_PARENT_PAGE_ID" ]   && echo "[install] info: NOTION_PARENT_PAGE_ID not set — Notion write disabled"

echo "[install] done"
