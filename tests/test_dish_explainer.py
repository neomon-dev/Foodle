from services.dish_explainer import DishExplanation, explain_dish


class FakeLLM:
    def explain_dish_json(self, dish_name, source_language, target_language):
        return {
            "original_name": dish_name,
            "translated_name": "Masala Dosa",
            "short_description": "A savory, crisp South Indian breakfast dish.",
            "ingredients": ["Rice batter", "Lentils", "Potato"],
            "preparation_method": "Fermented and cooked on a griddle.",
            "flavor_profile": "Savory and crisp with a mild tang.",
            "spice_level": "Mild to medium.",
            "dietary_tags": ["Vegetarian"],
            "confidence_or_uncertainty": "High confidence for a common dish name.",
            "additional_notes": "Check the filling because restaurant recipes vary.",
        }


def test_explain_dish_preserves_original_name_and_reports_uncertainty():
    result = explain_dish("Masala Dosa", "English", "English", llm_service=FakeLLM())
    assert isinstance(result, DishExplanation)
    assert result.original_name == "Masala Dosa"
    assert "confidence" in result.confidence_or_uncertainty.lower()


def test_fallback_explanation_is_structured():
    result = explain_dish("Butter Chicken", "English", "Hindi")
    assert result.original_name == "Butter Chicken"
    assert result.short_description
    assert "Butter Chicken" in result.short_description or "Butter Chicken" in result.original_name
