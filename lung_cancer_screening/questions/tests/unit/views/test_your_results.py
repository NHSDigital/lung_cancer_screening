from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user


class TestYourResults(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:your_results")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/your-results", fetch_redirect_response=False)

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:your_results"))

        self.assertEqual(response.status_code, 200)
