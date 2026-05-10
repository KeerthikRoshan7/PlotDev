import uuid
import streamlit as st
from google import genai
from google.genai import types
from data import (
    SHOW_TITLE, SHOW_TAGLINE, SHOW_PREMISE,
    STAGES, QUESTIONS, SYSTEM_PROMPT
)
from db import load_session, upsert_entry, update_ai_response, delete_session

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CLOUD RED — Writers' Room",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "db_loaded" not in st.session_state:
    st.session_state.db_loaded = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "developments" not in st.session_state:
    st.session_state.developments = {}

if "active_stage" not in st.session_state:
    st.session_state.active_stage = "characters"

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Load from Supabase once per session
if not st.session_state.db_loaded:
    saved_answers, saved_devs = load_session(st.session_state.session_id)
    if saved_answers:
        st.session_state.answers = saved_answers
        st.session_state.developments = saved_devs
        st.session_state.splash_done = True   # skip splash if resuming
    st.session_state.db_loaded = True

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --accent: #ff5a2c;
    --accent2: #ff8c5a;
    --accent-dim: rgba(255,90,44,0.12);
    --accent-border: rgba(255,90,44,0.3);
    --bg: #080810;
    --bg2: #0d0d18;
    --bg3: #111120;
    --border: #1a1a2e;
    --border2: #222235;
    --text: #e8e0d0;
    --text2: #a09888;
    --text3: #605850;
    --text4: #302828;
    --mono: 'DM Mono', monospace;
    --serif: 'DM Serif Display', serif;
    --body: 'Lora', serif;
}

html, body, [class*="css"] {
    font-family: var(--body) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background-color: var(--bg) !important;
    background-image:
        linear-gradient(rgba(255,90,44,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,90,44,0.025) 1px, transparent 1px) !important;
    background-size: 36px 36px !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"]      { display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 4rem !important;
}

.bw-display {
    font-family: var(--serif) !important;
    font-size: clamp(52px, 10vw, 80px);
    line-height: 1;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #fff5ee 0%, #ff8c5a 40%, #ff5a2c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.bw-mono {
    font-family: var(--mono) !important;
    font-size: 11px;
    letter-spacing: 6px;
    color: var(--accent);
    opacity: 0.65;
    text-transform: uppercase;
}
.bw-tagline {
    font-family: var(--body) !important;
    font-style: italic;
    font-size: 14px;
    color: var(--text3);
    margin-top: 10px;
    line-height: 1.7;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}
.stProgress > div > div {
    background: var(--border) !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    background: transparent !important;
}
div[data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-family: var(--mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    color: var(--text3) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--accent-dim) !important;
    border-color: var(--accent-border) !important;
    color: var(--accent2) !important;
}
div[data-testid="stRadio"] input { display: none !important; }

.q-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
    transition: border-color 0.3s;
}
.q-card.answered { border-color: rgba(255,90,44,0.22); }
.q-card-label {
    font-family: var(--mono) !important;
    font-size: 9px;
    letter-spacing: 3px;
    color: var(--accent);
    opacity: 0.6;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.q-card-question {
    font-family: var(--body) !important;
    font-size: 14px;
    color: var(--text2);
    line-height: 1.65;
    margin-bottom: 14px;
}
.q-answer-preview {
    font-family: var(--body) !important;
    font-size: 12px;
    font-style: italic;
    color: var(--text3);
    line-height: 1.6;
    padding: 10px 14px;
    background: rgba(0,0,0,0.2);
    border-radius: 6px;
    border-left: 2px solid var(--accent-border);
    margin-bottom: 12px;
}

textarea, .stTextArea textarea {
    background: var(--bg) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    resize: vertical !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--accent-border) !important;
    box-shadow: 0 0 0 1px var(--accent-dim) !important;
}
.stTextArea label { display: none !important; }

.stButton > button {
    background: var(--accent-dim) !important;
    border: 1px solid var(--accent-border) !important;
    border-radius: 8px !important;
    color: var(--accent2) !important;
    font-family: var(--mono) !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    padding: 10px 22px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,90,44,0.22) !important;
    border-color: rgba(255,90,44,0.5) !important;
}
.stButton > button:active { transform: scale(0.98) !important; }

