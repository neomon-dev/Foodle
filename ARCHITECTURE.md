# Foodle Architecture

## 1. OCR-to-translation pipeline

The core workflow starts with an uploaded menu image. The file is validated to confirm it is a real image and under the local size threshold. The OCR service then opens the image using Pillow, resizes it if necessary, and runs local OCR via Tesseract. The extracted text is reviewed by the user before translation so that OCR mistakes can be corrected before AI inference.

The app intentionally separates OCR from translation and explanation. This makes it easier to replace or improve either step independently without rewriting the entire application.

## 2. Model abstraction

The Ollama integration is centralized through `services/llm_service.py`. The service checks the configured base URL and model, then issues local inference requests to the Ollama API. The application does not hardcode a specific model name outside the configuration layer. Model choice is configurable through environment variables and the `.env` file.

If Ollama is unavailable or the named model is missing, the app raises a clear error and falls back to deterministic, carefully labeled outputs instead of pretending translation succeeded.

## 3. Dish explanation pipeline

The product uses structured dish explanations with a validated Pydantic model. Each explanation includes the original name, translated name, short description, ingredients, preparation method, flavor profile, spice level, dietary tags, confidence or uncertainty, and notes.

The explanation pipeline first tries a local model response when available. If inference fails or returns malformed JSON, the application falls back to deterministic culinary guidance using a conservative description system. This ensures the user sees honest uncertainty rather than invented certainty.

## 4. Local database

SQLite stores saved translation sessions and draft menus. The data layer lives under `database/` and is intentionally minimal. It supports initialization, saving, retrieval, and deletion of translation sessions. The database is local-only and is not required for the default AI workflow when the user is simply testing the app.

## 5. Error handling and privacy boundaries

Foodle handles several reliability concerns explicitly:

- Missing OCR dependency: the app surfaces a clear installation message.
- Missing model: the app shows a helpful warning and disables false certainty.
- Empty OCR output: the user is told to upload a clearer image or enter text manually.
- Uncertain dish explanations: the app warns the user to verify details with restaurant staff.
- Unsupported file types or oversize uploads: the app rejects them early.

The default privacy boundary is local inference. The app is built to avoid sending menu photos or restaurant information to paid external providers unless the user deliberately opts into a different pipeline.

## 6. Offline behavior

Foodle is designed for offline operation after the required dependencies are installed. Menu translation can still work with manual text input and deterministic fallback translation when local AI is unavailable. Local exports to CSV and JSON maintain a privacy-friendly offline environment.

## 7. UI architecture

The UI is a Streamlit app with a simple navigation sidebar and multiple sections:

- Home
- Translate a Menu
- Explain a Dish
- Restaurant Menu Studio
- Saved Translations
- Settings and Privacy

This architecture keeps the product simple while making it easy to expand into a business-facing restaurant workflow.
