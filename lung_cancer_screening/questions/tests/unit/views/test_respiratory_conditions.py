from django.test import TestCase
from django.urls import reverse

from .helpers.authentication import login_user


class TestRespiratoryConditions(TestCase):
    def setUp(self):
        self.user = login_user(self.client)

        self.user.responseset_set.create()
        self.valid_params = {"respiratory_conditions": ["P", "E"]}


    def test_get_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse("questions:respiratory_conditions")
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/respiratory-conditions", fetch_redirect_response=False)


    def test_get_responds_successfully(self):
        response = self.client.get(reverse("questions:respiratory_conditions"))
        self.assertEqual(response.status_code, 200)

    def test_get_contains_the_correct_form_fields(self):
        response = self.client.get(reverse("questions:respiratory_conditions"))
        self.assertContains(response, "Have you ever been diagnosed with any of the following respiratory conditions?")
        self.assertContains(response, "Pneumonia")
        self.assertContains(response, "Emphysema")
        self.assertContains(response, "Bronchitis")
        self.assertContains(response, "Tuberculosis (TB)")
        self.assertContains(response, "Chronic obstructive pulmonary disease (COPD)")
        self.assertContains(response, "No, I have not had any of these respiratory conditions")

    def test_post_redirects_if_the_user_is_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertRedirects(response, "/oidc/authenticate/?next=/respiratory-conditions", fetch_redirect_response=False)


    def test_post_stores_a_valid_response_for_the_user(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            response_set.respiratory_conditions,
            self.valid_params["respiratory_conditions"]
        )
        self.assertEqual(response_set.user, self.user)

    def test_post_stores_single_selection(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["N"]}
        )

        response_set = self.user.responseset_set.first()
        self.assertEqual(
            response_set.respiratory_conditions,
            ["N"]
        )

    def test_post_redirects_to_the_next_page(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            self.valid_params
        )

        self.assertEqual(response.status_code, 302)

    def test_post_responds_with_422_if_the_response_fails_to_create(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_responds_with_422_if_no_selection_is_made(self):
        response = self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": []}
        )

        self.assertEqual(response.status_code, 422)

    def test_post_does_not_update_response_set_on_invalid_data(self):
        self.client.post(
            reverse("questions:respiratory_conditions"),
            {"respiratory_conditions": ["INVALID"]}
        )

        self.assertEqual(
            self.user.responseset_set.first().respiratory_conditions,
            None
        )
