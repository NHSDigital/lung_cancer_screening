from django.test import TestCase, tag
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .helpers.authentication import login_user


@tag("CancerDiagnosis")
class TestGetCancerDiagnosis(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:cancer_diagnosis")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cancer-diagnosis",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:cancer_diagnosis")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:cancer_diagnosis"))

        self.assertEqual(response.status_code, 200)


@tag("CancerDiagnosis")
class TestPostCancerDiagnosis(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": True}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:cancer_diagnosis"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/cancer-diagnosis",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:cancer_diagnosis")
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:cancer_diagnosis")
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
            reverse("questions:cancer_diagnosis")
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
            reverse("questions:cancer_diagnosis")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_post_redirects_to_family_history_lung_cancer(self):
        response = self.client.post(
            reverse("questions:cancer_diagnosis"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:family_history_lung_cancer"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:cancer_diagnosis"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))
