import json
from typing import Any, Dict, Optional

import requests

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class ModelUnavailableError(RuntimeError):
    """Raised when the local Ollama endpoint is unavailable or the model is missing."""


class OllamaService:
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")
        self.model = model or OLLAMA_MODEL

    def _list_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        except requests.RequestException as exc:  # pragma: no cover - network path
            raise ModelUnavailableError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc

        if response.status_code != 200:
            raise ModelUnavailableError(f"Ollama request failed with status {response.status_code}.")

        payload = response.json()
        models = []
        for entry in payload.get("models", []):
            model_name = entry.get("name")
            if model_name:
                models.append(model_name)
        return models

    def is_available(self):
        try:
            models = self._list_models()
            return self.model in models or any(model.startswith(f"{self.model}:") for model in models)
        except ModelUnavailableError:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2):
        if not self.is_available():
            raise ModelUnavailableError(
                f"Ollama model '{self.model}' is not available. Start Ollama and pull the model first."
            )

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=60)
        except requests.RequestException as exc:  # pragma: no cover - network path
            raise ModelUnavailableError(f"Request failed while contacting Ollama: {exc}") from exc

        if response.status_code != 200:
            raise ModelUnavailableError(f"Ollama returned status {response.status_code}.")

        data = response.json()
        return str(data.get("response", "")).strip()

    def translate_text(self, text: str, source_language: str = "auto", target_language: str = "English") -> str:
        prompt = (
            f"Translate the following dish or menu text from {source_language} to {target_language}. "
            "Preserve the original dish name when it is culturally specific. Output only the translated text and nothing else.\n\n"
            f"Text: {text}"
        )
        return self.generate(prompt, system_prompt="You are a careful food translation assistant.")

    def explain_dish_json(self, dish_name: str, source_language: str = "auto", target_language: str = "English") -> Dict[str, Any]:
        prompt = (
            "Return valid JSON only with exactly these keys: original_name, translated_name, short_description, "
            "ingredients, preparation_method, flavor_profile, spice_level, dietary_tags, confidence_or_uncertainty, additional_notes. "
            "Use arrays for ingredients and dietary_tags. Preserve the original dish name. State uncertainties honestly. "
            f"Dish: {dish_name}. Source language: {source_language}. Target language: {target_language}."
        )
        result = self.generate(prompt, system_prompt="You are a cautious culinary explainer. Never invent certainty.")
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {}
