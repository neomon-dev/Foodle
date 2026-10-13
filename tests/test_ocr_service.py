import io

import pytest
from PIL import Image

import services.ocr_service as ocr_module
from services.ocr_service import OCRDependencyError, extract_text_from_image


def make_png_bytes(size=(60, 60)):
    image = Image.new("RGB", size, color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_extract_text_raises_when_no_readable_text(monkeypatch):
    payload = io.BytesIO(make_png_bytes())
    payload.name = "menu.png"
    monkeypatch.setattr(ocr_module, "pytesseract", type("Dummy", (), {"image_to_string": lambda *args, **kwargs: "   "})())

    with pytest.raises(ValueError, match="OCR extracted no readable text"):
        extract_text_from_image(payload)


def test_extract_text_raises_when_dependencies_missing():
    payload = io.BytesIO(make_png_bytes())
    payload.name = "menu.png"
    original = ocr_module.pytesseract
    ocr_module.pytesseract = None
    try:
        with pytest.raises(OCRDependencyError, match="OCR dependencies are not installed"):
            extract_text_from_image(payload)
    finally:
        ocr_module.pytesseract = original
