import io

import pytest
from PIL import Image

from services.ocr_service import validate_uploaded_image


def make_png_bytes(size=(100, 100), color="white"):
    image = Image.new("RGB", size, color)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_valid_image_upload_is_accepted():
    payload = io.BytesIO(make_png_bytes())
    payload.name = "menu.png"

    metadata = validate_uploaded_image(payload)

    assert metadata["name"] == "menu.png"
    assert metadata["width"] == 100
    assert metadata["height"] == 100


def test_invalid_file_type_is_rejected():
    payload = io.BytesIO(b"not an image")
    payload.name = "menu.txt"

    with pytest.raises(ValueError, match="Unsupported image format"):
        validate_uploaded_image(payload)


def test_oversized_upload_is_rejected():
    payload = io.BytesIO(make_png_bytes())
    payload.name = "large.png"

    with pytest.raises(ValueError, match="exceeds"):
        validate_uploaded_image(payload, max_size_mb=0.000001)
