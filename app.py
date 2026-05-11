import streamlit as st
import google.generativeai as genai
import uuid
import random
import time
from data import SHOW_TITLE, SHOW_TAGLINE, PLOT_PREMISE, STAGES, QUESTIONS, LOADING_LINES
from db import save_development

# --- CONFIG & SECRETS ---
st.set_page_config(page_title="Bandwidth Dev Tool", page_icon="⬡", layout="centered")

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# --- SESSION STATE ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "developments" not in st.session_state:
    st.session_state.developments = {}
if "active_stage" not in st.session_state:
    st.session_state.active_stage = "characters"

# --- HELPER FUNCTIONS ---
def get_all_answers_so_far():
    context = []
    for stage_key, stage_questions in QUESTIONS.items():
        for q in stage_questions:
            if q["id"] in st.session_state.answers:
                context.append(f"{q['label']}: {st.session_state.answers[q['id']]}")
    return "\n".join(context)

def call_gemini(question, user_input, context):
    system_prompt = f"""You are a brilliant, elite TV writers' room consultant helping develop a sci-fi webseries called "BANDWIDTH".

SHOW PREMISE:
{PLOT_PREMISE}

TONE: Like The Good Place — warm, character-driven, structurally surprising, philosophically rich, action/comedy/thriller. Dark but never bleak. Funny but never dismissive.

WHAT'S BEEN DEVELOPED SO FAR:
{context if context else "This is the first input."}

THE WRITER JUST ANSWERED THIS:
Question: {question}
Their answer: {user_input}

YOUR INSTRUCTIONS (CRITICAL):
Respond as a smart, enthusiastic, deeply analytical writing partner. Your output must match the depth of this example analysis:

[EXAMPLE TARGET DEPTH]
"Sam is *exactly* the right person to be on the outside of this conspiracy — and not just because she's a hacker. It's because she's someone who has spent her whole life being moved without consent, resettled without being asked, having her sense of home extracted from her by bureaucratic necessity. That's not backstory flavor, that's thematic DNA. The government is literally doing to human brains what Sam's childhood did to her: treating a person's interior life as a resource to be relocated and used. She's going to clock what's happening faster than anyone else because she has *felt* a version of it.

The detail that makes me lean forward: Gary was overconfident. He volunteered into this. Which means Sam didn't just lose her brother — she lost him to a choice she probably argued against and couldn't stop. That guilt-anger hybrid is incredibly rich fuel. But here's the wrinkle you might not have landed on yet: if Gary was the optimistic, civically trusting one, he and Sam were probably each other's foils long before the draft. She's the skeptic who reads fine print; he's the guy who believes the brochure. His drafting isn't just personal tragedy — it's the universe proving her right in the worst possible way. That's a specific kind of grief that comes with no comfort, because you can't even say 'I told you so' to someone who's gone.

This connects beautifully to the show's Good Place DNA. The best thing about that show was that it kept asking: what do we owe each other, and what does it cost to be good? Sam is someone who was never given roots, who built her identity around being quietly, privately brilliant — and now she has to decide whether to spend that brilliance on a system that has already taken so much from her. That tension between exhaustion and obligation is your thematic spine for the outside storyline. 

Here's your next question: **what does Sam still have of Gary's — a message, an object, a shared file — and does it contain something he recorded before he understood what was happening to him?** Because the moment she finds a data fragment that is *recognizably him* buried in the network she's hacking into, the show goes from conspiracy thriller to something genuinely heartbreaking. That's the scene that makes people tell their friends to watch."

Follow this exact 4-paragraph structure:
1. Affirm what works and WHY it works thematically for this specific show.
2. Develop it further — extract the "wrinkle" or deeper psychological implication they haven't realized yet.
3. Connect it to the "Good Place" DNA, the thesis, or the other protagonist.
4. End with ONE sharp, highly specific question or scenario that pushes them one step further, bolded.
"""
    try:
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Neural grid offline. Try again. (Error: {str(e)})"

