from django.test import TestCase, tag
from django.urls import reverse

from lung_cancer_screening.questions.models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedValues
from lung_cancer_screening.questions.tests.factories.family_history_lung_cancer_response_factory import FamilyHistoryLungCancerResponseFactory
from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues

from .helpers.authentication import login_user


@tag("RelativesAgeWhenDiagnosed")
class TestGetRelativesAgeWhenDiagnosed(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/relatives-age-when-diagnosed",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_responds_successfully(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=ResponseSetFactory.create(user=self.user, eligible=True),
            value=FamilyHistoryLungCancerValues.YES
        )

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )
        self.assertEqual(response.status_code, 200)

    def test_responds_redirect_for_no_family_history(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=ResponseSetFactory.create(user=self.user, eligible=True),
            value=FamilyHistoryLungCancerValues.NO
        )

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(
            response,
            reverse("questions:family_history_lung_cancer"),
            fetch_redirect_response=False
        )


@tag("RelativesAgeWhenDiagnosed")
class TestPostRelativesAgeWhenDiagnosed(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": RelativesAgeWhenDiagnosedValues.NO}

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/relatives-age-when-diagnosed",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_creates_a_relatives_age_when_diagnosed_response(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        FamilyHistoryLungCancerResponseFactory(
            response_set=response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        self.client.post(reverse("questions:relatives_age_when_diagnosed"), self.valid_params)

        response_set.refresh_from_db()
        self.assertEqual(
            response_set.relatives_age_when_diagnosed.value, self.valid_params["value"]
        )

    def test_redirects_to_responses(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        FamilyHistoryLungCancerResponseFactory(
            response_set=response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:age_when_started_smoking"))

    def test_redirects_to_responses_if_change_query_param_is_true(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        FamilyHistoryLungCancerResponseFactory(
            response_set=response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))
