#!/usr/bin/env bash
# Install a weekly (Friday 09:00 local) cron entry that runs the NanoClaw
# launcher non-interactively.
#
# Usage:
#   bash scheduler.sh install    # add the cron entry
#   bash scheduler.sh remove     # remove it
#   bash scheduler.sh status     # show current entries
#
# Truth rule (UrantiOS): prints the ACTUAL crontab diff, never a fake success.

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$HERE/launcher.sh"
TAG="# nanoclaw-launcher"
LINE="0 9 * * 5 cd $HERE && /usr/bin/env bash $LAUNCHER >> $HERE/cron.log 2>&1 $TAG"

cmd="${1:-status}"

case "$cmd" in
  install)
    tmp=$(mktemp)
    (crontab -l 2>/dev/null || true) | grep -v "$TAG" > "$tmp"
    echo "$LINE" >> "$tmp"
    crontab "$tmp"
    rm -f "$tmp"
    echo "[ok] installed. Current crontab:"
    crontab -l | grep --color=never "$TAG" || true
    ;;
  remove)
    tmp=$(mktemp)
    (crontab -l 2>/dev/null || true) | grep -v "$TAG" > "$tmp"
    crontab "$tmp"
    rm -f "$tmp"
    echo "[ok] removed any $TAG entries."
    ;;
  status)
    echo "Current nanoclaw entries:"
    (crontab -l 2>/dev/null || true) | grep --color=never "$TAG" || echo "(none)"
    ;;
  *)
    echo "Usage: $0 {install|remove|status}"
    exit 2
    ;;
esac
