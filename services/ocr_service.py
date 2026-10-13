import io
import os
from typing import BinaryIO, Optional

from PIL import Image, UnidentifiedImageError

try:
    import pytesseract
except ImportError:  # pragma: no cover - environment fallback
    pytesseract = None

from config import MAX_IMAGE_SIZE_MB


class OCRDependencyError(RuntimeError):
    """Raised when OCR dependencies are missing or cannot run locally."""


ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def validate_uploaded_image(file_obj: BinaryIO, max_size_mb: Optional[int] = None) -> dict:
    """Validate file bytes and return sanitized metadata used by the OCR step."""
    if file_obj is None:
        raise ValueError("No file was uploaded.")

    file_bytes = file_obj.read()
    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    extension = os.path.splitext(getattr(file_obj, "name", ""))[1].lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Unsupported image format. Use JPG, JPEG, PNG, or WEBP.")

    max_size_bytes = (max_size_mb or MAX_IMAGE_SIZE_MB) * 1024 * 1024
    if len(file_bytes) > max_size_bytes:
        raise ValueError(f"The uploaded image exceeds the {max_size_mb or MAX_IMAGE_SIZE_MB} MB limit.")

    image = None
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
    except (UnidentifiedImageError, OSError):
        raise ValueError("The uploaded file is not a valid image.")

    image = Image.open(io.BytesIO(file_bytes))

    width, height = image.size
    if width <= 0 or height <= 0:
        raise ValueError("The uploaded image is invalid or empty.")

    return {
        "bytes": file_bytes,
        "width": width,
        "height": height,
        "format": image.format or extension.lstrip("."),
        "name": getattr(file_obj, "name", "upload.png"),
    }


def extract_text_from_image(file_obj: BinaryIO, source_language: str = "auto") -> str:
    """Apply OCR locally and return the extracted text. This function intentionally keeps OCR separate from the translation layer."""
    if pytesseract is None:
        raise OCRDependencyError(
            "OCR dependencies are not installed. Install Tesseract OCR and pytesseract to use menu image translation."
        )

    metadata = validate_uploaded_image(file_obj)
    image = Image.open(io.BytesIO(metadata["bytes"]))

    max_pixel_count = 3000 * 3000
    if image.width * image.height > max_pixel_count:
        scale = (max_pixel_count / (image.width * image.height)) ** 0.5
        image = image.resize(
            (max(1, int(image.width * scale)), max(1, int(image.height * scale))),
            Image.Resampling.LANCZOS,
        )

    try:
        text = pytesseract.image_to_string(image, lang=_map_language_to_tesseract(source_language))
    except Exception as exc:  # pragma: no cover - handles runtime OCR failures
        raise OCRDependencyError(f"OCR failed to run locally: {exc}") from exc

    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not cleaned:
        raise ValueError("OCR extracted no readable text. Please upload a clearer menu image or enter items manually.")
    return cleaned


def _map_language_to_tesseract(language: str) -> str:
    if not language or language.lower() == "auto":
        return "eng"
    mapping = {
        "english": "eng",
        "hindi": "hin",
        "bengali": "ben",
        "telugu": "tel",
        "tamil": "tam",
        "kannada": "kan",
        "malayalam": "mal",
        "marathi": "mar",
        "gujarati": "guj",
        "punjabi": "pan",
        "urdu": "urd",
        "french": "fra",
        "spanish": "spa",
        "german": "deu",
        "italian": "ita",
        "japanese": "jpn",
        "korean": "kor",
        "chinese": "chi_sim",
        "arabic": "ara",
    }
    return mapping.get(language.lower(), "eng")
