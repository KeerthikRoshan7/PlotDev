import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

def save_development(session_id, question_id, user_input, ai_response):
    try:
        data = {
            "session_id": session_id,
            "question_id": question_id,
            "user_input": user_input,
            "ai_response": ai_response
        }
        supabase.table("cloud_red_dev").insert(data).execute()
        return True
    except Exception as e:
        print(f"Supabase Error: {e}")
        return False
