from django.test import TestCase, tag
from django.urls import reverse
from inflection import dasherize

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from lung_cancer_screening.questions.tests.factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory


@tag("SmokingCurrent")
class TestGetSmokingCurrent(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/cigarettes-smoking-current", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }))

        self.assertEqual(response.status_code, 200)


@tag("SmokingCurrent")
class TestPostSmokingCurrent(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        self.valid_params = {"value": True}


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoking_current", kwargs={"tobacco_type": "cigarettes"}),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/cigarettes-smoking-current", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_creates_a_smoking_current_response(self):
        self.client.post(reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }), self.valid_params)

        self.tobacco_smoking_history.refresh_from_db()
        self.assertEqual(
            self.tobacco_smoking_history.smoking_current_response.value, self.valid_params["value"]
        )

    def test_redirects_to_next_question(self):
        response = self.client.post(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:smoked_total_years", kwargs={
            "tobacco_type": dasherize(TobaccoSmokingHistoryTypes.CIGARETTES.value).lower()
        }), fetch_redirect_response=False)


    def test_redirects_to_next_question_forwarding_the_change_query_param(self):
        response = self.client.post(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:smoked_total_years",
            kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            },
            query={"change": "True"}
        ), fetch_redirect_response=False)


    def test_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:smoking_current", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