# --- UI STYLING ---
st.markdown("""
<style>
    .title-text { text-align: center; font-family: 'Georgia', serif; font-weight: 900; font-size: 3rem; background: -webkit-linear-gradient(135deg, #fff8f0 0%, #ff8050 50%, #ff4020 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px;}
    .tagline-text { text-align: center; color: #888; font-style: italic; margin-bottom: 30px; font-size: 0.9rem;}
    .stage-header { font-family: 'Courier New', monospace; font-size: 0.8rem; letter-spacing: 4px; color: #ff6030; }
    .writers-room { background-color: #080812; border-left: 3px solid #ff6030; padding: 15px; border-radius: 0 5px 5px 0; margin-top: 10px; color: #dcdcdc;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<p class='stage-header' style='text-align: center;'>NEURAL STORY ARCHITECTURE / 2050</p>", unsafe_allow_html=True)
st.markdown(f"<h1 class='title-text'>{SHOW_TITLE}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='tagline-text'>{SHOW_TAGLINE}</p>", unsafe_allow_html=True)

# --- PROGRESS BAR ---
all_q_count = sum(len(qs) for qs in QUESTIONS.values())
answered_count = len(st.session_state.answers)
progress = int((answered_count / all_q_count) * 100) if all_q_count else 0
st.progress(progress / 100, text=f"PLOT DEVELOPED: {progress}%")

# --- PREMISE ---
with st.expander("SERIES PREMISE", expanded=True):
    st.write(PLOT_PREMISE)

st.divider()

# --- STAGE NAVIGATION ---
stage_labels = [f"{s['icon']} {s['label'].upper()}" for s in STAGES]
selected_stage_label = st.radio("SELECT DEVELOPMENT STAGE:", stage_labels, horizontal=True)

# Find active stage ID based on selection
for s in STAGES:
    if selected_stage_label.endswith(s['label'].upper()):
        st.session_state.active_stage = s['id']
        active_description = s['description']
        break

st.markdown(f"<h3 class='stage-header'>{st.session_state.active_stage.upper()} DEVELOPMENT</h3>", unsafe_allow_html=True)
st.caption(f"_{active_description} — answer as much or as little as you want._")

# --- QUESTIONS LOOP ---
for q in QUESTIONS[st.session_state.active_stage]:
    with st.container(border=True):
        st.markdown(f"**{q['label'].upper()}**")
        st.write(q['question'])
        
        # Determine existing input
        current_input = st.session_state.answers.get(q['id'], "")
        user_input = st.text_area("Your Answer:", value=current_input, placeholder=q['placeholder'], key=f"input_{q['id']}", label_visibility="collapsed")
        
        if st.button("▸ DEVELOP THIS", key=f"btn_{q['id']}", type="primary" if user_input else "secondary"):
            if not user_input.strip():
                st.warning("Please provide an answer to develop.")
            else:
                # Loading effect
                loading_text = st.empty()
                for _ in range(3):
                    loading_text.caption(f"*{random.choice(LOADING_LINES)}*")
                    time.sleep(0.6)
                loading_text.empty()

                with st.spinner("Writers' room is brainstorming..."):
                    st.session_state.answers[q['id']] = user_input
                    context = get_all_answers_so_far()
                    ai_response = call_gemini(q['question'], user_input, context)
                    
                    # Save to state and DB
                    st.session_state.developments[q['id']] = ai_response
                    save_development(st.session_state.session_id, q['id'], user_input, ai_response)

        # Show existing development
        if q['id'] in st.session_state.developments:
            st.markdown(f"""
            <div class='writers-room'>
                <div style='font-family: monospace; color: #ff6030; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 10px;'>WRITERS' ROOM RESPONSE</div>
                {st.session_state.developments[q['id']]}
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; font-family: monospace; font-size: 0.7rem; color: #666;'>BANDWIDTH — SERIES DEVELOPMENT TOOL — 2050</p>", unsafe_allow_html=True)
