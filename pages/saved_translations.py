import pandas as pd
import streamlit as st

from database.menu_repository import delete_session, list_sessions


def render_saved_translations_page():
    st.title("Saved Translations")
    sessions = list_sessions()
    if not sessions:
        st.info("No saved translation sessions yet. Create one from the menu translator or restaurant studio.")
        return

    df = pd.DataFrame(sessions)
    st.dataframe(df, use_container_width=True)

    selected = st.selectbox("Choose a session to delete", [session["id"] for session in sessions])
    if st.button("Delete selected session"):
        delete_session(selected)
        st.success(f"Session {selected} was deleted.")
        st.rerun()
