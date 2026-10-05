from unittest.mock import patch

from django.core.mail import EmailMessage
from django.test import TestCase, override_settings
from django.urls import reverse

PAGES = [
    "home", "about", "services", "why_choose_us", "health_safety",
    "gallery", "materials", "faq", "privacy", "contact", "robots_txt", "sitemap_xml",
]


class PagesLoadTests(TestCase):
    """Every public page should load. Run with: python manage.py test"""

    def test_public_pages_return_200(self):
        for name in PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name), secure=True)
                self.assertEqual(response.status_code, 200)

    def test_unknown_page_returns_404(self):
        response = self.client.get("/this-page-does-not-exist/", secure=True)
        self.assertEqual(response.status_code, 404)


@override_settings(
    RESEND_API_KEY="re_test_key",
    EMAIL_BACKEND="core.email_backends.ResendEmailBackend",
    DEFAULT_FROM_EMAIL="info@lamarinvestment.rw",
)
class ResendBackendTests(TestCase):
    """The HTTPS email backend (used on Railway) builds the right request."""

    @patch("core.email_backends.urllib.request.urlopen")
    def test_message_is_posted_to_resend(self, urlopen):
        sent = EmailMessage(
            "Hello", "Body", "info@lamarinvestment.rw", ["info@lamarinvestment.rw"],
            reply_to=["visitor@example.com"],
        ).send()
        self.assertEqual(sent, 1)
        request = urlopen.call_args[0][0]
        self.assertEqual(request.full_url, "https://api.resend.com/emails")
        self.assertEqual(request.get_header("Authorization"), "Bearer re_test_key")
        self.assertIn(b"visitor@example.com", request.data)
