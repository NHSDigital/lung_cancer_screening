
from django.test import TestCase, tag
from django.urls import reverse

from ....models.smoking_frequency_response import SmokingFrequencyValues
from ....models.tobacco_smoking_history import TobaccoSmokingHistory, TobaccoSmokingHistoryTypes
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from .helpers.authentication import login_user
from ...factories.response_set_factory import ResponseSetFactory


@tag("SmokingFrequency")
class TestGetSmokingFrequency(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            complete=True
        )


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/cigarettes-smoking-frequency", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            })
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_responds_successfully(self):
        response = self.client.get(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }))

        self.assertEqual(response.status_code, 200)

    def test_back_link_normal_level(self):
        response = self.client.get(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }))

        self.assertEqual(
            response.context_data["back_link_url"],
            "/cigarettes-smoked-total-years",
        )

    def test_back_link_increased_level(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )

        response = self.client.get(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
                "level": TobaccoSmokingHistory.Levels.INCREASED.value.lower()
            }))

        self.assertEqual(
            response.context_data["back_link_url"],
            "/cigarettes-smoking-change"
        )

    def test_back_link_decreased_level_with_increased_level_present(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )

        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.DECREASED
        )

        response = self.client.get(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
                "level": TobaccoSmokingHistory.Levels.DECREASED.value.lower()
            }))

        self.assertEqual(
            response.context_data["back_link_url"],
            "/cigarettes-smoked-increased-amount"
        )

    def test_back_link_decreased_level_without_increased_level_present(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.DECREASED
        )

        response = self.client.get(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
                "level": TobaccoSmokingHistory.Levels.DECREASED.value.lower()
            }))

        self.assertEqual(
            response.context_data["back_link_url"],
            "/cigarettes-smoking-change"
        )


@tag("SmokingFrequency")
class TestPostSmokingFrequency(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            complete=True
        )

        self.valid_params = {"value": SmokingFrequencyValues.DAILY.value}


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoking_frequency", kwargs={"tobacco_type": "cigarettes"}),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/cigarettes-smoking-frequency", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_creates_a_smoking_frequency_response(self):
        self.client.post(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }), self.valid_params)

        self.tobacco_smoking_history.refresh_from_db()
        self.assertEqual(
            self.tobacco_smoking_history.smoking_frequency_response.value, self.valid_params["value"]
        )

    def test_creates_a_smoking_frequency_response_when_given_a_level(self):
        increased_level = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )
        self.client.post(reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
                "level": TobaccoSmokingHistory.Levels.INCREASED.value.lower()
            }), self.valid_params)

        increased_level.refresh_from_db()
        self.assertEqual(
            increased_level.smoking_frequency_response.value, self.valid_params["value"]
        )


    def test_redirects_to_next_question(self):
        response = self.client.post(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
        }), fetch_redirect_response=False)


    def test_redirects_to_next_question_when_given_a_level(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )
        response = self.client.post(
            reverse("questions:smoking_frequency", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
                "level": TobaccoSmokingHistory.Levels.INCREASED
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:smoked_amount", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
            "level": TobaccoSmokingHistory.Levels.INCREASED
        }),
        fetch_redirect_response=False)

    def test_redirects_to_next_question_forwarding_the_change_query_param(self):
        response = self.client.post(
            reverse(
                "questions:smoking_frequency",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            ),
            {**self.valid_params, "change": "True"},
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:smoked_amount",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
                query={"change": "True"},
            ),
            fetch_redirect_response=False,
        )
