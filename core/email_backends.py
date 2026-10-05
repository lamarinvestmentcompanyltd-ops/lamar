"""Send email through the Resend HTTPS API.

Railway's Free/Trial/Hobby plans block SMTP (ports 25/465/587), so Django's normal
SMTP backend cannot send there. This backend uses plain HTTPS instead and needs no
extra packages. Enable it by setting RESEND_API_KEY (see DEPLOYMENT.md).
"""
import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    api_url = "https://api.resend.com/emails"

    def send_messages(self, email_messages):
        api_key = getattr(settings, "RESEND_API_KEY", "")
        if not api_key:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY is not set.")
            return 0

        sent = 0
        for message in email_messages:
            payload = {
                "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
                "to": list(message.to),
                "subject": message.subject,
                "text": message.body,
            }
            if message.cc:
                payload["cc"] = list(message.cc)
            if message.bcc:
                payload["bcc"] = list(message.bcc)
            if message.reply_to:
                payload["reply_to"] = list(message.reply_to)

            request = urllib.request.Request(
                self.api_url,
                data=json.dumps(payload).encode("utf-8"),
                method="POST",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "lamar-site/1.0",
                },
            )
            try:
                timeout = getattr(settings, "EMAIL_TIMEOUT", None) or 10
                with urllib.request.urlopen(request, timeout=timeout):
                    pass
                sent += 1
            except (urllib.error.URLError, OSError):
                logger.exception("Resend API request failed")
                if not self.fail_silently:
                    raise
        return sent
