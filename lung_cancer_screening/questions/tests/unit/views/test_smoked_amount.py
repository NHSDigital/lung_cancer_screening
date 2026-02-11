from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ....models.smoking_frequency_response import SmokingFrequencyValues

@tag("SmokedAmount")
class TestGetSmokedAmount(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES
        )
        self.frequency_response = SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

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
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user)

        response = self.client.get(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_404_when_a_smoking_history_item_does_not_exist_for_the_given_type(self):
        self.smoking_history.delete()

        response = self.client.get(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertEqual(response.status_code, 404)


    def test_redirects_when_the_smoking_history_item_does_not_have_a_smoking_frequency_response(self):
        self.frequency_response.delete()

        response = self.client.get(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))

        self.assertEqual(response.status_code, 200)


@tag("SmokedAmount")
class TestPostSmokedAmount(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES
        )
        self.frequency_response = SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

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
        self.smoking_history.delete()

        response = self.client.post(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        self.assertEqual(response.status_code, 404)



    def test_redirects_when_the_smoking_history_item_does_not_have_a_smoking_frequency_response(self):
        self.frequency_response.delete()

        response = self.client.post(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))


    def test_creates_a_smoked_amount_response(self):
        self.client.post(reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), self.valid_params)

        self.smoking_history.refresh_from_db()
        self.assertEqual(
            self.smoking_history.smoked_amount_response.value, self.valid_params["value"]
        )

    def test_redirects_to_next_question(self):
        response = self.client.post(
            reverse("questions:smoked_amount", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:smoking_change", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }))


    def test_redirects_to_next_question_forwarding_the_change_query_param(self):
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
            reverse("questions:smoking_change", kwargs={
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }, query={"change": "True"}),
            fetch_redirect_response=False,
        )