.dev-card {
    background: #07070f;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-border);
    border-radius: 0 8px 8px 0;
    padding: 18px 20px;
    margin-top: 14px;
}
.dev-label {
    font-family: var(--mono) !important;
    font-size: 9px;
    letter-spacing: 4px;
    color: var(--accent);
    opacity: 0.5;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.dev-text {
    font-family: var(--body) !important;
    font-size: 13px;
    color: var(--text3);
    line-height: 1.9;
    white-space: pre-wrap;
}

.streamlit-expanderHeader {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
    font-size: 10px !important;
    letter-spacing: 4px !important;
    color: var(--text4) !important;
}
.streamlit-expanderContent {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    font-family: var(--body) !important;
    font-size: 13px !important;
    color: var(--text3) !important;
    font-style: italic !important;
    line-height: 1.85 !important;
}

.stSpinner > div { border-top-color: var(--accent) !important; }

.stAlert {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text2) !important;
    font-family: var(--body) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stMetric"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    color: var(--text3) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--serif) !important;
    font-size: 28px !important;
    color: var(--accent2) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.splash-container {
    text-align: center;
    padding: 80px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}
.section-header {
    font-family: var(--mono) !important;
    font-size: 10px;
    letter-spacing: 5px;
    color: var(--text4);
    text-transform: uppercase;
    margin-bottom: 4px;
}
.section-desc {
    font-family: var(--body) !important;
    font-size: 13px;
    font-style: italic;
    color: var(--text3);
    margin-bottom: 20px;
    line-height: 1.6;
}
.saved-pill {
    display: inline-block;
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 2px;
    color: #3a7a3a;
    background: rgba(50,120,50,0.1);
    border: 1px solid rgba(50,120,50,0.25);
    border-radius: 10px;
    padding: 2px 8px;
    margin-left: 8px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def get_all_answers_context() -> str:
    lines = []
    for stage_qs in QUESTIONS.values():
        for q in stage_qs:
            if q["id"] in st.session_state.answers:
                lines.append(f"{q['label']}: {st.session_state.answers[q['id']]}")
    return "\n".join(lines) if lines else "This is the first input."


def total_progress() -> int:
    total_qs = sum(len(qs) for qs in QUESTIONS.values())
    answered = len(st.session_state.answers)
    return int((answered / total_qs) * 100)


def stage_progress(stage_id: str) -> tuple[int, int]:
    qs = QUESTIONS[stage_id]
    answered = sum(1 for q in qs if q["id"] in st.session_state.answers)
    return answered, len(qs)


def stream_development(question_obj: dict, user_input: str):
    context = get_all_answers_context()
    user_msg = (
        f"WHAT'S BEEN DEVELOPED SO FAR:\n{context}\n\n"
        f"THE WRITER JUST ANSWERED:\n"
        f"Question: {question_obj['q']}\n"
        f"Their answer: {user_input}"
    )
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1000,
            temperature=0.9,
        ),
    ):
        if chunk.text:
            yield chunk.text


# ── SPLASH ────────────────────────────────────────────────────────────────────

