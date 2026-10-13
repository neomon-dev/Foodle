import streamlit as st

from config import get_supported_languages
from services.dish_explainer import explain_dish
from services.llm_service import OllamaService


def render_explain_dish_page():
    st.title("Explain a Dish")
    source_language = st.selectbox("Source language", get_supported_languages(), index=0)
    target_language = st.selectbox("Target language", get_supported_languages(), index=0)

    dish_input = st.text_area(
        "Dish names (one per line)",
        value="Paneer Tikka\nButter Chicken\nMasala Dosa",
        help="Enter one dish name per line. Foodle will explain each item and call out uncertainty.",
    )

    if st.button("Translate and explain"):
        entries = [line.strip() for line in dish_input.splitlines() if line.strip()]
        if not entries:
            st.warning("Please add at least one dish name.")
            return

        client = OllamaService()
        for item in entries:
            explanation = explain_dish(item, source_language, target_language, client)
            st.markdown(f"### {item}")
            st.write(f"**Translated name:** {explanation.translated_name}")
            st.write(f"**Short description:** {explanation.short_description}")
            st.write(f"**Ingredients:** {', '.join(explanation.ingredients) if explanation.ingredients else 'Unknown'}")
            st.write(f"**Preparation method:** {explanation.preparation_method}")
            st.write(f"**Flavor profile:** {explanation.flavor_profile}")
            st.write(f"**Spice level:** {explanation.spice_level}")
            st.write(f"**Dietary tags:** {', '.join(explanation.dietary_tags) if explanation.dietary_tags else 'Not enough evidence'}")
            st.write(f"**Confidence / uncertainty:** {explanation.confidence_or_uncertainty}")
            st.write(f"**Additional notes:** {explanation.additional_notes}")
            st.markdown("---")
