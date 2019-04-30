from __future__ import unicode_literals

from django.conf import settings
from twilio.rest import Client


def get_twilio_config():
    return (
        settings.TWILIO_NUMBER, settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN)


class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid,
         twilio_auth_token) = get_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

    def send_message(self, body, to):
        self.twilio_client.messages.create(
            body=body, to=to, from_=self.twilio_number)
