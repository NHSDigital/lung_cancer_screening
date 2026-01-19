from django.test import TestCase, tag
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from lung_cancer_screening.questions.models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedValues
from lung_cancer_screening.questions.tests.factories.family_history_lung_cancer_response_factory import FamilyHistoryLungCancerResponseFactory
from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues

from .helpers.authentication import login_user


@tag("RelativesAgeWhenDiagnosed")
class TestGetRelativesAgeWhenDiagnosed(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/relatives-age-when-diagnosed",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=ResponseSetFactory.create(user=self.user),
            value=FamilyHistoryLungCancerValues.YES
        )

        response = self.client.get(
            reverse("questions:relatives_age_when_diagnosed")
        )
        self.assertEqual(response.status_code, 200)

    def test_get_responds_redirect_for_no_family_history(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=ResponseSetFactory.create(user=self.user),
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

    def test_post_redirects_if_the_user_is_not_logged_in(self):
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

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:relatives_age_when_diagnosed")
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:relatives_age_when_diagnosed")
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_submitted_exists_over_year_ago(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_redirects_to_responses(self):
        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:relatives_age_when_diagnosed"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))
