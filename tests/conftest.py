import pytest


@pytest.fixture(autouse=True)
def twilio_env_mock(monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "Account SID Placeholder")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "Auth Token Placeholder")
    monkeypatch.setenv("TWILIO_WEBHOOK_URL", "Webhook URL Placeholder")
    monkeypatch.setenv("TWILIO_PHONE_NUMBER", "Phone Number Placeholder")


@pytest.fixture(autouse=True)
def summarize_env_mock(monkeypatch):
    monkeypatch.setenv("SUMMARIZE_MODEL", "mayflowergmbh/wiedervereinigung")
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")


@pytest.fixture(autouse=True)
def security_env_mock(monkeypatch):
    monkeypatch.setenv("API_KEY", "API Token Placeholder")
