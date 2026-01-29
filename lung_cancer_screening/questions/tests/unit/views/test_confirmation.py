from django.test import TestCase, tag
from django.urls import reverse

from ...factories.response_set_factory import ResponseSetFactory
from .helpers.authentication import login_user

@tag("Confirmation")
class TestGetConfirmation(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:confirmation")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/confirmation",
            fetch_redirect_response=False
        )


    def test_get_redirects_when_no_submitted_response_set_exists(
        self
    ):
        ResponseSetFactory.create(user=self.user, submitted_at=None)

        response = self.client.get(
            reverse("questions:confirmation")
        )

        self.assertRedirects(response, reverse("questions:responses"), fetch_redirect_response=False)

    def test_get_responds_successfully_when_a_submitted_response_set_exists(self):
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.get(reverse("questions:confirmation"))

        self.assertEqual(response.status_code, 200)
