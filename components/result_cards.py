import streamlit as st


def render_result_card(title, result):
    with st.container():
        st.markdown(f"<div class='card'><h3>{title}</h3>", unsafe_allow_html=True)
        for key, value in result.items():
            if value is None:
                continue
            label = key.replace("_", " ").title()
            if isinstance(value, list):
                value = ", ".join(value)
            st.markdown(f"**{label}:** {value}")
        st.markdown("</div>", unsafe_allow_html=True)
