
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import os

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
