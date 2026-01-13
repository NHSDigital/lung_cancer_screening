from django.test import TestCase
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.respiratory_conditions_response import RespiratoryConditionsResponse


class TestGetRespiratoryConditions(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/respiratory-conditions",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )
        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )
        self.assertContains(
            response,
            "Have you ever been diagnosed with any of the following "
            "respiratory conditions?"
        )
        self.assertContains(response, "Pneumonia")
        self.assertContains(response, "Emphysema")
        self.assertContains(response, "Bronchitis")
        self.assertContains(response, "Tuberculosis (TB)")
        self.assertContains(
            response, "Chronic obstructive pulmonary disease (COPD)"
        )
        self.assertContains(
            response,
            "No, I have not had any of these respiratory conditions"
        )


class TestPostRespiratoryConditions(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": ["P", "E"]}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/respiratory-conditions",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            RespiratoryConditionsResponse.objects.get(response_set=response_set).value,
            self.valid_params["value"]
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            RespiratoryConditionsResponse.objects.get(response_set=response_set).value,
            self.valid_params["value"]
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_submitted_exists_over_year_ago(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            RespiratoryConditionsResponse.objects.get(response_set=response_set).value,
            self.valid_params["value"]
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            RespiratoryConditionsResponse.objects.get(response_set=response_set).value,
            self.valid_params["value"]
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_stores_single_selection(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"value": ["N"]}
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            RespiratoryConditionsResponse.objects.get(response_set=response_set).value,
            ["N"]
        )

    def test_post_redirects_to_asbestos_exposure(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:asbestos_exposure"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_responds_with_422_if_no_selection_is_made(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"value": []}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        response_set = self.user.responseset_set.first()
        if response_set:
            self.assertFalse(RespiratoryConditionsResponse.objects.filter(response_set=response_set).exists())
