from __future__ import unicode_literals

import os
import logging
import json
from django.conf import settings
from django.middleware.common import MiddlewareMixin
from cafe_backend.libs.twilio.messages import MessageClient


logger = logging.getLogger(__name__)

MESSAGE = """[This is a test] ALERT! It appears the server is having issues.
Exception: %s. Go to: http://newrelic.com for more details."""

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


class TwilioNotificationsMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        self.administrators = settings.ADMINS
        self.client = MessageClient()
        super(TwilioNotificationsMiddleware, self).__init__(*args, **kwargs)

    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

        for admin in self.administrators:
            # self.client.send_message(message_to_send, admin['phone'])
            pass

        logger.info('Administrators notified')

        return None
