from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user


class TestHeight(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.user.responseset_set.create()

        self.valid_height = 170
        self.valid_params = {"height": self.valid_height}
        self.invalid_height = 80000


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:height")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/height", fetch_redirect_response=False)


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:height"))

        self.assertEqual(response.status_code, 200)

    def test_get_renders_the_metric_form_by_default(self):
        response = self.client.get(reverse("questions:height"))

        self.assertContains(response, "Centimetres")

    def test_get_renders_the_imperial_form_if_specified(self):
        response = self.client.get(reverse("questions:height"), {"unit": "imperial"})

        self.assertContains(response, "Feet")
        self.assertContains(response, "Inches")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/height", fetch_redirect_response=False)


    def test_post_stores_a_valid_response_set_for_the_user(self):
        self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()

        self.assertEqual(response_set.height, self.valid_height*10)
        self.assertEqual(response_set.user, self.user)

    def test_post_redirects_to_weight_path(self):
        response = self.client.post(
            reverse("questions:height"),
            self.valid_params
        )

        self.assertRedirects(response, reverse("questions:weight"))

    def test_post_responds_with_422_if_the_resource_is_invalid(self):
        response = self.client.post(
            reverse("questions:height"),
            {"height": "a"}
        )

        self.assertEqual(response.status_code, 422)
