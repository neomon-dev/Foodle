import streamlit as st

from components.navigation import render_navigation
from components.styles import inject_styles
from pages.explain_dish import render_explain_dish_page
from pages.home import render_home_page
from pages.restaurant_studio import render_restaurant_studio_page
from pages.saved_translations import render_saved_translations_page
from pages.settings import render_settings_page
from pages.translate_menu import render_translate_menu_page


st.set_page_config(page_title="Foodle", page_icon="🍽️", layout="wide")
st.markdown(inject_styles(), unsafe_allow_html=True)

PAGE_MAP = {
    "Home": render_home_page,
    "Translate a Menu": render_translate_menu_page,
    "Explain a Dish": render_explain_dish_page,
    "Restaurant Menu Studio": render_restaurant_studio_page,
    "Saved Translations": render_saved_translations_page,
    "Settings and Privacy": render_settings_page,
}

selection = render_navigation()
PAGE_MAP.get(selection, render_home_page)()
