from whatsapp_transcribe.commands import Message, command_handling


def test_echo():
    response = command_handling(Message(body="echo test", from_number="123"))
    assert response == "Echo: test"


def test_help():
    response = command_handling(Message(body="help", from_number="123"))
    assert response.startswith("Send a voice message to transcribe and summarize.")


def test_unknown():
    response = command_handling(Message(body="unknown", from_number="123"))
    # Expected response is the help message
    assert response == command_handling(Message(body="help", from_number="123"))
