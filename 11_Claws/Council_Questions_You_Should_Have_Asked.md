# Council Questions You Should Have Asked

*For the "Council of Seven Master Spirits" multi-agent n8n workflow*
*PhD in Triune Monism — Operational Reference*

---

## Section 1: Questions about Model Management

**What happens when a model is deprecated?**

When a provider deprecates a model (e.g., OpenAI retires `gpt-4-0314`), API calls begin returning `404` or a redirect to the successor model. The `update_council_models.py` script catches these as `API_ERROR` status and flags the seat for attention. The registry's `alternatives` list for each seat provides a ranked fallback chain — the updater will try each alternative in order until one is live. In the n8n workflow, the HTTP Request node for that seat will silently fail until you manually patch it or re-run the updater. Best practice: run the updater weekly so deprecations are caught before they break a Council session.

**Should we pin versions or use "latest"?**

Pin specific versions in the registry (e.g., `claude-sonnet-4-6` not `claude-sonnet-latest`). Reasons: (1) reproducibility — a Council run in June should produce structurally comparable output to one in October; (2) cost predictability — "latest" aliases can silently shift to more expensive models; (3) PhD integrity — your dissertation relies on documented, citable model versions. Use the `next_model` field in the registry to track announced successors and migrate deliberately. The `update_council_models.py` script proposes upgrades but does not apply them without your confirmation (or `--dry-run` to preview).

**How do we benchmark seat performance?**

Three levels: (1) *Response quality* — create a fixed benchmark question set (10–20 questions from your PhD corpus) and run the full Council. Score each seat's response on a 1–5 rubric for relevance, depth, and theological precision. Archive results in `council/benchmarks/`. (2) *Latency* — `council_status.py` reports ping latency per seat; run it before each session to identify slow seats. (3) *Cost efficiency* — divide response quality score by cost per run to find the cost-quality sweet spot. Ollama seats (4 & 5) are free but slower and less capable; factor this into weighting Gabriel's synthesis.

---

## Section 2: Questions about Cost

**What is the estimated cost per Council run?**

Approximately **$0.04 USD per full Council run** under typical conditions (500 input + 300 output tokens per seat; ~3,000 input + 800 output for Gabriel). Breakdown:

| Seat | Model | Cost/run |
|------|-------|----------|
| 1 Father | gpt-4.1 | $0.0034 |
| 2 Son | claude-sonnet-4-6 | $0.0060 |
| 3 Spirit | gemini-2.5-pro | $0.0036 |
| 4 Father-Son | gemma4:e4b (local) | $0.0000 |
| 5 Father-Spirit | deepseek-r1:7b (local) | $0.0000 |
| 6 Son-Spirit | glm-4 | ~$0.0001 |
| 7 Trinity | grok-3 | $0.0060 |
| Gabriel | claude-sonnet-4-6 | $0.0210 |
| **Total** | | **~$0.040** |

For a PhD dissertation chapter requiring 50 Council runs, budget ~$2 USD. At 500 runs (a full research year), ~$20 USD — essentially negligible. Gabriel dominates cost because it receives all 7 seat outputs as context (large input).

**Which seats are free (local) vs paid?**

- **Free (Ollama local, URANTiOS 204.168.143.98):** Seat 4 (Father-Son / gemma4:e4b), Seat 5 (Father-Spirit / deepseek-r1:7b)
- **Effectively free (free tier):** Seat 6 (Son-Spirit / GLM-4-flash has a free tier; main key currently depleted)
- **Paid API:** Seats 1, 2, 3, 7, and Gabriel

The two local seats represent the "sovereign" voices in the Council — they answer without external API dependency and without cost. However, their reasoning depth is lower than the cloud seats. Do not rely on them exclusively for theological precision.

**At what query volume does the cost become significant?**

At $0.04/run: 250 runs = $10, 2,500 runs = $100, 25,000 runs = $1,000. For a single PhD researcher, even 10,000 Council runs over three years costs roughly $400 — less than one academic conference. Cost becomes significant only at automated/batch-processing scale (e.g., running the Council over an entire corpus of 10,000 texts). At that scale, switch Seat 2 and Gabriel to `claude-haiku` variants and Seat 1 to `gpt-4o-mini` to reduce cost by ~70%.

---

## Section 3: Questions about Reliability

**What is the fallback chain per seat?**

Each seat in `COUNCIL_MODEL_REGISTRY.json` has an `alternatives` array ranked by preference. Logical fallback chains:

- **Seat 1 (Father / OpenAI):** gpt-4.1 → gpt-4o → gpt-4o-mini
- **Seat 2 (Son / Anthropic):** claude-sonnet-4-6 → claude-opus-4-6 → claude-haiku-4-5
- **Seat 3 (Spirit / Google):** gemini-2.5-pro → gemini-2.0-flash → gemini-1.5-pro
- **Seat 4 (Father-Son / Ollama):** gemma4:e4b → gemma3:27b → gemma3:12b → llama3.2:3b
- **Seat 5 (Father-Spirit / Ollama):** deepseek-r1:7b → deepseek-chat (API) → deepseek-r1:14b → qwen3:8b
- **Seat 6 (Son-Spirit / Z.ai):** glm-4 → glm-4-flash → glm-4-air *(key currently depleted — use glm-4-flash free tier)*
- **Seat 7 (Trinity / xAI):** grok-3 → grok-3-mini → grok-2
- **Gabriel:** claude-sonnet-4-6 → claude-opus-4-6 → claude-haiku-4-5

The n8n workflow does not implement automatic runtime fallback — if a seat fails, it returns an error node output. Gabriel's prompt should be written to tolerate missing seat responses gracefully: *"If any seat did not respond, note the absence and synthesize from the remaining voices."*

