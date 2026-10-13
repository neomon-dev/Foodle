# Foodle

Foodle is a local-first multilingual menu translator built for travelers, international students, restaurant customers, and small food businesses. Users can upload menu photos, review OCR results, translate dish names, and receive structured explanations while keeping the process local and privacy-aware.

## Problem Foodle solves

Many diners face menu cards written in unfamiliar languages. A dish name alone often does not explain what is in the food, how it is prepared, how spicy it is, or whether ingredients may be a concern. Foodle helps users understand meals without requiring a paid API or sending private customer or restaurant data to a third party.

## Target users

- Tourists and travelers exploring regional cuisine.
- International students and newcomers in multilingual communities.
- Restaurants and cafes that want draft multilingual menu translations.
- Small food businesses that value local inference and privacy.

## Product positioning

Foodle is designed as a small-business tool: free for personal use, with a possible future paid restaurant localization workflow for draft menu generation, translation, and exports. The app is intentionally local-first because local open-weight AI reduces per-request API dependency and keeps the workflow usable without a paid service.

## Feature list

- Menu image upload and preview.
- Local OCR for JPG, JPEG, PNG, and WEBP files.
- Manual text entry for menus without photos.
- Source and target language selection.
- Local translation with Ollama-backed inference when available.
- Structured dish explanations for ingredients, flavor, preparation, and dietary uncertainty.
- Privacy-friendly local database for saved translation sessions.
- CSV and JSON export for menu results.
- Clear fallback behavior when OCR or model resources are unavailable.

## Screenshots

<img width="1900" height="1133" alt="image" src="https://github.com/user-attachments/assets/54136969-9082-4add-9508-b8e8362dbb66" />
<img width="1907" height="1145" alt="image" src="https://github.com/user-attachments/assets/cb6ac4f8-137f-43ab-8b1c-ad76320a8557" />

## Architecture overview

Foodle uses a modular Python app built with Streamlit. OCR runs locally with Tesseract and Pillow. The translation layer uses Ollama and an open-weight multilingual model when installed. SQLite stores saved translation sessions. Dish explanations are generated with a structured schema and a cautious fallback path when inference is not available.

## Requirements

- Python 3.12 or newer recommended.
- Windows PowerShell support.
- Ollama installed locally.
- A compatible open-weight model downloaded through Ollama.
- Tesseract OCR installed on the machine.
- Local SQLite database.

## Windows PowerShell setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

## Dependency installation

```powershell
python -m pip install -r requirements.txt
```

## Ollama installation and configuration

1. Install Ollama from the official installer for your platform.
2. Start the Ollama service locally.
3. Pull a compatible model, for example:

```powershell
ollama pull qwen2.5:7b
```

4. Set the following environment variables in a local `.env` file or through your shell:

```dotenv
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
DEFAULT_TARGET_LANGUAGE=English
MAX_IMAGE_SIZE_MB=10
DB_PATH=data/foodle.db
```

The project ships with a `.env.example` file for safe defaults. If the configured model is missing, Foodle shows a clear message and falls back to deterministic menu translation placeholders rather than pretending a translation succeeded.

## OCR installation and language packs

Tesseract OCR must be installed and available on PATH. On Windows, install Tesseract and ensure the `tesseract` command works in PowerShell:

```powershell
tesseract --version
```

If a specific language pack is required for a non-English script, install the corresponding Tesseract language data file for that language.

## App startup

```powershell
streamlit run app.py
```

## Offline functionality and limitations

Foodle is designed to work offline after the model, OCR dependencies, and SQLite database are installed locally. However, local inference requires suitable hardware and may be slower than a cloud API. Some model capabilities depend on the selected open-weight model and its language support. OCR quality can vary for blurry, rotated, or low-contrast menu images. Translation quality should be reviewed by the user before ordering or exporting results.

## Privacy policy

Foodle does not require a paid AI API key for the default workflow. By default, the app uses local Ollama inference and local OCR. Menu data is stored locally in SQLite for saved translations. The project does not collect menu data externally. Users should still avoid uploading private or sensitive menu data when the device is shared or when a local environment is not trusted.

## Testing commands

```powershell
python -m pytest -q
```

## Troubleshooting

- If Ollama returns a connection error, confirm that the Ollama service is running and the base URL is correct.
- If the configured model is missing, run `ollama pull <model-name>`.
- If OCR fails, ensure Tesseract is installed and available on PATH.
- If a menu image is blurry or rotated, try a clearer photo or enter the dish names manually.
- If a dish explanation seems uncertain, Foodle intentionally warns users that the output should be verified with staff.

## License and model license information

This project is intended for educational and local development use. Check the actual license and restrictions of the Ollama model you choose before production use. Some open-weight models have specific licensing terms, usage restrictions, or safety policies. Foodle does not claim the model is guaranteed to support every language pair equally well.

## Business model sketch

Foodle can be positioned as a free personal translator with optional paid restaurant services for multilingual menu drafts, localization, and export workflows. The local inference model reduces dependency on paid per-request AI APIs and gives restaurants more control over unpublished menu content.

## User testing plan

1. Ask a traveler to translate a menu from a language they do not read.
2. Test a restaurant menu with both images and manual input.
3. Review dish explanations for ambiguity and uncertainty.
4. Confirm that saved sessions and exports work offline.
5. Capture user feedback on confidence, clarity, and ordering decisions.

## Feedback mechanism

Users can record quick notes in local session metadata and export menu drafts to CSV or JSON. This keeps data within the local environment and avoids external collection without consent.
