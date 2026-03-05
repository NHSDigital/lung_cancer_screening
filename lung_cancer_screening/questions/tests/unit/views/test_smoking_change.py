from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.tobacco_smoking_history import (
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
            complete=True,
        )


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse("questions:smoking_change", kwargs={
                "tobacco_type": self.tobacco_smoking_history.url_type()
            })
        )
        self.assertRedirects(
            response,
            f"/oidc/authenticate/?next=/{self.tobacco_smoking_history.url_type()}-smoking-change",
            fetch_redirect_response=False,
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, recently_submitted=True)

        response = self.client.get(
            reverse(
                "questions:smoking_change",
                kwargs={
                    "tobacco_type": self.tobacco_smoking_history.url_type()
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
                    "tobacco_type": self.tobacco_smoking_history.url_type()
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
                    "tobacco_type": self.tobacco_smoking_history.url_type()
                },
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:smoked_amount",
                kwargs={
                    "tobacco_type": self.tobacco_smoking_history.url_type()
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
                    "tobacco_type": self.tobacco_smoking_history.url_type()
                },
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:smoked_amount",
                kwargs={
                    "tobacco_type": self.tobacco_smoking_history.url_type()
                }
            ),
            fetch_redirect_response=False
        )

    def test_responds_successfully(self):
        response = self.client.get(
            reverse("questions:smoking_change", kwargs={
                "tobacco_type": self.tobacco_smoking_history.url_type()
            })
        )

        self.assertEqual(response.status_code, 200)


@tag("SmokingChange")
class TestPostSmokingChange(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.response_set = ResponseSetFactory.create(user=self.user, complete=True)
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            rolling_tobacco=True,
            complete=True
        )
        self.valid_params = {
            "value": [TobaccoSmokingHistory.Levels.NO_CHANGE],
        }


    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:smoking_change", kwargs={
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            self.valid_params
        )

        self.assertRedirects(
            response,
            f"/oidc/authenticate/?next=/{self.tobacco_smoking_history.url_type()}-smoking-change", fetch_redirect_response=False
        )


    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        self.response_set.delete()
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        self.response_set.delete()
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_redirects_to_the_next_question_given_no_level(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))


    def test_redirects_to_the_next_question_given_level_increased(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            {"value": [TobaccoSmokingHistory.Levels.INCREASED]}
        )

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": self.tobacco_smoking_history.url_type(),
            "level": TobaccoSmokingHistory.Levels.INCREASED.value.lower()
        }))


    def test_redirects_to_the_next_question_given_level_decreased_only(self):
        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            {"value": [TobaccoSmokingHistory.Levels.DECREASED]}
        )

        self.assertRedirects(response, reverse("questions:smoking_frequency", kwargs={
            "tobacco_type": self.tobacco_smoking_history.url_type(),
            "level": TobaccoSmokingHistory.Levels.DECREASED.value.lower()
        }))


    def test_does_not_redirect_to_increased_if_increased_exists_for_another_type_and_is_not_selected(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=self.tobacco_smoking_history.type,
            complete=True,
            increased=True,
        )
        medium_cigars = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            medium_cigars=True,
            complete=True
        )

        response = self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": medium_cigars.url_type()
            }),
            {"value": [TobaccoSmokingHistory.Levels.NO_CHANGE]}
        )

        self.assertRedirects(response, reverse("questions:responses"),
            fetch_redirect_response=False
        )


    def test_creates_a_smoking_change_response(self):
        self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            self.valid_params
        )

        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 2)
        self.assertEqual(self.response_set.tobacco_smoking_history.last().level, TobaccoSmokingHistory.Levels.NO_CHANGE)


    def test_creates_a_smoking_change_response_for_increased_and_decreased(self):
        self.client.post(
            reverse("questions:smoking_change", kwargs = {
                "tobacco_type": self.tobacco_smoking_history.url_type()
            }),
            {"value": [TobaccoSmokingHistory.Levels.INCREASED, TobaccoSmokingHistory.Levels.DECREASED]}
        )

        self.assertEqual(self.response_set.tobacco_smoking_history.count(), 3)

        smoking_history_levels = self.response_set.tobacco_smoking_history.all().values_list("level", flat=True)
        self.assertIn(TobaccoSmokingHistory.Levels.INCREASED, smoking_history_levels)
        self.assertIn(TobaccoSmokingHistory.Levels.DECREASED, smoking_history_levels)
        self.assertIn(TobaccoSmokingHistory.Levels.NORMAL, smoking_history_levels)