if not st.session_state.splash_done:
    st.markdown(
        '<div class="splash-container"><div style="font-family:\'DM Mono\',monospace;'
        'font-size:11px;letter-spacing:7px;color:#ff5a2c;opacity:0.6;margin-bottom:8px">'
        '2050 · NEURAL STORY ARCHITECTURE</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<h1 class="bw-display" style="text-align:center">CLOUD RED</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="bw-tagline" style="text-align:center">{SHOW_TAGLINE}</p>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▸  ENTER THE WRITERS' ROOM", key="splash_btn"):
            st.session_state.splash_done = True
            st.rerun()
    st.stop()


# ── HEADER ────────────────────────────────────────────────────────────────────

col_title, col_pct = st.columns([3, 1])
with col_title:
    st.markdown('<div class="bw-mono">CLOUD RED · PLOT DEVELOPMENT</div>', unsafe_allow_html=True)
    st.markdown(
        "<h1 class=\"bw-display\" style=\"font-size:clamp(36px,6vw,52px)\">Writers' Room</h1>",
        unsafe_allow_html=True,
    )
with col_pct:
    pct = total_progress()
    st.metric("DEVELOPED", f"{pct}%")

st.progress(pct / 100)

sid_short = st.session_state.session_id[:8].upper()
st.markdown(
    f'<div style="font-family:\'DM Mono\',monospace;font-size:9px;color:#2a2a35;'
    f'letter-spacing:2px;margin-bottom:4px">SESSION · {sid_short} '
    f'<span class="saved-pill">● SUPABASE SYNC</span></div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ── PREMISE EXPANDER ──────────────────────────────────────────────────────────

with st.expander("SERIES PREMISE"):
    st.markdown(
        f'<p style="font-family:\'Lora\',serif;font-size:13px;color:#605850;'
        f'font-style:italic;line-height:1.85">{SHOW_PREMISE}</p>',
        unsafe_allow_html=True,
    )

st.write("")


# ── STAGE NAVIGATION ──────────────────────────────────────────────────────────

stage_labels = []
for s in STAGES:
    answered, total = stage_progress(s["id"])
    badge = f" {answered}/{total}" if answered > 0 else ""
    stage_labels.append(f"{s['icon']} {s['label']}{badge}")

stage_ids = [s["id"] for s in STAGES]
current_idx = stage_ids.index(st.session_state.active_stage)

selected_label = st.radio(
    "Stage",
    stage_labels,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed",
)
selected_idx = stage_labels.index(selected_label)
st.session_state.active_stage = stage_ids[selected_idx]
st.write("")

active_stage_meta = STAGES[selected_idx]
st.markdown(
    f'<div class="section-header">{active_stage_meta["label"].upper()} DEVELOPMENT</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="section-desc">{active_stage_meta["desc"]} — answer as much or as little as you want.</div>',
    unsafe_allow_html=True,
)


# ── QUESTION CARDS ────────────────────────────────────────────────────────────

active_questions = QUESTIONS[st.session_state.active_stage]

for i, q in enumerate(active_questions):
    qid         = q["id"]
    is_answered = qid in st.session_state.answers
    has_dev     = qid in st.session_state.developments
    answered_class = "answered" if is_answered else ""

    preview_html = (
        f"<div class='q-answer-preview'>\"{st.session_state.answers[qid]}\"</div>"
        if is_answered else ""
    )
    st.markdown(
        f"""
        <div class="q-card {answered_class}">
            <div class="q-card-label">{q['label'].upper()}</div>
            <div class="q-card-question">{q['q']}</div>
            {preview_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_val = st.session_state.answers.get(qid, "")
    user_input = st.text_area(
        label=q["label"],
        value=current_val,
        placeholder=q["ph"],
        height=90,
        key=f"ta_{qid}",
        label_visibility="collapsed",
    )

    btn_label = "▸  DEVELOP THIS" if not has_dev else "▸  RE-DEVELOP"
    if st.button(btn_label, key=f"btn_{qid}"):
        if user_input.strip():
            answer_text = user_input.strip()
            st.session_state.answers[qid] = answer_text

            # Persist answer to Supabase immediately
            upsert_entry(
                session_id    = st.session_state.session_id,
                stage_id      = st.session_state.active_stage,
                question_id   = qid,
                question_text = q["q"],
                user_answer   = answer_text,
            )

            # Stream AI response
            with st.spinner("Accessing memory fragment..."):
                full_response = ""
                placeholder = st.empty()
                for chunk in stream_development(q, answer_text):
                    full_response += chunk
                    placeholder.markdown(
                        f"""
                        <div class="dev-card">
                            <div class="dev-label">WRITERS' ROOM RESPONSE</div>
                            <div class="dev-text">{full_response}▌</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                placeholder.empty()

            st.session_state.developments[qid] = full_response

            # Persist AI response to Supabase
            update_ai_response(
                session_id  = st.session_state.session_id,
                question_id = qid,
                ai_response = full_response,
            )

            st.rerun()
        else:
            st.warning("Write something first — even a rough idea works.")

    if has_dev:
        st.markdown(
            f"""
            <div class="dev-card">
                <div class="dev-label">WRITERS' ROOM RESPONSE</div>
                <div class="dev-text">{st.session_state.developments[qid]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="bw-mono" style="margin-bottom:4px">STORY SO FAR</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:\'DM Mono\',monospace;font-size:9px;color:#2a2a35;'
        f'letter-spacing:2px;margin-bottom:12px">SESSION {sid_short}</div>',
        unsafe_allow_html=True,
    )

    total_answered = len(st.session_state.answers)
    total_all = sum(len(qs) for qs in QUESTIONS.values())
    st.progress(total_answered / total_all if total_all > 0 else 0)
    st.caption(f"{total_answered} of {total_all} questions answered")
    st.markdown("<hr>", unsafe_allow_html=True)

    if st.session_state.answers:
        for stage in STAGES:
            stage_qs = QUESTIONS[stage["id"]]
            stage_answers = [
                (q, st.session_state.answers[q["id"]])
                for q in stage_qs if q["id"] in st.session_state.answers
            ]
            if stage_answers:
                st.markdown(
                    f'<div class="bw-mono" style="font-size:9px;margin:12px 0 8px">'
                    f'{stage["icon"]} {stage["label"].upper()}</div>',
                    unsafe_allow_html=True,
                )
                for q, ans in stage_answers:
                    st.markdown(
                        f'<div style="font-size:11px;color:#605850;font-family:\'DM Mono\','
                        f'monospace;margin-bottom:2px">{q["label"]}</div>',
                        unsafe_allow_html=True,
                    )
                    preview = ans[:120] + ("..." if len(ans) > 120 else "")
                    st.markdown(
                        f'<div style="font-size:12px;font-style:italic;color:#404040;'
                        f'line-height:1.6;margin-bottom:10px">"{preview}"</div>',
                        unsafe_allow_html=True,
                    )
    else:
        st.markdown(
            '<p style="font-size:13px;font-style:italic;color:#302828">'
            'Nothing yet. Start developing your plot above.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("↺  RESET EVERYTHING", key="reset_btn"):
        delete_session(st.session_state.session_id)
        st.session_state.answers      = {}
        st.session_state.developments = {}
        st.session_state.active_stage = "characters"
        st.session_state.splash_done  = False
        st.session_state.session_id   = str(uuid.uuid4())
        st.rerun()


# ── FOOTER ────────────────────────────────────────────────────────────────────

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<p style="font-family:\'DM Mono\',monospace;font-size:10px;color:#1e1e2e;'
    'letter-spacing:3px;text-align:center">CLOUD RED · SERIES DEVELOPMENT TOOL · 2050</p>',
    unsafe_allow_html=True,
)
