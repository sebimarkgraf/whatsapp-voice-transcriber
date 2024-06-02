from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Header, Form, Response, BackgroundTasks
from .transcribe import TranscriptionService
from .twilio_client import TwilioClient
from pydantic import BaseModel
from typing import Annotated
from twilio.twiml.messaging_response import MessagingResponse
import requests
import io
import logging
from dataclasses import dataclass

transcription_service = TranscriptionService()
twilio_client = TwilioClient()

app = FastAPI()

logger = logging.getLogger(__name__)


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/transcribe")
async def transcribe(voice_message: UploadFile):
    if not voice_message.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    transcription = transcription_service.transcribe(voice_message.file)

    return {"transcription": "".join(transcription)}


@dataclass()
class TranscriptionTask:
    media_url: str
    from_number: str

def perform_transcription(task: TranscriptionTask):
    logger.info("Media URL found, downloading...")
    content = twilio_client.download_media(task.media_url)
    logger.info("Media downloaded.")

    transcription = transcription_service.transcribe(content)

    twilio_client.send_message(task.from_number, f"Transcription: {''.join(transcription)}")


@app.post("/twilio-whatsapp")
async def twilio_whatsapp(background_tasks: BackgroundTasks, req: Request, From: str = Form(...), Body: Annotated[str | None, Form()] = None, x_twilio_signature: Annotated[str | None, Header()] = None, MediaUrl0: Annotated[str | None, Form()] = None ):
    form_ = await req.form()
    twilio_client.validateRequest(req.url, form_, x_twilio_signature)

    if MediaUrl0 is None and not Body:
        return Response(content="No message or media found", status_code=400)

    if MediaUrl0 is None:
        return twilio_client.create_return_message(f"Echo: {Body}")

    background_tasks.add_task(perform_transcription, TranscriptionTask(MediaUrl0, From))

    return twilio_client.create_return_message("Transcription in progress")
