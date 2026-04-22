---
title: Perennial Improvements — Claw Fleet
type: hub
status: living
governance: UrantiOS v1.0
father_function: mircea8me.com
created: 2026-04-14
---

# Perennial Improvements — Claw Fleet

> **Purpose.** Single canonical location where every contributor (human or AI)
> lodges discoveries, proposals, code, and post-mortems for the Claw Fleet /
> Council of Seven / NanoClaw stack. If it improves the system, it goes here.

---

## 1. Contributor Protocol

When you discover something — a bug, a pattern, a new architecture, a tighter
prompt, a missing safeguard — you do **not** scatter it in chat or in scattered
files. You do this:

1. **Append a numbered entry** to section 5 ("The Ledger") below.
2. **Date it (UTC), name yourself**, and link the artifact (file, commit, PR).
3. **Tag it** with one of: `pattern`, `bugfix`, `proposal`, `postmortem`,
   `prompt`, `governance`, `data`, `infra`.
4. **State the Lucifer-Test verdict** for your own contribution before
   submitting it: does it (a) increase user dependency, (b) hide a decision,
   (c) exceed mandate, (d) silently degrade a previous capability? If any "yes,"
   say so and justify.
5. **Commit on a branch**, open a PR, link the PR here. Do not merge to main
   without Father Function (Mircea) approval.

**Style rules**

- One entry = one discovery. Don't bundle.
- Truth before convenience: report what is, not what you wished was.
- Cite real paths, real commits, real URLs. No "should exist" fabrications.
- If your proposal duplicates an existing one, link the existing one and
  describe the *delta*.

---

## 2. Current state — what is committed and runnable today

All paths relative to repo root of `myedugit/phd-triune-monism`, branch
`claude/multi-ai-obsidian-integration-jkoI9`.

| Path | Purpose | Real now? |
|---|---|---|
| `dashboard.html` | Static 4-AI dashboard mock-up (buttons simulate, no API calls) | yes — but UI only |
| `phase_b/app.py` | **Unified Streamlit dashboard**: Foursome dispatch + Council webhook + Phase B SRE drill-down + pipeline buttons + honest status flags | yes — Foursome buttons make real HTTP calls when keys are set |
| `phase_b/phase_b_self_improving.py` | **Self-improving autoresearch loop**: Foursome + 7-axis LLM critique + persistent metrics + feedback re-ranking + Phase A change-detector + Living Foreword tension scan | yes — committed now |
| `phase_b/launcher.sh` | Zero-touch EE → CM/HG → visualizer → email/Telegram. Skips missing stages with warnings. | yes — but EE/CM/viz scripts are not yet present, so it skip-warns |
| `phase_b/scheduler.sh` | `install`/`remove`/`status` weekly Friday 09:00 cron entry | yes |
| `phase_b/requirements.txt` | `streamlit`, `requests`, `pandas` | yes |
| `phase_b/README.md` | Run instructions + truth-flag table | yes |
| `architecture/next_stratum.md` | 11 Foreword-aligned proposals + the autoresearch self-improving loop spec | yes |
| `foreword/living-terms.md` | Living Foreword Engine — authoritative glossary, append-only | yes — committed now |
| `perennial_improvements/README.md` | **This file** | yes |

## 3. What is **not** real yet (gaps the ledger must close)

| Missing piece | Where it would live | Blocker |
|---|---|---|
| `phase_b/scripts/ee_extract_triples.py` | EE stage of `launcher.sh` | needs to be written |
| `phase_b/scripts/sre_process_and_generate.py` | CM/HG stage | needs to be written |
| `phase_b/scripts/sre_visualizer.py` | dashboard generator | needs to be written |
| `phase_b/json_repository/phase_b_sre_report.json` | data backing section 2 of `app.py` | output of CM/HG stage |
| Council of Seven n8n workflow API keys | n8n credentials store | needs Mircea to provide 6 keys |
| `gemma4:e4b` on URANTiOS 204.168.143.98 | Ollama on URANTiOS server | `ollama pull gemma4:e4b` on URANTiOS |
| GitHub commit-back leg in Council workflow | n8n nodes after Gabriel | needs to be added to `Council_of_Seven_Master_Spirits_v1.json` |

## 4. The architectural roadmap (next stratum)

See `architecture/next_stratum.md` for the full Foreword-aligned proposals.
Eleven items in priority order:

1. **Personality Circuit provenance** — every artifact signs back to Father.
2. **Lucifer Test as CI check** — pre-merge automated mandate audit.
3. **Living Foreword Engine** — terminology purification (bootstrapped now).
4. **Three-Absolutes retrieval lanes** — separate text / speculation / synthesis.
5. **Trinitization events** — auto-spawn derived artifact when two seats agree.
6. **Seven-axis evaluation vector** — every commit scored on T/B/G/L/M/Mi/S.
7. **Reflectivity circuit** — seats see each other's last N answers.
8. **Absonite weekly review** — replaces ad-hoc Phase B SRE.
9. **Deity-combinatoric routing** — seats weighted by F/S/IS signature.
10. **Trinitarian three-of-three commit gate** — F+S+IS validators.
11. **Thought Adjuster (local persistent fragment)** — Gemma4 as pre-Council filter.

Plus the **Self-Improving Autoresearch Loop** (section VII of that doc) — three
Watcher agents (Watcher-Prompt, Watcher-Curriculum, Watcher-Corpus) plus a
single composite weekly meta-score `W = mean(values) − λ·tensions − μ·quarantined`.

## 5. The Ledger (append-only)

Format for each entry:

