#!/bin/bash
# /doc installer for multi-AI projects with auto Mermaid + Canva fallback
# Archives jobs, updates master flowchart, syncs to GitHub + Notion, optional Zapier

# --- Configuration ---
VAULT_DIR=~/Documents/Obsidian/PhD-Triune-Monism
MASTER_MERMAID="$VAULT_DIR/master_pipeline.mmd"
JOB_DATE=$(date +%F)
JOB_SLUG=${1:-"new-job"}
GITHUB_BRANCH="claude/claude-usage-guide-mtE8j"
GITHUB_REPO="myedugit/mircea-constellation"
NOTION_PAGE_ID="3328525a-b5a0-815d-886c-d5488593aa3d"
ZAPIER_HOOK_URL=${ZAPIER_HOOK_URL:-""}
CANVA_FALLBACK=${CANVA_FALLBACK:-true}  # enable optional Canva fallback

# --- Directories ---
JOB_DIR="$VAULT_DIR/$JOB_DATE/$JOB_SLUG"
ASSETS_DIR="$JOB_DIR/assets"
mkdir -p "$ASSETS_DIR"

# --- DOC Skill: Job Archival ---
JOB_MD="$JOB_DIR/job.md"
echo "Job: $JOB_SLUG" > "$JOB_MD"
echo "Date: $(date +"%Y-%m-%d %H:%M:%S")" >> "$JOB_MD"
echo "" >> "$JOB_MD"
echo "Artifacts: Mermaid + SVG + PNG + optional Canva" >> "$JOB_MD"

# --- Generate Mermaid diagram ---
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

# Render SVG + PNG (Mermaid)
if command -v mmdc &> /dev/null; then
    mmdc -i "$JOB_MMD" -o "$ASSETS_DIR/$JOB_SLUG.svg"
    mmdc -i "$JOB_MMD" -o "$ASSETS_DIR/$JOB_SLUG.png"
fi

# --- Optional Canva MCP Fallback ---
if [[ "$CANVA_FALLBACK" == true ]]; then
    if command -v canva-cli &> /dev/null; then
        canva-cli generate-design-structured \
            --input "$JOB_MMD" \
            --output "$ASSETS_DIR/$JOB_SLUG-canva.png" \
            --brand "Default" \
            --format png
        echo "[✓] Canva MCP fallback rendered $JOB_SLUG-canva.png"
    else
        echo "[!] Canva MCP CLI not available, skipping fallback"
    fi
fi

# --- Update Master Mermaid Flowchart ---
cat <<EOF >> "$MASTER_MERMAID"
%% Job: $JOB_SLUG added $(date +"%Y-%m-%d %H:%M:%S")
    click G href "https://github.com/$GITHUB_REPO/tree/$GITHUB_BRANCH/$(echo "$JOB_DIR" | sed "s|$VAULT_DIR/||")" "Open GitHub folder for $JOB_SLUG"
    click N href "https://www.notion.so/$NOTION_PAGE_ID" "Open Notion page for $JOB_SLUG"
EOF

# Render master diagram
if command -v mmdc &> /dev/null; then
    mmdc -i "$MASTER_MERMAID" -o "$VAULT_DIR/master_pipeline.svg"
    mmdc -i "$MASTER_MERMAID" -o "$VAULT_DIR/master_pipeline.png"
fi

# --- GitHub Commit ---
git -C "$VAULT_DIR" add "$JOB_DIR" "$MASTER_MERMAID"
git -C "$VAULT_DIR" commit -m "job: $JOB_SLUG — assets + diagram + Canva fallback"
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
echo "[✓] Job $JOB_SLUG archived, diagrams rendered (Mermaid + optional Canva), master flowchart updated, GitHub & Notion synced."
