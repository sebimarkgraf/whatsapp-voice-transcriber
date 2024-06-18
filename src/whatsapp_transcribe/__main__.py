import logging
from dataclasses import dataclass
from typing import Annotated

from fastapi import (
    BackgroundTasks,
    FastAPI,
    Form,
    Header,
    HTTPException,
    Request,
    Response,
    Security,
    UploadFile,
)
from fastapi.security.api_key import APIKey

from .authentication import setup_api_key_auth
from .commands import Message, command_handling
from .summarize import Summarizer
from .transcribe import TranscriptionService
from .twilio_client import TwilioClient

transcription_service = TranscriptionService()
summarization_service = Summarizer()
twilio_client = TwilioClient()

app = FastAPI()

get_api_key = setup_api_key_auth()

logger = logging.getLogger(__name__)


@app.get("/health")
async def health():
    """
    Check the health of the service

    Returns:
        dict: Status of the service
    """
    return {"status": "UP"}


@app.post("/transcribe")
async def transcribe(
    voice_message: UploadFile, api_key: APIKey = Security(get_api_key)
):
    """
    Transcribe and summarize a voice message.

    Requires the API key to be passed in the Authorization header.

    Args:
        voice_message (UploadFile): The voice message to transcribe
        api_key (APIKey, Security
        The API key to authenticate the request

    Returns:
        dict: The transcription and summary of the voice message
    """
    if not voice_message.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    transcription = transcription_service.transcribe(voice_message.file)
    summary = summarization_service.summarize("".join(transcription))

    return {"transcription": "".join(transcription), "summary": summary}


@dataclass()
class TranscriptionTask:
    """
    Data wrapping for the transcription task.

    This contains all information that should be needed to perform a full transcription.
    Currently, this includes the URL of the voice message and the number
    that sent the request
    """

    media_url: str
    from_number: str


def perform_transcription(task: TranscriptionTask):
    """
    Perform a transcription task defined in the arg
    """
    logger.info("Media URL found, downloading...")
    content = twilio_client.download_media(task.media_url)
    logger.info("Media downloaded.")

    transcription = transcription_service.transcribe(content)
    summary = summarization_service.summarize("".join(transcription))

    twilio_client.send_message(task.from_number, f"Summarized: {summary}")


@app.post("/twilio-whatsapp")
async def twilio_whatsapp(
    background_tasks: BackgroundTasks,
    req: Request,
    From: str = Form(...),
    Body: Annotated[str | None, Form()] = None,
    x_twilio_signature: Annotated[str | None, Header()] = None,
    MediaUrl0: Annotated[str | None, Form()] = None,
):
    """
    Handle incoming messages from Twilio WhatsApp

    This endpoint is called by Twilio when a message is received.
    It will handle the message and respond accordingly.


    Args:
        background_tasks (BackgroundTasks): The background tasks to run
        req (Request): The request object
        From (str): The number that sent the message
        Body (str): The message body
        x_twilio_signature (str): The Twilio signature
        MediaUrl0 (str): The URL of the media
    """
    logger.info(f"Received message from {From}")
    form_ = await req.form()
    twilio_client.validate_request(form_, x_twilio_signature)

    if MediaUrl0 is None and not Body:
        return Response(content="No message or media found", status_code=400)

    if MediaUrl0 is None:
        logger.info("No media found, echoing message")
        return twilio_client.create_return_message(
            command_handling(Message(body=Body, from_number=From))
        )

    background_tasks.add_task(perform_transcription, TranscriptionTask(MediaUrl0, From))

    return twilio_client.create_return_message("Transcription in progress")
