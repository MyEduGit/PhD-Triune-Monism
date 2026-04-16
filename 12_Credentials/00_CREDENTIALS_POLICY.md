# Credentials Policy — Mircea's Constellation

> **Governed by UrantiOS v1.0 — Truth · Beauty · Goodness**
> **Updated:** 2026-04-12

---

## The Rule

**Every API key, password, token, and secret MUST be recorded in Obsidian.**

If it is not in Obsidian, it does not officially exist. If you cannot find a key, check here first.

---

## File Structure

| File | What It Contains | In GitHub? |
|------|-----------------|------------|
| `SECRETS.template.md` | Structure only — no real values | ✅ Yes |
| `SECRETS.md` | **Actual keys** — local Obsidian only | ❌ No (gitignored) |
| `Services_Index.md` | All services, what they're for, status | ✅ Yes |
| `00_CREDENTIALS_POLICY.md` | This file — the rules | ✅ Yes |

---

## How to Use

### First time setup on a new machine:
```bash
# 1. Clone the repo
git clone <repo-url>

# 2. Copy the template to create your local secrets file
cp 12_Credentials/SECRETS.template.md 12_Credentials/SECRETS.md

# 3. Fill in all the actual values in SECRETS.md
# SECRETS.md is gitignored — it will NEVER be pushed to GitHub
```

### Adding a new credential:
1. Add it to `SECRETS.md` (local, actual value)
2. Add the key NAME (not value) to `SECRETS.template.md`
3. Add the service to `Services_Index.md`
4. Commit and push `SECRETS.template.md` and `Services_Index.md`

### Never:
- Never paste an actual API key into any `.md` file that is NOT `SECRETS.md`
- Never share API keys in chat
- Never commit `SECRETS.md` to GitHub

---

## Why This System

- **Local Obsidian**: You can see and search all keys from any device via Obsidian Sync
- **GitHub**: Only structure is committed — safe for collaboration and backup
- **gitignore**: Enforces the boundary automatically — git will refuse to track `SECRETS.md`

---

## Related

- [[SECRETS.template]] — Copy this to create your local SECRETS.md
- [[Services_Index]] — All known services
- [[11_Claws/00_CLAWS_MASTER]] — Infrastructure overview
