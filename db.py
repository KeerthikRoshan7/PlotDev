"""
db.py — Supabase persistence layer for CLOUD RED Writers' Room.

Table schema (run in Supabase SQL editor):

    create table if not exists bandwidth_entries (
        id            uuid primary key default gen_random_uuid(),
        session_id    text not null,
        stage_id      text not null,
        question_id   text not null,
        question_text text not null,
        user_answer   text not null,
        ai_response   text,
        created_at    timestamptz default now(),
        updated_at    timestamptz default now()
    );

    create index if not exists idx_bandwidth_session
        on bandwidth_entries (session_id);

    create index if not exists idx_bandwidth_question
        on bandwidth_entries (session_id, question_id);

    -- Auto-update updated_at on row change
    create or replace function set_updated_at()
    returns trigger language plpgsql as $$
    begin
        new.updated_at = now();
        return new;
    end;
    $$;

    create or replace trigger bandwidth_updated_at
        before update on bandwidth_entries
        for each row execute procedure set_updated_at();
"""

from __future__ import annotations
import streamlit as st
from supabase import create_client, Client
from typing import Optional

TABLE = "bandwidth_entries"


@st.cache_resource
def get_supabase() -> Client:
    """Return a cached Supabase client using Streamlit secrets."""
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ── READ ─────────────────────────────────────────────────────────────────────

def load_session(session_id: str) -> tuple[dict, dict]:
    """
    Fetch all rows for a session.
    Returns (answers, developments) as {question_id: text} dicts.
    """
    try:
        client = get_supabase()
        res = (
            client.table(TABLE)
            .select("question_id, user_answer, ai_response")
            .eq("session_id", session_id)
            .execute()
        )
        answers: dict[str, str] = {}
        developments: dict[str, str] = {}
        for row in res.data or []:
            qid = row["question_id"]
            answers[qid] = row["user_answer"]
            if row.get("ai_response"):
                developments[qid] = row["ai_response"]
        return answers, developments
    except Exception as e:
        st.toast(f"⚠️ Could not load session: {e}", icon="⚠️")
        return {}, {}


# ── WRITE ─────────────────────────────────────────────────────────────────────

def upsert_entry(
    session_id: str,
    stage_id: str,
    question_id: str,
    question_text: str,
    user_answer: str,
    ai_response: Optional[str] = None,
) -> None:
    """
    Insert or update a single question entry for this session.
    Uses question_id + session_id as the natural unique key via upsert.
    """
    try:
        client = get_supabase()
        payload = {
            "session_id":    session_id,
            "stage_id":      stage_id,
            "question_id":   question_id,
            "question_text": question_text,
            "user_answer":   user_answer,
        }
        if ai_response is not None:
            payload["ai_response"] = ai_response

        # Check if row already exists
        existing = (
            client.table(TABLE)
            .select("id")
            .eq("session_id", session_id)
            .eq("question_id", question_id)
            .execute()
        )

        if existing.data:
            # Update
            client.table(TABLE).update(payload).eq(
                "session_id", session_id
            ).eq("question_id", question_id).execute()
        else:
            # Insert
            client.table(TABLE).insert(payload).execute()

    except Exception as e:
        st.toast(f"⚠️ Could not save entry: {e}", icon="⚠️")


def update_ai_response(
    session_id: str,
    question_id: str,
    ai_response: str,
) -> None:
    """Patch only the ai_response field after streaming completes."""
    try:
        client = get_supabase()
        client.table(TABLE).update({"ai_response": ai_response}).eq(
            "session_id", session_id
        ).eq("question_id", question_id).execute()
    except Exception as e:
        st.toast(f"⚠️ Could not save AI response: {e}", icon="⚠️")


def delete_session(session_id: str) -> None:
    """Delete all rows belonging to a session (used on Reset)."""
    try:
        client = get_supabase()
        client.table(TABLE).delete().eq("session_id", session_id).execute()
    except Exception as e:
        st.toast(f"⚠️ Could not reset session: {e}", icon="⚠️")
