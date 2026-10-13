import pandas as pd
import streamlit as st

from config import get_supported_languages
from services.ocr_service import OCRDependencyError, extract_text_from_image, validate_uploaded_image
from services.translation_service import translate_menu_items


def render_translate_menu_page():
    st.title("Translate a Menu")
    source_language = st.selectbox("Source language", get_supported_languages() + ["Auto detect"], index=len(get_supported_languages()) - 1)
    target_language = st.selectbox("Target language", get_supported_languages(), index=0)

    uploaded_file = st.file_uploader(
        "Upload a menu image",
        type=["png", "jpg", "jpeg", "webp"],
        help="Images are validated before OCR and limited to a sensible local size threshold.",
    )

    if uploaded_file is not None:
        try:
            metadata = validate_uploaded_image(uploaded_file)
            st.image(metadata["bytes"], caption=metadata["name"], use_container_width=True)
        except ValueError as exc:
            st.error(str(exc))
            return

    ocr_text = st.session_state.get("ocr_text", "")
    ocr_text = st.text_area("OCR text preview and editing", value=ocr_text, height=220)
    st.session_state["ocr_text"] = ocr_text

    if st.button("Extract text from menu"):
        if uploaded_file is None:
            st.warning("Please upload a menu image before extracting text.")
            return
        try:
            extracted = extract_text_from_image(uploaded_file, source_language if source_language != "Auto detect" else "auto")
            st.session_state["ocr_text"] = extracted
            st.success("Extraction finished. Review and edit the OCR text before translating.")
            st.rerun()
        except (OCRDependencyError, ValueError) as exc:
            st.error(str(exc))

    if st.button("Translate extracted dishes"):
        if not ocr_text.strip():
            st.warning("OCR text is empty. Add a clearer menu image or enter items manually.")
            return

        entries = [line.strip() for line in ocr_text.splitlines() if line.strip()]
        translated = translate_menu_items(entries, source_language if source_language != "Auto detect" else "auto", target_language)
        df = pd.DataFrame(translated)
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False)
        st.download_button("Download CSV", data=csv_data, file_name="foodle_translations.csv", mime="text/csv")
        st.download_button("Download JSON", data=df.to_json(orient="records", force_ascii=False), file_name="foodle_translations.json", mime="application/json")
