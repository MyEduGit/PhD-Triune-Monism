#!/bin/bash
# SessionStart hook — PhD-Triune-Monism / UrantiOS
# Installs markdown tooling and verifies environment on session start.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

# ── markdownlint-cli (markdown linter) ─────────────────────────────────────
if ! command -v markdownlint &>/dev/null; then
  if command -v npm &>/dev/null; then
    echo "[session-start] Installing markdownlint-cli..."
    npm install -g markdownlint-cli --no-audit --no-fund 2>&1
  else
    echo "[session-start] WARN: npm not found — cannot install markdownlint."
  fi
else
  echo "[session-start] markdownlint already available."
fi

# ── pandoc (document conversion) ────────────────────────────────────────────
if ! command -v pandoc &>/dev/null; then
  if command -v apt-get &>/dev/null; then
    echo "[session-start] Installing pandoc..."
    apt-get install -y --no-install-recommends pandoc 2>&1
  elif command -v brew &>/dev/null; then
    brew install pandoc 2>&1
  else
    echo "[session-start] WARN: Cannot install pandoc — no package manager found."
  fi
else
  echo "[session-start] pandoc already available."
fi

echo "[session-start] PhD-Triune-Monism session ready."
