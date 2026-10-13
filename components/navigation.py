import streamlit as st


NAV_ITEMS = [
    "Home",
    "Translate a Menu",
    "Explain a Dish",
    "Restaurant Menu Studio",
    "Saved Translations",
    "Settings and Privacy",
]


def render_navigation():
    with st.sidebar:
        st.title("Foodle")
        st.caption("Your local multilingual menu translator")
        choice = st.radio("Navigate", NAV_ITEMS, index=0)
        st.markdown("---")
        st.caption("Local AI inference for privacy-conscious menu help.")
        return choice
