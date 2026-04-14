#!/usr/bin/env bash
# doc-verify.sh — pre-commit gate. Every job.md must have a rendered SVG
# sibling and a non-empty github_commit in frontmatter (except 'draft').
set -euo pipefail

JOB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOB_SLUG="$(basename "$JOB_DIR")"
JOB_MD="$JOB_DIR/job.md"
SVG="$JOB_DIR/assets/$JOB_SLUG.svg"

[ -f "$JOB_MD" ] || { echo "[doc-verify] FAIL: missing job.md"; exit 1; }

status="$(awk -F': *' '/^status:/{print $2; exit}' "$JOB_MD" || true)"
[ "$status" = "draft" ] && { echo "[doc-verify] skip: draft status"; exit 0; }

[ -f "$SVG" ] || { echo "[doc-verify] FAIL: missing $SVG"; exit 2; }

commit="$(awk -F': *' '/^github_commit:/{print $2; exit}' "$JOB_MD" || true)"
if [ -z "$commit" ] || [ "$commit" = "pending" ]; then
  echo "[doc-verify] FAIL: github_commit not set in frontmatter"
  exit 3
fi

echo "[doc-verify] ok: $JOB_SLUG"
