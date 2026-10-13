import streamlit as st


def render_home_page():
    st.markdown(
        """
        <div class='hero'>
            <div class='hero-badge'>Local-first menu AI</div>
            <h1 class='hero-title'>Foodle</h1>
            <p class='hero-subtitle'>Translate the menu, understand the food, and order with confidence.</p>
            <div class='cta-row'>
                <span class='pill pill--accent'>🍽️ Multi-language menu reading</span>
                <span class='pill'>🧠 Local Ollama translation</span>
                <span class='pill'>🔒 Privacy-first workflow</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feature_cols = st.columns(3)
    feature_items = [
        ("📷 Menu upload", "Upload a menu image, review OCR, and correct extraction before translating."),
        ("🌍 Deep dish context", "Get translated names, ingredients, flavor notes, preparation clues, and uncertainty warnings."),
        ("🏪 Restaurant-ready", "Prepare draft multilingual menus and export them for local review or staff use."),
    ]
    for idx, (title, copy) in enumerate(feature_items):
        with feature_cols[idx]:
            st.markdown(
                f"""
                <div class='card'>
                    <h3>{title}</h3>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    stats = st.columns(3)
    stat_values = [("3 steps", "OCR → translate → explain"), ("Local AI", "Ollama powered"), ("Privacy", "No cloud default")]
    for idx, (value, label) in enumerate(stat_values):
        with stats[idx]:
            st.markdown(
                f"""
                <div class='stat'>
                    <span class='value'>{value}</span>
                    <div class='label'>{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### How Foodle works")
    st.markdown(
        """
        <ol>
            <li>Upload a menu image or enter a dish name.</li>
            <li>Extract text locally with OCR.</li>
            <li>Translate with a local open-weight model when available.</li>
            <li>Review explanations and save session results locally.</li>
        </ol>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Example translations")
    examples = [
        ("Butter Chicken", "बटर चिकन"),
        ("Paneer Tikka", "पनीर टिक्का"),
        ("Masala Dosa", "मसाला दोसा"),
        ("Biryani", "बिरयानी"),
    ]
    st.markdown(
        "<ul class='example-list'>" + "".join(f"<li>{original} → {translated}</li>" for original, translated in examples) + "</ul>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='info-box'>
            <strong>Foodle runs local AI inference by default.</strong> This keeps menu data on your device, but it needs a suitable machine and installed Ollama plus model files.
        </div>
        """,
        unsafe_allow_html=True,
    )
