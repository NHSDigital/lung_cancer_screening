from django.test import TestCase
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from .helpers.authentication import login_user
from ....models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues
from ....models.date_of_birth_response import DateOfBirthResponse


class TestGetResponses(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = self.user.responseset_set.create()

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/check-your-answers",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response, reverse("questions:start")
        )

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:responses"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_users_responses(self):
        DateOfBirthResponseFactory.create(
            response_set=self.response_set,
            value=date(2000, 9, 8)
        )

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertContains(response, "8 September 2000")

    def test_get_does_not_contain_responses_for_other_users(self):
        DateOfBirthResponseFactory.create(response_set=self.response_set, value=date(2000, 9, 8))

        other_response_set = ResponseSetFactory.create()
        DateOfBirthResponseFactory.create(response_set=other_response_set, value=date(1990, 1, 1))

        response = self.client.get(reverse("questions:responses"))

        self.assertNotContains(response, "1 January 1990")


class TestPostResponses(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = self.user.responseset_set.create()
        HaveYouEverSmokedResponse.objects.create(response_set=self.response_set, value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE)
        DateOfBirthResponse.objects.create(response_set=self.response_set, value=date(2000, 9, 8))

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/check-your-answers",
            fetch_redirect_response=False
        )

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:responses")
        )

        self.assertRedirects(response, reverse("questions:start"))


    def test_post_redirects_to_your_results(self):
        response = self.client.post(reverse("questions:responses"))

        self.assertRedirects(response, reverse("questions:your_results"), fetch_redirect_response=False)


    def test_post_marks_the_result_set_as_submitted(self):
        self.client.post(reverse("questions:responses"))

        self.assertIsNotNone(
            self.user.responseset_set.last().submitted_at
        )
