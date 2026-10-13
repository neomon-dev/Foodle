import json
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
DEFAULT_TARGET_LANGUAGE = os.getenv("DEFAULT_TARGET_LANGUAGE", "English")
MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "foodle.db"))


def _load_language_data():
    path = BASE_DIR / "data" / "languages.json"
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("languages", [])


SUPPORTED_LANGUAGES = _load_language_data()
SUPPORTED_LANGUAGE_CODES = {item["name"]: item["code"] for item in SUPPORTED_LANGUAGES}
SUPPORTED_LANGUAGE_NAMES = [item["name"] for item in SUPPORTED_LANGUAGES]


def get_supported_languages():
    return list(SUPPORTED_LANGUAGE_NAMES)


def get_default_target_language():
    if DEFAULT_TARGET_LANGUAGE in SUPPORTED_LANGUAGE_NAMES:
        return DEFAULT_TARGET_LANGUAGE
    return "English"
