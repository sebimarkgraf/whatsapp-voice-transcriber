from whatsapp_transcribe.commands import Message, command_handling


def test_echo():
    """Test echo command --> Should return text prefixed with Echo:

    e.g echo test --> Echo: test
    """
    response = command_handling(Message(body="echo test", from_number="123"))
    assert response == "Echo: test"


def test_help():
    """Test invocation with help command --> Should return the help message"""
    response = command_handling(Message(body="help", from_number="123"))
    assert response.startswith("Send a voice message to transcribe and summarize.")


def test_unknown():
    """Test invocation without known command --> Should return the help message"""
    response = command_handling(Message(body="unknown", from_number="123"))
    # Expected response is the help message
    assert response == command_handling(Message(body="help", from_number="123"))
