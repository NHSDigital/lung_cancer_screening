from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user


class TestAsbestosExposure(TestCase):
    def setUp(self):
        self.user = login_user(self.client)
        self.user.responseset_set.create()

        self.valid_params = {"asbestos_exposure": True}

    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:asbestos_exposure")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/asbestos-exposure", fetch_redirect_response=False)

    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:asbestos_exposure"))

        self.assertContains(response, "Have you ever worked in a job where you might have been exposed to asbestos?")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/asbestos-exposure", fetch_redirect_response=False)

    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            response_set.asbestos_exposure,
            self.valid_params["asbestos_exposure"]
        )
        self.assertEqual(response_set.user, self.user)


    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            self.valid_params
        )

        # Assuming it redirects to the next question page - adjust as needed
        self.assertEqual(response.status_code, 302)

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:asbestos_exposure"),
            {"asbestos_exposure": "something not in list"}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:asbestos_exposure"),
            {"asbestos_exposure": "invalid"}
        )

        self.assertEqual(
            self.user.responseset_set.first().asbestos_exposure,
            None
        )
