"""
Claw Fleet Unified Dashboard
============================
Combines:
  1) Awesome Foursome dispatch UI (ChatGPT, Claude, Grok, Gemma4) - real API calls
  2) Phase B SRE conflicts & hypotheses drill-down (filter, expand)
  3) Zero-touch pipeline launcher button

Run:
    cd phase_b
    pip install -r requirements.txt
    streamlit run app.py

Governance: UrantiOS / Triune Monism. Truth before convenience.
Every button surface tells you whether it is LIVE, PLACEHOLDER, or MISSING DATA.
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "json_repository" / "phase_b_sre_report.json"
DEMO_PATH = ROOT / "json_repository" / "phase_b_sre_report.demo.json"
LAUNCHER = ROOT / "launcher.sh"
ORCHESTRATOR = ROOT / "NanoClaw_Orchestrator.py"

# Endpoint defaults — override via sidebar or env vars
DEFAULT_ENDPOINTS = {
    "gemma4_ollama": os.getenv("GEMMA4_URL", "http://127.0.0.1:11434/api/chat"),
    "gemma4_model":  os.getenv("GEMMA4_MODEL", "gemma4:e4b"),
    "council_webhook": os.getenv("COUNCIL_WEBHOOK", "http://46.225.51.30:5678/webhook/council"),
    "anthropic_model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    "openai_model":    os.getenv("OPENAI_MODEL", "gpt-4o"),
    "xai_model":       os.getenv("XAI_MODEL", "grok-2-latest"),
}

# ---------------------------------------------------------------------------
# Page chrome
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Claw Fleet Dashboard",
    page_icon="🦞",
    layout="wide",
)

st.markdown(
    """
    <style>
    .live  { color:#4ade80; font-weight:bold; }
    .pend  { color:#fbbf24; font-weight:bold; }
    .miss  { color:#f87171; font-weight:bold; }
    .card  { background:#1e2937; padding:12px; border-radius:10px; }
    .head  { background:#0f172a; padding:16px; border-radius:10px; margin-bottom:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="head"><h1>🦞 Claw Fleet Dashboard</h1>'
    "<p>Obsidian Vault • Hetzner • Awesome Foursome • Council of Seven</p></div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar — endpoints, keys, notifications
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Config")

    ep = {}
    ep["gemma4_ollama"]   = st.text_input("Gemma4 Ollama URL",   DEFAULT_ENDPOINTS["gemma4_ollama"])
    ep["gemma4_model"]    = st.text_input("Gemma4 model tag",     DEFAULT_ENDPOINTS["gemma4_model"])
    ep["council_webhook"] = st.text_input("Council n8n webhook",  DEFAULT_ENDPOINTS["council_webhook"])
    ep["anthropic_model"] = st.text_input("Anthropic model",      DEFAULT_ENDPOINTS["anthropic_model"])
    ep["openai_model"]    = st.text_input("OpenAI model",         DEFAULT_ENDPOINTS["openai_model"])
    ep["xai_model"]       = st.text_input("xAI (Grok) model",     DEFAULT_ENDPOINTS["xai_model"])

    st.divider()
    st.subheader("🔑 API key status")
    key_status = {
        "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
        "OPENAI_API_KEY":    bool(os.getenv("OPENAI_API_KEY")),
        "XAI_API_KEY":       bool(os.getenv("XAI_API_KEY")),
    }
    for k, present in key_status.items():
        tag = '<span class="live">SET</span>' if present else '<span class="miss">MISSING</span>'
        st.markdown(f"- `{k}`: {tag}", unsafe_allow_html=True)

    st.divider()
    st.subheader("📢 Notifications")
    notify_email    = st.checkbox("Email on pipeline completion", value=False)
    notify_telegram = st.checkbox("Telegram on pipeline completion", value=False)

# ---------------------------------------------------------------------------
# AI dispatchers — real HTTP calls, honest errors
# ---------------------------------------------------------------------------
def call_gemma4(task: str) -> str:
    try:
        r = requests.post(
            ep["gemma4_ollama"],
            json={
                "model": ep["gemma4_model"],
                "messages": [{"role": "user", "content": task}],
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content") or json.dumps(data)[:400]
    except Exception as exc:
        return f"[GEMMA4 ERROR] {exc}"


def call_claude(task: str) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return "[CLAUDE SKIPPED] ANTHROPIC_API_KEY not set in environment."
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": ep["anthropic_model"],
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": task}],
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return "".join(b.get("text", "") for b in data.get("content", []))
    except Exception as exc:
        return f"[CLAUDE ERROR] {exc}"


def call_chatgpt(task: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "[CHATGPT SKIPPED] OPENAI_API_KEY not set in environment."
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
            json={
                "model": ep["openai_model"],
                "messages": [{"role": "user", "content": task}],
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"[CHATGPT ERROR] {exc}"


def call_grok(task: str) -> str:
    key = os.getenv("XAI_API_KEY")
    if not key:
        return "[GROK SKIPPED] XAI_API_KEY not set in environment."
    try:
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
            json={
                "model": ep["xai_model"],
                "messages": [{"role": "user", "content": task}],
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"[GROK ERROR] {exc}"


def call_council(task: str) -> str:
    """POST to n8n Council of Seven webhook, which fans out to all 7 seats."""
    try:
        r = requests.post(ep["council_webhook"], json={"question": task}, timeout=180)
        r.raise_for_status()
        return r.text
    except Exception as exc:
        return f"[COUNCIL ERROR] {exc}  (webhook may not be wired yet)"


DISPATCH = {
    "ChatGPT":  call_chatgpt,
    "Claude":   call_claude,
    "Grok":     call_grok,
    "Gemma4":   call_gemma4,
    "Council7": call_council,
}

# ---------------------------------------------------------------------------
# Section 1: Awesome Foursome
# ---------------------------------------------------------------------------
st.header("1. Awesome Foursome — dispatch")
st.caption(
    "Every button is a real HTTP call. Missing keys are reported honestly; "
    "Gemma4 uses local Ollama, Council uses the n8n webhook."
)

task = st.text_area(
    "Task",
    placeholder="e.g. what is the first concept of the foreword of The Urantia Book",
    height=80,
)

col1, col2, col3, col4 = st.columns(4)

def dispatch_single(name: str):
    if not task.strip():
        st.warning("Enter a task first.")
        return
    t0 = time.time()
    with st.spinner(f"{name} working…"):
        out = DISPATCH[name](task)
    dt = time.time() - t0
    st.session_state.setdefault("log", [])
    st.session_state["log"].append((name, dt, out))

with col1:
    st.markdown('<div class="card"><h4>ChatGPT</h4></div>', unsafe_allow_html=True)
    if st.button("Send → ChatGPT", use_container_width=True):
        dispatch_single("ChatGPT")
with col2:
    st.markdown('<div class="card"><h4>Claude</h4></div>', unsafe_allow_html=True)
    if st.button("Send → Claude", use_container_width=True):
        dispatch_single("Claude")
with col3:
    st.markdown('<div class="card"><h4>Grok</h4></div>', unsafe_allow_html=True)
    if st.button("Send → Grok", use_container_width=True):
        dispatch_single("Grok")
with col4:
    st.markdown('<div class="card"><h4>Gemma4</h4></div>', unsafe_allow_html=True)
    if st.button("Send → Gemma4", use_container_width=True):
        dispatch_single("Gemma4")

fc1, fc2 = st.columns([1, 1])
with fc1:
    if st.button("🚀 Run ALL with Awesome Foursome (parallel-ish)", use_container_width=True):
        if not task.strip():
            st.warning("Enter a task first.")
        else:
            for name in ("ChatGPT", "Claude", "Grok", "Gemma4"):
                dispatch_single(name)
with fc2:
    if st.button("🏛️ Run with Council of Seven (webhook)", use_container_width=True):
        if not task.strip():
            st.warning("Enter a task first.")
        else:
            dispatch_single("Council7")

st.subheader("Live output")
log = st.session_state.get("log", [])
if not log:
    st.info("No dispatches yet.")
else:
    for name, dt, out in reversed(log[-10:]):
        with st.expander(f"{name} • {dt:.1f}s"):
            st.code(out, language="markdown")

# ---------------------------------------------------------------------------
# Section 2: Phase B SRE conflicts & hypotheses
# ---------------------------------------------------------------------------
st.header("2. Phase B SRE — conflicts & hypotheses")

def load_report():
    if JSON_PATH.exists():
        return json.loads(JSON_PATH.read_text(encoding="utf-8")), "live"
    if DEMO_PATH.exists():
        return json.loads(DEMO_PATH.read_text(encoding="utf-8")), "demo"
    # Emit a tiny demo in-memory so the UI still works on first run
    return {
        "conflicts": [
            {
                "Model": "gemma4",
                "Subject": "Triune Monism",
                "Predicate": "grounds",
                "Object": "absolute unity",
                "Raw_Input": "Placeholder — run the pipeline to populate real data.",
            }
        ],
        "hypotheses": [
            {
                "Conflict_Source": {
                    "Subject": "Triune Monism",
                    "Predicate": "grounds",
                },
                "Hypothesis": "Placeholder hypothesis.",
                "Missing_Data/Theory": "Run ee_extract_triples.py + sre_process_and_generate.py.",
                "Suggested_Test": "Click 'Run Full Pipeline' below once scripts are in place.",
            }
        ],
    }, "placeholder"

report, origin = load_report()
tag = {"live": "live", "demo": "pend", "placeholder": "miss"}[origin]
st.markdown(
    f'Data source: <span class="{tag}">{origin.upper()}</span> '
    f'&nbsp; (<code>{JSON_PATH.relative_to(ROOT)}</code>)',
    unsafe_allow_html=True,
)

conflicts  = report.get("conflicts", [])
hypotheses = report.get("hypotheses", [])

models = sorted({c.get("Model", "unknown") for c in conflicts})
subjects = sorted({c.get("Subject", "") for c in conflicts if c.get("Subject")})

fcol1, fcol2 = st.columns(2)
with fcol1:
    model_filter = st.multiselect("Filter by AI Model", options=models)
with fcol2:
    subject_filter = st.multiselect("Filter by Subject", options=subjects)

filtered = [
    c for c in conflicts
    if (not model_filter   or c.get("Model")   in model_filter)
    and (not subject_filter or c.get("Subject") in subject_filter)
]

st.subheader(f"Conflicts ({len(filtered)} / {len(conflicts)})")
for i, c in enumerate(filtered, 1):
    title = f"{i}. {c.get('Subject','?')} → {c.get('Predicate','?')}  [{c.get('Model','?')}]"
    with st.expander(title):
        st.write("**Extracted Triple:**",
                 (c.get("Subject"), c.get("Predicate"), c.get("Object")))
        st.write("**Raw Evidence:**")
        st.code(c.get("Raw_Input", "N/A"))

st.subheader(f"Hypotheses ({len(hypotheses)})")
for i, h in enumerate(hypotheses, 1):
    src = h.get("Conflict_Source", {})
    title = f"{i}. {src.get('Subject','?')} → {src.get('Predicate','?')}"
    with st.expander(title):
        st.write("**Hypothesis:**",           h.get("Hypothesis", ""))
        st.write("**Required Data/Theory:**", h.get("Missing_Data/Theory", ""))
        st.write("**Suggested Test:**",       h.get("Suggested_Test", ""))

# ---------------------------------------------------------------------------
# Section 3: Run Full Pipeline
# ---------------------------------------------------------------------------
st.header("3. Orchestrator — run the zero-touch pipeline")

orchestrator_present = ORCHESTRATOR.exists()
launcher_present     = LAUNCHER.exists()

status_bits = []
status_bits.append(
    f'Orchestrator: <span class="{"live" if orchestrator_present else "miss"}">'
    f'{"FOUND" if orchestrator_present else "MISSING"}</span> '
    f'(<code>{ORCHESTRATOR.name}</code>)'
)
status_bits.append(
    f'Launcher: <span class="{"live" if launcher_present else "miss"}">'
    f'{"FOUND" if launcher_present else "MISSING"}</span> '
    f'(<code>{LAUNCHER.name}</code>)'
)
st.markdown(" &nbsp;•&nbsp; ".join(status_bits), unsafe_allow_html=True)

run_cols = st.columns(2)
with run_cols[0]:
    if st.button("▶ Run launcher.sh (EE → CM/HG → dashboard)", use_container_width=True,
                 disabled=not launcher_present):
        with st.spinner("Pipeline running…"):
            p = subprocess.run(
                ["bash", str(LAUNCHER)],
                cwd=ROOT, capture_output=True, text=True, timeout=900,
            )
        st.success(f"exit={p.returncode}")
        st.text_area("stdout", p.stdout, height=240)
        st.text_area("stderr", p.stderr, height=120)
        _notify(notify_email, notify_telegram, p.returncode)

with run_cols[1]:
    if st.button("▶ Run NanoClaw_Orchestrator.py", use_container_width=True,
                 disabled=not orchestrator_present):
        with st.spinner("Orchestrator running…"):
            cmd = ["python3", str(ORCHESTRATOR)]
            if notify_email:    cmd += ["--notify", "--email"]
            if notify_telegram: cmd += ["--notify", "--telegram"]
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
        st.success(f"exit={p.returncode}")
        st.text_area("stdout", p.stdout, height=240)
        st.text_area("stderr", p.stderr, height=120)
        _notify(notify_email, notify_telegram, p.returncode)


def _notify(email: bool, telegram: bool, code: int):
    """Fire-and-forget notifications. Honest about what is configured."""
    if email:
        try:
            import smtplib
            from email.message import EmailMessage
            m = EmailMessage()
            m.set_content(f"NanoClaw pipeline complete. exit={code}")
            m["Subject"] = "NanoClaw pipeline"
            m["From"] = "nanoclaw@localhost"
            m["To"] = os.getenv("NOTIFY_EMAIL", "research@phd.edu")
            with smtplib.SMTP("localhost") as s:
                s.send_message(m)
            st.toast("Email sent", icon="📧")
        except Exception as exc:
            st.toast(f"Email failed: {exc}", icon="⚠️")
    if telegram:
        tok = os.getenv("TELEGRAM_BOT_TOKEN")
        chat = os.getenv("TELEGRAM_CHAT_ID")
        if not (tok and chat):
            st.toast("Telegram env vars missing", icon="⚠️")
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{tok}/sendMessage",
                data={"chat_id": chat,
                      "text": f"NanoClaw pipeline complete. exit={code}"},
                timeout=10,
            )
            st.toast("Telegram sent", icon="📨")
        except Exception as exc:
            st.toast(f"Telegram failed: {exc}", icon="⚠️")

# ---------------------------------------------------------------------------
# Footer — receipts for audit (UrantiOS: truth before convenience)
# ---------------------------------------------------------------------------
with st.expander("ℹ️ Ground truth & receipts"):
    st.markdown(f"- **Now**: `{datetime.utcnow().isoformat()}Z`")
    st.markdown(f"- **ROOT**: `{ROOT}`")
    st.markdown(f"- **Report path**: `{JSON_PATH}` ({'exists' if JSON_PATH.exists() else 'missing'})")
    st.markdown(f"- **Orchestrator**: `{ORCHESTRATOR}` ({'exists' if ORCHESTRATOR.exists() else 'missing'})")
    st.markdown(f"- **Launcher**: `{LAUNCHER}` ({'exists' if LAUNCHER.exists() else 'missing'})")
    st.markdown(
        "- **Dispatch targets**: "
        f"Gemma4=`{ep['gemma4_ollama']}` · "
        f"Council=`{ep['council_webhook']}` · "
        f"Claude=`{ep['anthropic_model']}` · "
        f"GPT=`{ep['openai_model']}` · "
        f"Grok=`{ep['xai_model']}`"
    )
