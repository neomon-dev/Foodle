import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from services.llm_service import ModelUnavailableError, OllamaService


class DishExplanation(BaseModel):
    original_name: str
    translated_name: str
    short_description: str
    ingredients: List[str] = Field(default_factory=list)
    preparation_method: str = "Unknown"
    flavor_profile: str = "Not enough information"
    spice_level: str = "Unknown"
    dietary_tags: List[str] = Field(default_factory=list)
    confidence_or_uncertainty: str = "Moderate confidence; verify with staff if this is a special or regional dish."
    additional_notes: str = "Ingredients and preparation details are not verified from a restaurant recipe."


def _fallback_explanation(dish_name: str, source_language: str = "auto", target_language: str = "English") -> DishExplanation:
    name = dish_name.strip() or "Dish"
    if not name:
        raise ValueError("Dish name cannot be empty.")

    lowered = name.lower()
    ingredients = ["Common regional ingredients"]
    preparation = "Prepared by cooking the ingredients in a traditional manner."
    flavor = "Varies by recipe and restaurant; likely savory and aromatic."
    spice = "Unknown or mild depending on preparation."
    dietary: List[str] = []

    if "paneer" in lowered:
        ingredients = ["Paneer", "Spices", "Onion", "Tomato", "Yogurt or cream"]
        preparation = "Paneer is marinated and cooked with a spiced sauce or tandoor-style preparation."
        flavor = "Creamy, smoky, mildly spiced, and rich."
        spice = "Mild to medium."
        dietary = ["Vegetarian"]
    elif "butter" in lowered and "chicken" in lowered:
        ingredients = ["Chicken", "Tomato", "Butter", "Cream", "Warm spices"]
        preparation = "Chicken is marinated, cooked, and finished in a rich tomato-butter sauce."
        flavor = "Rich, creamy, mild, and comforting."
        spice = "Mild."
        dietary = ["Contains dairy"]
    elif "biryani" in lowered:
        ingredients = ["Rice", "Seasoning", "Herbs", "Vegetables or meat"]
        preparation = "Rice and ingredients are layered and slow-cooked with aromatic spices."
        flavor = "Fragrant, savory, and aromatic with a layered texture."
        spice = "Medium depending on the recipe."
    elif "dosa" in lowered:
        ingredients = ["Rice batter", "Lentils", "Fermented batter", "Vegetable or filling"]
        preparation = "The batter is fermented and cooked on a griddle, sometimes filled or folded."
        flavor = "Crisp exterior, soft interior, savory and tangy."
        spice = "Usually mild to medium."
        dietary = ["Vegetarian"]

    return DishExplanation(
        original_name=name,
        translated_name=name,
        short_description=f"{name} is a dish that may include familiar local ingredients and a traditional cooking method.",
        ingredients=ingredients,
        preparation_method=preparation,
        flavor_profile=flavor,
        spice_level=spice,
        dietary_tags=dietary,
        confidence_or_uncertainty="Moderate confidence. Regional recipes vary and ingredient details should be confirmed with staff.",
        additional_notes="This description is general and not a substitute for a restaurant recipe or allergy verification.",
    )


def explain_dish(dish_name: str, source_language: str = "auto", target_language: str = "English", llm_service: Optional[OllamaService] = None) -> DishExplanation:
    if not dish_name or not dish_name.strip():
        raise ValueError("Dish name cannot be empty.")

    if llm_service is not None:
        try:
            raw = llm_service.explain_dish_json(dish_name, source_language, target_language)
            if raw:
                return DishExplanation.model_validate(raw)
        except (ModelUnavailableError, ValueError, TypeError, json.JSONDecodeError):
            pass

    return _fallback_explanation(dish_name, source_language, target_language)
