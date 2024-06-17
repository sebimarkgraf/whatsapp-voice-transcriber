"""
# Twilio Client Module

This module contains the TwilioClient class which is responsible for
sending and receiving messages from Twilio.
This encapsulates the Twilio API and provides utility functions to format messages.

If we want to exchange Twilio for a custom implementation or another provider
 in the future, we only need to change this module.
"""

import io
import logging
import os
from base64 import b64encode

import requests
from fastapi import HTTPException, Response
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


class TwilioClient:
    """
    Twilio client for sending and receiving messages.

    This class is responsible for sending and receiving messages from Twilio.
    Additionally, it provides utility functions to format messages.

    Use this instead of the Twilio API directly, to allow better testing and mocking.
    """

    def __init__(self):
        self._auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self._account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self._webhook_url = os.environ["TWILIO_WEBHOOK_URL"]
        self.client = Client(self._account_sid, self._auth_token)
        self.validator = RequestValidator(self._auth_token)
        self._max_len = 1500
        self._from_number = os.environ["TWILIO_PHONE_NUMBER"]
        self._logger = logging.getLogger(__name__)

    def validate_request(self, body, signature):
        """
        Validate a Twilio request.

        A signature is invalid  due to a malicious request or
        wrongly configured URL, Token or Account SID.

        Args:
        ----
            body: The body of the request.
            signature: The signature of the request given by Twilio.

        Returns:
        -------
            bool: True if the request is valid, False otherwise.

        Raises:
        ------
            HTTPException: If the request signature is invalid.
        """
        if not self.validator.validate(str(self._webhook_url), body, signature):
            self._logger.error("Invalid Twilio signature")
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
        return True

    def create_return_message(self, message: str):
        """
        Create a Twilio response message.

        Args:
        ----
              message: The message to send. Is shortened to max_len characters.

        """
        response = MessagingResponse()
        response.message(self.shorten_message(message))
        return Response(content=str(response), media_type="application/xml")

    def _auth_header(self):
        token = b64encode(
            bytes(f"{self._account_sid}:{self._auth_token}", "utf-8")
        ).decode("utf-8")
        return {"Authorization": f"Basic {token}"}

    def download_media(self, url):
        response = requests.get(url, headers=self._auth_header())
        if response.status_code != 200:
            self._logger.error(f"Error downloading media: {response.text}")
            raise HTTPException(status_code=500, detail="Error downloading media")
        return io.BytesIO(response.content)

    def shorten_message(self, message: str):
        """
        Utility method to shorten strings to the maximum length defined in the class

        Args:
        ----
            message: Message to shorten

        Returns:
        -------

        """
        return (
            message[: self._max_len] + "..."
            if len(message) > self._max_len
            else message
        )

    def send_message(self, to: str, body: str):
        self._logger.verbose(f"Sending message to {to}")
        self.client.messages.create(
            to=to,
            from_=self._from_number,
            body=self.shorten_message(body),
        )
