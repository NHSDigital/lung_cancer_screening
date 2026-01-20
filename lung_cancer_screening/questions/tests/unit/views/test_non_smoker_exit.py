from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory


class TestGetNonSmokerExit(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:non_smoker_exit")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/non-smoker-exit",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:non_smoker_exit")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:non_smoker_exit"))

        self.assertEqual(response.status_code, 200)
