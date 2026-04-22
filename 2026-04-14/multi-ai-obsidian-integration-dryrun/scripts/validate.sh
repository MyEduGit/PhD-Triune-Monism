#!/usr/bin/env bash
# validate.sh — render Mermaid, check links, fail loud on missing artefacts.
set -euo pipefail

JOB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOB_SLUG="$(basename "$JOB_DIR")"
MMD="$JOB_DIR/assets/$JOB_SLUG.mmd"
SVG="$JOB_DIR/assets/$JOB_SLUG.svg"
PNG="$JOB_DIR/assets/$JOB_SLUG.png"

[ -f "$MMD" ] || { echo "[validate] FAIL: missing $MMD"; exit 1; }

if command -v mmdc >/dev/null 2>&1; then
  echo "[validate] rendering SVG"
  mmdc -i "$MMD" -o "$SVG"
  echo "[validate] rendering PNG"
  mmdc -i "$MMD" -o "$PNG"
else
  echo "[validate] FAIL: mmdc not installed. npm i -g @mermaid-js/mermaid-cli"
  exit 2
fi

# Confirm job.md references the diagram
if ! grep -q "$JOB_SLUG.svg\|$JOB_SLUG.mmd" "$JOB_DIR/job.md"; then
  echo "[validate] FAIL: job.md does not reference the diagram"
  exit 3
fi

echo "[validate] ok: $JOB_SLUG"
