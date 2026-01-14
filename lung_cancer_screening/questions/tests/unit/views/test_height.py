from django.test import TestCase, tag
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.height_response import HeightResponse


@tag("Height")
class TestGetHeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/height",
            fetch_redirect_response=False
        )

    def test_get_redirects_when_submitted_response_set_exists_within_last_year(
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:height"))

        self.assertEqual(response.status_code, 200)

    def test_get_renders_the_metric_form_by_default(self):
        response = self.client.get(reverse("questions:height"))

        self.assertContains(response, "Centimetres")

    def test_get_renders_the_imperial_form_if_already_has_imperial_height(self):
        response_set = self.user.responseset_set.create()
        HeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:height"))

        self.assertContains(response, "Feet")

    def test_get_renders_the_metric_form_if_already_has_imperial_height_but_unit_is_metric(self):
        response_set = self.user.responseset_set.create()
        HeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:height"), {"unit": "metric"})

        self.assertContains(response, "Centimetres")

    def test_get_renders_the_imperial_form_if_specified(self):
        response = self.client.get(
            reverse("questions:height"), {"unit": "imperial"}
        )

        self.assertContains(response, "Feet")
        self.assertContains(response, "Inches")


@tag("Height")
class TestPostHeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_height_metric = 170
        self.valid_params = {"metric": self.valid_height_metric}
        self.invalid_height = 80000

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/height",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HeightResponse.objects.get(response_set=response_set).metric, self.valid_height_metric * 10)
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HeightResponse.objects.get(response_set=response_set).metric, self.valid_height_metric * 10)
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_submitted_exists_over_year_ago(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(years=1)
        )

        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(HeightResponse.objects.get(response_set=response_set).metric, self.valid_height_metric * 10)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(  # noqa: E501
        self
    ):
        self.user.responseset_set.create(
            submitted_at=timezone.now() - relativedelta(days=364)
        )

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:start"))

    def test_post_stores_a_valid_response_set_for_the_user(self):
        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()

        self.assertEqual(HeightResponse.objects.get(response_set=response_set).metric, self.valid_height_metric * 10)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_to_weight(self):
        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:weight"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:height"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:height"),
            {"metric": "a"}
        )

        self.assertEqual(response.status_code, 422)
