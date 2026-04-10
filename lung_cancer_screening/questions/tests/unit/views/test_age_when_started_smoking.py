from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory

@tag("AgeWhenStartedSmoking")
class TestGetAgeWhenStartedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/age-when-started-smoking",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )

        self.assertRedirects(response, reverse("questions:agree_terms_of_use"))

    def test_back_link_url_is_responses_if_change_query_param_is_true(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:age_when_started_smoking", query={"change": "True"})
        )

        self.assertEqual(response.context_data["back_link_url"], reverse("questions:responses"))

    def test_back_link_url_is_relatives_age_when_diagnosed_if_change_query_param_is_not_true(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )

        self.assertEqual(response.context_data["back_link_url"], reverse("questions:relatives_age_when_diagnosed"))

    def test_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:age_when_started_smoking")
        )
        self.assertEqual(response.status_code, 200)

@tag("AgeWhenStartedSmoking")
class TestPostAgeWhenStartedSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        self.valid_params = {
            "value": self.response_set.date_of_birth_response.age_in_years() - 20
        }

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/age-when-started-smoking",
            fetch_redirect_response=False
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:agree_terms_of_use"))


    def test_creates_an_age_when_started_smoking_response(self):
        self.client.post(reverse("questions:age_when_started_smoking"), self.valid_params)

        self.response_set.refresh_from_db()
        self.assertEqual(
            self.response_set.age_when_started_smoking_response.value, self.valid_params["value"]
        )


    def test_redirects_to_periods_when_you_stopped_smoking_as_a_current_smoker(self):
        self.response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            current_smoker=True
        )

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:periods_when_you_stopped_smoking"))


    def test_redirects_to_periods_when_you_stopped_smoking_as_a_current_smoker_if_change_query_param_is_true(self):
        self.response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set, current_smoker=True
        )

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(
            response,
            reverse("questions:periods_when_you_stopped_smoking", query={"change": "True"})
        )


    def test_redirects_to_when_you_quit_smoking_as_a_former_smoker(self):
        self.response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True
        )

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:when_you_quit_smoking"))


    def test_redirects_to_when_you_quit_smoking_as_a_former_smoker_if_change_query_param_is_true(self):
        self.response_set.have_you_ever_smoked_response.delete()
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True
        )

        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(
            response,
            reverse("questions:when_you_quit_smoking", query={"change": "True"})
        )


    def test_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:age_when_started_smoking"),
            {"value": "not a valid age"}
        )

        self.assertEqual(response.status_code, 422)
