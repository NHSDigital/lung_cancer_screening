from django.test import TestCase, tag
from django.urls import reverse

from .helpers.authentication import login_user
from lung_cancer_screening.questions.models.height_response import HeightResponse
from ...factories.response_set_factory import ResponseSetFactory


@tag("Height")
class TestGetHeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

    def test_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(
            response,
            "/oidc/authenticate/?next=/height",
            fetch_redirect_response=False
        )

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user, eligible=False)

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_responds_successfully(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:height"))

        self.assertEqual(response.status_code, 200)

    def test_renders_the_metric_form_by_default(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.get(reverse("questions:height"))

        self.assertContains(response, "Centimetres")

    def test_renders_the_imperial_form_if_already_has_imperial_height(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        HeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:height"))

        self.assertContains(response, "Feet")

    def test_renders_the_metric_form_if_already_has_imperial_height_but_unit_is_metric(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)
        HeightResponse.objects.create(response_set=response_set, imperial=60)

        response = self.client.get(reverse("questions:height"), {"unit": "metric"})

        self.assertContains(response, "Centimetres")

    def test_renders_the_imperial_form_if_specified(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

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

    def test_redirects_if_the_user_is_not_logged_in(self):
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

    def test_redirects_when_a_submitted_response_set_exists_within_the_last_year(self):
        ResponseSetFactory.create(
            user=self.user,
            recently_submitted=True
        )

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:confirmation"))

    def test_redirects_when_the_user_is_not_eligible(self):
        ResponseSetFactory.create(user=self.user)

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:have_you_ever_smoked"))

    def test_creates_a_height_response(self):
        response_set = ResponseSetFactory.create(user=self.user, eligible=True)

        self.client.post(reverse("questions:height"), self.valid_params)

        response_set.refresh_from_db()
        self.assertEqual(
            response_set.height_response.metric, self.valid_height_metric * 10
        )

    def test_redirects_to_weight(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:weight"))

    def test_redirects_to_responses_if_change_query_param_is_true(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:height"),
            {
                **self.valid_params,
                "change": "True"
            }
        )

        self.assertRedirects(response, reverse("questions:responses"))

    def test_responds_with_422_if_the_response_fails_to_create(self):
        ResponseSetFactory.create(user=self.user, eligible=True)

        response = self.client.post(
            reverse("questions:height"),
            {"metric": "a"}
        )

        self.assertEqual(response.status_code, 422)
