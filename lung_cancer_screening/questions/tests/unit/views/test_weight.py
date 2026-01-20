from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.weight_response import WeightResponse
from ...factories.response_set_factory import ResponseSetFactory


@tag("Weight")
class TestGetWeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:weight")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/weight",
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
            reverse("questions:weight")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:weight"))

        self.assertEqual(response.status_code, 200)

    def test_get_renders_the_metric_form(self):
        response = self.client.get(reverse("questions:weight"))

        self.assertContains(response, "Kilograms")

    def test_get_renders_the_imperial_form_if_already_has_imperial_weight(self):
        response_set = self.user.responseset_set.create()
        WeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:weight"))

        self.assertContains(response, "Stone")

    def test_get_renders_the_metric_form_if_already_has_imperial_weight_but_unit_is_metric(self):
        response_set = self.user.responseset_set.create()
        WeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:weight"), {"unit": "metric"})

        self.assertContains(response, "Kilograms")

    def test_get_renders_the_imperial_form_if_specified(self):
        response = self.client.get(
            reverse("questions:weight"), {"unit": "imperial"}
        )

        self.assertContains(response, "Stone")
        self.assertContains(response, "Pounds")


@tag("Weight")
class TestPostWeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.valid_weight = 70
        self.valid_params = {"metric": self.valid_weight}

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/weight",
            fetch_redirect_response=False
        )

    def test_post_creates_unsubmitted_response_set_when_no_response_set_exists(
        self
    ):
        self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            WeightResponse.objects.get(response_set=response_set).metric, self.valid_weight * 10
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_updates_unsubmitted_response_set_when_one_exists(self):
        response_set = self.user.responseset_set.create()

        self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        response_set.refresh_from_db()
        self.assertEqual(self.user.responseset_set.count(), 1)
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            WeightResponse.objects.get(response_set=response_set).metric, self.valid_weight * 10
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_creates_new_unsubmitted_response_set_when_not_recently_submitted_exists(  # noqa: E501
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            not_recently_submitted=True
        )

        self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        self.assertEqual(self.user.responseset_set.count(), 2)
        self.assertEqual(self.user.responseset_set.unsubmitted().count(), 1)

        response_set = self.user.responseset_set.last()
        self.assertEqual(response_set.submitted_at, None)
        self.assertEqual(
            WeightResponse.objects.get(response_set=response_set).metric, self.valid_weight * 10
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_when_submitted_response_set_exists_within_last_year(  # noqa: E501
        self
    ):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_post_redirects_to_sex_at_birth(self):
        response = self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:sex_at_birth"))

    def test_post_redirects_to_responses_if_change_query_param_is_true(self):
        response = self.client.post(
            reverse("questions:weight"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_post_valid_weight_added_to_response_set(self):
        self.client.post(
            reverse("questions:weight"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            WeightResponse.objects.get(response_set=response_set).metric, self.valid_weight * 10
        )

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:weight"),
            {"metric": "not a valid weight"}
        )

        self.assertEqual(response.status_code, 422)