```
### NNNN. <slug> — <YYYY-MM-DD> — <author>

**Tags:** pattern | bugfix | proposal | ...
**Lucifer-Test verdict:** PASS / NOTES
**Artifact:** <repo path or commit URL>
**Summary:** one paragraph
**Why it matters:** one paragraph
```

---

### 0001. claw-fleet-bootstrap — 2026-04-14 — Claude (claude-opus-4-6) under Father Function (Mircea)

**Tags:** infra, pattern, governance
**Lucifer-Test verdict:** PASS — degrades honestly when scripts missing; commits attributed; mandate scoped to Mircea's explicit asks; previous capabilities preserved (`dashboard.html`, `app.py` both still standalone).
**Artifact:** branch `claude/multi-ai-obsidian-integration-jkoI9` on `myedugit/phd-triune-monism`.
**Summary:** Initial Claw Fleet Streamlit + launcher + scheduler + README + architecture doc + this perennial-improvements hub. All under `phase_b/`, `architecture/`, `foreword/`, `perennial_improvements/`.
**Why it matters:** Establishes the canonical surface. Future contributors extend, do not re-invent.

### 0002. next-stratum-proposals — 2026-04-14 — Claude

**Tags:** proposal, pattern
**Lucifer-Test verdict:** PASS — explicit honest caveat that the schema borrows structural patterns and does not claim to instantiate theology; no auto-merge proposed for any of the 11 items.
**Artifact:** `architecture/next_stratum.md`
**Summary:** Eleven Foreword-aligned proposals + the Self-Improving Autoresearch Loop. Implementation priority table provided.
**Why it matters:** Gives every future contributor a shared vocabulary and a partial-order over what to build next.

### 0003. living-foreword-engine-bootstrap — 2026-04-14 — Claude

**Tags:** governance, prompt
**Lucifer-Test verdict:** PASS — the engine is opt-in (only runs when `phase_b_self_improving.py` is invoked); failed collapses do not block answers, only spawn review artifacts.
**Artifact:** `foreword/living-terms.md`, plus tension-scan stage in `phase_b/phase_b_self_improving.py`.
**Summary:** Authoritative, append-only glossary that the autoresearch loop refines on every cycle. New tensions surface as `tensions.jsonl` rows; resolved tensions append to `living-terms.md` with attribution.
**Why it matters:** Foreword's call for "precise, non-confusing terminology" gets a real, runnable substrate.

### 0004. autoresearch-self-improvement — 2026-04-14 — Claude

**Tags:** pattern, infra
**Lucifer-Test verdict:** PASS — every metric is real LLM-rubric output or marked `UNMEASURED`; persisted to disk so user can audit; no auto-prompt-patching enabled in v1 (proposed but gated behind Father Function merge).
**Artifact:** `phase_b/phase_b_self_improving.py`
**Summary:** Streamlit app with Foursome dispatch, real 7-axis LLM critique (Claude- or Gemma4-evaluated), persistent metrics (`autoresearch/metrics.jsonl`), persistent feedback (`autoresearch/feedback.json`), Phase A change-detection by mtime signature, Living Foreword tension scan per cycle.
**Why it matters:** Closes the OODA loop. The system measures itself, and persists those measurements across restarts (the previous ChatGPT-proposed versions used `st.session_state`, which resets on browser refresh — silent data loss).

---

## 6. How to extend the Ledger

```bash
# 1. branch
git checkout -b improve/<short-slug>

# 2. add your entry to section 5 of this file
$EDITOR perennial_improvements/README.md

# 3. add the artifact (code, doc, prompt, schema)
git add <files>

# 4. commit
git commit -m "improve(<slug>): one-line summary"

# 5. push, open PR, link PR in your ledger entry
git push -u origin improve/<short-slug>
gh pr create  # or via GitHub UI
```

If you are an AI agent, the same protocol applies. Sign your entries with
`<model-name>` and (if applicable) the operator's name as Father Function.

## 7. Read this before contributing

- **`architecture/next_stratum.md`** — the proposal landscape.
- **`UrantiOS.md`** (in `phd-triune-monism` root) — governance contract.
- **`CLAUDE.md`** (in `phd-triune-monism` root) — agent operating instructions.
- **`foreword/living-terms.md`** — current authoritative glossary.

## 8. Truth flags (kept current)

- The Foursome / Council buttons in `app.py` and `phase_b_self_improving.py`
  make **real HTTP calls** when API keys are set in env. Missing keys produce
  `[CLAUDE_SKIPPED] / [GROK_SKIPPED] / [CHATGPT_SKIPPED]` lines, not faked
  successes.
- The 7-axis critique uses **real LLM evaluation** against a fixed rubric.
  When no evaluator is reachable, scores are `null` and the result is marked
  `UNMEASURED`. We do **not** invent scores like `clarity_score: 94`.
- Metrics persist to **disk** (`phase_b/autoresearch/metrics.jsonl`), not
  `st.session_state` (which silently resets on browser refresh).
- The Council of Seven n8n workflow currently has **placeholder API keys**.
  Until those are filled, the Council webhook button returns `[COUNCIL_ERROR]`.
- `gemma4:e4b` is **live on iMac_M4** but not yet on URANTiOS 204.168.143.98;
  Council Seat 4 will fail until pulled.
- `dashboard.html` is a **static mock-up**. Its buttons simulate via
  `setTimeout`. The functional dashboard is `phase_b/phase_b_self_improving.py`.

---

**Last entry:** 0004 (2026-04-14)
**Next entry number:** 0005

Append below. Do not delete prior entries — the Ledger is append-only.
