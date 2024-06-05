from faster_whisper import WhisperModel
import os
from io import BytesIO

model_size = os.environ.get("MODEL_SIZE", "small")


class TranscriptionService:
    """
    Simple transcription service returning a Iterable of extracted Segments
    """

    def __init__(self):
        self.whisper_model = WhisperModel(model_size, device="cpu")

    def transcribe(self, voice_message: BytesIO):
        segments, _ = self.whisper_model.transcribe(voice_message)
        return list(s.text for s in segments)
