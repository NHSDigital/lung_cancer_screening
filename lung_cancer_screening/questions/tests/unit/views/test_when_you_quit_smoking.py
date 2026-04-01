from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory


@tag("WhenYouQuitSmoking")
class TestGetWhenYouQuitSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory(
            response_set=self.response_set,
            value=self.response_set.date_of_birth_response.age_in_years() - 20,
        )

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/when-you-quit-smoking",
            fetch_redirect_response=False,
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertRedirects(response, reverse("questions:agree_terms_of_use"))


    def test_redirects_to_age_started_smoking_if_the_user_has_not_answered_age_started_smoking(self):
        self.age_when_started_smoking_response.delete()

        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertRedirects(response, reverse("questions:age_when_started_smoking"))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertEqual(response.status_code, 200)


    def test_has_a_back_link_to_age_started_smoking(self):
        response = self.client.get(reverse("questions:when_you_quit_smoking"))

        self.assertEqual(
            response.context_data["back_link_url"],
            reverse("questions:age_when_started_smoking"),
        )

    def test_has_a_back_link_when_change_is_true(self):
        response = self.client.get(
            reverse("questions:when_you_quit_smoking"),
            {"change": "True"}
        )

        self.assertEqual(
            response.context_data["back_link_url"],
            reverse("questions:responses")
        )


@tag("WhenYouQuitSmoking")
class TestPostWhenYouQuitSmoking(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory(
            response_set=self.response_set,
            value=self.response_set.date_of_birth_response.age_in_years() - 20,
        )

        self.valid_params = {"value": 18}

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:when_you_quit_smoking"), self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/when-you-quit-smoking",
            fetch_redirect_response=False,
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.post(
            reverse("questions:when_you_quit_smoking"), self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(
            reverse("questions:when_you_quit_smoking"), self.valid_params
        )

        self.assertRedirects(response, reverse("questions:agree_terms_of_use"))


    def test_creates_an_when_you_quit_smoking_response(self):
        self.client.post(
            reverse("questions:when_you_quit_smoking"), self.valid_params
        )

        self.response_set.refresh_from_db()
        self.assertEqual(
            self.response_set.when_you_quit_smoking_response.value,
            self.valid_params["value"],
        )

    def test_redirects_to_periods_when_you_stopped_smoking(self):
        response = self.client.post(
            reverse("questions:when_you_quit_smoking"), self.valid_params
        )

        self.assertRedirects(
            response, reverse("questions:periods_when_you_stopped_smoking")
        )


    def test_redirects_to_periods_when_you_stopped_smoking_if_change_query_param_is_true(
        self,
    ):
        response = self.client.post(
            reverse("questions:when_you_quit_smoking"),
            {**self.valid_params, "change": "True"},
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:periods_when_you_stopped_smoking", query={"change": "True"}
            ),
        )

    def test_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:when_you_quit_smoking"), {"value": "not a valid age"}
        )

        self.assertEqual(response.status_code, 422)
