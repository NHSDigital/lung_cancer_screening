from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory


@tag("SmokedAmount")
class TestGetSmokedAmount(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cigarettes-smoked-amount",
            fetch_redirect_response=False
        )

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_404_when_a_smoking_history_item_does_not_exist_for_the_given_type(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertEqual(response.status_code, 404)

    def test_responds_successfully(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        TobaccoSmokingHistoryFactory.create(
            response_set=response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.get(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertEqual(response.status_code, 200)


@tag("SmokedAmount")
class TestPostSmokedAmount(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.valid_params = {"value": 20}

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cigarettes-smoked-amount",
            fetch_redirect_response=False
        )

    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_404_when_a_smoking_history_item_does_not_exist_for_the_given_type(self):
        response = self.client.post(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        self.assertEqual(response.status_code, 404)

    def test_creates_a_smoked_amount_response(self):
        smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        self.client.post(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        smoking_history.refresh_from_db()
        self.assertEqual(
            smoking_history.smoked_amount_response.value, self.valid_params["value"]
        )

    def test_redirects_to_responses(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.post(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_redirects_to_next_question_forwarding_the_change_query_param(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

        response = self.client.post(
            reverse(
                "questions:smoked_amount",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            ),
            {**self.valid_params, "change": "True"},
        )

        self.assertRedirects(
            response,
            reverse("questions:responses"),
            fetch_redirect_response=False,
        )
