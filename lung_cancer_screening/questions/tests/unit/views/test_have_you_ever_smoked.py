from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues


@tag("HaveYouEverSmoked")
class TestGetHaveYouEverSmoked(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:have_you_ever_smoked")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/have-you-ever-smoked", fetch_redirect_response=False)


    def test_get_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:have_you_ever_smoked")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:have_you_ever_smoked"))

        self.assertEqual(response.status_code, 200)


@tag("HaveYouEverSmoked")
class TestPostHaveYouEverSmoked(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = { "value": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY }


    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/have-you-ever-smoked", fetch_redirect_response=False)


    def test_post_creates_an_unsubmitted_response_set_for_the_user_when_no_response_set_exists(self):
        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HaveYouEverSmokedResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_updates_an_unsubmitted_response_set_for_the_user_when_an_unsubmitted_response_set_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HaveYouEverSmokedResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_creates_an_new_unsubmitted_response_set_for_the_user_when_an_submitted_response_set_exists_over_a_year_ago(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HaveYouEverSmokedResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_when_an_submitted_response_set_exists_within_the_last_year(self):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_post_redirects_to_date_of_birth(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:date_of_birth"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_date_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)


    def test_post_redirects_if_the_user_not_a_smoker(self):
        response = self.client.post(
            reverse("questions:have_you_ever_smoked"),
            {"value": HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED.value }
        )

        self.assertRedirects(response, reverse("questions:non_smoker_exit"))
