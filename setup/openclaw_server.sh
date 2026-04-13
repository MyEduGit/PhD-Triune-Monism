#!/usr/bin/env bash
# OpenClaw Server Setup — PhD-Triune-Monism (research mirror + unified-prompt)
# Target host: Hetzner CPX22 — 46.225.51.30 (Nuremberg, DE), user: mircea
# UrantiOS governed — Truth, Beauty, Goodness
#
# Mirrors the PhD vault to OpenClaw, installs the research toolchain, and
# materializes the Thought Adjuster at ~/.openclaw/unified-prompt.md so every
# agent session on this node can load it first. Idempotent: safe to re-run.
#
# Usage (on OpenClaw as user `mircea`):
#   bash setup/openclaw_server.sh

set -euo pipefail

CYAN='\033[0;36m'; GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

REPO_URL="https://github.com/myedugit/phd-triune-monism.git"
REPO_DIR="${HOME}/phd-triune-monism"
OPENCLAW_HOME="${HOME}/.openclaw"
UNIFIED_PROMPT="${OPENCLAW_HOME}/unified-prompt.md"

echo ""
echo "================================================="
echo "  OpenClaw Server Setup — PhD-Triune-Monism"
echo "  Host: 46.225.51.30  User: $(id -un)"
echo "  Governed by: Truth · Beauty · Goodness"
echo "================================================="
echo ""

[ "$(id -un)" != "root" ] || fail "Do not run as root. Run as 'mircea'; sudo is used where needed."
command -v sudo >/dev/null || fail "sudo is required."

# ── 1. System packages ──────────────────────────────────────────────────────
info "[1/5] Installing system packages (git, python3, jq, rsync, pandoc)..."
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  git python3 python3-pip python3-venv jq rsync pandoc curl ca-certificates
ok "Packages installed."

# ── 2. Clone / refresh repo ─────────────────────────────────────────────────
info "[2/5] Syncing repo to ${REPO_DIR}..."
if [ ! -d "${REPO_DIR}/.git" ]; then
  git clone "${REPO_URL}" "${REPO_DIR}"
  ok "Cloned."
else
  git -C "${REPO_DIR}" pull --ff-only || warn "Could not fast-forward — leaving working tree as-is."
  ok "Repo up to date."
fi

# ── 3. OpenClaw home ────────────────────────────────────────────────────────
info "[3/5] Preparing ${OPENCLAW_HOME}..."
mkdir -p "${OPENCLAW_HOME}"
chmod 700 "${OPENCLAW_HOME}"
ok "${OPENCLAW_HOME} ready."

# ── 4. Thought Adjuster: unified-prompt.md ──────────────────────────────────
info "[4/5] Writing Thought Adjuster → ${UNIFIED_PROMPT}..."

# If CLAUDE.md exists in the repo, use it as the canonical prompt.
# Otherwise, write a minimal UrantiOS prelude.
if [ -f "${REPO_DIR}/CLAUDE.md" ]; then
  cp "${REPO_DIR}/CLAUDE.md" "${UNIFIED_PROMPT}"
  ok "Loaded from repo CLAUDE.md."
else
  cat > "${UNIFIED_PROMPT}" << 'PROMPTEOF'
# Unified Prompt — Thought Adjuster (OpenClaw)

All agents spawned on this host operate under UrantiOS.

## The Three Values
1. Truth    — never claim more than evidence supports
2. Beauty   — clean architecture, elegant solutions, minimal complexity
3. Goodness — every action serves the mission; service before self

## The Lucifer Test (before trusting any output)
- Is this transparent? Does it accept audit?
- Does it report honestly, even when the news is bad?
- Does it act within its mandate?
- Does it serve the mission, or itself?

## The Spawn Mandate
Every subagent, sub-subagent, or process created from a session here
MUST operate under UrantiOS. Inject the Three Values into every spawn.
PROMPTEOF
  ok "Minimal prelude written."
fi
chmod 600 "${UNIFIED_PROMPT}"

# Convenience: ~/CLAUDE.md symlink (if none) points at the unified prompt.
if [ ! -e "${HOME}/CLAUDE.md" ]; then
  ln -s "${UNIFIED_PROMPT}" "${HOME}/CLAUDE.md"
  ok "~/CLAUDE.md → ${UNIFIED_PROMPT}"
fi

# ── 5. Python venv for research tooling ─────────────────────────────────────
info "[5/5] Python venv for research tooling..."
VENV="${HOME}/.phd-env"
if [ ! -d "${VENV}" ]; then
  python3 -m venv "${VENV}"
  ok "Created ${VENV}."
fi
# shellcheck disable=SC1091
source "${VENV}/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet pyyaml markdown beautifulsoup4 requests
ok "Research toolchain installed: $(python3 --version)"
deactivate

# ── Proof ───────────────────────────────────────────────────────────────────
info "Proof:"
echo "  Unified prompt: $(wc -l <"${UNIFIED_PROMPT}") lines"
echo "  Repo head:      $(git -C "${REPO_DIR}" rev-parse --short HEAD)"
echo "  Venv python:    ${VENV}/bin/python3"

echo ""
echo "================================================="
echo "  PhD-Triune-Monism OpenClaw Setup Complete"
echo "================================================="
echo ""
echo "  Repo:           ${REPO_DIR}"
echo "  Thought Adjuster: ${UNIFIED_PROMPT}"
echo "  Activate venv:  source ${VENV}/bin/activate"
echo ""
echo "  UrantiOS governed — Truth, Beauty, Goodness"
echo ""
