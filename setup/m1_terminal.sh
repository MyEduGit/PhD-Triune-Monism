#!/usr/bin/env bash
# MacBook Pro M1 Terminal Setup — PhD-Triune-Monism / UrantiOS
# UrantiOS governed — Truth, Beauty, Goodness
set -euo pipefail

CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }

echo ""
echo "================================================="
echo "  MacBook Pro M1 Terminal Setup"
echo "  Project: PhD-Triune-Monism / UrantiOS"
echo "  Governed by: Truth · Beauty · Goodness"
echo "================================================="
echo ""

# Verify arm64 architecture
ARCH="$(uname -m)"
if [ "$ARCH" != "arm64" ]; then
  warn "Expected arm64 (Apple Silicon), got: $ARCH"
  warn "Continuing anyway — some paths may differ."
fi

# ── 1. Homebrew (arm64) ─────────────────────────────────────────────────────
info "[1/7] Homebrew..."
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
  ok "Homebrew installed."
else
  brew update --quiet
  ok "Homebrew up to date."
fi

# ── 2. Core CLI tools ────────────────────────────────────────────────────────
info "[2/7] Core CLI tools..."
brew install git node python3 wget jq || true
ok "git: $(git --version | cut -d' ' -f3)  node: $(node --version)  python: $(python3 --version | cut -d' ' -f2)"

# ── 3. Claude Code CLI ──────────────────────────────────────────────────────
info "[3/7] Claude Code CLI..."
if ! command -v claude &>/dev/null; then
  npm install -g @anthropic-ai/claude-code
  ok "Claude Code installed: $(claude --version 2>/dev/null || echo 'installed')"
else
  ok "Claude Code already present."
fi

# ── 4. SSH config for Hetzner ───────────────────────────────────────────────
info "[4/7] SSH config (Hetzner execution node)..."
SSH_DIR="$HOME/.ssh"
SSH_CONFIG="$SSH_DIR/config"
mkdir -p "$SSH_DIR" && chmod 700 "$SSH_DIR"

if ! grep -q "hetzner-urantios" "$SSH_CONFIG" 2>/dev/null; then
  cat >> "$SSH_CONFIG" << 'SSHEOF'

# UrantiOS — Hetzner execution node
Host hetzner-urantios
  HostName 46.225.51.30
  User mircea
  IdentityFile ~/.ssh/id_ed25519
  ServerAliveInterval 60
  ServerAliveCountMax 3
  StrictHostKeyChecking accept-new
SSHEOF
  ok "SSH config entry 'hetzner-urantios' added."
else
  ok "SSH config for hetzner-urantios already present."
fi

# Ensure an ed25519 key exists
if [ ! -f "$SSH_DIR/id_ed25519" ]; then
  warn "No ~/.ssh/id_ed25519 found."
  warn "Generate one with: ssh-keygen -t ed25519 -C 'macbook-m1'"
  warn "Then: ssh-copy-id -i ~/.ssh/id_ed25519.pub mircea@46.225.51.30"
fi

# ── 5. Git global config ─────────────────────────────────────────────────────
info "[5/7] Git global config..."
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input
ok "Git config applied."

# ── 6. Clone / refresh project repos ────────────────────────────────────────
info "[6/7] Project repos..."
PROJECTS_DIR="$HOME/projects"
mkdir -p "$PROJECTS_DIR"

declare -A REPOS=(
  ["phd-triune-monism"]="https://github.com/myedugit/phd-triune-monism.git"
  ["mircea-constellation"]="https://github.com/myedugit/mircea-constellation.git"
  ["lobsterbot"]="https://github.com/myedugit/lobsterbot.git"
)

for NAME in "${!REPOS[@]}"; do
  DIR="$PROJECTS_DIR/$NAME"
  URL="${REPOS[$NAME]}"
  if [ ! -d "$DIR/.git" ]; then
    git clone "$URL" "$DIR"
    ok "Cloned $NAME."
  else
    git -C "$DIR" pull --ff-only 2>/dev/null || warn "$NAME: could not fast-forward pull."
    ok "$NAME up to date."
  fi
done

# ── 7. Shell env (arm64 Homebrew path + ANTHROPIC_API_KEY hint) ───────────
info "[7/7] Shell environment (~/.zshrc)..."
ZSHRC="$HOME/.zshrc"
touch "$ZSHRC"

if ! grep -q '/opt/homebrew/bin/brew shellenv' "$ZSHRC"; then
  cat >> "$ZSHRC" << 'ZSHEOF'

# ── Homebrew (Apple Silicon arm64) ──────────────────────────────────────────
eval "$(/opt/homebrew/bin/brew shellenv)"
ZSHEOF
  ok "Homebrew shellenv added to ~/.zshrc"
fi

if ! grep -q 'ANTHROPIC_API_KEY' "$ZSHRC"; then
  cat >> "$ZSHRC" << 'ZSHEOF'

# ── Claude Code / Anthropic ──────────────────────────────────────────────────
# export ANTHROPIC_API_KEY="sk-ant-..."   # uncomment and fill in
ZSHEOF
  ok "ANTHROPIC_API_KEY placeholder added to ~/.zshrc"
fi

echo ""
echo "================================================="
echo "  Setup Complete!"
echo ""
echo "  Next steps:"
echo "  1.  source ~/.zshrc"
echo "  2.  Set ANTHROPIC_API_KEY in ~/.zshrc"
echo "  3.  Add SSH key to Hetzner if not done:"
echo "      ssh-keygen -t ed25519 -C 'macbook-m1'"
echo "      ssh-copy-id -i ~/.ssh/id_ed25519.pub mircea@46.225.51.30"
echo "  4.  Test connection: ssh hetzner-urantios"
echo "  5.  Start Claude Code: cd ~/projects/phd-triune-monism && claude"
echo "================================================="
echo ""
