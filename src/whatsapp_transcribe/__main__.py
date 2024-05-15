from fastapi import FastAPI, UploadFile, File
from .transcribe import TranscriptionService

transcription_service = TranscriptionService()

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/transcribe")
async def transcribe(voice_message: UploadFile):
    if not voice_message.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    transcription = transcription_service.transcribe(voice_message.file)

    return {"transcription": "".join(transcription)}
