from django.test import TestCase
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from ...factories.user_factory import UserFactory
from .helpers.authentication import login_user
from ....models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues
from ....models.date_of_birth_response import DateOfBirthResponse


class TestGetResponses(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.response_set = self.user.responseset_set.create()
        HaveYouEverSmokedResponse.objects.create(response_set=self.response_set, value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE)
        DateOfBirthResponse.objects.create(response_set=self.response_set, value=date(2000, 9, 8))

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:responses")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/responses",
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
        response = self.client.get(
            reverse("questions:responses")
        )

        have_you_ever_smoked = HaveYouEverSmokedResponse.objects.get(response_set=self.response_set)
        date_of_birth = DateOfBirthResponse.objects.get(response_set=self.response_set)
        self.assertContains(
            response,
            have_you_ever_smoked.get_value_display()
        )
        self.assertContains(
            response, date_of_birth.value
        )

    def test_get_does_not_contain_responses_for_other_users(self):
        other_user = UserFactory()
        other_response_set = other_user.responseset_set.create()
        DateOfBirthResponse.objects.create(response_set=other_response_set, value=date(1990, 1, 1))

        response = self.client.get(reverse("questions:responses"))

        other_date_of_birth = DateOfBirthResponse.objects.get(response_set=other_response_set)

        self.assertNotContains(
            response, other_date_of_birth.value
        )


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
            "/oidc/authenticate/?next=/responses",
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
