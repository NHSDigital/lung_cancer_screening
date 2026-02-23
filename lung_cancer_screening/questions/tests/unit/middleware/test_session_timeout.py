"""Tests for SessionTimeoutMiddleware."""
import time
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, override_settings, tag

from ....middleware.session_timeout import SessionTimeoutMiddleware

User = get_user_model()


def get_response(request):
    return Mock(status_code=200)


class FakeSession:
    """Dict-like session with flush() for middleware tests."""

    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __contains__(self, key):
        return key in self._data

    def flush(self):
        self._data.clear()


@override_settings(
    LOGIN_URL="/oidc/authenticate/",
    SESSION_INACTIVITY_TIMEOUT_SECONDS=30 * 60,
    SESSION_ABSOLUTE_TIMEOUT_SECONDS=12 * 60 * 60,
)
@tag("auth")
class SessionTimeoutMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionTimeoutMiddleware(get_response)
        self.user = User.objects.create_user(
            sub="test-sub",
            nhs_number="1234567890",
            email="test@example.com",
            given_name="Test",
            family_name="User",
        )

    def _request(self, path="/some-page/", user=None):
        request = self.factory.get(path)
        request.session = FakeSession()
        request.user = user or self.user
        return request

    def test_expires_after_inactivity_timeout(self):
        request = self._request()
        request.session["_last_activity"] = time.time() - (31 * 60)
        request.session["_session_start"] = time.time() - (10 * 60)

        response = self.middleware(request)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/oidc/authenticate/", response.url)
        self.assertIn("next=%2Fsome-page%2F", response.url)

    def test_expires_after_absolute_timeout(self):
        request = self._request()
        request.session["_last_activity"] = time.time() - 60
        request.session["_session_start"] = time.time() - (13 * 60 * 60)

        response = self.middleware(request)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/oidc/authenticate/", response.url)

    def test_does_not_expire_when_within_limits(self):
        request = self._request()
        request.session["_last_activity"] = time.time() - (10 * 60)
        request.session["_session_start"] = time.time() - (2 * 60 * 60)

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(request.session["_last_activity"], time.time() - 5)

    def test_unauthenticated_request_not_checked(self):
        request = self._request(user=AnonymousUser())

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_last_activity", request.session._data)
