from os import environ
from pathlib import Path

from fastapi.testclient import TestClient

test_dir = Path(__file__).parent


def test_transcribe_endpoint_success():
    """
    Test the transcribe endpoint

    This performs both the transcription and summarization of a voice message.
    This does not test the handling of the twilio messages
    """
    from whatsapp_transcribe.__main__ import app

    client = TestClient(app)

    headers = {"authorization": "Bearer " + environ.get("API_KEY")}

    response = client.post(
        "/transcribe",
        files={
            "voice_message": (
                "test.ogg",
                open(test_dir / "test.ogg", "rb"),
                "audio/ogg",
            )
        },
        headers=headers,
    )
    assert response.status_code == 200


def test_health_endpoint():
    from whatsapp_transcribe.__main__ import app

    client = TestClient(app)

    response = client.get(
        "/health",
    )
    assert response.status_code == 200
