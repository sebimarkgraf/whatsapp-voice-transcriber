
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import os
from fastapi import HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import io
import logging
from base64 import b64encode

logger = logging.getLogger(__name__)

class TwilioClient:
    def __init__(self):
        self._auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self._account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.client =  Client(self._account_sid, self._auth_token)
        self.validator = RequestValidator(self._auth_token)

    def validateRequest(self, url, body, signature):
        if not self.validator.validate(str(url), body, signature):
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
        return True

    def create_return_message(self, message):
        response = MessagingResponse()
        msg = response.message(self.shorten_message(message))
        return Response(content=str(response), media_type="application/xml")

    def _auth_header(self):
        token = b64encode(bytes(f"{self._account_sid}:{self._auth_token}", "utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {token}"}

    def download_media(self, url):
        response = requests.get(url, headers=self._auth_header())
        if response.status_code != 200:
            logger.error(f"Error downloading media: {response.text}")
            raise HTTPException(status_code=500, detail="Error downloading media")
        return io.BytesIO(response.content)

    def shorten_message(self, message):
        return message[:1500] + "..." if len(message) > 1500 else message

    def send_message(self, to, body):
        self.client.messages.create(to=to, from_=os.environ["TWILIO_PHONE_NUMBER"], body=self.shorten_message(body))
