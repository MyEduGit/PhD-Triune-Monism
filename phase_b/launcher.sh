#!/usr/bin/env bash
# NanoClaw Full Interactive Pipeline Launcher
# Phase A -> Phase B -> Interactive Dashboard -> Notifications
#
# Location:  phase_b/launcher.sh  (run from phase_b/)
# Usage:     bash launcher.sh              # run pipeline only
#            bash launcher.sh --ui          # also launch Streamlit
#            bash launcher.sh --ui --skip-notify
#
# Governance: UrantiOS / Triune Monism.
# Truth rule: every stage reports WHAT IT DID, not what it wished it did.
# Missing scripts are SKIPPED with a warning, not silently pretended.

set -u  # unset var = error, but keep pipe-tolerance for gracefulness

# ----- CONFIG ---------------------------------------------------------------
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

PHASE_A_DIR="${PHASE_A_DIR:-../phase_a/jobs}"
OUTPUT_JSON_DIR="${OUTPUT_JSON_DIR:-./json_repository}"
ASSETS_DIR="${ASSETS_DIR:-./assets}"
DASHBOARD_MD="$ASSETS_DIR/phase_b_sre_dashboard.md"
STREAMLIT_APP="./app.py"
EXEC_LOG="./execution_log.txt"
MODELS=(${MODELS:-gpt claude gemma4 grok})

EMAIL_TO="${EMAIL_TO:-research@phd.edu}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# Scripts — SKIPPED gracefully if missing
EE_SCRIPT="./scripts/ee_extract_triples.py"
CM_SCRIPT="./scripts/sre_process_and_generate.py"
VIZ_SCRIPT="./scripts/sre_visualizer.py"

WANT_UI=0
WANT_NOTIFY=1
for a in "$@"; do
  case "$a" in
    --ui)          WANT_UI=1 ;;
    --skip-notify) WANT_NOTIFY=0 ;;
    -h|--help)
      grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
  esac
done

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "$EXEC_LOG"; }
warn() { printf '[%s] WARN: %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "$EXEC_LOG" >&2; }

echo "===================================================================="
echo " NanoClaw Full Pipeline & Interactive Dashboard"
echo "===================================================================="

mkdir -p "$OUTPUT_JSON_DIR" "$ASSETS_DIR" "$(dirname "$EXEC_LOG")"
: > "$EXEC_LOG"
log "Launcher start. HERE=$HERE  UI=$WANT_UI  NOTIFY=$WANT_NOTIFY"

# ----- 1. Entity Extractor --------------------------------------------------
if [[ -f "$EE_SCRIPT" ]]; then
  log "Running Entity Extractor..."
  if [[ -d "$PHASE_A_DIR" ]]; then
    for model in "${MODELS[@]}"; do
      for task_dir in "$PHASE_A_DIR"/*/; do
        [[ -d "$task_dir" ]] || continue
        log_file="$task_dir/responses/$model.md"
        [[ -f "$log_file" ]] || continue
        out="$OUTPUT_JSON_DIR/$(basename "$task_dir")_${model}_triples.json"
        if python3 "$EE_SCRIPT" "$log_file" "$out"; then
          log "EE ok: $model / $(basename "$task_dir") -> $out"
        else
          warn "EE failed: $model / $(basename "$task_dir")"
        fi
      done
    done
  else
    warn "PHASE_A_DIR not found: $PHASE_A_DIR (skipping EE inputs)"
  fi
else
  warn "EE_SCRIPT missing: $EE_SCRIPT  (skipping stage 1)"
fi

# ----- 2. Conflict Mapper & Hypothesis Generator ----------------------------
shopt -s nullglob
json_files=("$OUTPUT_JSON_DIR"/*.json)
shopt -u nullglob

if [[ -f "$CM_SCRIPT" ]]; then
  if (( ${#json_files[@]} > 0 )); then
    log "Running Conflict Mapper & Hypothesis Generator on ${#json_files[@]} file(s)..."
    if python3 "$CM_SCRIPT" "${json_files[@]}"; then
      log "CM/HG ok."
    else
      warn "CM/HG failed."
    fi
  else
    warn "No JSON triple files in $OUTPUT_JSON_DIR (skipping CM/HG)."
  fi
else
  warn "CM_SCRIPT missing: $CM_SCRIPT (skipping stage 2)"
fi

# ----- 3. Visualizer --------------------------------------------------------
if [[ -f "$VIZ_SCRIPT" ]]; then
  log "Running SRE visualizer..."
  if python3 "$VIZ_SCRIPT"; then
    log "Dashboard Markdown written: $DASHBOARD_MD"
  else
    warn "Visualizer failed."
  fi
else
  warn "VIZ_SCRIPT missing: $VIZ_SCRIPT (skipping stage 3)"
fi

# ----- 4. Notifications -----------------------------------------------------
if (( WANT_NOTIFY )); then
  log "Sending notifications..."
  EMAIL_TO="$EMAIL_TO" \
  TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
  TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
  DASHBOARD_MD="$DASHBOARD_MD" \
  python3 - <<'PYEOF' || warn "Notification step had failures (see above)."
import os, smtplib, requests
from email.message import EmailMessage

email_to   = os.environ.get("EMAIL_TO", "")
tok        = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat       = os.environ.get("TELEGRAM_CHAT_ID", "")
dashboard  = os.environ.get("DASHBOARD_MD", "")

if email_to:
    try:
        m = EmailMessage()
        m.set_content(f"NanoClaw pipeline complete.\nDashboard: {dashboard}")
        m["Subject"] = "NanoClaw pipeline complete"
        m["From"]    = "nanoclaw@localhost"
        m["To"]      = email_to
        with smtplib.SMTP("localhost") as s:
            s.send_message(m)
        print(f"[ok] email sent to {email_to}")
    except Exception as e:
        print(f"[warn] email failed: {e}")
else:
    print("[skip] EMAIL_TO empty")

if tok and chat:
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendMessage",
            data={"chat_id": chat,
                  "text": f"NanoClaw pipeline complete. Dashboard: {dashboard}"},
            timeout=10,
        )
        r.raise_for_status()
        print("[ok] telegram sent")
    except Exception as e:
        print(f"[warn] telegram failed: {e}")
else:
    print("[skip] telegram token or chat_id missing")
PYEOF
else
  log "Notifications disabled (--skip-notify)."
fi

# ----- 5. Streamlit (optional) ---------------------------------------------
if (( WANT_UI )); then
  if [[ -f "$STREAMLIT_APP" ]]; then
    log "Launching Streamlit on 127.0.0.1..."
    exec streamlit run "$STREAMLIT_APP" \
      --browser.serverAddress=127.0.0.1 \
      --server.headless=false
  else
    warn "Streamlit app missing: $STREAMLIT_APP"
    exit 2
  fi
fi

echo "===================================================================="
log "Pipeline finished. See $EXEC_LOG for audit trail."
echo "===================================================================="
