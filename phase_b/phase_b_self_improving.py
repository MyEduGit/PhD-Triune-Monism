"""phase_b_self_improving.py — autoresearch loop for the multi-AI Obsidian
constellation.

Run:
    streamlit run phase_b/phase_b_self_improving.py

Honest degradation: every dispatcher returns "[<NAME>_SKIPPED] ..." or
"[<NAME>_ERROR] ..." when its API key or endpoint is missing, and every
critique axis is recorded as the literal string "UNMEASURED" when no
evaluator is reachable. No fake scores, no simulated success. See
foreword/living-terms.md entries 0004 and 0008.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Paths — all derived from this file's location. No hardcoded user paths.
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
AUTORESEARCH_DIR = HERE / "autoresearch"
METRICS_PATH = AUTORESEARCH_DIR / "metrics.jsonl"
FEEDBACK_PATH = AUTORESEARCH_DIR / "feedback.json"
PHASE_A_GLOB_ROOT = REPO_ROOT / "phase_a" / "jobs"
LIVING_TERMS_PATH = REPO_ROOT / "foreword" / "living-terms.md"

AUTORESEARCH_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Endpoint configuration. Override via env vars; sensible defaults match the
# existing constellation (NemoClaw n8n, URANTiOS Ollama).
# ---------------------------------------------------------------------------
ENDPOINTS: dict[str, str] = {
    "openai_chat":   os.getenv("OPENAI_URL", "https://api.openai.com/v1/chat/completions"),
    "anthropic":     os.getenv("ANTHROPIC_URL", "https://api.anthropic.com/v1/messages"),
    "xai":           os.getenv("XAI_URL", "https://api.x.ai/v1/chat/completions"),
    "ollama":        os.getenv("OLLAMA_URL", "http://204.168.143.98:11434/api/generate"),
    "council_n8n":   os.getenv("COUNCIL_WEBHOOK", "http://46.225.51.30:5678/webhook/council"),
}
MODELS: dict[str, str] = {
    "openai_model":     os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "anthropic_model":  os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    "xai_model":        os.getenv("XAI_MODEL", "grok-2-latest"),
    "ollama_model":     os.getenv("OLLAMA_MODEL", "gemma4:e4b"),
    # The evaluator is whichever model has a key; if multiple, prefer Claude.
}

AXES = ["truth", "beauty", "goodness", "love", "mercy", "ministry", "supremacy"]
RUBRIC_PROMPT = (
    "You are a strict evaluator. Score the OUTPUT against the TASK on each "
    "axis from 0.0 (absent) to 1.0 (fully realized). Return ONLY compact "
    "JSON with keys: " + ", ".join(AXES) + ". No prose, no markdown.\n\n"
    "TASK:\n{task}\n\nOUTPUT:\n{output}\n"
)

# ---------------------------------------------------------------------------
# Real HTTP dispatchers. Each returns a string. Failure modes are explicit.
# ---------------------------------------------------------------------------
def call_chatgpt(task: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "[CHATGPT_SKIPPED] OPENAI_API_KEY not set."
    try:
        r = requests.post(
            ENDPOINTS["openai_chat"],
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": MODELS["openai_model"],
                "messages": [{"role": "user", "content": task}],
                "temperature": 0.4,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as exc:  # noqa: BLE001
        return f"[CHATGPT_ERROR] {exc}"


def call_claude(task: str) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return "[CLAUDE_SKIPPED] ANTHROPIC_API_KEY not set."
    try:
        r = requests.post(
            ENDPOINTS["anthropic"],
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODELS["anthropic_model"],
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": task}],
            },
            timeout=120,
        )
        r.raise_for_status()
        return "".join(b.get("text", "") for b in r.json().get("content", []))
    except Exception as exc:  # noqa: BLE001
        return f"[CLAUDE_ERROR] {exc}"


def call_grok(task: str) -> str:
    key = os.getenv("XAI_API_KEY")
    if not key:
        return "[GROK_SKIPPED] XAI_API_KEY not set."
    try:
        r = requests.post(
            ENDPOINTS["xai"],
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": MODELS["xai_model"],
                "messages": [{"role": "user", "content": task}],
                "temperature": 0.4,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as exc:  # noqa: BLE001
        return f"[GROK_ERROR] {exc}"


def call_gemma4(task: str) -> str:
    """Call Ollama on URANTiOS. Returns honest skip if endpoint unreachable."""
    try:
        r = requests.post(
            ENDPOINTS["ollama"],
            json={"model": MODELS["ollama_model"], "prompt": task, "stream": False},
            timeout=180,
        )
        r.raise_for_status()
        return r.json().get("response", "[GEMMA4_ERROR] empty response payload")
    except requests.exceptions.ConnectionError as exc:
        return f"[GEMMA4_SKIPPED] Ollama unreachable at {ENDPOINTS['ollama']}: {exc}"
    except Exception as exc:  # noqa: BLE001
        return f"[GEMMA4_ERROR] {exc}"


def call_council(task: str) -> str:
    try:
        r = requests.post(
            ENDPOINTS["council_n8n"],
            json={"task": task, "source": "phase_b_self_improving"},
            timeout=300,
        )
        r.raise_for_status()
        try:
            return json.dumps(r.json(), indent=2)
        except ValueError:
            return r.text
    except Exception as exc:  # noqa: BLE001
        return f"[COUNCIL_ERROR] {exc}"


DISPATCHERS = {
    "ChatGPT": call_chatgpt,
    "Claude":  call_claude,
    "Grok":    call_grok,
    "Gemma4":  call_gemma4,
    "Council": call_council,
}

# ---------------------------------------------------------------------------
# 7-axis critique. Uses whichever evaluator key is present; prefers Claude.
# When no evaluator is reachable, every axis is the literal string
# "UNMEASURED" — see living-terms.md 0008.
# ---------------------------------------------------------------------------
def pick_evaluator() -> str | None:
    if os.getenv("ANTHROPIC_API_KEY"):
        return "Claude"
    if os.getenv("OPENAI_API_KEY"):
        return "ChatGPT"
    if os.getenv("XAI_API_KEY"):
        return "Grok"
    return None


def _parse_rubric_json(raw: str) -> dict[str, Any]:
    # Find the first {...} block; tolerate fenced markdown.
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON object in evaluator output: {raw[:120]}")
    obj = json.loads(match.group(0))
    out: dict[str, Any] = {}
    for axis in AXES:
        v = obj.get(axis, "UNMEASURED")
        if isinstance(v, (int, float)):
            out[axis] = float(v)
        else:
            out[axis] = "UNMEASURED"
    return out


def critique_7axis(task: str, output: str) -> dict[str, Any]:
    evaluator = pick_evaluator()
    if evaluator is None:
        return {axis: "UNMEASURED" for axis in AXES} | {"_evaluator": "none"}
    if output.startswith("[") and ("_SKIPPED]" in output or "_ERROR]" in output):
        # Don't burn evaluator tokens grading a skip/error string.
        return {axis: "UNMEASURED" for axis in AXES} | {"_evaluator": "skipped-input"}
    prompt = RUBRIC_PROMPT.format(task=task, output=output)
    raw = DISPATCHERS[evaluator](prompt)
    try:
        scores = _parse_rubric_json(raw)
    except Exception as exc:  # noqa: BLE001
        return {axis: "UNMEASURED" for axis in AXES} | {
            "_evaluator": evaluator, "_parse_error": str(exc)[:200]
        }
    scores["_evaluator"] = evaluator
    return scores


# ---------------------------------------------------------------------------
# Persistence — append-only metrics.jsonl, mutable feedback.json.
# ---------------------------------------------------------------------------
def append_metric(record: dict[str, Any]) -> None:
    record = {"ts": datetime.now(timezone.utc).isoformat(), **record}
    with METRICS_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_metrics() -> pd.DataFrame:
    if not METRICS_PATH.exists():
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    with METRICS_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(rows)


def load_feedback() -> dict[str, dict[str, float]]:
    if not FEEDBACK_PATH.exists():
        return {}
    try:
        return json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_feedback(data: dict[str, dict[str, float]]) -> None:
    FEEDBACK_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Phase A watcher — SHA256 over (relpath, mtime, size) tuples. No inotify.
# ---------------------------------------------------------------------------
def phase_a_signature() -> str:
    if not PHASE_A_GLOB_ROOT.exists():
        return "no-phase-a-dir"
    h = hashlib.sha256()
    for p in sorted(PHASE_A_GLOB_ROOT.rglob("*.md")):
        try:
            stat = p.stat()
        except FileNotFoundError:
            continue
        rel = p.relative_to(PHASE_A_GLOB_ROOT).as_posix()
        h.update(f"{rel}|{stat.st_mtime_ns}|{stat.st_size}\n".encode())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tension scan — string-level conflicts against living-terms.md headings.
# Returns list of (term, snippet); empty list ≠ guarantee of consistency.
# ---------------------------------------------------------------------------
def scan_tensions(output: str) -> list[tuple[str, str]]:
    if not LIVING_TERMS_PATH.exists() or not output.strip():
        return []
    terms: list[str] = []
    for line in LIVING_TERMS_PATH.read_text(encoding="utf-8").splitlines():
        m = re.match(r"##\s+\d{4}\s+—\s+(.+?)\s*$", line)
        if m:
            terms.append(m.group(1).strip())
    tensions: list[tuple[str, str]] = []
    lower = output.lower()
    for term in terms:
        # Flag if the term appears alongside negation within 60 chars.
        for hit in re.finditer(re.escape(term.lower()), lower):
            window = lower[max(0, hit.start() - 60): hit.end() + 60]
            if re.search(r"\b(not|never|no longer|fake|simulated)\b", window):
                tensions.append((term, output[max(0, hit.start() - 60): hit.end() + 60]))
    return tensions


# ---------------------------------------------------------------------------
# Re-prioritization — weakest-axis-first task selection.
# ---------------------------------------------------------------------------
@dataclass
class TaskPlan:
    model: str
    task: str
    rationale: str = ""
    weak_axes: list[str] = field(default_factory=list)


def numeric_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    keep = ["model"] + AXES
    sub = df[[c for c in keep if c in df.columns]].copy()
    for axis in AXES:
        if axis in sub.columns:
            sub[axis] = pd.to_numeric(sub[axis], errors="coerce")
    return sub


def reprioritize(df: pd.DataFrame, base_task: str) -> list[TaskPlan]:
    sub = numeric_metrics(df)
    plans: list[TaskPlan] = []
    if sub.empty:
        for model in DISPATCHERS:
            plans.append(TaskPlan(model=model, task=base_task,
                                  rationale="cold start — no metrics yet"))
        return plans
    means = sub.groupby("model")[AXES].mean(numeric_only=True)
    for model in DISPATCHERS:
        if model in means.index:
            row = means.loc[model].dropna()
            weak = row.nsmallest(2).index.tolist() if not row.empty else []
            focus = ", ".join(weak) if weak else "balanced"
            plans.append(TaskPlan(
                model=model,
                task=f"{base_task}\n\n[Self-improvement focus: emphasize {focus}.]",
                rationale=f"weakest axes: {focus}",
                weak_axes=weak,
            ))
        else:
            plans.append(TaskPlan(model=model, task=base_task,
                                  rationale="no prior runs for this model"))
    return plans


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Phase B — Self-Improving", layout="wide")
st.title("Phase B — Self-Improving Autoresearch")
st.caption(
    "Honest-degradation loop. Missing keys produce SKIPPED markers; "
    "missing evaluator produces UNMEASURED axes. See "
    "`foreword/living-terms.md` for terminology."
)

with st.sidebar:
    st.header("Truth Flags")
    flags = {
        "OPENAI_API_KEY":     bool(os.getenv("OPENAI_API_KEY")),
        "ANTHROPIC_API_KEY":  bool(os.getenv("ANTHROPIC_API_KEY")),
        "XAI_API_KEY":        bool(os.getenv("XAI_API_KEY")),
        "Ollama reachable":   None,
        "Council webhook":    None,
    }
    for k, v in flags.items():
        if v is True:
            st.success(f"{k}: present")
        elif v is False:
            st.warning(f"{k}: missing")
        else:
            st.info(f"{k}: probe on demand")
    st.divider()
    st.header("Phase A Watcher")
    watch_on = st.checkbox("Auto-rerun when Phase A changes", value=False)
    poll_s = st.number_input("Poll interval (s)", min_value=5, max_value=600, value=30)
    sig_now = phase_a_signature()
    st.code(sig_now[:16] + "…", language="text")
    last_sig = st.session_state.get("_phase_a_sig")
    if last_sig and last_sig != sig_now:
        st.warning("Phase A signature changed since last view.")
    st.session_state["_phase_a_sig"] = sig_now

tab_run, tab_metrics, tab_feedback, tab_tensions, tab_receipts = st.tabs(
    ["Run", "Metrics", "Feedback", "Tensions", "Receipts"]
)

# ---- Run tab --------------------------------------------------------------
with tab_run:
    base_task = st.text_area(
        "Base task",
        value="Summarize the most important insight from today's vault changes.",
        height=120,
    )
    df_now = load_metrics()
    plans = reprioritize(df_now, base_task)
    cols = st.columns(len(plans))
    for col, plan in zip(cols, plans):
        with col:
            st.subheader(plan.model)
            st.caption(plan.rationale)
            if st.button(f"Dispatch → {plan.model}", key=f"dispatch_{plan.model}"):
                with st.spinner(f"Calling {plan.model}…"):
                    output = DISPATCHERS[plan.model](plan.task)
                    scores = critique_7axis(plan.task, output)
                tensions = scan_tensions(output)
                record = {
                    "model": plan.model,
                    "task": plan.task,
                    "output": output,
                    "tensions": [{"term": t, "snippet": s} for t, s in tensions],
                    **{k: v for k, v in scores.items() if k in AXES},
                    "evaluator": scores.get("_evaluator"),
                }
                append_metric(record)
                st.code(output[:1200] + ("…" if len(output) > 1200 else ""),
                        language="markdown")
                st.json({k: scores[k] for k in AXES})
                if tensions:
                    st.warning(f"{len(tensions)} tension(s) flagged — see Tensions tab.")

# ---- Metrics tab ----------------------------------------------------------
with tab_metrics:
    df = load_metrics()
    if df.empty:
        st.info("No metrics yet. Dispatch a task in the Run tab.")
    else:
        st.write(f"{len(df)} records in `{METRICS_PATH.relative_to(REPO_ROOT)}`")
        sub = numeric_metrics(df)
        if not sub.empty:
            means = sub.groupby("model")[AXES].mean(numeric_only=True)
            st.subheader("Mean score per model (UNMEASURED excluded)")
            st.dataframe(means.style.format("{:.2f}"))
            st.subheader("Weakness spotlight")
            weak_per_model: dict[str, str] = {}
            for model, row in means.iterrows():
                row = row.dropna()
                weak_per_model[model] = row.idxmin() if not row.empty else "—"
            st.json(weak_per_model)
        st.subheader("Recent records")
        st.dataframe(df.tail(20))

# ---- Feedback tab ---------------------------------------------------------
with tab_feedback:
    fb = load_feedback()
    st.caption(
        "Human feedback persists to "
        f"`{FEEDBACK_PATH.relative_to(REPO_ROOT)}` and biases reprioritization."
    )
    for model in DISPATCHERS:
        st.markdown(f"**{model}**")
        cols = st.columns(len(AXES))
        model_fb = fb.get(model, {})
        for col, axis in zip(cols, AXES):
            current = float(model_fb.get(axis, 0.5))
            new_val = col.slider(axis, 0.0, 1.0, current, 0.05,
                                 key=f"fb_{model}_{axis}")
            model_fb[axis] = new_val
        fb[model] = model_fb
    if st.button("Save feedback"):
        save_feedback(fb)
        st.success(f"Saved {sum(len(v) for v in fb.values())} feedback values.")

# ---- Tensions tab ---------------------------------------------------------
with tab_tensions:
    df = load_metrics()
    if df.empty or "tensions" not in df.columns:
        st.info("No tensions recorded yet.")
    else:
        flagged = df[df["tensions"].apply(lambda x: bool(x) if isinstance(x, list) else False)]
        if flagged.empty:
            st.success("No tensions flagged across recorded runs.")
            st.caption("Empty list ≠ guarantee of consistency. Heuristic only.")
        else:
            for _, row in flagged.tail(20).iterrows():
                st.markdown(f"**{row.get('model')}** — {row.get('ts')}")
                for entry in row["tensions"]:
                    st.warning(f"`{entry['term']}` → …{entry['snippet']}…")

# ---- Receipts tab ---------------------------------------------------------
with tab_receipts:
    st.subheader("Ground-truth receipts")
    st.json({
        "metrics_path":      str(METRICS_PATH),
        "feedback_path":     str(FEEDBACK_PATH),
        "phase_a_signature": phase_a_signature(),
        "living_terms":      str(LIVING_TERMS_PATH),
        "endpoints":         ENDPOINTS,
        "models":            MODELS,
        "evaluator":         pick_evaluator() or "none (axes will be UNMEASURED)",
    })
    st.caption("This panel exists so any claim made by the UI can be audited "
               "against the underlying file system and configuration.")

# ---------------------------------------------------------------------------
# Optional auto-rerun. Uses st.rerun (st.experimental_rerun is deprecated).
# ---------------------------------------------------------------------------
if watch_on:
    time.sleep(int(poll_s))
    if phase_a_signature() != st.session_state.get("_phase_a_sig"):
        st.rerun()