**What happens if the Ollama server goes down?**

Seats 4 and 5 will time out (default 30s in the n8n HTTP Request node). The Council run will either stall or return error JSON from those seats. Options: (1) Set a short timeout (10s) so failures are fast and Gabriel can proceed without those voices. (2) Wire a fallback HTTP Request node for Seat 5 pointing to the DeepSeek API (`api.deepseek.com`) — the registry has `fallback_provider: deepseek` and `fallback_key_env_var: DEEPSEEK_API_KEY` defined for exactly this purpose. (3) Run `council_status.py` before each session to pre-check Ollama reachability. The URANTiOS server at 204.168.143.98 requires network connectivity from the n8n host (46.225.51.30); if the iMac is asleep or off-network, both seats will be unavailable.

**How do we handle partial Council responses?**

Design Gabriel's synthesizer prompt to be explicit: *"You have received responses from the following seats: {list}. If any seats are missing, acknowledge the absence and note which perspective is unrepresented."* In the n8n workflow, pipe all 7 seat outputs through a Merge node before feeding Gabriel — if a seat node returns an error, the Merge node should pass the error string (not null) so Gabriel knows the voice was attempted. Log partial runs in `council/session_log.jsonl` with a `seats_responded` field. For PhD purposes, partial responses are still valid data — the *absence* of a seat's voice is itself a theological datum (which hypostases are silent?).

---

## Section 4: Questions about Quality

**How do we evaluate synthesis quality from Gabriel?**

Three-stage evaluation: (1) *Completeness* — did Gabriel explicitly engage with all responding seats? Score 1 point per seat mentioned substantively (max 7). (2) *Theological coherence* — does the synthesis maintain internal consistency with Triune Monism principles? Score 1–5 manually or with a second Claude call acting as reviewer. (3) *Novel emergence* — did the synthesis produce an insight not present in any individual seat response? This is the key quality indicator for multi-agent value. Tag sessions with `emergence: true/false` in session logs. Over time, track which question types reliably produce emergent insights vs. mere aggregation.

**Should we score each seat's response before synthesis?**

Yes, and this can be done automatically. Add an intermediate n8n node (a "Scorer" HTTP Request to Claude or GPT-4o-mini) that rates each seat's response on three dimensions: relevance (0–2), depth (0–2), theological grounding (0–1). Pass these scores to Gabriel in the synthesis prompt: *"Seat 1 scored 4/5, Seat 3 scored 2/5 — weight your synthesis accordingly."* This prevents a verbose-but-shallow seat from dominating Gabriel's output. Scoring costs ~$0.001 extra per run (small model, 1-sentence output). Store scores in `council/scores/` for longitudinal analysis.

**How do we detect hallucinations?**

Hallucinations in theological multi-agent contexts take three forms: (1) *Factual hallucination* — a seat cites a non-existent Urantia Paper passage or misquotes scripture. Mitigate by providing verified excerpts in the system prompt rather than relying on model memory. (2) *Attribution hallucination* — Gabriel attributes a claim to the wrong seat, or invents a seat's position. Mitigate by having Gabriel quote directly from seat outputs. (3) *Synthesis hallucination* — Gabriel fabricates a "consensus" that no seat actually expressed. Mitigate by requiring Gabriel to cite which seat(s) support each claim in the synthesis. For formal PhD use, cross-reference any Urantia Book quotations against the official concordance before citing in your dissertation.

---

## Section 5: Operational Questions

**How often should we update models?**

Run `update_council_models.py` **monthly** as a baseline. Additionally trigger it: (a) when you receive a provider announcement email about new model availability; (b) when a seat starts returning degraded or off-pattern responses (a symptom of silent model changes on the provider's end); (c) before any major dissertation chapter session where reproducibility matters. Do not update models mid-dissertation-phase without archiving the current registry state first — use `git tag` to mark stable model configurations (e.g., `council-config-v1.0-chapter3`).

**Should the workflow run on a schedule or on-demand only?**

**On-demand only**, at least during the PhD research phase. Reasons: (1) Each run costs ~$0.04 and produces output that requires your interpretive attention — automated runs without review produce noise, not signal. (2) Scheduled runs without a meaningful question waste tokens and API quota. (3) The theological quality of the question determines the quality of the Council's output; rushed or formulaic questions yield formulaic synthesis. Reserve scheduled runs for specific use cases: daily "philosophical reflection prompt" (low-cost with haiku models), or automated literature scanning (pass new papers through the Council for relevance scoring).

**How do we archive Council outputs for the PhD?**

Implement a three-tier archive: (1) *Raw run logs* — JSON files in `council/sessions/YYYY-MM-DD_HH-MM_<question-slug>.json` containing: timestamp, question, each seat's full response, Gabriel's synthesis, model versions used, costs. The `COUNCIL_MODEL_REGISTRY.json` version at run time should be embedded. (2) *Curated extracts* — for sessions producing PhD-relevant insights, create a markdown file in the relevant PhD chapter folder (e.g., `06_Draft_Papers/chapter3_council_extracts.md`) with annotated quotes. (3) *Citation-ready records* — for any Council output you cite in the dissertation, record: date of run, model versions for all seats and Gabriel, exact question posed, and the specific text quoted. Format: *"Council of Seven, Session 2026-04-12, Gabriel synthesis, models: [list]. Question: '...' Response: '...'"* This satisfies academic citation standards for AI-assisted research.

---

*Last updated: 2026-04-12*
*See also: `setup/update_council_models.py`, `setup/council_status.py`, `council/COUNCIL_MODEL_REGISTRY.json`*
