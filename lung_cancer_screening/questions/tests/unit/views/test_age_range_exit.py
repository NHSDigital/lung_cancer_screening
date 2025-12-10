from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user


class TestPostAgeRangeExit(TestCase):
    def setUp(self):
        login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/age-range-exit", fetch_redirect_response=False)


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:age_range_exit"))

        self.assertEqual(response.status_code, 200)
