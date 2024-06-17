"""
# Transcription

This module contains the TranscriptionService class
which is responsible for transcribing voice messages.
"""

from io import BytesIO
from os import environ
from typing import Optional

from faster_whisper import WhisperModel


class TranscriptionService:
    """
    Simple transcription service returning a Iterable of extracted Segments.
    Backed by OpenAI Whisper.
    """

    def __init__(self, model_size: Optional[str] = None):
        """
        Create a transcription service and load the transcription model into RAM.

        Args:
        ----
            model_size: Whisper model size possible options: "small", "medium", "large"

        """
        model_size = (
            model_size
            if model_size is not None
            else environ.get("TRANSCRIBE_MODEL", "small")
        )
        self.whisper_model = WhisperModel(model_size, device="cpu")

    def transcribe(self, voice_message: BytesIO):
        segments, _ = self.whisper_model.transcribe(voice_message)
        return list(s.text for s in segments)
