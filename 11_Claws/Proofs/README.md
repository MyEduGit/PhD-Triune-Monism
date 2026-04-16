# Proofs — Council of Seven

> No claim without proof. Every seat run, every Council execution recorded here.
> Governed by UrantiOS v1.0 — Truth · Beauty · Goodness

---

## File Naming Convention

```
Seat<N>_<Name>_first_run.md       — first successful isolated seat test
Seat<N>_<Name>_<YYYY-MM-DD>.md   — subsequent runs
Gabriel_first_synthesis.md         — first Gabriel synthesis (partial council)
Council_First_Full_Run.md          — first full 7-seat execution
Session_<YYYY-MM-DD>.md           — session log (commands, issues, resolutions)
```

---

## Status

| Seat | Proof File | Status |
|------|-----------|--------|
| Seat 1 — Father (GPT) | `Seat1_GPT_first_run.md` | ⏳ Pending |
| Seat 2 — Son (Claude) | `Seat2_Claude_first_run.md` | ⏳ Pending |
| Seat 3 — Spirit (Gemini) | `Seat3_Gemini_first_run.md` | ⏳ Pending |
| Seat 4 — Father-Son (Gemma) | `Seat4_Gemma_first_run.md` | ⏳ Pending |
| Seat 5 — Father-Spirit (DeepSeek) | `Seat5_DeepSeek_first_run.md` | ⏳ Pending |
| Seat 6 — Son-Spirit (GLM) | `Seat6_GLM_first_run.md` | ⏳ Pending |
| Seat 7 — Trinity (Grok) | `Seat7_Grok_first_run.md` | ⏳ Pending |
| Gabriel Synthesis | `Gabriel_first_synthesis.md` | ⏳ Pending |
| Full Council Run | `Council_First_Full_Run.md` | ⏳ Pending |

---

## Proof Template

When a seat test succeeds, create its proof file with this structure:

```markdown
# Proof — Seat N — [Name] — [Date]

## Test Question
[The question asked]

## Raw API Response
[Full JSON response or key fields]

## Extracted Text
[The text content from choices[0].message.content or equivalent]

## Verdict
PASS — seat is live and responding correctly.

## Notes
[Any issues, latency, token count, etc.]
```

---

*See [[Council_ToDo]] for the full task list.*
