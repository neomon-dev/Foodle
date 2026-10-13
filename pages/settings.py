import streamlit as st

from config import DEFAULT_TARGET_LANGUAGE, MAX_IMAGE_SIZE_MB, OLLAMA_BASE_URL, OLLAMA_MODEL


def render_settings_page():
    st.title("Settings and Privacy")
    st.info(
        "Foodle keeps your menu data local by default. The AI inference happens on your machine when Ollama is available, and the app does not send menu photos to external providers by default."
    )

    st.subheader("Current configuration")
    st.write(f"**Ollama base URL:** {OLLAMA_BASE_URL}")
    st.write(f"**Configured model:** {OLLAMA_MODEL}")
    st.write(f"**Default target language:** {DEFAULT_TARGET_LANGUAGE}")
    st.write(f"**Max image upload size:** {MAX_IMAGE_SIZE_MB} MB")

    st.subheader("Model guidance")
    st.markdown(
        """
        - Pull a local multilingual open-weight model such as `qwen2.5:7b` or another compatible Qwen model through Ollama.
        - The app checks for the configured model at startup and shows a clear error if it is missing.
        - Support depends on the specific model and system resources available on your device.
        """
    )

    st.subheader("Privacy")
    st.write("Menu uploads are not sent to a paid external API in the default flow. The app recommends local inference and falls back gracefully when model or OCR dependencies are unavailable.")
