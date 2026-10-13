import json
from typing import Any, Dict, Iterable, List, Optional

from config import get_supported_languages
from services.llm_service import ModelUnavailableError, OllamaService


SUPPORTED_LANGUAGES = get_supported_languages()
PRESERVE_NAME_TRANSLATIONS = {
    "paneer tikka",
    "butter chicken",
    "biryani",
    "masala dosa",
    "idli",
    "samosa",
    "dal makhani",
    "chole bhature",
    "vada pav",
    "naan",
    "paratha",
    "gulab jamun",
    "dosa",
}
FALLBACK_TRANSLATIONS = {
    "paneer tikka": "Paneer Tikka",
    "butter chicken": "Butter Chicken",
    "biryani": "Biryani",
    "masala dosa": "Masala Dosa",
    "idli": "Idli",
    "samosa": "Samosa",
    "dal makhani": "Dal Makhani",
    "chole bhature": "Chole Bhature",
    "vada pav": "Vada Pav",
    "naan": "Naan",
    "paratha": "Paratha",
    "gulab jamun": "Gulab Jamun",
    "dosa": "Dosa",
    "rice": "Rice",
    "water": "Water",
    "tea": "Tea",
}


def validate_language(name: str):
    if not name or name.strip() == "":
        raise ValueError("Language selection cannot be empty.")
    if name not in SUPPORTED_LANGUAGES and name.lower() != "auto":
        raise ValueError(f"Unsupported language: {name}. Supported languages are managed centrally in config.py.")


def fallback_translate(text: str, source_language: str = "auto", target_language: str = "English") -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""

    lowered = cleaned.lower()
    if source_language.lower() == target_language.lower() == "english":
        if lowered in FALLBACK_TRANSLATIONS:
            return FALLBACK_TRANSLATIONS[lowered]
        return cleaned.title()

    if lowered in PRESERVE_NAME_TRANSLATIONS:
        return cleaned

    if target_language.lower() == "english":
        if lowered in FALLBACK_TRANSLATIONS:
            return FALLBACK_TRANSLATIONS[lowered]
        return cleaned.title()

    if source_language.lower() == "english" and target_language.lower() == "hindi":
        return {
            "butter chicken": "बटर चिकन",
            "paneer tikka": "पनीर टिक्का",
            "biryani": "बिरयानी",
            "masala dosa": "मसाला दोसा",
            "naan": "नान",
            "tea": "चाय",
        }.get(cleaned.lower(), cleaned)

    if source_language.lower() == "english" and target_language.lower() == "french":
        return {
            "butter chicken": "Poulet au beurre",
            "paneer tikka": "Paneer Tikka",
            "biryani": "Biryani",
            "masala dosa": "Masala Dosa",
        }.get(cleaned.lower(), cleaned)

    return cleaned


def translate_dish(dish_name: str, source_language: str = "auto", target_language: str = "English", llm_service: Optional[OllamaService] = None) -> Dict[str, Any]:
    if not dish_name or not dish_name.strip():
        raise ValueError("Dish name cannot be empty.")
    validate_language(source_language)
    validate_language(target_language)

    if llm_service is not None:
        try:
            translated = llm_service.translate_text(dish_name, source_language, target_language)
            if translated and translated.strip() != "":
                return {
                    "original_name": dish_name.strip(),
                    "translated_name": translated.strip(),
                    "status": "translated",
                }
        except ModelUnavailableError:
            pass

    return {
        "original_name": dish_name.strip(),
        "translated_name": fallback_translate(dish_name, source_language, target_language),
        "status": "fallback",
    }


def translate_menu_items(items: Iterable[str], source_language: str = "auto", target_language: str = "English") -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for item in items:
        name = str(item).strip()
        if not name:
            continue
        translated = translate_dish(name, source_language, target_language)
        results.append({
            "original_name": translated["original_name"],
            "translated_name": translated["translated_name"],
            "status": translated["status"],
        })
    return results
