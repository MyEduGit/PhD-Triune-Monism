# ChatGPT Imports

This folder stores files imported from ChatGPT's vault on Hetzner.

## Source Location
```
mircea@46.225.51.30:~/.openclaw/workspace/research/theory-of-everything-phd/
```

## Sync Command (run on iMac)
```bash
rsync -avz mircea@46.225.51.30:~/.openclaw/workspace/research/theory-of-everything-phd/ \
  "/Users/mircea8me.com/OpenClaw code for Hetzy_PhD_bot to Telegram/08_ChatGPT_Imports/"
```

## Known Files on Hetzner
- `09_Verification/RESEARCH-SCHEDULE-MASTER.md` — Master research schedule (locked)
- `10_Ontology/01-THE-I-AM.md` — ChatGPT's version of Step 1.1

## How We Use Two AIs

| Task | Claude (iMac) | ChatGPT (Hetzner) |
|---|---|---|
| Deep philosophical analysis | PRIMARY | Secondary |
| File creation (local) | iMac vault | Hetzner vault |
| Obsidian linking | PRIMARY | N/A |
| Summary cards | Secondary | PRIMARY |
| Execution tracking | Diary + Daily Log | Verification folder |
| Comparison tables | PRIMARY | N/A |

## Merging Strategy
When both AIs produce the same file:
1. Claude's version → `10_Ontology/` (the research file, detailed)
2. ChatGPT's version → `08_ChatGPT_Imports/` (reference, may be merged)
3. If ChatGPT's version has insights Claude missed → merge into Claude's file

---

*Created: 2026-03-11*
