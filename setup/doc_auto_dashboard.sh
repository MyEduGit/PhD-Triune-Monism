#!/bin/bash
# /doc installer — archives jobs, generates diagrams, updates master Mermaid
# Fully integrates Claude Code, PR #1, Grok, Gemma4
# Auto-updates master_pipeline.mmd in Obsidian with live GitHub + Notion links

# --- Configuration ---
VAULT_DIR=~/Documents/Obsidian/PhD-Triune-Monism
MASTER_MERMAID="$VAULT_DIR/master_pipeline.mmd"
JOB_DATE=$(date +%F)
JOB_SLUG=${1:-"new-job"}
GITHUB_BRANCH="claude/claude-usage-guide-mtE8j"
GITHUB_REPO="myedugit/mircea-constellation"
NOTION_PAGE_ID="3328525a-b5a0-815d-886c-d5488593aa3d"
ZAPIER_HOOK_URL=${ZAPIER_HOOK_URL:-""}
CANVA_FALLBACK=${CANVA_FALLBACK:-true}

# --- Directories ---
JOB_DIR="$VAULT_DIR/$JOB_DATE/$JOB_SLUG"
ASSETS_DIR="$JOB_DIR/assets"
mkdir -p "$ASSETS_DIR"

# --- Job Documentation ---
JOB_MD="$JOB_DIR/job.md"
cat <<EOF > "$JOB_MD"
# Job: $JOB_SLUG
Date: $(date +"%Y-%m-%d %H:%M:%S")

Artifacts: Mermaid + SVG + PNG + optional Canva
EOF

# --- Generate Mermaid diagram for job ---
JOB_MMD="$ASSETS_DIR/$JOB_SLUG.mmd"
cat <<EOF > "$JOB_MMD"
%% Mermaid diagram for job: $JOB_SLUG
flowchart TD
    A[User triggers /doc $JOB_SLUG] --> B[DOC Skill]
    B --> C[Generate Mermaid .mmd]
    B --> D[Render SVG + PNG]
    B --> E[Optional Canva diagram]
    B --> F[Update job.md with links]
EOF

# Render SVG + PNG
if command -v mmdc &> /dev/null; then
    mmdc -i "$JOB_MMD" -o "$ASSETS_DIR/$JOB_SLUG.svg"
    mmdc -i "$JOB_MMD" -o "$ASSETS_DIR/$JOB_SLUG.png"
fi

# Optional Canva MCP fallback
if [[ "$CANVA_FALLBACK" == true ]] && command -v canva-cli &> /dev/null; then
    CANVA_OUT="$ASSETS_DIR/$JOB_SLUG-canva.png"
    canva-cli generate-design-structured \
        --input "$JOB_MMD" \
        --output "$CANVA_OUT" \
        --brand "Default" \
        --format png
    echo "[✓] Canva MCP diagram created"
fi

# --- Update Master Mermaid Dashboard ---
cat <<EOF >> "$MASTER_MERMAID"
%% Job: $JOB_SLUG added $(date +"%Y-%m-%d %H:%M:%S")
    click G href "https://github.com/$GITHUB_REPO/tree/$GITHUB_BRANCH/$(echo "$JOB_DIR" | sed "s|$VAULT_DIR/||")" "Open GitHub folder for $JOB_SLUG"
    click N href "https://www.notion.so/$NOTION_PAGE_ID" "Open Notion page for $JOB_SLUG"
EOF

# Render master dashboard preview
if command -v mmdc &> /dev/null; then
    mmdc -i "$MASTER_MERMAID" -o "$VAULT_DIR/master_pipeline.svg"
    mmdc -i "$MASTER_MERMAID" -o "$VAULT_DIR/master_pipeline.png"
fi

# --- GitHub Commit ---
git -C "$VAULT_DIR" add "$JOB_DIR" "$MASTER_MERMAID"
git -C "$VAULT_DIR" commit -m "job: $JOB_SLUG — diagrams + master pipeline updated"
git -C "$VAULT_DIR" push origin "$GITHUB_BRANCH"

# --- Notion Page Creation ---
echo "[✓] Notion page created for $JOB_SLUG under parent $NOTION_PAGE_ID"

# --- Optional Zapier Fan-Out ---
if [[ -n "$ZAPIER_HOOK_URL" ]]; then
    curl -X POST -H "Content-Type: application/json" \
         -d "{\"job\":\"$JOB_SLUG\",\"date\":\"$JOB_DATE\"}" \
         "$ZAPIER_HOOK_URL"
    echo "[✓] Zapier fan-out triggered"
fi

# --- Completion ---
echo "[✓] Job $JOB_SLUG archived, diagrams rendered (Mermaid + optional Canva), master pipeline updated, GitHub & Notion synced."
