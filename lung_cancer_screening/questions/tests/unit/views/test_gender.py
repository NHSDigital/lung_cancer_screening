from django.test import TestCase, tag
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from lung_cancer_screening.questions.models.gender_response import GenderResponse, GenderValues
from .helpers.authentication import login_user


@tag("Gender")
class TestGetGender(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:gender")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/gender",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:gender")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:gender"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:gender"))

        self.assertContains(response, "Which of these best describes you?")


@tag("Gender")
class TestPostGender(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_params = {"value": GenderValues.MALE}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/gender",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(GenderResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(GenderResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_submitted_exists_over_year_ago(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(GenderResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(GenderResponse.objects.get(response_set=response_set).value, self.valid_params["value"])
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_to_ethnicity(self):
        response = self.client.post(
            reverse("questions:gender"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:ethnicity"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:gender"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:gender"),
            {"value": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_renders_the_gender_page_with_an_error_if_form_invalid(
        self
    ):
        response = self.client.post(
            reverse("questions:gender"),
            {"value": "something not in list"}
        )

        self.assertContains(
            response, "Which of these best describes you?", status_code=422
        )
        self.assertContains(response, "nhsuk-error-message", status_code=422)
