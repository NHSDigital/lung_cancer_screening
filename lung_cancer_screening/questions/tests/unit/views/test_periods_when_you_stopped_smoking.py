from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory


@tag("PeriodsWhenYouStoppedSmoking")
class TestGetPeriodsWhenYouStoppedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.age_when_started_smoking_response =  AgeWhenStartedSmokingResponseFactory.create(response_set=self.response_set)


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:periods_when_you_stopped_smoking")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/periods-when-you-stopped-smoking", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:periods_when_you_stopped_smoking")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.date_of_birth_response.delete()

        response = self.client.get(
            reverse("questions:periods_when_you_stopped_smoking")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:periods_when_you_stopped_smoking"))

        self.assertEqual(response.status_code, 200)


@tag("PeriodsWhenYouStoppedSmoking")
class TestPostPeriodsWhenYouStoppedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(response_set=self.response_set)

        self.valid_params = {
            "value": True,
            "duration_years": self.age_when_started_smoking_response.years_smoked_including_stopped() - 1
        }


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/periods-when-you-stopped-smoking", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.date_of_birth_response.delete()

        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_creates_a_periods_when_you_stopped_smoking_response(self):
        self.client.post(reverse("questions:periods_when_you_stopped_smoking"), self.valid_params)

        self.assertEqual(
            self.response_set.periods_when_you_stopped_smoking_response.value, self.valid_params["value"]
        )


    def test_redirects_to_responses(self):
        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:periods_when_you_stopped_smoking"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
