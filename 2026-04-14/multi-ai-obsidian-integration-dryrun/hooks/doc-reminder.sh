#!/usr/bin/env bash
# doc-reminder.sh — nudge when this job has status: draft for >24h.
# Intended as a Claude Code SessionStart hook or a cron entry.
set -euo pipefail

JOB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOB_MD="$JOB_DIR/job.md"
[ -f "$JOB_MD" ] || exit 0

status="$(awk -F': *' '/^status:/{print $2; exit}' "$JOB_MD" || true)"
[ "$status" = "draft" ] || exit 0

# Age check — portable across macOS and Linux
if stat -f %m "$JOB_MD" >/dev/null 2>&1; then
  mtime=$(stat -f %m "$JOB_MD")
else
  mtime=$(stat -c %Y "$JOB_MD")
fi
now=$(date +%s)
age=$(( now - mtime ))
if [ "$age" -gt 86400 ]; then
  echo "[doc-reminder] job $(basename "$JOB_DIR") has been draft for > 24h ($age s)"
fi
