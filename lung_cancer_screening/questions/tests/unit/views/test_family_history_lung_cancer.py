from django.test import TestCase, tag
from django.urls import reverse

from lung_cancer_screening.questions.models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
from ...factories.response_set_factory import ResponseSetFactory
from .helpers.authentication import login_user


@tag("FamilyHistoryLungCancer")
class TestGetFamilyHistoryLungCancer(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/family-history-lung-cancer",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertEqual(response.status_code, 200)


@tag("FamilyHistoryLungCancer")
class TestPostFamilyHistoryLungCancer(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": FamilyHistoryLungCancerValues.NO}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/family-history-lung-cancer",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:family_history_lung_cancer")
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:family_history_lung_cancer")
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_not_recently_submitted_exists(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )

        self.client.post(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_post_redirects_to_responses_path(self):
        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_redirects_to_responses_path_when_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_redirects_to_relatives_age_when_diagnosed_path_when_response_is_yes(self):
        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {"value": FamilyHistoryLungCancerValues.YES}
        )

        self.assertRedirects(response, reverse("questions:relatives_age_when_diagnosed"))

    def test_post_redirects_to_relatives_age_when_diagnosed_path_with_query_params_when_response_is_yes_and_change_true(self):
        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {
                "value": FamilyHistoryLungCancerValues.YES,
                "change": "True"
            }
        )

        self.assertRedirects(
            response,
            reverse(
                "questions:relatives_age_when_diagnosed",
                query={"change": "True"}
            )
        )
