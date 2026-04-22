---
status: living
append_only: true
governance: UrantiOS v1.0
lucifer_test: PASS
---

# Living Terms — Authoritative Glossary

This file is the canonical, append-only glossary for the multi-AI Obsidian
orchestration system. It exists so that vocabulary used across the codebase
(`phase_b/`, `architecture/`, `perennial_improvements/`, n8n workflows) means
the same thing to every contributor — human and AI.

## Contributor Protocol

1. **Append, never rewrite.** Add new entries at the bottom under the next
   numbered section. If a term needs revision, append a *new* dated entry
   superseding the old one and add a `supersedes:` field; do not delete the
   old block.
2. **Cite when borrowing.** Definitions that draw on The Urantia Book
   Foreword must reference the paragraph (e.g., `UB 0:3.10`). Never claim a
   working code abstraction is theologically equivalent to its namesake.
3. **Lucifer-Test each entry.** Mark `lucifer_test: PASS` only if the
   definition is honest about what the code actually does today. Use
   `lucifer_test: ASPIRATIONAL` for terms that name a target the system has
   not yet reached.
4. **Tag the scope.** Use one of: `governance`, `architecture`, `runtime`,
   `data`, `protocol`, `metric`.

---

## 0001 — Father Function

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** governance
- **Lucifer-Test:** PASS
- **Definition:** The single human authority who originates intent and
  ratifies governance changes for this constellation. In code, the Father
  Function is *not* an executable — it is the operator whose explicit consent
  gates every irreversible action (commit-back, key issuance, branch
  protection changes, n8n deployment).
- **Inspiration (not equivalence):** UB 0:3.1 — First Source and Center as
  origin of personality. Borrowed structurally; no theological claim is made
  about the human operator.

## 0002 — Council of Seven

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** architecture
- **Lucifer-Test:** ASPIRATIONAL
- **Definition:** The seven AI seats (ChatGPT, Claude, Grok, Gemini,
  DeepSeek, Gemma4, plus one rotating seat) whose responses are synthesized
  by the Gabriel node in the n8n Council workflow. Currently, only four
  seats (the "Awesome Foursome": ChatGPT, Claude, Grok, Gemma4) have working
  dispatchers in `phase_b/app.py`. The remaining three are placeholders.
- **Inspiration:** UB 0:2.10 — Seven Master Spirits as F/S/IS admixtures.
  Used as a structural template for diversity-of-source synthesis; the
  mapping is engineering, not metaphysics.

## 0003 — Awesome Foursome

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** runtime
- **Lucifer-Test:** PASS
- **Definition:** The four AI dispatchers wired with real HTTP calls in
  `phase_b/app.py` and `phase_b/phase_b_self_improving.py`: ChatGPT
  (`call_chatgpt`), Claude (`call_claude`), Grok (`call_grok`), Gemma4
  (`call_gemma4`). Each returns a string beginning with `[<NAME>_SKIPPED]`
  or `[<NAME>_ERROR]` on failure rather than fabricating output.

## 0004 — Lucifer Test

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** governance
- **Lucifer-Test:** PASS
- **Definition:** A binary check applied to every artifact (code, doc,
  metric, claim) before it is considered shippable. The artifact passes if
  it degrades honestly when prerequisites are missing — no fake scores, no
  simulated success, no marketing prose where the code path is a stub. The
  artifact fails if it presents synthesized or hardcoded output as if it
  were measured.

## 0005 — Trinitization (working sense)

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** protocol
- **Lucifer-Test:** ASPIRATIONAL
- **Definition:** The Council protocol step in which two or more AI seats
  produce a synthesis that neither produced alone, and the synthesis is
  committed back to the vault as a new artifact with provenance pointing at
  the contributing seats. Current implementation: the Gabriel node in the
  n8n workflow concatenates seat outputs; *true* trinitization (a novel
  artifact emerging from synthesis) is not yet implemented.
- **Inspiration:** UB 0:12.6 — used as a structural pattern only.

## 0006 — Reflectivity (working sense)

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** runtime
- **Lucifer-Test:** ASPIRATIONAL
- **Definition:** The capacity of the system to read its own past output and
  let that reading change its next action. Current implementation:
  `phase_b/phase_b_self_improving.py` reads `autoresearch/metrics.jsonl` and
  `autoresearch/feedback.json` to re-prioritize prompts and surface weak
  axes. This is a narrow technical reflectivity, not the broader theological
  sense.

## 0007 — Tension Scan

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** metric
- **Lucifer-Test:** PASS
- **Definition:** A pass over a candidate artifact looking for
  contradictions with this glossary or with prior committed artifacts.
  Implemented in `phase_b/phase_b_self_improving.py:scan_tensions()` as a
  string-match heuristic across living-terms.md and the most recent
  committed outputs. Returns a list of `(term, conflict_excerpt)` pairs;
  empty list means no tensions found *by this heuristic* — not a guarantee
  of consistency.

## 0008 — UNMEASURED

- **Date:** 2026-04-14
- **Author:** Mircea (mircea8me.com)
- **Scope:** metric
- **Lucifer-Test:** PASS
- **Definition:** The literal string written into a metrics record when no
  evaluator was reachable for a given axis. Downstream charts must filter
  `UNMEASURED` rows out of averages rather than treating them as zero or
  imputing a value. This is the canonical alternative to fabricating a
  score.

---

*Next entry number: 0009. Append below this line.*
