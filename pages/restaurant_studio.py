import json

import pandas as pd
import streamlit as st

from config import get_supported_languages
from database.menu_repository import save_session
from services.menu_export_service import export_menu_records


def render_restaurant_studio_page():
    st.title("Restaurant Menu Studio")
    with st.form("restaurant_studio_form"):
        title = st.text_input("Menu title", value="Seasonal Menu Draft")
        source_language = st.selectbox("Source language", get_supported_languages(), index=0)
        target_language = st.selectbox("Target language", get_supported_languages(), index=1)
        menu_lines = st.text_area(
            "Menu items (one per line)",
            value="Butter Chicken\nPaneer Tikka\nMasala Dosa\nBiryani",
            height=200,
        )
        submitted = st.form_submit_button("Save draft menu")

    if submitted:
        items = [line.strip() for line in menu_lines.splitlines() if line.strip()]
        if not items:
            st.warning("Add at least one menu item before saving a draft.")
            return

        session_id = save_session(title, source_language, target_language, items, notes="Draft menu")
        st.success(f"Local draft saved with session ID {session_id}.")

    st.subheader("Preview")
    menu_lines_list = [line.strip() for line in (st.session_state.get("restaurant_menu_preview", "")).splitlines() if line.strip()] if st.session_state.get("restaurant_menu_preview") else []
    preview_text = st.text_area("Quick preview", value="\n".join(menu_lines_list) or "Butter Chicken\nPaneer Tikka\nBiryani", height=150)
    st.session_state["restaurant_menu_preview"] = preview_text

    records = [{"original_name": item, "translated_name": item, "notes": "Restaurant draft"} for item in preview_text.splitlines() if item.strip()]
    if st.button("Export menu draft"):
        try:
            export_path = export_menu_records(records, "json")
            st.success(f"Export created at {export_path}")
        except ValueError as exc:
            st.error(str(exc))
