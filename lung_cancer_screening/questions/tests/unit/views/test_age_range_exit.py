from django.test import TestCase
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .helpers.authentication import login_user


class TestGetAgeRangeExit(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/age-range-exit",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:age_range_exit")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:age_range_exit"))

        self.assertEqual(response.status_code, 200)
