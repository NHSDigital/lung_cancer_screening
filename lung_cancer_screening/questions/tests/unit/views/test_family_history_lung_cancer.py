from django.test import TestCase, tag
from django.urls import reverse

from lung_cancer_screening.questions.models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
from ...factories.response_set_factory import ResponseSetFactory
from .helpers.authentication import login_user


@tag("FamilyHistoryLungCancer")
class TestGetFamilyHistoryLungCancer(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/family-history-lung-cancer",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(
            reverse("questions:family_history_lung_cancer")
        )

        self.assertEqual(response.status_code, 200)


@tag("FamilyHistoryLungCancer")
class TestPostFamilyHistoryLungCancer(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": FamilyHistoryLungCancerValues.NO}

    def test_redirects_if_the_user_is_not_logged_in(self):
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

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))


    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))


    def test_creates_a_family_history_lung_cancer_response(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        self.client.post(reverse("questions:family_history_lung_cancer"), self.valid_params)

        response_set.refresh_from_db()
        self.assertEqual(
            response_set.family_history_lung_cancer.value, self.valid_params["value"]
        )

    def test_redirects_to_age_when_started_smoking_when_response_is_no(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            { "value": FamilyHistoryLungCancerValues.NO }
        )

        self.assertRedirects(response, reverse("questions:age_when_started_smoking"))


    def test_redirects_to_age_when_diagnosed_when_response_is_yes(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            { "value": FamilyHistoryLungCancerValues.YES }
        )

        self.assertRedirects(
            response, reverse("questions:relatives_age_when_diagnosed")
        )


    def test_redirects_to_responses_path_when_change_query_param_is_true_an_response_is_no(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {
                "value": FamilyHistoryLungCancerValues.NO,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_redirects_to_responses_path_when_change_query_param_is_true_an_response_is_yes(
        self,
    ):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {
                "value": FamilyHistoryLungCancerValues.YES,
                "change": "True"
            }
        )

        self.assertRedirects(
            response,
            reverse("questions:relatives_age_when_diagnosed", query={"change": "True"}),
        )

    def test_responds_with_422_if_the_response_fails_to_create(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:family_history_lung_cancer"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)
