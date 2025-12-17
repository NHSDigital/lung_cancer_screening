from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .helpers.authentication import login_user


class TestLogout(TestCase):

    def setUp(self):
        self.user = login_user(self.client)


    def test_logout_redirects_to_logout_redirect_url(self):
        response = self.client.get(reverse("questions:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGOUT_REDIRECT_URL)


    def test_logout_destroys_session(self):
        self.client.get(reverse("questions:logout"))

        session = self.client.session
        self.assertTrue(session.is_empty())
