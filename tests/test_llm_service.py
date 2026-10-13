import requests
import pytest

from services.llm_service import ModelUnavailableError, OllamaService


def test_ollama_is_unavailable_when_endpoint_is_down(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException("down")

    monkeypatch.setattr(requests, "get", fake_get)
    service = OllamaService(base_url="http://localhost:11434", model="qwen2.5:7b")

    assert service.is_available() is False


def test_generate_raises_on_missing_model(monkeypatch):
    class DummyResponse:
        status_code = 200

        def json(self):
            return {"models": [{"name": "mistral:latest"}]}

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResponse())
    service = OllamaService(base_url="http://localhost:11434", model="qwen2.5:7b")

    with pytest.raises(ModelUnavailableError, match="not available"):
        service.generate("hello")
