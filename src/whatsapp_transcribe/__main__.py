from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Header, Form, Response
from .transcribe import TranscriptionService
from .twilio_client import TwilioClient
from pydantic import BaseModel
from typing import Annotated
from twilio.twiml.messaging_response import MessagingResponse

transcription_service = TranscriptionService()
twilio_client = TwilioClient()

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


class Message(BaseModel):
    body: str
    from_: str
    to: str

@app.post("/twilio-whatsapp")
async def twilio_whatsapp(req: Request, From: str = Form(...), Body: str = Form(), x_twilio_signature: Annotated[str | None, Header()] = None):
    print(From, Body, x_twilio_signature)
    form_ = await req.form()

    twilio_client.validateRequest(req.url, form_, x_twilio_signature)

    #transcription = transcription_service.transcribe(voice_message.file)
    response = MessagingResponse()
    msg = response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")
    return {"transcription": "".join(transcription)}
