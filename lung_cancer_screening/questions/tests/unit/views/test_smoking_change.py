from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.tobacco_smoking_history import (
    TobaccoSmokingHistoryTypes,
    TobaccoSmokingHistory,
)
from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory


@tag("SmokingChange")
class TestGetSmokingChange(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, complete=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            complete=True
        )


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse("questions:smoking_change", kwargs={"tobacco_type": "cigarettes"})
        )
        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cigarettes-smoking-change",
            fetch_redirect_response=False,
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.get(
            reverse(
                "questions:smoking_change",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            )
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse(
                "questions:smoking_change",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            )
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_redirects_to_smoking_frequency_when_does_not_have_a_smoking_frequency_response(
        self,
    ):
        self.tobacco_smoking_history.smoking_frequency_response.delete()

        response = self.client.get(
            reverse(
                "questions:smoking_change",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:smoked_amount",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            ),
            fetch_redirect_response=False,
        )

    def test_redirects_to_smoked_amount_when_does_not_have_a__smoked_amount_response(self):
        self.tobacco_smoking_history.smoked_amount_response.delete()

        response = self.client.get(
            reverse(
                "questions:smoking_change",
                kwargs={
                    "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
                },
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:smoked_amount",
                kwargs={"tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()}
            ),
            fetch_redirect_response=False
        )

    def test_responds_successfully(self):
        response = self.client.get(
            reverse("questions:smoking_change", kwargs={"tobacco_type": "cigarettes"})
        )

        self.assertEqual(response.status_code, 200)


@tag("SmokingChange")
class TestPostSmokingChange(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, complete=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            complete=True
        )
        self.valid_params = {
            "value": [TobaccoSmokingHistory.Levels.NO_CHANGE],
        }


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoking_change", kwargs={"tobacco_type": "cigarettes"}),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/cigarettes-smoking-change", fetch_redirect_response=False)


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_redirects_to_the_next_question_given_no_level(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_redirects_to_the_next_question_given_level_increased(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {"value": [TobaccoSmokingHistory.Levels.INCREASED]}
        )

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
            "level": TobaccoSmokingHistory.Levels.INCREASED.value.lower()
        }))


    def test_redirects_to_the_next_question_given_level_decreased_only(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {"value": [TobaccoSmokingHistory.Levels.DECREASED]}
        )

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower(),
            "level": TobaccoSmokingHistory.Levels.DECREASED.value.lower()
        }))


    def test_creates_a_smoking_change_response(self):
        self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            self.valid_params
        )

        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 2)
        self.assertEqual(self.response_set.tobacco_smoking_history.last().level, TobaccoSmokingHistory.Levels.NO_CHANGE)


    def test_creates_a_smoking_change_response_for_increased_and_decreased(self):
        self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": TobaccoSmokingHistoryTypes.CIGARETTES.value.lower()
            }),
            {"value": [TobaccoSmokingHistory.Levels.INCREASED, TobaccoSmokingHistory.Levels.DECREASED]}
        )

        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 3)

        smoking_history_levels = self.response_set.tobacco_smoking_history.all().values_list("level", flat=True)
        self.assertIn(TobaccoSmokingHistory.Levels.INCREASED, smoking_history_levels)
        self.assertIn(TobaccoSmokingHistory.Levels.DECREASED, smoking_history_levels)
        self.assertIn(TobaccoSmokingHistory.Levels.NORMAL, smoking_history_levels)
