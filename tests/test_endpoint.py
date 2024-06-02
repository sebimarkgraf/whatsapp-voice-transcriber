from fastapi.testclient import TestClient
from whatsapp_transcribe.__main__ import app
from pathlib import Path
from os import environ

test_dir = Path(__file__).parent


environ["TWILIO_AUTH_TOKEN"] = "Placeholder"

def test_transcribe_endpoint_success():
    client = TestClient(app)

    response = client.post("/transcribe", files={"voice_message": ("test.ogg", open(test_dir / "test.ogg", "rb"), "audio/ogg")})
    assert response.status_code == 200
