import pytest

from services.translation_service import fallback_translate, translate_dish, validate_language


def test_known_name_uses_fallback_translation():
    result = translate_dish("Paneer Tikka", "English", "Hindi")
    assert result["original_name"] == "Paneer Tikka"
    assert result["translated_name"] == "Paneer Tikka"


def test_unsupported_language_raises_value_error():
    with pytest.raises(ValueError, match="Unsupported language"):
        validate_language("Esperanto")


def test_fallback_translation_returns_titleized_value():
    assert fallback_translate("butter chicken", "English", "English") == "Butter Chicken"
