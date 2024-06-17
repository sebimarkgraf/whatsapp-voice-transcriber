from os import environ
from pathlib import Path

from fastapi.testclient import TestClient
from whatsapp_transcribe.__main__ import app

test_dir = Path(__file__).parent


environ["TWILIO_AUTH_TOKEN"] = "Placeholder"


def test_transcribe_endpoint_success():
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
