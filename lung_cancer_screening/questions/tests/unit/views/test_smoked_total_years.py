from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory


@tag("SmokedTotalYears")
class TestGetSmokedTotalYears(TestCase):
    def setUp(self):
        self.user = login_user(self.client)


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cigarettes-smoked-total-years",
            fetch_redirect_response=False
        )


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_404_when_a_smoking_history_item_does_not_exist_for_the_given_type(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:smoked_total_years", kwargs = {
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertEqual(response.status_code, 404)


    def test_responds_successfully(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.get(reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertEqual(response.status_code, 200)


@tag("SmokedTotalYears")
class TestPostSmokedTotalYears(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": 10}

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cigarettes-smoked-total-years",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_404_when_a_smoking_history_item_does_not_exist_for_the_given_type(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(reverse("questions:smoked_total_years", kwargs = {
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        self.assertEqual(response.status_code, 404)


    def test_creates_a_smoked_total_years_response(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        self.client.post(reverse("questions:smoked_total_years", kwargs = {
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        smoking_history.refresh_from_db()
        self.assertEqual(
            smoking_history.smoked_total_years_response.value, self.valid_params["value"]
        )

    def test_redirects_to_next_question(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_redirects_to_responses_if_change_query_param_is_true(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_responds_with_422_if_the_response_fails_to_create(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.post(
            reverse("questions:smoked_total_years", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
